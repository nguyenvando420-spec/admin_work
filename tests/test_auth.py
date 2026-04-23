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

def test_logout(client, setup_test_data):
    # Login
    resp = client.post("/api/v1/auth/login", data={"username": "admin", "password": "Admin@123"})
    token = resp.json()["access_token"]
    
    # Logout
    resp_logout = client.post("/api/v1/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert resp_logout.status_code == 200
    
    # Try using token again
    resp_me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp_me.status_code == 401
    assert resp_me.json()["detail"] == "Token has been revoked"

def test_change_password(client, setup_test_data):
    # Login
    resp = client.post("/api/v1/auth/login", data={"username": "user_view", "password": setup_test_data["pass"]})
    token = resp.json()["access_token"]
    
    # Change password
    resp_change = client.post(
        "/api/v1/auth/change-password",
        headers={"Authorization": f"Bearer {token}"},
        json={"old_password": setup_test_data["pass"], "new_password": "newpassword123"}
    )
    assert resp_change.status_code == 200
    
    # Login with new password
    resp_login_new = client.post("/api/v1/auth/login", data={"username": "user_view", "password": "newpassword123"})
    assert resp_login_new.status_code == 200

def test_password_expiry_warning(client, setup_test_data):
    # Login user with old password
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "user_expired", "password": setup_test_data["pass"]}
    )
    assert response.status_code == 200
    assert response.json()["need_change_password"] is True

    # Login user with fresh password (admin seed has current time)
    response_fresh = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "Admin@123"}
    )
    assert response_fresh.status_code == 200
    assert response_fresh.json()["need_change_password"] is False
