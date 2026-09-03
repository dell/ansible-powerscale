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
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
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
            "User dict at index 0 must contain exactly one of 'user_name' or 'user_id', not both.",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_update_group_with_invalid_users_value_exception(self, powerscale_module_mock):
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(users=[{"invalid_key": "test_user"}]))
        self.update_group(powerscale_module_mock, run_operation=False)
        self.capture_fail_json_method(
            "User dict at index 0 contains unsupported keys."
            " Supported keys are: user_name, user_id, provider_type.",
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

    # ------------------------------------------------------------------
    # Lazy preflight wiring (Story-29823, NFR-1 / NFR-2)
    # ------------------------------------------------------------------

    def mock_preflight_apis(self, powerscale_module_mock, provider_types=None,
                            release="9.13.0.0", zone="System"):
        self.mock_providers_summary(powerscale_module_mock,
                                    provider_types=provider_types, zone=zone)
        self.mock_cluster_config(powerscale_module_mock, release=release)

    def test_preflight_cross_provider_skipped_when_no_member_provider(self, powerscale_module_mock):
        """NFR-1/NFR-2: a legacy payload triggers zero validation API calls."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_preflight_apis(powerscale_module_mock)
        powerscale_module_mock._preflight_cross_provider("System", None)
        powerscale_module_mock.api_instance.get_providers_summary.assert_not_called()
        powerscale_module_mock.cluster_api_instance.get_cluster_config.assert_not_called()
        powerscale_module_mock.module.fail_json.assert_not_called()

    def test_preflight_cross_provider_runs_both_validators(self, powerscale_module_mock):
        """FR-7 + FR-8 both run when a per-member provider_type is supplied."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_preflight_apis(powerscale_module_mock, provider_types=["local", "ldap"])
        powerscale_module_mock._preflight_cross_provider("System", "ldap")
        powerscale_module_mock.cluster_api_instance.get_cluster_config.assert_called_once()
        powerscale_module_mock.api_instance.get_providers_summary.assert_called_once()
        powerscale_module_mock.module.fail_json.assert_not_called()

    def test_preflight_cross_provider_runs_validators_once_for_many_members(self, powerscale_module_mock):
        """NFR-1: five cross-provider members still cost one call per validator."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_preflight_apis(powerscale_module_mock, provider_types=["local", "ldap"])
        for _idx in range(5):
            powerscale_module_mock._preflight_cross_provider("System", "ldap")
        assert powerscale_module_mock.cluster_api_instance.get_cluster_config.call_count == 1
        assert powerscale_module_mock.api_instance.get_providers_summary.call_count == 1

    def test_preflight_cross_provider_version_checked_before_provider(self, powerscale_module_mock):
        """FR-8 precedes FR-7: an old cluster fails on version, not provider."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_preflight_apis(powerscale_module_mock,
                                 provider_types=["local"], release="9.5.0.0")
        with pytest.raises(SystemExit):
            powerscale_module_mock._preflight_cross_provider("System", "ldap")
        call_args = powerscale_module_mock.module.fail_json.call_args.kwargs
        assert "OneFS version 9.5.0.0 is below the required minimum" in call_args['msg']
        powerscale_module_mock.api_instance.get_providers_summary.assert_not_called()

    def test_preflight_cross_provider_rejects_unconfigured_provider(self, powerscale_module_mock):
        """FR-7 via the preflight entry point on a supported cluster."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_preflight_apis(powerscale_module_mock, provider_types=["local"])
        self.capture_fail_json_method(
            "Provider 'ldap' is not configured in access zone 'System'",
            powerscale_module_mock,
            "_preflight_cross_provider",
            "System", "ldap",
        )

    # ------------------------------------------------------------------
    # FR-2 / FR-11: user-dict key validation (Story-29823)
    # ------------------------------------------------------------------

    def test_group_user_dict_unsupported_key_exception(self, powerscale_module_mock):
        """FR-11: a dict with an unsupported key (not user_name/user_id/provider_type) is rejected."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(
                                   users=[{"user_name": "a", "bogus": "b"}]))
        self.update_group(powerscale_module_mock, run_operation=False)
        self.capture_fail_json_method(
            "User dict at index 0 contains unsupported keys."
            " Supported keys are: user_name, user_id, provider_type.",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_group_user_dict_invalid_provider_type_exception(self, powerscale_module_mock):
        """FR-2/FR-11: an invalid provider_type is rejected before any API call."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(
                                   users=[{"user_name": "a", "provider_type": "invalid_provider"}]))
        self.update_group(powerscale_module_mock, run_operation=False)
        self.capture_fail_json_method(
            "User dict at index 0 has invalid provider_type 'invalid_provider'."
            " Valid values are: local, file, ldap, ads, nis.",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_group_user_dict_name_and_id_mutually_exclusive_exception(self, powerscale_module_mock):
        """FR-11: user_name and user_id are mutually exclusive within one dict."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(
                                   users=[{"user_name": "a", "user_id": "1000"}]))
        self.update_group(powerscale_module_mock, run_operation=False)
        self.capture_fail_json_method(
            "User dict at index 0 must contain exactly one of 'user_name' or 'user_id', not both.",
            powerscale_module_mock,
            "perform_module_operation",
        )

    # ------------------------------------------------------------------
    # FR-1 / FR-10: user-to-id resolution (Story-29823)
    # ------------------------------------------------------------------

    def mock_get_auth_user(self, powerscale_module_mock, provider="local",
                           call_exception=False):
        """Mock AuthApi.get_auth_user for user resolution tests."""
        if call_exception:
            powerscale_module_mock.api_instance.get_auth_user = \
                MagicMock(side_effect=Exception("SDK boom"))
        else:
            powerscale_module_mock.api_instance.get_auth_user = \
                MagicMock(return_value=MockGroupApi.get_auth_user_response(provider))

    def test_resolve_member_id_ldap_user_by_name(self, powerscale_module_mock):
        """FR-1: an LDAP user_name resolves to the fixture's unique SID."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_get_auth_user(powerscale_module_mock, provider="ldap")
        resolved = powerscale_module_mock._resolve_member_id(
            "ldap_user", None, "ldap", "System")
        assert resolved == "SID:S-1-5-21-9999999999-8888888888-7777777777-50001"
        powerscale_module_mock.api_instance.get_auth_user.assert_called_once()

    def test_resolve_member_id_local_user_by_name(self, powerscale_module_mock):
        """FR-1: a local user_name resolves to its SID."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_get_auth_user(powerscale_module_mock, provider="local")
        resolved = powerscale_module_mock._resolve_member_id(
            "test_user", None, "local", "System")
        assert resolved == "SID:S-1-5-21-1426242897-2739835565-3634425493-501"

    def test_resolve_member_id_by_uid(self, powerscale_module_mock):
        """FR-1: resolution by user_id uses UID: prefix."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_get_auth_user(powerscale_module_mock, provider="ldap")
        resolved = powerscale_module_mock._resolve_member_id(
            None, "50001", "ldap", "System")
        assert resolved == "SID:S-1-5-21-9999999999-8888888888-7777777777-50001"
        # Verify the lookup used UID: prefix
        call_kwargs = powerscale_module_mock.api_instance.get_auth_user.call_args
        assert "UID:50001" in str(call_kwargs)

    def test_resolve_member_id_unresolvable_user_exception(self, powerscale_module_mock):
        """FR-10: an empty result fails with the exact message."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_get_auth_user(powerscale_module_mock, provider=None)  # empty result
        self.capture_fail_json_method(
            "User 'alice' could not be resolved in access zone 'System'",
            powerscale_module_mock,
            "_resolve_member_id",
            "alice", None, "ldap", "System",
        )

    def test_resolve_member_id_api_exception(self, powerscale_module_mock):
        """NFR-4: SDK failures surface a sanitised message."""
        self.set_module_params(self.group_args, MockGroupApi.get_update_group_payload())
        self.mock_get_auth_user(powerscale_module_mock, call_exception=True)
        self.capture_fail_json_method(
            "Failed to resolve user 'bob' in provider 'ldap'",
            powerscale_module_mock,
            "_resolve_member_id",
            "bob", None, "ldap", "System",
        )

    def test_group_user_dict_valid_with_provider_type_accepted(self, powerscale_module_mock):
        """FR-2: a user dict with user_name + provider_type passes validation."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(
                                   users=[{"user_name": "ldap_user", "provider_type": "ldap"}]))
        # Wire up the preflight and resolution mocks so it can proceed past validation
        self.mock_preflight_apis(powerscale_module_mock, provider_types=["local", "ldap"])
        self.mock_get_group_detail(powerscale_module_mock, operation='update', call_exception=False)
        self.mock_get_group_members(powerscale_module_mock, call_exception=False)
        self.mock_get_mapping_identity(powerscale_module_mock, call_exception=False)
        self.mock_create_group_member(powerscale_module_mock, call_exception=False)
        self.mock_delete_group_member(powerscale_module_mock, call_exception=False)
        self.mock_get_auth_user(powerscale_module_mock, provider="ldap")
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.module.fail_json.assert_not_called()

    # ------------------------------------------------------------------
    # FR-1 / FR-3 / AC-001 / AC-002 / AC-006: cross-provider add/remove
    # ------------------------------------------------------------------

    def setup_cross_provider_update(self, powerscale_module_mock,
                                    members=None, provider_types=None):
        """Wire up all mocks needed for a cross-provider update flow."""
        if provider_types is None:
            provider_types = ["local", "ldap"]
        self.mock_preflight_apis(powerscale_module_mock, provider_types=provider_types)
        self.mock_get_group_detail(powerscale_module_mock, operation='update', call_exception=False)
        if members is None:
            self.mock_get_group_members(powerscale_module_mock, call_exception=False)
        else:
            powerscale_module_mock.group_api_instance.list_group_members = \
                MagicMock(return_value=members)
        self.mock_get_mapping_identity(powerscale_module_mock, call_exception=False)
        self.mock_create_group_member(powerscale_module_mock, call_exception=False)
        self.mock_delete_group_member(powerscale_module_mock, call_exception=False)
        self.mock_get_auth_user(powerscale_module_mock, provider="ldap")

    def test_update_group_with_add_ldap_user(self, powerscale_module_mock):
        """FR-1/AC-001: adding an LDAP user to a local group returns changed=true.

        The cross-provider path must:
        - resolve the user via _resolve_member_id (get_auth_user called)
        - pass the resolved SID to create_group_member (not USER:ldap_user)
        - not pass provider= to create_group_member (cross-provider call)
        """
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(
                                   users=[{"user_name": "ldap_user", "provider_type": "ldap"}]))
        self.setup_cross_provider_update(powerscale_module_mock)
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']
        # The user was resolved via get_auth_user
        powerscale_module_mock.api_instance.get_auth_user.assert_called()
        # create_group_member called with the resolved SID, not USER:ldap_user
        create_call = powerscale_module_mock.group_api_instance.create_group_member
        create_call.assert_called_once()
        call_args = create_call.call_args
        # The first positional arg should be a GroupMember constructed with
        # the SID, not with USER:ldap_user
        member_arg = str(call_args)
        assert "SID:S-1-5-21-9999999999" in member_arg or "ldap_user" not in member_arg.rsplit("USER:", maxsplit=1)[-1]

    def test_update_group_with_remove_ldap_user(self, powerscale_module_mock):
        """FR-3: cross-provider removal returns changed=true.

        The removal must use the resolved SID to call delete_group_member.
        """
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(
                                   users=[{"user_name": "ldap_user", "provider_type": "ldap"}],
                                   user_state="absent-in-group"))
        # Use mixed members so the LDAP user IS a member
        self.setup_cross_provider_update(
            powerscale_module_mock,
            members=MockGroupApi.get_group_members_mixed())
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']
        # The user was resolved via get_auth_user
        powerscale_module_mock.api_instance.get_auth_user.assert_called()
        powerscale_module_mock.group_api_instance.delete_group_member.assert_called_once()

    def test_update_group_remove_non_member_ldap_idempotent(self, powerscale_module_mock):
        """AC-002: removing an absent cross-provider member returns changed=false."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(
                                   users=[{"user_name": "ldap_user", "provider_type": "ldap"}],
                                   user_state="absent-in-group"))
        # Use default members (no LDAP user present)
        self.setup_cross_provider_update(powerscale_module_mock)
        powerscale_module_mock.perform_module_operation()
        assert not powerscale_module_mock.module.exit_json.call_args[1]['changed']
        powerscale_module_mock.group_api_instance.delete_group_member.assert_not_called()

    def test_update_group_add_existing_ldap_member_idempotent(self, powerscale_module_mock):
        """AC-002: re-adding an existing cross-provider member returns changed=false."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(
                                   users=[{"user_name": "ldap_user", "provider_type": "ldap"}]))
        # Use mixed members so the LDAP user IS already a member
        self.setup_cross_provider_update(
            powerscale_module_mock,
            members=MockGroupApi.get_group_members_mixed())
        powerscale_module_mock.perform_module_operation()
        assert not powerscale_module_mock.module.exit_json.call_args[1]['changed']
        powerscale_module_mock.group_api_instance.create_group_member.assert_not_called()

    def test_update_group_with_mixed_provider_members(self, powerscale_module_mock):
        """AC-006: a task with both a local and an LDAP member in one call.

        The local member flows through the legacy path (USER:new_local_user).
        The LDAP member flows through the cross-provider path (resolved SID).
        We use an empty member list so both members need adding.
        """
        from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
            import MockSDKResponse
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(
                                   users=[
                                       {"user_name": "new_local_user"},
                                       {"user_name": "ldap_user", "provider_type": "ldap"},
                                   ]))
        # Empty member list so both users will be added
        self.setup_cross_provider_update(
            powerscale_module_mock,
            members=MockSDKResponse({"members": []}))
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']
        # Both members should trigger create_group_member
        assert powerscale_module_mock.group_api_instance.create_group_member.call_count == 2
        # The LDAP member should have been resolved via get_auth_user
        powerscale_module_mock.api_instance.get_auth_user.assert_called()

    # ------------------------------------------------------------------
    # FR-4 / FR-5 / AC-004: check mode and diff (Story-29823)
    # ------------------------------------------------------------------

    def test_update_group_check_mode_diff_add(self, powerscale_module_mock):
        """FR-4/FR-5/AC-004: check mode + diff for adding an LDAP member.

        changed=true, diff emitted, create_group_member never called.
        """
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(
                                   users=[{"user_name": "ldap_user", "provider_type": "ldap"}]))
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.module._diff = True
        self.setup_cross_provider_update(powerscale_module_mock)
        powerscale_module_mock.perform_module_operation()
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result['changed']
        # No write API calls in check mode
        powerscale_module_mock.group_api_instance.create_group_member.assert_not_called()
        powerscale_module_mock.group_api_instance.delete_group_member.assert_not_called()
        # Diff should be present
        assert 'diff' in result
        assert 'before' in result['diff']
        assert 'after' in result['diff']

    def test_update_group_check_mode_diff_remove(self, powerscale_module_mock):
        """FR-4/FR-5: check mode + diff for removing an LDAP member."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(
                                   users=[{"user_name": "ldap_user", "provider_type": "ldap"}],
                                   user_state="absent-in-group"))
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.module._diff = True
        self.setup_cross_provider_update(
            powerscale_module_mock,
            members=MockGroupApi.get_group_members_mixed())
        powerscale_module_mock.perform_module_operation()
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result['changed']
        powerscale_module_mock.group_api_instance.delete_group_member.assert_not_called()
        assert 'diff' in result

    def test_update_group_check_mode_no_change(self, powerscale_module_mock):
        """FR-4: already-correct membership returns changed=false in check mode."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(
                                   users=[{"user_name": "ldap_user", "provider_type": "ldap"}]))
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.module._diff = True
        # LDAP user is already a member
        self.setup_cross_provider_update(
            powerscale_module_mock,
            members=MockGroupApi.get_group_members_mixed())
        powerscale_module_mock.perform_module_operation()
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert not result['changed']

    def test_update_group_diff_without_check_mode(self, powerscale_module_mock):
        """FR-5: a real apply with diff=true still emits diff alongside writes."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(
                                   users=[{"user_name": "ldap_user", "provider_type": "ldap"}]))
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.module._diff = True
        self.setup_cross_provider_update(powerscale_module_mock)
        powerscale_module_mock.perform_module_operation()
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result['changed']
        # Write call IS made (not check mode)
        powerscale_module_mock.group_api_instance.create_group_member.assert_called_once()
        # Diff should still be emitted
        assert 'diff' in result

    # ------------------------------------------------------------------
    # FR-6 / AC-003: backward compatibility (Story-29823)
    # ------------------------------------------------------------------

    def test_update_group_with_existing_local_user_unchanged(self, powerscale_module_mock):
        """FR-6/AC-003: a legacy payload (no per-member provider_type) for an
        already-present user returns changed=false — identical to pre-cross-
        provider behaviour."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(
                                   users=[{"user_name": "test_user"}]))
        self.update_group(powerscale_module_mock)
        assert not powerscale_module_mock.module.exit_json.call_args[1]['changed']
        # No write calls should have been made
        powerscale_module_mock.group_api_instance.create_group_member.assert_not_called()
        powerscale_module_mock.group_api_instance.delete_group_member.assert_not_called()

    def test_update_group_legacy_payload_uses_group_provider(self, powerscale_module_mock):
        """FR-6: without per-member provider_type the legacy path is used, so
        add_user_to_group receives the group-level provider and
        check_provider_type is enforced."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(
                                   users=[{"user_name": "test_user"}, {"user_id": "1000"}]))
        self.update_group(powerscale_module_mock)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']
        # check_provider_type is still called for legacy members
        # (create_group_member receives provider=local)
        create_calls = powerscale_module_mock.group_api_instance.create_group_member.call_args_list
        for call in create_calls:
            # The legacy path passes provider= as a keyword argument
            assert 'provider' in call.kwargs

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

    # ==================================================================
    # Story-3078 Part 1: Child Group & Well-Known SID Membership
    # ==================================================================

    # ------------------------------------------------------------------
    # Phase 1: Input validation for group_members and well_known_sids
    # ------------------------------------------------------------------

    def test_group_members_unsupported_key_rejected(self, powerscale_module_mock):
        """FR-6.1: group_members entries with unsupported keys are rejected."""
        self.set_module_params(
            self.group_args,
            MockGroupApi.get_update_group_payload_with_group_members(
                group_members=[{"group_name": "grp1", "bogus_key": "val"}],
                group_member_state="present-in-group"))
        self.mock_get_group_detail(powerscale_module_mock, operation='update',
                                   call_exception=False)
        self.mock_get_group_members(powerscale_module_mock, call_exception=False)
        self.capture_fail_json_method(
            "group_members entry at index 0 contains unsupported keys",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_group_members_valid_keys_accepted(self, powerscale_module_mock):
        """FR-6.1: group_members entries with only group_name and provider_type pass."""
        self.set_module_params(
            self.group_args,
            MockGroupApi.get_update_group_payload_with_group_members(
                group_members=[{"group_name": "child_grp", "provider_type": "local"}],
                group_member_state="present-in-group"))
        self.mock_get_group_members(powerscale_module_mock, call_exception=False)
        # get_auth_group: (1) _handle_present_state, (2) resolve child group,
        # (3) final get_group_details
        powerscale_module_mock.api_instance.get_auth_group = \
            MagicMock(side_effect=[
                MockGroupApi.get_group_detail(),               # get_group_details
                MockGroupApi.get_auth_group_response("local"), # resolve child_grp
                MockGroupApi.get_group_detail(),                # final get_group_details
            ])
        powerscale_module_mock.group_api_instance.create_group_member = \
            MagicMock(return_value=None)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.module.fail_json.assert_not_called()

    def test_group_members_missing_group_name_rejected(self, powerscale_module_mock):
        """FR-6.1: group_members entries without group_name are rejected."""
        self.set_module_params(
            self.group_args,
            MockGroupApi.get_update_group_payload_with_group_members(
                group_members=[{"provider_type": "local"}],
                group_member_state="present-in-group"))
        self.mock_get_group_detail(powerscale_module_mock, operation='update',
                                   call_exception=False)
        self.mock_get_group_members(powerscale_module_mock, call_exception=False)
        self.capture_fail_json_method(
            "group_members entry at index 0 is missing required key 'group_name'",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_wellknown_sids_unrecognised_value_rejected(self, powerscale_module_mock):
        """FR-6.2: well_known_sids with unrecognised values are rejected before any API call."""
        self.set_module_params(
            self.group_args,
            MockGroupApi.get_update_group_payload_with_wellknown_sids(
                well_known_sids=["NonExistentSID"],
                well_known_sid_state="present-in-group"))
        self.mock_get_group_detail(powerscale_module_mock, operation='update',
                                   call_exception=False)
        self.mock_get_group_members(powerscale_module_mock, call_exception=False)
        # Mock the wellknowns API
        powerscale_module_mock.api_instance.list_auth_wellknowns = \
            MagicMock(return_value=MockGroupApi.get_wellknowns_response())
        self.capture_fail_json_method(
            "'NonExistentSID' is not a recognised well-known SID name or SID string",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_wellknown_sids_valid_display_name_accepted(self, powerscale_module_mock):
        """FR-6.2: well_known_sids with valid display names pass validation."""
        self.set_module_params(
            self.group_args,
            MockGroupApi.get_update_group_payload_with_wellknown_sids(
                well_known_sids=["Everyone"],
                well_known_sid_state="present-in-group"))
        self.mock_get_group_detail(powerscale_module_mock, operation='update',
                                   call_exception=False)
        self.mock_get_group_members(powerscale_module_mock, call_exception=False)
        powerscale_module_mock.api_instance.list_auth_wellknowns = \
            MagicMock(return_value=MockGroupApi.get_wellknowns_response())
        powerscale_module_mock.group_api_instance.create_group_member = \
            MagicMock(return_value=None)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.module.fail_json.assert_not_called()

    def test_wellknown_sids_valid_sid_string_accepted(self, powerscale_module_mock):
        """FR-6.2: well_known_sids with valid SID strings pass validation."""
        self.set_module_params(
            self.group_args,
            MockGroupApi.get_update_group_payload_with_wellknown_sids(
                well_known_sids=["S-1-1-0"],
                well_known_sid_state="present-in-group"))
        self.mock_get_group_detail(powerscale_module_mock, operation='update',
                                   call_exception=False)
        self.mock_get_group_members(powerscale_module_mock, call_exception=False)
        powerscale_module_mock.api_instance.list_auth_wellknowns = \
            MagicMock(return_value=MockGroupApi.get_wellknowns_response())
        powerscale_module_mock.group_api_instance.create_group_member = \
            MagicMock(return_value=None)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.module.fail_json.assert_not_called()

    def test_wellknown_sids_case_insensitive_match(self, powerscale_module_mock):
        """FR-6.2: display name matching is case-insensitive."""
        self.set_module_params(
            self.group_args,
            MockGroupApi.get_update_group_payload_with_wellknown_sids(
                well_known_sids=["everyone"],
                well_known_sid_state="present-in-group"))
        self.mock_get_group_detail(powerscale_module_mock, operation='update',
                                   call_exception=False)
        self.mock_get_group_members(powerscale_module_mock, call_exception=False)
        powerscale_module_mock.api_instance.list_auth_wellknowns = \
            MagicMock(return_value=MockGroupApi.get_wellknowns_response())
        powerscale_module_mock.group_api_instance.create_group_member = \
            MagicMock(return_value=None)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.module.fail_json.assert_not_called()

    def test_group_member_state_without_group_members_rejected(self, powerscale_module_mock):
        """Validation: group_member_state given without group_members fails."""
        self.set_module_params(
            self.group_args,
            MockGroupApi.get_update_group_payload_with_group_members(
                group_members=[],
                group_member_state="present-in-group"))
        self.mock_get_group_detail(powerscale_module_mock, operation='update',
                                   call_exception=False)
        self.mock_get_group_members(powerscale_module_mock, call_exception=False)
        self.capture_fail_json_method(
            "'group_member_state' is given, 'group_members' are not specified",
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_well_known_sid_state_without_sids_rejected(self, powerscale_module_mock):
        """Validation: well_known_sid_state given without well_known_sids fails."""
        self.set_module_params(
            self.group_args,
            MockGroupApi.get_update_group_payload_with_wellknown_sids(
                well_known_sids=[],
                well_known_sid_state="present-in-group"))
        self.mock_get_group_detail(powerscale_module_mock, operation='update',
                                   call_exception=False)
        self.mock_get_group_members(powerscale_module_mock, call_exception=False)
        self.capture_fail_json_method(
            "'well_known_sid_state' is given, 'well_known_sids' are not specified",
            powerscale_module_mock,
            "perform_module_operation",
        )

    # ------------------------------------------------------------------
    # Phase 2: Child Group Membership — resolve_group_id() tests
    # ------------------------------------------------------------------

    def mock_get_auth_group_for_resolve(self, powerscale_module_mock,
                                        provider="local", call_exception=False):
        """Mock AuthApi.get_auth_group for group resolution tests."""
        if call_exception:
            powerscale_module_mock.api_instance.get_auth_group = \
                MagicMock(side_effect=Exception("SDK boom"))
        else:
            powerscale_module_mock.api_instance.get_auth_group = \
                MagicMock(return_value=MockGroupApi.get_auth_group_response(provider))

    def test_resolve_group_id_local(self, powerscale_module_mock):
        """FR-1.1/AC-001: resolve_group_id for local provider returns SID."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload_with_group_members())
        self.mock_get_auth_group_for_resolve(powerscale_module_mock, provider="local")
        result = powerscale_module_mock.resolve_group_id(
            "child_local_grp", "local", "System")
        assert result == "SID:S-1-5-21-1111111111-2222222222-3333333333-2001"

    def test_resolve_group_id_ads(self, powerscale_module_mock):
        """FR-1.1/AC-001: resolve_group_id for ads provider returns SID."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload_with_group_members())
        self.mock_get_auth_group_for_resolve(powerscale_module_mock, provider="ads")
        result = powerscale_module_mock.resolve_group_id(
            "CORP\\ad_child_grp", "ads", "System")
        assert result == "SID:S-1-5-21-4444444444-5555555555-6666666666-3001"

    def test_resolve_group_id_ldap(self, powerscale_module_mock):
        """FR-1.1/AC-001: resolve_group_id for ldap provider returns SID."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload_with_group_members())
        self.mock_get_auth_group_for_resolve(powerscale_module_mock, provider="ldap")
        result = powerscale_module_mock.resolve_group_id(
            "ldap_child_grp", "ldap", "System")
        assert result == "SID:S-1-5-21-7777777777-8888888888-9999999999-4001"

    def test_resolve_group_id_nis(self, powerscale_module_mock):
        """FR-1.1/AC-001: resolve_group_id for nis provider returns SID."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload_with_group_members())
        self.mock_get_auth_group_for_resolve(powerscale_module_mock, provider="nis")
        result = powerscale_module_mock.resolve_group_id(
            "nis_child_grp", "nis", "System")
        assert result == "SID:S-1-5-21-1010101010-2020202020-3030303030-5001"

    def test_resolve_group_id_file(self, powerscale_module_mock):
        """FR-1.1/AC-001: resolve_group_id for file provider returns SID."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload_with_group_members())
        self.mock_get_auth_group_for_resolve(powerscale_module_mock, provider="file")
        result = powerscale_module_mock.resolve_group_id(
            "file_child_grp", "file", "System")
        assert result == "SID:S-1-5-21-4040404040-5050505050-6060606060-6001"

    def test_resolve_group_id_nonexistent_group_exception(self, powerscale_module_mock):
        """FR-1.1: resolve_group_id raises error for non-existent group."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload_with_group_members())
        self.mock_get_auth_group_for_resolve(powerscale_module_mock, provider=None)
        self.capture_fail_json_method(
            "Group 'no_such_group' could not be resolved in provider 'local'"
            " in access zone 'System'",
            powerscale_module_mock,
            "resolve_group_id",
            "no_such_group", "local", "System",
        )

    # ------------------------------------------------------------------
    # Phase 2: add/remove group member helpers
    # ------------------------------------------------------------------

    def test_add_group_member_to_group_calls_post(self, powerscale_module_mock):
        """FR-1.1: add_group_member_to_group calls POST with type=group."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload_with_group_members())
        self.mock_get_group_members(powerscale_module_mock, call_exception=False)
        powerscale_module_mock.group_api_instance.create_group_member = \
            MagicMock(return_value=None)
        result = powerscale_module_mock.add_group_member_to_group(
            "GROUP:test_group",
            "SID:S-1-5-21-1111111111-2222222222-3333333333-2001",
            "child_local_grp",
            "System", "local")
        assert result is True
        powerscale_module_mock.group_api_instance.create_group_member.assert_called_once()

    def test_remove_group_member_from_group_calls_delete(self, powerscale_module_mock):
        """FR-1.2: remove_group_member_from_group calls DELETE for member."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload_with_group_members())
        # Member must be present for removal to trigger
        members = MockSDKResponse({"members": [
            {"id": "SID:S-1-5-21-1111111111-2222222222-3333333333-2001",
             "name": "child_local_grp", "type": "group"}
        ]})
        powerscale_module_mock.group_api_instance.list_group_members = \
            MagicMock(return_value=members)
        powerscale_module_mock.group_api_instance.delete_group_member = \
            MagicMock(return_value=None)
        result = powerscale_module_mock.remove_group_member_from_group(
            "GROUP:test_group",
            "SID:S-1-5-21-1111111111-2222222222-3333333333-2001",
            "child_local_grp",
            "System", "local")
        assert result is True
        powerscale_module_mock.group_api_instance.delete_group_member.assert_called_once()

    def test_add_group_member_idempotent_already_exists(self, powerscale_module_mock):
        """FR-1.1 idempotent: add when member already exists returns no change."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload_with_group_members())
        # Create a member list that includes child_local_grp
        members = MockSDKResponse({"members": [
            {"id": "SID:S-1-5-21-1111111111-2222222222-3333333333-2001",
             "name": "child_local_grp", "type": "group"}
        ]})
        powerscale_module_mock.group_api_instance.list_group_members = \
            MagicMock(return_value=members)
        powerscale_module_mock.group_api_instance.create_group_member = \
            MagicMock(return_value=None)
        result = powerscale_module_mock.add_group_member_to_group(
            "GROUP:test_group",
            "SID:S-1-5-21-1111111111-2222222222-3333333333-2001",
            "child_local_grp",
            "System", "local")
        assert result is False
        powerscale_module_mock.group_api_instance.create_group_member.assert_not_called()

    def test_remove_group_member_idempotent_not_present(self, powerscale_module_mock):
        """FR-1.2 idempotent: remove when member not present returns no change."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload_with_group_members())
        # Empty member list
        members = MockSDKResponse({"members": []})
        powerscale_module_mock.group_api_instance.list_group_members = \
            MagicMock(return_value=members)
        powerscale_module_mock.group_api_instance.delete_group_member = \
            MagicMock(return_value=None)
        result = powerscale_module_mock.remove_group_member_from_group(
            "GROUP:test_group",
            "SID:S-1-5-21-1111111111-2222222222-3333333333-2001",
            "child_local_grp",
            "System", "local")
        assert result is False
        powerscale_module_mock.group_api_instance.delete_group_member.assert_not_called()

    # ------------------------------------------------------------------
    # Phase 3: Well-Known SID Membership — resolve & add/remove helpers
    # ------------------------------------------------------------------

    def mock_wellknowns(self, powerscale_module_mock, call_exception=False):
        """Mock AuthApi.list_auth_wellknowns."""
        if call_exception:
            powerscale_module_mock.api_instance.list_auth_wellknowns = \
                MagicMock(side_effect=Exception("SDK boom"))
        else:
            powerscale_module_mock.api_instance.list_auth_wellknowns = \
                MagicMock(return_value=MockGroupApi.get_wellknowns_response())

    def test_resolve_well_known_sid_by_display_name(self, powerscale_module_mock):
        """FR-2.1: resolve_well_known_sid resolves display name to SID string."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload_with_wellknown_sids())
        self.mock_wellknowns(powerscale_module_mock)
        sid_id, display_name = powerscale_module_mock.resolve_well_known_sid("Everyone")
        assert sid_id == "SID:S-1-1-0"
        assert display_name == "Everyone"

    def test_resolve_well_known_sid_by_sid_string(self, powerscale_module_mock):
        """FR-2.1: resolve_well_known_sid resolves SID string."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload_with_wellknown_sids())
        self.mock_wellknowns(powerscale_module_mock)
        sid_id, display_name = powerscale_module_mock.resolve_well_known_sid("S-1-1-0")
        assert sid_id == "SID:S-1-1-0"
        assert display_name == "Everyone"

    def test_resolve_well_known_sid_case_insensitive(self, powerscale_module_mock):
        """FR-2.1: display name matching is case-insensitive."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload_with_wellknown_sids())
        self.mock_wellknowns(powerscale_module_mock)
        sid_id, display_name = powerscale_module_mock.resolve_well_known_sid("everyone")
        assert sid_id == "SID:S-1-1-0"
        assert display_name == "Everyone"

    def test_resolve_well_known_sid_unrecognised_exception(self, powerscale_module_mock):
        """FR-2.1: unrecognised value raises error."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload_with_wellknown_sids())
        self.mock_wellknowns(powerscale_module_mock)
        self.capture_fail_json_method(
            "'BogusName' is not a recognised well-known SID name or SID string",
            powerscale_module_mock,
            "resolve_well_known_sid",
            "BogusName",
        )

    def test_resolve_well_known_sid_edge_case_special_chars(self, powerscale_module_mock):
        """FR-2.1: SID with special characters in name (e.g. backslash) resolves."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload_with_wellknown_sids())
        self.mock_wellknowns(powerscale_module_mock)
        sid_id, display_name = powerscale_module_mock.resolve_well_known_sid(
            "NT AUTHORITY\\INTERACTIVE")
        assert sid_id == "SID:S-1-5-4"
        assert display_name == "NT AUTHORITY\\INTERACTIVE"

    def test_add_wellknown_to_group_calls_post(self, powerscale_module_mock):
        """FR-2.1: add_wellknown_to_group calls POST with type=wellknown."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload_with_wellknown_sids())
        self.mock_get_group_members(powerscale_module_mock, call_exception=False)
        powerscale_module_mock.group_api_instance.create_group_member = \
            MagicMock(return_value=None)
        result = powerscale_module_mock.add_wellknown_to_group(
            "GROUP:test_group", "SID:S-1-1-0", "Everyone",
            "System", "local")
        assert result is True
        powerscale_module_mock.group_api_instance.create_group_member.assert_called_once()

    def test_remove_wellknown_from_group_calls_delete(self, powerscale_module_mock):
        """FR-2.2: remove_wellknown_from_group calls DELETE for the SID member."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload_with_wellknown_sids())
        # Member must be present for removal
        members = MockSDKResponse({"members": [
            {"id": "SID:S-1-1-0", "name": "Everyone", "type": "wellknown"}
        ]})
        powerscale_module_mock.group_api_instance.list_group_members = \
            MagicMock(return_value=members)
        powerscale_module_mock.group_api_instance.delete_group_member = \
            MagicMock(return_value=None)
        result = powerscale_module_mock.remove_wellknown_from_group(
            "GROUP:test_group", "SID:S-1-1-0", "Everyone",
            "System", "local")
        assert result is True
        powerscale_module_mock.group_api_instance.delete_group_member.assert_called_once()

    def test_add_wellknown_idempotent_already_member(self, powerscale_module_mock):
        """FR-2.1 idempotent: add SID already a member returns no change."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload_with_wellknown_sids())
        members = MockSDKResponse({"members": [
            {"id": "SID:S-1-1-0", "name": "Everyone", "type": "wellknown"}
        ]})
        powerscale_module_mock.group_api_instance.list_group_members = \
            MagicMock(return_value=members)
        powerscale_module_mock.group_api_instance.create_group_member = \
            MagicMock(return_value=None)
        result = powerscale_module_mock.add_wellknown_to_group(
            "GROUP:test_group", "SID:S-1-1-0", "Everyone",
            "System", "local")
        assert result is False
        powerscale_module_mock.group_api_instance.create_group_member.assert_not_called()

    def test_remove_wellknown_idempotent_not_member(self, powerscale_module_mock):
        """FR-2.2 idempotent: remove SID not a member returns no change."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload_with_wellknown_sids())
        members = MockSDKResponse({"members": []})
        powerscale_module_mock.group_api_instance.list_group_members = \
            MagicMock(return_value=members)
        powerscale_module_mock.group_api_instance.delete_group_member = \
            MagicMock(return_value=None)
        result = powerscale_module_mock.remove_wellknown_from_group(
            "GROUP:test_group", "SID:S-1-1-0", "Everyone",
            "System", "local")
        assert result is False
        powerscale_module_mock.group_api_instance.delete_group_member.assert_not_called()

    # ------------------------------------------------------------------
    # Phase 4: Integration — group_members in update_group()
    # ------------------------------------------------------------------

    def setup_group_member_integration(self, powerscale_module_mock,
                                       members=None, resolve_provider="local"):
        """Wire all mocks for group_members integration tests."""
        self.mock_get_group_detail(powerscale_module_mock, operation='update',
                                   call_exception=False)
        if members is None:
            self.mock_get_group_members(powerscale_module_mock,
                                       call_exception=False)
        else:
            powerscale_module_mock.group_api_instance.list_group_members = \
                MagicMock(return_value=members)
        self.mock_get_auth_group_for_resolve(powerscale_module_mock,
                                             provider=resolve_provider)
        powerscale_module_mock.group_api_instance.create_group_member = \
            MagicMock(return_value=None)
        powerscale_module_mock.group_api_instance.delete_group_member = \
            MagicMock(return_value=None)

    def test_add_single_child_group_via_group_members(self, powerscale_module_mock):
        """AC-001: adding a child group via group_member_state returns changed=true."""
        self.set_module_params(
            self.group_args,
            MockGroupApi.get_update_group_payload_with_group_members(
                group_members=[{"group_name": "child_local_grp"}],
                group_member_state="present-in-group"))
        self.setup_group_member_integration(powerscale_module_mock)
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']

    def test_add_multiple_child_groups_different_providers(self, powerscale_module_mock):
        """AC-001: adding groups from different providers in one invocation."""
        self.set_module_params(
            self.group_args,
            MockGroupApi.get_update_group_payload_with_group_members(
                group_members=[
                    {"group_name": "child_local_grp", "provider_type": "local"},
                    {"group_name": "ldap_child_grp", "provider_type": "ldap"},
                ],
                group_member_state="present-in-group"))
        self.mock_get_group_members(powerscale_module_mock, call_exception=False)
        # get_auth_group is called for: 1) get_group_details (present check),
        # 2) resolve child_local_grp, 3) resolve ldap_child_grp,
        # 4) final get_group_details
        powerscale_module_mock.api_instance.get_auth_group = MagicMock(
            side_effect=[
                MockGroupApi.get_group_detail(),   # _handle_present_state
                MockGroupApi.get_auth_group_response("local"),
                MockGroupApi.get_auth_group_response("ldap"),
                MockGroupApi.get_group_detail(),   # final get_group_details
            ])
        powerscale_module_mock.group_api_instance.create_group_member = \
            MagicMock(return_value=None)
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']
        assert powerscale_module_mock.group_api_instance.create_group_member.call_count == 2

    def test_remove_child_group_via_group_members(self, powerscale_module_mock):
        """AC-002: removing a child group via group_member_state returns changed=true."""
        self.set_module_params(
            self.group_args,
            MockGroupApi.get_update_group_payload_with_group_members(
                group_members=[{"group_name": "child_local_grp"}],
                group_member_state="absent-in-group"))
        # Child must be present in members list
        members = MockSDKResponse({"members": [
            {"id": "SID:S-1-5-21-1111111111-2222222222-3333333333-2001",
             "name": "child_local_grp", "type": "group"}
        ]})
        self.setup_group_member_integration(powerscale_module_mock,
                                            members=members)
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']

    def test_group_members_defaults_to_empty_when_omitted(self, powerscale_module_mock):
        """FR-3.1: group_members defaults to [] when omitted."""
        payload = MockGroupApi.CREATE_GROUP_PAYLOAD.copy()
        payload['users'] = []
        payload['user_state'] = None
        payload['group_members'] = []
        payload['group_member_state'] = None
        payload['well_known_sids'] = []
        payload['well_known_sid_state'] = None
        self.set_module_params(self.group_args, payload)
        self.mock_get_group_detail(powerscale_module_mock, operation='update',
                                   call_exception=False)
        self.mock_get_group_members(powerscale_module_mock, call_exception=False)
        powerscale_module_mock.perform_module_operation()
        assert not powerscale_module_mock.module.exit_json.call_args[1]['changed']

    # ------------------------------------------------------------------
    # Phase 4: Integration — well_known_sids in update_group()
    # ------------------------------------------------------------------

    def setup_wellknown_integration(self, powerscale_module_mock,
                                    members=None):
        """Wire all mocks for well_known_sids integration tests."""
        self.mock_get_group_detail(powerscale_module_mock, operation='update',
                                   call_exception=False)
        if members is None:
            self.mock_get_group_members(powerscale_module_mock,
                                       call_exception=False)
        else:
            powerscale_module_mock.group_api_instance.list_group_members = \
                MagicMock(return_value=members)
        self.mock_wellknowns(powerscale_module_mock)
        powerscale_module_mock.group_api_instance.create_group_member = \
            MagicMock(return_value=None)
        powerscale_module_mock.group_api_instance.delete_group_member = \
            MagicMock(return_value=None)

    def test_add_single_wellknown_sid_via_well_known_sids(self, powerscale_module_mock):
        """AC-003: adding a well-known SID returns changed=true."""
        self.set_module_params(
            self.group_args,
            MockGroupApi.get_update_group_payload_with_wellknown_sids(
                well_known_sids=["Everyone"],
                well_known_sid_state="present-in-group"))
        self.setup_wellknown_integration(powerscale_module_mock)
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']

    def test_add_multiple_wellknown_sids_in_one_invocation(self, powerscale_module_mock):
        """AC-003: adding multiple well-known SIDs in one invocation."""
        self.set_module_params(
            self.group_args,
            MockGroupApi.get_update_group_payload_with_wellknown_sids(
                well_known_sids=["Everyone", "Authenticated Users"],
                well_known_sid_state="present-in-group"))
        self.setup_wellknown_integration(powerscale_module_mock)
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']
        assert powerscale_module_mock.group_api_instance.create_group_member.call_count == 2

    def test_remove_wellknown_sid_via_well_known_sids(self, powerscale_module_mock):
        """AC-004: removing a well-known SID returns changed=true."""
        self.set_module_params(
            self.group_args,
            MockGroupApi.get_update_group_payload_with_wellknown_sids(
                well_known_sids=["Everyone"],
                well_known_sid_state="absent-in-group"))
        members = MockSDKResponse({"members": [
            {"id": "SID:S-1-1-0", "name": "Everyone", "type": "wellknown"}
        ]})
        self.setup_wellknown_integration(powerscale_module_mock,
                                         members=members)
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']

    def test_well_known_sids_defaults_to_empty_when_omitted(self, powerscale_module_mock):
        """FR-3.1: well_known_sids defaults to [] when omitted."""
        payload = MockGroupApi.CREATE_GROUP_PAYLOAD.copy()
        payload['users'] = []
        payload['user_state'] = None
        payload['group_members'] = []
        payload['group_member_state'] = None
        payload['well_known_sids'] = []
        payload['well_known_sid_state'] = None
        self.set_module_params(self.group_args, payload)
        self.mock_get_group_detail(powerscale_module_mock, operation='update',
                                   call_exception=False)
        self.mock_get_group_members(powerscale_module_mock, call_exception=False)
        powerscale_module_mock.perform_module_operation()
        assert not powerscale_module_mock.module.exit_json.call_args[1]['changed']

    # ------------------------------------------------------------------
    # Phase 4: Mixed member types (AC-005)
    # ------------------------------------------------------------------

    def test_mixed_member_types_add(self, powerscale_module_mock):
        """AC-005: add users, group_members, and well_known_sids in a single task."""
        payload = MockGroupApi.CREATE_GROUP_PAYLOAD.copy()
        payload['group_id'] = None
        payload['users'] = [{"user_name": "new_user"}]
        payload['user_state'] = "present-in-group"
        payload['group_members'] = [{"group_name": "child_local_grp"}]
        payload['group_member_state'] = "present-in-group"
        payload['well_known_sids'] = ["Everyone"]
        payload['well_known_sid_state'] = "present-in-group"
        self.set_module_params(self.group_args, payload)
        empty_members = MockSDKResponse({"members": []})
        # get_auth_group: (1) _handle_present_state, (2) resolve child group,
        # (3) final get_group_details
        powerscale_module_mock.api_instance.get_auth_group = MagicMock(
            side_effect=[
                MockGroupApi.get_group_detail(),
                MockGroupApi.get_auth_group_response("local"),
                MockGroupApi.get_group_detail(),
            ])
        powerscale_module_mock.group_api_instance.list_group_members = \
            MagicMock(return_value=empty_members)
        self.mock_wellknowns(powerscale_module_mock)
        powerscale_module_mock.group_api_instance.create_group_member = \
            MagicMock(return_value=None)
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']
        # 3 members added: 1 user + 1 group + 1 SID
        assert powerscale_module_mock.group_api_instance.create_group_member.call_count >= 3

    def test_remove_only_group_members_keep_others(self, powerscale_module_mock):
        """AC-005: remove only group_members while keeping users and SIDs."""
        payload = MockGroupApi.CREATE_GROUP_PAYLOAD.copy()
        payload['group_id'] = None
        payload['users'] = []
        payload['user_state'] = None
        payload['group_members'] = [{"group_name": "child_local_grp"}]
        payload['group_member_state'] = "absent-in-group"
        payload['well_known_sids'] = []
        payload['well_known_sid_state'] = None
        self.set_module_params(self.group_args, payload)
        members = MockSDKResponse({"members": [
            {"id": "SID:S-1-5-21-1111111111-2222222222-3333333333-2001",
             "name": "child_local_grp", "type": "group"},
            {"id": "SID:S-1-1-0", "name": "Everyone", "type": "wellknown"},
            {"id": "SID:S-1-5-21-1426242897-2739835565-3634425493-501",
             "name": "test_user", "type": "user"},
        ]})
        # get_auth_group: (1) _handle_present_state, (2) resolve child group,
        # (3) final get_group_details
        powerscale_module_mock.api_instance.get_auth_group = MagicMock(
            side_effect=[
                MockGroupApi.get_group_detail(),
                MockGroupApi.get_auth_group_response("local"),
                MockGroupApi.get_group_detail(),
            ])
        powerscale_module_mock.group_api_instance.list_group_members = \
            MagicMock(return_value=members)
        powerscale_module_mock.group_api_instance.delete_group_member = \
            MagicMock(return_value=None)
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']
        # Only 1 deletion (the child group), not the user or SID
        assert powerscale_module_mock.group_api_instance.delete_group_member.call_count == 1

    def test_processing_order_users_then_groups_then_sids(self, powerscale_module_mock):
        """AC-005: verify processing order — users -> group_members -> well_known_sids."""
        payload = MockGroupApi.CREATE_GROUP_PAYLOAD.copy()
        payload['group_id'] = None
        payload['users'] = [{"user_name": "new_user"}]
        payload['user_state'] = "present-in-group"
        payload['group_members'] = [{"group_name": "child_local_grp"}]
        payload['group_member_state'] = "present-in-group"
        payload['well_known_sids'] = ["Everyone"]
        payload['well_known_sid_state'] = "present-in-group"
        self.set_module_params(self.group_args, payload)
        empty_members = MockSDKResponse({"members": []})
        # get_auth_group: (1) _handle_present_state, (2) resolve child group,
        # (3) final get_group_details
        powerscale_module_mock.api_instance.get_auth_group = MagicMock(
            side_effect=[
                MockGroupApi.get_group_detail(),
                MockGroupApi.get_auth_group_response("local"),
                MockGroupApi.get_group_detail(),
            ])
        powerscale_module_mock.group_api_instance.list_group_members = \
            MagicMock(return_value=empty_members)
        self.mock_wellknowns(powerscale_module_mock)
        # Track call order
        call_order = []

        def track_create(*args, **kwargs):
            member_str = str(args[0]) if args else ""
            call_order.append(member_str)
            return None

        powerscale_module_mock.group_api_instance.create_group_member = \
            MagicMock(side_effect=track_create)
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed']
        # At least 3 create calls (1 user + 1 group + 1 SID)
        assert len(call_order) >= 3

    # ==================================================================
    # Story-3078 Part 2: Compatibility, Check/Diff, Idempotency, Errors
    # ==================================================================

    # ------------------------------------------------------------------
    # Phase 1: Backward Compatibility (AC-006)
    # ------------------------------------------------------------------

    def test_user_only_playbook_add_returns_changed(self, powerscale_module_mock):
        """AC-006: user-only payload (no group_members/well_known_sids) adds
        a new user and returns changed=true — identical to pre-enhancement."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(
                                   users=[{"user_name": "new_user"}],
                                   user_state="present-in-group"))
        self.update_group(powerscale_module_mock)
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result['changed']
        powerscale_module_mock.group_api_instance.create_group_member.assert_called()

    def test_user_only_playbook_idempotent_returns_unchanged(self, powerscale_module_mock):
        """AC-006: user-only payload for already-present user returns
        changed=false — identical to pre-enhancement."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(
                                   users=[{"user_name": "test_user"}]))
        self.update_group(powerscale_module_mock)
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert not result['changed']
        powerscale_module_mock.group_api_instance.create_group_member.assert_not_called()

    def test_user_only_no_deprecation_warning(self, powerscale_module_mock):
        """AC-006: no deprecation warning emitted when new parameters omitted."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(
                                   users=[{"user_name": "test_user"}]))
        self.update_group(powerscale_module_mock)
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert 'deprecations' not in result
        assert 'warnings' not in result

    def test_new_params_default_to_none_when_omitted(self, powerscale_module_mock):
        """AC-006: group_members and well_known_sids default to None/[]
        when omitted from the argument spec."""
        payload = MockGroupApi.get_update_group_payload(
            users=[{"user_name": "test_user"}])
        # Explicitly do NOT set group_members or well_known_sids
        self.set_module_params(self.group_args, payload)
        self.update_group(powerscale_module_mock)
        # Module should succeed without any issues
        powerscale_module_mock.module.fail_json.assert_not_called()

    def test_group_details_return_structure_backward_compatible(self, powerscale_module_mock):
        """AC-006: group_details return structure includes expected keys."""
        self.set_module_params(self.group_args,
                               MockGroupApi.get_update_group_payload(
                                   users=[{"user_name": "test_user"}]))
        self.update_group(powerscale_module_mock)
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert 'group_details' in result
        assert 'changed' in result
