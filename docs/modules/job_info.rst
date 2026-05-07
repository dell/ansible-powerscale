.. _job_info_module:


job_info -- Retrieve job information from a PowerScale Storage System
=====================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Retrieving job information from a PowerScale storage system includes getting details of a specific job, listing jobs with filters, fetching recent jobs, and obtaining job summary statistics.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.17 or later.
- Python 3.11, 3.12 or 3.13.



Parameters
----------

  job_id (optional, int, None)
    The ID of a specific job to retrieve.

    When specified, other filter options are ignored.


  state (optional, list, None)
    Filter jobs by their current state.

    Multiple states can be specified to match any of the given states.

    Valid choices are :literal:`running`, :literal:`paused_user`, :literal:`paused_system`, :literal:`paused_policy`, :literal:`paused_priority`.


  job_type (optional, list, None)
    Filter jobs by their type.

    This is a client-side filter applied after retrieving jobs from the API.

    Multiple types can be specified.


  sort (optional, str, None)
    The field to sort results by.


  dir (optional, str, ASC)
    The sort direction.

    Valid choices are :literal:`ASC`, :literal:`DESC`.


  limit (optional, int, None)
    The maximum number of jobs to return.


  include_recent (optional, bool, False)
    Whether to include recently completed jobs in the response.


  include_summary (optional, bool, False)
    Whether to include job summary statistics in the response.


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
   - This is a read-only info module. It does not modify any resources.
   - The :emphasis:`check\_mode` is supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get a specific job by ID
      dellemc.powerscale.job_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        job_id: 42

    - name: List all jobs
      dellemc.powerscale.job_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"

    - name: List running jobs sorted by ID descending
      dellemc.powerscale.job_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        state:
          - running
        sort: "id"
        dir: "DESC"
        limit: 10

    - name: List jobs filtered by type
      dellemc.powerscale.job_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        job_type:
          - SmartPools

    - name: Get all jobs with recent jobs and summary
      dellemc.powerscale.job_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        include_recent: true
        include_summary: true



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


job_details (always, list, [{'id': 42, 'type': 'SmartPools', 'state': 'running', 'priority': 5, 'policy': 'LOW', 'description': 'SmartPools job', 'start_time': 1687488892, 'end_time': None, 'progress': 50, 'paths': ['/ifs/data']}])
  List of job detail dictionaries.


  id (, int, )
    The unique identifier of the job.


  type (, str, )
    The type of the job.


  state (, str, )
    The current state of the job.


  priority (, int, )
    The priority of the job.


  policy (, str, )
    The scheduling policy of the job.


  description (, str, )
    A description of the job.


  start_time (, int, )
    The start time of the job in unix epoch seconds.


  end_time (, int, )
    The end time of the job in unix epoch seconds.


  progress (, int, )
    The progress percentage of the job.


  paths (, list, )
    The paths associated with the job.



total_jobs (always, int, 1)
  The total number of jobs returned.


recent_jobs (When :emphasis:`include\_recent` is true, list, )
  List of recently completed jobs.


job_summary (When :emphasis:`include\_summary` is true, dict, )
  Summary statistics for jobs.





Status
------





Authors
~~~~~~~

- Shrinidhi Rao (@ShrinidhiRao15)
