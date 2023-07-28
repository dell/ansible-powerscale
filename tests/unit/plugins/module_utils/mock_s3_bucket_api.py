# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock Api response for Unit tests of S3 bucket module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockS3BucketeApi:
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'
    BUCKET_NAME = "sample-s3-bucket"
    PATH_1 = "/ansible-s3-bucket-fs"
    ZONE = "sample-zone"
    OWNER = "Guest"
    USER_1 = "PIERTP\\chugha"
    USER_2 = "ansible-QEsys-user1"
    GROUP = "wheel"
    LOCAL_PROVIDER_TYPE = "local"
    STATE = "present"
    EFFECTIVE_PATH = "/ifs/sample-zone/ansible-s3-bucket-fs"
    ZONE_PATH = {'summary': {'path': '/ifs/sample_zone'}}

    S3_BUCKET_COMMON_ARGS = {
        "onefs_host": "**.***.**.***",
        "s3_bucket_name": None,
        "path": None,
        "access_zone": None,
        "create_path": None,
        "description": None,
        "owner": None,
        "object_acl_policy": None,
        "acl": None,
        "state": None
    }
    GET_S3_BUCKET_RESPONSE = {
        "buckets": [{
            "access_zone": ZONE,
            "acl": [
                {
                    "grantee": {
                        "id": None,
                        "name": USER_1,
                        "type": "user"
                    },
                    "permission": "READ_ACP"
                }
            ],
            "description": "created via module",
            "id": BUCKET_NAME,
            "name": BUCKET_NAME,
            "object_acl_policy": "replace",
            "owner": OWNER,
            "path": EFFECTIVE_PATH,
            "zid": 5
        }]
    }

    CREATE_S3_OBJECT_PARAMS = {
        'acl': [{'grantee': {'name': USER_1, 'type': 'user'},
                 'permission': 'READ_ACP'}],
        'create_path': True,
        'description': 'created via module',
        'name': BUCKET_NAME,
        'object_acl_policy': 'replace',
        'owner': OWNER,
        "path": EFFECTIVE_PATH,
    }

    MODIFY_S3_OBJECT_PARAMS = {
        'acl': [{'grantee': {'name': USER_2, 'type': 'user'},
                 'permission': 'WRITE_ACP'}],
        'description': 'Updated Description',
        'name': BUCKET_NAME,
        'object_acl_policy': 'deny'
    }

    MODIFY_S3_BUCKET_RESPONSE = {"buckets": [{
        "access_zone": ZONE,
        "acl": [
            {
                "grantee": {
                    "id": None,
                    "name": USER_2,
                    "type": "user"
                },
                "permission": "WRITE_ACP"
            },
            {
                "grantee": {
                    "id": None,
                    "name": USER_1,
                    "type": "user"
                },
                "permission": "READ_ACP"
            }
        ],
        "description": "Updated Description",
        "id": BUCKET_NAME,
        "name": BUCKET_NAME,
        "object_acl_policy": "deny",
        "owner": OWNER,
        "path": EFFECTIVE_PATH,
        "zid": 5
    }]}

    USER_DETAILS = {
        "users": [
            {
                "name": USER_1,
                "uid": {
                    "name": USER_1,
                    "type": "user"
                }
            }
        ]
    }

    GROUP_DETAILS = {
        "groups": [
            {
                "name": GROUP,
                "gid": {
                    "name": GROUP,
                    "type": "group"
                }
            }
        ]
    }

    WELLKNOWN_DETAILS = {
        "wellknowns": [
            {
                "name": GROUP,
                "id": "WID:123"
            }
        ]
    }

    @staticmethod
    def get_s3_bucket_exception_response(response_type):
        if response_type == 'get_details_exception':
            return "Failed to get details of S3 bucket sample-s3-bucket with" \
                   " error SDK Error message"
        elif response_type == 'create_exception':
            return "Create S3 Bucket with sample-s3-bucket for path"
        elif response_type == 'delete_exception':
            return "Delete S3 Bucket with sample-s3-bucket in access zone:" \
                   " sample-zone failed with error: SDK Error message"
        elif response_type == 'update_exception':
            return "Modify S3 Bucket with sample-s3-bucket in access zone:" \
                   " sample-zone failed with error: SDK Error message"
        elif response_type == "update_obj_exception":
            return "Modify S3Bucket object failed with error SDK Error message"
        elif response_type == "create_obj_exception":
            return "Create S3BucketCreateParams object failed with error SDK Error message"
        elif response_type == "zone_exception":
            return "Unable to fetch base path of Access Zone sample-zone" \
                   " failed with error: SDK Error message"

    @staticmethod
    def get_error_responses(response_type):
        if response_type == 'path_error':
            return "Path is required to create the S3 bucket"
        elif response_type == 's3_name_error':
            return "Invalid s3_bucket_name provided. Provide valid" \
                   " s3_bucket_name"
        elif response_type == "system_path_error":
            return "Invalid path PATH_1, Path must start with '/'"
        elif response_type == "user_exception":
            return "Failed to get the owner id for PIERTP\\chugha in zone " \
                   "sample-zone and provider ads due to error SDK Error message"
        elif response_type == "group_exception":
            return "Failed to get the group id for group wheel in zone " \
                   "sample-zone and provider local due to error SDK Error message"
        elif response_type == "wellknown_exception":
            return "Failed to get the wellknown id for wellknown wheel due to" \
                   " error Wellknown wheel does not exist. Provide valid wellknown"
        elif response_type == "modify_path":
            return "path of the S3 bucket is not modifiable after creation."
        elif response_type == "modify_owner":
            return "owner of the S3 bucket is not modifiable after creation."
