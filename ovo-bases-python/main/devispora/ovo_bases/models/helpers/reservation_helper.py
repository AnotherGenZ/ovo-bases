from devispora.ovo_bases.exception.exceptions import RequestException, RequestExceptionMessage
from devispora.ovo_bases.models.incoming_request import IncomingRequest
from devispora.ovo_bases.models.reservations import Reservation, ReservationType, ReservationContinent


def retrieve_reservation_type(reservation_type: str) -> ReservationType:
    for item in ReservationType.__members__.values():
        if item.value == reservation_type:
            return item
    raise RequestException(RequestExceptionMessage.RequestTypeNotRecognised, reservation_type)


def retrieve_reservation_continent(continent: str) -> ReservationContinent:
    for item in ReservationContinent.__members__.values():
        if item.value == continent:
            return item


def create_temp_reservations(incoming_request: IncomingRequest) -> [Reservation]:
    """"Splits request into a reservation for each base"""
    reservations = []
    for facility in incoming_request.facilities:
        reservations.append(
            Reservation(
                facility_id=facility.facility_id,
                continent=facility.zone_id,
                reservation_type=incoming_request.reservation_type,
                group_name=incoming_request.group_name,
                start_time=incoming_request.start_time,
                end_time=incoming_request.end_time
            )
        )
    return reservations
