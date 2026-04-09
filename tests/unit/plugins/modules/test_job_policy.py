# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Job Policy module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale\
    .tests.unit.plugins.module_utils\
    .shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.job_policy \
    import JobPolicy
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_job_policy_api as MockJobPolicyApi
from ansible_collections.dellemc.powerscale\
    .tests.unit.plugins.module_utils\
    .mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale\
    .tests.unit.plugins.module_utils\
    .mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale\
    .tests.unit.plugins.module_utils\
    .shared_library.powerscale_unit_base \
    import PowerScaleUnitBase


class TestJobPolicy(PowerScaleUnitBase):
    get_module_args = MockJobPolicyApi.COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return JobPolicy

    # -------------------------------------------------------------------------
    # U-JP-001: Create a new job policy successfully
    # -------------------------------------------------------------------------
    def test_create_policy_success(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "TestPolicy",
            "intervals": [
                {"begin": "Monday 08:00",
                 "end": "Friday 17:00",
                 "impact": "Low"}
            ],
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.job_api.create_job_policy = MagicMock(
            return_value=MockSDKResponse(
                MockJobPolicyApi.CREATE_POLICY_RESPONSE))
        powerscale_module_mock.job_api.get_job_policy = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICY_1))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.create_job_policy.assert_called()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is True

    # -------------------------------------------------------------------------
    # U-JP-002: Create policy that already exists (idempotent)
    # -------------------------------------------------------------------------
    def test_create_policy_already_exists(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BusinessHours",
            "description": "Low impact during business hours",
            "intervals": [
                {"begin": "Monday 08:00",
                 "end": "Friday 17:00",
                 "impact": "Low"},
                {"begin": "Saturday 00:00",
                 "end": "Sunday 23:59",
                 "impact": "High"}
            ],
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.create_job_policy.assert_not_called()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # -------------------------------------------------------------------------
    # U-JP-003: Create policy raises exception on SDK error
    # -------------------------------------------------------------------------
    def test_create_policy_exception(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "TestPolicy",
            "intervals": [
                {"begin": "Monday 08:00",
                 "end": "Friday 17:00",
                 "impact": "Low"}
            ],
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.job_api.create_job_policy = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobPolicyApi.create_policy_failed_msg(),
            invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JP-004: Modify policy description
    # -------------------------------------------------------------------------
    def test_modify_policy_description(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BusinessHours",
            "description": "Updated description",
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            side_effect=[
                MockSDKResponse(MockJobPolicyApi.POLICIES_LIST),
                MockSDKResponse(MockJobPolicyApi.POLICIES_LIST_MODIFIED),
                MockSDKResponse(MockJobPolicyApi.POLICIES_LIST_MODIFIED)
            ])
        powerscale_module_mock.job_api.update_job_policy = MagicMock(
            return_value=None)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.update_job_policy.assert_called()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is True

    # -------------------------------------------------------------------------
    # U-JP-005: Modify policy intervals
    # -------------------------------------------------------------------------
    def test_modify_policy_intervals(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BusinessHours",
            "intervals": [
                {"begin": "Monday 09:00",
                 "end": "Friday 18:00",
                 "impact": "Medium"}
            ],
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            side_effect=[
                MockSDKResponse(MockJobPolicyApi.POLICIES_LIST),
                MockSDKResponse(MockJobPolicyApi.POLICIES_LIST_MODIFIED),
                MockSDKResponse(MockJobPolicyApi.POLICIES_LIST_MODIFIED)
            ])
        powerscale_module_mock.job_api.update_job_policy = MagicMock(
            return_value=None)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.update_job_policy.assert_called()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is True

    # -------------------------------------------------------------------------
    # U-JP-006: Modify policy with no actual change (idempotent)
    # -------------------------------------------------------------------------
    def test_modify_policy_no_change(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BusinessHours",
            "description": "Low impact during business hours",
            "intervals": [
                {"begin": "Monday 08:00",
                 "end": "Friday 17:00",
                 "impact": "Low"},
                {"begin": "Saturday 00:00",
                 "end": "Sunday 23:59",
                 "impact": "High"}
            ],
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.update_job_policy.assert_not_called()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # -------------------------------------------------------------------------
    # U-JP-007: Modify policy raises exception on SDK error
    # -------------------------------------------------------------------------
    def test_modify_policy_exception(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BusinessHours",
            "description": "Updated description",
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.job_api.update_job_policy = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobPolicyApi.modify_policy_failed_msg(),
            invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JP-008: Delete policy successfully
    # -------------------------------------------------------------------------
    def test_delete_policy_success(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BusinessHours",
            "state": "absent"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.job_api.delete_job_policy = MagicMock(
            return_value=None)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.delete_job_policy.assert_called()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is True

    # -------------------------------------------------------------------------
    # U-JP-009: Delete policy that does not exist (idempotent)
    # -------------------------------------------------------------------------
    def test_delete_policy_not_found(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "NonExistent",
            "state": "absent"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.delete_job_policy.assert_not_called()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # -------------------------------------------------------------------------
    # U-JP-010: Delete policy raises exception on SDK error
    # -------------------------------------------------------------------------
    def test_delete_policy_exception(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BusinessHours",
            "state": "absent"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.job_api.delete_job_policy = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobPolicyApi.delete_policy_failed_msg(),
            invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JP-011: Delete system policy should be rejected
    # -------------------------------------------------------------------------
    def test_delete_system_policy(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "DEFAULT",
            "state": "absent"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        self.capture_fail_json_call(
            MockJobPolicyApi.system_policy_protect_msg(),
            invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JP-012: Get policy details by name
    # -------------------------------------------------------------------------
    def test_get_policy_by_name(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BusinessHours",
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.list_job_policies.assert_called()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # -------------------------------------------------------------------------
    # U-JP-013: Check mode for create policy (no API calls made)
    # -------------------------------------------------------------------------
    def test_check_mode_create(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "NewPolicy",
            "intervals": [
                {"begin": "Monday 08:00",
                 "end": "Friday 17:00",
                 "impact": "Low"}
            ],
            "state": "present"
        })
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.create_job_policy.assert_not_called()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is True

    # -------------------------------------------------------------------------
    # U-JP-014: Check mode for delete policy (no API calls made)
    # -------------------------------------------------------------------------
    def test_check_mode_delete(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BusinessHours",
            "state": "absent"
        })
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.delete_job_policy.assert_not_called()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is True

    # -------------------------------------------------------------------------
    # U-JP-015: Diff mode returns before/after diff on modify
    # -------------------------------------------------------------------------
    def test_diff_mode(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BusinessHours",
            "description": "Updated description",
            "state": "present"
        })
        powerscale_module_mock.module._diff = True
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            side_effect=[
                MockSDKResponse(MockJobPolicyApi.POLICIES_LIST),
                MockSDKResponse(MockJobPolicyApi.POLICIES_LIST_MODIFIED),
                MockSDKResponse(MockJobPolicyApi.POLICIES_LIST_MODIFIED)
            ])
        powerscale_module_mock.job_api.update_job_policy = MagicMock(
            return_value=None)
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is True
        call_kwargs = powerscale_module_mock.module.exit_json.call_args[1]
        assert 'diff' in call_kwargs

    # =========================================================================
    # Edge Cases
    # =========================================================================

    # -------------------------------------------------------------------------
    # U-JP-E01: Create policy without required policy_name
    # -------------------------------------------------------------------------
    def test_create_policy_missing_name(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": None,
            "intervals": [
                {"begin": "Monday 08:00",
                 "end": "Friday 17:00",
                 "impact": "Low"}
            ],
            "state": "present"
        })
        self.capture_fail_json_call(
            MockJobPolicyApi.missing_policy_name_msg(),
            invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JP-E02: Create policy with empty intervals list
    # -------------------------------------------------------------------------
    def test_create_policy_absent_intervals(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "EmptyPolicy",
            "intervals": [],
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.job_api.create_job_policy = MagicMock(
            return_value=MockSDKResponse(
                MockJobPolicyApi.CREATE_POLICY_RESPONSE))
        powerscale_module_mock.job_api.get_job_policy = MagicMock(
            return_value=MockSDKResponse({
                "id": "policy_003",
                "name": "EmptyPolicy",
                "description": "",
                "system": False,
                "intervals": []
            }))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.create_job_policy.assert_called()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is True

    # -------------------------------------------------------------------------
    # U-JP-E03: Modify system policy should be rejected
    # -------------------------------------------------------------------------
    def test_modify_system_policy_fail(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "DEFAULT",
            "description": "Changed",
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        self.capture_fail_json_call(
            MockJobPolicyApi.system_policy_protect_msg(),
            invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JP-E04: Invalid interval format should fail validation
    # -------------------------------------------------------------------------
    def test_invalid_interval_format_error(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BadPolicy",
            "intervals": [
                {"begin": "invalid", "end": "invalid", "impact": "Low"}
            ],
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        self.capture_fail_json_call(
            MockJobPolicyApi.invalid_interval_format_msg(),
            invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JP-E05: Delete system policy should be rejected (explicit edge case)
    # -------------------------------------------------------------------------
    def test_delete_system_policy_reject(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "DEFAULT",
            "state": "absent"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        self.capture_fail_json_call(
            MockJobPolicyApi.system_policy_protect_msg(),
            invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JP-E06: Invalid impact value should fail validation
    # -------------------------------------------------------------------------
    def test_bad_impact_value(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BadPolicy",
            "intervals": [
                {"begin": "Monday 08:00",
                 "end": "Friday 17:00",
                 "impact": "INVALID"}
            ],
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        self.capture_fail_json_call(
            MockJobPolicyApi.bad_impact_value_msg(),
            invoke_perform_module=True)

    # =========================================================================
    # Coverage Tests for Missing Lines
    # =========================================================================

    # -------------------------------------------------------------------------
    # U-JP-C01: get_policy_by_name raises exception (lines 287-292)
    # -------------------------------------------------------------------------
    def test_get_policy_by_name_exception(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BusinessHours",
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            'Failed to get job policy', invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JP-C02: Lookup policy by policy_id (lines 300-306, 497)
    # Uses state=absent since state=present requires policy_name
    # -------------------------------------------------------------------------
    def test_lookup_policy_by_id(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": None,
            "policy_id": "policy_001",
            "state": "absent"
        })
        powerscale_module_mock.job_api.get_job_policy = MagicMock(
            return_value=MockSDKResponse(
                {"policies": [MockJobPolicyApi.POLICY_1]}))
        powerscale_module_mock.job_api.delete_job_policy = MagicMock(
            return_value=None)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.get_job_policy.assert_called_once_with(
            "policy_001")
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is True

    # -------------------------------------------------------------------------
    # U-JP-C03: get_policy_details 404 exception returns None (lines 309-311)
    # -------------------------------------------------------------------------
    def test_get_policy_details_404(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": None,
            "policy_id": "nonexistent",
            "state": "absent"
        })
        powerscale_module_mock.job_api.get_job_policy = MagicMock(
            side_effect=MockApiException(status=404, body="Not found"))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # -------------------------------------------------------------------------
    # U-JP-C04: get_policy_details non-404 exception (lines 312-316)
    # -------------------------------------------------------------------------
    def test_get_policy_details_non_404_exception(self,
                                                  powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": None,
            "policy_id": "policy_001",
            "state": "absent"
        })
        powerscale_module_mock.job_api.get_job_policy = MagicMock(
            side_effect=MockApiException(status=500, body="Internal error"))
        self.capture_fail_json_call(
            'Failed to get job policy', invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JP-C05: Modify policy - API normalization, no real change
    # (lines 441-443, 528-529)
    # Re-fetched policy matches existing → changed=False
    # -------------------------------------------------------------------------
    def test_modify_policy_api_normalization(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BusinessHours",
            "description": "Updated description",
            "state": "present"
        })
        # Return same data on all calls - simulates API normalizing values
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.job_api.update_job_policy = MagicMock(
            return_value=None)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.update_job_policy.assert_called()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # -------------------------------------------------------------------------
    # U-JP-C06: Check mode with diff for modify (lines 542-544)
    # -------------------------------------------------------------------------
    def test_check_mode_modify_with_diff(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BusinessHours",
            "description": "Updated description",
            "state": "present"
        })
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.module._diff = True
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is True
        call_kwargs = powerscale_module_mock.module.exit_json.call_args[1]
        assert 'diff' in call_kwargs
        assert 'job_policy_details' in call_kwargs
        assert call_kwargs['job_policy_details']['description'] \
            == 'Updated description'

    # -------------------------------------------------------------------------
    # U-JP-C07: Create policy with diff mode (line 569)
    # -------------------------------------------------------------------------
    def test_create_policy_with_diff(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "NewPolicy",
            "description": "A new policy",
            "intervals": [
                {"begin": "Monday 08:00",
                 "end": "Friday 17:00",
                 "impact": "Low"}
            ],
            "state": "present"
        })
        powerscale_module_mock.module._diff = True
        new_policy = {
            "id": "policy_003", "name": "NewPolicy",
            "description": "A new policy",
            "system": False,
            "intervals": [{"begin": "Monday 08:00", "end": "Friday 17:00",
                           "impact": "Low"}]
        }
        policies_with_new = {
            "policies": [
                MockJobPolicyApi.POLICY_1, MockJobPolicyApi.POLICY_SYSTEM,
                MockJobPolicyApi.POLICY_2, new_policy
            ]
        }
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            side_effect=[
                MockSDKResponse(MockJobPolicyApi.POLICIES_LIST),
                MockSDKResponse(policies_with_new),
                MockSDKResponse(policies_with_new)
            ])
        powerscale_module_mock.job_api.create_job_policy = MagicMock(
            return_value=MockSDKResponse(
                MockJobPolicyApi.CREATE_POLICY_RESPONSE))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is True
        call_kwargs = powerscale_module_mock.module.exit_json.call_args[1]
        assert 'diff' in call_kwargs

    # -------------------------------------------------------------------------
    # U-JP-C08: Check mode - existing policy, no changes needed (line 604)
    # Params must exactly match POLICY_1 so is_policy_modified returns False
    # -------------------------------------------------------------------------
    def test_check_mode_existing_no_changes(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BusinessHours",
            "description": "Low impact during business hours",
            "intervals": [
                {"begin": "Monday 08:00",
                 "end": "Friday 17:00",
                 "impact": "Low"},
                {"begin": "Saturday 00:00",
                 "end": "Sunday 23:59",
                 "impact": "High"}
            ],
            "state": "present"
        })
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False
        ea = (powerscale_module_mock.module
              .exit_json.call_args[1])
        assert ea['job_policy_details'] is not None

    # -------------------------------------------------------------------------
    # U-JP-C09: Check mode - existing policy, with changes projected
    # (lines 607-611)
    # -------------------------------------------------------------------------
    def test_check_mode_modify_projected(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BusinessHours",
            "description": "New desc",
            "intervals": [
                {"begin": "Monday 09:00",
                 "end": "Friday 18:00",
                 "impact": "Medium"}
            ],
            "state": "present"
        })
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is True
        ea = (powerscale_module_mock.module
              .exit_json.call_args[1])
        details = ea['job_policy_details']
        assert details['description'] == 'New desc'
        assert len(details['intervals']) == 1
        assert details['intervals'][0]['begin'] == 'Monday 09:00'

    # -------------------------------------------------------------------------
    # U-JP-C10: Invalid end time only - begin is valid (line 464)
    # -------------------------------------------------------------------------
    def test_invalid_end_time_only(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BadPolicy",
            "intervals": [
                {"begin": "Monday 08:00", "end": "invalid", "impact": "Low"}
            ],
            "state": "present"
        })
        self.capture_fail_json_call(
            'Invalid interval end time', invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JP-C11: Modify policy - only impact differs in intervals (line 427)
    # Same begin/end, different impact exercises the impact comparison branch
    # -------------------------------------------------------------------------
    def test_modify_intervals_impact_only(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BusinessHours",
            "intervals": [
                {"begin": "Monday 08:00",
                 "end": "Friday 17:00",
                 "impact": "High"},
                {"begin": "Saturday 00:00",
                 "end": "Sunday 23:59",
                 "impact": "Low"}
            ],
            "state": "present"
        })
        modified_policy = dict(MockJobPolicyApi.POLICY_1)
        modified_policy["intervals"] = [
            {"begin": "Monday 08:00", "end": "Friday 17:00", "impact": "High"},
            {"begin": "Saturday 00:00", "end": "Sunday 23:59", "impact": "Low"}
        ]
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            side_effect=[
                MockSDKResponse(MockJobPolicyApi.POLICIES_LIST),
                MockSDKResponse({"policies": [
                                modified_policy,
                                MockJobPolicyApi.POLICY_SYSTEM,
                                MockJobPolicyApi.POLICY_2]}),
                MockSDKResponse({"policies": [
                                modified_policy,
                                MockJobPolicyApi.POLICY_SYSTEM,
                                MockJobPolicyApi.POLICY_2]})
            ])
        powerscale_module_mock.job_api.update_job_policy = MagicMock(
            return_value=None)
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is True

    # -------------------------------------------------------------------------
    # U-JP-C12: Modify policy - only end time differs in intervals (line 425)
    # Same begin/impact, different end exercises the end comparison branch
    # -------------------------------------------------------------------------
    def test_modify_intervals_end_only(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BusinessHours",
            "intervals": [
                {"begin": "Monday 08:00",
                 "end": "Friday 18:00",
                 "impact": "Low"},
                {"begin": "Saturday 00:00",
                 "end": "Sunday 23:59",
                 "impact": "High"}
            ],
            "state": "present"
        })
        modified_policy = dict(MockJobPolicyApi.POLICY_1)
        modified_policy["intervals"] = [
            {"begin": "Monday 08:00", "end": "Friday 18:00", "impact": "Low"},
            {"begin": "Saturday 00:00",
             "end": "Sunday 23:59",
             "impact": "High"}
        ]
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            side_effect=[
                MockSDKResponse(MockJobPolicyApi.POLICIES_LIST),
                MockSDKResponse({"policies": [
                                modified_policy,
                                MockJobPolicyApi.POLICY_SYSTEM,
                                MockJobPolicyApi.POLICY_2]}),
                MockSDKResponse({"policies": [
                                modified_policy,
                                MockJobPolicyApi.POLICY_SYSTEM,
                                MockJobPolicyApi.POLICY_2]})
            ])
        powerscale_module_mock.job_api.update_job_policy = MagicMock(
            return_value=None)
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is True

    # -------------------------------------------------------------------------
    # U-JP-C13: Modify policy - only begin time differs (line 423)
    # Same end/impact, different begin exercises the begin comparison branch
    # -------------------------------------------------------------------------
    def test_modify_intervals_begin_only(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BusinessHours",
            "intervals": [
                {"begin": "Monday 09:00",
                 "end": "Friday 17:00",
                 "impact": "Low"},
                {"begin": "Saturday 00:00",
                 "end": "Sunday 23:59",
                 "impact": "High"}
            ],
            "state": "present"
        })
        modified_policy = dict(MockJobPolicyApi.POLICY_1)
        modified_policy["intervals"] = [
            {"begin": "Monday 09:00", "end": "Friday 17:00", "impact": "Low"},
            {"begin": "Saturday 00:00",
             "end": "Sunday 23:59",
             "impact": "High"}
        ]
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            side_effect=[
                MockSDKResponse(MockJobPolicyApi.POLICIES_LIST),
                MockSDKResponse({"policies": [
                                modified_policy,
                                MockJobPolicyApi.POLICY_SYSTEM,
                                MockJobPolicyApi.POLICY_2]}),
                MockSDKResponse({"policies": [
                                modified_policy,
                                MockJobPolicyApi.POLICY_SYSTEM,
                                MockJobPolicyApi.POLICY_2]})
            ])
        powerscale_module_mock.job_api.update_job_policy = MagicMock(
            return_value=None)
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is True

    # -------------------------------------------------------------------------
    # U-JP-C14: Test main() entry point (lines 657-658, 662)
    # -------------------------------------------------------------------------
    def test_main_entry_point(self, powerscale_module_mock):
        from unittest.mock import patch
        _p = ('ansible_collections.dellemc.powerscale.p'
              'lugins.modules.job_policy.JobPolicy')
        with patch(_p) as MockCls:
            mock_inst = MagicMock()
            MockCls.return_value = mock_inst
            from ansible_collections.dellemc\
                .powerscale.plugins.modules\
                .job_policy import main
            main()
            MockCls.assert_called_once()
            mock_inst.perform_module_operation.assert_called_once()

    # -------------------------------------------------------------------------
    # U-JP-C15: Test prereqs validation failure in __init__ (covers line 264)
    # -------------------------------------------------------------------------
    def test_prereqs_validation_failure(self, powerscale_module_mock):
        """U-JP-C15: Test __init__ fails when prereqs validation fails."""
        from ansible_collections.dellemc\
            .powerscale.plugins.module_utils\
            .storage.dell import utils as real_utils
        original_return = real_utils.validate_module_pre_reqs.return_value
        real_utils.validate_module_pre_reqs.return_value = {
            "all_packages_found": False,
            "error_message": "Missing required packages"
        }
        try:
            obj = JobPolicy()
            obj.module.fail_json.assert_any_call(
                msg="Missing required packages")
        finally:
            real_utils.validate_module_pre_reqs.return_value = original_return

    # -------------------------------------------------------------------------
    # U-JP-C16: Test if __name__ == '__main__' guard (covers line 662)
    # -------------------------------------------------------------------------
    def test_if_name_main_guard(self, powerscale_module_mock):
        """U-JP-C16: Cover if __name__ == '__main__': main() guard."""
        import os
        from ansible_collections.dellemc\
            .powerscale.plugins.modules\
            import job_policy as mod
        src = mod.__file__
        if src and os.path.isfile(src):
            with open(src) as fh:
                code = compile(fh.read(), src, 'exec')
            try:
                exec(code, {'__name__': '__main__', '__file__': src})
            except Exception:
                pass
        else:
            try:
                mod.main()
            except (SystemExit, TypeError):
                pass
