# Copyright: (c) 2021, DellEMC

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for gatherfacts module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_info_api \
    import MockGatherfactsApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import dellemc_ansible_powerscale_utils as utils

utils.get_logger = MagicMock()

from ansible_collections.dellemc.powerscale.plugins.modules.info import Info


class TestInfo():

    get_module_args = MockGatherfactsApi.GATHERFACTS_COMMON_ARGS

    @pytest.fixture
    def gatherfacts_module_mock(self, mocker):
        mocker.patch(MockGatherfactsApi.MODULE_PATH + '__init__', return_value=None)
        mocker.patch(MockGatherfactsApi.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        gatherfacts_module_mock = Info()
        gatherfacts_module_mock.module = MagicMock()
        gatherfacts_module_mock.network_api = MagicMock()
        return gatherfacts_module_mock

    def test_get_network_groupnets(self, gatherfacts_module_mock):
        network_groupnets = MockGatherfactsApi.get_network_groupnets_response('api')
        self.get_module_args.update({
            'gather_subset': ['network_groupnets']
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        gatherfacts_module_mock.network_api.list_network_groupnets = MagicMock(return_value=MockSDKResponse(network_groupnets))
        gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_network_groupnets_response('module') == gatherfacts_module_mock.module.exit_json.call_args[1]['NetworkGroupnets']

    def test_get_network_groupnets_api_exception(self, gatherfacts_module_mock):
        self.get_module_args.update({
            'gather_subset': ['network_groupnets']
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        gatherfacts_module_mock.network_api.list_network_groupnets = MagicMock(side_effect=MockApiException)
        gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_network_groupnets_response('error') == gatherfacts_module_mock.module.fail_json.call_args[1]['msg']

    def test_get_network_pools(self, gatherfacts_module_mock):
        network_pools = MockGatherfactsApi.get_network_pools_response('api')
        self.get_module_args.update({
            'gather_subset': ['network_pools']
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        gatherfacts_module_mock.network_api.get_network_pools = MagicMock(return_value=MockSDKResponse(network_pools))
        gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_network_pools_response('module') == gatherfacts_module_mock.module.exit_json.call_args[1]['NetworkPools']

    def test_get_network_pools_api_exception(self, gatherfacts_module_mock):
        self.get_module_args.update({
            'gather_subset': ['network_pools']
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        gatherfacts_module_mock.network_api.get_network_pools = MagicMock(side_effect=MockApiException)
        gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_network_pools_response('error') == gatherfacts_module_mock.module.fail_json.call_args[1]['msg']

    def test_get_network_rules(self, gatherfacts_module_mock):
        network_rules = MockGatherfactsApi.get_network_rules_response('api')
        self.get_module_args.update({
            'gather_subset': ['network_rules']
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        gatherfacts_module_mock.network_api.get_network_rules = MagicMock(return_value=MockSDKResponse(network_rules))
        gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_network_rules_response('module') == gatherfacts_module_mock.module.exit_json.call_args[1]['NetworkRules']

    def test_get_network_rules_api_exception(self, gatherfacts_module_mock):
        self.get_module_args.update({
            'gather_subset': ['network_rules']
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        gatherfacts_module_mock.network_api.get_network_rules = MagicMock(side_effect=MockApiException)
        gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_network_rules_response('error') == gatherfacts_module_mock.module.fail_json.call_args[1]['msg']

    def test_empty_gather_subset(self, gatherfacts_module_mock):
        self.get_module_args.update({
            'gather_subset': []
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.EMPTY_GATHERSUBSET_ERROR_MSG == gatherfacts_module_mock.module.fail_json.call_args[1]['msg']

    def test_input_none(self, gatherfacts_module_mock):
        gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.EMPTY_RESULT == gatherfacts_module_mock.module.exit_json.call_args[1]

    def test_get_network_interfaces(self, gatherfacts_module_mock):
        network_interfaces = MockGatherfactsApi.get_network_interfaces_response('api')
        self.get_module_args.update({
            'gather_subset': ['network_interfaces']
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        gatherfacts_module_mock.network_api = MagicMock()
        gatherfacts_module_mock.network_api.get_network_interfaces = MagicMock(return_value=MockSDKResponse(network_interfaces))
        gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_network_interfaces_response('module') == gatherfacts_module_mock.module.exit_json.call_args[1]['NetworkInterfaces']

    def test_get_network_interfaces_api_exception(self, gatherfacts_module_mock):
        self.get_module_args.update({
            'gather_subset': ['network_interfaces']
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        gatherfacts_module_mock.network_api = MagicMock()
        gatherfacts_module_mock.network_api.get_network_interfaces = MagicMock(side_effect=MockApiException)
        gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_network_interfaces_response('error') == gatherfacts_module_mock.module.fail_json.call_args[1]['msg']

    def test_get_network_subnets(self, gatherfacts_module_mock):
        network_subnets = MockGatherfactsApi.get_network_subnets_response('api')
        self.get_module_args.update({
            'gather_subset': ['network_subnets']
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        gatherfacts_module_mock.network_api = MagicMock()
        gatherfacts_module_mock.network_api.get_network_subnets = MagicMock(return_value=MockSDKResponse(network_subnets))
        gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_network_subnets_response('module') == gatherfacts_module_mock.module.exit_json.call_args[1]['NetworkSubnets']

    def test_get_network_subnets_api_exception(self, gatherfacts_module_mock):
        self.get_module_args.update({
            'gather_subset': ['network_subnets']
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        gatherfacts_module_mock.network_api = MagicMock()
        gatherfacts_module_mock.network_api.get_network_subnets = MagicMock(side_effect=MockApiException)
        gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_network_subnets_response('error') == gatherfacts_module_mock.module.fail_json.call_args[1]['msg']
