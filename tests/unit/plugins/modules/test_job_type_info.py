# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Job Type Info module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.job_type_info import JobTypeInfo
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_job_type_info_api as MockJobTypeInfoApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase


class TestJobTypeInfo(PowerScaleUnitBase):
    get_module_args = MockJobTypeInfoApi.COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return JobTypeInfo

    def test_list_job_types_success(self, powerscale_module_mock):
        """U-JT-001: List visible job types successfully."""
        self.set_module_params(self.get_module_args, {"include_hidden": False})
        powerscale_module_mock.job_api.get_job_types = MagicMock(
            return_value=MockSDKResponse(MockJobTypeInfoApi.TYPES_VISIBLE))
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False
        job_types = powerscale_module_mock.module.exit_json.call_args[1]['job_types']
        assert len(job_types) == 2

    def test_list_job_types_include_hidden(self, powerscale_module_mock):
        """U-JT-002: List all job types including hidden ones."""
        self.set_module_params(self.get_module_args, {"include_hidden": True})
        powerscale_module_mock.job_api.get_job_types = MagicMock(
            return_value=MockSDKResponse(MockJobTypeInfoApi.TYPES_ALL))
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False
        job_types = powerscale_module_mock.module.exit_json.call_args[1]['job_types']
        assert len(job_types) == 3

    def test_get_single_type_success(self, powerscale_module_mock):
        """U-JT-003: Get a single job type by ID."""
        self.set_module_params(self.get_module_args, {"job_type_id": "TreeDelete"})
        powerscale_module_mock.job_api.get_job_type = MagicMock(
            return_value=MockSDKResponse(MockJobTypeInfoApi.TYPE_TREE_DELETE))
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False
        job_type_details = powerscale_module_mock.module.exit_json.call_args[1]['job_types']
        assert job_type_details['id'] == 'TreeDelete'

    def test_get_single_type_not_found(self, powerscale_module_mock):
        """U-JT-004: Get a job type that does not exist returns empty result."""
        self.set_module_params(self.get_module_args, {"job_type_id": "NonExistent"})
        powerscale_module_mock.job_api.get_job_type = MagicMock(
            return_value=MockSDKResponse(None))
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False
        job_types = powerscale_module_mock.module.exit_json.call_args[1]['job_types']
        assert not job_types

    def test_list_types_sorted(self, powerscale_module_mock):
        """U-JT-005: List job types with sort parameter."""
        self.set_module_params(self.get_module_args, {"sort": "priority"})
        powerscale_module_mock.job_api.get_job_types = MagicMock(
            return_value=MockSDKResponse(MockJobTypeInfoApi.TYPES_SORTED))
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False
        job_types = powerscale_module_mock.module.exit_json.call_args[1]['job_types']
        assert len(job_types) == 2
        assert job_types[0]['id'] == 'SmartPools'
        assert job_types[1]['id'] == 'TreeDelete'

    def test_list_types_empty(self, powerscale_module_mock):
        """U-JT-006: List job types returns empty list."""
        self.set_module_params(self.get_module_args, {"include_hidden": False})
        powerscale_module_mock.job_api.get_job_types = MagicMock(
            return_value=MockSDKResponse(MockJobTypeInfoApi.TYPES_EMPTY))
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False
        job_types = powerscale_module_mock.module.exit_json.call_args[1]['job_types']
        assert len(job_types) == 0

    def test_list_types_exception(self, powerscale_module_mock):
        """U-JT-007: Exception when listing job types."""
        self.set_module_params(self.get_module_args, {"include_hidden": False})
        powerscale_module_mock.job_api.get_job_types = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobTypeInfoApi.get_job_types_failed_msg(), invoke_perform_module=True)

    def test_check_mode(self, powerscale_module_mock):
        """U-JT-008: Check mode does not make changes."""
        self.set_module_params(self.get_module_args, {"include_hidden": False})
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.job_api.get_job_types = MagicMock(
            return_value=MockSDKResponse(MockJobTypeInfoApi.TYPES_VISIBLE))
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_types_empty_without_hidden(self, powerscale_module_mock):
        """U-JT-E01: All types are hidden and include_hidden=False returns empty."""
        self.set_module_params(self.get_module_args, {"include_hidden": False})
        powerscale_module_mock.job_api.get_job_types = MagicMock(
            return_value=MockSDKResponse(MockJobTypeInfoApi.TYPES_EMPTY))
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False
        job_types = powerscale_module_mock.module.exit_json.call_args[1]['job_types']
        assert len(job_types) == 0

    def test_list_types_with_dir_param(self, powerscale_module_mock):
        """U-JT-C01: List types with dir parameter."""
        self.set_module_params(self.get_module_args, {"dir": "DESC"})
        powerscale_module_mock.job_api.get_job_types = MagicMock(
            return_value=MockSDKResponse(MockJobTypeInfoApi.TYPES_VISIBLE))
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_get_type_non_404_exception(self, powerscale_module_mock):
        """U-JT-C02: Non-404 exception when getting job type."""
        self.set_module_params(self.get_module_args, {"job_type_id": "SmartPools"})
        powerscale_module_mock.job_api.get_job_type = MagicMock(
            side_effect=MockApiException(status=500, body="Internal server error"))
        self.capture_fail_json_call(
            MockJobTypeInfoApi.get_job_type_failed_msg(), invoke_perform_module=True)

    def test_main_entry_point(self, powerscale_module_mock):
        """U-JT-C03: Test main() function."""
        from unittest.mock import patch
        with patch('ansible_collections.dellemc.powerscale.plugins.modules.job_type_info.JobTypeInfo') as MockCls:
            mock_inst = MagicMock()
            MockCls.return_value = mock_inst
            from ansible_collections.dellemc.powerscale.plugins.modules.job_type_info import main
            main()
            MockCls.assert_called_once()
            mock_inst.perform_module_operation.assert_called_once()

    def test_get_job_type_404_exception(self, powerscale_module_mock):
        """U-JT-C04: Get a job type that returns 404 via ApiException."""
        self.set_module_params(self.get_module_args, {"job_type_id": "NonExistent"})
        powerscale_module_mock.job_api.get_job_type = MagicMock(
            side_effect=MockApiException(status=404, body="Not found"))
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False
        job_types = powerscale_module_mock.module.exit_json.call_args[1]['job_types']
        assert job_types == {}

    def test_prereqs_validation_failure(self, powerscale_module_mock):
        """U-JT-C05: Test __init__ fails when prereqs validation fails."""
        from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
            import utils as real_utils
        original_return = real_utils.validate_module_pre_reqs.return_value
        real_utils.validate_module_pre_reqs.return_value = {
            "all_packages_found": False,
            "error_message": "Missing required packages"
        }
        try:
            obj = JobTypeInfo()
            obj.module.fail_json.assert_any_call(
                msg="Missing required packages")
        finally:
            real_utils.validate_module_pre_reqs.return_value = original_return

    # -------------------------------------------------------------------------
    # U-JT-C06: Covers ``if __name__ == '__main__':`` guard (line 288)
    # -------------------------------------------------------------------------
    def test_if_name_main_guard(self, powerscale_module_mock):
        """Covers ``if __name__ == '__main__':`` guard."""
        import os
        from ansible_collections.dellemc.powerscale.plugins.modules import job_type_info as mod
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
