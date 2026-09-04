#!/usr/bin/python
# Copyright: (c) 2026, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing event alert suppression on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: event_alert_suppression

version_added: '3.11.0'

short_description: Manage event alert suppression on a PowerScale Storage System
description:
- Managing event alert suppression on a PowerScale system includes suppressing,
  un-suppressing, and querying per-event alert suppression.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
  - Ansible Team (@dell-ansible-team) <ansible.team@dell.com>
options:
  event_id:
    description:
    - The event type ID to suppress or un-suppress.
    - Required when I(state) is C(suppressed) or C(unsuppressed).
    - Optional when I(state) is C(get).
    type: str
  state:
    description:
    - The desired state of the event alert suppression.
    - C(suppressed) - suppress alerting for the specified event ID.
    - C(unsuppressed) - un-suppress alerting for the specified event ID.
    - C(get) - query the current suppression state.
    type: str
    choices: ['suppressed', 'unsuppressed', 'get']
    required: true
attributes:
  check_mode:
    description: Runs task to validate without performing action on the target
                 machine.
    support: full
  diff_mode:
    description: Runs the task to report the changes made or to be made.
    support: full
notes:
- This module operates on a single event ID per task.
- Bulk suppression of multiple event IDs is not supported.
- Time-based suppression or auto-revert is not supported by the OneFS API.
- Querying with I(event_id) returns only the suppression state. Event metadata
  such as name, category and description is returned only when querying all
  suppressed events.
'''

EXAMPLES = r'''
- name: Suppress an event alert
  dellemc.powerscale.event_alert_suppression:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    event_id: "100010001"
    state: "suppressed"

- name: Un-suppress an event alert
  dellemc.powerscale.event_alert_suppression:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    event_id: "100010001"
    state: "unsuppressed"

- name: Query all suppressed events
  dellemc.powerscale.event_alert_suppression:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    state: "get"

- name: Query a specific event's suppression state
  dellemc.powerscale.event_alert_suppression:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    event_id: "100010001"
    state: "get"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
    sample: "false"
event_alert_suppression_details:
    description: Details of the event alert suppression.
    type: complex
    returned: always
    contains:
        suppressions:
            description: List of suppressed events.
            type: list
            elements: dict
            returned: when I(state) is C(get) and I(event_id) is not provided
            contains:
                id:
                    description: Event ID.
                    type: str
                name:
                    description: Event name.
                    type: str
                category:
                    description: Event category.
                    type: str
                description:
                    description: Event description.
                    type: str
                node:
                    description: Whether the event is node-specific.
                    type: bool
                suppressed:
                    description: Whether the event is suppressed.
                    type: bool
        total:
            description: Total count of suppressed events.
            type: int
            returned: when I(state) is C(get) and I(event_id) is not provided
        event_id:
            description: Event ID.
            type: str
            returned: when I(event_id) is provided
        suppressed:
            description: Whether the event is currently suppressed.
            type: bool
            returned: when I(event_id) is provided
        would_change_to:
            description: The suppression state that would be applied.
            type: bool
            returned: when run in check mode and a change is required
    sample: {
      "event_id": "100010001",
      "suppressed": true
    }
msg:
    description: Status message describing the operation performed.
    type: str
    returned: always
    sample: "Successfully suppressed event 100010001"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.powerscale_base \
    import PowerScaleBase
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.events \
    import Events

LOG = utils.get_logger('event_alert_suppression')


class EventAlertSuppression(PowerScaleBase):
    """Class with event alert suppression operations"""

    def __init__(self):
        """ Define all parameters required by the event alert suppression module"""

        required_if_args = [
            ["state", "suppressed", ["event_id"]],
            ["state", "unsuppressed", ["event_id"]],
        ]
        ansible_module_params = {
            'argument_spec': self.get_event_alert_suppression_parameters(),
            'required_if': required_if_args,
            'supports_check_mode': True
        }
        super().__init__(AnsibleModule, ansible_module_params)

        # Result is a dictionary that contains changed status, event alert
        # suppression details and the status message
        self.result.update({
            "event_alert_suppression_details": {},
            "msg": "",
            "diff": {}
        })

    def get_suppressed_state(self, event_id):
        """Get the current suppression state of an event
        :param event_id: The event type ID
        :return: True if the event is suppressed else False
        :rtype: bool
        """
        LOG.info("Getting suppression state for event %s.", event_id)
        return Events(self.event_api, self.module).get_event_suppressed_state(
            event_id=event_id)

    def set_suppressed_state(self, event_id, suppressed):
        """Set the suppression state of an event
        :param event_id: The event type ID
        :param suppressed: Desired suppression state
        :return: True if the operation is successful.
        """
        LOG.info("Setting suppression state of event %s to %s.",
                 event_id, suppressed)
        event_suppress_params = self.isi_sdk.EventSuppressIdParams(
            suppressed=suppressed)
        if not self.module.check_mode:
            Events(self.event_api, self.module).set_event_suppressed_state(
                event_id=event_id,
                event_suppress_id_params=event_suppress_params)
        return True

    def get_suppressed_events(self):
        """Get all suppressed events with their metadata
        :return: Dictionary with the list of suppressions and the total count
        :rtype: dict
        """
        LOG.info("Getting all suppressed events.")
        suppressions = Events(self.event_api,
                              self.module).get_event_suppress_list()
        return {
            "suppressions": suppressions,
            "total": len(suppressions)
        }

    def get_event_alert_suppression_parameters(self):
        return dict(
            event_id=dict(type='str'),
            state=dict(type='str', required=True,
                       choices=['suppressed', 'unsuppressed', 'get']))


class EventAlertSuppressionExitHandler:
    def handle(self, suppression_obj, suppression_details):
        suppression_obj.result['event_alert_suppression_details'] = suppression_details
        suppression_obj.module.exit_json(**suppression_obj.result)


class EventAlertSuppressionModifyHandler:
    def handle(self, suppression_obj, suppression_params, current_state):
        event_id = suppression_params['event_id']
        desired_state = suppression_params['state'] == 'suppressed'
        action = 'suppressed' if desired_state else 'un-suppressed'

        if current_state == desired_state:
            suppression_obj.result['msg'] = \
                f"Event {event_id} is already {action}"
            suppression_details = {"event_id": event_id,
                                   "suppressed": current_state}
        else:
            if suppression_obj.module._diff:
                suppression_obj.result['diff'] = dict(
                    before={"event_id": event_id, "suppressed": current_state},
                    after={"event_id": event_id, "suppressed": desired_state})

            suppression_obj.result['changed'] = \
                suppression_obj.set_suppressed_state(event_id, desired_state)

            if suppression_obj.module.check_mode:
                suppression_obj.result['msg'] = \
                    f"Check mode: Event {event_id} would be {action}"
                suppression_details = {"event_id": event_id,
                                       "suppressed": current_state,
                                       "would_change_to": desired_state}
            else:
                suppression_obj.result['msg'] = \
                    f"Successfully {action} event {event_id}"
                suppression_details = {"event_id": event_id,
                                       "suppressed": desired_state}

        EventAlertSuppressionExitHandler().handle(suppression_obj,
                                                  suppression_details)


class EventAlertSuppressionQueryHandler:
    def handle(self, suppression_obj, suppression_params):
        event_id = suppression_params['event_id']

        if suppression_params['state'] == 'get':
            if event_id is None:
                suppression_details = suppression_obj.get_suppressed_events()
                suppression_obj.result['msg'] = \
                    f"Successfully queried {suppression_details['total']} suppressed events"
            else:
                suppression_details = {
                    "event_id": event_id,
                    "suppressed": suppression_obj.get_suppressed_state(event_id)}
                suppression_obj.result['msg'] = \
                    f"Successfully queried suppression state for event {event_id}"
            EventAlertSuppressionExitHandler().handle(suppression_obj,
                                                      suppression_details)
        else:
            current_state = suppression_obj.get_suppressed_state(event_id)
            EventAlertSuppressionModifyHandler().handle(suppression_obj,
                                                        suppression_params,
                                                        current_state)


class EventAlertSuppressionHandler:
    def handle(self, suppression_obj, suppression_params):
        EventAlertSuppressionQueryHandler().handle(suppression_obj,
                                                   suppression_params)


def main():
    """ perform action on PowerScale event alert suppression object and
        perform action on it based on user input from playbook."""
    obj = EventAlertSuppression()
    EventAlertSuppressionHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
