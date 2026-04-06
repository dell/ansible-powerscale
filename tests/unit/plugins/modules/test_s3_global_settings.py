# Copyright: (c) 2026, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for S3 global settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
import copy
from unittest.mock import patch
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.s3_global_settings import S3GlobalSettings
from ansible_collections.dellemc.powerscale.plugins.modules.s3_global_settings import S3GlobalSettingsHandler
from ansible_collections.dellemc.powerscale.plugins.modules.s3_global_settings import main as s3_global_main
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_s3_global_settings_api \
    import MockS3GlobalSettingsApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response import (
    MockSDKResponse,
)


class TestS3GlobalSettings(PowerScaleUnitBase):
    """TestS3GlobalSettings definition."""
    s3_global_args = MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        """Module object."""
        return S3GlobalSettings

    # U-SGS-001: GET - Successful retrieval of S3 global settings
    def test_get_s3_global_settings(self, powerscale_module_mock):
        """Test get s3 global settings."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {})
        powerscale_module_mock.protocol_api.get_s3_settings_global = MagicMock(
            return_value=MockSDKResponse(MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE))
        S3GlobalSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.get_s3_settings_global.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # U-SGS-002: GET - Response includes all expected fields
    def test_get_s3_global_settings_response_fields(self, powerscale_module_mock):
        """Test get s3 global settings response fields."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {})
        powerscale_module_mock.protocol_api.get_s3_settings_global = MagicMock(
            return_value=MockSDKResponse(MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE))
        S3GlobalSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        call_args = powerscale_module_mock.module.exit_json.call_args[1]
        assert 's3_global_settings_details' in call_args
        details = call_args['s3_global_settings_details']
        for key in ['http_port', 'https_port', 'https_only', 'service']:
            assert key in details

    # U-SGS-003: GET - Handle ApiException on retrieval
    def test_get_s3_global_settings_exception(self, powerscale_module_mock):
        """Test get s3 global settings exception."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {})
        powerscale_module_mock.protocol_api.get_s3_settings_global = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3GlobalSettingsApi.get_s3_global_settings_exception_response('get_details_exception'),
            S3GlobalSettingsHandler)

    # U-SGS-004: UPDATE - Modify HTTP port
    def test_modify_s3_global_settings_http_port(self, powerscale_module_mock):
        """Test modify s3 global settings http port."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {"http_port": 9020})
        powerscale_module_mock.get_s3_global_settings_details = MagicMock(
            return_value={"http_port": 9080, "https_port": 9021, "https_only": False, "service": True})
        S3GlobalSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.update_s3_settings_global.assert_called()

    # U-SGS-005: UPDATE - Modify HTTPS port
    def test_modify_s3_global_settings_https_port(self, powerscale_module_mock):
        """Test modify s3 global settings https port."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {"https_port": 9022})
        powerscale_module_mock.get_s3_global_settings_details = MagicMock(
            return_value=MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE)
        S3GlobalSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.update_s3_settings_global.assert_called()

    # U-SGS-006: UPDATE - Toggle HTTPS-only mode
    def test_modify_s3_global_settings_https_only(self, powerscale_module_mock):
        """Test modify s3 global settings https only."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {"https_only": True})
        powerscale_module_mock.get_s3_global_settings_details = MagicMock(
            return_value=MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE)
        S3GlobalSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.update_s3_settings_global.assert_called()

    # U-SGS-007: UPDATE - Toggle S3 service
    def test_modify_s3_global_settings_service(self, powerscale_module_mock):
        """Test modify s3 global settings service."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {"service": False})
        powerscale_module_mock.get_s3_global_settings_details = MagicMock(
            return_value=MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE)
        S3GlobalSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.update_s3_settings_global.assert_called()

    # U-SGS-008: UPDATE - Modify multiple parameters simultaneously
    def test_modify_s3_global_settings_multiple_params(self, powerscale_module_mock):
        """Test modify s3 global settings multiple params."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, MockS3GlobalSettingsApi.MODIFY_S3_GLOBAL_MULTIPLE_ARGS)
        powerscale_module_mock.get_s3_global_settings_details = MagicMock(
            return_value=MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE)
        S3GlobalSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.update_s3_settings_global.assert_called()

    # U-SGS-009: UPDATE - Handle ApiException on modify
    def test_modify_s3_global_settings_exception(self, powerscale_module_mock):
        """Test modify s3 global settings exception."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {"service": False})
        powerscale_module_mock.get_s3_global_settings_details = MagicMock(
            return_value=MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE)
        powerscale_module_mock.protocol_api.update_s3_settings_global = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3GlobalSettingsApi.get_s3_global_settings_exception_response('update_exception'),
            S3GlobalSettingsHandler)

    # U-SGS-010: IDEMPOTENCY - No change when desired matches current
    def test_modify_s3_global_settings_idempotent(self, powerscale_module_mock):
        """Test modify s3 global settings idempotent."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {"http_port": 9020, "https_port": 9021, "https_only": False, "service": True})
        powerscale_module_mock.get_s3_global_settings_details = MagicMock(
            return_value=MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE)
        S3GlobalSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # U-SGS-011: CHECK MODE - Skip API call, report changed
    def test_modify_s3_global_settings_check_mode(self, powerscale_module_mock):
        """Test modify s3 global settings check mode."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {"http_port": 9999})
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.get_s3_global_settings_details = MagicMock(
            return_value=MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE)
        powerscale_module_mock.protocol_api.update_s3_settings_global = MagicMock()
        S3GlobalSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.update_s3_settings_global.assert_not_called()

    # U-SGS-012: CHECK MODE - No change when idempotent
    def test_modify_s3_global_settings_check_mode_no_change(self, powerscale_module_mock):
        """Test modify s3 global settings check mode no change."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {"http_port": 9020, "https_port": 9021})
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.get_s3_global_settings_details = MagicMock(
            return_value=MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE)
        S3GlobalSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # U-SGS-013: DIFF MODE - Capture before/after state
    def test_modify_s3_global_settings_diff_mode(self, powerscale_module_mock):
        """Test modify s3 global settings diff mode."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {"service": False})
        powerscale_module_mock.module._diff = True
        powerscale_module_mock.get_s3_global_settings_details = MagicMock(
            return_value=MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE)
        powerscale_module_mock.protocol_api.update_s3_settings_global = MagicMock(return_value=None)
        S3GlobalSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        call_args = powerscale_module_mock.module.exit_json.call_args[1]
        assert call_args['changed'] is True
        assert 'diff' in call_args
        assert 'before' in call_args['diff']
        assert 'after' in call_args['diff']

    # U-SGS-014: NULL CHECK - Handle None http_port gracefully
    def test_validate_http_port_null(self, powerscale_module_mock):
        """Test validate http port null."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {"http_port": None})
        powerscale_module_mock.protocol_api.get_s3_settings_global = MagicMock(
            return_value=MockSDKResponse(MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE))
        S3GlobalSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # U-SGS-015: NULL CHECK - Handle None https_port gracefully
    def test_validate_https_port_null(self, powerscale_module_mock):
        """Test validate https port null."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {"https_port": None})
        powerscale_module_mock.protocol_api.get_s3_settings_global = MagicMock(
            return_value=MockSDKResponse(MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE))
        S3GlobalSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # U-SGS-016: BOUNDARY - Port at minimum (1024)
    def test_validate_http_port_boundary_low(self, powerscale_module_mock):
        """Test validate http port boundary low."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {"http_port": 1024})
        powerscale_module_mock.get_s3_global_settings_details = MagicMock(
            return_value=MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE)
        powerscale_module_mock.protocol_api.update_s3_settings_global = MagicMock(return_value=None)
        S3GlobalSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # U-SGS-017: BOUNDARY - Port at maximum (65535)
    def test_validate_http_port_boundary_high(self, powerscale_module_mock):
        """Test validate http port boundary high."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {"http_port": 65535})
        powerscale_module_mock.get_s3_global_settings_details = MagicMock(
            return_value=MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE)
        powerscale_module_mock.protocol_api.update_s3_settings_global = MagicMock(return_value=None)
        S3GlobalSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # U-SGS-018: NEGATIVE - Port below valid range
    def test_validate_http_port_below_range(self, powerscale_module_mock):
        """Test validate http port below range."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {"http_port": 1023})
        powerscale_module_mock.get_s3_global_settings_details = MagicMock(
            return_value=MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE)
        self.capture_fail_json_call(
            MockS3GlobalSettingsApi.get_s3_global_settings_exception_response('port_range_error'),
            S3GlobalSettingsHandler)

    # U-SGS-019: NEGATIVE - Port above valid range
    def test_validate_http_port_above_range(self, powerscale_module_mock):
        """Test validate http port above range."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {"http_port": 65536})
        powerscale_module_mock.get_s3_global_settings_details = MagicMock(
            return_value=MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE)
        self.capture_fail_json_call(
            MockS3GlobalSettingsApi.get_s3_global_settings_exception_response('port_range_error'),
            S3GlobalSettingsHandler)

    # U-SGS-020: NEGATIVE - HTTPS port below valid range
    def test_validate_https_port_below_range(self, powerscale_module_mock):
        """Test validate https port below range."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {"https_port": 0})
        powerscale_module_mock.get_s3_global_settings_details = MagicMock(
            return_value=MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE)
        self.capture_fail_json_call(
            MockS3GlobalSettingsApi.get_s3_global_settings_exception_response('port_range_error'),
            S3GlobalSettingsHandler)

    # U-SGS-021: NEGATIVE - HTTPS port above valid range
    def test_validate_https_port_above_range(self, powerscale_module_mock):
        """Test validate https port above range."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {"https_port": 70000})
        powerscale_module_mock.get_s3_global_settings_details = MagicMock(
            return_value=MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE)
        self.capture_fail_json_call(
            MockS3GlobalSettingsApi.get_s3_global_settings_exception_response('port_range_error'),
            S3GlobalSettingsHandler)

    # U-SGS-022: ERROR CASE - Handle 400 Bad Request
    def test_error_handling_400(self, powerscale_module_mock):
        """Test error handling 400."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {"http_port": 9025})
        powerscale_module_mock.get_s3_global_settings_details = MagicMock(
            return_value=MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE)
        powerscale_module_mock.protocol_api.update_s3_settings_global = MagicMock(
            side_effect=MockApiException(status=400, body="Bad Request"))
        self.capture_fail_json_call(
            MockS3GlobalSettingsApi.get_s3_global_settings_exception_response('update_exception'),
            S3GlobalSettingsHandler)

    # U-SGS-023: ERROR CASE - Handle 401 Unauthorized
    def test_error_handling_401(self, powerscale_module_mock):
        """Test error handling 401."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {})
        powerscale_module_mock.protocol_api.get_s3_settings_global = MagicMock(
            side_effect=MockApiException(status=401, body="Unauthorized"))
        self.capture_fail_json_call(
            MockS3GlobalSettingsApi.get_s3_global_settings_exception_response('get_details_exception'),
            S3GlobalSettingsHandler)

    # U-SGS-024: ERROR CASE - Handle 403 Forbidden
    def test_error_handling_403(self, powerscale_module_mock):
        """Test error handling 403."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {})
        powerscale_module_mock.protocol_api.get_s3_settings_global = MagicMock(
            side_effect=MockApiException(status=403, body="Forbidden"))
        self.capture_fail_json_call(
            MockS3GlobalSettingsApi.get_s3_global_settings_exception_response('get_details_exception'),
            S3GlobalSettingsHandler)

    # U-SGS-025: ERROR CASE - Handle 500 Server Error
    def test_error_handling_500(self, powerscale_module_mock):
        """Test error handling 500."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {"service": False})
        powerscale_module_mock.get_s3_global_settings_details = MagicMock(
            return_value=MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE)
        powerscale_module_mock.protocol_api.update_s3_settings_global = MagicMock(
            side_effect=MockApiException(status=500, body="Internal Server Error"))
        self.capture_fail_json_call(
            MockS3GlobalSettingsApi.get_s3_global_settings_exception_response('update_exception'),
            S3GlobalSettingsHandler)

    # U-SGS-026: ERROR CASE - Handle non-API exception on GET
    def test_get_s3_global_settings_general_exception(self, powerscale_module_mock):
        """Test get s3 global settings general exception."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {})
        powerscale_module_mock.protocol_api.get_s3_settings_global = MagicMock(
            side_effect=Exception("Unexpected error"))
        self.capture_fail_json_call(
            MockS3GlobalSettingsApi.get_s3_global_settings_exception_response('general_get_exception'),
            S3GlobalSettingsHandler)

    # U-SGS-027: ERROR CASE - Handle non-API exception on UPDATE
    def test_modify_s3_global_settings_general_exception(self, powerscale_module_mock):
        """Test modify s3 global settings general exception."""
        self.set_module_params(MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS, {"service": False})
        powerscale_module_mock.get_s3_global_settings_details = MagicMock(
            return_value=MockS3GlobalSettingsApi.GET_S3_GLOBAL_RESPONSE)
        powerscale_module_mock.protocol_api.update_s3_settings_global = MagicMock(
            side_effect=Exception("Unexpected error"))
        self.capture_fail_json_call(
            MockS3GlobalSettingsApi.get_s3_global_settings_exception_response('general_update_exception'),
            S3GlobalSettingsHandler)

    # U-SGS-028: PREREQS - Module fails when SDK prerequisites are missing
    def test_prereqs_validation_failure(self, powerscale_module_mock):
        """Test module fails when SDK prerequisites are missing."""
        original_return = utils.validate_module_pre_reqs.return_value
        utils.validate_module_pre_reqs.return_value = (
            MockS3GlobalSettingsApi.PREREQS_VALIDATE_FAILURE
        )
        mock_module = MagicMock()
        mock_module.params = copy.deepcopy(
            MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS)
        mock_module.check_mode = False
        mock_module.fail_json = MagicMock(side_effect=SystemExit)
        mock_am = MagicMock(return_value=mock_module)
        try:
            with patch(
                'ansible_collections.dellemc.powerscale.plugins.modules'
                '.s3_global_settings.AnsibleModule', mock_am
            ):
                with pytest.raises(SystemExit):
                    S3GlobalSettings()
            mock_module.fail_json.assert_called_once()
            assert "Required SDK packages not found" in str(
                mock_module.fail_json.call_args)
        finally:
            utils.validate_module_pre_reqs.return_value = original_return

    # U-SGS-029: MAIN - Test main() entry point
    def test_main(self, powerscale_module_mock):
        """Test main function entry point."""
        mock_module = MagicMock()
        mock_module.params = copy.deepcopy(
            MockS3GlobalSettingsApi.S3_GLOBAL_COMMON_ARGS)
        mock_module.check_mode = False
        mock_module._diff = False
        mock_am = MagicMock(return_value=mock_module)
        with patch(
            'ansible_collections.dellemc.powerscale.plugins.modules'
            '.s3_global_settings.AnsibleModule', mock_am
        ):
            s3_global_main()
