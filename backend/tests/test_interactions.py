"""Critical tests for interaction CRUD, filtering, and ownership."""

from app.models.user import UserRole

OCCURRED_AT = "2026-06-20T15:00:00Z"


def auth_headers(client, email, password="supersecret123"):
    token = client.post("/auth/login", json={"email": email, "password": password}).json()[
        "access_token"
    ]
    return {"Authorization": f"Bearer {token}"}


def make_customer(client, headers, name="Acme"):
    return client.post("/customers", json={"name": name}, headers=headers).json()["id"]


def make_interaction(client, headers, customer_id, **fields):
    payload = {
        "customer_id": customer_id,
        "title": "QBR",
        "notes": "Some meeting notes.",
        "occurred_at": OCCURRED_AT,
        **fields,
    }
    return client.post("/interactions", json=payload, headers=headers)


# ---------- Create ----------

def test_create_interaction_success(client, create_user):
    create_user("csm@x.com", role=UserRole.CSM)
    headers = auth_headers(client, "csm@x.com")
    customer_id = make_customer(client, headers)
    response = make_interaction(client, headers, customer_id, type="meeting")
    assert response.status_code == 201
    assert response.json()["customer_id"] == customer_id


def test_cannot_create_for_inaccessible_customer(client, create_user):
    create_user("csm1@x.com", role=UserRole.CSM)
    create_user("csm2@x.com", role=UserRole.CSM)
    h1 = auth_headers(client, "csm1@x.com")
    h2 = auth_headers(client, "csm2@x.com")
    other_customer = make_customer(client, h2, name="Owned by 2")

    response = make_interaction(client, h1, other_customer)
    assert response.status_code == 403


def test_create_missing_notes_is_rejected(client, create_user):
    create_user("csm@x.com", role=UserRole.CSM)
    headers = auth_headers(client, "csm@x.com")
    customer_id = make_customer(client, headers)
    response = make_interaction(client, headers, customer_id, notes="")
    assert response.status_code == 422


def test_create_bad_type_is_rejected(client, create_user):
    create_user("csm@x.com", role=UserRole.CSM)
    headers = auth_headers(client, "csm@x.com")
    customer_id = make_customer(client, headers)
    response = make_interaction(client, headers, customer_id, type="zoom")
    assert response.status_code == 422


# ---------- Filtering ----------

def test_list_filters_by_type(client, create_user):
    create_user("csm@x.com", role=UserRole.CSM)
    headers = auth_headers(client, "csm@x.com")
    customer_id = make_customer(client, headers)
    make_interaction(client, headers, customer_id, type="meeting", title="A meeting")
    make_interaction(client, headers, customer_id, type="call", title="A call")

    response = client.get("/interactions?type=call", headers=headers)
    titles = [i["title"] for i in response.json()]
    assert titles == ["A call"]


def test_csm_sees_only_own_interactions(client, create_user):
    create_user("csm1@x.com", role=UserRole.CSM)
    create_user("csm2@x.com", role=UserRole.CSM)
    h1 = auth_headers(client, "csm1@x.com")
    h2 = auth_headers(client, "csm2@x.com")
    c1 = make_customer(client, h1, name="C1")
    c2 = make_customer(client, h2, name="C2")
    make_interaction(client, h1, c1, title="For 1")
    make_interaction(client, h2, c2, title="For 2")

    assert [i["title"] for i in client.get("/interactions", headers=h1).json()] == ["For 1"]
    assert [i["title"] for i in client.get("/interactions", headers=h2).json()] == ["For 2"]


# ---------- Update / 404 ----------

def test_update_interaction(client, create_user):
    create_user("csm@x.com", role=UserRole.CSM)
    headers = auth_headers(client, "csm@x.com")
    customer_id = make_customer(client, headers)
    interaction_id = make_interaction(client, headers, customer_id).json()["id"]

    response = client.patch(
        f"/interactions/{interaction_id}", json={"title": "Updated"}, headers=headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


def test_get_missing_interaction_returns_404(client, create_user):
    create_user("csm@x.com", role=UserRole.CSM)
    headers = auth_headers(client, "csm@x.com")
    assert client.get("/interactions/999", headers=headers).status_code == 404
