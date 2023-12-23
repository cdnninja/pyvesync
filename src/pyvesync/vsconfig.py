"""Configure devices based on API response."""
import logging
import json
from typing import Dict, Optional
from pyvesync.helpers import Helpers


_LOGGER = logging.getLogger(__name__)


actions = {
    60000: 'toggle_power',
    70001: 'modes',
    70002: 'primary_level_text',
    70003: 'secondary_toggle',
    70004: 'primary_level_numeric',
    70005: 'secondary_levels',
    70008: 'levels_text',
}


class VeSyncConfig:
    """Get device specs and linkage properties from the API.

    Class methods:
    get_linkage(manager, config_module=None) returns a dictionary of supported linkage properties
    for a specific device or all devices.

    get_all_specs(manager) returns a list of all device specifications from the API.

    get_device_specs(manager, config_module) returns a dictionary of device specs for a device
    """

    @classmethod
    def get_linkage(cls, manager, config_module: Optional[str] = None):
        """Get VeSync Device properties."""
        headers = Helpers.req_header_bypass()
        url = '/cloud/v1/app/linkage/getSupportedLinkageProperties'
        body = Helpers.bypass_body_v2(manager)
        body['method'] = 'getSupportedLinkageProperties'
        response, _ = Helpers.call_api(url, 'post', headers=headers, json_object=body)
        if not isinstance(response, dict) or response.get('code') != 0:
            _LOGGER.debug('Failed to get supported linkage properties')
        return cls._process_linkage(response, config_module)

    @classmethod
    def _process_linkage(cls, response: dict, config_module: Optional[str] = None
                         ) -> Optional[dict]:
        """Process supported linkage properties."""
        dev_list = response.get('result', {}).get('devicePropertiesList')
        dev_dict: Dict[str, dict] = {}
        if not isinstance(dev_list, list) or len(dev_list) == 0:
            _LOGGER.debug('No supported linkage properties found in API Response')
            return None
        for dev in dev_list:
            if config_module is not None and dev.get('configModule') != config_module:
                continue
            for prop in dev.get('actionPropertyList', []):
                if prop.get('actionType') in actions:
                    action = actions[prop.get('actionType')]
                else:
                    action = prop.get('actionType')
                if dev_dict.get(dev['configModule']) is None:
                    dev_dict[dev['configModule']] = {}
                dev_dict[dev['configModule']][action] = prop.get('actionProps')

        # Write linkage specs to a file
        # with open('linkage.json', 'w') as f:
        #     json.dump(dev_list, f, indent=4)
        if config_module is not None and len(dev_dict) == 0:
            _LOGGER.debug("No supported linkage properties found for config module %s",
                          config_module)
        return dev_dict

    @classmethod
    def get_specs_call(cls, manager) -> list:
        """Get device specifications."""
        headers = Helpers.req_header_bypass()
        url = '/cloud/v1/app/getAppConfigurationV2'
        body = Helpers.bypass_body_v2(manager)
        body['method'] = 'getAppConfigurationV2'
        body['token'] = ''
        body['accountID'] = ''
        body['userCountryCode'] = ''
        body['categories'] = [{
            "category": "SupportedModelsV3",
            "testMode": False,
            "version": ""
        }]
        response, _ = Helpers.call_api(url, 'post', headers=headers, json_object=body)
        if not isinstance(response, dict) or response.get('code') != 0:
            _LOGGER.debug('Failed to get device config')
            return []
        specs = response.get('result', {}).get('configList', [{}])[0].get('items', [])
        if len(specs) == 0 or not isinstance(specs[0], dict):
            _LOGGER.debug('No device specifications found')
            return []
        item_value = specs[0].get('itemValue', '')
        try:
            item_json = json.loads(item_value)
        except json.JSONDecodeError:
            _LOGGER.debug('Failed to parse device specifications')
            return []
        prod_line_list = item_json.get('productLineList')
        if not isinstance(prod_line_list, list):
            _LOGGER.debug('No device specifications found')
            return []
        return prod_line_list

    @classmethod
    def get_all_specs(cls, manager) -> dict:
        """Get all device specs."""
        return cls.process_specs(cls.get_specs_call(manager))

    @classmethod
    def get_device_specs(cls, manager, config_module: str) -> dict:
        """Get device specifications for a specific device.

        Returns dictionary of device specifications in the format:
        >>> {
        >>>     'model': 'LV600S',
        >>>     'setup_entry': 'air-humidifier',
        >>>     'model_display': 'LV600S',
        >>>     'model_name': 'LV600S',
        >>>     'config_modules': [
        >>>         'WFON_AHM_LUH-A602S-WUSR_US',
        >>>         'WFON_AHM_LUH-A602S-WEUR_EU',
        >>>         'WFON_AHM_LUH-A602S-WJP_JP',
        >>>      ]
        >>> }
        """
        model_specs = {}
        line_list = cls.get_specs_call(manager)
        if not isinstance(line_list, list):
            return []
        for prod_line in line_list:
            type_list = prod_line.get('typeInfoList')
            if not isinstance(type_list, list):
                continue
            for prod_type in type_list:
                for model in prod_type['modelInfoList']:
                    config_mod_list = model.get('configModuleInfoList')

                    if not isinstance(config_mod_list, list):
                        continue
                    if config_module.lower() in [x.lower() for x in config_mod_list]:
                        model_specs = {
                                'model': model['model'],
                                'setup_entry': model['setupEntry'],
                                'model_display': model['modelDisplay'],
                                'model_name': model['modelName'],
                                'config_modules': config_mod_list,
                            }
                        break
            if model_specs:
                break
        return model_specs

    @classmethod
    def process_specs(cls, prod_line_list: list) -> dict:
        """Process device specifications from the API."""
        for prod_line in prod_line_list:
            type_list = prod_line.get('typeInfoList')
            if not isinstance(type_list, list):
                continue
            specs = {}
            for prod_type in type_list:
                current_type = prod_type['typeName'].lower()
                for model in prod_type['modelInfoList']:
                    current_model = model['model'].lower()
                    current_devtype = model['deviceType'].lower()
                    config_mod_list = model.get('configModuleInfoList')
                    if not isinstance(config_mod_list,
                                      list) or 'wifi' not in model['connectionType'].lower():
                        continue
                    for config_mod in config_mod_list:
                        specs[config_mod['configModule']] = {
                            'devicetype': current_devtype,
                            'modeltype': current_type,
                            'model': current_model,
                            'model_name': model['modelName'].lower(),
                            'model_display': model['modelDisplay'].lower(),
                            'setup_entry': model['setupEntry'].lower(),
                        }

        # Write specs to a file
        # with open('specs.json', 'w') as f:
        #     json.dump(prod_line_list, f, indent=4)
        return specs
