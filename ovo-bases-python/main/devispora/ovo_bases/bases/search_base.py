from devispora.ovo_bases.exception.exceptions import RequestException, RequestExceptionMessage
from devispora.ovo_bases.models.facility import Facility, FacilityProperties


def retrieve_base_by_id(stored_facilities: [], base_id: int) -> Facility:
    for facility in stored_facilities:
        if FacilityProperties.FacilityId in facility:
            if int(facility[FacilityProperties.FacilityId]) == base_id:
                if int(facility[FacilityProperties.FacilityTypeId]) in [2, 3, 4]:
                    return Facility(
                        zone_id=facility[FacilityProperties.ZoneId],
                        facility_id=facility[FacilityProperties.FacilityId],
                        facility_name=facility[FacilityProperties.FacilityName],
                        facility_type=facility[FacilityProperties.FacilityType],
                        facility_type_id=facility[FacilityProperties.FacilityTypeId],
                        facility_name_long=facility[FacilityProperties.FacilityLongName]
                    )
                else:
                    return Facility(
                        zone_id=facility[FacilityProperties.ZoneId],
                        facility_id=facility[FacilityProperties.FacilityId],
                        facility_name=facility[FacilityProperties.FacilityName],
                        facility_type=facility[FacilityProperties.FacilityType],
                        facility_type_id=facility[FacilityProperties.FacilityTypeId]
                    )
    raise RequestException(RequestExceptionMessage.FacilityCannotBeFound)
