from enum import Enum

class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

def has_role(user_role: str, required_role: Role):
    if user_role != required_role.value:
        return False
    return True
