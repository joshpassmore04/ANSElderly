from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orm import Base
from orm.airport.flight import Flight
from orm.airport.location import Location


# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#relationship-patterns
class Airport(Base):
    __tablename__ = "airport"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))

    location: Mapped["Location"] = relationship("Location")

    # Define the relationship for flights departing from this airport
    flights_from: Mapped[list["Flight"]] = relationship(
        "Flight",
        back_populates="from_airport",
        cascade="all, delete-orphan",
        foreign_keys="[Flight.from_airport_id]"  # Explicitly specify the foreign key
    )

    # Define the relationship for flights arriving at this airport
    flights_to: Mapped[list["Flight"]] = relationship(
        "Flight",
        back_populates="destination",
        cascade="all, delete-orphan",
        foreign_keys="[Flight.destination_airport_id]"  # Explicitly specify the foreign key
    )

    def __str__(self):
        return self.name

