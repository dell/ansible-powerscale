# Copyright: (c) 2022-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for NFS Export module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock

from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils
utils.get_nfs_map_object = MagicMock()


from ansible_collections.dellemc.powerscale.plugins.modules.nfs import NfsExport, NFSHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_nfs_export_api as MockNFSApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils.mock_nfs_export_api import NFSTestExport
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase


class TestNfsExport(PowerScaleUnitBase):
    get_nfs_args = MockNFSApi.NFS_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        """
        Returns an instance of the `NFS Export` class for testing purposes.

        :return: An instance of the `NFS Export` class.
        :rtype: `NFS Export`
        """
        return NfsExport

    def test_get_nfs_response(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.get_nfs_args,
            {"path": MockNFSApi.PATH_1,
             "access_zone": MockNFSApi.SYS_ZONE,
             "state": "present"})
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=NFSTestExport(1, MockNFSApi.NFS_1['exports']))
        NFSHandler().handle(powerscale_module_mock,
                            powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.list_nfs_exports.assert_called()

    def test_get_nfs_root_response(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.get_nfs_args,
            {"path": "/",
             "access_zone": "sample-zone",
             "state": "present"})
        powerscale_module_mock.get_zone_base_path = MagicMock(
            return_value="/ifs/sample-zone")
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=NFSTestExport(1, MockNFSApi.NFS_1['exports']))
        NFSHandler().handle(powerscale_module_mock,
                            powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.list_nfs_exports.assert_called()

    def test_get_nfs_non_system_az_response(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.get_nfs_args,
            {"path": "/sample_file_path1",
             "access_zone": "sample_zone",
             "state": "present"})
        powerscale_module_mock.module.params = self.get_nfs_args
        powerscale_module_mock.zones_summary_api.get_zones_summary_zone.to_dict = MagicMock(
            return_value=MockNFSApi.ZONE)
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=NFSTestExport(1, MockNFSApi.NFS_1['exports'])
        )
        NFSHandler().handle(powerscale_module_mock,
                            powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.list_nfs_exports.assert_called()

    def test_get_nfs_non_system_az_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.get_nfs_args,
            {"path": "/sample_file_path1",
             "access_zone": "sample_zone",
             "state": "present"})
        powerscale_module_mock.module.params = self.get_nfs_args
        MockApiException.status = '404'
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=NFSTestExport(1, MockNFSApi.NFS_1['exports']))
        powerscale_module_mock.zones_summary_api.get_zones_summary_zone.to_dict = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNFSApi.get_nfs_failed_msg(), powerscale_module_mock, NFSHandler)

    def operation_before_create(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.get_nfs_args,
            {"path": MockNFSApi.PATH_1,
             "access_zone": MockNFSApi.SYS_ZONE,
             "description": "description",
             "read_only": True,
             "read_only_clients": [MockNFSApi.SAMPLE_IP1],
             "clients": [MockNFSApi.SAMPLE_IP1],
             "client_state": "present-in-export",
             "security_flavors": ["kerberos"],
             "map_root": {
                 "enabled": True, "user": "root", "primary_group": "root",
                 "secondary_groups": [{"name": "group1", "state": "absent"}, {"name": "group2"}]},
             "map_non_root": {
                 "enabled": True, "user": "root", "primary_group": "root",
                 "secondary_groups": [{"name": "group1"}, {"name": "group2", "state": "absent"}]},
             "state": "present"})
        powerscale_module_mock.module.params = self.get_nfs_args
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=NFSTestExport()
        )

    def test_create_nfs_response(self, powerscale_module_mock):
        self.operation_before_create(powerscale_module_mock)
        powerscale_module_mock.isi_sdk.NfsExportCreateParams.to_dict = MagicMock(
            return_value=MockSDKResponse(MockNFSApi.CREATE_NFS_PARAMS))
        NFSHandler().handle(powerscale_module_mock,
                            powerscale_module_mock.module.params)
        powerscale_module_mock.isi_sdk.NfsExportCreateParams.assert_called()
        powerscale_module_mock.protocol_api.create_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_nfs_exception(self, powerscale_module_mock):
        self.operation_before_create(powerscale_module_mock)
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=NFSTestExport(1, MockNFSApi.NFS_1['exports']))
        powerscale_module_mock.protocol_api.create_nfs_export = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNFSApi.create_nfs_failed_msg(), powerscale_module_mock, NFSHandler)

    def test_create_nfs_params_exception(self, powerscale_module_mock):
        self.operation_before_create(powerscale_module_mock)
        powerscale_module_mock.isi_sdk.NfsExportCreateParams = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNFSApi.create_nfs_param_failed_msg(), powerscale_module_mock, NFSHandler)

    def test_create_nfs_without_clients(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.get_nfs_args,
            {"path": MockNFSApi.PATH_1,
             "access_zone": MockNFSApi.SYS_ZONE,
             "description": "description",
             "read_only": True,
             "client_state": "present-in-export",
             "security_flavors": ["kerberos"],
             "state": "present"})
        powerscale_module_mock.module.params = self.get_nfs_args
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=NFSTestExport()
        )
        self.capture_fail_json_call(MockNFSApi.without_clients_failed_msg(), powerscale_module_mock, NFSHandler)

    def test_create_nfs_without_client_state(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.get_nfs_args,
            {"path": MockNFSApi.PATH_1,
             "access_zone": MockNFSApi.SYS_ZONE,
             "read_only": True,
             "read_only_clients": [MockNFSApi.SAMPLE_IP1],
             "clients": [MockNFSApi.SAMPLE_IP1],
             "state": "present"})
        powerscale_module_mock.module.params = self.get_nfs_args
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=NFSTestExport()
        )
        self.capture_fail_json_call(MockNFSApi.without_client_state_failed_msg(), powerscale_module_mock, NFSHandler)

    def operation_before_modify(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.get_nfs_args,
            {"path": MockNFSApi.PATH_1,
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
             "map_root": {
                 "enabled": True, "user": "root", "primary_group": "root",
                 "secondary_groups": [{"name": "group1", "state": "absent"}, {"name": "group2"}]},
             "map_non_root": {"enabled": False}, "state": "present"})
        powerscale_module_mock.module.params = self.get_nfs_args
        powerscale_module_mock.get_nfs_export = MagicMock(
            return_value=MockNFSApi.NFS_1['exports'][0])
        powerscale_module_mock.isi_sdk.NfsExport = MagicMock(
            return_value=MagicMock())

    def test_modify_nfs_response(self, powerscale_module_mock):
        self.operation_before_modify(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock,
                            powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_nfs_response_exception(self, powerscale_module_mock):
        self.operation_before_modify(powerscale_module_mock)
        powerscale_module_mock.protocol_api.update_nfs_export = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNFSApi.modify_nfs_failed_msg(), powerscale_module_mock, NFSHandler)

    def test_remove_clients_nfs(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.get_nfs_args,
            {"path": MockNFSApi.PATH_1,
             "access_zone": MockNFSApi.SYS_ZONE,
             "read_only_clients": [MockNFSApi.SAMPLE_IP2, MockNFSApi.SAMPLE_IP3],
             "clients": [MockNFSApi.SAMPLE_IP2],
             "read_write_clients": [MockNFSApi.SAMPLE_IP2],
             "root_clients": [MockNFSApi.SAMPLE_IP2],
             "client_state": "absent-in-export",
             "state": "present"})
        powerscale_module_mock.module.params = self.get_nfs_args
        powerscale_module_mock.get_nfs_export = MagicMock(
            return_value=MockNFSApi.NFS_2['exports'][0])
        powerscale_module_mock.isi_sdk.NfsExport = MagicMock(
            return_value=MagicMock())
        NFSHandler().handle(powerscale_module_mock,
                            powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_replace_clients_nfs(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.get_nfs_args,
            {"path": MockNFSApi.PATH_1,
             "access_zone": MockNFSApi.SYS_ZONE,
             "read_only_clients": [MockNFSApi.SAMPLE_IP1],
             "clients": [MockNFSApi.SAMPLE_IP2],
             "read_write_clients": [MockNFSApi.SAMPLE_IP3],
             "root_clients": [MockNFSApi.SAMPLE_IP1],
             "state": "present"})
        powerscale_module_mock.module.params = self.get_nfs_args
        powerscale_module_mock.get_nfs_export = MagicMock(
            return_value=MockNFSApi.NFS_2['exports'][0])
        powerscale_module_mock.isi_sdk.NfsExport = MagicMock(
            return_value=MagicMock())
        NFSHandler().handle(powerscale_module_mock,
                            powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_nfs_response(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.get_nfs_args,
            {"path": MockNFSApi.PATH_1,
             "access_zone": MockNFSApi.SYS_ZONE,
             "state": "absent"})
        powerscale_module_mock.module.params = self.get_nfs_args
        powerscale_module_mock.get_nfs_export = MagicMock(
            return_value=MockNFSApi.NFS_2['exports'][0])
        NFSHandler().handle(powerscale_module_mock,
                            powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.delete_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_nfs_response_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.get_nfs_args,
            {"path": MockNFSApi.PATH_1,
             "access_zone": MockNFSApi.SYS_ZONE,
             "state": "absent"})
        powerscale_module_mock.module.params = self.get_nfs_args
        powerscale_module_mock.get_nfs_export = MagicMock(
            return_value=MockNFSApi.NFS_2['exports'][0])
        powerscale_module_mock.protocol_api.delete_nfs_export = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNFSApi.delete_nfs_failed_msg(), powerscale_module_mock, NFSHandler)
