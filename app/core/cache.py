from typing import Set

# In-memory token store
# Trong thực tế nên dùng Redis
active_tokens: Set[str] = set()

def add_token(token: str):
    active_tokens.add(token)

def remove_token(token: str):
    if token in active_tokens:
        active_tokens.remove(token)

def is_token_active(token: str) -> bool:
    return token in active_tokens
