import datetime

from devispora.ovo_bases.exception.exceptions import RequestExceptionMessage, RequestException
from devispora.ovo_bases.models.incoming_request import IncomingRequest
from devispora.ovo_bases.tools.time_service import one_hour_in_seconds, three_days


def validate_basic_time_rules(reservation: IncomingRequest):
    """
    Validates if the reservation respects basic time rules
    """
    try:
        start_not_in_long_past(reservation)
        starts_before_end(reservation)
        start_not_far_from_end(reservation)
    except RequestException:
        raise


def start_not_in_long_past(incoming_request: IncomingRequest) -> bool:
    """Check if the reservation start time is not longer than 1 hour ago"""
    now_timestamp = create_current_epoch()
    difference = incoming_request.start_time - now_timestamp
    if incoming_request.start_time > now_timestamp:
        return True
    elif abs(difference) - one_hour_in_seconds >= 0:
        raise RequestException(message=RequestExceptionMessage.MoreThanOneHourAgo)
    else:
        return True


def start_not_far_from_end(incoming_request: IncomingRequest) -> bool:
    """Reservations cannot take longer than three days"""
    day_difference = incoming_request.end_time - incoming_request.start_time
    if day_difference > three_days:
        raise RequestException(message=RequestExceptionMessage.MoreThanThreeDAys)
    else:
        return True


def starts_before_end(incoming_request: IncomingRequest) -> bool:
    """Check if the reservation start time is not after the end time"""
    if incoming_request.start_time > incoming_request.end_time:
        raise RequestException(message=RequestExceptionMessage.StartAfterEnd)
    else:
        return True


def create_current_epoch() -> int:
    return int(datetime.datetime.now().timestamp())
