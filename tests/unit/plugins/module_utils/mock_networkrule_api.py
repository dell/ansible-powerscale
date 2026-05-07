# Copyright: (c) 2021-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
