from pydantic import BaseModel, ConfigDict


class LocationCreate(BaseModel):
    latitude: float
    longitude: float
    name: str

class LocationOut(LocationCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)