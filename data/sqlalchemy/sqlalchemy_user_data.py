from abc import ABC
from typing import Optional

from sqlalchemy import Engine, select, and_
from sqlalchemy.orm import Session

from data.user_data import UserData
from orm.user.permission import Permission
from orm.user.traveller import Traveller
from orm.user.user import User


class SQLAlchemyUserData(UserData, ABC):

    def __init__(self, engine: Engine):
        self.engine = engine

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        with Session(self.engine) as session:
            return session.get(User, user_id)

    def get_traveller_by_id(self, traveller_id: int) -> Optional[Traveller]:
        with Session(self.engine) as session:
            return session.get(Traveller, traveller_id)

    def create_user(self, first_name: str, last_name: str, email: str, hashed_password: str) -> Optional[User]:
        user = User(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    hashed_password=hashed_password)
        self.save_user(user)

    def create_traveller(self, user_id: int) -> Optional[Traveller]:
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            if user is None or isinstance(user, Traveller):
                return None
            traveller = Traveller(
                id=user_id,
            )
            session.delete(user)
            session.add(traveller)
            session.commit()
            return traveller

    def save_user(self, user: User):
        with Session(self.engine) as session:
            exists = session.get(User, user.id)
            if not exists:
                session.add(user)
            session.commit()

    def has_permission(self, user_id: int, permission: str) -> bool:
        with Session(self.engine) as session:
            stmt = select(Permission).where(
                and_(
                    Permission.user_id == user_id,
                    Permission.name == permission
                )
            )
            result = session.execute(stmt).scalar_one_or_none()
            return result is not None

    def delete_user_by_id(self, user_id: int) -> bool:
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            if user:
                session.delete(user)
                session.commit()
                return True
        return False
