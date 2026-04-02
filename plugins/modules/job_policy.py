#!/usr/bin/python
# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing Job impact policies on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: job_policy
version_added: '3.0.0'
short_description: Manage Job impact policies on a PowerScale Storage System
description:
- Managing Job impact policies on a PowerScale system includes creating,
  modifying, deleting and retrieving details of job impact policies.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Dell Technologies Ansible Team <ansible.team@dell.com>

options:
  policy_name:
    description:
    - The name of the job impact policy.
    - Required for create, modify, and delete operations.
    type: str
  policy_id:
    description:
    - The ID of the job impact policy.
    - Used to retrieve a specific policy by ID.
    type: str
  intervals:
    description:
    - List of time intervals and their impact levels.
    type: list
    elements: dict
  description:
    description:
    - Description of the job impact policy.
    type: str
  state:
    description:
    - Defines whether the job impact policy should exist or not.
    - Value C(present) indicates that the policy should exist on the system.
    - Value C(absent) indicates that the policy should not exist on the system.
    type: str
    choices: ['present', 'absent']
    default: present
notes:
- The I(check_mode) is supported.
'''

EXAMPLES = r'''
- name: Create a job impact policy
  dellemc.powerscale.job_policy:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"  # example
    verify_ssl: "{{verify_ssl}}"
    policy_name: "LOW_IMPACT"
    intervals:
      - begin: "Monday 18:00"
        end: "Monday 06:00"
        impact: "Low"
    state: "present"

- name: Get a job impact policy by name
  dellemc.powerscale.job_policy:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"  # example
    verify_ssl: "{{verify_ssl}}"
    policy_name: "LOW_IMPACT"
    state: "present"

- name: Modify a job impact policy
  dellemc.powerscale.job_policy:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"  # example
    verify_ssl: "{{verify_ssl}}"
    policy_name: "LOW_IMPACT"
    description: "Updated description"
    intervals:
      - begin: "Monday 20:00"
        end: "Tuesday 08:00"
        impact: "Low"
    state: "present"

- name: Delete a job impact policy
  dellemc.powerscale.job_policy:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"  # example
    verify_ssl: "{{verify_ssl}}"
    policy_name: "LOW_IMPACT"
    state: "absent"

- name: List all job impact policies
  dellemc.powerscale.job_policy:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"  # example
    verify_ssl: "{{verify_ssl}}"
    state: "present"
'''

RETURN = r'''
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
job_policy_details:
    description: The job impact policy details.
    type: dict
    returned: When a specific policy is targeted.
    contains:
        id:
            description: The ID of the job impact policy.
            type: str
        name:
            description: The name of the job impact policy.
            type: str
        description:
            description: Description of the job impact policy.
            type: str
        intervals:
            description: List of time intervals and their impact levels.
            type: list
    sample: {
        "id": "LOW_IMPACT",
        "name": "LOW_IMPACT",
        "description": "",
        "intervals": [
            {
                "begin": "Monday 18:00",
                "end": "Monday 06:00",
                "impact": "Low"
            }
        ]
    }
job_policies:
    description: List of all job impact policies.
    type: list
    returned: When no specific policy is targeted.
    sample: [
        {
            "id": "LOW",
            "name": "LOW",
            "description": "Impact-throttled to use fewer cluster resources",
            "intervals": []
        }
    ]
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('job_policy')


class JobPolicy:
    """Class with Job Policy operations"""

    def __init__(self):
        """Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(self.get_job_policy_parameters())
        # Initialize the ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=True
        )
        # Result is a dictionary that contains changed status and details
        self.result = {
            "changed": False,
            "job_policy_details": {},
            "job_policies": []
        }

        # Validate the pre-requisites packages for the module
        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        # Initialize the connection to PowerScale
        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        LOG.info('Got python SDK instance for provisioning on PowerScale')
        check_mode_msg = f'Check mode flag is {self.module.check_mode}'
        LOG.info(check_mode_msg)

        # Initialize the APIs
        self.job_api = self.isi_sdk.JobApi(self.api_client)

    def get_job_policy_details(self, policy_name=None, policy_id=None):
        """
        Get details of a job impact policy.
        :param policy_name: Name of the policy
        :param policy_id: ID of the policy
        :return: Policy details dict or None
        """
        if policy_id:
            try:
                msg = f"Getting job policy details for ID: {policy_id}"
                LOG.info(msg)
                result = self.job_api.get_job_policy(policy_id)
                if result:
                    data = result.to_dict()
                    if isinstance(data, dict):
                        if "policies" in data and data["policies"]:
                            return data["policies"][0]
                        return data
                return None
            except utils.ApiException as e:
                if str(e.status) == "404":
                    log_msg = f"Job policy {policy_id} not found (404)"
                    LOG.info(log_msg)
                    return None
                error_msg = f"Failed to get job policy details with " \
                            f"error: {utils.determine_error(e)}"
                LOG.error(error_msg)
                self.module.fail_json(msg=error_msg)
            except Exception as e:
                error_msg = f"Failed to get job policy details with " \
                            f"error: {utils.determine_error(e)}"
                LOG.error(error_msg)
                self.module.fail_json(msg=error_msg)
        elif policy_name:
            try:
                msg = f"Getting job policy details for name: {policy_name}"
                LOG.info(msg)
                result = self.job_api.list_job_policies()
                if result:
                    data = result.to_dict()
                    if isinstance(data, dict):
                        for policy in data.get("policies", []):
                            if isinstance(policy, dict) and \
                                    policy.get("name") == policy_name:
                                return policy
                return None
            except Exception as e:
                error_msg = f"Failed to list job policies with " \
                            f"error: {utils.determine_error(e)}"
                LOG.error(error_msg)
                self.module.fail_json(msg=error_msg)
        return None

    def list_job_policies(self):
        """
        List all job impact policies.
        :return: List of policy dicts or None
        """
        try:
            LOG.info("Listing all job policies")
            result = self.job_api.list_job_policies()
            if result:
                data = result.to_dict()
                if isinstance(data, dict) and "policies" in data:
                    msg = f"Job policies: {data.get('policies', [])}"
                    LOG.info(msg)
                    return data.get("policies", [])
            return None
        except Exception as e:
            error_msg = f"Failed to list job policies with " \
                        f"error: {utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def create_job_policy(self, policy_name, intervals=None,
                          description=None):
        """
        Create a new job impact policy.
        :param policy_name: Name of the policy
        :param intervals: List of interval dicts
        :param description: Policy description
        """
        try:
            job_policy = {"name": policy_name}
            if intervals is not None:
                job_policy["intervals"] = intervals
            if description is not None:
                job_policy["description"] = description
            msg = f"Creating job policy with parameters: {job_policy}"
            LOG.info(msg)
            self.job_api.create_job_policy(job_policy=job_policy)
            LOG.info("Successfully created the job policy.")
        except Exception as e:
            error_msg = f"Failed to create policy with " \
                        f"error: {utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def modify_job_policy(self, policy_id, modify_params):
        """
        Modify an existing job impact policy.
        :param policy_id: ID/name of the policy to modify
        :param modify_params: Dict of parameters to modify
        """
        try:
            msg = f"Modifying job policy {policy_id} with " \
                  f"parameters: {modify_params}"
            LOG.info(msg)
            self.job_api.update_job_policy(
                job_policy=modify_params,
                job_policy_id=policy_id)
            LOG.info("Successfully modified the job policy.")
        except Exception as e:
            error_msg = f"Failed to modify job policy with " \
                        f"error: {utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def delete_job_policy(self, policy_id):
        """
        Delete a job impact policy.
        :param policy_id: ID/name of the policy to delete
        """
        try:
            msg = f"Deleting job policy {policy_id}"
            LOG.info(msg)
            self.job_api.delete_job_policy(policy_id)
            LOG.info("Successfully deleted the job policy.")
        except Exception as e:
            error_msg = f"Failed to delete job policy with " \
                        f"error: {utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def is_modify_required(self, params, policy_details):
        """
        Check whether modification is required.
        :param params: Module parameters
        :param policy_details: Current policy details
        :return: Dict of parameters that need modification
        """
        modify_params = {}
        if params.get("intervals") is not None and \
                params["intervals"] != policy_details.get("intervals"):
            modify_params["intervals"] = params["intervals"]
        if params.get("description") is not None and \
                params["description"] != policy_details.get("description"):
            modify_params["description"] = params["description"]
        return modify_params

    def get_job_policy_parameters(self):
        """Get job policy parameters."""
        return dict(
            policy_name=dict(type='str'),
            policy_id=dict(type='str'),
            intervals=dict(type='list', elements='dict'),
            description=dict(type='str'),
            state=dict(type='str', choices=['present', 'absent'],
                       default='present')
        )


class JobPolicyExitHandler:
    """JobPolicyExitHandler definition."""
    def handle(self, obj, policy_details):
        """Handle."""
        obj.result["job_policy_details"] = policy_details
        obj.module.exit_json(**obj.result)


class JobPolicyDeleteHandler:
    """JobPolicyDeleteHandler definition."""
    def handle(self, obj, params, policy_details):
        """Handle."""
        if params["state"] == "absent" and policy_details:
            if not obj.module.check_mode:
                policy_id = policy_details.get("id") or \
                    params.get("policy_name")
                obj.delete_job_policy(policy_id)
            obj.result["changed"] = True

        JobPolicyExitHandler().handle(obj, policy_details)


class JobPolicyModifyHandler:
    """JobPolicyModifyHandler definition."""
    def handle(self, obj, params, policy_details):
        """Handle."""
        if params["state"] == "present" and policy_details:
            modify_params = obj.is_modify_required(params, policy_details)
            if modify_params:
                if obj.module._diff:
                    obj.result["diff"] = {
                        "before": policy_details,
                        "after": {**policy_details, **modify_params}
                    }
                if not obj.module.check_mode:
                    policy_id = policy_details.get("id") or \
                        params.get("policy_name")
                    obj.modify_job_policy(policy_id, modify_params)
                obj.result["changed"] = True
                if not obj.module.check_mode:
                    policy_details = obj.get_job_policy_details(
                        policy_name=params.get("policy_name"),
                        policy_id=params.get("policy_id"))

        JobPolicyDeleteHandler().handle(obj, params, policy_details)


class JobPolicyCreateHandler:
    """JobPolicyCreateHandler definition."""
    def handle(self, obj, params, policy_details):
        """Handle."""
        if params["state"] == "present" and policy_details is None:
            policy_name = params.get("policy_name")
            if not obj.module.check_mode:
                obj.create_job_policy(
                    policy_name,
                    intervals=params.get("intervals"),
                    description=params.get("description"))
            obj.result["changed"] = True

        JobPolicyModifyHandler().handle(obj, params, policy_details)


class JobPolicyHandler:
    """JobPolicyHandler definition."""
    def handle(self, obj, params):
        """Handle."""
        policy_name = params.get("policy_name")
        policy_id = params.get("policy_id")

        # List operation when neither name nor id is provided
        if policy_name is None and policy_id is None:
            policies = obj.list_job_policies()
            if policies is not None:
                obj.result["job_policies"] = policies
                JobPolicyExitHandler().handle(obj, None)
                return
            obj.module.fail_json(
                msg="policy_name is required to create or modify "
                    "a job policy")

        # Validate policy_name is not empty
        if policy_name is not None and len(policy_name.strip()) == 0:
            obj.module.fail_json(msg="Invalid policy_name provided")

        # Get existing policy details
        policy_details = obj.get_job_policy_details(
            policy_name=policy_name,
            policy_id=policy_id)

        # Chain to create/modify/delete/exit handlers
        JobPolicyCreateHandler().handle(obj, params, policy_details)


def main():
    """Create PowerScale Job Policy object and perform action on it
       based on user input from playbook."""
    obj = JobPolicy()
    JobPolicyHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
