from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, AfterValidator, EmailStr


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

class UserLogin(UserBase):
    password: Annotated[str, AfterValidator(is_not_empty)]

class UserOut(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserWithPassword(UserOut):
    first_name: Annotated[str, AfterValidator(is_not_empty)]
    last_name: Annotated[str, AfterValidator(is_not_empty)]
    hashed_password: Annotated[str, AfterValidator(is_not_empty)]