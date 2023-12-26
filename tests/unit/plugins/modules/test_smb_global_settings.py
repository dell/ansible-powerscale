# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for SMB global settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils
from ansible_collections.dellemc.powerscale.plugins.modules.smb_global_settings import SMBGlobalSettings
from ansible_collections.dellemc.powerscale.plugins.modules.smb_global_settings import SMBGlobalSettingsHandler
from ansible_collections.dellemc.powerscale.plugins.modules.smb_global_settings import main
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_smb_global_settings_api \
    import MockSMBGlobalSettingsApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse


class TestSMBGlobalSettings(PowerScaleUnitBase):
    smb_global_args = MockSMBGlobalSettingsApi.SMB_GLOBAL_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return SMBGlobalSettings

    def test_get_smb_global_details(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.smb_global_args, {})
        SMBGlobalSettingsHandler().handle(powerscale_module_mock,
                                          powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.get_smb_settings_global.assert_called()

    def test_get_smb_global_details_empty(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.smb_global_args, {})
        powerscale_module_mock.protocol_api.get_smb_settings_global.return_value = MockSDKResponse(None)
        SMBGlobalSettingsHandler().handle(powerscale_module_mock,
                                          powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False
        assert powerscale_module_mock.module.exit_json.call_args[
            1]['smb_global_settings_details'] is None

    def test_get_smb_global_details_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.smb_global_args, {})
        powerscale_module_mock.protocol_api.get_smb_settings_global = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSMBGlobalSettingsApi.get_smb_global_settings_exception_response('get_details_exception'),
            powerscale_module_mock, SMBGlobalSettingsHandler)

    @pytest.mark.parametrize("service_val", [True, False])
    def test_modify_smb_global_response(self, powerscale_module_mock, service_val):
        self.smb_global_args.update({
            "service": service_val
        })
        self.set_module_params(powerscale_module_mock,
                               self.smb_global_args, {})
        powerscale_module_mock.get_smb_global_settings_details = MagicMock(
            return_value=MockSMBGlobalSettingsApi.GET_SMB_GLOBAL_RESPONSE)
        SMBGlobalSettingsHandler().handle(powerscale_module_mock,
                                          powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is service_val
        if service_val:
            powerscale_module_mock.protocol_api.update_smb_settings_global.assert_called()

    def test_modify_smb_global_response_check_mode(self, powerscale_module_mock):
        self.smb_global_args.update({
            "service": True
        })
        powerscale_module_mock.module.check_mode = True
        self.set_module_params(powerscale_module_mock,
                               self.smb_global_args, {})
        powerscale_module_mock.get_smb_global_settings_details = MagicMock(
            return_value=MockSMBGlobalSettingsApi.GET_SMB_GLOBAL_RESPONSE)
        SMBGlobalSettingsHandler().handle(powerscale_module_mock,
                                          powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_smb_global_exception(self, powerscale_module_mock):
        self.smb_global_args.update({"service": True})
        self.set_module_params(powerscale_module_mock,
                               self.smb_global_args, {})
        powerscale_module_mock.get_smb_global_settings_details = MagicMock(
            return_value=MockSMBGlobalSettingsApi.GET_SMB_GLOBAL_RESPONSE)
        powerscale_module_mock.protocol_api.update_smb_settings_global = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSMBGlobalSettingsApi.get_smb_global_settings_exception_response('update_exception'),
            powerscale_module_mock, SMBGlobalSettingsHandler)

    def test_main(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.smb_global_args, {})
        powerscale_module_mock.get_smb_global_settings_details = MagicMock(
            return_value=MockSMBGlobalSettingsApi.GET_SMB_GLOBAL_RESPONSE)
        main()
        powerscale_module_mock.protocol_api.get_smb_settings_global.assert_called()
