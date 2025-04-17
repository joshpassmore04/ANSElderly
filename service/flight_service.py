from cachetools import TTLCache

from data.airport_data import AirportData
from orm.airport.flight import Flight


class FlightService:
    def __init__(self, airport_data: AirportData):
        self.airport_data = airport_data
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