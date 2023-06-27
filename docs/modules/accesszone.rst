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
- Ansible-core 2.13 or later.
- Python 3.9, 3.10 or 3.11.



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
      Specifies the ``UNIX`` mask bits (octal) that are removed when a directory is created, restricting permissions.

      Mask bits are applied before mode bits are applied.


    directory_create_mode (optional, str, None)
      Specifies the ``UNIX`` mode bits (octal) that are added when a directory is created, enabling permissions.


    file_create_mask (optional, str, None)
      Specifies the ``UNIX`` mask bits (octal) that are removed when a file is created, restricting permissions.


    file_create_mode (optional, str, None)
      Specifies the ``UNIX`` mode bits (octal) that are added when a file is created, enabling permissions.


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
      Set to ``true`` if NFS commit requests execute asynchronously.


    nfsv4_domain (optional, str, None)
      Specifies the domain or realm through which users and groups are associated.


    nfsv4_allow_numeric_ids (optional, bool, None)
      If ``true``, sends owners and groups as UIDs and GIDs when look up fails or if the *nfsv4_no_name* property is set to 1.


    nfsv4_no_domain (optional, bool, None)
      If ``true``, sends owners and groups without a domain name.


    nfsv4_no_domain_uids (optional, bool, None)
      If ``true``, sends UIDs and GIDs without a domain name.


    nfsv4_no_names (optional, bool, None)
      If ``true``, sends owners and groups as UIDs and GIDs.



  provider_state (False, str, None)
    Defines whether the auth providers should be added or removed from access zone.

    If *auth_providers* are given, then *provider_state* should also be specified.

    ``add`` - indicates that the auth providers should be added to the access zone.

    ``remove`` - indicates that auth providers should be removed from the access zone.


  auth_providers (optional, list, None)
    Specifies the auth providers which need to be added or removed from access zone.

    If *auth_providers* are given, then *provider_state* should also be specified.


    provider_name (True, str, None)
      Specifies the auth provider name which needs to be added or removed from access zone.


    provider_type (True, str, None)
      Specifies the auth provider type which needs to be added or removed from access zone.



  state (True, str, None)
    Defines whether the access zone should exist or not.

    ``present`` - indicates that the access zone should exist on the system.

    ``absent`` - indicates that the access zone should not exist on the system.


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
   - Deletion of access zone is not allowed through the Ansible module.
   - The *check_mode* is not supported.
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

    - name: Add Auth Providers to the  access zone
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



Return Values
-------------

changed (always, bool, )
  Whether or not the resource has changed.


smb_modify_flag (on success, bool, )
  Whether or not the default SMB settings of access zone has changed.


nfs_modify_flag (on success, bool, )
  Whether or not the default NFS settings of access zone has changed.


access_zone_modify_flag (on success, bool, )
  Whether auth providers linked to access zone has changed.


access_zone_details (When access zone exists, complex, )
  The access zone details.


  nfs_settings (, complex, )
    NFS settings of access zone


    export_settings (, complex, )
      Default values for NFS exports


      commit_asynchronous (, bool, )
        Set to ``true`` if NFS commit requests execute asynchronously



    zone_settings (, complex, )
      NFS server settings for this zone


      nfsv4_domain (, str, )
        Specifies the domain or realm through which users and groups are associated


      nfsv4_allow_numeric_ids (, bool, )
        If ``true``, sends owners and groups as UIDs and GIDs when look up fails or if the 'nfsv4_no_name' property is set to 1


      nfsv4_no_domain (, bool, )
        If ``true``, sends owners and groups without a domain name


      nfsv4_no_domain_uids (, bool, )
        If ``true``, sends UIDs and GIDs without a domain name


      nfsv4_no_names (, bool, )
        If ``true``, sends owners and groups as UIDs and GIDs




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

