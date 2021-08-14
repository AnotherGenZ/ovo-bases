from enum import IntEnum


def additional_bases():
    """"Manually added bases that cannot be retrieved from the REST API"""
    return [
        {
            "facility_name": "Koltyr Northern Warpgate",
            "facility_id": 400014,
            "facility_type_id": 7,
            "facility_type": "Warpgate",
            "zone_id": 131086
        },
        {
            "facility_name": "Koltyr Eastern Warpgate",
            "facility_id": 400015,
            "facility_type_id": 7,
            "facility_type": "Warpgate",
            "zone_id": 131086
        },
        {
            "facility_name": "Koltyr Southern Warpgate",
            "facility_id": 400016,
            "facility_type_id": 7,
            "facility_type": "Warpgate",
            "zone_id": 131086
        },
        {
            "facility_name": "Zorja",
            "facility_id": 400017,
            "facility_type_id": 2,
            "facility_type": "Amp Station",
            "zone_id": 131086
        },
        {
            "facility_name": "Xander",
            "facility_id": 400018,
            "facility_type_id": 3,
            "facility_type": "Bio Lab",
            "zone_id": 131086
        },
        {
            "facility_name": "Svarog",
            "facility_id": 400019,
            "facility_type_id": 4,
            "facility_type": "Tech Plant",
            "zone_id": 131086
        },
        {
            "facility_name": "Koltyr Tech Plant Outpost",
            "facility_id": 400020,
            "facility_type_id": 5,
            "facility_type": "Large Outpost",
            "zone_id": 131086
        },
        {
            "facility_name": "Koltyr Biolab Outpost",
            "facility_id": 400021,
            "facility_type_id": 5,
            "facility_type": "Large Outpost",
            "zone_id": 131086
        },
        {
            "facility_name": "Koltyr Amp Station Outpost",
            "facility_id": 400022,
            "facility_type_id": 5,
            "facility_type": "Large Outpost",
            "zone_id": 131086
        }
    ]
