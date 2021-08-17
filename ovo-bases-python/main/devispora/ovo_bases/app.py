import json

from devispora.ovo_bases.services.availability_service import process_base_request


def lambda_handler(event, context):
    #headers = event['headers']
    # todo jwt validation
    raw_body = event['body']
    return process_base_request(raw_body)
