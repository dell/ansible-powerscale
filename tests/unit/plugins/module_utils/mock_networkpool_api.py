# Copyright: (c) 2021, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock API responses for PowerScale Network Pool module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.networkpool.utils'

RANGE1 = "1.1.1.1"
RANGE2 = "2.2.2.2"

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
                                  "ranges": [{"low": RANGE1,
                                              "high": RANGE1}],
                                  "ifaces": [{"iface": "ext-1",
                                              "lnn": 4}],
                                  "static_routes": [{"gateway": RANGE1,
                                                     "prefixlen": 4,
                                                     "subnet": RANGE1}],
                                  "sc_dns_zone": RANGE1,
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


def network_pool_failed_msg(response_type):
    if response_type == 'invalid_pool_name':
        return 'The value for pool_name is invalid'
    elif response_type == 'invalid_pool_description':
        return 'The maximum length for description is 128'
    elif response_type == 'invalid_ip_range':
        return 'The value for IP range is invalid'
    elif response_type == 'invalid_iface':
        return 'Please enter valid value for iface'
    elif response_type == 'invalid_route':
        return 'Invalid static route value'
