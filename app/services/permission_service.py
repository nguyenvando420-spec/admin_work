from app.models.user import User

def load_effective_permissions(user: User):
    """
    Returns a dictionary of effective permissions for a user based on their roles.
    Format: {"resource_code": {"view": bool, "fore": bool, "effectiveFore": bool}}
    """
    permissions_map = {}
    
    # Collect all permissions from all roles
    if hasattr(user, 'roles'):
        for role in user.roles:
            if not role.is_active:
                continue
            for perm in role.permissions:
                res_code = perm.resource.resource_code
                action = perm.action_code
                
                if res_code not in permissions_map:
                    permissions_map[res_code] = {"view": False, "fore": False}
                    
                permissions_map[res_code][action] = True
            
    # Calculate effectiveFore = view AND fore
    for res_code, perms in permissions_map.items():
        perms["effectiveFore"] = perms["view"] and perms["fore"]
        
    return permissions_map

def has_permission(user_permissions: dict, resource_code: str, action: str) -> bool:
    res_perms = user_permissions.get(resource_code)
    if not res_perms:
        return False
        
    if action == "view":
        return res_perms.get("view", False)
        
    if action == "fore":
        return res_perms.get("effectiveFore", False)
        
    return False
