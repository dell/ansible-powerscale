# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for NFS Zone Settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.nfs_zone_settings \
    import NFSZoneSettings
from ansible_collections.dellemc.powerscale.plugins.modules.nfs_zone_settings \
    import NFSZoneSettingsHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_nfs_zone_settings \
    import MockNFSZoneSettingsApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase


class TestNFSZoneSettings(PowerScaleUnitBase):
    nfs_settings_args = MockNFSZoneSettingsApi.ZONE_SETTINGS_COMMON_ARGS

    @pytest.fixture
    def module_object(self, mocker):
        return NFSZoneSettings

    def test_get_nfs_zone_settings(self, powerscale_module_mock):
        self.nfs_settings_args.update({
            "access_zone": MockNFSZoneSettingsApi.ZONE
        })
        powerscale_module_mock.module.params = self.nfs_settings_args
        NFSZoneSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False
        powerscale_module_mock.protocol_api.get_nfs_settings_zone.assert_called()

    def test_get_nfs_zone_settings_exception(self, powerscale_module_mock):
        self.nfs_settings_args.update({
            "access_zone": MockNFSZoneSettingsApi.ZONE
        })
        powerscale_module_mock.module.params = self.nfs_settings_args
        powerscale_module_mock.protocol_api.get_nfs_settings_zone = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockNFSZoneSettingsApi.zone_settings_exception(
                response_type="get_settings_exception"), NFSZoneSettingsHandler)

    def test_update_nfs_zone_settings(self, powerscale_module_mock):
        self.nfs_settings_args.update({
            "access_zone": MockNFSZoneSettingsApi.ZONE,
            "nfsv4_allow_numeric_ids": False,
            "nfsv4_domain": MockNFSZoneSettingsApi.NFS_DOMAIN,
            "nfsv4_no_domain": False,
            "nfsv4_no_domain_uids": False,
            "nfsv4_no_names": False,
            "nfsv4_replace_domain": False
        })
        powerscale_module_mock.module.params = self.nfs_settings_args
        powerscale_module_mock.protocol_api.get_nfs_settings_zone.to_dict = MagicMock(
            return_value=MockNFSZoneSettingsApi.GET_NFS_ZONE_SETTINGS_RESPONSE)
        NFSZoneSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.update_nfs_settings_zone.assert_called()

    def test_update_nfs_zone_settings_exception(self, powerscale_module_mock):
        self.nfs_settings_args.update({
            "access_zone": MockNFSZoneSettingsApi.ZONE,
            "nfsv4_allow_numeric_ids": False,
            "nfsv4_domain": MockNFSZoneSettingsApi.NFS_DOMAIN,
            "nfsv4_no_domain": False,
            "nfsv4_no_domain_uids": False,
            "nfsv4_no_names": False,
            "nfsv4_replace_domain": False
        })
        powerscale_module_mock.module.params = self.nfs_settings_args
        powerscale_module_mock.protocol_api.get_nfs_settings_zone.to_dict = MagicMock(
            return_value=MockNFSZoneSettingsApi.GET_NFS_ZONE_SETTINGS_RESPONSE)
        powerscale_module_mock.protocol_api.update_nfs_settings_zone = MagicMock(
            side_effect=MockApiException
        )
        self.capture_fail_json_call(
            MockNFSZoneSettingsApi.zone_settings_exception(
                response_type="update_zone_settings_exception"),
            NFSZoneSettingsHandler)

    def test_prepare_zone_settings_modify_object_exception(self, powerscale_module_mock):
        self.nfs_settings_args.update({
            "access_zone": MockNFSZoneSettingsApi.ZONE,
            "nfsv4_allow_numeric_ids": False,
            "nfsv4_domain": MockNFSZoneSettingsApi.NFS_DOMAIN,
            "nfsv4_no_domain": False,
            "nfsv4_no_domain_uids": False,
            "nfsv4_no_names": False,
            "nfsv4_replace_domain": False
        })
        powerscale_module_mock.module.params = self.nfs_settings_args
        powerscale_module_mock.protocol_api.get_nfs_settings_zone.to_dict = MagicMock(
            return_value=MockNFSZoneSettingsApi.GET_NFS_ZONE_SETTINGS_RESPONSE)
        powerscale_module_mock.isi_sdk.NfsSettingsZoneSettings = MagicMock(
            side_effect=MockApiException
        )
        self.capture_fail_json_call(
            MockNFSZoneSettingsApi.zone_settings_exception(
                response_type="prepare_zone_settings_object_exception"),
            NFSZoneSettingsHandler)

    def test_get_nfs_zone_settings_invalid_az_exception(self, powerscale_module_mock):
        self.nfs_settings_args.update({
            "access_zone": "invalid zone",
        })
        powerscale_module_mock.module.params = self.nfs_settings_args
        self.capture_fail_json_call(
            MockNFSZoneSettingsApi.zone_settings_exception(
                response_type="invalid_zone_exception"),
            NFSZoneSettingsHandler)
