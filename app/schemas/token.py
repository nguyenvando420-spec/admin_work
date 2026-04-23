from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    need_change_password: bool = False
    user: Optional[dict] = None

class TokenPayload(BaseModel):
    sub: Optional[str] = None
