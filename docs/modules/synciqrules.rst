.. _synciqrules_module:


synciqrules -- Manage SyncIQ performance rules on PowerScale Storage System
===========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing SyncIQ performance rules on PowerScale includes create a SyncIQ performance rule, modify a SyncIQ performance rule, get details of a SyncIQ performance rule, delete a SyncIQ performance rule.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.15 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  rule_type (optional, str, None)
    The type of system resource this rule limits.

    This is mandatory parameter while creating/deleting a performance rule.

    This cannot be modified.


  sync_rule_id (optional, str, None)
    This is an auto generated ID at the time of creation of SyncIQ performance rule.

    For get/modify/delete operations *sync_rule_id* is required.

    The ID of a performance rule is not absolute to a particular existing rule configuration. The IDs are auto-sequenced during creation/deletion of a performance rule.


  limit (optional, int, None)
    It tells the amount the specified system resource type is limited by this rule.

    Units are kb/s for bandwidth, files/s for file-count, processing percentage used for cpu, or percentage of maximum available workers.

    This is a mandatory parameter while creating/deleting a performance rule.


  description (optional, str, None)
    User entered description of the performance rule.


  enabled (optional, bool, None)
    Indicates whether the performance rule is currently in effect during its specified interval.

    This mandatory while creating/deleting a performance rule.


  schedule (optional, dict, None)
    A schedule defining when during a week this performance rule is in effect.

    It is mandatory to enter schedule while creating/deleting a performance rule.


    begin (optional, str, None)
      Start time for this schedule, during its specified days.

      It is of the format hh:mm (24 hour format).


    end (optional, str, None)
      End time for this schedule, during its specified days.

      It is of the format hh:mm (24 hour format).


    days_of_week (optional, list, None)
      The days in a week when the performance rule is effective.



  state (True, str, None)
    The state option is used to determine whether the performance rule exists or not.


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
   - Operations performed in parallel from other interfaces apart from playbook cannot guarantee desirable results.
   - The *check_mode* is not supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create SyncIQ performance rule
      dellemc.powerscale.synciqrules:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        description: "Create a rule"
        enabled: true
        schedule:
        begin: "00:00"
        end: "13:30"
        days_of_week:
          - "monday"
          - "tuesday"
          - "sunday"
        rule_type: "cpu"
        limit: "80"
        state: "present"

    - name: Modify SyncIQ performance rule
      dellemc.powerscale.synciqrules:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        sync_rule_id: "cpu-0"
        limit: "85"
        description: "Modify the performance rule"
        state: "present"

    - name: Get SyncIQ performance rule details
      dellemc.powerscale.synciqrules:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        sync_rule_id: "cpu-0"
        state: "present"

    - name: Delete SyncIQ performance rule
      dellemc.powerscale.synciqrules:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        sync_rule_id: "cpu-0"
        enabled: true
        schedule:
        begin: "00:00"
        end: "13:30"
        days_of_week:
          - "monday"
          - "tuesday"
          - "sunday"
        rule_type: "bandwidth"
        limit: "85"
        state: "absent"



Return Values
-------------

changed (always, bool, )
  Whether or not the resource has changed.


sync_rule_details (When SyncIQ performance rule exists, complex, )
  Details of the SyncIQ performance rule.


  description (, str, )
    Description of the performance rule.


  id (, str, )
    ID of the performance rule.


  enabled (, bool, )
    Indicates whether performance rule is enabled


  type (, str, )
    Type of performance rule


  schedule (, str, )
    Duration when performance rule is effective


  limit (, int, )
    Amount the specified system resource type is limited by this rule






Status
------





Authors
~~~~~~~

- Spandita Panigrahi (@panigs7) <ansible.team@dell.com>

