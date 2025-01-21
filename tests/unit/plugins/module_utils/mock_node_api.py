# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock API responses for PowerScale Node module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.node.utils'

NODE = {
    "id": 1,
    "lnn": 1,
    "partitions": {
        "count": 1,
        "partitions": [
            {
                "block_size": 1024,
                "capacity": 1957516,
                "component_devices": "ada0p2",
                "mount_point": "/",
                "percent_used": "50%",
                "statfs": {
                    "f_namemax": 255,
                    "f_owner": 0,
                    "f_type": 53,
                    "f_version": 538182936
                },
                "used": 909066
            }
        ]
    }
}


def api_exception_msg():
    return 'get node info for PowerScale cluster'


def invalid_node_msg():
    return 'Please provide a valid Node Id'
