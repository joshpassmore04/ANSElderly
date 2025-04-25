from pydantic import BaseModel, ConfigDict


class LocationCreate(BaseModel):
    latitude: float
    longitude: float
    model_config = ConfigDict(from_attributes=True)

class LocationOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)