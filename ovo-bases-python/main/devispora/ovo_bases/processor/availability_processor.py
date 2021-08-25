from typing import Dict, List, Set

from devispora.ovo_bases.models.availability_result import AvailabilityResult
from devispora.ovo_bases.models.reservations import Reservation, ReservationType


def check_if_available(incoming_reservations: [Reservation], stored_reservations: [Reservation]) -> AvailabilityResult:
    segmented_incoming = segment_reservations_by_day(incoming_reservations)
    segmented_stored = segment_reservations_by_day(stored_reservations)
    result = segmented_checker(segmented_incoming, segmented_stored)
    return result


def segment_reservations_by_day(reservations: [Reservation]) -> Dict[int, Set[Reservation]]:
    """Groups reservations of the same days together"""
    reservation_dict = {}
    for reservation in reservations:
        if reservation.reservation_day not in reservation_dict:
            reservation_dict[reservation.reservation_day] = {reservation}
        else:
            reservation_dict[reservation.reservation_day].add(reservation)
    return reservation_dict


def segmented_checker(
        segmented_incoming: Dict[int, Set[Reservation]],
        segmented_stored: Dict[int, Set[Reservation]]) -> AvailabilityResult:
    """Checks if a reservation is possible or has to be denied"""
    possible_reservations = []
    denied_reservations = []
    for incoming_day in segmented_incoming:
        segmented_day = segmented_incoming[incoming_day]
        stored_day = segmented_stored[incoming_day]
        for incoming_reservation in segmented_day:
            previous_denied_size = len(denied_reservations)
            for stored_reservation in stored_day:
                if check_location_conflict(incoming_reservation, stored_reservation):
                    if check_if_reservation_between(incoming_reservation, stored_reservation):
                        denied_reservations.append(incoming_reservation)
            if previous_denied_size is len(denied_reservations):
                possible_reservations.append(incoming_reservation)

    return AvailabilityResult(possible_reservations, denied_reservations)


def check_if_reservation_between(incoming_reservation: Reservation, existing_reservation: Reservation) -> bool:
    start_issue = (existing_reservation.start_time <= incoming_reservation.start_time < existing_reservation.end_time)
    end_issue = (existing_reservation.start_time < incoming_reservation.end_time <= existing_reservation.end_time)
    return start_issue or end_issue


chac_fusion_facility_id = 307010
kessels_facility_id = 266000


def check_location_conflict(incoming_reservation: Reservation, stored_reservation: Reservation) -> bool:
    """
    Returns whether or not the locations of two reservations are the same.
    Large events reserve the entire continent and will qualify as a location conflict.
    Special care for Kessel's Crossing and Chac Fusion due to proximity
    """
    if incoming_reservation.continent is stored_reservation.continent:
        if stored_reservation.reservation_type is ReservationType.LargeEvent:
            return True
        if stored_reservation.facility_id == incoming_reservation.facility_id:
            return True
        if stored_reservation.facility_id == chac_fusion_facility_id or kessels_facility_id:
            if incoming_reservation.facility_id == chac_fusion_facility_id or kessels_facility_id:
                return True
    else:
        return False
