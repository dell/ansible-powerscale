# Copyright: (c) 2022, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

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


class TestSmartPoolSettings():
    get_smartpool_settings_args = {"virtual_hot_spare_limit_percent": None,
                                   "virtual_hot_spare_hide_spare": None,
                                   "state": None}

    @pytest.fixture
    def smartpool_settings_module_mock(self, mocker):
        mocker.patch(MockSmartPoolSettingsApi.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        smartpoolsettings_module_mock = SmartPoolSettings()
        smartpoolsettings_module_mock.module = MagicMock()
        return smartpoolsettings_module_mock

    def test_get_smartpool_setting(self, smartpool_settings_module_mock):
        self.get_smartpool_settings_args.update({"state": "present"})
        smartpool_settings_module_mock.module.params = self.get_smartpool_settings_args
        smartpool_settings_module_mock.storagepool_api.get_storagepool_settings = MagicMock(
            return_value=MockSDKResponse(MockSmartPoolSettingsApi.GET_SMARTPOOL_SETTINGS))
        smartpool_settings_module_mock.perform_module_operation()
        assert smartpool_settings_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_get_smartpool_setting_with_exception(self, smartpool_settings_module_mock):
        self.get_smartpool_settings_args.update({"state": "present"})
        smartpool_settings_module_mock.module.params = self.get_smartpool_settings_args
        smartpool_settings_module_mock.storagepool_api.get_storagepool_settings = MagicMock(side_effect=utils.ApiException)
        smartpool_settings_module_mock.perform_module_operation()
        assert MockSmartPoolSettingsApi.get_networksettings_failed_msg() in \
            smartpool_settings_module_mock.module.fail_json.call_args[1]['msg']

    def test_modify_smartpool_settings(self, smartpool_settings_module_mock):
        self.get_smartpool_settings_args.update({"state": "present", "virtual_hot_spare_limit_percent": 10, "virtual_hot_spare_hide_spare": True})
        smartpool_settings_module_mock.module.params = self.get_smartpool_settings_args
        smartpool_settings_module_mock.storagepool_api.update_storagepool_settings = MagicMock(
            return_value=MockSDKResponse(MockSmartPoolSettingsApi.UPDATE_SMARTPOOL_SETTINGS))
        smartpool_settings_module_mock.perform_module_operation()
        assert smartpool_settings_module_mock.module.exit_json.call_args[1]['changed']

    def test_modify_smartpool_settings_with_exception(self, smartpool_settings_module_mock):
        self.get_smartpool_settings_args.update({"state": "present", "virtual_hot_spare_limit_percent": 10, "virtual_hot_spare_hide_spare": True})
        smartpool_settings_module_mock.module.params = self.get_smartpool_settings_args
        smartpool_settings_module_mock.storagepool_api.update_storagepool_settings = MagicMock(side_effect=utils.ApiException)
        smartpool_settings_module_mock.perform_module_operation()
        assert MockSmartPoolSettingsApi.modify_networksettings_failed_msg() in \
            smartpool_settings_module_mock.module.fail_json.call_args[1]['msg']
