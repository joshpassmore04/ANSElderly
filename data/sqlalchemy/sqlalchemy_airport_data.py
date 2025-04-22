from abc import ABC
from datetime import datetime
from typing import List, Optional, Any

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from data.airport_data import AirportData
from orm.airport.aircraft import Aircraft
from orm.airport.airport import Airport
from orm.airport.flight import Flight
from orm.airport.gate import Gate
from orm.airport.location import Location
from orm.user.luggage import Luggage
from orm.user.traveller import Traveller


class SQLAlchemyAirportData(AirportData, ABC):

    def __init__(self, engine: Engine):
        self.engine = engine

    def get_flight_by_id(self, flight_id: int) -> Optional[Flight]:
        with Session(self.engine) as session:
            return session.get(Flight, flight_id)

    def get_flight_by_number(self, number: str) -> Optional[Flight]:
        with Session(self.engine) as session:
            stmt = select(Flight).where(Flight.number == number)
            return session.execute(stmt).one_or_none()

    def find_flight_by_attribute(self, column_name: str, value: Any) -> Optional[Flight]:
        with Session(self.engine) as session:
            stmt = select(Flight).filter_by(**{column_name: value})
            return session.execute(stmt).scalar_one_or_none()

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

    def register_gate(self, number: int, opening_time: datetime, longitude: float = 0, latitude: float = 0) -> Gate:
        with Session(self.engine) as session:
            gate = Gate(
                number=number,
                opening_time=opening_time,
                location=Location(longitude=longitude, latitude=latitude)
            )
            session.add(gate)
            session.commit()
            return gate

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

    def register_flight(self, aircraft_id: int, to_airport_id: int, gate_id: int, name: str, arrival_time: datetime,
                        departure_time: datetime = datetime.now()) -> Flight:
        created_flight = Flight(
            aircraft_id=aircraft_id,
            to_airport_id=to_airport_id,
            arrival_time=arrival_time,
            departure_time=departure_time,
            gate_id=gate_id,
            name=name,
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
            exists = session.get(Flight, Flight.id)
            if not exists:
                session.add(flight_to_save)
            session.commit()
