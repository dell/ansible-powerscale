# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of S3 bucket module on PowerScale"""

from __future__ import absolute_import, division, print_function
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell import (
    utils,
)

__metaclass__ = type


class MockS3KeyApi:
    MODULE_UTILS_PATH = (
        "ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils"
    )
    ZONE = "sample-zone"
    STATE = "present"
    USER = "sample-user"
    sdk = utils.get_powerscale_sdk()

    S3_KEY_COMMON_ARGS = {
        "onefs_host": "**.***.**.***",
        "access_zone": ZONE,
        "user": USER,
        "state": STATE,
    }

    S3_GET_DETAILS_EXISTING_RESPONSE = {
        "access_id": "sample_user_accid",
        "old_key_expiry": None,
        "old_key_timestamp": None,
        "old_secret_key": None,
        "secret_key": "********",
        "secret_key_timestamp": 1755782540,
    }

    S3_GET_DETAILS_NO_EXISTING_RESPONSE = {
        "access_id": None,
        "old_key_expiry": None,
        "old_key_timestamp": None,
        "secret_key_timestamp": None,
    }

    S3_CREATE_KEY_RESPONSE = {
        "access_id": "sample_user_accid",
        "old_key_expiry": None,
        "old_key_timestamp": None,
        "old_secret_key": None,
        "secret_key": "1234567890asdfhjkl",
        "secret_key_timestamp": 1755782540,
    }

    @staticmethod
    def get_s3_key_exception_response(response_type):
        if response_type == "get_details_exception":
            return (
                "Failed to get details of S3 Key for user sample-user"
                " in access zone sample-zone with error: SDK Error message"
            )
        elif response_type == "create_exception":
            return (
                "Create S3 Key for user sample-user in access zone sample-zone"
                " failed with error: SDK Error message"
            )
        elif response_type == "delete_exception":
            return (
                "Delete S3 Key for user sample-user in access zone sample-zone"
                " failed with error: SDK Error message"
            )
