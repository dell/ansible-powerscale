# Copyright: (c) 2022-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Smartpool Settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils


from ansible_collections.dellemc.powerscale.plugins.modules.smartpoolsettings import SmartPoolSettings
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_smartpoolsettings_api as MockSmartPoolSettingsApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase


class TestSmartPoolSettings(PowerScaleUnitBase):
    get_smartpool_settings_args = {"virtual_hot_spare_limit_percent": None,
                                   "virtual_hot_spare_hide_spare": None,
                                   "state": None}

    @pytest.fixture
    def module_object(self, mocker):
        return SmartPoolSettings

    def test_get_smartpool_setting(self, powerscale_module_mock):
        self.get_smartpool_settings_args.update({"state": "present"})
        powerscale_module_mock.module.params = self.get_smartpool_settings_args
        powerscale_module_mock.storagepool_api.get_storagepool_settings = MagicMock(
            return_value=MockSDKResponse(MockSmartPoolSettingsApi.GET_SMARTPOOL_SETTINGS))
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_get_smartpool_setting_with_exception(self, powerscale_module_mock):
        self.get_smartpool_settings_args.update({"state": "present"})
        powerscale_module_mock.module.params = self.get_smartpool_settings_args
        powerscale_module_mock.storagepool_api.get_storagepool_settings = MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockSmartPoolSettingsApi.get_networksettings_failed_msg(),
                                    invoke_perform_module=True)

    def test_modify_smartpool_settings(self, powerscale_module_mock):
        self.get_smartpool_settings_args.update({"state": "present", "virtual_hot_spare_limit_percent": 10, "virtual_hot_spare_hide_spare": True})
        powerscale_module_mock.module.params = self.get_smartpool_settings_args
        powerscale_module_mock.storagepool_api.update_storagepool_settings = MagicMock(
            return_value=MockSDKResponse(MockSmartPoolSettingsApi.UPDATE_SMARTPOOL_SETTINGS))
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']

    def test_modify_smartpool_settings_with_exception(self, powerscale_module_mock):
        self.get_smartpool_settings_args.update({"state": "present", "virtual_hot_spare_limit_percent": 10, "virtual_hot_spare_hide_spare": True})
        powerscale_module_mock.module.params = self.get_smartpool_settings_args
        powerscale_module_mock.storagepool_api.update_storagepool_settings = MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockSmartPoolSettingsApi.modify_networksettings_failed_msg(),
                                    invoke_perform_module=True)
