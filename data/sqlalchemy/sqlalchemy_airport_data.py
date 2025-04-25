from abc import ABC
from datetime import datetime
from typing import Optional, Any

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from data.airport_data import AirportData
from data.schema.aircraft import AircraftOut
from data.schema.airport import AirportOut
from data.schema.flight import FlightOut
from data.schema.gate import GateOut
from data.schema.location import LocationOut
from data.schema.luggage import LuggageOut
from data.schema.traveller import TravellerOut
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

    def get_flight_by_id(self, flight_id: int) -> Optional[FlightOut]:
        with Session(self.engine) as session:
            flight = session.get(Flight, flight_id)
            return FlightOut.make_flight(flight) if flight else None

    def get_flight_by_number(self, number: str) -> Optional[FlightOut]:
        with Session(self.engine) as session:
            stmt = select(Flight).where(Flight.number == number)
            result = session.execute(stmt).scalars().all()
            return FlightOut.make_flight(result) if result else None

    def get_flights_by_attribute(self, column_name: str, value: Any) -> list[FlightOut]:
        with Session(self.engine) as session:
            stmt = select(Flight).filter_by(**{column_name: value})
            return [FlightOut.make_flight(flight) for flight in session.execute(stmt).scalars().all()]

    def get_airport_by_id(self, airport_id: int) -> Optional[AirportOut]:
        with Session(self.engine) as session:
            airport = session.get(Airport, airport_id)
            return AirportOut.model_validate(airport) if airport else None

    def register_airport(self, name: str, longitude: float = 0, latitude: float = 0) -> AirportOut:
        with Session(self.engine) as session:
            airport = Airport(name=name, location=Location(latitude=latitude, longitude=longitude))
            session.add(airport)
            session.commit()
            return AirportOut.model_validate(airport)

    def register_aircraft(self, name: str, longitude: float = 0, latitude: float = 0) -> AircraftOut:
        with Session(self.engine) as session:
            aircraft = Aircraft(name=name, location=Location(latitude=latitude, longitude=longitude))
            session.add(aircraft)
            session.commit()
            return AircraftOut.model_validate(aircraft)

    def register_gate(self, number: int, opening_time: datetime, longitude: float = 0, latitude: float = 0) -> GateOut:
        with Session(self.engine) as session:
            gate = Gate(number=number, opening_time=opening_time,
                        location=Location(longitude=longitude, latitude=latitude))
            session.add(gate)
            session.commit()
            return GateOut.model_validate(gate)

    def get_flights_after(self, time: datetime = datetime.now()) -> list[FlightOut]:
        with Session(self.engine) as session:
            stmt = select(Flight).where(Flight.expected_arrival_time > time)
            return [FlightOut.make_flight(flight) for flight in session.execute(stmt).scalars().all()]

    def get_flights_before(self, time: datetime = datetime.now()) -> list[FlightOut]:
        with Session(self.engine) as session:
            stmt = select(Flight).where(Flight.expected_arrival_time < time)
            return [FlightOut.make_flight(flight) for flight in session.execute(stmt).scalars().all()]

    def add_luggage_to_traveller(self, weight_kg: float, latitude: float, longitude: float, traveller_id: int) -> bool:
        with Session(self.engine) as session:
            # Optional: validate foreign keys exist
            traveller = session.get(Traveller, traveller_id)
            if not traveller:
                return False
            luggage = Luggage(
                weight_kg=weight_kg,
                location=Location(latitude=latitude, longitude=longitude),
                traveller_id=traveller_id,
            )
            session.add(luggage)
            session.commit()
            return True

    def remove_luggage_from_traveller(self, traveller_id: int, luggage_id: int) -> bool:
        with Session(self.engine) as session:
            traveller_stmt = select(Traveller).where(Traveller.id == traveller_id)
            luggage_stmt = select(Luggage).where(Luggage.id == luggage_id)

            traveller = session.execute(traveller_stmt).scalar_one_or_none()
            luggage = session.execute(luggage_stmt).scalar_one_or_none()

            if not traveller or not luggage or luggage not in traveller.luggage_items:
                return False

            traveller.luggage_items.remove(luggage)
            session.commit()
            return True

    def get_luggage_for(self, traveller_id: int) -> list[LuggageOut]:
        with Session(self.engine) as session:
            stmt = select(Luggage).where(Luggage.traveller_id == traveller_id)
            return [LuggageOut.model_validate(l) for l in session.execute(stmt).scalars().all()]

    def get_luggage_by_id(self, luggage_id: int) -> Optional[LuggageOut]:
        with Session(self.engine) as session:
            luggage = session.get(Luggage, luggage_id)
            return LuggageOut.model_validate(luggage) if luggage else None

    def register_flight(self, aircraft_id: int, from_airport_id: int, to_airport_id: int, gate_id: int, number: str, arrival_time: datetime,
                        departure_time: datetime = datetime.now()) -> FlightOut:
        created_flight = Flight(
            aircraft_id=aircraft_id,
            destination_airport_id=to_airport_id,
            expected_arrival_time=arrival_time,
            leaving_time=departure_time,
            gate_id=gate_id,
            number=number,
        )
        self.save_flight(created_flight)
        return FlightOut.make_flight(created_flight)

    def register_location(self, latitude: float, longitude: float) -> LocationOut:
        with Session(self.engine) as session:
            # Create a new Location instance
            location = Location(latitude=latitude, longitude=longitude)

            # Add the new location to the session and commit the transaction
            session.add(location)
            session.commit()

            # Return the LocationOut model for the newly created location
            return LocationOut.model_validate(location)

    def get_flights_to(self, airport_id: int) -> list[FlightOut]:
        with Session(self.engine) as session:
            stmt = select(Flight).where(Flight.destination_airport_id == airport_id)
            return [FlightOut.make_flight(f) for f in session.execute(stmt).scalars().all()]

    def get_all_travellers_on(self, flight_id: int) -> list[TravellerOut]:
        with Session(self.engine) as session:
            stmt = select(Traveller).where(Traveller.flight_id == flight_id)
            return [TravellerOut.model_validate(t) for t in session.execute(stmt).scalars().all()]

    def get_all_active_flights(self) -> list[FlightOut]:
        with Session(self.engine) as session:
            stmt = select(Flight)
            return [FlightOut.make_flight(f) for f in session.execute(stmt).scalars().all()]

    def get_all_gate(self) -> list[GateOut]:
        with Session(self.engine) as session:
            stmt = select(Gate)
            gates = session.execute(stmt).scalars().all()
        return [GateOut.model_validate(gate) for gate in gates]

    def get_all_airports(self) -> list[AirportOut]:
        with Session(self.engine) as session:
            stmt = select(Airport)
            airports = session.execute(stmt).scalars().all()
        return [AirportOut.model_validate(airport) for airport in airports]

    def get_all_location(self) -> list[LocationOut]:
        with Session(self.engine) as session:
            stmt = select(Location)
            locations = session.execute(stmt).scalars().all()
        return [LocationOut.model_validate(location) for location in locations]

    def get_flights_for(self, traveller_id: int) -> list[FlightOut]:
        with Session(self.engine) as session:
            stmt = select(Flight).where(Flight.travellers.any(Traveller.id == traveller_id))
            return [FlightOut.make_flight(f) for f in session.execute(stmt).scalars().all()]

    def save_flight(self, flight_to_save: Flight):
        with Session(self.engine) as session:
            exists = session.get(Flight, flight_to_save.id)
            if not exists:
                session.add(flight_to_save)
            session.commit()

