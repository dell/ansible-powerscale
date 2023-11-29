# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

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
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_fail_json \
    import FailJsonException, fail_json


class TestNfsDefaultSettings():
    nfsdefaultsettings_args = MockNfsDefaultSettingsApi.NFS_DEFAULT_SETTINGS_COMMON_ARGS

    @pytest.fixture
    def nfsdefaultsettings_module_mock(self, mocker):
        mocker.patch(MockNfsDefaultSettingsApi.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        nfsdefaultsettings_module_mock = NFSDefaultSettings()
        nfsdefaultsettings_module_mock.module.check_mode = False
        nfsdefaultsettings_module_mock.module.fail_json = fail_json
        return nfsdefaultsettings_module_mock

    def test_get_nfsdefaultsettings(self, nfsdefaultsettings_module_mock):
        nfsdefaultsettings_details = MockNfsDefaultSettingsApi.GET_NFSDEFAULTSETTINGS_RESPONSE
        nfsdefaultsettings_module_mock.module.params = self.nfsdefaultsettings_args
        Protocol.get_nfs_default_settings = MagicMock(return_value=nfsdefaultsettings_details)
        NFSDefaultSettingsHandler().handle(nfsdefaultsettings_module_mock)
        assert nfsdefaultsettings_module_mock.module.exit_json.call_args[1]['changed'] is False

    def capture_fail_json_call(self, error_msg, nfsdefaultsettings_module_mock):
        try:
            NFSDefaultSettingsHandler().handle(nfsdefaultsettings_module_mock)
        except FailJsonException as fj_object:
            assert error_msg == fj_object.message

    def test_update_nfsdefaultsettings_for_map_dict(self, nfsdefaultsettings_module_mock):
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
        nfsdefaultsettings_module_mock.module.params = self.nfsdefaultsettings_args
        Protocol.get_nfs_default_settings = MagicMock(return_value=nfsdefaultsettings_details)
        NFSDefaultSettingsHandler().handle(nfsdefaultsettings_module_mock)
        assert nfsdefaultsettings_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_update_nfsdefaultsettings_for_map_dict_two(self, nfsdefaultsettings_module_mock):
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
        nfsdefaultsettings_module_mock.module.params = self.nfsdefaultsettings_args
        Protocol.get_nfs_default_settings = MagicMock(return_value=nfsdefaultsettings_details)
        NFSDefaultSettingsHandler().handle(nfsdefaultsettings_module_mock)
        assert nfsdefaultsettings_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_update_nfsdefaultsettings_for_size_dict(self, nfsdefaultsettings_module_mock):
        nfsdefaultsettings_details = MockNfsDefaultSettingsApi.GET_NFSDEFAULTSETTINGS_RESPONSE
        self.nfsdefaultsettings_args.update({
            "max_file_size": {
                "size_value": 1000,
                "size_unit": "KB"
            }
        })
        nfsdefaultsettings_module_mock.module.params = self.nfsdefaultsettings_args
        Protocol.get_nfs_default_settings = MagicMock(return_value=nfsdefaultsettings_details)
        NFSDefaultSettingsHandler().handle(nfsdefaultsettings_module_mock)
        assert nfsdefaultsettings_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_update_nfsdefaultsettings_for_time_dict(self, nfsdefaultsettings_module_mock):
        nfsdefaultsettings_details = MockNfsDefaultSettingsApi.GET_NFSDEFAULTSETTINGS_RESPONSE
        self.nfsdefaultsettings_args.update({
            "time_delta": {
                "time_value": 1000,
                "time_unit": "seconds"
            }
        })
        nfsdefaultsettings_module_mock.module.params = self.nfsdefaultsettings_args
        Protocol.get_nfs_default_settings = MagicMock(return_value=nfsdefaultsettings_details)
        NFSDefaultSettingsHandler().handle(nfsdefaultsettings_module_mock)
        assert nfsdefaultsettings_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_update_nfsdefaultsettings_for_security_dict(self, nfsdefaultsettings_module_mock):
        nfsdefaultsettings_details = MockNfsDefaultSettingsApi.GET_NFSDEFAULTSETTINGS_RESPONSE
        self.nfsdefaultsettings_args.update({
            "security_flavors": [
                'kerberos_integrity'
            ]
        })
        nfsdefaultsettings_module_mock.module.params = self.nfsdefaultsettings_args
        Protocol.get_nfs_default_settings = MagicMock(return_value=nfsdefaultsettings_details)
        NFSDefaultSettingsHandler().handle(nfsdefaultsettings_module_mock)
        assert nfsdefaultsettings_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_update_nfsdefaultsettings_for_bool_dict(self, nfsdefaultsettings_module_mock):
        nfsdefaultsettings_details = MockNfsDefaultSettingsApi.GET_NFSDEFAULTSETTINGS_RESPONSE
        self.nfsdefaultsettings_args.update({
            'commit_asynchronous': True
        })
        nfsdefaultsettings_module_mock.module.params = self.nfsdefaultsettings_args
        Protocol.get_nfs_default_settings = MagicMock(return_value=nfsdefaultsettings_details)
        NFSDefaultSettingsHandler().handle(nfsdefaultsettings_module_mock)
        assert nfsdefaultsettings_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_update_nfsdefaultsettings_for_bool_dict_exception(self, nfsdefaultsettings_module_mock):
        nfsdefaultsettings_details = MockNfsDefaultSettingsApi.GET_NFSDEFAULTSETTINGS_RESPONSE
        self.nfsdefaultsettings_args.update({
            'commit_asynchronous': True
        })
        nfsdefaultsettings_module_mock.module.params = self.nfsdefaultsettings_args
        Protocol.get_nfs_default_settings = MagicMock(return_value=nfsdefaultsettings_details)
        nfsdefaultsettings_module_mock.protocol_api.update_nfs_settings_export = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(MockNfsDefaultSettingsApi.get_nfsdefaultsettings_exception_response('update_exception'),
                                    nfsdefaultsettings_module_mock)

    def test_update_nfsdefaultsettings_form_modify_exception(self, nfsdefaultsettings_module_mock):
        nfsdefaultsettings_details = MockNfsDefaultSettingsApi.GET_NFSDEFAULTSETTINGS_RESPONSE
        nfsdefaultsettings_module_mock.module.params = self.nfsdefaultsettings_args
        Protocol.get_nfs_default_settings = MagicMock(return_value=nfsdefaultsettings_details)
        nfsdefaultsettings_module_mock.form_map_dict = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(MockNfsDefaultSettingsApi.get_nfsdefaultsettings_exception_response('form_dict_exception'),
                                    nfsdefaultsettings_module_mock)
