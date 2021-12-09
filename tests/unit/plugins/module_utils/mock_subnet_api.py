# Copyright: (c) 2021, DellEMC

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock Subnet Api for Subnet Test module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }


def get_subnet_details(subnet_name):
    if subnet_name == 'new_subnet':
        return None
    else:
        return {'subnets': [{'addr_family': 'ipv4',
                             'base_addr': '10.*.*.*',
                             'description': 'Initial subnet',
                             'dsr_addrs': [],
                             'gateway': '10.*.*.*',
                             'gateway_priority': 10,
                             'groupnet': 'groupnet0',
                             'id': 'groupnet0.subnet0',
                             'mtu': 1500,
                             'name': 'subnet0',
                             'pools': ['pool0'],
                             'prefixlen': 21,
                             'sc_service_addrs': [
                                 {
                                     'high': '10.*.*.*',
                                     'low': '10.*.*.*'
                                 }
                             ],
                             'sc_service_name': "",
                             'vlan_enabled': False,
                             'vlan_id': None}]}


def get_invalid_subnet():
    return "The value for subnet_name is invalid"


def get_invalid_len():
    return "The maximum length for subnet_name is 32"


def get_invalid_desc():
    return "The maximum length for description is 128"


def get_invalid_netmask():
    return "Invalid IPV4 address specified for netmask"


def get_invalid_gateway_priority():
    return "Please enter a valid value for gateway_priority"


def get_invalid_vlan_id():
    return "The minimum value for vlan_id is 2"


def get_invalid_gateway():
    return "Invalid address specified for gateway"


def get_invalid_sc_ip():
    return "The value for start_range is invalid"


def get_subnet_ex_msg(subnet_name):
    return "Getting details of subnet " + subnet_name + " failed with error"


def modify_subnet_ex_msg(subnet_name):
    return "Modifying subnet " + subnet_name + " failed with error"


def delete_subnet_ex_msg(subnet_name):
    return "Deleting subnet " + subnet_name + " failed with error"


def create_subnet_ex_msg(subnet_name):
    return "Creating subnet " + subnet_name + " failed with error"


def get_invalid_mtu():
    return "The minimum value for mtu is 576"
