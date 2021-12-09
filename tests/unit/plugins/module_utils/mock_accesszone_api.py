# Copyright: (c) 2021, DellEMC

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock API responses for PowerScale Access zone module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.dellemc_powerscale_accesszone.utils'

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
