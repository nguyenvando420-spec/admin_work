from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    password_updated_at = Column(DateTime, default=func.now(), nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    status = Column(String(20), default="ACTIVE", nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    roles = relationship("Role", secondary="user_roles", back_populates="users")
