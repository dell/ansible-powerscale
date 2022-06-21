# Copyright: (c) 2021, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock API responses for PowerScale Network Rule module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.networkrule.utils'

NETWORK_RULES = {'rules': [{'description': '',
                            'groupnet': 'groupnet0',
                            'id': 'groupnet0.subnet1.pool1.rule1',
                            'iface': 'ext-1',
                            'name': 'rule1',
                            'node_type': 'any',
                            'pool': 'pool1',
                            'subnet': 'subnet1'}]
                 }


def create_rule_failed_msg(rule_name):
    return 'Unable to create network rule ' + rule_name + '. failed with error:'


def modify_rule_failed_msg(rule_name):
    return 'Unable to modify settings for rule ' + rule_name + '. failed with error'


def delete_rule_failed_msg(rule_name):
    return 'Unable to delete network rule ' + rule_name + '. failed with error:'
