#!/usr/bin/python
# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for retrieving job report information on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: job_report_info

version_added: '4.0.0'

short_description: Retrieve job report information from PowerScale
description:
- Retrieving job report information from a PowerScale storage system includes
  listing job reports with various filters such as job type, job ID, event key,
  time range, and verbosity options.
- Supports automatic pagination to retrieve all available reports.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Shrinidhi Rao (@shrinidhirao) <ansible.team@dell.com>

options:
  job_type:
    description:
    - Filter reports by job type.
    type: str

  job_id:
    description:
    - Filter reports by job ID.
    type: int

  event_key:
    description:
    - Filter reports by event key.
    type: str

  begin:
    description:
    - Filter reports starting from this time (unix epoch seconds).
    type: int

  end:
    description:
    - Filter reports ending at this time (unix epoch seconds).
    type: int

  last_phase_only:
    description:
    - If true, only return reports for the last phase of each job.
    type: bool

  verbose:
    description:
    - If true, return verbose report details.
    type: bool

  limit:
    description:
    - The maximum number of reports to return per API request.
    type: int

notes:
- This is a read-only info module. It does not modify any resources.
- The I(check_mode) is supported.
- Pagination is handled automatically. All matching reports are returned.

requirements:
- JIRA ECS02C-842
'''

EXAMPLES = r'''
- name: Get all job reports
  dellemc.powerscale.job_report_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"

- name: Get reports filtered by job type
  dellemc.powerscale.job_report_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    job_type: "SmartPools"

- name: Get reports filtered by job ID
  dellemc.powerscale.job_report_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    job_id: 42

- name: Get reports with time range and verbose output
  dellemc.powerscale.job_report_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    begin: 1700000000
    end: 1700002000
    verbose: true

- name: Get reports for last phase only with limit
  dellemc.powerscale.job_report_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    last_phase_only: true
    limit: 10

- name: Get reports filtered by event key
  dellemc.powerscale.job_report_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    event_key: "phase_complete"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool

job_reports:
    description: List of job report dictionaries.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: The unique identifier of the report.
            type: str
        job_id:
            description: The ID of the job this report belongs to.
            type: int
        job_type:
            description: The type of the job.
            type: str
        event_key:
            description: The event key for this report.
            type: str
        phase:
            description: The phase of the job this report describes.
            type: str
        timestamp:
            description: The timestamp of the report in unix epoch seconds.
            type: int
        statistics:
            description: Statistics associated with the report.
            type: dict

total_reports:
    description: The total number of reports returned.
    returned: always
    type: int
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('job_report_info')


class JobReportInfo(object):
    """Class with Job Report Info operations"""

    def __init__(self):
        """Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_job_report_info_parameters())

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

    def get_reports(self, **params):
        """
        Get job reports with optional filters.
        :param params: Filter parameters for the API call
        :return: Dict with 'reports' and 'resume' keys
        """
        try:
            api_response = self.job_api.get_job_reports(**params)
            return api_response.to_dict()
        except utils.ApiException as e:
            error_message = 'Failed to get job reports with error: %s' \
                            % (utils.determine_error(error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def perform_module_operation(self):
        """
        Perform different actions on job report info module based on
        parameters chosen in playbook
        """
        job_type = self.module.params['job_type']
        job_id = self.module.params['job_id']
        event_key = self.module.params['event_key']
        begin = self.module.params['begin']
        end = self.module.params['end']
        last_phase_only = self.module.params['last_phase_only']
        verbose = self.module.params['verbose']
        limit = self.module.params['limit']

        # Build filter dict, excluding None values
        params = {}
        if job_type is not None:
            params['job_type'] = job_type
        if job_id is not None:
            params['job_id'] = job_id
        if event_key is not None:
            params['key'] = event_key
        if begin is not None:
            params['begin'] = begin
        if end is not None:
            params['end'] = end
        if last_phase_only is not None:
            params['last_phase_only'] = last_phase_only
        if verbose is not None:
            params['verbose'] = verbose
        if limit is not None:
            params['limit'] = limit

        # Fetch reports with pagination
        all_reports = []
        response = self.get_reports(**params)
        reports = response.get('reports', []) if response else []
        all_reports.extend(reports)

        # Handle pagination: keep fetching while resume token exists
        # (skip pagination if limit was set by user)
        if limit is None:
            resume = response.get('resume') if response else None
            while resume:
                paginated_params = dict(params)
                paginated_params['resume'] = resume
                response = self.get_reports(**paginated_params)
                reports = response.get('reports', []) if response else []
                all_reports.extend(reports)
                resume = response.get('resume') if response else None

        result = dict(
            changed=False,
            job_reports=all_reports,
            total_reports=len(all_reports)
        )

        self.module.exit_json(**result)


def get_job_report_info_parameters():
    """
    This method provides parameters required for the ansible job report
    info module on PowerScale
    """
    return dict(
        job_type=dict(type='str'),
        job_id=dict(type='int'),
        event_key=dict(type='str', no_log=False),
        begin=dict(type='int'),
        end=dict(type='int'),
        last_phase_only=dict(type='bool'),
        verbose=dict(type='bool'),
        limit=dict(type='int')
    )


def main():
    """Create PowerScale Job Report Info object and perform action on it
       based on user input from playbook"""
    obj = JobReportInfo()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
