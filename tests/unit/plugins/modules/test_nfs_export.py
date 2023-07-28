# Copyright: (c) 2022, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for NFS Export module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

utils.get_logger = MagicMock()
utils.isi_sdk = MagicMock()
from ansible.module_utils import basic
basic.AnsibleModule = MagicMock()


from ansible_collections.dellemc.powerscale.plugins.modules.nfs import NfsExport
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_nfs_export_api as MockNFSApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException


class TestNfsExport():
    get_nfs_args = MockNFSApi.NFS_COMMON_ARGS

    @pytest.fixture
    def nfs_module_mock(self, mocker):
        mocker.patch(MockNFSApi.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        nfs_module_mock = NfsExport()
        nfs_module_mock.module = MagicMock()
        nfs_module_mock.module.check_mode = False
        return nfs_module_mock

    def test_get_nfs_response(self, nfs_module_mock):
        self.get_nfs_args.update({"path": MockNFSApi.PATH_1,
                                  "access_zone": MockNFSApi.SYS_ZONE,
                                  "state": "present"})
        nfs_module_mock.module.params = self.get_nfs_args
        nfs_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=MockSDKResponse(MockNFSApi.NFS_1))
        nfs_module_mock.perform_module_operation()
        nfs_module_mock.protocol_api.list_nfs_exports.assert_called()

    def test_get_nfs_root_response(self, nfs_module_mock):
        self.get_nfs_args.update({"path": "/",
                                  "access_zone": "sample-zone",
                                  "state": "present"})
        nfs_module_mock.module.params = self.get_nfs_args
        nfs_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=MockNFSApi.NFS_1)
        nfs_module_mock.perform_module_operation()
        nfs_module_mock.protocol_api.list_nfs_exports.assert_called()

    def test_get_nfs_response_using_id(self, nfs_module_mock):
        self.get_nfs_args.update({"path": MockNFSApi.PATH_1,
                                  "access_zone": MockNFSApi.SYS_ZONE,
                                  "state": "present"})
        nfs_module_mock.module.params = self.get_nfs_args
        nfs_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=None)
        nfs_module_mock.protocol_api.get_nfs_export = MagicMock(
            side_effect=utils.ApiException)
        nfs_module_mock.perform_module_operation()
        nfs_module_mock.protocol_api.get_nfs_export.assert_called()

    def test_get_nfs_response_multiple_path(self, nfs_module_mock):
        self.get_nfs_args.update({"path": MockNFSApi.PATH_1,
                                  "access_zone": MockNFSApi.SYS_ZONE,
                                  "state": "present"})
        nfs_module_mock.module.params = self.get_nfs_args
        nfs_module_mock.protocol_api.list_nfs_exports.to_dict = MagicMock(
            return_value=MockNFSApi.NFS_MULTIPLE)
        nfs_module_mock.perform_module_operation()
        nfs_module_mock.protocol_api.get_nfs_export.assert_called()

    def test_get_nfs_non_system_az_response(self, nfs_module_mock):
        self.get_nfs_args.update({"path": "/sample_file_path1",
                                  "access_zone": "sample_zone",
                                  "state": "present"})
        nfs_module_mock.module.params = self.get_nfs_args
        nfs_module_mock.zone_summary_api.get_zones_summary_zone.to_dict = MagicMock(
            return_value=MockNFSApi.ZONE)
        nfs_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=MockSDKResponse(MockNFSApi.NFS_1))
        nfs_module_mock.perform_module_operation()
        nfs_module_mock.protocol_api.list_nfs_exports.assert_called()

    def test_get_nfs_non_system_az_exception(self, nfs_module_mock):
        self.get_nfs_args.update({"path": "/sample_file_path1",
                                  "access_zone": "sample_zone",
                                  "state": "present"})
        nfs_module_mock.module.params = self.get_nfs_args
        MockApiException.status = '404'
        nfs_module_mock.zone_summary_api.get_zones_summary_zone.to_dict = MagicMock(
            side_effect=utils.ApiException)
        nfs_module_mock.perform_module_operation()
        nfs_module_mock.protocol_api.list_nfs_exports.assert_called()

    def test_get_nfs_404_exception(self, nfs_module_mock):
        self.get_nfs_args.update({"path": MockNFSApi.PATH_1,
                                  "access_zone": MockNFSApi.SYS_ZONE,
                                  "state": "present"})
        nfs_module_mock.module.params = self.get_nfs_args
        MockApiException.status = '404'
        nfs_module_mock.protocol_api.list_nfs_exports = MagicMock(
            side_effect=utils.ApiException)
        nfs_module_mock.perform_module_operation()
        assert MockNFSApi.get_nfs_failed_msg() in \
               nfs_module_mock.module.fail_json.call_args[1]['msg']
        nfs_module_mock.protocol_api.list_nfs_exports.assert_called()

    def operation_before_create(self, nfs_module_mock):
        self.get_nfs_args.update({"path": MockNFSApi.PATH_1,
                                  "access_zone": MockNFSApi.SYS_ZONE,
                                  "description": "description",
                                  "read_only": True,
                                  "read_only_clients": [MockNFSApi.SAMPLE_IP1],
                                  "clients": [MockNFSApi.SAMPLE_IP1],
                                  "client_state": "present-in-export",
                                  "security_flavors": ["kerberos"],
                                  "state": "present"})
        nfs_module_mock.module.params = self.get_nfs_args
        nfs_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=None)

    def test_create_nfs_response(self, nfs_module_mock):
        self.operation_before_create(nfs_module_mock)
        nfs_module_mock.isi_sdk.NfsExportCreateParams.to_dict = MagicMock(
            return_value=MockSDKResponse(MockNFSApi.CREATE_NFS_PARAMS))
        nfs_module_mock.perform_module_operation()
        nfs_module_mock.isi_sdk.NfsExportCreateParams.assert_called()
        nfs_module_mock.protocol_api.create_nfs_export.assert_called()
        assert nfs_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_nfs_exception(self, nfs_module_mock):
        self.operation_before_create(nfs_module_mock)
        nfs_module_mock.isi_sdk.NfsExportCreateParams = MagicMock(
            return_value=MockNFSApi.NFS_1)
        nfs_module_mock.protocol_api.create_nfs_export = MagicMock(
            side_effect=utils.ApiException)
        nfs_module_mock.perform_module_operation()
        nfs_module_mock.isi_sdk.NfsExportCreateParams.assert_called()
        nfs_module_mock.protocol_api.create_nfs_export.assert_called()
        assert MockNFSApi.create_nfs_failed_msg() in \
            nfs_module_mock.module.fail_json.call_args[1]['msg']

    def test_create_nfs_params_exception(self, nfs_module_mock):
        self.operation_before_create(nfs_module_mock)
        nfs_module_mock.isi_sdk.NfsExportCreateParams = MagicMock(
            side_effect=utils.ApiException)
        nfs_module_mock.perform_module_operation()
        nfs_module_mock.isi_sdk.NfsExportCreateParams.assert_called()
        assert MockNFSApi.create_nfs_param_failed_msg() in \
            nfs_module_mock.module.fail_json.call_args[1]['msg']

    def test_create_nfs_without_clients(self, nfs_module_mock):
        self.get_nfs_args.update({"path": MockNFSApi.PATH_1,
                                  "access_zone": MockNFSApi.SYS_ZONE,
                                  "description": "description",
                                  "read_only": True,
                                  "client_state": "present-in-export",
                                  "security_flavors": ["kerberos"],
                                  "state": "present"})
        nfs_module_mock.module.params = self.get_nfs_args
        nfs_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=None)
        nfs_module_mock.perform_module_operation()
        assert MockNFSApi.without_clients_failed_msg() in \
            nfs_module_mock.module.fail_json.call_args[1]['msg']

    def test_create_nfs_without_client_state(self, nfs_module_mock):
        self.get_nfs_args.update({"path": MockNFSApi.PATH_1,
                                  "access_zone": MockNFSApi.SYS_ZONE,
                                  "read_only": True,
                                  "read_only_clients": [MockNFSApi.SAMPLE_IP1],
                                  "clients": [MockNFSApi.SAMPLE_IP1],
                                  "state": "present"})
        nfs_module_mock.module.params = self.get_nfs_args
        nfs_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=None)
        nfs_module_mock.perform_module_operation()
        assert MockNFSApi.without_client_state_failed_msg() in \
            nfs_module_mock.module.fail_json.call_args[1]['msg']

    def operation_before_modify(self, nfs_module_mock):
        self.get_nfs_args.update({"path": MockNFSApi.PATH_1,
                                  "access_zone": MockNFSApi.SYS_ZONE,
                                  "description": "description1",
                                  "read_only": True,
                                  "read_only_clients": [MockNFSApi.SAMPLE_IP2, MockNFSApi.SAMPLE_IP3],
                                  "clients": [MockNFSApi.SAMPLE_IP2],
                                  "read_write_clients": [MockNFSApi.SAMPLE_IP2],
                                  "root_clients": [MockNFSApi.SAMPLE_IP2],
                                  "client_state": "present-in-export",
                                  "sub_directories_mountable": True,
                                  "security_flavors": ["unix", "kerberos_privacy"],
                                  "state": "present"})
        nfs_module_mock.module.params = self.get_nfs_args
        nfs_module_mock.get_nfs_export = MagicMock(
            return_value=MockNFSApi.NFS_1['exports'][0])
        nfs_module_mock.isi_sdk.NfsExport = MagicMock(
            return_value=MagicMock())

    def test_modify_nfs_response(self, nfs_module_mock):
        self.operation_before_modify(nfs_module_mock)
        nfs_module_mock.perform_module_operation()
        nfs_module_mock.protocol_api.update_nfs_export.assert_called()
        assert nfs_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_nfs_response_exception(self, nfs_module_mock):
        self.operation_before_modify(nfs_module_mock)
        nfs_module_mock.protocol_api.update_nfs_export = MagicMock(
            side_effect=utils.ApiException)
        nfs_module_mock.perform_module_operation()
        nfs_module_mock.protocol_api.update_nfs_export.assert_called()
        assert MockNFSApi.modify_nfs_failed_msg() in \
               nfs_module_mock.module.fail_json.call_args[1]['msg']

    def test_remove_clients_nfs(self, nfs_module_mock):
        self.get_nfs_args.update({"path": MockNFSApi.PATH_1,
                                  "access_zone": MockNFSApi.SYS_ZONE,
                                  "read_only_clients": [MockNFSApi.SAMPLE_IP2,
                                                        MockNFSApi.SAMPLE_IP3],
                                  "clients": [MockNFSApi.SAMPLE_IP2],
                                  "read_write_clients": [
                                      MockNFSApi.SAMPLE_IP2],
                                  "root_clients": [MockNFSApi.SAMPLE_IP2],
                                  "client_state": "absent-in-export",
                                  "state": "present"})
        nfs_module_mock.module.params = self.get_nfs_args
        nfs_module_mock.get_nfs_export = MagicMock(
            return_value=MockNFSApi.NFS_2['exports'][0])
        nfs_module_mock.isi_sdk.NfsExport = MagicMock(
            return_value=MagicMock())
        nfs_module_mock.perform_module_operation()
        nfs_module_mock.protocol_api.update_nfs_export.assert_called()
        assert nfs_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_nfs_response(self, nfs_module_mock):
        self.get_nfs_args.update({"path": MockNFSApi.PATH_1,
                                  "access_zone": MockNFSApi.SYS_ZONE,
                                  "state": "absent"})
        nfs_module_mock.module.params = self.get_nfs_args
        nfs_module_mock.get_nfs_export = MagicMock(
            return_value=MockNFSApi.NFS_2['exports'][0])
        nfs_module_mock.perform_module_operation()
        nfs_module_mock.protocol_api.delete_nfs_export.assert_called()
        assert nfs_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_nfs_response_exception(self, nfs_module_mock):
        self.get_nfs_args.update({"path": MockNFSApi.PATH_1,
                                  "access_zone": MockNFSApi.SYS_ZONE,
                                  "state": "absent"})
        nfs_module_mock.module.params = self.get_nfs_args
        nfs_module_mock.get_nfs_export = MagicMock(
            return_value=MockNFSApi.NFS_2['exports'][0])
        nfs_module_mock.protocol_api.delete_nfs_export = MagicMock(
            side_effect=utils.ApiException)
        nfs_module_mock.perform_module_operation()
        nfs_module_mock.protocol_api.delete_nfs_export.assert_called()
        assert MockNFSApi.delete_nfs_failed_msg() in \
               nfs_module_mock.module.fail_json.call_args[1]['msg']
