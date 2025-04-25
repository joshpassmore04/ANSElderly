from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from orm.airport.airport import Airport
from orm.airport.flight import Flight
from orm.user.luggage import Luggage
from orm.user.user import User


# https://iifx.dev/en/articles/230056541
class Traveller(User):

    __tablename__ = "traveller"
    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    passport_verified: Mapped[bool] = mapped_column(default=False)
    luggage_items: Mapped[list["Luggage"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )
    
    flight_id: Mapped[int] = mapped_column(ForeignKey("flight.id"))
    flight: Mapped["Flight"] = relationship(
        "Flight", cascade="all, delete-orphan", single_parent=True  # Add single_parent=True
    )

    destination_airport_id: Mapped[int] = mapped_column(ForeignKey("airport.id"))
    destination_airport: Mapped["Airport"] = relationship()

    __mapper_args__ = {
        "polymorphic_identity": "traveller"
    }