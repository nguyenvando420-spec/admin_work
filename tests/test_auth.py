def test_login_success(client, setup_test_data):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "Admin@123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client, setup_test_data):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    
def test_access_without_token(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401

def test_invalid_token(client):
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
