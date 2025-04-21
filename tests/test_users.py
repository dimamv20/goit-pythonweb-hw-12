def test_register_user(client):
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_user(client):
    client.post("/auth/register", json={
        "email": "login@example.com",
        "password": "loginpass"
    })
    response = client.post("/auth/login", json={
        "email": "login@example.com",
        "password": "loginpass"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
