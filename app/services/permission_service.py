from app.models.user import User, UserRole

def load_effective_permissions(user: User):
    """
    Trả về danh sách quyền hiệu dụng của user.
    Admin có toàn quyền.
    """
    if user.role == UserRole.admin:
        return ["*"] # Toàn quyền
    
    return user.permission or []

def has_permission(user_permissions: list, required_permission: str) -> bool:
    """
    Kiểm tra xem user có quyền cụ thể nào đó không.
    """
    if "*" in user_permissions:
        return True
    
    return required_permission in user_permissions
