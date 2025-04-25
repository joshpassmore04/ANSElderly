from pydantic import BaseModel, ConfigDict

from data.schema.location import LocationOut


class AircraftCreate(BaseModel):
    name: str
    capacity: int
    location_id: int

class AircraftOut(BaseModel):
    name: str
    location: LocationOut
    model_config = ConfigDict(from_attributes=True)