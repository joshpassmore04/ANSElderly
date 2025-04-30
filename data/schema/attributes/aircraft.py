from pydantic import BaseModel, ConfigDict

from data.schema.attributes.location import LocationOut
from data.schema.attributes.util import FlightAttributeAction


class AircraftCreate(BaseModel):
    name: str
    capacity: int
    location_id: int
    action: FlightAttributeAction

class AircraftOut(BaseModel):
    id: int
    name: str
    location: LocationOut
    model_config = ConfigDict(from_attributes=True)