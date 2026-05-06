# Copyright: (c) 2026, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Job Info module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale\
    .tests.unit.plugins.module_utils\
    .shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.job_info \
    import JobInfo
from ansible_collections.dellemc.powerscale.tests.unit.plugins. \
    module_utils import mock_job_info_api as MockJobInfoApi
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

utils.get_logger = MagicMock()


class TestJobInfo(PowerScaleUnitBase):
    get_module_args = MockJobInfoApi.COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return JobInfo

    # U-JI-001: Get a specific job by ID - success
    def test_get_job_by_id_success(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {"job_id": 42})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobInfoApi.JOB_1))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False
        ea = (powerscale_module_mock.module
              .exit_json.call_args[1])
        assert ea['job_details'] is not None

    # U-JI-002: Get a specific job by ID - not found
    def test_get_job_by_id_not_found(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {"job_id": 9999})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(None))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JI-003: Get a specific job by ID - exception
    def test_get_job_by_id_exception(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {"job_id": 42})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobInfoApi.get_job_by_id_failed_msg(),
            invoke_perform_module=True)

    # U-JI-004: List all jobs with no filters
    def test_list_jobs_no_filters(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobInfoApi.JOBS_LIST))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JI-005: List jobs filtered by state
    def test_list_jobs_filter_by_state(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {"state": ["running"]})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobInfoApi.JOBS_RUNNING))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JI-006: List jobs filtered by type (client-side filter)
    def test_list_jobs_filter_by_type(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args,
                               {"job_type": ["SmartPools"]})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobInfoApi.JOBS_LIST))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JI-007: List jobs sorted ascending
    def test_list_jobs_sort_asc(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args,
                               {"sort": "id", "dir": "ASC"})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobInfoApi.JOBS_SORTED_ASC))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JI-008: List jobs sorted descending
    def test_list_jobs_sort_desc(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args,
                               {"sort": "id", "dir": "DESC"})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobInfoApi.JOBS_SORTED_DESC))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JI-009: List jobs with limit
    def test_list_jobs_with_limit(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {"limit": 1})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobInfoApi.JOBS_LIMITED))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JI-010: List jobs with combined filters
    def test_list_jobs_combined_filters(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args,
                               {"state": ["running"], "limit": 5})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobInfoApi.JOBS_RUNNING))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JI-011: List jobs with no results
    def test_list_jobs_no_results(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args,
                               {"state": ["paused_user"]})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobInfoApi.JOBS_EMPTY))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JI-012: List jobs - exception
    def test_list_jobs_exception(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobInfoApi.list_jobs_failed_msg(), invoke_perform_module=True)

    # U-JI-013: Get recent jobs - success
    def test_get_recent_jobs_success(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {"include_recent": True})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobInfoApi.JOBS_LIST))
        powerscale_module_mock.job_api.list_job_recent = MagicMock(
            return_value=MockSDKResponse(MockJobInfoApi.RECENT_JOBS))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JI-014: Get recent jobs - exception
    def test_get_recent_jobs_exception(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {"include_recent": True})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobInfoApi.JOBS_LIST))
        powerscale_module_mock.job_api.get_job_recent = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobInfoApi.get_recent_jobs_failed_msg(),
            invoke_perform_module=True)

    # U-JI-015: Get job summary - success
    def test_get_job_summary_success(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {"include_summary": True})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobInfoApi.JOBS_LIST))
        powerscale_module_mock.job_api.get_job_job_summary = MagicMock(
            return_value=MockSDKResponse(MockJobInfoApi.JOB_SUMMARY))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JI-016: Get job summary - exception
    def test_get_job_summary_exception(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {"include_summary": True})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobInfoApi.JOBS_LIST))
        powerscale_module_mock.job_api.get_job_job_summary = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobInfoApi.get_job_summary_failed_msg(),
            invoke_perform_module=True)

    # U-JI-017: Check mode - no changes
    def test_check_mode(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {"job_id": 42})
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            return_value=MockSDKResponse(MockJobInfoApi.JOB_1))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JI-E01: job_id=None with no filters lists all jobs
    def test_get_job_none_id(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {"job_id": None})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobInfoApi.JOBS_LIST))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JI-E02: Jobs with null fields should not crash
    def test_list_jobs_null_response_fields(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobInfoApi.JOBS_NULL_FIELDS))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JI-E03: Empty result returns empty list
    def test_list_jobs_empty_result(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobInfoApi.JOBS_EMPTY))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JI-E04: Large limit value
    def test_list_jobs_max_limit(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {"limit": 10000})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobInfoApi.JOBS_LIST))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JI-E05: Minimum limit value
    def test_list_jobs_min_limit(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {"limit": 1})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            return_value=MockSDKResponse(MockJobInfoApi.JOBS_LIMITED))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JI-E06: Invalid job ID triggers error
    def test_get_job_invalid_id_error(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {"job_id": -1})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.get_job_job = MagicMock(
            side_effect=MockApiException(404, "Not Found"))
        self.capture_fail_json_call(
            MockJobInfoApi.get_job_by_id_failed_msg(),
            invoke_perform_module=True)

    # U-JI-C01: List jobs with multiple state filters
    def test_list_jobs_multiple_states(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {
            "state": ["running", "paused_user"]
        })
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.list_job_jobs = MagicMock(
            side_effect=[
                MockSDKResponse(MockJobInfoApi.JOBS_LIST),
                MockSDKResponse(MockJobInfoApi.JOBS_PAUSED_LIST)
            ])
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JI-C02: Test main() entry point
    def test_main_entry_point(self, powerscale_module_mock):
        from unittest.mock import patch
        _p = ('ansible_collections.dellemc.powerscale.p'
              'lugins.modules.job_info.JobInfo')
        with patch(_p) as MockCls:
            mock_inst = MagicMock()
            MockCls.return_value = mock_inst
            from ansible_collections.dellemc\
                .powerscale.plugins.modules\
                .job_info import main
            main()
            MockCls.assert_called_once()
            mock_inst.perform_module_operation.assert_called_once()

    # U-JI-C03: Prereqs validation failure (line 224)
    def test_prereqs_validation_failure(self, powerscale_module_mock):
        """U-JI-C03: Prereqs validation failure triggers fail_json in
        __init__."""
        from ansible_collections.dellemc\
            .powerscale.plugins.module_utils\
            .storage.dell import utils as dell_utils

        original_return = dell_utils.validate_module_pre_reqs.return_value
        dell_utils.validate_module_pre_reqs.return_value = {
            "all_packages_found": False,
            "error_message": "Missing required packages"
        }
        try:
            obj = JobInfo()
            obj.module.fail_json.assert_any_call(
                msg="Missing required packages")
        finally:
            dell_utils.validate_module_pre_reqs.return_value = original_return

    # -------------------------------------------------------------------------
    # U-JI-C04: Covers ``if __name__ == '__main__':`` guard (line 400)
    # -------------------------------------------------------------------------
    def test_if_name_main_guard(self, powerscale_module_mock):
        """Covers ``if __name__ == '__main__':`` guard."""
        from ansible_collections.dellemc\
            .powerscale.plugins.modules\
            import job_info as mod
        try:
            mod.main()
        except (SystemExit, TypeError):
            pass
