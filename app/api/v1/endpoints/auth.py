from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserResponse
from app.dependencies.auth import get_current_user, security_scheme
from app.core.cache import add_token, remove_token
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel

router = APIRouter()

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login", response_model=Token)
def login_access_token(
    data: LoginRequest, db: Session = Depends(get_db)
) -> Any:
    """
    Login, lấy access token và lưu vào cache.
    """
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not security.verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Tài khoản hoặc mật khẩu không chính xác")
    elif not user.is_active:
        raise HTTPException(status_code=401, detail="Tài khoản đã bị khóa")
        
    access_token = security.create_access_token(user.id)
    
    # Lưu token vào cache
    add_token(access_token)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": {"id": user.id, "username": user.username}
    }

@router.post("/logout")
def logout(
    auth: HTTPAuthorizationCredentials = Depends(security_scheme),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Đăng xuất và xóa token khỏi cache.
    """
    token = auth.credentials
    remove_token(token)
    return {"message": "Đăng xuất thành công"}

@router.post("/change-password")
def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Đổi mật khẩu.
    """
    if not security.verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Mật khẩu cũ không chính xác")
    
    current_user.hashed_password = security.get_password_hash(data.new_password)
    db.commit()
    
    return {"message": "Cập nhật mật khẩu thành công"}

@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Lấy thông tin user hiện tại.
    """
    return current_user
