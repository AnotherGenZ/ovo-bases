import json
import unittest

import boto3
from boto3.dynamodb.conditions import Key

from devispora.ovo_bases.models.reservations import Reservation, reservation_table_name, ReservationType, \
    ReservationContinent
from devispora.ovo_bases.services.dynamodb_service import put_reservation, reservations_of_day


class DynamoDBServiceTest(unittest.TestCase):
    """"Just some random DynamoDB trial tests"""

    def test_check_if_available(self):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(reservation_table_name)
        # response = table.query(
        #     IndexName='base_start_time',
        #     KeyConditionExpression=Key('base_id').eq(234)
        #     & Key('start_time').between(12456788, 12456790)
        # )
        # result = response['Items']
        # print(result)

        response2 = table.query(
            IndexName='reservation_day_continent',
            KeyConditionExpression=Key('reservation_day').eq(12441600)
            # & Key('continent').eq(ReservationContinent.Amerish.value)
        )
        result3 = response2['Items']
        print(result3)
        pass

    def test_put_reservation(self):
        reservation = Reservation(
            facility_id=232,
            continent=ReservationContinent.Amerish,
            group_name='TEST',
            reservation_type=ReservationType.Scrim,
            start_time=12456788,
            end_time=12456790
        )
        # result = reservations_of_day(reservation)
        # print(result[0]['reservation_type'])
        #result = put_reservation(reservation)
        #print(result)


if __name__ == '__main__':
    unittest.main()
