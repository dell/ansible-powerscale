# Copyright: (c) 2021-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for general settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
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
        self.set_module_params(self.settings_args, {})
        powerscale_module_mock.get_email_settings = MagicMock(return_value=MockSettingsApi.GET_SETTINGS)
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.get_email_settings.assert_called()

    def test_get_ntp_servers(self, powerscale_module_mock):
        self.set_module_params(self.settings_args, {})
        powerscale_module_mock.get_ntp_servers = MagicMock(return_value=MockSettingsApi.SETTINGS['NTP_servers'][0])
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.get_ntp_servers.assert_called()

    def test_get_cluster_identity_settings(self, powerscale_module_mock):
        self.set_module_params(self.settings_args, {})
        powerscale_module_mock.get_cluster_identity_details = MagicMock(return_value=MockSettingsApi.SETTINGS['cluster_identity'])
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.get_cluster_identity_details.assert_called()

    def test_get_cluster_owner_details(self, powerscale_module_mock):
        self.set_module_params(self.settings_args, {})
        powerscale_module_mock.get_cluster_owner_details = MagicMock(return_value=MockSettingsApi.SETTINGS['cluster_owner'])
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.get_cluster_owner_details.assert_called()

    def test_update_email_settings(self, powerscale_module_mock):
        self.set_module_params(self.settings_args,
                               {"mail_relay": "mailrelaymod.itp.xyz.net",
                                "mail_sender": "lab-a2_mod@dell.com",
                                "mail_subject": "lab_mod-alerts"})
        powerscale_module_mock.get_email_settings = MagicMock(return_value=MockSettingsApi.GET_SETTINGS)
        powerscale_module_mock.update_cluster_email = MagicMock(return_value=True)
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_update_email_settings_exception(self, powerscale_module_mock):
        self.set_module_params(self.settings_args,
                               {"mail_relay": "mailrelaymod.itp.xyz.net",
                                "mail_sender": "lab-a2_mod@dell.com",
                                "mail_subject": "lab_mod-alerts"})
        powerscale_module_mock.get_email_settings = MagicMock(return_value=MockSettingsApi.GET_SETTINGS)
        powerscale_module_mock.cluster_api.update_cluster_email = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSettingsApi.get_settings_exception_response('update_email_exception'),
            SettingsHandler)

    def test_update_cluster_identity_settings(self, powerscale_module_mock):
        self.set_module_params(self.settings_args,
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
        self.set_module_params(self.settings_args,
                               {"description": "This is a test description",
                                "logon": {"motd": "This is a test description",
                                          "motd_header": "This is a test title"},
                                "mttdl_level_msg": "none",
                                "name": "PIE-IsilonS-24241-Cluster"})
        powerscale_module_mock.get_cluster_identity_details = MagicMock(return_value=MockSettingsApi.SETTINGS['cluster_identity'])
        powerscale_module_mock.cluster_api.update_cluster_identity = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSettingsApi.get_settings_exception_response('update_cluster_identity'),
            SettingsHandler)

    def test_update_cluster_owner_settings(self, powerscale_module_mock):
        self.set_module_params(self.settings_args,
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
        self.set_module_params(self.settings_args,
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
            SettingsHandler)

    def test_delete_ntp_server(self, powerscale_module_mock):
        self.set_module_params(self.settings_args, {"state": "absent", "ntp_servers": [MockSettingsApi.IP_ADDRESS]})
        powerscale_module_mock.get_ntp_servers = MagicMock(return_value=MockSettingsApi.SETTINGS['NTP_servers'][0])
        powerscale_module_mock.protocol_api.delete_ntp_server = MagicMock(return_value=True)
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_add_ntp_server(self, powerscale_module_mock):
        self.set_module_params(self.settings_args, {"ntp_servers": [MockSettingsApi.IP_ADDRESS]})
        powerscale_module_mock.get_ntp_servers = MagicMock(return_value=MockSettingsApi.SETTINGS['NTP_servers'][0])
        powerscale_module_mock.protocol_api.create_ntp_server = MagicMock(return_value=(MockSettingsApi.SETTINGS['NTP_server'][0]))
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_add_ntp_server_with_invalid_value(self, powerscale_module_mock):
        self.set_module_params(self.settings_args, {"ntp_servers": [MockSettingsApi.IP_ADDRESS]})
        powerscale_module_mock.get_ntp_servers = MagicMock(return_value="")
        powerscale_module_mock.protocol_api.create_ntp_server = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSettingsApi.get_settings_exception_response('adding_invalid_server'),
            SettingsHandler)

    def test_delete_ntp_server_with_invalid_value(self, powerscale_module_mock):
        self.set_module_params(self.settings_args, {"state": "absent", "ntp_servers": [MockSettingsApi.IP_ADDRESS]})
        powerscale_module_mock.get_ntp_servers = MagicMock(return_value=MockSettingsApi.SETTINGS['NTP_servers'][0])
        powerscale_module_mock.protocol_api.delete_ntp_server = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSettingsApi.get_settings_exception_response('removing_invalid_server'),
            SettingsHandler)

    def test_add_ntp_server_with_blank_value(self, powerscale_module_mock):
        self.set_module_params(self.settings_args, {"ntp_servers": ['']})
        self.capture_fail_json_call(
            MockSettingsApi.get_settings_exception_response('invalid_NTP_value'),
            SettingsHandler)

    def test_cluster_name_invalid_length(self, powerscale_module_mock):
        self.set_module_params(self.settings_args, {"name": 'PIE-IsilonS-24241-ClusterPIE-IsilonS-242PIE-IsilonS-24241-'
                                                            'ClusterPIE-IsilonS-242PIE-IsilonS-24241-ClusterPIE-IsilonS-'
                                                            '242PIE-IsilonS-24241'})
        self.capture_fail_json_call(
            MockSettingsApi.get_settings_exception_response('update_invalid_cluster_name'),
            SettingsHandler)

    def test_cluster_description_invalid_length(self, powerscale_module_mock):
        self.set_module_params(self.settings_args,
                               {"description": 'PIE-IsilonS-24241-ClusterPIE-IsilonS-242PIE-IsilonS-'
                                               '24241-ClusterPIE-IsilonS-242PIE-IsilonS-24241-Cluster'
                                               'PIE-IsilonS-242PIE-IsilonS-24241-ClusterPIE-IsilonS-24'
                                               '2PIE-IsilonS-24241-ClusterPIE-IsilonS-242 PIE-IsilonS-'
                                               '24241-ClusterPIE-IsilonS-242PIE-IsilonS-242sdfsdfsfsdf'})
        self.capture_fail_json_call(
            MockSettingsApi.get_settings_exception_response('update_invalid_cluster_description'),
            SettingsHandler)

    def test_cluster_owner_invalid_email(self, powerscale_module_mock):
        self.set_module_params(self.settings_args, {"mail_sender": "primary_email123"})
        self.capture_fail_json_call(
            MockSettingsApi.get_settings_exception_response('update_invalid_mail_sender_email'),
            SettingsHandler)

    # ========================================================================
    # Declarative NTP Server Tests (Test IDs: U-001 through U-017)
    # ========================================================================

    # Null overrides for non-NTP params to prevent spurious changes
    # from unmocked email/cluster/owner getters returning MagicMock.
    _NTP_ONLY = {
        "mail_relay": None, "mail_sender": None, "mail_subject": None,
        "name": None, "description": None, "logon_details": None,
        "company": None, "location": None,
        "primary_contact": None, "secondary_contact": None,
    }

    def test_ntp_declarative_convergence_add_and_remove(self, powerscale_module_mock):
        """U-001: Declarative convergence — adds missing servers and removes extra servers."""
        self.set_module_params(self.settings_args,
                               {**self._NTP_ONLY,
                                "ntp_servers": ["ntp1.example.com", "ntp2.example.com"],
                                "state": "present"})
        powerscale_module_mock.get_ntp_servers = MagicMock(
            return_value=MockSettingsApi.NTP_SERVERS_TWO_CURRENT)
        powerscale_module_mock.protocol_api.create_ntp_server = MagicMock(return_value=True)
        powerscale_module_mock.protocol_api.delete_ntp_server = MagicMock(return_value=True)
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result['changed'] is True
        assert powerscale_module_mock.module.exit_json.called is True
        # ntp2 should be added (not in current [ntp1, ntp-old])
        powerscale_module_mock.protocol_api.create_ntp_server.assert_called()
        assert powerscale_module_mock.protocol_api.create_ntp_server.call_count >= 1
        # ntp-old should be removed (not in desired [ntp1, ntp2])
        powerscale_module_mock.protocol_api.delete_ntp_server.assert_called()
        assert powerscale_module_mock.protocol_api.delete_ntp_server.call_count >= 1

    def test_ntp_declarative_idempotent_no_change(self, powerscale_module_mock):
        """U-002: Idempotency — no changes when desired == current."""
        self.set_module_params(self.settings_args,
                               {**self._NTP_ONLY,
                                "ntp_servers": ["ntp1.example.com", "ntp2.example.com"],
                                "state": "present"})
        powerscale_module_mock.get_ntp_servers = MagicMock(
            return_value=MockSettingsApi.NTP_SERVERS_MATCHING)
        powerscale_module_mock.protocol_api.create_ntp_server = MagicMock(return_value=True)
        powerscale_module_mock.protocol_api.delete_ntp_server = MagicMock(return_value=True)
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result['changed'] is False
        assert powerscale_module_mock.module.exit_json.called is True
        assert powerscale_module_mock.protocol_api.create_ntp_server.call_count == 0
        assert powerscale_module_mock.protocol_api.delete_ntp_server.call_count == 0
        powerscale_module_mock.protocol_api.create_ntp_server.assert_not_called()
        powerscale_module_mock.protocol_api.delete_ntp_server.assert_not_called()

    def test_ntp_declarative_add_only(self, powerscale_module_mock):
        """U-003: Declarative add-only — adds new servers, none removed."""
        self.set_module_params(self.settings_args,
                               {**self._NTP_ONLY,
                                "ntp_servers": ["ntp1.example.com", "ntp2.example.com", "ntp3.example.com"],
                                "state": "present"})
        powerscale_module_mock.get_ntp_servers = MagicMock(
            return_value=MockSettingsApi.NTP_SERVERS_MATCHING)
        powerscale_module_mock.protocol_api.create_ntp_server = MagicMock(return_value=True)
        powerscale_module_mock.protocol_api.delete_ntp_server = MagicMock(return_value=True)
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result['changed'] is True
        assert powerscale_module_mock.module.exit_json.called is True
        powerscale_module_mock.protocol_api.create_ntp_server.assert_called()
        assert powerscale_module_mock.protocol_api.create_ntp_server.call_count == 1
        assert powerscale_module_mock.protocol_api.delete_ntp_server.call_count == 0
        powerscale_module_mock.protocol_api.delete_ntp_server.assert_not_called()

    def test_ntp_declarative_remove_only(self, powerscale_module_mock):
        """U-004: Declarative remove-only — removes extra servers, none added."""
        self.set_module_params(self.settings_args,
                               {**self._NTP_ONLY,
                                "ntp_servers": ["ntp1.example.com"],
                                "state": "present"})
        powerscale_module_mock.get_ntp_servers = MagicMock(
            return_value=MockSettingsApi.NTP_SERVERS_TWO_CURRENT)
        powerscale_module_mock.protocol_api.create_ntp_server = MagicMock(return_value=True)
        powerscale_module_mock.protocol_api.delete_ntp_server = MagicMock(return_value=True)
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result['changed'] is True
        assert powerscale_module_mock.module.exit_json.called is True
        assert powerscale_module_mock.protocol_api.create_ntp_server.call_count == 0
        powerscale_module_mock.protocol_api.create_ntp_server.assert_not_called()
        powerscale_module_mock.protocol_api.delete_ntp_server.assert_called()
        assert powerscale_module_mock.protocol_api.delete_ntp_server.call_count == 1

    def test_ntp_declarative_check_mode(self, powerscale_module_mock):
        """U-005: Check mode — detects changes but does not apply."""
        powerscale_module_mock.module.check_mode = True
        self.set_module_params(self.settings_args,
                               {**self._NTP_ONLY,
                                "ntp_servers": ["ntp1.example.com"],
                                "state": "present"})
        powerscale_module_mock.get_ntp_servers = MagicMock(
            return_value=MockSettingsApi.NTP_SERVERS_SINGLE)
        powerscale_module_mock.protocol_api.create_ntp_server = MagicMock(return_value=True)
        powerscale_module_mock.protocol_api.delete_ntp_server = MagicMock(return_value=True)
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result['changed'] is True
        assert powerscale_module_mock.module.exit_json.called is True
        assert powerscale_module_mock.module.check_mode is True
        assert powerscale_module_mock.protocol_api.create_ntp_server.call_count == 0
        assert powerscale_module_mock.protocol_api.delete_ntp_server.call_count == 0
        powerscale_module_mock.protocol_api.create_ntp_server.assert_not_called()
        powerscale_module_mock.protocol_api.delete_ntp_server.assert_not_called()

    def test_ntp_declarative_diff_mode(self, powerscale_module_mock):
        """U-006: Diff mode — produces before/after output."""
        powerscale_module_mock.module._diff = True
        self.set_module_params(self.settings_args,
                               {**self._NTP_ONLY,
                                "ntp_servers": ["ntp1.example.com"],
                                "state": "present"})
        powerscale_module_mock.get_ntp_servers = MagicMock(
            return_value=MockSettingsApi.NTP_SERVERS_SINGLE)
        powerscale_module_mock.protocol_api.create_ntp_server = MagicMock(return_value=True)
        powerscale_module_mock.protocol_api.delete_ntp_server = MagicMock(return_value=True)
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result['changed'] is True
        assert powerscale_module_mock.module.exit_json.called is True
        assert 'diff' in result
        assert isinstance(result['diff'], dict)
        assert 'before' in result['diff']
        assert 'after' in result['diff']
        assert 'ntp_servers' in result['diff']['before']
        assert 'ntp_servers' in result['diff']['after']
        assert isinstance(result['diff']['before']['ntp_servers'], list)
        assert isinstance(result['diff']['after']['ntp_servers'], list)
        assert 'ntp-old.example.com' in result['diff']['before']['ntp_servers']
        assert 'ntp1.example.com' in result['diff']['after']['ntp_servers']

    def test_ntp_declarative_check_and_diff_mode(self, powerscale_module_mock):
        """U-007: Combined check+diff — detects changes, shows diff, no API calls."""
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.module._diff = True
        self.set_module_params(self.settings_args,
                               {**self._NTP_ONLY,
                                "ntp_servers": ["ntp1.example.com", "ntp2.example.com"],
                                "state": "present"})
        powerscale_module_mock.get_ntp_servers = MagicMock(
            return_value=MockSettingsApi.NTP_SERVERS_SINGLE)
        powerscale_module_mock.protocol_api.create_ntp_server = MagicMock(return_value=True)
        powerscale_module_mock.protocol_api.delete_ntp_server = MagicMock(return_value=True)
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result['changed'] is True
        assert powerscale_module_mock.module.exit_json.called is True
        assert powerscale_module_mock.module.check_mode is True
        assert 'diff' in result
        assert isinstance(result['diff'], dict)
        assert 'before' in result['diff']
        assert 'after' in result['diff']
        assert powerscale_module_mock.protocol_api.create_ntp_server.call_count == 0
        assert powerscale_module_mock.protocol_api.delete_ntp_server.call_count == 0
        powerscale_module_mock.protocol_api.create_ntp_server.assert_not_called()
        powerscale_module_mock.protocol_api.delete_ntp_server.assert_not_called()

    def test_ntp_legacy_absent_behavior_preserved(self, powerscale_module_mock):
        """U-008: Backward compat — state=absent removes only listed servers."""
        self.set_module_params(self.settings_args,
                               {**self._NTP_ONLY,
                                "ntp_servers": ["ntp1.example.com"],
                                "state": "absent"})
        powerscale_module_mock.get_ntp_servers = MagicMock(
            return_value=MockSettingsApi.NTP_SERVERS_TWO_CURRENT)
        powerscale_module_mock.protocol_api.delete_ntp_server = MagicMock(return_value=True)
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result['changed'] is True
        # Only ntp1 should be removed (not ntp-old)
        powerscale_module_mock.protocol_api.delete_ntp_server.assert_called_once()

    def test_ntp_declarative_single_server(self, powerscale_module_mock):
        """U-015: Boundary — converge to single NTP server from three."""
        self.set_module_params(self.settings_args,
                               {**self._NTP_ONLY,
                                "ntp_servers": ["ntp1.example.com"],
                                "state": "present"})
        powerscale_module_mock.get_ntp_servers = MagicMock(
            return_value=MockSettingsApi.NTP_SERVERS_THREE)
        powerscale_module_mock.protocol_api.create_ntp_server = MagicMock(return_value=True)
        powerscale_module_mock.protocol_api.delete_ntp_server = MagicMock(return_value=True)
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result['changed'] is True
        # ntp2 and ntp3 should be removed
        assert powerscale_module_mock.protocol_api.delete_ntp_server.call_count == 2
        powerscale_module_mock.protocol_api.create_ntp_server.assert_not_called()

    def test_ntp_declarative_duplicate_servers_deduplication(self, powerscale_module_mock):
        """U-016: Negative — duplicate servers in desired list are deduplicated."""
        self.set_module_params(self.settings_args,
                               {**self._NTP_ONLY,
                                "ntp_servers": ["ntp1.example.com", "ntp1.example.com", "ntp2.example.com"],
                                "state": "present"})
        powerscale_module_mock.get_ntp_servers = MagicMock(
            return_value=MockSettingsApi.NTP_SERVERS_MATCHING)
        powerscale_module_mock.protocol_api.create_ntp_server = MagicMock(return_value=True)
        powerscale_module_mock.protocol_api.delete_ntp_server = MagicMock(return_value=True)
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        result = powerscale_module_mock.module.exit_json.call_args[1]
        # After dedup: {ntp1, ntp2} == current, so no change
        assert result['changed'] is False
        powerscale_module_mock.protocol_api.create_ntp_server.assert_not_called()
        powerscale_module_mock.protocol_api.delete_ntp_server.assert_not_called()

    def test_ntp_compute_servers_to_remove(self, powerscale_module_mock):
        """U-017: Unit — compute_ntp_servers_to_remove returns correct difference."""
        powerscale_module_mock.get_ntp_servers = MagicMock(
            return_value=MockSettingsApi.NTP_SERVERS_TWO_CURRENT)
        assert hasattr(powerscale_module_mock, 'compute_ntp_servers_to_remove')
        result = powerscale_module_mock.compute_ntp_servers_to_remove(
            ["ntp1.example.com", "ntp2.example.com"])
        assert isinstance(result, list)
        assert len(result) == 1
        assert "ntp-old.example.com" in result
        assert "ntp1.example.com" not in result
        assert "ntp2.example.com" not in result

    def test_ntp_declarative_full_workflow(self, powerscale_module_mock):
        """I-001: Integration — set NTP servers declaratively, then re-run for idempotency."""
        # First run: converge from [ntp1, ntp-old] to [ntp1, ntp2]
        self.set_module_params(self.settings_args,
                               {**self._NTP_ONLY,
                                "ntp_servers": ["ntp1.example.com", "ntp2.example.com"],
                                "state": "present"})
        powerscale_module_mock.get_ntp_servers = MagicMock(
            return_value=MockSettingsApi.NTP_SERVERS_TWO_CURRENT)
        powerscale_module_mock.protocol_api.create_ntp_server = MagicMock(return_value=True)
        powerscale_module_mock.protocol_api.delete_ntp_server = MagicMock(return_value=True)
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        first_result = powerscale_module_mock.module.exit_json.call_args[1]
        assert first_result['changed'] is True
        assert powerscale_module_mock.module.exit_json.called is True
        assert powerscale_module_mock.protocol_api.create_ntp_server.call_count >= 1
        assert powerscale_module_mock.protocol_api.delete_ntp_server.call_count >= 1

        # Second run: now current matches desired — should be idempotent
        powerscale_module_mock.module.exit_json.reset_mock()
        powerscale_module_mock.protocol_api.create_ntp_server.reset_mock()
        powerscale_module_mock.protocol_api.delete_ntp_server.reset_mock()
        powerscale_module_mock.result = {
            "changed": False, "email_settings": {},
            "ntp_servers": {}, "cluster_owner": {}, "cluster_identity": {}
        }
        powerscale_module_mock.get_ntp_servers = MagicMock(
            return_value=MockSettingsApi.NTP_SERVERS_MATCHING)
        SettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        second_result = powerscale_module_mock.module.exit_json.call_args[1]
        assert second_result['changed'] is False
        assert powerscale_module_mock.module.exit_json.called is True
        assert powerscale_module_mock.protocol_api.create_ntp_server.call_count == 0
        assert powerscale_module_mock.protocol_api.delete_ntp_server.call_count == 0
