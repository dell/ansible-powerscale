#!/usr/bin/python
# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for retrieving job information on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: job_info

version_added: '4.0.0'

short_description: Retrieve job information from PowerScale
description:
- Retrieving job information from a PowerScale storage system includes
  getting details of a specific job, listing jobs with filters, fetching
  recent jobs, and obtaining job summary statistics.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Shrinidhi Rao (@shrinidhirao) <ansible.team@dell.com>

options:
  job_id:
    description:
    - The ID of a specific job to retrieve.
    - When specified, other filter options are ignored.
    type: int

  state:
    description:
    - Filter jobs by their current state.
    - Multiple states can be specified to match any of the given states.
    type: list
    elements: str
    choices: ['running', 'paused_user', 'paused_system', 'paused_policy', 'paused_priority']

  job_type:
    description:
    - Filter jobs by their type.
    - This is a client-side filter applied after retrieving jobs from the API.
    - Multiple types can be specified.
    type: list
    elements: str

  sort:
    description:
    - The field to sort results by.
    type: str

  dir:
    description:
    - The sort direction.
    type: str
    choices: ['ASC', 'DESC']
    default: 'ASC'

  limit:
    description:
    - The maximum number of jobs to return.
    type: int

  include_recent:
    description:
    - Whether to include recently completed jobs in the response.
    type: bool
    default: false

  include_summary:
    description:
    - Whether to include job summary statistics in the response.
    type: bool
    default: false

notes:
- This is a read-only info module. It does not modify any resources.
- The I(check_mode) is supported.

requirements:
- JIRA ECS02C-841
'''

EXAMPLES = r'''
- name: Get a specific job by ID
  dellemc.powerscale.job_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    job_id: 42

- name: List all jobs
  dellemc.powerscale.job_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"

- name: List running jobs sorted by ID descending
  dellemc.powerscale.job_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    state:
      - running
    sort: "id"
    dir: "DESC"
    limit: 10

- name: List jobs filtered by type
  dellemc.powerscale.job_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    job_type:
      - SmartPools

- name: Get all jobs with recent jobs and summary
  dellemc.powerscale.job_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    include_recent: true
    include_summary: true
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool

job_details:
    description: List of job detail dictionaries.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: The unique identifier of the job.
            type: int
        type:
            description: The type of the job.
            type: str
        state:
            description: The current state of the job.
            type: str
        priority:
            description: The priority of the job.
            type: int
        policy:
            description: The scheduling policy of the job.
            type: str
        description:
            description: A description of the job.
            type: str
        start_time:
            description: The start time of the job in unix epoch seconds.
            type: int
        end_time:
            description: The end time of the job in unix epoch seconds.
            type: int
        progress:
            description: The progress percentage of the job.
            type: int
        paths:
            description: The paths associated with the job.
            type: list
            elements: str

total_jobs:
    description: The total number of jobs returned.
    returned: always
    type: int

recent_jobs:
    description: List of recently completed jobs.
    returned: When I(include_recent) is true
    type: list
    elements: dict

job_summary:
    description: Summary statistics for jobs.
    returned: When I(include_summary) is true
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('job_info')


class JobInfo(object):
    """Class with Job Info operations"""

    def __init__(self):
        """Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_job_info_parameters())

        # initialize the Ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=True
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
        Get the details of a specific job by ID.
        :param job_id: The ID of the job to retrieve
        :return: Job details dict or None if not found
        """
        try:
            api_response = self.job_api.get_job_job(job_id)
            return api_response.to_dict()
        except utils.ApiException as e:
            error_message = 'Failed to get job details for job ID %s ' \
                            'with error: %s' % (job_id, utils.determine_error
                                                (error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def list_jobs(self, **params):
        """
        List jobs with optional filters.
        :param params: Filter parameters (state, sort, dir, limit)
        :return: Dict with 'jobs' key containing list of job dicts
        """
        try:
            api_response = self.job_api.list_job_jobs(**params)
            return api_response.to_dict()
        except utils.ApiException as e:
            error_message = 'Failed to list jobs with error: %s' \
                            % (utils.determine_error(error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_recent_jobs(self):
        """
        Get recently completed jobs.
        :return: Dict with 'jobs' key containing list of recent job dicts
        """
        try:
            api_response = self.job_api.get_job_recent()
            return api_response.to_dict()
        except utils.ApiException as e:
            error_message = 'Failed to get recent jobs with error: %s' \
                            % (utils.determine_error(error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_job_summary(self):
        """
        Get job summary statistics.
        :return: Dict with job summary information
        """
        try:
            api_response = self.job_api.get_job_job_summary()
            return api_response.to_dict()
        except utils.ApiException as e:
            error_message = 'Failed to get job summary with error: %s' \
                            % (utils.determine_error(error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def perform_module_operation(self):
        """
        Perform different actions on job info module based on parameters
        chosen in playbook
        """
        job_id = self.module.params['job_id']
        state_filter = self.module.params['state']
        job_type_filter = self.module.params['job_type']
        sort = self.module.params['sort']
        dir_param = self.module.params['dir']
        limit = self.module.params['limit']
        include_recent = self.module.params['include_recent']
        include_summary = self.module.params['include_summary']

        result = dict(
            changed=False,
            job_details=[],
            total_jobs=0,
            recent_jobs=None,
            job_summary=None
        )

        # If job_id is specified, get that specific job
        if job_id is not None:
            job_details = self.get_job_details(job_id)
            if job_details is not None:
                result['job_details'] = [job_details] if not isinstance(job_details, list) else job_details
                result['total_jobs'] = len(result['job_details'])
        else:
            # Build filter parameters for list_job_jobs
            params = {}
            if sort:
                params['sort'] = sort
            if dir_param:
                params['dir'] = dir_param
            if limit is not None:
                params['limit'] = limit

            # Handle multiple state filters by making separate calls
            if state_filter and len(state_filter) > 1:
                job_details = []
                seen_ids = set()
                for s in state_filter:
                    state_params = dict(params, state=s)
                    jobs_response = self.list_jobs(**state_params)
                    for job in (jobs_response.get('jobs', [])
                                if jobs_response else []):
                        jid = job.get('id')
                        if jid not in seen_ids:
                            seen_ids.add(jid)
                            job_details.append(job)
            elif state_filter:
                params['state'] = state_filter[0]
                jobs_response = self.list_jobs(**params)
                job_details = jobs_response.get('jobs', []) \
                    if jobs_response else []
            else:
                jobs_response = self.list_jobs(**params)
                job_details = jobs_response.get('jobs', []) \
                    if jobs_response else []

            # Apply client-side job_type filter
            if job_type_filter and job_details:
                job_details = [job for job in job_details
                               if job.get('type') in job_type_filter]

            result['job_details'] = job_details
            result['total_jobs'] = len(job_details)

        # Include recent jobs if requested
        if include_recent:
            recent_response = self.get_recent_jobs()
            result['recent_jobs'] = recent_response.get('jobs', []) \
                if recent_response else []

        # Include job summary if requested
        if include_summary:
            result['job_summary'] = self.get_job_summary()

        self.module.exit_json(**result)


def get_job_info_parameters():
    """
    This method provides parameters required for the ansible job info
    module on PowerScale
    """
    return dict(
        job_id=dict(type='int'),
        state=dict(type='list', elements='str',
                   choices=['running', 'paused_user', 'paused_system',
                            'paused_policy', 'paused_priority']),
        job_type=dict(type='list', elements='str'),
        sort=dict(type='str'),
        dir=dict(type='str', choices=['ASC', 'DESC'], default='ASC'),
        limit=dict(type='int'),
        include_recent=dict(type='bool', default=False),
        include_summary=dict(type='bool', default=False)
    )


def main():
    """Create PowerScale Job Info object and perform action on it
       based on user input from playbook"""
    obj = JobInfo()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
