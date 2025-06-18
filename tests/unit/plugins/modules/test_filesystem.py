# Copyright: (c) 2022-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for filesystem module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock

from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response import MockSDKResponse
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils
from ansible.module_utils import basic

from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase

basic.AnsibleModule = MagicMock()

from ansible_collections.dellemc.powerscale.plugins.modules.filesystem import FileSystem
from ansible_collections.dellemc.powerscale.plugins.modules.filesystem import FilesystemHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_filesystem_api \
    import MockFileSystemApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException


class TestFileSystem(PowerScaleUnitBase):
    get_filesystem_args = {'path': None,
                           'access_zone': None,
                           'owner': None,
                           'group': None,
                           'access_control': None,
                           'access_control_rights': None,
                           'access_control_rights_state': None,
                           'recursive': None,
                           'recursive_force_delete': None,
                           'quota': None,
                           'list_snapshots': None,
                           'state': None
                           }
    path1 = "/ifs/ATest3"

    @pytest.fixture
    def module_object(self):
        return FileSystem

    @pytest.fixture(autouse=True)
    def inject_attributes(self, powerscale_module_mock):
        powerscale_module_mock.namespace_api = MagicMock()
        powerscale_module_mock.quota_api = MagicMock()
        powerscale_module_mock.protocol_api = MagicMock()
        powerscale_module_mock.auth_api = MagicMock()
        powerscale_module_mock.zone_summary_api = MagicMock()

    def test_get_file_system_404(self, powerscale_module_mock):
        self.set_module_params(self.get_filesystem_args,
                               {
                                   "group": {
                                       "name": "group_test",
                                   },
                                   "owner": {
                                       "name": "owner_test",
                                   },
                                   "path": self.path1,
                                   "access_control": "private",
                                   "access_zone": "System",
                                   "state": "present"})
        powerscale_module_mock.namespace_api.get_directory_metadata = MagicMock(side_effect=MockApiException(404))
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.namespace_api.get_directory_metadata.assert_called()

    def test_delete_file_system(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "recursive_force_delete": True, "access_zone": "System", "state": "absent"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.get_filesystem = MagicMock(return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=MockSDKResponse(MockFileSystemApi.EMPTY_NFS_EXPORTS))
        powerscale_module_mock.protocol_api.list_smb_shares = MagicMock(
            return_value=MockSDKResponse(MockFileSystemApi.EMPTY_SMB_SHARES))
        powerscale_module_mock.module.check_mode = False
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']
        powerscale_module_mock.namespace_api.delete_directory.assert_called()

    def test_delete_file_system_check_mode(self, powerscale_module_mock):
        self.set_module_params(self.get_filesystem_args,
                               {"path": self.path1, "recursive_force_delete": True, "access_zone": "System",
                                "state": "absent"})
        powerscale_module_mock.get_filesystem = MagicMock(return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(
            return_value=MockSDKResponse(MockFileSystemApi.EMPTY_NFS_EXPORTS))
        powerscale_module_mock.protocol_api.list_smb_shares = MagicMock(
            return_value=MockSDKResponse(MockFileSystemApi.EMPTY_SMB_SHARES))
        powerscale_module_mock.module.check_mode = True
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']

    def test_delete_file_system_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "recursive_force_delete": True, "access_zone": "System", "state": "absent"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.protocol_api.list_nfs_exports = MagicMock(side_effect=MockApiException)
        powerscale_module_mock.determine_error = MagicMock()
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'delete_filesystem_exception'), FilesystemHandler)

    def test_delete_file_system_with_export_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update(
            {"path": self.path1, "recursive_force_delete": True, "access_zone": "System", "state": "absent"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.get_filesystem = MagicMock(
            return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.protocol_api.list_smb_shares = MagicMock(
            return_value=MockSDKResponse(MockFileSystemApi.EMPTY_SMB_SHARES))
        powerscale_module_mock.module.check_mode = False
        self.capture_fail_json_call(MockFileSystemApi.get_error_responses(
            "delete_file_system_with_export_exception"), FilesystemHandler)

    def test_create_file_system_with_access_control_rights(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "owner": {"name": "test"}, "group": {"name": "group_test"},
                                         "access_control_rights":
                                             {"access_rights": ["dir_gen_all"], "inherit_flags": "container_inherit",
                                              "access_type": "allow",
                                              "trustee": {"name": "test_user", "type": "user",
                                                          "provider_type": "local"}},
                                         "access_zone": "System", "state": "present",
                                         "access_control_rights_state": "add"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.module.params = self.get_filesystem_args
        utils.get_acl_object = MagicMock()
        powerscale_module_mock.get_filesystem = MagicMock(return_value=None)
        powerscale_module_mock.get_acl_object = MagicMock(return_value=True)
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] \
               and powerscale_module_mock.module.exit_json.call_args[1]['create_filesystem']

    def test_create_file_system_with_access_control_rights_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "owner": {"name": "test"}, "group": {"name": "group_test"},
                                         "access_control_rights":
                                             {"access_rights": ["dir_gen_all"], "inherit_flags": "container_inherit",
                                              "access_type": "allow",
                                              "trustee": {"name": "test_user", "type": "test",
                                                          "provider_type": "local"}},
                                         "access_zone": "System", "state": "present",
                                         "access_control_rights_state": "add"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.module.params = self.get_filesystem_args
        utils.get_acl_object = MagicMock()
        powerscale_module_mock.get_filesystem = MagicMock(return_value=None)
        powerscale_module_mock.get_acl_object = MagicMock(return_value=True)
        powerscale_module_mock.auth_api.get_auth_wellknowns = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(MockFileSystemApi.get_error_responses(
            "create_file_system_with_access_control_rights_exception"
        ), FilesystemHandler)

    def test_get_acl_object_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "owner": {"name": "test"}, "group": {"name": "group_test"},
                                         "access_control_rights":
                                             {"access_rights": ["dir_gen_all"], "inherit_flags": "container_inherit",
                                              "access_type": "allow",
                                              "trustee": {"name": "test_user", "type": "user",
                                                          "provider_type": "local"}},
                                         "access_zone": "System", "state": "present",
                                         "access_control_rights_state": "add"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.module.params = self.get_filesystem_args
        utils.get_acl_object = MagicMock(side_effect=MockApiException)
        powerscale_module_mock.get_filesystem = MagicMock(return_value=None)
        powerscale_module_mock.get_acl_object = MagicMock(return_value=True)
        self.capture_fail_json_call(MockFileSystemApi.get_error_responses(
            'get_acl_object_exception'), FilesystemHandler)

    def test_create_file_system_with_access_control_private_read(self, powerscale_module_mock):
        self.get_filesystem_args.update(
            {
                "path": self.path1,
                "owner": {"name": "test"},
                "quota": {
                    "thresholds_on": "fs_logical_size",
                    "soft_limit_size": 5,
                    "hard_limit_size": 10,
                    "cap_unit": "GB",
                    "container": True,
                    "quota_state": "present",
                },
                "access_control": "private_read",
                "access_zone": "System", "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.get_filesystem = MagicMock(return_value=None)
        powerscale_module_mock.get_acl_object = MagicMock(return_value=True)
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] \
               and powerscale_module_mock.module.exit_json.call_args[1]['create_filesystem']

    def test_create_quota_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update(
            {
                "path": self.path1,
                "owner": {"name": "test"},
                "quota": {
                    "thresholds_on": "fs_logical_size",
                    "soft_limit_size": 5,
                    "hard_limit_size": 10,
                    "cap_unit": "GB",
                    "container": True,
                    "quota_state": "present",
                },
                "access_zone": "System", "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.get_filesystem = MagicMock(return_value=None)
        powerscale_module_mock.get_acl_object = MagicMock(return_value=True)
        powerscale_module_mock.quota_api.create_quota_quota = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'create_quota_exception'), FilesystemHandler)

    def test_access_control_private_response(self, powerscale_module_mock):
        self.set_module_params(self.get_filesystem_args,
                               {"path": self.path1,
                                "access_control": "private", "access_zone": "System", "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(
            return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.get_acl = MagicMock(
            return_value=MockFileSystemApi.get_acl_response())
        modified_acl = MockFileSystemApi.get_acl_response()
        modified_acl['mode'] = '0770'
        powerscale_module_mock.get_acl = MagicMock(return_value=modified_acl)
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        assert not powerscale_module_mock.module.exit_json.call_args[1]['changed']

    def test_access_control_private_read_response(self, powerscale_module_mock):
        self.set_module_params(self.get_filesystem_args,
                               {"path": self.path1,
                                "access_control": "private_read", "access_zone": "System", "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(
            return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        modified_acl = MockFileSystemApi.get_acl_response()
        modified_acl['mode'] = '0550'
        powerscale_module_mock.get_acl = MagicMock(return_value=modified_acl)
        powerscale_module_mock.get_acl_object = MagicMock(return_value=True)
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        assert not powerscale_module_mock.module.exit_json.call_args[1]['changed']

    def test_access_control_public_read_response(self, powerscale_module_mock):
        self.set_module_params(self.get_filesystem_args,
                               {"path": self.path1,
                                "access_control": "public_read", "access_zone": "System", "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(
            return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        modified_acl = MockFileSystemApi.get_acl_response()
        modified_acl['mode'] = '0775'
        powerscale_module_mock.get_acl = MagicMock(return_value=modified_acl)
        powerscale_module_mock.get_acl_object = MagicMock(return_value=True)
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        assert not powerscale_module_mock.module.exit_json.call_args[1]['changed']

    def test_access_control_public_read_write_response(self, powerscale_module_mock):
        self.set_module_params(self.get_filesystem_args,
                               {"path": self.path1,
                                "access_control": "public_read_write", "access_zone": "System", "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(
            return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        modified_acl = MockFileSystemApi.get_acl_response()
        modified_acl['mode'] = '0777'
        powerscale_module_mock.get_acl = MagicMock(return_value=modified_acl)
        powerscale_module_mock.get_acl_object = MagicMock(return_value=True)
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        assert not powerscale_module_mock.module.exit_json.call_args[1]['changed']

    def test_modify_file_system_with_access_control_public(self, powerscale_module_mock):
        self.set_module_params(self.get_filesystem_args,
                               {"path": self.path1,
                                "access_control": "0777", "access_zone": "System", "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(
            return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        modified_acl = MockFileSystemApi.get_acl_response()
        modified_acl['authoritative'] = 'mode'
        powerscale_module_mock.get_acl = MagicMock(return_value=modified_acl)
        powerscale_module_mock.get_acl_object = MagicMock(return_value=True)
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] \
               and powerscale_module_mock.module.exit_json.call_args[1]['modify_filesystem']

    def test_check_acl_modified_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1,
                                         "access_control": "0777", "access_zone": "System", "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.get_filesystem = MagicMock(
            return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.get_acl = MagicMock(
            return_value=MockFileSystemApi.get_acl_response())
        powerscale_module_mock.get_acl_posix = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'check_acl_modified_exception'), FilesystemHandler)

    def test_create_file_system_with_check_mode(self, powerscale_module_mock):
        self.get_filesystem_args.update(
            {
                "path": self.path1,
                "owner": {"name": "test"},
                "group": {"name": "group_test", "provider_type": "ldap"},
                "access_control_rights": {
                    "access_rights": ["dir_gen_all"],
                    "inherit_flags": "container_inherit",
                    "access_type": "allow",
                    "trustee": {
                        "name": "test_user",
                        "type": "user",
                        "provider_type": "local"
                    }
                },
                "access_zone": "System", "state": "present", "access_control_rights_state": "add"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.namespace_api.get_filesystem = MagicMock(return_value={})
        powerscale_module_mock.get_acl_object = MagicMock()
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']

    def test_modify_acl(self, powerscale_module_mock):
        self.get_filesystem_args.update(
            {
                "path": self.path1,
                "owner": {"name": "test"},
                "group": {"name": "group_test", "provider_type": "ldap"},
                "access_control_rights": {
                    "access_rights": ["dir_gen_all"],
                    "inherit_flags": "container_inherit",
                    "access_type": "allow",
                    "trustee": {
                        "name": "test_user_new",
                        "type": "user",
                        "provider_type": "local"
                    }
                },
                "access_zone": "System", "state": "present", "access_control_rights_state": "add"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.namespace_api.get_filesystem = MagicMock(
            return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.get_acl = MagicMock(
            return_value=MockFileSystemApi.get_acl_response())
        powerscale_module_mock.get_trustee_id = MagicMock(
            return_value="id:2000")
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] \
               and powerscale_module_mock.module.exit_json.call_args[1]['modify_filesystem']

    def test_modify_acl_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update(
            {
                "path": self.path1,
                "owner": {"name": "test"},
                "group": {"name": "group_test", "provider_type": "ldap"},
                "access_control": None,
                "access_control_rights": {
                    "access_rights": ["dir_gen_all"],
                    "inherit_flags": "container_inherit",
                    "access_type": "allow",
                    "trustee": {
                        "name": "test_user",
                        "type": "user",
                        "provider_type": "local"
                    }
                },
                "access_zone": "System", "state": "present", "access_control_rights_state": "add"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        utils.get_acl_object = MagicMock()
        powerscale_module_mock.namespace_api.get_filesystem = MagicMock(
            return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.get_acl = MagicMock(
            return_value=MockFileSystemApi.get_acl_response())
        powerscale_module_mock.get_trustee_id = MagicMock(
            return_value="id:2000")
        powerscale_module_mock.is_owner_modified = MagicMock(
            return_value=True)
        powerscale_module_mock.is_group_modified = MagicMock(
            return_value=True)
        powerscale_module_mock.namespace_api.set_acl = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'modify_acl_exception'), FilesystemHandler)

    def test_modify_acl_posix_exception(self, powerscale_module_mock):
        self.set_module_params(self.get_filesystem_args,
                               {
                                   "path": self.path1,
                                   "owner": {"name": "test"},
                                   "group": {"name": "group_test", "provider_type": "ldap"},
                                   "access_control": "0775",
                                   "access_control_rights": {
                                       "access_rights": ["dir_gen_all"],
                                       "inherit_flags": "container_inherit",
                                       "access_type": "allow",
                                       "trustee": {
                                           "name": "test_user",
                                           "type": "user",
                                           "provider_type": "local"
                                       }
                                   },
                                   "access_zone": "System", "state": "present", "access_control_rights_state": "add"})
        powerscale_module_mock.module.check_mode = False
        utils.get_acl_object = MagicMock()
        powerscale_module_mock.namespace_api.get_filesystem = MagicMock(
            return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        acl_resp = MockFileSystemApi.get_acl_response()
        acl_resp['authoritative'] = 'mode'
        acl_resp['mode'] = '0777'
        powerscale_module_mock.get_acl = MagicMock(
            return_value=acl_resp)
        powerscale_module_mock.get_trustee_id = MagicMock(
            return_value="id:2000")
        powerscale_module_mock.is_owner_modified = MagicMock(
            return_value=True)
        powerscale_module_mock.is_group_modified = MagicMock(
            return_value=True)
        powerscale_module_mock.namespace_api.set_acl = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'modify_acl_posix_exception'), FilesystemHandler)

    def test_modify_acl_posix_not_allowed_exception(self, powerscale_module_mock):
        self.set_module_params(self.get_filesystem_args,
                               {
                                   "path": self.path1,
                                   "owner": {"name": "test"},
                                   "group": {"name": "group_test", "provider_type": "ldap"},
                                   "access_control": "0775",
                                   "access_control_rights": {
                                       "access_rights": ["dir_gen_all"],
                                       "inherit_flags": "container_inherit",
                                       "access_type": "allow",
                                       "trustee": {
                                           "name": "test_user",
                                           "type": "user",
                                           "provider_type": "local"
                                       }
                                   },
                                   "access_zone": "System", "state": "present", "access_control_rights_state": "add"})
        powerscale_module_mock.module.check_mode = False
        utils.get_acl_object = MagicMock()
        powerscale_module_mock.namespace_api.get_filesystem = MagicMock(
            return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        acl_resp = MockFileSystemApi.get_acl_response()
        powerscale_module_mock.get_acl = MagicMock(
            return_value=acl_resp)
        powerscale_module_mock.get_trustee_id = MagicMock(
            return_value="id:2000")
        powerscale_module_mock.is_owner_modified = MagicMock(
            return_value=True)
        powerscale_module_mock.is_group_modified = MagicMock(
            return_value=True)
        powerscale_module_mock.namespace_api.set_acl = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'modify_acl_posix_exception'), FilesystemHandler)

    def test_is_owner_modified_exception(self, powerscale_module_mock):
        self.set_module_params(self.get_filesystem_args,
                               {
                                   "path": self.path1,
                                   "owner": {"name": "test"},
                                   "group": {"name": "group_test", "provider_type": "ldap"},
                                   "access_control": "0775",
                                   "access_control_rights": {
                                       "access_rights": ["dir_gen_all"],
                                       "inherit_flags": "container_inherit",
                                       "access_type": "allow",
                                       "trustee": {
                                           "name": "test_user",
                                           "type": "user",
                                           "provider_type": "local"
                                       }
                                   },
                                   "access_zone": "System", "state": "present", "access_control_rights_state": "add"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_owner_id = MagicMock(
            side_effect=MockApiException)
        powerscale_module_mock.namespace_api.get_filesystem = MagicMock(
            return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'is_owner_modified_exception'), FilesystemHandler)

    def test_is_group_modified_exception(self, powerscale_module_mock):
        self.set_module_params(self.get_filesystem_args,
                               {
                                   "path": self.path1,
                                   "owner": {"name": "test"},
                                   "group": {"name": "group_test", "provider_type": "ldap"},
                                   "access_control": "0775",
                                   "access_control_rights": {
                                       "access_rights": ["dir_gen_all"],
                                       "inherit_flags": "container_inherit",
                                       "access_type": "allow",
                                       "trustee": {
                                           "name": "test_user",
                                           "type": "user",
                                           "provider_type": "local"
                                       }
                                   },
                                   "access_zone": "System", "state": "present", "access_control_rights_state": "add"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_group_id = MagicMock(side_effect=MockApiException)
        powerscale_module_mock.namespace_api.get_filesystem = MagicMock(
            return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'is_group_modified_exception'), FilesystemHandler)

    def test_get_owner_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "owner": {"name": "test"}, "access_zone": "System", "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_acl = MagicMock(
            return_value=MockFileSystemApi.get_acl_response())
        powerscale_module_mock.auth_api.get_auth_user = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'get_owner_id_exception'), FilesystemHandler)

    def test_modify_owner_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "owner": {"name": "test"}, "access_zone": "System", "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_acl = MagicMock(
            return_value=MockFileSystemApi.get_acl_response())
        powerscale_module_mock.namespace_api.set_acl = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'modify_owner_exception'), FilesystemHandler)

    def test_create_file_system_exception(self, powerscale_module_mock):
        self.set_module_params(self.get_filesystem_args,
                               {"path": self.path1, "owner": {"name": "test"}, "group": {"name": "group_test"},
                                "access_control_rights":
                                {"access_rights": ["dir_gen_all"], "inherit_flags": "container_inherit",
                                   "access_type": "allow",
                                   "trustee": {"name": "test_user", "type": "user",
                                               "provider_type": "local"}},
                                   "access_zone": "System", "state": "present",
                                   "access_control_rights_state": "add"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(return_value=None)
        powerscale_module_mock.get_owner_id = MagicMock()
        powerscale_module_mock.isi_sdk.NamespaceAcl = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'create_file_system_exception'), FilesystemHandler)

    def test_create_file_system_wo_owner_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "access_zone": "System", "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(return_value=None)
        powerscale_module_mock.get_owner_id = MagicMock()
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'create_file_system_wo_owner_exception'), FilesystemHandler)

    def test_create_file_system_wo_owner_name_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "owner": {"provider_type": "nis"}, "access_zone": "System", "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(return_value=None)
        powerscale_module_mock.get_owner_id = MagicMock()
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'create_file_system_wo_owner_name_exception'), FilesystemHandler)

    def test_modify_file_system_wo_owner_name_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "owner": {"provider_type": "nis"}, "access_zone": "System", "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(
            return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.get_owner_id = MagicMock()
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'create_file_system_wo_owner_name_exception'), FilesystemHandler)

    def test_create_file_system_wo_group_name_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update(
            {
                "path": self.path1,
                "owner": {"name": "test"},
                "group": {"provider_type": "ads"},
                "access_zone": "System", "state": "present"
            })
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(return_value=None)
        powerscale_module_mock.get_acl_object = MagicMock()
        powerscale_module_mock.determine_error = MagicMock()
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'create_file_system_wo_group_name_exception'), FilesystemHandler)

    def test_modify_file_system_wo_group_name_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "group": {"provider_type": "ads"}, "access_zone": "System", "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.namespace_api.get_filesystem = MagicMock(
            return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.get_acl_object = MagicMock()
        powerscale_module_mock.determine_error = MagicMock()
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'create_file_system_wo_group_name_exception'), FilesystemHandler)

    def test_get_file_system_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "access_zone": "System", "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.namespace_api.get_directory_metadata = MagicMock(side_effect=MockApiException)
        powerscale_module_mock.determine_error = MagicMock()
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'get_filesystem_exception'), FilesystemHandler)

    def test_get_file_system_non_system_az(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "access_zone": "sample_zone", "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.namespace_api.get_directory_metadata.to_dict = MagicMock(
            return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.zone_summary_api.get_zones_summary_zone.to_dict = MagicMock(
            return_value=MockFileSystemApi.ZONE_PATH)
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.zone_summary_api.get_zones_summary_zone.assert_called()

    def test_get_zone_path_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "access_zone": "sample_zone1", "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.zone_summary_api.get_zones_summary_zone = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'get_zone_path_exception'), FilesystemHandler)

    def test_get_acl_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "access_zone": "System", "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.namespace_api.get_acl = MagicMock(side_effect=MockApiException)
        powerscale_module_mock.determine_error = MagicMock()
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'get_acl_exception'), FilesystemHandler)

    def test_update_quota_advisory(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1,
                                         "access_zone": "System",
                                         "quota": {
                                             "thresholds_on": None,
                                             "soft_limit_size": 2,
                                             "hard_limit_size": 8,
                                             "advisory_limit_size": 7,
                                             "cap_unit": "MB",
                                             "container": False,
                                             "quota_state": "present",
                                         },
                                         "list_snapshots": True,
                                         "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(
            return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.get_quota = MagicMock(
            return_value=MockFileSystemApi.QUOTA_DETAILS_0)
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] \
               and powerscale_module_mock.module.exit_json.call_args[1]['modify_filesystem']

    def test_update_quota_soft(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1,
                                         "access_zone": "System",
                                         "quota": {
                                             "thresholds_on": None,
                                             "soft_limit_size": 2,
                                             "hard_limit_size": None,
                                             "advisory_limit_size": None,
                                             "cap_unit": "MB",
                                             "container": False,
                                             "quota_state": "present",
                                         },
                                         "list_snapshots": True,
                                         "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(
            return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.get_quota = MagicMock(
            return_value=MockFileSystemApi.QUOTA_DETAILS_0)
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] \
               and powerscale_module_mock.module.exit_json.call_args[1]['modify_filesystem']

    def test_update_quota_hard(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1,
                                         "access_zone": "System",
                                         "quota": {
                                             "thresholds_on": None,
                                             "soft_limit_size": None,
                                             "hard_limit_size": 8,
                                             "advisory_limit_size": None,
                                             "cap_unit": "MB",
                                             "container": False,
                                             "quota_state": "present",
                                         },
                                         "list_snapshots": True,
                                         "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(
            return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.get_quota = MagicMock(
            return_value=MockFileSystemApi.QUOTA_DETAILS_0)
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] \
               and powerscale_module_mock.module.exit_json.call_args[1]['modify_filesystem']

    def test_update_quota_exception(self, powerscale_module_mock):
        self.set_module_params(self.get_filesystem_args,
                               {"path": self.path1,
                                "access_zone": "System",
                                "quota": {
                                    "thresholds_on": "fs_logical_size",
                                    "soft_limit_size": None,
                                    "hard_limit_size": None,
                                    "advisory_limit_size": 7,
                                    "cap_unit": None,
                                    "container": None,
                                    "quota_state": "present",
                                },
                                "list_snapshots": True,
                                "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.quota_api.update_quota_quota = MagicMock(side_effect=MockApiException)
        powerscale_module_mock.determine_error = MagicMock()
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'update_quota_error_exception'), FilesystemHandler)

    def test_update_include_snap_data_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1,
                                         "access_zone": "System",
                                         "quota": {
                                             "include_snap_data": True,
                                             "thresholds_on": None,
                                             "soft_limit_size": None,
                                             "hard_limit_size": None,
                                             "advisory_limit_size": 7,
                                             "cap_unit": None,
                                             "container": None,
                                             "quota_state": "present",
                                         },
                                         "list_snapshots": True,
                                         "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(
            return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.get_quota = MagicMock(
            return_value=MockFileSystemApi.QUOTA_DETAILS_0)
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'update_include_snap_data_exception'), FilesystemHandler)

    def test_update_quota_wo_quota_state_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1,
                                         "access_zone": "System",
                                         "quota": {
                                             "thresholds_on": "fs_logical_size",
                                             "soft_limit_size": 5,
                                             "hard_limit_size": 10,
                                             "cap_unit": "GB",
                                             "container": True,
                                             "quota_state": None,
                                         },
                                         "list_snapshots": True,
                                         "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.determine_error = MagicMock()
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'get_quota_state_exception'), FilesystemHandler)

    def test_update_quota_invalid_cap_unit_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1,
                                         "access_zone": "System",
                                         "quota": {
                                             "thresholds_on": "fs_logical_size",
                                             "soft_limit_size": 5,
                                             "hard_limit_size": 10,
                                             "cap_unit": "KB",
                                             "container": True,
                                             "quota_state": "present",
                                         },
                                         "list_snapshots": True,
                                         "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.determine_error = MagicMock()
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'get_cap_unit_exception'), FilesystemHandler)

    def test_delete_quota(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1,
                                         "access_zone": "System",
                                         "quota": {
                                             "thresholds_on": "fs_logical_size",
                                             "soft_limit_size": 5,
                                             "hard_limit_size": 10,
                                             "cap_unit": "GB",
                                             "container": True,
                                             "quota_state": "absent",
                                         },
                                         "list_snapshots": True,
                                         "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.get_quota = MagicMock(return_value=MockFileSystemApi.QUOTA_DETAILS_1)
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] \
               and powerscale_module_mock.module.exit_json.call_args[1]['delete_quota']

    def test_delete_quota_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1,
                                         "access_zone": "System",
                                         "quota": {
                                             "thresholds_on": "fs_logical_size",
                                             "soft_limit_size": 5,
                                             "hard_limit_size": 10,
                                             "cap_unit": "GB",
                                             "container": True,
                                             "quota_state": "absent",
                                         },
                                         "list_snapshots": True,
                                         "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.get_quota = MagicMock(return_value=MockFileSystemApi.QUOTA_DETAILS_1)
        powerscale_module_mock.quota_api.delete_quota_quotas = MagicMock(side_effect=MockApiException)
        powerscale_module_mock.determine_error = MagicMock()
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'delete_quota_exception'), FilesystemHandler)

    def test_invalid_path_exception(self, powerscale_module_mock):
        self.set_module_params(self.get_filesystem_args,
                               {"path": "sample_zone/path1",
                                "access_zone": "System",
                                "quota": {
                                    "thresholds_on": "fs_logical_size",
                                    "soft_limit_size": 5,
                                    "hard_limit_size": 10,
                                    "cap_unit": "MB",
                                    "container": True,
                                    "quota_state": "present",
                                },
                                "list_snapshots": True,
                                "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.determine_error = MagicMock()
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'invalid_path_exception'), FilesystemHandler)

    def test_get_filesystem_snapshots_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "access_zone": "System", "list_snapshots": True, "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.snapshot_api.list_snapshot_snapshots = MagicMock(side_effect=MockApiException)
        powerscale_module_mock.determine_error = MagicMock()
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'get_filesystem_snapshots_exception'), FilesystemHandler)

    def test_modify_file_system_with_access_control_rights(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "owner": {"name": "test"}, "group": {"name": "group_test"},
                                         "access_control_rights":
                                             {"access_rights": ["dir_gen_all"], "inherit_flags": "container_inherit",
                                              "access_type": "allow",
                                              "trustee": {"name": "test_user", "type": "user",
                                                          "provider_type": "local"}},
                                         "access_zone": "System", "state": "present", "access_control_rights_state": "add"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.get_acl = MagicMock(return_value=MockFileSystemApi.get_acl_response())
        utils.get_acl_object = MagicMock()
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] \
               and powerscale_module_mock.module.exit_json.call_args[1]['modify_filesystem']

    def test_modify_file_system_with_access_control_rights_with_trustee_group(self, powerscale_module_mock):
        self.set_module_params(self.get_filesystem_args,
                               {"path": self.path1, "owner": {"name": "test"}, "group": {"name": "group_test"},
                                "access_control_rights":
                                    {"access_rights": ["dir_gen_all"], "inherit_flags": "container_inherit",
                                     "access_type": "allow",
                                     "trustee": {"name": "test_group", "type": "group", "provider_type": "local"}},
                                "access_zone": "System", "state": "present", "access_control_rights_state": "add"})
        powerscale_module_mock.get_acl = MagicMock(return_value=MockFileSystemApi.get_acl_response())
        powerscale_module_mock.get_acl_object = MagicMock()
        utils.get_acl_object = MagicMock()
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] \
               and powerscale_module_mock.module.exit_json.call_args[1]['modify_filesystem']

    def test_modify_file_system_with_access_control_rights_with_trustee_wellknown_id_non_exist(self,
                                                                                               powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "owner": {"name": "test"}, "group": {"name": "group_test"}, "quota": None,
                                         "access_control_rights":
                                             {"access_rights": ["dir_gen_all"], "inherit_flags": "container_inherit",
                                              "access_type": "allow",
                                              "trustee": {"name": "test_group", "type": "everyone",
                                                          "provider_type": "local"}},
                                         "access_zone": "System", "state": "present", "access_control_rights_state": "add"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.get_acl = MagicMock(return_value=MockFileSystemApi.get_acl_response())
        powerscale_module_mock.auth_api.get_auth_wellknowns.to_dict = MagicMock(return_value={})
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'invalid_wellknown_exception'), FilesystemHandler)

    def test_get_group_id_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "owner": {"name": "test"}, "group": {"name": "group_test"},
                                         "access_zone": "System", "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.auth_api.get_auth_group = MagicMock(side_effect=MockApiException)
        powerscale_module_mock.determine_error = MagicMock()
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'get_group_id_exception'), FilesystemHandler)

    def test_modify_group_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "group": {"name": "group_test", "provider_type": "ads"},
                                         "access_zone": "System", "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.get_filesystem = MagicMock(return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.get_acl = MagicMock(
            return_value=MockFileSystemApi.get_acl_response())
        powerscale_module_mock.is_acl_rights_modified = MagicMock(return_value=False)
        powerscale_module_mock.is_owner_modified = MagicMock(return_value=False)
        powerscale_module_mock.namespace_api.set_acl = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'modify_group_exception'), FilesystemHandler)

    def test_modify_file_system_with_check_mode(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "owner": {"name": "test"}, "group": {"name": "group_test"},
                                         "access_control_rights":
                                             {"access_rights": ["dir_gen_all"], "inherit_flags": "container_inherit",
                                              "access_type": "allow",
                                              "trustee": {"name": "test_user", "type": "user",
                                                          "provider_type": "local"}},
                                         "access_zone": "System", "state": "present", "access_control_rights_state": "add"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.get_acl = MagicMock(return_value=MockFileSystemApi.get_acl_response())
        powerscale_module_mock.get_acl_object = MagicMock()
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']

    def test_access_control_rights_validation(self, powerscale_module_mock):
        self.set_module_params(self.get_filesystem_args,
                               {"path": self.path1, "owner": {"name": "test"}, "group": {"name": "group_test"},
                                "access_control_rights":
                                    {"access_type": "allow", "access_rights": None, "inherit_flags": None,
                                     "trustee": {"name": "test_user", "type": "user", "provider_type": "local"}},
                                "access_zone": "System", "state": "present", "access_control_rights_state": "add"})
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'acl_validation_exception'), FilesystemHandler)

    def test_file_system_create_quota(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1,
                                         "access_zone": "System",
                                         "quota": {
                                             "thresholds_on": "fs_logical_size",
                                             "soft_limit_size": 5,
                                             "hard_limit_size": 10,
                                             "cap_unit": "GB",
                                             "container": True,
                                             "quota_state": "present",
                                         },
                                         "list_snapshots": True,
                                         "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.get_quota = MagicMock(return_value=MockFileSystemApi.QUOTA_DETAILS)
        powerscale_module_mock.get_quota_param = MagicMock(return_value=None)
        powerscale_module_mock.quota_api.create_quota_quota = MagicMock(return_value=None)
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        powerscale_module_mock.quota_api.create_quota_quota.assert_called()

    def test_file_system_create_quota_get_quota_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1,
                                         "access_zone": "System",
                                         "quota": {
                                             "thresholds_on": "fs_logical_size",
                                             "soft_limit_size": 5,
                                             "hard_limit_size": 10,
                                             "cap_unit": "GB",
                                             "container": True,
                                             "quota_state": "present",
                                         },
                                         "list_snapshots": True,
                                         "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.get_quota = MagicMock(
            return_value=MockFileSystemApi.QUOTA_DETAILS
        )
        powerscale_module_mock.isi_sdk.QuotaQuotaCreateParams = MagicMock(side_effect=MockApiException)
        utils.determine_error = MagicMock(return_value=None)
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'create_quota_error_exception'), FilesystemHandler)

    def test_file_system_modify_quota(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1,
                                         "access_zone": "System",
                                         "quota": {
                                             "thresholds_on": "fs_logical_size",
                                             "soft_limit_size": 5,
                                             "hard_limit_size": 10,
                                             "cap_unit": "GB",
                                             "container": True,
                                             "quota_state": "present",
                                         },
                                         "list_snapshots": True,
                                         "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.protocol_api = MagicMock()
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.quota_api.update_quota_quota = MagicMock(return_value=True)
        utils.determine_error = MagicMock(return_value=None)
        FilesystemHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_file_system_create_quota_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1,
                                         "access_zone": "System",
                                         "quota": {
                                             "thresholds_on": "fs_logical_size",
                                             "soft_limit_size": 5,
                                             "hard_limit_size": 10,
                                             "cap_unit": "GB",
                                             "container": True,
                                             "quota_state": "present",
                                         },
                                         "list_snapshots": True,
                                         "state": "present"})
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.get_quota = MagicMock(return_value=MockFileSystemApi.QUOTA_DETAILS)
        powerscale_module_mock.get_quota_param = MagicMock(return_value=None)
        powerscale_module_mock.quota_api.create_quota_quota = MagicMock(side_effect=MockApiException)
        utils.determine_error = MagicMock(return_value=None)
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'create_quota_error_exception'), FilesystemHandler)

    def test_file_system_modify_quota_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1,
                                         "access_zone": "System",
                                         "quota": {
                                             "thresholds_on": "fs_logical_size",
                                             "soft_limit_size": 5,
                                             "hard_limit_size": 10,
                                             "cap_unit": "GB",
                                             "container": True,
                                             "quota_state": "present",
                                         },
                                         "list_snapshots": True,
                                         "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.quota_api = MagicMock()
        powerscale_module_mock.namespace_api.get_directory_metadata = MagicMock()
        powerscale_module_mock.quota_api.list_quota_quotas = MagicMock()
        powerscale_module_mock.namespace_api.get_acl = MagicMock()
        utils.get_threshold_overhead_parameter = MagicMock()
        utils.get_size_bytes = MagicMock()
        powerscale_module_mock.get_container_param = MagicMock()
        powerscale_module_mock.quota_api.update_quota_quota = MagicMock(side_effect=MockApiException)
        powerscale_module_mock.determine_error = MagicMock(return_value=None)
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'update_quota_exception'), FilesystemHandler)

    def test_file_system_get_quota_update_param_exception(self, powerscale_module_mock):
        self.get_filesystem_args.update({"path": self.path1,
                                         "access_zone": "System",
                                         "quota": {
                                             "thresholds_on": "fs_logical_size",
                                             "soft_limit_size": 5,
                                             "hard_limit_size": 10,
                                             "cap_unit": "GB",
                                             "container": True,
                                             "quota_state": "present",
                                         },
                                         "list_snapshots": True,
                                         "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.module.params = self.get_filesystem_args
        powerscale_module_mock.quota_api = MagicMock()
        powerscale_module_mock.namespace_api.get_directory_metadata = MagicMock()
        powerscale_module_mock.quota_api.list_quota_quotas = MagicMock()
        powerscale_module_mock.namespace_api.get_acl = MagicMock()
        utils.get_threshold_overhead_parameter = MagicMock()
        utils.get_size_bytes = MagicMock()
        powerscale_module_mock.get_container_param = MagicMock()
        powerscale_module_mock.isi_sdk.QuotaQuota = MagicMock(
            side_effect=MockApiException)
        powerscale_module_mock.determine_error = MagicMock(return_value=None)
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'get_quota_update_param_exception'), FilesystemHandler)

    def test_file_system_get_identity_exception(self, powerscale_module_mock):
        self.set_module_params(self.get_filesystem_args,
                               {"path": self.path1,
                                "owner": {"name": "test"},
                                "group": {"name": "group_test"},
                                "access_control_rights":
                                {
                                    "access_rights": "dir_gen_all",
                                    "inherit_flags": "container_inherit",
                                    "access_type": "allow",
                                    "trustee": {"name": "group_test", "type": "group",
                                                "provider_type": "local"}},
                                "state": "present",
                                "access_control_rights_state": "add"})
        powerscale_module_mock.module.check_mode = False
        utils.get_acl_object = MagicMock()
        powerscale_module_mock.get_filesystem = MagicMock(return_value=None)
        powerscale_module_mock.get_acl_object = MagicMock(return_value=True)
        powerscale_module_mock.auth_api.get_mapping_identity = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses('get_identity_exception'), FilesystemHandler)

    def test_file_system_delete_group_access_control_rights(self, powerscale_module_mock):
        self.set_module_params(self.get_filesystem_args,
                               {"path": self.path1,
                                "access_control_rights":
                                {
                                    "access_rights": "dir_gen_all",
                                    "inherit_flags": "container_inherit",
                                    "access_type": "allow",
                                    "trustee": {"name": "group_test", "type": "group",
                                                "provider_type": "local"}},
                                "state": "present",
                                "access_control_rights_state": "remove"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.get_quota = MagicMock(return_value=MockFileSystemApi.QUOTA_DETAILS_1)
        powerscale_module_mock.get_acl_object = MagicMock()
        utils.get_acl_object = MagicMock()
        powerscale_module_mock.auth_api.get_mapping_identity.to_dict = \
            MagicMock(return_value=MockFileSystemApi.GROUP_IDENTITY_DETAIL)
        FilesystemHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        print(powerscale_module_mock.module.exit_json.call_args[1])
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] \
            and powerscale_module_mock.module.exit_json.call_args[1]['modify_filesystem']

    def test_file_system_delete_user_access_control_rights(self, powerscale_module_mock):
        self.set_module_params(self.get_filesystem_args,
                               {"path": self.path1,
                                "access_control_rights":
                                {
                                    "access_rights": "dir_gen_all",
                                    "inherit_flags": "container_inherit",
                                    "access_type": "allow",
                                    "trustee": {"name": "test_user", "type": "user",
                                                "provider_type": "local"}},
                                "state": "present",
                                "access_control_rights_state": "remove"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_filesystem = MagicMock(return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        powerscale_module_mock.get_quota = MagicMock(return_value=MockFileSystemApi.QUOTA_DETAILS_1)
        powerscale_module_mock.get_acl_object = MagicMock()
        utils.get_acl_object = MagicMock()
        powerscale_module_mock.auth_api.get_mapping_identity.to_dict = \
            MagicMock(return_value=MockFileSystemApi.GROUP_IDENTITY_DETAIL)
        FilesystemHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        print(powerscale_module_mock.module.exit_json.call_args[1])
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] \
            and powerscale_module_mock.module.exit_json.call_args[1]['modify_filesystem']
