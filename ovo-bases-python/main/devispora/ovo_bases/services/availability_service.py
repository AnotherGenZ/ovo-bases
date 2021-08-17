from devispora.ovo_bases.exception.exceptions import RequestException
from devispora.ovo_bases.models.responses import error_response
from devispora.ovo_bases.services.request_service import discover_request, RequestType


def process_base_request(raw_body: {}):
    try:
        request_type = discover_request(raw_body)
        if request_type is RequestType.Availability:
            process_availability_request(raw_body)
            pass
        if request_type is RequestType.Reservation:
            process_reservation_request(raw_body)
            pass
    except RequestException as rex:
        return error_response(rex)


def process_availability_request(raw_body: {}):
    pass


def process_reservation_request(raw_body: {}):
    pass
