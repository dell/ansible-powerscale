#!/usr/bin/python
# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing jobs on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: job

version_added: '4.0.0'

short_description: Manage jobs on PowerScale

description:
- Managing jobs on PowerScale storage system includes starting,
  pausing, resuming, cancelling, and modifying jobs.
- This module supports starting a new job by type and controlling
  an existing job by ID.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Shrinidhi Rao (@shrinidhirao) <ansible.team@dell.com>

notes:
- Refer to JIRA ECS02C-845 for feature details.
- The I(check_mode) is supported.

options:
  job_id:
    description:
    - The ID of an existing job to control.
    - Mutually exclusive with I(job_type).
    - Required if I(job_type) is not specified.
    type: int

  job_type:
    description:
    - The type of job to start (e.g. C(SmartPools), C(TreeDelete)).
    - Mutually exclusive with I(job_id).
    - Required if I(job_id) is not specified.
    type: str

  job_state:
    description:
    - The desired control state of the job.
    - C(started) - Start a new job (used with I(job_type)).
    - C(paused) - Pause a running job.
    - C(running) - Resume a paused job.
    - C(cancelled) - Cancel a running or paused job.
    choices: ['started', 'paused', 'running', 'cancelled']
    type: str

  paths:
    description:
    - List of filesystem paths for the job.
    - Required when starting a new job with I(job_type).
    type: list
    elements: str

  priority:
    description:
    - The priority of the job. Must be between 1 and 10.
    type: int

  policy:
    description:
    - The impact policy name to associate with the job.
    type: str

  allow_dup:
    description:
    - Whether to allow starting a duplicate job of the same type.
    - If set to C(false) and a running job of the same type exists,
      the operation is a no-op.
    type: bool
    default: false

  job_params:
    description:
    - Additional parameters to pass when starting the job.
    type: dict

  wait:
    description:
    - Whether to wait for the job to complete after starting it.
    type: bool
    default: false

  wait_timeout:
    description:
    - Maximum time in seconds to wait for job completion.
    type: int
    default: 300

  wait_interval:
    description:
    - Interval in seconds between polling for job status during wait.
    type: int
    default: 10

  state:
    description:
    - The state of the job resource.
    - C(present) - Indicates the job should exist or be controlled.
    choices: ['present']
    type: str
    default: present
'''

EXAMPLES = r'''
- name: Start a SmartPools job
  dellemc.powerscale.job:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    job_type: "SmartPools"
    paths:
      - "/ifs/data"
    priority: 5
    state: "present"

- name: Start a TreeDelete job and wait for completion
  dellemc.powerscale.job:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    job_type: "TreeDelete"
    paths:
      - "/ifs/data/old_dir"
    wait: true
    wait_timeout: 600
    wait_interval: 15
    state: "present"

- name: Pause a running job
  dellemc.powerscale.job:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    job_id: 12345
    job_state: "paused"
    state: "present"

- name: Resume a paused job
  dellemc.powerscale.job:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    job_id: 12345
    job_state: "running"
    state: "present"

- name: Cancel a running job
  dellemc.powerscale.job:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    job_id: 12345
    job_state: "cancelled"
    state: "present"

- name: Modify job priority and policy
  dellemc.powerscale.job:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    job_id: 12345
    priority: 3
    policy: "LOW"
    state: "present"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool

job_details:
    description: The job details.
    returned: When job exists
    type: dict
    contains:
        id:
            description: The unique identifier of the job.
            type: int
        type:
            description: The job type.
            type: str
        state:
            description: The current state of the job.
            type: str
        priority:
            description: The priority of the job.
            type: int
        policy:
            description: The impact policy name.
            type: str
        paths:
            description: The filesystem paths associated with the job.
            type: list
        start_time:
            description: The job start time.
            type: int
        end_time:
            description: The job end time.
            type: int
    sample: {
        "id": 12345,
        "type": "SmartPools",
        "state": "running",
        "priority": 5,
        "policy": "LOW",
        "paths": ["/ifs/data"],
        "start_time": 1687488892,
        "end_time": null
    }

outcome:
    description: The outcome of the operation.
    returned: always
    type: str
    sample: "started"

diff:
    description: The before/after diff when running in diff mode.
    returned: When diff mode is enabled
    type: dict
    contains:
        before:
            description: The job state before the operation.
            type: dict
        after:
            description: The job state after the operation.
            type: dict
'''

import time
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('job')

# Terminal states - job is complete
TERMINAL_STATES = ('succeeded', 'failed', 'cancelled_user', 'cancelled_system')

# Paused states
PAUSED_STATES = ('paused_user',
                 'paused_system',
                 'paused_policy',
                 'paused_priority')

# Running states
RUNNING_STATES = ('running',)


class Job(object):
    """Class with Job operations"""

    def __init__(self):
        """Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_job_parameters())

        # initialize the Ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=True,
            mutually_exclusive=[['job_id', 'job_type']],
            required_one_of=[['job_id', 'job_type']]
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

    def get_job_details(self, job_id):
        """
        Get the details of a job by ID.
        :param job_id: Specifies the job ID.
        :return: If exists returns details of the job, else returns None.
        """
        try:
            api_response = self.job_api.get_job_job(job_id)
            if api_response:
                response_dict = api_response.to_dict()
                if response_dict and 'jobs' in response_dict \
                        and len(response_dict['jobs']) > 0:
                    return response_dict['jobs'][0]
            return None
        except utils.ApiException as e:
            error_message = 'Failed to get job details for job %s ' \
                            'with error: %s' % (job_id, utils.determine_error
                                                (error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def find_job_by_type(self, job_type):
        """
        Find a running job by type.
        :param job_type: The job type to search for.
        :return: First matching running job or None.
        """
        try:
            api_response = self.job_api.list_job_jobs()
            if api_response:
                response_dict = api_response.to_dict()
                if response_dict and 'jobs' in response_dict:
                    for job in response_dict['jobs']:
                        if job.get('type') == job_type and job.get(
                            'state') in RUNNING_STATES + PAUSED_STATES:
                            return job
            return None
        except utils.ApiException as e:
            error_message = 'Failed to list jobs with error: %s' \
                            % (utils.determine_error(error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def start_job(self, params):
        """
        Start a new job.
        :param params: Dictionary containing job parameters.
        :return: The created job response.
        """
        try:
            create_params = {
                'type': params['job_type']
            }
            if params.get('paths'):
                create_params['paths'] = params['paths']
            if params.get('priority') is not None:
                create_params['priority'] = params['priority']
            if params.get('policy'):
                create_params['policy'] = params['policy']
            if params.get('allow_dup'):
                create_params['allow_dup'] = params['allow_dup']
            if params.get('job_params'):
                create_params['changelistcreate_params'] = params['job_params']

            body = self.isi_sdk.JobJobCreateParams(**create_params)
            api_response = self.job_api.create_job_job(body)
            if api_response:
                return api_response.to_dict()
            return None
        except utils.ApiException as e:
            error_message = 'Failed to start job of type %s with ' \
                            'error: %s' % (params['job_type'],
                                           utils.determine_error(error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def modify_job(self, job_id, **kwargs):
        """
        Modify an existing job.
        :param job_id: The job ID to modify.
        :param kwargs: Keyword arguments for modification (control, priority,
            policy).
        :return: True if modification is successful.
        """
        try:
            update_params = {}
            if 'control' in kwargs and kwargs['control'] is not None:
                # SDK uses 'state' to control job (pause, resume, cancel)
                update_params['state'] = kwargs['control']
            if 'priority' in kwargs and kwargs['priority'] is not None:
                update_params['priority'] = kwargs['priority']
            if 'policy' in kwargs and kwargs['policy'] is not None:
                update_params['policy'] = kwargs['policy']

            body = self.isi_sdk.JobJob(**update_params)
            self.job_api.update_job_job(body, job_id)
            return True
        except utils.ApiException as e:
            error_message = 'Failed to modify job %s with error: %s' \
                            % (job_id, utils.determine_error(error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def wait_for_completion(self, job_id, timeout, interval):
        """
        Wait for a job to reach a terminal state.
        :param job_id: The job ID to monitor.
        :param timeout: Maximum wait time in seconds.
        :param interval: Polling interval in seconds.
        :return: The final job details.
        """
        elapsed = 0
        while elapsed < timeout:
            job_details = self.get_job_details(job_id)
            if job_details is None:
                LOG.warning("Job %s not found during wait", job_id)
                return None
            current_state = job_details.get('state', '')
            if current_state in TERMINAL_STATES:
                LOG.info("Job %s reached terminal state: %s",
                         job_id, current_state)
                return job_details
            LOG.info("Job %s in state %s, waiting... (%d/%d seconds)",
                     job_id, current_state, elapsed, timeout)
            time.sleep(interval)
            elapsed += interval

        error_message = 'Job %s timed out waiting for completion ' \
                        'after %d seconds' % (job_id, timeout)
        LOG.error(error_message)
        self.module.fail_json(msg=error_message)

    def validate_start_params(self):
        """Validate parameters required for starting a job."""
        job_type = self.module.params.get('job_type')
        paths = self.module.params.get('paths')
        priority = self.module.params.get('priority')

        if job_type:
            if paths is None or (isinstance(paths, list) and len(paths) == 0):
                self.module.fail_json(
                    msg="The paths parameter is required when starting "
                        "a job and must contain at least one path.")

        if priority is not None and (priority < 1 or priority > 10):
            self.module.fail_json(
                msg="Invalid priority %d. Priority must be between "
                    "1 and 10." % priority)

    def perform_module_operation(self):
        """
        Perform different actions on job module based on parameters
        chosen in playbook.
        """
        job_id = self.module.params.get('job_id')
        job_type = self.module.params.get('job_type')
        job_state = self.module.params.get('job_state')
        paths = self.module.params.get('paths')
        priority = self.module.params.get('priority')
        policy = self.module.params.get('policy')
        allow_dup = self.module.params.get('allow_dup')
        wait = self.module.params.get('wait')
        wait_timeout = self.module.params.get('wait_timeout')
        wait_interval = self.module.params.get('wait_interval')

        changed = False
        outcome = 'noop'
        job_details = None
        diff_dict = {}

        # Validate that either job_id or job_type is provided
        if not job_type and job_id is None:
            self.module.fail_json(
                msg="Either job_id or job_type must be specified.")

        # Validate input parameters
        self.validate_start_params()

        # Start scenario: job_type provided
        if job_type:
            existing_job = self.find_job_by_type(job_type)

            if existing_job and not allow_dup:
                # Job of same type already running and duplicates not allowed
                LOG.info("Job of type %s already running (ID: %s), "
                         "allow_dup is false. No-op.",
                         job_type, existing_job.get('id'))
                outcome = 'noop'
                job_details = existing_job
            else:
                # Start a new job
                if self.module._diff:
                    diff_dict = {
                        'before': {},
                        'after': {'type': job_type, 'state': 'running'}
                    }

                if not self.module.check_mode:
                    start_response = self.start_job({
                        'job_type': job_type,
                        'paths': paths,
                        'priority': priority,
                        'policy': policy,
                        'allow_dup': allow_dup,
                        'job_params': self.module.params.get('job_params')
                    })

                    if start_response and 'id' in start_response:
                        new_job_id = start_response['id']
                        job_details = self.get_job_details(new_job_id)

                        # Wait for completion if requested
                        if wait and job_details:
                            job_details = self.wait_for_completion(
                                new_job_id, wait_timeout, wait_interval)

                        if self.module._diff and job_details:
                            diff_dict['after'] = job_details
                    else:
                        job_details = start_response

                changed = True
                outcome = 'started'

        # Control scenario: job_id provided
        elif job_id:
            job_details = self.get_job_details(job_id)

            if job_details is None:
                self.module.fail_json(
                    msg="Failed to get job details for job %d: "
                        "not found." % job_id)

            current_state = job_details.get('state', '')
            before_details = dict(job_details) if job_details else {}

            # Handle job_state transitions
            if job_state == 'paused':
                if current_state in RUNNING_STATES:
                    if self.module._diff:
                        diff_dict = {
                            'before': before_details,
                            'after': dict(before_details, state='paused_user')
                        }
                    if not self.module.check_mode:
                        self.modify_job(job_id, control='pause')
                        job_details = self.get_job_details(job_id)
                        if self.module._diff and job_details:
                            diff_dict['after'] = job_details
                    changed = True
                    outcome = 'paused'
                elif current_state in PAUSED_STATES:
                    LOG.info("Job %s is already in paused state: %s",
                             job_id, current_state)
                    outcome = 'noop'
                elif current_state in TERMINAL_STATES:
                    self.module.fail_json(
                        msg="Cannot pause job %d in terminal state '%s'."
                            % (job_id, current_state))

            elif job_state == 'running':
                if current_state in PAUSED_STATES:
                    if self.module._diff:
                        diff_dict = {
                            'before': before_details,
                            'after': dict(before_details, state='running')
                        }
                    if not self.module.check_mode:
                        self.modify_job(job_id, control='run')
                        job_details = self.get_job_details(job_id)
                        if self.module._diff and job_details:
                            diff_dict['after'] = job_details
                    changed = True
                    outcome = 'resumed'
                elif current_state in RUNNING_STATES:
                    LOG.info("Job %s is already running.", job_id)
                    outcome = 'noop'
                elif current_state in TERMINAL_STATES:
                    self.module.fail_json(
                        msg="Cannot resume job %d in terminal state '%s'."
                            % (job_id, current_state))

            elif job_state == 'cancelled':
                if current_state in RUNNING_STATES + PAUSED_STATES:
                    if self.module._diff:
                        diff_dict = {
                            'before': before_details,
                            'after': dict(before_details,
                                          state='cancelled_user')
                        }
                    if not self.module.check_mode:
                        self.modify_job(job_id, control='cancel')
                        job_details = self.get_job_details(job_id)
                        if self.module._diff and job_details:
                            diff_dict['after'] = job_details
                    changed = True
                    outcome = 'cancelled'
                elif current_state in TERMINAL_STATES:
                    self.module.fail_json(
                        msg="Cannot cancel job %d in terminal state '%s'."
                            % (job_id, current_state))

            # Handle priority/policy modifications
            if priority is not None or policy is not None:
                modify_kwargs = {}
                needs_modify = False

                if priority is not None \
                        and job_details.get('priority') != priority:
                    modify_kwargs['priority'] = priority
                    needs_modify = True

                if policy is not None \
                        and job_details.get('policy') != policy:
                    modify_kwargs['policy'] = policy
                    needs_modify = True

                if needs_modify:
                    if self.module._diff:
                        if not diff_dict:
                            diff_dict = {
                                'before': before_details,
                                'after': dict(
                                    job_details if job_details else {},
                                    **modify_kwargs)
                            }
                        else:
                            diff_dict['after'].update(modify_kwargs)

                    if not self.module.check_mode:
                        self.modify_job(job_id, **modify_kwargs)
                        job_details = self.get_job_details(job_id)
                        if self.module._diff and job_details:
                            diff_dict['after'] = job_details

                    changed = True
                    if outcome == 'noop':
                        outcome = 'modified'

        result = dict(
            changed=changed,
            job_details=job_details,
            outcome=outcome
        )

        if self.module._diff and diff_dict:
            result['diff'] = diff_dict

        self.module.exit_json(**result)


def get_job_parameters():
    """
    This method provides parameters required for the ansible job
    module on PowerScale.
    """
    return dict(
        job_id=dict(type='int'),
        job_type=dict(type='str'),
        job_state=dict(type='str',
                       choices=['started', 'paused', 'running', 'cancelled']),
        paths=dict(type='list', elements='str'),
        priority=dict(type='int'),
        policy=dict(type='str'),
        allow_dup=dict(type='bool', default=False),
        job_params=dict(type='dict'),
        wait=dict(type='bool', default=False),
        wait_timeout=dict(type='int', default=300),
        wait_interval=dict(type='int', default=10),
        state=dict(type='str', choices=['present'], default='present')
    )


def main():
    """Create PowerScale Job object and perform action on it
    based on user input from playbook"""
    obj = Job()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
