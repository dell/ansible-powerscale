# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Alert Setting module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import patch, MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils
from ansible_collections.dellemc.powerscale.plugins.modules.alert_management import AlertRule, AlertRuleHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_alert_management_api import MockAlertRuleApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase


class TestAlertRule(PowerScaleUnitBase):

    alert_rule_args = MockAlertRuleApi.ALERT_RULE_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return AlertRule

    @pytest.fixture
    def mock_events(self):
        with patch("ansible_collections.dellemc.powerscale.plugins.modules.alert_management.Events") as MockEvents:
            yield MockEvents

    def test_get_create_alert_rule(self, powerscale_module_mock, mock_events):
        self.set_module_params(powerscale_module_mock, self.alert_rule_args,
                               MockAlertRuleApi.UPDATE_ALERT_RULE_OPTIONS)
        mock_event_instance = mock_events.return_value
        mock_event_instance.get_alert_rules = MagicMock(
            return_value=MockAlertRuleApi.GET_EXISTING_ALERT_RULE_OPTIONS)
        powerscale_module_mock.modify_alert_condition = MagicMock(return_value=(True, {"name": "alert_rule"}))
        AlertRuleHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_alert_rule(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.alert_rule_args, {})
        powerscale_module_mock.get_alert_rule = MagicMock(return_value={})
        AlertRuleHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_alert_rule_check_mode(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.alert_rule_args, {})
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.module._diff = True
        powerscale_module_mock.get_alert_rule = MagicMock(return_value={})
        AlertRuleHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_alert_rule_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.alert_rule_args, {})
        powerscale_module_mock.get_alert_rule = MagicMock(return_value={})
        powerscale_module_mock.event_api.create_event_alert_condition = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call("Failed to create alert condition: SDK Error message", powerscale_module_mock, AlertRuleHandler)

    def test_update_alert_rule(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.alert_rule_args,
                               MockAlertRuleApi.UPDATE_ALERT_RULE_OPTIONS)
        powerscale_module_mock.get_alert_rule = MagicMock(
            return_value=MockAlertRuleApi.EXISTING_ALERT_RULE_OPTIONS)
        AlertRuleHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_update_alert_rule_check_mode(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.alert_rule_args,
                               MockAlertRuleApi.UPDATE_ALERT_RULE_OPTIONS)
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.module._diff = True
        powerscale_module_mock.get_alert_rule = MagicMock(
            return_value=MockAlertRuleApi.EXISTING_ALERT_RULE_OPTIONS)
        AlertRuleHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_update_alert_rule_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.alert_rule_args,
                               MockAlertRuleApi.UPDATE_ALERT_RULE_OPTIONS)
        powerscale_module_mock.get_alert_rule = MagicMock(
            return_value=MockAlertRuleApi.EXISTING_ALERT_RULE_OPTIONS)
        powerscale_module_mock.event_api.update_event_alert_condition = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call("Failed to update alert condition: SDK Error message", powerscale_module_mock, AlertRuleHandler)
