#!/usr/bin/python
# Copyright: (c) 2021, DellEMC

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

""" Ansible module for managing SyncIQ Policy on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: synciqpolicy

version_added: "1.3.0"

short_description: Manage SyncIQ policies on PowerScale
description:
- Managing SyncIQ policies on PowerScale includes
  create a SyncIQ policy,
  modify a SyncIQ policy,
  get details of a SyncIQ policy,
  creating jobs on SyncIQ policy.

extends_documentation_fragment:
  - dellemc.powerscale.dellemc_powerscale.powerscale
author:
- Spandita Panigrahi (@panigs7) <ansible.team@dell.com>

options:
  policy_name:
    description:
    - The name of the policy.
    - Required at the time of policy creation, for the rest of the operations
      either policy_name or policy_id is required.
    type: str
  policy_id:
    description:
    - The policy_id is auto generated at the time of creation.
    - For get/modify operations either policy_name or policy_id is needed.
    - Parameters policy_name and policy_id are mutually exclusive.
    type: str
  new_policy_name:
    description:
    - The new name of the policy while renaming an existing policy.
    - policy_name or policy_id is required together with new_policy_name.
    type: str
  action:
    description:
    - Indicates type of replication action to be performed on the source.
    type: str
    choices: [ 'sync', 'copy' ]
  state:
    description:
    - The state option is used to determine whether the policy
      exists or not.
    type: str
    required: True
    choices: [ 'absent', 'present']
  description:
    description:
    - Description of the policy.
    type: str
  enabled:
    description:
    - Indicates whether policy is enabled or disabled.
    type: bool
  run_job:
    description:
    - Types of scheduling a job on the policy.
    type: str
    choices: ['on-schedule', 'when-source-modified', 'when-snapshot-taken']
  job_delay:
    description:
    - If run_job is set to when-source-modified, job_delay is the
      duration to wait before triggering a job once there is modification on source.
    type: int
  job_delay_unit:
    description:
    - Unit for job_delay.
    type: str
    choices: ['seconds', 'minutes', 'hours', 'days']
    default: 'seconds'
  rpo_alert:
    description:
    - If run_job is set to 'on-schedule' is set to a time/date,
      an alert is created if the specified RPO for this policy is exceeded.
    - The default value is 0, which will not generate RPO alerts.
    type: int
  rpo_alert_unit:
    description:
    - Unit for rpo_alert.
    type: str
    choices: ['minutes', 'hours', 'days', 'weeks', 'months', 'years']
    default: 'minutes'
  snapshot_sync_pattern:
    description:
    - The naming pattern that a snapshot must match to trigger
      a sync when the schedule is when-snapshot-taken.
    type: str
  skip_when_source_unmodified:
    description:
    - If true and schedule is set , the policy will not run if
      no changes have been made to the contents of the source
      directory since the last job successfully completed.
    - Option modifiable when run_job is "on_schedule".
    type: bool
  schedule:
    description:
    - Schedule set when run_policy is 'on-schedule'.
    - It must be in isidate format.
    - If the format is not proper an error will be thrown.
    type: str
  source_cluster:
    description:
    - Defines the details of source_cluster.
    type: dict
    suboptions:
        source_root_path:
            description:
            - The root directory on the source cluster where
              the files will be synced from.
            - Source root path should begin with /ifs. For example, if we want to create a synciq
              policy for the directory 'source' in the base path /ifs, then the source_root_path
              will be '/ifs/source'.
            type: str
        source_exclude_directories:
            description:
            - List of path to the directories that
              should be excluded while running a policy.
            - For example, if we want to exclude directory 'exclude1' at location '/ifs/source',
              then the source_exclude_directories will be '/ifs/source/exclude1'.
            type: list
            elements: str
        source_include_directories:
            description:
            -  List of path to the directories
               that should be included while running a policy
            - For example, if we want to include directory 'include1' at location '/ifs/source',
              then the source_exclude_directories will be '/ifs/source/include1'.
            type: list
            elements: str
        source_network:
            description:
            - Run the policy only on nodes in the specified subnet and pool.
            type: dict
            suboptions:
                pool:
                    description:
                    - The pool to restrict replication policies to.
                    type: str
                subnet:
                    description:
                    - The subnet to restrict replication policies to.
                    type: str
  target_cluster:
    description:
    - Details of the target cluster.
    type: dict
    suboptions:
        target_host:
            description:
            - Host IP or FQDN where we want to replicate the source.
            type: str
        target_path:
            description:
            - The directory location to have the replicated source data at.
            type: str
        target_certificate_id:
            description:
            - The ID of the target cluster certificate being used for encryption
            - This parameter is not supported by isi_sdk_8_1_1
            type: str
        target_certificate_name:
            description:
            - The name of the target cluster certificate being used for encryption
            - Parameters target_certficate_name and target_certificate_id are mutually exclusive
            - This parameter is not supported by isi_sdk_8_1_1
            type: str
  target_snapshot:
    description:
    - Details of snapshots to be created at the target.
    type: dict
    suboptions:
        target_snapshot_archive:
            description:
            - Indicates whether to take snapshot of the target.
            type: bool
        target_snapshot_expiration:
            description:
            - Expiration time of snapshot.
            - Value 0 means no expiration.
            type: int
        exp_time_unit:
            description:
            - Unit of target_snapshot expiration time.
            type: str
            choices: ['years', 'months', 'weeks', 'days']
            default: 'years'
  job_params:
    description:
    - Specifies the parameters to create a job on SyncIQ policy.
    type: dict
    suboptions:
        action:
            description:
            - The action to be taken by this job.
            choices: ['run', 'resync_prep', 'allow_write',
                      'allow_write_revert']
            type: str
            required: True
        wait_for_completion:
            description:
            - Specifies if the job should run synchronously or asynchronously.
              By default the job is created to run asynchronously.
            type: bool
            default: False
        source_snapshot:
            description:
            - An optional snapshot to copy/sync from.
            type: str
        workers_per_node:
            description:
            - Specifies the desired workers per node. This parameter is valid
              for allow_write, and allow_write_revert operation. This is an
              optional parameter and it defaults to 3.
            type: int

notes:
- There is a delay to view the jobs running on the policy.

'''
EXAMPLES = r'''
  - name: Create SyncIQ policy
    dellemc.powerscale.synciqpolicy:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      action: "copy"
      description: "Creating a policy"
      enabled: True
      policy_name: "New_policy"
      run_job: "on-schedule"
      schedule: "every 1 days at 12:00 PM"
      skip_when_source_unmodified: True
      rpo_alert: 100
      source_cluster:
        source_root_path: "<path_to_source>"
        source_exclude_directories: "<path_to_exclude>"
        source_include_directories: "<path_to_include>"
        source_network:
            pool: "pool0"
            subnet: "subnet0"
      target_cluster:
        target_host: "198.10.xxx.xxx"
        target_path: "<path_to_target>"
        target_certificate_id: "7sdgvejkiau7629903048hdjdkljsbwgsuasj7169823kkckll"
      target_snapshot:
        target_snapshot_archive: True
        target_snapshot_expiration: 90
        exp_time_unit: "day"
      state: "present"

  - name: Modify SyncIQ policy
    dellemc.powerscale.synciqpolicy:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      policy_name: "New_policy"
      action: "sync"
      description: "Creating a policy"
      enabled: False
      run_job: "when-snapshot-taken"
      snapshot_sync_patten: "^snapshot\\-$latest"
      source_cluster:
        source_root_path: "<path_to_source>"
        source_exclude_directories: "<path_to_exclude>"
        source_include_directories: "<path_to_include>"
        source_network:
            pool: "pool1"
            subnet: "subnet1"
      target_cluster:
        target_host: "198.10.xxx.xxx"
        target_path: "<path_to_target>"
        target_certificate_id: "7sdgvejkiau7629903048hdjdkljsbwgsuasj716iuhywthsjk"
      target_snapshot:
        target_snapshot_archive: False
      state: "present"

  - name: Rename a SyncIQ policy
    dellemc.powerscale.synciqpolicy:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      policy_id: "d63b079d34adf2d2ec3ce92f15bfc730"
      new_policy_name: "Policy_Rename"
      state: "present"

  - name: Get SyncIQ policy details
    dellemc.powerscale.synciqpolicy:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      policy_name: "Policy_rename"
      state: "present"

  - name: Create a job on SyncIQ policy
    dellemc.powerscale.synciqpolicy:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      policy_name: "Test_SSL"
      job_params:
        action: "run"
        source_snapshot: "TestSIQ-snapshot"
        wait_for_completion: False
      state: "present"

  - name: Create a resync_prep job on SyncIQ policy
    dellemc.powerscale.synciqpolicy:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      policy_name: "Test_SSL"
      job_params:
        action: "resync_prep"
        source_snapshot: "TestSIQ-snapshot"
        wait_for_completion: False
      state: "present"

  - name: Allow writes on target of SyncIQ policy
    dellemc.powerscale.synciqpolicy:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      policy_name: "Test_SSL"
      job_params:
        action: "allow_write"
        source_snapshot: "TestSIQ-snapshot"
        workers_per_node: 3
        wait_for_completion: False
      state: "present"

  - name: Disallow writes on target of SyncIQ policy
    dellemc.powerscale.synciqpolicy:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      policy_name: "Test_SSL"
      job_params:
        action: "allow_write_revert"
        source_snapshot: "TestSIQ-snapshot"
        workers_per_node: 3
        wait_for_completion: False
      state: "present"

  - name: Delete SyncIQ policy by policy name
    dellemc.powerscale.synciqpolicy:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      policy_name: "Policy_rename"
      state: "absent"

  - name: Delete SyncIQ policy by policy ID
    dellemc.powerscale.synciqpolicy:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      policy_id: "d63b079d34adf2d2ec3ce92f15bfc730"
      state: "absent"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
synciq_policy_details:
    description: Details of the SyncIQ policy.
    returned: When SyncIQ policy exists
    type: complex
    contains:
        name:
            description: The name of the policy.
            type: str
        id:
            description: ID of the policy.
            type: str
        enabled:
            description: Indicates whether policy is enabled
            type: bool
        action:
            description: Type of action for the policy
            type: str
        schedule:
            description: Type of schedule chosen to run a policy
            type: str
        source_root_path:
            description: The path to the source directory to be replicated
            type: str
        target_host:
            description: The IP/FQDN of the host where source is replicated
            type: str
        target_path:
            description: The target directory where source is replicated
            type: str
        jobs:
            description: List of jobs running on the policy
            type: list
target_synciq_policy_details:
    description: Details of the target SyncIQ policy.
    returned: When failover/failback is performed on target cluster
    type: complex
    contains:
        name:
            description: The name of the policy.
            type: str
        id:
            description: ID of the policy.
            type: str
        failover_failback_state:
            description: The state of the policy with respect to sync
                         failover/failback.
            type: str
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import dellemc_ansible_powerscale_utils as utils

LOG = utils.get_logger('synciqpolicy')


class SynciqPolicy(object):
    """Class with SyncIQ Policy operations"""

    def __init__(self):
        """ Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_synciqpolicy_parameters())
        mutually_exclusive = [['policy_name', 'policy_id']]

        # initialize the Ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False,
            mutually_exclusive=mutually_exclusive
        )
        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)

        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        self.api_instance = utils.isi_sdk.SyncApi(self.api_client)
        LOG.info('Got python SDK instance for provisioning on PowerScale')

    def get_synciq_policy_details(self, policy_name, policy_id, job_params=None):
        """
        Get the details of the SyncIQ policy.
        :param policy_name: Specifies the SyncIQ policy name.
        :param policy_id: Specifies the SyncIQ policy ID.
        :param job_params: Dictionary of parameters for creating a job
        :return: if exists returns details of the SyncIQ policy or target
        SyncIQ policy object else returns None.
        """
        name_or_id = policy_name if policy_name else policy_id
        try:
            policy = self.api_instance.get_sync_policy(name_or_id).policies
            if policy:
                return policy[0], False

            return None, False
        except utils.ApiException as e:
            if str(e.status) == "404":
                LOG.info("SyncIQ policy %s is not found", name_or_id)
                return self.get_target_policy(name_or_id, job_params)
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Get details of SyncIQ policy %s failed with ' \
                            'error : %s' % (name_or_id, str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_target_policy(self, policy_id, job_params):
        """ Returns details of target syncIQ policy"""
        if job_params and job_params['action'] in \
                ('allow_write', 'allow_write_revert'):
            try:
                target_policy = \
                    self.api_instance.get_target_policy(policy_id).policies
                if target_policy:
                    if len(target_policy) > 1:
                        self.module.fail_json(msg="Multiple target policy "
                                              "instances are returned for the "
                                              "given policy_name. Please "
                                              "specify policy_id to run "
                                              "failover/failover revert job.")
                    else:
                        return target_policy[0], True
            except Exception as e:
                error_msg = utils.determine_error(error_obj=e)
                error_message = 'Get details of target SyncIQ policy %s failed with ' \
                                'error : %s' % (policy_id, str(error_msg))
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
        return None, False

    def get_synciq_policy_display_attributes(self, policy_obj):
        """
        Display the SyncIQ policy attributes
        :policy_obj: Policy object
        :return: dict with SyncIQ policy details
        """
        try:
            policy_details = policy_obj.to_dict()

            if 'target_certificate_id' in policy_details and policy_details['target_certificate_id']:
                policy_details['target_certificate_name'] = \
                    self.get_target_cert_id_name(cert_id=policy_details['target_certificate_id'])

            if policy_details['job_delay'] is not None:
                policy_details['job_delay'] = utils.get_time_with_unit(policy_details['job_delay'])

            if policy_details['target_snapshot_expiration'] is not None:
                policy_details['target_snapshot_expiration'] = \
                    utils.get_time_with_unit(policy_details['target_snapshot_expiration'])

            if policy_details['rpo_alert'] is not None:
                policy_details['rpo_alert'] = \
                    utils.get_time_with_unit(policy_details['rpo_alert'])

            return policy_details

        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            errormsg = "Display details of SyncIQ policy %s failed with " \
                       "error %s" % (policy_obj.name, str(error_msg))
            LOG.error(errormsg)
            self.module.fail_json(msg=errormsg)

    def create_synciq_policy(self, policy_param):
        """
        Create SyncIQ Policy
        :param: Dictionary of parameters to be set while creating a policy
        :return: Policy ID once creation is successful
        """
        try:
            LOG.debug("Parameters to set when creating a SyncIQ policy %s", policy_param)
            policy_id = self.api_instance.create_sync_policy(sync_policy=policy_param)
            return policy_id
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Creating SyncIQ policy %s failed with ' \
                            'error : %s' % (policy_param['name'], str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def modify_synciq_policy(self, policy_params_dict, policy_id):
        """
        Modify SyncIQ policy.
        :policy_params_dict: Dictionary of parameters to be modified of a policy
        :policy_id: ID of the policy to be modified
        :return: True if modify is successful
        """

        try:
            if policy_params_dict is not None:
                LOG.debug("Policy parameters being modified : %s", policy_params_dict)
                self.api_instance.update_sync_policy(sync_policy=policy_params_dict, sync_policy_id=policy_id)
            return True
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Failed to modify SyncIQ policy with ' \
                            'error : %s' % str(error_msg)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_policy_jobs(self, policy_id):
        """
        Get the list of jobs on the SyncIQ policy.
        :param policy_id: Specifies the id or name of the SyncIQ policy
        :return: returns details of the jobs on the policy
        else returns None.
        """
        try:
            jobs_list = []
            api_response = self.api_instance.list_sync_jobs().jobs
            jobs = [job for job in api_response if job.id == policy_id]
            for job in jobs:
                jobs_list.append({"id": job.id,
                                  "state": job.state,
                                  "action": job.action})
            return jobs_list
        except Exception as e:
            error_message = 'Get jobs on SyncIQ policy %s failed with ' \
                            'error: %s' % (policy_id,
                                           utils.determine_error
                                           (error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def create_synciq_job(self, policy_id, job_params):
        """
        Create a job on SyncIQ policy.
        :policy_id: name or id of the policy on which job should be created
        :job_params: Dictionary of parameters for creating a job
        :return: True if job creation is successful
        """

        try:
            if job_params:
                sync_job_params = {}
                sync_job_keys = ['action', 'source_snapshot', 'workers_per_node']
                sync_job_params['id'] = policy_id
                for key in sync_job_keys:
                    if key == 'action' and job_params[key] == 'run':
                        continue
                    sync_job_params[key] = job_params[key]
                sync_job = utils.isi_sdk.SyncJobCreateParams(
                    **sync_job_params)
                if job_params['wait_for_completion']:
                    self.api_instance.create_sync_job(sync_job)
                else:
                    self.api_instance.create_sync_job(sync_job, async_req=True)

            return True
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Failed to create job on SyncIQ policy with ' \
                            'error : %s' % str(error_msg)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete_synciq_policy(self, policy_id):
        """
        Delete SyncIQ policy.
        :param policy_id: ID of SyncIQ policy
        :return: True if deletion is successful
        """

        try:
            self.api_instance.delete_sync_policy(sync_policy_id=policy_id)
            return True
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Deleting SyncIQ policy %s failed with ' \
                            'error : %s' % (policy_id, str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_target_cert_id_name(self, cert_name=None, cert_id=None):
        """
        Get target certificate id from certificate name
        :param cert_name: Alias name of target certificate
        :param cert_id: ID of the target certificate
        :return: ID of certificate if name is provided else name of certificate
                 if ID is provided
        """
        try:
            cert_list = self.api_instance.list_certificates_peer().certificates
            for cert in cert_list:
                if cert_name and cert.name == cert_name:
                    return cert.id
                elif cert_id and cert.id == cert_id:
                    return cert.name
            self.module.fail_json(msg="Please provide a valid certificate.")
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Get certificate %s failed with ' \
                            'error : %s' % (cert_name, str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def construct_policy_params(self, input_param, schedule, rpo_alert, job_delay):
        """
        Construct dictionary of parameters to be set for create operation
        :param input_param: Dictionary of parameters provided from playbook
        :param schedule: Schedule set to run the policy
        :param rpo_alert: An alert is created if the specified RPO for this
         policy is exceeded when schedule is "on-schedule"
        :param job_delay: Delay a job when schedule is "when-source-modified"
        :return: dictionary of parameters to be set while create operation
        """
        policy_param = {}

        policy_param_keys = ['description', 'enabled', 'action', 'skip_when_source_unmodified',
                             'source_root_path', 'source_network',
                             'source_include_directories', 'source_exclude_directories',
                             'target_host', 'target_path', 'target_certificate_id', 'target_snapshot_archive',
                             'target_snapshot_expiration', 'snapshot_sync_pattern'
                             ]

        for param in input_param:
            if param in policy_param_keys and input_param[param] is not None:
                policy_param[param] = input_param[param]

        if input_param['policy_name']:
            policy_param['name'] = input_param['policy_name']

        if input_param['policy_id']:
            policy_param['id'] = input_param['policy_id']

        if input_param['run_job']:
            policy_param['schedule'] = schedule

        if input_param['rpo_alert']:
            policy_param['rpo_alert'] = rpo_alert

        if input_param['job_delay']:
            policy_param['job_delay'] = job_delay

        if input_param['source_cluster']:
            policy_param.update(construct_dict(input_param, 'source_cluster', policy_param_keys))

        if input_param['target_cluster']:
            policy_param.update(construct_dict(input_param, 'target_cluster', policy_param_keys))

            if input_param['target_cluster']['target_certificate_name']:
                policy_param['target_certificate_id'] = \
                    self.get_target_cert_id_name(cert_name=input_param['target_cluster']['target_certificate_name'])

        if input_param['target_snapshot']:
            policy_param.update(construct_dict(input_param, 'target_snapshot', policy_param_keys))

        return policy_param

    def validate_create_params(self, policy_param):
        """
        Validate if mandatory parameters are present while creating a SyncIQ policy.
        :param policy_param: Dictionary of parameters provided from playbook
        """
        if 'name' not in policy_param.keys() or policy_param['name'] is None:
            self.module.fail_json(msg="Please provide a name for the SyncIQ policy.")
        if 'source_root_path' not in policy_param.keys() or policy_param['source_root_path'] is None:
            self.module.fail_json(msg="Please provide a path to the source directory.")
        if 'target_path' not in policy_param.keys() or policy_param['target_path'] is None:
            self.module.fail_json(msg="Please provide a path to the target directory.")
        if utils.ISI_SDK_VERSION_9 and ('target_certificate_id' not in policy_param.keys()
                                        or policy_param['target_certificate_id'] is None):
            self.module.fail_json(msg="Please provide a target certificate ID or name.")
        if 'target_host' not in policy_param.keys() or policy_param['target_host'] is None:
            self.module.fail_json(msg="Please provide target host.")
        if 'action' not in policy_param.keys() or policy_param['action'] is None:
            self.module.fail_json(msg="Please provide action for the SyncIQ policy.")

    def validate_create_job(self, policy_details, is_target_policy):
        if not is_target_policy and not policy_details.enabled:
            self.module.fail_json(msg='Job cannot be started '
                                      'as policy is in disabled state.')

    def validate_job_params(self, job_params):
        if job_params['workers_per_node'] is not None:
            if job_params['action'] not in \
                    ('allow_write', 'allow_write_revert'):
                self.module.fail_json(msg='workers_per_node is valid '
                                      'only for allow_write and '
                                      'allow_write_revert operation.')

            if job_params['workers_per_node'] <= 0:
                self.module.fail_json(msg='Please enter a value greater than '
                                      '0 for workers_per_node.')

    def is_job_running(self, policy_obj, is_target_policy, action):
        job_exists = False
        if is_target_policy:
            target_policy_state = "enabling_writes" if action == \
                "allow_write" else "disabling_writes"
            job_exists = True if policy_obj.failover_failback_state == \
                target_policy_state and policy_obj.last_job_state != "failed" \
                else False
        else:
            policy_jobs = self.get_policy_jobs(policy_obj.name)
            job_exists = \
                [job for job in policy_jobs if job['action'] == action]

        return job_exists

    def validate_input(self, policy_id_or_name):
        if not policy_id_or_name or utils.is_input_empty(policy_id_or_name):
            self.module.fail_json(msg='Please specify policy_name or policy_id')

    def perform_module_operation(self):
        """
        Perform different actions on SyncIQ policy module based on
        parameters chosen in playbook
        """

        policy_name = self.module.params['policy_name']
        policy_id = self.module.params['policy_id']
        new_policy_name = self.module.params['new_policy_name']
        schedule = self.module.params['schedule']
        run_job = self.module.params['run_job']
        rpo_alert = self.module.params['rpo_alert']
        rpo_alert_unit = self.module.params['rpo_alert_unit']
        target_snapshot = self.module.params['target_snapshot']
        job_delay = self.module.params['job_delay']
        job_delay_unit = self.module.params['job_delay_unit']
        job_params = self.module.params['job_params']
        target_cluster = self.module.params['target_cluster']
        state = self.module.params['state']

        # Dictionary of inputs from playbook
        input_param = {}
        for param in self.module.params:
            input_param[param] = self.module.params[param]

        # result is a dictionary that contains changed status and SyncIQ
        # policy details
        result = dict(
            changed=False,
            synciq_policy_details='',
            target_synciq_policy_details='',
            create_synciq_policy=False,
            modify_synciq_policy=False,
            create_job_synciq_policy=False,
            delete_synciq_policy=False
        )
        policy_modifiable_dict = {}
        self.validate_input(policy_name or policy_id)
        if job_params:
            self.validate_job_params(job_params)

        # Check if policy exists
        policy_obj, is_target_policy = \
            self.get_synciq_policy_details(policy_name, policy_id, job_params)
        if not is_target_policy:
            if rpo_alert:
                rpo_alert = utils.get_time_in_seconds(rpo_alert,
                                                      rpo_alert_unit)

            if job_delay:
                job_delay = utils.get_time_in_seconds(job_delay,
                                                      job_delay_unit)

            if target_snapshot and \
                    target_snapshot['target_snapshot_expiration'] is not None:
                target_snapshot['target_snapshot_expiration'] = \
                    utils.get_time_in_seconds(
                        target_snapshot['target_snapshot_expiration'],
                        target_snapshot['exp_time_unit'])

            if run_job == 'when-source-modified' or \
                    run_job == 'when-snapshot-taken':
                schedule = run_job

            if target_cluster and not utils.ISI_SDK_VERSION_9 \
                    and (target_cluster['target_certificate_id']
                         or target_cluster['target_certificate_name']):
                self.module.fail_json(msg="Target certificate ID or name is "
                                      "not supported by isi_sdk_8_1_1.")

            # Construct dictionary of policy parameters to be passed while creating policy
            policy_param = self.construct_policy_params(input_param, schedule,
                                                        rpo_alert, job_delay)

            # Form dictionary of modifiable parameters of policy
            if policy_obj is not None and policy_param:
                policy_modifiable_dict = \
                    is_policy_modify(policy_obj, policy_param)

            # Rename policy
            if new_policy_name is not None and utils.is_input_empty(new_policy_name):
                self.module.fail_json(msg='new_policy_name cannot be empty. Please provide a valid '
                                          'new_policy_name to rename policy.')
            elif new_policy_name and policy_obj and new_policy_name != policy_obj.name:
                policy_modifiable_dict['name'] = policy_name = new_policy_name

            # Create a policy
            if policy_obj is None and state == 'present':
                # Check if all mandatory params are provided
                self.validate_create_params(policy_param)

                policy_id = self.create_synciq_policy(policy_param)
                result['create_synciq_policy'] = True
                result['changed'] = True

            # Modify SyncIQ policy
            if policy_modifiable_dict and state == "present":
                result['modify_synciq_policy'] = \
                    self.modify_synciq_policy(policy_modifiable_dict,
                                              policy_obj.id)
                result['changed'] = True

            # Delete SyncIQ policy
            if policy_obj and state == "absent":
                result['delete_synciq_policy'] = \
                    self.delete_synciq_policy(policy_obj.id)
                result['changed'] = True

            policy_obj, is_target_policy = \
                self.get_synciq_policy_details(policy_name, policy_id)

        # Create a job on SyncIQ policy
        if job_params:
            if job_params['action'] in ('allow_write', 'allow_write_revert'):
                if not policy_obj:
                    name_or_id = policy_name if policy_name else policy_id
                    self.module.fail_json("Target policy %s is not found to "
                                          "run failover/failover revert "
                                          "job." % (name_or_id))

            self.validate_create_job(policy_obj, is_target_policy)
            if not self.is_job_running(policy_obj, is_target_policy,
                                       job_params['action']):
                result['create_job_synciq_policy'] = \
                    self.create_synciq_job(policy_obj.id, job_params)
                result['changed'] = True

        # Display policy details
        if policy_obj:
            if is_target_policy:
                result['target_synciq_policy_details'] = policy_obj.to_dict()
            else:
                result['synciq_policy_details'] = \
                    self.get_synciq_policy_display_attributes(
                        policy_obj)
                policy_jobs = self.get_policy_jobs(policy_obj.name)
                result['synciq_policy_details'].update(jobs=policy_jobs)

        self.module.exit_json(**result)


def is_policy_modify(policy_obj, policy_param):
    """
    Check whether policy is modifiable
    :param policy_obj: Policy object of existing policy
    :param policy_param: Dictionary of parameters input from playbook
    :return :Dictionary of parameters that needs to be modified,
     if no parameters are to be modified dict is empty
    """
    modify_policy_dict = {}

    exclude_key = ['source_include_directories', 'source_exclude_directories', 'source_network']

    if 'source_include_directories' in policy_param and \
            set(policy_obj.source_include_directories) != set(policy_param['source_include_directories']):
        modify_policy_dict['source_include_directories'] = policy_param['source_include_directories']

    if 'source_exclude_directories' in policy_param and \
            set(policy_obj.source_exclude_directories) != set(policy_param['source_exclude_directories']):
        modify_policy_dict['source_exclude_directories'] = policy_param['source_exclude_directories']

    if 'source_network' in policy_param:
        modified_source_network = get_modified_source_network(policy_obj.source_network,
                                                              policy_param['source_network'])
        if modified_source_network:
            modify_policy_dict['source_network'] = modified_source_network

    policy_obj = policy_obj.to_dict()

    for param in policy_param:
        if policy_obj[param] != policy_param[param] and param not in exclude_key:
            modify_policy_dict[param] = policy_param[param]

    return modify_policy_dict


def construct_dict(input_param, key_name, policy_param_keys):
    """
    Construct a dictionary of parameters
    :param input_param: Dictionary of parameters provided from playbook
    :param key_name: Name of the key whose details needs to be constructed into dictionary
    :param policy_param_keys: List of keys that can be present in the final dictionary
    :return: dictionary of details
    """
    policy_param = {}
    for param in input_param[key_name]:
        if param in policy_param_keys and input_param[key_name][param] is not None:
            policy_param[param] = input_param[key_name][param]

    return policy_param


def get_modified_source_network(policy_obj_source_network, policy_param_source_network):
    if policy_obj_source_network:
        if policy_obj_source_network.pool != policy_param_source_network['pool'] \
                or policy_obj_source_network.subnet != policy_param_source_network['subnet']:
            return policy_param_source_network
    else:
        return policy_param_source_network


def get_synciqpolicy_parameters():
    """This method provides parameters required for the ansible SyncIQ policy
       module on PowerScale"""
    return dict(
        policy_name=dict(type='str'),
        new_policy_name=dict(type='str'),
        description=dict(type='str'),
        enabled=dict(type='bool'),
        policy_id=dict(type='str'),
        action=dict(type='str', choices=['copy', 'sync']),
        schedule=dict(type='str'),
        run_job=dict(type='str', choices=['on-schedule',
                                          'when-source-modified', 'when-snapshot-taken']),
        skip_when_source_unmodified=dict(type='bool'),
        rpo_alert=dict(type='int'),
        rpo_alert_unit=dict(type='str', choices=['minutes', 'hours',
                                                 'days', 'weeks', 'months', 'years'],
                            default='minutes'),
        job_delay=dict(type='int'),
        job_delay_unit=dict(type='str', choices=['seconds', 'minutes', 'hours', 'days'],
                            default='seconds'),
        snapshot_sync_pattern=dict(type='str'),
        source_cluster=dict(type='dict', options=dict(
            source_root_path=dict(type='str', no_log=True),
            source_network=dict(type='dict', options=dict(
                pool=dict(type='str'),
                subnet=dict(type='str')
            )),
            source_include_directories=dict(type='list', elements='str', no_log=True),
            source_exclude_directories=dict(type='list', elements='str', no_log=True))),
        target_cluster=dict(type='dict', options=dict(target_host=dict(type='str', no_log=True),
                                                      target_path=dict(type='str', no_log=True),
                                                      target_certificate_id=dict(type='str'),
                                                      target_certificate_name=dict(type='str')),
                            mutually_exclusive=[['target_certificate_id', 'target_certificate_name']]),
        target_snapshot=dict(type='dict', options=dict(target_snapshot_archive=dict(type='bool'),
                                                       target_snapshot_expiration=dict(type='int'),
                                                       exp_time_unit=dict(type='str', choices=['years', 'months',
                                                                                               'weeks', 'days'],
                                                                          default='years'),
                                                       )),
        job_params=dict(type='dict',
                        options=dict(action=dict(type='str', required=True,
                                                 choices=['run', 'resync_prep',
                                                          'allow_write',
                                                          'allow_write_revert']),
                                     source_snapshot=dict(type='str'),
                                     workers_per_node=dict(type='int'),
                                     wait_for_completion=dict(type='bool', default=False))),
        state=dict(required=True, type='str', choices=['present', 'absent'])
    )


def main():
    """ Create PowerScale SyncIQ policy object and perform action on it
        based on user input from playbook"""
    obj = SynciqPolicy()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
