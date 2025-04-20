from datetime import datetime

from pydantic import BaseModel


class FlightBase(BaseModel):
    destination: str
    departure_time: datetime
    arrival_time: datetime

class FlightOut(FlightBase):
    id: int
    class Config:
        orm_mode = True
