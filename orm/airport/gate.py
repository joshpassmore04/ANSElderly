import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orm import Base
from orm.airport.location import Location


class Gate(Base):
    __tablename__ = "gate"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column()
    opening_time: Mapped[datetime] = mapped_column()

    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"), nullable=False)
    location: Mapped["Location"] = relationship("Location", back_populates="gate")