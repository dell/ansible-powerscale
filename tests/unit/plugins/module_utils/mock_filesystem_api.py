# Copyright:  (c) 2022-2024,  Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of filesystem module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockFileSystemApi:
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'
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
    ZONE_PATH = {
        'summary': {
            'path': '/ifs/sample_zone'
        }
    }
    DATE_TIME = "Thu, 15 Jun 2023 12:20:42 GMT"
    QUOTA_DETAILS_0 = {
        "quotas": [
            {
                "thresholds": {
                    "advisory": 5242880,
                    "hard": 11534336,
                    "soft": 4194304
                },
                "include_snapshots": False
            }
        ]
    }
    #                                          "thresholds_on": "fs_logical_size",
    #                                          "soft_limit_size": 4,
    #                                          "hard_limit_size": 11,
    #                                          "advisory_limit_size": 5,
    #                                          "cap_unit": 'GB',
    #                                          "container": True,
    #                                          "quota_state": "present",
    #                                      }
    # }
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
                "value": DATE_TIME
            },
            {
                "name": "change_time",
                "namespace": None,
                "value": DATE_TIME
            },
            {
                "name": "access_time",
                "namespace": None,
                "value": DATE_TIME
            },
            {
                "name": "create_time",
                "namespace": None,
                "value": DATE_TIME
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

    QUOTA_DETAILS_1 = {
        "quotas": {
            "inodes": 1,
            "logical": 0,
            "physical": 2048
        }
    }
    QUOTA_DETAILS = {

        "quotas": None,
        "resume": None
    }
    EMPTY_NFS_EXPORTS = {
        "exports": None
    }
    EMPTY_SMB_SHARES = {
        "shares": []
    }
    GROUP_IDENTITY_DETAIL = {
        "identities": [
            {
                "targets": [
                    {
                        "on_disk": True,
                        "target": {
                            "id": "id:2000",
                            "name": "test_group",
                            "type": "group"
                        }
                    }
                ]
            }
        ]
    }

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
    def get_error_responses(response_type):
        err_msg_dict = {
            "404_exception": "status is 404",
            "get_filesystem_exception": "Failed to get details of Filesystem",
            "update_quota_error_exception": "Modification of Quota on path",
            "create_quota_exception": "Creation of Quota ifs/ATest3 failed with error:",
            "delete_filesystem_exception": "Deletion of Filesystem",
            "delete_file_system_with_export_exception": "The Filesystem path ifs/ATest3 has NFS exports. Hence, deleting this directory is not safe",
            "acl_validation_exception": "Please specify access_rights or inherit_flags to set ACL",
            "get_acl_exception": "while retrieving the access control list",
            "get_acl_object_exception": "Error SDK Error message while retrieving ACL object instance",
            "get_filesystem_snapshots_exception": "Failed to get filesystem snapshots",
            "get_zone_path_exception": "Unable to fetch base path of Access Zone",
            "get_quota_state_exception": "quota_state is required",
            "get_cap_unit_exception": "Invalid cap_unit provided",
            "invalid_path_exception": "The path provided must start with /",
            "get_group_id_exception": "Failed to get the group id for group",
            "get_owner_id_exception": "Failed to get the owner id",
            "modify_owner_exception": "Failed to modify owner due to error",
            "modify_group_exception": "Failed to modify group due to error",
            "create_file_system_exception": "Creation of Filesystem ifs/ATest3 failed",
            "create_file_system_wo_owner_exception": "owner is required while creating Filesystem",
            "create_file_system_wo_owner_name_exception": "Please specify a name for the owner.",
            "create_file_system_wo_group_name_exception": "Please specify a name for the group.",
            "create_file_system_with_access_control_rights_exception": "Failed to get the wellknown id for wellknown",
            "set_acl_exception": "Setting ACL rights of Filesystem",
            "modify_acl_exception": "Setting ACL rights of Filesystem",
            "modify_acl_posix_exception": "Modification of ACL",
            "check_acl_modified_exception": "determining if ACLs are modified",
            "invalid_wellknown_exception": "Provide valid wellknown",
            "delete_quota_exception": "Deletion of Quota on path",
            "update_quota_exception": "Modification of Quota on path",
            "create_quota_error_exception": "Creation of Quota",
            "get_quota_update_param_exception": "Creation of Quota update param failed with error",
            "update_include_snap_data_exception": "Modifying include_snap_data is not supported",
            "create_quota_get_exception": "Creation of Quota",
            "set_access_control_rights_exception": "Setting ACL rights of Filesystem",
            "is_owner_modified_exception": "Failed to determine if owner is modified",
            "is_group_modified_exception": "Failed to determine if group is modified",
            "get_identity_exception": "Failed to get the identity id"
        }
        return err_msg_dict.get(response_type)
