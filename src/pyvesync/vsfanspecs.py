"""VeSync Fan and Humidifier Specs."""

from pyvesync.devhelpers import FANFEATURES, FANMODES

humid_features: dict = {
    "Classic300S": {
        "module": "VeSyncHumid200300S",
        'model': 'Classic300S',
        "config_modules": [
            "WiFiBTOnboardingNotify_AirHumidifier_Classic300S_EU",
            "WiFiBTOnboardingNotify_AirHumidifier_Classic300S_US",
            "WFON_AHM_LUH-A601S-WUSB_US",
            "VS_WFON_APR_Classic300S_OFL_EU",
            "WiFiBTOnboardingNotify_AirHumidifier_Classic300S_JP"
        ],
        "features": [FANFEATURES.NIGHTLIGHT],
        "mist_modes": [FANMODES.AUTO, FANMODES.MANUAL, FANMODES.SLEEP],
        "mist_levels": list(range(1, 10)),
    },
    "Classic200S": {
        "module": "VeSyncHumid200S",
        'model': 'Classic200S',
        "config_modules": [
            "WiFiBTOnboardingNotify_AirHumidifier_Classic200S_JP",
            "WiFiBTOnboardingNotify_AirHumidifier_Classic200S_US"
        ],
        "features": [],
        "mist_modes": [FANMODES.AUTO, FANMODES.MANUAL],
        "mist_levels": list(range(1, 10)),
    },
    "Dual200S": {
        "module": "VeSyncHumid200300S",
        'model': 'Dual200S',
        "config_modules": [
            "WFON_AHM_LUH-D301S-WUSR_US",
            "WFON_AHM_LUH-D301S-WJP_JP",
            "WFON_AHM_LUH-D301S-WEU_EU",
            "WiFiBTOnboardingNotify_AirHumidifier_Dual200S_US",
            "VS_WFON_AHM_LUH-D301S-KEUR_EU"
        ],
        "features": [],
        "mist_modes": [FANMODES.AUTO, FANMODES.MANUAL],
        "mist_levels": list(range(1, 3)),
    },
    "LV600S": {
        "module": "VeSyncHumid200300S",
        'model': 'LUH-A602S-WUSR',
        "config_modules": [
            "WFON_AHM_LUH-A602S-WUSR_US",
            "WFON_AHM_LUH-A602S-WEUR_EU",
            "WFON_AHM_LUH-A602S-WJP_JP",
            "WFON_AHM_LUH-A602S-WUS_US",
            "WFON_AHM_LUH-A602S-WEU_EU",
        ],
        "features": [FANFEATURES.WARM_MIST, FANFEATURES.NIGHTLIGHT],
        "mist_modes": [FANMODES.HUMIDITY, FANMODES.SLEEP, FANMODES.MANUAL],
        "mist_levels": list(range(1, 10)),
        "warm_mist_levels": [0, 1, 2, 3],
    },
    "OASISMIST": {  # Oasis Mist
        "module": "VeSyncHumid200300S",
        'model': 'LUH-O451S-WUS',
        "config_modules": [
            "WFON_AHM_LUH-A451S-WUSR_US",
            "WFON_AHM_LUH-A451S-WEUR_EU",
            "WFON_AHM_LUH-A451S-WUS_US",
            "WFON_AHM_LUH-A451S-WEU_EU",
            "VS_WFON_AHM_LUH-O601S-KUS_US",
        ],
        "features": [FANFEATURES.WARM_MIST],
        "mist_modes": [FANMODES.HUMIDITY, FANMODES.SLEEP, FANMODES.MANUAL],
        "mist_levels": list(range(1, 10)),
        "warm_mist_levels": list(range(4)),
    },
    "OASISMIST1000S": {
        "module": "VeSyncHumid1000S",
        'model': 'LUH-M101S-WUS',
        "config_modules": [
            "VS_WFON_AHM_LUH-M101S-WUSR_US",
            "VS_WFON_AHM_LUH-M101S-WUS_US",
            "VS_WFON_AHM_LUH-M101S-WEUR_EU",
        ],
        "features": [],
        "mist_modes": [FANMODES.AUTO, FANMODES.MANUAL, FANMODES.SLEEP],
        "mist_levels": list(range(1, 10)),
    },
}


air_features: dict = {
    "Core200S": {
        "module": "VeSyncAirBypass",
        'model': 'Core200S',
        "config_modules": [
            "WFBO_APR_LAP-C201S-AUSR_US",
            "WFBO_APR_LAP-C202S-WUSR_US",
            "WiFiBTOnboarding_AirPurifier_Core200S_JP",
            "WiFiBTOnboarding_AirPurifier_Core200S_EU",
            "WiFiBTOnboarding_AirPurifier_Core200S_US"
        ],
        "modes": [FANMODES.SLEEP, FANMODES.OFF, FANMODES.MANUAL],
        "features": [],
        "levels": list(range(1, 4)),
    },
    "Core300S": {
        "module": "VeSyncAirBypass",
        'model': 'Core300S',
        "config_modules": [
            "WFON_APR_LAP-C301S-WJP_JP",
            "WFON_APR_LAP-C302S-WUSB_US",
            "WiFiBTOnboardingNotify_AirPurifier_Core300S_EU",
            "WiFiBTOnboardingNotify_AirPurifier_Core300S_US",
            "WFON_APR_LAP-C301S-WAAA_TA"
        ],
        "modes": [FANMODES.SLEEP, FANMODES.OFF, FANMODES.MANUAL, FANMODES.AUTO],
        "features": [FANFEATURES.AIR_QUALITY],
        "levels": list(range(1, 5)),
    },
    "Core400S": {
        "module": "VeSyncAirBypass",
        "model": 'Core400S',
        "config_modules": [
            "WFON_APR_LAP-C401S-WJP_JP",
            "WiFiBTOnboardingNotify_AirPurifier_LAP-C401S-WUSR_US",
            "WiFiBTOnboardingNotify_AirPurifier_Core400S_US",
            "WFON_APR_LAP-C401S-WAAA_TA",
            "WiFiBTOnboardingNotify_AirPurifier_Core400S_EU"
        ],
        "modes": [FANMODES.SLEEP, FANMODES.OFF, FANMODES.MANUAL, FANMODES.AUTO],
        "features": ["air_quality"],
        "levels": list(range(1, 5)),
    },
    "Core600S": {
        "module": "VeSyncAirBypass",
        'model': 'Core600S',
        "config_modules": [
            "WFON_APR_LAP-C601S-WUSR_US",
            "WFON_APR_LAP-C601S-WEU_EU",
            "WFON_APR_LAP-C601S-WUS_US"
        ],
        "modes": [FANMODES.SLEEP, FANMODES.OFF, FANMODES.MANUAL, FANMODES.AUTO],
        "features": [FANFEATURES.AIR_QUALITY],
        "levels": list(range(1, 5)),
    },
    "LV-PUR131S": {
        'model': 'LV-PUR131S',
        "module": "VeSyncAir131",
        "config_modules": [
            "AirPurifier131",
            "WF_APR_LV-RH131S-WM_US",
        ],
        "features": [FANFEATURES.AIR_QUALITY],
    },
    "Vital100S": {
        "module": "VeSyncVital",
        'model': 'LAP-V102S-AASR',
        "dev_type": "",
        "config_modules": [
            "VS_WFON_APR_LAP-V102S-AASR_TA",
            "VS_WFON_APR_LAP-V102S-AJPR_OFL_JP",
            "VS_WFON_APR_LAP-V102S-WJP_JP",
            "VS_WFON_APR_LAP-V102S-WEU_EU",
            "VS_WFON_APR_LAP-V102S-AUSR_US",
            "VS_WFON_APR_LAP-V102S-WUS_US"
        ],
        "modes": [FANMODES.SLEEP, FANMODES.OFF,
                  FANMODES.MANUAL, FANMODES.AUTO, FANMODES.PET],
        "features": [FANFEATURES.AIR_QUALITY],
        "levels": list(range(1, 5)),
    },
    "Vital200S": {
        "module": "VeSyncVital",
        'model': 'LAP-V201S-AASR',
        "config_modules": [
            "VS_WFON_APR_LAP-V201S-AEUR_OFL_EU",
            "VS_WFON_APR_LAP-V201S-AASR_TA",
            "VS_WFON_APR_LAP-V201S-WJP_JP",
            "VS_WFON_APR_LAP-V201S-WEU_EU",
            "VS_WFON_APR_LAP-V201S-AUSR_US",
            "VS_WFON_APR_LAP-V201S-WUS_US"
        ],
        "modes": [FANMODES.SLEEP, FANMODES.OFF,
                  FANMODES.MANUAL, FANMODES.AUTO, FANMODES.PET],
        "features": [FANFEATURES.AIR_QUALITY],
        "levels": list(range(1, 5)),
    },
}
