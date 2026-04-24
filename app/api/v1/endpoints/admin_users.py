from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserResponse
from app.dependencies.permission import require_permission
from app.core.security import get_password_hash

router = APIRouter()

@router.post("", response_model=UserResponse, dependencies=[Depends(require_permission("user_admin", "fore"))])
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    user = db.query(User).filter(User.username == user_in.username).first()
    if user:
        raise HTTPException(status_code=400, detail="The user with this username already exists in the system.")
    
    user = User(
        username=user_in.username,
        email=user_in.email,
        name=user_in.name,
        hashed_password=get_password_hash(user_in.password),
        is_active=True,
    )
    db.add(user)
    
    if user_in.roleCodes:
        roles = db.query(Role).filter(Role.role_code.in_(user_in.roleCodes)).all()
        user.roles.extend(roles)
        
    db.commit()
    db.refresh(user)
    
    roleCodes = [role.role_code for role in user.roles]
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "name": user.name,
        "is_active": user.is_active,
        "roleCodes": roleCodes
    }

@router.get("", response_model=List[UserResponse], dependencies=[Depends(require_permission("user_admin", "view"))])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    users = db.query(User).offset(skip).limit(limit).all()
    results = []
    for user in users:
        roleCodes = [role.role_code for role in user.roles]
        results.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "is_active": user.is_active,
            "roleCodes": roleCodes
        })
    return results
