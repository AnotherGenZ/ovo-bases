import json

from devispora.ovo_bases.bases.parse_bases import BaseParser
from devispora.ovo_bases.services.availability_service import process_base_request
from devispora.ovo_bases.services.auth_service import auth_request


base_parser: BaseParser()

def lambda_handler(event, context):
    headers = event['headers']
    
    (authed, auth, response) = auth_request(headers['Authorization'])

    if not authed:
        return response
    
    #todo: Consume auth details

    if not base_parser.stored_facilities:
        base_parser.create_base_list()
    raw_body = event['body']
    return process_base_request(base_parser, raw_body)
