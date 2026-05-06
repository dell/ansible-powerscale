# Copyright: (c) 2025 Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Snapshot Schedule module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.plugins.modules.snapshotschedule import SnapshotSchedule


class TestSnapshotSchedule:
    """Test class for SnapshotSchedule helper methods"""

    @pytest.fixture
    def module_mock(self, mocker):
        """Create a mock SnapshotSchedule module."""
        module = mocker.MagicMock(spec=SnapshotSchedule)
        module.module = mocker.MagicMock()
        return module

    def test_check_retention_modified_increase(self, module_mock):
        """Test _check_retention_modified when retention is increased."""
        snapshot_schedule_details = {
            'schedules': [{'duration': 3600}]  # 1 hour in seconds
        }
        retention_in_sec = 7200  # 2 hours in seconds
        snapshot_schedule_modify = {}

        result = SnapshotSchedule._check_retention_modified(
            module_mock, retention_in_sec, snapshot_schedule_details, snapshot_schedule_modify)
        
        assert result is True
        assert snapshot_schedule_modify['duration'] == 7200

    def test_check_retention_modified_same(self, module_mock):
        """Test _check_retention_modified when retention is the same."""
        snapshot_schedule_details = {
            'schedules': [{'duration': 3600}]  # 1 hour in seconds
        }
        retention_in_sec = 3600  # 1 hour in seconds
        snapshot_schedule_modify = {}

        result = SnapshotSchedule._check_retention_modified(
            module_mock, retention_in_sec, snapshot_schedule_details, snapshot_schedule_modify)
        
        assert result is False
        assert snapshot_schedule_modify == {}

    def test_check_retention_modified_below_minimum(self, module_mock):
        """Test _check_retention_modified when retention is below 2 hours."""
        snapshot_schedule_details = {
            'schedules': [{'duration': 3600}]  # 1 hour in seconds
        }
        retention_in_sec = 1800  # 30 minutes in seconds
        snapshot_schedule_modify = {}

        module_mock.module.fail_json = MagicMock()

        result = SnapshotSchedule._check_retention_modified(
            module_mock, retention_in_sec, snapshot_schedule_details, snapshot_schedule_modify)
        
        module_mock.module.fail_json.assert_called_once_with(
            msg="The snapshot desired retention must be at least 2 hours")
