# Copyright: (c) 2022-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for NFS alias module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import patch, MagicMock
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils


from ansible_collections.dellemc.powerscale.plugins.modules.nfs_alias import NfsAlias
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_nfs_alias_api as MockNfsAliasApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase


class TestNfsAlias(PowerScaleUnitBase):
    get_nfs_alias_args = {"nfs_alias_name": None,
                          "path": None,
                          "access_zone": 'System',
                          "scope": None,
                          "check": None,
                          "direction": None,
                          "resume": None,
                          "limit": None,
                          "sort": None,
                          "new_alias_name": None}
    nfs_alias_name_1 = "/test_alias_1"

    @pytest.fixture
    def module_object(self, mocker):
        return NfsAlias

    def test_get_nfs_alias_by_name_response(self, powerscale_module_mock):
        self.get_nfs_alias_args.update({"nfs_alias_name": self.nfs_alias_name_1,
                                        "state": "present"})
        powerscale_module_mock.module.params = self.get_nfs_alias_args
        powerscale_module_mock.protocol_api.get_nfs_alias = MagicMock(
            return_value=MockSDKResponse(MockNfsAliasApi.NFS_ALIAS))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.protocol_api.get_nfs_alias.assert_called()

    def test_get_nfs_alias_by_name_404_exception(self, powerscale_module_mock):
        self.get_nfs_alias_args.update({"nfs_alias_name": self.nfs_alias_name_1,
                                        "path": "/ifs",
                                        "state": "present"})
        powerscale_module_mock.module.params = self.get_nfs_alias_args
        with patch.object(
                powerscale_module_mock.protocol_api, 'get_nfs_alias', side_effect=MockApiException(404)):
            powerscale_module_mock.perform_module_operation()
            powerscale_module_mock.protocol_api.get_nfs_alias.assert_called()

    def test_get_nfs_alias_by_name_422_exception(self, powerscale_module_mock):
        self.get_nfs_alias_args.update({"nfs_alias_name": self.nfs_alias_name_1,
                                        "state": "present"})
        powerscale_module_mock.module.params = self.get_nfs_alias_args
        with patch.object(
                powerscale_module_mock.protocol_api, 'get_nfs_alias', side_effect=MockApiException(422)):
            self.capture_fail_json_call(MockNfsAliasApi.get_nfs_alias_failure_msg(), invoke_perform_module=True)

    def test_create_nfs_alias_response(self, powerscale_module_mock):
        self.get_nfs_alias_args.update({"nfs_alias_name": self.nfs_alias_name_1,
                                        "path": "/ifs",
                                        "access_zone": "sample-zone",
                                        "state": "present"})
        powerscale_module_mock.module.params = self.get_nfs_alias_args
        powerscale_module_mock.protocol_api.get_nfs_alias = MagicMock(side_effect=MockApiException(404))
        powerscale_module_mock.isi_sdk.NfsAliasCreateParams = MagicMock(
            return_value=MockSDKResponse(MockNfsAliasApi.CREATE_NFS_ALIAS_PARAMS))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.protocol_api.create_nfs_alias.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_nfs_alias_name_with_space(self, powerscale_module_mock):
        self.get_nfs_alias_args.update({"nfs_alias_name": "/sample alias",
                                        "new_alias_name": "/renamed_alias",
                                        "path": "/ifs",
                                        "state": "present"})
        powerscale_module_mock.module.params = self.get_nfs_alias_args
        powerscale_module_mock.protocol_api.get_nfs_alias = MagicMock(return_value=None)
        powerscale_module_mock.isi_sdk.NfsAliasCreateParams = MagicMock(
            return_value=MockSDKResponse(MockNfsAliasApi.CREATE_NFS_ALIAS_PARAMS))
        self.capture_fail_json_call(MockNfsAliasApi.space_in_nfs_alias_name_msg(), invoke_perform_module=True)

    def test_create_nfs_alias_name_with_new_alias_name(self, powerscale_module_mock):
        self.get_nfs_alias_args.update({"nfs_alias_name": self.nfs_alias_name_1,
                                        "new_alias_name": "renamed_alias",
                                        "path": "/ifs",
                                        "state": "present"})
        powerscale_module_mock.module.params = self.get_nfs_alias_args
        powerscale_module_mock.protocol_api.get_nfs_alias = MagicMock(side_effect=MockApiException(404))
        powerscale_module_mock.isi_sdk.NfsAliasCreateParams = MagicMock(
            return_value=MockSDKResponse(MockNfsAliasApi.CREATE_NFS_ALIAS_PARAMS))
        self.capture_fail_json_call(MockNfsAliasApi.new_alias_name_when_creation_msg(), invoke_perform_module=True)

    def test_create_nfs_alias_exception(self, powerscale_module_mock):
        self.get_nfs_alias_args.update({"nfs_alias_name": self.nfs_alias_name_1,
                                        "path": "/ifs",
                                        "state": "present"})
        powerscale_module_mock.module.params = self.get_nfs_alias_args
        powerscale_module_mock.protocol_api.get_nfs_alias = MagicMock(return_value=None)
        powerscale_module_mock.isi_sdk.NfsAliasCreateParams = MagicMock(
            return_value=MockNfsAliasApi.NFS_ALIAS)
        powerscale_module_mock.protocol_api.create_nfs_alias = MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNfsAliasApi.create_nfs_alias_failed_msg(), invoke_perform_module=True)

    def test_create_nfs_alias_no_name_exception(self, powerscale_module_mock):
        self.get_nfs_alias_args.update({"path": "/ifs",
                                        "state": "present"})
        powerscale_module_mock.module.params = self.get_nfs_alias_args
        powerscale_module_mock.protocol_api.get_nfs_alias = MagicMock(side_effect=MockApiException(404))
        powerscale_module_mock.isi_sdk.NfsAliasCreateParams = MagicMock(
            return_value=MockNfsAliasApi.NFS_ALIAS)
        self.capture_fail_json_call(MockNfsAliasApi.empty_nfs_alias_name_msg(), invoke_perform_module=True)

    def test_modify_nfs_alias_response(self, powerscale_module_mock):
        self.get_nfs_alias_args.update({"nfs_alias_name": self.nfs_alias_name_1,
                                        "new_alias_name": "/Renamed_test_alias_1",
                                        "path": "/ifs/Test/sample1",
                                        "state": "present"})

        powerscale_module_mock.module.params = self.get_nfs_alias_args
        powerscale_module_mock.protocol_api.get_nfs_alias.to_dict = MagicMock(
            return_value=MockNfsAliasApi.NFS_ALIAS)
        powerscale_module_mock.isi_sdk.NfsAlias = MagicMock(
            return_value=MockSDKResponse(MockNfsAliasApi.MODIFY_NFS_ALIAS_PARAMS))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.protocol_api.update_nfs_alias.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_nfs_alias_exception(self, powerscale_module_mock):
        self.get_nfs_alias_args.update({"nfs_alias_name": self.nfs_alias_name_1,
                                        "new_alias_name": "/Renamed_test_alias_1",
                                        "path": "/ifs/Test/sample1",
                                        "state": "present"})
        powerscale_module_mock.module.params = self.get_nfs_alias_args
        powerscale_module_mock.protocol_api.get_nfs_alias.to_dict = MagicMock(
            return_value=MockNfsAliasApi.NFS_ALIAS)
        powerscale_module_mock.isi_sdk.NfsAlias = MagicMock(
            return_value=MockSDKResponse(MockNfsAliasApi.MODIFY_NFS_ALIAS_PARAMS))
        powerscale_module_mock.protocol_api.update_nfs_alias = MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNfsAliasApi.modify_nfs_alias_failed_msg(), invoke_perform_module=True)

    def test_delete_nfs_alias_by_name_response(self, powerscale_module_mock):
        self.get_nfs_alias_args.update({"nfs_alias_name": self.nfs_alias_name_1,
                                        "state": "absent"})
        powerscale_module_mock.module.params = self.get_nfs_alias_args
        powerscale_module_mock.protocol_api.get_nfs_alias.to_dict = MagicMock(
            return_value=MockNfsAliasApi.NFS_ALIAS)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.protocol_api.delete_nfs_alias.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
