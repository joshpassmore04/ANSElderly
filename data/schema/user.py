from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, AfterValidator, EmailStr

from data.permission import PermissionType, PermissionAction


def is_not_empty(value: Optional[str]) -> Optional[str]:
    if value is not None and len(value.strip()) == 0:
        raise ValueError("Field cannot be empty")
    return value


class UserBase(BaseModel):
    email: EmailStr


class UserRegister(UserBase):
    first_name: Annotated[str, AfterValidator(is_not_empty)]
    last_name: Annotated[str, AfterValidator(is_not_empty)]
    password: Annotated[str, AfterValidator(is_not_empty)]


class UserCreate(UserBase):
    password: Annotated[str, AfterValidator(is_not_empty)]


class UserOut(UserBase):
    id: int
    first_name: Annotated[str, AfterValidator(is_not_empty)]
    last_name: Annotated[str, AfterValidator(is_not_empty)]
    model_config = ConfigDict(from_attributes=True)


class UserWithPassword(UserOut):
    hashed_password: Annotated[str, AfterValidator(is_not_empty)]


class UserUpdatePermission(BaseModel):
    to_id: int
    permission_name: PermissionType
    action: PermissionAction
    debug_bypass: Optional[bool]
