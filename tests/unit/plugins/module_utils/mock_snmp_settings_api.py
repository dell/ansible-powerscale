# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of SNMP settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockSNMPSettingsApi:
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'
    SNMP_SETTINGS_COMMON_ARGS = {
        'onefs_host': '**.***.**.***',
        'read_only_community': None,
        'service': None,
        'snmp_v2c_access': None,
        'snmp_v3': None,
        'system_contact': None,
        'system_location': None
    }
    GET_SNMP_SETTINGS_RESPONSE = {
        "read_only_community": "I$ilonpublic",
        "service": True,
        "snmp_v1_v2c_access": True,
        "snmp_v3_access": True,
        "snmp_v3_auth_protocol": "SHA",
        "snmp_v3_priv_protocol": "AES",
        "snmp_v3_read_only_user": "general",
        "snmp_v3_security_level": "authNoPriv",
        "system_contact": "unset@unset.none",
        "system_location": "unset"
    }

    @staticmethod
    def get_snmpsettings_exception_response(response_type):
        if response_type == 'update_exception':
            return "Modifying SNMP settings failed with error: SDK Error message"
        elif response_type == 'get_resp_exception':
            return "Fetching SNMP settings failed with error:"
        elif response_type == 'system_contact_exception':
            return "Provide valid system_contact parameter."
        elif response_type == 'system_location_exception':
            return "Provide valid system_location parameter."
