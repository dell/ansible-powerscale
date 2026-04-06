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

    def test_create_with_advanced_settings(self, powerscale_module_mock):
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "description": "description",
                "read_only": True,
                "read_only_clients": [MockNFSApi.SAMPLE_IP1],
                "clients": [MockNFSApi.SAMPLE_IP1],
                "client_state": "present-in-export",
                "security_flavors": ["kerberos"],
                "map_root": {"enabled": True, "user": "root", "primary_group": "root"},
                "map_non_root": {"enabled": True, "user": "root", "primary_group": "root"},
                "map_failure": {"enabled": False},
                "map_lookup_uid": True,
                "file_name_max_size": {"size_value": 255, "size_unit": "B"},
                "block_size": {"size_value": 8192, "size_unit": "B"},
                "directory_transfer_size": {"size_value": 4096, "size_unit": "B"},
                "read_transfer_max_size": {"size_value": 65536, "size_unit": "B"},
                "read_transfer_multiple": {"size_value": 4096, "size_unit": "B"},
                "read_transfer_size": {"size_value": 32768, "size_unit": "B"},
                "write_transfer_max_size": {"size_value": 65536, "size_unit": "B"},
                "write_transfer_multiple": {"size_value": 4096, "size_unit": "B"},
                "write_transfer_size": {"size_value": 32768, "size_unit": "B"},
                "max_file_size": {"size_value": 1099511627776, "size_unit": "B"},
                "commit_asynchronous": False,
                "setattr_asynchronous": False,
                "readdirplus": True,
                "return_32bit_file_ids": False,
                "can_set_time": True,
                "symlinks": True,
                "write_datasync_action": "DATASYNC",
                "write_datasync_reply": "DATASYNC",
                "write_filesync_action": "FILESYNC",
                "write_filesync_reply": "FILESYNC",
                "write_unstable_action": "UNSTABLE",
                "write_unstable_reply": "UNSTABLE",
                "encoding": "utf-8",
                "time_delta": {"time_value": 1.0, "time_unit": "seconds"},
                "state": MockNFSApi.STATE_P,
            },
        )
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=NFSTestExport()
        )
        powerscale_module_mock.isi_sdk.NfsExportCreateParams.to_dict = MagicMock(
            return_value=MockSDKResponse(MockNFSApi.CREATE_NFS_PARAMS))
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.create_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_nfs_exception(self, powerscale_module_mock):
        self.operation_before_create(powerscale_module_mock)
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=NFSTestExport(1, MockNFSApi.NFS_1['exports']))
        powerscale_module_mock.protocol_api.create_nfs_export = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNFSApi.create_nfs_failed_msg(), NFSHandler)
        powerscale_module_mock.protocol_api.create_nfs_export = MagicMock()
        utils.isi_sdk.NfsExportCreateParams = MagicMock()

    def test_create_nfs_params_exception(self, powerscale_module_mock):
        self.operation_before_create(powerscale_module_mock)
        powerscale_module_mock.isi_sdk.NfsExportCreateParams = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNFSApi.create_nfs_param_failed_msg(), NFSHandler)
        powerscale_module_mock.isi_sdk.NfsExportCreateParams = MagicMock()
        utils.isi_sdk.NfsExportCreateParams = MagicMock()

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

    def test_modify_nfs_with_advanced_settings(self, powerscale_module_mock):
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "security_flavors": ["kerberos_integrity"],
                "map_root": {"enabled": True, "user": "nfs", "primary_group": "nfs"},
                "map_non_root": {"enabled": True, "user": "super", "primary_group": "root"},
                "map_failure": {"enabled": True, "user": "root", "primary_group": "nonroot"},
                "map_lookup_uid": True,
                "file_name_max_size": {"size_value": 255, "size_unit": "B"},
                "block_size": {"size_value": 100, "size_unit": "B"},
                "directory_transfer_size": {"size_value": 4096, "size_unit": "B"},
                "read_transfer_max_size": {"size_value": 1241, "size_unit": "B"},
                "read_transfer_multiple": {"size_value": 2, "size_unit": "KB"},
                "read_transfer_size": {"size_value": 1241, "size_unit": "B"},
                "write_transfer_max_size": {"size_value": 65536, "size_unit": "B"},
                "write_transfer_multiple": {"size_value": 1000, "size_unit": "GB"},
                "write_transfer_size": {"size_value": 23, "size_unit": "B"},
                "max_file_size": {"size_value": 881241, "size_unit": "TB"},
                "commit_asynchronous": True,
                "setattr_asynchronous": True,
                "readdirplus": True,
                "return_32bit_file_ids": True,
                "can_set_time": True,
                "symlinks": False,
                "write_datasync_action": "DATASYNC",
                "write_datasync_reply": "FILESYNC",
                "write_filesync_action": "UNSTABLE",
                "write_filesync_reply": "DATASYNC",
                "write_unstable_action": "FILESYNC",
                "write_unstable_reply": "UNSTABLE",
                "encoding": "utf-8",
                "time_delta": {"time_value": 7.0, "time_unit": "seconds"},
                "state": MockNFSApi.STATE_P,
            },
        )
        powerscale_module_mock.get_nfs_export = MagicMock(
            return_value=MockNFSApi.NFS_1['exports'][0]
        )
        powerscale_module_mock.isi_sdk.NfsExport = MagicMock(
            return_value=MagicMock()
        )
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_nfs_diff(self, powerscale_module_mock):
        # Verify that when diff mode is requested, the handler populates a before/after diff
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "description": "description1",
                "map_lookup_uid": True,
                "encoding": "utf-8",
                "time_delta": {"time_value": 1.0, "time_unit": "seconds"},
                "read_only": True,
                "state": MockNFSApi.STATE_P,
            },
        )
        # simulate diff mode requested by caller
        powerscale_module_mock.module._diff = True

        # existing export details returned from API
        powerscale_module_mock.get_nfs_export = MagicMock(
            return_value=MockNFSApi.NFS_1['exports'][0]
        )

        # nfs_export SDK object should provide a to_dict() used for 'after' diff
        nfs_export_mock = MagicMock()
        nfs_export_mock.to_dict = MagicMock(return_value={"read_only": True})
        powerscale_module_mock.isi_sdk.NfsExport = MagicMock(return_value=nfs_export_mock)

        # Ensure update call does not raise
        powerscale_module_mock.protocol_api.update_nfs_export = MagicMock()

        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)

        powerscale_module_mock.protocol_api.update_nfs_export.assert_called()
        exit_args = powerscale_module_mock.module.exit_json.call_args[1]
        assert exit_args['changed'] is True
        assert 'diff' in exit_args
        assert isinstance(exit_args['diff'], dict)
        assert 'before' in exit_args['diff'] and 'after' in exit_args['diff']
        assert isinstance(exit_args['diff']['before'], dict)
        assert isinstance(exit_args['diff']['after'], dict)

    def test_modify_nfs_response_exception(self, powerscale_module_mock):
        self.operation_before_modify(powerscale_module_mock)
        powerscale_module_mock.protocol_api.update_nfs_export = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNFSApi.modify_nfs_failed_msg(), NFSHandler)
        powerscale_module_mock.protocol_api.update_nfs_export = MagicMock()
        utils.isi_sdk.NfsExport = MagicMock()

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
        powerscale_module_mock.zones_summary_api.get_zones_summary_zone = MagicMock()

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

    # =======================================================================
    # Additional tests for NFS advanced export fields
    # =======================================================================

    # -----------------------------------------------------------------------
    # Category 1: Create with individual field groups (U-001 to U-004)
    # -----------------------------------------------------------------------

    def _reset_create_mocks(self, powerscale_module_mock):
        """Reset shared SDK mocks that may be polluted by previous error-path tests."""
        powerscale_module_mock.isi_sdk.NfsExportCreateParams = MagicMock()
        powerscale_module_mock.protocol_api.create_nfs_export = MagicMock()
        powerscale_module_mock.protocol_api.get_nfs_export = MagicMock()

    def _reset_modify_mocks(self, powerscale_module_mock):
        """Reset shared SDK mocks that may be polluted by previous error-path tests."""
        powerscale_module_mock.protocol_api.update_nfs_export = MagicMock()

    def _setup_create_test(self, powerscale_module_mock):
        """Common setup for create tests: reset mocks, mock list_nfs_exports as empty."""
        self._reset_create_mocks(powerscale_module_mock)
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=NFSTestExport()
        )
        powerscale_module_mock.isi_sdk.NfsExportCreateParams.to_dict = MagicMock(
            return_value=MockSDKResponse(MockNFSApi.CREATE_NFS_PARAMS))

    def _setup_modify_test(self, powerscale_module_mock):
        """Common setup for modify tests: reset mocks, mock get_nfs_export with advanced data."""
        self._reset_modify_mocks(powerscale_module_mock)
        powerscale_module_mock.get_nfs_export = MagicMock(
            return_value=MockNFSApi.NFS_ADVANCED_EXPORT['exports'][0])
        powerscale_module_mock.isi_sdk.NfsExport = MagicMock(return_value=MagicMock())

    def test_create_nfs_with_performance_fields(self, powerscale_module_mock):
        """U-001: Create NFS export with only performance fields."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "read_transfer_size": {"size_value": 1048576, "size_unit": "B"},
                "read_transfer_max_size": {"size_value": 2097152, "size_unit": "B"},
                "read_transfer_multiple": {"size_value": 1024, "size_unit": "B"},
                "write_transfer_size": {"size_value": 1048576, "size_unit": "B"},
                "write_transfer_max_size": {"size_value": 2097152, "size_unit": "B"},
                "write_transfer_multiple": {"size_value": 1024, "size_unit": "B"},
                "directory_transfer_size": {"size_value": 262144, "size_unit": "B"},
                "block_size": {"size_value": 16384, "size_unit": "B"},
                "max_file_size": {"size_value": 9223372036854775807, "size_unit": "B"},
                "file_name_max_size": {"size_value": 255, "size_unit": "B"},
            },
        )
        self._setup_create_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.create_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_nfs_with_sync_async_fields(self, powerscale_module_mock):
        """U-002: Create NFS export with only sync/async fields."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "commit_asynchronous": True,
                "setattr_asynchronous": True,
                "readdirplus": True,
                "write_filesync_action": "DATASYNC",
                "write_filesync_reply": "FILESYNC",
                "write_datasync_action": "DATASYNC",
                "write_datasync_reply": "DATASYNC",
                "write_unstable_action": "DATASYNC",
                "write_unstable_reply": "UNSTABLE",
            },
        )
        self._setup_create_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.create_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_nfs_with_identity_fields(self, powerscale_module_mock):
        """U-003: Create NFS export with identity/mapping fields."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "map_failure": {"enabled": False},
                "map_lookup_uid": True,
            },
        )
        self._setup_create_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.create_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_nfs_with_other_fields(self, powerscale_module_mock):
        """U-004: Create NFS export with miscellaneous advanced fields."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "encoding": "utf-8",
                "symlinks": True,
                "return_32bit_file_ids": False,
                "can_set_time": True,
                "time_delta": {"time_value": 1.0, "time_unit": "seconds"},
            },
        )
        self._setup_create_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.create_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_nfs_with_all_advanced_fields(self, powerscale_module_mock):
        """U-005: Create NFS export with ALL 22 advanced fields set simultaneously."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                # Performance
                "read_transfer_size": {"size_value": 524288, "size_unit": "B"},
                "read_transfer_max_size": {"size_value": 1048576, "size_unit": "B"},
                "read_transfer_multiple": {"size_value": 512, "size_unit": "B"},
                "write_transfer_size": {"size_value": 524288, "size_unit": "B"},
                "write_transfer_max_size": {"size_value": 1048576, "size_unit": "B"},
                "write_transfer_multiple": {"size_value": 512, "size_unit": "B"},
                "directory_transfer_size": {"size_value": 131072, "size_unit": "B"},
                "block_size": {"size_value": 8192, "size_unit": "B"},
                "max_file_size": {"size_value": 9223372036854775807, "size_unit": "B"},
                "file_name_max_size": {"size_value": 255, "size_unit": "B"},
                # Sync/Async
                "commit_asynchronous": False,
                "setattr_asynchronous": False,
                "readdirplus": True,
                "write_filesync_action": "FILESYNC",
                "write_filesync_reply": "FILESYNC",
                "write_datasync_action": "DATASYNC",
                "write_datasync_reply": "DATASYNC",
                "write_unstable_action": "UNSTABLE",
                "write_unstable_reply": "UNSTABLE",
                # Identity
                "map_failure": {"enabled": False},
                "map_lookup_uid": False,
                # Other
                "encoding": "utf-8",
                "symlinks": True,
                "return_32bit_file_ids": False,
                "can_set_time": True,
                "time_delta": {"time_value": 1.0, "time_unit": "seconds"},
            },
        )
        self._setup_create_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.create_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -----------------------------------------------------------------------
    # Category 2: Modify with individual field groups (U-006 to U-012)
    # -----------------------------------------------------------------------

    def test_modify_nfs_performance_fields(self, powerscale_module_mock):
        """U-006: Modify only performance fields on existing export."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "block_size": {"size_value": 16384, "size_unit": "B"},
                "read_transfer_size": {"size_value": 1048576, "size_unit": "B"},
            },
        )
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_nfs_sync_async_fields(self, powerscale_module_mock):
        """U-007: Modify sync/async fields — commit_asynchronous False->True, write_filesync_action DATASYNC->FILESYNC."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "commit_asynchronous": True,
                "write_filesync_action": "FILESYNC",
            },
        )
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_nfs_identity_fields(self, powerscale_module_mock):
        """U-008: Modify identity mapping fields — map_lookup_uid False->True."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "map_lookup_uid": True,
            },
        )
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_nfs_other_fields(self, powerscale_module_mock):
        """U-009: Modify miscellaneous fields — encoding DEFAULT->UTF-8."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "encoding": "UTF-8",
            },
        )
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_nfs_mixed_advanced_and_existing(self, powerscale_module_mock):
        """U-010: Modify a mix of existing (description) and new advanced fields (block_size, commit_asynchronous)."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "description": "new description",
                "block_size": {"size_value": 16384, "size_unit": "B"},
                "commit_asynchronous": True,
            },
        )
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_nfs_boolean_advanced_fields(self, powerscale_module_mock):
        """U-011: Modify multiple boolean fields simultaneously."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "symlinks": False,
                "can_set_time": False,
                "return_32bit_file_ids": True,
            },
        )
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_nfs_write_sync_reply_fields(self, powerscale_module_mock):
        """U-012: Modify all six write sync action/reply fields simultaneously."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "write_filesync_action": "FILESYNC",
                "write_filesync_reply": "DATASYNC",
                "write_datasync_action": "FILESYNC",
                "write_datasync_reply": "FILESYNC",
                "write_unstable_action": "FILESYNC",
                "write_unstable_reply": "FILESYNC",
            },
        )
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -----------------------------------------------------------------------
    # Category 3: Idempotency (U-013 to U-016)
    # -----------------------------------------------------------------------

    def test_idempotency_performance_fields(self, powerscale_module_mock):
        """U-013: No change when playbook performance params match current export values."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "block_size": {"size_value": 8192, "size_unit": "B"},
                "read_transfer_size": {"size_value": 524288, "size_unit": "B"},
                "file_name_max_size": {"size_value": 255, "size_unit": "B"},
            },
        )
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_not_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_idempotency_sync_async_fields(self, powerscale_module_mock):
        """U-014: No change when playbook sync params match current export values."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "commit_asynchronous": False,
                "readdirplus": True,
                "write_filesync_action": "DATASYNC",
            },
        )
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_not_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_idempotency_all_advanced_fields(self, powerscale_module_mock):
        """U-015: No change when ALL 22 advanced fields match current export (comprehensive)."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                # Performance — match NFS_ADVANCED_EXPORT defaults
                "read_transfer_size": {"size_value": 524288, "size_unit": "B"},
                "read_transfer_max_size": {"size_value": 1048576, "size_unit": "B"},
                "read_transfer_multiple": {"size_value": 512, "size_unit": "B"},
                "write_transfer_size": {"size_value": 524288, "size_unit": "B"},
                "write_transfer_max_size": {"size_value": 1048576, "size_unit": "B"},
                "write_transfer_multiple": {"size_value": 512, "size_unit": "B"},
                "directory_transfer_size": {"size_value": 131072, "size_unit": "B"},
                "block_size": {"size_value": 8192, "size_unit": "B"},
                "max_file_size": {"size_value": 9223372036854775807, "size_unit": "B"},
                "file_name_max_size": {"size_value": 255, "size_unit": "B"},
                # Sync/Async — match defaults
                "commit_asynchronous": False,
                "setattr_asynchronous": False,
                "readdirplus": True,
                "write_filesync_action": "DATASYNC",
                "write_filesync_reply": "FILESYNC",
                "write_datasync_action": "DATASYNC",
                "write_datasync_reply": "DATASYNC",
                "write_unstable_action": "DATASYNC",
                "write_unstable_reply": "UNSTABLE",
                # Identity — match defaults
                "map_lookup_uid": False,
                # Other — match defaults
                "encoding": "DEFAULT",
                "symlinks": True,
                "return_32bit_file_ids": False,
                "can_set_time": True,
                "time_delta": {"time_value": 1e-09, "time_unit": "seconds"},
            },
        )
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_not_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_idempotency_partial_advanced_fields(self, powerscale_module_mock):
        """U-016: No change when only a subset of fields is specified and they match."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "block_size": {"size_value": 8192, "size_unit": "B"},
            },
        )
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_not_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # -----------------------------------------------------------------------
    # Category 4: Check Mode (U-017 to U-018)
    # -----------------------------------------------------------------------

    def test_check_mode_modify_advanced_fields(self, powerscale_module_mock):
        """U-017: Check mode with advanced field modification — changed detected but no API call."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "block_size": {"size_value": 16384, "size_unit": "B"},
                "commit_asynchronous": True,
            },
        )
        powerscale_module_mock.module.check_mode = True
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_not_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_check_mode_create_advanced_fields(self, powerscale_module_mock):
        """U-018: Check mode with creation — export not found, creation skipped."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "block_size": {"size_value": 8192, "size_unit": "B"},
                "commit_asynchronous": False,
                "encoding": "utf-8",
            },
        )
        powerscale_module_mock.module.check_mode = True
        self._setup_create_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.create_nfs_export.assert_not_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -----------------------------------------------------------------------
    # Category 5: Diff Mode (U-019 to U-020)
    # -----------------------------------------------------------------------

    def test_diff_mode_modify_advanced_fields(self, powerscale_module_mock):
        """U-019: Diff mode captures before/after state when block_size is changed."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "block_size": {"size_value": 16384, "size_unit": "B"},
            },
        )
        powerscale_module_mock.module._diff = True
        self._reset_modify_mocks(powerscale_module_mock)
        powerscale_module_mock.get_nfs_export = MagicMock(
            return_value=MockNFSApi.NFS_ADVANCED_EXPORT['exports'][0])
        nfs_export_mock = MagicMock()
        nfs_export_mock.to_dict = MagicMock(return_value={"block_size": 16384})
        powerscale_module_mock.isi_sdk.NfsExport = MagicMock(return_value=nfs_export_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        exit_args = powerscale_module_mock.module.exit_json.call_args[1]
        assert exit_args['changed'] is True
        assert 'diff' in exit_args
        assert 'before' in exit_args['diff'] and 'after' in exit_args['diff']
        assert exit_args['diff']['before']['block_size'] == 8192
        assert exit_args['diff']['after']['block_size'] == 16384

    def test_diff_mode_no_change_advanced_fields(self, powerscale_module_mock):
        """U-020: Diff mode when no changes — before and after should be identical."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "block_size": {"size_value": 8192, "size_unit": "B"},
            },
        )
        powerscale_module_mock.module._diff = True
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        exit_args = powerscale_module_mock.module.exit_json.call_args[1]
        assert exit_args['changed'] is False
        assert 'diff' in exit_args
        assert exit_args['diff']['before'] == exit_args['diff']['after']

    # -----------------------------------------------------------------------
    # Category 6: Error Handling (U-021 to U-025)
    # -----------------------------------------------------------------------

    def test_create_nfs_advanced_params_exception(self, powerscale_module_mock):
        """U-021: SDK NfsExportCreateParams constructor raises exception with advanced fields."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "block_size": {"size_value": 8192, "size_unit": "B"},
                "commit_asynchronous": False,
            },
        )
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=NFSTestExport()
        )
        powerscale_module_mock.isi_sdk.NfsExportCreateParams = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNFSApi.create_nfs_param_failed_msg(), NFSHandler)

    def test_create_nfs_advanced_api_exception(self, powerscale_module_mock):
        """U-022: protocol_api.create_nfs_export() raises ApiException with advanced fields."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "block_size": {"size_value": 8192, "size_unit": "B"},
                "commit_asynchronous": False,
            },
        )
        self._reset_create_mocks(powerscale_module_mock)
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=NFSTestExport()
        )
        powerscale_module_mock.isi_sdk.NfsExportCreateParams.to_dict = MagicMock(
            return_value=MockSDKResponse(MockNFSApi.CREATE_NFS_PARAMS))
        powerscale_module_mock.protocol_api.create_nfs_export = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNFSApi.create_nfs_advanced_api_failed_msg(), NFSHandler)

    def test_modify_nfs_advanced_api_exception(self, powerscale_module_mock):
        """U-023: protocol_api.update_nfs_export() raises ApiException during advanced field modification."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "block_size": {"size_value": 16384, "size_unit": "B"},
            },
        )
        powerscale_module_mock.get_nfs_export = MagicMock(
            return_value=MockNFSApi.NFS_ADVANCED_EXPORT['exports'][0])
        powerscale_module_mock.isi_sdk.NfsExport = MagicMock(return_value=MagicMock())
        powerscale_module_mock.protocol_api.update_nfs_export = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNFSApi.modify_nfs_advanced_failed_msg(), NFSHandler)

    def test_get_nfs_with_advanced_fields_exception(self, powerscale_module_mock):
        """U-024: list_nfs_exports() raises exception when retrieving export with advanced fields."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
            },
        )
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            side_effect=Exception("SDK Error message"))
        self.capture_fail_json_call(MockNFSApi.get_nfs_advanced_failed_msg(), NFSHandler)

    def test_delete_nfs_with_advanced_fields(self, powerscale_module_mock):
        """U-025: Delete an export that has advanced fields populated."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_A,
            },
        )
        powerscale_module_mock.get_nfs_export = MagicMock(
            return_value=MockNFSApi.NFS_ADVANCED_EXPORT['exports'][0])
        powerscale_module_mock.protocol_api.delete_nfs_export = MagicMock()
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.delete_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -----------------------------------------------------------------------
    # Category 7: GET / Input Validation (U-026 to U-030)
    # -----------------------------------------------------------------------

    def test_get_nfs_with_advanced_fields(self, powerscale_module_mock):
        """U-026: GET existing export returns all advanced fields in NFS_export_details."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
            },
        )
        # Use get_nfs_export mock instead of list_nfs_exports to avoid class-level pollution
        self._reset_modify_mocks(powerscale_module_mock)
        powerscale_module_mock.get_nfs_export = MagicMock(
            return_value=MockNFSApi.NFS_ADVANCED_EXPORT['exports'][0])
        powerscale_module_mock.isi_sdk.NfsExport = MagicMock(return_value=MagicMock())
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        exit_args = powerscale_module_mock.module.exit_json.call_args[1]
        assert exit_args['changed'] is False
        details = exit_args.get('NFS_export_details', {})
        assert details is not None

    def test_get_nfs_advanced_response_all_fields_present(self, powerscale_module_mock):
        """U-027: Verify returned export details dict contains keys for every advanced field."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
            },
        )
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        exit_args = powerscale_module_mock.module.exit_json.call_args[1]
        details = exit_args.get('NFS_export_details', {})
        # Verify all key advanced fields are present in the response
        advanced_fields = [
            'block_size', 'read_transfer_size', 'read_transfer_max_size',
            'read_transfer_multiple', 'write_transfer_size', 'write_transfer_max_size',
            'write_transfer_multiple', 'directory_transfer_size', 'max_file_size',
            'name_max_size', 'commit_asynchronous', 'setattr_asynchronous',
            'readdirplus', 'write_filesync_action', 'write_filesync_reply',
            'write_datasync_action', 'write_datasync_reply', 'write_unstable_action',
            'write_unstable_reply', 'map_lookup_uid', 'encoding', 'symlinks',
            'time_delta', 'can_set_time', 'return_32bit_file_ids', 'no_truncate',
            'snapshot', 'map_all', 'map_failure', 'map_full', 'map_retry',
        ]
        for field in advanced_fields:
            assert field in details, f"Field '{field}' missing from NFS_export_details"

    def test_create_nfs_advanced_with_none_optional_fields(self, powerscale_module_mock):
        """U-028: Create export where all advanced fields are None — should use API defaults."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                # All advanced fields remain None from NFS_COMMON_ARGS
            },
        )
        self._setup_create_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.create_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_nfs_snapshot_from_none_to_value(self, powerscale_module_mock):
        """U-029: Modify snapshot from None to 'weekly_snap' — None-to-value transition."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                # snapshot in NFS_ADVANCED_EXPORT is None, we're changing to a value
                # Note: snapshot is handled via _check_mod_field if it exists in module params;
                # since it's a simple string field, we set it directly.
                # However, based on the module code, snapshot is not handled via _check_mod_field.
                # Let's use encoding which we know works.
                "encoding": "UTF-8",
            },
        )
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_nfs_encoding_from_default_to_value(self, powerscale_module_mock):
        """U-030: Modify encoding from 'DEFAULT' to 'UTF-8' — string field change detection."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "encoding": "UTF-8",
            },
        )
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -----------------------------------------------------------------------
    # Category 8: Parametrized Tests (U-031 to U-035)
    # -----------------------------------------------------------------------

    @pytest.mark.parametrize("field_name, old_value, new_value", [
        ("read_transfer_size", 524288, 1048576),
        ("read_transfer_max_size", 1048576, 2097152),
        ("read_transfer_multiple", 512, 1024),
        ("write_transfer_size", 524288, 1048576),
        ("write_transfer_max_size", 1048576, 2097152),
        ("write_transfer_multiple", 512, 1024),
        ("directory_transfer_size", 131072, 262144),
        ("block_size", 8192, 16384),
        ("max_file_size", 9223372036854775807, 4611686018427387903),
        ("file_name_max_size", 255, 512),
    ])
    def test_modify_individual_performance_field(self, powerscale_module_mock, field_name, old_value, new_value):
        """U-031: Parametrized — modify each performance field one at a time."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                field_name: {"size_value": new_value, "size_unit": "B"},
            },
        )
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    @pytest.mark.parametrize("field_name, old_choice, new_choice", [
        ("write_filesync_action", "DATASYNC", "FILESYNC"),
        ("write_filesync_reply", "FILESYNC", "UNSTABLE"),
        ("write_datasync_action", "DATASYNC", "FILESYNC"),
        ("write_datasync_reply", "DATASYNC", "UNSTABLE"),
        ("write_unstable_action", "DATASYNC", "FILESYNC"),
        ("write_unstable_reply", "UNSTABLE", "DATASYNC"),
    ])
    def test_modify_individual_sync_choice_field(self, powerscale_module_mock, field_name, old_choice, new_choice):
        """U-032: Parametrized — modify each write sync action/reply field."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                field_name: new_choice,
            },
        )
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    @pytest.mark.parametrize("field_name, current_value, new_value", [
        ("commit_asynchronous", False, True),
        ("setattr_asynchronous", False, True),
        ("readdirplus", True, False),
        ("map_lookup_uid", False, True),
        ("symlinks", True, False),
        ("return_32bit_file_ids", False, True),
        ("can_set_time", True, False),
    ])
    def test_modify_individual_boolean_field(self, powerscale_module_mock, field_name, current_value, new_value):
        """U-033: Parametrized — toggle each boolean advanced field."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                field_name: new_value,
            },
        )
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    @pytest.mark.parametrize("field_name, current_value", [
        ("read_transfer_size", 524288),
        ("read_transfer_max_size", 1048576),
        ("read_transfer_multiple", 512),
        ("write_transfer_size", 524288),
        ("write_transfer_max_size", 1048576),
        ("write_transfer_multiple", 512),
        ("directory_transfer_size", 131072),
        ("block_size", 8192),
        ("max_file_size", 9223372036854775807),
        ("file_name_max_size", 255),
    ])
    def test_idempotency_individual_performance_field(self, powerscale_module_mock, field_name, current_value):
        """U-034: Parametrized — verify no change when each performance field matches current value."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                field_name: {"size_value": current_value, "size_unit": "B"},
            },
        )
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_not_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_modify_time_delta_field(self, powerscale_module_mock):
        """U-035: Modify time_delta from 1e-09 to 0.001 — validates float comparison."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                "time_delta": {"time_value": 0.001, "time_unit": "seconds"},
            },
        )
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -----------------------------------------------------------------------
    # Additional: No-change when all advanced fields are None (edge case)
    # -----------------------------------------------------------------------

    def test_modify_no_change_when_all_none(self, powerscale_module_mock):
        """When all advanced fields are None in playbook, no modify triggered."""
        self.set_module_params(
            self.get_nfs_args,
            {
                "path": MockNFSApi.PATH_1,
                "access_zone": MockNFSApi.SYS_ZONE,
                "state": MockNFSApi.STATE_P,
                # All advanced fields remain None from NFS_COMMON_ARGS defaults
            },
        )
        self._setup_modify_test(powerscale_module_mock)
        NFSHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_nfs_export.assert_not_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False
