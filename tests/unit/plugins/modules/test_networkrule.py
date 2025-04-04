# Copyright: (c) 2021-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Network Rule module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils


from ansible_collections.dellemc.powerscale.plugins.modules.networkrule import NetworkRule
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_networkrule_api as MockNetworkRuleApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase


class TestNetworkRule(PowerScaleUnitBase):
    get_network_rule_args = {
        'groupnet_name': 'groupnet0',
        'subnet_name': 'subnet1',
        'pool_name': 'pool1',
        'rule_name': 'rule1',
        'new_rule_name': None,
        'description': None,
        'iface': None,
        'node_type': None,
        'state': 'present'
    }

    @pytest.fixture
    def module_object(self):
        return NetworkRule

    def test_get_network_rules(self, powerscale_module_mock):
        network_rule = MockNetworkRuleApi.NETWORK_RULES['rules'][0]
        powerscale_module_mock.module.params = self.get_network_rule_args
        powerscale_module_mock.network_api_instance.get_pools_pool_rule = MagicMock(
            return_value=MockSDKResponse(MockNetworkRuleApi.NETWORK_RULES))
        powerscale_module_mock.perform_module_operation()

        assert network_rule == powerscale_module_mock.module.exit_json.call_args[1]['network_rule_details']
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_create_network_rule(self, powerscale_module_mock):
        self.get_network_rule_args.update({
            'rule_name': 'new_rule',
            'description': 'create rule',
            'iface': 'ext-1'
        })
        powerscale_module_mock.module.params = self.get_network_rule_args
        powerscale_module_mock.get_network_rule = MagicMock(return_value=[])
        powerscale_module_mock.perform_module_operation()

        assert (powerscale_module_mock.module.exit_json.call_args[1]['create_network_rule'])
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_network_rule(self, powerscale_module_mock):
        self.get_network_rule_args.update({
            'description': 'modify rule',
            'iface': 'ext-4',
        })
        powerscale_module_mock.module.params = self.get_network_rule_args
        powerscale_module_mock.network_api_instance.get_pools_pool_rule = MagicMock(
            return_value=MockSDKResponse(MockNetworkRuleApi.NETWORK_RULES))
        powerscale_module_mock.perform_module_operation()

        assert (powerscale_module_mock.module.exit_json.call_args[1]['modify_network_rule'])
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_network_rule(self, powerscale_module_mock):
        self.get_network_rule_args.update({
            'state': 'absent'
        })
        powerscale_module_mock.module.params = self.get_network_rule_args
        powerscale_module_mock.network_api_instance.get_pools_pool_rule = MagicMock(
            return_value=MockSDKResponse(MockNetworkRuleApi.NETWORK_RULES))
        powerscale_module_mock.perform_module_operation()

        assert (powerscale_module_mock.module.exit_json.call_args[1]['delete_network_rule'])
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_rename_network_rule(self, powerscale_module_mock):
        self.get_network_rule_args.update({
            'new_rule_name': 'Renamed_rule',
        })
        powerscale_module_mock.module.params = self.get_network_rule_args
        powerscale_module_mock.network_api_instance.get_pools_pool_rule = MagicMock(
            return_value=MockSDKResponse(MockNetworkRuleApi.NETWORK_RULES))
        powerscale_module_mock.perform_module_operation()

        assert (powerscale_module_mock.module.exit_json.call_args[1]['modify_network_rule'])
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_rule_with_invalid_iface(self, powerscale_module_mock):
        self.get_network_rule_args.update({
            'iface': 'invalid',
        })
        powerscale_module_mock.module.params = self.get_network_rule_args
        powerscale_module_mock.get_network_rule = MagicMock(return_value=[])
        powerscale_module_mock.network_api_instance.create_pools_pool_rule = \
            MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNetworkRuleApi.create_rule_failed_msg(self.get_network_rule_args['rule_name']),
                                    invoke_perform_module=True)

    def test_get_network_rule_with_404_exception(self, powerscale_module_mock):
        rule_name = 'test_rule'
        self.set_module_params(self.get_network_rule_args, {
            'rule_name': rule_name,
            'iface': 'ext-4',
        })
        powerscale_module_mock.network_api_instance.get_pools_pool_rule = \
            MagicMock(side_effect=MockApiException(404))
        powerscale_module_mock.perform_module_operation()
        assert (powerscale_module_mock.module.exit_json.call_args[1]['create_network_rule'])
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_network_rule_throws_exception(self, powerscale_module_mock):
        rule_name = 'test_rule'
        self.get_network_rule_args.update({
            'rule_name': rule_name,
            'state': 'absent'
        })
        powerscale_module_mock.module.params = self.get_network_rule_args
        powerscale_module_mock.network_api_instance.get_pools_pool_rule = MagicMock(
            return_value=MockSDKResponse(MockNetworkRuleApi.NETWORK_RULES))
        powerscale_module_mock.network_api_instance.delete_pools_pool_rule = \
            MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNetworkRuleApi.delete_rule_failed_msg(rule_name), invoke_perform_module=True)

    def test_modify_network_rule_throws_exception(self, powerscale_module_mock):
        rule_name = 'test_rule'
        self.get_network_rule_args.update({
            'rule_name': rule_name,
            'node_type': 'Invalid_node_type',
        })
        powerscale_module_mock.module.params = self.get_network_rule_args
        powerscale_module_mock.network_api_instance.get_pools_pool_rule = MagicMock(
            return_value=MockSDKResponse(MockNetworkRuleApi.NETWORK_RULES))
        powerscale_module_mock.network_api_instance.update_pools_pool_rule = \
            MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNetworkRuleApi.modify_rule_failed_msg(rule_name), invoke_perform_module=True)
