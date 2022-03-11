import json

from devispora.ovo_bases.bases.parse_bases import BaseParser
from devispora.ovo_bases.services.availability_service import process_base_request
from devispora.ovo_bases.services.auth_service import auth_request, retrieve_auth_details

base_parser = BaseParser()


def lambda_handler(event, context):
    print(event)
    (supplied_auth, auth_headers, auth_missing_response) = retrieve_auth_details(event)
    if not supplied_auth:
        return auth_missing_response
    (authorized, auth, error_response) = auth_request(auth_headers)
    if not authorized:
        return error_response
    # todo: Consume auth details
    if not base_parser.stored_facilities:
        base_parser.create_base_list()
    raw_body = json.loads(event['body'])
    print(raw_body)
    return process_base_request(base_parser, raw_body)
