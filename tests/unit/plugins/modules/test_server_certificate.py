# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for server certificate module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils
from ansible_collections.dellemc.powerscale.plugins.modules.server_certificate import ServerCertificate, ServerCertificateHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_server_certificate_api \
    import MockServerCertificateApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase


CRT_PATH = "/ifs/server.crt"
KEY_PATH = "/ifs/server.key"
KEY_PASSWORD = "Secret@123!"
ALIAS_NAME = "test"
CERTIFICATE_ID = "6999b9c02949c962e84b600560a8faf001ab24438a474c2f662c95a17cd81034"


class TestServerCertificate(PowerScaleUnitBase):
    server_certificate_args = MockServerCertificateApi.SERVER_CERTIFICATE_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return ServerCertificate

    def test_validate_module_params(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.server_certificate_args,
                               {"state": "absent", "alias_name": ALIAS_NAME * 129})
        self.capture_fail_json_call(MockServerCertificateApi.get_module_params_error("alias_name_error"),
                                    powerscale_module_mock, ServerCertificateHandler)
        self.set_module_params(powerscale_module_mock, self.server_certificate_args,
                               {"state": "present", "description": ALIAS_NAME * 2048, "alias_name": ALIAS_NAME})
        self.capture_fail_json_call(MockServerCertificateApi.get_module_params_error("description_error"),
                                    powerscale_module_mock, ServerCertificateHandler)
        self.set_module_params(powerscale_module_mock, self.server_certificate_args,
                               {"state": "present", "description": ALIAS_NAME, "alias_name": ALIAS_NAME,
                                "certificate_key_password": KEY_PASSWORD * 256})
        self.capture_fail_json_call(MockServerCertificateApi.get_module_params_error("key_password_error"),
                                    powerscale_module_mock, ServerCertificateHandler)
        self.set_module_params(powerscale_module_mock, self.server_certificate_args,
                               {"state": "present", "description": ALIAS_NAME, "alias_name": ALIAS_NAME,
                                "certificate_key_password": KEY_PASSWORD, "certificate_path": CRT_PATH,
                                "certificate_key_path": KEY_PATH, "certificate_pre_expiration_threshold": -10})
        self.capture_fail_json_call(MockServerCertificateApi.get_module_params_error("threshold_error"),
                                    powerscale_module_mock, ServerCertificateHandler)

    def test_import_server_certificate_error(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.server_certificate_args,
                               {"state": "present", "alias_name": "test_new_cert",
                                "description": "This is the example for test new certificate.",
                                "certificate_key_password": KEY_PASSWORD, "is_default_certificate": True,
                                "certificate_monitor_enabled": True, "certificate_pre_expiration_threshold": 45673})
        powerscale_module_mock.certificate_api.create_certificate_server_item().to_dict = MagicMock(
            return_value=MockServerCertificateApi.IMPORT_CERTIFICATE_RESPONSE)
        self.capture_fail_json_call(MockServerCertificateApi.get_import_certificate_error('certificate_required_error'),
                                    powerscale_module_mock, ServerCertificateHandler)

    def test_import_server_certificate_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.server_certificate_args,
                               {"state": "present", "alias_name": "test_new_cert", "certificate_path": CRT_PATH,
                                "description": "This is the example for test_new cert.",
                                "certificate_key_path": KEY_PATH, "certificate_key_password": KEY_PASSWORD,
                                "is_default_certificate": True, "certificate_monitor_enabled": True,
                                "certificate_pre_expiration_threshold": 45673})
        powerscale_module_mock.certificate_api.create_certificate_server_item().to_dict = MagicMock(
            return_value=MockApiException)
        self.capture_fail_json_call(MockServerCertificateApi.get_import_certificate_error('certificate_exception'),
                                    powerscale_module_mock, ServerCertificateHandler)

    def test_import_server_certificate_check_mode(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.server_certificate_args,
                               {"state": "present", "alias_name": "test_new_cert", "certificate_path": CRT_PATH,
                                "description": "This is the example for test_new cert.",
                                "certificate_key_path": KEY_PATH, "certificate_key_password": KEY_PASSWORD,
                                "is_default_certificate": True, "certificate_monitor_enabled": True,
                                "certificate_pre_expiration_threshold": 45673})
        powerscale_module_mock.module.check_mode = True
        ServerCertificateHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_import_server_certificate_response_empty(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.server_certificate_args,
                               {"state": "present", "alias_name": "test_new_cert", "certificate_path": CRT_PATH,
                                "description": "This is the example for test new cert.",
                                "certificate_key_path": KEY_PATH, "certificate_key_password": KEY_PASSWORD,
                                "is_default_certificate": True, "certificate_monitor_enabled": True,
                                "certificate_pre_expiration_threshold": 45673})
        powerscale_module_mock.certificate_api.create_certificate_server_item().to_dict = MagicMock(
            return_value=MockServerCertificateApi.IMPORT_CERTIFICATE_RESPONSE_EMPTY)
        self.capture_fail_json_call(MockServerCertificateApi.get_import_certificate_error('certificate_exception'),
                                    powerscale_module_mock, ServerCertificateHandler)

    def test_import_server_certificate(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.server_certificate_args,
                               {"state": "present", "alias_name": "test_new_cert", "certificate_path": CRT_PATH,
                                "description": "This is the example for test new cert.",
                                "certificate_key_path": KEY_PATH, "certificate_key_password": KEY_PASSWORD,
                                "is_default_certificate": True, "certificate_monitor_enabled": True,
                                "certificate_pre_expiration_threshold": 45673})
        powerscale_module_mock.certificate_api.update_certificate_settings().to_dict = MagicMock(
            return_value=MockServerCertificateApi.UPDATE_DEFAULT_CERTIFICATE)
        powerscale_module_mock.certificate_api.create_certificate_server_item().to_dict = MagicMock(
            return_value=MockServerCertificateApi.IMPORT_CERTIFICATE_RESPONSE)
        powerscale_module_mock.certificate_api.list_certificate_server().to_dict = MagicMock(
            return_value=MockServerCertificateApi.GET_SERVER_CERTIFICATE_RESPONSE)
        ServerCertificateHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_update_server_certificate_without_value(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.server_certificate_args,
                               {"state": "present", "new_alias_name": None, "alias_name": None,
                                "description": None, "certificate_id": CERTIFICATE_ID,
                                "is_default_certificate": False})
        ServerCertificateHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']

    def test_update_server_certificate_check_mode(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.server_certificate_args,
                               {"state": "present", "new_alias_name": "test_updated", "alias_name": None,
                                "description": None, "certificate_id": CERTIFICATE_ID,
                                "is_default_certificate": False})
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.certificate_api.get_certificate_server_by_id(CERTIFICATE_ID).to_dict = MagicMock(
            return_value=MockServerCertificateApi.GET_SERVER_CERTIFICATE_RESPONSE)
        ServerCertificateHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_update_server_certificate_idempotence(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.server_certificate_args,
                               {"state": "present", "new_alias_name": "test", "alias_name": None,
                                "description": None, "certificate_id": CERTIFICATE_ID,
                                "is_default_certificate": False})
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.certificate_api.get_certificate_server_by_id(CERTIFICATE_ID).to_dict = MagicMock(
            return_value=MockServerCertificateApi.GET_SERVER_CERTIFICATE_RESPONSE)
        ServerCertificateHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert not powerscale_module_mock.module.exit_json.call_args[1]['changed']

    def test_update_server_certificate(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.server_certificate_args,
                               {"state": "present", "new_alias_name": "updated_test", "certificate_id": CERTIFICATE_ID,
                                "description": "This is the updated description certificate.",
                                "is_default_certificate": True, "certificate_monitor_enabled": True,
                                "certificate_pre_expiration_threshold": 45673})
        powerscale_module_mock.certificate_api.update_certificate_server_by_id().to_dict = MagicMock(
            return_value=MockServerCertificateApi.UPDATE_DEFAULT_CERTIFICATE)
        powerscale_module_mock.certificate_api.update_certificate_settings().to_dict = MagicMock(
            return_value=MockServerCertificateApi.UPDATE_DEFAULT_CERTIFICATE)
        ServerCertificateHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_certificate_name(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.server_certificate_args,
                               {"state": "absent", "alias_name": ALIAS_NAME})
        powerscale_module_mock.certificate_api.list_certificate_server().to_dict = MagicMock(
            return_value=MockServerCertificateApi.GET_SERVER_CERTIFICATE_RESPONSE)
        ServerCertificateHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_certificate_id(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.server_certificate_args,
                               {"state": "absent", "certificate_id": CERTIFICATE_ID})
        powerscale_module_mock.certificate_api.get_certificate_server_by_id(CERTIFICATE_ID).to_dict = MagicMock(
            return_value=MockServerCertificateApi.GET_SERVER_CERTIFICATE_RESPONSE)
        ServerCertificateHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_certificate_check_mode(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.server_certificate_args,
                               {"state": "absent", "alias_name": ALIAS_NAME})
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.certificate_api.list_certificate_server().to_dict = MagicMock(
            return_value=MockServerCertificateApi.GET_SERVER_CERTIFICATE_RESPONSE)
        ServerCertificateHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_certificate_check_mode_invalid_alias_name(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.server_certificate_args,
                               {"state": "absent", "alias_name": "test_example", "certificate_id": None})
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.certificate_api.list_certificate_server().to_dict = MagicMock(
            return_value=MockServerCertificateApi.GET_SERVER_CERTIFICATE_RESPONSE)
        ServerCertificateHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert not powerscale_module_mock.module.exit_json.call_args[1]['changed']

    def test_delete_default_certificate(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.server_certificate_args,
                               {"state": "absent", "alias_name": ALIAS_NAME})
        powerscale_module_mock.certificate_api.list_certificate_server().to_dict = MagicMock(
            return_value=MockServerCertificateApi.GET_SERVER_CERTIFICATE_RESPONSE)
        powerscale_module_mock.certificate_api.get_certificate_settings().to_dict = MagicMock(
            return_value=MockServerCertificateApi.GET_DEFAULT_CERTIFICATE)
        self.capture_fail_json_call(MockServerCertificateApi.get_default_certificate_error(),
                                    powerscale_module_mock, ServerCertificateHandler)

    def test_delete_certificate_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.server_certificate_args,
                               {"state": "absent", "alias_name": ALIAS_NAME})
        certificate_id = "6999b9c02949c962e84b600"
        self.set_module_params(powerscale_module_mock, self.server_certificate_args,
                               {"state": "absent", "certificate_id": certificate_id})
        powerscale_module_mock.certificate_api.get_certificate_server_by_id(certificate_id).to_dict = MagicMock(
            return_value=MockApiException)
        self.capture_fail_json_call(MockServerCertificateApi.get_certificate_error('get_certificate_error_id'),
                                    powerscale_module_mock, ServerCertificateHandler)
