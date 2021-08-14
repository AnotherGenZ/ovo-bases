import datetime

from devispora.ovo_bases.exception.exceptions import ReservationExceptionMessage, ReservationException
from devispora.ovo_bases.models.reservations import Reservation
from devispora.ovo_bases.tools.time_service import one_hour_in_seconds, three_days


class ReservationValidation:
    def __init__(self, valid: bool, error_message: ReservationExceptionMessage = None):
        self.valid = valid
        self.error_message = error_message


def validate_basic_time_rules(reservation: Reservation) -> ReservationValidation:
    """
    Validates if the reservation respects basic time rules
    """
    try:
        start_not_in_long_past(reservation)
        starts_before_end(reservation)
        start_not_far_from_end(reservation)
        return ReservationValidation(valid=True)
    except ReservationException as te:
        return ReservationValidation(valid=False, error_message=te.message)


def start_not_in_long_past(reservation: Reservation) -> bool:
    """Check if the reservation start time is not longer than 1 hour ago"""
    now_timestamp = create_current_epoch()
    difference = reservation.start_time - now_timestamp
    if reservation.start_time > now_timestamp:
        return True
    elif abs(difference) - one_hour_in_seconds >= 0:
        raise ReservationException(message=ReservationExceptionMessage.MoreThanOneHourAgo)
    else:
        return True


def start_not_far_from_end(reservation: Reservation) -> bool:
    """Reservations cannot take longer than three days"""
    day_difference = reservation.end_time - reservation.start_time
    if day_difference > three_days:
        raise ReservationException(message=ReservationExceptionMessage.MoreThanThreeDAys)
    else:
        return True


def starts_before_end(reservation: Reservation) -> bool:
    """Check if the reservation start time is not after the end time"""
    if reservation.start_time > reservation.end_time:
        raise ReservationException(message=ReservationExceptionMessage.StartAfterEnd)
    else:
        return True


def create_current_epoch() -> int:
    return int(datetime.datetime.now().timestamp())
