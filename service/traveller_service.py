from typing import Optional

from data.airport_data import AirportData
from data.user_data import UserData
from orm.user.luggage import Luggage
from orm.user.traveller import Traveller


class TravellerService:
    def __init__(self, user_data: UserData, airport_data: AirportData):
        self.user_data = user_data
        self.airport_data = airport_data

    def convert_to_traveller(self, user_id: int) -> Optional[Traveller]:
        return self.user_data.create_traveller(user_id)

    def verify_passport(self, traveller_id: int):
        traveller = self.user_data.get_traveller_by_id(traveller_id)
        if traveller is None:
            raise ValueError(f"Traveller with ID {traveller_id} not found.")
        traveller.passport_verified = True
        self.user_data.save_user(traveller)

    def add_luggage(self, traveller_id: int, weight_kg: float, latitude: float, longitude: float) -> bool:
        return self.airport_data.add_luggage_to_traveller(traveller_id=traveller_id, weight_kg=weight_kg, location_id=location_id)

    def remove_luggage(self, traveller_id: int, luggage_id: int):
        traveller = self.user_data.get_traveller_by_id(traveller_id)
        if traveller is None:
            raise ValueError(f"Traveller with ID {traveller_id} not found.")
        luggage = self.airport_data.get_luggage_by_id(luggage_id)
        if luggage is None:
            raise ValueError(f"Luggage with ID {luggage_id} not found.")
        traveller.luggage_items.remove(luggage)
        self.user_data.save_user(traveller)

    def add_flight_to(self, traveller_id: int, flight_id: int):
        flight = self.airport_data.get_flight_by_id(flight_id)
        if flight is None:
            raise ValueError(f"Flight with ID {flight_id} not found.")
        traveller = self.user_data.get_traveller_by_id(traveller_id)
        if traveller is None:
            raise ValueError(f"Traveller with ID {traveller_id} not found.")
        flight.add_traveller(traveller)
        self.airport_data.save_flight(flight)

    def remove_flight_from(self, traveller_id: int, flight_id: int):
        flight = self.airport_data.get_flight_by_id(flight_id)
        if flight is None:
            raise ValueError(f"Flight with ID {flight_id} not found.")
        traveller = self.user_data.get_traveller_by_id(traveller_id)
        if traveller is None:
            raise ValueError(f"Traveller with ID {traveller_id} not found.")
        flight.remove_traveller(traveller)
        self.airport_data.save_flight(flight)
