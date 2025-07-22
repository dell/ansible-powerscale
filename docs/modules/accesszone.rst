.. _accesszone_module:


accesszone -- Manages access zones on PowerScale
================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing access zones on the PowerScale storage system includes getting details of the access zone and modifying the smb and nfs settings.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.17 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  az_name (True, str, None)
    The name of the access zone.


  path (optional, str, None)
    Specifies the access zone base directory path.


  groupnet (optional, str, groupnet0)
    Name of the groupnet for create access zone.


  create_path (optional, bool, None)
    Determines if a path is created when a path does not exist.


  smb (optional, dict, None)
    Specifies the default SMB setting parameters of access zone.


    create_permissions (optional, str, default acl)
      Sets the default source permissions to apply when a file or directory is created.


    directory_create_mask (optional, str, None)
      Specifies the :literal:`UNIX` mask bits (octal) that are removed when a directory is created, restricting permissions.

      Mask bits are applied before mode bits are applied.


    directory_create_mode (optional, str, None)
      Specifies the :literal:`UNIX` mode bits (octal) that are added when a directory is created, enabling permissions.


    file_create_mask (optional, str, None)
      Specifies the :literal:`UNIX` mask bits (octal) that are removed when a file is created, restricting permissions.


    file_create_mode (optional, str, None)
      Specifies the :literal:`UNIX` mode bits (octal) that are added when a file is created, enabling permissions.


    access_based_enumeration (optional, bool, None)
      Allows access based enumeration only on the files and folders that the requesting user can access.


    access_based_enumeration_root_only (optional, bool, None)
      Access-based enumeration on only the root directory of the share.


    ntfs_acl_support (optional, bool, None)
      Allows ACLs to be stored and edited from SMB clients.


    oplocks (optional, bool, None)
      An oplock allows clients to provide performance improvements by using locally-cached information.



  nfs (optional, dict, None)
    Specifies the default NFS setting parameters of access zone.


    commit_asynchronous (optional, bool, None)
      Set to :literal:`true` if NFS commit requests execute asynchronously.


    nfsv4_domain (optional, str, None)
      Specifies the domain or realm through which users and groups are associated.


    nfsv4_allow_numeric_ids (optional, bool, None)
      If :literal:`true`\ , sends owners and groups as UIDs and GIDs when look up fails or if the :emphasis:`nfsv4\_no\_name` property is set to 1.


    nfsv4_no_domain (optional, bool, None)
      If :literal:`true`\ , sends owners and groups without a domain name.


    nfsv4_no_domain_uids (optional, bool, None)
      If :literal:`true`\ , sends UIDs and GIDs without a domain name.


    nfsv4_no_names (optional, bool, None)
      If :literal:`true`\ , sends owners and groups as UIDs and GIDs.



  provider_state (False, str, None)
    Defines whether the auth providers should be added or removed from access zone.

    If :emphasis:`auth\_providers` are given, then :emphasis:`provider\_state` should also be specified.

    :literal:`add` - indicates that the auth providers should be added to the access zone.

    :literal:`remove` - indicates that auth providers should be removed from the access zone.


  auth_providers (optional, list, None)
    Specifies the auth providers which need to be added or removed from access zone.

    If :emphasis:`auth\_providers` are given, then :emphasis:`provider\_state` should also be specified.


    provider_name (True, str, None)
      Specifies the auth provider name which needs to be added or removed from access zone.


    provider_type (True, str, None)
      Specifies the auth provider type which needs to be added or removed from access zone.


    priority (optional, int, None)
      Specifies the order of priority of the auth provider which needs to be added to access zone.

      :literal:`1` denotes the topmost priority.

      If :emphasis:`priority` is not provided, authentication provider will have lowest priority.



  state (True, str, None)
    Defines whether the access zone should exist or not.

    :literal:`present` - indicates that the access zone should exist on the system.

    :literal:`absent` - indicates that the access zone should not exist on the system.


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
   - Built-in System zone cannot be deleted.
   - When access zone is deleted, all associated authentication providers remain available to other zones, the IP addresses are not reassigned to other zones.
   - When access zone is deleted, SMB shares, NFS exports, and HDFS data paths are deleted, the directories and data still exist, and  new shares, exports, or paths can be mapped in another access zone.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get details of access zone including smb and nfs settings
      dellemc.powerscale.accesszone:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        az_name: "{{access zone}}"
        state: "present"

    - name: Modify smb settings of access zone
      dellemc.powerscale.accesszone:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        az_name: "{{access zone}}"
        state: "present"
        smb:
          create_permissions: 'default acl'
          directory_create_mask: '777'
          directory_create_mode: '700'
          file_create_mask: '700'
          file_create_mode: '100'
          access_based_enumeration: true
          access_based_enumeration_root_only: false
          ntfs_acl_support: true
          oplocks: true

    - name: Modify nfs settings of access zone
      dellemc.powerscale.accesszone:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        az_name: "{{access zone}}"
        state: "present"
        nfs:
          commit_asynchronous: false
          nfsv4_allow_numeric_ids: false
          nfsv4_domain: 'localhost'
          nfsv4_no_domain: false
          nfsv4_no_domain_uids: false
          nfsv4_no_names: false

    - name: Modify smb and nfs settings of access zone
      dellemc.powerscale.accesszone:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        az_name: "{{access zone}}"
        state: "present"
        smb:
          create_permissions: 'default acl'
          directory_create_mask: '777'
          directory_create_mode: '700'
          file_create_mask: '700'
          file_create_mode: '100'
          access_based_enumeration: true
          access_based_enumeration_root_only: false
          ntfs_acl_support: true
          oplocks: true
        nfs:
          commit_asynchronous: false
          nfsv4_allow_numeric_ids: false
          nfsv4_domain: 'localhost'
          nfsv4_no_domain: false
          nfsv4_no_domain_uids: false
          nfsv4_no_names: false

    - name: Add Auth Providers to the access zone
      dellemc.powerscale.accesszone:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        az_name: "{{access zone}}"
        provider_state: "add"
        auth_providers:
          - provider_name: "System"
            provider_type: "file"
            priority: 3
          - provider_name: "ldap-prashant"
            provider_type: "ldap"
        state: "present"

    - name: Remove Auth Providers from the  access zone
      dellemc.powerscale.accesszone:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        az_name: "{{access zone}}"
        provider_state: "remove"
        auth_providers:
          - provider_name: "System"
            provider_type: "file"
        state: "present"

    - name: Create New Access Zone
      dellemc.powerscale.accesszone:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        az_name: "{{access zone}}"
        path: "/ifs/test_dir"
        groupnet: "groupnet1"
        create_path: true
        provider_state: "add"
        auth_providers:
          - provider_name: "System"
            provider_type: "file"
        state: "present"

    - name: Delete Access Zone
      dellemc.powerscale.accesszone:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        az_name: "sample_name"
        state: "absent"



Return Values
-------------

changed (always, bool, false)
  Whether or not the resource has changed.


smb_modify_flag (on success, bool, false)
  Whether or not the default SMB settings of access zone has changed.


nfs_modify_flag (on success, bool, false)
  Whether or not the default NFS settings of access zone has changed.


access_zone_modify_flag (on success, bool, false)
  Whether auth providers linked to access zone has changed.


access_zone_details (When access zone exists, complex, {'nfs_settings': {'export_settings': {'all_dirs': False, 'block_size': 8192, 'can_set_time': True, 'case_insensitive': False, 'case_preserving': True, 'chown_restricted': False, 'commit_asynchronous': False, 'directory_transfer_size': 131072, 'encoding': 'DEFAULT', 'link_max': 32767, 'map_all': None, 'map_failure': {'enabled': False, 'primary_group': {'id': None, 'name': None, 'type': None}, 'secondary_groups': [], 'user': {'id': 'USER:nobody', 'name': None, 'type': None}}, 'map_full': True, 'map_lookup_uid': False, 'map_non_root': {'enabled': False, 'primary_group': {'id': None, 'name': None, 'type': None}, 'secondary_groups': [], 'user': {'id': 'USER:nobody', 'name': None, 'type': None}}, 'map_retry': True, 'map_root': {'enabled': True, 'primary_group': {'id': None, 'name': None, 'type': None}, 'secondary_groups': [], 'user': {'id': 'USER:nobody', 'name': None, 'type': None}}, 'max_file_size': 9223372036854775807, 'name_max_size': 255, 'no_truncate': False, 'read_only': False, 'read_transfer_max_size': 1048576, 'read_transfer_multiple': 512, 'read_transfer_size': 131072, 'readdirplus': True, 'readdirplus_prefetch': 10, 'return_32bit_file_ids': False, 'security_flavors': ['unix'], 'setattr_asynchronous': False, 'snapshot': '-', 'symlinks': True, 'time_delta': '1e-09', 'write_datasync_action': 'DATASYNC', 'write_datasync_reply': 'DATASYNC', 'write_filesync_action': 'FILESYNC', 'write_filesync_reply': 'FILESYNC', 'write_transfer_max_size': 1048576, 'write_transfer_multiple': 512, 'write_transfer_size': 524288, 'write_unstable_action': 'UNSTABLE', 'write_unstable_reply': 'UNSTABLE', 'zone': 'System'}, 'zone_settings': {'nfsv4_allow_numeric_ids': True, 'nfsv4_domain': 'localhost', 'nfsv4_no_domain': False, 'nfsv4_no_domain_uids': True, 'nfsv4_no_names': False, 'nfsv4_replace_domain': True, 'zone': None}}, 'smb_settings': {'access_based_enumeration': False, 'access_based_enumeration_root_only': False, 'allow_delete_readonly': False, 'allow_execute_always': False, 'ca_timeout': 120, 'ca_write_integrity': 'write-read-coherent', 'change_notify': 'norecurse', 'continuously_available': None, 'create_permissions': 'default acl', 'csc_policy': None, 'directory_create_mask': 448, 'directory_create_mask(octal)': '700', 'directory_create_mode': 0, 'directory_create_mode(octal)': '0', 'file_create_mask': 448, 'file_create_mask(octal)': '700', 'file_create_mode': 64, 'file_create_mode(octal)': '100', 'file_filter_extensions': [], 'file_filter_type': 'deny', 'file_filtering_enabled': False, 'hide_dot_files': False, 'host_acl': [], 'impersonate_guest': 'never', 'impersonate_user': '', 'ntfs_acl_support': True, 'oplocks': True, 'smb3_encryption_enabled': False, 'sparse_file': False, 'strict_ca_lockout': True, 'strict_flush': True, 'strict_locking': False, 'zone': None}, 'zones': [{'alternate_system_provider': 'lsa-file-provider:System', 'auth_providers': ['lsa-ldap-provider:ansildap'], 'cache_entry_expiry': 14400, 'create_path': None, 'force_overlap': None, 'groupnet': 'groupnet0', 'home_directory_umask': 63, 'id': 'System', 'ifs_restricted': [], 'map_untrusted': '', 'name': 'System', 'negative_cache_entry_expiry': 60, 'netbios_name': '', 'path': '/ifs', 'skeleton_directory': '/usr/share', 'system': True, 'system_provider': 'lsa-file-provider:System', 'user_mapping_rules': ['test_user_13 ++ test_user_15 [user]', 'test_user_14 => test_user []', 'test_user_13 ++ test_user_15 [user]', 'test_user_12 &= test_user_13 []'], 'zone_id': 1}]})
  The access zone details.


  Zones (, list, )
    Specifies the properties of Zone.


    name (, str, )
      Specifies the access zone name.


    auth_providers (, list, )
      Specifies the list of authentication providers available on this access zone.


    ifs_restricted (, list, )
      Specifies a list of users and groups that have read and write access to /ifs.


    zone_id (, int, )
      Specifies the access zone ID on the system.


    groupnet (, str, )
      Groupnet identifier.


    user_mapping_rules (, list, )
      Specifies the current ID mapping rules.


    system_provider (, str, )
      Specifies the system provider for the access zone.


    alternate_system_provider (, str, )
      Specifies an alternate system provider.



  nfs_settings (, complex, )
    NFS settings of access zone


    export_settings (, complex, )
      Default values for NFS exports


      commit_asynchronous (, bool, )
        Set to :literal:`true` if NFS commit requests execute asynchronously



    zone_settings (, complex, )
      NFS server settings for this zone


      nfsv4_domain (, str, )
        Specifies the domain or realm through which users and groups are associated


      nfsv4_allow_numeric_ids (, bool, )
        If :literal:`true`\ , sends owners and groups as UIDs and GIDs when look up fails or if the 'nfsv4\_no\_name' property is set to 1


      nfsv4_no_domain (, bool, )
        If :literal:`true`\ , sends owners and groups without a domain name


      nfsv4_no_domain_uids (, bool, )
        If :literal:`true`\ , sends UIDs and GIDs without a domain name


      nfsv4_no_names (, bool, )
        If :literal:`true`\ , sends owners and groups as UIDs and GIDs




  smb_settings (, complex, )
    SMB settings of access zone


    directory_create_mask(octal) (, str, )
      UNIX mask bits for directory in octal format


    directory_create_mode(octal) (, str, )
      UNIX mode bits for directory in octal format


    file_create_mask(octal) (, str, )
      UNIX mask bits for file in octal format


    file_create_mode(octal) (, str, )
      UNIX mode bits for file in octal format







Status
------





Authors
~~~~~~~

- Akash Shendge (@shenda1) <ansible.team@dell.com>
- Pavan Mudunuri (@Pavan-Mudunuri) <ansible.team@dell.com>
- Trisha Datta (@trisha-dell) <ansible.team@dell.com>

