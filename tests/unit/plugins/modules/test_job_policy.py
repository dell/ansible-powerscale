# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Job Policy module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.job_policy import JobPolicy
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_job_policy_api as MockJobPolicyApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
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
                {"begin": "Monday 08:00", "end": "Friday 17:00", "impact": "Low"}
            ],
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.job_api.create_job_policy = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.CREATE_POLICY_RESPONSE))
        powerscale_module_mock.job_api.get_job_policy = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICY_1))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.create_job_policy.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -------------------------------------------------------------------------
    # U-JP-002: Create policy that already exists (idempotent)
    # -------------------------------------------------------------------------
    def test_create_policy_already_exists(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BusinessHours",
            "description": "Low impact during business hours",
            "intervals": [
                {"begin": "Monday 08:00", "end": "Friday 17:00", "impact": "Low"},
                {"begin": "Saturday 00:00", "end": "Sunday 23:59", "impact": "High"}
            ],
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.create_job_policy.assert_not_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # -------------------------------------------------------------------------
    # U-JP-003: Create policy raises exception on SDK error
    # -------------------------------------------------------------------------
    def test_create_policy_exception(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "TestPolicy",
            "intervals": [
                {"begin": "Monday 08:00", "end": "Friday 17:00", "impact": "Low"}
            ],
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.job_api.create_job_policy = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobPolicyApi.create_policy_failed_msg(), invoke_perform_module=True)

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
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.job_api.update_job_policy = MagicMock(
            return_value=None)
        powerscale_module_mock.job_api.get_job_policy = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICY_MODIFIED))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.update_job_policy.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -------------------------------------------------------------------------
    # U-JP-005: Modify policy intervals
    # -------------------------------------------------------------------------
    def test_modify_policy_intervals(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BusinessHours",
            "intervals": [
                {"begin": "Monday 09:00", "end": "Friday 18:00", "impact": "Medium"}
            ],
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.job_api.update_job_policy = MagicMock(
            return_value=None)
        powerscale_module_mock.job_api.get_job_policy = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICY_MODIFIED))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.update_job_policy.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -------------------------------------------------------------------------
    # U-JP-006: Modify policy with no actual change (idempotent)
    # -------------------------------------------------------------------------
    def test_modify_policy_no_change(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BusinessHours",
            "description": "Low impact during business hours",
            "intervals": [
                {"begin": "Monday 08:00", "end": "Friday 17:00", "impact": "Low"},
                {"begin": "Saturday 00:00", "end": "Sunday 23:59", "impact": "High"}
            ],
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.update_job_policy.assert_not_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

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
            MockJobPolicyApi.modify_policy_failed_msg(), invoke_perform_module=True)

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
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

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
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

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
            MockJobPolicyApi.delete_policy_failed_msg(), invoke_perform_module=True)

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
            MockJobPolicyApi.system_policy_protect_msg(), invoke_perform_module=True)

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
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # -------------------------------------------------------------------------
    # U-JP-013: Check mode for create policy (no API calls made)
    # -------------------------------------------------------------------------
    def test_check_mode_create(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "NewPolicy",
            "intervals": [
                {"begin": "Monday 08:00", "end": "Friday 17:00", "impact": "Low"}
            ],
            "state": "present"
        })
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.create_job_policy.assert_not_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

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
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

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
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        powerscale_module_mock.job_api.update_job_policy = MagicMock(
            return_value=None)
        powerscale_module_mock.job_api.get_job_policy = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICY_MODIFIED))
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
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
                {"begin": "Monday 08:00", "end": "Friday 17:00", "impact": "Low"}
            ],
            "state": "present"
        })
        self.capture_fail_json_call(
            MockJobPolicyApi.missing_policy_name_msg(), invoke_perform_module=True)

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
            return_value=MockSDKResponse(MockJobPolicyApi.CREATE_POLICY_RESPONSE))
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
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

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
            MockJobPolicyApi.system_policy_protect_msg(), invoke_perform_module=True)

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
            MockJobPolicyApi.invalid_interval_format_msg(), invoke_perform_module=True)

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
            MockJobPolicyApi.system_policy_protect_msg(), invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JP-E06: Invalid impact value should fail validation
    # -------------------------------------------------------------------------
    def test_bad_impact_value(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "policy_name": "BadPolicy",
            "intervals": [
                {"begin": "Monday 08:00", "end": "Friday 17:00", "impact": "INVALID"}
            ],
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.POLICIES_LIST))
        self.capture_fail_json_call(
            MockJobPolicyApi.bad_impact_value_msg(), invoke_perform_module=True)
