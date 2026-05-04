import enum
from sqlalchemy import Column, Integer, String, Boolean, JSON, Enum
from app.db.base_class import Base

class UserRole(str, enum.Enum):
    admin = "admin"
    operator = "operator"
    viewer = "viewer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255))
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.viewer)
    permission = Column(JSON, default=[], nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
