# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Group module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library \
    import initial_mock
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.plugins.modules.group import Group
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_group_api \
    import MockGroupApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase


class TestGroup(PowerScaleUnitBase):
    group_args = MockGroupApi.GROUP_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return Group

    def mock_get_group_detail(self, powerscale_module_mock, call_exception, operation='create'):
        if operation == 'update':
            if not call_exception:
                powerscale_module_mock.api_instance.get_auth_group = \
                    MagicMock(side_effect=[MockGroupApi.get_group_detail(), MockGroupApi.get_group_detail()])
            else:
                powerscale_module_mock.api_instance.get_auth_group = \
                    MagicMock(return_value=MockGroupApi.get_group_detail(gid_name="invalid_test_group"))
        elif operation == 'delete':
            powerscale_module_mock.api_instance.get_auth_group = \
                MagicMock(side_effect=[MockGroupApi.get_group_detail(), MockApiException(404)])
        else:
            if not call_exception:
                powerscale_module_mock.api_instance.get_auth_group = \
                    MagicMock(side_effect=[MockApiException(404), MockGroupApi.get_group_detail()])
            elif call_exception == '500':
                powerscale_module_mock.api_instance.get_auth_group = MagicMock(side_effect=MockApiException(500))
            else:
                powerscale_module_mock.api_instance.get_auth_group = MagicMock(side_effect=Exception)

    def mock_get_group_list(self, powerscale_module_mock):
        powerscale_module_mock.api_instance.list_auth_groups = \
            MagicMock(side_effect=[MockApiException(404), MockGroupApi.get_group_detail(provider_type="nis")])

    def mock_get_group_members(self, powerscale_module_mock, call_exception):
        if not call_exception:
            powerscale_module_mock.group_api_instance.list_group_members = \
                MagicMock(return_value=MockGroupApi.get_group_members_list())
        else:
            powerscale_module_mock.group_api_instance.list_group_members = MagicMock(side_effect=Exception)

    def mock_create_group(self, powerscale_module_mock, call_exception):
        if not call_exception:
            powerscale_module_mock.api_instance.create_auth_group = MagicMock(return_value=1000)
        else:
            powerscale_module_mock.api_instance.create_auth_group = MagicMock(side_effect=Exception)

    def mock_delete_group(self, powerscale_module_mock, call_exception):
        if not call_exception:
            powerscale_module_mock.api_instance.delete_auth_group = MagicMock(return_value=None)
        else:
            powerscale_module_mock.api_instance.delete_auth_group = MagicMock(side_effect=Exception)

    def mock_get_mapping_identity(self, powerscale_module_mock, call_exception, user_name=None):
        if not call_exception:
            powerscale_module_mock.api_instance.get_mapping_identity = \
                MagicMock(return_value=MockGroupApi.get_user_mapping_identity())
        else:
            powerscale_module_mock.api_instance.get_mapping_identity = MagicMock(side_effect=Exception)

    def mock_create_group_member(self, powerscale_module_mock, call_exception):
        if not call_exception:
            powerscale_module_mock.group_api_instance.create_group_member = MagicMock(return_value=None)
        else:
            powerscale_module_mock.group_api_instance.create_group_member = MagicMock(side_effect=Exception)

    def mock_delete_group_member(self, powerscale_module_mock, call_exception):
        if not call_exception:
            powerscale_module_mock.group_api_instance.delete_group_member = MagicMock(return_value=None)
        else:
            powerscale_module_mock.group_api_instance.delete_group_member = MagicMock(side_effect=Exception)

    def create_group(self, powerscale_module_mock, run_operation=True,
                     call_get_exception=None, call_members_exception=False,
                     call_create_exception=False):
        self.mock_get_group_detail(powerscale_module_mock, call_get_exception)
        self.mock_get_group_list(powerscale_module_mock)
        self.mock_get_group_members(powerscale_module_mock, call_members_exception)
        self.mock_create_group(powerscale_module_mock, call_create_exception)
        if run_operation:
            powerscale_module_mock.perform_module_operation()

    def update_group(self, powerscale_module_mock, run_operation=True,
                     call_create_member_exception=False, call_delete_member_exception=False,
                     call_mapping_identity_exception=False, call_get_exception=False):
        self.mock_get_group_detail(powerscale_module_mock, operation='update', call_exception=call_get_exception)
        self.mock_get_group_members(powerscale_module_mock, call_exception=False)
        self.mock_get_mapping_identity(powerscale_module_mock, call_mapping_identity_exception)
        self.mock_create_group_member(powerscale_module_mock, call_create_member_exception)
        self.mock_delete_group_member(powerscale_module_mock, call_delete_member_exception)
        if run_operation:
            powerscale_module_mock.perform_module_operation()

    def delete_group(self, powerscale_module_mock, call_delete_exception=False):
        self.mock_get_group_detail(powerscale_module_mock, operation='delete', call_exception=False)
        self.mock_delete_group(powerscale_module_mock, call_delete_exception)
        if not call_delete_exception:
            powerscale_module_mock.perform_module_operation()

    def test_create_group(self, powerscale_module_mock):
        self.set_module_params(self.group_args,
                               MockGroupApi.get_create_group_payload(
                                   name="test_group",
                                   id=1000,
                                   users=[{"user_name": "test_user"}, {"user_id": "1000"}],
                                   user_state="present-in-group"))
        self.create_group(powerscale_module_mock)
        assert "1000" in powerscale_module_mock.module.exit_json.call_args[1]['group_details']['gid']['id']

    def test_create_group_with_nis_provider_exception(self, powerscale_module_mock):
        self.set_module_params(self.group_args,
                               MockGroupApi.get_create_group_payload(name="test_group", provider_type="nis"))
        self.create_group(powerscale_module_mock, run_operation=False)
        self.capture_fail_json_method(
            "Create group is allowed only if provider_type is local, got 'nis' provider",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_create_group_with_name(self, powerscale_module_mock):
        self.set_module_params(self.group_args,
                               MockGroupApi.get_create_group_payload(name="test_group"))
        self.create_group(powerscale_module_mock)
        assert "test_group" in powerscale_module_mock.module.exit_json.call_args[1]['group_details']['gid']['name']

    def test_create_group_without_name_exception(self, powerscale_module_mock):
        self.set_module_params(self.group_args, MockGroupApi.get_create_group_payload(id=1000))
        self.create_group(powerscale_module_mock, run_operation=False)
        self.capture_fail_json_method(
            "Unable to create a group, 'group_name' is missing",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_create_group_without_name_id_exception(self, powerscale_module_mock):
        self.set_module_params(self.group_args, MockGroupApi.get_create_group_payload())
        self.create_group(powerscale_module_mock, run_operation=False)
        self.capture_fail_json_method(
            "Invalid group_name or group_id provided.",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_create_group_with_invalid_users_type_exception(self, powerscale_module_mock):
        self.set_module_params(self.group_args,
                               MockGroupApi.get_create_group_payload(
                                   name="test_group",
                                   users=["user1", "user2"],
                                   user_state="present-in-group"))
        self.create_group(powerscale_module_mock, run_operation=False)
        self.capture_fail_json_method(
            "Key Value pair is allowed, Provided user1.",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_create_group_with_invalid_users_value_exception(self, powerscale_module_mock):
        self.set_module_params(self.group_args,
                               MockGroupApi.get_create_group_payload(
                                   name="test_group",
                                   users=[{"invalid_key": "test_user"}],
                                   user_state="present-in-group"))
        self.create_group(powerscale_module_mock, run_operation=False)
        self.capture_fail_json_method(
            "user_id or user_name  is expected, \"invalid_key\" given.",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_create_group_with_users_exception(self, powerscale_module_mock):
        self.set_module_params(self.group_args,
                               MockGroupApi.get_create_group_payload(name="test_group", users=["user1", "user2"]))
        self.create_group(powerscale_module_mock, run_operation=False)
        self.capture_fail_json_method(
            "'user_state' is not specified, 'users' are given",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_create_group_with_user_state_exception(self, powerscale_module_mock):
        self.set_module_params(self.group_args,
                               MockGroupApi.get_create_group_payload(name="test_group", user_state="present-in-group"))
        self.create_group(powerscale_module_mock, run_operation=False)
        self.capture_fail_json_method(
            "'user_state' is given, 'users' are not specified",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_create_group_with_name_id_exception(self, powerscale_module_mock):
        self.set_module_params(self.group_args, MockGroupApi.CREATE_GROUP_PAYLOAD)
        self.create_group(powerscale_module_mock, call_create_exception=True, run_operation=False)
        self.capture_fail_json_method(
            "Create Group test_group failed with ",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_create_group_with_get_exception(self, powerscale_module_mock):
        self.set_module_params(self.group_args, MockGroupApi.get_create_group_payload(id=1000))
        self.create_group(powerscale_module_mock, call_get_exception=True, run_operation=False)
        self.capture_fail_json_method(
            "Get Group Details GID:1000 failed with ",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_create_group_with_get_api_exception(self, powerscale_module_mock):
        self.set_module_params(self.group_args, MockGroupApi.get_create_group_payload(id=1000))
        self.create_group(powerscale_module_mock, call_get_exception='500', run_operation=False)
        self.capture_fail_json_method(
            "Get Group Details GID:1000 failed with SDK Error message",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_create_group_with_members_exception(self, powerscale_module_mock):
        self.set_module_params(self.group_args,
                               MockGroupApi.get_create_group_payload(name="test_group"))
        self.create_group(powerscale_module_mock, call_members_exception=True, run_operation=False)
        self.capture_fail_json_method(
            "Get Users for group GROUP:test_group failed with ",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_update_group_with_add_user(self, powerscale_module_mock):
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.update_group(powerscale_module_mock)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']

    def test_update_group_with_add_user_exception(self, powerscale_module_mock):
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.update_group(powerscale_module_mock, call_create_member_exception=True, run_operation=False)
        self.capture_fail_json_method(
            "Add user UID:1000 to group failed with  ",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_update_group_with_delete_user(self, powerscale_module_mock):
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(user_state="absent-in-group"))
        self.update_group(powerscale_module_mock)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']

    def test_update_group_with_delete_user_exception(self, powerscale_module_mock):
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(user_state="absent-in-group"))
        self.update_group(powerscale_module_mock, call_delete_member_exception=True, run_operation=False)
        self.capture_fail_json_method(
            "Remove user GID:1000 from group failed with ",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_update_group_with_user_mapping_exception(self, powerscale_module_mock):
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.update_group(powerscale_module_mock, call_mapping_identity_exception=True, run_operation=False)
        self.capture_fail_json_method(
            "Get user_name for 1000 failed with  ",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_update_group_with_invalid_users_type_exception(self, powerscale_module_mock):
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(users=["user1", "user2"]))
        self.update_group(powerscale_module_mock, run_operation=False)
        self.capture_fail_json_method(
            "Key Value pair is allowed, Provided user1.",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_update_group_with_invalid_users_key_exception(self, powerscale_module_mock):
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(
                                   users=[{"user_name": "test_user", "user_id": "1000"}]))
        self.update_group(powerscale_module_mock, run_operation=False)
        self.capture_fail_json_method(
            "One Key per dictionary is allowed, ['user_name', 'user_id'] given",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_update_group_with_invalid_users_value_exception(self, powerscale_module_mock):
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(users=[{"invalid_key": "test_user"}]))
        self.update_group(powerscale_module_mock, run_operation=False)
        self.capture_fail_json_method(
            "user_id or user_name  is expected, \"invalid_key\" given.",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_update_group_with_id_exists_exception(self, powerscale_module_mock):
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.update_group(powerscale_module_mock, run_operation=False, call_get_exception=True)
        self.capture_fail_json_method(
            "Group already exists with GID 1000",
            powerscale_module_mock,
            "perform_module_operation",
        )

    # ------------------------------------------------------------------
    # FR-7: provider existence validation (Story-29823)
    # ------------------------------------------------------------------

    def mock_providers_summary(self, powerscale_module_mock, provider_types=None,
                               zone="System", call_exception=False):
        if call_exception:
            powerscale_module_mock.api_instance.get_providers_summary = \
                MagicMock(side_effect=Exception)
        else:
            powerscale_module_mock.api_instance.get_providers_summary = \
                MagicMock(return_value=MockGroupApi.get_providers_summary(
                    provider_types=provider_types, zone=zone))

    def test_validate_provider_exists_unconfigured_provider_exception(self, powerscale_module_mock):
        """FR-7/AC-007: a provider absent from the zone fails with the exact message."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_providers_summary(powerscale_module_mock, provider_types=["local", "file", "ldap"])
        self.capture_fail_json_method(
            "Provider 'nis' is not configured in access zone 'System'",
            powerscale_module_mock,
            "_validate_provider_exists",
            "nis", "System",
        )

    def test_validate_provider_exists_makes_no_member_api_calls_on_failure(self, powerscale_module_mock):
        """FR-7/AC-007: validation fails before any membership API call is issued."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_providers_summary(powerscale_module_mock, provider_types=["local"])
        powerscale_module_mock.group_api_instance.list_group_members = MagicMock()
        powerscale_module_mock.group_api_instance.create_group_member = MagicMock()
        powerscale_module_mock.group_api_instance.delete_group_member = MagicMock()
        with pytest.raises(SystemExit):
            powerscale_module_mock._validate_provider_exists("ldap", "System")
        powerscale_module_mock.group_api_instance.list_group_members.assert_not_called()
        powerscale_module_mock.group_api_instance.create_group_member.assert_not_called()
        powerscale_module_mock.group_api_instance.delete_group_member.assert_not_called()

    def test_validate_provider_exists_configured_provider_accepted(self, powerscale_module_mock):
        """FR-7: a configured provider passes validation without failing."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_providers_summary(powerscale_module_mock, provider_types=["local", "ldap"])
        powerscale_module_mock._validate_provider_exists("ldap", "System")
        powerscale_module_mock.module.fail_json.assert_not_called()

    def test_validate_provider_exists_is_cached_across_calls(self, powerscale_module_mock):
        """NFR-1: the per-zone summary is fetched once, not once per member."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_providers_summary(powerscale_module_mock, provider_types=["local", "ldap"])
        powerscale_module_mock._validate_provider_exists("ldap", "System")
        powerscale_module_mock._validate_provider_exists("local", "System")
        powerscale_module_mock._validate_provider_exists("ldap", "System")
        assert powerscale_module_mock.api_instance.get_providers_summary.call_count == 1

    def test_validate_provider_exists_respects_access_zone(self, powerscale_module_mock):
        """FR-7: a provider configured in another zone is not accepted for this zone."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_providers_summary(powerscale_module_mock,
                                    provider_types=["local", "ldap"], zone="sampleZone")
        self.capture_fail_json_method(
            "Provider 'ldap' is not configured in access zone 'System'",
            powerscale_module_mock,
            "_validate_provider_exists",
            "ldap", "System",
        )

    def test_validate_provider_exists_api_exception(self, powerscale_module_mock):
        """NFR-4: SDK failures surface a sanitised message, not a stack trace."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_providers_summary(powerscale_module_mock, call_exception=True)
        self.capture_fail_json_method(
            "Failed to fetch authentication providers for access zone 'System'",
            powerscale_module_mock,
            "_validate_provider_exists",
            "ldap", "System",
        )

    # ------------------------------------------------------------------
    # FR-8: OneFS version validation (Story-29823)
    # ------------------------------------------------------------------

    def mock_cluster_config(self, powerscale_module_mock, release="9.13.0.0",
                            call_exception=False):
        if call_exception:
            powerscale_module_mock.cluster_api_instance.get_cluster_config = \
                MagicMock(side_effect=Exception)
        else:
            powerscale_module_mock.cluster_api_instance.get_cluster_config = \
                MagicMock(return_value=MockGroupApi.get_cluster_config(release=release))

    @pytest.mark.parametrize("release", ["9.5.0.0", "9.10.9.0", "9.10.0.0", "8.2.2.0"])
    def test_validate_onefs_version_below_minimum_exception(self, powerscale_module_mock, release):
        """FR-8/AC-008: a cluster below 9.11.0 fails with the exact message."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_cluster_config(powerscale_module_mock, release=release)
        self.capture_fail_json_method(
            "OneFS version %s is below the required minimum 9.11.0"
            " for cross-provider group membership" % release,
            powerscale_module_mock,
            "_validate_onefs_version",
        )

    @pytest.mark.parametrize("release", ["9.11.0.0", "9.11.0", "9.12.0.0", "9.13.0.0", "10.0.0.0"])
    def test_validate_onefs_version_at_or_above_minimum_accepted(self, powerscale_module_mock, release):
        """FR-8: 9.11.0 is inclusive; anything above it passes."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_cluster_config(powerscale_module_mock, release=release)
        powerscale_module_mock._validate_onefs_version()
        powerscale_module_mock.module.fail_json.assert_not_called()

    def test_validate_onefs_version_makes_no_member_api_calls_on_failure(self, powerscale_module_mock):
        """FR-8/AC-008: validation fails before any membership API call is issued."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_cluster_config(powerscale_module_mock, release="9.5.0.0")
        powerscale_module_mock.group_api_instance.list_group_members = MagicMock()
        powerscale_module_mock.group_api_instance.create_group_member = MagicMock()
        powerscale_module_mock.group_api_instance.delete_group_member = MagicMock()
        with pytest.raises(SystemExit):
            powerscale_module_mock._validate_onefs_version()
        powerscale_module_mock.group_api_instance.list_group_members.assert_not_called()
        powerscale_module_mock.group_api_instance.create_group_member.assert_not_called()
        powerscale_module_mock.group_api_instance.delete_group_member.assert_not_called()

    def test_validate_onefs_version_is_cached_across_calls(self, powerscale_module_mock):
        """NFR-1: the cluster version is fetched once per module invocation."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_cluster_config(powerscale_module_mock, release="9.13.0.0")
        powerscale_module_mock._validate_onefs_version()
        powerscale_module_mock._validate_onefs_version()
        powerscale_module_mock._validate_onefs_version()
        assert powerscale_module_mock.cluster_api_instance.get_cluster_config.call_count == 1

    def test_validate_onefs_version_tolerates_v_prefix(self, powerscale_module_mock):
        """FR-8: a 'v'-prefixed release string is parsed, not rejected outright."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_cluster_config(powerscale_module_mock, release="v9.13.0.0")
        powerscale_module_mock._validate_onefs_version()
        powerscale_module_mock.module.fail_json.assert_not_called()

    def test_validate_onefs_version_api_exception(self, powerscale_module_mock):
        """NFR-4: SDK failures surface a sanitised message, not a stack trace."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_cluster_config(powerscale_module_mock, call_exception=True)
        self.capture_fail_json_method(
            "Failed to determine the OneFS version of the cluster",
            powerscale_module_mock,
            "_validate_onefs_version",
        )

    def test_validate_onefs_version_unparseable_release(self, powerscale_module_mock):
        """FR-8: an unusable release string fails clearly rather than crashing."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_cluster_config(powerscale_module_mock, release="not-a-version")
        self.capture_fail_json_method(
            "Failed to determine the OneFS version of the cluster",
            powerscale_module_mock,
            "_validate_onefs_version",
        )

    def test_delete_group(self, powerscale_module_mock):
        self.set_module_params(self.group_args, MockGroupApi.get_delete_group_payload())
        self.delete_group(powerscale_module_mock)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']

    def test_delete_group_with_delete_exception(self, powerscale_module_mock):
        self.set_module_params(self.group_args, MockGroupApi.get_delete_group_payload())
        self.delete_group(powerscale_module_mock, call_delete_exception=True)
        self.capture_fail_json_method(
            "Delete GID:1000  failed with ",
            powerscale_module_mock,
            "perform_module_operation",
        )
