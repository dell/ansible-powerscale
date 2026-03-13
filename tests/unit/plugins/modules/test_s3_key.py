# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for S3 Key module on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

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

    def test_get_s3_key_details(self, powerscale_module_mock):
        # set module params
        powerscale_module_mock.module.params = self.s3_key_args

        # existing key details are returned
        s3_key_obj_mock = MagicMock()
        keys_mock = MagicMock()
        keys_mock.to_dict.return_value = MockS3KeyApi.S3_GET_DETAILS_EXISTING_RESPONSE
        s3_key_obj_mock.keys = keys_mock
        powerscale_module_mock.protocol_api.get_s3_key.return_value = s3_key_obj_mock

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
        powerscale_module_mock.module.params = self.s3_key_args
        powerscale_module_mock.protocol_api.get_s3_key = MagicMock(
            side_effect=MockApiException
        )
        self.capture_fail_json_call(
            MockS3KeyApi.get_s3_key_exception_response("get_details_exception"),
            S3KeyHandler,
        )

    def test_create_s3_key_no_existing(self, powerscale_module_mock):
        # set module params
        self.s3_key_args.update(
            {"user": "test-user", "access_zone": "test-zone", "state": "present"}
        )
        powerscale_module_mock.module.params = self.s3_key_args

        # key is not present
        powerscale_module_mock.get_key_details = MagicMock(
            return_value=MockS3KeyApi.S3_GET_DETAILS_NO_EXISTING_RESPONSE
        )

        # new key is created
        s3_key_obj_mock = MagicMock()
        keys_mock = MagicMock()
        keys_mock.to_dict.return_value = MockS3KeyApi.S3_CREATE_KEY_RESPONSE
        s3_key_obj_mock.keys = keys_mock
        powerscale_module_mock.protocol_api.create_s3_key.return_value = s3_key_obj_mock

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
        # set module params
        existing_key_expire_time = 42
        self.s3_key_args.update(
            {
                "user": "test-user",
                "access_zone": "test-zone",
                "state": "present",
                "generate_new_key": "always",
                "existing_key_expiry_minutes": existing_key_expire_time,
            }
        )
        powerscale_module_mock.module.params = self.s3_key_args

        # key is present
        powerscale_module_mock.get_key_details = MagicMock(
            return_value=MockS3KeyApi.S3_GET_DETAILS_EXISTING_RESPONSE
        )

        # mock call protocol api call_args
        powerscale_module_mock.isi_sdk.S3Key.return_value = {
            "existing_key_expiry_time": existing_key_expire_time
        }

        # new key is created
        s3_key_obj_mock = MagicMock()
        keys_mock = MagicMock()
        keys_mock.to_dict.return_value = MockS3KeyApi.S3_CREATE_KEY_RESPONSE
        s3_key_obj_mock.keys = keys_mock
        powerscale_module_mock.protocol_api.create_s3_key.return_value = s3_key_obj_mock

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
        # set module params
        self.s3_key_args.update(
            {
                "state": "present",
                "generate_new_key": "always",
            }
        )
        powerscale_module_mock.module.params = self.s3_key_args

        # key is present
        powerscale_module_mock.get_key_details = MagicMock(
            return_value=MockS3KeyApi.S3_GET_DETAILS_EXISTING_RESPONSE
        )

        # raise execption
        powerscale_module_mock.protocol_api.create_s3_key = MagicMock(
            side_effect=MockApiException
        )

        self.capture_fail_json_call(
            MockS3KeyApi.get_s3_key_exception_response("create_exception"), S3KeyHandler
        )

    def test_delete_s3_key_no_existing(self, powerscale_module_mock):
        # set module params
        self.s3_key_args.update(
            {"user": "test-user", "access_zone": "test-zone", "state": "absent"}
        )
        powerscale_module_mock.module.params = self.s3_key_args

        # key is not present
        powerscale_module_mock.get_key_details = MagicMock(
            return_value=MockS3KeyApi.S3_GET_DETAILS_NO_EXISTING_RESPONSE
        )

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
        # set module params
        self.s3_key_args.update(
            {"user": "test-user", "access_zone": "test-zone", "state": "absent"}
        )
        powerscale_module_mock.module.params = self.s3_key_args

        # key is present and then absent
        powerscale_module_mock.get_key_details = MagicMock(
            side_effect=[
                MockS3KeyApi.S3_GET_DETAILS_EXISTING_RESPONSE,
                MockS3KeyApi.S3_GET_DETAILS_NO_EXISTING_RESPONSE,
            ]
        )

        # key is deleted
        powerscale_module_mock.protocol_api.delete_s3_key.return_value = (
            MockS3KeyApi.S3_GET_DETAILS_NO_EXISTING_RESPONSE
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
        # set module params
        self.s3_key_args.update(
            {
                "state": "absent",
            }
        )
        powerscale_module_mock.module.params = self.s3_key_args

        # key is present
        powerscale_module_mock.get_key_details = MagicMock(
            return_value=MockS3KeyApi.S3_GET_DETAILS_EXISTING_RESPONSE
        )

        # raise execption
        powerscale_module_mock.protocol_api.delete_s3_key = MagicMock(
            side_effect=MockApiException
        )

        self.capture_fail_json_call(
            MockS3KeyApi.get_s3_key_exception_response("delete_exception"), S3KeyHandler
        )

    def test_validate_params_invalid_user(self, powerscale_module_mock):
        self.s3_key_args.update(
            {
                "user": " ",
                "access_zone": "test-zone",
                "state": "absent",
            }
        )
        powerscale_module_mock.module.params = self.s3_key_args
        self.capture_fail_json_call(
            "Invalid user provided. Provide valid user.", S3KeyHandler
        )

        self.s3_key_args.update(
            {
                "user": "in valid",
                "access_zone": "test-zone",
                "state": "absent",
            }
        )
        powerscale_module_mock.module.params = self.s3_key_args
        self.capture_fail_json_call(
            "Invalid user provided. Provide valid user.", S3KeyHandler
        )

    def test_validate_params_invalid_access_zone(self, powerscale_module_mock):
        self.s3_key_args.update(
            {
                "user": "test-user",
                "access_zone": " ",
                "state": "absent",
            }
        )
        powerscale_module_mock.module.params = self.s3_key_args
        self.capture_fail_json_call(
            "Invalid access_zone provided. Provide valid access_zone.", S3KeyHandler
        )

        self.s3_key_args.update(
            {
                "user": "test-user",
                "access_zone": "in valid",
                "state": "absent",
            }
        )
        powerscale_module_mock.module.params = self.s3_key_args
        self.capture_fail_json_call(
            "Invalid access_zone provided. Provide valid access_zone.", S3KeyHandler
        )
