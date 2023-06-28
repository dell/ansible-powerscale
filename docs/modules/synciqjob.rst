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
- Ansible-core 2.13 or later.
- Python 3.9, 3.10 or 3.11.



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



modified_job (When SyncIQ job is modified, complex, )
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

