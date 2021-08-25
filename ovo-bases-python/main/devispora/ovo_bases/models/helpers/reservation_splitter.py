from devispora.ovo_bases.models.reservations import Reservation
from devispora.ovo_bases.tools.time_service import get_event_day_from_timestamp, grab_next_day


def split_into_multi_reservations_when_needed(reservations: [Reservation]):
    """"Returns a list of all reservations. Will multiply reservations if there is a crossover in days"""
    final_reservations = []
    for reservation in reservations:
        final_reservations.extend(split_reservation_when_needed(reservation))
    return final_reservations


def split_reservation_when_needed(reservation: Reservation) -> [Reservation]:
    """"Returns a list of reservations. Depending on the duration of the reservation it will return more than one"""
    start_day = get_event_day_from_timestamp(reservation.start_time)
    end_day = get_event_day_from_timestamp(reservation.end_time)
    if start_day == end_day:
        return [reservation]
    else:
        return reservation_splitter(reservation, start_day, end_day)


def reservation_splitter(reservation: Reservation, start_day: int, end_day: int) -> [Reservation]:
    """"Will split into multiple reservations based on the amount of days required"""
    reservations = []
    checked_day = start_day
    while checked_day <= end_day:
        calibrated_day = grab_next_day(checked_day)
        if calibrated_day >= reservation.end_time:
            # make this final reservation
            reservations.append(create_similar_reservation(reservation, checked_day, reservation.end_time))
            return reservations
        else:
            if len(reservations) == 0:
                # Drop in the first day
                reservations.append(create_similar_reservation(reservation, reservation.start_time, calibrated_day))
            # turn into 1 new reservation and keep iterating.
            else:
                reservations.append(create_similar_reservation(reservation, checked_day, calibrated_day))
            checked_day = calibrated_day


def create_similar_reservation(old_reservation: Reservation, start_time: int, end_time: int) -> Reservation:
    return Reservation(
        facility_id=old_reservation.facility_id,
        continent=old_reservation.continent,
        group_name=old_reservation.group_name,
        reservation_type=old_reservation.reservation_type,
        start_time=start_time,
        end_time=end_time
    )
