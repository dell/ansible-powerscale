# Copyright: (c) 2024, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock API responses for PowerScale Role module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockRoleApi:

    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.role.utils'

    IP_ADDRESS = '1.1.1.1'

    ROLE_COMMON_ARGS = {
        "onefs_host": IP_ADDRESS,
        "role_name": "Test_Role",
        "new_role_name": "",
        "access_zone": "System",
        "copy_role": False,
        "description": "This is role description",
        "privileges": None,
        "members": None,
        "state": "present"}

    PRIVILEGES = {"privileges": [{'id': 'ISI_PRIV_AUDIT', 'name': 'Audit', 'permission': 'w'}]}
    MEMBERS = {'id': 'UID:2140', 'name': 'esa', 'type': 'user'}
    MEMBERS_GROUP = {'id': 'UID:2146', 'name': 'Guest', 'type': 'group'}
    MEMBERS_WELLKNOW = {"wellknowns": [{'id': 'SID:S-1-1-0', 'name': 'user', 'type': 'wellknown'}]}

    GET_ROLE = {
        "role":
            {
                "description":
                "Test_Description",
                "id": "Test_Role",
                "members": [
                    {
                        "id": "UID:2140",
                        "name": "esa",
                        "type": "user"
                    }
                ],
                "name": "Test_Role",
                "privileges": [
                    {
                        "id": "ISI_PRIV_AUDIT",
                        "name": "Audit",
                        "permission": "w"
                    }
                ]
            }
    }

    GET_ROLE_GROUP = {
        "role":
            {
                "description": "Test_Description",
                "id": "Test_Role",
                "members": [
                    {
                        "id": "UID:2146",
                        "name": "esa",
                        "type": "group"
                    }
                ],
                "name": "Test_Role",
                "privileges": [
                    {
                        "id": "ISI_PRIV_AUDIT",
                        "name": "Audit",
                        "permission": "w"
                    }
                ]
            }
    }

    GET_ROLE_WELLKNOWN = {
        "role":
            {
                "description": "Test_Description",
                "id": "Test_Role",
                "members":
                    [
                        {
                            "id": "SID:S-1-1-0",
                            "name": "user",
                            "type": "wellknown"
                        }
                    ],
                "name": "Test_Role",
                "privileges":
                    [
                        {
                            "id": "ISI_PRIV_AUDIT",
                            "name": "Audit",
                            "permission": "w"
                        }
                    ]
            }
    }

    GET_COPY_ROLE = {
        "role":
            {
                "description": "Test_Description",
                "id": "Test_Role_Copy",
                "name": "Test_Role_Copy"
            }
    }

    GET_COPY_ROLE_WITHOUT_NEW_ROLE_NAME = {
        "role":
            {
                "description": "Test_Description",
                "id": "Test_Role_Copy",
                "members":
                    [
                        {
                            "id": "UID:2140",
                            "name": "esa",
                            "type": "user"
                        }
                    ],
                "name": "Test_Role",
                "privileges":
                    [
                        {
                            "id": "ISI_PRIV_AUDIT",
                            "name": "Audit",
                            "permission": "w"
                        }
                    ]
            }
    }

    GET_ROLE_RESPONSE = {
        "description": "Test_Description",
        "id": "Test_Role2",
        "members": [
            {
                "id": "UID:1XXX",
                "name": "admin",
                "type": "user"
            },
            {
                "id": "UID:2XXX",
                "name": "esa",
                "type": "user"
            }
        ],
        "name": "Test_Role2",
        "privileges": [
            {
                "id": "ISI_PRIV_ANTIVIRUS",
                "name": "Antivirus",
                "permission": "w"
            },
            {
                "id": "ISI_PRIV_RECOVERY_SHELL",
                "name": "Recovery Shell",
                "permission": "r"
            }
        ]
    }

    GET_EMPTY_ROLE_RESPONSE = {
        "description": "Test_Description",
        "id": "Test_Role1",
        "name": "Test_Role1",
        "members": [],
        "privileges": []
    }

    USER_DETAILS = {
        "users": [
            {
                "uid": {
                    "id": "User12_Ansible_Test_SMB",
                    "name": "User12_Ansible_Test_SMB",
                    "type": "user"}
            }
        ]
    }

    GROUP_DETAILS = {
        "groups": [
            {
                "gid": {
                    "id": "Group_Ansible_Test_SMB",
                    "name": "Group_Ansible_Test_SMB",
                    "type": "group"}
            }
        ]
    }

    WELLKNOWN_DETAILS = {
        "id": "Everyone",
        "name": "Everyone",
        "type": "wellknown"
    }
    NEW_MEMBER_LIST = [
        {
            "id": "User12_Ansible_Test_SMB",
            "name": "User12_Ansible_Test_SMB",
            "provider_type": "local",
            "type": "user"
        },
        {
            "id": "Group_Ansible_Test_SMB",
            "name": "Group_Ansible_Test_SMB",
            "provider_type": "local",
            "type": "group"
        },
        {
            "id": "Everyone",
            "name": "Everyone",
            "provider_type": "local",
            "type": "wellknown"
        }
    ]

    NEW_MEMBER_LIST_1 = [
        {
            "id": "User12_Ansible_Test_SMB",
            "name": "User12_Ansible_Test_SMB",
            "provider_type": "local",
            "type": "user",
            "state": "present"
        }
    ]
    PRIVILEGE_LIST = {
        "privileges": [
            {
                "category": "Login",
                "description": "Log in from the console",
                "id": "ISI_PRIV_LOGIN_CONSOLE",
                "name": "Console",
                "parent_id": "ISI_PRIV_ZERO",
                "permission": "r",
                "privilegelevel": "flag",
                "uri": ""
            },
            {
                "category": "Configuration",
                "description": "Configure antivirus scanning",
                "id": "ISI_PRIV_ANTIVIRUS",
                "name": "Antivirus",
                "parent_id": "ISI_PRIV_ZERO",
                "permission": "w",
                "privilegelevel": "flag",
                "uri": ""
            },
            {
                "category": "Security",
                "description": "Privilege to enter Recovery Shell from Restricted Shell",
                "id": "ISI_PRIV_RECOVERY_SHELL",
                "name": "Recovery Shell",
                "parent_id": "ISI_PRIV_ZERO",
                "permission": "r",
                "privilegelevel": "flag",
                "uri": ""
            }
        ]
    }
    NEW_PRIVILEGE_LIST = [
        {
            "id": "ISI_PRIV_LOGIN_CONSOLE",
            "name": "Console",
            "permission": "r"
        }
    ]

    @staticmethod
    def get_role_exception_response(response_type):
        if response_type == 'delete_role_exception':
            return "Delete role Test_Role123failed with error: SDK Error message"
        elif response_type == 'create_role_exception':
            return "Create role with failed with error: SDK Error message"
        elif response_type == 'role_name_empty':
            return "Role name cannot be empty"
        elif response_type == 'description_invalid_length':
            return "description must be less than or equal to 255 characters."
        elif response_type == 'create_role_with_invalid_priilage':
            return "Privilege test is either invalid or cannot be added to role in non-System access zone."
        if response_type == 'get_details_exception':
            return "Failed to get details of Role"
        elif response_type == 'modify_exception':
            return "failed with error: SDK Error message"
        elif response_type == 'empty_name_exception':
            return "Role name cannot be empty"
        elif response_type == 'invalid_privilege_exception':
            return "Privilage invalid_privilege is either invalid or cannot be added to role in non-System access zone."
