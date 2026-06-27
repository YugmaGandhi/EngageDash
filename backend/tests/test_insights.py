"""Critical tests for AI insights: parsing, fallback, and RBAC.

The AI client is always mocked, so these tests never make a real network call.
"""

import pytest

from app.models.user import UserRole
from app.services.ai.parsing import parse_insight

OCCURRED_AT = "2026-06-20T15:00:00Z"


# ---------- Parser (pure functions) ----------

def test_parse_clean_json():
    result = parse_insight(
        '{"summary":"All good","sentiment":"positive","action_items":["x"],"risks":[]}'
    )
    assert result.summary == "All good"
    assert result.sentiment.value == "positive"
    assert result.action_items == ["x"]


def test_parse_json_in_code_fence_with_prose():
    text = 'Sure!\n```json\n{"summary":"ok","sentiment":"Negative","action_items":[],"risks":["price"]}\n```\nDone.'
    result = parse_insight(text)
    assert result.sentiment.value == "negative"  # casing normalized
    assert result.risks == ["price"]


def test_parse_invalid_json_raises():
    with pytest.raises(ValueError):
        parse_insight("this is not json")


def test_parse_invalid_sentiment_raises():
    with pytest.raises(Exception):
        parse_insight('{"summary":"s","sentiment":"angry"}')


# ---------- Mock AI clients ----------

class GoodClient:
    model = "fake-model"

    def generate(self, messages, **kwargs):
        return '{"summary":"Customer happy","sentiment":"positive","action_items":["follow up"],"risks":[]}'


class FailingClient:
    model = "fake-model"

    def generate(self, messages, **kwargs):
        raise RuntimeError("AI is down")


def mock_ai(monkeypatch, client_class):
    """Swap the AI client used by the generator with a fake one."""
    monkeypatch.setattr("app.services.ai.generator.AIClient", client_class)


# ---------- Helpers ----------

def auth_headers(client, email, password="supersecret123"):
    token = client.post("/auth/login", json={"email": email, "password": password}).json()[
        "access_token"
    ]
    return {"Authorization": f"Bearer {token}"}


def make_interaction(client, headers):
    customer_id = client.post("/customers", json={"name": "Acme"}, headers=headers).json()["id"]
    return client.post(
        "/interactions",
        json={
            "customer_id": customer_id,
            "title": "QBR",
            "notes": "Customer is happy but worried about pricing.",
            "occurred_at": OCCURRED_AT,
        },
        headers=headers,
    ).json()["id"]


# ---------- Endpoint: generate + fallback + RBAC ----------

def test_generate_insight_success(client, create_user, monkeypatch):
    mock_ai(monkeypatch, GoodClient)
    create_user("csm@x.com", role=UserRole.CSM)
    headers = auth_headers(client, "csm@x.com")
    interaction_id = make_interaction(client, headers)

    response = client.post(f"/interactions/{interaction_id}/insights", headers=headers)
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "success"
    assert body["sentiment"] == "positive"
    assert body["action_items"] == ["follow up"]


def test_generate_insight_falls_back_when_ai_fails(client, create_user, monkeypatch):
    mock_ai(monkeypatch, FailingClient)
    create_user("csm@x.com", role=UserRole.CSM)
    headers = auth_headers(client, "csm@x.com")
    interaction_id = make_interaction(client, headers)

    response = client.post(f"/interactions/{interaction_id}/insights", headers=headers)
    # The request still succeeds (no 500); the insight is marked as a fallback.
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "fallback"
    assert body["sentiment"] == "neutral"


def test_list_insights_returns_history(client, create_user, monkeypatch):
    mock_ai(monkeypatch, GoodClient)
    create_user("csm@x.com", role=UserRole.CSM)
    headers = auth_headers(client, "csm@x.com")
    interaction_id = make_interaction(client, headers)

    client.post(f"/interactions/{interaction_id}/insights", headers=headers)
    client.post(f"/interactions/{interaction_id}/insights", headers=headers)

    response = client.get(f"/interactions/{interaction_id}/insights", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_csm_cannot_generate_for_inaccessible_interaction(client, create_user, monkeypatch):
    mock_ai(monkeypatch, GoodClient)
    create_user("csm1@x.com", role=UserRole.CSM)
    create_user("csm2@x.com", role=UserRole.CSM)
    h1 = auth_headers(client, "csm1@x.com")
    h2 = auth_headers(client, "csm2@x.com")
    interaction_id = make_interaction(client, h1)

    response = client.post(f"/interactions/{interaction_id}/insights", headers=h2)
    assert response.status_code == 403
