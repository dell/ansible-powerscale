# Copyright: (c) 2021, Dell Technologies

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
    import utils

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
        gatherfacts_module_mock.protocol_api = MagicMock()
        utils.ISI_SDK_VERSION_9 = MagicMock(return_value=True)
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
        self.get_module_args.update({})
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

    def test_get_nfs_aliases(self, gatherfacts_module_mock):
        nfs_aliases = MockGatherfactsApi.get_nfs_aliases_response('api')
        self.get_module_args.update({
            'zone': "System",
            'gather_subset': ['nfs_aliases']
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        gatherfacts_module_mock.protocol_api = MagicMock()
        gatherfacts_module_mock.protocol_api.list_nfs_aliases = MagicMock(return_value=MockSDKResponse(nfs_aliases))
        gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_nfs_aliases_response('module') == gatherfacts_module_mock.module.exit_json.call_args[1]['NfsAliases']

    def test_get_nfs_aliases_api_exception(self, gatherfacts_module_mock):
        self.get_module_args.update({
            'zone': "System",
            'gather_subset': ['nfs_aliases']
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        gatherfacts_module_mock.protocol_api = MagicMock()
        gatherfacts_module_mock.protocol_api.list_nfs_aliases = MagicMock(side_effect=MockApiException)
        gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_nfs_aliases_response('error') == gatherfacts_module_mock.module.fail_json.call_args[1]['msg']

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

    def test_get_node_pools(self, gatherfacts_module_mock):
        node_pools = MockGatherfactsApi.get_node_pool_response('api')
        self.get_module_args.update({
            'gather_subset': ['node_pools']
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        gatherfacts_module_mock.storagepool_api = MagicMock()
        gatherfacts_module_mock.storagepool_api.list_storagepool_nodepools = MagicMock(return_value=MockSDKResponse(node_pools))
        gatherfacts_module_mock.perform_module_operation()
        assert node_pools['nodepools'] == gatherfacts_module_mock.module.exit_json.call_args[1]['NodePools']

    def test_get_node_pools_api_exception(self, gatherfacts_module_mock):
        self.get_module_args.update({
            'gather_subset': ['node_pools']
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        gatherfacts_module_mock.storagepool_api = MagicMock()
        gatherfacts_module_mock.storagepool_api.list_storagepool_nodepools = MagicMock(side_effect=MockApiException)
        gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_node_pool_response('error') == gatherfacts_module_mock.module.fail_json.call_args[1]['msg']

    def test_get_storagepool_tiers(self, gatherfacts_module_mock):
        storage_tiers = MockGatherfactsApi.get_storage_tier_response('api')
        self.get_module_args.update({
            'gather_subset': ['storagepool_tiers']
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        gatherfacts_module_mock.storagepool_api = MagicMock()
        gatherfacts_module_mock.storagepool_api.list_storagepool_tiers = MagicMock(return_value=MockSDKResponse(storage_tiers))
        gatherfacts_module_mock.perform_module_operation()
        assert storage_tiers['tiers'] == gatherfacts_module_mock.module.exit_json.call_args[1]['StoragePoolTiers']

    def test_get_storage_tiers_api_exception(self, gatherfacts_module_mock):
        self.get_module_args.update({
            'gather_subset': ['storagepool_tiers']
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        gatherfacts_module_mock.storagepool_api = MagicMock()
        gatherfacts_module_mock.storagepool_api.list_storagepool_tiers = MagicMock(side_effect=MockApiException)
        gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_storage_tier_response('error') == gatherfacts_module_mock.module.fail_json.call_args[1]['msg']

    def test_get_smb_files(self, gatherfacts_module_mock):
        smb_files = MockGatherfactsApi.get_smb_files_response('api')
        self.get_module_args.update({
            'gather_subset': ['smb_files']
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        gatherfacts_module_mock.protocol_api = MagicMock()
        gatherfacts_module_mock.protocol_api.get_smb_openfiles = MagicMock(return_value=MockSDKResponse(smb_files))
        gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_smb_files_response('module') == gatherfacts_module_mock.module.exit_json.call_args[1]['SmbOpenFiles']

    def test_get_smb_files_api_exception(self, gatherfacts_module_mock):
        self.get_module_args.update({
            'gather_subset': ['smb_files']
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        gatherfacts_module_mock.protocol_api = MagicMock()
        gatherfacts_module_mock.protocol_api.get_smb_openfiles = MagicMock(side_effect=MockApiException)
        gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_smb_files_response('error') == gatherfacts_module_mock.module.fail_json.call_args[1]['msg']
