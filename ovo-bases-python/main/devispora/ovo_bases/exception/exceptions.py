from enum import Enum


class ReservationException(Exception):
    def __init__(self, message, additional_message: str = None):
        self.message = message
        self.additional_message = additional_message

    def __str__(self):
        return self.message.value


class ReservationExceptionMessage(str, Enum):
    MissingReservationPart = 'The reservation is missing required information'
    MoreThanOneHourAgo = 'The start_time cannot be more than one hour ago'
    MoreThanThreeDAys = 'The start_time cannot be more than 3 days before the end_time'
    StartAfterEnd = 'The start_time cannot be after the end_time'
