from abc import ABC, abstractmethod
from typing import Optional

from data.permission import PermissionType, PermissionResult
from data.schema.user import UserOut, UserWithPassword
from orm.user.permission import Permission
from orm.user.traveller import Traveller
from orm.user.user import User


class UserData(ABC):

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[UserOut]:
        pass

    def get_user_by_email(self, email: str) -> Optional[UserOut]:
        pass

    def validate_user_by_email(self, email: str) -> Optional[UserWithPassword]:
        pass

    @abstractmethod
    def get_traveller_by_id(self, traveller_id: int) -> Optional[Traveller]:
        pass

    @abstractmethod
    def create_user(self, first_name: str, last_name: str, email: str, hashed_password: str) -> Optional[UserOut]:
        pass

    @abstractmethod
    def create_traveller(self, user_id: int) -> Optional[Traveller]:
        pass

    @abstractmethod
    def save_user(self, user: User):
        pass

    @abstractmethod
    def give_permission(self, to_user_id: int, name: str) -> PermissionResult:
        pass

    @abstractmethod
    def remove_permission(self, to_user_id: int, name: str) -> bool:
        pass

    @abstractmethod
    def has_permission(self, user_id: int, permission: str) -> bool:
        pass

    # TODO: Make sure this change cascades
    @abstractmethod
    def delete_user_by_id(self, user_id: int) -> bool:
        pass




