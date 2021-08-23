import json

from devispora.ovo_bases.bases.parse_bases import BaseParser
from devispora.ovo_bases.services.availability_service import process_base_request


base_parser: BaseParser()

def lambda_handler(event, context):
    #headers = event['headers']
    # todo jwt validation
    if not base_parser.stored_facilities:
        base_parser.create_base_list()
    raw_body = event['body']
    return process_base_request(base_parser, raw_body)
