# Copyright: (c) 2023, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of SMB global settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockSMBGlobalSettingsApi:
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'

    SMB_GLOBAL_COMMON_ARGS = {
        "onefs_host": "**.***.**.***",
        "verify_ssl": False
    }
    GET_SMB_GLOBAL_RESPONSE = {
        "access_based_share_enum": False,
        "dot_snap_accessible_child": True,
        "dot_snap_accessible_root": True,
        "dot_snap_visible_child": False,
        "dot_snap_visible_root": True,
        "enable_security_signatures": False,
        "guest_user": "nobody",
        "ignore_eas": False,
        "onefs_cpu_multiplier": 4,
        "onefs_num_workers": 0,
        "reject_unencrypted_access": False,
        "require_security_signatures": False,
        "server_side_copy": False,
        "server_string": "PowerScale Server",
        "service": False,
        "support_multichannel": True,
        "support_netbios": False,
        "support_smb2": True,
        "support_smb3_encryption": True
    }

    @staticmethod
    def get_smb_global_settings_exception_response(response_type):
        if response_type == 'get_details_exception':
            return "Got error SDK Error message while getting SMB global setings details "
        elif response_type == 'update_exception':
            return "Modify SMB global settings failed with error: SDK Error message"
        elif response_type == 'prereq_exception':
            return 'Prerequisite validation failed'
