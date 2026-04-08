.. _job_event_info_module:


job_event_info -- Get Job Event information on a PowerScale Storage System
==========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Retrieving information about job events on a PowerScale storage system.

This module supports filtering events by state, time range, job ID, job type, event key, and other criteria.

Supports pagination for large result sets.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.17 or later.
- Python 3.11, 3.12 or 3.13.



Parameters
----------

  state (optional, str, None)
    Filter events by job state.

    Valid choices are :literal:`running`, :literal:`paused_user`, :literal:`paused_system`, :literal:`paused_policy`, :literal:`paused_priority`, :literal:`cancelled_user`, :literal:`cancelled_system`, :literal:`failed`, :literal:`succeeded`, :literal:`unknown`, :literal:`failed_not_retried`.


  begin_time (optional, str, None)
    Filter events that occurred after this time.

    Accepts epoch timestamp (numeric string) or ISO 8601 format.

    Mutually exclusive with :emphasis:`duration`.


  end_time (optional, str, None)
    Filter events that occurred before this time.

    Accepts epoch timestamp (numeric string) or ISO 8601 format.

    Mutually exclusive with :emphasis:`duration`.


  duration (optional, dict, None)
    Filter events within a time window relative to the current time.

    Mutually exclusive with :emphasis:`begin\_time` and :emphasis:`end\_time`.


    value (True, int, None)
      The numeric duration value.


    unit (True, str, None)
      The unit of the duration value.

      Valid choices are :literal:`minutes`, :literal:`hours`, :literal:`days`.



  job_id (optional, int, None)
    Filter events by a specific job ID.


  job_type (optional, str, None)
    Filter events by job type name.


  event_key (optional, str, None)
    Filter events by event key.


  ended_jobs_only (optional, bool, None)
    If set to :literal:`true`, return only events for ended jobs.


  limit (optional, int, None)
    Maximum number of events to return per API call.


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
   - This is a read-only info module and does not make any changes.
   - The :emphasis:`check\_mode` is supported.
   - When :emphasis:`duration` is specified, the module calculates a time window ending at the current time.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get all job events
      dellemc.powerscale.job_event_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"

    - name: Get job events filtered by running state
      dellemc.powerscale.job_event_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        state: "running"

    - name: Get job events within a time range using epoch timestamps
      dellemc.powerscale.job_event_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        begin_time: "1700000000"
        end_time: "1700003000"

    - name: Get job events within a time range using ISO 8601 format
      dellemc.powerscale.job_event_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        begin_time: "2026-01-01T00:00:00Z"

    - name: Get job events from the last 24 hours
      dellemc.powerscale.job_event_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        duration:
          value: 24
          unit: "hours"

    - name: Get job events for a specific job ID
      dellemc.powerscale.job_event_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        job_id: 42

    - name: Get job events filtered by job type
      dellemc.powerscale.job_event_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        job_type: "SmartPools"

    - name: Get events for ended jobs only with limit
      dellemc.powerscale.job_event_info:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        ended_jobs_only: true
        limit: 100



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


job_events (always, list, [{'id': 'event_456', 'job_id': 42, 'job_type': 'SmartPools', 'state': 'running', 'event_key': 'job_started', 'timestamp': 1700000000, 'message': 'Job started successfully'}])
  The list of job event details.


  id (, str, )
    The unique identifier for the event.


  job_id (, int, )
    The ID of the job associated with this event.


  job_type (, str, )
    The type of the job associated with this event.


  state (, str, )
    The state of the job at the time of the event.


  event_key (, str, )
    The event key identifier.


  timestamp (, int, )
    The epoch timestamp when the event occurred.


  message (, str, )
    A human-readable message describing the event.



total_events (always, int, 1)
  The total number of events returned.





Status
------





Authors
~~~~~~~

- Shrinidhi Rao (@shrinidhirao) <ansible.team@dell.com>
