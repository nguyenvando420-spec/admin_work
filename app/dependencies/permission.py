from fastapi import Depends, HTTPException
from app.models.user import User
from app.dependencies.auth import get_current_active_user
from app.services.permission_service import load_effective_permissions, has_permission

def require_permission(resource_code: str, action: str):
    def permission_checker(current_user: User = Depends(get_current_active_user)):
        if current_user.is_superuser:
            return True # Super admin bypass
            
        permissions = load_effective_permissions(current_user)
        if not has_permission(permissions, resource_code, action):
            action_desc = "view" if action == "view" else "run job on"
            raise HTTPException(
                status_code=403, 
                detail={"code": "FORBIDDEN", "message": f"You do not have permission to {action_desc} {resource_code}"}
            )
        return True
    return permission_checker
