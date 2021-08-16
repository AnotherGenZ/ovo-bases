from devispora.ovo_bases.models.facility import ZoneIdTranslation
from devispora.ovo_bases.models.reservations import ReservationContinent


def find_reservation_continent_by_zone_id(zone_id: int) -> ReservationContinent:
    """Retrieves the correct ReservationContinent Enum by """
    for zone_id_translation in ZoneIdTranslation.__members__.values():
        if zone_id_translation.value == zone_id:
            for reservation_continent in ReservationContinent.__members__.values():
                if reservation_continent.name == zone_id_translation.name:
                    return reservation_continent
