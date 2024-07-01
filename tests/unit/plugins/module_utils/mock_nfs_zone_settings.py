# Copyright: (c) 2023, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of NFS Zone Settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockNFSZoneSettingsApi:
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'
    ZONE = "sample-zone"
    NFS_DOMAIN = "example.com"

    ZONE_SETTINGS_COMMON_ARGS = {
        "onefs_host": "**.***.**.***",
        "access_zone": None,
        "nfsv4_allow_numeric_ids": None,
        "nfsv4_domain": None,
        "nfsv4_no_domain": None,
        "nfsv4_no_domain_uids": None,
        "nfsv4_no_names": None,
        "nfsv4_replace_domain": None
    }

    GET_NFS_ZONE_SETTINGS_RESPONSE = {
        "settings": {
            "nfsv4_allow_numeric_ids": True,
            "nfsv4_domain": None,
            "nfsv4_no_domain": True,
            "nfsv4_no_domain_uids": True,
            "nfsv4_no_names": True,
            "nfsv4_replace_domain": True,
            "zone": "sample-zone"
        }
    }

    @staticmethod
    def zone_settings_exception(response_type):
        if response_type == "get_settings_exception":
            return 'Got error SDK Error message while getting NFS zone ' \
                   'settings details for access zone: sample-zone'
        elif response_type == "update_zone_settings_exception":
            return 'Modify NFS zone settings with in access zone: ' \
                   'sample-zone failed with error: SDK Error message'
        elif response_type == "prepare_zone_settings_object_exception":
            return 'Got error SDK Error message while preparing NFS zone' \
                   ' settings modify object'
        elif response_type == "invalid_zone_exception":
            return 'Invalid access zone provided. Provide valid access zone'
        elif response_type == "pre_reqs_exception":
            return '**********'
