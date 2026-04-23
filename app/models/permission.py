from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False, index=True)
    action_code = Column(String(20), nullable=False) # 'view' or 'fore'
    description = Column(String(500))
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint('resource_id', 'action_code', name='uq_permissions_resource_action'),
    )

    resource = relationship("Resource", back_populates="permissions")
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")
