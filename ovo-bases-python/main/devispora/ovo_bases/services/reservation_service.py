from devispora.ovo_bases.exception.exceptions import RequestException
from devispora.ovo_bases.models.helpers.reservation_helper import create_temp_reservations
from devispora.ovo_bases.models.incoming_request import IncomingRequest
from devispora.ovo_bases.validation.reservation_validation import validate_basic_time_rules

# todo These basically have to make no distinction between what is happening. Just


def incoming_pog_reservation(incoming_request: IncomingRequest) -> IncomingRequest:
    """"Creates a reservation based on the current time for the next 45min-1hour depending on availability"""
    # todo
    #  Set times to current + 45min - 1 hour
    #  Create temp reservations
    #  Do calls to DB to check them all
    #  Get ready to return availability of each.
    pass


def incoming_reservation(incoming_request: IncomingRequest):
    try:
        validate_basic_time_rules(incoming_request)
        temp_reservations = create_temp_reservations(incoming_request)
        # todo actually process the reservations
    except RequestException:
        raise
        # todo check for calendar availability
    pass


