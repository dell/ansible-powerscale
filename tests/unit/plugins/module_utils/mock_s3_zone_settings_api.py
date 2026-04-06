# Copyright: (c) 2026, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of S3 zone settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockS3ZoneSettingsApi:
    """MockS3ZoneSettingsApi definition."""
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'

    S3_ZONE_COMMON_ARGS = {
        "onefs_host": "**.***.**.***",
        "access_zone": "System",
        "base_domain": None,
        "bucket_directory_create_mode": None,
        "object_acl_policy": None,
        "root_path": None,
        "use_md5_for_etag": None,
        "validate_content_md5": None
    }

    GET_S3_ZONE_RESPONSE = {
        "base_domain": "",
        "bucket_directory_create_mode": 448,
        "object_acl_policy": "replace",
        "root_path": "/ifs",
        "use_md5_for_etag": False,
        "validate_content_md5": False
    }

    MODIFY_S3_ZONE_BASE_DOMAIN_ARGS = {
        "base_domain": "s3.example.com"
    }

    MODIFY_S3_ZONE_ROOT_PATH_ARGS = {
        "root_path": "/ifs/data/s3"
    }

    MODIFY_S3_ZONE_ACL_POLICY_ARGS = {
        "object_acl_policy": "deny"
    }

    MODIFY_S3_ZONE_BUCKET_DIR_MODE_ARGS = {
        "bucket_directory_create_mode": 493
    }

    MODIFY_S3_ZONE_MD5_ARGS = {
        "use_md5_for_etag": True,
        "validate_content_md5": True
    }

    MODIFY_S3_ZONE_MULTIPLE_ARGS = {
        "base_domain": "s3.newdomain.com",
        "root_path": "/ifs/data/s3new",
        "object_acl_policy": "deny",
        "bucket_directory_create_mode": 493,
        "use_md5_for_etag": True,
        "validate_content_md5": True
    }

    MODIFY_S3_ZONE_BOUNDARY_MODE_LOW_ARGS = {
        "bucket_directory_create_mode": 0
    }

    MODIFY_S3_ZONE_BOUNDARY_MODE_HIGH_ARGS = {
        "bucket_directory_create_mode": 511
    }

    PREREQS_VALIDATE_FAILURE = {
        "all_packages_found": False,
        "error_message": "Required SDK packages not found",
    }

    @staticmethod
    def get_s3_zone_settings_exception_response(response_type):
        """Get s3 zone settings exception response."""
        responses = {
            'get_details_exception': "while getting S3 zone settings details",
            'update_exception': "Modify S3 zone settings failed with error:",
            'domain_length_error': "base_domain must not exceed 255 characters",
            'mode_range_error': "bucket_directory_create_mode is not in the valid range",
            'root_path_length_error': "root_path must not exceed 4096 characters",
            'empty_access_zone_error': "Invalid access zone provided",
            'general_get_exception': "getting S3 zone settings",
            'general_update_exception': "Modify S3 zone settings failed",
        }
        return responses.get(response_type)
