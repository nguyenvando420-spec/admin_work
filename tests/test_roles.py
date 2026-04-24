import pytest

def test_list_roles(client, setup_test_data):
    # Login as admin
    resp = client.post("/api/v1/auth/login", json={"username": "admin", "password": "Admin@123"})
    token = resp.json()["access_token"]
    
    # List roles
    resp_roles = client.get("/api/v1/admin/roles", headers={"Authorization": f"Bearer {token}"})
    assert resp_roles.status_code == 200
    roles = resp_roles.json()
    assert len(roles) >= 4
    role_codes = [r["role_code"] for r in roles]
    assert "admin" in role_codes
    assert "viewer" in role_codes


def test_create_role(client, setup_test_data):
    # Login as admin
    resp = client.post("/api/v1/auth/login", json={"username": "admin", "password": "Admin@123"})
    token = resp.json()["access_token"]
    
    # Create new role
    role_data = {
        "role_code": "manager",
        "role_name": "Manager",
        "description": "Manager Role",
        "is_active": True
    }
    resp_create = client.post("/api/v1/admin/roles", headers={"Authorization": f"Bearer {token}"}, json=role_data)
    assert resp_create.status_code == 200
    assert resp_create.json()["role_code"] == "manager"
    
    # Verify it exists in list
    resp_roles = client.get("/api/v1/admin/roles", headers={"Authorization": f"Bearer {token}"})
    role_codes = [r["role_code"] for r in resp_roles.json()]
    assert "manager" in role_codes

def test_create_duplicate_role(client, setup_test_data):
    # Login as admin
    resp = client.post("/api/v1/auth/login", json={"username": "admin", "password": "Admin@123"})
    token = resp.json()["access_token"]
    
    # Create existing role
    role_data = {
        "role_code": "admin",
        "role_name": "Admin Duplicate",
    }
    resp_create = client.post("/api/v1/admin/roles", headers={"Authorization": f"Bearer {token}"}, json=role_data)
    assert resp_create.status_code == 400
    assert "Role code already exists" in resp_create.json()["detail"]
