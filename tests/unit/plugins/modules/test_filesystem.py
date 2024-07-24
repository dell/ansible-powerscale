# Copyright: (c) 2022-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for filesystem module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils
from ansible.module_utils import basic
basic.AnsibleModule = MagicMock()

from ansible_collections.dellemc.powerscale.plugins.modules.filesystem import FileSystem
from ansible_collections.dellemc.powerscale.plugins.modules.filesystem import FilesystemHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_filesystem_api \
    import MockFileSystemApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_fail_json \
    import FailJsonException, fail_json


class TestFileSystem():
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
    def filesystem_module_mock(self, mocker):
        mocker.patch(MockFileSystemApi.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        filesystem_module_mock = FileSystem()
        filesystem_module_mock.module.check_mode = False
        filesystem_module_mock.module.fail_json = fail_json
        filesystem_module_mock.module = MagicMock()
        filesystem_module_mock.namespace_api = MagicMock()
        filesystem_module_mock.quota_api = MagicMock()
        filesystem_module_mock.protocol_api = MagicMock()
        filesystem_module_mock.auth_api = MagicMock()
        return filesystem_module_mock

    def capture_fail_json_call(self, error_msg, filesystem_module_mock):
        try:
            FilesystemHandler().handle(filesystem_module_mock, filesystem_module_mock.module.params)
        except FailJsonException as fj_object:
            assert error_msg in fj_object.message

    def test_delete_file_system(self, filesystem_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "recursive_force_delete": True, "access_zone": "System", "state": "absent"})
        filesystem_module_mock.module.params = self.get_filesystem_args
        filesystem_module_mock.get_filesystem = MagicMock(return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        filesystem_module_mock.protocol_api.list_nfs_exports.to_dict = MagicMock(
            return_value=MockFileSystemApi.EMPTY_NFS_EXPORTS)
        filesystem_module_mock.protocol_api.list_smb_shares.to_dict = MagicMock(
            return_value=MockFileSystemApi.EMPTY_SMB_SHARES)
        filesystem_module_mock.module.check_mode = False
        FilesystemHandler().handle(
            filesystem_module_mock, filesystem_module_mock.module.params)
        assert filesystem_module_mock.module.exit_json.call_args[1]['changed']
        filesystem_module_mock.namespace_api.delete_directory.assert_called()

    def test_delete_file_system_check_mode(self, filesystem_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "recursive_force_delete": True, "access_zone": "System", "state": "absent"})
        filesystem_module_mock.module.params = self.get_filesystem_args
        filesystem_module_mock.get_filesystem = MagicMock(return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        filesystem_module_mock.protocol_api.list_nfs_exports.to_dict = MagicMock(
            return_value=MockFileSystemApi.EMPTY_NFS_EXPORTS)
        filesystem_module_mock.protocol_api.list_smb_shares.to_dict = MagicMock(
            return_value=MockFileSystemApi.EMPTY_SMB_SHARES)
        filesystem_module_mock.module.check_mode = True
        FilesystemHandler().handle(
            filesystem_module_mock, filesystem_module_mock.module.params)
        assert filesystem_module_mock.module.exit_json.call_args[1]['changed']

    def test_test_delete_file_system_exception(self, filesystem_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "recursive_force_delete": True, "access_zone": "System", "state": "absent"})
        filesystem_module_mock.module.params = self.get_filesystem_args
        filesystem_module_mock.protocol_api.list_nfs_exports = MagicMock(side_effect=MockApiException)
        filesystem_module_mock.determine_error = MagicMock()
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'delete_filesystem_exception'), filesystem_module_mock)

    def test_create_file_system_with_access_control_rights(self, filesystem_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "owner": {"name": "test"}, "group": {"name": "group_test"},
                                         "access_control_rights":
                                         {"access_rights": ["dir_gen_all"], "inherit_flags": "container_inherit",
                                          "access_type": "allow",
                                          "trustee": {"name": "test_user", "type": "user", "provider_type": "local"}},
                                        "access_zone": "System", "state": "present", "access_control_rights_state": "add"})
        filesystem_module_mock.module.check_mode = False
        filesystem_module_mock.module.params = self.get_filesystem_args
        filesystem_module_mock.get_filesystem = MagicMock(return_value={})
        filesystem_module_mock.get_acl_object = MagicMock(return_value=True)
        FilesystemHandler().handle(
            filesystem_module_mock, filesystem_module_mock.module.params)
        assert filesystem_module_mock.module.exit_json.call_args[1]['changed'] \
            and filesystem_module_mock.module.exit_json.call_args[1]['create_filesystem']

    def test_create_file_system_with_check_mode(self, filesystem_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "owner": {"name": "test"}, "group": {"name": "group_test"},
                                         "access_control_rights":
                                         {"access_rights": ["dir_gen_all"], "inherit_flags": "container_inherit",
                                          "access_type": "allow",
                                          "trustee": {"name": "test_user", "type": "user", "provider_type": "local"}},
                                        "access_zone": "System", "state": "present", "access_control_rights_state": "add"})
        filesystem_module_mock.module.params = self.get_filesystem_args
        filesystem_module_mock.module.check_mode = True
        filesystem_module_mock.namespace_api.get_filesystem = MagicMock(return_value={})
        filesystem_module_mock.get_acl_object = MagicMock()
        FilesystemHandler().handle(
            filesystem_module_mock, filesystem_module_mock.module.params)
        assert filesystem_module_mock.module.exit_json.call_args[1]['changed']

    def test_modify_file_system_with_access_control_rights(self, filesystem_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "owner": {"name": "test"}, "group": {"name": "group_test"},
                                         "access_control_rights":
                                         {"access_rights": ["dir_gen_all"], "inherit_flags": "container_inherit",
                                          "access_type": "allow",
                                          "trustee": {"name": "test_user", "type": "user", "provider_type": "local"}},
                                         "access_zone": "System", "state": "present", "access_control_rights_state": "add"})
        filesystem_module_mock.module.params = self.get_filesystem_args
        filesystem_module_mock.get_acl = MagicMock(return_value=MockFileSystemApi.get_acl_response())
        filesystem_module_mock.get_acl_object = MagicMock()
        FilesystemHandler().handle(
            filesystem_module_mock, filesystem_module_mock.module.params)
        assert filesystem_module_mock.module.exit_json.call_args[1]['changed'] \
            and filesystem_module_mock.module.exit_json.call_args[1]['modify_filesystem']

    def test_modify_file_system_with_check_mode(self, filesystem_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "owner": {"name": "test"}, "group": {"name": "group_test"},
                                         "access_control_rights":
                                         {"access_rights": ["dir_gen_all"], "inherit_flags": "container_inherit",
                                          "access_type": "allow",
                                          "trustee": {"name": "test_user", "type": "user", "provider_type": "local"}},
                                         "access_zone": "System", "state": "present", "access_control_rights_state": "add"})
        filesystem_module_mock.module.params = self.get_filesystem_args
        filesystem_module_mock.module.check_mode = True
        filesystem_module_mock.get_acl = MagicMock(return_value=MockFileSystemApi.get_acl_response())
        filesystem_module_mock.get_acl_object = MagicMock()
        FilesystemHandler().handle(
            filesystem_module_mock, filesystem_module_mock.module.params)
        assert filesystem_module_mock.module.exit_json.call_args[1]['changed']

    def test_access_control_rights_validation(self, filesystem_module_mock):
        self.get_filesystem_args.update({"path": self.path1, "owner": {"name": "test"}, "group": {"name": "group_test"},
                                         "access_control_rights":
                                         {"access_type": "allow", "access_rights": None, "inherit_flags": None,
                                          "trustee": {"name": "test_user", "type": "user", "provider_type": "local"}},
                                         "access_zone": "System", "state": "present", "access_control_rights_state": "add"})
        filesystem_module_mock.module.params = self.get_filesystem_args
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'acl_validation_exception'), filesystem_module_mock)

    def test_file_system_create_quota(self, filesystem_module_mock):
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
        filesystem_module_mock.module.params = self.get_filesystem_args
        filesystem_module_mock.module.check_mode = False
        filesystem_module_mock.get_filesystem = MagicMock(return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        filesystem_module_mock.get_quota = MagicMock(return_value=MockFileSystemApi.QUOTA_DETAILS)
        filesystem_module_mock.get_quota_param = MagicMock(return_value=None)
        filesystem_module_mock.quota_api.create_quota_quota = MagicMock(return_value=None)
        FilesystemHandler().handle(
            filesystem_module_mock, filesystem_module_mock.module.params)
        assert filesystem_module_mock.module.exit_json.call_args[1]["changed"] is True
        filesystem_module_mock.quota_api.create_quota_quota.assert_called()

    def test_file_system_modify_quota(self, filesystem_module_mock):
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
        filesystem_module_mock.module.params = self.get_filesystem_args
        filesystem_module_mock.protocol_api = MagicMock()
        filesystem_module_mock.module.check_mode = False
        filesystem_module_mock.quota_api.update_quota_quota = MagicMock(return_value=True)
        utils.determine_error = MagicMock(return_value=None)
        FilesystemHandler().handle(
            filesystem_module_mock, filesystem_module_mock.module.params)
        assert filesystem_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_file_system_create_quota_exception(self, filesystem_module_mock):
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
        filesystem_module_mock.module.params = self.get_filesystem_args
        filesystem_module_mock.module.check_mode = False
        filesystem_module_mock.get_filesystem = MagicMock(return_value=MockFileSystemApi.FILESYSTEM_DETAILS)
        filesystem_module_mock.get_quota = MagicMock(return_value=MockFileSystemApi.QUOTA_DETAILS)
        filesystem_module_mock.get_quota_param = MagicMock(return_value=None)
        filesystem_module_mock.quota_api.create_quota_quota = MagicMock(side_effect=MockApiException)
        utils.determine_error = MagicMock(return_value=None)
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'create_quota_exception'), filesystem_module_mock)

    def test_file_system_modify_quota_exception(self, filesystem_module_mock):
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
        filesystem_module_mock.module.check_mode = False
        filesystem_module_mock.module.params = self.get_filesystem_args
        filesystem_module_mock.quota_api = MagicMock()
        filesystem_module_mock.namespace_api.get_directory_metadata = MagicMock()
        filesystem_module_mock.quota_api.list_quota_quotas = MagicMock()
        filesystem_module_mock.namespace_api.get_acl = MagicMock()
        utils.get_threshold_overhead_parameter = MagicMock()
        utils.get_size_bytes = MagicMock()
        filesystem_module_mock.get_container_param = MagicMock()
        filesystem_module_mock.quota_api.update_quota_quota = MagicMock(side_effect=MockApiException)
        filesystem_module_mock.determine_error = MagicMock(return_value=None)
        FilesystemHandler().handle(
            filesystem_module_mock, filesystem_module_mock.module.params)
        self.capture_fail_json_call(
            MockFileSystemApi.get_error_responses(
                'update_quota_exception'), filesystem_module_mock)
