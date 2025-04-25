from pydantic import BaseModel, ConfigDict


class LuggageCreate(BaseModel):
    weight_kg: float
    capacity: int
    location_id: int
    traveller_id: int

class LuggageOut(LuggageCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)