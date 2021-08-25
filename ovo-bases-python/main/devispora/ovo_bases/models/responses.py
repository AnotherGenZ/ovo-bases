import json

import jsonpickle

from devispora.ovo_bases.exception.exceptions import RequestException

content_json = {"content-type": "application/json"}


def error_response(status_code: int, rex: RequestException):
    response = {
        'statusCode': status_code,
        'headers': content_json,
    }
    if rex.additional_message is not None:
        response['body'] = json.dumps({
            rex.message.name: f'{rex.message.value}: {rex.additional_message}'
        })
    else:
        response['body'] = json.dumps({
            rex.message.name: rex.message.value
        })
    return response


def generic_response(content):
    return {
        'statusCode': 200,
        'headers': content_json,
        'body': json.dumps({
            'result': json.loads(jsonpickle.encode(content, unpicklable=False))
        })
    }
