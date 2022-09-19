# Copyright: (c) 2022, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for SMB share module on PowerScale"""

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


from ansible_collections.dellemc.powerscale.plugins.modules.smb import SMB
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_smb_api as MockSMBApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException


class TestSMB():
    get_smb_args = {
        "share_name": None,
        "path": None,
        "access_zone": None,
        "description": None,
        "permissions": None,
        "state": None,
        "new_share_name": None,
        "access_based_enumeration": None,
        "access_based_enumeration_root_only": None,
        "browsable": None,
        "ntfs_acl_support": None,
        "directory_create_mask": None,
        "directory_create_mode": None,
        "file_create_mask": None,
        "file_create_mode": None,
        "create_path": None,
        "allow_variable_expansion": None,
        "auto_create_directory": None,
        "continuously_available": None,
        "file_filter_extension": None,
        "file_filtering_enabled": None,
        "ca_timeout": None,
        "strict_ca_lockout": None,
        "change_notify": None,
        "oplocks": None,
        "impersonate_guest": None,
        "impersonate_user": None,
        "host_acls": None}

    @pytest.fixture
    def smb_module_mock(self, mocker):
        mocker.patch(MockSMBApi.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        smb_module_mock = SMB()
        smb_module_mock.module = MagicMock()
        smb_module_mock.module.check_mode = False
        return smb_module_mock

    def test_get_smb_by_name_response(self, smb_module_mock):
        self.get_smb_args.update({"share_name": "test_sample_smb",
                                  "state": "present"})
        smb_module_mock.module.params = self.get_smb_args
        smb_module_mock.protocol_api.get_smb_share = MagicMock(
            return_value=MockSDKResponse(MockSMBApi.SMB))
        smb_module_mock.perform_module_operation()
        smb_module_mock.protocol_api.get_smb_share.assert_called()

    def test_get_smb_by_name_404_exception(self, smb_module_mock):
        self.get_smb_args.update({"share_name": "test_sample_smb",
                                  "state": "present"})
        smb_module_mock.module.params = self.get_smb_args
        MockApiException.status = '404'
        smb_module_mock.protocol_api.get_smb_share = MagicMock(
            side_effect=utils.ApiException)
        smb_module_mock.perform_module_operation()
        smb_module_mock.protocol_api.get_smb_share.assert_called()

    def test_get_smb_by_name_422_exception(self, smb_module_mock):
        self.get_smb_args.update({"share_name": "test_sample_smb",
                                  "state": "present"})
        smb_module_mock.module.params = self.get_smb_args
        MockApiException.status = '422'
        smb_module_mock.protocol_api.get_smb_share = MagicMock(
            side_effect=utils.ApiException)
        smb_module_mock.perform_module_operation()
        smb_module_mock.protocol_api.get_smb_share.assert_called()

    def test_create_smb_response(self, smb_module_mock):
        self.get_smb_args.update({"share_name": "test_sample_smb",
                                  "path": "/ifs",
                                  "description": "description",
                                  "permissions": [{"user_name": "system_az_user",
                                                   "permission": "full",
                                                   "permission_type": "allow"},
                                                  {"group_name": "system_az_group",
                                                   "permission": "read",
                                                   "permission_type": "allow"},
                                                  {"wellknown": "everyone",
                                                   "permission": "read",
                                                   "permission_type": "allow"}],
                                  "directory_create_mask": "700",
                                  "directory_create_mode": "0",
                                  "file_create_mask": "700",
                                  "file_create_mode": "100",
                                  "ntfs_acl_support": False,
                                  "access_based_enumeration": True,
                                  "access_based_enumeration_root_only": True,
                                  "smb3_encryption_enabled": True,
                                  "ca_write_integrity": "full",
                                  "browsable": True,
                                  "create_path": False,
                                  "allow_variable_expansion": True,
                                  "auto_create_directory": True,
                                  "continuously_available": True,
                                  "file_filter_extension": {"extensions": ['sample_extension_1'],
                                                            "type": "allow",
                                                            "state": "present-in-share"},
                                  "file_filtering_enabled": True,
                                  "ca_timeout": {"value": 60,
                                                 "unit": "minutes"},
                                  "strict_ca_lockout": True,
                                  "change_notify": "all",
                                  "oplocks": True,
                                  "impersonate_guest": "never",
                                  "impersonate_user": True,
                                  "host_acls": [{"name": "sample_host_acl_1",
                                                 "access_type": "allow"},
                                                {"name": "sample_host_acl_2",
                                                 "access_type": "deny"}],
                                  "state": "present"})
        smb_module_mock.module.params = self.get_smb_args
        smb_module_mock.protocol_api.get_smb_share = MagicMock(return_value=None)
        smb_module_mock.isi_sdk.SmbShareCreateParams.to_dict = MagicMock(
            return_value=MockSDKResponse(MockSMBApi.CREATE_SMB_PARAMS))
        smb_module_mock.perform_module_operation()
        smb_module_mock.protocol_api.create_smb_share.assert_called()
        assert smb_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_smb_exception(self, smb_module_mock):
        self.get_smb_args.update({"share_name": "test_sample_smb",
                                  "path": "/ifs",
                                  "description": "description",
                                  "permissions": [{"user_name": "system_az_user",
                                                   "permission": "full",
                                                   "permission_type": "allow"},
                                                  {"group_name": "system_az_group",
                                                   "permission": "read",
                                                   "permission_type": "allow"},
                                                  {"wellknown": "everyone",
                                                   "permission": "read",
                                                   "permission_type": "allow"}],
                                  "directory_create_mask": "700",
                                  "directory_create_mode": "0",
                                  "file_create_mask": "700",
                                  "file_create_mode": "100",
                                  "ntfs_acl_support": False,
                                  "access_based_enumeration": True,
                                  "access_based_enumeration_root_only": True,
                                  "browsable": True,
                                  "create_path": False,
                                  "allow_variable_expansion": True,
                                  "auto_create_directory": True,
                                  "continuously_available": True,
                                  "file_filter_extension": {"extensions": ['sample_extension_1'],
                                                            "type": "allow",
                                                            "state": "present-in-share"},
                                  "file_filtering_enabled": True,
                                  "ca_timeout": {"value": 60,
                                                 "unit": "minutes"},
                                  "strict_ca_lockout": True,
                                  "change_notify": "all",
                                  "oplocks": True,
                                  "impersonate_guest": "never",
                                  "impersonate_user": True,
                                  "host_acls": [{"name": "sample_host_acl_1",
                                                 "access_type": "allow"},
                                                {"name": "sample_host_acl_2",
                                                 "access_type": "deny"}],
                                  "state": "present"})
        smb_module_mock.module.params = self.get_smb_args
        smb_module_mock.protocol_api.get_smb_share = MagicMock(return_value=None)
        smb_module_mock.isi_sdk.SmbShareCreateParams = MagicMock(
            return_value=MockSMBApi.SMB)
        smb_module_mock.protocol_api.create_smb_share = MagicMock(side_effect=utils.ApiException)
        smb_module_mock.perform_module_operation()
        assert MockSMBApi.create_smb_failed_msg() in \
            smb_module_mock.module.fail_json.call_args[1]['msg']

    def test_modify_smb_response(self, smb_module_mock):
        self.get_smb_args.update({"share_name": "test_sample_smb",
                                  "path": "/ifs",
                                  "description": "description",
                                  "permissions": [{"user_name": "system_az_user",
                                                   "permission": "full",
                                                   "permission_type": "allow"},
                                                  {"group_name": "system_az_group",
                                                   "permission": "read",
                                                   "permission_type": "allow"},
                                                  {"wellknown": "everyone",
                                                   "permission": "read",
                                                   "permission_type": "allow"}],
                                  "directory_create_mask": "700",
                                  "directory_create_mode": "0",
                                  "file_create_mask": "700",
                                  "file_create_mode": "100",
                                  "ntfs_acl_support": True,
                                  "access_based_enumeration": False,
                                  "access_based_enumeration_root_only": False,
                                  "browsable": True,
                                  "allow_variable_expansion": True,
                                  "smb3_encryption_enabled": True,
                                  "ca_write_integrity": "full",
                                  "auto_create_directory": True,
                                  "continuously_available": True,
                                  "file_filter_extension": {"extensions": ['sample_extension_2'],
                                                            "type": "allow",
                                                            "state": "present-in-share"},
                                  "file_filtering_enabled": True,
                                  "ca_timeout": {"value": 30,
                                                 "unit": "minutes"},
                                  "strict_ca_lockout": True,
                                  "change_notify": "all",
                                  "oplocks": False,
                                  "impersonate_guest": "never",
                                  "impersonate_user": True,
                                  "host_acls": [{"name": "sample_host_acl_1",
                                                 "access_type": "deny"},
                                                {"name": "sample_host_acl_2",
                                                 "access_type": "allow"}],
                                  "state": "present"})
        smb_module_mock.module.params = self.get_smb_args
        smb_module_mock.protocol_api.get_smb_share = MagicMock(
            return_value=MockSDKResponse(MockSMBApi.SMB))
        smb_module_mock.isi_sdk.SmbShare.to_dict = MagicMock(
            return_value=MockSMBApi.MODIFY_SMB_PARAMS)
        smb_module_mock.perform_module_operation()
        smb_module_mock.protocol_api.update_smb_share.assert_called()
        assert smb_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_smb_exception(self, smb_module_mock):
        self.get_smb_args.update({"share_name": "test_sample_smb",
                                  "path": "/ifs",
                                  "description": "description",
                                  "permissions": [{"user_name": "system_az_user",
                                                   "permission": "full",
                                                   "permission_type": "allow"},
                                                  {"group_name": "system_az_group",
                                                   "permission": "read",
                                                   "permission_type": "allow"},
                                                  {"wellknown": "everyone",
                                                   "permission": "read",
                                                   "permission_type": "allow"}],
                                  "directory_create_mask": "700",
                                  "directory_create_mode": "0",
                                  "file_create_mask": "700",
                                  "file_create_mode": "100",
                                  "ntfs_acl_support": True,
                                  "access_based_enumeration": False,
                                  "access_based_enumeration_root_only": False,
                                  "browsable": True,
                                  "allow_variable_expansion": True,
                                  "smb3_encryption_enabled": True,
                                  "ca_write_integrity": "full",
                                  "auto_create_directory": True,
                                  "continuously_available": True,
                                  "file_filter_extension": {"extensions": ['sample_extension_2'],
                                                            "type": "allow",
                                                            "state": "present-in-share"},
                                  "file_filtering_enabled": True,
                                  "ca_timeout": {"value": 30,
                                                 "unit": "minutes"},
                                  "strict_ca_lockout": True,
                                  "change_notify": "all",
                                  "oplocks": False,
                                  "impersonate_guest": "never",
                                  "impersonate_user": True,
                                  "host_acls": [{"name": "sample_host_acl_1",
                                                 "access_type": "deny"},
                                                {"name": "sample_host_acl_2",
                                                 "access_type": "allow"}],
                                  "state": "present"})
        smb_module_mock.module.params = self.get_smb_args
        smb_module_mock.protocol_api.get_smb_share = MagicMock(
            return_value=MockSDKResponse(MockSMBApi.SMB))
        smb_module_mock.isi_sdk.SmbShare.to_dict = MagicMock(
            return_value=MockSMBApi.MODIFY_SMB_PARAMS)
        smb_module_mock.protocol_api.update_smb_share = MagicMock(
            side_effect=utils.ApiException)
        smb_module_mock.perform_module_operation()
        smb_module_mock.protocol_api.update_smb_share.assert_called()
        assert MockSMBApi.modify_smb_failed_msg() in \
            smb_module_mock.module.fail_json.call_args[1]['msg']

    def test_delete_smb_share_response(self, smb_module_mock):
        self.get_smb_args.update({"share_name": "test_sample_smb",
                                  "state": "absent"})
        smb_module_mock.module.params = self.get_smb_args
        smb_module_mock.protocol_api.get_smb_share = MagicMock(
            return_value=MockSDKResponse(MockSMBApi.SMB))
        smb_module_mock.perform_module_operation()
        smb_module_mock.protocol_api.delete_smb_share.assert_called()
        assert smb_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_smb_share_exception(self, smb_module_mock):
        self.get_smb_args.update({"share_name": "test_sample_smb",
                                  "state": "absent"})
        smb_module_mock.module.params = self.get_smb_args
        smb_module_mock.protocol_api.get_smb_share = MagicMock(
            return_value=MockSDKResponse(MockSMBApi.SMB))
        smb_module_mock.protocol_api.delete_smb_share = MagicMock(side_effect=utils.ApiException)
        smb_module_mock.perform_module_operation()
        smb_module_mock.protocol_api.delete_smb_share.assert_called()
        assert MockSMBApi.delete_smb_failed_msg() in \
            smb_module_mock.module.fail_json.call_args[1]['msg']
