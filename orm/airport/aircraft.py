from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orm import Base
from orm.airport.location import Location


class Aircraft(Base):
    __tablename__ = "aircraft"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    capacity: Mapped[int] = mapped_column()

    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
    location: Mapped["Location"] = relationship()