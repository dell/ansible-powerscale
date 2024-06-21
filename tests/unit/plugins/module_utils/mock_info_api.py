# Copyright: (c) 2021-2024, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock Api response for Unit tests of Info module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockGatherfactsApi:
    MODULE_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.info.Info.'
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'
    GATHERFACTS_COMMON_ARGS = {
        'onefs_host': '**.***.**.***',
        'access_zone': 'System',
        'scope': 'effective',
        'include_all_access_zones': False
    }
    EMPTY_GATHERSUBSET_ERROR_MSG = "Please specify gather_subset"
    EMPTY_RESULT = {
        'Attributes': [
        ],
        'AccessZones': [
        ],
        'Nodes': [
        ],
        'Providers': [
        ],
        'Users': [
        ],
        'Groups': [
        ],
        'SmbShares': [
        ],
        'Clients': [
        ],
        'NfsExports': [
        ],
        'NfsAliases': [
        ],
        'SynciqReports': [
        ],
        'SynciqTargetReports': [
        ],
        'SynciqPolicies': [
        ],
        'SynciqPerformanceRules': [
        ],
        'NetworkGroupnets': [
        ],
        'NetworkPools': [
        ],
        'NetworkRules': [
        ],
        'NetworkInterfaces': [
        ],
        'NetworkSubnets': [
        ],
        'NodePools': [
        ],
        'StoragePoolTiers': [
        ],
        'SmbOpenFiles': [
        ],
        'SynciqTargetClusterCertificate': [
        ],
        'UserMappingRules': [
        ],
        'LdapProviders': [
        ],
        'NfsZoneSettings': {},
        'NfsDefaultSettings': {},
        'NfsGlobalSettings': {},
        'SynciqGlobalSettings': {},
        's3Buckets': {},
        'SmbGlobalSettings': {},
        'SnmpSettings': {},
        'NTPServers': {},
        'EmailSettings': {},
        'ClusterIdentity': {},
        'ClusterOwner': {},
        'ServerCertificate': [],
        'support_assist_settings': {}
    }
    API = "api"
    MODULE = "module"

    @staticmethod
    def get_network_groupnets_response(response_type):
        if response_type == 'api':
            return {
                "groupnets": [
                    {
                        "description": "",
                        "dns_cache_enabled": True,
                        "dns_options": [
                        ],
                        "dns_search": [
                        ],
                        "dns_servers": [
                        ],
                        "id": "Test_GroupNet",
                        "name": "Test_GroupNet",
                        "server_side_dns_search": True,
                        "subnets": [
                        ]
                    },
                    {
                        "description": "Initial groupnet",
                        "dns_cache_enabled": True,
                        "dns_options": [
                        ],
                        "dns_search": [
                            "pie.lab.emc.com"
                        ],
                        "dns_servers": [
                            "1.1.1.1",
                            "1.1.1.1"
                        ],
                        "id": "groupnet0",
                        "name": "groupnet0",
                        "server_side_dns_search": True,
                        "subnets": [
                            "subnet0"
                        ]
                    }
                ]
            }
        elif response_type == 'module':
            return [
                {
                    'id': 'Test_GroupNet',
                    'name': 'Test_GroupNet'
                },
                {
                    'id': 'groupnet0',
                    'name': 'groupnet0'
                }
            ]
        else:
            return "Getting list of network groupnets for PowerScale: %s failed with error: SDK Error message" % (
                   MockGatherfactsApi.GATHERFACTS_COMMON_ARGS['onefs_host'])

    @staticmethod
    def get_network_pools_response(response_type):
        if response_type == 'api':
            return {
                "pools": [
                    {
                        "access_zone": "System",
                        "addr_family": "ipv4",
                        "aggregation_mode": "lacp",
                        "alloc_method": "static",
                        "description": "Initial ext-1 pool",
                        "groupnet": "groupnet0",
                        "id": "groupnet0.subnet0.pool0",
                        "ifaces": [
                            {
                                "iface": "ext-1",
                                "lnn": 1
                            }
                        ],
                        "name": "pool0",
                        "ranges": [
                            {
                                "high": "1.1.1.1",
                                "low": "1.1.1.1"
                            }
                        ],
                        "rebalance_policy": "auto",
                        "rules": [
                            "rule0"
                        ],
                        "sc_auto_unsuspend_delay": 0,
                        "sc_connect_policy": "round_robin",
                        "sc_dns_zone": "",
                        "sc_dns_zone_aliases": [
                        ],
                        "sc_failover_policy": "round_robin",
                        "sc_subnet": "",
                        "sc_suspended_nodes": [
                        ],
                        "sc_ttl": 0,
                        "static_routes": [
                        ],
                        "subnet": "subnet0"
                    }
                ]
            }
        elif response_type == 'module':
            return [
                {
                    'id': 'groupnet0.subnet0.pool0',
                    'name': 'pool0'
                }
            ]
        else:
            return "Getting list of network pools for PowerScale: %s failed with error: SDK Error message" % (
                   MockGatherfactsApi.GATHERFACTS_COMMON_ARGS['onefs_host'])

    @staticmethod
    def get_network_rules_response(response_type):
        if response_type == 'api':
            return {
                "rules": [
                    {
                        "description": "Initial ext-1 provisioning rule",
                        "groupnet": "groupnet0",
                        "id": "groupnet0.subnet0.pool0.rule0",
                        "iface": "ext-1",
                        "name": "rule0",
                        "node_type": "any",
                        "pool": "pool0",
                        "subnet": "subnet0"
                    }
                ]
            }
        elif response_type == 'module':
            return [
                {
                    'id': 'groupnet0.subnet0.pool0.rule0',
                    'name': 'rule0'
                }
            ]
        else:
            return "Getting list of network rules for PowerScale: %s failed with error: SDK Error message" % (
                   MockGatherfactsApi.GATHERFACTS_COMMON_ARGS['onefs_host'])

    @staticmethod
    def get_network_interfaces_response(response_type):
        if response_type == 'api':
            return {
                "interfaces": [
                    {
                        "flags": [],
                        "id": "3:ext-agg",
                        "ip_addrs": [],
                        "ipv4_gateway": None,
                        "ipv6_gateway": None,
                        "lnn": 3,
                        "mtu": 0,
                        "name": "ext-agg",
                        "nic_name": "lagg0",
                        "owners": [],
                        "speed": None,
                        "status": "inactive",
                        "type": "aggregated",
                        "vlans": []
                    }
                ]
            }
        elif response_type == 'module':
            return [
                {
                    "flags": [],
                    "id": "3:ext-agg",
                    "ip_addrs": [],
                    "ipv4_gateway": None,
                    "ipv6_gateway": None,
                    "lnn": 3,
                    "mtu": 0,
                    "name": "ext-agg",
                    "nic_name": "lagg0",
                    "owners": [],
                    "speed": None,
                    "status": "inactive",
                    "type": "aggregated",
                    "vlans": []
                }
            ]
        else:
            return "Getting list of network interfaces for PowerScale: %s failed with error: SDK Error message" % (
                   MockGatherfactsApi.GATHERFACTS_COMMON_ARGS['onefs_host'])

    @staticmethod
    def get_nfs_aliases_response(response_type):
        alias_1 = "/sample_alias_1"
        alias_2 = "/sample_alias_2"
        if response_type == 'api':
            return {
                "aliases": [
                    {
                        "health": "not exported",
                        "id": alias_1,
                        "name": alias_1,
                        "path": "/ifs",
                        "zone": "System"
                    },
                    {
                        "health": "path not found",
                        "id": alias_2,
                        "name": alias_2,
                        "path": "/ifs/Trisha",
                        "zone": "System"
                    }

                ]
            }
        elif response_type == 'module':
            return [
                {
                    "health": "not exported",
                    "id": alias_1,
                    "name": alias_1,
                    "path": "/ifs",
                    "zone": "System"
                },
                {
                    "health": "path not found",
                    "id": alias_2,
                    "name": alias_2,
                    "path": "/ifs/Trisha",
                    "zone": "System"
                }
            ]
        else:
            return "Getting list of NFS aliases for PowerScale: %s failed with error: SDK Error message" % (
                   MockGatherfactsApi.GATHERFACTS_COMMON_ARGS['onefs_host'])

    @staticmethod
    def get_network_subnets_response(response_type):
        if response_type == 'api':
            return {
                "subnets": [
                    {
                        "addr_family": "ipv4",
                        "base_addr": "0.0.0.0",
                        "description": "",
                        "dsr_addrs": [],
                        "gateway": "0.0.0.0",
                        "gateway_priority": 40,
                        "groupnet": "VSI",
                        "id": "VSI.Ganesh_subnet_1",
                        "mtu": 1500,
                        "name": "Ganesh_subnet_1",
                        "pools": [],
                        "prefixlen": 20,
                        "sc_service_addr": "0.0.0.0",
                        "vlan_enabled": False
                    },
                    {
                        "addr_family": "ipv4",
                        "base_addr": "1.1.1.1",
                        "description": "a sample ad",
                        "dsr_addrs": [],
                        "gateway": "1.1.1.1",
                        "gateway_priority": 30,
                        "groupnet": "VSI",
                        "id": "VSI.vsiad",
                        "mtu": 1500,
                        "name": "vsiad",
                        "pools": [],
                        "prefixlen": 21,
                        "sc_service_addr": "0.0.0.0",
                        "vlan_enabled": False
                    },
                    {
                        "addr_family": "ipv4",
                        "base_addr": "1.1.1.1",
                        "description": "Initial subnet",
                        "dsr_addrs": [],
                        "gateway": "1.1.1.1",
                        "gateway_priority": 10,
                        "groupnet": "groupnet0",
                        "id": "groupnet0.subnet0",
                        "mtu": 1500,
                        "name": "subnet0",
                        "pools": [
                            "pool0",
                            "CSI-Zone",
                            "NFS"
                        ],
                        "prefixlen": 24,
                        "sc_service_addr": "1.1.1.1",
                        "vlan_enabled": False
                    },
                    {
                        "addr_family": "ipv6",
                        "base_addr": "2620:0:170:2842::",
                        "description": "ipv6 Subnet",
                        "dsr_addrs": [],
                        "gateway": "2620:0:170:2842::1",
                        "gateway_priority": 20,
                        "groupnet": "groupnet0",
                        "id": "groupnet0.subnet1",
                        "mtu": 1500,
                        "name": "subnet1",
                        "pools": [
                            "pool1"
                        ],
                        "prefixlen": 64,
                        "sc_service_addr": "2620:0:170:2842::ff",
                        "vlan_enabled": False
                    }
                ]
            }
        elif response_type == 'module':
            return [
                {
                    'id': 'VSI.Ganesh_subnet_1',
                    'name': 'Ganesh_subnet_1'
                },
                {
                    'id': 'VSI.vsiad',
                    'name': 'vsiad'
                },
                {
                    'id': 'groupnet0.subnet0',
                    'name': 'subnet0'
                },
                {
                    'id': 'groupnet0.subnet1',
                    'name': 'subnet1'
                }
            ]
        else:
            return "Getting list of network subnets for PowerScale: %s failed with error: SDK Error message" % (
                   MockGatherfactsApi.GATHERFACTS_COMMON_ARGS['onefs_host'])

    @staticmethod
    def get_node_pool_response(response_type):
        if response_type == 'api':
            return {
                "nodepools": [
                    {
                        "can_disable_l3": True,
                        "can_enable_l3": True,
                        "health_flags": [],
                        "id": 75,
                        "l3": True,
                        "l3_status": "l3",
                        "lnns": [1, 2, 3],
                        "manual": False,
                        "name": "test_name_1",
                        "node_type_ids": [3],
                        "protection_policy": "+2d:1n",
                        "tier": "esa_tier",
                        "usage": {"avail_bytes": "1111111111111",
                                  "avail_hdd_bytes": "1111111111111",
                                  "avail_ssd_bytes": "0",
                                  "balanced": False,
                                  "free_bytes": "1111111111111",
                                  "free_hdd_bytes": "1111111111111",
                                  "free_ssd_bytes": "0",
                                  "pct_used": "11.1111",
                                  "pct_used_hdd": "11.1111",
                                  "pct_used_ssd": "0.00000",
                                  "total_bytes": "1111111111111",
                                  "total_hdd_bytes": "1111111111111",
                                  "total_ssd_bytes": "0",
                                  "usable_bytes": "1111111111111",
                                  "usable_hdd_bytes": "1111111111111",
                                  "usable_ssd_bytes": "0",
                                  "used_bytes": "11111111111111",
                                  "used_hdd_bytes": "11111111111111",
                                  "used_ssd_bytes": "0",
                                  "virtual_hot_spare_bytes": "1111111111111"}
                    }
                ]
            }
        elif response_type == 'module':
            return [
                {
                    "id": 75,
                    "name": "test_name_1"
                }
            ]
        else:
            return "Getting list of node pools for PowerScale: %s failed with error: SDK Error message" % (
                   MockGatherfactsApi.GATHERFACTS_COMMON_ARGS['onefs_host'])

    @staticmethod
    def get_storage_tier_response(response_type):
        if response_type == 'api':
            return {
                "tiers": [
                    {
                        "children": [],
                        "id": 38,
                        "lnns": [],
                        "name": "test_tier_1",
                        "node_type_ids": [],
                        "usage": {
                            "avail_bytes": "0",
                            "avail_hdd_bytes": "0",
                            "avail_ssd_bytes": "0",
                            "balanced": True,
                            "free_bytes": "0",
                            "free_hdd_bytes": "0",
                            "free_ssd_bytes": "0",
                            "pct_used": "0.00000",
                            "pct_used_hdd": "0.00000",
                            "pct_used_ssd": "0.00000",
                            "total_bytes": "0",
                            "total_hdd_bytes": "0",
                            "total_ssd_bytes": "0",
                            "usable_bytes": "0",
                            "usable_hdd_bytes": "0",
                            "usable_ssd_bytes": "0",
                            "used_bytes": "0",
                            "used_hdd_bytes": "0",
                            "used_ssd_bytes": "0",
                            "virtual_hot_spare_bytes": "0"
                        }
                    },
                    {
                        "children": [],
                        "id": 54,
                        "lnns": [],
                        "name": "test_tier_2",
                        "node_type_ids": [],
                        "usage": {
                            "avail_bytes": "0",
                            "avail_hdd_bytes": "0",
                            "avail_ssd_bytes": "0",
                            "balanced": True,
                            "free_bytes": "0",
                            "free_hdd_bytes": "0",
                            "free_ssd_bytes": "0",
                            "pct_used": "0.00000",
                            "pct_used_hdd": "0.00000",
                            "pct_used_ssd": "0.00000",
                            "total_bytes": "0",
                            "total_hdd_bytes": "0",
                            "total_ssd_bytes": "0",
                            "usable_bytes": "0",
                            "usable_hdd_bytes": "0",
                            "usable_ssd_bytes": "0",
                            "used_bytes": "0",
                            "used_hdd_bytes": "0",
                            "used_ssd_bytes": "0",
                            "virtual_hot_spare_bytes": "0"
                        }
                    },
                    {
                        "children": [
                            "test_child_1"
                        ],
                        "id": 95,
                        "lnns": [
                            1,
                            2,
                            3
                        ],
                        "name": "test_tier_3",
                        "node_type_ids": [],
                        "usage": {
                            "avail_bytes": "1111111111111",
                            "avail_hdd_bytes": "1111111111111",
                            "avail_ssd_bytes": "0",
                            "balanced": False,
                            "free_bytes": "1111111111111",
                            "free_hdd_bytes": "1111111111111",
                            "free_ssd_bytes": "0",
                            "pct_used": "91.5820",
                            "pct_used_hdd": "91.5820",
                            "pct_used_ssd": "0.00000",
                            "total_bytes": "1111111111111",
                            "total_hdd_bytes": "1111111111111",
                            "total_ssd_bytes": "0",
                            "usable_bytes": "1111111111111",
                            "usable_hdd_bytes": "1111111111111",
                            "usable_ssd_bytes": "0",
                            "used_bytes": "11111111111111",
                            "used_hdd_bytes": "11111111111111",
                            "used_ssd_bytes": "0",
                            "virtual_hot_spare_bytes": "1111111111111"
                        }
                    }],
            }
        elif response_type == 'module':
            return [
                {
                    "id": 38,
                    "name": "test_tier_1"
                },
                {
                    "id": 54,
                    "name": "test_tier_2"
                },
                {
                    "id": 95,
                    "name": "test_tier_3"
                }
            ]
        else:
            return "Getting list of storagepool tiers for PowerScale: %s failed with error: SDK Error message" % (
                   MockGatherfactsApi.GATHERFACTS_COMMON_ARGS['onefs_host'])

    @staticmethod
    def get_smb_files_response(response_type):
        if response_type == 'api':
            return {
                "openfiles": [
                    {
                        "file": "C:\\ifs\\data",
                        "id": 1880,
                        "locks": 0,
                        "permissions": [
                            "read"
                        ],
                        "user": "admin"
                    }
                ]
            }
        elif response_type == 'module':
            return [
                {
                    "file": "C:\\ifs\\data",
                    "id": 1880,
                    "locks": 0,
                    "permissions": [
                        "read"
                    ],
                    "user": "admin"
                }
            ]
        else:
            return "Getting list of smb open files for PowerScale: %s failed with error: SDK Error message" % (
                   MockGatherfactsApi.GATHERFACTS_COMMON_ARGS['onefs_host'])

    @staticmethod
    def get_user_mapping_rules_response(response_type):
        if response_type == 'api':
            return {
                'rules': {
                    'rules': [
                        {
                            'operator': 'trim',
                            'options': {
                                '_break': False,
                                'default_user': None,
                                'group': False,
                                'groups': False,
                                'user': False
                            },
                            'user1': {
                                'domain': None,
                                'user': 'test_ans_user'
                            }
                        }
                    ]
                }
            }
        elif response_type == 'module':
            return [
                {
                    'operator': 'trim',
                    'options': {
                        '_break': False,
                        'default_user': None,
                        'group': False,
                        'groups': False,
                        'user': False
                    },
                    'user1': {
                        'domain': None,
                        'user': 'test_ans_user'
                    },
                    'apply_order': 1
                }
            ]
        else:
            return "Getting list of user mapping rules for PowerScale: %s failed with error: SDK Error message" % (
                   MockGatherfactsApi.GATHERFACTS_COMMON_ARGS['onefs_host'])

    @staticmethod
    def get_ldap_details_response(response_type):
        if response_type == 'api':
            return {
                "ldap": [
                    {
                        "alternate_security_identities_attribute": "altSecurityIdentities",
                        "authentication": True,
                        "balance_servers": True,
                        "base_dn": "dc=ansildap,dc=com",
                        "bind_dn": "cn=admin,dc=ansildap,dc=com",
                        "bind_mechanism": "simple",
                        "bind_timeout": 10,
                        "certificate_authority_file": "",
                        "check_online_interval": 180,
                        "cn_attribute": "cn",
                        "create_home_directory": False,
                        "crypt_password_attribute": "",
                        "email_attribute": "mail",
                        "enabled": True,
                        "enumerate_groups": True,
                        "enumerate_users": True,
                        "findable_groups": [],
                        "findable_users": [],
                        "gecos_attribute": "gecos",
                        "gid_attribute": "gidNumber",
                        "group_base_dn": "",
                        "group_domain": "LDAP_GROUPS",
                        "group_filter": "(objectClass=posixGroup)",
                        "group_members_attribute": "memberUid",
                        "group_search_scope": "default",
                        "groupnet": "groupnet0",
                        "home_directory_template": "",
                        "homedir_attribute": "homeDirectory",
                        "id": "ansildap1",
                        "ignore_tls_errors": False,
                        "listable_groups": [],
                        "listable_users": [],
                        "login_shell": "",
                        "member_lookup_method": "default",
                        "member_of_attribute": "",
                        "name": "ansildap1",
                        "name_attribute": "uid",
                        "netgroup_base_dn": "",
                        "netgroup_filter": "(objectClass=nisNetgroup)",
                        "netgroup_members_attribute": "memberNisNetgroup",
                        "netgroup_search_scope": "default",
                        "netgroup_triple_attribute": "nisNetgroupTriple",
                        "normalize_groups": False,
                        "normalize_users": False,
                        "nt_password_attribute": "",
                        "ntlm_support": "all",
                        "provider_domain": "",
                        "require_secure_connection": False,
                        "restrict_findable": True,
                        "restrict_listable": False,
                        "search_scope": "subtree",
                        "search_timeout": 100,
                        "server_uris": [
                            "ldap://10.xx.xx.xx"
                        ],
                        "shadow_expire_attribute": "shadowExpire",
                        "shadow_flag_attribute": "shadowFlag",
                        "shadow_inactive_attribute": "shadowInactive",
                        "shadow_last_change_attribute": "shadowLastChange",
                        "shadow_max_attribute": "shadowMax",
                        "shadow_min_attribute": "shadowMin",
                        "shadow_user_filter": "(objectClass=shadowAccount)",
                        "shadow_warning_attribute": "shadowWarning",
                        "shell_attribute": "loginShell",
                        "ssh_public_key_attribute": "sshPublicKey",
                        "status": "online",
                        "system": False,
                        "tls_protocol_min": "1.2",
                        "uid_attribute": "uidNumber",
                        "unfindable_groups": [
                            "wheel",
                            "0",
                            "insightiq",
                            "15",
                            "isdmgmt",
                            "16"
                        ],
                        "unfindable_users": [
                            "root",
                            "0",
                            "insightiq",
                            "15",
                            "isdmgmt",
                            "16"
                        ],
                        "unique_group_members_attribute": "",
                        "unlistable_groups": [],
                        "unlistable_users": [],
                        "user_base_dn": "",
                        "user_domain": "LDAP_USERS",
                        "user_filter": "(objectClass=posixAccount)",
                        "user_search_scope": "default",
                        "zone_name": "System"
                    }
                ]
            }
        elif response_type == 'module':
            return [
                {
                    "alternate_security_identities_attribute": "altSecurityIdentities",
                    "authentication": True,
                    "balance_servers": True,
                    "base_dn": "dc=ansildap,dc=com",
                    "bind_dn": "cn=admin,dc=ansildap,dc=com",
                    "bind_mechanism": "simple",
                    "bind_timeout": 10,
                    "certificate_authority_file": "",
                    "check_online_interval": 180,
                    "cn_attribute": "cn",
                    "create_home_directory": False,
                    "crypt_password_attribute": "",
                    "email_attribute": "mail",
                    "enabled": True,
                    "enumerate_groups": True,
                    "enumerate_users": True,
                    "findable_groups": [],
                    "findable_users": [],
                    "gecos_attribute": "gecos",
                    "gid_attribute": "gidNumber",
                    "group_base_dn": "",
                    "group_domain": "LDAP_GROUPS",
                    "group_filter": "(objectClass=posixGroup)",
                    "group_members_attribute": "memberUid",
                    "group_search_scope": "default",
                    "groupnet": "groupnet0",
                    "home_directory_template": "",
                    "homedir_attribute": "homeDirectory",
                    "id": "ansildap1",
                    "ignore_tls_errors": False,
                    "listable_groups": [],
                    "listable_users": [],
                    "login_shell": "",
                    "member_lookup_method": "default",
                    "member_of_attribute": "",
                    "name": "ansildap1",
                    "name_attribute": "uid",
                    "netgroup_base_dn": "",
                    "netgroup_filter": "(objectClass=nisNetgroup)",
                    "netgroup_members_attribute": "memberNisNetgroup",
                    "netgroup_search_scope": "default",
                    "netgroup_triple_attribute": "nisNetgroupTriple",
                    "normalize_groups": False,
                    "normalize_users": False,
                    "nt_password_attribute": "",
                    "ntlm_support": "all",
                    "provider_domain": "",
                    "require_secure_connection": False,
                    "restrict_findable": True,
                    "restrict_listable": False,
                    "search_scope": "subtree",
                    "search_timeout": 100,
                    "server_uris": [
                        "ldap://10.xx.xx.xx"
                    ],
                    "shadow_expire_attribute": "shadowExpire",
                    "shadow_flag_attribute": "shadowFlag",
                    "shadow_inactive_attribute": "shadowInactive",
                    "shadow_last_change_attribute": "shadowLastChange",
                    "shadow_max_attribute": "shadowMax",
                    "shadow_min_attribute": "shadowMin",
                    "shadow_user_filter": "(objectClass=shadowAccount)",
                    "shadow_warning_attribute": "shadowWarning",
                    "shell_attribute": "loginShell",
                    "ssh_public_key_attribute": "sshPublicKey",
                    "status": "online",
                    "system": False,
                    "tls_protocol_min": "1.2",
                    "uid_attribute": "uidNumber",
                    "unfindable_groups": [
                        "wheel",
                        "0",
                        "insightiq",
                        "15",
                        "isdmgmt",
                        "16"
                    ],
                    "unfindable_users": [
                        "root",
                        "0",
                        "insightiq",
                        "15",
                        "isdmgmt",
                        "16"
                    ],
                    "unique_group_members_attribute": "",
                    "unlistable_groups": [],
                    "unlistable_users": [],
                    "user_base_dn": "",
                    "user_domain": "LDAP_USERS",
                    "user_filter": "(objectClass=posixAccount)",
                    "user_search_scope": "default",
                    "zone_name": "System"
                }
            ]
        else:
            return "Getting list of ldap providers for PowerScale: %s failed with error: SDK Error message" % (
                   MockGatherfactsApi.GATHERFACTS_COMMON_ARGS['onefs_host'])

    @staticmethod
    def get_smb_global_settings(response_type):
        if response_type == "api":
            return {
                "settings": {
                    'access_based_share_enum': False,
                    'dot_snap_accessible_child': True,
                    'dot_snap_accessible_root': True,
                    'dot_snap_visible_child': False,
                    'dot_snap_visible_root': True,
                }
            }
        elif response_type == "module":
            return {
                'access_based_share_enum': False,
                'dot_snap_accessible_child': True,
                'dot_snap_accessible_root': True,
                'dot_snap_visible_child': False,
                'dot_snap_visible_root': True,
            }
        else:
            return "Got error SDK Error message while getting SMB global setings details "

    @staticmethod
    def get_nfsglobal_settings(response_type):
        if response_type == "api":
            return {
                "settings": {
                    "service": True
                }
            }
        elif response_type == "module":
            return {
                "service": True
            }
        else:
            return "Getting NFS global settings for PowerScale: **.***.**.*** failed with error: SDK Error message"

    @staticmethod
    def get_snmp_settings_response(response_type):
        if response_type == "api":
            return {
                "settings": {
                    "service": True,
                    "snmp_v1_v2c_access": True,
                    "snmp_v3_access": True,
                    "snmp_v3_auth_protocol": "MD5",
                    "snmp_v3_priv_protocol": "DES",
                    "read_only_community": "readonly"
                }
            }
        elif response_type == "module":
            return {
                "service": True,
                "snmp_v1_v2c_access": True,
                "snmp_v3_access": True,
                "snmp_v3_auth_protocol": "MD5",
                "snmp_v3_priv_protocol": "DES",
                "read_only_community": "readonly"
            }
        else:
            return "Fetching SNMP settings failed with error: SDK Error message"

    @staticmethod
    def get_nfs_zone_settings(response_type):
        if response_type == "api":
            return {
                "settings": {
                    "nfsv4_replace_domain": False,
                    "zone": "System"
                }
            }
        elif response_type == "module":
            return {
                "nfsv4_replace_domain": False,
                "zone": "System"
            }
        else:
            return "Getting zone settings for PowerScale: **.***.**.*** failed with error: SDK Error message"

    @staticmethod
    def get_nfs_default_settings_response(response_type):
        if response_type == "api":
            return {
                "settings": {
                    'write_datasync_action': 'DATASYNC',
                    'write_datasync_reply': 'DATASYNC',
                }
            }
        elif response_type == "module":
            return {
                'write_datasync_action': 'DATASYNC',
                'write_datasync_reply': 'DATASYNC',
            }
        else:
            return "Fetching NFS default settings failed with error: SDK Error message"

    @staticmethod
    def get_providers_response(response_type):
        resp = [{
                "name": "ansildap1",
                }, {
                "name": "ansildap2",
                }]
        if response_type == "error":
            return "Get authentication Providers List for PowerScale cluster: **.***.**.*** failed with error: SDK Error message"
        else:
            return resp

    @staticmethod
    def get_users_response(response_type):
        resp = [{
                "name": "testuser",
                }, {
                "name": "testuser1",
                }]
        if response_type == "error":
            return "Get Users List for PowerScale cluster: **.***.**.*** and access zone: System failed with error: SDK Error message"
        else:
            return resp

    @staticmethod
    def get_groups_response(response_type):
        resp = [{
                "name": "testgroup",
                }, {
                "name": "testgroup1",
                }]
        if response_type == "error":
            return "Get Group List for PowerScale cluster: **.***.**.*** andaccess zone: System failed with error: SDK Error message"
        else:
            return resp

    @staticmethod
    def get_s3_buckets_response(response_type):
        resp = [{
                "name": "testuser",
                }, {
                "name": "testuser1",
                }]
        if response_type == "error":
            return "Fetching S3 bucket list failed with error: SDK Error message"
        else:
            return resp

    @staticmethod
    def get_smb_shares_response(response_type):
        if response_type == "module":
            return [{"id": "1", "name": "testuser"}, {
                "id": "2", "name": "testuser1",
            }]
        elif response_type == "api":
            return {"shares": [{"id": "1", "name": "testuser"}, {
                "id": "2", "name": "testuser1",
            }]}
        else:
            return "Get smb_shares list for PowerScale cluster: **.***.**.*** failed witherror: SDK Error message"

    @staticmethod
    def get_nfs_exports_response(response_type):
        if response_type == "module":
            return [{"id": "1", "paths": "testuser"}, {
                "id": "2", "paths": "testuser1",
            }]
        elif response_type == "api":
            return {"exports": [{"id": "1", "paths": "testuser"}, {
                "id": "2", "paths": "testuser1",
            }]}
        else:
            return "Get nfs_exports list for PowerScale cluster: **.***.**.*** failed witherror: SDK Error message"

    @staticmethod
    def get_attributes_response(response_type):
        cluster_config = {"name": "cluster"}
        external_ips = ["*.**.***.*", "*.**.***.*"]
        logon_msg = "logon msg"
        contact_info = "Contact Info"
        cluster_version = "9.5"
        if response_type == "error":
            return "Get Attributes List for PowerScale cluster: **.***.**.*** failed with error: SDK Error message"
        elif response_type == "module":
            return cluster_config, external_ips, logon_msg, contact_info, cluster_version
        else:
            return {"Config": cluster_config, "Contact_Info": contact_info,
                    "External_IP": {"External IPs": ','.join(external_ips)},
                    "Logon_msg": logon_msg,
                    "Cluster_Version": cluster_version}

    @staticmethod
    def get_nodes_response(response_type):
        if response_type == "error":
            return "Get Nodes List for PowerScale cluster: **.***.**.*** failed witherror: SDK Error message"
        return [{"node_name": "node1"}, {"node_name": "node2"}]

    @staticmethod
    def get_synciq_reports_response(response_type):
        if response_type == "error":
            return "Get SyncIQ Report list for PowerScale cluster: **.***.**.*** failed witherror: SDK Error message"
        elif response_type == "api":
            return {"total": 2,
                    "reports": [
                        {
                            "id": "rep1",
                            "policy_name": "Policy1"
                        },
                        {
                            "id": "rep2",
                            "policy_name": "Policy2"
                        },
                    ]
                    }
        elif response_type == "module":
            return [
                {
                    "id": "rep1",
                    "name": "Policy1"
                },
                {
                    "id": "rep2",
                    "name": "Policy2"
                },
            ]

    @staticmethod
    def get_synciq_target_reports_response(response_type):
        if response_type == "error":
            return "Get SyncIQ Target Report list for PowerScale cluster: **.***.**.*** failed witherror: SDK Error message"
        elif response_type == "api":
            return {"total": 2,
                    "reports": [
                        {
                            "id": "rep1",
                            "policy_name": "Policy1"
                        },
                        {
                            "id": "rep2",
                            "policy_name": "Policy2"
                        },
                    ]
                    }
        elif response_type == "module":
            return [
                {
                    "id": "rep1",
                    "name": "Policy1"
                },
                {
                    "id": "rep2",
                    "name": "Policy2"
                },
            ]

    @staticmethod
    def get_synciq_performance_rules_response(response_type):
        if response_type == "error":
            return "Get SyncIQ performance rules list for PowerScale cluster: **.***.**.*** failed witherror: SDK Error message"
        elif response_type == "api":
            return {
                "rules": [
                    {
                        "id": "rep1",
                        "schedule": "schedule",
                        "enabled": True,
                        "type": "bandwidth",
                        "limit": 2
                    },
                    {
                        "id": "rep1",
                        "schedule": "schedule",
                        "enabled": True,
                        "type": "cpu",
                        "limit": 4
                    },
                    {
                        "id": "rep1",
                        "schedule": "schedule",
                        "enabled": True,
                        "type": "file_count",
                        "limit": 1
                    },
                    {
                        "id": "rep1",
                        "schedule": "schedule",
                        "enabled": True,
                        "type": "worker",
                        "limit": 3
                    },
                ]
            }
        elif response_type == "module":
            return [
                {
                    "id": "rep1",
                    "schedule": "schedule",
                    "enabled": True,
                    "type": "bandwidth",
                    "limit": "2kb/s"
                },
                {
                    "id": "rep1",
                    "schedule": "schedule",
                    "enabled": True,
                    "type": "cpu",
                    "limit": "4%"
                },
                {
                    "id": "rep1",
                    "schedule": "schedule",
                    "enabled": True,
                    "type": "file_count",
                    "limit": "1files/sec"
                },
                {
                    "id": "rep1",
                    "schedule": "schedule",
                    "enabled": True,
                    "type": "worker",
                    "limit": "3%"
                },
            ]

    @staticmethod
    def get_synciq_policies_response(response_type):
        resp = [
            {
                "id": "p1",
                "name": "Policy1",
                "source_root_path": "path",
                "target_path": "target_path",
                "action": "action",
                "schedule": "schedule",
                            "enabled": True
            },
            {
                "id": "p2",
                "name": "Policy2",
                "source_root_path": "path",
                "target_path": "target_path",
                "action": "action",
                "schedule": "schedule",
                            "enabled": False
            },
        ]
        if response_type == "error":
            return "Get list of SyncIQ Policies for PowerScale: **.***.**.*** failed witherror: SDK Error message"
        if response_type == "api":
            return {
                "policies": resp
            }
        elif response_type == "module":
            return resp

    @staticmethod
    def get_synciq_target_cluster_certificates_response(response_type):
        resp = [
            {
                "id": "c1",
                "name": "cert1",
            },
            {
                "id": "c2",
                "name": "cert2",
            }
        ]
        if response_type == "error":
            return "Get list of SyncIQ target cluster certificates for PowerScale: **.***.**.*** failed witherror: SDK Error message"
        elif response_type == "api":
            return {
                "certificates": resp
            }
        else:
            return resp

    @staticmethod
    def get_access_zones_response(response_type):
        if response_type == "error":
            return "Get Access zone List for PowerScale cluster: **.***.**.*** failedwith error: SDK Error message"
        return [{"id": "1"}, {"id": "2"}]

    @staticmethod
    def get_clients_response(response_type):
        if response_type == "error":
            return "Get active clients list for PowerScale cluster: **.***.**.*** failed witherror: SDK Error message"
        elif response_type == "api":
            return {
                "client": [
                    {
                        "local_addr": "local_address1",
                        "local_name": "local_name1",
                        "remote_addr": "remote_address1",
                        "remote_name": "remote_name1",
                        "node": "node1",
                        "protocol": "protocol1",
                    },
                    {
                        "local_addr": "local_address2",
                        "local_name": "local_name2",
                        "remote_addr": "remote_address2",
                        "remote_name": "remote_name2",
                        "node": "node2",
                        "protocol": "protocol2",
                    }
                ]
            }
        elif response_type == "module":
            return [
                {
                    "local_address": "local_address1",
                    "local_name": "local_name1",
                    "remote_address": "remote_address1",
                    "remote_name": "remote_name1",
                    "node": "node1",
                    "protocol": "protocol1",
                },
                {
                    "local_address": "local_address2",
                    "local_name": "local_name2",
                    "remote_address": "remote_address2",
                    "remote_name": "remote_name2",
                    "node": "node2",
                    "protocol": "protocol2",
                }
            ]

    @staticmethod
    def get_support_assist_settings(response_type):
        if response_type == "api" or response_type == "module":
            return {
                "automatic_case_creation": False,
                "connection": {
                    "gateway_endpoints": [
                        {
                            "enabled": True,
                            "host": "XX.XX.XX.XX",
                            "port": 9443,
                            "priority": 1,
                            "use_proxy": False,
                            "validate_ssl": False
                        }
                    ],
                    "mode": "gateway",
                    "network_pools": [
                        {
                            "pool": "pool2",
                            "subnet": "subnet0"
                        }
                    ]
                },
                "connection_state": "enabled",
                "contact": {
                    "primary": {
                        "email": "abc.def@sample.com",
                        "first_name": "abc",
                        "last_name": "def",
                        "phone": "1234567890"
                    },
                    "secondary": {
                        "email": "kangD@example.com",
                        "first_name": "Daniel",
                        "last_name": "Kang",
                        "phone": "1234567891"
                    }
                },
                "enable_download": False,
                "enable_remote_support": False,
                "onefs_software_id": "ELMISL1019H4GY",
                "supportassist_enabled": True,
                "telemetry": {
                    "offline_collection_period": 60,
                    "telemetry_enabled": True,
                    "telemetry_persist": True,
                    "telemetry_threads": 10
                }
            }
        else:
            return "Got error SDK Error message while getting support assist settings details "

    @staticmethod
    def get_gather_facts_module_response(gather_subset):
        param = "module"
        subset_error_dict = {
            "nfs_global_settings": MockGatherfactsApi.get_nfsglobal_settings(param),
            "smb_global_settings": MockGatherfactsApi.get_smb_global_settings(param),
            "nfs_zone_settings": MockGatherfactsApi.get_nfs_zone_settings(param),
            "ldap": MockGatherfactsApi.get_ldap_details_response(param),
            "user_mapping_rules": MockGatherfactsApi.get_user_mapping_rules_response(param),
            "smb_files": MockGatherfactsApi.get_smb_files_response(param),
            "storagepool_tiers": MockGatherfactsApi.get_storage_tier_response('api')['tiers'],
            "node_pools": MockGatherfactsApi.get_node_pool_response('api')['nodepools'],
            "network_subnets": MockGatherfactsApi.get_network_subnets_response(param),
            "nfs_aliases": MockGatherfactsApi.get_nfs_aliases_response(param),
            "network_interfaces": MockGatherfactsApi.get_network_interfaces_response(param),
            "network_rules": MockGatherfactsApi.get_network_rules_response(param),
            "network_pools": MockGatherfactsApi.get_network_pools_response(param),
            "network_groupnets": MockGatherfactsApi.get_network_groupnets_response(param),
            "providers": MockGatherfactsApi.get_providers_response(param),
            "users": MockGatherfactsApi.get_users_response(param),
            "groups": MockGatherfactsApi.get_groups_response(param),
            "smb_shares": MockGatherfactsApi.get_smb_shares_response(param),
            "nfs_exports": MockGatherfactsApi.get_nfs_exports_response(param),
            "nfs_default_settings": MockGatherfactsApi.get_nfs_default_settings_response(param),
            "s3_buckets": MockGatherfactsApi.get_s3_buckets_response(param),
            "nodes": MockGatherfactsApi.get_nodes_response(param),
            "synciq_reports": MockGatherfactsApi.get_synciq_reports_response(param),
            "synciq_target_reports": MockGatherfactsApi.get_synciq_target_reports_response(param),
            "synciq_policies": MockGatherfactsApi.get_synciq_policies_response(param),
            "synciq_performance_rules": MockGatherfactsApi.get_synciq_performance_rules_response(param),
            "synciq_target_cluster_certificates": MockGatherfactsApi.get_synciq_target_cluster_certificates_response(param),
            "access_zones": MockGatherfactsApi.get_access_zones_response(param),
            "clients": MockGatherfactsApi.get_clients_response(param),
            "snmp_settings": MockGatherfactsApi.get_snmp_settings_response(param),
            "support_assist_settings": MockGatherfactsApi.get_support_assist_settings(param)
        }
        return subset_error_dict.get(gather_subset)

    @staticmethod
    def get_gather_facts_api_response(gather_subset):
        param = "api"
        subset_error_dict = {
            "nfs_global_settings": MockGatherfactsApi.get_nfsglobal_settings(param),
            "smb_global_settings": MockGatherfactsApi.get_smb_global_settings(param),
            "nfs_zone_settings": MockGatherfactsApi.get_nfs_zone_settings(param),
            "ldap": MockGatherfactsApi.get_ldap_details_response(param),
            "user_mapping_rules": MockGatherfactsApi.get_user_mapping_rules_response(param),
            "smb_files": MockGatherfactsApi.get_smb_files_response(param),
            "storagepool_tiers": MockGatherfactsApi.get_storage_tier_response(param),
            "node_pools": MockGatherfactsApi.get_node_pool_response(param),
            "network_subnets": MockGatherfactsApi.get_network_subnets_response(param),
            "nfs_aliases": MockGatherfactsApi.get_nfs_aliases_response(param),
            "network_interfaces": MockGatherfactsApi.get_network_interfaces_response(param),
            "network_rules": MockGatherfactsApi.get_network_rules_response(param),
            "network_pools": MockGatherfactsApi.get_network_pools_response(param),
            "network_groupnets": MockGatherfactsApi.get_network_groupnets_response(param),
            "providers": MockGatherfactsApi.get_providers_response(param),
            "users": MockGatherfactsApi.get_users_response(param),
            "groups": MockGatherfactsApi.get_groups_response(param),
            "smb_shares": MockGatherfactsApi.get_smb_shares_response(param),
            "nfs_exports": MockGatherfactsApi.get_nfs_exports_response(param),
            "nfs_default_settings": MockGatherfactsApi.get_nfs_default_settings_response(param),
            "s3_buckets": MockGatherfactsApi.get_s3_buckets_response(param),
            "nodes": MockGatherfactsApi.get_nodes_response(param),
            "synciq_reports": MockGatherfactsApi.get_synciq_reports_response(param),
            "synciq_target_reports": MockGatherfactsApi.get_synciq_target_reports_response(param),
            "synciq_policies": MockGatherfactsApi.get_synciq_policies_response(param),
            "synciq_performance_rules": MockGatherfactsApi.get_synciq_performance_rules_response(param),
            "synciq_target_cluster_certificates": MockGatherfactsApi.get_synciq_target_cluster_certificates_response(param),
            "access_zones": MockGatherfactsApi.get_access_zones_response(param),
            "clients": MockGatherfactsApi.get_clients_response(param),
            "snmp_settings": MockGatherfactsApi.get_snmp_settings_response(param),
            "support_assist_settings": MockGatherfactsApi.get_support_assist_settings(param)
        }
        return subset_error_dict.get(gather_subset)

    @staticmethod
    def get_gather_facts_error_response(gather_subset):
        param = "error"
        subset_error_dict = {
            "nfs_global_settings": MockGatherfactsApi.get_nfsglobal_settings(param),
            "smb_global_settings": MockGatherfactsApi.get_smb_global_settings(param),
            "nfs_zone_settings": MockGatherfactsApi.get_nfs_zone_settings(param),
            "ldap": MockGatherfactsApi.get_ldap_details_response(param),
            "user_mapping_rules": MockGatherfactsApi.get_user_mapping_rules_response(param),
            "smb_files": MockGatherfactsApi.get_smb_files_response(param),
            "storagepool_tiers": MockGatherfactsApi.get_storage_tier_response(param),
            "node_pools": MockGatherfactsApi.get_node_pool_response(param),
            "network_subnets": MockGatherfactsApi.get_network_subnets_response(param),
            "nfs_aliases": MockGatherfactsApi.get_nfs_aliases_response(param),
            "network_interfaces": MockGatherfactsApi.get_network_interfaces_response(param),
            "network_rules": MockGatherfactsApi.get_network_rules_response(param),
            "network_pools": MockGatherfactsApi.get_network_pools_response(param),
            "network_groupnets": MockGatherfactsApi.get_network_groupnets_response(param),
            "providers": MockGatherfactsApi.get_providers_response(param),
            "users": MockGatherfactsApi.get_users_response(param),
            "groups": MockGatherfactsApi.get_groups_response(param),
            "smb_shares": MockGatherfactsApi.get_smb_shares_response(param),
            "nfs_exports": MockGatherfactsApi.get_nfs_exports_response(param),
            "nfs_default_settings": MockGatherfactsApi.get_nfs_default_settings_response(param),
            "s3_buckets": MockGatherfactsApi.get_s3_buckets_response(param),
            "attributes": MockGatherfactsApi.get_attributes_response(param),
            "nodes": MockGatherfactsApi.get_nodes_response(param),
            "synciq_reports": MockGatherfactsApi.get_synciq_reports_response(param),
            "synciq_target_reports": MockGatherfactsApi.get_synciq_target_reports_response(param),
            "synciq_policies": MockGatherfactsApi.get_synciq_policies_response(param),
            "synciq_performance_rules": MockGatherfactsApi.get_synciq_performance_rules_response(param),
            "synciq_target_cluster_certificates": MockGatherfactsApi.get_synciq_target_cluster_certificates_response(param),
            "access_zones": MockGatherfactsApi.get_access_zones_response(param),
            "clients": MockGatherfactsApi.get_clients_response(param),
            "snmp_settings": MockGatherfactsApi.get_snmp_settings_response(param),
            "support_assist_settings": MockGatherfactsApi.get_support_assist_settings(param)
        }
        return subset_error_dict.get(gather_subset)

    @staticmethod
    def get_gather_facts_error_method(gather_subset):
        subset_method_dict = {
            "nfs_global_settings": "get_nfs_settings_global",
            "smb_global_settings": "get_smb_settings_global",
            "nfs_zone_settings": "get_nfs_settings_zone",
            "nfs_aliases": "list_nfs_aliases",
            "smb_shares": "list_smb_shares",
            "nfs_exports": "list_nfs_exports",
            "nfs_default_settings": "get_nfs_settings_export",
            "s3_buckets": "list_s3_buckets",
            "snmp_settings": "get_snmp_settings",

            "ldap": "list_providers_ldap",
            "user_mapping_rules": "get_mapping_users_rules",
            "smb_files": "get_smb_openfiles",
            "providers": "get_providers_summary",
            "users": "list_auth_users",
            "groups": "list_auth_groups",

            "storagepool_tiers": "list_storagepool_tiers",
            "node_pools": "list_storagepool_nodepools",

            "network_subnets": "get_network_subnets",
            "network_interfaces": "get_network_interfaces",
            "network_rules": "get_network_rules",
            "network_pools": "get_network_pools",
            "network_groupnets": "list_network_groupnets",

            "attributes": "get_cluster_config",
            "nodes": "get_cluster_nodes",

            "synciq_reports": "get_sync_reports",
            "synciq_target_reports": "get_target_reports",
            "synciq_policies": "list_sync_policies",
            "synciq_performance_rules": "list_sync_rules",
            "synciq_target_cluster_certificates": "list_certificates_peer",

            "access_zones": "list_zones",
            "clients": "get_summary_client",
            "support_assist_settings": "get_supportassist_settings"
        }
        return subset_method_dict.get(gather_subset)
