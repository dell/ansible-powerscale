.. _job_report_info_module:


job_report_info -- Retrieve job report information from a PowerScale Storage System
====================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Retrieving job report information from a PowerScale storage system includes listing job reports with various filters such as job type, job ID, event key, time range, and verbosity options.

Supports automatic pagination to retrieve all available reports.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.17 or later.
- Python 3.11, 3.12 or 3.13.



Parameters
----------

  job_type (optional, str, None)
    Filter reports by job type.


  job_id (optional, int, None)
    Filter reports by job ID.


  event_key (optional, str, None)
    Filter reports by event key.


  begin (optional, int, None)
    Filter reports starting from this time (unix epoch seconds).


  end (optional, int, None)
    Filter reports ending at this time (unix epoch seconds).


  last_phase_only (optional, bool, None)
    If true, only return reports for the last phase of each job.


  verbose (optional, bool, None)
    If true, return verbose report details.


  limit (optional, int, None)
    The maximum number of reports to return per API request.


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
   - Pagination is handled automatically. All matching reports are returned.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get all job reports
      dellemc.powerscale.job_report_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"

    - name: Get reports filtered by job type
      dellemc.powerscale.job_report_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        job_type: "SmartPools"

    - name: Get reports filtered by job ID
      dellemc.powerscale.job_report_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        job_id: 42

    - name: Get reports with time range and verbose output
      dellemc.powerscale.job_report_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        begin: 1700000000
        end: 1700002000
        verbose: true

    - name: Get reports for last phase only with limit
      dellemc.powerscale.job_report_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        last_phase_only: true
        limit: 10

    - name: Get reports filtered by event key
      dellemc.powerscale.job_report_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        event_key: "phase_complete"



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


job_reports (always, list, [{'id': 'report_789', 'job_id': 42, 'job_type': 'SmartPools', 'event_key': 'phase_complete', 'phase': '1/3', 'timestamp': 1700001000, 'statistics': {}}])
  List of job report dictionaries.


  id (, str, )
    The unique identifier of the report.


  job_id (, int, )
    The ID of the job this report belongs to.


  job_type (, str, )
    The type of the job.


  event_key (, str, )
    The event key for this report.


  phase (, str, )
    The phase of the job this report describes.


  timestamp (, int, )
    The timestamp of the report in unix epoch seconds.


  statistics (, dict, )
    Statistics associated with the report.



total_reports (always, int, 1)
  The total number of reports returned.





Status
------





Authors
~~~~~~~

- Shrinidhi Rao (@ShrinidhiRao15)
