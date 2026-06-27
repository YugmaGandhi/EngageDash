"""Shared test fixtures.

Tests run against an in-memory SQLite database and a fake (in-memory) Redis,
so they are fast and never touch the real Postgres/Redis services.
"""

import fakeredis
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.db import Base, get_db
from app.core.redis import RedisCache, get_redis
from app.core.security import hash_password
from app.main import app
from app.models.user import User, UserRole

# One in-memory SQLite database shared across the test (StaticPool keeps a single
# connection, so the data created in a test is visible to the API call).
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=test_engine, autoflush=False, expire_on_commit=False)


@pytest.fixture(autouse=True)
def create_tables():
    """Create all tables before each test and drop them after, for isolation."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    """A database session backed by the test database."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    """A TestClient with the DB and Redis dependencies swapped for test doubles."""

    def override_get_db():
        yield db_session

    fake_cache = RedisCache(fakeredis.FakeRedis(decode_responses=True))

    def override_get_redis():
        yield fake_cache

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def create_user(db_session):
    """Factory to insert a user directly (used to set up roles in tests)."""

    def _create_user(email, password="supersecret123", role=UserRole.CSM, name="Test", is_active=True):
        user = User(
            name=name,
            email=email,
            hashed_password=hash_password(password),
            role=role,
            is_active=is_active,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    return _create_user

