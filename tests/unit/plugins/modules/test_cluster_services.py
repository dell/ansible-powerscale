# Copyright: (c) 2026, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for cluster services module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import copy
from unittest.mock import patch
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.cluster_services import ClusterServices
from ansible_collections.dellemc.powerscale.plugins.modules.cluster_services import ClusterServicesHandler
from ansible_collections.dellemc.powerscale.plugins.modules.cluster_services import main as cluster_services_main
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_cluster_services_api \
    import MockClusterServicesApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response import (
    MockSDKResponse,
)


class TestClusterServices(PowerScaleUnitBase):
    """TestClusterServices definition."""
    cluster_services_args = MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        """Module object."""
        return ClusterServices

    # -------------------------------------------------------------------------
    # GET Operations
    # -------------------------------------------------------------------------

    # U-CS-001: GET - Successful retrieval of all service states (facts gathering)
    def test_get_all_services(self, powerscale_module_mock):
        """Test get all cluster services."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS, {})
        powerscale_module_mock.protocol_api.get_nfs_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_NFS_RESPONSE))
        powerscale_module_mock.protocol_api.get_smb_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_SMB_RESPONSE))
        powerscale_module_mock.protocol_api.get_s3_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_S3_RESPONSE))
        powerscale_module_mock.protocol_api.get_hdfs_settings = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_HDFS_RESPONSE))
        powerscale_module_mock.antivirus_api.get_antivirus_settings = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_ANTIVIRUS_RESPONSE))
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # U-CS-002: GET - Response includes all expected fields
    def test_get_services_response_fields(self, powerscale_module_mock):
        """Test get services response fields."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS, {})
        powerscale_module_mock.protocol_api.get_nfs_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_NFS_RESPONSE))
        powerscale_module_mock.protocol_api.get_smb_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_SMB_RESPONSE))
        powerscale_module_mock.protocol_api.get_s3_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_S3_RESPONSE))
        powerscale_module_mock.protocol_api.get_hdfs_settings = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_HDFS_RESPONSE))
        powerscale_module_mock.antivirus_api.get_antivirus_settings = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_ANTIVIRUS_RESPONSE))
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        call_args = powerscale_module_mock.module.exit_json.call_args[1]
        assert 'cluster_services_details' in call_args
        details = call_args['cluster_services_details']
        for key in ['nfs_service', 'smb_service', 's3_service', 'hdfs_service', 'antivirus_service']:
            assert key in details

    # U-CS-003: GET - Handle ApiException on NFS retrieval
    def test_get_nfs_exception(self, powerscale_module_mock):
        """Test get NFS service exception."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.ENABLE_NFS_ARGS)
        powerscale_module_mock.protocol_api.get_nfs_settings_global = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockClusterServicesApi.get_cluster_services_exception_response('get_nfs_exception'),
            ClusterServicesHandler)

    # U-CS-004: GET - Handle ApiException on SMB retrieval
    def test_get_smb_exception(self, powerscale_module_mock):
        """Test get SMB service exception."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.DISABLE_SMB_ARGS)
        powerscale_module_mock.protocol_api.get_smb_settings_global = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockClusterServicesApi.get_cluster_services_exception_response('get_smb_exception'),
            ClusterServicesHandler)

    # U-CS-005: GET - Handle ApiException on Antivirus retrieval
    def test_get_antivirus_exception(self, powerscale_module_mock):
        """Test get Antivirus service exception."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.ENABLE_ANTIVIRUS_ARGS)
        powerscale_module_mock.antivirus_api.get_antivirus_settings = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockClusterServicesApi.get_cluster_services_exception_response('get_antivirus_exception'),
            ClusterServicesHandler)

    # -------------------------------------------------------------------------
    # UPDATE Operations
    # -------------------------------------------------------------------------

    # U-CS-010: UPDATE - Enable NFS service
    def test_enable_nfs_service(self, powerscale_module_mock):
        """Test enable NFS service."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.ENABLE_NFS_ARGS)
        powerscale_module_mock.get_service_status = MagicMock(
            return_value=False)
        powerscale_module_mock.protocol_api.get_nfs_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_NFS_DISABLED_RESPONSE))
        powerscale_module_mock.protocol_api.update_nfs_settings_global = MagicMock(return_value=None)
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # U-CS-011: UPDATE - Disable SMB service
    def test_disable_smb_service(self, powerscale_module_mock):
        """Test disable SMB service."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.DISABLE_SMB_ARGS)
        powerscale_module_mock.protocol_api.get_smb_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_SMB_RESPONSE))
        powerscale_module_mock.protocol_api.update_smb_settings_global = MagicMock(return_value=None)
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # U-CS-012: UPDATE - Enable S3 service
    def test_enable_s3_service(self, powerscale_module_mock):
        """Test enable S3 service."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.ENABLE_S3_ARGS)
        powerscale_module_mock.protocol_api.get_s3_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_S3_RESPONSE))
        powerscale_module_mock.protocol_api.update_s3_settings_global = MagicMock(return_value=None)
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # U-CS-013: UPDATE - Enable HDFS service
    def test_enable_hdfs_service(self, powerscale_module_mock):
        """Test enable HDFS service."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.ENABLE_HDFS_ARGS)
        powerscale_module_mock.protocol_api.get_hdfs_settings = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_HDFS_RESPONSE))
        powerscale_module_mock.protocol_api.update_hdfs_settings = MagicMock(return_value=None)
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # U-CS-014: UPDATE - Enable Antivirus service
    def test_enable_antivirus_service(self, powerscale_module_mock):
        """Test enable Antivirus service."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.ENABLE_ANTIVIRUS_ARGS)
        powerscale_module_mock.antivirus_api.get_antivirus_settings = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_ANTIVIRUS_DISABLED_RESPONSE))
        powerscale_module_mock.antivirus_api.update_antivirus_settings = MagicMock(return_value=None)
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -------------------------------------------------------------------------
    # Exception Handling
    # -------------------------------------------------------------------------

    # U-CS-020: EXCEPTION - Modify NFS exception
    def test_modify_nfs_exception(self, powerscale_module_mock):
        """Test modify NFS service exception."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.ENABLE_NFS_ARGS)
        powerscale_module_mock.protocol_api.get_nfs_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_NFS_DISABLED_RESPONSE))
        powerscale_module_mock.protocol_api.update_nfs_settings_global = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockClusterServicesApi.get_cluster_services_exception_response('modify_nfs_exception'),
            ClusterServicesHandler)

    # U-CS-021: EXCEPTION - Modify S3 exception
    def test_modify_s3_exception(self, powerscale_module_mock):
        """Test modify S3 service exception."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.ENABLE_S3_ARGS)
        powerscale_module_mock.protocol_api.get_s3_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_S3_RESPONSE))
        powerscale_module_mock.protocol_api.update_s3_settings_global = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockClusterServicesApi.get_cluster_services_exception_response('modify_s3_exception'),
            ClusterServicesHandler)

    # U-CS-022: EXCEPTION - Modify Antivirus exception
    def test_modify_antivirus_exception(self, powerscale_module_mock):
        """Test modify Antivirus service exception."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.ENABLE_ANTIVIRUS_ARGS)
        powerscale_module_mock.antivirus_api.get_antivirus_settings = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_ANTIVIRUS_DISABLED_RESPONSE))
        powerscale_module_mock.antivirus_api.update_antivirus_settings = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockClusterServicesApi.get_cluster_services_exception_response('modify_antivirus_exception'),
            ClusterServicesHandler)

    # -------------------------------------------------------------------------
    # Idempotency
    # -------------------------------------------------------------------------

    # U-CS-030: IDEMPOTENT - NFS already enabled
    def test_idempotent_nfs_already_enabled(self, powerscale_module_mock):
        """Test idempotent NFS already enabled."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.ENABLE_NFS_ARGS)
        powerscale_module_mock.protocol_api.get_nfs_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_NFS_RESPONSE))
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False
        powerscale_module_mock.protocol_api.update_nfs_settings_global.assert_not_called()

    # U-CS-031: IDEMPOTENT - SMB already disabled
    def test_idempotent_smb_already_disabled(self, powerscale_module_mock):
        """Test idempotent SMB already disabled."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.DISABLE_SMB_ARGS)
        powerscale_module_mock.protocol_api.get_smb_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_SMB_DISABLED_RESPONSE))
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False
        powerscale_module_mock.protocol_api.update_smb_settings_global.assert_not_called()

    # U-CS-032: IDEMPOTENT - No params = facts only
    def test_idempotent_no_params(self, powerscale_module_mock):
        """Test idempotent no params returns facts only."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS, {})
        powerscale_module_mock.protocol_api.get_nfs_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_NFS_RESPONSE))
        powerscale_module_mock.protocol_api.get_smb_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_SMB_RESPONSE))
        powerscale_module_mock.protocol_api.get_s3_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_S3_RESPONSE))
        powerscale_module_mock.protocol_api.get_hdfs_settings = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_HDFS_RESPONSE))
        powerscale_module_mock.antivirus_api.get_antivirus_settings = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_ANTIVIRUS_RESPONSE))
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False
        assert powerscale_module_mock.module.exit_json.call_args[1]['cluster_services_details'] is not None

    # -------------------------------------------------------------------------
    # Check Mode
    # -------------------------------------------------------------------------

    # U-CS-040: CHECK MODE - Enable NFS
    def test_check_mode_enable_nfs(self, powerscale_module_mock):
        """Test check mode enable NFS."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.ENABLE_NFS_ARGS)
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.protocol_api.get_nfs_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_NFS_DISABLED_RESPONSE))
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.update_nfs_settings_global.assert_not_called()

    # U-CS-041: CHECK MODE - Disable SMB
    def test_check_mode_disable_smb(self, powerscale_module_mock):
        """Test check mode disable SMB."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.DISABLE_SMB_ARGS)
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.protocol_api.get_smb_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_SMB_RESPONSE))
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.update_smb_settings_global.assert_not_called()

    # -------------------------------------------------------------------------
    # Diff Mode
    # -------------------------------------------------------------------------

    # U-CS-050: DIFF MODE - Enable NFS
    def test_diff_mode_enable_nfs(self, powerscale_module_mock):
        """Test diff mode enable NFS."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.ENABLE_NFS_ARGS)
        powerscale_module_mock.module._diff = True
        powerscale_module_mock.protocol_api.get_nfs_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_NFS_DISABLED_RESPONSE))
        powerscale_module_mock.protocol_api.update_nfs_settings_global = MagicMock(return_value=None)
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert 'diff' in result
        assert result['diff']['before']['nfs_service'] is False
        assert result['diff']['after']['nfs_service'] is True

    # U-CS-051: DIFF MODE - Multiple services
    def test_diff_mode_multiple_services(self, powerscale_module_mock):
        """Test diff mode multiple services."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               {"nfs_service": True, "smb_service": False})
        powerscale_module_mock.module._diff = True
        powerscale_module_mock.protocol_api.get_nfs_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_NFS_DISABLED_RESPONSE))
        powerscale_module_mock.protocol_api.get_smb_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_SMB_RESPONSE))
        powerscale_module_mock.protocol_api.update_nfs_settings_global = MagicMock(return_value=None)
        powerscale_module_mock.protocol_api.update_smb_settings_global = MagicMock(return_value=None)
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert 'diff' in result
        assert result['diff']['before']['nfs_service'] is False
        assert result['diff']['after']['nfs_service'] is True
        assert result['diff']['before']['smb_service'] is True
        assert result['diff']['after']['smb_service'] is False

    # -------------------------------------------------------------------------
    # Multi-service / Boundary
    # -------------------------------------------------------------------------

    # U-CS-060: BOUNDARY - Enable all 5 services
    def test_enable_all_services(self, powerscale_module_mock):
        """Test enable all services."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.ENABLE_ALL_ARGS)
        powerscale_module_mock.protocol_api.get_nfs_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_NFS_DISABLED_RESPONSE))
        powerscale_module_mock.protocol_api.get_smb_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_SMB_DISABLED_RESPONSE))
        powerscale_module_mock.protocol_api.get_s3_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_S3_RESPONSE))
        powerscale_module_mock.protocol_api.get_hdfs_settings = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_HDFS_RESPONSE))
        powerscale_module_mock.antivirus_api.get_antivirus_settings = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_ANTIVIRUS_DISABLED_RESPONSE))
        for method in ('update_nfs_settings_global', 'update_smb_settings_global',
                       'update_s3_settings_global', 'update_hdfs_settings'):
            setattr(powerscale_module_mock.protocol_api, method, MagicMock(return_value=None))
        powerscale_module_mock.antivirus_api.update_antivirus_settings = MagicMock(return_value=None)
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # U-CS-061: BOUNDARY - Disable all 5 services
    def test_disable_all_services(self, powerscale_module_mock):
        """Test disable all services."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.DISABLE_ALL_ARGS)
        powerscale_module_mock.protocol_api.get_nfs_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_NFS_RESPONSE))
        powerscale_module_mock.protocol_api.get_smb_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_SMB_RESPONSE))
        powerscale_module_mock.protocol_api.get_s3_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_S3_ENABLED_RESPONSE))
        powerscale_module_mock.protocol_api.get_hdfs_settings = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_HDFS_ENABLED_RESPONSE))
        powerscale_module_mock.antivirus_api.get_antivirus_settings = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_ANTIVIRUS_RESPONSE))
        for method in ('update_nfs_settings_global', 'update_smb_settings_global',
                       'update_s3_settings_global', 'update_hdfs_settings'):
            setattr(powerscale_module_mock.protocol_api, method, MagicMock(return_value=None))
        powerscale_module_mock.antivirus_api.update_antivirus_settings = MagicMock(return_value=None)
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # U-CS-062: BOUNDARY - Partial update (2 of 5)
    def test_partial_service_update(self, powerscale_module_mock):
        """Test partial service update."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.PARTIAL_ARGS)
        powerscale_module_mock.protocol_api.get_nfs_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_NFS_DISABLED_RESPONSE))
        powerscale_module_mock.protocol_api.get_s3_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_S3_ENABLED_RESPONSE))
        powerscale_module_mock.protocol_api.update_nfs_settings_global = MagicMock(return_value=None)
        powerscale_module_mock.protocol_api.update_s3_settings_global = MagicMock(return_value=None)
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.update_smb_settings_global.assert_not_called()
        powerscale_module_mock.protocol_api.update_hdfs_settings.assert_not_called()

    # -------------------------------------------------------------------------
    # Module Infrastructure
    # -------------------------------------------------------------------------

    # U-CS-070: Module main() entry point
    def test_main_function(self, powerscale_module_mock):
        """Test module main function."""
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS, {})
        powerscale_module_mock.protocol_api.get_nfs_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_NFS_RESPONSE))
        powerscale_module_mock.protocol_api.get_smb_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_SMB_RESPONSE))
        powerscale_module_mock.protocol_api.get_s3_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_S3_RESPONSE))
        powerscale_module_mock.protocol_api.get_hdfs_settings = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_HDFS_RESPONSE))
        powerscale_module_mock.antivirus_api.get_antivirus_settings = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_ANTIVIRUS_RESPONSE))
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.module.exit_json.assert_called()

    # U-CS-071: SDK prerequisites failure
    def test_sdk_prereqs_failure(self, powerscale_module_mock):
        """Test SDK prerequisites failure."""
        original_return = utils.validate_module_pre_reqs.return_value
        utils.validate_module_pre_reqs.return_value = (
            MockClusterServicesApi.PREREQS_VALIDATE_FAILURE
        )
        mock_module = MagicMock()
        mock_module.params = copy.deepcopy(
            MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS)
        mock_module.check_mode = False
        mock_module.fail_json = MagicMock(side_effect=SystemExit)
        mock_am = MagicMock(return_value=mock_module)
        try:
            with patch(
                'ansible_collections.dellemc.powerscale.plugins.modules'
                '.cluster_services.AnsibleModule', mock_am
            ):
                with pytest.raises(SystemExit):
                    ClusterServices()
            mock_module.fail_json.assert_called_once()
            assert "Required SDK packages not found" in str(
                mock_module.fail_json.call_args)
        finally:
            utils.validate_module_pre_reqs.return_value = original_return

    # -------------------------------------------------------------------------
    # Integration Flow Tests
    # -------------------------------------------------------------------------

    # I-CS-002: Enable then disable NFS flow
    def test_enable_then_disable_nfs_flow(self, powerscale_module_mock):
        """Test enable then disable NFS flow."""
        # Step 1: Enable NFS
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.ENABLE_NFS_ARGS)
        powerscale_module_mock.protocol_api.get_nfs_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_NFS_DISABLED_RESPONSE))
        powerscale_module_mock.protocol_api.update_nfs_settings_global = MagicMock(return_value=None)
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

        # Step 2: Disable NFS
        powerscale_module_mock.module.exit_json.reset_mock()
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.DISABLE_NFS_ARGS)
        powerscale_module_mock.protocol_api.get_nfs_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_NFS_RESPONSE))
        powerscale_module_mock.protocol_api.update_nfs_settings_global = MagicMock(return_value=None)
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # I-CS-003: Full service lifecycle
    def test_full_service_lifecycle(self, powerscale_module_mock):
        """Test full service lifecycle."""
        # Step 1: Get facts
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS, {})
        powerscale_module_mock.protocol_api.get_nfs_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_NFS_DISABLED_RESPONSE))
        powerscale_module_mock.protocol_api.get_smb_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_SMB_DISABLED_RESPONSE))
        powerscale_module_mock.protocol_api.get_s3_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_S3_RESPONSE))
        powerscale_module_mock.protocol_api.get_hdfs_settings = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_HDFS_RESPONSE))
        powerscale_module_mock.antivirus_api.get_antivirus_settings = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_ANTIVIRUS_DISABLED_RESPONSE))
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

        # Step 2: Enable all
        powerscale_module_mock.module.exit_json.reset_mock()
        self.set_module_params(MockClusterServicesApi.CLUSTER_SERVICES_COMMON_ARGS,
                               MockClusterServicesApi.ENABLE_ALL_ARGS)
        for method in ('update_nfs_settings_global', 'update_smb_settings_global',
                       'update_s3_settings_global', 'update_hdfs_settings'):
            setattr(powerscale_module_mock.protocol_api, method, MagicMock(return_value=None))
        powerscale_module_mock.antivirus_api.update_antivirus_settings = MagicMock(return_value=None)
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

        # Step 3: Idempotent re-run (all already enabled)
        powerscale_module_mock.module.exit_json.reset_mock()
        powerscale_module_mock.result = {"changed": False, "cluster_services_details": {}}
        powerscale_module_mock.protocol_api.get_nfs_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_NFS_RESPONSE))
        powerscale_module_mock.protocol_api.get_smb_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_SMB_RESPONSE))
        powerscale_module_mock.protocol_api.get_s3_settings_global = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_S3_ENABLED_RESPONSE))
        powerscale_module_mock.protocol_api.get_hdfs_settings = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_HDFS_ENABLED_RESPONSE))
        powerscale_module_mock.antivirus_api.get_antivirus_settings = MagicMock(
            return_value=MockSDKResponse(MockClusterServicesApi.GET_ANTIVIRUS_RESPONSE))
        ClusterServicesHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False
