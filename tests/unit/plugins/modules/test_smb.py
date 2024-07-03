# Copyright: (c) 2022-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for SMB share module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.smb import SMB, SMBHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_smb_api import MockSMBApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase


class TestSMB(PowerScaleUnitBase):
    smb_args = MockSMBApi.SMB_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        """
        Returns an instance of the `SMB` class for testing purposes.

        :return: An instance of the `SMB` class.
        :rtype: `SMB`
        """
        return SMB

    def test_get_smb_by_name_response(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": MockSMBApi.SMB_NAME, "state": MockSMBApi.STATE_P})
        SMBHandler().handle(powerscale_module_mock,
                            powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.get_smb_share.assert_called()

    def test_get_smb_by_name_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": MockSMBApi.SMB_NAME, "state": MockSMBApi.STATE_P})
        MockApiException.status = '400'
        powerscale_module_mock.protocol_api.get_smb_share = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(
            MockSMBApi.get_smb_exception_response('get_smb'),
            powerscale_module_mock, SMBHandler)

    def test_create_smb_withoutpath_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": MockSMBApi.SMB_NAME, "state": MockSMBApi.STATE_P})
        MockApiException.status = '404'
        powerscale_module_mock.protocol_api.get_smb_share = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(
            MockSMBApi.get_smb_exception_response('invalid_path'),
            powerscale_module_mock, SMBHandler)

    def test_get_smb_by_name_422_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": MockSMBApi.SMB_NAME, "state": MockSMBApi.STATE_P})
        MockApiException.status = '422'
        powerscale_module_mock.protocol_api.get_smb_share = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(
            MockSMBApi.get_smb_exception_response('get_smb'),
            powerscale_module_mock, SMBHandler
        )

    def test_validate_name_params_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": "", "state": MockSMBApi.STATE_P})
        self.capture_fail_json_call(
            MockSMBApi.get_smb_exception_response('invalid_name'),
            powerscale_module_mock, SMBHandler
        )

    def test_validate_path_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": MockSMBApi.SMB_NAME, "state": MockSMBApi.STATE_P,
             "path": "path/path", "access_zone": MockSMBApi.SYS_AZ})
        self.capture_fail_json_call(
            MockSMBApi.get_smb_exception_response('path_err'),
            powerscale_module_mock, SMBHandler
        )

    def test_filter_param_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": MockSMBApi.SMB_NAME, "state": MockSMBApi.STATE_P,
             "path": MockSMBApi.PATH1,
             "file_filter_extension": {"extensions": ["*.pdf"],
                                       "type": MockSMBApi.ALLOW_TYPE,
                                       "state": ""}})
        self.capture_fail_json_call(
            MockSMBApi.get_smb_exception_response('filter_err'),
            powerscale_module_mock, SMBHandler)

    def test_invaild_rar_name_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": MockSMBApi.SMB_NAME, "state": MockSMBApi.STATE_P,
             "path": MockSMBApi.PATH1,
             "run_as_root": [{"name": "rar user", "type": "user"}]})
        self.capture_fail_json_call(
            MockSMBApi.get_smb_exception_response('rar_persona_err'),
            powerscale_module_mock, SMBHandler)

    def test_create_smb(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": MockSMBApi.SMB_NAME, "state": MockSMBApi.STATE_P,
             "path": MockSMBApi.PATH1,
             "permissions": [{"user_name": MockSMBApi.USER1,
                              "permission": "write",
                              "permission_type": MockSMBApi.ALLOW_TYPE}],
             "run_as_root": [{"name": "root", "type": MockSMBApi.USER1,
                              "state": MockSMBApi.ALLOW_TYPE}],
             "description": "sample description", "allow_delete_readonly": True,
             "allow_execute_always": True, "access_zone": MockSMBApi.SYS_AZ,
             "file_filter_extension": {"extensions": ["*.pdf"],
                                       "type": MockSMBApi.ALLOW_TYPE,
                                       "state": MockSMBApi.STATE_P},
             "ca_timeout": {"value": 60, "unit": "minutes"},
             "auto_create_directory": True, "create_path": True,
             "host_acls": [{"name": MockSMBApi.USER1,
                            "access_type": MockSMBApi.ALLOW_TYPE}],
             "directory_create_mask": "700", "directory_create_mode": "0",
             "file_create_mask": "700", "file_create_mode": "100"})
        powerscale_module_mock.protocol_api.get_smb_share = MagicMock(
            return_value=None)
        SMBHandler().handle(powerscale_module_mock,
                            powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.create_smb_share.assert_called()

    def test_create_smb_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": MockSMBApi.SMB_NAME, "state": MockSMBApi.STATE_P,
             "path": MockSMBApi.PATH1,
             "directory_create_mask": "700", "directory_create_mode": "0",
             "file_create_mask": "700", "file_create_mode": "100"})
        powerscale_module_mock.protocol_api.get_smb_share = MagicMock(
            return_value=None)
        powerscale_module_mock.protocol_api.create_smb_share = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSMBApi.get_smb_exception_response('create_err'),
            powerscale_module_mock, SMBHandler)

    def test_rar_obj_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": MockSMBApi.SMB_NAME, "state": MockSMBApi.STATE_P,
             "path": MockSMBApi.PATH1,
             "run_as_root": [{"name": "root", "type": MockSMBApi.USER1,
                              "state": MockSMBApi.ALLOW_TYPE}]})
        powerscale_module_mock.protocol_api.get_smb_share = MagicMock(
            return_value=None)
        powerscale_module_mock.isi_sdk.AuthAccessAccessItemFileGroup = \
            MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSMBApi.get_smb_exception_response('rar_obj_err'),
            powerscale_module_mock, SMBHandler)

    def test_permission_dict_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": MockSMBApi.SMB_NAME, "state": MockSMBApi.STATE_P,
             "path": MockSMBApi.PATH1,
             "permissions": [{"group_name": "group", "permission": "write",
                              "permission_type": MockSMBApi.DENY_TYPE}]})
        powerscale_module_mock.protocol_api.get_smb_share = MagicMock(
            return_value=None)
        powerscale_module_mock.isi_sdk.SmbSharePermission = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSMBApi.get_smb_exception_response('permission_dict_err'),
            powerscale_module_mock, SMBHandler)

    def test_modify_smb(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": MockSMBApi.SMB_NAME, "state": MockSMBApi.STATE_P,
             "permissions": [{"group_name": "sample-group",
                              "permission": "write",
                              "permission_type": MockSMBApi.ALLOW_TYPE},
                             {"wellknown": "everyone", "permission": "read",
                              "permission_type": MockSMBApi.ALLOW_TYPE},
                             {"user_name": "sample-user", "permission": "full",
                              "permission_type": MockSMBApi.DENY_TYPE}],
             "run_as_root": [{"name": "root", "type": MockSMBApi.USER1,
                              "state": MockSMBApi.DENY_TYPE},
                             {"name": "sample-group", "type": "group",
                              "state": MockSMBApi.ALLOW_TYPE}],
             "description": "updated description", "allow_delete_readonly": True,
             "allow_execute_always": True, "access_zone": MockSMBApi.SYS_AZ,
             "file_filter_extension": {"extensions": ["sample_extension_1"],
                                       "type": MockSMBApi.DENY_TYPE,
                                       "state": "present-in-share"},
             "ca_timeout": {"value": 40}, "new_share_name": "renamed_smb",
             "ntfs_acl_support": False,
             "host_acls": [{"name": MockSMBApi.USER1,
                            "access_type": MockSMBApi.ALLOW_TYPE}],
             "directory_create_mask": "777", "directory_create_mode": "64",
             "file_create_mask": "777", "file_create_mode": "0"})
        powerscale_module_mock.protocol_api.get_smb_share.to_dict = MagicMock(
            return_value=MockSMBApi.SMB)
        SMBHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_smb_share.assert_called()

    def test_smb_modify_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": MockSMBApi.SMB_NAME, "state": MockSMBApi.STATE_P,
             "description": "updated description", "allow_delete_readonly": True,
             "ca_timeout": {"value": 40}, "new_share_name": "renamed_smb",
             "ntfs_acl_support": False, "directory_create_mask": "777",
             "directory_create_mode": "64", "file_create_mask": "777",
             "file_create_mode": "0"})
        powerscale_module_mock.protocol_api.get_smb_share.to_dict = \
            MagicMock(return_value=MockSMBApi.SMB)
        powerscale_module_mock.protocol_api.update_smb_share = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSMBApi.get_smb_exception_response('modify_err'),
            powerscale_module_mock, SMBHandler)

    def test_delete_smb(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": MockSMBApi.SMB_NAME, "state": "absent"})
        powerscale_module_mock.protocol_api.get_smb_share.to_dict = \
            MagicMock(return_value=MockSMBApi.SMB)
        SMBHandler().handle(powerscale_module_mock,
                            powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.delete_smb_share.assert_called()

    def test_delete_smb_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": MockSMBApi.SMB_NAME, "state": "absent"})
        powerscale_module_mock.protocol_api.get_smb_share.to_dict = MagicMock(
            return_value=MockSMBApi.SMB)
        powerscale_module_mock.protocol_api.delete_smb_share = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSMBApi.get_smb_exception_response('delete_err'),
            powerscale_module_mock, SMBHandler)

    def test_modify_path_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": MockSMBApi.SMB_NAME, "state": MockSMBApi.STATE_P,
             "path": MockSMBApi.PATH1})
        powerscale_module_mock.protocol_api.get_smb_share.to_dict = MagicMock(
            return_value=MockSMBApi.SMB)
        self.capture_fail_json_call(
            MockSMBApi.get_smb_exception_response('modify_path_err'),
            powerscale_module_mock, SMBHandler)

    def test_modify_file_filter(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": MockSMBApi.SMB_NAME, "state": MockSMBApi.STATE_P,
             "access_zone": "non-system",
             "file_filter_extension": {"extensions": ["sample_extension_1"],
                                       "type": MockSMBApi.DENY_TYPE,
                                       "state": "absent-in-share"}})
        powerscale_module_mock.protocol_api.get_smb_share.to_dict = MagicMock(
            return_value=MockSMBApi.SMB)
        SMBHandler().handle(powerscale_module_mock,
                            powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_smb_share.assert_called()
        powerscale_module_mock.isi_sdk.SmbShare.assert_called()

    def test_create_non_system_az_smb(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": MockSMBApi.SMB_NAME,
             "state": MockSMBApi.STATE_P, "access_zone": "nonsystem",
             "path": "path/path"})
        powerscale_module_mock.validate_path = MagicMock(return_value=False)
        powerscale_module_mock.protocol_api.get_smb_share = MagicMock(
            return_value=None)
        SMBHandler().handle(powerscale_module_mock,
                            powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.create_smb_share.assert_called()

    def test_get_sid_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": MockSMBApi.SMB_NAME, "state": MockSMBApi.STATE_P,
             "run_as_root": [{"name": "root", "type": MockSMBApi.USER1,
                              "state": MockSMBApi.DENY_TYPE}]})
        powerscale_module_mock.protocol_api.get_smb_share.to_dict = MagicMock(
            return_value=MockSMBApi.SMB)
        powerscale_module_mock.auth_api.get_auth_user = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSMBApi.get_smb_exception_response('sid_err'),
            powerscale_module_mock, SMBHandler)

    def test_modify_hostacl(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": MockSMBApi.SMB_NAME, "state": MockSMBApi.STATE_P,
             "host_acls": [{"name": MockSMBApi.USER1,
                            "access_type": MockSMBApi.ALLOW_TYPE}]})
        powerscale_module_mock.protocol_api.get_smb_share.to_dict = MagicMock(
            return_value=MockSMBApi.SMB)
        SMBHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_smb_share.assert_called()

    def test_modify_permission(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.smb_args,
            {"share_name": MockSMBApi.SMB_NAME, "state": MockSMBApi.STATE_P,
             "permissions": [{"group_name": "sample-group",
                              "permission": "Write",
                              "permission_type": MockSMBApi.ALLOW_TYPE,
                              "provider_type": "local"},
                             {"wellknown": "Batch", "permission": "read",
                              "permission_type": MockSMBApi.DENY_TYPE},
                             {"user_name": "sample-user", "permission": "full",
                              "permission_type": MockSMBApi.ALLOW_TYPE,
                              "provider_type": "local"}]})
        powerscale_module_mock.protocol_api.get_smb_share.to_dict = MagicMock(
            return_value=MockSMBApi.SMB)
        SMBHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.update_smb_share.assert_called()

    def test_get_smb_permissions_dict(self, powerscale_module_mock):
        permission = MockSMBApi.PERMISSIONS
        resp = powerscale_module_mock.get_smb_permissions_dict(permission)
        assert resp is not None

    def test_is_sid_in_permission(self, powerscale_module_mock):
        permission_list = MockSMBApi.USER_PERM
        sid = MockSMBApi.PERMISSIONS[0]['trustee']['id']
        index = 0
        smb_perm = MockSMBApi.SMB["shares"][0]["permissions"][0]
        resp = powerscale_module_mock.is_sid_in_permission_list(
            permission_list, index, sid, smb_perm)
        assert resp is True

    def test_arrange_persona_dict_exp(self, powerscale_module_mock):
        persona = {"name": "root", "type": "wellknown",
                   "state": MockSMBApi.DENY_TYPE}
        powerscale_module_mock.auth_api.get_auth_wellknowns.to_dict = \
            MagicMock(return_value=MockSMBApi.WELLKNOWN)
        self.capture_fail_json_method(
            MockSMBApi.get_smb_exception_response("wellknown_err"),
            powerscale_module_mock, "arrange_persona_dict",
            persona)
