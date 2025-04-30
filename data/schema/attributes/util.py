from enum import Enum


class FlightAttributeAction(str, Enum):
    CREATE = "create"
    ALL = "all"
    DELETE = "delete"