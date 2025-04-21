from datetime import datetime

from pydantic import BaseModel


class FlightCreate(BaseModel):
    destination_airport_id: int
    aircraft_id: int
    gate_id: int
    departure_time: datetime
    arrival_time: datetime
    number: str

class FlightOut(FlightCreate):
    id: int

    class Config:
        orm_mode = True

class FlightQuery(BaseModel):
    number: str


