# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('Events')


class Events:

    '''Class with Event operations'''

    def __init__(self, event_api, module):
        """
        Initialize the Event class
        :param event_api: The event sdk instance
        :param module: Ansible module object
        """
        self.event_api = event_api
        self.module = module

    def get_event_maintenance(self):
        """
        Get maintenance events
        :param limit: limit value
        :return: maintenance events
        :rtype: dict
        """
        try:
            maintenance_events = (self.event_api.get_event_maintenance(history=True)).to_dict()
            if maintenance_events:
                return maintenance_events
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Fetching maintenance events failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
