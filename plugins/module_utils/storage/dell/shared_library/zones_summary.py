# Copyright: (c) 2024, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('zones_summary')


class ZonesSummary:

    '''Class with methods to get zones summary details'''

    def __init__(self, zones_summary_api, module):
        """
        Initialize the zones_summary class
        :param zones_summary_api: The zones_summary sdk instance
        :param module: Ansible module object
        """
        self.zones_summary_api = zones_summary_api
        self.module = module

    def get_zone_base_path(self, access_zone):
        """
        Get the zone base path
        :param access_zone: The access zone name
        :return: zone base path
        :rtype: dict
        """
        try:
            LOG.info(f"Getting zone base path for {access_zone} access zone")
            zone_path = (self.zones_summary_api.
                              get_zones_summary_zone(access_zone)).to_dict()
            # returning access zone base path
            if zone_path:
                LOG.info(f"Zone base path is: {zone_path['summary']['path']}")
                return zone_path['summary']['path']
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Fetching zone base path for access zone {access_zone} is failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
