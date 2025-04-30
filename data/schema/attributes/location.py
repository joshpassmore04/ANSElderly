from pydantic import BaseModel, ConfigDict

from data.schema.attributes.util import FlightAttributeAction


class LocationCreate(BaseModel):
    latitude: float
    longitude: float
    name: str
    action: FlightAttributeAction

class LocationOut(BaseModel):
    id: int
    latitude: float
    longitude: float
    name: str
    model_config = ConfigDict(from_attributes=True)