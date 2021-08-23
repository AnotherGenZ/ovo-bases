from enum import Enum

from devispora.ovo_bases.models.facility import Facility
from devispora.ovo_bases.models.reservations import ReservationType


class RequestType(str, Enum):
    Availability = 'availability'
    Reservation = 'reservation'


class IncomingRequestContext(str, Enum):
    FacilityIds = 'facility_ids'
    RequestType = 'request_type'


class IncomingRequest:
    """"Maps incoming request. The start and end time are optional as they aren't needed for certain requests"""
    def __init__(self, facilities: [Facility], reservation_type: ReservationType, request_type: RequestType, group_name: str,
                 start_time: int = None, end_time: int = None):
        self.facilities = facilities
        self.reservation_type = reservation_type
        self.request_type = request_type
        self.group_name = group_name
        if start_time is not None:
            self.start_time = start_time
        if end_time is not None:
            self.end_time = end_time
