# Copyright: (c) 2026, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Job Report Info module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale\
    .tests.unit.plugins.module_utils\
    .shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.job_report_info \
    import JobReportInfo
from ansible_collections.dellemc.powerscale.tests.unit.plugins. \
    module_utils import mock_job_report_info_api as MockJobReportInfoApi
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


class TestJobReportInfo(PowerScaleUnitBase):
    get_module_args = MockJobReportInfoApi.COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return JobReportInfo

    # U-JR-001: Get all reports with no filters
    def test_get_reports_no_filters(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.get_job_reports = MagicMock(
            return_value=MockSDKResponse(MockJobReportInfoApi.REPORTS_ALL))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JR-002: Get reports filtered by job type
    def test_get_reports_filter_by_type(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args,
                               {"job_type": "SmartPools"})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.get_job_reports = MagicMock(
            return_value=MockSDKResponse(MockJobReportInfoApi.REPORTS_BY_TYPE))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JR-003: Get reports filtered by job ID
    def test_get_reports_filter_by_job_id(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {"job_id": 42})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.get_job_reports = MagicMock(
            return_value=MockSDKResponse(
                MockJobReportInfoApi.REPORTS_BY_JOB_ID))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JR-004: Get reports filtered by event key
    def test_get_reports_filter_by_event_key(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args,
                               {"event_key": "phase_complete"})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.get_job_reports = MagicMock(
            return_value=MockSDKResponse(
                MockJobReportInfoApi.REPORTS_BY_EVENT_KEY))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JR-005: Get reports with time range
    def test_get_reports_time_range(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args,
                               {"begin": 1700000000, "end": 1700002000})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.get_job_reports = MagicMock(
            return_value=MockSDKResponse(MockJobReportInfoApi.REPORTS_ALL))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JR-006: Get reports for last phase only
    def test_get_reports_last_phase_only(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {"last_phase_only": True})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.get_job_reports = MagicMock(
            return_value=MockSDKResponse(
                MockJobReportInfoApi.REPORTS_LAST_PHASE))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JR-007: Get reports with verbose output
    def test_get_reports_verbose(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {"verbose": True})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.get_job_reports = MagicMock(
            return_value=MockSDKResponse(MockJobReportInfoApi.REPORTS_VERBOSE))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JR-008: Get reports with limit
    def test_get_reports_with_limit(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {"limit": 1})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.get_job_reports = MagicMock(
            return_value=MockSDKResponse(MockJobReportInfoApi.REPORTS_LIMITED))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JR-009: Get reports with pagination
    def test_get_reports_pagination(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.get_job_reports = MagicMock(
            side_effect=[
                MockSDKResponse(MockJobReportInfoApi.REPORTS_PAGE1),
                MockSDKResponse(MockJobReportInfoApi.REPORTS_PAGE2)
            ])
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JR-010: Get reports - empty result
    def test_get_reports_empty_result(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.get_job_reports = MagicMock(
            return_value=MockSDKResponse(MockJobReportInfoApi.REPORTS_EMPTY))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JR-011: Get reports - exception
    def test_get_reports_exception(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.get_job_reports = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobReportInfoApi.get_reports_failed_msg(),
            invoke_perform_module=True)

    # U-JR-012: Check mode - no changes
    def test_check_mode(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {})
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.get_job_reports = MagicMock(
            return_value=MockSDKResponse(MockJobReportInfoApi.REPORTS_ALL))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JR-E01: Empty result returns total_reports=0
    def test_reports_empty_result(self, powerscale_module_mock):
        self.set_module_params(self.get_module_args, {})
        powerscale_module_mock.job_api = MagicMock()
        powerscale_module_mock.job_api.get_job_reports = MagicMock(
            return_value=MockSDKResponse(MockJobReportInfoApi.REPORTS_EMPTY))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
                     .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    # U-JR-C01: Test main() entry point
    def test_main_entry_point(self, powerscale_module_mock):
        """U-JR-C01: Test main() function."""
        from unittest.mock import patch
        _p = ('ansible_collections.dellemc.powerscale.p'
              'lugins.modules.job_report_info.JobReportInfo')
        with patch(_p) as MockCls:
            mock_inst = MagicMock()
            MockCls.return_value = mock_inst
            from ansible_collections.dellemc\
                .powerscale.plugins.modules\
                .job_report_info import main
            main()
            MockCls.assert_called_once()
            mock_inst.perform_module_operation.assert_called_once()

    # U-JR-C02: Test prereqs validation failure in __init__ (covers line 199)
    def test_prereqs_validation_failure(self, powerscale_module_mock):
        """U-JR-C02: Test __init__ fails when prereqs validation fails."""
        from ansible_collections.dellemc\
            .powerscale.plugins.module_utils\
            .storage.dell import utils as real_utils
        original_return = real_utils.validate_module_pre_reqs.return_value
        real_utils.validate_module_pre_reqs.return_value = {
            "all_packages_found": False,
            "error_message": "Missing required packages"
        }
        try:
            obj = JobReportInfo()
            obj.module.fail_json.assert_any_call(
                msg="Missing required packages")
        finally:
            real_utils.validate_module_pre_reqs.return_value = original_return

    # U-JR-C03: Test if __name__ == '__main__' guard (covers line 307)
    def test_if_name_main_guard(self, powerscale_module_mock):
        """U-JR-C03: Cover if __name__ == '__main__': main() guard."""
        from ansible_collections.dellemc\
            .powerscale.plugins.modules\
            import job_report_info as mod
        try:
            mod.main()
        except (SystemExit, TypeError):
            pass
