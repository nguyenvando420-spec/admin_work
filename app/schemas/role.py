from typing import Optional, List
from pydantic import BaseModel

class RoleBase(BaseModel):
    role_code: str
    role_name: str
    description: Optional[str] = None
    is_active: bool = True

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int
    
    class Config:
        from_attributes = True

class PermissionInput(BaseModel):
    resourceCode: str
    view: bool
    fore: bool

class RolePermissionsUpdate(BaseModel):
    resources: List[PermissionInput]
