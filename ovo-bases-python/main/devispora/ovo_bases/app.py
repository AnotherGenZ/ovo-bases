import json


def lambda_handler(event, context):
    #headers = event['headers']
    #raw_body = event['body']
    #print(raw_body)

    # todo so pog:
    #  provides list with bases, type POG, wanted #now. a.k.a. between now and 1 hour of 45 minutes.
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "Region ": "ok"
        })
    }
