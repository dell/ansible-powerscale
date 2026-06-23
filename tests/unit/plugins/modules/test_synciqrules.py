# Copyright: (c) 2025 Dell Technologies

# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for SyncIQ Rules module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.plugins.modules.synciqrules \
    import SynciqRules


class TestSynciqRules:
    """Test class for SynciqRules helper methods"""

    @pytest.fixture
    def module_mock(self, mocker):
        """Create a mock SynciqRules module."""
        module = mocker.MagicMock(spec=SynciqRules)
        module.module = mocker.MagicMock()
        return module

    def test_validate_sync_rule_params_with_id(self, module_mock):
        """Test _validate_sync_rule_params when sync_rule_id is provided."""
        sync_rule_id = "rule123"
        rule_type = "type1"
        limit = 100
        schedule = {"days_of_week": "Mon", "begin": "00:00", "end": "23:59"}
        enabled = True
        state = "present"

        SynciqRules._validate_sync_rule_params(
            module_mock, sync_rule_id, rule_type, limit, schedule, enabled,
            state)

        module_mock.module.fail_json.assert_not_called()

    def test_validate_sync_rule_params_missing_rule_type(self, module_mock):
        """Test _validate_sync_rule_params when rule_type is missing."""
        sync_rule_id = None
        rule_type = None
        limit = 100
        schedule = {"days_of_week": "Mon", "begin": "00:00", "end": "23:59"}
        enabled = True
        state = "present"
        module_mock.module.fail_json = MagicMock()

        SynciqRules._validate_sync_rule_params(
            module_mock, sync_rule_id, rule_type, limit, schedule, enabled,
            state)

        module_mock.module.fail_json.assert_called_once()

    def test_validate_sync_rule_params_missing_limit(self, module_mock):
        """Test _validate_sync_rule_params when limit is missing."""
        sync_rule_id = None
        rule_type = "type1"
        limit = None
        schedule = {"days_of_week": "Mon", "begin": "00:00", "end": "23:59"}
        enabled = True
        state = "present"
        module_mock.module.fail_json = MagicMock()

        SynciqRules._validate_sync_rule_params(
            module_mock, sync_rule_id, rule_type, limit, schedule, enabled,
            state)

        module_mock.module.fail_json.assert_called_once()

    def test_validate_sync_rule_params_missing_days_of_week(self, module_mock):
        """Test _validate_sync_rule_params when days_of_week is missing."""
        sync_rule_id = None
        rule_type = "type1"
        limit = 100
        schedule = {"days_of_week": None, "begin": "00:00", "end": "23:59"}
        enabled = True
        state = "present"
        module_mock.module.fail_json = MagicMock()

        SynciqRules._validate_sync_rule_params(
            module_mock, sync_rule_id, rule_type, limit, schedule, enabled,
            state)

        module_mock.module.fail_json.assert_called_once()

    def test_validate_sync_rule_params_missing_enabled(self, module_mock):
        """Test _validate_sync_rule_params when enabled is missing."""
        sync_rule_id = None
        rule_type = "type1"
        limit = 100
        schedule = {"days_of_week": "Mon", "begin": "00:00", "end": "23:59"}
        enabled = None
        state = "present"
        module_mock.module.fail_json = MagicMock()

        SynciqRules._validate_sync_rule_params(
            module_mock, sync_rule_id, rule_type, limit, schedule, enabled,
            state)

        module_mock.module.fail_json.assert_called_once()

    def test_validate_sync_rule_params_absent_without_id(self, module_mock):
        """Test _validate_sync_rule_params when state is absent but no id
        provided."""
        sync_rule_id = None
        rule_type = "type1"
        limit = 100
        schedule = {"days_of_week": "Mon", "begin": "00:00", "end": "23:59"}
        enabled = True
        state = "absent"
        module_mock.module.fail_json = MagicMock()

        SynciqRules._validate_sync_rule_params(
            module_mock, sync_rule_id, rule_type, limit, schedule, enabled,
            state)

        module_mock.module.fail_json.assert_called_once()
