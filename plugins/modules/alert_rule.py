#!/usr/bin/python
# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing alert rule"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: alert_rule
version_added: '3.3.0'
short_description:  Manage alert rule on a PowerScale Storage System
description:
  - Manage alert rule on a PowerScale Storage System includes create, modify or delete.
extends_documentation_fragment:
  - dellemc.powerscale.powerscale
author:
  - Felix Stephen (@felixs88) <ansible.team@dell.com>
options:
  state:
    description:
      - The state option is used to mention the existence of server certificate.
    type: str
    choices: [absent, present]
    default: present
  name:
    description:
      - The I(name) of the rule is a unique that cannot be changed.
    type: str
    required: true
  condition:
    description:
      - Trigger condition for alert.
    type: str
    choices: ['NEW', 'NEW EVENTS', 'ONGOING', 'SEVERITY INCREASE', 'SEVERITY DECREASE', 'RESOLVED']
  categories:
    description:
      - Event group categories to be alerted.
    type: list
    elements: str
    choices: ['all', 'SYS_DISK_EVENTS', 'NODE_STATUS_EVENTS', 'REBOOT_EVENTS',
      'SW_EVENTS', 'QUOTA_EVENTS', 'SNAP_EVENTS', 'WINNET_EVENTS', 'FILESYS_EVENTS',
      'HW_EVENTS', 'CPOOL_EVENTS']
  channels:
    description:
      - Channels for the alert.
      - This is option is required for create alert condition.
    type: list
    elements: str
  eventgroup_ids:
    description:
      - Event group ID's to be alerted.
    type: list
    elements: str
  exclude_eventgroup_ids:
    description:
      - Event group categories to be excluded from alerts.
    type: list
    elements: str
  interval:
    description:
      - Required with ONGOING condition only, period in seconds between
        alerts of ongoing conditions.
      - I(interval) range is 0 - 9223372036854775807.
    type: int
  limit:
    description:
      - Required with NEW EVENTS condition only, limits the number of
        alerts sent as events are added.
      - I(limit) range is 0 - 9223372036854775807.
    type: int
  severities:
    description:
      - Severities to be alerted.
    type: list
    elements: str
    choices: ['emergency', 'critical', 'warning', 'information']
  transient:
    description:
      - Any event group lasting less than this many seconds is deemed
        transient and will not generate alerts under this condition.
      - I(transient) range is 0 - 9223372036854775807.
    type: int
notes:
  - The I(check_mode) is supported.
  - The I(diff) is supported.
'''

EXAMPLES = r'''
- name: To create the a new alert condition.
  dellemc.powerscale.alert_rule:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    state: present
    name: alert_rule_new
    condition: NEW
    categories:
      - all
      - SYS_DISK_EVENTS
    channels:
      - SupportAssist
    eventgroup_ids:
      - 100010001
      - 100010002
      - 100010003
    exclude_eventgroup_ids:
      - 100010005
    interval: 11
    transient: 10
    limit: 10
    severities:
      - emergency

- name: To update the existing alert condition.
  dellemc.powerscale.alert_rule:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    state: present
    name: alert_rule_new
    condition: NEW
    categories:
      - all
      - SYS_DISK_EVENTS
      - NODE_STATUS_EVENTS
    channels:
      - SupportAssist
    eventgroup_ids:
      - 100010001
      - 100010002
    exclude_eventgroup_ids:
      - 100010005
    interval: 1100
    transient: 10
    limit: 10
    severities:
      - emergency
      - critical

- name: To delete the existing alert condition.
  dellemc.powerscale.alert_rule:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    state: absent
    name: alert_rule_new
'''

RETURN = r'''
changed:
  description: A boolean indicating if the task had to make changes.
  returned: always
  type: bool
  sample: "false"
alert_conditions:
  description: The alert condition details.
  type: dict
  returned: always
  contains:
    name:
      description: The name of the alert condition.
      type: str
    condition:
      description: The condition of the alert condition.
      type: str
    categories:
      description: The categories of the alert condition.
      type: list
      elements: str
    channels:
      description: The channels of the alert condition.
      type: list
      elements: str
    eventgroup_ids:
      description: The event group IDs of the alert condition.
      type: list
      elements: str
    exclude_eventgroup_ids:
      description: The event group categories of the alert condition.
      type: list
      elements: str
    interval:
      description: The interval of the alert condition.
      type: int
    limit:
      description: The limit of the alert condition.
      type: int
    severities:
      description: The severities of the alert condition.
      type: list
      elements: str
    transient:
      description: The transient of the alert condition.
      type: int
  sample:
    {
      "name": "alert_rule_new",
      "condition": "NEW",
      "categories": ["all", "SYS_DISK_EVENTS"],
      "channels": ["SupportAssist"],
      "eventgroup_ids": ["100010001", "100010002", "100010003"],
      "exclude_eventgroup_ids": ["100010005"],
      "interval": 11,
      "limit": 10,
      "severities": ["emergency"],
      "transient": 10
    }
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.powerscale_base \
    import PowerScaleBase
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.events \
    import Events
from copy import deepcopy

LOG = utils.get_logger('alert_rule')

CATEGORY_DICT = {
    "all": "all",
    "100000000": "SYS_DISK_EVENTS",
    "200000000": "NODE_STATUS_EVENTS",
    "300000000": "REBOOT_EVENTS",
    "400000000": "SW_EVENTS",
    "500000000": "QUOTA_EVENTS",
    "600000000": "SNAP_EVENTS",
    "700000000": "WINNET_EVENTS",
    "800000000": "FILESYS_EVENTS",
    "900000000": "HW_EVENTS",
    "1100000000": "CPOOL_EVENTS"}


class AlertRule(PowerScaleBase):

    def __init__(self):

        required_if_args = [
            ["state", "present", ["channels"]]
        ]

        ansible_module_params = {
            'argument_spec': self.get_alert_rule_parameters(),
            'required_if': required_if_args,
            'supports_check_mode': True}
        super().__init__(AnsibleModule, ansible_module_params)

        self.result.update({"alert_conditions": {}, "diff": None})

    def get_alert_rule_parameters(self):
        return dict(
            state=dict(type='str', choices=['present', 'absent'], default='present'),
            name=dict(type='str', required=True),
            condition=dict(type='str', choices=['NEW', 'NEW EVENTS', 'ONGOING',
                                                'SEVERITY INCREASE', 'SEVERITY DECREASE', 'RESOLVED']),
            categories=dict(type='list', elements='str',
                            choices=['all', 'SYS_DISK_EVENTS', 'NODE_STATUS_EVENTS',
                                     'REBOOT_EVENTS', 'SW_EVENTS', 'QUOTA_EVENTS',
                                     'SNAP_EVENTS', 'WINNET_EVENTS', 'FILESYS_EVENTS',
                                     'HW_EVENTS', 'CPOOL_EVENTS']),
            channels=dict(type='list', elements='str'),
            eventgroup_ids=dict(type='list', elements='str'),
            exclude_eventgroup_ids=dict(type='list', elements='str'),
            interval=dict(type='int'),
            limit=dict(type='int'),
            transient=dict(type='int'),
            severities=dict(type='list', elements='str',
                            choices=['emergency', 'critical', 'warning', 'information']),
        )

    def get_alert_rule(self, module_params):
        event_obj = Events(self.event_api, self.module)
        all_alert_rules = event_obj.get_alert_rules()
        alert_conditions = []
        for each in all_alert_rules:
            if each.get("alert_conditions"):
                alert_conditions.extend(each.get("alert_conditions"))
                break

        alert_rule = {}
        if alert_conditions:
            rule_name = module_params.get("name")
            for each_rule in alert_conditions:
                if each_rule["name"] == rule_name:
                    alert_rule.update(each_rule)
                    break

            if alert_rule.get("categories"):
                categories = sorted([CATEGORY_DICT[key] for key in alert_rule["categories"]], reverse=True)
                alert_rule.update({"categories": categories})
        return alert_rule

    def get_module_params(self, module_params):
        return {
            "name": module_params.get("name"),
            "condition": module_params.get("condition"),
            "categories": module_params.get("categories"),
            "channels": module_params.get("channels"),
            "eventgroup_ids": module_params.get("eventgroup_ids"),
            "exclude_eventgroup_ids": module_params.get("exclude_eventgroup_ids"),
            "interval": module_params.get("interval"),
            "limit": module_params.get("limit"),
            "severities": module_params.get("severities"),
            "transient": module_params.get("transient")
        }

    def create_alert_condition(self, module_params):
        changed = False
        alert_data = self.get_module_params(module_params)

        if not self.module.check_mode:
            try:
                self.event_api.create_event_alert_condition(alert_data)
                alert_data = self.get_alert_rule(module_params)
                changed = True
            except Exception as e:
                error_message = f"Failed to create alert condition: {utils.determine_error(e)}"
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

        if self.module._diff:
            self.result.update({"diff": {"before": {}, "after": alert_data}})

        if self.module.check_mode:
            changed, alert_data = True, {}

        return changed, alert_data

    def get_difference(self, alert_rule_details, alert_data):
        difference = False

        if alert_data.get("categories"):
            alert_data_category = sorted(alert_data["categories"], reverse=True)
            alert_data.update({"categories": alert_data_category})

        for key, value in alert_rule_details.items():
            if not alert_data.get(key):
                alert_data.update({key: value})

        for each_attr, value in alert_rule_details.items():
            if alert_data.get(each_attr) != value:
                difference = True
                break

        return difference, alert_data

    def modify_alert_condition(self, alert_rule_details, module_params):
        changed = False
        alert_data = self.get_module_params(module_params)
        difference, updated_payload = self.get_difference(alert_rule_details, alert_data)
        after_updated_payload = deepcopy(updated_payload)

        if self.module.check_mode and difference:
            changed = True
            alert_data = alert_rule_details

        if not self.module.check_mode and difference:
            try:
                updated_payload.pop("name")
                rule_id = updated_payload.pop("id")
                self.event_api.update_event_alert_condition(updated_payload, rule_id)
                alert_data = self.get_alert_rule(module_params)
                changed = True
            except Exception as e:
                error_message = f"Failed to update alert condition: {utils.determine_error(e)}"
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

        if self.module._diff:
            self.result.update({"diff": {"before": alert_rule_details, "after": after_updated_payload}})

        return changed, alert_data

    def delete_alert_condition(self, alert_rule_condition):
        changed, alert_rule = False, alert_rule_condition
        if self.module.check_mode and alert_rule_condition:
            changed = True

        if not self.module.check_mode and alert_rule_condition:
            try:
                self.event_api.delete_event_alert_condition(alert_rule_condition["id"])
                alert_rule = {}
                changed = True
            except Exception as e:
                error_message = f"Failed to delete alert condition: {utils.determine_error(e)}"
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

        if self.module._diff:
            self.result.update({"diff": {"before": alert_rule_condition, "after": {}}})
        return changed, alert_rule


class AlertRuleCreateHandler:

    def handle(self, alert_rule_obj, module_params, alert_rule_details):
        state = module_params["state"]
        if state == "present" and not alert_rule_details:
            changed, alert_rule_details = alert_rule_obj.create_alert_condition(module_params)
            alert_rule_obj.result['changed'] = changed
            AlertRuleExitHander().handle(alert_rule_obj, alert_rule_details)

        AlertRuleUpdateHandler().handle(alert_rule_obj, module_params, alert_rule_details)


class AlertRuleUpdateHandler:

    def handle(self, alert_rule_obj, module_params, alert_rule_details):
        state = module_params["state"]
        if state == "present" and alert_rule_details:
            changed, alert_rule_details = alert_rule_obj.modify_alert_condition(alert_rule_details, module_params)
            alert_rule_obj.result['changed'] = changed

        AlertRuleDeleteHandler().handle(alert_rule_obj, module_params, alert_rule_details)


class AlertRuleDeleteHandler:

    def handle(self, alert_rule_obj, module_params, alert_rule_details):
        state = module_params["state"]
        if state == "absent":
            changed, alert_rule_details = alert_rule_obj.delete_alert_condition(alert_rule_details)
            alert_rule_obj.result['changed'] = changed
        AlertRuleExitHander().handle(alert_rule_obj, alert_rule_details)


class AlertRuleExitHander:

    def handle(self, alert_rule_obj, alert_rule_details):
        alert_rule_obj.result["alert_conditions"] = alert_rule_details
        alert_rule_obj.module.exit_json(**alert_rule_obj.result)


class AlertRuleHandler:

    def handle(self, alert_rule_obj, module_params):
        alert_rule_details = alert_rule_obj.get_alert_rule(module_params)
        AlertRuleCreateHandler().handle(alert_rule_obj, module_params, alert_rule_details)


def main():
    obj = AlertRule()
    AlertRuleHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
