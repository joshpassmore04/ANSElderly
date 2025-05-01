from flask import Blueprint, request, jsonify, g
from flask_cors import cross_origin
from pydantic import ValidationError

from data.schema.attributes.aircraft import AircraftCreate
from data.schema.attributes.airport import AirportCreate
from data.schema.attributes.util import FlightAttributeAction
from data.schema.flight import FlightQuery, FlightCreate
from data.schema.attributes.gate import GateCreate
from data.schema.attributes.location import LocationCreate
from routes.util import login_required, invalid_data, authentication_required
from service.flight_service import FlightService
from service.user_service import UserService


def create_flight_blueprint(base_endpoint, user_service: UserService, flight_service: FlightService):
    flight_blueprint = Blueprint('airport', __name__, url_prefix=base_endpoint + '/airport')

    @flight_blueprint.route("/get-flight", methods=["POST"])
    @cross_origin(supports_credentials=True)
    @login_required
    def get():
        try:
            flight_query = FlightQuery(**request.json)
            if flight_query:
                flights = flight_service.get_flights_by_attribute(flight_query.attribute, flight_query.value)
                if flights:
                    return jsonify(
                        {"status": "success", "message": "Flights found", "flights": flights}), 200
                return jsonify({"status": "failure", "message": "Flights not found"}), 404
            else:
                return invalid_data()
        except ValidationError:
            return invalid_data()

    # AIRPORT
    @flight_blueprint.route("/airport", methods=["POST"])
    @cross_origin(supports_credentials=True)
    @login_required
    def create_airport():
        from_user_id = g.get("USER_ID")
        try:
            airport_create = AirportCreate(**request.json)
            airport = flight_service.register_airport(
                from_user_id, airport_create.name, airport_create.location_id
            )
            if airport:
                return jsonify({
                    "status": "success",
                    "message": "Airport created",
                    "airport": airport.model_dump()
                }), 200
            else:
                return invalid_data()
        except ValidationError as e:
            print(e)
            return invalid_data()

    @flight_blueprint.route("/airport", methods=["GET"])
    @cross_origin(supports_credentials=True)
    @login_required
    def get_all_airports():
        airports = flight_service.get_all_airports()
        return jsonify({
            "status": "success",
            "message": "Airports found",
            "items": [airport.model_dump() for airport in airports]
        }), 200

    # GATE
    @flight_blueprint.route("/gate", methods=["POST"])
    @cross_origin(supports_credentials=True)
    @login_required
    def create_gate():
        from_user_id = g.get("USER_ID")
        try:
            gate_create = GateCreate(**request.json)
            gate = flight_service.register_gate(
                from_user_id,
                gate_create.number,
                gate_create.opening_time,
                gate_create.location_id
            )
            if gate:
                return jsonify({"status": "success", "message": "Gate created", "gate": gate.model_dump()}), 200
            else:
                return authentication_required()
        except ValidationError:
            return invalid_data()

    @flight_blueprint.route("/gate", methods=["GET"])
    @cross_origin(supports_credentials=True)
    @login_required
    def get_all_gates():
        gates = flight_service.get_all_gates()
        return jsonify({
            "status": "success",
            "message": "Gates found",
            "items": [gate.model_dump() for gate in gates]
        }), 200

    # AIRCRAFT
    @flight_blueprint.route("/aircraft", methods=["POST"])
    @cross_origin(supports_credentials=True)
    @login_required
    def create_aircraft():
        from_user_id = g.get("USER_ID")
        try:
            aircraft_create = AircraftCreate(**request.json)
            aircraft = flight_service.register_aircraft(
                from_user_id,
                aircraft_create.name,
                aircraft_create.capacity,
                aircraft_create.location_id
            )
            if aircraft:
                return jsonify({
                    "status": "success",
                    "message": "Aircraft created",
                    "aircraft": aircraft.model_dump()
                }), 200
            else:
                return authentication_required()
        except ValidationError:
            return invalid_data()

    @flight_blueprint.route("/aircraft", methods=["GET"])
    @cross_origin(supports_credentials=True)
    @login_required
    def get_all_aircraft():
        aircraft_list = flight_service.get_all_aircraft()
        return jsonify({
            "status": "success",
            "message": "Aircraft found",
            "items": [a.model_dump() for a in aircraft_list]
        }), 200

    # LOCATION
    @flight_blueprint.route("/location", methods=["POST"])
    @cross_origin(supports_credentials=True)
    @login_required
    def create_location():
        from_user_id = g.get("USER_ID")
        try:
            location_create = LocationCreate(**request.json)
            location = flight_service.register_location(
                from_user_id,
                longitude=location_create.longitude,
                name=location_create.name,
                latitude=location_create.latitude
            )
            if location:
                return jsonify({
                    "status": "success",
                    "message": "Location created",
                    "location": location.model_dump()
                }), 200
            else:
                return authentication_required()
        except ValidationError as e:
            return invalid_data()

    @flight_blueprint.route("/location", methods=["GET"])
    @cross_origin(supports_credentials=True)
    @login_required
    def get_all_locations():
        locations = flight_service.get_all_locations()
        return jsonify({
            "status": "success",
            "message": "Locations found",
            "items": [loc.model_dump() for loc in locations]
        }), 200

    @flight_blueprint.route("/create-flight", methods=["POST"])
    @cross_origin(supports_credentials=True)
    @login_required
    def create_flight():
        from_user_id = g.get("USER_ID")
        try:
            flight_create = FlightCreate(**request.json)  # FlightCreate should be a Pydantic model for validation
            flight = flight_service.register_flight(
                from_user_id,
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
                return authentication_required()
        except ValidationError as e:
            print(e.errors)
            return invalid_data()

    return flight_blueprint





