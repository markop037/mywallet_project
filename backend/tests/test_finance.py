from fastapi.testclient import TestClient


def _register_and_login(client: TestClient) -> str:
    client.post("/auth/register", json={
        "first_name": "Marko",
        "last_name": "Peric",
        "username": "marko123",
        "password": "SecurePass1!",
        "email": "marko@example.com",
    })
    res = client.post("/auth/login", json={"username": "marko123", "password": "SecurePass1!"})
    return res.json()["access_token"]


def test_get_balance_empty(client: TestClient):
    token = _register_and_login(client)
    res = client.get("/finance/balance", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["balance"] == 0


def test_add_income(client: TestClient):
    token = _register_and_login(client)
    res = client.post(
        "/finance/incomes",
        json={"category_id": 1, "amount": 500.0, "description": "Salary"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 201

    balance = client.get(
        "/finance/balance",
        headers={"Authorization": f"Bearer {token}"},
    ).json()["balance"]
    assert balance == 500.0


def test_add_expense(client: TestClient):
    token = _register_and_login(client)
    client.post(
        "/finance/incomes",
        json={"category_id": 1, "amount": 1000.0},
        headers={"Authorization": f"Bearer {token}"},
    )
    res = client.post(
        "/finance/expenses",
        json={"category_id": 1, "amount": 300.0, "description": "Groceries"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 201

    balance = client.get(
        "/finance/balance",
        headers={"Authorization": f"Bearer {token}"},
    ).json()["balance"]
    assert balance == 700.0


def test_expense_exceeds_balance(client: TestClient):
    token = _register_and_login(client)
    res = client.post(
        "/finance/expenses",
        json={"category_id": 1, "amount": 100.0},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400
    assert "Balance" in res.json()["detail"]


def test_get_transactions(client: TestClient):
    token = _register_and_login(client)
    client.post("/finance/incomes", json={"category_id": 1, "amount": 200.0},
                headers={"Authorization": f"Bearer {token}"})
    res = client.get("/finance/transactions", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    txs = res.json()
    assert len(txs) == 1
    assert txs[0]["type"] == "Income"
    assert txs[0]["amount"] == 200.0


def test_delete_transaction(client: TestClient):
    token = _register_and_login(client)
    client.post("/finance/incomes", json={"category_id": 1, "amount": 300.0},
                headers={"Authorization": f"Bearer {token}"})
    txs = client.get("/finance/transactions",
                     headers={"Authorization": f"Bearer {token}"}).json()
    tx_id = txs[0]["id"]

    res = client.delete(f"/finance/transactions/Income/{tx_id}",
                        headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 204

    balance = client.get("/finance/balance",
                         headers={"Authorization": f"Bearer {token}"}).json()["balance"]
    assert balance == 0
