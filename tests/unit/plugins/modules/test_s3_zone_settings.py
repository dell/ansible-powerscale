# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for S3 zone settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.s3_zone_settings import S3ZoneSettings
from ansible_collections.dellemc.powerscale.plugins.modules.s3_zone_settings import S3ZoneSettingsHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_s3_zone_settings_api \
    import MockS3ZoneSettingsApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response import (
    MockSDKResponse,
)


class TestS3ZoneSettings(PowerScaleUnitBase):
    """TestS3ZoneSettings definition."""
    s3_zone_args = MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        """Module object."""
        return S3ZoneSettings

    # U-SZS-001: GET - Successful retrieval of S3 zone settings
    def test_get_s3_zone_settings(self, powerscale_module_mock):
        """Test get s3 zone settings."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, {"access_zone": "System"})
        powerscale_module_mock.protocol_api.get_s3_settings_zone = MagicMock(
            return_value=MockSDKResponse(MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE))
        S3ZoneSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.get_s3_settings_zone.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # U-SZS-002: GET - Retrieve settings for custom access zone
    def test_get_s3_zone_settings_custom_zone(self, powerscale_module_mock):
        """Test get s3 zone settings custom zone."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, {"access_zone": "myzone"})
        powerscale_module_mock.protocol_api.get_s3_settings_zone = MagicMock(
            return_value=MockSDKResponse(MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE))
        S3ZoneSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.get_s3_settings_zone.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # U-SZS-003: GET - Response includes all expected fields
    def test_get_s3_zone_settings_response_fields(self, powerscale_module_mock):
        """Test get s3 zone settings response fields."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, {})
        powerscale_module_mock.protocol_api.get_s3_settings_zone = MagicMock(
            return_value=MockSDKResponse(MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE))
        S3ZoneSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        call_args = powerscale_module_mock.module.exit_json.call_args[1]
        assert 's3_zone_settings_details' in call_args
        details = call_args['s3_zone_settings_details']
        for key in ['base_domain', 'bucket_directory_create_mode', 'object_acl_policy',
                     'root_path', 'use_md5_for_etag', 'validate_content_md5']:
            assert key in details

    # U-SZS-004: GET - Handle ApiException on retrieval
    def test_get_s3_zone_settings_exception(self, powerscale_module_mock):
        """Test get s3 zone settings exception."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, {})
        powerscale_module_mock.protocol_api.get_s3_settings_zone = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3ZoneSettingsApi.get_s3_zone_settings_exception_response('get_details_exception'),
            S3ZoneSettingsHandler)

    # U-SZS-005: UPDATE - Modify base_domain
    def test_modify_s3_zone_settings_base_domain(self, powerscale_module_mock):
        """Test modify s3 zone settings base domain."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, MockS3ZoneSettingsApi.MODIFY_S3_ZONE_BASE_DOMAIN_ARGS)
        powerscale_module_mock.get_s3_zone_settings_details = MagicMock(
            return_value=MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE)
        S3ZoneSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.update_s3_settings_zone.assert_called()

    # U-SZS-006: UPDATE - Modify root_path
    def test_modify_s3_zone_settings_root_path(self, powerscale_module_mock):
        """Test modify s3 zone settings root path."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, MockS3ZoneSettingsApi.MODIFY_S3_ZONE_ROOT_PATH_ARGS)
        powerscale_module_mock.get_s3_zone_settings_details = MagicMock(
            return_value=MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE)
        S3ZoneSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.update_s3_settings_zone.assert_called()

    # U-SZS-007: UPDATE - Modify ACL policy
    def test_modify_s3_zone_settings_object_acl_policy(self, powerscale_module_mock):
        """Test modify s3 zone settings object acl policy."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, MockS3ZoneSettingsApi.MODIFY_S3_ZONE_ACL_POLICY_ARGS)
        powerscale_module_mock.get_s3_zone_settings_details = MagicMock(
            return_value=MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE)
        S3ZoneSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.update_s3_settings_zone.assert_called()

    # U-SZS-008: UPDATE - Modify bucket directory create mode
    def test_modify_s3_zone_settings_bucket_directory_create_mode(self, powerscale_module_mock):
        """Test modify s3 zone settings bucket directory create mode."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, MockS3ZoneSettingsApi.MODIFY_S3_ZONE_BUCKET_DIR_MODE_ARGS)
        powerscale_module_mock.get_s3_zone_settings_details = MagicMock(
            return_value=MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE)
        S3ZoneSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.update_s3_settings_zone.assert_called()

    # U-SZS-009: UPDATE - Modify MD5 options
    def test_modify_s3_zone_settings_md5_options(self, powerscale_module_mock):
        """Test modify s3 zone settings md5 options."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, MockS3ZoneSettingsApi.MODIFY_S3_ZONE_MD5_ARGS)
        powerscale_module_mock.get_s3_zone_settings_details = MagicMock(
            return_value=MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE)
        S3ZoneSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.update_s3_settings_zone.assert_called()

    # U-SZS-010: UPDATE - Modify multiple zone parameters simultaneously
    def test_modify_s3_zone_settings_multiple_params(self, powerscale_module_mock):
        """Test modify s3 zone settings multiple params."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, MockS3ZoneSettingsApi.MODIFY_S3_ZONE_MULTIPLE_ARGS)
        powerscale_module_mock.get_s3_zone_settings_details = MagicMock(
            return_value=MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE)
        S3ZoneSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.update_s3_settings_zone.assert_called()

    # U-SZS-011: UPDATE - Handle ApiException on modify
    def test_modify_s3_zone_settings_exception(self, powerscale_module_mock):
        """Test modify s3 zone settings exception."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, MockS3ZoneSettingsApi.MODIFY_S3_ZONE_BASE_DOMAIN_ARGS)
        powerscale_module_mock.get_s3_zone_settings_details = MagicMock(
            return_value=MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE)
        powerscale_module_mock.protocol_api.update_s3_settings_zone = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3ZoneSettingsApi.get_s3_zone_settings_exception_response('update_exception'),
            S3ZoneSettingsHandler)

    # U-SZS-012: IDEMPOTENCY - No change when desired matches current
    def test_modify_s3_zone_settings_idempotent(self, powerscale_module_mock):
        """Test modify s3 zone settings idempotent."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, {"base_domain": "", "bucket_directory_create_mode": 448,
                                "object_acl_policy": "replace", "root_path": "/ifs",
                                "use_md5_for_etag": False, "validate_content_md5": False})
        powerscale_module_mock.get_s3_zone_settings_details = MagicMock(
            return_value=MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE)
        S3ZoneSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # U-SZS-013: CHECK MODE - Skip API call, report changed
    def test_modify_s3_zone_settings_check_mode(self, powerscale_module_mock):
        """Test modify s3 zone settings check mode."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, {"base_domain": "s3.new.example.com"})
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.get_s3_zone_settings_details = MagicMock(
            return_value=MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE)
        powerscale_module_mock.protocol_api.update_s3_settings_zone = MagicMock(return_value=None)
        S3ZoneSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.update_s3_settings_zone.assert_not_called()

    # U-SZS-014: DIFF MODE - Capture before/after state
    def test_modify_s3_zone_settings_diff_mode(self, powerscale_module_mock):
        """Test modify s3 zone settings diff mode."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, {"root_path": "/ifs/data/s3"})
        powerscale_module_mock.module._diff = True
        powerscale_module_mock.get_s3_zone_settings_details = MagicMock(
            return_value=MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE)
        powerscale_module_mock.protocol_api.update_s3_settings_zone = MagicMock(return_value=None)
        S3ZoneSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        call_args = powerscale_module_mock.module.exit_json.call_args[1]
        assert call_args['changed'] is True
        assert 'diff' in call_args
        assert 'before' in call_args['diff']
        assert 'after' in call_args['diff']

    # U-SZS-015: NULL CHECK - Handle None access_zone (uses default)
    def test_validate_access_zone_null(self, powerscale_module_mock):
        """Test validate access zone null."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, {"access_zone": None})
        powerscale_module_mock.protocol_api.get_s3_settings_zone = MagicMock(
            return_value=MockSDKResponse(MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE))
        S3ZoneSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # U-SZS-016: EMPTY CHECK - Handle empty base_domain string
    def test_validate_base_domain_empty(self, powerscale_module_mock):
        """Test validate base domain empty."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, {"base_domain": ""})
        powerscale_module_mock.get_s3_zone_settings_details = MagicMock(
            return_value=MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE)
        S3ZoneSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        # empty string matches current "" - should be idempotent
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # U-SZS-017: BOUNDARY - base_domain at maximum length (255 chars)
    def test_validate_base_domain_boundary_max(self, powerscale_module_mock):
        """Test validate base domain boundary max."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, {"base_domain": "a" * 255})
        powerscale_module_mock.get_s3_zone_settings_details = MagicMock(
            return_value=MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE)
        powerscale_module_mock.protocol_api.update_s3_settings_zone = MagicMock(return_value=None)
        S3ZoneSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # U-SZS-018: NEGATIVE - base_domain exceeds 255 chars
    def test_validate_base_domain_over_max(self, powerscale_module_mock):
        """Test validate base domain over max."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, {"base_domain": "a" * 256})
        powerscale_module_mock.get_s3_zone_settings_details = MagicMock(
            return_value=MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE)
        self.capture_fail_json_call(
            MockS3ZoneSettingsApi.get_s3_zone_settings_exception_response('domain_length_error'),
            S3ZoneSettingsHandler)

    # U-SZS-019: BOUNDARY - root_path at maximum length (4096 chars)
    def test_validate_root_path_boundary_max(self, powerscale_module_mock):
        """Test validate root path boundary max."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, {"root_path": "/" + "a" * 4095})
        powerscale_module_mock.get_s3_zone_settings_details = MagicMock(
            return_value=MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE)
        powerscale_module_mock.protocol_api.update_s3_settings_zone = MagicMock(return_value=None)
        S3ZoneSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # U-SZS-020: BOUNDARY - Mode at minimum (0)
    def test_validate_bucket_directory_create_mode_boundary_low(self, powerscale_module_mock):
        """Test validate bucket directory create mode boundary low."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, {"bucket_directory_create_mode": 0})
        powerscale_module_mock.get_s3_zone_settings_details = MagicMock(
            return_value=MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE)
        powerscale_module_mock.protocol_api.update_s3_settings_zone = MagicMock(return_value=None)
        S3ZoneSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # U-SZS-021: BOUNDARY - Mode at maximum (511)
    def test_validate_bucket_directory_create_mode_boundary_high(self, powerscale_module_mock):
        """Test validate bucket directory create mode boundary high."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, {"bucket_directory_create_mode": 511})
        powerscale_module_mock.get_s3_zone_settings_details = MagicMock(
            return_value=MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE)
        powerscale_module_mock.protocol_api.update_s3_settings_zone = MagicMock(return_value=None)
        S3ZoneSettingsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # U-SZS-022: NEGATIVE - Mode above range (512)
    def test_validate_bucket_directory_create_mode_above_range(self, powerscale_module_mock):
        """Test validate bucket directory create mode above range."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, {"bucket_directory_create_mode": 512})
        powerscale_module_mock.get_s3_zone_settings_details = MagicMock(
            return_value=MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE)
        self.capture_fail_json_call(
            MockS3ZoneSettingsApi.get_s3_zone_settings_exception_response('mode_range_error'),
            S3ZoneSettingsHandler)

    # U-SZS-023: NEGATIVE - Negative mode value
    def test_validate_bucket_directory_create_mode_negative(self, powerscale_module_mock):
        """Test validate bucket directory create mode negative."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, {"bucket_directory_create_mode": -1})
        powerscale_module_mock.get_s3_zone_settings_details = MagicMock(
            return_value=MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE)
        self.capture_fail_json_call(
            MockS3ZoneSettingsApi.get_s3_zone_settings_exception_response('mode_range_error'),
            S3ZoneSettingsHandler)

    # U-SZS-024: ERROR CASE - Handle 400 Bad Request
    def test_error_handling_400(self, powerscale_module_mock):
        """Test error handling 400."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, {"base_domain": "s3.example.com"})
        powerscale_module_mock.get_s3_zone_settings_details = MagicMock(
            return_value=MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE)
        powerscale_module_mock.protocol_api.update_s3_settings_zone = MagicMock(
            side_effect=MockApiException(status=400, body="Bad Request"))
        self.capture_fail_json_call(
            MockS3ZoneSettingsApi.get_s3_zone_settings_exception_response('update_exception'),
            S3ZoneSettingsHandler)

    # U-SZS-025: ERROR CASE - Handle 401 Unauthorized
    def test_error_handling_401(self, powerscale_module_mock):
        """Test error handling 401."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, {})
        powerscale_module_mock.protocol_api.get_s3_settings_zone = MagicMock(
            side_effect=MockApiException(status=401, body="Unauthorized"))
        self.capture_fail_json_call(
            MockS3ZoneSettingsApi.get_s3_zone_settings_exception_response('get_details_exception'),
            S3ZoneSettingsHandler)

    # U-SZS-026: ERROR CASE - Handle 403 Forbidden
    def test_error_handling_403(self, powerscale_module_mock):
        """Test error handling 403."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, {})
        powerscale_module_mock.protocol_api.get_s3_settings_zone = MagicMock(
            side_effect=MockApiException(status=403, body="Forbidden"))
        self.capture_fail_json_call(
            MockS3ZoneSettingsApi.get_s3_zone_settings_exception_response('get_details_exception'),
            S3ZoneSettingsHandler)

    # U-SZS-027: ERROR CASE - Handle 404 zone not found
    def test_error_handling_404(self, powerscale_module_mock):
        """Test error handling 404."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, {"access_zone": "nonexistent"})
        powerscale_module_mock.protocol_api.get_s3_settings_zone = MagicMock(
            side_effect=MockApiException(status=404, body="Zone not found"))
        self.capture_fail_json_call(
            MockS3ZoneSettingsApi.get_s3_zone_settings_exception_response('get_details_exception'),
            S3ZoneSettingsHandler)

    # U-SZS-028: ERROR CASE - Handle 500 Server Error
    def test_error_handling_500(self, powerscale_module_mock):
        """Test error handling 500."""
        self.set_module_params(MockS3ZoneSettingsApi.S3_ZONE_COMMON_ARGS, {"base_domain": "s3.example.com"})
        powerscale_module_mock.get_s3_zone_settings_details = MagicMock(
            return_value=MockS3ZoneSettingsApi.GET_S3_ZONE_RESPONSE)
        powerscale_module_mock.protocol_api.update_s3_settings_zone = MagicMock(
            side_effect=MockApiException(status=500, body="Internal Server Error"))
        self.capture_fail_json_call(
            MockS3ZoneSettingsApi.get_s3_zone_settings_exception_response('update_exception'),
            S3ZoneSettingsHandler)
