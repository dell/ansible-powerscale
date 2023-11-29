# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for NFS global settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.nfs_global_settings import NFSGlobalSettings
from ansible_collections.dellemc.powerscale.plugins.modules.nfs_global_settings import NFSGlobalSettingsHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_nfs_global_settings_api \
    import MockNFSGlobalSettingsApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_fail_json \
    import FailJsonException, fail_json


class TestNFSGlobalSettings():
    nfs_global_args = MockNFSGlobalSettingsApi.NFS_GLOBAL_COMMON_ARGS

    @pytest.fixture
    def nfs_global_module_mock(self, mocker):
        mocker.patch(MockNFSGlobalSettingsApi.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        nfs_global_module_mock = NFSGlobalSettings()
        nfs_global_module_mock.module.check_mode = False
        nfs_global_module_mock.module.fail_json = fail_json
        return nfs_global_module_mock

    def capture_fail_json_call(self, error_msg, nfs_global_module_mock):
        try:
            NFSGlobalSettingsHandler().handle(nfs_global_module_mock, nfs_global_module_mock.module.params)
        except FailJsonException as fj_object:
            assert error_msg in fj_object.message

    def test_get_nfs_global_details(self, nfs_global_module_mock):
        self.nfs_global_args.update({
        })
        nfs_global_module_mock.module.params = self.nfs_global_args
        NFSGlobalSettingsHandler().handle(nfs_global_module_mock, nfs_global_module_mock.module.params)
        nfs_global_module_mock.protocol_api.get_nfs_settings_global.assert_called()

    def test_get_nfs_global_details_exception(self, nfs_global_module_mock):
        self.nfs_global_args.update({})
        nfs_global_module_mock.module.params = self.nfs_global_args
        nfs_global_module_mock.protocol_api.get_nfs_settings_global = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockNFSGlobalSettingsApi.get_nfs_global_settings_exception_response('get_details_exception'), nfs_global_module_mock)

    def test_modify_nfs_global_response(self, nfs_global_module_mock):
        self.nfs_global_args.update({
            "service": True,
            "nfsv3": {"nfsv3_enabled": True, "nfsv3_rdma_enabled": None},
            "nfsv4": {
                "nfsv4_enabled": True,
                "nfsv40_enabled": False,
                "nfsv41_enabled": None,
                "nfsv42_enabled": True
            }
        })
        nfs_global_module_mock.module.params = self.nfs_global_args
        nfs_global_module_mock.get_nfs_global_settings_details = MagicMock(
            return_value=MockNFSGlobalSettingsApi.GET_NFS_GLOBAL_RESPONSE)
        NFSGlobalSettingsHandler().handle(nfs_global_module_mock,
                                          nfs_global_module_mock.module.params)
        assert nfs_global_module_mock.module.exit_json.call_args[1]['changed'] is True
        nfs_global_module_mock.protocol_api.update_nfs_settings_global.assert_called()

    def test_modify_nfs_global_exception(self, nfs_global_module_mock):
        self.nfs_global_args.update({
            "service": True,
            "nfsv3": {"nfsv3_enabled": True, "nfsv3_rdma_enabled": None},
            "nfsv4": {
                "nfsv4_enabled": True,
                "nfsv40_enabled": False,
                "nfsv41_enabled": None,
                "nfsv42_enabled": True
            }
        })
        nfs_global_module_mock.module.params = self.nfs_global_args
        nfs_global_module_mock.get_nfs_global_settings_details = MagicMock(
            return_value=MockNFSGlobalSettingsApi.GET_NFS_GLOBAL_RESPONSE)
        nfs_global_module_mock.protocol_api.update_nfs_settings_global = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockNFSGlobalSettingsApi.get_nfs_global_settings_exception_response('update_exception'), nfs_global_module_mock)
