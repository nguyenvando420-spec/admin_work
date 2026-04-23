import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.models.user import User
from app.models.role import Role
from app.models.resource import Resource
from app.models.permission import Permission
from app.core.security import get_password_hash

from sqlalchemy.pool import StaticPool

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def setup_test_data(db_session):
    # Setup roles
    r_admin = Role(role_code="admin", role_name="Admin")
    r_viewer = Role(role_code="viewer", role_name="Viewer")
    r_operator = Role(role_code="operator", role_name="Operator")
    r_bad_operator = Role(role_code="bad_operator", role_name="Bad Operator")
    
    # Setup resources & permissions
    res_job = Resource(resource_code="job_monitor", resource_name="Job Monitor")
    db_session.add_all([r_admin, r_viewer, r_operator, r_bad_operator, res_job])
    db_session.commit()
    
    p_view = Permission(resource_id=res_job.id, action_code="view")
    p_fore = Permission(resource_id=res_job.id, action_code="fore")
    db_session.add_all([p_view, p_fore])
    db_session.commit()
    
    # Assign permissions
    r_viewer.permissions.append(p_view)
    r_operator.permissions.extend([p_view, p_fore])
    r_bad_operator.permissions.append(p_fore) # Only fore, no view
    db_session.commit()
    
    # Setup users
    u_admin = User(username="admin", password_hash=get_password_hash("Admin@123"), status="ACTIVE", is_superuser=True)
    u_viewer = User(username="user_view", password_hash=get_password_hash("testpass"), status="ACTIVE")
    u_operator = User(username="user_op", password_hash=get_password_hash("testpass"), status="ACTIVE")
    u_bad_op = User(username="user_bad_op", password_hash=get_password_hash("testpass"), status="ACTIVE")
    u_no_roles = User(username="user_noroles", password_hash=get_password_hash("testpass"), status="ACTIVE")
    
    u_admin.roles.append(r_admin)
    u_viewer.roles.append(r_viewer)
    u_operator.roles.append(r_operator)
    u_bad_op.roles.append(r_bad_operator)
    
    db_session.add_all([u_admin, u_viewer, u_operator, u_bad_op, u_no_roles])
    db_session.commit()
    
    return {
        "pass": "testpass"
    }
