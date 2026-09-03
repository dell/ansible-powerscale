#!/usr/bin/python
# Copyright: (c) 2024, Dell Technologies

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
|- Managing event alert suppression on a PowerScale system includes suppressing,
  un-suppressing, and querying per-event alert suppression.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
  - Dell Technologies Ansible Team <ansible.team@dell.com>
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
notes:
|- This module operates on a single event ID per task.
|- Bulk suppression of multiple event IDs is not supported.
|- Time-based suppression or auto-revert is not supported by the OneFS API.
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
event_alert_suppression_details:
    description: Details of the event alert suppression.
    type: complex
    returned: always
    contains:
        suppressions:
            description: List of suppressed events (when querying all events).
            type: list
            elements: dict
            returned: when state is C(get) and event_id is not provided
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
        event_id:
            description: Event ID (when querying a specific event).
            type: str
            returned: when state is C(get) and event_id is provided
        name:
            description: Event name (when querying a specific event).
            type: str
            returned: when state is C(get) and event_id is provided
        category:
            description: Event category (when querying a specific event).
            type: str
            returned: when state is C(get) and event_id is provided
        description:
            description: Event description (when querying a specific event).
            type: str
            returned: when state is C(get) and event_id is provided
        node:
            description: Whether the event is node-specific (when querying a specific event).
            type: bool
            returned: when state is C(get) and event_id is provided
        suppressed:
            description: Whether the event is suppressed (when querying a specific event).
            type: bool
            returned: when state is C(get) and event_id is provided
        total:
            description: Total count of suppressed events.
            type: int
            returned: when state is C(get) and event_id is not provided
changed:
    description: Whether the module made any changes.
    type: bool
    returned: always
msg:
    description: Status message.
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.events import Events

LOG = utils.get_logger('event_alert_suppression')


class EventAlertSuppression(Events):
    """Class for managing event alert suppression on PowerScale"""

    def __init__(self, event_api, module):
        """
        Initialize the EventAlertSuppression class
        :param event_api: The event sdk instance
        :param module: Ansible module object
        """
        super(EventAlertSuppression, self).__init__(event_api, module)

    def query_all_suppressed_events(self):
        """
        Query all suppressed events
        :return: Suppressed events list and total count
        :rtype: dict
        """
        try:
            all_suppressed_events = []
            result = (self.event_api.get_event_suppress()).to_dict()
            all_suppressed_events.append(result)
            resume = result.get('resume')

            while resume:
                result_resume = (self.event_api.get_event_suppress(
                    resume=resume)).to_dict()
                resume = result_resume.get('resume')
                all_suppressed_events.append(result_resume)

            # Flatten the suppressions list
            suppressions = []
            for page in all_suppressed_events:
                suppressions.extend(page.get('suppressions', []))

            return {
                'suppressions': suppressions,
                'total': len(suppressions)
            }
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Fetching suppressed events failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def query_specific_event(self, event_id):
        """
        Query a specific event's suppression state with full metadata
        :param event_id: Event ID
        :return: Event details with full metadata
        :rtype: dict
        """
        try:
            # Get suppression state
            suppression_state = (self.event_api.get_event_suppress_by_id(
                event_suppress_id=event_id)).to_dict()

            # Get full metadata from eventgroup definitions
            event_group = (self.event_api.get_event_eventgroup_definitions(
                filter=f'id eq {event_id}')).to_dict()

            # Find the matching event
            event_details = None
            for event in event_group.get('eventgroup-definitions', []):
                if event.get('id') == event_id:
                    event_details = event
                    break

            if event_details:
                event_details['suppressed'] = suppression_state.get('suppressed', False)
                return event_details
            else:
                return suppression_state
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Fetching event details for {event_id} failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)


def main():
    """Main function for the event_alert_suppression module"""
    module_args = dict(
        event_id=dict(type='str'),
        state=dict(
            type='str',
            choices=['suppressed', 'unsuppressed', 'get'],
            required=True
        )
    )

    required_if = [
        ('state', 'suppressed', ['event_id']),
        ('state', 'unsuppressed', ['event_id']),
    ]

    module = AnsibleModule(
        argument_spec=module_args,
        required_if=required_if,
        supports_check_mode=True
    )

    event_id = module.params.get('event_id')
    state = module.params.get('state')

    # Get PowerScale connection
    api_client = utils.get_powerscale_connection(module.params)
    from isilon_sdk.v9_10_0 import EventApi
    event_api = EventApi(api_client)

    event_alert_suppression = EventAlertSuppression(event_api, module)

    result = {}
    changed = False
    msg = ''

    try:
        if state == 'get':
            if event_id:
                # Query specific event
                LOG.info(f'Querying suppression state for event {event_id}')
                event_details = event_alert_suppression.query_specific_event(event_id)
                result['event_alert_suppression_details'] = event_details
                msg = f'Successfully queried suppression state for event {event_id}'
            else:
                # Query all suppressed events
                LOG.info('Querying all suppressed events')
                suppressed_events = event_alert_suppression.query_all_suppressed_events()
                result['event_alert_suppression_details'] = suppressed_events
                msg = f'Successfully queried {suppressed_events["total"]} suppressed events'
            changed = False

        elif state == 'suppressed':
            LOG.info(f'Suppressing event {event_id}')
            current_state = event_alert_suppression.get_event_suppressed_state(event_id)
            
            if current_state:
                # Already suppressed - idempotent
                LOG.info(f'Event {event_id} is already suppressed')
                result['event_alert_suppression_details'] = {
                    'event_id': event_id,
                    'suppressed': True
                }
                msg = f'Event {event_id} is already suppressed'
                changed = False
            else:
                # Suppress the event
                if module.check_mode:
                    # Check mode - skip actual mutation
                    LOG.info(f'Check mode: Would suppress event {event_id}')
                    result['event_alert_suppression_details'] = {
                        'event_id': event_id,
                        'suppressed': False,
                        'would_change_to': True
                    }
                    msg = f'Check mode: Would suppress event {event_id}'
                    changed = True
                    # Add diff output for check mode
                    result['diff'] = {
                        'before': {
                            'event_id': event_id,
                            'suppressed': False
                        },
                        'after': {
                            'event_id': event_id,
                            'suppressed': True
                        }
                    }
                else:
                    # Actual suppress operation
                    event_alert_suppression.set_event_suppressed_state(event_id, True)
                    
                    # Post-write verification
                    new_state = event_alert_suppression.get_event_suppressed_state(event_id)
                    if new_state:
                        LOG.info(f'Successfully suppressed event {event_id}')
                        result['event_alert_suppression_details'] = {
                            'event_id': event_id,
                            'suppressed': True
                        }
                        msg = f'Successfully suppressed event {event_id}'
                        changed = True
                        # Add diff output for actual change
                        result['diff'] = {
                            'before': {
                                'event_id': event_id,
                                'suppressed': False
                            },
                            'after': {
                                'event_id': event_id,
                                'suppressed': True
                            }
                        }
                    else:
                        error_msg = f'Failed to verify suppression state for event {event_id}'
                        LOG.error(error_msg)
                        module.fail_json(msg=error_msg)

        elif state == 'unsuppressed':
            LOG.info(f'Un-suppressing event {event_id}')
            current_state = event_alert_suppression.get_event_suppressed_state(event_id)
            
            if not current_state:
                # Already unsuppressed - idempotent
                LOG.info(f'Event {event_id} is already unsuppressed')
                result['event_alert_suppression_details'] = {
                    'event_id': event_id,
                    'suppressed': False
                }
                msg = f'Event {event_id} is already unsuppressed'
                changed = False
            else:
                # Un-suppress the event
                if module.check_mode:
                    # Check mode - skip actual mutation
                    LOG.info(f'Check mode: Would un-suppress event {event_id}')
                    result['event_alert_suppression_details'] = {
                        'event_id': event_id,
                        'suppressed': True,
                        'would_change_to': False
                    }
                    msg = f'Check mode: Would un-suppress event {event_id}'
                    changed = True
                    # Add diff output for check mode
                    result['diff'] = {
                        'before': {
                            'event_id': event_id,
                            'suppressed': True
                        },
                        'after': {
                            'event_id': event_id,
                            'suppressed': False
                        }
                    }
                else:
                    # Actual un-suppress operation
                    event_alert_suppression.set_event_suppressed_state(event_id, False)
                    
                    # Post-write verification
                    new_state = event_alert_suppression.get_event_suppressed_state(event_id)
                    if not new_state:
                        LOG.info(f'Successfully un-suppressed event {event_id}')
                        result['event_alert_suppression_details'] = {
                            'event_id': event_id,
                            'suppressed': False
                        }
                        msg = f'Successfully un-suppressed event {event_id}'
                        changed = True
                        # Add diff output for actual change
                        result['diff'] = {
                            'before': {
                                'event_id': event_id,
                                'suppressed': True
                            },
                            'after': {
                                'event_id': event_id,
                                'suppressed': False
                            }
                        }
                    else:
                        error_msg = f'Failed to verify un-suppression state for event {event_id}'
                        LOG.error(error_msg)
                        module.fail_json(msg=error_msg)

        module.exit_json(changed=changed, msg=msg, **result)

    except Exception as e:
        error_msg = utils.determine_error(error_obj=e)
        error_message = f'Event alert suppression operation failed with error: {error_msg}'
        LOG.error(error_message)
        module.fail_json(msg=error_message)


if __name__ == '__main__':
    main()
