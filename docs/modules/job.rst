.. _job_module:


job -- Manage jobs on a PowerScale Storage System
==================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing jobs on a PowerScale storage system includes starting, pausing, resuming, cancelling, and modifying jobs.

This module supports starting a new job by type and controlling an existing job by ID.

This module supports check mode and diff mode.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.17 or later.
- Python 3.11, 3.12 or 3.13.



Parameters
----------

  job_id (optional, int, None)
    The ID of an existing job to control.

    Mutually exclusive with :emphasis:`job\_type`.

    Required if :emphasis:`job\_type` is not specified.


  job_type (optional, str, None)
    The type of job to start (e.g. :literal:`SmartPools`, :literal:`TreeDelete`).

    Mutually exclusive with :emphasis:`job\_id`.

    Required if :emphasis:`job\_id` is not specified.


  job_state (optional, str, None)
    The desired control state of the job.

    :literal:`started` - Start a new job (used with :emphasis:`job\_type`).

    :literal:`paused` - Pause a running job.

    :literal:`running` - Resume a paused job.

    :literal:`cancelled` - Cancel a running or paused job.


  paths (optional, list, None)
    List of filesystem paths for the job.

    Required when starting a new job with :emphasis:`job\_type`.


  priority (optional, int, None)
    The priority of the job. Must be between 1 and 10.


  policy (optional, str, None)
    The impact policy name to associate with the job.


  allow_dup (optional, bool, False)
    Whether to allow starting a duplicate job of the same type.

    If set to :literal:`false` and a running job of the same type exists, the operation is a no-op.


  job_params (optional, dict, None)
    Additional parameters to pass when starting the job.


  wait (optional, bool, False)
    Whether to wait for the job to complete after starting it.


  wait_timeout (optional, int, 300)
    Maximum time in seconds to wait for job completion.


  wait_interval (optional, int, 10)
    Interval in seconds between polling for job status during wait.


  state (optional, str, present)
    The state of the job resource.

    Value :literal:`present` indicates the job should exist or be controlled.


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
   - The :emphasis:`check\_mode` is supported.
   - The :emphasis:`diff` mode is supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Start a SmartPools job
      dellemc.powerscale.job:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        job_type: "SmartPools"
        paths:
          - "/ifs/data"
        priority: 5
        state: "present"

    - name: Start a TreeDelete job and wait for completion
      dellemc.powerscale.job:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        job_type: "TreeDelete"
        paths:
          - "/ifs/data/old_dir"
        wait: true
        wait_timeout: 600
        wait_interval: 15
        state: "present"

    - name: Pause a running job
      dellemc.powerscale.job:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        job_id: 12345
        job_state: "paused"
        state: "present"

    - name: Resume a paused job
      dellemc.powerscale.job:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        job_id: 12345
        job_state: "running"
        state: "present"

    - name: Cancel a running job
      dellemc.powerscale.job:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        job_id: 12345
        job_state: "cancelled"
        state: "present"

    - name: Modify job priority and policy
      dellemc.powerscale.job:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        job_id: 12345
        priority: 3
        policy: "LOW"
        state: "present"



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


job_details (When job exists, dict, {'id': 12345, 'type': 'SmartPools', 'state': 'running', 'priority': 5, 'policy': 'LOW', 'paths': ['/ifs/data'], 'start_time': 1687488892, 'end_time': None})
  The job details.


  id (, int, )
    The unique identifier of the job.


  type (, str, )
    The job type.


  state (, str, )
    The current state of the job.


  priority (, int, )
    The priority of the job.


  policy (, str, )
    The impact policy name.


  paths (, list, )
    The filesystem paths associated with the job.


  start_time (, int, )
    The job start time.


  end_time (, int, )
    The job end time.



outcome (always, str, started)
  The outcome of the operation.


diff (when diff mode is enabled and changes are made, dict, {'before': {}, 'after': {}})
  The differences between the before and after states.


  before (, dict, )
    The job state before the operation.


  after (, dict, )
    The job state after the operation.





Status
------





Authors
~~~~~~~

- Shrinidhi Rao (@ShrinidhiRao15)
