from flask import Blueprint, request, jsonify, g
from flask_cors import cross_origin
from pydantic import ValidationError

from data.permission import PermissionType
from data.schema.aircraft import AircraftCreate
from data.schema.airport import AirportCreate
from data.schema.flight import FlightQuery, FlightOut, FlightCreate
from data.schema.gate import GateCreate
from data.schema.location import LocationCreate
from routes.util import login_required, invalid_data
from service.flight_service import FlightService
from service.user_service import UserService


def create_airport_blueprint(base_endpoint, user_service: UserService, flight_service: FlightService):
    flight_blueprint = Blueprint('airport', __name__, url_prefix=base_endpoint + '/airport')

    @flight_blueprint.route("/get-flight", methods=["POST"])
    @cross_origin(supports_credentials=True)
    @login_required
    def get():
        try:
            flight_query = FlightQuery(**request.json)
            if flight_query:
                flights = flight_service.get_all_by_attribute(flight_query.attribute, flight_query.value)
                if flights:
                    return jsonify(
                        {"status": "success", "message": "Flights found", "flights": flights}), 200
                return jsonify({"status": "failure", "message": "Flights not found"}), 404
            else:
                return invalid_data()
        except ValidationError:
            return invalid_data()

    @flight_blueprint.route("/create-airport", methods=["POST"])
    @cross_origin(supports_credentials=True)
    @login_required
    def create_airport():
        from_user_id = g.get("USER_ID")
        try:
            airport_create = AirportCreate(**request.json)
            airport = flight_service.register_airport(from_user_id, airport_create.name, airport_create.longitude, airport_create.latitude)
            if airport:
                return jsonify({"status": "success", "message": "Airport created", "airport": airport.model_dump()}), 200
            else:
                return invalid_data()
        except ValidationError:
            return invalid_data()

    @flight_blueprint.route("/create-gate", methods=["POST"])
    @cross_origin(supports_credentials=True)
    @login_required
    def create_gate():
        from_user_id = g.get("USER_ID")
        try:
            gate_create = GateCreate(**request.json)  # GateCreate should be a Pydantic model for validation
            gate = flight_service.register_gate(
                from_user_id,
                gate_create.number,
                gate_create.opening_time,
                gate_create.longitude,
                gate_create.latitude
            )
            if gate:
                return jsonify({"status": "success", "message": "Gate created", "gate": gate.model_dump()}), 200
            else:
                return invalid_data()
        except ValidationError:
            return invalid_data()

    @flight_blueprint.route("/create-aircraft", methods=["POST"])
    @cross_origin(supports_credentials=True)
    @login_required
    def create_aircraft():
        from_user_id = g.get("USER_ID")
        try:
            aircraft_create = AircraftCreate(**request.json)  # AircraftCreate should be a Pydantic model for validation
            aircraft = flight_service.register_aircraft(
                from_user_id,
                aircraft_create.name,
                aircraft_create.longitude,
                aircraft_create.latitude
            )
            if aircraft:
                return jsonify(
                    {"status": "success", "message": "Aircraft created", "aircraft": aircraft.model_dump()}), 200
            else:
                return invalid_data()
        except ValidationError:
            return invalid_data()

    @flight_blueprint.route("/create-location", methods=["POST"])
    @cross_origin(supports_credentials=True)
    @login_required
    def create_location():
        from_user_id = g.get("USER_ID")
        try:
            location_create = LocationCreate(**request.json)  # LocationCreate should be a Pydantic model for validation
            location = flight_service.register_location(
                from_user_id,
                location_create.longitude,
                location_create.latitude
            )
            if location:
                return jsonify(
                    {"status": "success", "message": "Location created", "location": location.model_dump()}), 200
            else:
                return invalid_data()
        except ValidationError:
            return invalid_data()

    @flight_blueprint.route("/create-flight", methods=["POST"])
    @cross_origin(supports_credentials=True)
    @login_required
    def create_flight():
        from_user_id = g.get("USER_ID")
        try:
            flight_create = FlightCreate(**request.json)  # FlightCreate should be a Pydantic model for validation
            flight = flight_service.register_flight(
                flight_create.aircraft_id,
                flight_create.from_airport_id,
                flight_create.to_airport_id,
                flight_create.gate_id,
                flight_create.number,
                flight_create.arrival_time,
                flight_create.departure_time
            )
            if flight:
                return jsonify({"status": "success", "message": "Flight created", "flight": flight.model_dump()}), 200
            else:
                return invalid_data()
        except ValidationError:
            return invalid_data()






