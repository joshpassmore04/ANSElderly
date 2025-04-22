from typing import Optional

from pydantic import BaseModel, EmailStr, model_validator

from service.errors.invalid_data import InvalidData


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True