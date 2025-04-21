from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orm import Base, flight_airport_lnk
from orm.airport.airport import Airport
from orm.airport.gate import Gate
from orm.user.traveller import Traveller


class Flight(Base):

    __tablename__ = "flight"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column()

    gate_id: Mapped[int] = mapped_column(ForeignKey("gate.id"), nullable=False)
    gate: Mapped["Gate"] = relationship("Gate")

    leaving_time: Mapped[datetime] = mapped_column()
    expected_arrival_time: Mapped[datetime] = mapped_column()

    destination_airport_id: Mapped[int] = mapped_column(ForeignKey("airport.id"))
    destination: Mapped["Airport"] = relationship("Airport", back_populates="flights")

    travellers: Mapped[List["Traveller"]] = relationship(
        back_populates="flight",
        cascade="all, delete-orphan"
    )

    airport: Mapped["Airport"] = relationship(
        "Airport",
        secondary=flight_airport_lnk,
        uselist=False,
        back_populates="flights"
    )

    def add_traveller(self, traveller: Traveller):
        self.travellers.append(traveller)

    def remove_traveller(self, traveller: Traveller):
        self.travellers.remove(traveller)


