.. _snapshotschedule_module:


snapshotschedule -- Manage snapshot schedules on PowerScale
===========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

You can perform the following operations.

Managing snapshot schedules on PowerScale.

Create snapshot schedule.

Modify snapshot schedule.

Get details of snapshot schedule.

Delete snapshot schedule.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.17 or later.
- Python 3.11, 3.12 or 3.13.



Parameters
----------

  name (True, str, None)
    The name of the snapshot schedule.


  path (optional, str, None)
    The path on which the snapshot will be taken. This path is relative to the base path of the Access Zone.

    For 'System' access zone, the path is absolute.

    This parameter is required at the time of creation.

    Modification of the path is not allowed through the Ansible module.


  access_zone (optional, str, System)
    The effective path where the snapshot is created will be determined by the base path of the Access Zone and the path provided by the user in the playbook.


  new_name (optional, str, None)
    The new name of the snapshot schedule.


  desired_retention (optional, int, None)
    The number of hours/days for which snapshots created by this snapshot schedule should be retained.

    If retention is not specified at the time of creation, then the snapshots created by the snapshot schedule will be retained forever.

    Minimum retention duration is 2 hours.

    For large durations (beyond days/weeks), PowerScale may round off the retention to a somewhat larger value to match a whole number of days/weeks.


  retention_unit (optional, str, hours)
    The retention unit for the snapshot created by this schedule.


  alias (optional, str, None)
    The alias will point to the latest snapshot created by the snapshot schedule.


  pattern (optional, str, None)
    Pattern expanded with strftime to create snapshot names.

    This parameter is required at the time of creation.


  schedule (optional, str, None)
    The isidate compatible natural language description of the schedule.

    It specifies the frequency of the schedule.

    This parameter is required at the time of creation.


  state (True, str, None)
    Defines whether the snapshot schedule should exist or not.


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

    
    - name: Create snapshot schedule
      dellemc.powerscale.snapshotschedule:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        name: "{{name}}"
        access_zone: '{{access_zone}}'
        path: '<path>'
        alias: "{{alias1}}"
        desired_retention: "{{desired_retention1}}"
        pattern: "{{pattern1}}"
        schedule: "{{schedule1}}"
        state: "{{state_present}}"

    - name: Get details of snapshot schedule
      dellemc.powerscale.snapshotschedule:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        name: "{{name}}"
        state: "{{state_present}}"

    - name: Rename snapshot schedule
      dellemc.powerscale.snapshotschedule:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        name: "{{name}}"
        new_name: "{{new_name}}"
        state: "{{state_present}}"

    - name: Modify alias of snapshot schedule
      dellemc.powerscale.snapshotschedule:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        name: "{{new_name}}"
        alias: "{{alias2}}"
        state: "{{state_present}}"

    - name: Modify pattern of snapshot schedule
      dellemc.powerscale.snapshotschedule:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        name: "{{new_name}}"
        pattern: "{{pattern2}}"
        state: "{{state_present}}"

    - name: Modify schedule of snapshot schedule
      dellemc.powerscale.snapshotschedule:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        name: "{{new_name}}"
        schedule: "{{schedule2}}"
        state: "{{state_present}}"

    - name: Modify retention of snapshot schedule
      dellemc.powerscale.snapshotschedule:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        name: "{{new_name}}"
        desired_retention: 2
        retention_unit: "{{retention_unit_days}}"
        state: "{{state_present}}"

    - name: Delete snapshot schedule
      dellemc.powerscale.snapshotschedule:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        name: "{{new_name}}"
        state: "{{state_absent}}"

    - name: Delete snapshot schedule - Idempotency
      dellemc.powerscale.snapshotschedule:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        name: "{{new_name}}"
        state: "{{state_absent}}"



Return Values
-------------

changed (always, bool, )
  Whether or not the resource has changed.


snapshot_schedule_details (When snapshot schedule exists, complex, {'schedules': [{'alias': None, 'duration': 604800, 'id': 1759, 'name': 'Atest', 'next_run': 1687564800, 'next_snapshot': 'ScheduleName_duration_2023-06-24_00:00', 'path': '/ifs', 'pattern': 'ScheduleName_duration_%Y-%m-%d_%H:%M', 'schedule': 'every 1 days at 12:00 AM'}], 'snapshot_list': {'resume': None, 'snapshots': [], 'total': 0}})
  Details of the snapshot schedule including snapshot details.


  schedules (, complex, )
    Details of snapshot schedule


    duration (, int, )
      Time in seconds added to creation time to construction expiration time


    id (, int, )
      The system ID given to the schedule


    next_run (, int, )
      Unix Epoch time of next snapshot to be created


    next_snapshot (, str, )
      Formatted name of next snapshot to be created



  snapshot_list (, complex, )
    List of snapshots taken by this schedule


    snapshots (, complex, )
      Details of snapshot


      created (, int, )
        The Unix Epoch time the snapshot was created


      expires (, int, )
        The Unix Epoch time the snapshot will expire and be eligible for automatic deletion.


      id (, int, )
        The system ID given to the snapshot.This is useful for tracking the status of delete pending snapshots


      name (, str, )
        The user or system supplied snapshot name. This will be null for snapshots pending delete


      size (, int, )
        The amount of storage in bytes used to store this snapshot



    total (, int, )
      Total number of items available







Status
------





Authors
~~~~~~~

- Akash Shendge (@shenda1) <ansible.team@dell.com>

