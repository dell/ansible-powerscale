# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Alert Setting module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils
from ansible_collections.dellemc.powerscale.plugins.modules.writable_snapshot import WritableSnapshot, WritableSnapshotHandler
# from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_alert_management_api import MockAlertRuleApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase


class TestWritableSnapshot(PowerScaleUnitBase):

    writable_snapshot_args = {"onefs_host": "XX.XX.XX.XX",
                              "port_no": "8080",
                              "verify_ssl": "false",
                              "api_user": "root",
                              "api_password": "pancake"
                              }

    @pytest.fixture
    def module_object(self):
        return WritableSnapshot

    def test_create_writable_snapshot_check_mode(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.writable_snapshot_args,
                               {"writable_snapshot": [{"src_snap": 2, "dst_path": "/ifs/ansible/", "state": "present"}]})
        powerscale_module_mock.check_mode = True
        powerscale_module_mock.segregate_snapshots = MagicMock(
            return_value=([{"src_snap": 2, "dst_path": "/ifs/ansible/", "state": "present"}], [], []))
        powerscale_module_mock.get_writable_snapshot = MagicMock(return_value=(False, []))
        WritableSnapshotHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_writable_snapshot(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.writable_snapshot_args,
                               {"writable_snapshot": [{"src_snap": 2, "dst_path": "/ifs/ansible/", "state": "present"}]})
        powerscale_module_mock.check_mode = False
        powerscale_module_mock.get_writable_snapshot = MagicMock(return_value=(False, []))
        WritableSnapshotHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_writable_snapshot_idempotence_mode(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.writable_snapshot_args,
                               {"writable_snapshot": [{"src_snap": 2, "dst_path": "/ifs/ansible/", "state": "present"}]})
        powerscale_module_mock.check_mode = False
        powerscale_module_mock.get_writable_snapshot = MagicMock(
            return_value=(True, [{"src_snap": 2, "dst_path": "/ifs/ansible/"}]))
        WritableSnapshotHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_create_writable_snapshot_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.writable_snapshot_args,
                               {"writable_snapshot": [{"src_snap": 2, "dst_path": "/ifs/ansible/", "state": "present"}]})
        powerscale_module_mock.check_mode = False
        powerscale_module_mock.determine_error = MagicMock()
        powerscale_module_mock.get_writable_snapshot = MagicMock(return_value=(False, []))
        powerscale_module_mock.snapshot_api.create_snapshot_writable_item = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call("Failed to create writable snapshot", powerscale_module_mock, WritableSnapshotHandler)

    def test_delete_writable_snapshot_check_mode(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.writable_snapshot_args,
                               {"writable_snapshot": [{"src_snap": 2, "dst_path": "/ifs/ansible/", "state": "absent"}]})
        powerscale_module_mock.check_mode = True
        powerscale_module_mock.get_writable_snapshot = MagicMock(return_value=(True, []))
        WritableSnapshotHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_writable_snapshot(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.writable_snapshot_args,
                               {"writable_snapshot": [{"src_snap": 2, "dst_path": "/ifs/ansible/", "state": "absent"}]})
        powerscale_module_mock.check_mode = False
        powerscale_module_mock.get_writable_snapshot = MagicMock(
            return_value=(True, [{"src_snap": 2, "dst_path": "/ifs/ansible/"}]))
        WritableSnapshotHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_writable_snapshot_idempotence_mode(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.writable_snapshot_args,
                               {"writable_snapshot": [{"src_snap": 2, "dst_path": "/ifs/ansible/", "state": "absent"}]})
        powerscale_module_mock.check_mode = False
        powerscale_module_mock.get_writable_snapshot = MagicMock(return_value=(False, []))
        WritableSnapshotHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_delete_writable_snapshot_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.writable_snapshot_args,
                               {"writable_snapshot": [{"src_snap": 2, "dst_path": "/ifs/ansible/", "state": "absent"}]})
        powerscale_module_mock.check_mode = False
        powerscale_module_mock.snapshot_api.delete_snapshot_writable_wspath = MagicMock(side_effect=Exception)
        self.capture_fail_json_call("Failed to delete snapshot: /ifs/ansible/ with error", powerscale_module_mock, WritableSnapshotHandler)
