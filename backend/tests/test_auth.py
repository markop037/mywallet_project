from fastapi.testclient import TestClient


def test_register_success(client: TestClient):
    res = client.post("/auth/register", json={
        "first_name": "Marko",
        "last_name": "Peric",
        "username": "marko123",
        "password": "SecurePass1!",
        "email": "marko@example.com",
    })
    assert res.status_code == 201
    assert res.json()["message"] == "User successfully registered"


def test_register_duplicate(client: TestClient):
    payload = {
        "first_name": "Marko",
        "last_name": "Peric",
        "username": "marko123",
        "password": "SecurePass1!",
        "email": "marko@example.com",
    }
    client.post("/auth/register", json=payload)
    res = client.post("/auth/register", json=payload)
    assert res.status_code == 400
    assert "already exists" in res.json()["detail"]


def test_login_success(client: TestClient):
    client.post("/auth/register", json={
        "first_name": "Marko",
        "last_name": "Peric",
        "username": "marko123",
        "password": "SecurePass1!",
        "email": "marko@example.com",
    })
    res = client.post("/auth/login", json={"username": "marko123", "password": "SecurePass1!"})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient):
    client.post("/auth/register", json={
        "first_name": "Marko",
        "last_name": "Peric",
        "username": "marko123",
        "password": "SecurePass1!",
        "email": "marko@example.com",
    })
    res = client.post("/auth/login", json={"username": "marko123", "password": "wrongpass"})
    assert res.status_code == 401


def test_protected_endpoint_requires_token(client: TestClient):
    res = client.get("/finance/balance")
    assert res.status_code == 401
