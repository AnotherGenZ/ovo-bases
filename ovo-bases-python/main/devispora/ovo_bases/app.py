import json


def lambda_handler(event, context):
    #headers = event['headers']
    #raw_body = event['body']
    #print(raw_body)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "Region ": "ok"
        })
    }
