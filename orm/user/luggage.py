from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orm import Base
from orm.airport.location import Location
from orm.user.traveller import Traveller


class Luggage(Base):
    __tablename__ = "luggage"

    id: Mapped[int] = mapped_column(primary_key=True)

    weight_kg: Mapped[float] = mapped_column()
    contents_verified: Mapped[bool] = mapped_column()

    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
    location: Mapped["Location"] = relationship()

    traveller_id: Mapped[int] = mapped_column(ForeignKey("travellers.id"))
    owner: Mapped["Traveller"] = relationship("Traveller", back_populates="luggage")