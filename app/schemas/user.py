from typing import Optional, List
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    status: str = "ACTIVE"

class UserCreate(UserBase):
    password: str
    roleCodes: Optional[List[str]] = []

class UserResponse(UserBase):
    id: int
    roleCodes: Optional[List[str]] = []
    
    class Config:
        from_attributes = True

class UserInDB(UserBase):
    id: int
    is_superuser: bool
    password_hash: str
