from devispora.ovo_bases.bases.extra_bases import additional_bases
from devispora.ovo_bases.bases.load_bases import load_facilities_file
from devispora.ovo_bases.models.facility import FacilityProperties


class BaseParser:
    stored_facilities = []

    def create_base_list(self) -> {}:
        facility_json = load_facilities_file()
        facilities_section = facility_json['map_region_list']
        loaded_bases = parse_bases(facilities_section)
        loaded_bases.extend(load_extra_bases())
        self.stored_facilities = loaded_bases


def parse_bases(facilities) -> {}:
    """
    Loads facilities from the map region list and transforms the names of large facilities.
    For example: Naum of facility type 2 will get Amp Station appended to it.
    The varieties are: 2 = Amp Station, 3 = Bio Lab, 4 = Tech Plant.
    """
    for facility in facilities:
        if FacilityProperties.FacilityTypeId in facility:
            facility_type_parsed = int(facility[FacilityProperties.FacilityTypeId])
            if facility_type_parsed in [2, 3, 4]:
                facility[FacilityProperties.FacilityLongName] = \
                    facility[FacilityProperties.FacilityName] + ' ' + facility[FacilityProperties.FacilityType]
            facility[FacilityProperties.FacilityTypeId] = facility_type_parsed
        if FacilityProperties.ZoneId in facility:
            facility[FacilityProperties.ZoneId] = int(facility[FacilityProperties.ZoneId])
        if FacilityProperties.FacilityId in facility:
            facility[FacilityProperties.FacilityId] = int(facility[FacilityProperties.FacilityId])
    return facilities


def load_extra_bases() -> []:
    other_bases = additional_bases()
    parsed_extra_bases = parse_bases(other_bases)
    return parsed_extra_bases
