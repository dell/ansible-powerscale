# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Role module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase
from ansible_collections.dellemc.powerscale.plugins.modules.role import Role
from ansible_collections.dellemc.powerscale.plugins.modules.role import RoleHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_role_api \
    import MockRoleApi
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.auth \
    import Auth


class TestRole(PowerScaleUnitBase):
    role_args = MockRoleApi.ROLE_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return Role

    def test_create_role(self, powerscale_module_mock):
        self.set_module_params(
            self.role_args,
            {
                "privileges": [
                    {
                        "name": "Audit",
                        "permission": "w",
                        "state": "present"
                    }
                ],
                "members": [
                    {
                        "name": "esa",
                        "type": "user",
                        'provider_type': "local",
                        "state": "present"
                    }
                ]
            })
        powerscale_module_mock.get_role_details = MagicMock(return_value=None)
        powerscale_module_mock.Auth = MagicMock()
        powerscale_module_mock.Auth.get_user_details(zone="System").to_dict = MagicMock(return_value=MockRoleApi.MEMBERS)
        powerscale_module_mock.auth_api.get_auth_privileges(zone="System").to_dict = MagicMock(return_value=MockRoleApi.PRIVILEGES)
        powerscale_module_mock.auth_api.create_auth_role = MagicMock(return_value=MockRoleApi.GET_ROLE)
        RoleHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_role_without_description(self, powerscale_module_mock):
        self.set_module_params(self.role_args, {"description": ""})
        powerscale_module_mock.get_role_details = MagicMock(return_value=None)
        powerscale_module_mock.Auth = MagicMock()
        powerscale_module_mock.Auth.get_user_details(zone="System").to_dict = MagicMock(return_value=MockRoleApi.MEMBERS)
        powerscale_module_mock.auth_api.get_auth_privileges(zone="System").to_dict = MagicMock(return_value=MockRoleApi.PRIVILEGES)
        powerscale_module_mock.auth_api.create_auth_role = MagicMock(return_value=MockRoleApi.GET_ROLE)
        RoleHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_role_with_type_group(self, powerscale_module_mock):
        self.set_module_params(self.role_args,
                               {
                                   "members": [
                                       {
                                           "name": "Guest",
                                           "type": "group",
                                           'provider_type': "local",
                                           "state": "present"
                                       }
                                   ]
                               })
        powerscale_module_mock.get_role_details = MagicMock(return_value=None)
        powerscale_module_mock.Auth = MagicMock()
        powerscale_module_mock.Auth.get_user_details(zone="System").to_dict = MagicMock(return_value=MockRoleApi.MEMBERS_GROUP)
        powerscale_module_mock.auth_api.get_auth_privileges(zone="System").to_dict = MagicMock(return_value=MockRoleApi.PRIVILEGES)
        powerscale_module_mock.auth_api.create_auth_role = MagicMock(return_value=MockRoleApi.GET_ROLE_GROUP)
        RoleHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_role_with_type_wellknown(self, powerscale_module_mock):
        self.set_module_params(self.role_args,
                               {
                                   "members": [
                                       {
                                           "name": "user",
                                           "type": "wellknown",
                                           'provider_type': "local",
                                           "state": "present"
                                       }
                                   ]
                               })
        powerscale_module_mock.get_role_details = MagicMock(return_value=None)
        powerscale_module_mock.Auth = MagicMock()
        powerscale_module_mock.auth_api.get_auth_wellknowns().to_dict = MagicMock(return_value=MockRoleApi.MEMBERS_WELLKNOW)
        powerscale_module_mock.auth_api.get_auth_privileges(zone="System").to_dict = MagicMock(return_value=MockRoleApi.PRIVILEGES)
        powerscale_module_mock.auth_api.create_auth_role = MagicMock(return_value=MockRoleApi.GET_ROLE_WELLKNOWN)
        RoleHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_role_with_exception(self, powerscale_module_mock):
        self.set_module_params(self.role_args, {})
        powerscale_module_mock.get_role_details = MagicMock(return_value=None)
        powerscale_module_mock.Auth = MagicMock()
        powerscale_module_mock.Auth.get_user_details(zone="System").to_dict = MagicMock(return_value=MockRoleApi.MEMBERS)
        powerscale_module_mock.auth_api.get_auth_privileges(zone="System").to_dict = MagicMock(return_value=MockRoleApi.PRIVILEGES)
        powerscale_module_mock.auth_api.create_auth_role = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockRoleApi.get_role_exception_response('create_role_exception'),
            RoleHandler)

    def test_create_role_with_invalid_privilege(self, powerscale_module_mock):
        self.set_module_params(self.role_args,
                               {
                                   "privileges": [
                                       {
                                           "name": "test",
                                           "permission": "w",
                                           "state": "present"
                                       }
                                   ]
                               })
        powerscale_module_mock.get_role_details = MagicMock(return_value=None)
        powerscale_module_mock.Auth = MagicMock()
        powerscale_module_mock.Auth.get_user_details(zone="System").to_dict = MagicMock(return_value=MockRoleApi.MEMBERS)
        powerscale_module_mock.auth_api.get_auth_privileges(zone="System").to_dict = MagicMock(return_value=MockRoleApi.PRIVILEGES)
        powerscale_module_mock.auth_api.create_auth_role = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockRoleApi.get_role_exception_response('create_role_with_invalid_priilage'),
            RoleHandler)

    def test_delete_role(self, powerscale_module_mock):
        self.set_module_params(self.role_args,
                               {
                                   "role_name": "Test_Role",
                                   "state": "absent"
                               })
        powerscale_module_mock.auth_api.get_role.return_value = MagicMock(return_value=MockRoleApi.GET_ROLE)
        powerscale_module_mock.auth_api.delete_auth_role.return_value = MagicMock(return_value=True)
        RoleHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_role_exception(self, powerscale_module_mock):
        self.set_module_params(self.role_args,
                               {
                                   "state": "absent",
                                   "role_name": "Test_Role123"
                               })
        powerscale_module_mock.get_role = MagicMock(return_value=None)
        powerscale_module_mock.auth_api.delete_auth_role = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockRoleApi.get_role_exception_response('delete_role_exception'),
            RoleHandler)

    def test_copy_role_with_new_role_name(self, powerscale_module_mock):
        self.set_module_params(self.role_args,
                               {
                                   "copy_role": True,
                                   "new_role_name": "Test_Role_Copy",
                                   "privileges": [
                                       {
                                           "name": "Antivirus",
                                           "permission": "r",
                                           "state": "present"
                                       }
                                   ],
                                   "members": [
                                       {
                                           "name": "esa_user",
                                           "type": "user",
                                           'provider_type': "local",
                                           "state": "present"
                                       }
                                   ]
                               })
        powerscale_module_mock.get_role_details = MagicMock(return_value=None)
        powerscale_module_mock.Auth = MagicMock()
        powerscale_module_mock.Auth.get_user_details(zone="System").to_dict = MagicMock(return_value=MockRoleApi.MEMBERS)
        powerscale_module_mock.auth_api.get_auth_privileges(zone="System").to_dict = MagicMock(return_value=MockRoleApi.PRIVILEGES)
        powerscale_module_mock.auth_api.create_auth_role = MagicMock(return_value=MockRoleApi.GET_COPY_ROLE)
        RoleHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_copy_role_without_new_role_name(self, powerscale_module_mock):
        self.set_module_params(self.role_args,
                               {
                                   "copy_role": True,
                                   "privileges":
                                       [
                                           {
                                               "name": "Audit",
                                               "permission": "w",
                                               "state": "present"
                                           }
                                       ],
                                   "members":
                                       [
                                           {
                                               "name": "esa",
                                               "type": "user",
                                               'provider_type': "local",
                                               "state": "present"
                                           }
                                       ]
                               })
        powerscale_module_mock.get_role_details = MagicMock(return_value=None)
        powerscale_module_mock.Auth = MagicMock()
        powerscale_module_mock.Auth.get_user_details(zone="System").to_dict = MagicMock(return_value=MockRoleApi.MEMBERS)
        powerscale_module_mock.auth_api.get_auth_privileges(zone="System").to_dict = MagicMock(return_value=MockRoleApi.PRIVILEGES)
        powerscale_module_mock.auth_api.create_auth_role = MagicMock(return_value=MockRoleApi.GET_COPY_ROLE_WITHOUT_NEW_ROLE_NAME)
        RoleHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_role_without_role_name(self, powerscale_module_mock):
        self.set_module_params(self.role_args,
                               {
                                   "role_name": "",
                                   "privileges": [
                                       {
                                           "name": "Audit",
                                           "permission": "w",
                                           "state": "present"
                                       }
                                   ],
                                   "members": [
                                       {
                                           "name": "esa",
                                           "type": "user",
                                           'provider_type': "local",
                                           "state": "present"
                                       }
                                   ]
                               })
        self.capture_fail_json_call(
            MockRoleApi.get_role_exception_response('role_name_empty'),
            RoleHandler)

    def test_create_role_without_invalid_length_description(self, powerscale_module_mock):
        self.set_module_params(self.role_args,
                               {
                                   "description": 'PIE-IsilonS-24241-ClusterPIE-IsilonS-242PIE-IsilonS-24241-ClusterPIE-'
                                                  'IsilonS-242PIE-IsilonS-24241-ClusterPIE-IsilonS-242PIE-IsilonS-24241P'
                                                  'IE-IsilonS-24241-ClusterPIE-IsilonS-242PIE-IsilonS-24241-ClusterPIE-'
                                                  'IsilonS-242PIEPIE-IsilonS-24241PIE-IsilonS-2424123',
                                   "privileges": [
                                       {
                                           "name": "Audit",
                                           "permission": "w",
                                           "state": "present"
                                       }
                                   ],
                                   "members": [
                                       {
                                           "name": "esa",
                                           "type": "user",
                                           'provider_type': "local",
                                           "state": "present"
                                       }
                                   ]
                               })
        self.capture_fail_json_call(
            MockRoleApi.get_role_exception_response('description_invalid_length'),
            RoleHandler)

    def test_get_role_details(self, powerscale_module_mock):
        self.set_module_params(self.role_args, {"role_name": "Test_Role2"})
        powerscale_module_mock.auth_api.get_auth_role.roles[0] = MagicMock(
            return_value=MockRoleApi.GET_ROLE_RESPONSE)
        RoleHandler().handle(powerscale_module_mock,
                             powerscale_module_mock.module.params)
        powerscale_module_mock.auth_api.get_auth_role.assert_called()

    def test_get_role_details_exception(self, powerscale_module_mock):
        self.set_module_params(self.role_args, {"role_name": "Test_Role2"})
        powerscale_module_mock.auth_api.get_auth_role = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockRoleApi.get_role_exception_response('get_details_exception'),
            RoleHandler)

    def test_modify_role_priveleges_response(self, powerscale_module_mock):
        self.set_module_params(self.role_args,
                               {
                                   "role_name": "Test_Role2",
                                   "new_role_name": "Test_Role_new",
                                   "description": "Test_Description_Modify",
                                   "privileges": [
                                       {
                                           "name": "Antivirus",
                                           "permission": "w",
                                           "state": "absent"
                                       },
                                       {
                                           "name": "Console",
                                           "permission": "r",
                                           "state": "present"
                                       }
                                   ]
                               })
        powerscale_module_mock.get_role_details = MagicMock(
            return_value=MockRoleApi.GET_ROLE_RESPONSE)
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.auth_api.get_auth_privileges().to_dict = MagicMock(
            return_value=MockRoleApi.PRIVILEGE_LIST)
        RoleHandler().handle(powerscale_module_mock,
                             powerscale_module_mock.module.params)
        powerscale_module_mock.auth_api.update_auth_role.assert_called()

    def test_modify_role_priveleges_plus_response(self, powerscale_module_mock):
        self.set_module_params(self.role_args,
                               {
                                   "role_name": "Test_Role2",
                                   "privileges": [
                                       {
                                           "name": "Backup",
                                           "permission": "r",
                                           "state": "present"
                                       }
                                   ]
                               })
        powerscale_module_mock.get_role_details = MagicMock(
            return_value=MockRoleApi.GET_ROLE_RESPONSE_BACKUP_PLUS_SIG)
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.auth_api.get_auth_privileges().to_dict = MagicMock(
            return_value=MockRoleApi.PRIVILEGE_LIST_BACKUP_AUDIT)
        RoleHandler().handle(powerscale_module_mock,
                             powerscale_module_mock.module.params)
        powerscale_module_mock.auth_api.update_auth_role.assert_not_called()

    def test_modify_role_priveleges_response_1(self, powerscale_module_mock):
        self.set_module_params(self.role_args,
                               {
                                   "role_name": "Test_Role2",
                                   "new_role_name": "Test_Role_new",
                                   "description": "Test_Description_Modify",
                                   "privileges": [
                                       {
                                           "name": "Antivirus",
                                           "permission": "w",
                                           "state": "absent"
                                       },
                                       {
                                           "name": "Recovery Shell",
                                           "permission": "w",
                                           "state": "present"
                                       },
                                       {
                                           "name": "Console",
                                           "permission": "r",
                                           "state": "present"
                                       }
                                   ]
                               })
        powerscale_module_mock.get_role_details = MagicMock(
            return_value=MockRoleApi.GET_ROLE_RESPONSE)
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.auth_api.get_auth_privileges().to_dict = MagicMock(
            return_value=MockRoleApi.PRIVILEGE_LIST)
        RoleHandler().handle(powerscale_module_mock,
                             powerscale_module_mock.module.params)
        powerscale_module_mock.auth_api.update_auth_role.assert_called()

    def test_modify_role_add_members_response(self, powerscale_module_mock):
        self.set_module_params(self.role_args,
                               {
                                   "role_name": "Test_Role2",
                                   "members": [
                                       {
                                           "name": "User12_Ansible_Test_SMB",
                                           "type": "user",
                                           "state": "present"
                                       },
                                       {
                                           "name": "Group_Ansible_Test_SMB",
                                           "type": "group",
                                           "state": "present"
                                       },
                                       {
                                           "name": "Everyone",
                                           "type": "wellknown",
                                           "state": "present"
                                       }
                                   ]
                               })
        powerscale_module_mock.get_role_details = MagicMock(
            return_value=MockRoleApi.GET_ROLE_RESPONSE)
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.remove_duplicate_entries = MagicMock(
            return_value=MockRoleApi.NEW_MEMBER_LIST
        )
        Auth.get_user_details = MagicMock(return_value=MockRoleApi.USER_DETAILS)
        Auth.get_group_details = MagicMock(return_value=MockRoleApi.GROUP_DETAILS)
        Auth.get_wellknown_details = MagicMock(return_value=MockRoleApi.WELLKNOWN_DETAILS)
        RoleHandler().handle(powerscale_module_mock,
                             powerscale_module_mock.module.params)
        powerscale_module_mock.auth_api.update_auth_role.assert_called()

    def test_modify_role_remove_members_response(self, powerscale_module_mock):
        self.set_module_params(self.role_args,
                               {
                                   "role_name": "Test_Role2",
                                   "members": [
                                       {
                                           "name": "admin",
                                           "type": "user",
                                           "state": "absent"
                                       }
                                   ]
                               })
        powerscale_module_mock.get_role_details = MagicMock(
            return_value=MockRoleApi.GET_ROLE_RESPONSE)
        powerscale_module_mock.module.check_mode = False
        RoleHandler().handle(powerscale_module_mock,
                             powerscale_module_mock.module.params)
        powerscale_module_mock.auth_api.update_auth_role.assert_called()

    def test_modify_role_remove_members_exception(self, powerscale_module_mock):
        self.set_module_params(self.role_args,
                               {
                                   "role_name": "Test_Role2",
                                   "members": [
                                       {
                                           "name": "admin",
                                           "type": "user",
                                           "state": "absent"
                                       }
                                   ]
                               })
        powerscale_module_mock.get_role_details = MagicMock(
            return_value=MockRoleApi.GET_ROLE_RESPONSE)
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.auth_api.update_auth_role = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockRoleApi.get_role_exception_response('modify_exception'),
            RoleHandler)

    def test_add_role_priveleges_response(self, powerscale_module_mock):
        self.set_module_params(self.role_args,
                               {
                                   "role_name": "Test_Role1",
                                   "privileges": [
                                       {
                                           "name": "Recovery Shell",
                                           "permission": "w",
                                           "state": "present"
                                       }
                                   ]
                               })
        powerscale_module_mock.get_role_details = MagicMock(
            return_value=MockRoleApi.GET_EMPTY_ROLE_RESPONSE)
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.auth_api.get_auth_privileges().to_dict = MagicMock(
            return_value=MockRoleApi.PRIVILEGE_LIST)
        RoleHandler().handle(powerscale_module_mock,
                             powerscale_module_mock.module.params)
        powerscale_module_mock.auth_api.update_auth_role.assert_called()

    def test_add_role_members_response(self, powerscale_module_mock):
        self.set_module_params(self.role_args,
                               {
                                   "role_name": "Test_Role1",
                                   "members": [
                                       {
                                           "name": "User12_Ansible_Test_SMB",
                                           "type": "user",
                                           "state": "present"
                                       }
                                   ]

                               })
        powerscale_module_mock.get_role_details = MagicMock(
            return_value=MockRoleApi.GET_EMPTY_ROLE_RESPONSE)
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.remove_duplicate_entries = MagicMock(
            return_value=MockRoleApi.NEW_MEMBER_LIST_1)
        Auth.get_user_details = MagicMock(return_value=MockRoleApi.USER_DETAILS)
        RoleHandler().handle(powerscale_module_mock,
                             powerscale_module_mock.module.params)
        powerscale_module_mock.auth_api.update_auth_role.assert_called()
