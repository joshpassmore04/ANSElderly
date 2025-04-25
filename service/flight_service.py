from datetime import datetime
from typing import Optional

from cachetools import TTLCache

from data.airport_data import AirportData
from data.permission import PermissionType
from data.schema.aircraft import AircraftOut
from data.schema.airport import AirportOut
from data.schema.flight import FlightOut
from data.schema.gate import GateOut
from data.schema.location import LocationOut
from data.user_data import UserData
from orm.airport.flight import Flight


class FlightService:
    def __init__(self, airport_data: AirportData, user_data: UserData):
        self.airport_data = airport_data
        self.user_data = user_data
        self.flight_cache = TTLCache(maxsize=100, ttl=600)
    def get_all_active_flights(self) -> list[Flight]:
        if self.flight_cache:
            return [flight for flight in self.flight_cache.values() if isinstance(flight, Flight)]
        flights = self.airport_data.get_all_active_flights()
        self.flight_cache.clear()
        for flight in flights:
            self.flight_cache[flight.id] = flight
        return flights
    def add_flight(self, flight: Flight):
        self.flight_cache[flight.id] = flight
        self.airport_data.save_flight(flight)
    def get_all_by_attribute(self, attribute: str, value) -> list[FlightOut]:
        return self.airport_data.get_flights_by_attribute(attribute, value)
    def register_airport(self, from_user_id: int, name: str, longitude: float = 0, latitude: float = 0) -> Optional[AirportOut]:
        if self.user_data.has_permission(from_user_id, PermissionType.ACCESS_ALL_AIRPORT_INFO):
            return self.airport_data.register_airport(name, longitude, latitude)
        return None
    def register_gate(self, from_user_id: int, number: int, opening_time: datetime, longitude: float = 0, latitude: float = 0) -> Optional[GateOut]:
        if self.user_data.has_permission(from_user_id, PermissionType.ACCESS_ALL_AIRPORT_INFO):
            return self.airport_data.register_gate(number, opening_time, longitude, latitude)
        return None
    def register_location(self, from_user_id: int, longitude: float = 0, latitude: float = 0) -> Optional[LocationOut]:
        if self.user_data.has_permission(from_user_id, PermissionType.ACCESS_ALL_AIRPORT_INFO):
            return self.airport_data.register_location(longitude, latitude)
        return None
    def register_aircraft(self, from_user_id: int, name: str, longitude: float = 0, latitude: float = 0) -> Optional[AircraftOut]:
        if self.user_data.has_permission(from_user_id, PermissionType.ACCESS_ALL_AIRPORT_INFO):
            return self.airport_data.register_aircraft(name, longitude, latitude)
        return None
    def register_flight(self, aircraft_id: int, from_airport_id: int, to_airport_id: int, gate_id: int, number: str, arrival_time: datetime,
                        departure_time: datetime = datetime.now()) -> Optional[FlightOut]:
        return self.airport_data.register_flight(aircraft_id, from_airport_id, to_airport_id, gate_id, number, arrival_time, departure_time)
