from typing import Optional, List
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    is_active: bool = True

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
    hashed_password: str
