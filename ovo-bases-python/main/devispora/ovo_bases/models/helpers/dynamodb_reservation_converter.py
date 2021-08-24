from devispora.ovo_bases.models.helpers.reservation_helper import retrieve_reservation_type, \
    retrieve_reservation_continent
from devispora.ovo_bases.models.reservations import Reservation, ReservationContext


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
        reservation_day=reservation_item[ReservationContext.ReservationDay].__int__()
    )
