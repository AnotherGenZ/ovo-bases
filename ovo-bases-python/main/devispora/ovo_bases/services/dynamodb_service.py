import boto3
from boto3.dynamodb.conditions import Key

from devispora.ovo_bases.models.reservations import Reservation, reservation_table_name, ReservationContext, \
    ReservationContinent

dynamodb = boto3.resource('dynamodb')

class DynamoDBService:
    pass


def reservations_of_day(reservation: Reservation) -> [Reservation]:
    table = dynamodb.Table(reservation_table_name)
    response = table.query(
        IndexName='start_day_continent',
        KeyConditionExpression=Key('start_day').eq(reservation.event_day)
        & Key('continent').eq(reservation.continent)
    )
    return response['Items']


def check_if_available(reservation: Reservation):
    # we need to check if there's any crossover for the next day
    # which I guess could be done by cehcking?
    reservations = reservations_of_day(reservation)

    pass
    # Predicted timewindow. Maybe 1 day before, one after.
    # Then filter down if the time period within each of them:
    # if start time or end time is within start-end time
    # then scream hell and fury and deny
    # Secondarily: Risky base-id check. (embed instead of lookup?)


def put_reservation(reservation: Reservation):
    table = dynamodb.Table(reservation_table_name)
    response = table.put_item(
        Item={
            ReservationContext.ReservationID.value: reservation.reservation_id,
            ReservationContext.BaseID.value: reservation.base_id,
            ReservationContext.Continent.value: reservation.continent,
            ReservationContext.GroupName.value: reservation.group_name,
            ReservationContext.EventType.value: reservation.event_type,
            ReservationContext.EventDay.value: reservation.event_day,
            ReservationContext.StartTime.value: reservation.start_time,
            ReservationContext.EndTime.value: reservation.end_time
        }
    )
    return response





# {'ResponseMetadata': {'RequestId': '3VSI4BO2MQFNAE0LHVA9TQDKMJVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Sat, 24 Jul 2021 03:22:34 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '2', 'connection': 'keep-alive', 'x-amzn-requestid': '3VSI4BO2MQFNAE0LHVA9TQDKMJVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '2745614147'}, 'RetryAttempts': 0}}
