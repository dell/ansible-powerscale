# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for user mapping rules module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import copy
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.user_mapping_rule import UserMappingRule
from ansible_collections.dellemc.powerscale.plugins.modules.user_mapping_rule import UserMappingRuleHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_usermappingrules_api \
    import MockUserMappingRuleApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_fail_json \
    import FailJsonException, fail_json
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse


class TestUserMappingRule():
    usermappingrules_args = MockUserMappingRuleApi.USER_MAPPING_RULES_COMMON_ARGS

    @pytest.fixture
    def usermappingrules_module_mock(self, mocker):
        mocker.patch(MockUserMappingRuleApi.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        usermappingrules_module_mock = UserMappingRule()
        usermappingrules_module_mock.module.check_mode = False
        usermappingrules_module_mock.module.fail_json = fail_json
        return usermappingrules_module_mock

    def test_get_usermappingrules(self, usermappingrules_module_mock):
        usermappingrules_details = MockUserMappingRuleApi.GET_USERMAPPINGRULE_RESPONSE
        self.usermappingrules_args.update({
            'apply_order': 1,
            'state': 'present'
        })
        usermappingrules_module_mock.module.params = self.usermappingrules_args
        usermappingrules_module_mock.auth_api.get_mapping_users_rules = MagicMock(return_value=MockSDKResponse(usermappingrules_details))
        UserMappingRuleHandler().handle(usermappingrules_module_mock, usermappingrules_module_mock.module.params)
        assert usermappingrules_module_mock.module.exit_json.call_args[1]['changed'] is False
        assert usermappingrules_details['rules']['rules'][0] == usermappingrules_module_mock.module.exit_json.call_args[1]['user_mapping_rule_details']

    def capture_fail_json_call(self, error_msg, usermappingrules_module_mock):
        try:
            UserMappingRuleHandler().handle(usermappingrules_module_mock, usermappingrules_module_mock.module.params)
        except FailJsonException as fj_object:
            assert error_msg == fj_object.message

    def test_get_usermappingrules_exception(self, usermappingrules_module_mock):
        self.usermappingrules_args.update({
            'apply_order': 1,
            'state': 'present'
        })
        usermappingrules_module_mock.module.params = self.usermappingrules_args
        usermappingrules_module_mock.auth_api.get_mapping_users_rules = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(MockUserMappingRuleApi.get_usermappingrules_exception_response('get_details_exception'), usermappingrules_module_mock)

    def test_create_usermappingrule(self, usermappingrules_module_mock):
        usermappingrules_details = MockUserMappingRuleApi.GET_USERMAPPINGRULE_RESPONSE
        usermappingrules_details_after_update = copy.deepcopy(usermappingrules_details)
        usermappingrules_details_after_update['rules']['rules'].append(usermappingrules_details['rules']['rules'][0])
        self.usermappingrules_args.update({
            'rule': {
                'operator': 'insert',
                'options': {
                    'break_on_match': False,
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
            },
            'state': 'present'
        })
        mock_none_response = MagicMock(return_value=None)
        usermappingrules_module_mock.module.params = self.usermappingrules_args
        usermappingrules_module_mock.auth_api.get_mapping_users_rules = MagicMock(side_effect=[MockSDKResponse(usermappingrules_details),
                                                                                               MockSDKResponse(usermappingrules_details_after_update)])
        usermappingrules_module_mock.auth_api.update_mapping_users_rules = mock_none_response
        UserMappingRuleHandler().handle(usermappingrules_module_mock, usermappingrules_module_mock.module.params)
        assert usermappingrules_module_mock.module.exit_json.call_args[1]['changed'] is True
        assert usermappingrules_details_after_update['rules']['rules'][1] == \
            usermappingrules_module_mock.module.exit_json.call_args[1]['user_mapping_rule_details']

    def test_create_usermappingrule_exception(self, usermappingrules_module_mock):
        usermappingrules_details = MockUserMappingRuleApi.GET_USERMAPPINGRULE_RESPONSE
        usermappingrules_details_after_update = copy.deepcopy(usermappingrules_details)
        usermappingrules_details_after_update['rules']['rules'].append(usermappingrules_details['rules']['rules'][0])
        self.usermappingrules_args.update({
            'rule': {
                'operator': 'insert',
                'options': {
                    'break_on_match': False,
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
            },
            'state': 'present'
        })
        usermappingrules_module_mock.module.params = self.usermappingrules_args
        usermappingrules_module_mock.auth_api.get_mapping_users_rules = MagicMock(side_effect=[MockSDKResponse(usermappingrules_details),
                                                                                               MockSDKResponse(usermappingrules_details_after_update)])
        usermappingrules_module_mock.auth_api.update_mapping_users_rules = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(MockUserMappingRuleApi.get_usermappingrules_exception_response('create_exception'), usermappingrules_module_mock)

    def test_update_usermappingrule(self, usermappingrules_module_mock):
        usermappingrules_details = MockUserMappingRuleApi.GET_USERMAPPINGRULE_RESPONSE
        usermappingrules_details['rules']['rules'].append(usermappingrules_details['rules']['rules'][0])
        usermappingrules_details_after_update = copy.deepcopy(usermappingrules_details)
        new_rule = copy.deepcopy(usermappingrules_details['rules']['rules'][0])
        new_rule['rule'] = {
            'operator': 'insert',
            'options': {
                'break_on_match': True,
                'default_user': None,
                'group': True,
                'groups': True,
                'user': True
            },
            'user1': {
                'domain': None,
                'user': 'test_ans_users'
            },
            'user2': {
                'domain': None,
                'user': 'Test_userAnands'
            }
        }
        usermappingrules_details_after_update['rules']['rules'][0] = new_rule
        self.usermappingrules_args.update({
            'apply_order': 2,
            'new_order': 1,
            'rule': new_rule['rule'],
            'state': 'present'
        })
        mock_none_response = MagicMock(return_value=None)
        usermappingrules_module_mock.module.params = self.usermappingrules_args
        usermappingrules_module_mock.auth_api.get_mapping_users_rules = MagicMock(side_effect=[MockSDKResponse(usermappingrules_details),
                                                                                               MockSDKResponse(usermappingrules_details),
                                                                                               MockSDKResponse(usermappingrules_details_after_update)])
        usermappingrules_module_mock.auth_api.update_mapping_users_rules = mock_none_response
        UserMappingRuleHandler().handle(usermappingrules_module_mock, usermappingrules_module_mock.module.params)
        assert usermappingrules_module_mock.module.exit_json.call_args[1]['changed'] is True
        assert new_rule == usermappingrules_module_mock.module.exit_json.call_args[1]['user_mapping_rule_details']

    def test_update_operator_usermappingrule(self, usermappingrules_module_mock):
        usermappingrules_details = MockUserMappingRuleApi.GET_USERMAPPINGRULE_RESPONSE
        usermappingrules_details['rules']['rules'].append(usermappingrules_details['rules']['rules'][0])
        usermappingrules_details_after_update = copy.deepcopy(usermappingrules_details)
        new_rule = copy.deepcopy(usermappingrules_details['rules']['rules'][0])
        new_rule['rule'] = {
            'operator': 'trim'
        }
        usermappingrules_details_after_update['rules']['rules'][0] = new_rule
        self.usermappingrules_args.update({
            'apply_order': 2,
            'new_order': 1,
            'rule': new_rule['rule'],
            'state': 'present'
        })
        mock_none_response = MagicMock(return_value=None)
        usermappingrules_module_mock.module.params = self.usermappingrules_args
        usermappingrules_module_mock.auth_api.get_mapping_users_rules = MagicMock(side_effect=[MockSDKResponse(usermappingrules_details),
                                                                                               MockSDKResponse(usermappingrules_details),
                                                                                               MockSDKResponse(usermappingrules_details_after_update)])
        usermappingrules_module_mock.auth_api.update_mapping_users_rules = mock_none_response
        UserMappingRuleHandler().handle(usermappingrules_module_mock, usermappingrules_module_mock.module.params)
        assert usermappingrules_module_mock.module.exit_json.call_args[1]['changed'] is True
        assert new_rule == usermappingrules_module_mock.module.exit_json.call_args[1]['user_mapping_rule_details']

    def test_update_trim_usermappingrule_exception(self, usermappingrules_module_mock):
        usermappingrules_details = MockUserMappingRuleApi.GET_USERMAPPINGRULE_RESPONSE_FOR_TRIM
        usermappingrules_details['rules']['rules'].append(usermappingrules_details['rules']['rules'][0])
        usermappingrules_details_after_update = copy.deepcopy(usermappingrules_details)
        new_rule = copy.deepcopy(usermappingrules_details['rules']['rules'][0])
        new_rule['rule'] = {
            'operator': 'insert'
        }
        usermappingrules_details_after_update['rules']['rules'][0] = new_rule
        self.usermappingrules_args.update({
            'apply_order': 2,
            'new_order': 1,
            'rule': new_rule['rule'],
            'state': 'present'
        })
        mock_none_response = MagicMock(return_value=None)
        usermappingrules_module_mock.module.params = self.usermappingrules_args
        usermappingrules_module_mock.auth_api.get_mapping_users_rules = MagicMock(side_effect=[MockSDKResponse(usermappingrules_details),
                                                                                               MockSDKResponse(usermappingrules_details)])
        usermappingrules_module_mock.auth_api.update_mapping_users_rules = mock_none_response
        self.capture_fail_json_call(MockUserMappingRuleApi.get_error_responses('trim_update_error'), usermappingrules_module_mock)

    def test_update_usermappingrule_exception(self, usermappingrules_module_mock):
        usermappingrules_details = MockUserMappingRuleApi.GET_USERMAPPINGRULE_RESPONSE
        usermappingrules_details['rules']['rules'].append(usermappingrules_details['rules']['rules'][0])
        usermappingrules_details_after_update = copy.deepcopy(usermappingrules_details)
        new_rule = copy.deepcopy(usermappingrules_details['rules']['rules'][0])
        new_rule['rule'] = {
            'operator': 'insert',
            'options': {
                'break_on_match': True,
                'default_user': {
                    'domain': None,
                    'user': 'test_ans_users'
                },
                'group': True,
                'groups': True,
                'user': True
            },
            'user1': {
                'domain': None,
                'user': 'test_ans_users'
            },
            'user2': {
                'domain': None,
                'user': 'Test_userAnands'
            }
        }
        usermappingrules_details_after_update['rules']['rules'][0] = new_rule
        self.usermappingrules_args.update({
            'apply_order': 2,
            'new_order': 1,
            'rule': new_rule['rule'],
            'state': 'present'
        })
        usermappingrules_module_mock.module.params = self.usermappingrules_args
        usermappingrules_module_mock.auth_api.get_mapping_users_rules = MagicMock(side_effect=[MockSDKResponse(usermappingrules_details),
                                                                                               MockSDKResponse(usermappingrules_details),
                                                                                               MockSDKResponse(usermappingrules_details_after_update)])
        usermappingrules_module_mock.auth_api.update_mapping_users_rules = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(MockUserMappingRuleApi.get_usermappingrules_exception_response('update_exception'), usermappingrules_module_mock)

    def test_delete_usermappingrule(self, usermappingrules_module_mock):
        usermappingrules_details = MockUserMappingRuleApi.GET_USERMAPPINGRULE_RESPONSE
        self.usermappingrules_args.update({
            'apply_order': 1,
            'state': 'absent'
        })
        mock_none_response = MagicMock(return_value=None)
        usermappingrules_module_mock.module.params = self.usermappingrules_args
        usermappingrules_module_mock.auth_api.get_mapping_users_rules = MagicMock(return_value=MockSDKResponse(usermappingrules_details))
        usermappingrules_module_mock.auth_api.update_mapping_users_rules = mock_none_response
        UserMappingRuleHandler().handle(usermappingrules_module_mock, usermappingrules_module_mock.module.params)
        assert usermappingrules_module_mock.module.exit_json.call_args[1]['changed'] is True
        assert usermappingrules_module_mock.module.exit_json.call_args[1]['user_mapping_rule_details'] == {}

    def test_delete_usermappingrule_exception(self, usermappingrules_module_mock):
        usermappingrules_details = MockUserMappingRuleApi.GET_USERMAPPINGRULE_RESPONSE
        self.usermappingrules_args.update({
            'apply_order': 1,
            'state': 'absent'
        })
        usermappingrules_module_mock.module.params = self.usermappingrules_args
        usermappingrules_module_mock.auth_api.get_mapping_users_rules = MagicMock(return_value=MockSDKResponse(usermappingrules_details))
        usermappingrules_module_mock.auth_api.update_mapping_users_rules = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(MockUserMappingRuleApi.get_usermappingrules_exception_response('delete_exception'), usermappingrules_module_mock)

    def test_create_usermappingrule_without_operator(self, usermappingrules_module_mock):
        self.usermappingrules_args.update({
            'rule': {
                'user1': {
                    'domain': None,
                    'user': 'test_ans_users'
                },
            },
            'state': 'present'
        })
        mock_none_response = MagicMock(return_value=None)
        usermappingrules_module_mock.module.params = self.usermappingrules_args
        usermappingrules_module_mock.form_rule_payload = mock_none_response
        usermappingrules_module_mock.create_user_mapping_rule = mock_none_response
        self.capture_fail_json_call(MockUserMappingRuleApi.get_error_responses('operator_error'), usermappingrules_module_mock)

    def test_create_usermappingrule_without_user2(self, usermappingrules_module_mock):
        self.usermappingrules_args.update({
            'rule': {
                'operator': 'insert',
                'user1': {
                    'domain': None,
                    'user': 'test_ans_users'
                },
            },
            'state': 'present'
        })
        mock_none_response = MagicMock(return_value=None)
        usermappingrules_module_mock.module.params = self.usermappingrules_args
        usermappingrules_module_mock.form_rule_payload = mock_none_response
        usermappingrules_module_mock.create_user_mapping_rule = mock_none_response
        self.capture_fail_json_call(MockUserMappingRuleApi.get_error_responses('user2_error'), usermappingrules_module_mock)

    def test_create_usermappingrule_without_user1(self, usermappingrules_module_mock):
        self.usermappingrules_args.update({
            'rule': {
                'operator': 'trim'
            },
            'state': 'present'
        })
        mock_none_response = MagicMock(return_value=None)
        usermappingrules_module_mock.module.params = self.usermappingrules_args
        usermappingrules_module_mock.form_rule_payload = mock_none_response
        usermappingrules_module_mock.create_user_mapping_rule = mock_none_response
        self.capture_fail_json_call(MockUserMappingRuleApi.get_error_responses('user1_error'), usermappingrules_module_mock)

    def test_create_usermappingrule_with_group_for_replace(self, usermappingrules_module_mock):
        self.usermappingrules_args.update({
            'rule': {
                'operator': 'replace',
                'options': {
                    'group': True
                },
                'user1': {
                    'domain': None,
                    'user': 'test_ans_users'
                },
                'user2': {
                    'domain': None,
                    'user': 'test_users'
                },
            },
            'state': 'present'
        })
        mock_none_response = MagicMock(return_value=None)
        usermappingrules_module_mock.module.params = self.usermappingrules_args
        usermappingrules_module_mock.form_rule_payload = mock_none_response
        usermappingrules_module_mock.create_user_mapping_rule = mock_none_response
        self.capture_fail_json_call(MockUserMappingRuleApi.get_error_responses('group_error'), usermappingrules_module_mock)

    def test_create_usermappingrule_with_user_for_trim(self, usermappingrules_module_mock):
        self.usermappingrules_args.update({
            'rule': {
                'operator': 'trim',
                'options': {
                    'user': True
                },
                'user1': {
                    'domain': None,
                    'user': 'test_ans_users'
                }
            },
            'state': 'present'
        })
        mock_none_response = MagicMock(return_value=None)
        usermappingrules_module_mock.module.params = self.usermappingrules_args
        usermappingrules_module_mock.form_rule_payload = mock_none_response
        usermappingrules_module_mock.create_user_mapping_rule = mock_none_response
        self.capture_fail_json_call(MockUserMappingRuleApi.get_error_responses('trim_user_error'), usermappingrules_module_mock)

    def test_create_usermappingrule_with_user2_for_trim(self, usermappingrules_module_mock):
        self.usermappingrules_args.update({
            'rule': {
                'operator': 'trim',
                'user1': {
                    'domain': None,
                    'user': 'test_ans_users'
                },
                'user2': {
                    'domain': None,
                    'user': 'test_ans_users'
                },
            },
            'state': 'present'
        })
        mock_none_response = MagicMock(return_value=None)
        usermappingrules_module_mock.module.params = self.usermappingrules_args
        usermappingrules_module_mock.form_rule_payload = mock_none_response
        usermappingrules_module_mock.create_user_mapping_rule = mock_none_response
        self.capture_fail_json_call(MockUserMappingRuleApi.get_error_responses('trim_user2_error'), usermappingrules_module_mock)

    def test_delete_usermappingrule_without_applyorder(self, usermappingrules_module_mock):
        usermappingrules_details = MockUserMappingRuleApi.GET_USERMAPPINGRULE_RESPONSE
        self.usermappingrules_args.update({
            'state': 'absent'
        })
        mock_none_response = MagicMock(return_value=None)
        usermappingrules_module_mock.module.params = self.usermappingrules_args
        usermappingrules_module_mock.auth_api.get_mapping_users_rules = MagicMock(return_value=MockSDKResponse(usermappingrules_details))
        usermappingrules_module_mock.auth_api.update_mapping_users_rules = mock_none_response
        self.capture_fail_json_call(MockUserMappingRuleApi.get_error_responses('delete_without_order'), usermappingrules_module_mock)

    def test_delete_usermappingrule_with_invalid_new_order(self, usermappingrules_module_mock):
        usermappingrules_details = MockUserMappingRuleApi.GET_USERMAPPINGRULE_RESPONSE
        self.usermappingrules_args.update({
            'apply_order': 1,
            'new_order': 6,
            'state': 'present'
        })
        usermappingrules_module_mock.module.params = self.usermappingrules_args
        usermappingrules_module_mock.auth_api.get_mapping_users_rules = MagicMock(return_value=MockSDKResponse(usermappingrules_details))
        self.capture_fail_json_call(MockUserMappingRuleApi.get_error_responses('new_order_error'), usermappingrules_module_mock)

    def test_order_change_with_wrong_order(self, usermappingrules_module_mock):
        self.usermappingrules_args.update({
            'apply_order': 1,
            'new_order': 0,
            'state': 'present'
        })
        usermappingrules_details = MockUserMappingRuleApi.GET_USERMAPPINGRULE_RESPONSE
        usermappingrules_module_mock.module.params = self.usermappingrules_args
        usermappingrules_module_mock.auth_api.get_mapping_users_rules = MagicMock(return_value=MockSDKResponse(usermappingrules_details))
        self.capture_fail_json_call(MockUserMappingRuleApi.get_error_responses('invalid_new_order'), usermappingrules_module_mock)

    def test_get_wrong_order(self, usermappingrules_module_mock):
        self.usermappingrules_args.update({
            'apply_order': 0,
            'state': 'present'
        })
        usermappingrules_details = MockUserMappingRuleApi.GET_USERMAPPINGRULE_RESPONSE
        usermappingrules_module_mock.module.params = self.usermappingrules_args
        usermappingrules_module_mock.auth_api.get_mapping_users_rules = MagicMock(return_value=MockSDKResponse(usermappingrules_details))
        self.capture_fail_json_call(MockUserMappingRuleApi.get_error_responses('invalid_apply_order'), usermappingrules_module_mock)

    def test_outbound_apply_order(self, usermappingrules_module_mock):
        self.usermappingrules_args.update({
            'apply_order': 5,
            'state': 'present'
        })
        usermappingrules_details = MockUserMappingRuleApi.GET_USERMAPPINGRULE_RESPONSE
        usermappingrules_module_mock.module.params = self.usermappingrules_args
        usermappingrules_module_mock.auth_api.get_mapping_users_rules = MagicMock(return_value=MockSDKResponse(usermappingrules_details))
        self.capture_fail_json_call(MockUserMappingRuleApi.get_error_responses('outbound_apply_order'), usermappingrules_module_mock)
