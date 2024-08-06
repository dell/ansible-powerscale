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

from ansible_collections.dellemc.powerscale.plugins.modules.alert_management import AlertRule, AlertRuleHandler, main
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

    def test_create_alert_rule(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.alert_rule_args, {})
        powerscale_module_mock.get_alert_rule = MagicMock(return_value={})
        AlertRuleHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_alert_rule_check_mode(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.alert_rule_args, {})
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.get_alert_rule = MagicMock(return_value={})
        AlertRuleHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
