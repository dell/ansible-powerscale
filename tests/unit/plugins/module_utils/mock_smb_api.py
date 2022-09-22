# Copyright: (c) 2022, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock API responses for PowerScale SMB share module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.smb.utils'

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
       "host_acl": [],
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


CREATE_SMB_PARAMS = {
    "name": "test_sample_smb",
    "path": "/ifs",
    "description": "description",
    "permissions": [
        {
            "user_name": "system_az_user",
            "permission": "full",
            "permission_type": "allow"},
        {
            "group_name": "system_az_group",
            "permission": "read",
            "permission_type": "allow"},
        {
            "wellknown": "everyone",
            "permission": "read",
            "permission_type": "allow"}],
    "directory_create_mask": "700",
    "directory_create_mode": "0",
    "file_create_mask": "700",
    "file_create_mode": "100",
    "ntfs_acl_support": False,
    "access_based_enumeration": True,
    "access_based_enumeration_root_only": True,
    "browsable": True,
    "create_path": False,
    "allow_variable_expansion": True,
    "auto_create_directory": True,
    "continuously_available": True,
    "smb3_encryption_enabled": True,
    "ca_write_integrity": "full",
    "file_filter_extensions": ['sample_extension_1'],
    "file_filter_type": "allow",
    "file_filtering_enabled": True,
    "file_filter_extension_state": "present-in-share",
    "ca_timeout": 60,
    "ca_timeout_unit": "minutes",
    "strict_ca_lockout": True,
    "change_notify": "all",
    "oplocks": True,
    "impersonate_guest": "never",
    "impersonate_user": True,
    "host_acl": []}

MODIFY_SMB_PARAMS = {
    "name": "test_sample_smb",
    "path": "/ifs",
    "description": "description",
    "permissions": [
        {
            "user_name": "system_az_user",
            "permission": "full",
            "permission_type": "allow"},
        {
            "group_name": "system_az_group",
            "permission": "read",
            "permission_type": "allow"},
        {
            "wellknown": "everyone",
            "permission": "read",
            "permission_type": "deny"}],
    "directory_create_mask": "700",
    "directory_create_mode": "0",
    "file_create_mask": "700",
    "file_create_mode": "100",
    "ntfs_acl_support": False,
    "access_based_enumeration": True,
    "access_based_enumeration_root_only": True,
    "browsable": False,
    "create_path": False,
    "allow_variable_expansion": True,
    "auto_create_directory": True,
    "continuously_available": True,
    "smb3_encryption_enabled": True,
    "ca_write_integrity": "full",
    "file_filter_extensions": ['sample_extension_1'],
    "file_filter_type": "allow",
    "file_filtering_enabled": True,
    "file_filter_extension_state": "present-in-share",
    "ca_timeout": 1000,
    "strict_ca_lockout": False,
    "change_notify": "all",
    "oplocks": True,
    "impersonate_guest": "never",
    "impersonate_user": True,
    "host_acl": []}


def create_smb_failed_msg():
    return 'Failed to create SMB share'


def modify_smb_failed_msg():
    return 'Failed to update the SMB share'


def delete_smb_failed_msg():
    return 'Failed to delete a SMB share'
