# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of Group module on PowerScale"""

from __future__ import (absolute_import, division, print_function)
import copy
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
        'group_members': [],
        'group_member_state': None,
        'well_known_sids': [],
        'well_known_sid_state': None,
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
    # Mirrors ProvidersSummary -> provider_instances[] from the PowerScale SDK.
    # Each instance carries the bare provider ``type`` (local, file, ldap, ads,
    # nis) alongside the zone it is configured in, which is what FR-7 validates.
    GET_PROVIDERS_SUMMARY = {
        "provider_instances": [
            {
                "groupnet": "groupnet0",
                "id": "lsa-local-provider:System",
                "name": "System",
                "status": "active",
                "type": "local",
                "zone_name": "System"
            },
            {
                "groupnet": "groupnet0",
                "id": "lsa-file-provider:System",
                "name": "System",
                "status": "active",
                "type": "file",
                "zone_name": "System"
            },
            {
                "groupnet": "groupnet0",
                "id": "lsa-ldap-provider:example.org",
                "name": "example.org",
                "status": "online",
                "type": "ldap",
                "zone_name": "System"
            }
        ]
    }
    # Mirrors ClusterConfig -> onefs_version. ``release`` is a dotted string such
    # as "9.13.0.0"; FR-8 compares it against the 9.11.0 minimum.
    GET_CLUSTER_CONFIG = {
        "onefs_version": {
            "build": "B_MAIN_0000(RELEASE)",
            "release": "9.13.0.0",
            "revision": "1234567890",
            "type": "Isilon OneFS",
            "version": "Isilon OneFS v9.13.0.0"
        }
    }

    # Mirrors AuthUser response from ``AuthApi.get_auth_user()``. Each entry
    # has the fields consumed by ``_resolve_member_id()``: ``uid``, ``sid``,
    # and ``name``.
    GET_AUTH_USER_LOCAL = {
        "users": [
            {
                "dn": "CN=test_user,CN=Users,DC=VXX267-XX",
                "dns_domain": None,
                "domain": "VXX267-XX",
                "name": "test_user",
                "provider": "lsa-local-provider:System",
                "uid": {
                    "id": "UID:1000",
                    "name": "test_user",
                    "type": "user"
                },
                "sid": {
                    "id": "SID:S-1-5-21-1426242897-2739835565-3634425493-501",
                    "name": "test_user",
                    "type": "user"
                },
                "type": "user"
            }
        ]
    }
    GET_AUTH_USER_LDAP = {
        "users": [
            {
                "dn": "uid=ldap_user,ou=People,dc=example,dc=org",
                "dns_domain": None,
                "domain": "LDAP_DOMAIN",
                "name": "ldap_user",
                "provider": "lsa-ldap-provider:example.org",
                "uid": {
                    "id": "UID:50001",
                    "name": "ldap_user",
                    "type": "user"
                },
                "sid": {
                    "id": "SID:S-1-5-21-9999999999-8888888888-7777777777-50001",
                    "name": "ldap_user",
                    "type": "user"
                },
                "type": "user"
            }
        ]
    }
    # Mixed group members: one local and one LDAP member, as returned by
    # ``list_group_members``. Used to test cross-provider membership.
    GET_GROUP_MEMBERS_MIXED = {
        "members": [
            {
                "id": "SID:S-1-5-21-1426242897-2739835565-3634425493-501",
                "name": "test_user",
                "type": "user"
            },
            {
                "id": "SID:S-1-5-21-9999999999-8888888888-7777777777-50001",
                "name": "ldap_user",
                "type": "user"
            }
        ]
    }

    # Mirrors the response from ``GET /platform/1/auth/wellknowns``.
    # Includes the ER table SIDs plus edge cases (special characters, long
    # names) per the spec.
    GET_WELLKNOWNS = {
        "wellknowns": [
            {
                "gid": None,
                "name": "Everyone",
                "sid": "S-1-1-0",
                "uid": None
            },
            {
                "gid": None,
                "name": "Creator Owner",
                "sid": "S-1-3-0",
                "uid": None
            },
            {
                "gid": None,
                "name": "Authenticated Users",
                "sid": "S-1-5-11",
                "uid": None
            },
            {
                "gid": None,
                "name": "Batch",
                "sid": "S-1-5-3",
                "uid": None
            },
            {
                "gid": None,
                "name": "NT AUTHORITY\\INTERACTIVE",
                "sid": "S-1-5-4",
                "uid": None
            },
            {
                "gid": None,
                "name": "This Organization",
                "sid": "S-1-5-15",
                "uid": None
            }
        ]
    }

    # Auth group responses for resolve_group_id() — mirrors the response from
    # ``GET /platform/1/auth/groups/{v1AuthGroupId}`` for child group
    # resolution across all five provider types.
    GET_AUTH_GROUP_LOCAL = {
        "groups": [
            {
                "dn": "CN=child_local_grp,CN=Groups,DC=VXX267-XX",
                "name": "child_local_grp",
                "provider": "lsa-local-provider:System",
                "gid": {"id": "GID:2001", "name": "child_local_grp", "type": "group"},
                "sid": {
                    "id": "SID:S-1-5-21-1111111111-2222222222-3333333333-2001",
                    "name": "child_local_grp", "type": "group"
                },
                "type": "group"
            }
        ]
    }
    GET_AUTH_GROUP_ADS = {
        "groups": [
            {
                "dn": "CN=ad_child_grp,CN=Groups,DC=CORP,DC=EXAMPLE,DC=COM",
                "name": "CORP\\ad_child_grp",
                "provider": "lsa-activedirectory-provider:CORP.EXAMPLE.COM",
                "gid": {"id": "GID:3001", "name": "CORP\\ad_child_grp", "type": "group"},
                "sid": {
                    "id": "SID:S-1-5-21-4444444444-5555555555-6666666666-3001",
                    "name": "CORP\\ad_child_grp", "type": "group"
                },
                "type": "group"
            }
        ]
    }
    GET_AUTH_GROUP_LDAP = {
        "groups": [
            {
                "dn": "cn=ldap_child_grp,ou=Groups,dc=example,dc=org",
                "name": "ldap_child_grp",
                "provider": "lsa-ldap-provider:example.org",
                "gid": {"id": "GID:4001", "name": "ldap_child_grp", "type": "group"},
                "sid": {
                    "id": "SID:S-1-5-21-7777777777-8888888888-9999999999-4001",
                    "name": "ldap_child_grp", "type": "group"
                },
                "type": "group"
            }
        ]
    }
    GET_AUTH_GROUP_NIS = {
        "groups": [
            {
                "name": "nis_child_grp",
                "provider": "lsa-nis-provider:CorpNIS",
                "gid": {"id": "GID:5001", "name": "nis_child_grp", "type": "group"},
                "sid": {
                    "id": "SID:S-1-5-21-1010101010-2020202020-3030303030-5001",
                    "name": "nis_child_grp", "type": "group"
                },
                "type": "group"
            }
        ]
    }
    GET_AUTH_GROUP_FILE = {
        "groups": [
            {
                "name": "file_child_grp",
                "provider": "lsa-file-provider:System",
                "gid": {"id": "GID:6001", "name": "file_child_grp", "type": "group"},
                "sid": {
                    "id": "SID:S-1-5-21-4040404040-5050505050-6060606060-6001",
                    "name": "file_child_grp", "type": "group"
                },
                "type": "group"
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
    def get_update_group_payload(users=None, user_state=None, provider_type=None,
                                 access_zone=None):
        group_payload = MockGroupApi.CREATE_GROUP_PAYLOAD.copy()
        group_payload['users'] = [{"user_name": "test_user"}, {"user_id": "1000"}]
        group_payload['user_state'] = "present-in-group"
        if user_state:
            group_payload['user_state'] = user_state
        if users is not None:
            group_payload['users'] = users
        if provider_type:
            group_payload['provider_type'] = provider_type
        if access_zone:
            group_payload['access_zone'] = access_zone
        return group_payload

    @staticmethod
    def get_delete_group_payload():
        group_payload = MockGroupApi.CREATE_GROUP_PAYLOAD.copy()
        group_payload['state'] = "absent"
        return group_payload

    @staticmethod
    def get_group_detail(provider_type=None, gid_name=None):
        group_detail = copy.deepcopy(MockGroupApi.GET_GROUP_DETAILS)
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

    @staticmethod
    def get_providers_summary(provider_types=None, zone="System"):
        """Build a ProvidersSummary response.

        :param provider_types: bare provider types to expose (e.g.
            ``['local', 'ldap']``). Defaults to the full fixture set
            (local, file, ldap).
        :param zone: access zone reported on every provider instance.
        """
        instances = copy.deepcopy(
            MockGroupApi.GET_PROVIDERS_SUMMARY['provider_instances'])
        if provider_types is not None:
            instances = [i for i in instances if i['type'] in provider_types]
        for instance in instances:
            instance['zone_name'] = zone
        return MockSDKResponse({"provider_instances": instances})

    @staticmethod
    def get_cluster_config(release="9.13.0.0"):
        """Build a ClusterConfig response carrying the given OneFS release."""
        config = copy.deepcopy(MockGroupApi.GET_CLUSTER_CONFIG)
        config['onefs_version']['release'] = release
        return MockSDKResponse(config)

    @staticmethod
    def get_auth_user_response(provider="local"):
        """Build a single-user auth response.

        :param provider: ``'local'`` or ``'ldap'`` — selects the fixture.
            Pass ``None`` to return an empty user list (unresolvable user).
        """
        if provider is None:
            return MockSDKResponse({"users": []})
        fixture = (MockGroupApi.GET_AUTH_USER_LOCAL if provider == "local"
                   else MockGroupApi.GET_AUTH_USER_LDAP)
        return MockSDKResponse(copy.deepcopy(fixture))

    @staticmethod
    def get_group_members_mixed():
        """Return a member list containing both local and LDAP members."""
        return MockSDKResponse(copy.deepcopy(MockGroupApi.GET_GROUP_MEMBERS_MIXED))

    @staticmethod
    def get_wellknowns_response():
        """Build the well-known SIDs response from ``GET /platform/1/auth/wellknowns``."""
        return MockSDKResponse(copy.deepcopy(MockGroupApi.GET_WELLKNOWNS))

    @staticmethod
    def get_auth_group_response(provider="local"):
        """Build a single-group auth response for resolve_group_id().

        :param provider: one of ``'local'``, ``'ads'``, ``'ldap'``, ``'nis'``,
            ``'file'``. Pass ``None`` to return an empty group list
            (unresolvable group).
        """
        if provider is None:
            return MockSDKResponse({"groups": []})
        fixtures = {
            "local": MockGroupApi.GET_AUTH_GROUP_LOCAL,
            "ads": MockGroupApi.GET_AUTH_GROUP_ADS,
            "ldap": MockGroupApi.GET_AUTH_GROUP_LDAP,
            "nis": MockGroupApi.GET_AUTH_GROUP_NIS,
            "file": MockGroupApi.GET_AUTH_GROUP_FILE,
        }
        fixture = fixtures.get(provider, MockGroupApi.GET_AUTH_GROUP_LOCAL)
        return MockSDKResponse(copy.deepcopy(fixture))

    @staticmethod
    def get_update_group_payload_with_group_members(
            group_members=None, group_member_state=None, **kwargs):
        """Build a payload that exercises the ``group_members`` parameter."""
        payload = MockGroupApi.CREATE_GROUP_PAYLOAD.copy()
        payload['users'] = []
        payload['user_state'] = None
        payload['group_members'] = group_members or []
        payload['group_member_state'] = group_member_state
        payload['well_known_sids'] = []
        payload['well_known_sid_state'] = None
        payload.update(kwargs)
        return payload

    @staticmethod
    def get_update_group_payload_with_wellknown_sids(
            well_known_sids=None, well_known_sid_state=None, **kwargs):
        """Build a payload that exercises the ``well_known_sids`` parameter."""
        payload = MockGroupApi.CREATE_GROUP_PAYLOAD.copy()
        payload['users'] = []
        payload['user_state'] = None
        payload['group_members'] = []
        payload['group_member_state'] = None
        payload['well_known_sids'] = well_known_sids or []
        payload['well_known_sid_state'] = well_known_sid_state
        payload.update(kwargs)
        return payload
