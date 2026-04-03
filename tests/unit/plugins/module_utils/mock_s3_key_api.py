# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of S3 Key module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockS3KeyApi:
    """MockS3KeyApi definition."""
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'

    S3_KEY_COMMON_ARGS = {
        "onefs_host": "**.***.**.***",
        "user_name": "s3user1",
        "access_zone": "System",
        "state": "present",
        "force": False,
        "existing_key_expiry_time": None
    }

    GET_S3_KEY_RESPONSE = {
        "keys": [
            {
                "access_id": "ABCDEF1234567890"
            }
        ]
    }

    CREATE_S3_KEY_RESPONSE = {
        "keys": [
            {
                "access_id": "NEWKEY1234567890",
                "secret_key": "mock_secret_key_for_unit_test"
            }
        ]
    }

    CREATE_S3_KEY_ARGS = {
        "user_name": "s3user1",
        "access_zone": "System",
        "state": "present"
    }

    CREATE_S3_KEY_CUSTOM_ZONE_ARGS = {
        "user_name": "s3user1",
        "access_zone": "myzone",
        "state": "present"
    }

    DELETE_S3_KEY_ARGS = {
        "user_name": "s3user1",
        "access_zone": "System",
        "state": "absent"
    }

    FORCE_REGENERATE_ARGS = {
        "user_name": "s3user1",
        "access_zone": "System",
        "state": "present",
        "force": True
    }

    FORCE_REGENERATE_WITH_EXPIRY_ARGS = {
        "user_name": "s3user1",
        "access_zone": "System",
        "state": "present",
        "force": True,
        "existing_key_expiry_time": 60
    }

    BOUNDARY_EXPIRY_LOW_ARGS = {
        "user_name": "s3user1",
        "access_zone": "System",
        "state": "present",
        "force": True,
        "existing_key_expiry_time": 0
    }

    BOUNDARY_EXPIRY_HIGH_ARGS = {
        "user_name": "s3user1",
        "access_zone": "System",
        "state": "present",
        "force": True,
        "existing_key_expiry_time": 1440
    }

    @staticmethod
    def get_s3_key_exception_response(response_type):
        """Get s3 key exception response."""
        if response_type == 'get_exception':
            return "while getting S3 key details"
        elif response_type == 'create_exception':
            return "Failed to generate S3 key with error:"
        elif response_type == 'delete_exception':
            return "Failed to delete S3 key with error:"
        elif response_type == 'expiry_range_error':
            return "existing_key_expiry_time is not in the valid range"
        elif response_type == 'user_name_error':
            return "user_name is required"
        elif response_type == 'invalid_user_name':
            return "Invalid user_name provided"
