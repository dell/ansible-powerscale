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
        self.set_module_params(
            powerscale_module_mock, self.alert_args, {"name": MockAlertChannelApi.CHANNEL_NAME})
        AlertChannelHandler().handle(powerscale_module_mock,
                                     powerscale_module_mock.module.params)
        powerscale_module_mock.event_api.get_event_channel.assert_called()

    def test_get_alert_channel_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.alert_args, {"name": MockAlertChannelApi.CHANNEL_NAME})
        powerscale_module_mock.event_api.get_event_channel = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockAlertChannelApi.get_alert_channel_exception('get_alert'),
            powerscale_module_mock, AlertChannelHandler)
