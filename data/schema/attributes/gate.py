from datetime import datetime

from pydantic import BaseModel, ConfigDict

from data.schema.attributes.util import FlightAttributeAction


class GateCreate(BaseModel):
    number: int
    opening_time: datetime
    location_id: int
    action: FlightAttributeAction

class GateOut(BaseModel):
    number: int
    opening_time: datetime
    location_id: int
    id: int
    model_config = ConfigDict(from_attributes=True)