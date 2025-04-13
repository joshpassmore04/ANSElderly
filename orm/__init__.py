from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

flight_airport_lnk = Table(
    "flight_airport_link",
    Base.metadata,
    Column("flight_id", ForeignKey("flight.id"), primary_key=True),
    Column("airport_id", ForeignKey("airport.id"), primary_key=True)
)