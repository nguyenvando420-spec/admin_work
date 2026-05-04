from typing import Optional, List
from pydantic import BaseModel
from app.models.user import UserRole

class UserBase(BaseModel):
    username: str
    name: Optional[str] = None
    role: UserRole = UserRole.viewer
    permission: List[str] = []
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    permission: Optional[List[str]] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class UserInDB(UserBase):
    id: int
    hashed_password: str
