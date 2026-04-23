from sqlalchemy import Column, String, DateTime, Integer
from app.db.base_class import Base

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(500), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
