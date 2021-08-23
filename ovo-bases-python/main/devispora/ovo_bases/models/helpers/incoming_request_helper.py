from devispora.ovo_bases.bases.parse_bases import BaseParser
from devispora.ovo_bases.exception.exceptions import RequestException, RequestExceptionMessage
from devispora.ovo_bases.models.facility import Facility
from devispora.ovo_bases.models.helpers.facility_helper import find_facilities
from devispora.ovo_bases.models.helpers.reservation_helper import retrieve_reservation_type
from devispora.ovo_bases.models.incoming_request import IncomingRequest, RequestType, IncomingRequestContext
from devispora.ovo_bases.models.reservations import ReservationContext


def retrieve_request_type(request: str) -> RequestType:
    for item in RequestType.__members__.values():
        if item.value == request:
            return item
    raise RequestException(RequestExceptionMessage.RequestTypeNotRecognised, request)


def discover_request(raw_body: {}) -> RequestType:
    try:
        request = raw_body[IncomingRequestContext.RequestType]
        return retrieve_request_type(request)
    except KeyError:
        raise RequestException(RequestExceptionMessage.RequestTypeNotProvided)
    except RequestException:
        raise


def discover_bases(base_parser: BaseParser, raw_body: {}) -> [Facility]:
    try:
        request = raw_body[IncomingRequestContext.FacilityIds]
        return find_facilities(base_parser, request)
    except KeyError:
        raise RequestException(RequestExceptionMessage.FacilityNotProvided)
    except RequestException:
        raise


def retrieve_and_convert_time(raw_time, context: ReservationContext) -> int:
    """"The idea is that it will provide """
    try:
        return int(raw_time)
    except ValueError:
        raise RequestException(
            RequestExceptionMessage.IntValueError,
            f'Could not parse {context.value} to int with the provided value: {raw_time}'
        )


def parse_incoming_request(base_parser: BaseParser, raw_body: {}) -> IncomingRequest:
    try:
        facilities = discover_bases(base_parser, raw_body)
        request_type = discover_request(raw_body)
        reservation_type = retrieve_reservation_type(raw_body[ReservationContext.ReservationType])
        group_name = raw_body[ReservationContext.GroupName]
        incoming_request = IncomingRequest(
            facilities=facilities,
            request_type=request_type,
            reservation_type=reservation_type,
            group_name=group_name
        )
        if ReservationContext.StartTime.value in raw_body:
            start_time = raw_body[ReservationContext.StartTime]
            incoming_request.start_time = retrieve_and_convert_time(start_time, ReservationContext.StartTime)
        if ReservationContext.EndTime.value in raw_body:
            end_time = raw_body[ReservationContext.EndTime]
            incoming_request.end_time = retrieve_and_convert_time(end_time, ReservationContext.EndTime)
        return incoming_request
    except KeyError as ke:
        raise RequestException(RequestExceptionMessage.MissingReservationPart, ke.args[0])
    except RequestException:
        raise
