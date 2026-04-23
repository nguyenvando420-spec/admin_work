from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.models.token_blacklist import TokenBlacklist
from app.schemas.token import Token
from app.schemas.user import UserResponse
from app.dependencies.auth import get_current_user, oauth2_scheme
from jose import jwt

from datetime import datetime, timedelta
from pydantic import BaseModel

router = APIRouter()

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    elif user.status != "ACTIVE":
        raise HTTPException(status_code=401, detail="Inactive user")
        
    # Check if password needs update (30 days)
    need_change = False
    if user.password_updated_at:
        if datetime.now() - user.password_updated_at > timedelta(days=30):
            need_change = True

    access_token = security.create_access_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "need_change_password": need_change,
        "user": {"id": user.id, "username": user.username}
    }

@router.post("/change-password")
def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Change password.
    """
    if not security.verify_password(data.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect old password")
    
    current_user.password_hash = security.get_password_hash(data.new_password)
    current_user.password_updated_at = datetime.now()
    db.commit()
    
    return {"message": "Password updated successfully"}

@router.post("/logout")
def logout(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Log out and blacklist the current token.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        exp = payload.get("exp")
        expires_at = datetime.fromtimestamp(exp)
        
        blacklisted_token = TokenBlacklist(token=token, expires_at=expires_at)
        db.add(blacklisted_token)
        db.commit()
    except Exception:
        # If token is invalid or can't be decoded, we don't need to blacklist it
        pass
    
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get current user.
    """
    roleCodes = [role.role_code for role in current_user.roles] if hasattr(current_user, 'roles') else []
    return {
        "id": current_user.id,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "status": current_user.status,
        "roleCodes": roleCodes
    }
