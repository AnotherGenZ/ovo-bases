from devispora.ovo_bases.bases.parse_bases import BasesParser
from devispora.ovo_bases.bases.search_base import retrieve_base_by_id
from devispora.ovo_bases.exception.exceptions import RequestException, RequestExceptionMessage
from devispora.ovo_bases.models.facility_helper import find_reservation_continent_by_zone_id
from devispora.ovo_bases.models.reservations import Reservation, ReservationContext
from devispora.ovo_bases.validation.reservation_validation import validate_basic_time_rules

# todo need to supply this instead or smth?


def incoming_pog_reservation(base_list: BasesParser, raw_body: {}):
    """"Creates a reservation based on the current time for the next 45min-1hour depending on availability"""
    pass


def incoming_reservation(base_list: BasesParser, parsed_reservation: {}):
    temp_reservation = create_temp_reservation(base_list, parsed_reservation)
    validation = validate_basic_time_rules(temp_reservation)
    if validation.valid:
        # todo check for calendar availability
        pass
    else:
        pass


def create_temp_reservation(base_list: BasesParser, raw_reservation: {}) -> Reservation:
    try:
        facility = retrieve_base_by_id(base_list, raw_reservation[ReservationContext.BaseID.value])
        return Reservation(
            base_id=raw_reservation[ReservationContext.BaseID.value],
            continent=find_reservation_continent_by_zone_id(facility.zone_id),
            event_type=raw_reservation[ReservationContext.EventType.value],
            group_name=raw_reservation[ReservationContext.GroupName.value],
            start_time=raw_reservation[ReservationContext.StartTime.value],
            end_time=raw_reservation[ReservationContext.EndTime.value]
        )
    except KeyError as ke:
        raise RequestException(RequestExceptionMessage.MissingReservationPart, ke.args[0])
