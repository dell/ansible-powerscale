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

- A Dell PowerScale Storage system.
- Ansible-core 2.15 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  policy_name (optional, str, None)
    The name of the policy.

    Required at the time of policy creation, for the rest of the operations either :emphasis:`policy\_name` or :emphasis:`policy\_id` is required.


  policy_id (optional, str, None)
    The :emphasis:`policy\_id` is auto generated at the time of creation.

    For get/modify operations either :emphasis:`policy\_name` or :emphasis:`policy\_id` is needed.

    Parameters :emphasis:`policy\_name` and :emphasis:`policy\_id` are mutually exclusive.


  new_policy_name (optional, str, None)
    The new name of the policy while renaming an existing policy.

    :emphasis:`policy\_name` or :emphasis:`policy\_id` is required together with :emphasis:`new\_policy\_name`.


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
    If :emphasis:`run\_job` is set to :literal:`when-source-modified`\ , :emphasis:`job\_delay` is the duration to wait before triggering a job once there is modification on source.


  job_delay_unit (optional, str, seconds)
    Unit for :emphasis:`job\_delay`.


  rpo_alert (optional, int, None)
    If :emphasis:`run\_job` is set to :literal:`on-schedule` it is set to time/date, an alert is created if the specified RPO for this policy is exceeded.

    The default value is 0, which will not generate RPO alerts.


  rpo_alert_unit (optional, str, minutes)
    Unit for :emphasis:`rpo\_alert`.


  snapshot_sync_pattern (optional, str, None)
    The naming pattern that a snapshot must match to trigger a sync when the schedule is :literal:`when-snapshot-taken`.


  skip_when_source_unmodified (optional, bool, None)
    If true and schedule is set , the policy will not run if no changes have been made to the contents of the source directory since the last job successfully completed.

    Option modifiable when :emphasis:`run\_job` is :literal:`on-schedule`.


  schedule (optional, str, None)
    Schedule set when :emphasis:`run\_policy` is :literal:`on-schedule`.

    It must be in isidate format.

    If the format is not proper an error will be thrown.


  source_cluster (optional, dict, None)
    Defines the details of :emphasis:`source\_cluster`.


    source_root_path (optional, str, None)
      The root directory on the source cluster where the files will be synced from.

      Source root path should begin with /ifs. For example, if we want to create a synciq policy for the directory 'source' in the base path /ifs, then the :emphasis:`source\_root\_path` will be '/ifs/source'.


    source_exclude_directories (optional, list, None)
      List of path to the directories that should be excluded while running a policy.

      For example, if we want to exclude directory 'exclude1' at location '/ifs/source', then the :emphasis:`source\_exclude\_directories` will be '/ifs/source/exclude1'.


    source_include_directories (optional, list, None)
      List of path to the directories that should be included while running a policy

      For example, if we want to include directory 'include1' at location '/ifs/source', then the :emphasis:`source\_exclude\_directories` will be '/ifs/source/include1'.


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

      This parameter is not supported by isi\_sdk\_8\_1\_1


    target_certificate_name (optional, str, None)
      The name of the target cluster certificate being used for encryption

      Parameters :emphasis:`target\_certficate\_name` and :emphasis:`target\_certificate\_id` are mutually exclusive

      This parameter is not supported by isi\_sdk\_8\_1\_1



  target_snapshot (optional, dict, None)
    Details of snapshots to be created at the target.


    target_snapshot_archive (optional, bool, None)
      Indicates whether to take snapshot of the target.


    target_snapshot_expiration (optional, int, None)
      Expiration time of snapshot.

      Value 0 means no expiration.


    exp_time_unit (optional, str, years)
      Unit of :emphasis:`target\_snapshot` expiration time.



  job_params (optional, dict, None)
    Specifies the parameters to create a job on SyncIQ policy.


    action (True, str, None)
      The action to be taken by this job.


    wait_for_completion (optional, bool, False)
      Specifies if the job should run synchronously or asynchronously. By default the job is created to run asynchronously.


    source_snapshot (optional, str, None)
      An optional snapshot to copy/sync from.


    workers_per_node (optional, int, None)
      Specifies the desired workers per node. This parameter is valid for :emphasis:`allow\_write`\ , and :emphasis:`allow\_write\_revert` operation. This is an optional parameter and it defaults to 3.



  accelerated_failback (optional, bool, None)
    If set to :literal:`true`\ , SyncIQ will perform failback configuration tasks during the next job run, rather than waiting to perform those tasks during the failback process.

    Performing these tasks ahead of time will increase the speed of failback operations.

    It defaults to :literal:`true`\ , if not specified.


  restrict_target_network (optional, bool, None)
    If set to :literal:`true` then replication policies will connect only to nodes in the specified SmartConnect zone.

    If set to :literal:`false`\ , replication policies are not restricted to specific nodes on the target cluster.


  onefs_host (True, str, None)
    IP address or FQDN of the PowerScale cluster.


  port_no (False, str, 8080)
    Port number of the PowerScale cluster.It defaults to 8080 if not specified.


  verify_ssl (True, bool, None)
    boolean variable to specify whether to validate SSL certificate or not.

    :literal:`true` - indicates that the SSL certificate should be verified.

    :literal:`false` - indicates that the SSL certificate should not be verified.


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



Return Values
-------------

changed (always, bool, true)
  Whether or not the resource has changed.


synciq_policy_details (When SyncIQ policy exists, dict, {'action': 'copy', 'bandwidth': 100, 'description': 'SyncIQ policy Description', 'enabled': True, 'encryption': False, 'file_matching_pattern': {'or_criteria': 'None'}, 'id': 'd63b079d34adf2d2ec3ce92f15bfc730', 'job_delay': '1.0 days', 'job': [], 'name': 'SyncIQ_Policy', 'next_run_time': '1700479390', 'schedule': 'when-source-modified', 'source_root_path': '/ifs', 'target_certificate_id': '7sdgvejkiau7629903048hdjdkljsbwgsuasj7169823kkckll', 'target_certificate_name': 'test', 'target_host': '192.10.xxx.xxx', 'target_path': '/ifs/synciq', 'target_snapshot_archive': False})
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



target_synciq_policy_details (When failover/failback is performed on target cluster, dict, {'name': 'SyncIQ_Policy', 'id': 'd63b079d34adf2d2ec3ce92f15bfc730', 'failover_failback_state': 'enabled'})
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
- Kritika Bhateja(@Kritika-Bhateja-03) <ansible.team.dell.com>)

