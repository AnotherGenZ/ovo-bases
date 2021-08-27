from devispora.ovo_bases.bases.parse_bases import BaseParser
from devispora.ovo_bases.exception.exceptions import RequestException
from devispora.ovo_bases.models.availability_result import AvailabilityResult
from devispora.ovo_bases.models.reservation_result import ReservationResult
from devispora.ovo_bases.models.reservations import ReservationType
from devispora.ovo_bases.models.responses import error_response, generic_response
from devispora.ovo_bases.models.helpers.incoming_request_helper import parse_incoming_request, create_pog_adjustments
from devispora.ovo_bases.models.incoming_request import RequestType, IncomingRequest
from devispora.ovo_bases.services.dynamodb_service import put_reservation
from devispora.ovo_bases.services.reservation_service import incoming_reservation_check


def process_base_request(base_parser: BaseParser, raw_body: {}):

    try:
        incoming_request = parse_incoming_request(base_parser, raw_body)
        if incoming_request.request_type is RequestType.Availability:
            return process_availability_request(incoming_request)
        if incoming_request.request_type is RequestType.Reservation:
            return process_reservation_request(incoming_request)
    except RequestException as rex:
        return error_response(400, rex)


def process_availability_request(incoming_request: IncomingRequest):
    """
    Processes the incoming request into desired reservations.
    Then checks if these can be completed.
    """
    availability_result = process_availability(incoming_request)
    return generic_response(availability_result)


def process_availability(incoming_request: IncomingRequest) -> AvailabilityResult:
    if incoming_request.reservation_type is ReservationType.POG:
        create_pog_adjustments(incoming_request)
        return incoming_reservation_check(incoming_request)
    else:
        return incoming_reservation_check(incoming_request)


def process_reservation_request(incoming_request: IncomingRequest):
    availability_result = process_availability(incoming_request)
    if len(availability_result.denied_reservations) > 0:
        return generic_response(availability_result)
    else:
        succeeded_reservations = []
        failed_reservations = []
        for reservation in availability_result.possible_reservations:
            response = put_reservation(reservation)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                succeeded_reservations.append(reservation)
            else:
                failed_reservations.append(reservation)
        return generic_response(ReservationResult(succeeded_reservations, failed_reservations))
