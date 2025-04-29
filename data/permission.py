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
    CAN_UPDATE_OTHERS_ROLES = "users.all.roles.update"
    CAN_CHECK_OTHER_ROLES = "users.all.roles.check"

class RolePermissions(Enum):
    MANAGER = (
        "manager",
        [
            PermissionType.ACCESS_ALL_FLIGHTS,
            PermissionType.ACCESS_ALL_AIRPORT_INFO,
            PermissionType.ADD_LUGGAGE_TO_OTHERS,
            PermissionType.CREATE_FLIGHTS,
            PermissionType.CREATE_AIRPORT,
            PermissionType.CREATE_GATE,
            PermissionType.CREATE_AIRCRAFT,
            PermissionType.CAN_UPDATE_OTHERS_PERMISSIONS,
            PermissionType.CAN_UPDATE_OTHERS_ROLES,
            PermissionType.CAN_CHECK_OTHER_ROLES,
        ],
    )

    def __init__(self, label: str, permissions: list[PermissionType]):
        self.label = label
        self.permissions = permissions

    @classmethod
    def from_label(cls, label: str):
        for role in cls:
            if role.label == label:
                return role
        raise ValueError(f"Invalid role label: {label}")


class PermissionAction(str, Enum):
    GIVE = "give"
    REMOVE = "remove"
    CHECK_CURRENT_USER = "check_current_user"

class PermissionResult(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    EXISTS = "exists"
