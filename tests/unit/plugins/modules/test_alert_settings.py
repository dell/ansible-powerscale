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

from ansible_collections.dellemc.powerscale.plugins.modules.alert_settings import AlertSettings, AlertSettingsModifyHandler, main
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_alert_settings_api import MockAlertSettingsApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase


class TestAlertSettings(PowerScaleUnitBase):
    alert_args = MockAlertSettingsApi.ALERT_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        """
        Returns an instance of the `AlertSettings` class for testing purposes.

        :return: An instance of the `AlertSettings` class.
        :rtype: `AlertSettings`
        """
        return AlertSettings

    def test_get_alert_settings_response(self, powerscale_module_mock):
        self.set_module_params(self.alert_args, {})
        powerscale_module_mock.major = 9
        powerscale_module_mock.minor = 7
        AlertSettingsModifyHandler().handle(powerscale_module_mock,
                                            powerscale_module_mock.module.params)
        powerscale_module_mock.event_api.get_event_maintenance.assert_called()

    def test_get_alert_settings_exception(self, powerscale_module_mock):
        self.set_module_params(self.alert_args, {})
        powerscale_module_mock.major = 9
        powerscale_module_mock.minor = 7
        powerscale_module_mock.event_api.get_event_maintenance = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockAlertSettingsApi.get_alert_exception_response('get_alert'),
            AlertSettingsModifyHandler)

    def test_modify_maintenance_mode(self, powerscale_module_mock):
        self.set_module_params(self.alert_args,
                               {"enable_celog_maintenance_mode": True, "prune": 10})
        powerscale_module_mock.major = 9
        powerscale_module_mock.minor = 7
        powerscale_module_mock.get_alert_settings_details = MagicMock(
            return_value=MockAlertSettingsApi.SETTING_DETAILS)
        powerscale_module_mock.isi_sdk.EventMaintenanceExtended = MagicMock(
            {"maintenance": True, "prune": 10})
        AlertSettingsModifyHandler().handle(powerscale_module_mock,
                                            powerscale_module_mock.module.params)
        powerscale_module_mock.event_api.update_event_maintenance.assert_called()

    def test_modify_maintenance_mode_exception(self, powerscale_module_mock):
        self.set_module_params(self.alert_args,
                               {"enable_celog_maintenance_mode": True, "prune": 10})
        powerscale_module_mock.get_alert_settings_details = MagicMock(
            return_value=MockAlertSettingsApi.SETTING_DETAILS)
        powerscale_module_mock.isi_sdk.EventMaintenanceExtended = MagicMock(
            side_effect=MockApiException)
        powerscale_module_mock.major = 9
        powerscale_module_mock.minor = 7
        self.capture_fail_json_call(
            MockAlertSettingsApi.get_alert_exception_response(
                'modify_exp'),
            AlertSettingsModifyHandler)

    def test_modify_maintenance_mode_api_911(self, powerscale_module_mock):
        self.set_module_params(self.alert_args,
                               {"enable_celog_maintenance_mode": True, "prune": 10})
        powerscale_module_mock.major = 9
        powerscale_module_mock.minor = 11
        powerscale_module_mock.get_alert_settings_details = MagicMock(
            return_value=MockAlertSettingsApi.CLUSTER_MAINTENANCE_SETTINGS)
        powerscale_module_mock.isi_sdk.EventMaintenanceExtended = MagicMock(
            {"maintenance": True, "prune": 10})
        powerscale_module_mock.isi_sdk.event_api.update_event_settings = MagicMock(return_value=None)
        powerscale_module_mock.isi_sdk.cluster_api.update_maintenance_settings = MagicMock(return_value=None)
        AlertSettingsModifyHandler().handle(powerscale_module_mock,
                                            powerscale_module_mock.module.params)
        powerscale_module_mock.event_api.update_event_settings.assert_called()
        powerscale_module_mock.cluster_api.update_maintenance_settings.assert_called()

    def test_main(self, powerscale_module_mock):
        main()
