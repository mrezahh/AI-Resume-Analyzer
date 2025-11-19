def test_register_user(client):
    response = client.post("/auth/register", json={
        "full_name": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data
    

def test_login_user(client):
    # First, register the user
    client.post("/auth/register", json={
        "full_name": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    
    # Then, attempt to log in(OAuth2PasswordRequestForm requires form data)
    response = client.post("/auth/login", data={
        "username": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"