# Copyright: (c) 2021, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for general settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

utils.get_logger = MagicMock()
utils.isi_sdk = MagicMock()
from ansible.module_utils import basic
basic.AnsibleModule = MagicMock()


from ansible_collections.dellemc.powerscale.plugins.modules.settings import Settings
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_settings_api as MockSettingApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException


class TestSettings():
    get_settings_args = {"mail_relay": None,
                         "mail_sender": None,
                         "mail_subject": None,
                         "state": None,
                         "email_settings": None,
                         "ntp_servers": None,
                         "ntp_server_id": None}

    @pytest.fixture
    def setting_module_mock(self, mocker):
        mocker.patch(MockSettingApi.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        setting_module_mock = Settings()
        setting_module_mock.module = MagicMock()
        return setting_module_mock

    def test_get_email_settings(self, setting_module_mock):
        setting_params = MockSettingApi.GET_SETTINGS
        self.get_settings_args.update({"state": "present", "email_settings": True})
        setting_module_mock.module.params = self.get_settings_args
        setting_module_mock.cluster_api.get_cluster_email = MagicMock(
            return_value=MockSDKResponse(MockSettingApi.GET_SETTINGS))
        setting_module_mock.perform_module_operation()
        assert setting_module_mock.module.exit_json.call_args[1]['changed'] is False
        assert setting_params == setting_module_mock.module.exit_json.call_args[1]['email_settings']

    def test_get_email_settings_with_exception(self, setting_module_mock):
<<<<<<< HEAD
        MockSettingApi.GET_SETTINGS
=======
        setting_params = MockSettingApi.GET_SETTINGS
>>>>>>> 0a01b051f102176470948082e530d4f51e9af771
        self.get_settings_args.update({"state": "present", "email_settings": True})
        setting_module_mock.module.params = self.get_settings_args
        setting_module_mock.cluster_api.get_email_settings = MagicMock(return_value=None)
        setting_module_mock.cluster_api.get_cluster_email = MagicMock(side_effect=utils.ApiException)
        setting_module_mock.perform_module_operation()
        assert MockSettingApi.get_email_setting_failed_msg() in \
            setting_module_mock.module.fail_json.call_args[1]['msg']

    def test_update_email_settings(self, setting_module_mock):
        self.get_settings_args.update({"mail_relay": "mailrelaymod.itp.xyz.net", "mail_sender": "lab-a2_mod@dell.com",
                                       "mail_subject": "lab_mod-alerts", "state": "present", "email_settings": False})
        setting_module_mock.module.params = self.get_settings_args
        setting_module_mock.cluster_api.update_cluster_email = MagicMock(
            return_value=MockSDKResponse(MockSettingApi.SETTINGS['email_settings_mod'][0]))
        setting_module_mock.perform_module_operation()
        assert setting_module_mock.module.exit_json.call_args[1]['changed'] is True
        assert setting_module_mock.module.exit_json.call_args[1]['email_settings']

    def test_update_email_settings_with_some_params(self, setting_module_mock):
        self.get_settings_args.update({"mail_relay": "mailrelaymod.itp.xyz.net", "mail_sender": "lab-a2_mod@dell.com",
                                       "state": "present", "email_settings": False})
        setting_module_mock.module.params = self.get_settings_args
        setting_module_mock.cluster_api.update_cluster_email = MagicMock(
            return_value=MockSDKResponse(MockSettingApi.SETTINGS['email_settings_mod'][0]))
        setting_module_mock.perform_module_operation()
        assert setting_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_update_email_settings_with_exception(self, setting_module_mock):
        self.get_settings_args.update({"mail_relay": "mailrelaymod.itp.xyz.net", "mail_sender": "lab-a2_mod@dell.com",
                                       "mail_subject": "lab_mod-alerts", "state": "present", "email_settings": False})
        setting_module_mock.module.params = self.get_settings_args
        setting_module_mock.cluster_api.update_cluster_email = MagicMock(side_effect=utils.ApiException)
        setting_module_mock.perform_module_operation()
        assert MockSettingApi.update_email_setting_failed_msg() in \
            setting_module_mock.module.fail_json.call_args[1]['msg']

<<<<<<< HEAD
    def test_get_ntp_server(self, setting_module_mock):
=======
    def test_get_NTP_server(self, setting_module_mock):
>>>>>>> 0a01b051f102176470948082e530d4f51e9af771
        ntp_details = MockSettingApi.SETTINGS['NTP_server'][0]
        self.get_settings_args.update({"state": "present", "email_settings": False, "ntp_server_id": "1.1.1.1"})
        setting_module_mock.module.params = self.get_settings_args
        setting_module_mock.protocol_api.get_ntp_server = MagicMock(
            return_value=MockSDKResponse(MockSettingApi.SETTINGS['NTP_server'][0]))
        setting_module_mock.perform_module_operation()
        assert setting_module_mock.module.exit_json.call_args[1]['changed'] is False
        assert ntp_details == setting_module_mock.module.exit_json.call_args[1]['ntp_server']

<<<<<<< HEAD
    def test_delete_ntp_server(self, setting_module_mock):
=======
    def test_delete_NTP_server(self, setting_module_mock):
>>>>>>> 0a01b051f102176470948082e530d4f51e9af771
        self.get_settings_args.update({"state": "absent", "email_settings": False, "ntp_servers": ['1.1.1.1']})
        setting_module_mock.module.params = self.get_settings_args
        setting_module_mock.protocol_api.list_ntp_servers = MagicMock(
            return_value=MockSDKResponse(MockSettingApi.SETTINGS['NTP_servers'][0]))
        setting_module_mock.protocol_api.delete_ntp_server = MagicMock(
            return_value=MockSDKResponse(MockSettingApi.SETTINGS['NTP_server'][0]))
        setting_module_mock.perform_module_operation()
        assert setting_module_mock.module.exit_json.call_args[1]['changed'] is True

<<<<<<< HEAD
    def test_add_ntp_server(self, setting_module_mock):
=======
    def test_add_NTP_server(self, setting_module_mock):
>>>>>>> 0a01b051f102176470948082e530d4f51e9af771
        self.get_settings_args.update({"mail_relay": "mailrelaymod.itp.xyz.net", "mail_sender": "lab-a2_mod@dell.com",
                                       "mail_subject": "lab_mod-alerts", "state": "present", "email_settings": False,
                                       "ntp_servers": ['1.1.1.1', '2.2.2.2']})
        setting_module_mock.module.params = self.get_settings_args
        setting_module_mock.protocol_api.list_ntp_servers = MagicMock(
            return_value=MockSDKResponse(MockSettingApi.SETTINGS['NTP_servers'][0]))
        setting_module_mock.protocol_api.create_ntp_server = MagicMock(
            return_value=MockSDKResponse(MockSettingApi.SETTINGS['NTP_server'][0]))
        setting_module_mock.perform_module_operation()
        assert setting_module_mock.module.exit_json.call_args[1]['changed'] is True

<<<<<<< HEAD
    def test_get_ntp_server_with_invalid_value(self, setting_module_mock):
=======
    def test_get_NTP_server_with_invalid_value(self, setting_module_mock):
>>>>>>> 0a01b051f102176470948082e530d4f51e9af771
        server = "asdasdasd"
        self.get_settings_args.update({"state": "present", "email_settings": False, "ntp_server_id": server})
        setting_module_mock.module.params = self.get_settings_args
        setting_module_mock.protocol_api.get_ntp_server = MagicMock(side_effect=utils.ApiException)
        setting_module_mock.perform_module_operation()
        assert MockSettingApi.get_ntp_server_failed_msg(server) in \
            setting_module_mock.module.fail_json.call_args[1]['msg']

<<<<<<< HEAD
    def test_add_ntp_server_with_blank_value(self, setting_module_mock):
=======
    def test_add_NTP_server_with_blank_value(self, setting_module_mock):
>>>>>>> 0a01b051f102176470948082e530d4f51e9af771
        server_list = ['1.1.1.1', '2.2.2.2']
        self.get_settings_args.update({"state": "present", "email_settings": False, "ntp_servers": server_list})
        setting_module_mock.module.params = self.get_settings_args
        setting_module_mock.protocol_api.list_ntp_servers = MagicMock(
            return_value=MockSDKResponse(MockSettingApi.SETTINGS['NTP_servers'][0]))
        setting_module_mock.protocol_api.create_ntp_server = MagicMock(side_effect=utils.ApiException)
        setting_module_mock.perform_module_operation()
        assert MockSettingApi.add_blank_ntp_server_msg(server_list) in \
            setting_module_mock.module.fail_json.call_args[1]['msg']

<<<<<<< HEAD
    def test_delete_ntp_server_with_invalid_value(self, setting_module_mock):
=======
    def test_delete_NTP_server_with_invalid_value(self, setting_module_mock):
>>>>>>> 0a01b051f102176470948082e530d4f51e9af771
        server = ["1.1.1.1"]
        self.get_settings_args.update({"state": "absent", "email_settings": False, "ntp_servers": server})
        setting_module_mock.module.params = self.get_settings_args
        setting_module_mock.protocol_api.list_ntp_servers = MagicMock(
            return_value=MockSDKResponse(MockSettingApi.SETTINGS['NTP_servers'][0]))
        setting_module_mock.protocol_api.delete_ntp_server = MagicMock(side_effect=utils.ApiException)
        setting_module_mock.perform_module_operation()
        assert MockSettingApi.delete_ntp_server_failed_msg(server) in \
            setting_module_mock.module.fail_json.call_args[1]['msg']
