#!/usr/bin/python
# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing Jobs on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: job
version_added: '3.0.0'
short_description: Manage Jobs on a PowerScale Storage System
description:
- Managing jobs on a PowerScale system includes creating, modifying,
  retrieving details, and gathering information about jobs.
- Supports starting new jobs, pausing, resuming, and cancelling running jobs.
- Provides gather functionality for job events, reports, types, statistics,
  recent jobs, and job summary.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Dell Technologies Ansible Team <ansible.team@dell.com>

options:
  job_id:
    description:
    - The ID of an existing job.
    - Required for get and modify operations.
    type: int
  job_type:
    description:
    - The type of job to create (e.g., TreeDelete, QuotaScan).
    - Required for create operations.
    type: str
  job_state:
    description:
    - The desired state of the job.
    - Use C(run) to start or resume a job.
    - Use C(pause) to pause a running job.
    - Use C(cancel) to cancel a running job.
    type: str
    choices: ['run', 'pause', 'cancel']
  paths:
    description:
    - List of paths for the job to operate on.
    type: list
    elements: str
  policy:
    description:
    - The impact policy for the job.
    type: str
  priority:
    description:
    - The priority of the job.
    type: int
  gather_subset:
    description:
    - List of information subsets to gather.
    type: list
    elements: str
    choices: ['jobs', 'events', 'reports', 'types', 'statistics', 'recent', 'summary']
  filter_state:
    description:
    - Filter jobs by state when listing.
    type: str
  sort:
    description:
    - Field to sort results by.
    type: str
  sort_dir:
    description:
    - Sort direction.
    type: str
    choices: ['ASC', 'DESC']
  limit:
    description:
    - Maximum number of results to return.
    type: int
  begin:
    description:
    - Filter events starting from this time.
    type: int
  end:
    description:
    - Filter events ending at this time.
    type: int
  event_key:
    description:
    - Filter events by key.
    type: str
  show_all:
    description:
    - Show all job types including hidden ones.
    type: bool
    default: false
  verbose:
    description:
    - Enable verbose output.
    type: bool
    default: false
  state:
    description:
    - Defines whether the job should exist or not.
    - Value C(present) indicates that the job should exist in system.
    - Value C(absent) indicates that the job should not exist in system.
    type: str
    choices: ['absent', 'present']
    default: present
notes:
- The I(check_mode) is supported.
'''

EXAMPLES = r'''
- name: Create a TreeDelete job
  dellemc.powerscale.job:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"  # example
    verify_ssl: "{{ verify_ssl }}"
    job_type: "TreeDelete"
    paths:
      - "/ifs/data"
    state: "present"

- name: Get job details
  dellemc.powerscale.job:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"  # example
    verify_ssl: "{{ verify_ssl }}"
    job_id: 12345
    state: "present"

- name: Pause a running job
  dellemc.powerscale.job:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"  # example
    verify_ssl: "{{ verify_ssl }}"
    job_id: 12345
    job_state: "pause"
    state: "present"

- name: Gather job events
  dellemc.powerscale.job:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"  # example
    verify_ssl: "{{ verify_ssl }}"
    gather_subset:
      - "events"
'''

RETURN = r'''
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
job_details:
    description: The job details for single job operations.
    type: dict
    returned: when performing single job operations
jobs:
    description: List of jobs when using gather_subset with jobs.
    type: dict
    returned: when gather_subset includes jobs
job_events:
    description: Job events information.
    type: dict
    returned: when gather_subset includes events
job_reports:
    description: Job reports information.
    type: dict
    returned: when gather_subset includes reports
job_types:
    description: Job types information.
    type: dict
    returned: when gather_subset includes types
job_statistics:
    description: Job statistics information.
    type: dict
    returned: when gather_subset includes statistics
recent_jobs:
    description: Recently completed jobs.
    type: dict
    returned: when gather_subset includes recent
job_summary:
    description: Job summary information.
    type: dict
    returned: when gather_subset includes summary
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('job')


class Job:
    """Class with Job operations"""

    def __init__(self):
        """Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(self.get_job_parameters())
        # Initialize the ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=True
        )
        # Result is a dictionary that contains changed status and job details
        self.result = {
            "changed": False,
            "job_details": {}
        }

        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        LOG.info('Got python SDK instance for provisioning on PowerScale')
        check_mode_msg = f'Check mode flag is {self.module.check_mode}'
        LOG.info(check_mode_msg)

        self.job_api = self.isi_sdk.JobApi(self.api_client)

    def get_job_details(self, job_id):
        """
        Get details of a specific job by ID.
        :param job_id: ID of the job
        :return: dict with job details or None
        """
        try:
            msg = f"Getting job details for job ID: {job_id}"
            LOG.info(msg)
            response = self.job_api.get_job_job(job_id)
            if response:
                raw = response.to_dict()
                # Unwrap nested response (API may return {"jobs": [...]})
                if isinstance(raw, dict) and 'jobs' in raw:
                    inner = raw['jobs']
                    if isinstance(inner, list) and inner:
                        job_dict = inner[0]
                    elif isinstance(inner, dict):
                        job_dict = inner
                    else:
                        job_dict = raw
                else:
                    job_dict = raw
                msg = f"Job details are: {job_dict}"
                LOG.info(msg)
                return job_dict
        except Exception as e:
            error_msg = f"Failed to get job details with error: " \
                        f"{utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def create_job(self, params):
        """
        Create a new job.
        :param params: dict with job parameters
        :return: dict with created job details
        """
        try:
            job_params = {"type": params['job_type']}
            if params.get('paths'):
                job_params['paths'] = params['paths']
            if params.get('policy'):
                job_params['policy'] = params['policy']
            if params.get('priority') is not None:
                job_params['priority'] = params['priority']
            msg = f"Creating job with parameters: {job_params}"
            LOG.info(msg)
            response = self.job_api.create_job_job(job_job=job_params)
            if response:
                job_details = self.get_job_details(response.id)
                msg = f"Successfully created job with details: {job_details}"
                LOG.info(msg)
                return job_details
        except Exception as e:
            error_msg = f"Failed to create job with error: " \
                        f"{utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def modify_job(self, job_id, modify_dict):
        """
        Modify an existing job.
        :param job_id: ID of the job to modify
        :param modify_dict: dict with parameters to modify
        """
        try:
            msg = f"Modifying job {job_id} with parameters: {modify_dict}"
            LOG.info(msg)
            self.job_api.update_job_job(
                job_job=modify_dict, job_job_id=job_id)
            LOG.info("Successfully modified the job.")
        except Exception as e:
            error_msg = f"Failed to modify job with error: " \
                        f"{utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def list_jobs(self):
        """
        List all jobs.
        :return: dict with jobs list
        """
        try:
            msg = "Listing all jobs"
            LOG.info(msg)
            response = self.job_api.list_job_jobs()
            if response:
                raw = response.to_dict()
                return raw.get('jobs', raw) if isinstance(raw, dict) else raw
        except Exception as e:
            error_msg = f"Failed to list jobs with error: " \
                        f"{utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_job_events(self):
        """
        Get job events.
        :return: dict with events
        """
        try:
            msg = "Getting job events"
            LOG.info(msg)
            response = self.job_api.get_job_events()
            if response:
                return response.to_dict()
        except Exception as e:
            error_msg = f"Failed to get job events with error: " \
                        f"{utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_job_reports(self):
        """
        Get job reports.
        :return: dict with reports
        """
        try:
            msg = "Getting job reports"
            LOG.info(msg)
            response = self.job_api.get_job_reports()
            if response:
                return response.to_dict()
        except Exception as e:
            error_msg = f"Failed to get job reports with error: " \
                        f"{utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_job_types(self):
        """
        Get job types.
        :return: dict with types
        """
        try:
            msg = "Getting job types"
            LOG.info(msg)
            response = self.job_api.get_job_types()
            if response:
                return response.to_dict()
        except Exception as e:
            error_msg = f"Failed to get job types with error: " \
                        f"{utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_job_statistics(self):
        """
        Get job statistics.
        :return: dict with statistics
        """
        try:
            msg = "Getting job statistics"
            LOG.info(msg)
            response = self.job_api.get_job_statistics()
            if response:
                return response.to_dict()
        except Exception as e:
            error_msg = f"Failed to get job statistics with error: " \
                        f"{utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_recent_jobs(self):
        """
        Get recently completed jobs.
        :return: dict with recent jobs
        """
        try:
            msg = "Getting recent jobs"
            LOG.info(msg)
            response = self.job_api.get_job_recent()
            if response:
                return response.to_dict()
        except Exception as e:
            error_msg = f"Failed to get recent jobs with error: " \
                        f"{utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_job_summary(self):
        """
        Get job summary.
        :return: dict with summary
        """
        try:
            msg = "Getting job summary"
            LOG.info(msg)
            response = self.job_api.get_job_job_summary()
            if response:
                return response.to_dict()
        except Exception as e:
            error_msg = f"Failed to get job summary with error: " \
                        f"{utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    @staticmethod
    def get_job_parameters():
        """Get job parameters."""
        return dict(
            job_id=dict(type='int'),
            job_type=dict(type='str'),
            job_state=dict(type='str', choices=['run', 'pause', 'cancel']),
            paths=dict(type='list', elements='str'),
            policy=dict(type='str'),
            priority=dict(type='int'),
            state=dict(type='str', choices=['present', 'absent'],
                       default='present'),
            gather_subset=dict(type='list', elements='str'),
            filter_state=dict(type='str'),
            sort=dict(type='str'),
            sort_dir=dict(type='str', choices=['ASC', 'DESC']),
            limit=dict(type='int'),
            begin=dict(type='int'),
            end=dict(type='int'),
            event_key=dict(type='str'),
            show_all=dict(type='bool', default=False),
            verbose=dict(type='bool', default=False)
        )


class JobExitHandler:
    """JobExitHandler definition."""
    def handle(self, job_obj):
        """Handle."""
        job_obj.module.exit_json(**job_obj.result)


class JobGatherHandler:
    """JobGatherHandler definition."""
    def handle(self, job_obj, job_params):
        """Handle."""
        gather_subset = job_params.get('gather_subset', [])

        for subset in gather_subset:
            if subset == 'jobs':
                job_obj.result['jobs'] = job_obj.list_jobs()
            elif subset == 'events':
                job_obj.result['job_events'] = job_obj.get_job_events()
            elif subset == 'reports':
                job_obj.result['job_reports'] = job_obj.get_job_reports()
            elif subset == 'types':
                job_obj.result['job_types'] = job_obj.get_job_types()
            elif subset == 'statistics':
                job_obj.result['job_statistics'] = \
                    job_obj.get_job_statistics()
            elif subset == 'recent':
                job_obj.result['recent_jobs'] = job_obj.get_recent_jobs()
            elif subset == 'summary':
                job_obj.result['job_summary'] = job_obj.get_job_summary()

        JobExitHandler().handle(job_obj)


class JobModifyHandler:
    """JobModifyHandler definition."""
    def handle(self, job_obj, job_params, job_details):
        """Handle."""
        if job_params.get('state') == 'present' and job_details:
            modify_dict = self._get_modify_dict(job_params, job_details)

            if modify_dict:
                before = dict(job_details) if getattr(
                    job_obj.module, '_diff', False) else None
                job_obj.result['changed'] = True
                if not job_obj.module.check_mode:
                    job_obj.modify_job(job_params['job_id'], modify_dict)
                    job_details = job_obj.get_job_details(
                        job_params['job_id'])
                if before is not None:
                    job_obj.result['diff'] = {
                        'before': before,
                        'after': modify_dict
                    }

        job_obj.result['job_details'] = job_details
        JobExitHandler().handle(job_obj)

    @staticmethod
    def _get_modify_dict(job_params, job_details):
        """Determine what modifications are needed."""
        modify_dict = {}

        # Check if state change is needed
        if job_params.get('job_state'):
            current_state = job_details.get('state', '')
            state_map = {
                "run": "running",
                "pause": "paused",
                "cancel": "cancel"
            }
            desired_prefix = state_map.get(
                job_params['job_state'], job_params['job_state'])
            if not current_state.startswith(desired_prefix):
                modify_dict['state'] = job_params['job_state']

        # Check if policy change is needed
        if job_params.get('policy') and \
                job_params['policy'] != job_details.get('policy'):
            modify_dict['policy'] = job_params['policy']

        # Check if priority change is needed
        if job_params.get('priority') is not None and \
                job_params['priority'] != job_details.get('priority'):
            modify_dict['priority'] = job_params['priority']

        return modify_dict


class JobCreateHandler:
    """JobCreateHandler definition."""
    def handle(self, job_obj, job_params):
        """Handle."""
        if job_params.get('state') == 'present' and \
                job_params.get('job_type'):
            job_obj.result['changed'] = True
            if not job_obj.module.check_mode:
                job_details = job_obj.create_job(job_params)
                job_obj.result['job_details'] = job_details

        JobExitHandler().handle(job_obj)


class JobHandler:
    """JobHandler definition."""
    def handle(self, job_obj, job_params):
        """Handle."""
        # Validate limit
        if job_params.get('limit') is not None and \
                job_params['limit'] < 0:
            job_obj.module.fail_json(
                msg="limit must be a positive integer")

        # Route: gather subset
        if job_params.get('gather_subset'):
            JobGatherHandler().handle(job_obj, job_params)
            return

        # Validate: job_state requires job_id
        if job_params.get('job_state') and not job_params.get('job_id'):
            job_obj.module.fail_json(
                msg="job_id is required to modify a job")

        # Route: job_id present - get/modify
        if job_params.get('job_id'):
            job_details = job_obj.get_job_details(job_params['job_id'])
            JobModifyHandler().handle(job_obj, job_params, job_details)
            return

        # Route: job_type present - create
        if job_params.get('job_type'):
            JobCreateHandler().handle(job_obj, job_params)
            return

        # No valid action specified
        job_obj.module.fail_json(
            msg="job_type is required to create a job")


def main():
    """Perform action on PowerScale Jobs based on user input
    from playbook."""
    obj = Job()
    JobHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
