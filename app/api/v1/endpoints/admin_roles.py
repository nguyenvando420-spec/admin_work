from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.role import Role
from app.models.resource import Resource
from app.models.permission import Permission
from app.schemas.role import RolePermissionsUpdate, RoleCreate, RoleResponse
from app.dependencies.permission import require_permission

router = APIRouter()

@router.get("/", response_model=List[RoleResponse], dependencies=[Depends(require_permission("role_admin", "view"))])
def get_roles(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve roles.
    """
    roles = db.query(Role).offset(skip).limit(limit).all()
    return roles

@router.post("/", response_model=RoleResponse, dependencies=[Depends(require_permission("role_admin", "fore"))])
def create_role(
    *,
    db: Session = Depends(get_db),
    role_in: RoleCreate,
) -> Any:
    """
    Create new role.
    """
    role = db.query(Role).filter(Role.role_code == role_in.role_code).first()
    if role:
        raise HTTPException(status_code=400, detail="Role code already exists")
    
    role = Role(
        role_code=role_in.role_code,
        role_name=role_in.role_name,
        description=role_in.description,
        is_active=role_in.is_active
    )
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@router.put("/{role_code}/permissions", dependencies=[Depends(require_permission("role_admin", "fore"))])
def update_role_permissions(
    *,
    db: Session = Depends(get_db),
    role_code: str,
    payload: RolePermissionsUpdate,
) -> Any:
    role = db.query(Role).filter(Role.role_code == role_code).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
        
    # Clear existing permissions
    role.permissions = []
    db.commit()
    
    for res_input in payload.resources:
        if res_input.fore and not res_input.view:
            raise HTTPException(status_code=400, detail=f"Invalid permission configuration for {res_input.resourceCode}: 'fore' requires 'view' to be true")
            
        resource = db.query(Resource).filter(Resource.resource_code == res_input.resourceCode).first()
        if not resource:
            continue
            
        if res_input.view:
            p_view = db.query(Permission).filter(Permission.resource_id == resource.id, Permission.action_code == "view").first()
            if p_view:
                role.permissions.append(p_view)
        
        if res_input.fore:
            p_fore = db.query(Permission).filter(Permission.resource_id == resource.id, Permission.action_code == "fore").first()
            if p_fore:
                role.permissions.append(p_fore)
                
    db.commit()
    return {"message": "Permissions updated successfully"}
