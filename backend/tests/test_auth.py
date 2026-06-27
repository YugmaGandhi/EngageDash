"""Critical tests for authentication and role-based access control."""

from app.models.user import UserRole

REGISTER_PAYLOAD = {
    "name": "Asha",
    "email": "asha@example.com",
    "password": "supersecret123",
}


def login(client, email, password):
    """Helper: log in and return the JSON token response."""
    response = client.post("/auth/login", json={"email": email, "password": password})
    return response


# ---------- Register ----------

def test_register_success(client):
    response = client.post("/auth/register", json=REGISTER_PAYLOAD)
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "asha@example.com"
    assert body["role"] == "csm"  # new users always start as CSM
    assert "password" not in body and "hashed_password" not in body


def test_register_duplicate_email_is_rejected(client):
    client.post("/auth/register", json=REGISTER_PAYLOAD)
    response = client.post("/auth/register", json=REGISTER_PAYLOAD)
    assert response.status_code == 409


# ---------- Login ----------

def test_login_success(client):
    client.post("/auth/register", json=REGISTER_PAYLOAD)
    response = login(client, "asha@example.com", "supersecret123")
    assert response.status_code == 200
    body = response.json()
    assert body["access_token"] and body["refresh_token"]
    assert body["token_type"] == "bearer"


def test_login_wrong_password_is_rejected(client):
    client.post("/auth/register", json=REGISTER_PAYLOAD)
    response = login(client, "asha@example.com", "wrong-password")
    assert response.status_code == 401


# ---------- Protected route ----------

def test_me_requires_authentication(client):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_me_with_valid_token(client):
    client.post("/auth/register", json=REGISTER_PAYLOAD)
    token = login(client, "asha@example.com", "supersecret123").json()["access_token"]
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "asha@example.com"


def test_invalid_token_is_rejected(client):
    response = client.get("/auth/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert response.status_code == 401


# ---------- RBAC ----------

def test_csm_cannot_access_admin_route(client, create_user):
    create_user("csm@example.com", role=UserRole.CSM)
    token = login(client, "csm@example.com", "supersecret123").json()["access_token"]
    response = client.get("/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_admin_can_access_admin_route(client, create_user):
    create_user("admin@example.com", role=UserRole.ADMIN)
    token = login(client, "admin@example.com", "supersecret123").json()["access_token"]
    response = client.get("/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ---------- Refresh ----------

def test_refresh_returns_a_working_access_token(client):
    client.post("/auth/register", json=REGISTER_PAYLOAD)
    tokens = login(client, "asha@example.com", "supersecret123").json()

    response = client.post("/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert response.status_code == 200
    new_access = response.json()["access_token"]

    # The new access token should actually work on a protected route.
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {new_access}"})
    assert me.status_code == 200
