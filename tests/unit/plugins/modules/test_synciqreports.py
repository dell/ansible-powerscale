# Copyright: (c) 2025 Dell Technologies

# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for SyncIQ Reports module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.plugins.modules.synciqreports \
    import SyncIQReports


class TestSyncIQReports:
    """Test class for SyncIQReports helper methods"""

    @pytest.fixture
    def module_mock(self, mocker):
        """Create a mock SyncIQReports module."""
        module = mocker.MagicMock(spec=SyncIQReports)
        module.module = mocker.MagicMock()
        module.module.params = {'id': None, 'name': None}
        return module

    def test_resolve_report_id_with_id(self, module_mock):
        """Test _resolve_report_id when id is provided."""
        module_mock.module.params = {'id': 'report123', 'name': None}

        result = SyncIQReports._resolve_report_id(module_mock)

        assert result == 'report123'
        module_mock.module.fail_json.assert_not_called()

    def test_resolve_report_id_with_name(self, module_mock):
        """Test _resolve_report_id when name is provided."""
        module_mock.module.params = {'id': None, 'name': 'report_name'}
        module_mock.get_report_id = MagicMock(return_value='report456')

        result = SyncIQReports._resolve_report_id(module_mock)

        assert result == 'report456'
        module_mock.get_report_id.assert_called_once_with('report_name')

    def test_resolve_report_id_without_id_or_name(self, module_mock):
        """Test _resolve_report_id when neither id nor name is provided."""
        module_mock.module.params = {'id': None, 'name': None}
        module_mock.module.fail_json = MagicMock()

        SyncIQReports._resolve_report_id(module_mock)

        module_mock.module.fail_json.assert_called_once_with(
            msg='Please provide a valid report id or valid report name')
