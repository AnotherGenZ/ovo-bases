import boto3
from boto3.dynamodb.conditions import Key

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
        expression = Key('start_day').eq(query.reservation_day)
    else:
        expression = Key('start_day').eq(query.reservation_day) & Key('continent').eq(query.continent)
    response = table.query(
        IndexName='start_day_continent',
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


def put_reservation(reservation: Reservation):
    table = dynamodb.Table(reservation_table_name)
    response = table.put_item(
        Item={
            ReservationContext.ReservationID.value: reservation.reservation_id,
            ReservationContext.BaseID.value: reservation.facility_id,
            ReservationContext.Continent.value: reservation.continent,
            ReservationContext.GroupName.value: reservation.group_name,
            ReservationContext.ReservationType.value: reservation.reservation_type,
            ReservationContext.ReservationDay.value: reservation.reservation_day,
            ReservationContext.StartTime.value: reservation.start_time,
            ReservationContext.EndTime.value: reservation.end_time
        }
    )
    return response





# {'ResponseMetadata': {'RequestId': '3VSI4BO2MQFNAE0LHVA9TQDKMJVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Sat, 24 Jul 2021 03:22:34 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '2', 'connection': 'keep-alive', 'x-amzn-requestid': '3VSI4BO2MQFNAE0LHVA9TQDKMJVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '2745614147'}, 'RetryAttempts': 0}}
