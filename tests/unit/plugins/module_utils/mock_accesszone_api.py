# Copyright: (c) 2021-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock API responses for PowerScale Access zone module"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

MODULE_UTILS_PATH = (
    "ansible_collections.dellemc.powerscale.plugins.modules.accesszone.utils"
)

ACCESS_ZONE_DETAILS_1 = {
    "zones": [
        {
            "alternate_system_provider": "lsa-file-provider:System",
            "auth_providers": ["ldap:ansildap"],
            "cache_entry_expiry": 14400,
            "create_path": None,
            "force_overlap": None,
            "groupnet": "groupnet0",
            "home_directory_umask": 63,
            "id": "System",
            "ifs_restricted": [],
            "map_untrusted": "",
            "name": "System",
            "negative_cache_entry_expiry": 60,
            "netbios_name": "",
            "path": "/ifs",
            "skeleton_directory": "/usr/share",
            "system": True,
            "system_provider": "lsa-file-provider:System",
            "user_mapping_rules": [
                "test_user_13 ++ test_user_15 [user]",
                "test_user_14 => test_user []",
                "test_user_13 ++ test_user_15 [user]",
                "test_user_12 &= test_user_13 []",
            ],
            "zone_id": 1,
        }
    ],
    "smb_settings": {
        "create_permissions": "default acl test",
        "directory_create_mask": "700",
        "directory_create_mode": "100",
        "file_create_mask": "777",
        "file_create_mode": "700",
        "access_based_enumeration": False,
        "access_based_enumeration_root_only": False,
        "ntfs_acl_support": False,
        "oplocks": False,
    },
    "nfs_settings": {
        "export_settings": {"commit_asynchronous": True},
        "zone_settings": {
            "nfsv4_allow_numeric_ids": True,
            "nfsv4_domain": "test_domain",
            "nfsv4_no_domain": True,
            "nfsv4_no_domain_uids": True,
            "nfsv4_no_names": True,
        },
    },
}

ACCESS_ZONE_DETAILS_2 = {
    "zones": [
        {
            "az_name": "testaz",
            "groupnet": "groupnet1",
            "path": "/ifs",
            "iface": "ext-1",
            "create_path": False,
            "provider_state_add": "add",
            "provider_state_remove": None,
            "auth_providers": ["ldap:ansildap"],
        }
    ]
}

NFS_EXPORT_SETTINGS = {
    "settings": {
        "all_dirs": False,
        "block_size": 8192,
        "can_set_time": True,
        "case_insensitive": False,
        "case_preserving": True,
        "chown_restricted": False,
        "commit_asynchronous": False,
        "directory_transfer_size": 131072,
        "encoding": "DEFAULT",
        "link_max": 32767,
        "map_all": None,
        "map_failure": {
            "enabled": False,
            "primary_group": {"id": None, "name": None, "type": None},
            "secondary_groups": [],
            "user": {"id": "USER:nobody", "name": None, "type": None},
        },
        "map_full": True,
        "map_lookup_uid": False,
        "map_non_root": {
            "enabled": False,
            "primary_group": {"id": None, "name": None, "type": None},
            "secondary_groups": [],
            "user": {"id": "USER:nobody", "name": None, "type": None},
        },
        "map_retry": True,
        "map_root": {
            "enabled": True,
            "primary_group": {"id": None, "name": None, "type": None},
            "secondary_groups": [],
            "user": {"id": "USER:nobody", "name": None, "type": None},
        },
        "max_file_size": 9223372036854775807,
        "name_max_size": 255,
        "no_truncate": False,
        "read_only": False,
        "read_transfer_max_size": 1048576,
        "read_transfer_multiple": 512,
        "read_transfer_size": 131072,
        "readdirplus": True,
        "readdirplus_prefetch": 10,
        "return_32bit_file_ids": False,
        "security_flavors": ["unix"],
        "setattr_asynchronous": False,
        "snapshot": "-",
        "symlinks": True,
        "time_delta": 1e-09,
        "write_datasync_action": "DATASYNC",
        "write_datasync_reply": "DATASYNC",
        "write_filesync_action": "FILESYNC",
        "write_filesync_reply": "FILESYNC",
        "write_transfer_max_size": 1048576,
        "write_transfer_multiple": 512,
        "write_transfer_size": 524288,
        "write_unstable_action": "UNSTABLE",
        "write_unstable_reply": "UNSTABLE",
        "zone": "System",
    }
}

NFS_ZONE_SETTINGS = {
    "settings": {
        "nfsv4_allow_numeric_ids": True,
        "nfsv4_domain": "localhost",
        "nfsv4_no_domain": False,
        "nfsv4_no_domain_uids": True,
        "nfsv4_no_names": False,
        "nfsv4_replace_domain": True,
        "zone": None,
    }
}

SMB_SHARE_SETTINGS = {
    "settings": {
        "access_based_enumeration": False,
        "access_based_enumeration_root_only": False,
        "allow_delete_readonly": False,
        "allow_execute_always": False,
        "ca_timeout": 120,
        "ca_write_integrity": "write-read-coherent",
        "change_notify": "norecurse",
        "continuously_available": None,
        "create_permissions": "default acl",
        "csc_policy": None,
        "directory_create_mask": 448,
        "directory_create_mask(octal)": "700",
        "directory_create_mode": 0,
        "directory_create_mode(octal)": "0",
        "file_create_mask": 448,
        "file_create_mask(octal)": "700",
        "file_create_mode": 64,
        "file_create_mode(octal)": "100",
        "file_filter_extensions": [],
        "file_filter_type": "deny",
        "file_filtering_enabled": False,
        "hide_dot_files": False,
        "host_acl": [],
        "impersonate_guest": "never",
        "impersonate_user": "",
        "ntfs_acl_support": True,
        "oplocks": True,
        "smb3_encryption_enabled": False,
        "sparse_file": False,
        "strict_ca_lockout": True,
        "strict_flush": True,
        "strict_locking": False,
        "zone": None,
    }
}


class ProviderSummary:
    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type


def get_error_message(response_type, az_name=None):
    error_msg = {
        "create_zone_exception": f"Creation of access zone {az_name} failed with error:",
        "create_zone_without_path_exception": "Provide a valid path to create an access zone",
        "delete_zone_exception": "Failed to delete access zone",
        "get_zone_exception": f"Get details of access zone {az_name} failed with error:",
        "provider_type_no_exist_exception": "Provider: System of type: file does not exist",
        "add_provider_exception": f"Add auth providers to access zone {az_name} failed with error:",
        "remove_provider_exception": f"Remove auth providers to access zone {az_name} failed with error:",
        "modify_smb_exception": f"Modify SMB share settings of access zone {az_name} failed with error",
        "modify_smb_conversion_exception": "Conversion from octal to decimal failed",
        "modify_nfs_exception": f"Modify NFS export settings of access zone {az_name} failed with error",
    }
    return error_msg[response_type]
