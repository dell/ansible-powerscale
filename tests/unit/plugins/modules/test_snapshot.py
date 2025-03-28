# Copyright: (c) 2025 Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Snapshot module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import patch, MagicMock
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils


from ansible_collections.dellemc.powerscale.plugins.modules.snapshot import Snapshot
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_snapshot_api as MockSnapshotApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase


class TestSnapshot(PowerScaleUnitBase):
    get_snapshot_args = {
        "snapshot_name": None,
        "path": None,
        "access_zone": 'System',
        "new_snapshot_name": None,
        "expiration_timestamp": None,
        "desired_retention": None,
        "retention_unit": None,
        "alias": None,
        "state": None
    }

    snapshot_name_1 = "ansible_test_snapshot"

    @pytest.fixture
    def module_object(self, mocker):
        return Snapshot

    def test_get_snapshot_by_name_response(self, powerscale_module_mock):
        self.get_snapshot_args.update({"snapshot_name": self.snapshot_name_1,
                                       "state": "present"})
        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.snapshot_api.get_snapshot_snapshot = MagicMock(
            return_value=MockSDKResponse(MockSnapshotApi.SNAPSHOT))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.snapshot_api.get_snapshot_snapshot.assert_called()

    def test_get_snapshot_wo_name_exception(self, powerscale_module_mock):
        self.get_snapshot_args.update({"state": "present"})
        powerscale_module_mock.module.params = self.get_snapshot_args
        self.capture_fail_json_call(
            MockSnapshotApi.get_snapshot_wo_name_failed_msg(), invoke_perform_module=True)

    def test_get_snapshot_exception(self, powerscale_module_mock):
        self.get_snapshot_args.update({"snapshot_name": self.snapshot_name_1,
                                       "state": "present"})
        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.snapshot_api.get_snapshot_snapshot = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(
            MockSnapshotApi.get_snapshot_failed_msg(), invoke_perform_module=True)

    def test_create_snapshot_response(self, powerscale_module_mock):
        self.get_snapshot_args.update({"path": "/ifs/ansible_test_snapshot",
                                       "access_zone": "sample_zone",
                                       "snapshot_name": "ansible_test_snapshot",
                                       "desired_retention": "2",
                                       "retention_unit": "days",
                                       "alias": "snap_alias_1",
                                       "state": "present"})
        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.isi_sdk.SnapshotSnapshotCreateParams = MagicMock(
            return_value=MockSDKResponse(MockSnapshotApi.CREATE_SNAPSHOT_PARAMS))
        with patch.object(powerscale_module_mock.snapshot_api,
                          'get_snapshot_snapshot',
                          side_effect=MockApiException(404)):
            powerscale_module_mock.perform_module_operation()
            powerscale_module_mock.snapshot_api.create_snapshot_snapshot.assert_called()
            assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_snapshot_wo_retention_unit_response(self, powerscale_module_mock):
        self.get_snapshot_args.update({"path": "/ifs/ansible_test_snapshot",
                                       "access_zone": "sample_zone",
                                       "snapshot_name": "ansible_test_snapshot",
                                       "desired_retention": "2",
                                       "alias": "snap_alias_1",
                                       "state": "present"})
        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.snapshot_api.get_snapshot_snapshot = MagicMock(
            return_value=None)
        powerscale_module_mock.isi_sdk.SnapshotSnapshotCreateParams = MagicMock(
            return_value=MockSDKResponse(MockSnapshotApi.CREATE_SNAPSHOT_PARAMS))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.snapshot_api.create_snapshot_snapshot.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_snapshot_retention_unit_hours_response(self, powerscale_module_mock):
        self.get_snapshot_args.update({"path": "/ifs/ansible_test_snapshot",
                                       "access_zone": "sample_zone",
                                       "snapshot_name": "ansible_test_snapshot",
                                       "desired_retention": "3",
                                       "retention_unit": "hours",
                                       "alias": "snap_alias_1",
                                       "state": "present"})
        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.snapshot_api.get_snapshot_snapshot = MagicMock(
            return_value=None)
        powerscale_module_mock.isi_sdk.SnapshotSnapshotCreateParams = MagicMock(
            return_value=MockSDKResponse(MockSnapshotApi.CREATE_SNAPSHOT_PARAMS))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.snapshot_api.create_snapshot_snapshot.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_snapshot_exception(self, powerscale_module_mock):
        self.get_snapshot_args.update({"path": "/ifs/ansible_test_snapshot",
                                       "access_zone": "sample_zone",
                                       "snapshot_name": "ansible_test_snapshot",
                                       "desired_retention": "2",
                                       "retention_unit": "days",
                                       "alias": "snap_alias_1",
                                       "state": "present"})
        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.snapshot_api.get_snapshot_snapshot = MagicMock(
            return_value=None)
        powerscale_module_mock.isi_sdk.SnapshotSnapshotCreateParams = MagicMock(
            return_value=MockSDKResponse(MockSnapshotApi.CREATE_SNAPSHOT_PARAMS))
        powerscale_module_mock.snapshot_api.create_snapshot_snapshot = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(
            MockSnapshotApi.create_snapshot_failed_msg(), invoke_perform_module=True)

    def test_create_snapshot_wo_desired_retention(self, powerscale_module_mock):
        self.set_module_params(self.get_snapshot_args, {"path": "/ifs/ansible_test_snapshot",
                                                        "access_zone": "sample_zone",
                                                        "snapshot_name": "ansible_test_snapshot",
                                                        "desired_retention": "none",
                                                        "state": "present"})
        powerscale_module_mock.snapshot_api.get_snapshot_snapshot = MagicMock(
            return_value=None)
        self.powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_snapshot_invalid_desired_retention_exception(self, powerscale_module_mock):
        self.get_snapshot_args.update({"path": "/ifs/ansible_test_snapshot",
                                       "access_zone": "sample_zone",
                                       "snapshot_name": "ansible_test_snapshot",
                                       "desired_retention": "string",
                                       "state": "present"})
        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.snapshot_api.get_snapshot_snapshot = MagicMock(
            return_value=None)
        self.capture_fail_json_call(
            MockSnapshotApi.create_snapshot_invalid_desired_retention_failed_msg(), invoke_perform_module=True)

    def test_create_snapshot_wo_retention_exception(self, powerscale_module_mock):
        self.get_snapshot_args.update({"path": "/ifs/ansible_test_snapshot",
                                       "access_zone": "sample_zone",
                                       "snapshot_name": "ansible_test_snapshot",
                                       "state": "present"})
        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.snapshot_api.get_snapshot_snapshot = MagicMock(
            return_value=None)
        self.capture_fail_json_call(
            MockSnapshotApi.create_snapshot_wo_retention_failed_msg(), invoke_perform_module=True)

    def test_create_snapshot_with_new_name_exception(self, powerscale_module_mock):
        self.get_snapshot_args.update({"path": "/ifs/ansible_test_snapshot",
                                       "access_zone": "sample_zone",
                                       "snapshot_name": "ansible_test_snapshot",
                                       "desired_retention": "2",
                                       "retention_unit": "days",
                                       "alias": "snap_alias_1",
                                       "new_snapshot_name": "new_name",
                                       "state": "present"})
        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.snapshot_api.get_snapshot_snapshot = MagicMock(
            return_value=None)
        self.capture_fail_json_call(
            MockSnapshotApi.create_snapshot_with_new_name_failed_msg(), invoke_perform_module=True)

    def test_create_snapshot_without_path_exception(self, powerscale_module_mock):
        self.get_snapshot_args.update({"access_zone": "sample_zone",
                                       "snapshot_name": "ansible_test_snapshot",
                                       "desired_retention": "2",
                                       "retention_unit": "days",
                                       "alias": "snap_alias_1",
                                       "state": "present"})
        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.snapshot_api.get_snapshot_snapshot = MagicMock(
            return_value=None)
        self.capture_fail_json_call(
            MockSnapshotApi.create_snapshot_without_path_failed_msg(), invoke_perform_module=True)

    def test_create_snapshot_invalid_access_zone_exception(self, powerscale_module_mock):
        self.get_snapshot_args.update({"path": "/ifs/ansible_test_snapshot",
                                       "access_zone": "invalid_zone",
                                       "snapshot_name": "ansible_test_snapshot",
                                       "desired_retention": "2",
                                       "retention_unit": "days",
                                       "alias": "snap_alias_1",
                                       "state": "present"})
        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.snapshot_api.get_snapshot_snapshot = MagicMock(
            return_value=None)
        powerscale_module_mock.zone_summary_api.get_zones_summary_zone = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(
            MockSnapshotApi.invalid_access_zone_failed_msg(),
            invoke_perform_module=True)

    def test_rename_snapshot_response(self, powerscale_module_mock):
        self.get_snapshot_args.update({"snapshot_name": self.snapshot_name_1,
                                       "new_snapshot_name": "renamed_snapshot_name_1",
                                       "state": "present"})

        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.snapshot_api.get_snapshot_snapshot.to_dict = MagicMock(
            return_value=MockSnapshotApi.SNAPSHOT)
        powerscale_module_mock.isi_sdk.SnapshotSnapshot = MagicMock(
            return_value=MockSDKResponse(MockSnapshotApi.RENAME_SNAPSHOT_PARAMS))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.snapshot_api.update_snapshot_snapshot.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_rename_snapshot_same_name_response(self, powerscale_module_mock):
        self.get_snapshot_args.update({"snapshot_name": self.snapshot_name_1,
                                       "new_snapshot_name": self.snapshot_name_1,
                                       "state": "present"})

        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.get_filesystem_snapshot_details = MagicMock(
            return_value=MockSnapshotApi.SNAPSHOT)
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_rename_snapshot_exception(self, powerscale_module_mock):
        self.get_snapshot_args.update({"snapshot_name": self.snapshot_name_1,
                                       "new_snapshot_name": "renamed_snapshot_name_1",
                                       "state": "present"})

        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.snapshot_api.get_snapshot_snapshot.to_dict = MagicMock(
            return_value=MockSDKResponse(MockSnapshotApi.SNAPSHOT))
        powerscale_module_mock.isi_sdk.SnapshotSnapshot = MagicMock(
            return_value=MockSDKResponse(MockSnapshotApi.RENAME_SNAPSHOT_PARAMS))
        powerscale_module_mock.snapshot_api.update_snapshot_snapshot = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(
            MockSnapshotApi.rename_snapshot_failed_msg(), invoke_perform_module=True)

    def test_get_snapshot_alias_response(self, powerscale_module_mock):
        self.get_snapshot_args.update({"snapshot_name": self.snapshot_name_1,
                                       "alias": "alias_name_2",
                                       "state": "present"})

        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.get_filesystem_snapshot_details = MagicMock(
            return_value=MockSnapshotApi.SNAPSHOT)
        powerscale_module_mock.snapshot_api.list_snapshot_snapshots.to_dict = MagicMock(
            return_value=MockSnapshotApi.ALIAS)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.snapshot_api.list_snapshot_snapshots.assert_called()

    def test_get_snapshot_alias_exception(self, powerscale_module_mock):
        self.get_snapshot_args.update({"snapshot_name": self.snapshot_name_1,
                                       "alias": "alias_name_2",
                                       "state": "present"})

        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.get_filesystem_snapshot_details = MagicMock(
            return_value=MockSnapshotApi.SNAPSHOT)
        powerscale_module_mock.snapshot_api.list_snapshot_snapshots = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(
            MockSnapshotApi.get_snapshot_alias_failed_msg(), invoke_perform_module=True)

    def test_modify_snapshot_expiration_timestamp_response(self, powerscale_module_mock):
        self.get_snapshot_args.update({"snapshot_name": self.snapshot_name_1,
                                       "expiration_timestamp": '2025-01-18T11:50:20Z',
                                       "state": "present"})

        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.get_filesystem_snapshot_details = MagicMock(
            return_value=MockSnapshotApi.SNAPSHOT)
        powerscale_module_mock.isi_sdk.SnapshotSnapshot = MagicMock(
            return_value=MockSDKResponse(MockSnapshotApi.MODIFY_SNAPSHOT_PARAMS))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.snapshot_api.update_snapshot_snapshot.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_snapshot_expiration_timestamp_wo_expires_response(self, powerscale_module_mock):
        self.get_snapshot_args.update({"snapshot_name": self.snapshot_name_1,
                                       "expiration_timestamp": '2025-01-18T11:50:20Z',
                                       "state": "present"})

        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.get_filesystem_snapshot_details = MagicMock(
            return_value=MockSnapshotApi.SNAPSHOT_WO_EXPIRES)
        powerscale_module_mock.isi_sdk.SnapshotSnapshot = MagicMock(
            return_value=MockSDKResponse(MockSnapshotApi.MODIFY_SNAPSHOT_PARAMS))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.snapshot_api.update_snapshot_snapshot.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_non_existing_path_exception(self, powerscale_module_mock):
        self.get_snapshot_args.update({"snapshot_name": self.snapshot_name_1,
                                       "path": "/ifs/non_existing_path",
                                       "expiration_timestamp": '2025-01-18T11:50:20Z',
                                       "state": "present"})

        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.get_filesystem_snapshot_details = MagicMock(
            return_value=MockSnapshotApi.SNAPSHOT)
        self.capture_fail_json_call(
            MockSnapshotApi.modify_non_existing_path_failed_msg(), invoke_perform_module=True)

    def test_modify_snapshot_expiration_timestamp_exception(self, powerscale_module_mock):
        self.get_snapshot_args.update({"snapshot_name": self.snapshot_name_1,
                                       "expiration_timestamp": '2025-01-18T11:50:20Z',
                                       "state": "present"})

        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.get_filesystem_snapshot_details = MagicMock(
            return_value=MockSnapshotApi.SNAPSHOT)
        powerscale_module_mock.isi_sdk.SnapshotSnapshot = MagicMock(
            return_value=MockSDKResponse(MockSnapshotApi.MODIFY_SNAPSHOT_PARAMS))
        powerscale_module_mock.snapshot_api.update_snapshot_snapshot = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(
            MockSnapshotApi.modify_snapshot_failed_msg(), invoke_perform_module=True)

    def test_modify_snapshot_response(self, powerscale_module_mock):
        self.get_snapshot_args.update({"snapshot_name": self.snapshot_name_1,
                                       "desired_retention": "2",
                                       "retention_unit": "days",
                                       "state": "present"})

        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.get_filesystem_snapshot_details = MagicMock(
            return_value=MockSnapshotApi.SNAPSHOT)
        powerscale_module_mock.isi_sdk.SnapshotSnapshot = MagicMock(
            return_value=MockSDKResponse(MockSnapshotApi.MODIFY_SNAPSHOT_PARAMS))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.snapshot_api.update_snapshot_snapshot.assert_called()

    def test_modify_snapshot_no_retention_unit_response(self, powerscale_module_mock):
        self.get_snapshot_args.update({"snapshot_name": self.snapshot_name_1,
                                       "desired_retention": "2",
                                       "state": "present"})

        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.get_filesystem_snapshot_details = MagicMock(
            return_value=MockSnapshotApi.SNAPSHOT)
        powerscale_module_mock.isi_sdk.SnapshotSnapshot = MagicMock(
            return_value=MockSDKResponse(MockSnapshotApi.MODIFY_SNAPSHOT_PARAMS))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.snapshot_api.update_snapshot_snapshot.assert_called()

    def test_modify_snapshot_retention_unit_hours_response(self, powerscale_module_mock):
        self.get_snapshot_args.update({"snapshot_name": self.snapshot_name_1,
                                       "desired_retention": "2",
                                       "retention_unit": "hours",
                                       "state": "present"})

        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.get_filesystem_snapshot_details = MagicMock(
            return_value=MockSnapshotApi.SNAPSHOT)
        powerscale_module_mock.isi_sdk.SnapshotSnapshot = MagicMock(
            return_value=MockSDKResponse(MockSnapshotApi.MODIFY_SNAPSHOT_PARAMS))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.snapshot_api.update_snapshot_snapshot.assert_called()

    def test_modify_snapshot_exception(self, powerscale_module_mock):
        self.get_snapshot_args.update({"snapshot_name": self.snapshot_name_1,
                                       "desired_retention": "2",
                                       "retention_unit": "days",
                                       "state": "present"})

        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.get_filesystem_snapshot_details = MagicMock(
            return_value=MockSnapshotApi.SNAPSHOT)
        powerscale_module_mock.isi_sdk.SnapshotSnapshot = MagicMock(
            return_value=MockSDKResponse(MockSnapshotApi.MODIFY_SNAPSHOT_PARAMS))
        powerscale_module_mock.snapshot_api.update_snapshot_snapshot = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(
            MockSnapshotApi.modify_snapshot_failed_msg(), invoke_perform_module=True)

    def test_modify_snapshot_wo_desired_retention_exception(self, powerscale_module_mock):
        self.get_snapshot_args.update({"snapshot_name": self.snapshot_name_1,
                                       "retention_unit": "days",
                                       "state": "present"})

        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.get_filesystem_snapshot_details = MagicMock(
            return_value=MockSnapshotApi.SNAPSHOT)
        powerscale_module_mock.isi_sdk.SnapshotSnapshot = MagicMock(
            return_value=MockSDKResponse(MockSnapshotApi.MODIFY_SNAPSHOT_PARAMS))
        self.capture_fail_json_call(
            MockSnapshotApi.modify_snapshot_wo_desired_retention_failed_msg(), invoke_perform_module=True)

    def test_delete_snapshot_by_name_response(self, powerscale_module_mock):
        self.get_snapshot_args.update({"snapshot_name": self.snapshot_name_1,
                                       "state": "absent"})
        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.get_filesystem_snapshot_details = MagicMock(
            return_value=MockSnapshotApi.SNAPSHOT)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.snapshot_api.delete_snapshot_snapshot.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_snapshot_exception(self, powerscale_module_mock):
        self.get_snapshot_args.update({"snapshot_name": self.snapshot_name_1,
                                       "state": "absent"})
        powerscale_module_mock.module.params = self.get_snapshot_args
        powerscale_module_mock.get_filesystem_snapshot_details = MagicMock(
            return_value=MockSnapshotApi.SNAPSHOT)
        powerscale_module_mock.snapshot_api.delete_snapshot_snapshot = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(
            MockSnapshotApi.delete_snapshot_exception_failed_msg(), invoke_perform_module=True)
