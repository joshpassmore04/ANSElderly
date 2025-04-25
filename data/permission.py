from enum import Enum


class PermissionType(str, Enum):
    ACCESS_ALL_FLIGHTS = "flights.access.all"
    ACCESS_ALL_AIRPORT_INFO = "flights.access.all.info"
    ADD_LUGGAGE_TO_OTHERS = "travellers.add.others.luggage"
    CREATE_FLIGHTS = "flights.create"
    CREATE_AIRPORT = "airports.create"
    CREATE_GATE = "gates.create"
    CREATE_AIRCRAFT = "airports.create"
    CAN_UPDATE_OTHERS_PERMISSIONS = "users.all.permissions.update"


class PermissionAction(str, Enum):
    GIVE = "give"
    REMOVE = "remove"
    CHECK_CURRENT_USER = "check_current_user"

class PermissionResult(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    EXISTS = "exists"

class Role(str, Enum):
    MANAGER = "manager"
    USER = "user"
