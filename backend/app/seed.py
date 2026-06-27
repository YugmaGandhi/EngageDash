"""Seed the database with demo data so every feature can be tried out.

Run it after the database is migrated:
    docker compose exec backend python -m app.seed     # when running via Docker
    python -m app.seed                                 # when running locally

It is idempotent: if the demo admin already exists, it does nothing.

Demo logins (all passwords are valid for testing):
    admin@engagedash.com   / Admin@123      (admin   — manages users + everything)
    manager@engagedash.com / Manager@123    (manager — sees all customers, can delete)
    csm@engagedash.com     / Csm@12345      (csm     — only their own customers)
"""

from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from app.core.db import SessionLocal
from app.core.security import hash_password
from app.models.customer import Customer, CustomerStatus
from app.models.insight import Insight, InsightStatus, Sentiment
from app.models.interaction import Interaction, InteractionType
from app.models.user import User, UserRole

ADMIN_EMAIL = "admin@engagedash.com"


def seed() -> None:
    db = SessionLocal()
    try:
        if db.scalar(select(User).where(User.email == ADMIN_EMAIL)):
            print("Demo data already exists — nothing to seed.")
            return

        now = datetime.now(timezone.utc)

        # --- Users (one per role) ---
        admin = User(
            name="Admin User",
            email=ADMIN_EMAIL,
            hashed_password=hash_password("Admin@123"),
            role=UserRole.ADMIN,
        )
        manager = User(
            name="Manager User",
            email="manager@engagedash.com",
            hashed_password=hash_password("Manager@123"),
            role=UserRole.MANAGER,
        )
        csm = User(
            name="CSM User",
            email="csm@engagedash.com",
            hashed_password=hash_password("Csm@12345"),
            role=UserRole.CSM,
        )
        db.add_all([admin, manager, csm])
        db.commit()
        for u in (admin, manager, csm):
            db.refresh(u)

        # --- Customers (varied statuses; mostly owned by the CSM) ---
        acme = Customer(name="Acme Corp", company="Acme", email="hi@acme.com", phone="+1-555-0100",
                        status=CustomerStatus.ACTIVE, health_score=85,
                        assigned_csm_id=csm.id, created_by_id=csm.id)
        globex = Customer(name="Globex", company="Globex Inc", email="team@globex.com",
                          status=CustomerStatus.AT_RISK, health_score=40,
                          assigned_csm_id=csm.id, created_by_id=csm.id)
        initech = Customer(name="Initech", company="Initech LLC",
                           status=CustomerStatus.PROSPECT, health_score=60,
                           assigned_csm_id=csm.id, created_by_id=csm.id)
        umbrella = Customer(name="Umbrella Co", company="Umbrella",
                            status=CustomerStatus.CHURNED, health_score=20,
                            assigned_csm_id=manager.id, created_by_id=manager.id)
        db.add_all([acme, globex, initech, umbrella])
        db.commit()
        for c in (acme, globex, initech, umbrella):
            db.refresh(c)

        # --- Interactions ---
        meeting = Interaction(
            customer_id=acme.id, created_by_id=csm.id, type=InteractionType.MEETING,
            title="Quarterly business review",
            notes="Customer is very happy with onboarding and the product. They raised concerns "
                  "about the planned pricing increase next year and want to see a roadmap.",
            occurred_at=now - timedelta(days=1),
        )
        call = Interaction(
            customer_id=globex.id, created_by_id=csm.id, type=InteractionType.CALL,
            title="Renewal risk check-in",
            notes="Customer is frustrated with slow support response times and is actively "
                  "evaluating a competitor. Renewal is at risk.",
            occurred_at=now - timedelta(days=2),
        )
        db.add_all([meeting, call])
        db.commit()
        for i in (meeting, call):
            db.refresh(i)

        # --- Insights (inserted directly so the demo works without a live AI call) ---
        db.add_all([
            Insight(
                interaction_id=meeting.id,
                summary="Positive relationship; pricing is the main concern.",
                sentiment=Sentiment.POSITIVE,
                action_items=["Share the pricing roadmap", "Schedule a renewal call"],
                risks=["Price sensitivity ahead of renewal"],
                status=InsightStatus.SUCCESS,
                model="seed",
            ),
            Insight(
                interaction_id=call.id,
                summary="At-risk customer due to support issues and competitor interest.",
                sentiment=Sentiment.NEGATIVE,
                action_items=["Escalate open support tickets", "Offer an executive check-in"],
                risks=["Churn risk", "Evaluating a competitor"],
                status=InsightStatus.SUCCESS,
                model="seed",
            ),
        ])
        db.commit()

        print("Seed complete! Demo logins:")
        print("  admin@engagedash.com   / Admin@123")
        print("  manager@engagedash.com / Manager@123")
        print("  csm@engagedash.com     / Csm@12345")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
