# Copyright: (c) 2021, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for general settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils


from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase
from ansible_collections.dellemc.powerscale.plugins.modules.settings import Settings
from ansible_collections.dellemc.powerscale.plugins.modules.settings import SettingsHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_settings_api \
    import MockSettingsApi


class TestSettings(PowerScaleUnitBase):
    settings_args = MockSettingsApi.SETTINGS_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return Settings

    def test_get_email_settings(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.settings_args, {})
        powerscale_module_mock.get_email_settings = MagicMock(return_value=MockSettingsApi.GET_SETTINGS)
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.get_email_settings.assert_called()

    def test_get_ntp_servers(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.settings_args, {})
        powerscale_module_mock.get_ntp_servers = MagicMock(return_value=MockSettingsApi.SETTINGS['NTP_servers'][0])
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.get_ntp_servers.assert_called()

    def test_get_cluster_identity_settings(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.settings_args, {})
        powerscale_module_mock.get_cluster_identity_details = MagicMock(return_value=MockSettingsApi.SETTINGS['cluster_identity'])
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.get_cluster_identity_details.assert_called()

    def test_get_cluster_owner_details(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.settings_args, {})
        powerscale_module_mock.get_cluster_owner_details = MagicMock(return_value=MockSettingsApi.SETTINGS['cluster_owner'])
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.get_cluster_owner_details.assert_called()

    def test_update_email_settings(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.settings_args,
                               {"mail_relay": "mailrelaymod.itp.xyz.net",
                                "mail_sender": "lab-a2_mod@dell.com",
                                "mail_subject": "lab_mod-alerts"})
        powerscale_module_mock.get_email_settings = MagicMock(return_value=MockSettingsApi.GET_SETTINGS)
        powerscale_module_mock.update_cluster_email = MagicMock(return_value=True)
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_update_email_settings_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.settings_args,
                               {"mail_relay": "mailrelaymod.itp.xyz.net",
                                "mail_sender": "lab-a2_mod@dell.com",
                                "mail_subject": "lab_mod-alerts"})
        powerscale_module_mock.get_email_settings = MagicMock(return_value=MockSettingsApi.GET_SETTINGS)
        powerscale_module_mock.cluster_api.update_cluster_email = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSettingsApi.get_settings_exception_response('update_email_exception'),
            powerscale_module_mock, SettingsHandler)

    def test_update_cluster_identity_settings(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.settings_args,
                               {"description": "This is a new description",
                                "logon": {"motd": "This is a new description",
                                          "motd_header": "This is the a new title"},
                                "mttdl_level_msg": "none",
                                "name": "PIE-IsilonS-24241-Cluster"})
        powerscale_module_mock.get_cluster_identity_details = MagicMock(return_value=MockSettingsApi.SETTINGS['cluster_identity'])
        powerscale_module_mock.update_cluster_identity = MagicMock(return_value=True)
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_update_cluster_identity_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.settings_args,
                               {"description": "This is a test description",
                                "logon": {"motd": "This is a test description",
                                          "motd_header": "This is a test title"},
                                "mttdl_level_msg": "none",
                                "name": "PIE-IsilonS-24241-Cluster"})
        powerscale_module_mock.get_cluster_identity_details = MagicMock(return_value=MockSettingsApi.SETTINGS['cluster_identity'])
        powerscale_module_mock.cluster_api.update_cluster_identity = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSettingsApi.get_settings_exception_response('update_cluster_identity'),
            powerscale_module_mock, SettingsHandler)

    def test_update_cluster_owner_settings(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.settings_args,
                               {"company": "Test company 1",
                                "location": "Test location 1",
                                "primary_email": "primary_email1@email.com",
                                "primary_name": "primary_name1",
                                "primary_phone1": "primary_phone11",
                                "primary_phone2": "primary_phone21",
                                "secondary_email": "secondary_email1@email.com",
                                "secondary_name": "secondary_name1",
                                "secondary_phone1": "secondary_phone11",
                                "secondary_phone2": "secondary_phone21"})
        powerscale_module_mock.get_cluster_owner_details = MagicMock(return_value=MockSettingsApi.SETTINGS['cluster_owner'])
        powerscale_module_mock.update_owner_identity = MagicMock(return_value=True)
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_update_cluster_owner_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.settings_args,
                               {"company": "Test company 1",
                                "location": "Test location 1",
                                "primary_email": "primary_email1@email.com",
                                "primary_name": "primary_name1",
                                "primary_phone1": "primary_phone11",
                                "primary_phone2": "primary_phone21",
                                "secondary_email": "secondary_email1@email.com",
                                "secondary_name": "secondary_name1",
                                "secondary_phone1": "secondary_phone11",
                                "secondary_phone2": "secondary_phone21"})
        powerscale_module_mock.get_cluster_owner_details = MagicMock(return_value=MockSettingsApi.SETTINGS['cluster_owner'])
        powerscale_module_mock.cluster_api.update_cluster_owner = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSettingsApi.get_settings_exception_response('update_cluster_owner'),
            powerscale_module_mock, SettingsHandler)

    def test_delete_ntp_server(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.settings_args, {"state": "absent", "ntp_servers": [MockSettingsApi.IP_ADDRESS]})
        powerscale_module_mock.get_ntp_servers = MagicMock(return_value=MockSettingsApi.SETTINGS['NTP_servers'][0])
        powerscale_module_mock.protocol_api.delete_ntp_server = MagicMock(return_value=True)
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_add_ntp_server(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.settings_args, {"ntp_servers": [MockSettingsApi.IP_ADDRESS]})
        powerscale_module_mock.get_ntp_servers = MagicMock(return_value=MockSettingsApi.SETTINGS['NTP_servers'][0])
        powerscale_module_mock.protocol_api.create_ntp_server = MagicMock(return_value=(MockSettingsApi.SETTINGS['NTP_server'][0]))
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_add_ntp_server_with_invalid_value(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.settings_args, {"ntp_servers": [MockSettingsApi.IP_ADDRESS]})
        powerscale_module_mock.get_ntp_servers = MagicMock(return_value=MockSettingsApi.SETTINGS['NTP_servers'][0])
        powerscale_module_mock.protocol_api.create_ntp_server = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSettingsApi.get_settings_exception_response('adding_invalid_server'),
            powerscale_module_mock, SettingsHandler)

    def test_delete_ntp_server_with_invalid_value(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.settings_args, {"state": "absent", "ntp_servers": [MockSettingsApi.IP_ADDRESS]})
        powerscale_module_mock.get_ntp_servers = MagicMock(return_value=MockSettingsApi.SETTINGS['NTP_servers'][0])
        powerscale_module_mock.protocol_api.delete_ntp_server = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSettingsApi.get_settings_exception_response('removing_invalid_server'),
            powerscale_module_mock, SettingsHandler)

    def test_add_ntp_server_with_blank_value(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.settings_args, {"ntp_servers": ['']})
        self.capture_fail_json_call(
            MockSettingsApi.get_settings_exception_response('invalid_NTP_value'),
            powerscale_module_mock, SettingsHandler)

    def test_cluster_name_invalid_length(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.settings_args, {"name": 'PIE-IsilonS-24241-ClusterPIE-IsilonS-242PIE-IsilonS-24241-'
                                                                                    'ClusterPIE-IsilonS-242PIE-IsilonS-24241-ClusterPIE-IsilonS-'
                                                                                    '242PIE-IsilonS-24241'})
        self.capture_fail_json_call(
            MockSettingsApi.get_settings_exception_response('update_invalid_cluster_name'),
            powerscale_module_mock, SettingsHandler)

    def test_cluster_description_invalid_length(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.settings_args, {"description": 'PIE-IsilonS-24241-ClusterPIE-IsilonS-242PIE-IsilonS-'
                                                                                           '24241-ClusterPIE-IsilonS-242PIE-IsilonS-24241-Cluster'
                                                                                           'PIE-IsilonS-242PIE-IsilonS-24241-ClusterPIE-IsilonS-24'
                                                                                           '2PIE-IsilonS-24241-ClusterPIE-IsilonS-242 PIE-IsilonS-'
                                                                                           '24241-ClusterPIE-IsilonS-242PIE-IsilonS-242sdfsdfsfsdf'})
        self.capture_fail_json_call(
            MockSettingsApi.get_settings_exception_response('update_invalid_cluster_description'),
            powerscale_module_mock, SettingsHandler)

    def test_cluster_owner_invalid_email(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.settings_args, {"mail_sender": "primary_email123"})
        self.capture_fail_json_call(
            MockSettingsApi.get_settings_exception_response('update_invalid_mail_sender_email'),
            powerscale_module_mock, SettingsHandler)
