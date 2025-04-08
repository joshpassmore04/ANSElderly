from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orm import Base
from orm.airport.flight import Flight
from orm.airport.location import Location


class Airport(Base):
    __tablename__ = "airports"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))

    location: Mapped["Location"] = relationship("Location", backref="airports")

    flights: Mapped[list["Flight"]] = relationship("Flight", backref="destination_airport")