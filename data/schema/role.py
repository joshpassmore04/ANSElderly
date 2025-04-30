from pydantic import BaseModel, field_validator
from typing import Optional
from enum import Enum

from data.permission import RolePermission


class RoleAction(str, Enum):
    SET = "set"
    CHECK = "check"

class RoleQuery(BaseModel):
    user_id: int
    role: RolePermission
    debug_bypass: Optional[bool] = False
    action: RoleAction

    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, value: str | RolePermission) -> RolePermission:
        if isinstance(value, RolePermission):
            return value
        return RolePermission.from_label(value)
