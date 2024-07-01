# Copyright: (c) 2023, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of nfs default settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockNfsDefaultSettingsApi:
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'
    NFS_DEFAULT_SETTINGS_COMMON_ARGS = {
        'onefs_host': '**.***.**.***',
        'access_zone': 'System',
        'map_root': {},
        'map_non_root': {},
        'map_failure': {},
        'file_name_max_size': None,
        'block_size': None,
        'commit_asynchronous': None,
        'directory_transfer_size': None,
        'read_transfer_max_size': None,
        'read_transfer_multiple': None,
        'read_transfer_size': None,
        'setattr_asynchronous': None,
        'write_datasync_action': None,
        'write_datasync_reply': None,
        'write_filesync_action': None,
        'write_filesync_reply': None,
        'write_transfer_max_size': None,
        'write_transfer_multiple': None,
        'write_transfer_size': None,
        'write_unstable_action': None,
        'write_unstable_reply': None,
        'max_file_size': None,
        'readdirplus': None,
        'return_32bit_file_ids': None,
        'can_set_time': None,
        'encoding': None,
        'map_lookup_uid': None,
        'symlinks': None,
        'time_delta': None,
        'security_flavors': []
    }
    GET_NFSDEFAULTSETTINGS_RESPONSE = {
        "commit_asynchronous": False,
        "encoding": "UTF-8",
        "map_full": True,
        "map_root": {
            "enabled": False,
            "primary_group": {
                "id": "GROUP:0001",
                "name": None,
                "type": None
            },
            "secondary_groups": [
                {
                    "id": "GROUP:0002"
                },
                {
                    "id": "GROUP:0003"
                },
                {
                    "id": "GROUP:0004"
                }
            ],
            "user": {
                "id": "USER:0005",
                "name": None,
                "type": None
            }
        },
        "max_file_size": 3145728,
        "name_max_size": 10009,
        "security_flavors": [
            "unix",
            "krb5"
        ],
        "time_delta": 1.0,
        "write_datasync_action": "DATASYNC",
        "zone": "System"
    }

    @staticmethod
    def get_nfsdefaultsettings_exception_response(response_type):
        if response_type == 'update_exception':
            return "Modifying NFS default settings for access zone: System failed with error: SDK Error message"
        elif response_type == 'form_dict_exception':
            return "Forming modification dict failed with error: "
