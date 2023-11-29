# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock Api response for Unit tests of SyncIQ global settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockSyncIQCertificateApi:
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'

    SYNCIQ_CERTIFICATE_COMMON_ARGS = {
        "onefs_host": "**.***.**.***",
        "certificate_file": "/ifs/server.crt",
        "description": "From python",
        "alias_name": "Test_1",
        "state": 'present',
        "certificate_id": "ywqeqwe76898y98wqwe",
        "new_alias_name": None
    }

    GET_SYNCIQ_CERTIFICATE_RESPONSE = {
        "certificates": [
            {
                "description": "From python module",
                "fingerprints": [
                    {
                        "type": "SHA1",
                        "value": "xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:5e:xx:xx:xx:xx:xx:xx:xx:xx"
                    },
                    {
                        "type": "SHA256",
                        "value": "xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:5e:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:"
                    }
                ],
                "id": "ywqeqwe76898y98wqwe",
                "issuer": "C=AU, ST=Some-State, O=Internet Widgits Pty Ltd",
                "name": "Sample",
                "not_after": 1753465054,
                "not_before": 1690393054,
                "status": "valid",
                "subject": "C=AU, ST=Some-State, O=Internet Widgits Pty Ltd"
            }
        ]
    }

    CREATE_CERTIFICATE_ID = {"id": "ywqeqwe76898y98wqwe"}

    MODIFY_CERTIFICATE_DETAILS = {
        "description": "new_description",
        "fingerprints": [
            {
                "type": "SHA1",
                "value": "xx:xx:xx:xx:xx:xx:84:xx:56:xx:xx:5e:xx:xx:xx:xx:xx:xx:xx:xx"
            },
            {
                "type": "SHA256",
                "value": "xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:5e:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:94:44:xx:xx:xx:xx:xx:"
            }
        ],
        "id": "ywqeqwe76898yadasdsad98wqwe",
        "issuer": "C=AU, ST=Some-State1, O=Internet of things Widgits Pvt Ltd",
        "name": "new_name",
        "not_after": 1753465054,
        "not_before": 1690393054,
        "status": "valid",
        "subject": "C=AU, ST=Some-State1, O=Internet of things Widgits Pvt Ltd"
    }

    @staticmethod
    def get_synciq_certificate_exception_response(response_type):
        if response_type == 'get_details_exception':
            return "Fetching SyncIQ certificate failed with error: SDK Error message"
        elif response_type == 'import_exception':
            return "Importing SyncIQ target certificate failed with error:"
        elif response_type == 'delete_exception':
            return "Deleting SyncIQ target certificate failed with error:"
        elif response_type == 'update_exception':
            return "Updating SyncIQ target certificate details failed with error:"

    @staticmethod
    def import_certificate_format_error_msg():
        return "File format is not supported"

    @staticmethod
    def alias_name_error_msg(param):
        return "The value for " + param + " is invalid"

    @staticmethod
    def description_error_msg():
        return "The maximum length for description is 128"
