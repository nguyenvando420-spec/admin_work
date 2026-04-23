from typing import Any
from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.permission_service import load_effective_permissions

router = APIRouter()

@router.get("/permissions")
def read_my_permissions(
    current_user: User = Depends(get_current_user),
) -> Any:
    permissions = load_effective_permissions(current_user)
    
    resources_list = []
    for res_code, perms in permissions.items():
        resources_list.append({
            "resourceCode": res_code,
            "view": perms["view"],
            "fore": perms["fore"],
            "effectiveFore": perms["effectiveFore"]
        })
        
    return {
        "user": {
            "id": current_user.id,
            "username": current_user.username
        },
        "resources": resources_list
    }
