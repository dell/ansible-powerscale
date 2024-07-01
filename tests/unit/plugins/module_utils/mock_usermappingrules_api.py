# Copyright: (c) 2023, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of user mapping rules module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockUserMappingRuleApi:
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'
    USER_MAPPING_RULES_COMMON_ARGS = {
        'onefs_host': '**.***.**.***',
        'apply_order': None,
        'new_order': None,
        'rule': None,
        'access_zone': 'System',
        'state': None
    }
    GET_USERMAPPINGRULE_RESPONSE = {
        'rules': {
            'rules': [
                {
                    'operator': 'insert',
                    'options': {
                        '_break': False,
                        'default_user': None,
                        'group': False,
                        'groups': False,
                        'user': False
                    },
                    'user1': {
                        'domain': None,
                        'user': 'test_ans_user'
                    },
                    'user2': {
                        'domain': None,
                        'user': 'Test_userAnand'
                    }
                }
            ]
        }
    }

    GET_USERMAPPINGRULE_RESPONSE_FOR_TRIM = {
        'rules': {
            'rules': [
                {
                    'operator': 'trim',
                    'options': {
                        '_break': False,
                        'default_user': None,
                        'group': False,
                        'groups': False,
                        'user': False
                    },
                    'user1': {
                        'domain': None,
                        'user': 'test_ans_user'
                    }
                }
            ]
        }
    }

    @staticmethod
    def get_usermappingrules_exception_response(response_type):
        if response_type == 'get_details_exception':
            return "Fetching user mapping rule failed with error: SDK Error message"
        elif response_type == 'create_exception':
            return "Creating user mapping rule failed with error: SDK Error message"
        elif response_type == 'delete_exception':
            return "Deleting user mapping rule failed with error: SDK Error message"
        elif response_type == 'update_exception':
            return "Updating user mapping rule failed with error: SDK Error message"

    @staticmethod
    def get_error_responses(response_type):
        if response_type == 'operator_error':
            return " 'operator' is required for creation of user mapping rule."
        elif response_type == 'user2_error':
            return " 'user2' is required for creation of user mapping rule."
        elif response_type == 'user1_error':
            return " 'user1' is required for creation of user mapping rule."
        elif response_type == 'group_error':
            return " '['group', 'groups', 'user']' cannot be given with '['replace', 'union']' operators."
        elif response_type == 'trim_user_error':
            return " '['group', 'groups', 'user', 'default_user']' cannot be given with 'trim' operator."
        elif response_type == 'trim_user2_error':
            return "'user2' cannot be given with 'trim' operator."
        elif response_type == 'trim_update_error':
            return " 'user2' is required for insert."
        elif response_type == 'delete_without_order':
            return "'apply_order' is required to delete the rule"
        elif response_type == 'invalid_new_order':
            return "new_order should be greater than 0."
        elif response_type == 'invalid_apply_order':
            return "apply_order should be greater than 0."
        elif response_type == 'new_order_error':
            return "Updating user mapping rule failed with error: new_order should be in range of 1 to 1"
        elif response_type == 'outbound_apply_order':
            return "Fetching user mapping rule failed with error: apply order should be in range of 1 to 1"
