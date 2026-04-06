# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock API responses for PowerScale NFS export module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.nfs.utils'

SAMPLE_IP1 = "xx.xx.xx.xx"
SAMPLE_IP2 = "xx.xx.xx.xy"
SAMPLE_IP3 = "xx.xx.xx.xz"
NFS_ID_1 = "205"
NFS_ID_2 = "206"
SYS_ZONE = "system"
PATH_1 = "/ifs/test_sample_nfs"
SAMPLE_ZONE = "sample_zone"
STATE_P = "present"
STATE_A = "absent"

NFS_COMMON_ARGS = {
    "path": None,
    "access_zone": None,
    "clients": None,
    "root_clients": None,
    "map_root": None,
    "map_non_root": None,
    "read_only_clients": None,
    "read_write_clients": None,
    "client_state": None,
    "description": None,
    "read_only": None,
    "sub_directories_mountable": None,
    "security_flavors": None,
    "ignore_unresolvable_hosts": None,
    "state": None,
    # --- Advanced Performance Fields ---
    "read_transfer_size": None,
    "read_transfer_max_size": None,
    "read_transfer_multiple": None,
    "write_transfer_size": None,
    "write_transfer_max_size": None,
    "write_transfer_multiple": None,
    "directory_transfer_size": None,
    "block_size": None,
    "max_file_size": None,
    "file_name_max_size": None,
    # --- Advanced Sync/Async Fields ---
    "commit_asynchronous": None,
    "setattr_asynchronous": None,
    "readdirplus": None,
    "write_filesync_action": None,
    "write_filesync_reply": None,
    "write_datasync_action": None,
    "write_datasync_reply": None,
    "write_unstable_action": None,
    "write_unstable_reply": None,
    # --- Advanced Identity/Mapping Fields ---
    "map_all": None,
    "map_failure": None,
    "map_full": None,
    "map_lookup_uid": None,
    "map_retry": None,
    # --- Advanced Other Fields ---
    "snapshot": None,
    "encoding": None,
    "symlinks": None,
    "no_truncate": None,
    "return_32bit_file_ids": None,
    "can_set_time": None,
    "time_delta": None,
}

NFS_1 = {"exports": [{
    "all_dirs": False,
    "block_size": 8192,
    "case_insensitive": False,
    "case_preserving": True,
    "clients": [
        SAMPLE_IP1
    ],
    "description": "description",
    "id": NFS_ID_1,
    "name_max_size": 255,
    "paths": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
    "read_only": False,
    "read_only_clients": [],
    "read_write_clients": [],
    "readdirplus": True,
    "root_clients": [],
    "security_flavors": [
        "krb5"
    ],
    "map_root": {
        "enabled": True,
        "primary_group": {
            "id": "GROUP:group1",
            "name": None,
            "type": None
        },
        "secondary_groups": [],
        "user": {
            "id": "USER:user",
            "name": None,
            "type": None
        }
    },
    "map_non_root": {
        "enabled": True,
        "primary_group": {
            "id": "GROUP:group1",
            "name": None,
            "type": None
        },
        "secondary_groups": [],
        "user": {
            "id": "USER:root",
            "name": None,
            "type": None
        }
    },
    "map_failure": {
        "enabled": False,
        "primary_group": {},
        "secondary_groups": [],
        "user": {},
    },
    "snapshot": None,
    "zone": SYS_ZONE}]}

NFS_EMPTY = {"exports": [], "total": 0}

ZONE = {'summary': {'path': '/ifs/sample_zone'}}

NFS_MULTIPLE = {"exports": [{
    "all_dirs": False,
    "block_size": 8192,
    "case_insensitive": False,
    "case_preserving": True,
    "clients": [
        SAMPLE_IP1
    ],
    "description": "description",
    "id": NFS_ID_1,
    "name_max_size": 255,
    "paths": [PATH_1],
    "read_only": False,
    "read_only_clients": [],
    "read_write_clients": [],
    "readdirplus": True,
    "root_clients": [],
    "security_flavors": [
        "krb5"
    ],
    "snapshot": None,
    "zone": SYS_ZONE},
    {
        "all_dirs": False,
        "block_size": 8192,
        "case_insensitive": False,
        "case_preserving": True,
        "clients": [
            SAMPLE_IP1
        ],
        "description": "description",
        "id": NFS_ID_2,
        "name_max_size": 255,
        "paths": [PATH_1],
        "read_only": False,
        "read_only_clients": [],
        "read_write_clients": [],
        "readdirplus": True,
        "root_clients": [],
        "security_flavors": [
            "krb5"
        ],
        "snapshot": None,
        "zone": SYS_ZONE}],
    "total": 2}

NFS_2 = {"exports": [{
    "all_dirs": False,
    "block_size": 8192,
    "case_insensitive": False,
    "case_preserving": True,
    "clients": [
        SAMPLE_IP1,
        SAMPLE_IP2
    ],
    "description": "description1",
    "id": NFS_ID_1,
    "name_max_size": 255,
    "paths": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
    "read_only": False,
    "read_only_clients": [SAMPLE_IP2, SAMPLE_IP3],
    "read_write_clients": [SAMPLE_IP2],
    "readdirplus": True,
    "root_clients": [SAMPLE_IP2],
    "security_flavors": [
        "krb5",
        "unix"
    ],
    "snapshot": None,
    "zone": SYS_ZONE}]}

CREATE_NFS_PARAMS = {
    "path": PATH_1,
    "access_zone": SYS_ZONE,
    "description": "description",
    "read_only": True,
    "read_only_clients": [SAMPLE_IP1],
    "clients": [SAMPLE_IP1],
    "client_state": "present-in-export",
    "security_flavors": ["kerberos"],
    "map_root": {"user": "root", "primary_group": "root", "secondary_groups": [{"name": "group1"}, {"name": "group2"}]},
    "map_non_root": {"user": "root", "primary_group": "root", "secondary_groups": [{"name": "group1"}, {"name": "group2"}]}
}

MODIFY_NFS_PARAMS = {
    "path": PATH_1,
    "access_zone": SYS_ZONE,
    "description": "description1",
    "read_only": True,
    "read_only_clients": [SAMPLE_IP2, SAMPLE_IP3],
    "clients": [SAMPLE_IP2],
    "read_write_clients": [SAMPLE_IP2],
    "root_clients": [SAMPLE_IP2],
    "client_state": "present-in-export",
    "sub_directories_mountable": True,
    "security_flavors": ["unix", "kerberos_privacy"],
    "map_root": {"user": "root", "primary_group": "root", "secondary_groups": [{"name": "group1", "state": "absent"}, {"name": "group2"}]},
    "map_non_root": {"user": "root", "primary_group": "root", "secondary_groups": [{"name": "group1"}, {"name": "group2"}]}
}


class NFSTestExportObj:
    export_obj = None

    def __init__(self, obj):
        self.export_obj = obj

    @staticmethod
    def to_dict():
        return NFSTestExportObj.export_obj


class NFSTestExport:
    total = 0
    exports = []

    def __init__(self, total=0, export_obj=None):
        self.total = total
        if export_obj:
            self.exports.append(NFSTestExportObj(export_obj))


def get_nfs_failed_msg():
    return 'Got error SDK Error message while getting NFS export details for path'


def get_nfs_non_zone_failed_msg():
    return 'Unable to fetch base path of Access Zone'


def create_nfs_failed_msg():
    return 'Create NFS export for path: /ifs/test_sample_nfs and access zone: system failed'


def create_nfs_param_failed_msg():
    return 'Create NfsExportCreateParams object for path /ifs/test_sample_nfs failed with error SDK Error'


def without_clients_failed_msg():
    return 'Invalid input: Client state is given, clients not specified'


def without_client_state_failed_msg():
    return 'Invalid input: Clients are given, client state not specified'


def modify_nfs_failed_msg():
    return 'Modify NFS export for path: /ifs/test_sample_nfs and access zone: system failed with error'


def delete_nfs_failed_msg():
    return 'Delete NFS export with path: V, zone: system, id: 205 failed with error'


def get_failed_msgs(response_type):
    err_msg_dict = {
        "az_path_err": "Unable to fetch base path of Access Zone sample_zone failed with error: SDK Error message",
        "id_err": "Got error Test Exception while getting NFS export details for ID: 123 and access zone: system",
        "multiple_nfs_err": "Multiple NFS Exports found",
    }
    return err_msg_dict.get(response_type)


# ---------------------------------------------------------------------------
# Advanced NFS export mock data
# ---------------------------------------------------------------------------

NFS_ADVANCED_EXPORT = {"exports": [{
    # Existing fields
    "all_dirs": False,
    "clients": [SAMPLE_IP1],
    "description": "advanced export",
    "id": NFS_ID_1,
    "paths": [PATH_1],
    "read_only": False,
    "read_only_clients": [],
    "read_write_clients": [],
    "root_clients": [],
    "security_flavors": ["unix"],
    "zone": SYS_ZONE,
    "map_root": {
        "enabled": True,
        "primary_group": {"id": "GROUP:group1", "name": None, "type": None},
        "secondary_groups": [],
        "user": {"id": "USER:user", "name": None, "type": None}
    },
    "map_non_root": {
        "enabled": False,
        "primary_group": {"id": None, "name": None, "type": None},
        "secondary_groups": [],
        "user": {"id": "USER:nobody", "name": None, "type": None}
    },
    # Advanced Performance Fields (API defaults)
    "read_transfer_size": 524288,
    "read_transfer_max_size": 1048576,
    "read_transfer_multiple": 512,
    "write_transfer_size": 524288,
    "write_transfer_max_size": 1048576,
    "write_transfer_multiple": 512,
    "directory_transfer_size": 131072,
    "block_size": 8192,
    "max_file_size": 9223372036854775807,
    "name_max_size": 255,
    # Advanced Sync/Async Fields (API defaults)
    "commit_asynchronous": False,
    "setattr_asynchronous": False,
    "readdirplus": True,
    "write_filesync_action": "DATASYNC",
    "write_filesync_reply": "FILESYNC",
    "write_datasync_action": "DATASYNC",
    "write_datasync_reply": "DATASYNC",
    "write_unstable_action": "DATASYNC",
    "write_unstable_reply": "UNSTABLE",
    # Advanced Identity/Mapping Fields (API defaults)
    "map_all": {
        "enabled": False,
        "primary_group": {"id": None, "name": None, "type": None},
        "secondary_groups": [],
        "user": {"id": "USER:nobody", "name": None, "type": None}
    },
    "map_failure": {
        "enabled": False,
        "primary_group": {"id": None, "name": None, "type": None},
        "secondary_groups": [],
        "user": {"id": "USER:nobody", "name": None, "type": None}
    },
    "map_full": True,
    "map_lookup_uid": False,
    "map_retry": True,
    # Advanced Other Fields (API defaults)
    "snapshot": None,
    "encoding": "DEFAULT",
    "symlinks": True,
    "no_truncate": False,
    "return_32bit_file_ids": False,
    "can_set_time": True,
    "time_delta": 1e-09,
    "case_insensitive": False,
    "case_preserving": True,
}]}


NFS_ADVANCED_MODIFIED = {"exports": [{
    # Same structure but with modified values
    "all_dirs": False,
    "clients": [SAMPLE_IP1],
    "description": "advanced export",
    "id": NFS_ID_1,
    "paths": [PATH_1],
    "read_only": False,
    "read_only_clients": [],
    "read_write_clients": [],
    "root_clients": [],
    "security_flavors": ["unix"],
    "zone": SYS_ZONE,
    "map_root": {
        "enabled": True,
        "primary_group": {"id": "GROUP:group1", "name": None, "type": None},
        "secondary_groups": [],
        "user": {"id": "USER:user", "name": None, "type": None}
    },
    "map_non_root": {
        "enabled": False,
        "primary_group": {"id": None, "name": None, "type": None},
        "secondary_groups": [],
        "user": {"id": "USER:nobody", "name": None, "type": None}
    },
    # Modified performance fields
    "read_transfer_size": 1048576,
    "read_transfer_max_size": 2097152,
    "read_transfer_multiple": 1024,
    "write_transfer_size": 1048576,
    "write_transfer_max_size": 2097152,
    "write_transfer_multiple": 1024,
    "directory_transfer_size": 262144,
    "block_size": 16384,
    "max_file_size": 9223372036854775807,
    "name_max_size": 255,
    # Modified sync/async fields
    "commit_asynchronous": True,
    "setattr_asynchronous": True,
    "readdirplus": True,
    "write_filesync_action": "FILESYNC",
    "write_filesync_reply": "FILESYNC",
    "write_datasync_action": "FILESYNC",
    "write_datasync_reply": "FILESYNC",
    "write_unstable_action": "FILESYNC",
    "write_unstable_reply": "FILESYNC",
    # Identity fields (unchanged)
    "map_all": {
        "enabled": False,
        "primary_group": {"id": None, "name": None, "type": None},
        "secondary_groups": [],
        "user": {"id": "USER:nobody", "name": None, "type": None}
    },
    "map_failure": {
        "enabled": False,
        "primary_group": {"id": None, "name": None, "type": None},
        "secondary_groups": [],
        "user": {"id": "USER:nobody", "name": None, "type": None}
    },
    "map_full": True,
    "map_lookup_uid": False,
    "map_retry": True,
    # Modified other fields
    "snapshot": "weekly_snap",
    "encoding": "UTF-8",
    "symlinks": True,
    "no_truncate": False,
    "return_32bit_file_ids": False,
    "can_set_time": False,
    "time_delta": 0.001,
    "case_insensitive": False,
    "case_preserving": True,
}]}


# Convenience field-name lists for parametrized tests
ADVANCED_PERFORMANCE_FIELDS = [
    "read_transfer_size", "read_transfer_max_size", "read_transfer_multiple",
    "write_transfer_size", "write_transfer_max_size", "write_transfer_multiple",
    "directory_transfer_size", "block_size", "max_file_size", "file_name_max_size"
]

ADVANCED_SYNC_FIELDS = [
    "commit_asynchronous", "setattr_asynchronous", "readdirplus",
    "write_filesync_action", "write_filesync_reply",
    "write_datasync_action", "write_datasync_reply",
    "write_unstable_action", "write_unstable_reply"
]

ADVANCED_BOOLEAN_FIELDS = [
    "commit_asynchronous", "setattr_asynchronous", "readdirplus",
    "map_lookup_uid", "symlinks", "no_truncate",
    "return_32bit_file_ids", "can_set_time"
]

ADVANCED_SYNC_CHOICE_FIELDS = [
    "write_filesync_action", "write_filesync_reply",
    "write_datasync_action", "write_datasync_reply",
    "write_unstable_action", "write_unstable_reply"
]


def modify_nfs_advanced_failed_msg():
    return 'Modify NFS export for path: /ifs/test_sample_nfs and access zone: system failed with error'


def create_nfs_advanced_api_failed_msg():
    return 'Create NFS export for path: /ifs/test_sample_nfs and access zone: system failed'


def get_nfs_advanced_failed_msg():
    return 'Got error'
