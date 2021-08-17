from enum import Enum

from devispora.ovo_bases.exception.exceptions import RequestException, RequestExceptionMessage


class RequestType(str, Enum):
    Availability = 'Availability'
    Reservation = 'Reservation'


def retrieve_request_type(request: str) -> RequestType:
    for item in RequestType.__members__.values():
        if item.value == request:
            return item
    raise RequestException(RequestExceptionMessage.RequestTypeNotRecognised, request)


def discover_request(raw_body: {}) -> RequestType:
    try:
        request = raw_body['request_type']
        return retrieve_request_type(request)
    except KeyError:
        raise RequestException(RequestExceptionMessage.RequestTypeNotProvided)
    except RequestException:
        raise
