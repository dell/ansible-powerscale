.. _job_policy_module:


job_policy -- Manage job policies on a PowerScale Storage System
================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing job policies on a PowerScale storage system includes creating, modifying, deleting, and retrieving details of job policies.

Job policies define impact schedules that control when and how aggressively background jobs consume system resources.

This module supports check mode and diff mode.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.17 or later.
- Python 3.11, 3.12 or 3.13.



Parameters
----------

  policy_name (optional, str, None)
    The name of the job policy.

    Required when :emphasis:`state` is :literal:`present`.


  policy_id (optional, str, None)
    The unique identifier of the job policy.

    Can be used to identify the policy for get, modify, or delete operations.


  description (optional, str, )
    Description of the job policy.


  intervals (optional, list, None)
    List of interval definitions for the job policy schedule.

    Each interval specifies a time window and its impact level.


    begin (True, str, None)
      The start time of the interval in :literal:`WWWW HH:MM` format (e.g. :literal:`Monday 08:00`).


    end (True, str, None)
      The end time of the interval in :literal:`WWWW HH:MM` format (e.g. :literal:`Monday 17:00`).


    impact (True, str, None)
      The impact level for the interval.

      Valid choices are :literal:`Low`, :literal:`Medium`, :literal:`High`, :literal:`Paused`.



  state (optional, str, present)
    The state of the job policy.

    Value :literal:`present` indicates that the policy should exist on the system.

    Value :literal:`absent` indicates that the policy should not exist on the system.


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
   - System policies cannot be modified or deleted.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create a job policy
      dellemc.powerscale.job_policy:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        policy_name: "custom_low_impact"
        description: "Low impact policy for overnight jobs"
        intervals:
          - begin: "Monday 00:00"
            end: "Monday 06:00"
            impact: "Low"
          - begin: "Monday 06:00"
            end: "Monday 18:00"
            impact: "Paused"
        state: "present"

    - name: Modify a job policy description
      dellemc.powerscale.job_policy:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        policy_name: "custom_low_impact"
        description: "Updated low impact policy"
        state: "present"

    - name: Modify a job policy intervals
      dellemc.powerscale.job_policy:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        policy_name: "custom_low_impact"
        intervals:
          - begin: "Monday 00:00"
            end: "Monday 08:00"
            impact: "Medium"
        state: "present"

    - name: Get job policy details
      dellemc.powerscale.job_policy:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        policy_name: "custom_low_impact"
        state: "present"

    - name: Delete a job policy by name
      dellemc.powerscale.job_policy:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        policy_name: "custom_low_impact"
        state: "absent"

    - name: Delete a job policy by ID
      dellemc.powerscale.job_policy:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        policy_id: "custom_low_impact_id"
        state: "absent"



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


job_policy_details (When job policy exists, dict, {'id': 'custom_low_impact', 'name': 'custom_low_impact', 'description': 'Low impact policy for overnight jobs', 'intervals': [{'begin': 'Monday 00:00', 'end': 'Monday 06:00', 'impact': 'Low'}], 'system': False})
  The job policy details.


  id (, str, )
    The unique identifier of the policy.


  name (, str, )
    The name of the policy.


  description (, str, )
    The description of the policy.


  intervals (, list, )
    The list of intervals for the policy.


    begin (, str, )
      The start time of the interval.


    end (, str, )
      The end time of the interval.


    impact (, str, )
      The impact level.



  system (, bool, )
    Whether this is a system policy.



diff (when diff mode is enabled and changes are made, dict, {'before': {}, 'after': {}})
  The differences between the before and after states.


  before (, dict, )
    The policy state before the operation.


  after (, dict, )
    The policy state after the operation.





Status
------





Authors
~~~~~~~

- Shrinidhi Rao (@ShrinidhiRao15)
