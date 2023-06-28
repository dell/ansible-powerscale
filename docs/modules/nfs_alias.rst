.. _nfs_alias_module:


nfs_alias -- Manage NFS aliases on a PowerScale Storage System
==============================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing NFS aliases on an PowerScale system includes creating NFS alias for NFS export, Getting details of an NFS alias, Modifying different attributes of the NFS alias and Deleting an NFS alias.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.13 or later.
- Python 3.9, 3.10 or 3.11.



Parameters
----------

  nfs_alias_name (True, str, None)
    Name of an NFS alias.


  path (False, str, None)
    Specifies the path to which the alias points.

    It is the absolute path for System access zone and it is relative if using non-system access zone.

    If your access zone is System, and you have 'directory1' in the access zone, the path provided should be '/ifs/directory1'.

    The directory on the path must exist, the NFS alias module will not create the directory.


  access_zone (optional, str, System)
    Specifies the zone in which the alias is valid.

    Access zone once set cannot be changed.


  scope (optional, str, effective)
    When specified as ``effective``, or not specified, all fields are returned.

    When specified as ``user``, only fields with non-default values are shown.


  check (optional, bool, False)
    Check for conflicts when viewing alias.


  new_alias_name (optional, str, None)
    New name of the alias.


  state (optional, str, present)
    Defines whether the NFS alias should exist or not.

    ``present`` indicates that the NFS alias should exist in system.

    ``absent`` indicates that the NFS alias should not exist in system.


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
   - The *check_mode* is supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
      - name: Create NFS alias - check mode
        dellemc.powerscale.nfs_alias:
          onefs_host: "{{onefs_host}}"
          verify_ssl: "{{verify_ssl}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          nfs_alias_name: "/sample_alias_2"
          path: "/ifs"
          access_zone: 'System'
          state: "present"
        check_mode: true

      - name: Create NFS alias
        dellemc.powerscale.nfs_alias:
          onefs_host: "{{onefs_host}}"
          verify_ssl: "{{verify_ssl}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          nfs_alias_name: "/sample_alias_2"
          path: "/ifs"
          access_zone: 'System'
          state: "present"

      - name: Get NFS alias by name
        dellemc.powerscale.nfs_alias:
          onefs_host: "{{onefs_host}}"
          verify_ssl: "{{verify_ssl}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          nfs_alias_name: "/sample_alias_2"
          scope: "effective"
          check: true

      - name: Modify NFS alias - check mode
        dellemc.powerscale.nfs_alias:
          onefs_host: "{{onefs_host}}"
          verify_ssl: "{{verify_ssl}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          nfs_alias_name: "/sample_alias_2"
          new_alias_name: "/Renamed_alias_2"
          path: "/ifs/Test"
          state: "present"
        check_mode: true

      - name: Modify NFS alias
        dellemc.powerscale.nfs_alias:
          onefs_host: "{{onefs_host}}"
          verify_ssl: "{{verify_ssl}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          nfs_alias_name: "/sample_alias_2"
          new_alias_name: "/Renamed_alias_2"
          path: "/ifs/Test"
          state: "present"

      - name: Delete NFS alias - check mode
        dellemc.powerscale.nfs_alias:
          onefs_host: "{{onefs_host}}"
          verify_ssl: "{{verify_ssl}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          nfs_alias_name: "/Renamed_alias_2"
          state: "absent"
        check_mode: true

      - name: Delete NFS alias
        dellemc.powerscale.nfs_alias:
          onefs_host: "{{onefs_host}}"
          verify_ssl: "{{verify_ssl}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          nfs_alias_name: "/Renamed_alias_2"
          state: "absent"



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


nfs_alias_details (always, complex, {'aliases': [{'health': 'unknown', 'id': '/test_alias_1', 'name': '/test_alias_1', 'path': '/ifs/Test', 'zone': 'System'}]})
  The NFS alias details.


  health (, str, unknown)
    The health of the NFS alias.


  id (, str, /Sample_alias1)
    The ID of the NFS alias.


  name (, str, /Sample_alias1)
    The name of the NFS alias.


  path (, str, /ifs/dir/filepath)
    The path of the NFS alias.


  zone (, str, System)
    Specifies the zone in which the NFS alias is valid.






Status
------





Authors
~~~~~~~

- Trisha Datta(@Trisha-Datta) <ansible.team@dell.com>

