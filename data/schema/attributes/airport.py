from pydantic import BaseModel, ConfigDict

from data.schema.attributes.location import LocationOut
from data.schema.attributes.util import FlightAttributeAction


class AirportCreate(BaseModel):
    name: str
    location_id: int
    action: FlightAttributeAction

class AirportOut(BaseModel):
    id: int
    name: str
    location: LocationOut
    model_config = ConfigDict(from_attributes=True)