from fastapi import Depends, HTTPException
from app.models.user import User
from app.dependencies.auth import get_current_active_user
from app.services.permission_service import load_effective_permissions, has_permission

def require_permission(permission_name: str):
    def permission_checker(current_user: User = Depends(get_current_active_user)):
        user_permissions = load_effective_permissions(current_user)
        if not has_permission(user_permissions, permission_name):
            raise HTTPException(
                status_code=403, 
                detail={
                    "code": "FORBIDDEN", 
                    "message": f"Bạn không có quyền thực hiện hành động này: {permission_name}"
                }
            )
        return True
    return permission_checker
