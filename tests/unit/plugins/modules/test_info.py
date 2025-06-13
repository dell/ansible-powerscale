# Copyright: (c) 2021-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase

utils.get_logger = MagicMock()


class TestInfo(PowerScaleUnitBase):

    get_module_args = MockGatherfactsApi.GATHERFACTS_COMMON_ARGS

    @pytest.fixture
    def module_object(self, mocker):
        utils.ISI_SDK_VERSION_9 = MagicMock(return_value=True)
        return Info

    @pytest.fixture(autouse=True)
    def inject_attributes(self, powerscale_module_mock):
        powerscale_module_mock.api_client = MagicMock()
        powerscale_module_mock.synciq_api = MagicMock()
        powerscale_module_mock.support_assist_api = MagicMock()
        return powerscale_module_mock

    def test_empty_gather_subset(self, powerscale_module_mock):
        self.get_module_args.update({
            'gather_subset': []
        })
        powerscale_module_mock.module.params = self.get_module_args
        self.capture_fail_json_call(MockGatherfactsApi.EMPTY_GATHERSUBSET_ERROR_MSG, invoke_perform_module=True)

    def test_input_none(self, powerscale_module_mock):
        self.get_module_args.update({})
        powerscale_module_mock.perform_module_operation()
        assert MockGatherfactsApi.EMPTY_RESULT == powerscale_module_mock.module.exit_json.call_args[
            1]

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "clients", "return_key": "Clients"},
    ]
    )
    def test_get_facts_statistics_api_module(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the cluster api endpoint to get the module response"""
        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.statistics_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            powerscale_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", [
        "clients",
    ]
    )
    def test_get_facts_statistics_api_exception(self, powerscale_module_mock, gather_subset):
        """Test the get_facts that uses the cluster api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.statistics_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            self.capture_fail_json_call(MockGatherfactsApi.get_gather_facts_error_response(
                gather_subset), invoke_perform_module=True)

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "access_zones", "return_key": "AccessZones"},
    ]
    )
    def test_get_facts_zone_api_module(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the cluster api endpoint to get the module response"""
        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.zone_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            powerscale_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", [
        "access_zones",
    ]
    )
    def test_get_facts_zone_api_exception(self, powerscale_module_mock, gather_subset):
        """Test the get_facts that uses the cluster api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.zone_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            self.capture_fail_json_call(MockGatherfactsApi.get_gather_facts_error_response(
                gather_subset), invoke_perform_module=True)

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "synciq_reports", "return_key": "SynciqReports"},
        {"gather_subset": "synciq_target_reports", "return_key": "SynciqTargetReports"},
        {"gather_subset": "synciq_policies", "return_key": "SynciqPolicies"},
        {"gather_subset": "synciq_performance_rules", "return_key": "SynciqPerformanceRules"},
        {"gather_subset": "synciq_target_cluster_certificates", "return_key": "SynciqTargetClusterCertificate"},
    ]
    )
    def test_get_facts_synciq_api_module(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the cluster api endpoint to get the module response"""
        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.synciq_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            powerscale_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", [
        "synciq_reports",
        "synciq_target_reports",
        "synciq_policies",
        "synciq_performance_rules",
        "synciq_target_cluster_certificates"
    ]
    )
    def test_get_facts_synciq_api_exception(self, powerscale_module_mock, gather_subset):
        """Test the get_facts that uses the cluster api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.synciq_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            self.capture_fail_json_call(MockGatherfactsApi.get_gather_facts_error_response(
                gather_subset), invoke_perform_module=True)

    def test_get_facts_attributes_module(self, powerscale_module_mock):
        """Test the get_facts of attributes response"""
        gather_subset = "attributes"
        return_key = "Attributes"
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        # Mocking
        cluster_config, external_ips, logon_msg, contact_info, cluster_version = MockGatherfactsApi.get_attributes_response("module")
        powerscale_module_mock.module.params = self.get_module_args
        powerscale_module_mock.cluster_api.get_cluster_config = MagicMock(return_value=MockSDKResponse(cluster_config))
        powerscale_module_mock.cluster_api.get_cluster_external_ips = MagicMock(return_value=external_ips)
        powerscale_module_mock.cluster_api.get_cluster_identity = MagicMock(return_value=MockSDKResponse(logon_msg))
        powerscale_module_mock.cluster_api.get_cluster_owner = MagicMock(return_value=MockSDKResponse(contact_info))
        powerscale_module_mock.cluster_api.get_cluster_version = MagicMock(
            return_value=MockSDKResponse(cluster_version))
        powerscale_module_mock.perform_module_operation()
        return_resp = MockGatherfactsApi.get_attributes_response("api")
        assert return_resp == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "nodes", "return_key": "Nodes"},
    ]
    )
    def test_get_facts_cluster_api_module(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the cluster api endpoint to get the module response"""
        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.cluster_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            powerscale_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", [
        "attributes",
        "nodes"
    ]
    )
    def test_get_facts_cluster_api_exception(self, powerscale_module_mock, gather_subset):
        """Test the get_facts that uses the cluster api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.cluster_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            self.capture_fail_json_call(MockGatherfactsApi.get_gather_facts_error_response(
                gather_subset), invoke_perform_module=True)

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
    def test_get_facts_network_api_module(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the network api endpoint to get the module response"""
        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.network_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            powerscale_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", [
        "network_subnets",
        "network_interfaces",
        "network_rules",
        "network_pools",
        "network_groupnets"
    ]
    )
    def test_get_facts_network_api_exception(self, powerscale_module_mock, gather_subset):
        """Test the get_facts that uses the network api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.network_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            self.capture_fail_json_call(MockGatherfactsApi.get_gather_facts_error_response(
                gather_subset), invoke_perform_module=True)

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "storagepool_tiers",
            "return_key": "StoragePoolTiers"},
        {"gather_subset": "node_pools",
            "return_key": "NodePools"},
    ]
    )
    def test_get_facts_stooragepool_api_module(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the storageapi api endpoint to get the module response"""
        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.storagepool_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            powerscale_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", ["storagepool_tiers", "node_pools"])
    def test_get_facts_storagepool_api_exception(self, powerscale_module_mock, gather_subset):
        """Test the get_facts that uses the storageapi api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.storagepool_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            self.capture_fail_json_call(MockGatherfactsApi.get_gather_facts_error_response(
                gather_subset), invoke_perform_module=True)

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "user_mapping_rules", "return_key": "UserMappingRules"},
        {"gather_subset": "providers", "return_key": "Providers"},
        {"gather_subset": "groups", "return_key": "Groups"},
        {"gather_subset": "roles", "return_key": "roles"},
    ]
    )
    def test_get_facts_auth_api_module(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the auth api endpoint to get the module response"""

        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.auth_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            powerscale_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", ["ldap", "user_mapping_rules", "providers", "users", "groups", "roles"])
    def test_get_facts_auth_api_exception(self, powerscale_module_mock, gather_subset):
        """Test the get_facts that uses the auth api endpoint to get the exception"""

        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.auth_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            self.capture_fail_json_call(MockGatherfactsApi.get_gather_facts_error_response(
                gather_subset), invoke_perform_module=True)

    @pytest.mark.parametrize("input_params", [
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
    def test_get_facts_protocols_api_module(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the protocols api endpoint to get the module response"""

        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': [gather_subset],
            'zone': "System"
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.protocol_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            powerscale_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    def test_get_facts_nfs_exports_api_module(self, powerscale_module_mock):
        """Test the get_facts that uses the protocols api endpoint to get the module response"""

        gather_subset = "nfs_exports"
        return_key = "NfsExports"
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': [gather_subset],
            'zone': "System",
            'filters': [{"filter_key": "id", "filter_operator": "equal", "filter_value": "1"}]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.protocol_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            powerscale_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset, "module_filter") == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "smb_files", "return_key": "SmbOpenFiles"},
        {"gather_subset": "smb_files", "return_key": "SmbOpenFiles", "filters":
            [{"filter_key": "id", "filter_operator": "equal", "filter_value": 1880}]}
    ]
    )
    def test_get_facts_smb_files_module(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the protocols api endpoint to get the module response"""
        return_key = input_params.get('return_key')
        gather_subset = input_params.get('gather_subset')
        self.get_module_args.update({
            'gather_subset': [gather_subset],
            'zone': "System",
            "filters": input_params.get('filters')
        })
        powerscale_module_mock.cluster_ip = "xx.xx.xx.xx"
        powerscale_module_mock.cluster_api.get_cluster_external_ips = MagicMock(
            return_value=[powerscale_module_mock.cluster_ip])
        powerscale_module_mock.module.params = self.get_module_args
        powerscale_module_mock.api_client = utils.get_powerscale_connection(self.get_module_args)
        powerscale_module_mock.isi_sdk.ProtocolsApi = MagicMock(return_value=powerscale_module_mock.protocol_api)
        powerscale_module_mock.protocol_api.get_smb_openfiles = MagicMock(
            return_value=MockSDKResponse(MockGatherfactsApi.get_gather_facts_api_response(
                gather_subset)))
        powerscale_module_mock.perform_module_operation()
        module_output = MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset)
        for file in module_output:
            file['node'] = powerscale_module_mock.cluster_ip
        assert module_output == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    def test_get_facts_smb_files_module_with_resume(self, powerscale_module_mock, mocker):
        """Test the get_facts that uses the protocols api endpoint to get the module response"""
        gather_subset = "smb_files"
        return_key = "SmbOpenFiles"
        self.get_module_args.update({
            'gather_subset': [gather_subset],
            'zone': "System"
        })
        powerscale_module_mock.cluster_ip = "xx.xx.xx.xx"
        powerscale_module_mock.cluster_api.get_cluster_external_ips = MagicMock(
            return_value=[powerscale_module_mock.cluster_ip])
        powerscale_module_mock.module.params = self.get_module_args
        powerscale_module_mock.api_client = utils.get_powerscale_connection(self.get_module_args)
        powerscale_module_mock.isi_sdk.ProtocolsApi = MagicMock(return_value=powerscale_module_mock.protocol_api)

        def mock_get_smb_files_with_resume(*args, **kwargs):
            if kwargs.get('resume', None) == "abcd":
                return MockSDKResponse(MockGatherfactsApi.get_gather_facts_api_response(
                    "smb_files_with_resume2"))
            return MockSDKResponse(MockGatherfactsApi.get_gather_facts_api_response(
                "smb_files_with_resume"))

        with patch.object(powerscale_module_mock.protocol_api, "get_smb_openfiles") as mock_method:
            mock_method.side_effect = MagicMock(side_effect=mock_get_smb_files_with_resume)
            powerscale_module_mock.perform_module_operation()
        module_output = MockGatherfactsApi.get_gather_facts_module_response(
            "smb_files_with_resume")
        for file in module_output:
            file['node'] = powerscale_module_mock.cluster_ip
        assert module_output == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", [
        "nfs_global_settings",
        "smb_global_settings",
        "nfs_zone_settings",
        "nfs_aliases",
        "smb_shares",
        "nfs_exports",
        "nfs_default_settings",
        "s3_buckets",
        "snmp_settings"
    ]
    )
    def test_get_facts_protocols_api_exception(self, powerscale_module_mock, gather_subset):
        """Test the get_facts that uses the protocols api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset],
            'zone': "System",
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.protocol_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            self.capture_fail_json_call(MockGatherfactsApi.get_gather_facts_error_response(
                gather_subset), invoke_perform_module=True)

    def test_get_facts_smb_files_cluster_ip_exception(self, powerscale_module_mock):
        """Test the get_facts that uses the protocols api endpoint to get the exception"""
        gather_subset = "smb_files"
        self.get_module_args.update({
            'gather_subset': [gather_subset],
            'zone': "System",
        })
        powerscale_module_mock.module.params = self.get_module_args
        powerscale_module_mock.cluster_api.get_cluster_external_ips = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockGatherfactsApi.get_gather_facts_error_response(gather_subset, "cluster_ip_exception"),
            invoke_perform_module=True)

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "smb_files", "return_key": "SmbOpenFiles"},
    ]
    )
    def test_get_facts_smb_files_unreachable_ips(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the protocols api endpoint to smb open files with unreachable ips"""
        return_key = input_params.get('return_key')
        gather_subset = input_params.get('gather_subset')
        self.get_module_args.update({
            'gather_subset': [gather_subset],
            'zone': "System",
        })
        powerscale_module_mock.cluster_ip = "xx.xx.xx.xx"
        powerscale_module_mock.cluster_api.get_cluster_external_ips = MagicMock(
            return_value=[powerscale_module_mock.cluster_ip])
        powerscale_module_mock.module.params = self.get_module_args
        powerscale_module_mock.api_client.to_dict.onefs_host = MagicMock(return_value=powerscale_module_mock.cluster_ip)
        powerscale_module_mock.isi_sdk.ProtocolsApi = MagicMock(return_value=powerscale_module_mock.protocol_api)
        powerscale_module_mock.protocol_api.get_smb_openfiles = MagicMock(
            side_effect=MockApiException)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.module.warn.assert_called_once()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset, "ip_unreachable") == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "support_assist_settings", "return_key": "support_assist_settings"}
    ]
    )
    def test_get_facts_support_assist_api_module(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the support assist api endpoint to get the module response"""

        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': ['support_assist_settings'],
            'zone': "System",
        })
        powerscale_module_mock.module.params = self.get_module_args
        powerscale_module_mock.major = 9
        powerscale_module_mock.minor = 5
        with patch.object(powerscale_module_mock.support_assist_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            powerscale_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", [
        "support_assist_settings"
    ]
    )
    def test_get_facts_support_assist_api_exception(self, powerscale_module_mock, gather_subset):
        """Test the get_facts that uses the support assist api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset],
            'zone': "System",
        })
        powerscale_module_mock.module.params = self.get_module_args
        powerscale_module_mock.major = 9
        powerscale_module_mock.minor = 5
        with patch.object(powerscale_module_mock.support_assist_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            self.capture_fail_json_call(MockGatherfactsApi.get_gather_facts_error_response(
                gather_subset), invoke_perform_module=True)

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "alert_settings", "return_key": "alert_settings"}
    ]
    )
    def test_get_facts_alert_settings_api_module(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the alert settings api endpoint to get the module response"""

        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': ['alert_settings']
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.event_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            powerscale_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "alert_settings", "return_key": "alert_settings"}
    ]
    )
    def test_get_facts_alert_settings_api_911_module(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the alert settings api endpoint to get the module response"""

        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': ['alert_settings']
        })
        powerscale_module_mock.major = 9
        powerscale_module_mock.minor = 11
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.cluster_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            powerscale_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", ["alert_settings"])
    def test_get_facts_alert_settings_api_exception(self, powerscale_module_mock, gather_subset):
        """Test the get_facts that uses the alert settings api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.event_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            self.capture_fail_json_call(MockGatherfactsApi.get_gather_facts_error_response(
                gather_subset), invoke_perform_module=True)

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "alert_categories", "return_key": "alert_categories"}])
    def test_get_facts_alert_categories_api_module(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the alert categories api endpoint to get the module response"""

        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': ['alert_categories'],
            'query_parameters': {'alert_categories': [{'limit': '4'}]}
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.event_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            powerscale_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == powerscale_module_mock.module.exit_json.call_args[1][return_key][0]

    @pytest.mark.parametrize("gather_subset", ["alert_categories"])
    def test_get_facts_alert_categories_api_exception(self, powerscale_module_mock, gather_subset):
        """Test the get_facts that uses the alert categories api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.event_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            self.capture_fail_json_call(MockGatherfactsApi.get_gather_facts_error_response(
                gather_subset), invoke_perform_module=True)

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "alert_channels", "return_key": "alert_channels"}])
    def test_get_facts_alert_channels_api_module(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the alert channels api endpoint to get the module response"""

        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': ['alert_channels'],
            'query_parameters': {'alert_channels': [{'sort': 'name'}, {'sort_dir': 'desc'}]}
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.event_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            powerscale_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == powerscale_module_mock.module.exit_json.call_args[1][return_key][0]

    @pytest.mark.parametrize("gather_subset", ["alert_channels"])
    def test_get_facts_alert_channels_api_exception(self, powerscale_module_mock, gather_subset):
        """Test the get_facts that uses the alert channels api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.event_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            self.capture_fail_json_call(MockGatherfactsApi.get_gather_facts_error_response(
                gather_subset), invoke_perform_module=True)

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "alert_rules", "return_key": "alert_rules"}])
    def test_get_facts_alert_rules_api_module(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the alert rules api endpoint to get the module response"""

        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': ['alert_rules'],
            'query_parameters': {'alert_rules': [
                {'sort_dir': 'asc'}, {'sort': 'name'}, {'channel': 'condition'}]}
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.event_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            powerscale_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == powerscale_module_mock.module.exit_json.call_args[1][return_key][0]

    @pytest.mark.parametrize("gather_subset", ["alert_rules"])
    def test_get_facts_alert_rules_api_exception(self, powerscale_module_mock, gather_subset):
        """Test the get_facts that uses the alert rules api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.event_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            self.capture_fail_json_call(MockGatherfactsApi.get_gather_facts_error_response(
                gather_subset), invoke_perform_module=True)

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "event_group", "return_key": "event_groups"}])
    def test_get_facts_event_groups_api_module(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the event groups api endpoint to get the module response"""

        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': ['event_group'],
            'query_parameters': {'event_group': [{'alert_info': 'true'},
                                                 {'category': '400000000'}]}
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.event_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            powerscale_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == powerscale_module_mock.module.exit_json.call_args[1][return_key][0]

    @pytest.mark.parametrize("gather_subset", ["event_group"])
    def test_get_facts_event_groups_api_exception(self, powerscale_module_mock, gather_subset):
        """Test the get_facts that uses the event group api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.event_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            self.capture_fail_json_call(MockGatherfactsApi.get_gather_facts_error_response(
                gather_subset), invoke_perform_module=True)

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "smartquota", "return_key": "smart_quota"},
        {"gather_subset": "smartquota", "return_key": "smart_quota", "filters":
            [{"filter_key": "id", "filter_operator": "equal", "filter_value": "xxxx"}]}
    ]
    )
    def test_get_facts_smartquota_api_module(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the smartquota api endpoint to get the module response"""

        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': [gather_subset],
            'zone': "System",
            'filters': input_params.get('filters')
        })
        powerscale_module_mock.module.params = self.get_module_args

        with patch.object(powerscale_module_mock.smartquota_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            powerscale_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset)['quotas'] == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    def test_get_facts_smartquota_with_resume(self, powerscale_module_mock, mocker):
        """Test the get_facts that uses the protocols api endpoint to get the module response"""
        gather_subset = "smartquota"
        return_key = "smart_quota"
        self.get_module_args.update({
            'gather_subset': [gather_subset],
            'zone': "System"
        })
        powerscale_module_mock.module.params = self.get_module_args

        def mock_get_smartquota_with_resume(*args, **kwargs):
            if kwargs.get('resume', None) == "abcd":
                return MockSDKResponse(MockGatherfactsApi.get_gather_facts_api_response(
                    "smartquota"))
            return MockSDKResponse(MockGatherfactsApi.get_gather_facts_api_response(
                "smartquota_with_resume"))

        with patch.object(powerscale_module_mock.smartquota_api, "list_quota_quotas") as mock_method:
            mock_method.side_effect = MagicMock(side_effect=mock_get_smartquota_with_resume)
            powerscale_module_mock.perform_module_operation()
        module_output = MockGatherfactsApi.get_gather_facts_module_response(
            "smartquota_with_resume")
        assert module_output == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", [
        "smartquota"
    ]
    )
    def test_get_facts_smartquota_api_exception(self, powerscale_module_mock, gather_subset):
        """Test the get_facts that uses the smartquota api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset],
            'zone': "System",
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.smartquota_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            self.capture_fail_json_call(MockGatherfactsApi.get_gather_facts_error_response(
                gather_subset), invoke_perform_module=True)

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "filesystem", "return_key": "file_system"},
        {"gather_subset": "filesystem", "return_key": "file_system", "filters":
            [{"filter_key": "name", "filter_operator": "equal", "filter_value": "home"}]},
        {"gather_subset": "filesystem", "return_key": "file_system",
            'query_parameters': {'filesystem': {'path': "/ifs/home"}}}
    ]
    )
    def test_get_facts_filesystem_api_module(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the filesystem api endpoint to get the module response"""

        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': ['filesystem'],
            'zone': "System",
            'filters': input_params.get('filters'),
            'query_parameters': input_params.get('query_parameters')
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.namespace_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            powerscale_module_mock.perform_module_operation()
        if input_params.get('filters'):
            module_output = MockGatherfactsApi.get_gather_facts_module_response(
                gather_subset, "module_filter")
        else:
            module_output = MockGatherfactsApi.get_gather_facts_module_response(
                gather_subset)
        assert module_output == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", [
        "filesystem"
    ]
    )
    def test_get_facts_filesystem_api_exception(self, powerscale_module_mock, gather_subset):
        """Test the get_facts that uses the filesystem api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': [gather_subset],
            'zone': "System",
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.namespace_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            self.capture_fail_json_call(MockGatherfactsApi.get_gather_facts_error_response(
                gather_subset), invoke_perform_module=True)

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "filesystem", "return_key": "file_system"}
    ]
    )
    def test_get_facts_filesystem_empty_list(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the filesystem api endpoint to get the exception"""
        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        self.set_module_params(self.get_module_args, {
            'gather_subset': [gather_subset],
            'zone': "System",
        })
        with patch.object(powerscale_module_mock.namespace_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse([])
            powerscale_module_mock.perform_module_operation()
            assert not powerscale_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "writable_snapshots", "return_key": "writable_snapshots"}
    ]
    )
    def test_get_facts_writable_snapshot_api_module(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the writable snapshot api endpoint to get the module response"""

        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': ['writable_snapshots'],
            'zone': "System",
            "filters": [{"filter_key": "id", "filter_operator": "equal", "filter_value": 66258688}]
        })
        powerscale_module_mock.module.params = self.get_module_args

        with patch.object(powerscale_module_mock.snapshot_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            powerscale_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset) == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("gather_subset", [
        "writable_snapshots"
    ]
    )
    def test_get_facts_writable_snapshot_api_exception(self, powerscale_module_mock, gather_subset):
        """Test the get_facts that uses the writable snapshot api endpoint to get the exception"""
        self.get_module_args.update({
            'gather_subset': ['writable_snapshots'],
            'zone': "System",
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.snapshot_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.side_effect = MagicMock(side_effect=MockApiException)
            self.capture_fail_json_call(MockGatherfactsApi.get_gather_facts_error_response(
                gather_subset), invoke_perform_module=True)

    def test_get_filters_empty_case(self, powerscale_module_mock):
        resp = powerscale_module_mock.get_filters()
        assert resp == {}

    def test_get_filters_failure_case1(self, powerscale_module_mock):
        filter_dict = [{"filter_key": "id", "filter_operator": "equal"}]
        with pytest.raises(SystemExit):
            powerscale_module_mock.get_filters(filters=filter_dict)
        assert "filter_key, filter_operator, filter_value are expected." \
               == powerscale_module_mock.module.fail_json.call_args[1][
                   'msg']

    def test_get_filters_failure_case2(self, powerscale_module_mock):
        filter_dict = [{"filter_key": "id", "filter_operator": "less", "filter_value": 123}]
        with pytest.raises(SystemExit):
            powerscale_module_mock.get_filters(filters=filter_dict)
        assert powerscale_module_mock.module.fail_json.call_args[1]['msg'] \
               == "The filter operator is not supported -- only 'equal' is supported."

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "users", "return_key": "Users"}
    ]
    )
    def test_get_facts_auth_user_module(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the auth api endpoint to get the module response"""

        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.auth_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            powerscale_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset)['users'] == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("input_params", [
        {"gather_subset": "ldap", "return_key": "LdapProviders"}
    ]
    )
    def test_get_facts_ldap(self, powerscale_module_mock, input_params):
        """Test the get_facts that uses the auth api endpoint to get the module response"""

        gather_subset = input_params.get('gather_subset')
        return_key = input_params.get('return_key')
        api_response = MockGatherfactsApi.get_gather_facts_api_response(
            gather_subset)
        self.get_module_args.update({
            'gather_subset': [gather_subset]
        })
        powerscale_module_mock.module.params = self.get_module_args
        with patch.object(powerscale_module_mock.auth_api,
                          MockGatherfactsApi.get_gather_facts_error_method(gather_subset)) as mock_method:
            mock_method.return_value = MockSDKResponse(api_response)
            powerscale_module_mock.perform_module_operation()
        assert MockGatherfactsApi.get_gather_facts_module_response(
            gather_subset)['ldap'] == powerscale_module_mock.module.exit_json.call_args[1][return_key]

    @pytest.mark.parametrize("input_params", [
        {
            "mock_data_fetchers": {
                'metadata': lambda x: {'key1': 'value1', 'key2': 'value2'},
            },
            "mock_required_params": ['metadata'],
            "output": {'key1': 'value1', 'key2': 'value2'}
        },
        {
            "mock_data_fetchers": {
                'snapshot': lambda x: ['snapshot1', 'snapshot2'],
            },
            "mock_required_params": ['snapshot'],
            "output": {'snapshots': ['snapshot1', 'snapshot2']}
        },
    ])
    def test_fetch_data_with_snapshot(self, powerscale_module_mock, input_params):
        """Test the fetch_data method with a snapshot in the data fetchers."""
        effective_path = '/path/to/filesystem'
        mock_data_fetchers = input_params['mock_data_fetchers']
        mock_required_params = input_params['mock_required_params']
        fetched_data = powerscale_module_mock.fetch_data(effective_path, mock_data_fetchers, mock_required_params)
        assert fetched_data == input_params["output"]
