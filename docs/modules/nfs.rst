.. _nfs_module:


nfs -- Manage NFS exports on a PowerScale Storage System
========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing NFS exports on an PowerScale system includes retrieving details of NFS export, creating NFS export in specified access zone, adding or removing clients, modifying and deleting NFS export.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.13 or later.
- Python 3.9, 3.10 or 3.11.



Parameters
----------

  path (True, str, None)
    Specifies the filesystem path. It is the absolute path for System access zone and it is relative if using non-system access zone.

    For example, if your access zone is 'Ansible' and it has a base path '/ifs/ansible' and the path specified is '/user1', then the effective path would be '/ifs/ansible/user1'.

    If your access zone is System, and you have 'directory1' in the access zone, the path provided should be '/ifs/directory1'.

    The directory on the path must exist - the NFS module will not create the directory.

    Ansible module will only support exports with a unique path.

    If there are multiple exports present with the same path, fetching details, creation, modification or deletion of such exports will fail.


  access_zone (optional, str, System)
    Specifies the zone in which the export is valid.

    Access zone once set cannot be changed.


  clients (optional, list, None)
    Specifies the clients to the export. The type of access to clients in this list is determined by the *read_only* parameter.

    This list can be changed anytime during the lifetime of the NFS export.


  root_clients (optional, list, None)
    Specifies the clients with root access to the export.

    This list can be changed anytime during the lifetime of the NFS export.


  read_only_clients (optional, list, None)
    Specifies the clients with read-only access to the export, even when the export is read/write.

    This list can be changed anytime during the lifetime of the NFS export.


  read_write_clients (optional, list, None)
    Specifies the clients with both read and write access to the export, even when the export is set to read-only.

    This list can be changed anytime during the lifetime of the NFS export.


  read_only (optional, bool, None)
    Specifies whether the export is read-only or read-write. This parameter only has effect on the 'clients' list and not the other three types of clients.

    This setting can be modified any time. If it is not set at the time of creation, the export will be of type read/write.


  sub_directories_mountable (optional, bool, None)
    ``true`` if all directories under the specified paths are mountable. If not set, sub-directories will not be mountable.

    This setting can be modified any time.


  description (optional, str, None)
    Optional description field for the NFS export.

    Can be modified by passing a new value.


  state (True, str, None)
    Defines whether the NFS export should exist or not.

    Value ``present`` indicates that the NFS export should exist in system.

    Value ``absent`` indicates that the NFS export should not exist in system.


  client_state (optional, str, None)
    Defines whether the clients can access the NFS export.

    Value ``present-in-export`` indicates that the clients can access the NFS export.

    Value ``absent-in-export`` indicates that the client cannot access the NFS export.

    Required when adding or removing access of clients from the export.

    While removing clients, only the specified clients will be removed from the export, others will remain as is.


  security_flavors (optional, list, None)
    Specifies the authentication types that are supported for this export.


  ignore_unresolvable_hosts (optional, bool, None)
    Does not present an error condition on unresolvable hosts when creating or modifying an export.


  map_root (optional, dict, None)
    Specifies the users and groups to which non-root and root clients are mapped.


    enabled (optional, bool, True)
      True if the user mapping is applied.


    user (optional, str, None)
      Specifies the persona name.


    primary_group (optional, str, None)
      Specifies the primary group name.


    secondary_groups (optional, list, None)
      Specifies the secondary groups.


      name (True, str, None)
        Specifies the group name.


      state (optional, str, present)
        Specifies the group state.




  map_non_root (optional, dict, None)
    Specifies the users and groups to which non-root and root clients are mapped.


    enabled (optional, bool, True)
      True if the user mapping is applied.


    user (optional, str, None)
      Specifies the persona name.


    primary_group (optional, str, None)
      Specifies the primary group name.


    secondary_groups (optional, list, None)
      Specifies the secondary groups.


      name (True, str, None)
        Specifies the group name.


      state (optional, str, present)
        Specifies the group state.




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

    
      - name: Create NFS Export
        dellemc.powerscale.nfs:
          onefs_host: "{{onefs_host}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          path: "<path>"
          access_zone: "{{access_zone}}"
          read_only_clients:
          - "{{client1}}"
          - "{{client2}}"
          read_only: true
          clients: ["{{client3}}"]
          client_state: 'present-in-export'
          state: 'present'

      - name: Get NFS Export
        dellemc.powerscale.nfs:
          onefs_host: "{{onefs_host}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          path: "<path>"
          access_zone: "{{access_zone}}"
          state: 'present'

      - name: Add a root client
        dellemc.powerscale.nfs:
          onefs_host: "{{onefs_host}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          path: "<path>"
          access_zone: "{{access_zone}}"
          root_clients:
          - "{{client4}}"
          client_state: 'present-in-export'
          state: 'present'

      - name: Set sub_directories_mountable flag to true
        dellemc.powerscale.nfs:
          onefs_host: "{{onefs_host}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          path: "<path>"
          access_zone: "{{access_zone}}"
          sub_directories_mountable: true
          state: 'present'

      - name: Remove a root client
        dellemc.powerscale.nfs:
          onefs_host: "{{onefs_host}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          path: "<path>"
          access_zone: "{{access_zone}}"
          root_clients:
          - "{{client4}}"
          client_state: 'absent-in-export'
          state: 'present'

      - name: Modify NFS Export
        dellemc.powerscale.nfs:
          onefs_host: "{{onefs_host}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          path: "<path>"
          access_zone: "{{access_zone}}"
          description: "new description"
          security_flavors:
          - "kerberos_integrity"
          - "kerberos"
          state: 'present'

      - name: Set read_only flag to false
        dellemc.powerscale.nfs:
          onefs_host: "{{onefs_host}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          path: "<path>"
          access_zone: "{{access_zone}}"
          read_only: false
          state: 'present'

      - name: Modify map_root and map_non_root
        dellemc.powerscale.nfs:
          onefs_host: "{{onefs_host}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          path: "<path>"
          access_zone: "{{access_zone}}"
          map_root:
            user: "root"
            primary_group: "root"
            secondary_groups:
              - name: "group_test"
          map_non_root:
            user: "root"
            primary_group: "root"
            secondary_groups:
              - name: "group_test"
                state: "absent"
          state: 'present'

      - name: Disable map_root
        dellemc.powerscale.nfs:
          onefs_host: "{{onefs_host}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          path: "<path>"
          access_zone: "{{access_zone}}"
          map_root:
            enabled: false
          state: 'present'

      - name: Delete NFS Export
        dellemc.powerscale.nfs:
          onefs_host: "{{onefs_host}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          path: "<path>"
          access_zone: "{{access_zone}}"
          state: 'absent'



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


NFS_export_details (always, complex, {'all_dir': 'false', 'block_size': 8192, 'clients': 'None', 'id': 9324, 'read_only_client': ['x.x.x.x'], 'security_flavors': ['unix', 'krb5'], 'zone': 'System', 'map_root': {'enabled': True, 'primary_group': {'id': 'GROUP:group1', 'name': None, 'type': None}, 'secondary_groups': [], 'user': {'id': 'USER:user', 'name': None, 'type': None}}, 'map_non_root': {'enabled': False, 'primary_group': {'id': None, 'name': None, 'type': None}, 'secondary_groups': [], 'user': {'id': 'USER:nobody', 'name': None, 'type': None}}})
  The updated NFS Export details.


  all_dirs (, bool, )
    *sub_directories_mountable* flag value.


  id (, int, 12)
    The ID of the NFS Export, generated by the array.


  paths (, list, ['/ifs/dir/filepath'])
    The filesystem path.


  zone (, str, System)
    Specifies the zone in which the export is valid.


  read_only (, bool, )
    Specifies whether the export is read-only or read-write.


  read_only_clients (, list, ['client_ip', 'client_ip'])
    The list of read only clients for the NFS Export.


  read_write_clients (, list, ['client_ip', 'client_ip'])
    The list of read write clients for the NFS Export.


  root_clients (, list, ['client_ip', 'client_ip'])
    The list of root clients for the NFS Export.


  clients (, list, ['client_ip', 'client_ip'])
    The list of clients for the NFS Export.


  description (, str, )
    Description for the export.


  map_root (, complex, )
    Specifies the users and groups to which non-root and root clients are mapped.


    enabled (, bool, )
      True if the user mapping is applied.


    user (, complex, )
      Specifies the persona name.


      id (, str, )
        Specifies the persona name.



    primary_group (, complex, )
      Specifies the primary group.


      id (, str, )
        Specifies the primary group name.



    secondary_groups (, list, )
      Specifies the secondary groups.



  map_non_root (, complex, )
    Specifies the users and groups to which non-root and root clients are mapped.


    enabled (, bool, )
      True if the user mapping is applied.


    user (, complex, )
      Specifies the persona details.


      id (, str, )
        Specifies the persona name.



    primary_group (, complex, )
      Specifies the primary group details.


      id (, str, )
        Specifies the primary group name.



    secondary_groups (, list, )
      Specifies the secondary groups details.







Status
------





Authors
~~~~~~~

- Manisha Agrawal(@agrawm3) <ansible.team@dell.com>
- Bhavneet Sharma(@Bhavneet-Sharma) <ansible.team@dell.com>
- Trisha Datta(@trisha-dell) <ansible.team@dell.com>

