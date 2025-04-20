from abc import ABC
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from data.airport_data import AirportData
from orm.airport import flight
from orm.airport.aircraft import Aircraft
from orm.airport.airport import Airport
from orm.airport.flight import Flight
from orm.airport.location import Location
from orm.user.luggage import Luggage
from orm.user.traveller import Traveller


class SQLAlchemyAirportData(AirportData, ABC):

    def __init__(self, engine: Engine):
        self.engine = engine

    def get_flight_by_id(self, flight_id: int) -> Optional[Flight]:
        with Session(self.engine) as session:
            return session.get(Flight, flight_id)

    def get_airport_by_id(self, airport_id: int) -> Optional[Airport]:
        with Session(self.engine) as session:
            return session.get(Airport, airport_id)

    def register_airport(self, name: str, longitude: float = 0, latitude: float = 0) -> Airport:
        with Session(self.engine) as session:
            airport = Airport(name=name, location=Location(latitude=latitude, longitude=longitude))
            session.add(airport)
            session.commit()
            return airport

    def register_aircraft(self, name: str, longitude: float = 0, latitude: float = 0) -> Aircraft:
        with Session(self.engine) as session:
            aircraft = Aircraft(
                name=name,
                location=Location(latitude=latitude, longitude=longitude))
            session.add(aircraft)
            session.commit()
            return aircraft

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
        created_flight = Flight(
                aircraft_id=aircraft_id,
                to_airport_id=to_airport_id,
                arrival_time=arrival_time,
                departure_time=departure_time,
        )
        self.save_flight(created_flight)
        return created_flight

    def get_flights_to(self, airport_id: int) -> list[Flight]:
        with Session(self.engine) as session:
            stmt = select(Flight).where(Flight.destination_airport_id == airport_id)
            return list(session.execute(stmt).scalars().all())

    def get_all_travellers_on(self, flight_id: int) -> list[Traveller]:
        with Session(self.engine) as session:
            stmt = select(Traveller).where(Traveller.flight_id == flight_id)
            return list(session.execute(stmt).scalars().all())

    def get_all_active_flights(self):
        with Session(self.engine) as session:
            stmt = select(Flight)
            return list(session.execute(stmt).scalars().all())

    def get_flights_for(self, traveller_id: int) -> List[Flight]:
        with Session(self.engine) as session:
            stmt = select(Flight).where(Flight.travellers.any(Traveller.id == traveller_id))
            return list(session.execute(stmt).scalars().all())

    def save_flight(self, flight_to_save: Flight):
        with Session(self.engine) as session:
            session.add(flight_to_save)
            session.commit()



