# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for S3 bucket module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

utils.get_logger = MagicMock()
utils.isi_sdk = MagicMock()
PREREQS_VALIDATE = {
    "all_packages_found": True
}
utils.validate_module_pre_reqs = MagicMock(return_value=PREREQS_VALIDATE)
from ansible.module_utils import basic
basic.AnsibleModule = MagicMock()

from ansible_collections.dellemc.powerscale.plugins.modules.s3_bucket import S3Bucket
from ansible_collections.dellemc.powerscale.plugins.modules.s3_bucket import S3BucketHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_s3_bucket_api \
    import MockS3BucketeApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_fail_json \
    import FailJsonException, fail_json


class TestS3Bucket():
    s3bucket_args = MockS3BucketeApi.S3_BUCKET_COMMON_ARGS

    @pytest.fixture
    def s3bucket_module_mock(self, mocker):
        mocker.patch(MockS3BucketeApi.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        s3bucket_module_mock = S3Bucket()
        s3bucket_module_mock.module.check_mode = False
        s3bucket_module_mock.module.fail_json = fail_json
        return s3bucket_module_mock

    def capture_fail_json_call(self, error_msg, s3bucket_module_mock):
        try:
            S3BucketHandler().handle(s3bucket_module_mock, s3bucket_module_mock.module.params)
        except FailJsonException as fj_object:
            assert error_msg in fj_object.message

    def test_get_s3_bucket_details(self, s3bucket_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "state": MockS3BucketeApi.STATE
        })
        s3bucket_module_mock.module.params = self.s3bucket_args
        S3BucketHandler().handle(s3bucket_module_mock, s3bucket_module_mock.module.params)
        assert s3bucket_module_mock.module.exit_json.call_args[1]['changed'] is False
        s3bucket_module_mock.protocol_api.get_s3_bucket.assert_called()

    def test_get_s3_bucket_details_exception(self, s3bucket_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "state": MockS3BucketeApi.STATE
        })
        s3bucket_module_mock.module.params = self.s3bucket_args
        s3bucket_module_mock.protocol_api.get_s3_bucket = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_s3_bucket_exception_response(
                'get_details_exception'), s3bucket_module_mock)

    def test_create_s3_bucket(self, s3bucket_module_mock):
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
        s3bucket_module_mock.module.params = self.s3bucket_args
        s3bucket_module_mock.protocol_api.get_s3_bucket = MagicMock(
            return_value={})
        s3bucket_module_mock.zone_summary_api.get_zones_summary_zone.to_dict = MagicMock(
            return_value=MockS3BucketeApi.ZONE_PATH)
        s3bucket_module_mock.isi_sdk.S3BucketCreateParams = MagicMock(
            return_value=MockS3BucketeApi.CREATE_S3_OBJECT_PARAMS)
        S3BucketHandler().handle(s3bucket_module_mock,
                                 s3bucket_module_mock.module.params)
        assert s3bucket_module_mock.module.exit_json.call_args[1]['changed'] is True
        s3bucket_module_mock.protocol_api.create_s3_bucket.assert_called()

    def test_create_s3_bucket_exception(self, s3bucket_module_mock):
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
        s3bucket_module_mock.module.params = self.s3bucket_args
        s3bucket_module_mock.protocol_api.get_s3_bucket = MagicMock(
            return_value={})
        s3bucket_module_mock.protocol_api.create_s3_bucket = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_s3_bucket_exception_response(
                'create_exception'), s3bucket_module_mock)

    def test_modify_s3_bucket(self, s3bucket_module_mock):
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
        s3bucket_module_mock.module.params = self.s3bucket_args
        s3bucket_module_mock.get_bucket_details = MagicMock(
            return_value=MockS3BucketeApi.GET_S3_BUCKET_RESPONSE["buckets"][0])
        s3bucket_module_mock.auth_api.get_auth_user.to_dict = MagicMock(
            return_value=MockS3BucketeApi.USER_DETAILS)
        s3bucket_module_mock.auth_api.get_auth_group.to_dict = MagicMock(
            return_value=MockS3BucketeApi.GROUP_DETAILS)
        s3bucket_module_mock.isi_sdk.S3Bucket = MagicMock(
            return_value=MockS3BucketeApi.MODIFY_S3_OBJECT_PARAMS)
        S3BucketHandler().handle(s3bucket_module_mock,
                                 s3bucket_module_mock.module.params)
        assert s3bucket_module_mock.module.exit_json.call_args[1]['changed'] is True
        s3bucket_module_mock.protocol_api.update_s3_bucket.assert_called()

    def test_modify_s3_bucket_remove_acl(self, s3bucket_module_mock):
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
        s3bucket_module_mock.module.params = self.s3bucket_args
        s3bucket_module_mock.get_bucket_details = MagicMock(
            return_value=MockS3BucketeApi.MODIFY_S3_BUCKET_RESPONSE["buckets"][0])
        s3bucket_module_mock.isi_sdk.S3Bucket = MagicMock(
            return_value=MockS3BucketeApi.MODIFY_S3_OBJECT_PARAMS)
        S3BucketHandler().handle(s3bucket_module_mock,
                                 s3bucket_module_mock.module.params)
        assert s3bucket_module_mock.module.exit_json.call_args[1]['changed'] is True
        s3bucket_module_mock.protocol_api.update_s3_bucket.assert_called()

    def test_modify_s3_bucket_exception(self, s3bucket_module_mock):
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
        s3bucket_module_mock.module.params = self.s3bucket_args
        s3bucket_module_mock.get_bucket_details = MagicMock(
            return_value=MockS3BucketeApi.GET_S3_BUCKET_RESPONSE["buckets"][0])
        s3bucket_module_mock.isi_sdk.S3Bucket = MagicMock(
            return_value=MockS3BucketeApi.MODIFY_S3_OBJECT_PARAMS)
        s3bucket_module_mock.protocol_api.update_s3_bucket = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_s3_bucket_exception_response(
                'update_exception'), s3bucket_module_mock)

    def test_modify_s3_bucket_obj_exception(self, s3bucket_module_mock):
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
        s3bucket_module_mock.module.params = self.s3bucket_args
        s3bucket_module_mock.get_bucket_details = MagicMock(
            return_value=MockS3BucketeApi.GET_S3_BUCKET_RESPONSE["buckets"][0])
        s3bucket_module_mock.isi_sdk.S3Bucket = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_s3_bucket_exception_response(
                'update_obj_exception'), s3bucket_module_mock)

    def test_create_s3_bucket_obj_exception(self, s3bucket_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "path": MockS3BucketeApi.PATH_1,
            "access_zone": MockS3BucketeApi.ZONE,
            "create_path": True,
            "owner": MockS3BucketeApi.OWNER,
            "state": MockS3BucketeApi.STATE
        })
        s3bucket_module_mock.module.params = self.s3bucket_args
        s3bucket_module_mock.protocol_api.get_s3_bucket = MagicMock(
            return_value={})
        s3bucket_module_mock.zone_summary_api.get_zones_summary_zone.to_dict = MagicMock(
            return_value=MockS3BucketeApi.ZONE_PATH)
        s3bucket_module_mock.isi_sdk.S3BucketCreateParams = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_s3_bucket_exception_response(
                'create_obj_exception'), s3bucket_module_mock)

    def test_delete_s3_bucket(self, s3bucket_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "access_zone": MockS3BucketeApi.ZONE,
            "state": "absent"
        })
        s3bucket_module_mock.module.params = self.s3bucket_args
        s3bucket_module_mock.get_bucket_details = MagicMock(
            return_value=MockS3BucketeApi.MODIFY_S3_BUCKET_RESPONSE["buckets"][0])
        S3BucketHandler().handle(s3bucket_module_mock,
                                 s3bucket_module_mock.module.params)
        assert s3bucket_module_mock.module.exit_json.call_args[1]['changed'] is True
        s3bucket_module_mock.protocol_api.delete_s3_bucket.assert_called()

    def test_delete_s3_bucket_exception(self, s3bucket_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "access_zone": MockS3BucketeApi.ZONE,
            "state": "absent"
        })
        s3bucket_module_mock.module.params = self.s3bucket_args
        s3bucket_module_mock.get_bucket_details = MagicMock(
            return_value=MockS3BucketeApi.MODIFY_S3_BUCKET_RESPONSE["buckets"][0])
        s3bucket_module_mock.protocol_api.delete_s3_bucket = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_s3_bucket_exception_response(
                'delete_exception'), s3bucket_module_mock)

    def test_s3_bucket_zone_exception(self, s3bucket_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "path": MockS3BucketeApi.PATH_1,
            "access_zone": MockS3BucketeApi.ZONE,
            "create_path": True,
            "owner": MockS3BucketeApi.OWNER,
            "state": MockS3BucketeApi.STATE
        })
        s3bucket_module_mock.module.params = self.s3bucket_args
        s3bucket_module_mock.protocol_api.get_s3_bucket = MagicMock(
            return_value={})
        s3bucket_module_mock.zone_summary_api.get_zones_summary_zone = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_s3_bucket_exception_response(
                'zone_exception'), s3bucket_module_mock)

    def test_create_s3_bucket_path_exception(self, s3bucket_module_mock):
        MockApiException.status = '404'
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "path": None,
            "state": MockS3BucketeApi.STATE
        })
        s3bucket_module_mock.module.params = self.s3bucket_args
        s3bucket_module_mock.protocol_api.get_s3_bucket = MagicMock(
            return_value={})
        self.capture_fail_json_call(
            MockS3BucketeApi.get_error_responses(
                'path_error'), s3bucket_module_mock)

    def test_get_s3_bucket_name_exception(self, s3bucket_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": " ",
            "state": MockS3BucketeApi.STATE
        })
        s3bucket_module_mock.module.params = self.s3bucket_args
        s3bucket_module_mock.protocol_api.get_s3_bucket = MagicMock(
            return_value={})
        self.capture_fail_json_call(
            MockS3BucketeApi.get_error_responses(
                's3_name_error'), s3bucket_module_mock)

    def test_s3_bucket_system_zone_path_exception(self, s3bucket_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "path": "PATH_1",
            "access_zone": "system",
            "create_path": True,
            "owner": MockS3BucketeApi.OWNER,
            "state": MockS3BucketeApi.STATE
        })
        s3bucket_module_mock.module.params = self.s3bucket_args
        s3bucket_module_mock.protocol_api.get_s3_bucket = MagicMock(
            return_value={})
        s3bucket_module_mock.zone_summary_api.get_zones_summary_zone = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_error_responses(
                'system_path_error'), s3bucket_module_mock)

    def test_get_user_exception(self, s3bucket_module_mock):
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
        s3bucket_module_mock.module.params = self.s3bucket_args
        s3bucket_module_mock.protocol_api.get_s3_bucket = MagicMock(
            return_value={})
        s3bucket_module_mock.auth_api.get_auth_user = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_error_responses(
                'user_exception'), s3bucket_module_mock)

    def test_get_group_exception(self, s3bucket_module_mock):
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
        s3bucket_module_mock.module.params = self.s3bucket_args
        s3bucket_module_mock.protocol_api.get_s3_bucket = MagicMock(
            return_value={})
        s3bucket_module_mock.auth_api.get_auth_group = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_error_responses(
                'group_exception'), s3bucket_module_mock)

    def test_modify_s3_bucket_wellknowns(self, s3bucket_module_mock):
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
        s3bucket_module_mock.module.params = self.s3bucket_args
        s3bucket_module_mock.get_bucket_details = MagicMock(
            return_value=MockS3BucketeApi.GET_S3_BUCKET_RESPONSE["buckets"][0])
        s3bucket_module_mock.auth_api.get_auth_wellknowns.to_dict = MagicMock(
            return_value=MockS3BucketeApi.WELLKNOWN_DETAILS)
        s3bucket_module_mock.auth_api.get_auth_wellknown.to_dict = MagicMock(
            return_value=MockS3BucketeApi.WELLKNOWN_DETAILS)
        s3bucket_module_mock.isi_sdk.S3Bucket = MagicMock(
            return_value=MockS3BucketeApi.MODIFY_S3_OBJECT_PARAMS)
        self.capture_fail_json_call(
            MockS3BucketeApi.get_error_responses(
                'wellknown_exception'), s3bucket_module_mock)

    def test_s3_bucket_path_modify_exception(self, s3bucket_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "path": "/PATH_1",
            "access_zone": MockS3BucketeApi.ZONE,
            "create_path": True,
            "state": MockS3BucketeApi.STATE
        })
        s3bucket_module_mock.module.params = self.s3bucket_args
        s3bucket_module_mock.get_bucket_details = MagicMock(
            return_value=MockS3BucketeApi.GET_S3_BUCKET_RESPONSE["buckets"][0])
        self.capture_fail_json_call(
            MockS3BucketeApi.get_error_responses(
                'modify_path'), s3bucket_module_mock)

    def test_s3_bucket_owner_modify_exception(self, s3bucket_module_mock):
        self.s3bucket_args.update({
            "s3_bucket_name": MockS3BucketeApi.BUCKET_NAME,
            "access_zone": MockS3BucketeApi.ZONE,
            "owner": MockS3BucketeApi.USER_2,
            "state": MockS3BucketeApi.STATE
        })
        s3bucket_module_mock.module.params = self.s3bucket_args
        s3bucket_module_mock.get_bucket_details = MagicMock(
            return_value=MockS3BucketeApi.GET_S3_BUCKET_RESPONSE["buckets"][0])
        self.capture_fail_json_call(
            MockS3BucketeApi.get_error_responses(
                'modify_owner'), s3bucket_module_mock)
