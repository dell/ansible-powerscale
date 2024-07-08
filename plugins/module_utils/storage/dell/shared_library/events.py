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

    def get_event_groups(self):
        """
        Get event groups
        :param alert_info: Include alert rules and channels in output.
        :param category: Return eventgroups in the specified category.
        :return: event groups
        :rtype: list
        """
        try:
            alert_info = self.module.params.get('alert_info')
            category = self.module.params.get('category')
            all_event_groups = []
            filter_params = {}
            if alert_info:
                filter_params['alert_info'] = alert_info
            elif category:
                filter_params['category'] = category

            event_groups = (self.event_api.get_event_eventgroup_definitions(**filter_params)).to_dict()
            all_event_groups.append(event_groups)
            resume = event_groups.get('resume')

            while resume:
                event_groups_resume = (self.event_api.get_event_eventgroup_definitions(resume=resume, **filter_params)).to_dict()
                resume = event_groups_resume.get('resume')
                all_event_groups.append(event_groups_resume)
            return all_event_groups

        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Fetching event groups failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_alert_categories(self):
        """
        Get alert categories
        :return: alert categories
        :rtype: list
        """
        try:
            all_alert_categories = []
            alert_categories = (self.event_api.get_event_categories()).to_dict()
            all_alert_categories.append(alert_categories)

            while alert_categories.get('resume'):
                alert_categories_resume = (self.event_api.get_event_categories(resume=alert_categories.get('resume'))).to_dict()
                all_alert_categories.append(alert_categories_resume)
            return all_alert_categories

        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Fetching alert categories failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_alert_rules(self):
        """
        Get alert rules
        :param sort_dir: Sort results in ascending or descending order.
        :param sort: Sort results by the specified field.
        :param channels: Limit results to the specified channels.
        :return: alert rules
        :rtype: list
        """
        try:
            sort_dir = self.module.params.get('sort_dir')
            sort = self.module.params.get('sort')
            channels = self.module.params.get('channels')
            all_alert_rules = []
            base_params = {}
            if sort_dir:
                base_params = {'dir': sort_dir.upper()}
            elif sort:
                base_params = {'sort': sort}
            elif channels:
                base_params['channels'] = channels

            alert_rules = (self.event_api.list_event_alert_conditions(**base_params)).to_dict()
            all_alert_rules.append(alert_rules)
            resume = alert_rules['resume']

            while resume:
                alert_rules = (self.event_api.list_event_alert_conditions(resume=resume, **base_params)).to_dict()
                resume = alert_rules['resume']
                all_alert_rules.append(alert_rules)
            return all_alert_rules

        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Fetching alert rules failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_event_channels(self):
        """
        Get event channels
        :return: event channels
        :rtype: list
        """
        try:
            sort_dir = self.module.params.get('sort_dir')
            sort = self.module.params.get('sort')
            all_event_channels = []
            filter_params = {}

            if sort_dir:
                filter_params = {'dir': sort_dir.upper()}
            elif sort:
                filter_params = {'sort': sort}

            event_channels = (self.event_api.list_event_channels(**filter_params)).to_dict()
            all_event_channels.append(event_channels)
            resume = event_channels.get('resume')

            while resume:
                event_channels_resume = (self.event_api.list_event_channels(resume=resume, **filter_params)).to_dict()
                all_event_channels.append(event_channels_resume)
                resume = event_channels_resume.get('resume')
            return all_event_channels

        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Fetching event channels failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
