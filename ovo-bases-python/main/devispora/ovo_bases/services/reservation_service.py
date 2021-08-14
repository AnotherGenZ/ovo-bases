from devispora.ovo_bases.exception.exceptions import ReservationException, ReservationExceptionMessage
from devispora.ovo_bases.models.reservations import Reservation, ReservationContext
from devispora.ovo_bases.validation.reservation_validation import validate_basic_time_rules


def incoming_reservation(raw_body: {}):
    temp_reservation = create_temp_reservation(raw_body)
    validation = validate_basic_time_rules(temp_reservation)
    if validation.valid:
        # todo check for calendar availability
        pass
    else:
        pass


def create_temp_reservation(raw_body: {}) -> Reservation:
    try:
        return Reservation(
            base_id=raw_body[ReservationContext.BaseID.value],
            continent=raw_body[ReservationContext.Continent.value],
            event_type=raw_body[ReservationContext.EventType.value],
            group_name=raw_body[ReservationContext.GroupName.value],
            start_time=raw_body[ReservationContext.StartTime.value],
            end_time=raw_body[ReservationContext.EndTime.value]
        )
    except KeyError as ke:
        raise ReservationException(ReservationExceptionMessage.MissingReservationPart, ke.args[0])
