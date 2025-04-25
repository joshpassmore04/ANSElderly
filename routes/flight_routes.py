from flask import Blueprint, request, jsonify, g
from flask_cors import cross_origin
from pydantic import ValidationError

from data.permission import PermissionType
from data.schema.flight import FlightOut
from orm.airport.flight import Flight
from orm.user.traveller import Traveller
from routes.util import login_required
from service.errors.invalid_data import InvalidData
from service.flight_service import FlightService
from service.user_service import UserService


def create_flight_blueprint(base_endpoint, user_service: UserService, flight_service: FlightService):
    flight_blueprint = Blueprint('flights', __name__, url_prefix=base_endpoint + '/flights')

    @flight_blueprint.route("/get", methods=["GET"])
    @cross_origin(supports_credentials=True)
    @login_required
    def get_by_number():

        def return_flight(flight_in: Flight):
            flight_out = FlightOut.model_validate(flight_in)
            return jsonify(
                {"status": "success", "flight": flight_out.model_dump()}
            ), 200

        try:
            user_id = g.get("USER_ID")
            flight_number = request.args.get("number")

            flight = flight_service.get_flight_by_number(flight_number)

            if not flight_number or not flight:
                raise InvalidData

            user = user_service.get_user_by_id(user_id)
            if isinstance(user, Traveller):
                if user.flight_id == flight.id:
                    return return_flight(flight)
                else:
                    raise InvalidData
            else:
                if user_service.has_permission(user_id, PermissionType.ACCESS_ALL_FLIGHTS):
                    return return_flight(flight)
                else:
                    raise InvalidData
        except ValidationError:
            raise InvalidData

