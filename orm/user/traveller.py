from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from orm.airport.flight import Flight
from orm.user.luggage import Luggage
from orm.user.user import User


# https://iifx.dev/en/articles/230056541
class Traveller(User):

    __tablename__ = "traveller"
    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    passport_verified: Mapped[bool] = mapped_column(default=False)
    luggage_items: Mapped[List["Luggage"]] = relationship(
        "Luggage", back_populates="owner", cascade="all, delete-orphan"
    )

    flight: Mapped["Flight"] = relationship(
        back_populates="travellers"
    )

    __mapper_args__ = {
        "polymorphic_identity": "traveller"
    }

    def verify_passport(self):
        self.passport_verified = True

    def add_to_luggage(self, luggage: Luggage):
        self.luggage_items.append(luggage)

    def remove_from_luggage(self, luggage: Luggage):
        self.luggage_items.remove(luggage)

    def clear_luggage(self):
        self.luggage_items = []