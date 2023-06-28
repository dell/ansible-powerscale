# Copyright: (c) 2021, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock Api response for Unit tests of Gatherfacts module on PowerScale"""

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
        ]
    }

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
                        "id": "1.ext-1",
                        "ip_addrs": [
                            "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"
                        ],
                        "lnn": 1,
                        "name": "ext-1",
                        "nic_name": "em1",
                        "owners": [
                            {
                                "groupnet": "groupnet0",
                                "ip_addrs": [
                                    "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"
                                ],
                                "pool": "pool0",
                                "subnet": "subnet0"
                            }
                        ],
                        "status": "up",
                        "type": "gige"
                    },
                    {
                        "id": "1.ext-2",
                        "ip_addrs": [],
                        "lnn": 1,
                        "name": "ext-2",
                        "nic_name": "em3",
                        "owners": [],
                        "status": "inactive",
                        "type": "gige"
                    },
                    {
                        "id": "1.ext-3",
                        "ip_addrs": [],
                        "lnn": 1,
                        "name": "ext-3",
                        "nic_name": "em4",
                        "owners": [],
                        "status": "inactive",
                        "type": "gige"
                    },
                    {
                        "id": "1.ext-4",
                        "ip_addrs": [],
                        "lnn": 1,
                        "name": "ext-4",
                        "nic_name": "em5",
                        "owners": [],
                        "status": "inactive",
                        "type": "gige"
                    },
                    {
                        "id": "1.ext-5",
                        "ip_addrs": [],
                        "lnn": 1,
                        "name": "ext-5",
                        "nic_name": "em6",
                        "owners": [],
                        "status": "inactive",
                        "type": "gige"
                    },
                    {
                        "id": "1.ext-6",
                        "ip_addrs": [],
                        "lnn": 1,
                        "name": "ext-6",
                        "nic_name": "em7",
                        "owners": [],
                        "status": "inactive",
                        "type": "gige"
                    },
                    {
                        "id": "1.int-a",
                        "ip_addrs": [
                            "1.1.1.31"
                        ],
                        "lnn": 1,
                        "name": "int-a",
                        "nic_name": "em0",
                        "owners": [
                            {
                                "groupnet": "internal",
                                "ip_addrs": [
                                    "1.1.1.1"
                                ],
                                "pool": "int-a-pool",
                                "subnet": "int-a-subnet"
                            }
                        ],
                        "status": "up",
                        "type": "gige"
                    }
                ]
            }
        elif response_type == 'module':
            return [
                {
                    'id': '1.ext-1',
                    'name': 'ext-1',
                    'lnn': 1
                },
                {
                    'id': '1.ext-2',
                    'name': 'ext-2',
                    'lnn': 1
                },
                {
                    'id': '1.ext-3',
                    'name': 'ext-3',
                    'lnn': 1
                },
                {
                    'id': '1.ext-4',
                    'name': 'ext-4',
                    'lnn': 1
                },
                {
                    'id': '1.ext-5',
                    'name': 'ext-5',
                    'lnn': 1
                },
                {
                    'id': '1.ext-6',
                    'name': 'ext-6',
                    'lnn': 1
                },
                {
                    'id': '1.int-a',
                    'name': 'int-a',
                    'lnn': 1
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
