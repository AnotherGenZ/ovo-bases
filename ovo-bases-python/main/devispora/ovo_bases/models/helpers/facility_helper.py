from devispora.ovo_bases.bases.parse_bases import BaseParser
from devispora.ovo_bases.bases.search_base import retrieve_base_by_id
from devispora.ovo_bases.exception.exceptions import RequestExceptionMessage, RequestException
from devispora.ovo_bases.models.facility import ZoneIdTranslation, Facility
from devispora.ovo_bases.models.reservations import ReservationContinent


def find_reservation_continent_by_zone_id(zone_id: int) -> ReservationContinent:
    """Retrieves the correct ReservationContinent Enum by  """
    for zone_id_translation in ZoneIdTranslation.__members__.values():
        if zone_id_translation.value == zone_id:
            for reservation_continent in ReservationContinent.__members__.values():
                if reservation_continent.name == zone_id_translation.name:
                    return reservation_continent


def find_facilities(base_parser: BaseParser, requested_facilities: [int]) -> [Facility]:
    if not requested_facilities:
        raise RequestException(RequestExceptionMessage.FacilityNotProvided)
    found_bases = []
    for requested_facility in requested_facilities:
        try:
            facility_id = int(requested_facility)
            found_facility = retrieve_base_by_id(base_parser.stored_facilities, facility_id)
            found_bases.append(found_facility)
        except ValueError:
            raise RequestException(RequestExceptionMessage.FacilityCannotBeFound, requested_facility)
    return found_bases
