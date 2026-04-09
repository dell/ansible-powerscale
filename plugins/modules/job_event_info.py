#!/usr/bin/python
# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for retrieving Job Event information on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: job_event_info

version_added: '4.0.0'

short_description: Get Job Event information on PowerScale
description:
- Retrieving information about job events on PowerScale storage system.
- This module supports filtering events by state, time range, job ID,
  job type, event key, and other criteria.
- Supports pagination for large result sets.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Shrinidhi Rao (@shrinidhirao) <ansible.team@dell.com>

options:
  state:
    description:
    - Filter events by job state.
    type: str
    choices: ['running', 'paused_user', 'paused_system', 'paused_policy',
              'paused_priority', 'cancelled_user', 'cancelled_system',
              'failed', 'succeeded', 'unknown', 'failed_not_retried']

  begin_time:
    description:
    - Filter events that occurred after this time.
    - Accepts epoch timestamp (numeric string) or ISO 8601 format.
    - Mutually exclusive with I(duration).
    type: str

  end_time:
    description:
    - Filter events that occurred before this time.
    - Accepts epoch timestamp (numeric string) or ISO 8601 format.
    - Mutually exclusive with I(duration).
    type: str

  duration:
    description:
    - Filter events within a time window relative to the current time.
    - Mutually exclusive with I(begin_time) and I(end_time).
    type: dict
    suboptions:
      value:
        description:
        - The numeric duration value.
        type: int
        required: true
      unit:
        description:
        - The unit of the duration value.
        type: str
        required: true
        choices: ['minutes', 'hours', 'days']

  job_id:
    description:
    - Filter events by a specific job ID.
    type: int

  job_type:
    description:
    - Filter events by job type name.
    type: str

  event_key:
    description:
    - Filter events by event key.
    type: str

  ended_jobs_only:
    description:
    - If set to C(true), return only events for ended jobs.
    type: bool

  limit:
    description:
    - Maximum number of events to return per API call.
    type: int

notes:
- This is a read-only info module and does not make any changes.
- The I(check_mode) is supported.
- When I(duration) is specified, the module calculates a time window
  ending at the current time.

requirements:
- JIRA ECS02C-844
'''

EXAMPLES = r'''
- name: Get all job events
  dellemc.powerscale.job_event_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"

- name: Get job events filtered by running state
  dellemc.powerscale.job_event_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    state: "running"

- name: Get job events within a time range using epoch timestamps
  dellemc.powerscale.job_event_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    begin_time: "1700000000"
    end_time: "1700003000"

- name: Get job events within a time range using ISO 8601 format
  dellemc.powerscale.job_event_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    begin_time: "2026-01-01T00:00:00Z"

- name: Get job events from the last 24 hours
  dellemc.powerscale.job_event_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    duration:
      value: 24
      unit: "hours"

- name: Get job events for a specific job ID
  dellemc.powerscale.job_event_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    job_id: 42

- name: Get job events filtered by job type
  dellemc.powerscale.job_event_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    job_type: "SmartPools"

- name: Get events for ended jobs only with limit
  dellemc.powerscale.job_event_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    ended_jobs_only: true
    limit: 100
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool

job_events:
    description: The list of job event details.
    returned: always
    type: list
    contains:
        id:
            description: The unique identifier for the event.
            type: str
        job_id:
            description: The ID of the job associated with this event.
            type: int
        job_type:
            description: The type of the job associated with this event.
            type: str
        state:
            description: The state of the job at the time of the event.
            type: str
        event_key:
            description: The event key identifier.
            type: str
        timestamp:
            description: The epoch timestamp when the event occurred.
            type: int
        message:
            description: A human-readable message describing the event.
            type: str
    sample: [
        {
            "id": "event_456",
            "job_id": 42,
            "job_type": "SmartPools",
            "state": "running",
            "event_key": "job_started",
            "timestamp": 1700000000,
            "message": "Job started successfully"
        }
    ]

total_events:
    description: The total number of events returned.
    returned: always
    type: int
'''

import time
from datetime import datetime, timezone
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('job_event_info')


class JobEventInfo(object):
    """Class with Job Event Info operations"""

    def __init__(self):
        """Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_job_event_info_parameters())

        # initialize the Ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=True,
            mutually_exclusive=[
                ['begin_time', 'duration'],
                ['end_time', 'duration']
            ]
        )

        # result is a dictionary that contains changed status
        self.result = {"changed": False}
        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        self.job_api = self.isi_sdk.JobApi(self.api_client)
        LOG.info('Got the isi_sdk instance for authorization on to PowerScale')

    def parse_time_input(self, time_str):
        """
        Parse a time string input into an epoch integer.
        :param time_str: A string that is either a numeric epoch or
                         ISO 8601 datetime format
        :return: Epoch integer timestamp
        """
        if time_str.isdigit() or (time_str.startswith('-')
                                  and time_str[1:].isdigit()):
            return int(time_str)

        try:
            # Handle ISO 8601 format with timezone info
            if time_str.endswith('Z'):
                time_str = time_str[:-1] + '+00:00'
            dt = datetime.fromisoformat(time_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return int(dt.timestamp())
        except (ValueError, TypeError):
            error_message = 'Invalid time format: %s. Accepted formats ' \
                            'are epoch timestamp (numeric string) or ' \
                            'ISO 8601 format.' % time_str
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def convert_duration_to_window(self, duration):
        """
        Convert a duration dict to begin_time and end_time epoch values.
        :param duration: Dict with 'value' and 'unit' keys
        :return: Tuple of (begin_epoch, end_epoch)
        """
        end_time = int(time.time())
        value = duration['value']
        unit = duration['unit']

        unit_multipliers = {
            'minutes': 60,
            'hours': 3600,
            'days': 86400
        }

        seconds = value * unit_multipliers[unit]
        begin_time = end_time - seconds

        return begin_time, end_time

    def list_job_events(self, **params):
        """
        Get a list of job events.
        :param params: Query parameters for the API call
        :return: Dict with 'events' and 'resume' keys
        """
        try:
            api_response = self.job_api.get_job_events(**params)
            return api_response.to_dict()
        except utils.ApiException as e:
            error_message = 'Failed to get job events with ' \
                            'error: %s' % (utils.determine_error
                                           (error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def perform_module_operation(self):
        """
        Perform different actions on Job Event Info module based on
        parameters chosen in playbook
        """
        state = self.module.params['state']
        begin_time = self.module.params['begin_time']
        end_time = self.module.params['end_time']
        duration = self.module.params['duration']
        job_id = self.module.params['job_id']
        job_type = self.module.params['job_type']
        event_key = self.module.params['event_key']
        ended_jobs_only = self.module.params['ended_jobs_only']
        limit = self.module.params['limit']

        result = dict(
            changed=False,
            job_events=[],
            total_events=0
        )

        # Validate limit
        if limit is not None and limit < 0:
            self.module.fail_json(msg='Invalid limit value: %s. '
                                      'Limit must be a non-negative '
                                      'integer.' % limit)

        # Handle duration - convert to begin_time/end_time
        if duration is not None:
            begin_epoch, end_epoch = self.convert_duration_to_window(duration)
            begin_time = str(begin_epoch)
            end_time = str(end_epoch)

        # Validate and parse time parameters
        parsed_begin_time = None
        parsed_end_time = None

        if begin_time is not None:
            parsed_begin_time = self.parse_time_input(begin_time)
        if end_time is not None:
            parsed_end_time = self.parse_time_input(end_time)

        # Build API parameters, excluding None values
        api_params = {}
        if state is not None:
            api_params['state'] = state
        if parsed_begin_time is not None:
            api_params['begin'] = parsed_begin_time
        if parsed_end_time is not None:
            api_params['end'] = parsed_end_time
        if job_id is not None:
            api_params['job_id'] = job_id
        if job_type is not None:
            api_params['job_type'] = job_type
        if event_key is not None:
            api_params['key'] = event_key
        if ended_jobs_only is not None:
            api_params['ended_jobs_only'] = ended_jobs_only
        if limit is not None:
            api_params['limit'] = limit

        # Fetch events with pagination
        all_events = []
        response = self.list_job_events(**api_params)
        all_events.extend(response.get('events', []))

        # Handle pagination via resume token (skip if limit was set)
        if limit is None:
            while response.get('resume') is not None:
                api_params['resume'] = response['resume']
                response = self.list_job_events(**api_params)
                all_events.extend(response.get('events', []))

        result['job_events'] = all_events
        result['total_events'] = len(all_events)

        self.module.exit_json(**result)


def main():
    """Create PowerScale Job Event Info object and perform action on it
       based on user input from playbook"""
    obj = JobEventInfo()
    obj.perform_module_operation()


def get_job_event_info_parameters():
    """
    This method provides parameters required for the ansible Job Event
    Info module on PowerScale
    """
    return dict(
        state=dict(type='str', choices=[
            'running', 'paused_user', 'paused_system', 'paused_policy',
            'paused_priority', 'cancelled_user', 'cancelled_system',
            'failed', 'succeeded', 'unknown', 'failed_not_retried'
        ]),
        begin_time=dict(type='str'),
        end_time=dict(type='str'),
        duration=dict(type='dict', options=dict(
            value=dict(type='int', required=True),
            unit=dict(type='str', required=True,
                      choices=['minutes', 'hours', 'days'])
        )),
        job_id=dict(type='int'),
        job_type=dict(type='str'),
        event_key=dict(type='str', no_log=False),
        ended_jobs_only=dict(type='bool'),
        limit=dict(type='int')
    )


if __name__ == '__main__':
    main()
