import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orm import Base
from orm.airport.airport import Airport
from orm.airport.gate import Gate


class Flight(Base):

    __tablename__ = "flight"

    id: Mapped[int] = mapped_column(primary_key=True)

    gate_id: Mapped[int] = mapped_column(ForeignKey("gate.id"), nullable=False)
    gate: Mapped["Gate"] = relationship("Gate")

    leaving_time: Mapped[datetime] = mapped_column()
    expected_arrival_time: Mapped[datetime] = mapped_column()

    destination_airport_id: Mapped[int] = mapped_column(ForeignKey("airport.id"))
    destination: Mapped["Airport"] = relationship("Airport", back_populates="flights")
