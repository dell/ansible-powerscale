# Copyright: (c) 2021-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Network Settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils


from ansible_collections.dellemc.powerscale.plugins.modules.networksettings import NetworkSettings
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_networksettings_api as MockNetworkSettingsApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase


class TestNetworkSettings(PowerScaleUnitBase):
    get_network_settings_args = {"enable_source_routing": None,
                                 "state": None}

    @pytest.fixture
    def module_object(self, mocker):
        return NetworkSettings

    def test_get_network_setting(self, powerscale_module_mock):
        self.get_network_settings_args.update({"state": "present"})
        powerscale_module_mock.module.params = self.get_network_settings_args
        powerscale_module_mock.network_api.get_network_external = MagicMock(
            return_value=MockSDKResponse(MockNetworkSettingsApi.GET_NETWORK_SETTINGS))
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_get_network_settings_with_exception(self, powerscale_module_mock):
        self.get_network_settings_args.update({"state": "present"})
        powerscale_module_mock.module.params = self.get_network_settings_args
        powerscale_module_mock.network_api.get_network_external = MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNetworkSettingsApi.get_networksettings_failed_msg(), invoke_perform_module=True)

    def test_modify_network_settings(self, powerscale_module_mock):
        self.get_network_settings_args.update({"state": "present", "enable_source_routing": True})
        powerscale_module_mock.module.params = self.get_network_settings_args
        powerscale_module_mock.network_api.update_network_external = MagicMock(
            return_value=MockSDKResponse(MockNetworkSettingsApi.UPDATE_NETWORK_SETTINGS))
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']

    def test_modify_network_settings_with_exception(self, powerscale_module_mock):
        self.get_network_settings_args.update({"state": "present", "enable_source_routing": True})
        powerscale_module_mock.module.params = self.get_network_settings_args
        powerscale_module_mock.network_api.update_network_external = MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNetworkSettingsApi.modify_networksettings_failed_msg(),
                                    invoke_perform_module=True)
