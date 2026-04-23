from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    resource_code = Column(String(100), unique=True, index=True, nullable=False)
    resource_name = Column(String(255), nullable=False)
    menu_key = Column(String(100))
    menu_label = Column(String(255))
    route_path = Column(String(255))
    parent_menu_key = Column(String(100))
    display_order = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    permissions = relationship("Permission", back_populates="resource")
