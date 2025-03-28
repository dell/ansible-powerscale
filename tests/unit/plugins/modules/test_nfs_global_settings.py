# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase


class TestNFSGlobalSettings(PowerScaleUnitBase):
    nfs_global_args = MockNFSGlobalSettingsApi.NFS_GLOBAL_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return NFSGlobalSettings

    def test_get_nfs_global_details(self, powerscale_module_mock):
        self.nfs_global_args.update({
        })
        powerscale_module_mock.module.params = self.nfs_global_args
        NFSGlobalSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.get_nfs_settings_global.assert_called()

    def test_get_nfs_global_details_exception(self, powerscale_module_mock):
        self.nfs_global_args.update({})
        powerscale_module_mock.module.params = self.nfs_global_args
        powerscale_module_mock.protocol_api.get_nfs_settings_global = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockNFSGlobalSettingsApi.get_nfs_global_settings_exception_response('get_details_exception'),
            NFSGlobalSettingsHandler)

    def test_modify_nfs_global_response(self, powerscale_module_mock):
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
        powerscale_module_mock.module.params = self.nfs_global_args
        powerscale_module_mock.get_nfs_global_settings_details = MagicMock(
            return_value=MockNFSGlobalSettingsApi.GET_NFS_GLOBAL_RESPONSE)
        NFSGlobalSettingsHandler().handle(powerscale_module_mock,
                                          powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.update_nfs_settings_global.assert_called()

    def test_modify_nfs_global_exception(self, powerscale_module_mock):
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
        powerscale_module_mock.module.params = self.nfs_global_args
        powerscale_module_mock.get_nfs_global_settings_details = MagicMock(
            return_value=MockNFSGlobalSettingsApi.GET_NFS_GLOBAL_RESPONSE)
        powerscale_module_mock.protocol_api.update_nfs_settings_global = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockNFSGlobalSettingsApi.get_nfs_global_settings_exception_response('update_exception'),
            NFSGlobalSettingsHandler)
