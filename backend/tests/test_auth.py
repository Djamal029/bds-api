"""Tests for the one complete feature this skeleton ships.

WORKED EXAMPLE — fully implemented.

WHY these test through the HTTP layer (`client.post(...)`) rather than
calling `AuthService` directly: this exercises the whole stack at once
(route -> service -> DAO -> model), which is what actually matters to a
user of the API. Pure service-level unit tests are valuable too for
complex business logic, but for a thin route like this one, testing
through HTTP costs almost nothing extra and catches wiring mistakes
(wrong status code, wrong response shape) that a service-only test
would miss entirely.

Notice what's tested beyond the happy path: a wrong password, a
duplicate email, an invalid token on a protected route. A feature isn't
done when the happy path works — it's done when the failure modes
behave correctly too.
"""

from fastapi.testclient import TestClient

EMAIL = "member@example.com"
PASSWORD = "correct-horse-battery"


def test_register_then_login(client: TestClient) -> None:
    register = client.post(
        "/api/v1/auth/register", json={"email": EMAIL, "password": PASSWORD}
    )
    assert register.status_code == 201
    assert register.json()["email"] == EMAIL

    login = client.post("/api/v1/auth/login", json={"email": EMAIL, "password": PASSWORD})
    assert login.status_code == 200
    assert "access_token" in login.json()


def test_register_duplicate_email_is_rejected(client: TestClient) -> None:
    client.post("/api/v1/auth/register", json={"email": EMAIL, "password": PASSWORD})
    second = client.post(
        "/api/v1/auth/register", json={"email": EMAIL, "password": PASSWORD}
    )
    assert second.status_code == 409


def test_login_wrong_password_is_rejected(client: TestClient) -> None:
    client.post("/api/v1/auth/register", json={"email": EMAIL, "password": PASSWORD})
    response = client.post(
        "/api/v1/auth/login", json={"email": EMAIL, "password": "wrong-password"}
    )
    assert response.status_code == 401


def test_me_requires_a_valid_token(client: TestClient) -> None:
    no_token = client.get("/api/v1/auth/me")
    assert no_token.status_code == 401

    client.post("/api/v1/auth/register", json={"email": EMAIL, "password": PASSWORD})
    login = client.post("/api/v1/auth/login", json={"email": EMAIL, "password": PASSWORD})
    token = login.json()["access_token"]

    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == EMAIL


def test_logging_in_again_invalidates_the_previous_token(client: TestClient) -> None:
    """Demonstrates the single-session behaviour documented in
    core/security.py and api/deps.py: a second login rotates the session
    id, silently invalidating whatever token was issued by the first
    login, even though that first token hasn't expired."""
    client.post("/api/v1/auth/register", json={"email": EMAIL, "password": PASSWORD})

    first_login = client.post(
        "/api/v1/auth/login", json={"email": EMAIL, "password": PASSWORD}
    )
    first_token = first_login.json()["access_token"]

    client.post("/api/v1/auth/login", json={"email": EMAIL, "password": PASSWORD})

    response = client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {first_token}"}
    )
    assert response.status_code == 401


def test_update_profile_sets_username(client: TestClient) -> None:
    client.post("/api/v1/auth/register", json={"email": EMAIL, "password": PASSWORD})
    login = client.post("/api/v1/auth/login", json={"email": EMAIL, "password": PASSWORD})
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    response = client.patch(
        "/api/v1/auth/me", json={"username": "member1"}, headers=headers
    )
    assert response.status_code == 200
    assert response.json()["username"] == "member1"
