from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Optional

from orm.airport.aircraft import Aircraft
from orm.airport.airport import Airport
from orm.airport.flight import Flight
from orm.user.luggage import Luggage
from orm.user.traveller import Traveller


class AirportData(ABC):

    @abstractmethod
    def get_flight_by_id(self, flight_id: int) -> Optional[Flight]:
        pass

    @abstractmethod
    def get_flight_by_attr(self, flight_attr: str) -> Optional[Flight]:
        pass

    # identifier
    @abstractmethod
    def get_flight_by_number(self, name: str) -> Optional[Flight]:
        pass

    @abstractmethod
    def get_airport_by_id(self, airport_id: int) -> Optional[Airport]:
        pass

    @abstractmethod
    def get_flights_after(self, time: datetime = datetime.now()) -> List[Flight]:
        pass

    @abstractmethod
    def get_flights_before(self, time: datetime = datetime.now()) -> List[Flight]:
        pass

    @abstractmethod
    def get_luggage_for(self, traveller_id: int) -> List[Luggage]:
        pass

    @abstractmethod
    def get_luggage_by_id(self, luggage_id: int) -> Optional[Luggage]:
        pass

    @abstractmethod
    def register_flight(self, aircraft_id: int, to_airport_id: int, name: str, arrival_time: datetime, departure_time: datetime = datetime.now()) -> Flight:
        pass

    @abstractmethod
    def register_airport(self, name: str, longitude: float = 0, latitude: float = 0) -> Airport:
        pass

    @abstractmethod
    def register_aircraft(self, name: str, longitude: float = 0, latitude: float = 0) -> Aircraft:
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
    def get_flights_for(self, traveller_id: int) -> List[Flight]:
        pass

    @abstractmethod
    def save_flight(self, flight: Flight):
        pass







