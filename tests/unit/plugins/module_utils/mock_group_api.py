# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of Group module on PowerScale"""

from __future__ import (absolute_import, division, print_function)
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse

__metaclass__ = type


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
    CREATE_GROUP_PAYLOAD = {
        'group_name': "test_group",
        'group_id': 1000,
        'access_zone': "System",
        'provider_type': "local",
        'state': 'present'
    }
    GET_GROUP_DETAILS = {
        "dn": "CN=test_group,CN=Groups,DC=VXX267-XX",
        "dns_domain": None,
        "domain": "VXX267-XX",
        "generated_gid": False,
        "gid": {
            "id": "GID:1000",
            "name": "test_group",
            "type": "group"
        },
        "id": "test_group",
        "member_of": None,
        "members": [],
        "name": "test_group",
        "object_history": [],
        "provider": "lsa-local-provider:System",
        "sam_account_name": "test_group",
        "sid": {
            "id": "SID:S-1-5-21-3654861085-2152665011-1765289110-12281",
            "name": "test_group",
            "type": "group"
        },
        "type": "group"
    }
    GET_GROUP_MEMBERS = {
        "members": [
            {
                "id": "SID:S-1-5-21-1426242897-2739835565-3634425493-501",
                "name": "test_user",
                "type": "user"
            },
            {
                "id": "SID:S-1-5-21-1426242897-2739835565-3634425493-502",
                "name": "test_user_remove",
                "type": "user"
            }
        ]
    }

    @staticmethod
    def get_create_group_payload(id=None, name=None, users=None, user_state=None, provider_type=None):
        group_payload = MockGroupApi.CREATE_GROUP_PAYLOAD.copy()
        group_payload['group_name'] = name
        group_payload['group_id'] = id
        group_payload['users'] = []
        group_payload['user_state'] = user_state
        if users is not None:
            group_payload['users'] = users
        if provider_type:
            group_payload['provider_type'] = provider_type
        return group_payload

    @staticmethod
    def get_update_group_payload(users=None, user_state=None):
        group_payload = MockGroupApi.CREATE_GROUP_PAYLOAD.copy()
        group_payload['users'] = [{"user_name": "test_user"}, {"user_id": "1000"}]
        group_payload['user_state'] = "present-in-group"
        if user_state:
            group_payload['user_state'] = user_state
        if users is not None:
            group_payload['users'] = users
        return group_payload

    @staticmethod
    def get_delete_group_payload():
        group_payload = MockGroupApi.CREATE_GROUP_PAYLOAD.copy()
        group_payload['state'] = "absent"
        return group_payload

    @staticmethod
    def get_group_detail(provider_type=None, gid_name=None):
        group_detail = MockGroupApi.GET_GROUP_DETAILS.copy()
        if provider_type == 'nis':
            group_detail['provider'] = "lsa-nis-provider:CorpNIS"
        if gid_name:
            group_detail['gid']['name'] = gid_name
        mock_group = MagicMock()
        mock_group.name = group_detail['name']
        mock_group.to_dict.return_value = group_detail
        mock_api_response = MagicMock()
        mock_api_response.groups = [mock_group]
        return mock_api_response

    @staticmethod
    def get_user_mapping_identity():
        mock_api_response = MagicMock()
        mock_api_response.identities[0].targets[0].target.name = "test_user_1000"
        return mock_api_response

    @staticmethod
    def get_group_members_list():
        return MockSDKResponse(MockGroupApi.GET_GROUP_MEMBERS)
