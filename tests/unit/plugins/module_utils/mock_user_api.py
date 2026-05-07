# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of User module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockUserApi:
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'
    PRIMARY_GROUP = 'Isilon Users'
    USER_COMMON_ARGS = {
        'onefs_host': '**.***.**.***',
        'user_name': None,
        'user_id': None,
        'password': None,
        'access_zone': None,
        'provider_type': None,
        'enabled': None,
        'primary_group': None,
        'shell': None,
        'full_name': None,
        'email': None,
        'role_name': None,
        'role_state': None,
        'home_directory': None,
        'state': None
    }

    CREATE_USER_WITH_ID = {
        'name': 'test_user_1',
        'uid': 7000,
        'password': '1234567',
        'enabled': False,
        'primary_group': PRIMARY_GROUP,
        'home_directory': None,
        'shell': '/usr/eee',
        'gecos': 'Test User',
        'email': 'test_user_2@gamil.com'
    }
    GET_USER_DETAILS = {
        "dn": "CN=test_user_1,CN=Users,DC=VXX267-XX",
        "dns_domain": None,
        "domain": "VXX267-XX",
        "email": "test_user_2@gamil.com",
        "enabled": False,
        "expired": False,
        "expiry": None,
        "gecos": "Test User",
        "generated_gid": False,
        "generated_uid": False,
        "generated_upn": True,
        "gid": {
            "id": "GID:1800",
            "name": PRIMARY_GROUP,
            "type": "group"
        },
        "home_directory": "/ifs/sample-zone/home/test_user_1",
        "id": "test_user_1",
        "locked": False,
        "max_password_age": 2419200,
        "member_of": None,
        "name": "test_user_1",
        "object_history": [],
        "on_disk_group_identity": {
            "id": "GID:1800",
            "name": PRIMARY_GROUP,
            "type": "group"
        },
        "on_disk_user_identity": {
            "id": "UID:7000",
            "name": "test_user_1",
            "type": "user"
        },
        "password_expired": False,
        "password_expires": True,
        "password_expiry": 1678765332,
        "password_last_set": 1676346132,
        "primary_group_sid": {
            "id": "SID:S-1-5-21-4168384747-3913729650-1141909635-800",
            "name": "Isilon Users",
            "type": "group"
        },
        "prompt_password_change": False,
        "provider": "lsa-local-provider:sample-zone",
        "sam_account_name": "test_user_1",
        "shell": "/usr/eee",
        "sid": {
            "id": "SID:S-1-5-21-4168384747-3913729650-1141909635-3496",
            "name": "test_user_1",
            "type": "user"
        },
        "ssh_public_keys": [],
        "type": "user",
        "uid": {
            "id": "UID:7000",
            "name": "test_user_1",
            "type": "user"
        },
        "upn": "test_user_1@VXX267-XX",
        "user_can_change_password": True
    }

    ZONE_SUMMARY = {
        "summary": {
            "path": "/ifs/test_user_1",
        }
    }

    @staticmethod
    def get_error_responses(response_type):
        err_msg_dict = {
            "get_create_user_id": "Create User 'test_user_1' failed with ",
            "get_user_details_error": "Get User Details UID:7000 failed with ",
            "get_user_details_role_error": "Exception when calling AuthApi->list_auth_roles",
            "create_user_with_empty_name": "Unable to create a user, 'user_name' is missing",
            "create_user_with_empty_password": "Unable to create a user, 'password' is missing",
            "create_user_with_existing_id": "User already exists with UID",
            "create_user_with_non_local_provider": "user is allowed only if provider_type is local",
            "error_fetch_base_path": "Unable to fetch base path of Access Zone",
            "param_error_user_id_and_name": "Invalid user_name or user_id provided",
            "param_error_email_format": "Email is not in the correct format",
            "param_error_role_name_and_state": "role_name and role_state both are required",
            "param_error_role_and_zone": "roles can be assigned to users and groups of System Access Zone",
            "delete_user_error": "Delete User 'UID:7000' failed with ",
            "delete_user_non_local_provider_error": "Cannot delete user from fake-provider provider_type",
            "update_user_error": "Update User 'UID:7000' failed with ",
            "update_user_add_role_error": "Add user UID:7000 to role AuditAdmin failed with SDK Error message",
            "update_user_remove_role_error": "Remove user UID:7000 from role AuditAdmin failed with SDK Error message",
            "update_password_error": "Update password for User 'UID:7000' failed with",
        }
        return err_msg_dict.get(response_type)
