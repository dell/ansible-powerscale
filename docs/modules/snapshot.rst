.. _snapshot_module:


snapshot -- Manage snapshots on PowerScale
==========================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

You can perform the following operations.

Managing snapshots on PowerScale.

Create a filesystem snapshot.

Modify a filesystem snapshot.

Get details of a filesystem snapshot.

Delete a filesystem snapshot.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.13 or later.
- Python 3.9, 3.10 or 3.11.



Parameters
----------

  snapshot_name (True, str, None)
    The name of the snapshot.


  path (optional, str, None)
    Specifies the filesystem path. It is the absolute path for System access zone and it is relative if using non-System access zone. For example, if your access zone is 'Ansible' and it has a base path '/ifs/ansible' and the path specified is '/user1', then the effective path would be '/ifs/ansible/user1'. If your access zone is System, and you have 'directory1' in the access zone, the path provided should be '/ifs/directory1'.


  access_zone (optional, str, System)
    The effective path where the Snapshot is created will be determined by the base path of the Access Zone and the path provided by the user in the playbook.


  new_snapshot_name (optional, str, None)
    The new name of the snapshot.


  expiration_timestamp (optional, str, None)
    The timestamp on which the snapshot will expire (UTC format).

    Either this or desired retention can be specified, but not both.


  desired_retention (optional, str, None)
    The number of days for which the snapshot can be retained.

    Either this or expiration timestamp can be specified, but not both.


  retention_unit (optional, str, None)
    The retention unit for the snapshot.

    The default value is hours.


  alias (optional, str, None)
    The alias for the snapshot.


  state (True, str, None)
    Defines whether the snapshot should exist or not.


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
   - The *check_mode* is not supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create a filesystem snapshot on PowerScale
      dellemc.powerscale.snapshot:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        path: "<path>"
        access_zone: "{{access_zone}}"
        snapshot_name: "{{snapshot_name}}"
        desired_retention: "{{desired_retention}}"
        retention_unit: "{{retention_unit_days}}"
        alias: "{{ansible_snap_alias}}"
        state: "{{present}}"

    - name: Get details of a filesystem snapshot
      dellemc.powerscale.snapshot:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        snapshot_name: "{{snapshot_name}}"
        state: "{{present}}"

    - name: Modify filesystem snapshot desired retention
      dellemc.powerscale.snapshot:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        snapshot_name: "{{snapshot_name}}"
        desired_retention: "{{desired_retention_new}}"
        retention_unit: "{{retention_unit_days}}"
        state: "{{present}}"

    - name: Modify filesystem snapshot expiration timestamp
      dellemc.powerscale.snapshot:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        snapshot_name: "{{snapshot_name}}"
        expiration_timestamp: "{{expiration_timestamp_new}}"
        state: "{{present}}"

    - name: Modify filesystem snapshot alias
      dellemc.powerscale.snapshot:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        snapshot_name: "{{snapshot_name}}"
        alias: "{{ansible_snap_alias_new}}"
        state: "{{present}}"

    - name: Delete snapshot alias
      dellemc.powerscale.snapshot:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        snapshot_name: "{{snapshot_name}}"
        alias: ""
        state: "{{present}}"

    - name: Rename filesystem snapshot
      dellemc.powerscale.snapshot:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        snapshot_name: "{{snapshot_name}}"
        new_snapshot_name: "{{new_snapshot_name}}"
        state: "{{present}}"

    - name: Delete filesystem snapshot
      dellemc.powerscale.snapshot:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        snapshot_name: "{{new_snapshot_name}}"
        state: "{{absent}}"



Return Values
-------------

changed (always, bool, True)
  Whether or not the resource has changed.


snapshot_details (When snapshot exists., complex, )
  The snapshot details.


  alias (, str, snapshot_alias)
    Snapshot alias.


  created (, int, 1578514373)
    The creation timestamp.


  expires (, int, 1578687172)
    The expiration timestamp.


  has_locks (, bool, False)
    Whether the snapshot has locks.


  id (, int, 230)
    The snapshot ID.


  name (, str, ansible_snapshot)
    The name of the snapshot.


  path (, str, /ifs/ansible/)
    The directory path whose snapshot has been taken.


  pct_filesystem (, float, 2.5)
    The percentage of filesystem used.


  pct_reserve (, float, 0.0)
    The percentage of filesystem reserved.


  size (, int, 4096)
    The snapshot size.


  state (, str, active)
    The state of the snapshot.


  target_id (, int, 10)
    target ID of snapshot whose alias it is.


  target_name (, str, ansible_target_snap)
    target name of snapshot whose alias it is.






Status
------





Authors
~~~~~~~

- Prashant Rakheja (@prashant-dell) <ansible.team@dell.com>

