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

    @classmethod
    def make_flight(cls, flight) -> "FlightOut":
        return cls(
            id=flight.id,
            from_airport_id=flight.from_airport_id,
            to_airport_id=flight.destination_airport_id,
            aircraft_id=flight.aircraft_id,
            gate_id=flight.gate_id,
            departure_time=flight.leaving_time,
            arrival_time=flight.expected_arrival_time,
            number=flight.number
        )


class FlightQuery(BaseModel):
    attribute: FlightAttribute
    value: Union[str, int]
