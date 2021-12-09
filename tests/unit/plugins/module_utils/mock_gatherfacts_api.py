# Copyright: (c) 2021, DellEMC

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock Api response for Unit tests of Gatherfacts module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }


class MockGatherfactsApi:
    MODULE_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.dellemc_powerscale_gatherfacts.PowerScaleGatherFacts.'
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.dellemc_ansible_powerscale_utils'
    GATHERFACTS_COMMON_ARGS = {
        'onefs_host': '**.***.**.***',
        'access_zone': 'System',
        'include_all_access_zones': False
    }
    EMPTY_GATHERSUBSET_ERROR_MSG = "Please specify gather_subset"
    EMPTY_RESULT = {
        'SynciqTargetReports': [
        ],
        'NetworkPools': [
        ],
        'AccessZones': [
        ],
        'SynciqReports': [
        ],
        'SynciqPerformanceRules': [
        ],
        'Providers': [
        ],
        'Clients': [
        ],
        'SynciqPolicies': [
        ],
        'SmbShares': [
        ],
        'NetworkGroupnets': [
        ],
        'Groups': [
        ],
        'Attributes': [
        ],
        'NfsExports': [
        ],
        'NetworkRules': [
        ],
        'Nodes': [
        ],
        'Users': [
        ],
        'NetworkInterfaces': [
        ],
        'NetworkSubnets': [
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
