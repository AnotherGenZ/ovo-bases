from devispora.ovo_bases.exception.exceptions import RequestException, RequestExceptionMessage
from devispora.ovo_bases.models.incoming_request import IncomingRequest
from devispora.ovo_bases.models.reservations import Reservation, ReservationType, ReservationContinent, ReservationQuery


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


def create_reservation_query_pool(reservations: [Reservation]) -> [ReservationQuery]:
    """Transform the reservations into a dict that can be used to create ReservationQuery objects"""
    query_dict = create_query_dict(reservations)
    queries = []
    for entry in query_dict:
        if len(query_dict[entry]) > 1:
            queries.append(ReservationQuery(
                reservation_day=entry, multi_continent=True)
            )
        else:
            continent_entry = list(query_dict[entry])[0]
            queries.append(ReservationQuery(
                reservation_day=entry, multi_continent=False, continent=continent_entry)
            )
    return queries


def create_query_dict(reservations: [Reservation]) -> dict:
    """
    Creates a dict with a set inside of it and will attempt to add to it dynamically.
    """
    query_dict = {}
    for reservation in reservations:
        if reservation.reservation_day not in query_dict:
            query_dict[reservation.reservation_day] = {reservation.continent}
        else:
            query_dict[reservation.reservation_day].add(reservation.continent)
    return query_dict
