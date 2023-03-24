#!/usr/bin/python
# Copyright: (c) 2021, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Ansible module for managing SyncIQ jobs on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: synciqjob

version_added: '1.3.0'

short_description: Manage SyncIQ jobs on PowerScale
description:
- Managing SyncIQ jobs on PowerScale storage system includes retrieving
  and modifying details of a SyncIQ job.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Jennifer John (@johnj9) <ansible.team@dell.com>

options:
  job_id:
    description:
    - Specifies the id or name of the policy job.
    type: str
    required: True

  job_state:
    description:
    - Specifies the state of the job.
    choices: ['run', 'pause', 'cancel']
    type: str

  state:
    description:
    - The state of the SyncIQ job after the task is performed.
    - present - indicates that the SyncIQ job should exist on the system.
    - absent - indicates that the SyncIQ job should not exist on the system.
    choices: ['absent', 'present']
    type: str
    required: True

notes:
- There is delay in the actual state change of the SyncIQ job. The state
  change of jobs in 'scheduled' state is not supported.

'''

EXAMPLES = r'''
- name: Get SyncIQ job details
  dellemc.powerscale.synciqjob:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      job_id: "Test_SSL"
      state: "present"

- name: Pause a SyncIQ job when in running state
  dellemc.powerscale.synciqjob:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      job_id: "Test_SSL"
      job_state: "pause"
      state: "present"

- name: Resume a SyncIQ job when in paused state
  dellemc.powerscale.synciqjob:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      job_id: "Test_SSL"
      job_state: "run"
      state: "present"

- name: Cancel a SyncIQ job
  dellemc.powerscale.synciqjob:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      job_id: "Test_SSL"
      job_state: "cancel"
      state: "absent"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool

job_details:
    description: The SyncIQ job details.
    returned: When SyncIQ job exists
    type: complex
    contains:
       action:
            description: The action to be taken by this job.
            type: str
       id:
            description: A unique identifier for this object.
            type: str
       policy_id:
            description: The id of the policy from which the job is
                         triggered.
            type: str
       policy_name:
            description: The name of the policy from which this job is
                         triggered.
            type: str
       sync_type:
            description: The type of sync being performed by this job.
            type: str
       state:
            description: The state of the job.
            type: str

modified_job:
    description: The modified SyncIQ job details.
    returned: When SyncIQ job is modified
    type: complex
    contains:
       id:
            description: A unique identifier for this object.
            type: str
       state:
            description: The state of the job.
            type: str

'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('synciqjob')


class SyncIQJob(object):
    """Class with SyncIQ job operations"""

    def __init__(self):
        """ Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_synciqjob_parameters())

        # initialize the Ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False
        )

        # result is a dictionary that contains changed status
        self.result = {"changed": False}
        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.sync_api_instance = utils.isi_sdk.SyncApi(self.api_client)
        LOG.info('Got the isi_sdk instance for authorization on to PowerScale')

    def get_job_details(self, job_id):
        """
        Get the details of the SyncIQ job.
        :param job_id: Specifies the id or name of the policy job
        :return: if exists returns details of the SyncIQ job
        else returns None.
        """
        try:
            api_response = \
                self.sync_api_instance.list_sync_jobs().jobs
            jobs = [job.to_dict() for job in api_response if job.id == job_id]
            return jobs
        except utils.ApiException as e:
            if str(e.status) == '404':
                error_message = "SyncIQ job %s details are not " \
                                "found" % (job_id)
                LOG.info(error_message)
                return None

            error_message = 'Get details of SyncIQ job %s failed with ' \
                            'error: %s' % (job_id, utils.determine_error
                                           (error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
        except Exception as e:
            error_message = 'Get details of SyncIQ job %s failed with ' \
                            'error: %s' % (job_id, utils.determine_error
                                           (error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def modify_job_state(self, job_id, job_state):
        """
        Modify the state of the SyncIQ job.
        :param job_id: Specifies the id or name of the policy job
        :param job_state: Specifies the state of the job.
        :return: True if job invocation is successful.
        """
        try:
            sync_job = utils.isi_sdk.SyncJob(state=job_state)
            self.sync_api_instance.update_sync_job(sync_job,
                                                   job_id)
            return True
        except utils.ApiException as e:
            error_message = 'Modify state of SyncIQ job %s failed with ' \
                            'error: %s' % (job_id, utils.determine_error
                                           (error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
        except Exception as e:
            error_message = 'Modify state of SyncIQ job %s failed with ' \
                            'error: %s' % (job_id, utils.determine_error
                                           (error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def validate_module(self, job_id, job_state, state):
        """ Validates the SyncIQ jobs module """
        if not job_id.strip():
            self.module.fail_json(msg="Please enter a valid job_id.")

        if job_state == 'cancel':
            if state != 'absent':
                self.module.fail_json(
                    msg="Please specify the state as absent for cancel.")
        elif state != 'present':
            self.module.fail_json(
                msg="Please specify a valid state.")

    def get_running_job(self, jobs):
        current_job = [job for job in jobs if job['job_id'] is not None]
        if current_job:
            return current_job[0]
        return None

    def perform_module_operation(self):
        """
        Perform different actions on SyncIQ job module based on parameters
        chosen in playbook
        """
        job_id = self.module.params['job_id']
        job_state = self.module.params['job_state']
        state = self.module.params['state']
        job_state_keys = {'pause': 'paused',
                          'cancel': 'canceled',
                          'run': 'running'}

        result = dict(
            changed=False,
            job_details=None,
            modified_job=None
        )

        self.validate_module(job_id, job_state, state)
        job_details = self.get_job_details(job_id)

        if not job_details and state != 'absent':
            err_msg = "Job with id %s does not exist. Creation of new job " \
                      "is not supported by this ansible module." % (job_id)
            self.module.fail_json(msg=err_msg)

        current_job = self.get_running_job(job_details)
        if current_job and job_state:
            current_job_state = current_job['state']
            modify_job_state = job_state_keys[job_state]
            if current_job_state != modify_job_state:
                result["changed"] = \
                    self.modify_job_state(job_id, modify_job_state)
                job_details = self.get_job_details(job_id)

        result["job_details"] = job_details
        if result["changed"]:
            result["modified_job"] = self.get_running_job(job_details)
        self.module.exit_json(**result)


def main():
    """ Create PowerScale SyncIQ job object and perform action on it
        based on user input from playbook"""
    obj = SyncIQJob()
    obj.perform_module_operation()


def get_synciqjob_parameters():
    """
    This method provides parameters required for the ansible SyncIQ job
    module on PowerScale
    """
    return dict(
        job_id=dict(type='str', required=True),
        job_state=dict(type='str', choices=['run', 'pause', 'cancel']),
        state=dict(required=True, type='str', choices=['present', 'absent'])
    )


if __name__ == '__main__':
    main()
