from typing import Optional

from werkzeug.security import generate_password_hash, check_password_hash

from data.user_data import UserData
from orm.user.user import User


class UserService:
    def __init__(self, user_data: UserData):
        self.user_data = user_data
    def register_user(self, first_name: str, last_name: str, email: str, password: str) -> Optional[User]:
        existing_user = self.user_data.get_user_by_email(email)
        if existing_user is None:
            user = User(first_name=first_name,
                        last_name=last_name,
                        email=email,
                        hashed_password=generate_password_hash(password))
            self.user_data.save_user(user)
            return user
        else:
            return None
    def validate_login(self, email: str, password: str) -> Optional[User]:
        user = self.user_data.get_user_by_email(email)
        if user is not None:
            if check_password_hash(user.hashed_password, password) and email == user.email:
                return user
        return None
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.user_data.get_user_by_id(user_id)
    def get_traveller_by_id(self, traveller_id: int) -> Optional[User]:
        return self.user_data.get_traveller_by_id(traveller_id)
    def delete_user_by_id(self, user_id: int) -> bool:
        return self.user_data.delete_user_by_id(user_id)
    def has_permission(self, user_id: int, permission: str) -> bool:
        return self.user_data.has_permission(user_id, permission) is not None


