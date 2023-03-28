.. _synciqpolicy_module:


synciqpolicy -- Manage SyncIQ policies on PowerScale
====================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing SyncIQ policies on PowerScale includes create a SyncIQ policy, modify a SyncIQ policy, get details of a SyncIQ policy, creating jobs on SyncIQ policy.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system. Ansible 2.12, 2.13 or 2.14.



Parameters
----------

  policy_name (optional, str, None)
    The name of the policy.

    Required at the time of policy creation, for the rest of the operations either policy_name or policy_id is required.


  policy_id (optional, str, None)
    The policy_id is auto generated at the time of creation.

    For get/modify operations either policy_name or policy_id is needed.

    Parameters policy_name and policy_id are mutually exclusive.


  new_policy_name (optional, str, None)
    The new name of the policy while renaming an existing policy.

    policy_name or policy_id is required together with new_policy_name.


  action (optional, str, None)
    Indicates type of replication action to be performed on the source.


  state (True, str, None)
    The state option is used to determine whether the policy exists or not.


  description (optional, str, None)
    Description of the policy.


  enabled (optional, bool, None)
    Indicates whether policy is enabled or disabled.


  run_job (optional, str, None)
    Types of scheduling a job on the policy.


  job_delay (optional, int, None)
    If run_job is set to when-source-modified, job_delay is the duration to wait before triggering a job once there is modification on source.


  job_delay_unit (optional, str, seconds)
    Unit for job_delay.


  rpo_alert (optional, int, None)
    If run_job is set to 'on-schedule' it is set to time/date, an alert is created if the specified RPO for this policy is exceeded.

    The default value is 0, which will not generate RPO alerts.


  rpo_alert_unit (optional, str, minutes)
    Unit for rpo_alert.


  snapshot_sync_pattern (optional, str, None)
    The naming pattern that a snapshot must match to trigger a sync when the schedule is when-snapshot-taken.


  skip_when_source_unmodified (optional, bool, None)
    If true and schedule is set , the policy will not run if no changes have been made to the contents of the source directory since the last job successfully completed.

    Option modifiable when run_job is "on_schedule".


  schedule (optional, str, None)
    Schedule set when run_policy is 'on-schedule'.

    It must be in isidate format.

    If the format is not proper an error will be thrown.


  source_cluster (optional, dict, None)
    Defines the details of source_cluster.


    source_root_path (optional, str, None)
      The root directory on the source cluster where the files will be synced from.

      Source root path should begin with /ifs. For example, if we want to create a synciq policy for the directory 'source' in the base path /ifs, then the source_root_path will be '/ifs/source'.


    source_exclude_directories (optional, list, None)
      List of path to the directories that should be excluded while running a policy.

      For example, if we want to exclude directory 'exclude1' at location '/ifs/source', then the source_exclude_directories will be '/ifs/source/exclude1'.


    source_include_directories (optional, list, None)
      List of path to the directories that should be included while running a policy

      For example, if we want to include directory 'include1' at location '/ifs/source', then the source_exclude_directories will be '/ifs/source/include1'.


    source_network (optional, dict, None)
      Run the policy only on nodes in the specified subnet and pool.


      pool (optional, str, None)
        The pool to restrict replication policies to.


      subnet (optional, str, None)
        The subnet to restrict replication policies to.




  target_cluster (optional, dict, None)
    Details of the target cluster.


    target_host (optional, str, None)
      Host IP or FQDN where we want to replicate the source.


    target_path (optional, str, None)
      The directory location to have the replicated source data.


    target_certificate_id (optional, str, None)
      The ID of the target cluster certificate being used for encryption

      This parameter is not supported by isi_sdk_8_1_1


    target_certificate_name (optional, str, None)
      The name of the target cluster certificate being used for encryption

      Parameters target_certficate_name and target_certificate_id are mutually exclusive

      This parameter is not supported by isi_sdk_8_1_1



  target_snapshot (optional, dict, None)
    Details of snapshots to be created at the target.


    target_snapshot_archive (optional, bool, None)
      Indicates whether to take snapshot of the target.


    target_snapshot_expiration (optional, int, None)
      Expiration time of snapshot.

      Value 0 means no expiration.


    exp_time_unit (optional, str, years)
      Unit of target_snapshot expiration time.



  job_params (optional, dict, None)
    Specifies the parameters to create a job on SyncIQ policy.


    action (True, str, None)
      The action to be taken by this job.


    wait_for_completion (optional, bool, False)
      Specifies if the job should run synchronously or asynchronously. By default the job is created to run asynchronously.


    source_snapshot (optional, str, None)
      An optional snapshot to copy/sync from.


    workers_per_node (optional, int, None)
      Specifies the desired workers per node. This parameter is valid for allow_write, and allow_write_revert operation. This is an optional parameter and it defaults to 3.



  accelerated_failback (optional, bool, None)
    If set to true, SyncIQ will perform failback configuration tasks during the next job run, rather than waiting to perform those tasks during the failback process. Performing these tasks ahead of time will increase the speed of failback operations.

    It defaults to True, if not specified.


  restrict_target_network (optional, bool, None)
    If set to true then replication policies will connect only to nodes in the specified SmartConnect zone. If set to false, replication policies are not restricted to specific nodes on the target cluster.


  onefs_host (True, str, None)
    IP address or FQDN of the PowerScale cluster.


  port_no (False, str, 8080)
    Port number of the PowerScale cluster.It defaults to 8080 if not specified.


  verify_ssl (True, bool, None)
    boolean variable to specify whether to validate SSL certificate or not.

    True - indicates that the SSL certificate should be verified.

    False - indicates that the SSL certificate should not be verified.


  api_user (True, str, None)
    username of the PowerScale cluster.


  api_password (True, str, None)
    the password of the PowerScale cluster.





Notes
-----

.. note::
   - There is a delay to view the jobs running on the policy.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
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
          accelerated_failback: False
          restrict_target_network: True
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
          accelerated_failback: True
          restrict_target_network: False
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



Return Values
-------------

changed (always, bool, )
  Whether or not the resource has changed.


synciq_policy_details (When SyncIQ policy exists, complex, )
  Details of the SyncIQ policy.


  name (, str, )
    The name of the policy.


  id (, str, )
    ID of the policy.


  enabled (, bool, )
    Indicates whether policy is enabled


  action (, str, )
    Type of action for the policy


  schedule (, str, )
    Type of schedule chosen to run a policy


  source_root_path (, str, )
    The path to the source directory to be replicated


  target_host (, str, )
    The IP/FQDN of the host where source is replicated


  target_path (, str, )
    The target directory where source is replicated


  jobs (, list, )
    List of jobs running on the policy



target_synciq_policy_details (When failover/failback is performed on target cluster, complex, )
  Details of the target SyncIQ policy.


  name (, str, )
    The name of the policy.


  id (, str, )
    ID of the policy.


  failover_failback_state (, str, )
    The state of the policy with respect to sync failover/failback.






Status
------





Authors
~~~~~~~

- Spandita Panigrahi (@panigs7) <ansible.team@dell.com>

