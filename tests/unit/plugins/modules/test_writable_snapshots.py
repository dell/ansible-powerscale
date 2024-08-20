# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Alert Setting module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils
from ansible_collections.dellemc.powerscale.plugins.modules.writable_snapshots import WritableSnapshot, WritableSnapshotHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_writable_snapshots_api \
    import MockWritableSanpshotsApi


class TestWritableSnapshot(PowerScaleUnitBase):
    writable_snapshot_args = MockWritableSanpshotsApi.WS_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return WritableSnapshot

    def test_create_writable_snapshot_check_mode(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.writable_snapshot_args,
                               MockWritableSanpshotsApi.WS_CREATE_ARGS
                               )
        powerscale_module_mock.check_mode = True
        powerscale_module_mock.segregate_snapshots = MagicMock(
            return_value=(MockWritableSanpshotsApi.WS_CREATE_ARGS["writable_snapshots"], [], []))
        powerscale_module_mock.get_writable_snapshot = MagicMock(return_value=(False, []))
        WritableSnapshotHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_writable_snapshot_with_id(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.writable_snapshot_args,
                               MockWritableSanpshotsApi.WS_CREATE_ARGS
                               )
        powerscale_module_mock.check_mode = False
        powerscale_module_mock._diff = True
        powerscale_module_mock.get_writable_snapshot = MagicMock(return_value=(False, []))
        WritableSnapshotHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_writable_snapshot_with_id_idempotence_mode(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.writable_snapshot_args,
                               MockWritableSanpshotsApi.WS_CREATE_ARGS
                               )
        powerscale_module_mock.check_mode = False
        WritableSnapshotHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_writable_snapshot_idempotence_mode(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.writable_snapshot_args,
                               MockWritableSanpshotsApi.WS_CREATE_ARGS_STR
                               )
        powerscale_module_mock.check_mode = False
        WritableSnapshotHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_writable_snapshot_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.writable_snapshot_args,
                               MockWritableSanpshotsApi.WS_CREATE_ARGS
                               )
        powerscale_module_mock.check_mode = False
        powerscale_module_mock.determine_error = MagicMock()
        powerscale_module_mock.get_writable_snapshot = MagicMock(return_value=(False, []))
        powerscale_module_mock.snapshot_api.create_snapshot_writable_item = MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockWritableSanpshotsApi.get_writeable_snpshots_error_response("create_exception"),
                                    powerscale_module_mock, WritableSnapshotHandler)

    def test_delete_writable_snapshot_check_mode(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.writable_snapshot_args,
                               MockWritableSanpshotsApi.WS_DELETE_ARGS)
        powerscale_module_mock.check_mode = True
        powerscale_module_mock.get_writable_snapshot = MagicMock(return_value=(True, []))
        WritableSnapshotHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_writable_snapshot(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.writable_snapshot_args,
                               MockWritableSanpshotsApi.WS_DELETE_ARGS
                               )
        powerscale_module_mock.check_mode = False
        powerscale_module_mock.get_writable_snapshot = MagicMock(
            return_value=(True, MockWritableSanpshotsApi.WS_DELETE_ARGS["writable_snapshots"]))
        WritableSnapshotHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_writable_snapshot_idempotence_mode(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.writable_snapshot_args,
                               MockWritableSanpshotsApi.WS_DELETE_ARGS
                               )
        powerscale_module_mock.check_mode = False
        powerscale_module_mock.get_writable_snapshot = MagicMock(return_value=(False, []))
        WritableSnapshotHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_delete_writable_snapshot_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.writable_snapshot_args,
                               MockWritableSanpshotsApi.WS_DELETE_ARGS
                               )
        powerscale_module_mock.check_mode = False
        powerscale_module_mock.snapshot_api.delete_snapshot_writable_wspath = MagicMock(side_effect=Exception)
        self.capture_fail_json_call(MockWritableSanpshotsApi.get_writeable_snpshots_error_response("delete_exception"),
                                    powerscale_module_mock, WritableSnapshotHandler)

    def test_get_writable_snapshot_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.writable_snapshot_args,
                               MockWritableSanpshotsApi.WS_DELETE_ARGS
                               )
        powerscale_module_mock.snapshot_api.get_snapshot_writable_wspath = MagicMock(side_effect=Exception)
        self.capture_fail_json_call(MockWritableSanpshotsApi.get_writeable_snpshots_error_response("delete_exception"),
                                    powerscale_module_mock, WritableSnapshotHandler)

    def test_invalid_writable_snapshot(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.writable_snapshot_args,
                               MockWritableSanpshotsApi.WS_INVALID_DSTPATH_ARGS
                               )
        powerscale_module_mock.check_mode = False
        powerscale_module_mock.validate_src_snap = MagicMock(return_value=(False))
        self.capture_fail_json_call(MockWritableSanpshotsApi.get_writeable_snpshots_error_response("invalid_dstpath"),
                                    powerscale_module_mock, WritableSnapshotHandler)
