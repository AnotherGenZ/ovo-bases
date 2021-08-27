from devispora.ovo_bases.exception.exceptions import RequestException
from devispora.ovo_bases.models.availability_result import AvailabilityResult
from devispora.ovo_bases.models.helpers.reservation_helper import create_temp_reservations
from devispora.ovo_bases.models.helpers.reservation_splitter import split_into_multi_reservations_when_needed
from devispora.ovo_bases.models.incoming_request import IncomingRequest
from devispora.ovo_bases.processor.availability_processor import check_if_available
from devispora.ovo_bases.services.dynamodb_service import retrieve_stored_reservations
from devispora.ovo_bases.validation.reservation_validation import validate_basic_time_rules


def incoming_reservation_check(incoming_request: IncomingRequest) -> AvailabilityResult:
    try:
        validate_basic_time_rules(incoming_request)
        temp_reservations = create_temp_reservations(incoming_request)
        final_reservations = split_into_multi_reservations_when_needed(temp_reservations)
        stored_reservations = retrieve_stored_reservations(final_reservations)
        availability_result = check_if_available(final_reservations, stored_reservations)
        return availability_result
    except RequestException:
        raise
