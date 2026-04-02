# Copyright: (c) 2024, Dell Technologies

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
from ansible_collections.dellemc.powerscale.plugins.modules.job import JobHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_job_api \
    import MockJobApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response import (
    MockSDKResponse,
)


class TestJob(PowerScaleUnitBase):
    """TestJob definition."""
    job_args = MockJobApi.JOB_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        """Module object."""
        return Job

    # U-JOB-001: CREATE - Start a new job by type
    def test_create_job(self, powerscale_module_mock):
        """Test create job."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.CREATE_JOB_ARGS)
        powerscale_module_mock.job_api.create_job_job = MagicMock(
            return_value=MagicMock(id=12345))
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.GET_JOB_RESPONSE))
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.job_api.create_job_job.assert_called()

    # U-JOB-002: CREATE - Start job with impact policy
    def test_create_job_with_policy(self, powerscale_module_mock):
        """Test create job with policy."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.CREATE_JOB_WITH_POLICY_ARGS)
        powerscale_module_mock.job_api.create_job_job = MagicMock(
            return_value=MagicMock(id=12345))
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.GET_JOB_RESPONSE))
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.job_api.create_job_job.assert_called()

    # U-JOB-003: CREATE - Start job with priority
    def test_create_job_with_priority(self, powerscale_module_mock):
        """Test create job with priority."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.CREATE_JOB_WITH_PRIORITY_ARGS)
        powerscale_module_mock.job_api.create_job_job = MagicMock(
            return_value=MagicMock(id=12345))
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.GET_JOB_RESPONSE))
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.job_api.create_job_job.assert_called()

    # U-JOB-004: CREATE - Handle ApiException on job creation
    def test_create_job_exception(self, powerscale_module_mock):
        """Test create job exception."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.CREATE_JOB_ARGS)
        powerscale_module_mock.job_api.create_job_job = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobApi.get_job_exception_response('create_exception'),
            JobHandler)

    # U-JOB-005: CHECK MODE - Skip create, report changed
    def test_create_job_check_mode(self, powerscale_module_mock):
        """Test create job check mode."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.CREATE_JOB_ARGS)
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.job_api.create_job_job = MagicMock()
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.job_api.create_job_job.assert_not_called()

    # U-JOB-006: GET - Retrieve job details by ID
    def test_get_job_details(self, powerscale_module_mock):
        """Test get job details."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GET_JOB_DETAILS_ARGS)
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobApi.GET_JOB_RESPONSE))
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.job_api.get_job_job.assert_called()

    # U-JOB-007: GET - Handle ApiException on job get
    def test_get_job_details_exception(self, powerscale_module_mock):
        """Test get job details exception."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GET_JOB_DETAILS_ARGS)
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobApi.get_job_exception_response('get_exception'),
            JobHandler)

    # U-JOB-008: GET - Handle 404 for non-existent job
    def test_get_job_details_not_found(self, powerscale_module_mock):
        """Test get job details not found."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, {"job_id": 99999, "state": "present"})
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            side_effect=MockApiException(status=404, body="Job not found"))
        self.capture_fail_json_call(
            MockJobApi.get_job_exception_response('get_exception'),
            JobHandler)

    # U-JOB-009: MODIFY - Pause a running job
    def test_modify_job_pause(self, powerscale_module_mock):
        """Test modify job pause."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.MODIFY_JOB_PAUSE_ARGS)
        powerscale_module_mock.get_job_details = MagicMock(
            return_value=MockJobApi.GET_JOB_RESPONSE)
        powerscale_module_mock.job_api.update_job_job = MagicMock(return_value=None)
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.job_api.update_job_job.assert_called()

    # U-JOB-010: MODIFY - Resume a paused job
    def test_modify_job_resume(self, powerscale_module_mock):
        """Test modify job resume."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.MODIFY_JOB_RESUME_ARGS)
        powerscale_module_mock.get_job_details = MagicMock(
            return_value=MockJobApi.GET_JOB_PAUSED_RESPONSE)
        powerscale_module_mock.job_api.update_job_job = MagicMock(return_value=None)
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.job_api.update_job_job.assert_called()

    # U-JOB-011: MODIFY - Cancel a running job
    def test_modify_job_cancel(self, powerscale_module_mock):
        """Test modify job cancel."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.MODIFY_JOB_CANCEL_ARGS)
        powerscale_module_mock.get_job_details = MagicMock(
            return_value=MockJobApi.GET_JOB_RESPONSE)
        powerscale_module_mock.job_api.update_job_job = MagicMock(return_value=None)
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.job_api.update_job_job.assert_called()

    # U-JOB-012: MODIFY - Handle ApiException on job modify
    def test_modify_job_exception(self, powerscale_module_mock):
        """Test modify job exception."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.MODIFY_JOB_PAUSE_ARGS)
        powerscale_module_mock.get_job_details = MagicMock(
            return_value=MockJobApi.GET_JOB_RESPONSE)
        powerscale_module_mock.job_api.update_job_job = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobApi.get_job_exception_response('modify_exception'),
            JobHandler)

    # U-JOB-013: IDEMPOTENCY - No change when already in desired state
    def test_modify_job_idempotent_same_state(self, powerscale_module_mock):
        """Test modify job idempotent same state."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, {"job_id": 12345, "job_state": "run", "state": "present"})
        powerscale_module_mock.get_job_details = MagicMock(
            return_value=MockJobApi.GET_JOB_RESPONSE)
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # U-JOB-014: CHECK MODE - Skip modify, report changed
    def test_modify_job_check_mode(self, powerscale_module_mock):
        """Test modify job check mode."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.MODIFY_JOB_PAUSE_ARGS)
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.get_job_details = MagicMock(
            return_value=MockJobApi.GET_JOB_RESPONSE)
        powerscale_module_mock.job_api.update_job_job = MagicMock()
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.job_api.update_job_job.assert_not_called()

    # U-JOB-015: DIFF MODE - Capture before/after job state
    def test_modify_job_diff_mode(self, powerscale_module_mock):
        """Test modify job diff mode."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.MODIFY_JOB_PAUSE_ARGS)
        powerscale_module_mock.module._diff = True
        powerscale_module_mock.get_job_details = MagicMock(
            return_value=MockJobApi.GET_JOB_RESPONSE)
        powerscale_module_mock.job_api.update_job_job = MagicMock(return_value=None)
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        call_args = powerscale_module_mock.module.exit_json.call_args[1]
        assert call_args['changed'] is True
        assert 'diff' in call_args
        assert 'before' in call_args['diff']
        assert 'after' in call_args['diff']

    # U-JOB-016: LIST - List all jobs
    def test_list_jobs(self, powerscale_module_mock):
        """Test list jobs."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GATHER_JOBS_ARGS)
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobApi.LIST_JOBS_RESPONSE))
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.job_api.list_job_jobs.assert_called()

    # U-JOB-017: LIST - Filter jobs by state
    def test_list_jobs_with_filter_state(self, powerscale_module_mock):
        """Test list jobs with filter state."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.LIST_JOBS_FILTERED_ARGS)
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobApi.LIST_JOBS_RESPONSE))
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.job_api.list_job_jobs.assert_called()

    # U-JOB-018: LIST - Sort and limit job list
    def test_list_jobs_with_sort_and_limit(self, powerscale_module_mock):
        """Test list jobs with sort and limit."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.LIST_JOBS_SORTED_ARGS)
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobApi.LIST_JOBS_RESPONSE))
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.job_api.list_job_jobs.assert_called()

    # U-JOB-019: LIST - Handle exception on list
    def test_list_jobs_exception(self, powerscale_module_mock):
        """Test list jobs exception."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GATHER_JOBS_ARGS)
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobApi.get_job_exception_response('list_exception'),
            JobHandler)

    # U-JOB-020: GATHER - View job events
    def test_gather_events(self, powerscale_module_mock):
        """Test gather events."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GATHER_EVENTS_ARGS)
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            return_value=MockSDKResponse(MockJobApi.GET_EVENTS_RESPONSE))
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.job_api.get_job_events.assert_called()

    # U-JOB-021: GATHER - View events with filters
    def test_gather_events_with_filters(self, powerscale_module_mock):
        """Test gather events with filters."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GATHER_EVENTS_FILTERED_ARGS)
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            return_value=MockSDKResponse(MockJobApi.GET_EVENTS_RESPONSE))
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.job_api.get_job_events.assert_called()

    # U-JOB-022: GATHER - Handle exception on events
    def test_gather_events_exception(self, powerscale_module_mock):
        """Test gather events exception."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GATHER_EVENTS_ARGS)
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobApi.get_job_exception_response('events_exception'),
            JobHandler)

    # U-JOB-023: GATHER - View job reports
    def test_gather_reports(self, powerscale_module_mock):
        """Test gather reports."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GATHER_REPORTS_ARGS)
        powerscale_module_mock.job_api.get_job_reports = MagicMock(
            return_value=MockSDKResponse(MockJobApi.GET_REPORTS_RESPONSE))
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.job_api.get_job_reports.assert_called()

    # U-JOB-024: GATHER - Handle exception on reports
    def test_gather_reports_exception(self, powerscale_module_mock):
        """Test gather reports exception."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GATHER_REPORTS_ARGS)
        powerscale_module_mock.job_api.get_job_reports = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobApi.get_job_exception_response('reports_exception'),
            JobHandler)

    # U-JOB-025: GATHER - View job types
    def test_gather_types(self, powerscale_module_mock):
        """Test gather types."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GATHER_TYPES_ARGS)
        powerscale_module_mock.job_api.get_job_types = MagicMock(
            return_value=MockSDKResponse(MockJobApi.GET_TYPES_RESPONSE))
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.job_api.get_job_types.assert_called()

    # U-JOB-026: GATHER - View all job types including hidden
    def test_gather_types_show_all(self, powerscale_module_mock):
        """Test gather types show all."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GATHER_TYPES_SHOW_ALL_ARGS)
        powerscale_module_mock.job_api.get_job_types = MagicMock(
            return_value=MockSDKResponse(MockJobApi.GET_TYPES_RESPONSE))
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.job_api.get_job_types.assert_called()

    # U-JOB-027: GATHER - Handle exception on types
    def test_gather_types_exception(self, powerscale_module_mock):
        """Test gather types exception."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GATHER_TYPES_ARGS)
        powerscale_module_mock.job_api.get_job_types = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobApi.get_job_exception_response('types_exception'),
            JobHandler)

    # U-JOB-028: GATHER - View job statistics
    def test_gather_statistics(self, powerscale_module_mock):
        """Test gather statistics."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GATHER_STATISTICS_ARGS)
        powerscale_module_mock.job_api.get_job_statistics = MagicMock(
            return_value=MockSDKResponse(MockJobApi.GET_STATISTICS_RESPONSE))
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.job_api.get_job_statistics.assert_called()

    # U-JOB-029: GATHER - Handle exception on statistics
    def test_gather_statistics_exception(self, powerscale_module_mock):
        """Test gather statistics exception."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GATHER_STATISTICS_ARGS)
        powerscale_module_mock.job_api.get_job_statistics = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobApi.get_job_exception_response('statistics_exception'),
            JobHandler)

    # U-JOB-030: GATHER - View recently completed jobs
    def test_gather_recent(self, powerscale_module_mock):
        """Test gather recent."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GATHER_RECENT_ARGS)
        powerscale_module_mock.job_api.get_job_recent = MagicMock(
            return_value=MockSDKResponse(MockJobApi.GET_RECENT_RESPONSE))
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.job_api.get_job_recent.assert_called()

    # U-JOB-031: GATHER - View recent jobs with limit
    def test_gather_recent_with_limit(self, powerscale_module_mock):
        """Test gather recent with limit."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GATHER_RECENT_WITH_LIMIT_ARGS)
        powerscale_module_mock.job_api.get_job_recent = MagicMock(
            return_value=MockSDKResponse(MockJobApi.GET_RECENT_RESPONSE))
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.job_api.get_job_recent.assert_called()

    # U-JOB-032: GATHER - Handle exception on recent
    def test_gather_recent_exception(self, powerscale_module_mock):
        """Test gather recent exception."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GATHER_RECENT_ARGS)
        powerscale_module_mock.job_api.get_job_recent = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobApi.get_job_exception_response('recent_exception'),
            JobHandler)

    # U-JOB-033: GATHER - View job summary
    def test_gather_summary(self, powerscale_module_mock):
        """Test gather summary."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GATHER_SUMMARY_ARGS)
        powerscale_module_mock.job_api.get_job_job_summary = MagicMock(
            return_value=MockSDKResponse(MockJobApi.GET_SUMMARY_RESPONSE))
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.job_api.get_job_job_summary.assert_called()

    # U-JOB-034: GATHER - Handle exception on summary
    def test_gather_summary_exception(self, powerscale_module_mock):
        """Test gather summary exception."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GATHER_SUMMARY_ARGS)
        powerscale_module_mock.job_api.get_job_job_summary = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobApi.get_job_exception_response('summary_exception'),
            JobHandler)

    # U-JOB-035: GATHER - Gather multiple subsets at once
    def test_gather_multiple_subsets(self, powerscale_module_mock):
        """Test gather multiple subsets."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GATHER_MULTIPLE_ARGS)
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobApi.LIST_JOBS_RESPONSE))
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            return_value=MockSDKResponse(MockJobApi.GET_EVENTS_RESPONSE))
        powerscale_module_mock.job_api.get_job_types = MagicMock(
            return_value=MockSDKResponse(MockJobApi.GET_TYPES_RESPONSE))
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.job_api.list_job_jobs.assert_called()
        powerscale_module_mock.job_api.get_job_events.assert_called()
        powerscale_module_mock.job_api.get_job_types.assert_called()

    # U-JOB-036: GATHER - Read-only operations always report changed=False
    def test_gather_subset_changed_false(self, powerscale_module_mock):
        """Test gather subset changed false."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GATHER_JOBS_ARGS)
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobApi.LIST_JOBS_RESPONSE))
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # U-JOB-037: NULL CHECK - job_type required for create
    def test_validate_job_type_null_for_create(self, powerscale_module_mock):
        """Test validate job type null for create."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, {"state": "present", "job_type": None, "job_id": None})
        self.capture_fail_json_call(
            MockJobApi.get_job_exception_response('job_type_required'),
            JobHandler)

    # U-JOB-038: NULL CHECK - job_id required for modify
    def test_validate_job_id_null_for_modify(self, powerscale_module_mock):
        """Test validate job id null for modify."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, {"state": "present", "job_state": "pause", "job_id": None})
        self.capture_fail_json_call(
            MockJobApi.get_job_exception_response('job_id_required'),
            JobHandler)

    # U-JOB-039: NEGATIVE - Negative limit value
    def test_validate_limit_negative(self, powerscale_module_mock):
        """Test validate limit negative."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, {"gather_subset": ["jobs"], "limit": -1})
        self.capture_fail_json_call(
            MockJobApi.get_job_exception_response('invalid_limit'),
            JobHandler)

    # U-JOB-040: ERROR CASE - Handle 400 Bad Request on create
    def test_error_handling_400(self, powerscale_module_mock):
        """Test error handling 400."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.CREATE_JOB_ARGS)
        powerscale_module_mock.job_api.create_job_job = MagicMock(
            side_effect=MockApiException(status=400, body="Bad Request"))
        self.capture_fail_json_call(
            MockJobApi.get_job_exception_response('create_exception'),
            JobHandler)

    # U-JOB-041: ERROR CASE - Handle 401 Unauthorized
    def test_error_handling_401(self, powerscale_module_mock):
        """Test error handling 401."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.GET_JOB_DETAILS_ARGS)
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            side_effect=MockApiException(status=401, body="Unauthorized"))
        self.capture_fail_json_call(
            MockJobApi.get_job_exception_response('get_exception'),
            JobHandler)

    # U-JOB-042: ERROR CASE - Handle 403 Forbidden
    def test_error_handling_403(self, powerscale_module_mock):
        """Test error handling 403."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.CREATE_JOB_ARGS)
        powerscale_module_mock.job_api.create_job_job = MagicMock(
            side_effect=MockApiException(status=403, body="Forbidden"))
        self.capture_fail_json_call(
            MockJobApi.get_job_exception_response('create_exception'),
            JobHandler)

    # U-JOB-043: ERROR CASE - Handle 500 Server Error
    def test_error_handling_500(self, powerscale_module_mock):
        """Test error handling 500."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.MODIFY_JOB_PAUSE_ARGS)
        powerscale_module_mock.get_job_details = MagicMock(
            return_value=MockJobApi.GET_JOB_RESPONSE)
        powerscale_module_mock.job_api.update_job_job = MagicMock(
            side_effect=MockApiException(status=500, body="Internal Server Error"))
        self.capture_fail_json_call(
            MockJobApi.get_job_exception_response('modify_exception'),
            JobHandler)

    # U-JOB-044: MODIFY - Change job impact policy
    def test_modify_job_update_policy(self, powerscale_module_mock):
        """Test modify job update policy."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.MODIFY_JOB_POLICY_ARGS)
        powerscale_module_mock.get_job_details = MagicMock(
            return_value=MockJobApi.GET_JOB_RESPONSE)
        powerscale_module_mock.job_api.update_job_job = MagicMock(return_value=None)
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.job_api.update_job_job.assert_called()

    # U-JOB-045: MODIFY - Change job priority
    def test_modify_job_update_priority(self, powerscale_module_mock):
        """Test modify job update priority."""
        self.set_module_params(MockJobApi.JOB_COMMON_ARGS, MockJobApi.MODIFY_JOB_PRIORITY_ARGS)
        powerscale_module_mock.get_job_details = MagicMock(
            return_value=MockJobApi.GET_JOB_RESPONSE)
        powerscale_module_mock.job_api.update_job_job = MagicMock(return_value=None)
        JobHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.job_api.update_job_job.assert_called()
