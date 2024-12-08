#!/usr/bin/python
# Copyright: (c) 2021-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
  - dellemc.powerscale.powerscale
author:
- Spandita Panigrahi (@panigs7) <ansible.team@dell.com>
- Kritika Bhateja(@Kritika-Bhateja-03) <ansible.team.dell.com>)

options:
  policy_name:
    description:
    - The name of the policy.
    - Required at the time of policy creation, for the rest of the operations
      either I(policy_name) or I(policy_id) is required.
    type: str
  policy_id:
    description:
    - The I(policy_id) is auto generated at the time of creation.
    - For get/modify operations either I(policy_name) or I(policy_id) is needed.
    - Parameters I(policy_name) and I(policy_id) are mutually exclusive.
    type: str
  new_policy_name:
    description:
    - The new name of the policy while renaming an existing policy.
    - I(policy_name) or I(policy_id) is required together with I(new_policy_name).
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
    required: true
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
    choices: ['on-schedule', 'when-source-modified', 'when-snapshot-taken', 'manual']
  job_delay:
    description:
    - If I(run_job) is set to C(when-source-modified), I(job_delay) is the
      duration to wait before triggering a job once there is modification on source.
    type: int
  job_delay_unit:
    description:
    - Unit for I(job_delay).
    type: str
    choices: ['seconds', 'minutes', 'hours', 'days']
    default: 'seconds'
  rpo_alert:
    description:
    - If I(run_job) is set to C(on-schedule) it is set to time/date,
      an alert is created if the specified RPO for this policy is exceeded.
    - The default value is 0, which will not generate RPO alerts.
    type: int
  rpo_alert_unit:
    description:
    - Unit for I(rpo_alert).
    type: str
    choices: ['minutes', 'hours', 'days', 'weeks', 'months', 'years']
    default: 'minutes'
  snapshot_sync_pattern:
    description:
    - The naming pattern that a snapshot must match to trigger
      a sync when the schedule is C(when-snapshot-taken).
    type: str
  skip_when_source_unmodified:
    description:
    - If true and schedule is set , the policy will not run if
      no changes have been made to the contents of the source
      directory since the last job successfully completed.
    - Option modifiable when I(run_job) is C(on-schedule).
    type: bool
  schedule:
    description:
    - Schedule set when I(run_policy) is C(on-schedule).
    - It must be in isidate format.
    - If the format is not proper an error will be thrown.
    type: str
  source_cluster:
    description:
    - Defines the details of I(source_cluster).
    type: dict
    suboptions:
        source_root_path:
            description:
            - The root directory on the source cluster where
              the files will be synced from.
            - Source root path should begin with /ifs. For example, if we want to create a synciq
              policy for the directory 'source' in the base path /ifs, then the I(source_root_path)
              will be '/ifs/source'.
            type: str
        source_exclude_directories:
            description:
            - List of path to the directories that
              should be excluded while running a policy.
            - For example, if we want to exclude directory 'exclude1' at location '/ifs/source',
              then the I(source_exclude_directories) will be '/ifs/source/exclude1'.
            type: list
            elements: str
        source_include_directories:
            description:
            -  List of path to the directories
               that should be included while running a policy
            - For example, if we want to include directory 'include1' at location '/ifs/source',
              then the I(source_exclude_directories) will be '/ifs/source/include1'.
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
            - The directory location to have the replicated source data.
            type: str
        target_certificate_id:
            description:
            - The ID of the target cluster certificate being used for encryption
            - This parameter is not supported by isi_sdk_8_1_1
            type: str
        target_certificate_name:
            description:
            - The name of the target cluster certificate being used for encryption
            - Parameters I(target_certficate_name) and I(target_certificate_id) are mutually exclusive
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
            - Unit of I(target_snapshot) expiration time.
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
            required: true
        wait_for_completion:
            description:
            - Specifies if the job should run synchronously or asynchronously.
              By default the job is created to run asynchronously.
            type: bool
            default: false
        source_snapshot:
            description:
            - An optional snapshot to copy/sync from.
            type: str
        workers_per_node:
            description:
            - Specifies the desired workers per node. This parameter is valid
              for I(allow_write), and I(allow_write_revert) operation. This is an
              optional parameter and it defaults to 3.
            type: int
  accelerated_failback:
    description:
    - If set to C(true), SyncIQ will perform failback configuration tasks during the next job run,
      rather than waiting to perform those tasks during the failback process.
    - Performing these tasks ahead of time will increase the speed of failback operations.
    - It defaults to C(true), if not specified.
    type: bool
  restrict_target_network:
    description:
    - If set to C(true) then replication policies will connect only to nodes in the specified SmartConnect zone.
    - If set to C(false), replication policies are not restricted to specific nodes on the target cluster.
    type: bool
attributes:
  check_mode:
    description:
    - Runs task to validate without performing action on the target machine.
    support: full
  diff_mode:
    description:
    - Runs the task to report the changes made or to be made.
    support: full
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
    enabled: true
    policy_name: "New_policy"
    run_job: "on-schedule"
    schedule: "every 1 days at 12:00 PM"
    skip_when_source_unmodified: true
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
      target_snapshot_archive: true
      target_snapshot_expiration: 90
      exp_time_unit: "day"
    accelerated_failback: false
    restrict_target_network: true
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
    enabled: false
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
      target_snapshot_archive: false
    accelerated_failback: true
    restrict_target_network: false
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
      wait_for_completion: false
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
      wait_for_completion: false
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
      wait_for_completion: false
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
      wait_for_completion: false
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
    sample: "true"
synciq_policy_details:
    description: Details of the SyncIQ policy.
    returned: When SyncIQ policy exists
    type: dict
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
    sample: {
        "action": "copy",
        "bandwidth": 100,
        "description": "SyncIQ policy Description",
        "enabled": true,
        "encryption": false,
        "file_matching_pattern": {
            "or_criteria": null
        },
        "id": "d63b079d34adf2d2ec3ce92f15bfc730",
        "job_delay": "1.0 days",
        "job": [],
        "name": "SyncIQ_Policy",
        "next_run_time": "1700479390",
        "schedule": "when-source-modified",
        "source_root_path": "/ifs",
        "target_certificate_id": "7sdgvejkiau7629903048hdjdkljsbwgsuasj7169823kkckll",
        "target_certificate_name": "test",
        "target_host": "192.10.xxx.xxx",
        "target_path": "/ifs/synciq",
        "target_snapshot_archive": false
    }
target_synciq_policy_details:
    description: Details of the target SyncIQ policy.
    returned: When failover/failback is performed on target cluster
    type: dict
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
    sample: {
        "name": "SyncIQ_Policy",
        "id": "d63b079d34adf2d2ec3ce92f15bfc730",
        "failover_failback_state": "enabled"
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('synciqpolicy')


class SynciqPolicy(object):
    """Class with SyncIQ Policy operations"""

    def __init__(self):
        """ Define all parameters required by this module"""
        self.result = {
            "changed": False,
            "synciq_policy_details": {},
            "target_synciq_policy_details": {},
            "create_synciq_policy": False,
            "modify_synciq_policy": False,
            "create_job_synciq_policy": False,
            "delete_synciq_policy": False,
            "diff": {}
        }
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_synciqpolicy_parameters())
        mutually_exclusive = [['policy_name', 'policy_id']]

        # initialize the Ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=True,
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
        if self.module._diff:
            self.result.update({"diff": {"before": {}, "after": policy_param}})
        try:
            LOG.debug("Parameters to set when creating a SyncIQ policy %s", policy_param)
            if not self.module.check_mode:
                policy_id = self.api_instance.create_sync_policy(sync_policy=policy_param)
                return policy_id
            return True
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Creating SyncIQ policy %s failed with ' \
                            'error : %s' % (policy_param['name'], str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def modify_synciq_policy(self, policy_params_dict, policy_id, policy_details):
        """
        Modify SyncIQ policy.
        :policy_params_dict: Dictionary of parameters to be modified of a policy
        :policy_id: ID of the policy to be modified
        :return: True if modify is successful
        """
        if self.module._diff:
            self.result.update({"diff": {"before": policy_details.to_dict(), "after": policy_params_dict}})
        try:
            if policy_params_dict is not None:
                LOG.debug("Policy parameters being modified : %s", policy_params_dict)
                if not self.module.check_mode:
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
            if job_params and not self.module.check_mode:
                sync_job_params = {}
                sync_job_keys = ['action', 'source_snapshot']
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

    def delete_synciq_policy(self, policy_id, policy_details):
        """
        Delete SyncIQ policy.
        :param policy_id: ID of SyncIQ policy
        :return: True if deletion is successful
        """
        if self.module._diff:
            self.result.update({"diff": {"before": policy_details.to_dict(), "after": {}}})
        try:
            if not self.module.check_mode:
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
                             'target_snapshot_expiration', 'snapshot_sync_pattern', 'accelerated_failback',
                             'restrict_target_network'
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

            if 'target_certificate_name' in input_param['target_cluster'] and input_param['target_cluster']['target_certificate_name']:
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
        if 'target_host' not in policy_param.keys() or policy_param['target_host'] is None:
            self.module.fail_json(msg="Please provide target host.")
        if 'action' not in policy_param.keys() or policy_param['action'] is None:
            self.module.fail_json(msg="Please provide action for the SyncIQ policy.")

    def validate_create_job(self, policy_details, is_target_policy):
        if not is_target_policy and not policy_details.enabled:
            self.module.fail_json(msg='Job cannot be started '
                                      'as policy is in disabled state.')

    def validate_job_params(self, job_params):

        # if not job_params:
        #     return
        if job_params.get('workers_per_node') is not None:
            if job_params['action'] not in \
                    ('allow_write', 'allow_write_revert'):
                self.module.fail_json(msg='workers_per_node is valid '
                                      'only for allow_write and '
                                      'allow_write_revert operation.')

            if job_params.get('workers_per_node') and job_params.get('workers_per_node') <= 0:
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
                                          'when-source-modified', 'when-snapshot-taken',
                                          'manual']),
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
        accelerated_failback=dict(type='bool'),
        restrict_target_network=dict(type='bool'),
        state=dict(required=True, type='str', choices=['present', 'absent'])
    )


class SynciqPolicyExitHandler:
    def handle(self, synciq_obj):
        synciq_obj.module.exit_json(**synciq_obj.result)


class SynciqPolicyGetDetailsHandler:
    def handle(self, synciq_obj, policy_obj, is_target_policy):
        if policy_obj:
            if is_target_policy:
                synciq_obj.result['target_synciq_policy_details'] = policy_obj.to_dict()
            else:
                synciq_obj.result['synciq_policy_details'] = \
                    synciq_obj.get_synciq_policy_display_attributes(
                        policy_obj)
                policy_jobs = synciq_obj.get_policy_jobs(policy_obj.name)
                synciq_obj.result['synciq_policy_details'].update(jobs=policy_jobs)
        SynciqPolicyExitHandler().handle(synciq_obj)


class SynciqPolicyJobCreateHandler:
    def handle(self, synciq_obj, synciq_params, policy_obj, is_target_policy):
        job_params = synciq_params.get('job_params')
        policy_name = synciq_params.get('policy_name')
        policy_id = synciq_params.get('policy_id')
        policy_obj, is_target_policy = \
            synciq_obj.get_synciq_policy_details(policy_name, policy_id)
        if job_params:
            if job_params['action'] in ('allow_write', 'allow_write_revert'):
                if not policy_obj:
                    name_or_id = policy_name if policy_name else policy_id
                    synciq_obj.module.fail_json("Target policy %s is not found to "
                                                "run failover/failover revert "
                                                "job." % (name_or_id))
            synciq_obj.validate_create_job(policy_obj, is_target_policy)
            if not synciq_obj.is_job_running(policy_obj, is_target_policy,
                                             job_params['action']):
                synciq_obj.result['create_job_synciq_policy'] = \
                    synciq_obj.create_synciq_job(policy_obj.id, job_params)
                synciq_obj.result['changed'] = True
        SynciqPolicyGetDetailsHandler().handle(synciq_obj, policy_obj, is_target_policy)


class SynciqPolicyDeleteHandler:
    def handle(self, synciq_obj, synciq_params, policy_obj, is_target_policy):
        if not is_target_policy and policy_obj:
            if synciq_params.get("state") == "absent":
                synciq_obj.result['delete_synciq_policy'] = \
                    synciq_obj.delete_synciq_policy(policy_obj.id, policy_obj)
                synciq_obj.result['changed'] = True
        SynciqPolicyJobCreateHandler().handle(synciq_obj, synciq_params, policy_obj, is_target_policy)


class SynciqPolicyModifyHandler:
    def handle(self, synciq_obj, synciq_params, policy_modifiable_dict, policy_obj, is_target_policy):
        if not is_target_policy:
            if policy_modifiable_dict and synciq_params.get("state") == "present":
                synciq_obj.result['modify_synciq_policy'] = \
                    synciq_obj.modify_synciq_policy(policy_modifiable_dict,
                                                    policy_obj.id, policy_obj)
                synciq_obj.result['changed'] = True
        SynciqPolicyDeleteHandler().handle(synciq_obj, synciq_params, policy_obj, is_target_policy)


class SynciqPolicyCreateHandler:
    def rename_policy(self, synciq_obj, policy_obj, synciq_params, policy_modifiable_dict):
        new_policy_name = synciq_params.get('new_policy_name')
        if new_policy_name is not None and utils.is_input_empty(new_policy_name):
            synciq_obj.module.fail_json(msg='new_policy_name cannot be empty. Please provide a valid '
                                        'new_policy_name to rename policy.')
        elif new_policy_name and policy_obj and new_policy_name != policy_obj.name:
            policy_modifiable_dict['name'] = policy_name = new_policy_name

    def create_policy(self, synciq_obj, synciq_params, policy_obj, policy_param):
        state = synciq_params.get('state')
        if policy_obj is None and state == 'present':
            # Check if all mandatory params are provided
            synciq_obj.validate_create_params(policy_param)
            policy_param['accelerated_failback'] = True if synciq_params.get('accelerated_failback') is None else synciq_params.get('accelerated_failback')
            policy_id = synciq_obj.create_synciq_policy(policy_param)
            synciq_obj.result['create_synciq_policy'] = True
            synciq_obj.result['changed'] = True

    def handle(self, synciq_obj, synciq_params, policy_param, policy_modifiable_dict, policy_obj, is_target_policy):
        if not is_target_policy:
            self.rename_policy(synciq_obj, policy_obj, synciq_params, policy_modifiable_dict)
            self.create_policy(synciq_obj, synciq_params, policy_obj, policy_param)

        SynciqPolicyModifyHandler().handle(synciq_obj, synciq_params, policy_modifiable_dict, policy_obj, is_target_policy)


class SynciqPolicyHandler:
    """SyncIQ Policy Handler"""

    def determine_schedule(self, run_job):
        """
        Determine the schedule based on the run_job value.
        :param run_job: The type of job scheduling
        :return: The schedule string
        """
        schedule = ''
        if run_job == 'when-source-modified' or run_job == 'when-snapshot-taken':
            schedule = run_job
        elif run_job == 'manual':
            schedule = ''
        return schedule

    def handle(self, synciq_obj, synciq_params):
        policy_name = synciq_params.get('policy_name')
        policy_id = synciq_params.get('policy_id')
        job_params = synciq_params.get('job_params')
        run_job = synciq_params.get('run_job')
        target_snapshot = synciq_params.get('target_snapshot')
        rpo_alert = synciq_params.get('rpo_alert')
        rpo_alert_unit = synciq_params.get('rpo_alert_unit')
        job_delay = synciq_params.get('job_delay')
        job_delay_unit = synciq_params.get('job_delay_unit')
        synciq_obj.validate_input(policy_name or policy_id)
        if job_params:
            synciq_obj.validate_job_params(job_params)

        policy_obj, is_target_policy = \
            synciq_obj.get_synciq_policy_details(policy_name, policy_id, job_params)
        if not is_target_policy:
            rpo_alert = utils.get_time_in_seconds(rpo_alert, rpo_alert_unit) if rpo_alert else None
            job_delay = utils.get_time_in_seconds(job_delay, job_delay_unit) if job_delay else None

            if target_snapshot and target_snapshot.get('target_snapshot_expiration') is not None:
                target_snapshot['target_snapshot_expiration'] = utils.get_time_in_seconds(
                    target_snapshot['target_snapshot_expiration'],
                    target_snapshot['exp_time_unit']
                )
            schedule = self.determine_schedule(run_job)

            # Construct dictionary of policy parameters to be passed while creating policy
            policy_param = synciq_obj.construct_policy_params(synciq_params, schedule,
                                                              rpo_alert, job_delay)
            # Form dictionary of modifiable parameters of policy
            policy_modifiable_dict = {}
            if policy_obj is not None and policy_param:
                policy_modifiable_dict = \
                    is_policy_modify(policy_obj, policy_param)

        SynciqPolicyCreateHandler().handle(synciq_obj, synciq_params, policy_param, policy_modifiable_dict, policy_obj, is_target_policy)


def main():
    """ Create PowerScale SyncIQ policy object and perform action on it
        based on user input from playbook"""
    obj = SynciqPolicy()
    SynciqPolicyHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
