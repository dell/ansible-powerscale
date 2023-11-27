# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for SyncIQ global settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.synciq_global_settings import SyncIQGlobalSettings
from ansible_collections.dellemc.powerscale.plugins.modules.synciq_global_settings import SyncIQGlobalSettingsHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_synciq_global_settings_api \
    import MockSyncIQGlobalSettingsApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase


class TestSyncIQGlobalSettings(PowerScaleUnitBase):
    synciq_global_args = MockSyncIQGlobalSettingsApi.SYNCIQ_GLOBAL_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return SyncIQGlobalSettings

    def test_get_synciq_global_details(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.synciq_global_args, {})
        SyncIQGlobalSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.synciq_api.get_sync_settings.assert_called()

    def test_get_synciq_global_details_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.synciq_global_args, {})
        powerscale_module_mock.synciq_api.get_sync_settings = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSyncIQGlobalSettingsApi.get_synciq_global_settings_exception_response('get_details_exception'),
            powerscale_module_mock, SyncIQGlobalSettingsHandler)

    def test_modify_synciq_global_response(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.synciq_global_args,
                               {"service": 'on',
                                "encryption_required": False})
        powerscale_module_mock.get_synciq_global_settings_details = MagicMock(
            return_value=MockSyncIQGlobalSettingsApi.GET_SYNCIQ_GLOBAL_RESPONSE)
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.is_synciq_global_modify_required = MagicMock()
        SyncIQGlobalSettingsHandler().handle(powerscale_module_mock,
                                             powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.synciq_api.update_sync_settings.assert_called()

    def test_modify_synciq_global_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.synciq_global_args,
                               {"service": 'on',
                                "encryption_required": False})
        powerscale_module_mock.get_synciq_global_settings_details = MagicMock(
            return_value=MockSyncIQGlobalSettingsApi.GET_SYNCIQ_GLOBAL_RESPONSE)
        powerscale_module_mock.synciq_api.update_sync_settings = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSyncIQGlobalSettingsApi.get_synciq_global_settings_exception_response('update_exception'), powerscale_module_mock, SyncIQGlobalSettingsHandler)
