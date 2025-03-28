# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for S3 bucket module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils
from ansible.module_utils import basic

from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase

basic.AnsibleModule = MagicMock()

from ansible_collections.dellemc.powerscale.plugins.modules.s3_bucket import S3Bucket
from ansible_collections.dellemc.powerscale.plugins.modules.s3_bucket import S3BucketHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_s3_bucket_api \
    import MockS3BucketeApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException


class TestS3Bucket(PowerScaleUnitBase):
    s3bucket_args = MockS3BucketeApi.S3_BUCKET_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return S3Bucket

    def test_get_s3_bucket_details(self, powerscale_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "state": MockS3BucketeApi.STATE
        })
        powerscale_module_mock.module.params = self.s3bucket_args
        S3BucketHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False
        powerscale_module_mock.protocol_api.get_s3_bucket.assert_called()

    def test_get_s3_bucket_details_exception(self, powerscale_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "state": MockS3BucketeApi.STATE
        })
        powerscale_module_mock.module.params = self.s3bucket_args
        powerscale_module_mock.protocol_api.get_s3_bucket = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_s3_bucket_exception_response(
                'get_details_exception'), S3BucketHandler)

    def test_create_s3_bucket(self, powerscale_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "path": MockS3BucketeApi.PATH_1,
            "access_zone": MockS3BucketeApi.ZONE,
            "create_path": True,
            "owner": MockS3BucketeApi.OWNER,
            "object_acl_policy": "replace",
            "description": "description",
            "acl": [{
                "permission": "READ_ACP",
                "grantee": {
                    "name": MockS3BucketeApi.USER_1,
                    "type": "user",
                    "provider_type": "ads"
                },
                "acl_state": MockS3BucketeApi.STATE
            }],
            "state": MockS3BucketeApi.STATE
        })
        powerscale_module_mock.module.params = self.s3bucket_args
        powerscale_module_mock.protocol_api.get_s3_bucket = MagicMock(
            return_value={})
        powerscale_module_mock.zone_summary_api.get_zones_summary_zone.to_dict = MagicMock(
            return_value=MockS3BucketeApi.ZONE_PATH)
        powerscale_module_mock.isi_sdk.S3BucketCreateParams = MagicMock(
            return_value=MockS3BucketeApi.CREATE_S3_OBJECT_PARAMS)
        S3BucketHandler().handle(powerscale_module_mock,
                                 powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.create_s3_bucket.assert_called()

    def test_create_s3_bucket_exception(self, powerscale_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "path": MockS3BucketeApi.PATH_1,
            "access_zone": MockS3BucketeApi.ZONE,
            "create_path": False,
            "owner": MockS3BucketeApi.OWNER,
            "description": "description_exception",
            "state": MockS3BucketeApi.STATE
        })
        powerscale_module_mock.module.params = self.s3bucket_args
        powerscale_module_mock.protocol_api.get_s3_bucket = MagicMock(
            return_value={})
        powerscale_module_mock.protocol_api.create_s3_bucket = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_s3_bucket_exception_response(
                'create_exception'), S3BucketHandler)

    def test_modify_s3_bucket(self, powerscale_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "object_acl_policy": "deny",
            "description": "updated description",
            "acl": [
                {
                    "permission": "WRITE_ACP",
                    "grantee": {
                        "name": MockS3BucketeApi.USER_2,
                        "type": "user",
                        "provider_type": MockS3BucketeApi.LOCAL_PROVIDER_TYPE
                    },
                    "acl_state": MockS3BucketeApi.STATE
                },
                {
                    "permission": "WRITE",
                    "grantee": {
                        "name": MockS3BucketeApi.GROUP,
                        "type": "group",
                        "provider_type": MockS3BucketeApi.LOCAL_PROVIDER_TYPE
                    },
                    "acl_state": MockS3BucketeApi.STATE
                }
            ],
            "state": MockS3BucketeApi.STATE
        })
        powerscale_module_mock.module.params = self.s3bucket_args
        powerscale_module_mock.get_bucket_details = MagicMock(
            return_value=MockS3BucketeApi.GET_S3_BUCKET_RESPONSE["buckets"][0])
        powerscale_module_mock.auth_api.get_auth_user.to_dict = MagicMock(
            return_value=MockS3BucketeApi.USER_DETAILS)
        powerscale_module_mock.auth_api.get_auth_group.to_dict = MagicMock(
            return_value=MockS3BucketeApi.GROUP_DETAILS)
        powerscale_module_mock.isi_sdk.S3Bucket = MagicMock(
            return_value=MockS3BucketeApi.MODIFY_S3_OBJECT_PARAMS)
        S3BucketHandler().handle(powerscale_module_mock,
                                 powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.update_s3_bucket.assert_called()

    def test_modify_s3_bucket_remove_acl(self, powerscale_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "object_acl_policy": "replace",
            "description": "description",
            "acl": [{
                "permission": "READ_ACP",
                "grantee": {
                    "name": MockS3BucketeApi.USER_2,
                    "type": "user",
                    "provider_type": MockS3BucketeApi.LOCAL_PROVIDER_TYPE
                },
                "acl_state": "absent"
            }],
            "state": MockS3BucketeApi.STATE
        })
        powerscale_module_mock.module.params = self.s3bucket_args
        powerscale_module_mock.get_bucket_details = MagicMock(
            return_value=MockS3BucketeApi.MODIFY_S3_BUCKET_RESPONSE["buckets"][0])
        powerscale_module_mock.isi_sdk.S3Bucket = MagicMock(
            return_value=MockS3BucketeApi.MODIFY_S3_OBJECT_PARAMS)
        S3BucketHandler().handle(powerscale_module_mock,
                                 powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.update_s3_bucket.assert_called()

    def test_modify_s3_bucket_exception(self, powerscale_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "object_acl_policy": "deny",
            "description": "updated description",
            "acl": [
                {
                    "permission": "WRITE_ACP",
                    "grantee": {
                        "name": MockS3BucketeApi.USER_2,
                        "type": "user",
                        "provider_type": MockS3BucketeApi.LOCAL_PROVIDER_TYPE
                    },
                    "acl_state": MockS3BucketeApi.STATE
                }
            ],
            "state": MockS3BucketeApi.STATE
        })
        powerscale_module_mock.module.params = self.s3bucket_args
        powerscale_module_mock.get_bucket_details = MagicMock(
            return_value=MockS3BucketeApi.GET_S3_BUCKET_RESPONSE["buckets"][0])
        powerscale_module_mock.isi_sdk.S3Bucket = MagicMock(
            return_value=MockS3BucketeApi.MODIFY_S3_OBJECT_PARAMS)
        powerscale_module_mock.protocol_api.update_s3_bucket = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_s3_bucket_exception_response(
                'update_exception'), S3BucketHandler)

    def test_modify_s3_bucket_obj_exception(self, powerscale_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "object_acl_policy": "deny",
            "acl": [
                {
                    "permission": "WRITE_ACP",
                    "grantee": {
                        "name": MockS3BucketeApi.USER_2,
                        "type": "user",
                        "provider_type": MockS3BucketeApi.LOCAL_PROVIDER_TYPE
                    },
                    "acl_state": MockS3BucketeApi.STATE
                }
            ],
            "state": MockS3BucketeApi.STATE
        })
        powerscale_module_mock.module.params = self.s3bucket_args
        powerscale_module_mock.get_bucket_details = MagicMock(
            return_value=MockS3BucketeApi.GET_S3_BUCKET_RESPONSE["buckets"][0])
        powerscale_module_mock.isi_sdk.S3Bucket = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_s3_bucket_exception_response(
                'update_obj_exception'), S3BucketHandler)

    def test_create_s3_bucket_obj_exception(self, powerscale_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "path": MockS3BucketeApi.PATH_1,
            "access_zone": MockS3BucketeApi.ZONE,
            "create_path": True,
            "owner": MockS3BucketeApi.OWNER,
            "state": MockS3BucketeApi.STATE
        })
        powerscale_module_mock.module.params = self.s3bucket_args
        powerscale_module_mock.protocol_api.get_s3_bucket = MagicMock(
            return_value={})
        powerscale_module_mock.zone_summary_api.get_zones_summary_zone.to_dict = MagicMock(
            return_value=MockS3BucketeApi.ZONE_PATH)
        powerscale_module_mock.isi_sdk.S3BucketCreateParams = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_s3_bucket_exception_response(
                'create_obj_exception'), S3BucketHandler)

    def test_delete_s3_bucket(self, powerscale_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "access_zone": MockS3BucketeApi.ZONE,
            "state": "absent"
        })
        powerscale_module_mock.module.params = self.s3bucket_args
        powerscale_module_mock.get_bucket_details = MagicMock(
            return_value=MockS3BucketeApi.MODIFY_S3_BUCKET_RESPONSE["buckets"][0])
        S3BucketHandler().handle(powerscale_module_mock,
                                 powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.protocol_api.delete_s3_bucket.assert_called()

    def test_delete_s3_bucket_exception(self, powerscale_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "access_zone": MockS3BucketeApi.ZONE,
            "state": "absent"
        })
        powerscale_module_mock.module.params = self.s3bucket_args
        powerscale_module_mock.get_bucket_details = MagicMock(
            return_value=MockS3BucketeApi.MODIFY_S3_BUCKET_RESPONSE["buckets"][0])
        powerscale_module_mock.protocol_api.delete_s3_bucket = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_s3_bucket_exception_response(
                'delete_exception'), S3BucketHandler)

    def test_s3_bucket_zone_exception(self, powerscale_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "path": MockS3BucketeApi.PATH_1,
            "access_zone": MockS3BucketeApi.ZONE,
            "create_path": True,
            "owner": MockS3BucketeApi.OWNER,
            "state": MockS3BucketeApi.STATE
        })
        powerscale_module_mock.module.params = self.s3bucket_args
        powerscale_module_mock.protocol_api.get_s3_bucket = MagicMock(
            return_value={})
        powerscale_module_mock.zone_summary_api.get_zones_summary_zone = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_s3_bucket_exception_response(
                'zone_exception'), S3BucketHandler)

    def test_create_s3_bucket_path_exception(self, powerscale_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "path": None,
            "state": MockS3BucketeApi.STATE
        })
        powerscale_module_mock.module.params = self.s3bucket_args
        powerscale_module_mock.protocol_api.get_s3_bucket = MagicMock(
            return_value={})
        self.capture_fail_json_call(
            MockS3BucketeApi.get_error_responses(
                'path_error'), S3BucketHandler)

    def test_get_s3_bucket_name_exception(self, powerscale_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": " ",
            "state": MockS3BucketeApi.STATE
        })
        powerscale_module_mock.module.params = self.s3bucket_args
        powerscale_module_mock.protocol_api.get_s3_bucket = MagicMock(
            return_value={})
        self.capture_fail_json_call(
            MockS3BucketeApi.get_error_responses(
                's3_name_error'), S3BucketHandler)

    def test_s3_bucket_system_zone_path_exception(self, powerscale_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "path": "PATH_1",
            "access_zone": "system",
            "create_path": True,
            "owner": MockS3BucketeApi.OWNER,
            "state": MockS3BucketeApi.STATE
        })
        powerscale_module_mock.module.params = self.s3bucket_args
        powerscale_module_mock.protocol_api.get_s3_bucket = MagicMock(
            return_value={})
        powerscale_module_mock.zone_summary_api.get_zones_summary_zone = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_error_responses(
                'system_path_error'), S3BucketHandler)

    def test_get_user_exception(self, powerscale_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "path": MockS3BucketeApi.PATH_1,
            "access_zone": MockS3BucketeApi.ZONE,
            "owner": MockS3BucketeApi.OWNER,
            "acl": [
                {
                    "permission": "READ_ACP",
                    "grantee": {
                        "name": MockS3BucketeApi.USER_1,
                        "type": "user",
                        "provider_type": "ads"
                    },
                    "acl_state": MockS3BucketeApi.STATE
                }
            ],
            "state": MockS3BucketeApi.STATE
        })
        powerscale_module_mock.module.params = self.s3bucket_args
        powerscale_module_mock.protocol_api.get_s3_bucket = MagicMock(
            return_value={})
        powerscale_module_mock.auth_api.get_auth_user = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_error_responses(
                'user_exception'), S3BucketHandler)

    def test_get_group_exception(self, powerscale_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "path": MockS3BucketeApi.PATH_1,
            "access_zone": MockS3BucketeApi.ZONE,
            "owner": MockS3BucketeApi.OWNER,
            "acl": [
                {
                    "permission": "WRITE",
                    "grantee": {
                        "name": MockS3BucketeApi.GROUP,
                        "type": "group",
                        "provider_type": MockS3BucketeApi.LOCAL_PROVIDER_TYPE
                    },
                    "acl_state": MockS3BucketeApi.STATE
                }
            ],
            "state": MockS3BucketeApi.STATE
        })
        powerscale_module_mock.module.params = self.s3bucket_args
        powerscale_module_mock.protocol_api.get_s3_bucket = MagicMock(
            return_value={})
        powerscale_module_mock.auth_api.get_auth_group = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_error_responses(
                'group_exception'), S3BucketHandler)

    def test_modify_s3_bucket_wellknowns(self, powerscale_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "acl": [
                {
                    "permission": "WRITE_ACP",
                    "grantee": {
                        "name": MockS3BucketeApi.GROUP,
                        "type": "wellknowns",
                        "provider_type": MockS3BucketeApi.LOCAL_PROVIDER_TYPE
                    },
                    "acl_state": MockS3BucketeApi.STATE
                }
            ],
            "state": MockS3BucketeApi.STATE
        })
        powerscale_module_mock.module.params = self.s3bucket_args
        powerscale_module_mock.get_bucket_details = MagicMock(
            return_value=MockS3BucketeApi.GET_S3_BUCKET_RESPONSE["buckets"][0])
        powerscale_module_mock.auth_api.get_auth_wellknowns.to_dict = MagicMock(
            return_value=MockS3BucketeApi.WELLKNOWN_DETAILS)
        powerscale_module_mock.auth_api.get_auth_wellknown.to_dict = MagicMock(
            return_value=MockS3BucketeApi.WELLKNOWN_DETAILS)
        powerscale_module_mock.isi_sdk.S3Bucket = MagicMock(
            return_value=MockS3BucketeApi.MODIFY_S3_OBJECT_PARAMS)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_error_responses(
                'wellknown_exception'), S3BucketHandler)

    def test_s3_bucket_path_modify_exception(self, powerscale_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "path": "/PATH_1",
            "access_zone": MockS3BucketeApi.ZONE,
            "create_path": True,
            "state": MockS3BucketeApi.STATE
        })
        powerscale_module_mock.module.params = self.s3bucket_args
        powerscale_module_mock.get_bucket_details = MagicMock(
            return_value=MockS3BucketeApi.GET_S3_BUCKET_RESPONSE["buckets"][0])
        self.capture_fail_json_call(
            MockS3BucketeApi.get_error_responses(
                'modify_path'), S3BucketHandler)

    def test_s3_bucket_owner_modify_exception(self, powerscale_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "access_zone": MockS3BucketeApi.ZONE,
            "owner": MockS3BucketeApi.USER_2,
            "state": MockS3BucketeApi.STATE
        })
        powerscale_module_mock.module.params = self.s3bucket_args
        powerscale_module_mock.get_bucket_details = MagicMock(
            return_value=MockS3BucketeApi.GET_S3_BUCKET_RESPONSE["buckets"][0])
        self.capture_fail_json_call(
            MockS3BucketeApi.get_error_responses(
                'modify_owner'), S3BucketHandler)
