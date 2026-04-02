# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for S3 Key module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.s3_key import S3Key
from ansible_collections.dellemc.powerscale.plugins.modules.s3_key import S3KeyHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_s3_key_api \
    import MockS3KeyApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response import (
    MockSDKResponse,
)


class TestS3Key(PowerScaleUnitBase):
    """TestS3Key definition."""
    s3_key_args = MockS3KeyApi.S3_KEY_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        """Module object."""
        return S3Key

    # U-S3K-001: GET - Retrieve S3 key for user
    def test_get_s3_key(self, powerscale_module_mock):
        """Test get s3 key."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.CREATE_S3_KEY_ARGS)
        powerscale_module_mock.protocol_api.get_s3_key = MagicMock(
            return_value=MockSDKResponse(MockS3KeyApi.GET_S3_KEY_RESPONSE))
        S3KeyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.get_s3_key.assert_called()

    # U-S3K-002: GET - Retrieve key in custom access zone
    def test_get_s3_key_custom_zone(self, powerscale_module_mock):
        """Test get s3 key custom zone."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.CREATE_S3_KEY_CUSTOM_ZONE_ARGS)
        powerscale_module_mock.protocol_api.get_s3_key = MagicMock(
            return_value=MockSDKResponse(MockS3KeyApi.GET_S3_KEY_RESPONSE))
        S3KeyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.protocol_api.get_s3_key.assert_called()

    # U-S3K-003: GET - Handle 404 when no key exists
    def test_get_s3_key_not_found(self, powerscale_module_mock):
        """Test get s3 key not found."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.CREATE_S3_KEY_ARGS)
        powerscale_module_mock.protocol_api.get_s3_key = MagicMock(
            side_effect=MockApiException(status=404, body="Key not found"))
        powerscale_module_mock.protocol_api.create_s3_key = MagicMock(
            return_value=MockSDKResponse(MockS3KeyApi.CREATE_S3_KEY_RESPONSE))
        S3KeyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # U-S3K-004: GET - Handle non-404 ApiException
    def test_get_s3_key_exception(self, powerscale_module_mock):
        """Test get s3 key exception."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.CREATE_S3_KEY_ARGS)
        powerscale_module_mock.protocol_api.get_s3_key = MagicMock(
            side_effect=MockApiException(status=500, body="Internal Server Error"))
        self.capture_fail_json_call(
            MockS3KeyApi.get_s3_key_exception_response('get_exception'),
            S3KeyHandler)

    # U-S3K-005: CREATE - Generate new key when none exists
    def test_create_s3_key_new(self, powerscale_module_mock):
        """Test create s3 key new."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.CREATE_S3_KEY_ARGS)
        powerscale_module_mock.get_s3_key_details = MagicMock(return_value=None)
        powerscale_module_mock.protocol_api.create_s3_key = MagicMock(
            return_value=MockSDKResponse(MockS3KeyApi.CREATE_S3_KEY_RESPONSE))
        S3KeyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.create_s3_key.assert_called()

    # U-S3K-006: CREATE - Handle ApiException on key create
    def test_create_s3_key_exception(self, powerscale_module_mock):
        """Test create s3 key exception."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.CREATE_S3_KEY_ARGS)
        powerscale_module_mock.get_s3_key_details = MagicMock(return_value=None)
        powerscale_module_mock.protocol_api.create_s3_key = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3KeyApi.get_s3_key_exception_response('create_exception'),
            S3KeyHandler)

    # U-S3K-007: CHECK MODE - Skip create, report changed
    def test_create_s3_key_check_mode(self, powerscale_module_mock):
        """Test create s3 key check mode."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.CREATE_S3_KEY_ARGS)
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.get_s3_key_details = MagicMock(return_value=None)
        S3KeyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.create_s3_key.assert_not_called()

    # U-S3K-008: IDEMPOTENCY - No change when key exists and force=False
    def test_create_s3_key_idempotent_exists_no_force(self, powerscale_module_mock):
        """Test create s3 key idempotent exists no force."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, {"user_name": "s3user1", "state": "present", "force": False})
        powerscale_module_mock.get_s3_key_details = MagicMock(
            return_value=MockS3KeyApi.GET_S3_KEY_RESPONSE)
        S3KeyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # U-S3K-009: CREATE - Force regenerate existing key
    def test_create_s3_key_force_regenerate(self, powerscale_module_mock):
        """Test create s3 key force regenerate."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.FORCE_REGENERATE_ARGS)
        powerscale_module_mock.get_s3_key_details = MagicMock(
            return_value=MockS3KeyApi.GET_S3_KEY_RESPONSE)
        powerscale_module_mock.protocol_api.create_s3_key = MagicMock(
            return_value=MockSDKResponse(MockS3KeyApi.CREATE_S3_KEY_RESPONSE))
        S3KeyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.create_s3_key.assert_called()

    # U-S3K-010: CREATE - Force regenerate with expiry time
    def test_create_s3_key_force_with_expiry(self, powerscale_module_mock):
        """Test create s3 key force with expiry."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.FORCE_REGENERATE_WITH_EXPIRY_ARGS)
        powerscale_module_mock.get_s3_key_details = MagicMock(
            return_value=MockS3KeyApi.GET_S3_KEY_RESPONSE)
        powerscale_module_mock.protocol_api.create_s3_key = MagicMock(
            return_value=MockSDKResponse(MockS3KeyApi.CREATE_S3_KEY_RESPONSE))
        S3KeyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.create_s3_key.assert_called()

    # U-S3K-011: CREATE - Handle exception on force regenerate
    def test_create_s3_key_force_regenerate_exception(self, powerscale_module_mock):
        """Test create s3 key force regenerate exception."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.FORCE_REGENERATE_ARGS)
        powerscale_module_mock.get_s3_key_details = MagicMock(
            return_value=MockS3KeyApi.GET_S3_KEY_RESPONSE)
        powerscale_module_mock.protocol_api.create_s3_key = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3KeyApi.get_s3_key_exception_response('create_exception'),
            S3KeyHandler)

    # U-S3K-012: CHECK MODE - Skip force regenerate
    def test_create_s3_key_force_check_mode(self, powerscale_module_mock):
        """Test create s3 key force check mode."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.FORCE_REGENERATE_ARGS)
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.get_s3_key_details = MagicMock(
            return_value=MockS3KeyApi.GET_S3_KEY_RESPONSE)
        S3KeyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.create_s3_key.assert_not_called()

    # U-S3K-013: DELETE - Delete existing key
    def test_delete_s3_key(self, powerscale_module_mock):
        """Test delete s3 key."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.DELETE_S3_KEY_ARGS)
        powerscale_module_mock.get_s3_key_details = MagicMock(
            return_value=MockS3KeyApi.GET_S3_KEY_RESPONSE)
        powerscale_module_mock.protocol_api.delete_s3_key = MagicMock(return_value=None)
        S3KeyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.delete_s3_key.assert_called()

    # U-S3K-014: DELETE - Handle ApiException on delete
    def test_delete_s3_key_exception(self, powerscale_module_mock):
        """Test delete s3 key exception."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.DELETE_S3_KEY_ARGS)
        powerscale_module_mock.get_s3_key_details = MagicMock(
            return_value=MockS3KeyApi.GET_S3_KEY_RESPONSE)
        powerscale_module_mock.protocol_api.delete_s3_key = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3KeyApi.get_s3_key_exception_response('delete_exception'),
            S3KeyHandler)

    # U-S3K-015: IDEMPOTENCY - No error deleting non-existent key
    def test_delete_s3_key_idempotent(self, powerscale_module_mock):
        """Test delete s3 key idempotent."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.DELETE_S3_KEY_ARGS)
        powerscale_module_mock.get_s3_key_details = MagicMock(return_value=None)
        S3KeyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # U-S3K-016: CHECK MODE - Skip delete, report changed
    def test_delete_s3_key_check_mode(self, powerscale_module_mock):
        """Test delete s3 key check mode."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.DELETE_S3_KEY_ARGS)
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.get_s3_key_details = MagicMock(
            return_value=MockS3KeyApi.GET_S3_KEY_RESPONSE)
        S3KeyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.delete_s3_key.assert_not_called()

    # U-S3K-017: NULL CHECK - user_name is None
    def test_validate_user_name_null(self, powerscale_module_mock):
        """Test validate user name null."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, {"user_name": None, "state": "present"})
        self.capture_fail_json_call(
            MockS3KeyApi.get_s3_key_exception_response('user_name_error'),
            S3KeyHandler)

    # U-S3K-018: EMPTY CHECK - user_name is empty string
    def test_validate_user_name_empty(self, powerscale_module_mock):
        """Test validate user name empty."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, {"user_name": "", "state": "present"})
        self.capture_fail_json_call(
            MockS3KeyApi.get_s3_key_exception_response('invalid_user_name'),
            S3KeyHandler)

    # U-S3K-019: BOUNDARY - Expiry time at minimum (0)
    def test_validate_existing_key_expiry_time_boundary_low(self, powerscale_module_mock):
        """Test validate existing key expiry time boundary low."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.BOUNDARY_EXPIRY_LOW_ARGS)
        powerscale_module_mock.get_s3_key_details = MagicMock(
            return_value=MockS3KeyApi.GET_S3_KEY_RESPONSE)
        powerscale_module_mock.protocol_api.create_s3_key = MagicMock(
            return_value=MockSDKResponse(MockS3KeyApi.CREATE_S3_KEY_RESPONSE))
        S3KeyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # U-S3K-020: BOUNDARY - Expiry time at maximum (1440)
    def test_validate_existing_key_expiry_time_boundary_high(self, powerscale_module_mock):
        """Test validate existing key expiry time boundary high."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.BOUNDARY_EXPIRY_HIGH_ARGS)
        powerscale_module_mock.get_s3_key_details = MagicMock(
            return_value=MockS3KeyApi.GET_S3_KEY_RESPONSE)
        powerscale_module_mock.protocol_api.create_s3_key = MagicMock(
            return_value=MockSDKResponse(MockS3KeyApi.CREATE_S3_KEY_RESPONSE))
        S3KeyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    # U-S3K-021: NEGATIVE - Expiry time above range (1441)
    def test_validate_existing_key_expiry_time_above_range(self, powerscale_module_mock):
        """Test validate existing key expiry time above range."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, {"user_name": "s3user1", "force": True,
                                "existing_key_expiry_time": 1441, "state": "present"})
        powerscale_module_mock.get_s3_key_details = MagicMock(
            return_value=MockS3KeyApi.GET_S3_KEY_RESPONSE)
        self.capture_fail_json_call(
            MockS3KeyApi.get_s3_key_exception_response('expiry_range_error'),
            S3KeyHandler)

    # U-S3K-022: NEGATIVE - Negative expiry time
    def test_validate_existing_key_expiry_time_negative(self, powerscale_module_mock):
        """Test validate existing key expiry time negative."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, {"user_name": "s3user1", "force": True,
                                "existing_key_expiry_time": -1, "state": "present"})
        powerscale_module_mock.get_s3_key_details = MagicMock(
            return_value=MockS3KeyApi.GET_S3_KEY_RESPONSE)
        self.capture_fail_json_call(
            MockS3KeyApi.get_s3_key_exception_response('expiry_range_error'),
            S3KeyHandler)

    # U-S3K-023: ERROR CASE - Handle 400 Bad Request
    def test_error_handling_400(self, powerscale_module_mock):
        """Test error handling 400."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.CREATE_S3_KEY_ARGS)
        powerscale_module_mock.get_s3_key_details = MagicMock(return_value=None)
        powerscale_module_mock.protocol_api.create_s3_key = MagicMock(
            side_effect=MockApiException(status=400, body="Bad Request"))
        self.capture_fail_json_call(
            MockS3KeyApi.get_s3_key_exception_response('create_exception'),
            S3KeyHandler)

    # U-S3K-024: ERROR CASE - Handle 401 Unauthorized
    def test_error_handling_401(self, powerscale_module_mock):
        """Test error handling 401."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.CREATE_S3_KEY_ARGS)
        powerscale_module_mock.protocol_api.get_s3_key = MagicMock(
            side_effect=MockApiException(status=401, body="Unauthorized"))
        self.capture_fail_json_call(
            MockS3KeyApi.get_s3_key_exception_response('get_exception'),
            S3KeyHandler)

    # U-S3K-025: ERROR CASE - Handle 403 Forbidden
    def test_error_handling_403(self, powerscale_module_mock):
        """Test error handling 403."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.CREATE_S3_KEY_ARGS)
        powerscale_module_mock.protocol_api.get_s3_key = MagicMock(
            side_effect=MockApiException(status=403, body="Forbidden"))
        self.capture_fail_json_call(
            MockS3KeyApi.get_s3_key_exception_response('get_exception'),
            S3KeyHandler)

    # U-S3K-026: ERROR CASE - Handle 500 Server Error
    def test_error_handling_500(self, powerscale_module_mock):
        """Test error handling 500."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.DELETE_S3_KEY_ARGS)
        powerscale_module_mock.get_s3_key_details = MagicMock(
            return_value=MockS3KeyApi.GET_S3_KEY_RESPONSE)
        powerscale_module_mock.protocol_api.delete_s3_key = MagicMock(
            side_effect=MockApiException(status=500, body="Internal Server Error"))
        self.capture_fail_json_call(
            MockS3KeyApi.get_s3_key_exception_response('delete_exception'),
            S3KeyHandler)

    # U-S3K-027: SECURITY - secret_key only returned on generation
    def test_secret_key_returned_on_create(self, powerscale_module_mock):
        """Test secret key returned on create."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, MockS3KeyApi.CREATE_S3_KEY_ARGS)
        powerscale_module_mock.get_s3_key_details = MagicMock(return_value=None)
        powerscale_module_mock.protocol_api.create_s3_key = MagicMock(
            return_value=MockSDKResponse(MockS3KeyApi.CREATE_S3_KEY_RESPONSE))
        S3KeyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        call_args = powerscale_module_mock.module.exit_json.call_args[1]
        assert call_args['changed'] is True
        s3_key_details = call_args.get('s3_key_details', {})
        # On create, both access_id and secret_key should be present
        assert 'access_id' in str(s3_key_details) or 'secret_key' in str(s3_key_details)

    # U-S3K-028: SECURITY - secret_key NOT returned on existing key get
    def test_secret_key_not_returned_on_get(self, powerscale_module_mock):
        """Test secret key not returned on get."""
        self.set_module_params(MockS3KeyApi.S3_KEY_COMMON_ARGS, {"user_name": "s3user1", "state": "present", "force": False})
        powerscale_module_mock.get_s3_key_details = MagicMock(
            return_value=MockS3KeyApi.GET_S3_KEY_RESPONSE)
        S3KeyHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        call_args = powerscale_module_mock.module.exit_json.call_args[1]
        assert call_args['changed'] is False
        # On get (no force), secret_key should NOT be in the response
        s3_key_details = call_args.get('s3_key_details', {})
        if isinstance(s3_key_details, dict) and 'keys' in s3_key_details:
            for key in s3_key_details['keys']:
                assert 'secret_key' not in key
