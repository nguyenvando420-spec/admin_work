from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.role import Role
from app.models.resource import Resource
from app.models.permission import Permission
from app.schemas.role import RolePermissionsUpdate
from app.dependencies.permission import require_permission

router = APIRouter()

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
