"""Critical tests for customer CRUD, filtering, and RBAC scoping."""

from app.models.user import UserRole


def auth_headers(client, email, password="supersecret123"):
    """Log in and return the Authorization header for that user."""
    token = client.post("/auth/login", json={"email": email, "password": password}).json()[
        "access_token"
    ]
    return {"Authorization": f"Bearer {token}"}


def create_customer(client, headers, **fields):
    payload = {"name": "Acme", **fields}
    return client.post("/customers", json=payload, headers=headers)


# ---------- Create + validation ----------

def test_create_customer_success(client, create_user):
    create_user("csm@x.com", role=UserRole.CSM)
    headers = auth_headers(client, "csm@x.com")
    response = create_customer(client, headers, company="Acme Corp", status="active", health_score=80)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Acme"
    assert body["assigned_csm_id"] == body["created_by_id"]  # defaults to creator


def test_create_customer_invalid_email_is_rejected(client, create_user):
    create_user("csm@x.com", role=UserRole.CSM)
    headers = auth_headers(client, "csm@x.com")
    response = create_customer(client, headers, email="not-an-email")
    assert response.status_code == 422


def test_create_customer_invalid_health_score_is_rejected(client, create_user):
    create_user("csm@x.com", role=UserRole.CSM)
    headers = auth_headers(client, "csm@x.com")
    response = create_customer(client, headers, health_score=150)
    assert response.status_code == 422


# ---------- Filtering ----------

def test_list_filters_by_status(client, create_user):
    create_user("csm@x.com", role=UserRole.CSM)
    headers = auth_headers(client, "csm@x.com")
    create_customer(client, headers, name="Active Co", status="active")
    create_customer(client, headers, name="Churned Co", status="churned")

    response = client.get("/customers?status=churned", headers=headers)
    names = [c["name"] for c in response.json()]
    assert names == ["Churned Co"]


def test_list_search_matches_name(client, create_user):
    create_user("csm@x.com", role=UserRole.CSM)
    headers = auth_headers(client, "csm@x.com")
    create_customer(client, headers, name="Globex")
    create_customer(client, headers, name="Initech")

    response = client.get("/customers?search=glob", headers=headers)
    names = [c["name"] for c in response.json()]
    assert names == ["Globex"]


# ---------- RBAC scoping ----------

def test_csm_sees_only_own_customers(client, create_user):
    create_user("csm1@x.com", role=UserRole.CSM)
    create_user("csm2@x.com", role=UserRole.CSM)
    h1 = auth_headers(client, "csm1@x.com")
    h2 = auth_headers(client, "csm2@x.com")
    create_customer(client, h1, name="Owned by 1")
    create_customer(client, h2, name="Owned by 2")

    assert [c["name"] for c in client.get("/customers", headers=h1).json()] == ["Owned by 1"]
    assert [c["name"] for c in client.get("/customers", headers=h2).json()] == ["Owned by 2"]


def test_csm_cannot_view_another_csms_customer(client, create_user):
    create_user("csm1@x.com", role=UserRole.CSM)
    create_user("csm2@x.com", role=UserRole.CSM)
    h1 = auth_headers(client, "csm1@x.com")
    h2 = auth_headers(client, "csm2@x.com")
    customer_id = create_customer(client, h1, name="Private").json()["id"]

    assert client.get(f"/customers/{customer_id}", headers=h2).status_code == 403


def test_manager_can_view_any_customer(client, create_user):
    create_user("csm@x.com", role=UserRole.CSM)
    create_user("mgr@x.com", role=UserRole.MANAGER)
    hc = auth_headers(client, "csm@x.com")
    hm = auth_headers(client, "mgr@x.com")
    customer_id = create_customer(client, hc, name="Any").json()["id"]

    assert client.get(f"/customers/{customer_id}", headers=hm).status_code == 200


# ---------- Update / delete / 404 ----------

def test_update_customer(client, create_user):
    create_user("csm@x.com", role=UserRole.CSM)
    headers = auth_headers(client, "csm@x.com")
    customer_id = create_customer(client, headers).json()["id"]

    response = client.patch(
        f"/customers/{customer_id}", json={"status": "at_risk"}, headers=headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == "at_risk"


def test_csm_cannot_delete_customer(client, create_user):
    create_user("csm@x.com", role=UserRole.CSM)
    headers = auth_headers(client, "csm@x.com")
    customer_id = create_customer(client, headers).json()["id"]

    assert client.delete(f"/customers/{customer_id}", headers=headers).status_code == 403


def test_manager_can_delete_customer(client, create_user):
    create_user("csm@x.com", role=UserRole.CSM)
    create_user("mgr@x.com", role=UserRole.MANAGER)
    hc = auth_headers(client, "csm@x.com")
    hm = auth_headers(client, "mgr@x.com")
    customer_id = create_customer(client, hc).json()["id"]

    assert client.delete(f"/customers/{customer_id}", headers=hm).status_code == 204
    # Now it's gone.
    assert client.get(f"/customers/{customer_id}", headers=hm).status_code == 404


def test_get_missing_customer_returns_404(client, create_user):
    create_user("csm@x.com", role=UserRole.CSM)
    headers = auth_headers(client, "csm@x.com")
    assert client.get("/customers/999", headers=headers).status_code == 404
