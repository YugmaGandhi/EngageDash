"""Critical tests for the dashboard: metrics, caching, invalidation, scoping."""

from datetime import datetime, timezone

import fakeredis

from app.core.redis import RedisCache
from app.models.customer import Customer, CustomerStatus
from app.models.insight import Insight, InsightStatus, Sentiment
from app.models.interaction import Interaction, InteractionType
from app.models.user import UserRole


def auth_headers(client, email, password="supersecret123"):
    token = client.post("/auth/login", json={"email": email, "password": password}).json()[
        "access_token"
    ]
    return {"Authorization": f"Bearer {token}"}


# ---------- Metrics correctness ----------

def test_dashboard_counts(client, create_user):
    create_user("csm@x.com", role=UserRole.CSM)
    headers = auth_headers(client, "csm@x.com")
    client.post("/customers", json={"name": "A", "status": "active"}, headers=headers)
    client.post("/customers", json={"name": "B", "status": "at_risk"}, headers=headers)

    data = client.get("/dashboard", headers=headers).json()
    assert data["total_customers"] == 2
    assert data["customers_by_status"]["at_risk"] == 1
    assert data["at_risk_customers"] == 1


# ---------- Caching ----------

def test_dashboard_cache_hit_serves_stale(client, create_user, db_session):
    user = create_user("csm@x.com", role=UserRole.CSM)
    headers = auth_headers(client, "csm@x.com")
    client.post("/customers", json={"name": "A"}, headers=headers)

    # First read computes and caches (1 customer).
    assert client.get("/dashboard", headers=headers).json()["total_customers"] == 1

    # Insert a customer DIRECTLY (bypassing the API, so the cache is NOT cleared).
    db_session.add(
        Customer(
            name="B",
            status=CustomerStatus.ACTIVE,
            health_score=50,
            assigned_csm_id=user.id,
            created_by_id=user.id,
        )
    )
    db_session.commit()

    # The dashboard still shows the cached value -> proves it was served from cache.
    assert client.get("/dashboard", headers=headers).json()["total_customers"] == 1


def test_dashboard_invalidated_after_create(client, create_user):
    create_user("csm@x.com", role=UserRole.CSM)
    headers = auth_headers(client, "csm@x.com")
    client.post("/customers", json={"name": "A"}, headers=headers)
    assert client.get("/dashboard", headers=headers).json()["total_customers"] == 1

    # Creating through the API clears the cache, so the next read is fresh.
    client.post("/customers", json={"name": "B"}, headers=headers)
    assert client.get("/dashboard", headers=headers).json()["total_customers"] == 2


def test_set_json_applies_ttl():
    cache = RedisCache(fakeredis.FakeRedis(decode_responses=True))
    cache.set_json("dashboard:all", {"total_customers": 3}, ttl=120)
    # A positive TTL means the key is set to expire.
    assert cache._client.ttl("dashboard:all") > 0
    assert cache.get_json("dashboard:all") == {"total_customers": 3}


# ---------- Role scoping ----------

def test_sentiment_breakdown_excludes_fallback_insights(client, create_user, db_session):
    user = create_user("csm@x.com", role=UserRole.CSM)
    headers = auth_headers(client, "csm@x.com")

    # A customer + interaction to attach insights to.
    customer = Customer(
        name="Acme",
        status=CustomerStatus.ACTIVE,
        health_score=50,
        assigned_csm_id=user.id,
        created_by_id=user.id,
    )
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)

    interaction = Interaction(
        customer_id=customer.id,
        created_by_id=user.id,
        type=InteractionType.MEETING,
        title="QBR",
        notes="notes",
        occurred_at=datetime.now(timezone.utc),
    )
    db_session.add(interaction)
    db_session.commit()
    db_session.refresh(interaction)

    # One real (success) neutral insight, and one fallback (also neutral).
    db_session.add_all(
        [
            Insight(
                interaction_id=interaction.id,
                summary="ok",
                sentiment=Sentiment.NEUTRAL,
                action_items=[],
                risks=[],
                status=InsightStatus.SUCCESS,
            ),
            Insight(
                interaction_id=interaction.id,
                summary="fallback",
                sentiment=Sentiment.NEUTRAL,
                action_items=[],
                risks=[],
                status=InsightStatus.FALLBACK,
            ),
        ]
    )
    db_session.commit()

    data = client.get("/dashboard", headers=headers).json()
    # Only the success insight counts — the fallback neutral is excluded.
    assert data["sentiment_breakdown"]["neutral"] == 1


def test_dashboard_role_scoping(client, create_user):
    create_user("csm@x.com", role=UserRole.CSM)
    create_user("admin@x.com", role=UserRole.ADMIN)
    csm_headers = auth_headers(client, "csm@x.com")
    admin_headers = auth_headers(client, "admin@x.com")

    client.post("/customers", json={"name": "CsmOwned"}, headers=csm_headers)
    client.post("/customers", json={"name": "AdminOwned"}, headers=admin_headers)

    # CSM sees only their own; admin sees everything.
    assert client.get("/dashboard", headers=csm_headers).json()["total_customers"] == 1
    assert client.get("/dashboard", headers=admin_headers).json()["total_customers"] == 2
