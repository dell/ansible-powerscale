# Copyright:  (c) 2022,  Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of filesystem module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockFileSystemApi:
    FILE_SYSTEM_MODULE_ARGS = {
        'unispherehost': '**.***.**.***',
        'path': None,
        'access_zone': None,
        'owner': None,
        'group': None,
        'access_control': None,
        'recursive': None,
        'recursive_force_delete': None,
        'quota': None,
        'state': None
    }

    FILESYSTEM_DETAILS = {
        "attrs": [
            {
                "name": "is_hidden",
                "namespace": None,
                "value": "False"
            },
            {
                "name": "size",
                "namespace": None,
                "value": "0"
            },
            {
                "name": "block_size",
                "namespace": None,
                "value": "8192"
            },
            {
                "name": "blocks",
                "namespace": None,
                "value": "4"
            },
            {
                "name": "last_modified",
                "namespace": None,
                "value": "Thu, 15 Jun 2023 12:20:42 GMT"
            },
            {
                "name": "change_time",
                "namespace": None,
                "value": "Thu, 15 Jun 2023 12:20:42 GMT"
            },
            {
                "name": "access_time",
                "namespace": None,
                "value": "Thu, 15 Jun 2023 12:20:42 GMT"
            },
            {
                "name": "create_time",
                "namespace": None,
                "value": "Thu, 15 Jun 2023 12:20:42 GMT"
            },
            {
                "name": "mtime_val",
                "namespace": None,
                "value": "1686831642"
            },
            {
                "name": "ctime_val",
                "namespace": None,
                "value": "1686831642"
            },
            {
                "name": "atime_val",
                "namespace": None,
                "value": "1686831642"
            },
            {
                "name": "btime_val",
                "namespace": None,
                "value": "1686831642"
            },
            {
                "name": "owner",
                "namespace": None,
                "value": "Unknown User"
            },
            {
                "name": "group",
                "namespace": None,
                "value": "wheel"
            },
            {
                "name": "uid",
                "namespace": None,
                "value": "2000"
            },
            {
                "name": "gid",
                "namespace": None,
                "value": "0"
            },
            {
                "name": "id",
                "namespace": None,
                "value": "4367853241"
            },
            {
                "name": "nlink",
                "namespace": None,
                "value": "2"
            },
            {
                "name": "type",
                "namespace": None,
                "value": "container"
            },
            {
                "name": "stub",
                "namespace": None,
                "value": "False"
            },
            {
                "name": "mode",
                "namespace": None,
                "value": "0700"
            }
        ],
        "namespace_acl": {
            "acl": [
                {
                    "accessrights": [
                        "dir_gen_read",
                        "dir_gen_write",
                        "dir_gen_execute",
                        "std_write_dac",
                        "delete_child"
                    ],
                    "accesstype": "allow",
                    "inherit_flags": [
                        "object_inherit"
                    ],
                    "op": None,
                    "trustee": {
                        "id": "UID:2000",
                        "name": None,
                        "type": None
                    }
                },
                {
                    "accessrights": [
                        "std_read_dac",
                        "std_synchronize",
                        "dir_read_attr"
                    ],
                    "accesstype": "allow",
                    "inherit_flags": [],
                    "op": None,
                    "trustee": {
                        "id": "GID:0",
                        "name": "wheel",
                        "type": "group"
                    }
                }
            ],
            "action": "replace",
            "authoritative": "acl",
            "group": {
                "id": "GID:0",
                "name": "wheel",
                "type": "group"
            },
            "mode": "0700",
            "owner": {
                "id": "UID:2000",
                "name": None,
                "type": None
            }
        }
    }

    QUOTA_DETAILS = {

        "quotas": [],
        "resume": None
    }

    @staticmethod
    def delete_file_system_response(error):
        return "Deletion of Filesystem"

    @staticmethod
    def get_acl_response():
        return {'acl': [
            {
                "accessrights": [
                    "std_read_dac",
                    "std_synchronize",
                    "dir_read_attr"
                ],
                "accesstype": "allow",
                "inherit_flags": [],
                "trustee": {
                    "id": "id:2000",
                    "name": "test_group_1",
                    "type": "group"
                }
            }],
            "authoritative": "acl",
            "group": {
                "id": "id:2000",
                "name": "test_group_1",
                "type": "group"},
            "mode": "0000",
            "owner": {
                "id": "id:2001",
                "name": "ansible_test_user1",
                "type": "user"}
        }

    @staticmethod
    def get_acl_validation_error():
        return "Please specify access_rights or inherit_flags to set ACL"

    @staticmethod
    def file_system_create_quota_response(error):
        return "Creation of Quota ifs/ATest3 failed with error: None"

    @staticmethod
    def file_system_update_quota_response(error):
        return "Modification of Quota on path"
