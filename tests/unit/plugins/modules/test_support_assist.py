# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for support assist settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils
from ansible_collections.dellemc.powerscale.plugins.modules.support_assist import SupportAssist
from ansible_collections.dellemc.powerscale.plugins.modules.support_assist import SupportAssistHandler
from ansible_collections.dellemc.powerscale.plugins.modules.support_assist import main
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_support_assist_api \
    import MockSupportAssistApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase


class TestSupportAssist(PowerScaleUnitBase):
    support_assist_args = MockSupportAssistApi.SUPPORT_ASSIST_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return SupportAssist

    def test_get_support_assist_details(self, powerscale_module_mock):
        self.set_module_params(self.support_assist_args, {})
        SupportAssistHandler().handle(powerscale_module_mock,
                                      powerscale_module_mock.module.params)
        powerscale_module_mock.support_assist_api.get_supportassist_settings.assert_called()

    def test_get_support_assist_details_exception(self, powerscale_module_mock):
        self.set_module_params(self.support_assist_args, {})
        powerscale_module_mock.support_assist_api.get_supportassist_settings = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSupportAssistApi.get_support_assist_settings_exception_response('get_details_exception'),
            SupportAssistHandler)

    def test_modify_support_assist_network_pool_response(self, powerscale_module_mock):
        self.set_module_params(self.support_assist_args,
                               {
                                   "connection": {
                                       "network_pools": [
                                           {
                                               "pool_name": "subnet0:pool1",
                                               "state": "absent"
                                           },
                                           {
                                               "pool_name": "subnet0:pool5",
                                               "state": "present"
                                           }
                                       ]
                                   }
                               })
        powerscale_module_mock.get_support_assist_details = MagicMock(
            return_value=MockSupportAssistApi.GET_SUPPORT_ASSIST_RESPONSE)
        powerscale_module_mock.module.check_mode = False
        SupportAssistHandler().handle(powerscale_module_mock,
                                      powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.support_assist_api.update_supportassist_settings.assert_called()

    def test_modify_support_assist_gateway_endpoints_response(self, powerscale_module_mock):
        self.set_module_params(self.support_assist_args,
                               {
                                   "connection": {
                                       "gateway_endpoints": [
                                           {
                                               "enabled": True,
                                               "gateway_host": "XX.XX.XX.XX",
                                               "gateway_port": 9443,
                                               "priority": 2,
                                               "use_proxy": False,
                                               "validate_ssl": False,
                                               "state": "present"
                                           },
                                           {
                                               "enabled": True,
                                               "gateway_host": "XX.XX.XX.XZ",
                                               "gateway_port": 9443,
                                               "priority": 1,
                                               "use_proxy": False,
                                               "validate_ssl": False,
                                               "state": "present"
                                           },
                                           {
                                               "enabled": True,
                                               "gateway_host": "XX.XX.XX.XY",
                                               "gateway_port": 9443,
                                               "priority": 2,
                                               "use_proxy": False,
                                               "validate_ssl": False,
                                               "state": "absent"
                                           }
                                       ],
                                       "mode": "gateway"
                                   }
                               })
        powerscale_module_mock.get_support_assist_details = MagicMock(
            return_value=MockSupportAssistApi.GET_SUPPORT_ASSIST_RESPONSE)
        powerscale_module_mock.module.check_mode = False
        SupportAssistHandler().handle(powerscale_module_mock,
                                      powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.support_assist_api.update_supportassist_settings.assert_called()

    def test_modify_support_assist_contact_response(self, powerscale_module_mock):
        self.set_module_params(self.support_assist_args,
                               {
                                   "contact": {
                                       "primary": {
                                           "email": "primary@example.com",
                                           "first_name": "Jane",
                                           "last_name": "Doe",
                                           "phone": "1234567890"
                                       },
                                       "secondary": {
                                           "email": "secondary@example.com",
                                           "first_name": "John",
                                           "last_name": "Doe",
                                           "phone": "1234567891"
                                       }
                                   }
                               })
        powerscale_module_mock.get_support_assist_details = MagicMock(
            return_value=MockSupportAssistApi.GET_SUPPORT_ASSIST_RESPONSE)
        powerscale_module_mock.module.check_mode = False
        SupportAssistHandler().handle(powerscale_module_mock,
                                      powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.support_assist_api.update_supportassist_settings.assert_called()

    def test_modify_support_assist_telemetry_response(self, powerscale_module_mock):
        self.set_module_params(self.support_assist_args,
                               {
                                   "telemetry": {
                                       "offline_collection_period": 61,
                                       "telemetry_enabled": True,
                                       "telemetry_persist": False,
                                       "telemetry_threads": 11
                                   }
                               })
        powerscale_module_mock.get_support_assist_details = MagicMock(
            return_value=MockSupportAssistApi.GET_SUPPORT_ASSIST_RESPONSE)
        powerscale_module_mock.module.check_mode = False
        SupportAssistHandler().handle(powerscale_module_mock,
                                      powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.support_assist_api.update_supportassist_settings.assert_called()

    def test_disable_support_assist_telemetry_response(self, powerscale_module_mock):
        self.set_module_params(self.support_assist_args,
                               {
                                   "telemetry": {
                                       "telemetry_enabled": False
                                   }
                               })
        powerscale_module_mock.get_support_assist_details = MagicMock(
            return_value=MockSupportAssistApi.GET_SUPPORT_ASSIST_RESPONSE)
        powerscale_module_mock.module.check_mode = False
        SupportAssistHandler().handle(powerscale_module_mock,
                                      powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.support_assist_api.update_supportassist_settings.assert_called()

    def test_modify_support_assist_params_response(self, powerscale_module_mock):
        self.set_module_params(self.support_assist_args,
                               {
                                   "enable_download": True,
                                   "enable_remote_support": True,
                                   "automatic_case_creation": True,
                                   "enable_service": False
                               })
        powerscale_module_mock.get_support_assist_details = MagicMock(
            return_value=MockSupportAssistApi.GET_SUPPORT_ASSIST_RESPONSE)
        powerscale_module_mock.module.check_mode = False
        SupportAssistHandler().handle(powerscale_module_mock,
                                      powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.support_assist_api.update_supportassist_settings.assert_called()

    def test_accept_support_assist_terms_response(self, powerscale_module_mock):
        self.set_module_params(self.support_assist_args,
                               {
                                   "accepted_terms": True
                               })
        powerscale_module_mock.get_support_assist_details = MagicMock(
            return_value=MockSupportAssistApi.GET_SUPPORT_ASSIST_RESPONSE)
        powerscale_module_mock.module.check_mode = False
        SupportAssistHandler().handle(powerscale_module_mock,
                                      powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.support_assist_api.update_supportassist_terms.assert_called()

    def test_modify_support_assist_response_check_mode(self, powerscale_module_mock):
        self.support_assist_args.update({"enable_download": True})
        powerscale_module_mock.module.check_mode = True
        self.set_module_params(self.support_assist_args, {})
        powerscale_module_mock.get_support_assist_details = MagicMock(
            return_value=MockSupportAssistApi.GET_SUPPORT_ASSIST_RESPONSE)
        SupportAssistHandler().handle(powerscale_module_mock,
                                      powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_accept_support_assist_terms_response_check_mode(self, powerscale_module_mock):
        self.support_assist_args.update({"accepted_terms": True})
        powerscale_module_mock.module.check_mode = True
        self.set_module_params(self.support_assist_args, {})
        powerscale_module_mock.get_support_assist_details = MagicMock(
            return_value=MockSupportAssistApi.GET_SUPPORT_ASSIST_RESPONSE)
        SupportAssistHandler().handle(powerscale_module_mock,
                                      powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_support_assist_exception(self, powerscale_module_mock):
        self.support_assist_args.update({"enable_download": True})
        self.set_module_params(self.support_assist_args, {})
        powerscale_module_mock.get_support_assist_details = MagicMock(
            return_value=MockSupportAssistApi.GET_SUPPORT_ASSIST_RESPONSE)
        powerscale_module_mock.support_assist_api.update_supportassist_settings = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSupportAssistApi.get_support_assist_settings_exception_response('update_exception'),
            SupportAssistHandler)

    def test_empty_gateway_endpoints_exception(self, powerscale_module_mock):
        self.support_assist_args.update(
            {
                "connection": {
                    "gateway_endpoints": [
                        {
                            "gateway_host": "XX.XX.XX.XX",
                            "state": "absent"
                        },
                        {
                            "gateway_host": "XX.XX.XX.XY",
                            "state": "absent"
                        }
                    ],
                    "mode": "gateway"
                }
            })
        self.set_module_params(self.support_assist_args, {})
        powerscale_module_mock.get_support_assist_details = MagicMock(
            return_value=MockSupportAssistApi.GET_SUPPORT_ASSIST_RESPONSE)
        self.capture_fail_json_call(
            MockSupportAssistApi.get_support_assist_settings_exception_response('empty_gateway_exception'),
            SupportAssistHandler)

    def test_empty_network_pools_exception(self, powerscale_module_mock):
        self.support_assist_args.update(
            {
                "connection": {
                    "network_pools": [
                        {
                            "pool_name": "subnet0:pool1",
                            "state": "absent"
                        }
                    ],
                    "mode": "gateway"
                }
            })
        self.set_module_params(self.support_assist_args, {})
        powerscale_module_mock.get_support_assist_details = MagicMock(
            return_value=MockSupportAssistApi.GET_SUPPORT_ASSIST_RESPONSE)
        self.capture_fail_json_call(
            MockSupportAssistApi.get_support_assist_settings_exception_response('empty_network_pools_exception'),
            SupportAssistHandler)

    def test_accept_support_assist_terms_exception(self, powerscale_module_mock):
        self.support_assist_args.update({"accepted_terms": True})
        self.set_module_params(self.support_assist_args, {})
        powerscale_module_mock.get_support_assist_details = MagicMock(
            return_value=MockSupportAssistApi.GET_SUPPORT_ASSIST_RESPONSE)
        powerscale_module_mock.support_assist_api.update_supportassist_terms = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSupportAssistApi.get_support_assist_settings_exception_response('accept_terms_exception'),
            SupportAssistHandler)

    def test_main(self, powerscale_module_mock):
        self.set_module_params(self.support_assist_args, {})
        powerscale_module_mock.get_support_assist_details = MagicMock(
            return_value=MockSupportAssistApi.GET_SUPPORT_ASSIST_RESPONSE)
        main()
        powerscale_module_mock.support_assist_api.get_supportassist_settings.assert_called()
