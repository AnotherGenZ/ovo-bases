import uuid
from enum import Enum

from devispora.ovo_bases.tools.time_service import get_event_day_from_timestamp

reservation_table_name = 'reservations'


class ReservationContext(str, Enum):
    """"Needs to mirror the names of reservation"""
    # todo create test that verifies that reservation contains this.
    ReservationID = 'reservation_id'
    BaseID = 'base_id'
    Continent = 'continent'
    GroupName = 'group_name'
    ReservationType = 'reservation_type'
    ReservationDay = 'reservation_day'
    StartTime = 'start_time'
    EndTime = 'end_time'

    def __getstate__(self):
        """Allows JsonPickle just to retrieve the value"""
        return self.value


class ReservationType(str, Enum):
    LargeEvent = 'large_event'
    Scrim = 'scrim'
    Training = 'training'
    POG = 'pog'

    def __getstate__(self):
        """Allows JsonPickle just to retrieve the value"""
        return self.value


class ReservationContinent(str, Enum):
    Indar = 'indar'
    Hossin = 'hossin'
    Amerish = 'amerish'
    Esamir = 'esamir'
    Koltyr = 'koltyr'

    def __getstate__(self):
        """Allows JsonPickle just to retrieve the value"""
        return self.value


def create_id() -> str:
    return str(uuid.uuid4())


class Reservation:
    def __init__(self, facility_id: int, continent: ReservationContinent, group_name: str,
                 reservation_type: ReservationType, start_time: int, end_time: int, reservation_day: int = None):
        self.reservation_id = create_id()
        self.facility_id = facility_id
        self.continent = continent
        self.group_name = group_name
        self.reservation_type = reservation_type
        self.start_time = start_time
        self.end_time = end_time
        if reservation_day is None:
            self.reservation_day = get_event_day_from_timestamp(start_time)
        else:
            self.reservation_day = reservation_day


class ReservationQuery:
    """"
    Subset of reservation used to query for availability in the continent
    If multi-continent is enabled
    """
    def __init__(self, reservation_day: int, multi_continent: bool, continent: ReservationContinent = None):
        self.reservation_day = reservation_day
        self.multi_continent = multi_continent
        self.continent = continent
