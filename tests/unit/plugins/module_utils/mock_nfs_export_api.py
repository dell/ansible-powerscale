# Copyright: (c) 2022, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

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

NFS_COMMON_ARGS = {
    "path": None,
    "access_zone": None,
    "clients": None,
    "root_clients": None,
    "read_only_clients": None,
    "read_write_clients": None,
    "client_state": None,
    "description": None,
    "read_only": None,
    "sub_directories_mountable": None,
    "security_flavors": None,
    "ignore_unresolvable_hosts": None,
    "state": None
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
    "security_flavors": ["kerberos"]
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
}


def get_nfs_failed_msg():
    return 'Got error SDK Error message while getting NFS export details for path'


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
