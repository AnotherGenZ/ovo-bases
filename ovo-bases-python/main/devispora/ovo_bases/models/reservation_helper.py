import datetime

from devispora.ovo_bases.models.reservations import Reservation, ReservationType, ReservationContinent
from devispora.ovo_bases.tools.time_service import get_event_day_from_timestamp


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
        event_type=retrieve_reservation_type(reservation_item['event_type']),
        base_id=reservation_item['base_id'].__int__(),
        continent=retrieve_reservation_continent(reservation_item['continent']),
        group_name=reservation_item['group_name'],
        start_time=reservation_item['start_time'].__int__(),
        end_time=reservation_item['end_time'].__int__(),
        event_day=reservation_item['event_day'].__int__()
    )


def retrieve_reservation_type(event_type: str) -> ReservationType:
    for item in ReservationType.__members__.values():
        if item.value == event_type:
            return item


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


def reservation_splitter(reservation: Reservation, start_day: int, end_day: int) -> [ReservationContinent]:
    """"Will split into multiple reservations based on the amount of days required"""
    reservations = []
    #start_day_date = retrieve_day(start_day)

