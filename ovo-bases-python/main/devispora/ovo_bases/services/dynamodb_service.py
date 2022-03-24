import boto3
from boto3.dynamodb.conditions import Key

from devispora.ovo_bases.models.auth import Auth
from devispora.ovo_bases.models.helpers.dynamodb_reservation_converter import create_reservations_list
from devispora.ovo_bases.models.helpers.reservation_helper import create_reservation_query_pool
from devispora.ovo_bases.models.reservations import Reservation, reservation_table_name, ReservationContext, \
    ReservationQuery

dynamodb = boto3.resource('dynamodb')

class DynamoDBService:
    pass


def reservations_of_day(query: ReservationQuery) -> [Reservation]:
    table = dynamodb.Table(reservation_table_name)
    if query.multi_continent:
        expression = Key('reservation_day').eq(query.reservation_day)
    else:
        expression = Key('reservation_day').eq(query.reservation_day) & Key('continent').eq(query.continent)
    response = table.query(
        IndexName='reservation_day_continent',
        KeyConditionExpression=expression
    )
    return response['Items']


def retrieve_stored_reservations(incoming_reservation: [Reservation]):
    query_pool = create_reservation_query_pool(incoming_reservation)
    stored_reservations = []
    for query in query_pool:
        found_reservations = reservations_of_day(query)
        stored_reservations.extend(create_reservations_list(found_reservations))
    return stored_reservations


def put_reservation(reservation: Reservation, auth: Auth):
    table = dynamodb.Table(reservation_table_name)
    response = table.put_item(
        Item={
            ReservationContext.ReservationID.value: reservation.reservation_id,
            ReservationContext.TokenID.value: auth.token_id,
            ReservationContext.BaseID.value: reservation.facility_id,
            ReservationContext.Continent.value: reservation.continent.value,
            ReservationContext.GroupName.value: reservation.group_name,
            ReservationContext.ReservationType.value: reservation.reservation_type.value,
            ReservationContext.ReservationDay.value: reservation.reservation_day,
            ReservationContext.StartTime.value: reservation.start_time,
            ReservationContext.EndTime.value: reservation.end_time
        }
    )
    return response
