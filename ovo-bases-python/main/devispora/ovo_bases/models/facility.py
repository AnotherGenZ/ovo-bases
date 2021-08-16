from enum import Enum


class FacilityProperties(str, Enum):
    ZoneId = 'zone_id'
    FacilityId = 'facility_id'
    FacilityName = 'facility_name'
    FacilityTypeId = 'facility_type_id'
    FacilityType = 'facility_type'
    FacilityLongName = 'facility_long_name'


class ZoneIdTranslation(int, Enum):
    Indar = 2
    Hossin = 4
    Amerish = 6
    Esamir = 8
    Koltyr = 131086


class Facility:
    def __init__(self, zone_id: int, facility_id: int,
                 facility_name: str, facility_type_id: int, facility_type: str, facility_name_long: str = None):
        self.zone_id = zone_id
        self.facility_id = facility_id
        self.facility_name = facility_name
        self.facility_type_id = facility_type_id
        self.facility_type = facility_type
        if facility_name_long is not None:
            self.facility_name_long = facility_name_long
