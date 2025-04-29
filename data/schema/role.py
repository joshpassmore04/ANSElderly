from enum import Enum

from pydantic import BaseModel, BeforeValidator
from sqlalchemy.sql.annotation import Annotated

from data.permission import RolePermissions


def validate_role(role):
    if isinstance(role, RolePermissions):
        return role
    return RolePermissions.from_label(role)

class RoleAction(str, Enum):
    SET = "set"
    CHECK = "check"

class RoleQuery(BaseModel):
    role: Annotated[RolePermissions, BeforeValidator(validate_role)]
    action: RoleAction
