# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for S3 Key module on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import copy
import pytest
from mock.mock import MagicMock

# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock import (
    utils,
)
from ansible.module_utils import basic

from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import (
    PowerScaleUnitBase,
)

basic.AnsibleModule = MagicMock()

from ansible_collections.dellemc.powerscale.plugins.modules.s3_key import (
    S3Key,
    S3KeyHandler,
)
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_s3_key_api import (
    MockS3KeyApi,
)
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception import (
    MockApiException,
)


class TestS3Key(PowerScaleUnitBase):
    """S3 Key module tests"""

    s3_key_args = MockS3KeyApi.S3_KEY_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return S3Key

    def _get_args(self, overrides=None):
        """Return a fresh copy of args with optional overrides."""
        args = copy.deepcopy(MockS3KeyApi.S3_KEY_COMMON_ARGS)
        if overrides:
            args.update(overrides)
        return args

    @staticmethod
    def _make_get_s3_key_mock(response_dict):
        """Create a fresh get_s3_key MagicMock that returns the given response dict."""
        s3_key_obj = MagicMock()
        keys_mock = MagicMock()
        keys_mock.to_dict.return_value = response_dict
        s3_key_obj.keys = keys_mock
        return MagicMock(return_value=s3_key_obj)

    @staticmethod
    def _make_create_s3_key_mock(response_dict):
        """Create a fresh create_s3_key MagicMock that returns the given response dict."""
        s3_key_obj = MagicMock()
        keys_mock = MagicMock()
        keys_mock.to_dict.return_value = response_dict
        s3_key_obj.keys = keys_mock
        return MagicMock(return_value=s3_key_obj)

    def test_get_s3_key_details(self, powerscale_module_mock):
        powerscale_module_mock.module.params = self._get_args()

        # existing key details are returned
        powerscale_module_mock.protocol_api.get_s3_key = self._make_get_s3_key_mock(
            MockS3KeyApi.S3_GET_DETAILS_EXISTING_RESPONSE
        )

        S3KeyHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is False
        assert (
            powerscale_module_mock.module.exit_json.call_args[1]["S3_key_details"]
            == MockS3KeyApi.S3_GET_DETAILS_EXISTING_RESPONSE
        )
        powerscale_module_mock.protocol_api.get_s3_key.assert_called()

    def test_get_s3_key_details_exception(self, powerscale_module_mock):
        powerscale_module_mock.module.params = self._get_args()
        powerscale_module_mock.protocol_api.get_s3_key = MagicMock(
            side_effect=MockApiException
        )
        self.capture_fail_json_call(
            MockS3KeyApi.get_s3_key_exception_response("get_details_exception"),
            S3KeyHandler,
        )

    def test_create_s3_key_no_existing(self, powerscale_module_mock):
        powerscale_module_mock.module.params = self._get_args(
            {"user": "test-user", "access_zone": "test-zone", "state": "present"}
        )

        # key is not present
        powerscale_module_mock.get_key_details = MagicMock(
            return_value=MockS3KeyApi.S3_GET_DETAILS_NO_EXISTING_RESPONSE
        )

        # new key is created
        powerscale_module_mock.protocol_api.create_s3_key = self._make_create_s3_key_mock(
            MockS3KeyApi.S3_CREATE_KEY_RESPONSE
        )

        S3KeyHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        powerscale_module_mock.protocol_api.create_s3_key.assert_called()
        assert (
            powerscale_module_mock.module.exit_json.call_args[1]["S3_key_details"]
            == MockS3KeyApi.S3_CREATE_KEY_RESPONSE
        )

    def test_create_s3_key_replace_existing(self, powerscale_module_mock):
        existing_key_expire_time = 42
        powerscale_module_mock.module.params = self._get_args(
            {
                "user": "test-user",
                "access_zone": "test-zone",
                "state": "present",
                "generate_new_key": "always",
                "existing_key_expiry_minutes": existing_key_expire_time,
            }
        )

        # key is present
        powerscale_module_mock.get_key_details = MagicMock(
            return_value=MockS3KeyApi.S3_GET_DETAILS_EXISTING_RESPONSE
        )

        # mock call protocol api call_args
        powerscale_module_mock.isi_sdk.S3Key.return_value = {
            "existing_key_expiry_time": existing_key_expire_time
        }

        # new key is created
        powerscale_module_mock.protocol_api.create_s3_key = self._make_create_s3_key_mock(
            MockS3KeyApi.S3_CREATE_KEY_RESPONSE
        )

        S3KeyHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.isi_sdk.S3Key.call_args[1] == {
            "existing_key_expiry_time": existing_key_expire_time
        }
        powerscale_module_mock.protocol_api.create_s3_key.assert_called()
        assert powerscale_module_mock.protocol_api.create_s3_key.call_args[1][
            "s3_key"
        ] == {"existing_key_expiry_time": existing_key_expire_time}
        assert (
            powerscale_module_mock.protocol_api.create_s3_key.call_args[1]["force"]
            is True
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert (
            powerscale_module_mock.module.exit_json.call_args[1]["S3_key_details"]
            == MockS3KeyApi.S3_CREATE_KEY_RESPONSE
        )

    def test_create_s3_key_exception(self, powerscale_module_mock):
        powerscale_module_mock.module.params = self._get_args(
            {
                "state": "present",
                "generate_new_key": "always",
            }
        )

        # key is present
        powerscale_module_mock.get_key_details = MagicMock(
            return_value=MockS3KeyApi.S3_GET_DETAILS_EXISTING_RESPONSE
        )

        # raise exception
        powerscale_module_mock.protocol_api.create_s3_key = MagicMock(
            side_effect=MockApiException
        )

        self.capture_fail_json_call(
            MockS3KeyApi.get_s3_key_exception_response("create_exception"), S3KeyHandler
        )

    def test_delete_s3_key_no_existing(self, powerscale_module_mock):
        powerscale_module_mock.module.params = self._get_args(
            {"user": "test-user", "access_zone": "test-zone", "state": "absent"}
        )

        # key is not present
        powerscale_module_mock.get_key_details = MagicMock(
            return_value=MockS3KeyApi.S3_GET_DETAILS_NO_EXISTING_RESPONSE
        )

        # reset delete mock to track calls from this test only
        powerscale_module_mock.protocol_api.delete_s3_key = MagicMock()

        S3KeyHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is False
        powerscale_module_mock.protocol_api.delete_s3_key.assert_not_called()
        assert (
            powerscale_module_mock.module.exit_json.call_args[1]["S3_key_details"]
            == MockS3KeyApi.S3_GET_DETAILS_NO_EXISTING_RESPONSE
        )

    def test_delete_s3_key(self, powerscale_module_mock):
        powerscale_module_mock.module.params = self._get_args(
            {"user": "test-user", "access_zone": "test-zone", "state": "absent"}
        )

        # key is present and then absent
        powerscale_module_mock.get_key_details = MagicMock(
            side_effect=[
                MockS3KeyApi.S3_GET_DETAILS_EXISTING_RESPONSE,
                MockS3KeyApi.S3_GET_DETAILS_NO_EXISTING_RESPONSE,
            ]
        )

        # key is deleted
        powerscale_module_mock.protocol_api.delete_s3_key = MagicMock(
            return_value=MockS3KeyApi.S3_GET_DETAILS_NO_EXISTING_RESPONSE
        )

        S3KeyHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        powerscale_module_mock.protocol_api.delete_s3_key.assert_called()
        assert (
            powerscale_module_mock.module.exit_json.call_args[1]["S3_key_details"]
            == MockS3KeyApi.S3_GET_DETAILS_NO_EXISTING_RESPONSE
        )

    def test_delete_s3_key_exception(self, powerscale_module_mock):
        powerscale_module_mock.module.params = self._get_args(
            {
                "state": "absent",
            }
        )

        # key is present
        powerscale_module_mock.get_key_details = MagicMock(
            return_value=MockS3KeyApi.S3_GET_DETAILS_EXISTING_RESPONSE
        )

        # raise exception
        powerscale_module_mock.protocol_api.delete_s3_key = MagicMock(
            side_effect=MockApiException
        )

        self.capture_fail_json_call(
            MockS3KeyApi.get_s3_key_exception_response("delete_exception"), S3KeyHandler
        )

    def test_validate_params_invalid_user(self, powerscale_module_mock):
        powerscale_module_mock.module.params = self._get_args(
            {
                "user": " ",
                "access_zone": "test-zone",
                "state": "absent",
            }
        )
        self.capture_fail_json_call(
            "Invalid user provided. Provide valid user.", S3KeyHandler
        )

        powerscale_module_mock.module.params = self._get_args(
            {
                "user": "in valid",
                "access_zone": "test-zone",
                "state": "absent",
            }
        )
        self.capture_fail_json_call(
            "Invalid user provided. Provide valid user.", S3KeyHandler
        )

    def test_validate_params_invalid_access_zone(self, powerscale_module_mock):
        powerscale_module_mock.module.params = self._get_args(
            {
                "user": "test-user",
                "access_zone": " ",
                "state": "absent",
            }
        )
        self.capture_fail_json_call(
            "Invalid access_zone provided. Provide valid access_zone.", S3KeyHandler
        )

        powerscale_module_mock.module.params = self._get_args(
            {
                "user": "test-user",
                "access_zone": "in valid",
                "state": "absent",
            }
        )
        self.capture_fail_json_call(
            "Invalid access_zone provided. Provide valid access_zone.", S3KeyHandler
        )

    def test_get_s3_key_details_404(self, powerscale_module_mock):
        """Test that 404 is handled gracefully (key does not exist)."""
        powerscale_module_mock.module.params = self._get_args(
            {"user": "test-user", "access_zone": "test-zone", "state": "present"}
        )

        # API returns 404
        powerscale_module_mock.protocol_api.get_s3_key = MagicMock(
            side_effect=MockApiException(404)
        )

        # key creation is triggered after 404
        powerscale_module_mock.protocol_api.create_s3_key = self._make_create_s3_key_mock(
            MockS3KeyApi.S3_CREATE_KEY_RESPONSE
        )

        S3KeyHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        powerscale_module_mock.protocol_api.create_s3_key.assert_called()

    def test_create_s3_key_if_not_present_existing_key(self, powerscale_module_mock):
        """Test idempotency: generate_new_key=if_not_present when key already exists."""
        powerscale_module_mock.module.params = self._get_args(
            {
                "user": "test-user",
                "access_zone": "test-zone",
                "state": "present",
                "generate_new_key": "if_not_present",
            }
        )

        # key already exists - use fresh mock to avoid side_effect leakage
        powerscale_module_mock.protocol_api.get_s3_key = self._make_get_s3_key_mock(
            MockS3KeyApi.S3_GET_DETAILS_EXISTING_RESPONSE
        )

        # reset create_s3_key to a fresh mock for clean call tracking
        powerscale_module_mock.protocol_api.create_s3_key = MagicMock()

        S3KeyHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is False
        powerscale_module_mock.protocol_api.create_s3_key.assert_not_called()
        assert (
            powerscale_module_mock.module.exit_json.call_args[1]["S3_key_details"]
            == MockS3KeyApi.S3_GET_DETAILS_EXISTING_RESPONSE
        )

    def test_create_s3_key_check_mode(self, powerscale_module_mock):
        """Test that check mode does not make API calls."""
        powerscale_module_mock.module.params = self._get_args(
            {
                "user": "test-user",
                "access_zone": "test-zone",
                "state": "present",
                "generate_new_key": "always",
            }
        )
        powerscale_module_mock.module.check_mode = True

        # key is present
        powerscale_module_mock.get_key_details = MagicMock(
            return_value=MockS3KeyApi.S3_GET_DETAILS_EXISTING_RESPONSE
        )

        # reset create_s3_key to a fresh mock for clean call tracking
        powerscale_module_mock.protocol_api.create_s3_key = MagicMock()

        S3KeyHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        powerscale_module_mock.protocol_api.create_s3_key.assert_not_called()

    def test_delete_s3_key_check_mode(self, powerscale_module_mock):
        """Test that check mode does not make delete API calls."""
        powerscale_module_mock.module.params = self._get_args(
            {
                "user": "test-user",
                "access_zone": "test-zone",
                "state": "absent",
            }
        )
        powerscale_module_mock.module.check_mode = True

        # key is present
        powerscale_module_mock.get_key_details = MagicMock(
            return_value=MockS3KeyApi.S3_GET_DETAILS_EXISTING_RESPONSE
        )

        # reset delete_s3_key to a fresh mock for clean call tracking
        powerscale_module_mock.protocol_api.delete_s3_key = MagicMock()

        S3KeyHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        powerscale_module_mock.protocol_api.delete_s3_key.assert_not_called()

    def test_get_s3_key_details_generic_exception(self, powerscale_module_mock):
        """Test generic (non-API) exception during get_key_details."""
        powerscale_module_mock.module.params = self._get_args(
            {"user": "test-user", "access_zone": "test-zone", "state": "present"}
        )
        powerscale_module_mock.protocol_api.get_s3_key = MagicMock(
            side_effect=Exception("Connection error")
        )
        self.capture_fail_json_call(
            "Got error", S3KeyHandler
        )

    def test_prereqs_validation_failure(self, powerscale_module_mock):
        """Test module fails when SDK prerequisites are missing."""
        original_return = utils.validate_module_pre_reqs.return_value
        utils.validate_module_pre_reqs.return_value = (
            MockS3KeyApi.PREREQS_VALIDATE_FAILURE
        )
        try:
            obj = S3Key()
            obj.module.fail_json.assert_called_once()
            call_kwargs = obj.module.fail_json.call_args
            assert "Required SDK packages not found" in str(call_kwargs)
        finally:
            utils.validate_module_pre_reqs.return_value = original_return

    def test_get_s3_key_returns_none(self, powerscale_module_mock):
        """Test get_key_details handles None response from API."""
        powerscale_module_mock.module.params = self._get_args(
            {"user": "test-user", "access_zone": "test-zone", "state": "present"}
        )

        # API returns None instead of a key object
        powerscale_module_mock.protocol_api.get_s3_key = MagicMock(return_value=None)

        # key creation is triggered since key_details is None
        powerscale_module_mock.protocol_api.create_s3_key = self._make_create_s3_key_mock(
            MockS3KeyApi.S3_CREATE_KEY_RESPONSE
        )

        S3KeyHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        powerscale_module_mock.protocol_api.create_s3_key.assert_called()

    def test_create_s3_key_falsy_response(self, powerscale_module_mock):
        """Test create_key handles falsy response from create API."""
        powerscale_module_mock.module.params = self._get_args(
            {
                "user": "test-user",
                "access_zone": "test-zone",
                "state": "present",
                "generate_new_key": "always",
            }
        )

        # key is present
        powerscale_module_mock.get_key_details = MagicMock(
            return_value=MockS3KeyApi.S3_GET_DETAILS_EXISTING_RESPONSE
        )

        # create_s3_key returns None (falsy)
        powerscale_module_mock.protocol_api.create_s3_key = MagicMock(
            return_value=None
        )

        S3KeyHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert (
            powerscale_module_mock.module.exit_json.call_args[1]["S3_key_details"] == {}
        )

    def test_create_s3_key_with_rotation_response(self, powerscale_module_mock):
        """Test key creation with rotation preserves old key info."""
        existing_key_expire_time = 30
        powerscale_module_mock.module.params = self._get_args(
            {
                "user": "test-user",
                "access_zone": "test-zone",
                "state": "present",
                "generate_new_key": "always",
                "existing_key_expiry_minutes": existing_key_expire_time,
            }
        )

        # key is present
        powerscale_module_mock.get_key_details = MagicMock(
            return_value=MockS3KeyApi.S3_GET_DETAILS_EXISTING_RESPONSE
        )

        # mock S3Key SDK object
        powerscale_module_mock.isi_sdk.S3Key.return_value = {
            "existing_key_expiry_time": existing_key_expire_time
        }

        # new key is created with rotation response - use fresh mock
        powerscale_module_mock.protocol_api.create_s3_key = self._make_create_s3_key_mock(
            MockS3KeyApi.S3_CREATE_KEY_WITH_ROTATION_RESPONSE
        )

        S3KeyHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result["changed"] is True
        assert result["S3_key_details"]["old_key_expiry"] is not None
        assert result["S3_key_details"]["old_key_timestamp"] is not None
        assert result["S3_key_details"]["old_secret_key"] is not None
