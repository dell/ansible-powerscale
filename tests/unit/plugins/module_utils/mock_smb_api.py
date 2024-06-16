# Copyright: (c) 2022-24, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock API responses for PowerScale SMB share module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.smb.utils'


class MockSMBApi:

    SMB_NAME = "test_sample_smb"
    PATH1 = "/path"
    STATE_P = "present"
    ALLOW_TYPE = "allow"
    DENY_TYPE = "deny"
    USER1 = "user"
    SYS_AZ = "system"
    SMB_COMMON_ARGS = {
        "share_name": None,
        "path": None,
        "access_zone": None,
        "description": None,
        "permissions": None,
        "state": None,
        "new_share_name": None,
        "access_based_enumeration": None,
        "access_based_enumeration_root_only": None,
        "browsable": None,
        "ntfs_acl_support": None,
        "directory_create_mask": None,
        "directory_create_mode": None,
        "file_create_mask": None,
        "file_create_mode": None,
        "create_path": None,
        "allow_variable_expansion": None,
        "auto_create_directory": None,
        "continuously_available": None,
        "file_filter_extension": None,
        "file_filtering_enabled": None,
        "ca_timeout": None,
        "strict_ca_lockout": None,
        "change_notify": None,
        "oplocks": None,
        "impersonate_guest": None,
        "impersonate_user": None,
        "host_acls": None,
        "run_as_root": None,
        "allow_execute_always": None,
        "allow_delete_readonly": None,
        "inheritable_path_acl": None
    }
    WELLKNOWN_DETAILS = {
        "wellknowns": [
            {
                "name": "everyone",
                "id": "WID:123"
            }
        ]
    }

    SMB = {"shares": [{
        "access_based_enumeration": False,
        "access_based_enumeration_root_only": False,
        "allow_delete_readonly": False,
        "allow_execute_always": False,
        "allow_variable_expansion": True,
        "auto_create_directory": True,
        "browsable": True,
        "ca_timeout": 3600,
        "ca_write_integrity": "write-read-coherent",
        "change_notify": "all",
        "continuously_available": True,
        "create_permissions": "default acl",
        "csc_policy": "manual",
        "description": "description",
        "directory_create_mask": 448,
        "directory_create_mask(octal)": "700",
        "directory_create_mode": 0,
        "directory_create_mode(octal)": "0",
        "file_create_mask": 448,
        "file_create_mask(octal)": "700",
        "file_create_mode": 64,
        "file_create_mode(octal)": "100",
        "file_filter_extensions": ["sample_extension_1"],
        "file_filter_type": "allow",
        "file_filtering_enabled": True,
        "hide_dot_files": False,
        "host_acl": ["allow: root"],
        "id": "test_sample_smb",
        "impersonate_guest": "never",
        "impersonate_user": "",
        "inheritable_path_acl": False,
        "mangle_byte_start": 60672,
        "mangle_map": [
            "0x01-0x1F:-1",
            "0x22:-1",
            "0x2A:-1",
            "0x3A:-1",
            "0x3C:-1",
            "0x3E:-1",
            "0x3F:-1",
            "0x5C:-1"],
        "name": "test_sample_smb",
        "ntfs_acl_support": True,
        "oplocks": True,
        "path": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
        "permissions": [{
            "permission": "read",
            "permission_type": "allow",
            "trustee": {
                "id": "SID:S-1-1-0",
                "name": "Everyone",
                "type": "wellknown"}}],
        "run_as_root": [],
        "smb3_encryption_enabled": False,
        "sparse_file": False,
        "strict_ca_lockout": True,
        "strict_flush": True,
        "strict_locking": False,
        "zid": 1}]}

    @staticmethod
    def get_smb_exception_response(response_type):
        err_msg_dict = {
            'get_smb': "Failed to get details of SMB Share test_sample_smb"
                       " with error SDK Error message",
            'invalid_path': "Invalid path. Valid path is required to create a smb share",
            'invalid_name': "Invalid share name",
            'path_err': "Invalid path path/path, Path must start with '/'",
            'filter_err': "extensions and state are required together when file_filter_extension is mentioned.",
            'rar_persona_err': "Provide valid value for persona name.",
            'create_err': "Failed to create SMB share test_sample_smb with error: SDK Error message",
            'rar_obj_err': "Failed to create persona dict with error SDK Error message",
            'permission_dict_err': "Creating permission dict failed with error SDK Error message",
            'modify_err': "Failed to update the SMB share: test_sample_smb with error: SDK Error message",
            'delete_err': "Failed to delete a SMB share: test_sample_smb with error: SDK Error message",
            'modify_path_err': "Modifying path for a SMB Share is not allowed through Ansible Module",
            'sid_err': "Failed to get the user details for root in zone None and provider None due to error",
        }
        return err_msg_dict.get(response_type)
