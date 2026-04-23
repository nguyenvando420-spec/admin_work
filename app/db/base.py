from app.db.base_class import Base
from app.models.user import User
from app.models.role import Role
from app.models.resource import Resource
from app.models.permission import Permission
from app.models.token_blacklist import TokenBlacklist
from app.models.associations import user_roles, role_permissions
