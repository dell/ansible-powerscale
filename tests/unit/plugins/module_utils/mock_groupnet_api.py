# Copyright: (c) 2021, DellEMC

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock Groupnet Api for Groupnet Test module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type
GENERIC_FAILURE_MSG = " failed with error"


def get_groupnet_details(groupnet_name):
    if groupnet_name == 'new_groupnet':
        return None
    else:
        return {'groupnets': [{'allow_wildcard_subdomains': True,
                               'description': 'Test Groupnet',
                               'dns_cache_enabled': True,
                               'dns_options': [],
                               'dns_search': "['test.com']",
                               'dns_servers': ['10.*.*.*', '10.*.*.*'],
                               'id': 'groupnet3',
                               'name': 'groupnet3',
                               'server_side_dns_search': False,
                               'subnets': ['subnet12']}]}


def get_invalid_groupnet():
    return "The value for groupnet_name is invalid"


def get_invalid_groupnet_len():
    return "The maximum length for groupnet_name is 32"


def get_invalid_dns():
    return "The value for dns_servers is invalid"


def get_groupnet_ex_msg(groupnet_name):
    return "Getting details of groupnet " + groupnet_name + GENERIC_FAILURE_MSG


def modify_groupnet_ex_msg(groupnet_name):
    return "Modifying groupnet " + groupnet_name + GENERIC_FAILURE_MSG


def delete_groupnet_ex_msg(groupnet_name):
    return "Deleting groupnet " + groupnet_name + GENERIC_FAILURE_MSG


def create_groupnet_ex_msg(groupnet_name):
    return "Creating groupnet " + groupnet_name + GENERIC_FAILURE_MSG


def get_invalid_desc():
    return "The maximum length for description is 128"
