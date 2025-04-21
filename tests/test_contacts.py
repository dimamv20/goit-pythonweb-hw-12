def test_create_contact(client):
    response = client.post("/auth/register", json={
        "email": "contact@example.com",
        "password": "contactpass"
    })
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    contact_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890"
    }
    response = client.post("/contacts/", json=contact_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "john.doe@example.com"

def test_read_contacts(client):
    response = client.get("/contacts/")
    assert response.status_code == 200
