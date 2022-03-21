# Copyright: (c) 2022, DellEMC

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock API responses for PowerScale SmartPool Settings module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.smartpoolsettings.utils'

GET_SMARTPOOL_SETTINGS = {"settings": {"automatically_manage_io_optimization": "files_at_default",
                                       "automatically_manage_protection": "files_at_default",
                                       "global_namespace_acceleration_enabled": False,
                                       "global_namespace_acceleration_state": "inactive",
                                       "protect_directories_one_level_higher": False,
                                       "spillover_enabled": True,
                                       "tcp_ports": {"id": None, "name": None, "type": "anywhere"},
                                       "ssd_l3_cache_default_enabled": True,
                                       "ssd_qab_mirrors": "one",
                                       "ssd_system_btree_mirrors": "one",
                                       "ssd_system_delta_mirrors": "one",
                                       "virtual_hot_spare_deny_writes": False,
                                       "virtual_hot_spare_hide_spare": True,
                                       "virtual_hot_spare_limit_drives": 4,
                                       "virtual_hot_spare_limit_percent": 15}}

UPDATE_SMARTPOOL_SETTINGS = {"smartpool_settings": [{"virtual_hot_spare_limit_percent": 15,
                                                     "virtual_hot_spare_hide_spare": True,
                                                     "state": "present"}]}


def get_networksettings_failed_msg():
    return 'Retrieving details of smartpool settings failed with error:'


def modify_networksettings_failed_msg():
    return 'Modifying smartpool settings failed with error:'
