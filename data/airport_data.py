from datetime import datetime
from abc import ABC, abstractmethod
from typing import List

from orm.airport.airport import Airport
from orm.user.luggage import Luggage


class AirportData(ABC):

    @abstractmethod
    def get_flights_after(self, time: datetime = datetime.now()) -> List[Airport]:
        pass

    @abstractmethod
    def get_flights_before(self, time: datetime = datetime.now()) -> List[Airport]:
        pass

    @abstractmethod
    def get_luggage_for(self, traveller_id: int) -> List[Luggage]:
        pass
