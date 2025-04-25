from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orm import Base
from orm.airport.aircraft import Aircraft
from orm.airport.gate import Gate


class Flight(Base):
    __tablename__ = "flight"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column()

    gate_id: Mapped[int] = mapped_column(ForeignKey("gate.id"), nullable=False)
    gate: Mapped["Gate"] = relationship("Gate")

    leaving_time: Mapped[datetime] = mapped_column()
    expected_arrival_time: Mapped[datetime] = mapped_column()

    from_airport_id: Mapped[int] = mapped_column(ForeignKey("airport.id"))
    from_airport: Mapped["Airport"] = relationship("Airport", foreign_keys=[from_airport_id], back_populates="flights_from")

    destination_airport_id: Mapped[int] = mapped_column(ForeignKey("airport.id"))
    destination: Mapped["Airport"] = relationship("Airport", foreign_keys=[destination_airport_id], back_populates="flights_to")

    travellers: Mapped[List["Traveller"]] = relationship(
        back_populates="flight",
        cascade="all, delete-orphan"
    )

    aircraft_id: Mapped[int] = mapped_column(ForeignKey("aircraft.id"))
    aircraft: Mapped["Aircraft"] = relationship("Aircraft")




