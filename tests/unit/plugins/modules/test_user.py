# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for User module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import patch, MagicMock

from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase
from ansible_collections.dellemc.powerscale.plugins.modules.user import User, get_user_parameters
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_user_api \
    import MockUserApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible.module_utils.compat.version import LooseVersion

utils.pkg_resources = MagicMock()
utils.parse_version = LooseVersion


class TestUser(PowerScaleUnitBase):
    user_args = MockUserApi.USER_COMMON_ARGS

    @pytest.fixture
    def module_object(self, mocker):
        # mock cluster config for version check
        mock_cluster_api = mocker.patch(
            MockUserApi.MODULE_UTILS_PATH + '.isi_sdk.ClusterApi')
        mock_cluster_instance = mock_cluster_api.return_value
        mock_response = MagicMock()
        mock_config = {
            'onefs_version': {
                'release': '9.8.0'
            }
        }
        mock_response.to_dict.return_value = mock_config
        mock_cluster_instance.get_cluster_config.return_value = mock_response
        return User

    def test_get_user_details(self, powerscale_module_mock):
        self.set_module_params(self.user_args, {
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': "Isilon Users",
            'state': 'present'})
        mock_api_response = MagicMock()
        mock_user = MagicMock()
        mock_user.to_dict.return_value = MockUserApi.GET_USER_DETAILS
        mock_api_response.users = [mock_user]
        powerscale_module_mock.api_instance.get_auth_user.return_value = mock_api_response

        # path: get role by name
        # mock roles properties
        mock_api_response = MagicMock()
        mock_role = MagicMock()
        mock_role.id = "AuditAdmin"
        mock_member = MagicMock()
        mock_member.name = "test_user_1"
        mock_member.id = "UID:7000"
        mock_role.members = [mock_member]
        mock_api_response.roles = [mock_role]
        powerscale_module_mock.api_instance.list_auth_roles.return_value = mock_api_response
        powerscale_module_mock.perform_module_operation()
        assert "7000" in powerscale_module_mock.module.exit_json.call_args[
            1]['user_details']['uid']['id']

        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'access_zone': "System",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': "Isilon Users",
            'role_name': 'AuditAdmin',
            'role_state': 'present-for-user',
            'state': 'present'})
        powerscale_module_mock.perform_module_operation()
        assert "7000" in powerscale_module_mock.module.exit_json.call_args[
            1]['user_details']['uid']['id']

        # path: don't get role by name with non-system zone
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'access_zone': "non-System",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': "Isilon Users",
            'state': 'present'})
        powerscale_module_mock.perform_module_operation()
        assert "7000" in powerscale_module_mock.module.exit_json.call_args[
            1]['user_details']['uid']['id']

    def test_get_user_details_exception(self, powerscale_module_mock):
        self.set_module_params(self.user_args, {
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': "Isilon Users",
            'state': 'present'})
        with patch.object(powerscale_module_mock.api_instance,
                          'get_auth_user',
                          side_effect=MockApiException):
            self.capture_fail_json_call(MockUserApi.get_error_responses(
                "get_user_details_error"), invoke_perform_module=True)
        with patch.object(powerscale_module_mock.api_instance,
                          'get_auth_user',
                          side_effect=Exception):
            self.capture_fail_json_call(MockUserApi.get_error_responses(
                "get_user_details_error"), invoke_perform_module=True)
        with patch.object(powerscale_module_mock.api_instance,
                          'list_auth_roles',
                          side_effect=MockApiException):
            self.powerscale_module_mock.perform_module_operation()

    def test_create_user_with_id(self, powerscale_module_mock):
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': "Isilon Users",
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[None, MockUserApi.GET_USER_DETAILS])
        utils.isi_sdk.AuthUserCreateParams = MagicMock(
            return_value=MockUserApi.CREATE_USER_WITH_ID)
        powerscale_module_mock.api_instance.create_auth_user = MagicMock(
            return_value=7000)
        powerscale_module_mock.perform_module_operation()
        assert "7000" in powerscale_module_mock.module.exit_json.call_args[
            1]['user_details']['uid']['id']

    def test_create_user_with_non_existing_id(self, powerscale_module_mock):
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 404,
            'access_zone': "System",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': "Isilon Users",
            'state': 'present'})
        utils.isi_sdk.AuthUserCreateParams = MagicMock(
            return_value=MockUserApi.CREATE_USER_WITH_ID)
        powerscale_module_mock.api_instance.create_auth_user = MagicMock(
            return_value=7000)
        mock_api_response = MagicMock()
        mock_user = MagicMock()
        mock_user.to_dict.return_value = MockUserApi.GET_USER_DETAILS
        mock_api_response.users = [mock_user]
        with patch.object(powerscale_module_mock.api_instance,
                          'get_auth_user',
                          side_effect=[MockApiException(404), mock_api_response]):
            powerscale_module_mock.perform_module_operation()
            assert "test_user_1" in powerscale_module_mock.module.exit_json.call_args[
                1]['user_details']['uid']['name']

    def test_create_user_with_non_username_password(self, powerscale_module_mock):
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 404,
            'access_zone': "System",
            'provider_type': "local",
            'full_name': 'Test User',
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': "Isilon Users",
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[None])
        self.capture_fail_json_call(MockUserApi.get_error_responses(
            "create_user_with_empty_password"), powerscale_module_mock, invoke_perform_module=True)

        self.set_module_params(self.user_args, {
            'user_id': 404,
            'access_zone': "System",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': "Isilon Users",
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[None])
        self.capture_fail_json_call(MockUserApi.get_error_responses(
            "create_user_with_empty_name"), powerscale_module_mock, invoke_perform_module=True)

    def test_create_user_with_id_exception(self, powerscale_module_mock):
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': "Isilon Users",
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[None, MockUserApi.GET_USER_DETAILS])
        utils.isi_sdk.AuthUserCreateParams = MagicMock(
            return_value=MockUserApi.CREATE_USER_WITH_ID)
        powerscale_module_mock.api_instance.create_auth_user = MagicMock(
            side_effect=Exception)
        self.capture_fail_json_call(MockUserApi.get_error_responses(
            "get_create_user_id"), powerscale_module_mock, invoke_perform_module=True)

    def test_create_user_with_non_local_provider_exception(self, powerscale_module_mock):
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "ldap",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': "Isilon Users",
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[None, MockUserApi.GET_USER_DETAILS])
        utils.isi_sdk.AuthUserCreateParams = MagicMock(
            return_value=MockUserApi.CREATE_USER_WITH_ID)
        powerscale_module_mock.api_instance.create_auth_user = MagicMock(
            side_effect=Exception)
        self.capture_fail_json_call(MockUserApi.get_error_responses(
            "create_user_with_non_local_provider"), powerscale_module_mock, invoke_perform_module=True)

    def test_create_user_with_existing_id_different_name(self, powerscale_module_mock):
        # existing id, but user_name param is different from existing name
        # check_if_id_exists will return true
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1_error",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': "Isilon Users",
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[MockUserApi.GET_USER_DETAILS])
        self.capture_fail_json_call(MockUserApi.get_error_responses(
            "create_user_with_existing_id"), powerscale_module_mock, invoke_perform_module=True)

    def test_set_validate_params(self, powerscale_module_mock):
        # Test with get_zones_summary_zone error
        self.set_module_params(self.user_args, {
            'access_zone': "test-zone",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'home_directory': "test_user_1",
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': 'Isilon Users',
            'role_name': 'AuditAdmin',
            'state': 'present'})
        with patch.object(powerscale_module_mock.zone_summary_api,
                          'get_zones_summary_zone',
                          side_effect=MockApiException):
            self.capture_fail_json_call(MockUserApi.get_error_responses(
                "error_fetch_base_path"), invoke_perform_module=True)

        # Test without user_name and user_id
        self.set_module_params(self.user_args, {
            'access_zone': "test-zone",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'home_directory': "test_user_1",
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': 'Isilon Users',
            'role_name': 'AuditAdmin',
            'state': 'present'})
        powerscale_module_mock.zone_summary_api.get_zones_summary_zone = MagicMock(
            return_value=MockSDKResponse(MockUserApi.ZONE_SUMMARY))
        self.capture_fail_json_call(MockUserApi.get_error_responses(
            "param_error_user_id_and_name"), invoke_perform_module=True)

        # Test with wrong email
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "test-zone",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'home_directory': "test_user_1",
            'email': 'fake_email',
            'shell': "/usr/local/bin/zsh",
            'primary_group': 'Isilon Users',
            'role_name': 'AuditAdmin',
            'state': 'present'})
        powerscale_module_mock.zone_summary_api.get_zones_summary_zone = MagicMock(
            return_value=MockSDKResponse(MockUserApi.ZONE_SUMMARY))
        self.capture_fail_json_call(MockUserApi.get_error_responses(
            "param_error_email_format"), invoke_perform_module=True)

        # Test with role_name and role_state
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "test-zone",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'home_directory': "test_user_1",
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': 'Isilon Users',
            'role_name': 'AuditAdmin',
            'state': 'present'})
        powerscale_module_mock.zone_summary_api.get_zones_summary_zone = MagicMock(
            return_value=MockSDKResponse(MockUserApi.ZONE_SUMMARY))
        self.capture_fail_json_call(MockUserApi.get_error_responses(
            "param_error_role_name_and_state"), invoke_perform_module=True)

        # Test with role and non-default zone
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "test-zone",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'home_directory': "test_user_1",
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': 'Isilon Users',
            'role_name': 'AuditAdmin',
            'role_state': 'present-for-user',
            'state': 'present'})
        powerscale_module_mock.zone_summary_api.get_zones_summary_zone = MagicMock(
            return_value=MockSDKResponse(MockUserApi.ZONE_SUMMARY))
        self.capture_fail_json_call(MockUserApi.get_error_responses(
            "param_error_role_and_zone"), invoke_perform_module=True)

    def test_modify_user(self, powerscale_module_mock):
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'home_directory': "/home/test_user_1",
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': 'Isilon Users',
            'role_name': 'AuditAdmin',
            'role_state': 'present-for-user',
            'enabled': True,
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[MockUserApi.GET_USER_DETAILS, MockUserApi.GET_USER_DETAILS])
        powerscale_module_mock.perform_module_operation()
        assert "7000" in powerscale_module_mock.module.exit_json.call_args[
            1]['user_details']['uid']['id']

    def test_modify_user_exception(self, powerscale_module_mock):
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'home_directory': "/home/test_user_1",
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': 'Isilon Users',
            'role_name': 'AuditAdmin',
            'role_state': 'present-for-user',
            'enabled': True,
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[MockUserApi.GET_USER_DETAILS, MockUserApi.GET_USER_DETAILS])
        with patch.object(powerscale_module_mock.api_instance,
                          'update_auth_user',
                          side_effect=[MockApiException]):
            self.capture_fail_json_call(MockUserApi.get_error_responses(
                "update_user_error"), invoke_perform_module=True)

    def test_modify_user_without_changes(self, powerscale_module_mock):
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'password': 'test_user_password_placeholder',
            'email': 'test_user_2@gamil.com',
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[MockUserApi.GET_USER_DETAILS, MockUserApi.GET_USER_DETAILS])
        powerscale_module_mock.perform_module_operation()
        assert "7000" in powerscale_module_mock.module.exit_json.call_args[
            1]['user_details']['uid']['id']

    def test_modify_user_password(self, powerscale_module_mock):
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'full_name': 'Test User',
            'update_password': 'always',
            'password': 'test_user_password_placeholder',
            'home_directory': "/home/test_user_1",
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': 'Isilon Users',
            'role_name': 'AuditAdmin',
            'role_state': 'present-for-user',
            'enabled': True,
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[MockUserApi.GET_USER_DETAILS, MockUserApi.GET_USER_DETAILS])
        with patch.object(powerscale_module_mock,
                          "array_version",
                          new="9.4.0"):
            powerscale_module_mock.perform_module_operation()
            assert "7000" in powerscale_module_mock.module.exit_json.call_args[
                1]['user_details']['uid']['id']

    def test_modify_user_add_role_exception(self, powerscale_module_mock):
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'full_name': 'Test User',
            'update_password': 'always',
            'password': 'test_user_password_placeholder',
            'home_directory': "/home/test_user_1",
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': 'Isilon Users',
            'role_name': 'AuditAdmin',
            'role_state': 'present-for-user',
            'enabled': True,
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            return_value=MockUserApi.GET_USER_DETAILS
        )
        powerscale_module_mock.get_roles_for_user = MagicMock(
            return_value=[]
        )
        with patch.object(powerscale_module_mock, "array_version", new="9.4.0"):
            with patch.object(powerscale_module_mock.role_api_instance,
                              'create_role_member',
                              side_effect=MockApiException):
                self.capture_fail_json_call(MockUserApi.get_error_responses(
                    "update_user_add_role_error"), invoke_perform_module=True)

    def test_modify_user_password_exception(self, powerscale_module_mock):
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'full_name': 'Test User',
            'update_password': 'always',
            'password': 'test_user_password_placeholder',
            'home_directory': "/home/test_user_1",
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': 'Isilon Users',
            'role_name': 'AuditAdmin',
            'role_state': 'present-for-user',
            'enabled': True,
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[MockUserApi.GET_USER_DETAILS, MockUserApi.GET_USER_DETAILS])
        with patch.object(powerscale_module_mock, 'array_version', new="9.4.0"):
            with patch.object(powerscale_module_mock.api_instance,
                              'update_auth_user',
                              side_effect=[None, MockApiException]):
                self.capture_fail_json_call(MockUserApi.get_error_responses(
                    "update_password_error"), invoke_perform_module=True)

    def test_modify_user_remove_role(self, powerscale_module_mock):
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'full_name': 'Test User',
            'update_password': 'always',
            'password': 'test_user_password_placeholder',
            'home_directory': "/home/test_user_1",
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': 'Isilon Users',
            'role_name': 'AuditAdmin',
            'role_state': 'absent-for-user',
            'enabled': True,
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[MockUserApi.GET_USER_DETAILS, MockUserApi.GET_USER_DETAILS])
        mock_api_response = MagicMock()
        mock_role = MagicMock()
        mock_role.id = "AuditAdmin"
        mock_member = MagicMock()
        mock_member.name = "test_user_1"
        mock_member.id = "UID:7000"
        mock_role.members = [mock_member]
        mock_api_response.roles = [mock_role]

        with patch.multiple(
                powerscale_module_mock,
                array_version="9.4.0",
                api_instance=MagicMock(list_auth_roles=MagicMock(
                    return_value=mock_api_response)),  # Mock API call
                role_api_instance=MagicMock(
                    delete_role_member=MagicMock())  # Mock deletion
        ):
            powerscale_module_mock.perform_module_operation()
            assert powerscale_module_mock.role_api_instance.delete_role_member.call_count > 0

    def test_modify_user_remove_role_exception(self, powerscale_module_mock):
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'full_name': 'Test User',
            'update_password': 'always',
            'password': 'test_user_password_placeholder',
            'home_directory': "/home/test_user_1",
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': 'Isilon Users',
            'role_name': 'AuditAdmin',
            'role_state': 'absent-for-user',
            'enabled': True,
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[MockUserApi.GET_USER_DETAILS])
        with patch.multiple(
                powerscale_module_mock,
                array_version="9.4.0",
                is_user_part_of_role=lambda *args, **kwargs: True):
            with patch.object(powerscale_module_mock.role_api_instance,
                              'delete_role_member',
                              side_effect=[MockApiException]):
                self.capture_fail_json_call(MockUserApi.get_error_responses(
                    "update_user_remove_role_error"), invoke_perform_module=True)

    def test_user_parameters_include_password_expires_and_expiry(self):
        # AC-001, AC-002: both parameters are part of the module argument spec
        user_params = get_user_parameters()
        assert user_params['password_expires']['type'] == 'bool'
        assert user_params['expiry']['type'] == 'int'

    def test_create_user_password_expires_non_local_provider_exception(self, powerscale_module_mock):
        # FR-5.1: password_expires is restricted to local users, and the error
        # must name the parameter rather than the generic create-provider message
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'access_zone': "System",
            'provider_type': "ldap",
            'password': 'test_user_password_placeholder',
            'password_expires': True,
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[None, MockUserApi.GET_USER_DETAILS])
        self.capture_fail_json_call(MockUserApi.get_error_responses(
            "password_expires_non_local_provider"), invoke_perform_module=True)

    def test_password_expires_local_provider_accepted(self, powerscale_module_mock):
        # FR-1: local provider passes validation without failing the module
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'access_zone': "System",
            'provider_type': "local",
            'password': 'test_user_password_placeholder',
            'password_expires': True,
            'state': 'present'})
        powerscale_module_mock.validate_local_only_params("local")
        powerscale_module_mock.module.fail_json.assert_not_called()

    def test_create_user_expiry_non_local_provider_exception(self, powerscale_module_mock):
        # FR-5.1: expiry is restricted to local users
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'access_zone': "System",
            'provider_type': "ads",
            'password': 'test_user_password_placeholder',
            'expiry': MockUserApi.VALID_EXPIRY,
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[None, MockUserApi.GET_USER_DETAILS])
        self.capture_fail_json_call(MockUserApi.get_error_responses(
            "expiry_non_local_provider"), invoke_perform_module=True)

    @pytest.mark.parametrize("invalid_expiry", [-1, 4294967296, 5000000000])
    def test_create_user_expiry_out_of_range_exception(self, powerscale_module_mock, invalid_expiry):
        # FR-5.2: expiry must fall within the PAPI schema range 0..4294967295
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'access_zone': "System",
            'provider_type': "local",
            'password': 'test_user_password_placeholder',
            'expiry': invalid_expiry,
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[None, MockUserApi.GET_USER_DETAILS])
        self.capture_fail_json_call(MockUserApi.get_error_responses(
            "expiry_out_of_range"), invoke_perform_module=True)

    @pytest.mark.parametrize("invalid_expiry", ["2024-10-22T00:00:00", 1729564800.5, True])
    def test_create_user_expiry_invalid_type_exception(self, powerscale_module_mock, invalid_expiry):
        # FR-5.2: non-integer expiry values are rejected with the epoch message.
        # Booleans are rejected explicitly: bool is a subclass of int in Python,
        # so True would otherwise silently pass as epoch 1.
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'access_zone': "System",
            'provider_type': "local",
            'password': 'test_user_password_placeholder',
            'expiry': invalid_expiry,
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[None, MockUserApi.GET_USER_DETAILS])
        self.capture_fail_json_call(MockUserApi.get_error_responses(
            "expiry_invalid_type"), invoke_perform_module=True)

    @pytest.mark.parametrize("valid_expiry", [0, 1729564800, 4294967295])
    def test_expiry_valid_timestamp_accepted(self, powerscale_module_mock, valid_expiry):
        # FR-2: boundary values 0 and 4294967295 are inclusive and accepted
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'access_zone': "System",
            'provider_type': "local",
            'password': 'test_user_password_placeholder',
            'expiry': valid_expiry,
            'state': 'present'})
        powerscale_module_mock.validate_expiry()
        powerscale_module_mock.module.fail_json.assert_not_called()

    def test_expiry_non_local_provider_no_api_call(self, powerscale_module_mock):
        # FR-5.1: validation fires before any create/update API call
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'access_zone': "System",
            'provider_type': "ldap",
            'password': 'test_user_password_placeholder',
            'expiry': MockUserApi.VALID_EXPIRY,
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[None, MockUserApi.GET_USER_DETAILS])
        powerscale_module_mock.api_instance.create_auth_user = MagicMock()
        self.capture_fail_json_call(MockUserApi.get_error_responses(
            "expiry_non_local_provider"), invoke_perform_module=True)
        powerscale_module_mock.api_instance.create_auth_user.assert_not_called()

    # ================================================================
    # Phase 2: Create/Update Wiring and Idempotency
    # ================================================================

    def test_create_user_with_password_expires_and_expiry(self, powerscale_module_mock):
        """AC-001, AC-002: password_expires and expiry are forwarded to
        AuthUserCreateParams during user creation."""
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'password': 'test_user_password_placeholder',
            'password_expires': False,
            'expiry': MockUserApi.VALID_EXPIRY,
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[None, MockUserApi.get_user_details(
                password_expires=False, expiry=MockUserApi.VALID_EXPIRY)])
        utils.isi_sdk.AuthUserCreateParams = MagicMock(
            return_value=MockUserApi.CREATE_USER_WITH_ID)
        powerscale_module_mock.api_instance.create_auth_user = MagicMock(
            return_value=7000)
        powerscale_module_mock.perform_module_operation()
        # Assert that AuthUserCreateParams received the new parameters
        create_kwargs = utils.isi_sdk.AuthUserCreateParams.call_args[1]
        assert create_kwargs.get('password_expires') is False, \
            "password_expires must be forwarded to AuthUserCreateParams"
        assert create_kwargs.get('expiry') == MockUserApi.VALID_EXPIRY, \
            "expiry must be forwarded to AuthUserCreateParams"

    def test_modify_user_preserve_password_expires_when_omitted(self, powerscale_module_mock):
        """FR-3 / AC-004: when password_expires is not specified on update,
        the existing value must be preserved (no API call to change it)."""
        user_details = MockUserApi.get_user_details(
            password_expires=True, expiry=MockUserApi.VALID_EXPIRY)
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'password': 'test_user_password_placeholder',
            'email': 'test_user_2@gamil.com',
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[user_details, user_details])
        powerscale_module_mock.perform_module_operation()
        # changed must be False — nothing was modified
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_modify_user_preserve_expiry_when_omitted(self, powerscale_module_mock):
        """FR-3 / AC-004: when expiry is not specified on update,
        the existing value must be preserved."""
        user_details = MockUserApi.get_user_details(
            password_expires=True, expiry=MockUserApi.VALID_EXPIRY)
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'password': 'test_user_password_placeholder',
            'email': 'test_user_2@gamil.com',
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[user_details, user_details])
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_modify_user_explicit_expiry_zero_clears_expiry(self, powerscale_module_mock):
        """FR-3 / AC-004: explicit expiry=0 clears account expiry and
        reports changed=True."""
        user_details_before = MockUserApi.get_user_details(
            password_expires=True, expiry=MockUserApi.VALID_EXPIRY)
        user_details_after = MockUserApi.get_user_details(
            password_expires=True, expiry=0)
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'password': 'test_user_password_placeholder',
            'email': 'test_user_2@gamil.com',
            'expiry': 0,
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[user_details_before, user_details_after])
        utils.isi_sdk.AuthUser = MagicMock(return_value=MagicMock())
        powerscale_module_mock.api_instance.update_auth_user = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        # Verify update_auth_user was called (i.e. the change was sent)
        powerscale_module_mock.api_instance.update_auth_user.assert_called()

    def test_modify_user_password_expires_change_reports_changed_true(self, powerscale_module_mock):
        """FR-3 / AC-004: toggling password_expires from True to False
        reports changed=True."""
        user_details_before = MockUserApi.get_user_details(
            password_expires=True, expiry=MockUserApi.VALID_EXPIRY)
        user_details_after = MockUserApi.get_user_details(
            password_expires=False, expiry=MockUserApi.VALID_EXPIRY)
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'password': 'test_user_password_placeholder',
            'email': 'test_user_2@gamil.com',
            'password_expires': False,
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[user_details_before, user_details_after])
        utils.isi_sdk.AuthUser = MagicMock(return_value=MagicMock())
        powerscale_module_mock.api_instance.update_auth_user = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_user_identical_params_reports_changed_false(self, powerscale_module_mock):
        """AC-004: when all supplied params match existing state,
        changed must be False (idempotent)."""
        user_details = MockUserApi.get_user_details(
            password_expires=True, expiry=MockUserApi.VALID_EXPIRY)
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'password': 'test_user_password_placeholder',
            'email': 'test_user_2@gamil.com',
            'password_expires': True,
            'expiry': MockUserApi.VALID_EXPIRY,
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[user_details, user_details])
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # ================================================================
    # Phase 3: Check Mode and Diff Support
    # ================================================================

    def test_modify_password_expires_check_mode_diff(self, powerscale_module_mock):
        """FR-4, FR-5, AC-003: in check mode, password_expires change is
        reported via changed=True and result['diff'] without calling the API."""
        user_details_before = MockUserApi.get_user_details(
            password_expires=True, expiry=MockUserApi.VALID_EXPIRY)
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'password': 'test_user_password_placeholder',
            'email': 'test_user_2@gamil.com',
            'password_expires': False,
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[user_details_before, user_details_before])
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.module._diff = True
        powerscale_module_mock.api_instance.update_auth_user = MagicMock()
        powerscale_module_mock.perform_module_operation()
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result['changed'] is True
        # API must NOT have been called
        powerscale_module_mock.api_instance.update_auth_user.assert_not_called()
        # Diff must show before/after for password_expires
        assert 'diff' in result
        assert result['diff']['before']['password_expires'] is True
        assert result['diff']['after']['password_expires'] is False

    def test_modify_expiry_check_mode_diff(self, powerscale_module_mock):
        """FR-4, FR-5, AC-003: in check mode, expiry change is reported
        via changed=True and result['diff'] without calling the API."""
        user_details_before = MockUserApi.get_user_details(
            password_expires=True, expiry=MockUserApi.VALID_EXPIRY)
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'password': 'test_user_password_placeholder',
            'email': 'test_user_2@gamil.com',
            'expiry': 0,
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[user_details_before, user_details_before])
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.module._diff = True
        powerscale_module_mock.api_instance.update_auth_user = MagicMock()
        powerscale_module_mock.perform_module_operation()
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result['changed'] is True
        powerscale_module_mock.api_instance.update_auth_user.assert_not_called()
        assert 'diff' in result
        assert result['diff']['before']['expiry'] == MockUserApi.VALID_EXPIRY
        assert result['diff']['after']['expiry'] == 0

    def test_check_mode_no_changes(self, powerscale_module_mock):
        """AC-003: check mode with no changes reports changed=False and
        no diff."""
        user_details = MockUserApi.get_user_details(
            password_expires=True, expiry=MockUserApi.VALID_EXPIRY)
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'password': 'test_user_password_placeholder',
            'email': 'test_user_2@gamil.com',
            'password_expires': True,
            'expiry': MockUserApi.VALID_EXPIRY,
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[user_details, user_details])
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.module._diff = True
        powerscale_module_mock.perform_module_operation()
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result['changed'] is False

    def test_diff_without_check_mode(self, powerscale_module_mock):
        """FR-5: diff output is emitted even when check_mode is False,
        as long as _diff is truthy."""
        user_details_before = MockUserApi.get_user_details(
            password_expires=True, expiry=MockUserApi.VALID_EXPIRY)
        user_details_after = MockUserApi.get_user_details(
            password_expires=False, expiry=MockUserApi.VALID_EXPIRY)
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'password': 'test_user_password_placeholder',
            'email': 'test_user_2@gamil.com',
            'password_expires': False,
            'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[user_details_before, user_details_after])
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.module._diff = True
        utils.isi_sdk.AuthUser = MagicMock(return_value=MagicMock())
        powerscale_module_mock.api_instance.update_auth_user = MagicMock()
        powerscale_module_mock.perform_module_operation()
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result['changed'] is True
        assert 'diff' in result
        assert result['diff']['before']['password_expires'] is True
        assert result['diff']['after']['password_expires'] is False

    def test_delete_user(self, powerscale_module_mock):
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'home_directory': "/home/test_user_1",
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': 'Isilon Users',
            'role_name': 'AuditAdmin',
            'role_state': 'present-for-user',
            'state': 'absent'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[MockUserApi.GET_USER_DETAILS, None])
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[
            1]['user_details'] is None

        # will handle role deletion
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'home_directory': "/home/test_user_1",
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': 'Isilon Users',
            'role_name': 'AuditAdmin',
            'role_state': 'absent-for-user',
            'state': 'absent'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[MockUserApi.GET_USER_DETAILS, None])
        # mock roles properties
        mock_api_response = MagicMock()
        mock_role = MagicMock()
        mock_role.id = "AuditAdmin"
        mock_member = MagicMock()
        mock_member.name = "test_user_1"
        mock_member.id = "UID:7000"
        mock_role.members = [mock_member]
        mock_api_response.roles = [mock_role]
        powerscale_module_mock.api_instance.list_auth_roles.return_value = mock_api_response
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[
            1]['user_details'] is None

        # will not handle role deletion
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "non-System",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'home_directory': "/home/test_user_1",
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': 'Isilon Users',
            'state': 'absent'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[MockUserApi.GET_USER_DETAILS, None])
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[
            1]['user_details'] is None

    def test_delete_user_exception(self, powerscale_module_mock):
        # API error
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'home_directory': "/home/test_user_1",
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': 'Isilon Users',
            'role_name': 'AuditAdmin',
            'role_state': 'present-for-user',
            'state': 'absent'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[MockUserApi.GET_USER_DETAILS, None])
        with patch.object(powerscale_module_mock.api_instance,
                          'delete_auth_user',
                          side_effect=MockApiException):
            self.capture_fail_json_call(MockUserApi.get_error_responses(
                "delete_user_error"), invoke_perform_module=True)

        # delete from non local provider
        self.set_module_params(self.user_args, {
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "fake-provider",
            'full_name': 'Test User',
            'password': 'test_user_password_placeholder',
            'home_directory': "/home/test_user_1",
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': 'Isilon Users',
            'role_name': 'AuditAdmin',
            'role_state': 'present-for-user',
            'state': 'absent'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[MockUserApi.GET_USER_DETAILS, None])
        self.capture_fail_json_call(MockUserApi.get_error_responses(
            "delete_user_non_local_provider_error"), invoke_perform_module=True)
