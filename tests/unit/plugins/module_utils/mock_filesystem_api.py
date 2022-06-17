# Copyright:  (c) 2022,  Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http: //www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock Api response for Unit tests of filesystem module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockFileSystemApi:
    FILE_SYSTEM_MODULE_ARGS = {
        'unispherehost': '**.***.**.***',
        'path': None,
        'access_zone': None,
        'owner': None,
        'group': None,
        'access_control': None,
        'recursive': None,
        'recursive_force_delete': None,
        'quota': None,
        'state': None
    }

    @staticmethod
    def delete_file_system_response(error):
        return "Deletion of Filesystem"

    @staticmethod
    def get_acl_response():
        return {'acl': [
            {
                "accessrights": [
                    "std_read_dac",
                    "std_synchronize",
                    "dir_read_attr"
                ],
                "accesstype": "allow",
                "inherit_flags": [],
                "trustee": {
                    "id": "id:2000",
                    "name": "test_group_1",
                    "type": "group"
                }
            }],
            "authoritative": "acl",
            "group": {
                "id": "id:2000",
                "name": "test_group_1",
                "type": "group"},
            "mode": "0000",
            "owner": {
                "id": "id:2001",
                "name": "ansible_test_user1",
                "type": "user"}
        }

    @staticmethod
    def get_acl_validation_error():
        return "Please specify access_rights or inherit_flags to set ACL"

    @staticmethod
    def file_system_create_quota_response(error):
        return "Creation of Quota update param failed with error"

    @staticmethod
    def file_system_update_quota_response(error):
        return "Modification of Quota on path"
