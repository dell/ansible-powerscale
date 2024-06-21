# Copyright: (c) 2024, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock Api response for Unit tests of Support Assist settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockSupportAssistApi:
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'

    SUPPORT_ASSIST_COMMON_ARGS = {
        "onefs_host": "**.***.**.***",
        "verify_ssl": False,
        "accepted_terms": None,
        "automatic_case_creation": None,
        "connection": {
            "gateway_endpoints": None,
            "mode": None,
            "network_pools": None
        },
        "connection_state": None,
        "enable_download": None,
        "enable_remote_support": None,
        "enable_service": None,
        "contact": {
            "primary": {
                "email": None,
                "first_name": None,
                "last_name": None,
                "phone": None
            },
            "secondary": {
                "email": None,
                "first_name": None,
                "last_name": None,
                "phone": None
            }
        },
        "telemetry": {
            "offline_collection_period": None,
            "telemetry_enabled": None,
            "telemetry_persist": None,
            "telemetry_threads": None
        }
    }
    GET_SUPPORT_ASSIST_RESPONSE = {
        "automatic_case_creation": False,
        "connection": {
            "gateway_endpoints": [
                {
                    "enabled": True,
                    "host": "XX.XX.XX.XX",
                    "port": 9443,
                    "priority": 1,
                    "use_proxy": False,
                    "validate_ssl": False
                },
                {
                    "enabled": True,
                    "host": "XX.XX.XX.XY",
                    "port": 9443,
                    "priority": 2,
                    "use_proxy": False,
                    "validate_ssl": False
                }
            ],
            "mode": "gateway",
            "network_pools": [
                {
                    "pool": "pool1",
                    "subnet": "subnet0"
                }
            ]
        },
        "connection_state": "disabled",
        "contact": {
            "primary": {
                "email": "p7VYg@example.com",
                "first_name": "Eric",
                "last_name": "Nam",
                "phone": "1234567890"
            },
            "secondary": {
                "email": "kangD@example.com",
                "first_name": "Daniel",
                "last_name": "Kang",
                "phone": "1234567891"
            }
        },
        "enable_download": False,
        "enable_remote_support": False,
        "onefs_software_id": "ELMISL1019H4GY",
        "supportassist_enabled": True,
        "telemetry": {
            "offline_collection_period": 60,
            "telemetry_enabled": True,
            "telemetry_persist": True,
            "telemetry_threads": 10
        }
    }

    @staticmethod
    def get_support_assist_settings_exception_response(response_type):
        if response_type == 'get_details_exception':
            return "Got error SDK Error message while getting support assist setings details "
        elif response_type == 'update_exception':
            return "Modify support assist settings failed with error: SDK Error message"
        elif response_type == 'accept_terms_exception':
            return 'Accept or reject support assist terms failed with error: SDK Error message'
        elif response_type == 'empty_gateway_exception':
            return 'Gateway endpoints cannot be empty when the mode is gateway.'
        elif response_type == 'empty_network_pools_exception':
            return 'Network pool list cannot be empty.'
