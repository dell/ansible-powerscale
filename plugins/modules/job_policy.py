#!/usr/bin/python
# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing job policies on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: job_policy

version_added: '4.0.0'

short_description: Manage job policies on PowerScale

description:
- Managing job policies on PowerScale storage system includes creating,
  modifying, deleting, and retrieving details of job policies.
- Job policies define impact schedules that control when and how
  aggressively background jobs consume system resources.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Shrinidhi Rao (@shrinidhirao) <ansible.team@dell.com>

notes:
- Refer to JIRA ECS02C-982 for feature details.
- System policies cannot be modified or deleted.
- The I(check_mode) is supported.

options:
  policy_name:
    description:
    - The name of the job policy.
    - Required when I(state) is C(present).
    type: str

  policy_id:
    description:
    - The unique identifier of the job policy.
    - Can be used to identify the policy for get, modify, or delete operations.
    type: str

  description:
    description:
    - Description of the job policy.
    type: str
    default: ''

  intervals:
    description:
    - List of interval definitions for the job policy schedule.
    - Each interval specifies a time window and its impact level.
    type: list
    elements: dict
    suboptions:
      begin:
        description:
        - The start time of the interval in C(WWWW HH:MM) format
          (e.g. C(Monday 08:00)).
        type: str
        required: true
      end:
        description:
        - The end time of the interval in C(WWWW HH:MM) format
          (e.g. C(Monday 17:00)).
        type: str
        required: true
      impact:
        description:
        - The impact level for the interval.
        type: str
        required: true
        choices: ['Low', 'Medium', 'High', 'Paused']

  state:
    description:
    - The state of the job policy.
    - C(present) - The policy should exist on the system.
    - C(absent) - The policy should not exist on the system.
    choices: ['present', 'absent']
    type: str
    default: present
'''

EXAMPLES = r'''
- name: Create a job policy
  dellemc.powerscale.job_policy:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    policy_name: "custom_low_impact"
    description: "Low impact policy for overnight jobs"
    intervals:
      - begin: "Monday 00:00"
        end: "Monday 06:00"
        impact: "Low"
      - begin: "Monday 06:00"
        end: "Monday 18:00"
        impact: "Paused"
    state: "present"

- name: Modify a job policy description
  dellemc.powerscale.job_policy:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    policy_name: "custom_low_impact"
    description: "Updated low impact policy"
    state: "present"

- name: Modify a job policy intervals
  dellemc.powerscale.job_policy:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    policy_name: "custom_low_impact"
    intervals:
      - begin: "Monday 00:00"
        end: "Monday 08:00"
        impact: "Medium"
    state: "present"

- name: Get job policy details
  dellemc.powerscale.job_policy:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    policy_name: "custom_low_impact"
    state: "present"

- name: Delete a job policy by name
  dellemc.powerscale.job_policy:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    policy_name: "custom_low_impact"
    state: "absent"

- name: Delete a job policy by ID
  dellemc.powerscale.job_policy:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    policy_id: "custom_low_impact_id"
    state: "absent"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool

job_policy_details:
    description: The job policy details.
    returned: When job policy exists
    type: dict
    contains:
        id:
            description: The unique identifier of the policy.
            type: str
        name:
            description: The name of the policy.
            type: str
        description:
            description: The description of the policy.
            type: str
        intervals:
            description: The list of intervals for the policy.
            type: list
            contains:
                begin:
                    description: The start time of the interval.
                    type: str
                end:
                    description: The end time of the interval.
                    type: str
                impact:
                    description: The impact level.
                    type: str
        system:
            description: Whether this is a system policy.
            type: bool
    sample: {
        "id": "custom_low_impact",
        "name": "custom_low_impact",
        "description": "Low impact policy for overnight jobs",
        "intervals": [
            {
                "begin": "Monday 00:00",
                "end": "Monday 06:00",
                "impact": "Low"
            }
        ],
        "system": false
    }

diff:
    description: The before/after diff when running in diff mode.
    returned: When diff mode is enabled
    type: dict
    contains:
        before:
            description: The policy state before the operation.
            type: dict
        after:
            description: The policy state after the operation.
            type: dict
'''

import re
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('job_policy')

# Pattern for interval time format: "WWWW HH:MM"
INTERVAL_TIME_PATTERN = re.compile(
    r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s+'
    r'([01]\d|2[0-3]):([0-5]\d)$'
)

VALID_IMPACT_VALUES = ('Low', 'Medium', 'High', 'Paused')


class JobPolicy(object):
    """Class with Job Policy operations"""

    def __init__(self):
        """Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_job_policy_parameters())

        # initialize the Ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=True,
            required_if=[
                ['state', 'present', ['policy_name']],
                ['state', 'absent', ['policy_name', 'policy_id'], True]
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

    def get_policy_by_name(self, name):
        """
        Get a job policy by name.
        :param name: The name of the policy.
        :return: The policy dict if found, else None.
        """
        try:
            api_response = self.job_api.list_job_policies()
            if api_response:
                response_dict = api_response.to_dict()
                if response_dict and 'policies' in response_dict:
                    for policy in response_dict['policies']:
                        if policy.get('name') == name:
                            return policy
            return None
        except utils.ApiException as e:
            error_message = 'Failed to get job policy %s with ' \
                            'error: %s' % (name, utils.determine_error
                                           (error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_policy_details(self, policy_id):
        """
        Get a job policy by ID.
        :param policy_id: The policy ID.
        :return: The policy dict if found, else None.
        """
        try:
            api_response = self.job_api.get_job_policy(policy_id)
            if api_response:
                response_dict = api_response.to_dict()
                if response_dict and 'policies' in response_dict \
                        and len(response_dict['policies']) > 0:
                    return response_dict['policies'][0]
            return None
        except utils.ApiException as e:
            if str(e.status) == '404':
                LOG.info("Job policy %s not found", policy_id)
                return None
            error_message = 'Failed to get job policy %s with ' \
                            'error: %s' % (policy_id, utils.determine_error
                                           (error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def create_policy(self, name, description, intervals):
        """
        Create a new job policy.
        :param name: The policy name.
        :param description: The policy description.
        :param intervals: The list of intervals.
        :return: True if creation is successful.
        """
        try:
            create_params = {
                'name': name
            }
            if description is not None:
                create_params['description'] = description
            if intervals is not None:
                create_params['intervals'] = intervals

            body = self.isi_sdk.JobPolicyCreateParams(**create_params)
            self.job_api.create_job_policy(body)
            return True
        except utils.ApiException as e:
            error_message = 'Failed to create job policy %s with ' \
                            'error: %s' % (name, utils.determine_error
                                           (error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def modify_policy(self, policy_id, **kwargs):
        """
        Modify an existing job policy.
        :param policy_id: The policy ID to modify.
        :param kwargs: Keyword arguments for modification (description,
            intervals).
        :return: True if modification is successful.
        """
        try:
            update_params = {}
            if 'description' in kwargs:
                update_params['description'] = kwargs['description']
            if 'intervals' in kwargs:
                update_params['intervals'] = kwargs['intervals']

            body = self.isi_sdk.JobPolicy(**update_params)
            self.job_api.update_job_policy(body, policy_id)
            return True
        except utils.ApiException as e:
            error_message = 'Failed to modify job policy %s with ' \
                            'error: %s' % (policy_id, utils.determine_error
                                           (error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete_policy(self, policy_id):
        """
        Delete a job policy.
        :param policy_id: The policy ID to delete.
        :return: True if deletion is successful.
        """
        try:
            self.job_api.delete_job_policy(policy_id)
            return True
        except utils.ApiException as e:
            error_message = 'Failed to delete job policy %s with ' \
                            'error: %s' % (policy_id, utils.determine_error
                                           (error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def is_policy_modified(self, current, desired):
        """
        Check if the policy needs to be modified.
        :param current: The current policy dict.
        :param desired: The desired policy attributes dict.
        :return: Tuple of (bool, dict_of_changes).
        """
        changes = {}

        # Check description change
        if 'description' in desired and desired['description'] is not None:
            if current.get('description', '') != desired['description']:
                changes['description'] = desired['description']

        # Check intervals change
        if 'intervals' in desired and desired['intervals'] is not None:
            current_intervals = current.get('intervals', [])
            desired_intervals = desired['intervals']

            if not self._intervals_equal(current_intervals,
                                         desired_intervals):
                changes['intervals'] = desired_intervals

        modified = len(changes) > 0
        return modified, changes

    def _intervals_equal(self, current, desired):
        """
        Compare two lists of intervals for equality.
        :param current: Current intervals list.
        :param desired: Desired intervals list.
        :return: True if equal, False otherwise.
        """
        if len(current) != len(desired):
            return False

        for curr, des in zip(current, desired):
            if curr.get('begin') != des.get('begin'):
                return False
            if curr.get('end') != des.get('end'):
                return False
            if curr.get('impact') != des.get('impact'):
                return False

        return True

    def _policy_equal(self, before, after):
        """
        Compare two policy dicts returned by the API to check for
        actual changes (handles API normalization of intervals).
        :param before: Policy dict before modification.
        :param after: Policy dict after modification.
        :return: True if policies are equivalent.
        """
        if before.get('description', '') != after.get('description', ''):
            return False
        before_intervals = before.get('intervals', [])
        after_intervals = after.get('intervals', [])
        return self._intervals_equal(before_intervals, after_intervals)

    def validate_intervals(self, intervals):
        """
        Validate the interval format.
        :param intervals: The list of interval dicts to validate.
        """
        if intervals is None:
            return

        for interval in intervals:
            begin = interval.get('begin', '')
            end = interval.get('end', '')
            impact = interval.get('impact', '')

            if not INTERVAL_TIME_PATTERN.match(begin):
                self.module.fail_json(
                    msg="Invalid interval begin time '%s'. "
                        "Expected format 'WWWW HH:MM' "
                        "(e.g. 'Monday 08:00')." % begin)
            if not INTERVAL_TIME_PATTERN.match(end):
                self.module.fail_json(
                    msg="Invalid interval end time '%s'. "
                        "Expected format 'WWWW HH:MM' "
                        "(e.g. 'Monday 17:00')." % end)
            if impact not in VALID_IMPACT_VALUES:
                self.module.fail_json(
                    msg="Invalid impact value '%s'. "
                        "Must be one of: %s."
                        % (impact, ', '.join(VALID_IMPACT_VALUES)))

    def perform_module_operation(self):
        """
        Perform different actions on job policy module based on parameters
        chosen in playbook.
        """
        policy_name = self.module.params.get('policy_name')
        policy_id = self.module.params.get('policy_id')
        description = self.module.params.get('description')
        intervals = self.module.params.get('intervals')
        state = self.module.params.get('state')

        changed = False
        job_policy_details = None
        diff_dict = {}

        # Validate intervals format
        self.validate_intervals(intervals)

        # Get existing policy
        existing = None
        if policy_name:
            existing = self.get_policy_by_name(policy_name)
        elif policy_id:
            existing = self.get_policy_details(policy_id)

        if state == 'present':
            if not policy_name:
                self.module.fail_json(
                    msg="policy_name is required when state is present.")

            if existing:
                # Check if modification is needed
                desired = {}
                if description:
                    desired['description'] = description
                if intervals is not None:
                    desired['intervals'] = intervals

                modified, changes = self.is_policy_modified(existing, desired)

                if modified:
                    # Check if it is a system policy
                    if existing.get('system', False):
                        self.module.fail_json(
                            msg="Cannot modify system policy '%s'. "
                                "System policies are read-only."
                                % policy_name)

                    if not self.module.check_mode:
                        self.modify_policy(existing['id'], **changes)

                        # Re-fetch to check if API actually changed
                        updated = self.get_policy_by_name(policy_name)
                        if updated and self._policy_equal(existing, updated):
                            changed = False
                            LOG.info(
                                "Job policy %s: API normalized values "
                                "match existing state. No real change.",
                                policy_name)
                        else:
                            changed = True
                            if self.module._diff:
                                diff_dict = {
                                    'before': existing,
                                    'after': updated if updated else
                                    dict(existing, **changes)
                                }
                    else:
                        changed = True
                        if self.module._diff:
                            diff_dict = {
                                'before': existing,
                                'after': dict(existing, **changes)
                            }
                else:
                    LOG.info("Job policy %s is already in the desired state.",
                             policy_name)
            else:
                # Create new policy
                if self.module._diff:
                    diff_dict = {
                        'before': {},
                        'after': {
                            'name': policy_name,
                            'description': description,
                            'intervals': intervals
                        }
                    }

                if not self.module.check_mode:
                    self.create_policy(policy_name, description, intervals)

                    if self.module._diff:
                        created = self.get_policy_by_name(policy_name)
                        if created:
                            diff_dict['after'] = created

                changed = True

        elif state == 'absent':
            if existing:
                # Check if it is a system policy
                if existing.get('system', False):
                    self.module.fail_json(
                        msg="Cannot delete system policy '%s'. "
                            "System policies cannot be removed."
                            % existing.get('name', policy_id))

                if self.module._diff:
                    diff_dict = {
                        'before': existing,
                        'after': {}
                    }

                if not self.module.check_mode:
                    self.delete_policy(existing['id'])

                changed = True
            else:
                LOG.info("Job policy does not exist. No action needed.")

        # Get final policy details for output
        if state == 'present' and not self.module.check_mode:
            if policy_name:
                job_policy_details = self.get_policy_by_name(policy_name)
            elif policy_id:
                job_policy_details = self.get_policy_details(policy_id)
        elif state == 'present' and self.module.check_mode:
            # In check mode return existing or projected details
            if existing and not changed:
                job_policy_details = existing
            elif existing and changed:
                # Return projected details
                job_policy_details = dict(existing)
                if description is not None:
                    job_policy_details['description'] = description
                if intervals is not None:
                    job_policy_details['intervals'] = intervals
            else:
                job_policy_details = {
                    'name': policy_name,
                    'description': description,
                    'intervals': intervals
                }

        result = dict(
            changed=changed,
            job_policy_details=job_policy_details
        )

        if self.module._diff and diff_dict:
            result['diff'] = diff_dict

        self.module.exit_json(**result)


def get_job_policy_parameters():
    """
    This method provides parameters required for the ansible job policy
    module on PowerScale.
    """
    return dict(
        policy_name=dict(type='str'),
        policy_id=dict(type='str'),
        description=dict(type='str', default=''),
        intervals=dict(
            type='list',
            elements='dict',
            options=dict(
                begin=dict(type='str', required=True),
                end=dict(type='str', required=True),
                impact=dict(type='str', required=True,
                            choices=['Low', 'Medium', 'High', 'Paused'])
            )
        ),
        state=dict(type='str', choices=['present', 'absent'],
                   default='present')
    )


def main():
    """Create PowerScale Job Policy object and perform action on it
    based on user input from playbook"""
    obj = JobPolicy()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
