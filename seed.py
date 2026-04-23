import asyncio
from sqlalchemy import func
from datetime import datetime
from app.db.session import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.models.resource import Resource
from app.models.permission import Permission
from app.core.security import get_password_hash
import app.db.base

from app.core.config import settings

def seed_data():
    db = SessionLocal()
    
    # 1. Resources
    # ... (giữ nguyên các resource khác)
    resources_data = [
        {"code": "user_admin", "name": "User Administration", "menu": "user_admin", "label": "Users"},
        {"code": "role_admin", "name": "Role Administration", "menu": "role_admin", "label": "Roles"},
        {"code": "job_monitor", "name": "Job Monitor", "menu": "job_monitor", "label": "Job Monitor"},
    ]
    
    resources = []
    for r in resources_data:
        resource = db.query(Resource).filter(Resource.resource_code == r["code"]).first()
        if not resource:
            resource = Resource(
                resource_code=r["code"],
                resource_name=r["name"],
                menu_key=r["menu"],
                menu_label=r["label"],
            )
            db.add(resource)
            db.commit()
            db.refresh(resource)
        resources.append(resource)
        
        # Add permissions
        for action in ["view", "fore"]:
            perm = db.query(Permission).filter(
                Permission.resource_id == resource.id,
                Permission.action_code == action
            ).first()
            if not perm:
                perm = Permission(
                    resource_id=resource.id,
                    action_code=action,
                    description=f"{r['name']} - {action}"
                )
                db.add(perm)
        db.commit()

    # 2. Roles
    roles_data = [
        ("super_admin", "Super Admin"),
        ("admin", "Admin"),
        ("viewer", "Viewer"),
        ("operator", "Operator"),
    ]
    
    for code, name in roles_data:
        role = db.query(Role).filter(Role.role_code == code).first()
        if not role:
            role = Role(role_code=code, role_name=name)
            db.add(role)
            db.commit()
            db.refresh(role)
            
            # If super_admin, assign all permissions
            if code == "super_admin":
                all_perms = db.query(Permission).all()
                for p in all_perms:
                    role.permissions.append(p)
                db.commit()
                
    # 3. Super admin user
    admin_user = db.query(User).filter(User.username == settings.FIRST_SUPERUSER_USERNAME).first()
    if not admin_user:
        admin_user = User(
            username=settings.FIRST_SUPERUSER_USERNAME,
            full_name="Initial System Admin",
            email=settings.FIRST_SUPERUSER_EMAIL,
            password_hash=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            password_updated_at=func.now(),
            is_superuser=True,
            status="ACTIVE"
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
    else:
        # Update existing admin from env if needed (Upsert logic)
        admin_user.email = settings.FIRST_SUPERUSER_EMAIL
        admin_user.password_hash = get_password_hash(settings.FIRST_SUPERUSER_PASSWORD)
        admin_user.password_updated_at = func.now()
        db.commit()
        
    super_admin_role = db.query(Role).filter(Role.role_code == "super_admin").first()
    if super_admin_role and super_admin_role not in admin_user.roles:
        admin_user.roles.append(super_admin_role)
        db.commit()

    print(f"Database seeded successfully with superuser: {settings.FIRST_SUPERUSER_USERNAME}")

if __name__ == "__main__":
    seed_data()
