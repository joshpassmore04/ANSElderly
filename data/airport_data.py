from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from data.schema.aircraft import AircraftOut
from data.schema.airport import AirportOut
from data.schema.flight import FlightOut
from data.schema.gate import GateOut
from data.schema.location import LocationOut
from data.schema.luggage import LuggageOut
from orm.airport.flight import Flight
from orm.user.traveller import Traveller


class AirportData(ABC):

    @abstractmethod
    def get_flight_by_id(self, flight_id: int) -> Optional[FlightOut]:
        pass

    @abstractmethod
    def get_flights_by_attribute(self, flight_attr: str, value) -> list[FlightOut]:
        pass

    # identifier
    @abstractmethod
    def get_flight_by_number(self, name: str) -> Optional[FlightOut]:
        pass

    @abstractmethod
    def get_airport_by_id(self, airport_id: int) -> Optional[FlightOut]:
        pass

    @abstractmethod
    def get_flights_after(self, time: datetime = datetime.now()) -> list[FlightOut]:
        pass

    @abstractmethod
    def get_flights_before(self, time: datetime = datetime.now()) -> list[FlightOut]:
        pass

    @abstractmethod
    def get_luggage_for(self, traveller_id: int) -> list[LuggageOut]:
        pass

    @abstractmethod
    def get_luggage_by_id(self, luggage_id: int) -> Optional[LuggageOut]:
        pass

    @abstractmethod
    def add_flight_to(self, traveller_id: int, flight_id: int) -> bool:
        pass

    @abstractmethod
    def remove_flight_from(self, traveller_id: int, flight_id: int) -> bool:
        pass

    @abstractmethod
    def add_luggage_to_traveller(self, weight_kg: float, latitude: float, longitude: float, traveller_id: int) -> bool:
        pass

    @abstractmethod
    def remove_luggage_from_traveller(self, traveller_id: int, luggage_id: int) -> bool:
        pass

    @abstractmethod
    def register_flight(self, aircraft_id: int, from_airport_id: int, to_airport_id: int, gate_id: int, number: str, arrival_time: datetime, departure_time: datetime = datetime.now()) -> Optional[FlightOut]:
        pass

    @abstractmethod
    def register_airport(self, name: str, longitude: float = 0, latitude: float = 0) -> AirportOut:
        pass

    @abstractmethod
    def register_aircraft(self, name: str, longitude: float = 0, latitude: float = 0) -> AircraftOut:
        pass

    @abstractmethod
    def register_gate(self, number: int, opening_time: datetime, longitude: float = 0, latitude: float = 0) -> GateOut:
        pass

    @abstractmethod
    def register_location(self, latitude: float, longitude: float, name: str) -> LocationOut:
        pass

    @abstractmethod
    def get_flights_to(self, airport_id: int) -> List[Flight]:
        pass

    @abstractmethod
    def get_all_travellers_on(self, flight_id: int) -> List[Traveller]:
        pass

    @abstractmethod
    def get_all_active_flights(self):
        pass

    @abstractmethod
    def get_all_aircraft(self) -> list[AircraftOut]:
        pass

    @abstractmethod
    def get_all_gate(self) -> list[GateOut]:
        pass

    @abstractmethod
    def get_all_airports(self) -> list[AirportOut]:
        pass

    @abstractmethod
    def get_all_location(self) -> list[LocationOut]:
        pass

    @abstractmethod
    def get_flights_for(self, traveller_id: int) -> List[Flight]:
        pass

    @abstractmethod
    def save_flight(self, flight: Flight):
        pass







