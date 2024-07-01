# Copyright: (c) 2021-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock API responses for PowerScale Access zone module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.accesszone.utils'

ACCESS_ZONE = {'access_zone': [{'az_name': 'testaz',
                                'groupnet': 'groupnet1',
                                'path': '/ifs',
                                'iface': 'ext-1',
                                "create_path": False,
                                "provider_state_add": "add",
                                "provider_state_remove": None,
                                "auth_providers": ["lsa-local-provider:System"]}]}


def create_accesszone_failed_msg(az_name):
    return 'Creation of access zone ' + az_name + ' failed with error:'


def delete_accesszone_failed_msg():
    return 'Failed to delete access zone'
