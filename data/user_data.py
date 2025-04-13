from abc import ABC, abstractmethod

from orm.user.traveller import Traveller
from orm.user.user import User


class UserData(ABC):

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_traveller_by_id(self, traveller_id: int) -> Traveller:
        pass

    @abstractmethod
    def create_user(self, first_name: str, last_name: str, email: str, hashed_password: str) -> User:
        pass

    @abstractmethod
    def create_traveller(self, user_id: int) -> Traveller:
        pass

    @abstractmethod
    def save_user(self, user: User):
        pass

    @abstractmethod
    def save_traveller(self, traveller: Traveller):
        pass

    # TODO: Make sure this change cascades
    @abstractmethod
    def delete_user(self, user_id: int):
        pass




