# Copyright: (c) 2026, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of S3 global settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockS3GlobalSettingsApi:
    """MockS3GlobalSettingsApi definition."""
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'

    S3_GLOBAL_COMMON_ARGS = {
        "onefs_host": "**.***.**.***",
        "http_port": None,
        "https_port": None,
        "https_only": None,
        "service": None
    }

    GET_S3_GLOBAL_RESPONSE = {
        "http_port": 9020,
        "https_port": 9021,
        "https_only": False,
        "service": True
    }

    MODIFY_S3_GLOBAL_ARGS = {
        "http_port": 9020,
        "service": True
    }

    MODIFY_S3_GLOBAL_HTTPS_ONLY_ARGS = {
        "https_only": True
    }

    MODIFY_S3_GLOBAL_SERVICE_ARGS = {
        "service": False
    }

    MODIFY_S3_GLOBAL_HTTPS_PORT_ARGS = {
        "https_port": 9022
    }

    MODIFY_S3_GLOBAL_MULTIPLE_ARGS = {
        "http_port": 9025,
        "https_port": 9026,
        "https_only": True
    }

    MODIFY_S3_GLOBAL_BOUNDARY_LOW_ARGS = {
        "http_port": 1024
    }

    MODIFY_S3_GLOBAL_BOUNDARY_HIGH_ARGS = {
        "http_port": 65535
    }

    PREREQS_VALIDATE_FAILURE = {
        "all_packages_found": False,
        "error_message": "Required SDK packages not found",
    }

    @staticmethod
    def get_s3_global_settings_exception_response(response_type):
        """Get s3 global settings exception response."""
        if response_type == 'get_details_exception':
            return "while getting S3 global settings details"
        elif response_type == 'update_exception':
            return "Modify S3 global settings failed with error:"
        elif response_type == 'port_range_error':
            return "is not in the valid port range"
        elif response_type == 'general_get_exception':
            return "getting S3 global settings"
        elif response_type == 'general_update_exception':
            return "Modify S3 global settings failed"
