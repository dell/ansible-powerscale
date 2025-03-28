# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for user mapping rules module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.snmp_settings import SNMPSettings
from ansible_collections.dellemc.powerscale.plugins.modules.snmp_settings import SNMPSettingsHandler
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.protocol \
    import Protocol
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_snmp_settings_api \
    import MockSNMPSettingsApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase


class TestSNMPSettings(PowerScaleUnitBase):
    snmp_settings_args = MockSNMPSettingsApi.SNMP_SETTINGS_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return SNMPSettings

    def test_get_snmp_settings(self, powerscale_module_mock):
        self.set_module_params(self.snmp_settings_args, {})
        SNMPSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.get_snmp_settings.assert_called()

    def test_get_snmp_settings_exception(self, powerscale_module_mock):
        self.set_module_params(self.snmp_settings_args, {})
        powerscale_module_mock.protocol_api.get_snmp_settings = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSNMPSettingsApi.get_snmpsettings_exception_response('get_resp_exception'),
            SNMPSettingsHandler)

    def test_modify_snmp_settings(self, powerscale_module_mock):
        self.set_module_params(self.snmp_settings_args,
                               {"system_contact": "contact@set.set",
                                "system_location": "location_set",
                                "snmp_v2c_access": False,
                                "snmp_v3": {
                                    "access": False,
                                    "auth_protocol": "MD5",
                                    "privacy_password": "password",
                                    "privacy_protocol": "DES",
                                    "security_level": "noAuthNoPriv",
                                    "read_only_user": "user",
                                    "password": "password_set"
                                },
                                "read_only_community": "community_set"})
        powerscale_module_mock.protocol_api.get_snmp_settings.to_dict = MagicMock(
            return_value=MockSNMPSettingsApi.GET_SNMP_SETTINGS_RESPONSE)
        SNMPSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.update_snmp_settings.assert_called()

    def test_modify_snmp_settings_exception(self, powerscale_module_mock):
        self.set_module_params(self.snmp_settings_args,
                               {"service": False})
        powerscale_module_mock.protocol_api.get_snmp_settings.to_dict = MagicMock(
            return_value=MockSNMPSettingsApi.GET_SNMP_SETTINGS_RESPONSE)
        powerscale_module_mock.protocol_api.update_snmp_settings = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSNMPSettingsApi.get_snmpsettings_exception_response('update_exception'),
            SNMPSettingsHandler)

    def test_validate_params_exception(self, powerscale_module_mock):
        self.set_module_params(self.snmp_settings_args,
                               {"system_contact": "set   .set"})
        powerscale_module_mock.protocol_api.get_snmp_settings.to_dict = MagicMock(
            return_value=MockSNMPSettingsApi.GET_SNMP_SETTINGS_RESPONSE)
        self.capture_fail_json_call(
            MockSNMPSettingsApi.get_snmpsettings_exception_response('system_contact_exception'), SNMPSettingsHandler)

    def test_valdiate_sysetm_location_exception(self, powerscale_module_mock):
        self.set_module_params(self.snmp_settings_args,
                               {"system_location": "  "})
        powerscale_module_mock.protocol_api.get_snmp_settings.to_dict = MagicMock(
            return_value=MockSNMPSettingsApi.GET_SNMP_SETTINGS_RESPONSE)
        self.capture_fail_json_call(
            MockSNMPSettingsApi.get_snmpsettings_exception_response('system_location_exception'), SNMPSettingsHandler)
