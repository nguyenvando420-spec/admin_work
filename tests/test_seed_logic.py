import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.models.role import Role
from app.models.user import User
from app.models.permission import Permission
from app.models.resource import Resource
from seed import seed_data
import seed

# Mock SessionLocal and settings
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_seed_logic(monkeypatch):
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Patch SessionLocal and db calls in seed
    monkeypatch.setattr(seed, "SessionLocal", lambda: db)
    
    # 1. Run seed first time
    seed_data()
    
    # Check if super_admin has permissions
    super_admin = db.query(Role).filter(Role.role_code == "super_admin").first()
    assert super_admin is not None
    assert len(super_admin.permissions) > 0
    
    # Check if admin user has super_admin role
    admin_user = db.query(User).filter(User.username == "admin").first()
    assert any(r.role_code == "super_admin" for r in admin_user.roles)
    
    # 2. Add a new resource and run seed again
    new_res = Resource(resource_code="new_res", resource_name="New Resource")
    db.add(new_res)
    db.commit()
    new_perm = Permission(resource_id=new_res.id, action_code="view")
    db.add(new_perm)
    db.commit()
    
    seed_data()
    
    # Check if super_admin now has the new permission
    db.refresh(super_admin)
    perm_codes = [p.action_code for p in super_admin.permissions if p.resource_id == new_res.id]
    assert "view" in perm_codes
    
    db.close()
    Base.metadata.drop_all(bind=engine)
