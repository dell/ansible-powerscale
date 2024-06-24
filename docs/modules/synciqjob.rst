.. _synciqjob_module:


synciqjob -- Manage SyncIQ jobs on PowerScale
=============================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing SyncIQ jobs on PowerScale storage system includes retrieving and modifying details of a SyncIQ job.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.15 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  job_id (True, str, None)
    Specifies the id or name of the policy job.


  job_state (optional, str, None)
    Specifies the state of the job.


  state (True, str, None)
    The state of the SyncIQ job after the task is performed.

    ``present`` - indicates that the SyncIQ job should exist on the system.

    ``absent`` - indicates that the SyncIQ job should not exist on the system.


  onefs_host (True, str, None)
    IP address or FQDN of the PowerScale cluster.


  port_no (False, str, 8080)
    Port number of the PowerScale cluster.It defaults to 8080 if not specified.


  verify_ssl (True, bool, None)
    boolean variable to specify whether to validate SSL certificate or not.

    ``true`` - indicates that the SSL certificate should be verified.

    ``false`` - indicates that the SSL certificate should not be verified.


  api_user (True, str, None)
    username of the PowerScale cluster.


  api_password (True, str, None)
    the password of the PowerScale cluster.





Notes
-----

.. note::
   - There is delay in the actual state change of the SyncIQ job. The state change of jobs in 'scheduled' state is not supported.
   - To start the SyncIQ job use the :ref:`dellemc.powerscale.synciqpolicy <dellemc.powerscale.synciqpolicy_module>` module.
   - The *check_mode* is not supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
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



Return Values
-------------

changed (always, bool, )
  Whether or not the resource has changed.


job_details (When SyncIQ job exists, complex, )
  The SyncIQ job details.


  action (, str, )
    The action to be taken by this job.


  id (, str, )
    A unique identifier for this object.


  policy_id (, str, )
    The id of the policy from which the job is triggered.


  policy_name (, str, )
    The name of the policy from which this job is triggered.


  sync_type (, str, )
    The type of sync being performed by this job.


  state (, str, )
    The state of the job.



modified_job (When SyncIQ job is modified, complex, {'job_details': [{'action': 'run', 'ads_streams_replicated': 0, 'block_specs_replicated': 0, 'bytes_recoverable': 0, 'bytes_transferred': 0, 'char_specs_replicated': 0, 'committed_files': 0, 'corrected_lins': 0, 'dead_node': False, 'directories_replicated': 0, 'dirs_changed': 0, 'dirs_deleted': 0, 'dirs_moved': 0, 'dirs_new': 0, 'duration': 1, 'encrypted': True, 'end_time': 1687488893, 'error': '', 'error_checksum_files_skipped': 0, 'error_io_files_skipped': 0, 'error_net_files_skipped': 0, 'errors': [], 'failed_chunks': 0, 'fifos_replicated': 0, 'file_data_bytes': 0, 'files_changed': 0, 'files_linked': 0, 'files_new': 0, 'files_selected': 0, 'files_transferred': 0, 'files_unlinked': 0, 'files_with_ads_replicated': 0, 'flipped_lins': 0, 'hard_links_replicated': 0, 'hash_exceptions_fixed': 0, 'hash_exceptions_found': 0, 'id': 'test', 'job_id': 1, 'lins_total': 0, 'network_bytes_to_source': 0, 'network_bytes_to_target': 0, 'new_files_replicated': 0, 'num_retransmitted_files': 0, 'phases': [], 'policy': {'action': 'sync', 'file_matching_pattern': {'or_criteria': None}, 'name': 'test', 'source_exclude_directories': [], 'source_include_directories': [], 'source_root_path': '/ifs/ATest', 'target_host': '10.**.**.**', 'target_path': '/ifs/ATest'}, 'policy_action': 'sync', 'policy_id': '2ed973731814666a9d258db3a8875b5d', 'policy_name': 'test', 'quotas_deleted': 0, 'regular_files_replicated': 0, 'resynced_lins': 0, 'retransmitted_files': [], 'retry': 1, 'running_chunks': 0, 'service_report': None, 'sockets_replicated': 0, 'source_bytes_recovered': 0, 'source_directories_created': 0, 'source_directories_deleted': 0, 'source_directories_linked': 0, 'source_directories_unlinked': 0, 'source_directories_visited': 0, 'source_files_deleted': 0, 'source_files_linked': 0, 'source_files_unlinked': 0, 'sparse_data_bytes': 0, 'start_time': 1687488892, 'state': 'running', 'succeeded_chunks': 0, 'symlinks_replicated': 0, 'sync_type': 'invalid', 'target_bytes_recovered': 0, 'target_directories_created': 0, 'target_directories_deleted': 0, 'target_directories_linked': 0, 'target_directories_unlinked': 0, 'target_files_deleted': 0, 'target_files_linked': 0, 'target_files_unlinked': 0, 'target_snapshots': [], 'throughput': '0 b/s', 'total_chunks': 0, 'total_data_bytes': 0, 'total_exported_services': None, 'total_files': 0, 'total_network_bytes': 0, 'total_phases': 0, 'unchanged_data_bytes': 0, 'up_to_date_files_skipped': 0, 'updated_files_replicated': 0, 'user_conflict_files_skipped': 0, 'warnings': [], 'workers': [], 'worm_committed_file_conflicts': 0}]})
  The modified SyncIQ job details.


  id (, str, )
    A unique identifier for this object.


  state (, str, )
    The state of the job.






Status
------





Authors
~~~~~~~

- Jennifer John (@johnj9) <ansible.team@dell.com>

