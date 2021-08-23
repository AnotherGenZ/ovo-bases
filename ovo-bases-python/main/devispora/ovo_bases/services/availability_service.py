from devispora.ovo_bases.bases.parse_bases import BaseParser
from devispora.ovo_bases.exception.exceptions import RequestException
from devispora.ovo_bases.models.reservations import ReservationType
from devispora.ovo_bases.models.responses import error_response
from devispora.ovo_bases.models.helpers.incoming_request_helper import parse_incoming_request
from devispora.ovo_bases.models.incoming_request import RequestType, IncomingRequest
from devispora.ovo_bases.services.reservation_service import incoming_pog_reservation


def process_base_request(base_parser: BaseParser, raw_body: {}):
    # todo return response on both
    try:
        incoming_request = parse_incoming_request(base_parser, raw_body)
        if incoming_request.request_type is RequestType.Availability:
            process_availability_request(incoming_request)
            pass
        if incoming_request.request_type is RequestType.Reservation:
            process_reservation_request(incoming_request)
            pass
    except RequestException as rex:
        return error_response(rex)


def process_availability_request(incoming_request: IncomingRequest):
    if incoming_request.reservation_type is ReservationType.POG:
        pog_request = incoming_pog_reservation(incoming_request)
        # then process it like a pog search.
    # make distinction between pog and normal request?
    pass


def process_reservation_request(incoming_request: IncomingRequest):
    pass

