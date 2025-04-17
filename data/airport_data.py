from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Optional

from orm.airport.airport import Airport
from orm.airport.flight import Flight
from orm.user.luggage import Luggage
from orm.user.traveller import Traveller


class AirportData(ABC):

    @abstractmethod
    def get_flight_by_id(self, flight_id: int) -> Optional[Flight]:
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
    def register_flight(self, aircraft_id: int, to_airport_id: int, arrival_time: datetime, departure_time: datetime = datetime.now()) -> Flight:
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







