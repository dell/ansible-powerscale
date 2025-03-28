# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Alert Channel module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.alert_channel import AlertChannel, AlertChannelHandler, main
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_alert_channel_api import MockAlertChannelApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase


class TestAlertChannel(PowerScaleUnitBase):
    alert_args = MockAlertChannelApi.ALERT_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        """
        Returns an instance of the `AlertChannel` class for testing purposes.

        :return: An instance of the `AlertChannel` class.
        :rtype: `AlertChannel`
        """
        return AlertChannel

    def test_get_alert_channel_response(self, powerscale_module_mock):
        self.set_module_params(self.alert_args, {"name": MockAlertChannelApi.CHANNEL_NAME})
        AlertChannelHandler().handle(powerscale_module_mock,
                                     powerscale_module_mock.module.params)
        powerscale_module_mock.event_api.get_event_channel.assert_called()

    def test_get_alert_channel_exception(self, powerscale_module_mock):
        self.set_module_params(self.alert_args, {"name": MockAlertChannelApi.CHANNEL_NAME})
        powerscale_module_mock.event_api.get_event_channel = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockAlertChannelApi.get_alert_channel_exception('get_alert'),
            AlertChannelHandler)

    def test_create_alert_channel(self, powerscale_module_mock):
        self.set_module_params(self.alert_args,
                               {"name": MockAlertChannelApi.CHANNEL_NAME, "enabled": True, "type": "smtp",
                                "smtp_parameters": MockAlertChannelApi.SMTP_ARGS, "allowed_nodes": [1],
                                "excluded_nodes": [2], "send_test_alert": True})
        powerscale_module_mock.get_alert_channel_details = MagicMock(
            return_value=None)
        AlertChannelHandler().handle(powerscale_module_mock,
                                     powerscale_module_mock.module.params)
        powerscale_module_mock.event_api.create_event_channel.assert_called()

    def test_create_alert_channel_exception(self, powerscale_module_mock):
        self.set_module_params(self.alert_args,
                               {"name": MockAlertChannelApi.CHANNEL_NAME, "enabled": MockAlertChannelApi.ENABLED,
                                "type": "smtp",
                                "smtp_parameters": MockAlertChannelApi.SMTP_ARGS, "allowed_nodes": [1],
                                "excluded_nodes": [2], "send_test_alert": MockAlertChannelApi.ENABLED})
        powerscale_module_mock.get_alert_channel_details = MagicMock(
            return_value=None)
        powerscale_module_mock.event_api.create_event_channel = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockAlertChannelApi.get_alert_channel_exception('create_exp'),
            AlertChannelHandler)

    def test_send_test_alert_message(self, powerscale_module_mock):
        self.set_module_params(self.alert_args,
                               {"name": MockAlertChannelApi.CHANNEL_NAME,
                                "send_test_alert": MockAlertChannelApi.ENABLED})
        powerscale_module_mock.get_alert_channel_details = MagicMock(
            return_value=MockAlertChannelApi.CHANNEL_DETAILS['channels'][0])
        AlertChannelHandler().handle(powerscale_module_mock,
                                     powerscale_module_mock.module.params)
        powerscale_module_mock.event_api.create_event_channel_0.assert_called()

    def test_send_test_alert_message_exception(self, powerscale_module_mock):
        self.set_module_params(self.alert_args,
                               {"name": MockAlertChannelApi.CHANNEL_NAME,
                                "send_test_alert": MockAlertChannelApi.ENABLED})
        powerscale_module_mock.get_alert_channel_details = MagicMock(
            return_value=MockAlertChannelApi.CHANNEL_DETAILS['channels'][0])
        powerscale_module_mock.event_api.create_event_channel_0 = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockAlertChannelApi.get_alert_channel_exception('test_alert_exp'),
            AlertChannelHandler)

    def test_delete_alert_channel(self, powerscale_module_mock):
        self.set_module_params(self.alert_args,
                               {"name": MockAlertChannelApi.CHANNEL_NAME, "state": "absent"})
        powerscale_module_mock.get_alert_channel_details = MagicMock(
            return_value=MockAlertChannelApi.CHANNEL_DETAILS['channels'][0])
        AlertChannelHandler().handle(powerscale_module_mock,
                                     powerscale_module_mock.module.params)
        powerscale_module_mock.event_api.delete_event_channel.assert_called()

    def test_delete_alert_channel_expection(self, powerscale_module_mock):
        self.set_module_params(self.alert_args,
                               {"name": MockAlertChannelApi.CHANNEL_NAME, "state": "absent"})
        powerscale_module_mock.get_alert_channel_details = MagicMock(
            return_value=MockAlertChannelApi.CHANNEL_DETAILS['channels'][0])
        powerscale_module_mock.event_api.delete_event_channel = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockAlertChannelApi.get_alert_channel_exception('delete_exp'),
            AlertChannelHandler)

    def test_modify_alert_channel(self, powerscale_module_mock):
        self.set_module_params(self.alert_args,
                               {"name": MockAlertChannelApi.CHANNEL_NAME, "enabled": True, "type": "smtp",
                                "smtp_parameters": MockAlertChannelApi.SMTP_ARGS, "allowed_nodes": [2],
                                "excluded_nodes": [1], "send_test_alert": True})
        powerscale_module_mock.get_alert_channel_details = MagicMock(
            return_value=MockAlertChannelApi.CHANNEL_DETAILS['channels'][0])
        AlertChannelHandler().handle(powerscale_module_mock,
                                     powerscale_module_mock.module.params)
        powerscale_module_mock.event_api.update_event_channel.assert_called()

    def test_modify_alert_channel_exception(self, powerscale_module_mock):
        self.set_module_params(self.alert_args,
                               {"name": MockAlertChannelApi.CHANNEL_NAME, "enabled": MockAlertChannelApi.ENABLED,
                                "type": "smtp",
                                "smtp_parameters": MockAlertChannelApi.SMTP_ARGS, "allowed_nodes": [2],
                                "excluded_nodes": [1], "send_test_alert": MockAlertChannelApi.ENABLED})
        powerscale_module_mock.get_alert_channel_details = MagicMock(
            return_value=MockAlertChannelApi.CHANNEL_DETAILS['channels'][0])
        powerscale_module_mock.event_api.update_event_channel = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockAlertChannelApi.get_alert_channel_exception('modify_exp'),
            AlertChannelHandler)

    def test_validate_name(self, powerscale_module_mock):
        self.set_module_params(self.alert_args,
                               {"name": "  "})
        self.capture_fail_json_call(
            MockAlertChannelApi.get_alert_channel_exception('invalid_name1'),
            AlertChannelHandler)

    def test_validate_name_with_slash(self, powerscale_module_mock):
        self.set_module_params(self.alert_args,
                               {"name": "name/name"})
        self.capture_fail_json_call(
            MockAlertChannelApi.get_alert_channel_exception('invalid_name2'),
            AlertChannelHandler)

    def test_modify_alert_channel_with_update(self, powerscale_module_mock):
        self.set_module_params(self.alert_args,
                               {"name": MockAlertChannelApi.CHANNEL_NAME,
                                "smtp_parameters": MockAlertChannelApi.SMTP_ARGS2})
        powerscale_module_mock.get_alert_channel_details = MagicMock(
            return_value=MockAlertChannelApi.CHANNEL_DETAILS['channels'][0])
        AlertChannelHandler().handle(powerscale_module_mock,
                                     powerscale_module_mock.module.params)
        powerscale_module_mock.event_api.update_event_channel.assert_called()

    def test_invalid_smtp_auth_exception(self, powerscale_module_mock):
        self.set_module_params(self.alert_args,
                               {"name": MockAlertChannelApi.CHANNEL_NAME,
                                "smtp_parameters": MockAlertChannelApi.INVALID_USE_AUTH})
        powerscale_module_mock.get_alert_channel_details = MagicMock(
            return_value=MockAlertChannelApi.CHANNEL_DETAILS['channels'][0])
        self.capture_fail_json_call(
            MockAlertChannelApi.get_alert_channel_exception('smtp_auth_err'),
            AlertChannelHandler)
