#!/usr/bin/python
# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for retrieving Job Type information on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: job_type_info

version_added: '4.0.0'

short_description: Get Job Type information on PowerScale
description:
- Retrieving information about job types on PowerScale storage system.
- This module supports getting details of all job types or a specific
  job type by its ID.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Shrinidhi Rao (@shrinidhirao) <ansible.team@dell.com>

options:
  job_type_id:
    description:
    - The ID of a specific job type to retrieve.
    - If specified, only that single job type is returned.
    type: str

  include_hidden:
    description:
    - Whether to include hidden job types in the listing.
    - Defaults to C(false), which returns only visible job types.
    type: bool
    default: false

  sort:
    description:
    - The field by which to sort the job type results.
    type: str

  dir:
    description:
    - The sort direction.
    choices: ['ASC', 'DESC']
    type: str

notes:
- This is a read-only info module and does not make any changes.
- The I(check_mode) is supported.

requirements:
- JIRA ECS02C-843
'''

EXAMPLES = r'''
- name: Get all visible job types
  dellemc.powerscale.job_type_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"

- name: Get all job types including hidden
  dellemc.powerscale.job_type_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    include_hidden: true

- name: Get a specific job type by ID
  dellemc.powerscale.job_type_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    job_type_id: "TreeDelete"

- name: Get job types sorted by priority in descending order
  dellemc.powerscale.job_type_info:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    sort: "priority"
    dir: "DESC"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool

job_types:
    description: The list of job type details.
    returned: always
    type: list
    contains:
        id:
            description: The unique identifier for the job type.
            type: str
        name:
            description: The display name of the job type.
            type: str
        description:
            description: A description of what the job type does.
            type: str
        is_hidden:
            description: Whether the job type is hidden.
            type: bool
        enabled:
            description: Whether the job type is enabled.
            type: bool
        priority:
            description: The priority level of the job type.
            type: int
        policy:
            description: The impact policy of the job type.
            type: str
        schedule:
            description: The schedule for the job type, if any.
            type: str
        allow_multiple_instances:
            description: Whether multiple instances of this job type
                         can run concurrently.
            type: bool
        exclusion_set:
            description: The exclusion set for the job type.
            type: str
    sample: [
        {
            "id": "TreeDelete",
            "name": "Tree Delete",
            "description": "Delete directory trees",
            "is_hidden": false,
            "enabled": true,
            "priority": 5,
            "policy": "LOW",
            "schedule": null,
            "allow_multiple_instances": false,
            "exclusion_set": "filesystem_ops"
        }
    ]
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('job_type_info')


class JobTypeInfo(object):
    """Class with Job Type Info operations"""

    def __init__(self):
        """Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_job_type_info_parameters())

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

    def get_job_types(self, include_hidden, sort, dir):
        """
        Get a list of job types.
        :param include_hidden: Whether to include hidden job types
        :param sort: Field to sort by
        :param dir: Sort direction
        :return: List of job type dicts
        """
        try:
            api_response = self.job_api.get_job_types(
                show_all=include_hidden, sort=sort, dir=dir)
            response_dict = api_response.to_dict()
            return response_dict.get('types', [])
        except utils.ApiException as e:
            error_message = 'Failed to get job types with ' \
                            'error: %s' % (utils.determine_error
                                           (error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_job_type(self, type_id):
        """
        Get a specific job type by ID.
        :param type_id: The job type ID
        :return: Job type dict or None if not found
        """
        try:
            api_response = self.job_api.get_job_type(type_id)
            response_dict = api_response.to_dict()
            return response_dict
        except utils.ApiException as e:
            if str(e.status) == '404':
                error_message = "Job type %s is not " \
                                "found" % (type_id)
                LOG.info(error_message)
                return None

            error_message = 'Failed to get job type details for %s ' \
                            'with error: %s' % (type_id,
                                                utils.determine_error
                                                (error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def perform_module_operation(self):
        """
        Perform different actions on Job Type Info module based on
        parameters chosen in playbook
        """
        job_type_id = self.module.params['job_type_id']
        include_hidden = self.module.params['include_hidden']
        sort = self.module.params['sort']
        dir = self.module.params['dir']

        result = dict(
            changed=False,
            job_types=[]
        )

        if job_type_id:
            job_type_details = self.get_job_type(job_type_id)
            if job_type_details:
                result['job_types'] = job_type_details
            else:
                result['job_types'] = {}
        else:
            result['job_types'] = self.get_job_types(
                include_hidden, sort, dir)

        self.module.exit_json(**result)


def main():
    """Create PowerScale Job Type Info object and perform action on it
       based on user input from playbook"""
    obj = JobTypeInfo()
    obj.perform_module_operation()


def get_job_type_info_parameters():
    """
    This method provides parameters required for the ansible Job Type
    Info module on PowerScale
    """
    return dict(
        job_type_id=dict(type='str'),
        include_hidden=dict(type='bool', default=False),
        sort=dict(type='str'),
        dir=dict(type='str', choices=['ASC', 'DESC'])
    )


if __name__ == '__main__':
    main()
