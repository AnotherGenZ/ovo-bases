import datetime
import unittest
import uuid

import requests
import boto3

from devispora.ovo_bases.models.reservations import ReservationContext

base = ''
api_key = ''


class AirTableAPITest(unittest.TestCase):
    # Max 5 per second, returns a 429 code if that happens. 30 second cooldown
    # auth.
    # We're going to use headers. Authorization: Bearer APIKEY
    #def test_connection(self):
        # headers = {'Authorization': f'Bearer {api_key}'}
        # print(datetime.datetime.now())
        # r = requests.get('https://api.airtable.com/v0/app7xwgUxFyFJBtzY/Reservations?maxRecords=3',
        #                  headers=headers)
        # print(r.json())
        # print(datetime.datetime.now())
        # r2 = requests.get('https://api.airtable.com/v0/app7xwgUxFyFJBtzY/Reservations?maxRecords=3',
        #                   headers=headers)
        # print(r2.json())
        # print(datetime.datetime.now())
        # r3 = requests.get('https://api.airtable.com/v0/app7xwgUxFyFJBtzY/Reservations?maxRecords=3',
        #                   headers=headers)
        # print(r3.json())
        # print(datetime.datetime.now())


    def test_dynamodb(self):
        dynamodb = boto3.resource('dynamodb')
        partition_key = str(uuid.uuid4())
        table = dynamodb.Table('reservations')
        table.put_item(
            Item={
                ReservationContext.ReservationID.value: partition_key,
                ReservationContext.BaseID.value: 2352345,
                ReservationContext.GroupName.value: 'TEST',
                ReservationContext.StartTime.value: 1627084800,
                ReservationContext.EndTime.value: 1627092000
            }
        )


if __name__ == '__main__':
    unittest.main()
