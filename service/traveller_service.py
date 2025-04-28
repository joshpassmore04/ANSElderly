from typing import Optional

from data.airport_data import AirportData
from data.user_data import UserData
from orm.user.traveller import Traveller


class TravellerService:
    def __init__(self, user_data: UserData, airport_data: AirportData):
        self.user_data = user_data
        self.airport_data = airport_data

    def convert_to_traveller(self, user_id: int) -> Optional[Traveller]:
        return self.user_data.create_traveller(user_id)

    def add_luggage(self, traveller_id: int, weight_kg: float, latitude: float, longitude: float) -> bool:
        return self.airport_data.add_luggage_to_traveller(traveller_id=traveller_id,
                                                          weight_kg=weight_kg,
                                                          latitude=latitude,
                                                          longitude=longitude)

    def remove_luggage(self, traveller_id: int, luggage_id: int) -> bool:
        return self.airport_data.remove_luggage_from_traveller(traveller_id=traveller_id, luggage_id=luggage_id)

    def add_flight_to(self, traveller_id: int, flight_id: int) -> bool:
        return self.airport_data.add_flight_to(flight_id=flight_id, traveller_id=traveller_id)

    def remove_flight_from(self, traveller_id: int, flight_id: int):
        return self.airport_data.remove_flight_from(flight_id=flight_id, traveller_id=traveller_id)
