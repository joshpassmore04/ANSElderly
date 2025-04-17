from abc import ABC
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from data.airport_data import AirportData
from orm.airport.flight import Flight
from orm.user.luggage import Luggage
from orm.user.traveller import Traveller


class SQLAlchemyAirportData(AirportData, ABC):

    def __init__(self, engine: Engine):
        self.engine = engine

    def get_flight_by_id(self, flight_id: int) -> Optional[Flight]:
        with Session(self.engine) as session:
            return session.get(Flight, flight_id)

    def get_flights_after(self, time: datetime = datetime.now()) -> list[Flight]:
        with Session(self.engine) as session:
            stmt = select(Flight).where(Flight.expected_arrival_time > time)
            return list(session.execute(stmt).scalars().all())

    def get_flights_before(self, time: datetime = datetime.now()) -> List[Flight]:
        with Session(self.engine) as session:
            stmt = select(Flight).where(Flight.expected_arrival_time < time)
            return list(session.execute(stmt).scalars().all())

    def get_luggage_for(self, traveller_id: int) -> list[Luggage]:
        with Session(self.engine) as session:
            stmt = select(Luggage).where(Luggage.traveller_id == traveller_id)
            return list(session.execute(stmt).scalars().all())

    def get_luggage_by_id(self, luggage_id: int) -> Optional[Luggage]:
        with Session(self.engine) as session:
            return session.get(Luggage, luggage_id)

    def register_flight(self, aircraft_id: int, to_airport_id: int, arrival_time: datetime,
                        departure_time: datetime = datetime.now()) -> Flight:
        pass

    def get_flights_to(self, airport_id: int) -> List[Flight]:
        pass

    def get_all_travellers_on(self, flight_id: int) -> List[Traveller]:
        pass

    def get_all_active_flights(self):
        pass

    def get_flights_for(self, traveller_id: int) -> List[Flight]:
        pass

    def save_flight(self, flight: Flight):
        pass


