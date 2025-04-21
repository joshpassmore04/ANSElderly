from typing import Optional

from pydantic import BaseModel, EmailStr, model_validator

from service.errors.invalid_data import InvalidData


class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

    @model_validator(mode="after")
    def at_least_one_required(self, values):
        username, email = values.get("username"), values.get("email")
        if not username and not email:
            raise InvalidData("Invalid login data")
        return values

class UserCreate(UserBase):
    plaintext_password: str

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True