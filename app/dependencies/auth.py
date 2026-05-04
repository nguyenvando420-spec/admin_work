from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core import config
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import TokenPayload
from app.core.cache import is_token_active

security_scheme = HTTPBearer()

def get_current_user(
    db: Session = Depends(get_db), auth: HTTPAuthorizationCredentials = Depends(security_scheme)
) -> User:
    token = auth.credentials
    
    # Check if token is in active cache
    if not is_token_active(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Phiên đăng nhập đã hết hạn hoặc không hợp lệ",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    try:
        payload = jwt.decode(
            token, config.settings.SECRET_KEY, algorithms=[config.settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Không thể xác thực thông tin đăng nhập",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == int(token_data.sub)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Không tìm thấy người dùng")
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Tài khoản đã bị khóa")
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user
