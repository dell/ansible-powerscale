# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Job module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.job import Job
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_job_api as MockJobApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase


class TestJob(PowerScaleUnitBase):
    get_module_args = MockJobApi.COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return Job

    # -------------------------------------------------------------------------
    # U-JB-001: Start a new job successfully
    # -------------------------------------------------------------------------
    def test_start_job_success(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_type": "TreeDelete",
            "paths": ["/ifs/data/archive"],
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOBS_LIST_EMPTY))
        powerscale_module_mock.job_api.create_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.CREATE_JOB_RESPONSE))
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_CREATED))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.create_job_job.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -------------------------------------------------------------------------
    # U-JB-002: Start a new job with explicit priority
    # -------------------------------------------------------------------------
    def test_start_job_with_priority(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_type": "TreeDelete",
            "paths": ["/ifs/data/archive"],
            "priority": 3,
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOBS_LIST_EMPTY))
        powerscale_module_mock.job_api.create_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.CREATE_JOB_RESPONSE))
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_CREATED))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.create_job_job.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -------------------------------------------------------------------------
    # U-JB-003: Start a new job with explicit policy
    # -------------------------------------------------------------------------
    def test_start_job_with_policy(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_type": "TreeDelete",
            "paths": ["/ifs/data/archive"],
            "policy": "LOW",
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOBS_LIST_EMPTY))
        powerscale_module_mock.job_api.create_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.CREATE_JOB_RESPONSE))
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_CREATED))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.create_job_job.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -------------------------------------------------------------------------
    # U-JB-004: Start a new job with custom parameters
    # -------------------------------------------------------------------------
    def test_start_job_with_params(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_type": "TreeDelete",
            "paths": ["/ifs/data/archive"],
            "job_params": {"key": "value"},
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOBS_LIST_EMPTY))
        powerscale_module_mock.job_api.create_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.CREATE_JOB_RESPONSE))
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_CREATED))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.create_job_job.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -------------------------------------------------------------------------
    # U-JB-005: Start a duplicate job when allow_dup is True
    # -------------------------------------------------------------------------
    def test_start_job_allow_dup(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_type": "SmartPools",
            "paths": ["/ifs/data"],
            "allow_dup": True,
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOBS_LIST_WITH_RUNNING))
        powerscale_module_mock.job_api.create_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.CREATE_JOB_RESPONSE))
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_CREATED))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.create_job_job.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -------------------------------------------------------------------------
    # U-JB-006: Start job is idempotent when same type is already running
    # -------------------------------------------------------------------------
    def test_start_job_idempotent(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_type": "SmartPools",
            "paths": ["/ifs/data"],
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOBS_LIST_WITH_RUNNING))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.create_job_job.assert_not_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # -------------------------------------------------------------------------
    # U-JB-007: Start job raises exception on SDK error
    # -------------------------------------------------------------------------
    def test_start_job_exception(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_type": "TreeDelete",
            "paths": ["/ifs/data/archive"],
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOBS_LIST_EMPTY))
        powerscale_module_mock.job_api.create_job_job = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobApi.start_job_failed_msg(), invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JB-008: Get job details by ID
    # -------------------------------------------------------------------------
    def test_get_job_by_id_success(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_id": 42,
            "state": "present"
        })
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_RUNNING))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.get_job_job.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # -------------------------------------------------------------------------
    # U-JB-009: Get job by ID when not found
    # -------------------------------------------------------------------------
    def test_get_job_by_id_not_found(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_id": 9999,
            "state": "present"
        })
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            side_effect=MockApiException(status=404, body="Job not found"))
        self.capture_fail_json_call(
            MockJobApi.get_job_failed_msg(), invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JB-010: Pause a running job
    # -------------------------------------------------------------------------
    def test_pause_running_job(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_id": 42,
            "job_state": "paused",
            "state": "present"
        })
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_RUNNING))
        powerscale_module_mock.job_api.update_job_job = MagicMock(
            return_value=None)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.update_job_job.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -------------------------------------------------------------------------
    # U-JB-011: Pause an already paused job (idempotent)
    # -------------------------------------------------------------------------
    def test_pause_already_paused(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_id": 42,
            "job_state": "paused",
            "state": "present"
        })
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_PAUSED))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.update_job_job.assert_not_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # -------------------------------------------------------------------------
    # U-JB-012: Resume a paused job
    # -------------------------------------------------------------------------
    def test_resume_paused_job(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_id": 42,
            "job_state": "running",
            "state": "present"
        })
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_PAUSED))
        powerscale_module_mock.job_api.update_job_job = MagicMock(
            return_value=None)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.update_job_job.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -------------------------------------------------------------------------
    # U-JB-013: Resume an already running job (idempotent)
    # -------------------------------------------------------------------------
    def test_resume_already_running(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_id": 42,
            "job_state": "running",
            "state": "present"
        })
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_RUNNING))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.update_job_job.assert_not_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # -------------------------------------------------------------------------
    # U-JB-014: Cancel a running job
    # -------------------------------------------------------------------------
    def test_cancel_job(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_id": 42,
            "job_state": "cancelled",
            "state": "present"
        })
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_RUNNING))
        powerscale_module_mock.job_api.update_job_job = MagicMock(
            return_value=None)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.update_job_job.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -------------------------------------------------------------------------
    # U-JB-015: Modify job priority
    # -------------------------------------------------------------------------
    def test_modify_priority(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_id": 42,
            "priority": 2,
            "state": "present"
        })
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_RUNNING))
        powerscale_module_mock.job_api.update_job_job = MagicMock(
            return_value=None)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.update_job_job.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -------------------------------------------------------------------------
    # U-JB-016: Modify job policy
    # -------------------------------------------------------------------------
    def test_modify_policy(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_id": 42,
            "policy": "HIGH",
            "state": "present"
        })
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_RUNNING))
        powerscale_module_mock.job_api.update_job_job = MagicMock(
            return_value=None)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.update_job_job.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -------------------------------------------------------------------------
    # U-JB-017: Check mode for start job (no API calls made)
    # -------------------------------------------------------------------------
    def test_check_mode_start(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_type": "TreeDelete",
            "paths": ["/ifs/data"],
            "state": "present"
        })
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOBS_LIST_EMPTY))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.create_job_job.assert_not_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -------------------------------------------------------------------------
    # U-JB-018: Check mode for modify job (no update API call made)
    # -------------------------------------------------------------------------
    def test_check_mode_modify(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_id": 42,
            "job_state": "paused",
            "state": "present"
        })
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_RUNNING))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.update_job_job.assert_not_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -------------------------------------------------------------------------
    # U-JB-019: Diff mode returns before/after diff
    # -------------------------------------------------------------------------
    def test_diff_mode(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_id": 42,
            "priority": 2,
            "state": "present"
        })
        powerscale_module_mock.module._diff = True
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            side_effect=[
                MockSDKResponse(MockJobApi.JOB_RUNNING),
                MockSDKResponse(MockJobApi.JOB_MODIFIED_PRIORITY)
            ])
        powerscale_module_mock.job_api.update_job_job = MagicMock(
            return_value=None)
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        call_kwargs = powerscale_module_mock.module.exit_json.call_args[1]
        assert 'diff' in call_kwargs

    # -------------------------------------------------------------------------
    # U-JB-020: Wait for job completion
    # -------------------------------------------------------------------------
    def test_wait_for_completion(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_type": "TreeDelete",
            "paths": ["/ifs/data/archive"],
            "wait": True,
            "wait_timeout": 30,
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOBS_LIST_EMPTY))
        powerscale_module_mock.job_api.create_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.CREATE_JOB_RESPONSE))
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            side_effect=[
                MockSDKResponse(MockJobApi.JOB_CREATED),
                MockSDKResponse(MockJobApi.JOB_SUCCEEDED)
            ])
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -------------------------------------------------------------------------
    # U-JB-021: Wait for job times out
    # -------------------------------------------------------------------------
    def test_wait_timeout(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_type": "TreeDelete",
            "paths": ["/ifs/data/archive"],
            "wait": True,
            "wait_timeout": 1,
            "wait_interval": 1,
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOBS_LIST_EMPTY))
        powerscale_module_mock.job_api.create_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.CREATE_JOB_RESPONSE))
        # Always returns running - never completes
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_CREATED))
        self.capture_fail_json_call(
            MockJobApi.wait_timeout_msg(), invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JB-022: Cancel a completed job should fail
    # -------------------------------------------------------------------------
    def test_cancel_completed_job(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_id": 42,
            "job_state": "cancelled",
            "state": "present"
        })
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_SUCCEEDED))
        self.capture_fail_json_call(
            MockJobApi.cancel_completed_job_msg(), invoke_perform_module=True)

    # =========================================================================
    # Edge Cases
    # =========================================================================

    # -------------------------------------------------------------------------
    # U-JB-E01: Start job without required paths
    # -------------------------------------------------------------------------
    def test_start_job_missing_paths(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_type": "TreeDelete",
            "paths": None,
            "state": "present"
        })
        self.capture_fail_json_call(
            MockJobApi.missing_paths_error_msg(), invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JB-E02: Modify job with no job_id and no job_type
    # -------------------------------------------------------------------------
    def test_modify_job_none_job_id(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_id": None,
            "job_type": None,
            "job_state": "paused",
            "state": "present"
        })
        self.capture_fail_json_call(
            MockJobApi.none_job_id_error_msg(), invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JB-E03: Start job with empty paths list
    # -------------------------------------------------------------------------
    def test_start_job_empty_paths_list(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_type": "TreeDelete",
            "paths": [],
            "state": "present"
        })
        self.capture_fail_json_call(
            MockJobApi.missing_paths_error_msg(), invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JB-E04: Start job with minimum priority boundary (1)
    # -------------------------------------------------------------------------
    def test_start_job_min_priority(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_type": "TreeDelete",
            "paths": ["/ifs"],
            "priority": 1,
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOBS_LIST_EMPTY))
        powerscale_module_mock.job_api.create_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.CREATE_JOB_RESPONSE))
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_CREATED))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.create_job_job.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -------------------------------------------------------------------------
    # U-JB-E05: Start job with maximum priority boundary (10)
    # -------------------------------------------------------------------------
    def test_start_job_max_priority(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_type": "TreeDelete",
            "paths": ["/ifs"],
            "priority": 10,
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOBS_LIST_EMPTY))
        powerscale_module_mock.job_api.create_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.CREATE_JOB_RESPONSE))
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_CREATED))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.job_api.create_job_job.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # -------------------------------------------------------------------------
    # U-JB-E06: Wait with zero timeout boundary
    # -------------------------------------------------------------------------
    def test_wait_zero_timeout_boundary(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_type": "TreeDelete",
            "paths": ["/ifs/data/archive"],
            "wait": True,
            "wait_timeout": 0,
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOBS_LIST_EMPTY))
        powerscale_module_mock.job_api.create_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.CREATE_JOB_RESPONSE))
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_CREATED))
        self.capture_fail_json_call(
            MockJobApi.wait_timeout_msg(), invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JB-E07: Cancel a completed job (state=succeeded) should fail
    # -------------------------------------------------------------------------
    def test_cancel_completed_job_fail(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_id": 42,
            "job_state": "cancelled",
            "state": "present"
        })
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_SUCCEEDED))
        self.capture_fail_json_call(
            MockJobApi.cancel_completed_job_msg(), invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JB-E08: Start job with invalid type triggers SDK error
    # -------------------------------------------------------------------------
    def test_start_invalid_job_type_error(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_type": "NonExistent",
            "paths": ["/ifs"],
            "state": "present"
        })
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOBS_LIST_EMPTY))
        powerscale_module_mock.job_api.create_job_job = MagicMock(
            side_effect=MockApiException(status=400, body="Invalid job type"))
        self.capture_fail_json_call(
            MockJobApi.start_job_failed_msg(), invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JB-E09: Start job with negative priority should fail validation
    # -------------------------------------------------------------------------
    def test_start_job_negative_priority(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_type": "TreeDelete",
            "paths": ["/ifs"],
            "priority": -1,
            "state": "present"
        })
        self.capture_fail_json_call(
            MockJobApi.negative_priority_error_msg(), invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JB-E10: Pause a completed job should fail
    # -------------------------------------------------------------------------
    def test_pause_wrong_state_completed(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_id": 42,
            "job_state": "paused",
            "state": "present"
        })
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_SUCCEEDED))
        self.capture_fail_json_call(
            MockJobApi.wrong_state_error_msg(), invoke_perform_module=True)

    # -------------------------------------------------------------------------
    # U-JB-E11: Resume a cancelled job should fail
    # -------------------------------------------------------------------------
    def test_resume_wrong_state_cancelled(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "job_id": 42,
            "job_state": "running",
            "state": "present"
        })
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.JOB_CANCELLED))
        self.capture_fail_json_call(
            MockJobApi.wrong_state_error_msg(), invoke_perform_module=True)
