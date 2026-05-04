from typing import Any
from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/permissions")
def read_my_permissions(
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Lấy danh sách quyền của user hiện tại.
    """
    return {
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "role": current_user.role
        },
        "permissions": current_user.permission
    }
