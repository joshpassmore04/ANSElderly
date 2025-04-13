from cachetools import TTLCache

from data.airport_data import AirportData


flight_cache = TTLCache(maxsize=100, ttl=600)

class FlightService:
    def __init__(self, airport_data: AirportData):
        self.airport_data = airport_data
