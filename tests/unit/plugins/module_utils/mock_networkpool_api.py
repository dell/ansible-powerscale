# Copyright: (c) 2021, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock API responses for PowerScale Network Pool module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.networkpool.utils'

GET_NETWORK_POOLS = {"pools": [{"access_zone": "ansible-neo",
                                "groupnet": "groupnet0",
                                "name": "Test_pool1",
                                "subnet": "subnet0",
                                "ranges": [""],
                                "ifaces": [""],
                                "static_routes": [],
                                "sc_dns_zone_aliases": []}]}

CREATE_NETWORK_POOL = {"pools": [{"access_zone": "ansible-neo",
                                  "groupnet": "groupnet0",
                                  "name": "Test_pool1",
                                  "subnet": "subnet0",
                                  "description": "Test_pool1",
                                  "ranges": [{"low": "1.*.*.*",
                                              "high": "1.*.*.*"}],
                                  "ifaces": [{"iface": "ext-1",
                                              "lnn": 4}],
                                  "static_routes": [{"gateway": "1.*.*.*",
                                                     "prefixlen": 4,
                                                     "subnetdict": "1.*.*.*"}],
                                  "sc_dns_zone": "1.*.*.*",
                                  "sc_connect_policy": "throughput",
                                  "sc_failover_policy": "throughput",
                                  "rebalance_policy": "auto",
                                  "alloc_method": "dynamic",
                                  "sc_auto_unsuspend_delay": 200,
                                  "sc_ttl": 300,
                                  "aggregation_mode": "lacp",
                                  "sc_subnet": "subnet_test",
                                  "sc_dns_zone_aliases": ["smartconn-zone"]}]}


def get_networkpool_failed_msg(pool_name):
    return 'Unable to get network pool ' + pool_name + ' failed with error:'


def create_networkpool_failed_msg(pool_name):
    return 'Unable to create network pool ' + pool_name


def modify_networkpool_failed_msg(pool_name):
    return 'Failed to update network pool: ' + pool_name + ' with error'


def delete_networkpool_failed_msg(pool_name):
    return 'Failed to delete network pool: ' + pool_name + ' with error'


def get_networkpool_invalid_id_msg(pool_name):
    return "Invalid value for 'id', must not be 'None'"
