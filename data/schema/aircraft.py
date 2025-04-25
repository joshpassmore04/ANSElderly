from pydantic import BaseModel, ConfigDict

from orm.airport.location import Location


class AircraftCreate(BaseModel):
    name: str
    capacity: int
    location_id: int

class AircraftOut(BaseModel):
    name: str
    location: Location
    model_config = ConfigDict(from_attributes=True)