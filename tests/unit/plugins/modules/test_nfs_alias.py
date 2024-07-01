# Copyright: (c) 2022, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for NFS alias module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils


from ansible_collections.dellemc.powerscale.plugins.modules.nfs_alias import NfsAlias
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_nfs_alias_api as MockNfsAliasApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException


class TestNfsAlias():
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
    def nfs_alias_module_mock(self, mocker):
        mocker.patch(MockNfsAliasApi.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        nfs_alias_module_mock = NfsAlias()
        nfs_alias_module_mock.module = MagicMock()
        nfs_alias_module_mock.module.check_mode = False
        return nfs_alias_module_mock

    def test_get_nfs_alias_by_name_response(self, nfs_alias_module_mock):
        self.get_nfs_alias_args.update({"nfs_alias_name": self.nfs_alias_name_1,
                                        "state": "present"})
        nfs_alias_module_mock.module.params = self.get_nfs_alias_args
        nfs_alias_module_mock.protocol_api.get_nfs_alias = MagicMock(
            return_value=MockSDKResponse(MockNfsAliasApi.NFS_ALIAS))
        nfs_alias_module_mock.perform_module_operation()
        nfs_alias_module_mock.protocol_api.get_nfs_alias.assert_called()

    def test_get_nfs_alias_by_name_404_exception(self, nfs_alias_module_mock):
        self.get_nfs_alias_args.update({"nfs_alias_name": self.nfs_alias_name_1,
                                        "state": "present"})
        nfs_alias_module_mock.module.params = self.get_nfs_alias_args
        MockApiException.status = '404'
        nfs_alias_module_mock.protocol_api.get_nfs_alias = MagicMock(
            side_effect=utils.ApiException)
        nfs_alias_module_mock.perform_module_operation()
        nfs_alias_module_mock.protocol_api.get_nfs_alias.assert_called()

    def test_get_nfs_alias_by_name_422_exception(self, nfs_alias_module_mock):
        self.get_nfs_alias_args.update({"nfs_alias_name": self.nfs_alias_name_1,
                                        "state": "present"})
        nfs_alias_module_mock.module.params = self.get_nfs_alias_args
        MockApiException.status = '422'
        nfs_alias_module_mock.protocol_api.get_nfs_alias = MagicMock(
            side_effect=utils.ApiException)
        nfs_alias_module_mock.perform_module_operation()
        nfs_alias_module_mock.protocol_api.get_nfs_alias.assert_called()

    def test_create_nfs_alias_response(self, nfs_alias_module_mock):
        self.get_nfs_alias_args.update({"nfs_alias_name": self.nfs_alias_name_1,
                                        "path": "/ifs",
                                        "access_zone": "sample-zone",
                                        "state": "present"})
        nfs_alias_module_mock.module.params = self.get_nfs_alias_args
        nfs_alias_module_mock.protocol_api.get_nfs_alias = MagicMock(return_value=None)
        nfs_alias_module_mock.isi_sdk.NfsAliasCreateParams = MagicMock(
            return_value=MockSDKResponse(MockNfsAliasApi.CREATE_NFS_ALIAS_PARAMS))
        nfs_alias_module_mock.perform_module_operation()
        nfs_alias_module_mock.protocol_api.create_nfs_alias.assert_called()
        assert nfs_alias_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_nfs_alias_name_with_space(self, nfs_alias_module_mock):
        self.get_nfs_alias_args.update({"nfs_alias_name": "/sample alias",
                                        "new_alias_name": "/renamed_alias",
                                        "path": "/ifs",
                                        "state": "present"})
        nfs_alias_module_mock.module.params = self.get_nfs_alias_args
        nfs_alias_module_mock.protocol_api.get_nfs_alias = MagicMock(return_value=None)
        nfs_alias_module_mock.isi_sdk.NfsAliasCreateParams = MagicMock(
            return_value=MockSDKResponse(MockNfsAliasApi.CREATE_NFS_ALIAS_PARAMS))
        nfs_alias_module_mock.perform_module_operation()
        nfs_alias_module_mock.protocol_api.create_nfs_alias.assert_called()
        assert nfs_alias_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_nfs_alias_name_with_new_alias_name(self, nfs_alias_module_mock):
        self.get_nfs_alias_args.update({"nfs_alias_name": self.nfs_alias_name_1,
                                        "path": "/ifs",
                                        "state": "present"})
        nfs_alias_module_mock.module.params = self.get_nfs_alias_args
        nfs_alias_module_mock.protocol_api.get_nfs_alias = MagicMock(return_value=None)
        nfs_alias_module_mock.isi_sdk.NfsAliasCreateParams = MagicMock(
            return_value=MockSDKResponse(MockNfsAliasApi.CREATE_NFS_ALIAS_PARAMS))
        nfs_alias_module_mock.perform_module_operation()
        nfs_alias_module_mock.protocol_api.create_nfs_alias.assert_called()
        assert nfs_alias_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_nfs_alias_exception(self, nfs_alias_module_mock):
        self.get_nfs_alias_args.update({"nfs_alias_name": self.nfs_alias_name_1,
                                        "path": "/ifs",
                                        "state": "present"})
        nfs_alias_module_mock.module.params = self.get_nfs_alias_args
        nfs_alias_module_mock.protocol_api.get_nfs_alias = MagicMock(return_value=None)
        nfs_alias_module_mock.isi_sdk.NfsAliasCreateParams = MagicMock(
            return_value=MockNfsAliasApi.NFS_ALIAS)
        nfs_alias_module_mock.protocol_api.create_nfs_alias = MagicMock(side_effect=utils.ApiException)
        nfs_alias_module_mock.perform_module_operation()
        assert MockNfsAliasApi.create_nfs_alias_failed_msg() in \
            nfs_alias_module_mock.module.fail_json.call_args[1]['msg']

    def test_create_nfs_alias_no_name_exception(self, nfs_alias_module_mock):
        self.get_nfs_alias_args.update({"path": "/ifs",
                                        "state": "present"})
        nfs_alias_module_mock.module.params = self.get_nfs_alias_args
        nfs_alias_module_mock.protocol_api.get_nfs_alias = MagicMock(return_value=None)
        nfs_alias_module_mock.isi_sdk.NfsAliasCreateParams = MagicMock(
            return_value=MockNfsAliasApi.NFS_ALIAS)
        nfs_alias_module_mock.perform_module_operation()
        nfs_alias_module_mock.protocol_api.create_nfs_alias.assert_called()

    def test_modify_nfs_alias_response(self, nfs_alias_module_mock):
        self.get_nfs_alias_args.update({"nfs_alias_name": self.nfs_alias_name_1,
                                        "new_alias_name": "/Renamed_test_alias_1",
                                        "path": "/ifs/Test/sample1",
                                        "state": "present"})

        nfs_alias_module_mock.module.params = self.get_nfs_alias_args
        nfs_alias_module_mock.protocol_api.get_nfs_alias.to_dict = MagicMock(
            return_value=MockNfsAliasApi.NFS_ALIAS)
        nfs_alias_module_mock.isi_sdk.NfsAlias = MagicMock(
            return_value=MockSDKResponse(MockNfsAliasApi.MODIFY_NFS_ALIAS_PARAMS))
        nfs_alias_module_mock.perform_module_operation()
        nfs_alias_module_mock.protocol_api.update_nfs_alias.assert_called()
        assert nfs_alias_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_nfs_alias_exception(self, nfs_alias_module_mock):
        self.get_nfs_alias_args.update({"nfs_alias_name": self.nfs_alias_name_1,
                                        "new_alias_name": "/Renamed_test_alias_1",
                                        "path": "/ifs/Test/sample1",
                                        "state": "present"})
        nfs_alias_module_mock.module.params = self.get_nfs_alias_args
        nfs_alias_module_mock.protocol_api.get_nfs_alias.to_dict = MagicMock(
            return_value=MockNfsAliasApi.NFS_ALIAS)
        nfs_alias_module_mock.isi_sdk.NfsAlias = MagicMock(
            return_value=MockSDKResponse(MockNfsAliasApi.MODIFY_NFS_ALIAS_PARAMS))
        nfs_alias_module_mock.protocol_api.update_nfs_alias = MagicMock(side_effect=utils.ApiException)
        nfs_alias_module_mock.perform_module_operation()
        nfs_alias_module_mock.protocol_api.update_nfs_alias.assert_called()
        assert MockNfsAliasApi.modify_nfs_alias_failed_msg() in \
            nfs_alias_module_mock.module.fail_json.call_args[1]['msg']

    def test_delete_nfs_alias_by_name_response(self, nfs_alias_module_mock):
        self.get_nfs_alias_args.update({"nfs_alias_name": self.nfs_alias_name_1,
                                        "state": "absent"})
        nfs_alias_module_mock.module.params = self.get_nfs_alias_args
        nfs_alias_module_mock.protocol_api.get_nfs_alias.to_dict = MagicMock(
            return_value=MockNfsAliasApi.NFS_ALIAS)
        nfs_alias_module_mock.perform_module_operation()
        nfs_alias_module_mock.protocol_api.delete_nfs_alias.assert_called()
        assert nfs_alias_module_mock.module.exit_json.call_args[1]['changed'] is True
