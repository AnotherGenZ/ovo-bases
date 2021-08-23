from devispora.ovo_bases.exception.exceptions import RequestException, RequestExceptionMessage
from devispora.ovo_bases.models.incoming_request import IncomingRequest
from devispora.ovo_bases.models.reservations import Reservation, ReservationType, ReservationContinent, \
    ReservationContext
from devispora.ovo_bases.tools.time_service import get_event_day_from_timestamp, day_in_seconds, grab_next_day


def create_reservations_list(dynamodb_items: [dict]) -> [Reservation]:
    reservation_list = []
    for item in dynamodb_items:
        reservation_list.append(reservation_from_dynamodb_dict(item))
    return reservation_list


def reservation_from_dynamodb_dict(reservation_item: dict) -> Reservation:
    """
    Transforms the returned object from DynamoDB to the python version of a Reservation.
    DynamoDB through Boto3 serializes all numbers to Decimal, but we don't like Decimal.
    """
    return Reservation(
        reservation_type=retrieve_reservation_type(reservation_item[ReservationContext.ReservationType]),
        facility_id=reservation_item[ReservationContext.BaseID].__int__(),
        continent=retrieve_reservation_continent(reservation_item[ReservationContext.ReservationType.Continent]),
        group_name=reservation_item[ReservationContext.GroupName],
        start_time=reservation_item[ReservationContext.StartTime].__int__(),
        end_time=reservation_item[ReservationContext.EndTime].__int__(),
        reservation_day=reservation_item[ReservationContext.ReservationType].__int__()
    )


def retrieve_reservation_type(reservation_type: str) -> ReservationType:
    for item in ReservationType.__members__.values():
        if item.value == reservation_type:
            return item
    raise RequestException(RequestExceptionMessage.RequestTypeNotRecognised, reservation_type)


def retrieve_reservation_continent(continent: str) -> ReservationContinent:
    for item in ReservationContinent.__members__.values():
        if item.value == continent:
            return item


def check_reservation_day_limit(reservation: Reservation) -> [ReservationContinent]:
    """"Returns a list of reservations. Depending on the length of the reservation it will return more than one"""
    start_day = get_event_day_from_timestamp(reservation.start_time)
    end_day = get_event_day_from_timestamp(reservation.end_time)
    if start_day == end_day:
        return [reservation]
    else:
        return reservation_splitter(reservation, start_day, end_day)


def reservation_splitter(reservation: Reservation, start_day: int, end_day: int) -> [Reservation]:
    """"Will split into multiple reservations based on the amount of days required"""
    # todo create massive amounts of tests for this one
    reservations = []
    checked_day = start_day
    while checked_day <= end_day:
        calibrated_day = grab_next_day(checked_day)
        if calibrated_day >= reservation.end_time:
            # make this final reservation
            reservations.append(create_similar_reservation(reservation, checked_day, reservation.end_time))
            return reservations
        else:
            if len(reservations) == 0:
                # Drop in the first day
                reservations.append(create_similar_reservation(reservation, reservation.start_time, calibrated_day))
            # turn into 1 new reservation and keep iterating.
            else:
                reservations.append(create_similar_reservation(reservation, checked_day, calibrated_day))
            checked_day = calibrated_day


def create_similar_reservation(old_reservation: Reservation, start_time: int, end_time: int) -> Reservation:
    return Reservation(
        facility_id=old_reservation.facility_id,
        continent=old_reservation.continent,
        group_name=old_reservation.group_name,
        reservation_type=old_reservation.reservation_type,
        start_time=start_time,
        end_time=end_time
    )

    # create an array of days for reservations
    # need to know increments of day
    # first reservation would be start normal reservation and end of day.
    # next day would be the end of that reservation
    # then the following reservation would be until end date or end of *yet* that day.
    # for every reservation we check if the new end day would be before or after the end_day
    # if yes, make final reservation, otherwise continue.

    #todo Split them up for every day. For every day create a new reservation, max is 3


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
