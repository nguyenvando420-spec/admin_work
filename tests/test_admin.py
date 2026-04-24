def test_list_users(client, setup_test_data):
    # Login as admin
    resp = client.post("/api/v1/auth/login", data={"username": "admin", "password": "Admin@123"})
    token = resp.json()["access_token"]
    
    # List users
    resp_users = client.get("/api/v1/admin/users", headers={"Authorization": f"Bearer {token}"})
    assert resp_users.status_code == 200
    assert len(resp_users.json()) >= 6

def test_create_user(client, setup_test_data):
    # Login as admin
    resp = client.post("/api/v1/auth/login", data={"username": "admin", "password": "Admin@123"})
    token = resp.json()["access_token"]
    
    # Create new user
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123",
        "name": "New User",
        "roleCodes": ["viewer"]
    }
    resp_create = client.post("/api/v1/admin/users", headers={"Authorization": f"Bearer {token}"}, json=user_data)
    assert resp_create.status_code == 200
    
    # Verify new user can login
    resp_login = client.post("/api/v1/auth/login", data={"username": "newuser", "password": "password123"})
    assert resp_login.status_code == 200

def test_update_role_permissions_rule(client, setup_test_data):
    # Login as admin
    resp = client.post("/api/v1/auth/login", data={"username": "admin", "password": "Admin@123"})
    token = resp.json()["access_token"]
    
    # Try to set fore=True but view=False (should fail 400)
    perm_data = {
        "resources": [
            {
                "resourceCode": "job_monitor",
                "view": False,
                "fore": True
            }
        ]
    }
    resp_update = client.put(
        "/api/v1/admin/roles/viewer/permissions",
        headers={"Authorization": f"Bearer {token}"},
        json=perm_data
    )
    assert resp_update.status_code == 400
    assert "requires 'view' to be true" in resp_update.json()["detail"]

def test_update_role_permissions_success(client, setup_test_data):
    # Login as admin
    resp = client.post("/api/v1/auth/login", data={"username": "admin", "password": "Admin@123"})
    token = resp.json()["access_token"]
    
    # Update viewer to have fore permission
    perm_data = {
        "resources": [
            {
                "resourceCode": "job_monitor",
                "view": True,
                "fore": True
            }
        ]
    }
    resp_update = client.put(
        "/api/v1/admin/roles/viewer/permissions",
        headers={"Authorization": f"Bearer {token}"},
        json=perm_data
    )
    assert resp_update.status_code == 200
    
    # Verify viewer now has fore permission (login as viewer)
    resp_v = client.post("/api/v1/auth/login", data={"username": "user_view", "password": setup_test_data["pass"]})
    token_v = resp_v.json()["access_token"]
    
    resp_run = client.post("/api/v1/job-monitor/run", headers={"Authorization": f"Bearer {token_v}"})
    assert resp_run.status_code == 200
