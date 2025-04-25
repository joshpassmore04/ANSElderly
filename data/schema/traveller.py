from data.schema.luggage import LuggageOut
from data.schema.user import UserOut


class TravellerOut(UserOut):
    flight_id: int
    destination_airport_id: int
    passport_verified: bool
    luggage_items: list[LuggageOut]