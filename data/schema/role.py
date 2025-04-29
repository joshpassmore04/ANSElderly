from pydantic import BaseModel, field_validator
from typing import Optional
from enum import Enum

# Assuming this is your enum
class RolePermissions(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

    @classmethod
    def from_label(cls, label: str) -> "RolePermissions":
        for member in cls:
            if member.value == label:
                return member
        raise ValueError(f"Invalid role label: {label}")

class RoleAction(str, Enum):
    SET = "set"
    CHECK = "check"

class RoleQuery(BaseModel):
    user_id: int
    role: RolePermissions
    debug_bypass: Optional[bool] = False
    action: RoleAction

    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, value: str | RolePermissions) -> RolePermissions:
        if isinstance(value, RolePermissions):
            return value
        return RolePermissions.from_label(value)
