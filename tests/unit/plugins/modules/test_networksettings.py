# Copyright: (c) 2021, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for Network Settings module on PowerScale"""

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


from ansible_collections.dellemc.powerscale.plugins.modules.networksettings import NetworkSettings
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_networksettings_api as MockNetworkSettingsApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException


class TestNetworkSettings():
    get_network_settings_args = {"enable_source_routing": None,
                                 "state": None}

    @pytest.fixture
    def network_settings_module_mock(self, mocker):
        mocker.patch(MockNetworkSettingsApi.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        networksettings_module_mock = NetworkSettings()
        networksettings_module_mock.module = MagicMock()
        return networksettings_module_mock

    def test_get_network_setting(self, network_settings_module_mock):
        self.get_network_settings_args.update({"state": "present"})
        network_settings_module_mock.module.params = self.get_network_settings_args
        network_settings_module_mock.network_api.get_network_external = MagicMock(
            return_value=MockSDKResponse(MockNetworkSettingsApi.GET_NETWORK_SETTINGS))
        network_settings_module_mock.perform_module_operation()
        assert network_settings_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_get_network_settings_with_exception(self, network_settings_module_mock):
        self.get_network_settings_args.update({"state": "present"})
        network_settings_module_mock.module.params = self.get_network_settings_args
        network_settings_module_mock.network_api.get_network_external = MagicMock(side_effect=utils.ApiException)
        network_settings_module_mock.perform_module_operation()
        assert MockNetworkSettingsApi.get_networksettings_failed_msg() in \
            network_settings_module_mock.module.fail_json.call_args[1]['msg']

    def test_modify_network_settings(self, network_settings_module_mock):
        self.get_network_settings_args.update({"state": "present", "enable_source_routing": True})
        network_settings_module_mock.module.params = self.get_network_settings_args
        network_settings_module_mock.network_api.update_network_external = MagicMock(
            return_value=MockSDKResponse(MockNetworkSettingsApi.UPDATE_NETWORK_SETTINGS))
        network_settings_module_mock.perform_module_operation()
        assert network_settings_module_mock.module.exit_json.call_args[1]['changed']

    def test_modify_network_settings_with_exception(self, network_settings_module_mock):
        self.get_network_settings_args.update({"state": "present", "enable_source_routing": True})
        network_settings_module_mock.module.params = self.get_network_settings_args
        network_settings_module_mock.network_api.update_network_external = MagicMock(side_effect=utils.ApiException)
        network_settings_module_mock.perform_module_operation()
        assert MockNetworkSettingsApi.modify_networksettings_failed_msg() in \
            network_settings_module_mock.module.fail_json.call_args[1]['msg']
