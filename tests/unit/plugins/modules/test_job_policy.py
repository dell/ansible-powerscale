# Copyright: (c) 2024, Dell Technologies

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
from ansible_collections.dellemc.powerscale.plugins.modules.job_policy import JobPolicyHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_job_policy_api \
    import MockJobPolicyApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response import (
    MockSDKResponse,
)


class TestJobPolicy(PowerScaleUnitBase):
    """TestJobPolicy definition."""
    job_policy_args = MockJobPolicyApi.JOB_POLICY_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        """Module object."""
        return JobPolicy

    # U-JP-001: CREATE - Create a new job impact policy
    def test_create_job_policy(self, powerscale_module_mock):
        """Test create job policy."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, MockJobPolicyApi.CREATE_JOB_POLICY_ARGS)
        powerscale_module_mock.get_job_policy_details = MagicMock(return_value=None)
        powerscale_module_mock.job_api.create_job_policy = MagicMock(
            return_value=MagicMock(id="LOW_IMPACT"))
        JobPolicyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.job_api.create_job_policy.assert_called()

    # U-JP-002: CREATE - Create policy with description
    def test_create_job_policy_with_description(self, powerscale_module_mock):
        """Test create job policy with description."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, MockJobPolicyApi.CREATE_JOB_POLICY_WITH_DESC_ARGS)
        powerscale_module_mock.get_job_policy_details = MagicMock(return_value=None)
        powerscale_module_mock.job_api.create_job_policy = MagicMock(
            return_value=MagicMock(id="NIGHT_OPS"))
        JobPolicyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.job_api.create_job_policy.assert_called()

    # U-JP-003: CREATE - Handle ApiException on create
    def test_create_job_policy_exception(self, powerscale_module_mock):
        """Test create job policy exception."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, MockJobPolicyApi.CREATE_JOB_POLICY_ARGS)
        powerscale_module_mock.get_job_policy_details = MagicMock(return_value=None)
        powerscale_module_mock.job_api.create_job_policy = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobPolicyApi.get_job_policy_exception_response('create_exception'),
            JobPolicyHandler)

    # U-JP-004: CHECK MODE - Skip create, report changed
    def test_create_job_policy_check_mode(self, powerscale_module_mock):
        """Test create job policy check mode."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, MockJobPolicyApi.CREATE_JOB_POLICY_ARGS)
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.get_job_policy_details = MagicMock(return_value=None)
        powerscale_module_mock.job_api.create_job_policy = MagicMock()
        JobPolicyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.job_api.create_job_policy.assert_not_called()

    # U-JP-005: IDEMPOTENCY - No create when policy already exists
    def test_create_job_policy_idempotent(self, powerscale_module_mock):
        """Test create job policy idempotent."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, MockJobPolicyApi.CREATE_JOB_POLICY_ARGS)
        powerscale_module_mock.get_job_policy_details = MagicMock(
            return_value=MockJobPolicyApi.GET_JOB_POLICY_RESPONSE)
        JobPolicyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # U-JP-006: GET - Retrieve policy by name
    def test_get_job_policy_by_name(self, powerscale_module_mock):
        """Test get job policy by name."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, MockJobPolicyApi.GET_JOB_POLICY_ARGS)
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.LIST_JOB_POLICIES_RESPONSE))
        JobPolicyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.job_api.list_job_policies.assert_called()

    # U-JP-007: GET - Retrieve policy by ID
    def test_get_job_policy_by_id(self, powerscale_module_mock):
        """Test get job policy by id."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, MockJobPolicyApi.GET_JOB_POLICY_BY_ID_ARGS)
        powerscale_module_mock.job_api.get_job_policy = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.GET_JOB_POLICY_RESPONSE))
        JobPolicyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.job_api.get_job_policy.assert_called()

    # U-JP-008: GET - Handle ApiException on get
    def test_get_job_policy_exception(self, powerscale_module_mock):
        """Test get job policy exception."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, MockJobPolicyApi.GET_JOB_POLICY_BY_ID_ARGS)
        powerscale_module_mock.job_api.get_job_policy = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobPolicyApi.get_job_policy_exception_response('get_exception'),
            JobPolicyHandler)

    # U-JP-009: GET - Policy not found returns None
    def test_get_job_policy_not_found(self, powerscale_module_mock):
        """Test get job policy not found."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, {"policy_name": "NONEXISTENT", "state": "present"})
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse({"policies": []}))
        powerscale_module_mock.job_api.create_job_policy = MagicMock(
            return_value=MagicMock(id="NONEXISTENT"))
        JobPolicyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # U-JP-010: MODIFY - Update policy intervals
    def test_modify_job_policy_intervals(self, powerscale_module_mock):
        """Test modify job policy intervals."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, MockJobPolicyApi.MODIFY_JOB_POLICY_INTERVALS_ARGS)
        powerscale_module_mock.get_job_policy_details = MagicMock(
            return_value=MockJobPolicyApi.GET_JOB_POLICY_RESPONSE)
        powerscale_module_mock.job_api.update_job_policy = MagicMock(return_value=None)
        JobPolicyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.job_api.update_job_policy.assert_called()

    # U-JP-011: MODIFY - Update policy description
    def test_modify_job_policy_description(self, powerscale_module_mock):
        """Test modify job policy description."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, MockJobPolicyApi.MODIFY_JOB_POLICY_DESC_ARGS)
        powerscale_module_mock.get_job_policy_details = MagicMock(
            return_value=MockJobPolicyApi.GET_JOB_POLICY_RESPONSE)
        powerscale_module_mock.job_api.update_job_policy = MagicMock(return_value=None)
        JobPolicyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.job_api.update_job_policy.assert_called()

    # U-JP-012: MODIFY - Handle ApiException on modify
    def test_modify_job_policy_exception(self, powerscale_module_mock):
        """Test modify job policy exception."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, MockJobPolicyApi.MODIFY_JOB_POLICY_INTERVALS_ARGS)
        powerscale_module_mock.get_job_policy_details = MagicMock(
            return_value=MockJobPolicyApi.GET_JOB_POLICY_RESPONSE)
        powerscale_module_mock.job_api.update_job_policy = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobPolicyApi.get_job_policy_exception_response('modify_exception'),
            JobPolicyHandler)

    # U-JP-013: IDEMPOTENCY - No change when intervals match
    def test_modify_job_policy_idempotent(self, powerscale_module_mock):
        """Test modify job policy idempotent."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, {"policy_name": "LOW_IMPACT_HOURS",
                                "intervals": [{"begin": "Monday 18:00", "end": "Monday 06:00", "impact": "Low"}],
                                "state": "present"})
        powerscale_module_mock.get_job_policy_details = MagicMock(
            return_value=MockJobPolicyApi.GET_JOB_POLICY_RESPONSE)
        JobPolicyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # U-JP-014: CHECK MODE - Skip modify, report changed
    def test_modify_job_policy_check_mode(self, powerscale_module_mock):
        """Test modify job policy check mode."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, MockJobPolicyApi.MODIFY_JOB_POLICY_INTERVALS_ARGS)
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.get_job_policy_details = MagicMock(
            return_value=MockJobPolicyApi.GET_JOB_POLICY_RESPONSE)
        powerscale_module_mock.job_api.update_job_policy = MagicMock()
        JobPolicyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.job_api.update_job_policy.assert_not_called()

    # U-JP-015: DIFF MODE - Capture before/after intervals
    def test_modify_job_policy_diff_mode(self, powerscale_module_mock):
        """Test modify job policy diff mode."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, MockJobPolicyApi.MODIFY_JOB_POLICY_INTERVALS_ARGS)
        powerscale_module_mock.module._diff = True
        powerscale_module_mock.get_job_policy_details = MagicMock(
            return_value=MockJobPolicyApi.GET_JOB_POLICY_RESPONSE)
        powerscale_module_mock.job_api.update_job_policy = MagicMock(return_value=None)
        JobPolicyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        call_args = powerscale_module_mock.module.exit_json.call_args[1]
        assert call_args['changed'] is True
        assert 'diff' in call_args
        assert 'before' in call_args['diff']
        assert 'after' in call_args['diff']

    # U-JP-016: DELETE - Delete an existing policy
    def test_delete_job_policy(self, powerscale_module_mock):
        """Test delete job policy."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, MockJobPolicyApi.DELETE_JOB_POLICY_ARGS)
        powerscale_module_mock.get_job_policy_details = MagicMock(
            return_value=MockJobPolicyApi.GET_JOB_POLICY_RESPONSE)
        powerscale_module_mock.job_api.delete_job_policy = MagicMock(return_value=None)
        JobPolicyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.job_api.delete_job_policy.assert_called()

    # U-JP-017: DELETE - Handle ApiException on delete
    def test_delete_job_policy_exception(self, powerscale_module_mock):
        """Test delete job policy exception."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, MockJobPolicyApi.DELETE_JOB_POLICY_ARGS)
        powerscale_module_mock.get_job_policy_details = MagicMock(
            return_value=MockJobPolicyApi.GET_JOB_POLICY_RESPONSE)
        powerscale_module_mock.job_api.delete_job_policy = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobPolicyApi.get_job_policy_exception_response('delete_exception'),
            JobPolicyHandler)

    # U-JP-018: IDEMPOTENCY - No error when deleting non-existent policy
    def test_delete_job_policy_idempotent(self, powerscale_module_mock):
        """Test delete job policy idempotent."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, {"policy_name": "NONEXISTENT", "state": "absent"})
        powerscale_module_mock.get_job_policy_details = MagicMock(return_value=None)
        JobPolicyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # U-JP-019: CHECK MODE - Skip delete, report changed
    def test_delete_job_policy_check_mode(self, powerscale_module_mock):
        """Test delete job policy check mode."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, MockJobPolicyApi.DELETE_JOB_POLICY_ARGS)
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.get_job_policy_details = MagicMock(
            return_value=MockJobPolicyApi.GET_JOB_POLICY_RESPONSE)
        powerscale_module_mock.job_api.delete_job_policy = MagicMock()
        JobPolicyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.job_api.delete_job_policy.assert_not_called()

    # U-JP-020: LIST - List all policies
    def test_list_job_policies(self, powerscale_module_mock):
        """Test list job policies."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, {"state": "present"})
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            return_value=MockSDKResponse(MockJobPolicyApi.LIST_JOB_POLICIES_RESPONSE))
        JobPolicyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.job_api.list_job_policies.assert_called()

    # U-JP-021: LIST - Handle exception on list
    def test_list_job_policies_exception(self, powerscale_module_mock):
        """Test list job policies exception."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, {"policy_name": "LOW_IMPACT", "state": "present"})
        powerscale_module_mock.job_api.list_job_policies = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockJobPolicyApi.get_job_policy_exception_response('list_exception'),
            JobPolicyHandler)

    # U-JP-022: NULL CHECK - policy_name is None for create
    def test_validate_policy_name_null(self, powerscale_module_mock):
        """Test validate policy name null."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, {"policy_name": None, "state": "present"})
        powerscale_module_mock.list_job_policies = MagicMock(return_value=None)
        self.capture_fail_json_call(
            MockJobPolicyApi.get_job_policy_exception_response('policy_name_required'),
            JobPolicyHandler)

    # U-JP-023: EMPTY CHECK - policy_name is empty string
    def test_validate_policy_name_empty(self, powerscale_module_mock):
        """Test validate policy name empty."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, {"policy_name": "", "state": "present"})
        self.capture_fail_json_call(
            MockJobPolicyApi.get_job_policy_exception_response('invalid_policy_name'),
            JobPolicyHandler)

    # U-JP-024: EMPTY CHECK - intervals is empty list
    def test_validate_intervals_empty_list(self, powerscale_module_mock):
        """Test validate intervals empty list."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, {"policy_name": "TEST_POLICY", "intervals": [], "state": "present"})
        powerscale_module_mock.get_job_policy_details = MagicMock(return_value=None)
        powerscale_module_mock.job_api.create_job_policy = MagicMock(
            return_value=MagicMock(id="TEST_POLICY"))
        JobPolicyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # U-JP-025: ERROR CASE - Handle 400 Bad Request
    def test_error_handling_400(self, powerscale_module_mock):
        """Test error handling 400."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, MockJobPolicyApi.CREATE_JOB_POLICY_ARGS)
        powerscale_module_mock.get_job_policy_details = MagicMock(return_value=None)
        powerscale_module_mock.job_api.create_job_policy = MagicMock(
            side_effect=MockApiException(status=400, body="Bad Request"))
        self.capture_fail_json_call(
            MockJobPolicyApi.get_job_policy_exception_response('create_exception'),
            JobPolicyHandler)

    # U-JP-026: ERROR CASE - Handle 401 Unauthorized
    def test_error_handling_401(self, powerscale_module_mock):
        """Test error handling 401."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, MockJobPolicyApi.GET_JOB_POLICY_BY_ID_ARGS)
        powerscale_module_mock.job_api.get_job_policy = MagicMock(
            side_effect=MockApiException(status=401, body="Unauthorized"))
        self.capture_fail_json_call(
            MockJobPolicyApi.get_job_policy_exception_response('get_exception'),
            JobPolicyHandler)

    # U-JP-027: ERROR CASE - Handle 403 Forbidden
    def test_error_handling_403(self, powerscale_module_mock):
        """Test error handling 403."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, MockJobPolicyApi.GET_JOB_POLICY_BY_ID_ARGS)
        powerscale_module_mock.job_api.get_job_policy = MagicMock(
            side_effect=MockApiException(status=403, body="Forbidden"))
        self.capture_fail_json_call(
            MockJobPolicyApi.get_job_policy_exception_response('get_exception'),
            JobPolicyHandler)

    # U-JP-028: ERROR CASE - Handle 500 Server Error
    def test_error_handling_500(self, powerscale_module_mock):
        """Test error handling 500."""
        self.set_module_params(MockJobPolicyApi.JOB_POLICY_COMMON_ARGS, MockJobPolicyApi.DELETE_JOB_POLICY_ARGS)
        powerscale_module_mock.get_job_policy_details = MagicMock(
            return_value=MockJobPolicyApi.GET_JOB_POLICY_RESPONSE)
        powerscale_module_mock.job_api.delete_job_policy = MagicMock(
            side_effect=MockApiException(status=500, body="Internal Server Error"))
        self.capture_fail_json_call(
            MockJobPolicyApi.get_job_policy_exception_response('delete_exception'),
            JobPolicyHandler)
