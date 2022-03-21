# Copyright: (c) 2021, DellEMC

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock API responses for PowerScale Network Settings module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.networksettings.utils'

GET_NETWORK_SETTINGS = {"network_settings": [{"default_groupnet": "groupnet0",
                                              "sbr": True,
                                              "sc_rebalance_delay": 0,
                                              "tcp_ports": [2049, 445, 20, 21, 80]}]}

UPDATE_NETWORK_SETTINGS = {"network_settings": [{"enable_source_routing": True, "state": "present"}]}


def get_networksettings_failed_msg():
    return 'Retrieving details of network settings failed with error:'


def modify_networksettings_failed_msg():
    return 'Modifying network settings failed with error:'
