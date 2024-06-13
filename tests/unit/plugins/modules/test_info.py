# Copyright: (c) 2021-2024, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for gatherfacts module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from unittest.mock import patch
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_info_api \
    import MockGatherfactsApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils
from ansible_collections.dellemc.powerscale.plugins.modules.info import Info

utils.get_logger = MagicMock()


class TestInfo():

    get_module_args = MockGatherfactsApi.GATHERFACTS_COMMON_ARGS

    @pytest.fixture
    def gatherfacts_module_mock(self, mocker):
        mocker.patch(MockGatherfactsApi.MODULE_PATH +
                     '__init__', return_value=None)
        mocker.patch(MockGatherfactsApi.MODULE_UTILS_PATH +
                     '.ApiException', new=MockApiException)
        gatherfacts_module_mock = Info()
        gatherfacts_module_mock.module = MagicMock()
        gatherfacts_module_mock.network_api = MagicMock()
        gatherfacts_module_mock.protocol_api = MagicMock()
        gatherfacts_module_mock.auth_api = MagicMock()
        gatherfacts_module_mock.storagepool_api = MagicMock()
        gatherfacts_module_mock.cluster_api = MagicMock()
        gatherfacts_module_mock.zone_api = MagicMock()
        gatherfacts_module_mock.synciq_api = MagicMock()
        gatherfacts_module_mock.statistics_api = MagicMock()
        gatherfacts_module_mock.support_assist_api = MagicMock()
        utils.ISI_SDK_VERSION_9 = MagicMock(return_value=True)
        return gatherfacts_module_mock

    def test_empty_gather_subset(self, gatherfacts_module_mock):
        self.get_module_args.update({
            'gather_subset': []
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.EMPTY_GATHERSUBSET_ERROR_MSG == gatherfacts_module_mock.module.fail_json.call_args[
            1]['msg']

    def test_input_none(self, gatherfacts_module_mock):
        self.get_module_args.update({})
        gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.EMPTY_RESULT == gatherfacts_module_mock.module.exit_json.call_args[
            1]

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "clients", "return_key": "Clients"},
    ]
    )
    def test_get_facts_statistics_api_module(self, gatherfacts_module_mock, input_params):
        """Test the get_facts that uses the cluster api endpoint to get the module response"""
        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        with patch.object(gatherfacts_module_mock.statistics_api, MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == gatherfacts_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", [
        "clients",
    ]
    )
    def test_get_facts_statistics_api_exception(self, gatherfacts_module_mock, gather_subset):
        """Test the get_facts that uses the cluster api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        with patch.object(gatherfacts_module_mock.statistics_api, MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_error_response(
            gather_subset) == gatherfacts_module_mock.module.fail_json.call_args[1]['msg']

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "access_zones", "return_key": "AccessZones"},
    ]
    )
    def test_get_facts_zone_api_module(self, gatherfacts_module_mock, input_params):
        """Test the get_facts that uses the cluster api endpoint to get the module response"""
        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        with patch.object(gatherfacts_module_mock.zone_api, MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == gatherfacts_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", [
        "access_zones",
    ]
    )
    def test_get_facts_zone_api_exception(self, gatherfacts_module_mock, gather_subset):
        """Test the get_facts that uses the cluster api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        with patch.object(gatherfacts_module_mock.zone_api, MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_error_response(
            gather_subset) == gatherfacts_module_mock.module.fail_json.call_args[1]['msg']

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "synciq_reports", "return_key": "SynciqReports"},
        {"gather_subset": "synciq_target_reports", "return_key": "SynciqTargetReports"},
        {"gather_subset": "synciq_policies", "return_key": "SynciqPolicies"},
        {"gather_subset": "synciq_performance_rules", "return_key": "SynciqPerformanceRules"},
        {"gather_subset": "synciq_target_cluster_certificates", "return_key": "SynciqTargetClusterCertificate"},
    ]
    )
    def test_get_facts_synciq_api_module(self, gatherfacts_module_mock, input_params):
        """Test the get_facts that uses the cluster api endpoint to get the module response"""
        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        with patch.object(gatherfacts_module_mock.synciq_api, MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == gatherfacts_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", [
        "synciq_reports",
        "synciq_target_reports",
        "synciq_policies",
        "synciq_performance_rules",
        "synciq_target_cluster_certificates"
    ]
    )
    def test_get_facts_synciq_api_exception(self, gatherfacts_module_mock, gather_subset):
        """Test the get_facts that uses the cluster api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        with patch.object(gatherfacts_module_mock.synciq_api, MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_error_response(
            gather_subset) == gatherfacts_module_mock.module.fail_json.call_args[1]['msg']

    def test_get_facts_attributes_module(self, gatherfacts_module_mock):
        """Test the get_facts of attributes response"""
        gather_subset = "attributes"
        return_key = "Attributes"
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        # Mocking
        cluster_config, external_ips, logon_msg, contact_info, cluster_version = MockGatherfactsApi.get_attributes_response("module")
        gatherfacts_module_mock.module.params = self.get_module_args
        gatherfacts_module_mock.cluster_api.get_cluster_config = MagicMock(return_value=MockSDKResponse(cluster_config))
        gatherfacts_module_mock.cluster_api.get_cluster_external_ips = MagicMock(return_value=external_ips)
        gatherfacts_module_mock.cluster_api.get_cluster_identity = MagicMock(return_value=MockSDKResponse(logon_msg))
        gatherfacts_module_mock.cluster_api.get_cluster_owner = MagicMock(return_value=MockSDKResponse(contact_info))
        gatherfacts_module_mock.cluster_api.get_cluster_version = MagicMock(return_value=MockSDKResponse(cluster_version))
        gatherfacts_module_mock.perform_module_operation()
        return_resp = MockGatherfactsApi.get_attributes_response("api")
        assert return_resp == gatherfacts_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "nodes", "return_key": "Nodes"},
    ]
    )
    def test_get_facts_cluster_api_module(self, gatherfacts_module_mock, input_params):
        """Test the get_facts that uses the cluster api endpoint to get the module response"""
        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        with patch.object(gatherfacts_module_mock.cluster_api, MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == gatherfacts_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", [
        "attributes",
        "nodes"
    ]
    )
    def test_get_facts_cluster_api_exception(self, gatherfacts_module_mock, gather_subset):
        """Test the get_facts that uses the cluster api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        with patch.object(gatherfacts_module_mock.cluster_api, MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_error_response(
            gather_subset) == gatherfacts_module_mock.module.fail_json.call_args[1]['msg']

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "network_subnets",
            "return_key": "NetworkSubnets"},
        {"gather_subset": "network_interfaces",
            "return_key": "NetworkInterfaces"},
        {"gather_subset": "network_rules",
            "return_key": "NetworkRules"},
        {"gather_subset": "network_groupnets",
            "return_key": "NetworkGroupnets"},
        {"gather_subset": "network_pools",
            "return_key": "NetworkPools"},
    ]
    )
    def test_get_facts_network_api_module(self, gatherfacts_module_mock, input_params):
        """Test the get_facts that uses the network api endpoint to get the module response"""
        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        with patch.object(gatherfacts_module_mock.network_api, MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == gatherfacts_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", [
        "network_subnets",
        "network_interfaces",
        "network_rules",
        "network_pools",
        "network_groupnets"
    ]
    )
    def test_get_facts_network_api_exception(self, gatherfacts_module_mock, gather_subset):
        """Test the get_facts that uses the network api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        with patch.object(gatherfacts_module_mock.network_api, MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_error_response(
            gather_subset) == gatherfacts_module_mock.module.fail_json.call_args[1]['msg']

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "storagepool_tiers",
            "return_key": "StoragePoolTiers"},
        {"gather_subset": "node_pools",
            "return_key": "NodePools"},
    ]
    )
    def test_get_facts_stooragepool_api_module(self, gatherfacts_module_mock, input_params):
        """Test the get_facts that uses the storageapi api endpoint to get the module response"""
        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        with patch.object(gatherfacts_module_mock.storagepool_api, MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == gatherfacts_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", ["storagepool_tiers", "node_pools"])
    def test_get_facts_storagepool_api_exception(self, gatherfacts_module_mock, gather_subset):
        """Test the get_facts that uses the storageapi api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        with patch.object(gatherfacts_module_mock.storagepool_api, MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_error_response(
            gather_subset) == gatherfacts_module_mock.module.fail_json.call_args[1]['msg']

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "ldap", "return_key": "LdapProviders"},
        {"gather_subset": "user_mapping_rules", "return_key": "UserMappingRules"},
        {"gather_subset": "providers", "return_key": "Providers"},
        {"gather_subset": "users", "return_key": "Users"},
        {"gather_subset": "groups", "return_key": "Groups"},
    ]
    )
    def test_get_facts_auth_api_module(self, gatherfacts_module_mock, input_params):
        """Test the get_facts that uses the auth api endpoint to get the module response"""

        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        with patch.object(gatherfacts_module_mock.auth_api, MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == gatherfacts_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", ["ldap", "user_mapping_rules", "providers", "users", "groups"])
    def test_get_facts_auth_api_exception(self, gatherfacts_module_mock, gather_subset):
        """Test the get_facts that uses the auth api endpoint to get the exception"""

        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        with patch.object(gatherfacts_module_mock.auth_api, MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_error_response(
            gather_subset) == gatherfacts_module_mock.module.fail_json.call_args[1]['msg']

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "smb_files", "return_key": "SmbOpenFiles"},
        {"gather_subset": "nfs_aliases", "return_key": "NfsAliases"},
        {"gather_subset": "smb_global_settings", "return_key": "SmbGlobalSettings"},
        {"gather_subset": "nfs_global_settings", "return_key": "NfsGlobalSettings"},
        {"gather_subset": "nfs_zone_settings", "return_key": "NfsZoneSettings"},
        {"gather_subset": "smb_shares", "return_key": "SmbShares"},
        {"gather_subset": "nfs_exports", "return_key": "NfsExports"},
        {"gather_subset": "nfs_default_settings", "return_key": "NfsDefaultSettings"},
        {"gather_subset": "s3_buckets", "return_key": "s3Buckets"},
        {"gather_subset": "snmp_settings", "return_key": "SnmpSettings"}
    ]
    )
    def test_get_facts_protocols_api_module(self, gatherfacts_module_mock, input_params):
        """Test the get_facts that uses the protocols api endpoint to get the module response"""

        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': [gather_subset],
            'zone': "System",
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        with patch.object(gatherfacts_module_mock.protocol_api, MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == gatherfacts_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", [
        "nfs_global_settings",
        "smb_global_settings",
        "nfs_zone_settings",
        "smb_files",
        "nfs_aliases",
        "smb_shares",
        "nfs_exports",
        "nfs_default_settings",
        "s3_buckets",
        "snmp_settings"
        ])
    def test_get_facts_protocols_api_exception(self, gatherfacts_module_mock, gather_subset):
        """Test the get_facts that uses the protocols api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset],
            'zone': "System",
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        with patch.object(gatherfacts_module_mock.protocol_api, MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_error_response(
            gather_subset) == gatherfacts_module_mock.module.fail_json.call_args[1]['msg']

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "support_assist_settings", "return_key": "SupportAssistSettings"}
    ]
    )
    def test_get_facts_support_assist_api_module(self, gatherfacts_module_mock, input_params):
        """Test the get_facts that uses the support assist api endpoint to get the module response"""

        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': ['support_assist_settings'],
            'zone': "System",
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        with patch.object(gatherfacts_module_mock.support_assist_api, MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == gatherfacts_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", [
        "support_assist_settings"
        ])
    def test_get_facts_support_assist_api_exception(self, gatherfacts_module_mock, gather_subset):
        """Test the get_facts that uses the support assist api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset],
            'zone': "System",
        })
        gatherfacts_module_mock.module.params = self.get_module_args
        with patch.object(gatherfacts_module_mock.support_assist_api, MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            gatherfacts_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_error_response(
            gather_subset) == gatherfacts_module_mock.module.fail_json.call_args[1]['msg']
