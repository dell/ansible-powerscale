# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for User module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import patch, MagicMock
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase
from ansible_collections.dellemc.powerscale.plugins.modules.user import User
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
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_id': 7000,
                                   'access_zone': "System",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'password': '1234567',
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

        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'access_zone': "System",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'password': '1234567',
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
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'access_zone': "non-System",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'password': '1234567',
                                   'email': 'test_user_2@gamil.com',
                                   'shell': "/usr/local/bin/zsh",
                                   'primary_group': "Isilon Users",
                                   'state': 'present'})
        powerscale_module_mock.perform_module_operation()
        assert "7000" in powerscale_module_mock.module.exit_json.call_args[
            1]['user_details']['uid']['id']

    def test_get_user_details_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_id': 7000,
                                   'access_zone': "System",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'password': '1234567',
                                   'email': 'test_user_2@gamil.com',
                                   'shell': "/usr/local/bin/zsh",
                                   'primary_group': "Isilon Users",
                                   'state': 'present'})
        with patch.object(powerscale_module_mock.api_instance,
                          'get_auth_user',
                          side_effect=MockApiException):
            self.capture_fail_json_call(MockUserApi.get_error_responses(
                "get_user_details_error"), powerscale_module_mock, invoke_perform_module=True)
        with patch.object(powerscale_module_mock.api_instance,
                          'get_auth_user',
                          side_effect=Exception):
            self.capture_fail_json_call(MockUserApi.get_error_responses(
                "get_user_details_error"), powerscale_module_mock, invoke_perform_module=True)
        with patch.object(powerscale_module_mock.api_instance,
                          'list_auth_roles',
                          side_effect=MockApiException):
            self.capture_fail_json_call(MockUserApi.get_error_responses(
                "get_user_details_role_error"), powerscale_module_mock, invoke_perform_module=True)

    def test_create_user_with_id(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'user_id': 7000,
                                   'access_zone': "System",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'password': '1234567',
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
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'user_id': 404,
                                   'access_zone': "System",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'password': '1234567',
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
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
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

        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_id': 404,
                                   'access_zone': "System",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'password': '1234567',
                                   'email': 'test_user_2@gamil.com',
                                   'shell': "/usr/local/bin/zsh",
                                   'primary_group': "Isilon Users",
                                   'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[None])
        self.capture_fail_json_call(MockUserApi.get_error_responses(
            "create_user_with_empty_name"), powerscale_module_mock, invoke_perform_module=True)

    def test_create_user_with_id_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'user_id': 7000,
                                   'access_zone': "System",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'password': '1234567',
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
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'user_id': 7000,
                                   'access_zone': "System",
                                   'provider_type': "ldap",
                                   'full_name': 'Test User',
                                   'password': '1234567',
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
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1_error",
                                   'user_id': 7000,
                                   'access_zone': "System",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'password': '1234567',
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
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'access_zone': "test-zone",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'password': '1234567',
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
                "error_fetch_base_path"), powerscale_module_mock, invoke_perform_module=True)

        # Test without user_name and user_id
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'access_zone': "test-zone",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'password': '1234567',
                                   'home_directory': "test_user_1",
                                   'email': 'test_user_2@gamil.com',
                                   'shell': "/usr/local/bin/zsh",
                                   'primary_group': 'Isilon Users',
                                   'role_name': 'AuditAdmin',
                                   'state': 'present'})
        get_zones_summary_mock = MagicMock()
        get_zones_summary_mock.to_dict.return_value = MockUserApi.ZONE_SUMMARY
        powerscale_module_mock.zone_summary_api.get_zones_summary_zone.return_value = get_zones_summary_mock
        self.capture_fail_json_call(MockUserApi.get_error_responses(
            "param_error_user_id_and_name"), powerscale_module_mock, invoke_perform_module=True)

        # Test with wrong email
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'user_id': 7000,
                                   'access_zone': "test-zone",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'password': '1234567',
                                   'home_directory': "test_user_1",
                                   'email': 'fake_email',
                                   'shell': "/usr/local/bin/zsh",
                                   'primary_group': 'Isilon Users',
                                   'role_name': 'AuditAdmin',
                                   'state': 'present'})
        get_zones_summary_mock = MagicMock()
        get_zones_summary_mock.to_dict.return_value = MockUserApi.ZONE_SUMMARY
        powerscale_module_mock.zone_summary_api.get_zones_summary_zone.return_value = get_zones_summary_mock
        self.capture_fail_json_call(MockUserApi.get_error_responses(
            "param_error_email_format"), powerscale_module_mock, invoke_perform_module=True)

        # Test with role_name and role_state
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'user_id': 7000,
                                   'access_zone': "test-zone",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'password': '1234567',
                                   'home_directory': "test_user_1",
                                   'email': 'test_user_2@gamil.com',
                                   'shell': "/usr/local/bin/zsh",
                                   'primary_group': 'Isilon Users',
                                   'role_name': 'AuditAdmin',
                                   'state': 'present'})
        get_zones_summary_mock = MagicMock()
        get_zones_summary_mock.to_dict.return_value = MockUserApi.ZONE_SUMMARY
        powerscale_module_mock.zone_summary_api.get_zones_summary_zone.return_value = get_zones_summary_mock
        self.capture_fail_json_call(MockUserApi.get_error_responses(
            "param_error_role_name_and_state"), powerscale_module_mock, invoke_perform_module=True)

        # Test with role and non-default zone
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'user_id': 7000,
                                   'access_zone': "test-zone",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'password': '1234567',
                                   'home_directory': "test_user_1",
                                   'email': 'test_user_2@gamil.com',
                                   'shell': "/usr/local/bin/zsh",
                                   'primary_group': 'Isilon Users',
                                   'role_name': 'AuditAdmin',
                                   'role_state': 'present-for-user',
                                   'state': 'present'})
        get_zones_summary_mock = MagicMock()
        get_zones_summary_mock.to_dict.return_value = MockUserApi.ZONE_SUMMARY
        powerscale_module_mock.zone_summary_api.get_zones_summary_zone.return_value = get_zones_summary_mock
        self.capture_fail_json_call(MockUserApi.get_error_responses(
            "param_error_role_and_zone"), powerscale_module_mock, invoke_perform_module=True)

    def test_modify_user(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'user_id': 7000,
                                   'access_zone': "System",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'password': '1234567',
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
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'user_id': 7000,
                                   'access_zone': "System",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'password': '1234567',
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
                "update_user_error"), powerscale_module_mock, invoke_perform_module=True)

    def test_modify_user_without_changes(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'user_id': 7000,
                                   'access_zone': "System",
                                   'provider_type': "local",
                                   'password': '1234567',
                                   'email': 'test_user_2@gamil.com',
                                   'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[MockUserApi.GET_USER_DETAILS, MockUserApi.GET_USER_DETAILS])
        powerscale_module_mock.perform_module_operation()
        assert "7000" in powerscale_module_mock.module.exit_json.call_args[
            1]['user_details']['uid']['id']

    def test_modify_user_password(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'user_id': 7000,
                                   'access_zone': "System",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'update_password': 'always',
                                   'password': '1234567',
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
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'user_id': 7000,
                                   'access_zone': "System",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'update_password': 'always',
                                   'password': '1234567',
                                   'home_directory': "/home/test_user_1",
                                   'email': 'test_user_2@gamil.com',
                                   'shell': "/usr/local/bin/zsh",
                                   'primary_group': 'Isilon Users',
                                   'role_name': 'AuditAdmin',
                                   'role_state': 'present-for-user',
                                   'enabled': True,
                                   'state': 'present'})
        powerscale_module_mock.get_user_details = MagicMock(
            side_effect=[MockUserApi.GET_USER_DETAILS])
        with patch.object(powerscale_module_mock, "array_version", new="9.4.0"):
            with patch.object(powerscale_module_mock.role_api_instance,
                              'create_role_member',
                              side_effect=[MockApiException]):
                self.capture_fail_json_call(MockUserApi.get_error_responses(
                    "update_user_add_role_error"), powerscale_module_mock, invoke_perform_module=True)

    def test_modify_user_password_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'user_id': 7000,
                                   'access_zone': "System",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'update_password': 'always',
                                   'password': '1234567',
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
                    "update_password_error"), powerscale_module_mock, invoke_perform_module=True)

    def test_modify_user_remove_role(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'user_id': 7000,
                                   'access_zone': "System",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'update_password': 'always',
                                   'password': '1234567',
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
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'user_id': 7000,
                                   'access_zone': "System",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'update_password': 'always',
                                   'password': '1234567',
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
                    "update_user_remove_role_error"), powerscale_module_mock, invoke_perform_module=True)

    def test_delete_user(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'user_id': 7000,
                                   'access_zone': "System",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'password': '1234567',
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
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'user_id': 7000,
                                   'access_zone': "System",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'password': '1234567',
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
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'user_id': 7000,
                                   'access_zone': "non-System",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'password': '1234567',
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
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'user_id': 7000,
                                   'access_zone': "System",
                                   'provider_type': "local",
                                   'full_name': 'Test User',
                                   'password': '1234567',
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
                "delete_user_error"), powerscale_module_mock, invoke_perform_module=True)

        # delete from non local provider
        self.set_module_params(powerscale_module_mock,
                               self.user_args, {
                                   'user_name': "test_user_1",
                                   'user_id': 7000,
                                   'access_zone': "System",
                                   'provider_type': "fake-provider",
                                   'full_name': 'Test User',
                                   'password': '1234567',
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
            "delete_user_non_local_provider_error"), powerscale_module_mock, invoke_perform_module=True)
