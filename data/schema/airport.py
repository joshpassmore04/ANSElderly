from pydantic import BaseModel, ConfigDict


class AirportCreate(BaseModel):
    name: str
    location_id: int

class AirportOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)