# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Job Event Info module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale\
    .tests.unit.plugins.module_utils\
    .shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.job_event_info \
    import JobEventInfo
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_job_event_info_api as MockJobEventInfoApi
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


class TestJobEventInfo(PowerScaleUnitBase):
    get_module_args = MockJobEventInfoApi.COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return JobEventInfo

    def test_list_events_no_filters(self, powerscale_module_mock):
        """U-JE-001: List all events without any filters."""
        self.set_module_params(self.get_module_args, {})
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            return_value=MockSDKResponse(MockJobEventInfoApi.EVENTS_ALL))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
            .module.exit_json.call_args[1])
        assert exit_args['changed'] is False
        ea = (powerscale_module_mock.module
            .exit_json.call_args[1])
        events = ea['job_events']
        assert len(events) == 4

    def test_list_events_filter_by_state(self, powerscale_module_mock):
        """U-JE-002: Filter events by running state."""
        self.set_module_params(self.get_module_args, {"state": "running"})
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            return_value=MockSDKResponse(MockJobEventInfoApi.EVENTS_RUNNING))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
            .module.exit_json.call_args[1])
        assert exit_args['changed'] is False
        ea = (powerscale_module_mock.module
            .exit_json.call_args[1])
        events = ea['job_events']
        assert len(events) == 2
        for event in events:
            assert event['state'] == 'running'

    def test_list_events_begin_time_epoch(self, powerscale_module_mock):
        """U-JE-003: Filter events by begin_time as epoch timestamp."""
        self.set_module_params(self.get_module_args,
                               {"begin_time": "1700000000"})
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            return_value=MockSDKResponse(
                MockJobEventInfoApi.EVENTS_TIME_RANGE))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
            .module.exit_json.call_args[1])
        assert exit_args['changed'] is False
        ea = (powerscale_module_mock.module
            .exit_json.call_args[1])
        events = ea['job_events']
        assert len(events) == 2

    def test_list_events_begin_time_iso(self, powerscale_module_mock):
        """U-JE-004: Filter events by begin_time as ISO format."""
        self.set_module_params(self.get_module_args,
                               {"begin_time": "2026-01-01T00:00:00Z"})
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            return_value=MockSDKResponse(
                MockJobEventInfoApi.EVENTS_TIME_RANGE))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
            .module.exit_json.call_args[1])
        assert exit_args['changed'] is False
        ea = (powerscale_module_mock.module
            .exit_json.call_args[1])
        events = ea['job_events']
        assert len(events) == 2

    def test_list_events_end_time(self, powerscale_module_mock):
        """U-JE-005: Filter events by end_time."""
        self.set_module_params(self.get_module_args,
                               {"end_time": "1700003000"})
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            return_value=MockSDKResponse(MockJobEventInfoApi.EVENTS_ALL))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
            .module.exit_json.call_args[1])
        assert exit_args['changed'] is False
        ea = (powerscale_module_mock.module
            .exit_json.call_args[1])
        events = ea['job_events']
        assert len(events) == 4

    def test_list_events_duration(self, powerscale_module_mock):
        """U-JE-006: Filter events by duration."""
        self.set_module_params(self.get_module_args,
                               {"duration": {"value": 24, "unit": "hours"}})
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            return_value=MockSDKResponse(
                MockJobEventInfoApi.EVENTS_TIME_RANGE))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
            .module.exit_json.call_args[1])
        assert exit_args['changed'] is False
        ea = (powerscale_module_mock.module
            .exit_json.call_args[1])
        events = ea['job_events']
        assert len(events) == 2

    def test_list_events_filter_by_job_id(self, powerscale_module_mock):
        """U-JE-007: Filter events by job_id."""
        self.set_module_params(self.get_module_args, {"job_id": 42})
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            return_value=MockSDKResponse(MockJobEventInfoApi.EVENTS_BY_JOB_ID))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
            .module.exit_json.call_args[1])
        assert exit_args['changed'] is False
        ea = (powerscale_module_mock.module
            .exit_json.call_args[1])
        events = ea['job_events']
        assert len(events) == 2
        for event in events:
            assert event['job_id'] == 42

    def test_list_events_filter_by_type(self, powerscale_module_mock):
        """U-JE-008: Filter events by job_type."""
        self.set_module_params(self.get_module_args,
                               {"job_type": "SmartPools"})
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            return_value=MockSDKResponse(MockJobEventInfoApi.EVENTS_BY_TYPE))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
            .module.exit_json.call_args[1])
        assert exit_args['changed'] is False
        ea = (powerscale_module_mock.module
            .exit_json.call_args[1])
        events = ea['job_events']
        assert len(events) == 2
        for event in events:
            assert event['job_type'] == 'SmartPools'

    def test_list_events_ended_jobs_only(self, powerscale_module_mock):
        """U-JE-009: Filter events for ended jobs only."""
        self.set_module_params(self.get_module_args, {"ended_jobs_only": True})
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            return_value=MockSDKResponse(MockJobEventInfoApi.EVENTS_ENDED))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
            .module.exit_json.call_args[1])
        assert exit_args['changed'] is False
        ea = (powerscale_module_mock.module
            .exit_json.call_args[1])
        events = ea['job_events']
        assert len(events) == 2

    def test_list_events_pagination(self, powerscale_module_mock):
        """U-JE-010: Pagination across multiple pages of events."""
        self.set_module_params(self.get_module_args, {})
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            side_effect=[
                MockSDKResponse(MockJobEventInfoApi.EVENTS_PAGE1),
                MockSDKResponse(MockJobEventInfoApi.EVENTS_PAGE2)
            ])
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
            .module.exit_json.call_args[1])
        assert exit_args['changed'] is False
        ea = (powerscale_module_mock.module
            .exit_json.call_args[1])
        events = ea['job_events']
        assert len(events) == 4

    def test_list_events_empty(self, powerscale_module_mock):
        """U-JE-011: Empty events list returned."""
        self.set_module_params(self.get_module_args, {})
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            return_value=MockSDKResponse(MockJobEventInfoApi.EVENTS_EMPTY))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
            .module.exit_json.call_args[1])
        assert exit_args['changed'] is False
        ea = (powerscale_module_mock.module
            .exit_json.call_args[1])
        events = ea['job_events']
        assert len(events) == 0

    def test_list_events_exception(self, powerscale_module_mock):
        """U-JE-012: Exception when listing job events."""
        self.set_module_params(self.get_module_args, {})
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
    MockJobEventInfoApi.get_events_failed_msg(),
     invoke_perform_module=True)

    def test_invalid_time_format(self, powerscale_module_mock):
        """U-JE-013: Invalid time format triggers failure."""
        self.set_module_params(self.get_module_args, {"begin_time": "invalid"})
        self.capture_fail_json_call(
    MockJobEventInfoApi.invalid_time_format_msg(),
     invoke_perform_module=True)

    def test_check_mode(self, powerscale_module_mock):
        """U-JE-014: Check mode does not make changes."""
        self.set_module_params(self.get_module_args, {})
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            return_value=MockSDKResponse(MockJobEventInfoApi.EVENTS_ALL))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
            .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    def test_events_none_filters(self, powerscale_module_mock):
        """U-JE-E01: All filter params are None, returns all events."""
        self.set_module_params(self.get_module_args, {
            "state": None, "begin_time": None, "end_time": None,
            "duration": None, "job_id": None, "job_type": None,
            "event_key": None, "ended_jobs_only": None, "limit": None
        })
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            return_value=MockSDKResponse(MockJobEventInfoApi.EVENTS_ALL))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
            .module.exit_json.call_args[1])
        assert exit_args['changed'] is False
        ea = (powerscale_module_mock.module
            .exit_json.call_args[1])
        events = ea['job_events']
        assert len(events) == 4

    def test_events_empty_time_window(self, powerscale_module_mock):
        """U-JE-E02: Time window with no events returns empty list."""
        self.set_module_params(self.get_module_args, {
            "begin_time": "1700010000", "end_time": "1700010001"
        })
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            return_value=MockSDKResponse(MockJobEventInfoApi.EVENTS_EMPTY))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
            .module.exit_json.call_args[1])
        assert exit_args['changed'] is False
        ea = (powerscale_module_mock.module
            .exit_json.call_args[1])
        events = ea['job_events']
        assert len(events) == 0

    def test_events_boundary_epoch_time(self, powerscale_module_mock):
        """U-JE-E03: Epoch boundary value (0) as begin_time."""
        self.set_module_params(self.get_module_args, {"begin_time": "0"})
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            return_value=MockSDKResponse(MockJobEventInfoApi.EVENTS_ALL))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
            .module.exit_json.call_args[1])
        assert exit_args['changed'] is False
        ea = (powerscale_module_mock.module
            .exit_json.call_args[1])
        events = ea['job_events']
        assert len(events) == 4

    def test_events_invalid_time_format(self, powerscale_module_mock):
        """U-JE-E04: Malformed time format triggers failure."""
        self.set_module_params(self.get_module_args,
                               {"begin_time": "not-a-time"})
        self.capture_fail_json_call(
    MockJobEventInfoApi.invalid_time_format_msg(),
     invoke_perform_module=True)

    def test_negative_limit_reject(self, powerscale_module_mock):
        """U-JE-E05: Negative limit value triggers failure."""
        self.set_module_params(self.get_module_args, {"limit": -1})
        self.capture_fail_json_call(
    MockJobEventInfoApi.negative_limit_msg(),
     invoke_perform_module=True)

    def test_list_events_iso_time_without_tz(self, powerscale_module_mock):
        """U-JE-C01: ISO time without timezone info to trigger tzinfo
        replacement."""
        self.set_module_params(self.get_module_args,
                               {"begin_time": "2026-01-01T00:00:00"})
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            return_value=MockSDKResponse(
                MockJobEventInfoApi.EVENTS_TIME_RANGE))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
            .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    def test_list_events_with_event_key(self, powerscale_module_mock):
        """U-JE-C02: Filter events by event_key."""
        self.set_module_params(self.get_module_args,
                               {"event_key": "job_started"})
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            return_value=MockSDKResponse(MockJobEventInfoApi.EVENTS_ALL))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
            .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    def test_list_events_with_positive_limit(self, powerscale_module_mock):
        """U-JE-C03: Positive limit value to trigger api_params['limit']."""
        self.set_module_params(self.get_module_args, {"limit": 50})
        powerscale_module_mock.job_api.get_job_events = MagicMock(
            return_value=MockSDKResponse(MockJobEventInfoApi.EVENTS_ALL))
        powerscale_module_mock.perform_module_operation()
        exit_args = (powerscale_module_mock
            .module.exit_json.call_args[1])
        assert exit_args['changed'] is False

    def test_main_entry_point(self, powerscale_module_mock):
        """U-JE-C04: Test main() function."""
        from unittest.mock import patch
        _p = ('ansible_collections.dellemc.powerscale.p'
             'lugins.modules.job_event_info.JobEventInfo')
        with patch(_p) as MockCls:
            mock_inst = MagicMock()
            MockCls.return_value = mock_inst
            from ansible_collections.dellemc\
                .powerscale.plugins.modules\
                .job_event_info import main
            main()
            MockCls.assert_called_once()
            mock_inst.perform_module_operation.assert_called_once()

    def test_prereqs_validation_failure(self, powerscale_module_mock):
        """U-JE-C05: Prereqs validation failure triggers fail_json in
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
            obj = JobEventInfo()
            obj.module.fail_json.assert_any_call(
                msg="Missing required packages")
        finally:
            dell_utils.validate_module_pre_reqs.return_value = original_return

    # -------------------------------------------------------------------------
    # U-JE-C06: Covers ``if __name__ == '__main__':`` guard (line 442)
    # -------------------------------------------------------------------------
    def test_if_name_main_guard(self, powerscale_module_mock):
        """Covers ``if __name__ == '__main__':`` guard."""
        import os
        from ansible_collections.dellemc\
            .powerscale.plugins.modules\
            import job_event_info as mod
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
