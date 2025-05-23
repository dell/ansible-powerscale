.. _synciqtargetreports_module:


synciqtargetreports -- Provides the SyncIQ target reports for PowerScale Storage System
=======================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

This module provides the SyncIQ target reports for PowerScale Storage System.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.16 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  name (optional, str, None)
    The name of the SyncIQ target report.


  id (optional, str, None)
    The id of the SyncIQ target report.


  sub_report_id (optional, str, None)
    The id of the SyncIQ target sub report.


  include_sub_reports (optional, bool, False)
    This flag is used to fetch the list of target sub reports.


  state (True, str, None)
    The state option is used to mention the existence of target reports.


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
   - The :emphasis:`check\_mode` is not supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get a single SyncIQ target report with id
      dellemc.powerscale.synciqtargetreports:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        id: "2-sample_policy"
        state: "present"

    - name: Get a single SyncIQ target report with name
      dellemc.powerscale.synciqtargetreports:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        name: "sample_policy"
        state: "present"

    - name: Get all SyncIQ target sub-reports with report id
      dellemc.powerscale.synciqtargetreports:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        id: "2-sample_policy"
        include_sub_reports: true
        state: "present"

    - name: Get all SyncIQ target sub-reports with report name
      dellemc.powerscale.synciqtargetreports:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        name: "sample_policy"
        include_sub_reports: true
        state: "present"

    - name: Get a single SyncIQ target sub-report with sub-report id
      dellemc.powerscale.synciqtargetreports:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        id: "2-sample_policy"
        sub_report_id: "1"
        state: "present"



Return Values
-------------

changed (always, bool, )
  Whether or not the resource has changed.


synciq_target_report (When SyncIQ target report exists, complex, )
  Details of the SyncIQ target report.


  action (, str, )
    The action to be taken by this job.


  ads_streams_replicated (, int, )
    The number of ads streams replicated by this job.


  block_specs_replicated (, int, )
    The number of block specs replicated by this job.


  bytes_recoverable (, int, )
    The number of bytes recoverable by this job.


  bytes_transferred (, int, )
    The number of bytes that have been transferred by this job.


  char_specs_replicated (, int, )
    The number of char specs replicated by this job.


  committed_files (, int, )
    The number of WORM committed files.


  corrected_lins (, int, )
    The number of LINs corrected by this job.


  dead_node (, bool, )
    This field is true if the node running this job is dead.


  directories_replicated (, int, )
    The number of directories replicated.


  dirs_changed (, int, )
    The number of directories changed by this job.


  dirs_deleted (, int, )
    The number of directories deleted by this job.


  dirs_moved (, int, )
    The number of directories moved by this job.


  dirs_new (, int, )
    The number of directories created by this job.


  duration (, int, )
    The amount of time in seconds between when the job was started and when it ended. If the job has not yet ended, this is the amount of time since the job started. This field is null if the job has not yet started.


  encrypted (, bool, )
    If true, syncs will be encrypted.


  end_time (, int, )
    The time the job ended in unix epoch seconds. The field is null if the job hasn't ended.


  error (, str, )
    The primary error message for this job.


  error_checksum_files_skipped (, int, )
    The number of files with checksum errors skipped by this job.


  error_io_files_skipped (, int, )
    The number of files with io errors skipped by this job.


  error_net_files_skipped (, int, )
    The number of files with network errors skipped by this job.


  errors (, list, )
    A list of error messages for this job.


  failed_chunks (, int, )
    The number of data chunks that failed transmission.


  fifos_replicated (, int, )
    The number of fifos replicated by this job.


  file_data_bytes (, int, )
    The number of bytes transferred that belong to files.


  files_changed (, int, )
    The number of files changed by this job.


  files_linked (, int, )
    The number of files linked by this job.


  files_new (, int, )
    The number of files created by this job.


  files_selected (, int, )
    The number of files selected by this job.


  files_transferred (, int, )
    The number of files transferred by this job.


  files_unlinked (, int, )
    The number of files unlinked by this job.


  files_with_ads_replicated (, int, )
    The number of files with ads replicated by this job.


  flipped_lins (, int, )
    The number of LINs flipped by this job.


  hard_links_replicated (, int, )
    The number of hard links replicated by this job.


  hash_exceptions_fixed (, int, )
    The number of hash exceptions fixed by this job.


  hash_exceptions_found (, int, )
    The number of hash exceptions found by this job.


  id (, str, )
    A unique identifier for this object.


  job_id (, int, )
    The ID of the job.


  lins_total (, int, )
    The number of LINs transferred by this job.


  network_bytes_to_source (, int, )
    The total number of bytes sent to the source by this job.


  network_bytes_to_target (, int, )
    The total number of bytes sent to the target by this job.


  new_files_replicated (, int, )
    The number of new files replicated by this job.


  num_retransmitted_files (, int, )
    The number of files that have been retransmitted by this job.


  phases (, complex, )
    Data for each phase of this job.


    phase (, str, )
      The phase that the job was in.


    end_time (, int, )
      The time the job ended this phase.


    start_time (, int, )
      The time the job began this phase.



  policy (, complex, )
    Policy details


    name (, str, )
      User-assigned name of this sync policy.


    source_root_path (, str, )
      The root directory on the source cluster the files will be synced from.


    target_host (, str, )
      Hostname or IP address of sync target cluster.



  policy_action (, str, )
    This is the action the policy is configured to perform.


  policy_id (, str, )
    The ID of the policy.


  policy_name (, str, )
    The name of the policy.


  quotas_deleted (, int, )
    The number of quotas removed from the target.


  regular_files_replicated (, int, )
    The number of regular files replicated by this job.


  resynced_lins (, int, )
    The number of LINs resynched by this job.


  retransmitted_files (, list, )
    The files that have been retransmitted by this job.


  retry (, int, )
    The number of times the job has been retried.


  running_chunks (, int, )
    The number of data chunks currently being transmitted.


  service_report (, complex, )
    Data for each component exported as part of service replication.


    status (, str, )
      The current status of export for this component.


    start_time (, int, )
      The time the job began this component.


    end_time (, int, )
      The time the job end this component.



  sockets_replicated (, int, )
    The number of sockets replicated by this job.


  source_bytes_recovered (, int, )
    The number of bytes recovered on the source.


  source_directories_created (, int, )
    The number of directories created on the source.


  source_directories_deleted (, int, )
    The number of directories deleted on the source.


  source_directories_linked (, int, )
    The number of directories linked on the source.


  source_directories_unlinked (, int, )
    The number of directories unlinked on the source.


  source_directories_visited (, int, )
    The number of directories visited on the source.


  source_files_deleted (, int, )
    The number of files deleted on the source.


  source_files_linked (, int, )
    The number of files linked on the source.


  source_files_unlinked (, int, )
    The number of sparse data bytes transferred by this job.


  start_time (, int, )
    The time the job started in unix epoch seconds. The field is null if the job hasn't started.


  state (, str, )
    The state of the job.


  subreport_count (, int, )
    The number of subreports that are available for this job report.


  succeeded_chunks (, int, )
    The number of data chunks that have been transmitted successfully.


  symlinks_replicated (, int, )
    The number of symlinks replicated by this job.


  sync_type (, str, )
    The type of sync being performed by this job.


  target_bytes_recovered (, int, )
    The number of bytes recovered on the target.


  target_directories_created (, int, )
    The number of directories created on the target.


  target_directories_deleted (, int, )
    The number of directories deleted on the target.


  target_directories_linked (, int, )
    The number of directories linked on the target.


  target_directories_unlinked (, int, )
    The number of directories unlinked on the target.


  target_files_deleted (, int, )
    The number of files deleted on the target.


  target_files_linked (, int, )
    The number of files linked on the target.


  target_files_unlinked (, int, )
    The number of files unlinked on the target.


  target_snapshots (, list, )
    The target snapshots created by this job.


  total_chunks (, int, )
    The total number of data chunks transmitted by this job.


  total_data_bytes (, int, )
    The total number of bytes transferred by this job.


  total_exported_services (, int, )
    The total number of components exported as part of service replication.


  total_files (, int, )
    The number of files affected by this job.


  total_network_bytes (, int, )
    The total number of bytes sent over the network by this job.


  total_phases (, int, )
    The total number of phases for this job.


  unchanged_data_bytes (, int, )
    The number of bytes unchanged by this job.


  up_to_date_files_skipped (, int, )
    The number of up-to-date files skipped by this job.


  updated_files_replicated (, int, )
    The number of updated files replicated by this job.


  user_conflict_files_skipped (, int, )
    The number of files with user conflicts skipped by this job.


  warnings (, list, )
    A list of warning messages for this job.


  worm_committed_file_conflicts (, int, )
    The number of WORM committed files which needed to be reverted. Since WORM committed files cannot be reverted, this is the number of files that were preserved in the compliance store.






Status
------





Authors
~~~~~~~

- Meenakshi Dembi (@dembim) <ansible.team@dell.com>

