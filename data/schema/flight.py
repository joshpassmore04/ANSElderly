from datetime import datetime
from enum import Enum
from typing import Union

from pydantic import BaseModel, ConfigDict


class FlightAttribute(str, Enum):
    AIRPORT = "airport"
    AIRCRAFT = "aircraft"
    GATE = "gate"
    NUMBER = "number"


class FlightCreate(BaseModel):
    from_airport_id: int
    to_airport_id: int
    aircraft_id: int
    gate_id: int
    departure_time: datetime
    arrival_time: datetime
    number: str

class FlightOut(FlightCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class FlightQuery(BaseModel):
    attribute: FlightAttribute
    value: Union[str, int]




