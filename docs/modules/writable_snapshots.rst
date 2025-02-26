.. _writable_snapshots_module:


writable_snapshots -- Manage writable snapshots on PowerScale
=============================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

You can perform the following operations.

Managing snapshots on PowerScale.

Create a writable snapshot.

Delete a writable snapshot.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.15 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  writable_snapshots (False, list, None)
    List of writable snapshots details.


    state (optional, str, present)
      The state of the writable snapshot to create or delete.

      :emphasis:`state` is :literal:`present` - To create a writable snapshot.

      :emphasis:`state` is :literal:`absent` - To delete the writable snapshot.


    dst_path (True, path, None)
      The /ifs of the writable snapshot.

      The destination path should be non-existing path and it is absolute path.


    src_snap (False, str, None)
      The source snapshot name or ID.

      This option is required :emphasis:`state` is :literal:`present`.



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
   - The :emphasis:`writable\_snapshots` parameter will follow the order of deleting operations before creating operations.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: To create a writable snapshot using ID
      dellemc.powerscale.writable_snapshots:
        onefs_host: "{{ onefs_host }}"
        verify_ssl: "{{ verify_ssl }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        writable_snapshots:
          - dst_path: "/ifs/test_one"
            src_snap: 2
            state: present
          - dst_path: "/ifs/test_two"
            src_snap: 2
            state: present

    - name: To create a writable snapshot using Name
      dellemc.powerscale.writable_snapshots:
        onefs_host: "{{ onefs_host }}"
        verify_ssl: "{{ verify_ssl }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        writable_snapshots:
          - dst_path: "/ifs/test_one"
            src_snap: "Snapshot: 2024Apr15, 4:40 PM"
            state: present
          - dst_path: "/ifs/test_two"
            src_snap: "Snapshot: 2024Apr15, 4:40 PM"
            state: present

    - name: To delete writable snapshot
      dellemc.powerscale.writable_snapshots:
        onefs_host: "{{ onefs_host }}"
        verify_ssl: "{{ verify_ssl }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        writable_snapshots:
          - dst_path: "/ifs/test_one"
            state: absent
          - dst_path: "/ifs/test_two"
            sstate: absent

    - name: To create and delete writable snapshot
      dellemc.powerscale.writable_snapshots:
        onefs_host: "{{ onefs_host }}"
        verify_ssl: "{{ verify_ssl }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        writable_snapshots:
          - dst_path: "/ifs/test_test"
            src_snap: 2
            state: present
          - dst_path: "/ifs/test_one"
            state: absent



Return Values
-------------

changed (always, bool, True)
  Whether or not the resource has changed.


writable_snapshots_details (When writable snapshot is created., complex, [{'created': 1719895971, 'dst_path': '/ifs/test_test', 'id': 23, 'log_size': 0, 'phys_size': 2048, 'src_id': 2, 'src_path': '/ifs/tfacc_file_system_test', 'src_snap': 'Snapshot: 2024Apr15, 4:40 PM', 'state': 'active'}])
  The writable snapshot details.


  created (, int, 1578514373)
    The creation timestamp.


  dst_path (, str, /ifs/ansible/)
    The directory path of the writable snapshot.


  id (, int, 23)
    The writable snapshot ID.


  log_size (, int, 2048)
    The logical size of the writable snapshot.


  phys_size (, int, 2048)
    The physical size of the writable snapshot.


  src_id (, int, 2)
    the source snapshot ID.


  src_path (, str, /ifs/tfacc_file_system_test)
    The directory path of the source snapshot.


  src_snap (, str, Snapshot: 2024Apr15, 4:40 PM)
    The directory path of the source snapshot.


  state (, str, active)
    The name of the source snapshot.






Status
------





Authors
~~~~~~~

- Kritika Bhateja(@Kritika-Bhateja-03) <ansible.team.dell.com>

