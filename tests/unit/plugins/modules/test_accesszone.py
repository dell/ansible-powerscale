# Copyright: (c) 2021, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for access zone module on PowerScale"""

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


from ansible_collections.dellemc.powerscale.plugins.modules.accesszone import AccessZone
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_accesszone_api as MockAccessZoneApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException


class TestAccessZone():
    get_access_zone_args = {"az_name": None,
                            "groupnet": None,
                            "path": None,
                            "state": None,
                            "create_path": None,
                            "provider_state": None,
                            "auth_providers": [{"provider_name": None, "provider_type": None}]}

    @pytest.fixture
    def accesszone_module_mock(self, mocker):
        mocker.patch(MockAccessZoneApi.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        az_module_mock = AccessZone()
        az_module_mock.module = MagicMock()
        return az_module_mock

    def test_create_access_zone_parmset1(self, accesszone_module_mock):
        self.get_access_zone_args.update({"az_name": "testaz",
                                          "groupnet": "groupnet1",
                                          "path": "/ifs",
                                          "smb": None,
                                          "nfs": None,
                                          "force_overlap": True,
                                          "state": "present",
                                          "create_path": False,
                                          "provider_state": "add",
                                          "auth_providers": [{"provider_name": "System", "provider_type": "file"}]})
        accesszone_module_mock.module.params = self.get_access_zone_args
        accesszone_module_mock.get_details = MagicMock(return_value=[])
        accesszone_module_mock.api_instance.create_zone = MagicMock(
            return_value=MockSDKResponse(MockAccessZoneApi.ACCESS_ZONE['access_zone'][0]))
        accesszone_module_mock.perform_module_operation()
        assert accesszone_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_access_zone_parmset2(self, accesszone_module_mock):
        self.get_access_zone_args.update({"az_name": "testaz",
                                          "groupnet": "groupnet1",
                                          "path": "/ifs",
                                          "smb": None,
                                          "nfs": None,
                                          "force_overlap": False,
                                          "state": "present",
                                          "create_path": True,
                                          "provider_state": "add",
                                          "auth_providers": [{"provider_name": "System", "provider_type": "local"}]})
        accesszone_module_mock.module.params = self.get_access_zone_args
        accesszone_module_mock.get_details = MagicMock(return_value=[])
        accesszone_module_mock.api_instance.create_zone = MagicMock(
            return_value=MockSDKResponse(MockAccessZoneApi.ACCESS_ZONE['access_zone'][0]))
        accesszone_module_mock.perform_module_operation()
        assert accesszone_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_access_zone_parmset3(self, accesszone_module_mock):
        self.get_access_zone_args.update({"az_name": "testaz",
                                          "groupnet": "groupnet1",
                                          "path": "/ifs",
                                          "smb": None,
                                          "nfs": None,
                                          "force_overlap": True,
                                          "state": "present",
                                          "create_path": False,
                                          "provider_state": "add",
                                          "auth_providers": [{"provider_name": "nis-server", "provider_type": "nis"}]})
        accesszone_module_mock.module.params = self.get_access_zone_args
        accesszone_module_mock.get_details = MagicMock(return_value=[])
        accesszone_module_mock.api_instance.create_zone = MagicMock(
            return_value=MockSDKResponse(MockAccessZoneApi.ACCESS_ZONE['access_zone'][0]))
        accesszone_module_mock.perform_module_operation()
        assert accesszone_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_access_zone_with_exception(self, accesszone_module_mock):
        self.get_access_zone_args.update({"az_name": "testaz",
                                          "groupnet": "groupnet1",
                                          "path": "/ifs",
                                          "smb": None,
                                          "nfs": None,
                                          "force_overlap": False,
                                          "state": "present",
                                          "create_path": True,
                                          "provider_state": "add",
                                          "auth_providers": [{"provider_name": "System", "provider_type": "file"}]})
        accesszone_module_mock.module.params = self.get_access_zone_args
        accesszone_module_mock.get_details = MagicMock(return_value=[])
        accesszone_module_mock.api_instance.create_zone = MagicMock(side_effect=utils.ApiException)
        accesszone_module_mock.perform_module_operation()
        assert MockAccessZoneApi.create_accesszone_failed_msg(MockAccessZoneApi.ACCESS_ZONE['access_zone'][0]['az_name']) in \
            accesszone_module_mock.module.fail_json.call_args[1]['msg']

    def test_delete_access_zone(self, accesszone_module_mock):
        self.get_access_zone_args.update({"az_name": "testaz",
                                          "groupnet": "groupnet1",
                                          "path": "/ifs",
                                          "smb": None,
                                          "nfs": None,
                                          "force_overlap": True,
                                          "state": "absent",
                                          "create_path": False,
                                          "provider_state": "add",
                                          "auth_providers": [{"provider_name": "System", "provider_type": "file"}]})
        accesszone_module_mock.module.params = self.get_access_zone_args
        accesszone_module_mock.get_details = MagicMock(return_value=MockAccessZoneApi.ACCESS_ZONE)
        accesszone_module_mock.api_instance.delete_zone = MagicMock(return_value=None)
        accesszone_module_mock.perform_module_operation()
        accesszone_module_mock.api_instance.delete_zone.assert_called()
        assert accesszone_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_access_zone_exception(self, accesszone_module_mock):
        self.get_access_zone_args.update({"az_name": "testaz",
                                          "groupnet": "groupnet1",
                                          "path": "/ifs",
                                          "smb": None,
                                          "nfs": None,
                                          "force_overlap": True,
                                          "state": "absent",
                                          "create_path": False,
                                          "provider_state": "add",
                                          "auth_providers": [{"provider_name": "System", "provider_type": "file"}]})
        accesszone_module_mock.module.params = self.get_access_zone_args
        accesszone_module_mock.get_details = MagicMock(return_value=MockAccessZoneApi.ACCESS_ZONE)
        accesszone_module_mock.api_instance.delete_zone = MagicMock(side_effect=utils.ApiException)
        accesszone_module_mock.perform_module_operation()
        accesszone_module_mock.api_instance.delete_zone.assert_called()
        assert MockAccessZoneApi.delete_accesszone_failed_msg() in \
            accesszone_module_mock.module.fail_json.call_args[1]['msg']
