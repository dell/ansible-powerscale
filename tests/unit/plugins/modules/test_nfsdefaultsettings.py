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

from ansible_collections.dellemc.powerscale.plugins.modules.nfs_default_settings import NFSDefaultSettings
from ansible_collections.dellemc.powerscale.plugins.modules.nfs_default_settings import NFSDefaultSettingsHandler
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.protocol \
    import Protocol
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_nfsdefaultsettings_api \
    import MockNfsDefaultSettingsApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase


class TestNfsDefaultSettings(PowerScaleUnitBase):
    nfsdefaultsettings_args = MockNfsDefaultSettingsApi.NFS_DEFAULT_SETTINGS_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return NFSDefaultSettings

    def capture_fail_json_call(self, error_msg, nfsdefaultsettings_module_mock):
        with pytest.raises(SystemExit):
            NFSDefaultSettingsHandler().handle(nfsdefaultsettings_module_mock)
        self.powerscale_module_mock.module.fail_json.assert_called()
        call_args = self.powerscale_module_mock.module.fail_json.call_args.kwargs
        assert error_msg in call_args['msg']

    def test_get_nfsdefaultsettings(self, powerscale_module_mock):
        nfsdefaultsettings_details = MockNfsDefaultSettingsApi.GET_NFSDEFAULTSETTINGS_RESPONSE
        powerscale_module_mock.module.params = self.nfsdefaultsettings_args
        Protocol.get_nfs_default_settings = MagicMock(return_value=nfsdefaultsettings_details)
        NFSDefaultSettingsHandler().handle(powerscale_module_mock)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_update_nfsdefaultsettings_for_map_dict(self, powerscale_module_mock):
        nfsdefaultsettings_details = MockNfsDefaultSettingsApi.GET_NFSDEFAULTSETTINGS_RESPONSE
        self.nfsdefaultsettings_args.update({
            'map_root': {
                "enabled": True,
                "primary_group": "test_user",
                "secondary_groups": [
                    {
                        "name": "test_group",
                        "state": "present"
                    }
                ],
                "user": "test_user_2"
            }
        })
        powerscale_module_mock.module.params = self.nfsdefaultsettings_args
        Protocol.get_nfs_default_settings = MagicMock(return_value=nfsdefaultsettings_details)
        NFSDefaultSettingsHandler().handle(powerscale_module_mock)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_update_nfsdefaultsettings_for_map_dict_two(self, powerscale_module_mock):
        nfsdefaultsettings_details = MockNfsDefaultSettingsApi.GET_NFSDEFAULTSETTINGS_RESPONSE
        nfsdefaultsettings_details['map_root']['enabled'] = True
        self.nfsdefaultsettings_args.update({
            'map_root': {
                "enabled": False,
                "secondary_groups": [
                    {
                        "name": "test_group",
                        "state": "absent"
                    }
                ],
            },
            'file_name_max_size': {
                "size_value": 1000,
                "size_unit": "KB"
            }
        })
        powerscale_module_mock.module.params = self.nfsdefaultsettings_args
        Protocol.get_nfs_default_settings = MagicMock(return_value=nfsdefaultsettings_details)
        NFSDefaultSettingsHandler().handle(powerscale_module_mock)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_update_nfsdefaultsettings_for_size_dict(self, powerscale_module_mock):
        nfsdefaultsettings_details = MockNfsDefaultSettingsApi.GET_NFSDEFAULTSETTINGS_RESPONSE
        self.nfsdefaultsettings_args.update({
            "max_file_size": {
                "size_value": 1000,
                "size_unit": "KB"
            }
        })
        powerscale_module_mock.module.params = self.nfsdefaultsettings_args
        Protocol.get_nfs_default_settings = MagicMock(return_value=nfsdefaultsettings_details)
        NFSDefaultSettingsHandler().handle(powerscale_module_mock)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_update_nfsdefaultsettings_for_time_dict(self, powerscale_module_mock):
        nfsdefaultsettings_details = MockNfsDefaultSettingsApi.GET_NFSDEFAULTSETTINGS_RESPONSE
        self.nfsdefaultsettings_args.update({
            "time_delta": {
                "time_value": 1000,
                "time_unit": "seconds"
            }
        })
        powerscale_module_mock.module.params = self.nfsdefaultsettings_args
        Protocol.get_nfs_default_settings = MagicMock(return_value=nfsdefaultsettings_details)
        NFSDefaultSettingsHandler().handle(powerscale_module_mock)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_update_nfsdefaultsettings_for_security_dict(self, powerscale_module_mock):
        nfsdefaultsettings_details = MockNfsDefaultSettingsApi.GET_NFSDEFAULTSETTINGS_RESPONSE
        self.nfsdefaultsettings_args.update({
            "security_flavors": [
                'kerberos_integrity'
            ]
        })
        powerscale_module_mock.module.params = self.nfsdefaultsettings_args
        Protocol.get_nfs_default_settings = MagicMock(return_value=nfsdefaultsettings_details)
        NFSDefaultSettingsHandler().handle(powerscale_module_mock)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_update_nfsdefaultsettings_for_bool_dict(self, powerscale_module_mock):
        nfsdefaultsettings_details = MockNfsDefaultSettingsApi.GET_NFSDEFAULTSETTINGS_RESPONSE
        self.nfsdefaultsettings_args.update({
            'commit_asynchronous': True
        })
        powerscale_module_mock.module.params = self.nfsdefaultsettings_args
        Protocol.get_nfs_default_settings = MagicMock(return_value=nfsdefaultsettings_details)
        NFSDefaultSettingsHandler().handle(powerscale_module_mock)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_update_nfsdefaultsettings_for_bool_dict_exception(self, powerscale_module_mock):
        nfsdefaultsettings_details = MockNfsDefaultSettingsApi.GET_NFSDEFAULTSETTINGS_RESPONSE
        self.nfsdefaultsettings_args.update({
            'commit_asynchronous': True
        })
        powerscale_module_mock.module.params = self.nfsdefaultsettings_args
        Protocol.get_nfs_default_settings = MagicMock(return_value=nfsdefaultsettings_details)
        powerscale_module_mock.protocol_api.update_nfs_settings_export = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(MockNfsDefaultSettingsApi.get_nfsdefaultsettings_exception_response('update_exception'),
                                    powerscale_module_mock)

    def test_update_nfsdefaultsettings_form_modify_exception(self, powerscale_module_mock):
        nfsdefaultsettings_details = MockNfsDefaultSettingsApi.GET_NFSDEFAULTSETTINGS_RESPONSE
        powerscale_module_mock.module.params = self.nfsdefaultsettings_args
        Protocol.get_nfs_default_settings = MagicMock(return_value=nfsdefaultsettings_details)
        powerscale_module_mock.form_map_dict = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(MockNfsDefaultSettingsApi.get_nfsdefaultsettings_exception_response('form_dict_exception'),
                                    powerscale_module_mock)
