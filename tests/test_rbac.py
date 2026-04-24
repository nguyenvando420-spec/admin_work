def test_user_with_view_can_read(client, setup_test_data):
    resp = client.post("/api/v1/auth/login", json={"username": "user_view", "password": setup_test_data["pass"]})
    token = resp.json()["access_token"]
    
    resp_read = client.get("/api/v1/job-monitor/items", headers={"Authorization": f"Bearer {token}"})
    assert resp_read.status_code == 200

def test_user_with_view_cannot_run(client, setup_test_data):
    resp = client.post("/api/v1/auth/login", json={"username": "user_view", "password": setup_test_data["pass"]})
    token = resp.json()["access_token"]
    
    resp_run = client.post("/api/v1/job-monitor/run", headers={"Authorization": f"Bearer {token}"})
    assert resp_run.status_code == 403

def test_user_with_view_and_fore_can_run(client, setup_test_data):
    resp = client.post("/api/v1/auth/login", json={"username": "user_op", "password": setup_test_data["pass"]})
    token = resp.json()["access_token"]
    
    resp_run = client.post("/api/v1/job-monitor/run", headers={"Authorization": f"Bearer {token}"})
    assert resp_run.status_code == 200

def test_user_with_fore_but_no_view_cannot_run(client, setup_test_data):
    resp = client.post("/api/v1/auth/login", json={"username": "user_bad_op", "password": setup_test_data["pass"]})
    token = resp.json()["access_token"]
    
    resp_run = client.post("/api/v1/job-monitor/run", headers={"Authorization": f"Bearer {token}"})
    assert resp_run.status_code == 403

def test_user_with_no_roles_cannot_access(client, setup_test_data):
    resp = client.post("/api/v1/auth/login", json={"username": "user_noroles", "password": setup_test_data["pass"]})
    token = resp.json()["access_token"]
    
    resp_read = client.get("/api/v1/job-monitor/items", headers={"Authorization": f"Bearer {token}"})
    assert resp_read.status_code == 403
