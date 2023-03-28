# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock Api response for Unit tests of Group module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from mock.mock import MagicMock


class MockGroupApi:
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'
    GROUP_COMMON_ARGS = {
        'onefs_host': '**.***.**.***',
        'group_name': None,
        'group_id': None,
        'access_zone': None,
        'provider_type': None,
        'users': [],
        'user_state': None,
        'state': None
    }
    CREATE_GROUP_WITH_ID = {
        'name': 'test_group',
        'gid': 1000,
        'members': []
    }
    GET_GROUP_DETAILS = {
        "dn": "CN=sample_empty_group,CN=Groups,DC=VXX267-XX",
        "dns_domain": None,
        "domain": "VXX267-XX",
        "generated_gid": False,
        "gid": {
            "id": "GID:1000",
            "name": "sample_empty_group",
            "type": "group"
        },
        "id": "sample_empty_group",
        "member_of": None,
        "members": [],
        "name": "sample_empty_group",
        "object_history": [],
        "provider": "lsa-local-provider:System",
        "sam_account_name": "sample_empty_group",
        "sid": {
            "id": "SID:S-1-5-21-3654861085-2152665011-1765289110-12281",
            "name": "sample_empty_group",
            "type": "group"
        },
        "type": "group"
    }

    @staticmethod
    def get_create_group_id_exception_response():
        return "Create Group test_group failed with "
