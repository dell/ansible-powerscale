# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

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
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_fail_json \
    import FailJsonException, fail_json


class TestNFSZoneSettings():
    nfs_settings_args = MockNFSZoneSettingsApi.ZONE_SETTINGS_COMMON_ARGS

    @pytest.fixture
    def nfs_settings_module_mock(self, mocker):
        mocker.patch(MockNFSZoneSettingsApi.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        nfs_settings_module_mock = NFSZoneSettings()
        nfs_settings_module_mock.module.check_mode = False
        nfs_settings_module_mock.module.fail_json = fail_json
        return nfs_settings_module_mock

    def capture_fail_json_call(self, error_msg, nfs_settings_module_mock):
        try:
            NFSZoneSettingsHandler().handle(nfs_settings_module_mock, nfs_settings_module_mock.module.params)
        except FailJsonException as fj_object:
            assert error_msg in fj_object.message

    def test_get_nfs_zone_settings(self, nfs_settings_module_mock):
        self.nfs_settings_args.update({
            "access_zone": MockNFSZoneSettingsApi.ZONE
        })
        nfs_settings_module_mock.module.params = self.nfs_settings_args
        NFSZoneSettingsHandler().handle(nfs_settings_module_mock, nfs_settings_module_mock.module.params)
        assert nfs_settings_module_mock.module.exit_json.call_args[1]['changed'] is False
        nfs_settings_module_mock.protocol_api.get_nfs_settings_zone.assert_called()

    def test_get_nfs_zone_settings_exception(self, nfs_settings_module_mock):
        self.nfs_settings_args.update({
            "access_zone": MockNFSZoneSettingsApi.ZONE
        })
        nfs_settings_module_mock.module.params = self.nfs_settings_args
        nfs_settings_module_mock.protocol_api.get_nfs_settings_zone = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockNFSZoneSettingsApi.zone_settings_exception(
                response_type="get_settings_exception"), nfs_settings_module_mock)

    def test_update_nfs_zone_settings(self, nfs_settings_module_mock):
        self.nfs_settings_args.update({
            "access_zone": MockNFSZoneSettingsApi.ZONE,
            "nfsv4_allow_numeric_ids": False,
            "nfsv4_domain": MockNFSZoneSettingsApi.NFS_DOMAIN,
            "nfsv4_no_domain": False,
            "nfsv4_no_domain_uids": False,
            "nfsv4_no_names": False,
            "nfsv4_replace_domain": False
        })
        nfs_settings_module_mock.module.params = self.nfs_settings_args
        nfs_settings_module_mock.protocol_api.get_nfs_settings_zone.to_dict = MagicMock(
            return_value=MockNFSZoneSettingsApi.GET_NFS_ZONE_SETTINGS_RESPONSE)
        NFSZoneSettingsHandler().handle(nfs_settings_module_mock, nfs_settings_module_mock.module.params)
        assert nfs_settings_module_mock.module.exit_json.call_args[1]['changed'] is True
        nfs_settings_module_mock.protocol_api.update_nfs_settings_zone.assert_called()

    def test_update_nfs_zone_settings_exception(self, nfs_settings_module_mock):
        self.nfs_settings_args.update({
            "access_zone": MockNFSZoneSettingsApi.ZONE,
            "nfsv4_allow_numeric_ids": False,
            "nfsv4_domain": MockNFSZoneSettingsApi.NFS_DOMAIN,
            "nfsv4_no_domain": False,
            "nfsv4_no_domain_uids": False,
            "nfsv4_no_names": False,
            "nfsv4_replace_domain": False
        })
        nfs_settings_module_mock.module.params = self.nfs_settings_args
        nfs_settings_module_mock.protocol_api.get_nfs_settings_zone.to_dict = MagicMock(
            return_value=MockNFSZoneSettingsApi.GET_NFS_ZONE_SETTINGS_RESPONSE)
        nfs_settings_module_mock.protocol_api.update_nfs_settings_zone = MagicMock(
            side_effect=MockApiException
        )
        self.capture_fail_json_call(
            MockNFSZoneSettingsApi.zone_settings_exception(
                response_type="update_zone_settings_exception"),
            nfs_settings_module_mock)

    def test_prepare_zone_settings_modify_object_exception(self, nfs_settings_module_mock):
        self.nfs_settings_args.update({
            "access_zone": MockNFSZoneSettingsApi.ZONE,
            "nfsv4_allow_numeric_ids": False,
            "nfsv4_domain": MockNFSZoneSettingsApi.NFS_DOMAIN,
            "nfsv4_no_domain": False,
            "nfsv4_no_domain_uids": False,
            "nfsv4_no_names": False,
            "nfsv4_replace_domain": False
        })
        nfs_settings_module_mock.module.params = self.nfs_settings_args
        nfs_settings_module_mock.protocol_api.get_nfs_settings_zone.to_dict = MagicMock(
            return_value=MockNFSZoneSettingsApi.GET_NFS_ZONE_SETTINGS_RESPONSE)
        nfs_settings_module_mock.isi_sdk.NfsSettingsZoneSettings = MagicMock(
            side_effect=MockApiException
        )
        self.capture_fail_json_call(
            MockNFSZoneSettingsApi.zone_settings_exception(
                response_type="prepare_zone_settings_object_exception"),
            nfs_settings_module_mock)

    def test_get_nfs_zone_settings_invalid_az_exception(self, nfs_settings_module_mock):
        self.nfs_settings_args.update({
            "access_zone": "invalid zone",
        })
        nfs_settings_module_mock.module.params = self.nfs_settings_args
        self.capture_fail_json_call(
            MockNFSZoneSettingsApi.zone_settings_exception(
                response_type="invalid_zone_exception"),
            nfs_settings_module_mock)
