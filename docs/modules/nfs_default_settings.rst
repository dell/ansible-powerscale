.. _nfs_default_settings_module:


nfs_default_settings -- Manage NFS default settings on a PowerScale Storage System
==================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing NFS default settings on an PowerScale system includes getting details of an NFS default settings and modifying different attributes of the NFS default settings.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.14 or later.
- Python 3.9, 3.10 or 3.11.



Parameters
----------

  map_root (False, dict, None)
    User and group mapping.

    Map incoming root users to a specific user and/or group ID.


    enabled (optional, bool, True)
      Indicates if user mapping is enabled or not.

      True if the user mapping is applied.


    primary_group (False, str, None)
      Specifies name of the primary group.


    secondary_groups (False, list, None)
      Specifies name and state of the secondary groups.


      name (True, str, None)
        Name of the group.


      state (optional, str, present)
        State of the secondary group.



    user (False, str, None)
      Specifies name of the user.



  map_non_root (False, dict, None)
    User and group mapping.

    Map non-root users to a specific user and/or group ID.


    enabled (optional, bool, True)
      Indicates if user mapping is enabled or not.

      True if the user mapping is applied.


    primary_group (False, str, None)
      Specifies name of the primary group.


    secondary_groups (False, list, None)
      Specifies name and state of the secondary groups.


      name (True, str, None)
        Name of the group.


      state (optional, str, present)
        State of the secondary group.



    user (False, str, None)
      Specifies name of the user.



  map_failure (False, dict, None)
    User and group mapping.

    Map users to a specific user and/or group ID after a failed auth attempt.


    enabled (optional, bool, True)
      Indicates if user mapping is enabled or not.

      True if the user mapping is applied.


    primary_group (False, str, None)
      Specifies name of the primary group.


    secondary_groups (False, list, None)
      Specifies name and state of the secondary groups.


      name (True, str, None)
        Name of the group.


      state (optional, str, present)
        State of the secondary group.



    user (False, str, None)
      Specifies name of the user.



  file_name_max_size (False, dict, None)
    Specifies the reported maximum length of a file name.

    This parameter does not affect server behavior, but is included to accommodate legacy client requirements.


    size_value (True, int, None)
      Size value.


    size_unit (True, str, None)
      Unit for the size value.



  block_size (False, dict, None)
    Specifies the block size returned by the NFS statfs procedure.


    size_value (True, int, None)
      Size value.


    size_unit (True, str, None)
      Unit for the size value.



  directory_transfer_size (False, dict, None)
    Specifies the preferred size for directory read operations.

    This value is used to advise the client of optimal settings for the server, but is not enforced.


    size_value (True, int, None)
      Size value.


    size_unit (True, str, None)
      Unit for the size value.



  read_transfer_max_size (False, dict, None)
    Specifies the maximum buffer size that clients should use on NFS read requests.

    This value is used to advise the client of optimal settings for the server, but is not enforced.


    size_value (True, int, None)
      Size value.


    size_unit (True, str, None)
      Unit for the size value.



  read_transfer_multiple (False, dict, None)
    Specifies the preferred multiple size for NFS read requests.

    This value is used to advise the client of optimal settings for the server, but is not enforced.


    size_value (True, int, None)
      Size value.


    size_unit (True, str, None)
      Unit for the size value.



  read_transfer_size (False, dict, None)
    Specifies the preferred size for NFS read requests.

    This value is used to advise the client of optimal settings for the server, but is not enforced.


    size_value (True, int, None)
      Size value.


    size_unit (True, str, None)
      Unit for the size value.



  write_transfer_max_size (False, dict, None)
    Specifies the maximum buffer size that clients should use on NFS write requests.

    This value is used to advise the client of optimal settings for the server, but is not enforced.


    size_value (True, int, None)
      Size value.


    size_unit (True, str, None)
      Unit for the size value.



  write_transfer_multiple (False, dict, None)
    Specifies the preferred multiple size for NFS write requests.

    This value is used to advise the client of optimal settings for the server, but is not enforced.


    size_value (True, int, None)
      Size value.


    size_unit (True, str, None)
      Unit for the size value.



  write_transfer_size (False, dict, None)
    Specifies the preferred multiple size for NFS write requests.

    This value is used to advise the client of optimal settings for the server, but is not enforced.


    size_value (True, int, None)
      Size value.


    size_unit (True, str, None)
      Unit for the size value.



  max_file_size (False, dict, None)
    Specifies the maximum file size for any file accessed from the export.

    This parameter does not affect server behavior, but is included to accommodate legacy client requirements.


    size_value (True, int, None)
      Size value.


    size_unit (True, str, None)
      Unit for the size value.



  security_flavors (False, list, None)
    Specifies the authentication types that are supported for this export.


  commit_asynchronous (False, bool, None)
    True if NFS commit requests execute asynchronously.


  setattr_asynchronous (False, bool, None)
    True if set attribute operations execute asynchronously.


  readdirplus (False, bool, None)
    True if 'readdirplus' requests are enabled.

    Enabling this property might improve network performance and is only available for NFSv3.


  return_32bit_file_ids (False, bool, None)
    Limits the size of file identifiers returned by NFSv3+ to 32-bit values (may require remount).


  can_set_time (False, bool, None)
    True if the client can set file times through the NFS set attribute request.

    This parameter does not affect server behavior, but is included to accommodate legacy client requirements.


  map_lookup_uid (False, bool, None)
    True if incoming user IDs (UIDs) are mapped to users in the OneFS user database.

    When set to False, incoming UIDs are applied directly to file operations.


  symlinks (False, bool, None)
    True if symlinks are supported.

    This value is used to advise the client of optimal settings for the server, but is not enforced.


  write_datasync_action (optional, str, None)
    Specifies the synchronization type for datasync action.


  write_datasync_reply (optional, str, None)
    Specifies the synchronization type for datasync reply.


  write_filesync_action (optional, str, None)
    Specifies the synchronization type for filesync action.


  write_filesync_reply (optional, str, None)
    Specifies the synchronization type for filesync reply.


  write_unstable_action (optional, str, None)
    Specifies the synchronization type for unstable action.


  write_unstable_reply (optional, str, None)
    Specifies the synchronization type for unstable reply.


  encoding (optional, str, None)
    Specifies the default character set encoding of the clients connecting to the export, unless otherwise specified.


  time_delta (False, dict, None)
    Specifies the resolution of all time values that are returned to the clients.


    time_value (True, float, None)
      Time value.


    time_unit (True, str, None)
      Unit for the time value.



  access_zone (optional, str, System)
    The zone to which the NFS default settings apply.


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

    
    - name: Get NFS default settings
      dellemc.powerscale.nfs_default_settings:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        access_zone: "sample-zone"

    - name: Update the NFS default settings
      dellemc.powerscale.nfs_default_settings:
        onefs_host: "{{ onefs_host }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        access_zone: "sample-zone"
        block_size:
          size_value: 5
          size_unit: 'KB'
        commit_asynchronous: false
        encoding: 'UTF8'
        map_root:
          enabled: true
          primary_group: 'test_group_1'
          secondary_groups:
            - name: 'test_group_2'
            - name: 'test_group_3'
              state: 'absent'
          user: 'test_user'
        map_non_root:
          enabled: true
          primary_group: 'test_non_root_group'
          secondary_groups:
            - name: 'test_non_root_group_2'
            - name: 'test_non_root_group_3'
              state: 'absent'
          user: 'test_non_root_user'
        readdirplus: true
        time_delta:
          time_value: 5
          time_unit: 'seconds'
        write_filesync_action: 'DATASYNC'
        security_flavors:
          - unix
          - kerberos



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


nfs_default_settings (always, dict, {'map_root': {'enabled': True, 'primary_group': {'id': 'None', 'name': 'None', 'type': 'None'}, 'secondary_groups': [], 'user': {'id': 'USER:nobody', 'name': 'None', 'type': 'None'}}, 'map_non_root': {'enabled': False, 'primary_group': {'id': 'None', 'name': 'None', 'type': 'None'}, 'secondary_groups': [], 'user': {'id': 'USER:nobody', 'name': 'None', 'type': 'None'}}, 'map_failure': {'enabled': False, 'primary_group': {'id': 'None', 'name': 'None', 'type': 'None'}, 'secondary_groups': [], 'user': {'id': 'USER:nobody', 'name': 'None', 'type': 'None'}}, 'name_max_size': 255, 'block_size': 8192, 'commit_asynchronous': False, 'directory_transfer_size': 131072, 'read_transfer_max_size': 1048576, 'read_transfer_multiple': 512, 'read_transfer_size': 131072, 'setattr_asynchronous': False, 'write_datasync_action': 'DATASYNC', 'write_datasync_reply': 'DATASYNC', 'write_filesync_action': 'FILESYNC', 'write_filesync_reply': 'FILESYNC', 'write_transfer_max_size': 1048576, 'write_transfer_multiple': 512, 'write_transfer_size': 524288, 'write_unstable_action': 'UNSTABLE', 'write_unstable_reply': 'UNSTABLE', 'max_file_size': 9223372036854775807, 'readdirplus': True, 'return_32bit_file_ids': False, 'can_set_time': True, 'encoding': 'DEFAULT', 'map_lookup_uid': False, 'symlinks': True, 'time_delta': '1e-09', 'zone': 'sample-zone'})
  The NFS default settings.


  map_root (, dict, )
    Mapping of incoming root users to a specific user and/or group ID.


  map_non_root (, dict, )
    Mapping of non-root users to a specific user and/or group ID.


  map_failure (, dict, )
    Mapping of users to a specific user and/or group ID after a failed auth attempt.


  name_max_size (, dict, )
    Specifies the reported maximum length of a file name. This parameter does not affect server behavior, but is included to accommodate legacy client requirements.


  block_size (, dict, )
    Specifies the block size returned by the NFS statfs procedure.


  directory_transfer_size (, dict, )
    Specifies the preferred size for directory read operations. This value is used to advise the client of optimal settings for the server, but is not enforced.


  read_transfer_max_size (, dict, )
    Specifies the maximum buffer size that clients should use on NFS read requests. This value is used to advise the client of optimal settings for the server, but is not enforced.


  read_transfer_multiple (, dict, )
    Specifies the preferred multiple size for NFS read requests. This value is used to advise the client of optimal settings for the server, but is not enforced.


  read_transfer_size (, dict, )
    Specifies the preferred size for NFS read requests. This value is used to advise the client of optimal settings for the server, but is not enforced.


  write_transfer_max_size (, dict, )
    Specifies the maximum buffer size that clients should use on NFS write requests. This value is used to advise the client of optimal settings for the server, but is not enforced.


  write_transfer_multiple (, dict, )
    Specifies the preferred multiple size for NFS write requests. This value is used to advise the client of optimal settings for the server, but is not enforced.


  write_transfer_size (, dict, )
    Specifies the preferred multiple size for NFS write requests. This value is used to advise the client of optimal settings for the server, but is not enforced.


  max_file_size (, dict, )
    Specifies the maximum file size for any file accessed from the export. This parameter does not affect server behavior, but is included to accommodate legacy client requirements.


  security_flavors (, list, )
    Specifies the authentication types that are supported for this export.


  commit_asynchronous (, bool, )
    True if NFS commit requests execute asynchronously.


  setattr_asynchronous (, bool, )
    True if set attribute operations execute asynchronously.


  readdirplus (, bool, )
    True if 'readdirplus' requests are enabled. Enabling this property might improve network performance and is only available for NFSv3.


  return_32bit_file_ids (, bool, )
    Limits the size of file identifiers returned by NFSv3+ to 32-bit values (may require remount).


  can_set_time (, bool, )
    True if the client can set file times through the NFS set attribute request. This parameter does not affect server behavior, but is included to accommodate legacy client requirements.


  map_lookup_uid (, bool, )
    True if incoming user IDs (UIDs) are mapped to users in the OneFS user database. When set to False, incoming UIDs are applied directly to file operations.


  symlinks (, bool, )
    True if symlinks are supported. This value is used to advise the client of optimal settings for the server, but is not enforced.


  write_datasync_action (, str, )
    Specifies the synchronization type for data sync action.


  write_datasync_reply (, str, )
    Specifies the synchronization type for data sync reply.


  write_filesync_action (, str, )
    Specifies the synchronization type for file sync action.


  write_filesync_reply (, str, )
    Specifies the synchronization type for file sync reply.


  write_unstable_action (, str, )
    Specifies the synchronization type for unstable action.


  write_unstable_reply (, str, )
    Specifies the synchronization type for unstable reply.


  encoding (, str, )
    Specifies the default character set encoding of the clients connecting to the export, unless otherwise specified.


  time_delta (, dict, )
    Specifies the resolution of all time values that are returned to the clients.


  zone (, str, )
    The zone to which the NFS default settings apply.






Status
------





Authors
~~~~~~~

- Ananthu S Kuttattu(@kuttattz) <ansible.team@dell.com>

