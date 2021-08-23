from enum import Enum


class RequestException(Exception):
    def __init__(self, message, additional_message: str = None):
        self.message = message
        self.additional_message = additional_message

    def __str__(self):
        return self.message.value


class RequestExceptionMessage(str, Enum):
    FacilityNotProvided = 'It is required to provide at least one base in the request'
    FacilityCannotBeFound = 'Could not find the base'
    FacilitiesStoredNotFound = 'An issue arose when trying to find facilities'
    IntValueError = 'Expected an int but got something else'
    MissingReservationPart = 'The reservation is missing required information'
    MoreThanOneHourAgo = 'The start_time cannot be more than one hour ago'
    MoreThanThreeDAys = 'The start_time cannot be more than 3 days before the end_time'
    RequestTypeNotProvided = 'A request type must be provided'
    RequestTypeNotRecognised = 'The supplied request type could not be recognised'
    StartAfterEnd = 'The start_time cannot be after the end_time'
