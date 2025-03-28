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


from ansible_collections.dellemc.powerscale.plugins.modules.nfs import NfsExport, NFSHandler, \
    is_map_primary_group_modified, is_map_secondary_groups_modified, main
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
            self.get_nfs_args,
            {"path": MockNFSApi.PATH_1,
             "access_zone": MockNFSApi.SYS_ZONE,
             "state": MockNFSApi.STATE_P})
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=NFSTestExport(1, MockNFSApi.NFS_1['exports']))
        NFSHandler().handle(powerscale_module_mock,
                            powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.list_nfs_exports.assert_called()

    def test_get_nfs_root_response(self, powerscale_module_mock):
        self.set_module_params(
            self.get_nfs_args,
            {"path": "/",
             "access_zone": "sample-zone",
             "state": MockNFSApi.STATE_P})
        powerscale_module_mock.get_zone_base_path = MagicMock(
            return_value="/ifs/sample-zone")
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=NFSTestExport(1, MockNFSApi.NFS_1['exports']))
        NFSHandler().handle(powerscale_module_mock,
                            powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.list_nfs_exports.assert_called()

    def test_get_nfs_non_system_az_response(self, powerscale_module_mock):
        self.set_module_params(
            self.get_nfs_args,
            {"path": "/sample_file_path1",
             "access_zone": "sample_zone",
             "state": MockNFSApi.STATE_P})
        powerscale_module_mock.zones_summary_api.get_zones_summary_zone.to_dict = MagicMock(
            return_value=MockSDKResponse(MockNFSApi.ZONE))
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=NFSTestExport(1, MockNFSApi.NFS_1['exports'])
        )
        NFSHandler().handle(powerscale_module_mock,
                            powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.list_nfs_exports.assert_called()

    def test_get_nfs_non_system_az_exception(self, powerscale_module_mock):
        self.set_module_params(
            self.get_nfs_args,
            {"path": "/sample_file_path1",
             "access_zone": "sample_zone",
             "state": MockNFSApi.STATE_P})
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=NFSTestExport(1, MockNFSApi.NFS_1['exports']))
        powerscale_module_mock.zones_summary_api.get_zones_summary_zone = MagicMock(
            side_effect=MockApiException(404))
        self.capture_fail_json_call(MockNFSApi.get_nfs_non_zone_failed_msg(), NFSHandler)

    def operation_before_create(self, powerscale_module_mock):
        self.set_module_params(
            self.get_nfs_args,
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
                 "secondary_groups": [{"name": "group1", "state": MockNFSApi.STATE_A}, {"name": "group2"}]},
             "map_non_root": {
                 "enabled": True, "user": "root", "primary_group": "root",
                 "secondary_groups": [{"name": "group1"}, {"name": "group2", "state": MockNFSApi.STATE_A}]},
             "state": MockNFSApi.STATE_P})
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
        self.capture_fail_json_call(MockNFSApi.create_nfs_failed_msg(), NFSHandler)

    def test_create_nfs_params_exception(self, powerscale_module_mock):
        self.operation_before_create(powerscale_module_mock)
        powerscale_module_mock.isi_sdk.NfsExportCreateParams = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNFSApi.create_nfs_param_failed_msg(), NFSHandler)

    def test_create_nfs_without_clients(self, powerscale_module_mock):
        self.set_module_params(
            self.get_nfs_args,
            {"path": MockNFSApi.PATH_1,
             "access_zone": MockNFSApi.SYS_ZONE,
             "description": "description",
             "read_only": True,
             "client_state": "present-in-export",
             "security_flavors": ["kerberos"],
             "state": MockNFSApi.STATE_P})
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=NFSTestExport()
        )
        self.capture_fail_json_call(MockNFSApi.without_clients_failed_msg(), NFSHandler)

    def test_create_nfs_without_client_state(self, powerscale_module_mock):
        self.set_module_params(
            self.get_nfs_args,
            {"path": MockNFSApi.PATH_1,
             "access_zone": MockNFSApi.SYS_ZONE,
             "read_only": True,
             "read_only_clients": [MockNFSApi.SAMPLE_IP1],
             "clients": [MockNFSApi.SAMPLE_IP1],
             "state": MockNFSApi.STATE_P})
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=NFSTestExport()
        )
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.create_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def operation_before_modify(self, powerscale_module_mock):
        self.set_module_params(
            self.get_nfs_args,
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
                 "secondary_groups": [{"name": "group1", "state": MockNFSApi.STATE_A}, {"name": "group2"}]},
             "map_non_root": {"enabled": False}, "state": MockNFSApi.STATE_P})
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
        self.capture_fail_json_call(MockNFSApi.modify_nfs_failed_msg(), NFSHandler)

    def test_remove_clients_nfs(self, powerscale_module_mock):
        self.set_module_params(
            self.get_nfs_args,
            {"path": MockNFSApi.PATH_1,
             "access_zone": MockNFSApi.SYS_ZONE,
             "read_only_clients": [MockNFSApi.SAMPLE_IP2, MockNFSApi.SAMPLE_IP3],
             "clients": [MockNFSApi.SAMPLE_IP2],
             "read_write_clients": [MockNFSApi.SAMPLE_IP2],
             "root_clients": [MockNFSApi.SAMPLE_IP2],
             "client_state": "absent-in-export",
             "state": MockNFSApi.STATE_P})
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
            self.get_nfs_args,
            {"path": MockNFSApi.PATH_1,
             "access_zone": MockNFSApi.SYS_ZONE,
             "read_only_clients": [MockNFSApi.SAMPLE_IP1],
             "clients": [MockNFSApi.SAMPLE_IP2],
             "read_write_clients": [MockNFSApi.SAMPLE_IP3],
             "root_clients": [MockNFSApi.SAMPLE_IP1],
             "state": MockNFSApi.STATE_P})
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
            self.get_nfs_args,
            {"path": MockNFSApi.PATH_1,
             "access_zone": MockNFSApi.SYS_ZONE,
             "state": MockNFSApi.STATE_A})
        powerscale_module_mock.get_nfs_export = MagicMock(
            return_value=MockNFSApi.NFS_2['exports'][0])
        NFSHandler().handle(powerscale_module_mock,
                            powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.delete_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_nfs_response_exception(self, powerscale_module_mock):
        self.set_module_params(
            self.get_nfs_args,
            {"path": MockNFSApi.PATH_1,
             "access_zone": MockNFSApi.SYS_ZONE,
             "state": MockNFSApi.STATE_A})
        powerscale_module_mock.get_nfs_export = MagicMock(
            return_value=MockNFSApi.NFS_2['exports'][0])
        powerscale_module_mock.protocol_api.delete_nfs_export = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNFSApi.delete_nfs_failed_msg(), NFSHandler)

    def test_get_zone_base_path_exception(self, powerscale_module_mock):
        self.set_module_params(
            self.get_nfs_args,
            {"path": "sample-path",
             "access_zone": MockNFSApi.SAMPLE_ZONE,
             "state": MockNFSApi.STATE_P})
        powerscale_module_mock.zones_summary_api.get_zones_summary_zone = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(MockNFSApi.get_failed_msgs("az_path_err"), NFSHandler)

    def test_multiple_nfs_exception(self, powerscale_module_mock):
        powerscale_module_mock.protocol_api.list_nfs_exports.return_value.total = 2
        self.capture_fail_json_call("Multiple NFS Exports found", NFSHandler)

    def test_nfs_by_id_exception(self, powerscale_module_mock):
        powerscale_module_mock.protocol_api.get_nfs_export.side_effect = Exception('Test Exception')
        self.capture_fail_json_method("Got error Test Exception while getting NFS export details",
                                      powerscale_module_mock, "_get_nfs_export_from_id", '123', MockNFSApi.SYS_ZONE)

    def test_invalid_path(self, powerscale_module_mock):
        self.capture_fail_json_method("Invalid path path, Path must start with '/'", powerscale_module_mock,
                                      "effective_path", MockNFSApi.SYS_ZONE, 'path')

    @pytest.mark.parametrize(
        "nfs_map_params, nfs_export_details, nfs_export_map, map_type, expected_result",
        [
            (
                {"primary_group": "some_group"},
                {"map_root": {"primary_group": {"id": "domain:groupB"}}},
                MagicMock(primary_group={"name": "groupA"}),
                "map_root",
                True,
            ),
        ]
    )
    def test_is_map_primary_group_modified(self, nfs_map_params, nfs_export_details, nfs_export_map, map_type, expected_result):
        result = is_map_primary_group_modified(nfs_map_params, nfs_export_details, nfs_export_map, map_type)

        assert result == expected_result

    @pytest.mark.parametrize(
        "nfs_map_params, nfs_export_details, nfs_export_map, map_type, expected_result",
        [
            (
                {"secondary_groups": ["groupA"]},
                {"export": {"secondary_groups": ["groupA"]}},
                MagicMock(secondary_groups=[]),
                "export",
                True,
            ),
        ]
    )
    def test_is_map_secondary_groups_modified(self, nfs_map_params, nfs_export_details, nfs_export_map, map_type, expected_result):
        result = is_map_secondary_groups_modified(nfs_map_params, nfs_export_details, nfs_export_map, map_type)

        assert result == expected_result

    def test_main(self, powerscale_module_mock):
        main()

    @pytest.mark.parametrize(
        "playbook_client_dict, nfs_export, mod_flag, expected_result",
        [
            (
                {"read_write_clients": None},
                {"key": "value"},
                False,
                (False, {"key": "value"}),
            )
        ]
    )
    def test_check_read_write_clients_none(self, powerscale_module_mock, playbook_client_dict, nfs_export, mod_flag, expected_result):
        result = powerscale_module_mock._check_read_write_clients(nfs_export, playbook_client_dict, {}, mod_flag)

        assert result == expected_result

    @pytest.mark.parametrize(
        "playbook_client_dict, nfs_export, mod_flag, expected_result",
        [
            (
                {"clients": None},
                {"key": "value"},
                False,
                (False, {"key": "value"}),
            )
        ]
    )
    def test_chek_clients_none(self, powerscale_module_mock, playbook_client_dict, nfs_export, mod_flag, expected_result):
        result = powerscale_module_mock._check_clients(nfs_export, playbook_client_dict, {}, mod_flag)

        assert result == expected_result
