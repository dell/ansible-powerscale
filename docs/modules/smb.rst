.. _smb_module:


smb -- Manage SMB shares on PowerScale Storage System
=====================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing SMB share on PowerScale which includes.

Create a new SMB share.

Modify an existing SMB share.

Get details of an existing SMB share.

Delete an existing SMB share.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.14 or later.
- Python 3.9, 3.10 or 3.11.



Parameters
----------

  share_name (True, str, None)
    The name of the SMB share.


  path (optional, str, None)
    The path of the SMB share. This parameter will be mandatory only for the create operation. This is the absolute path for System Access Zone and the relative path for non-System Access Zone.


  access_zone (optional, str, System)
    Access zone which contains this share. If not specified it will be considered as a System Access Zone.

    For a non-System Access Zone the effective path where the SMB is created will be determined by the base path of the Access Zone and the path provided by the user in the playbook.

    For a System Access Zone the effective path will be the absolute path provided by the user in the playbook.


  new_share_name (optional, str, None)
    The new name of the SMB share.


  description (optional, str, None)
    Description of the SMB share.


  permissions (optional, list, None)
    Specifies permission for specific user, group, or trustee. Valid options read, write, and full.

    This is a list of dictionaries. Each dictionry entry has 3 mandatory values as listed below.

    1)*user_name*/*group_name*/*wellknown* can have actual name of the trustee like ``user``/``group``/``wellknown``.

    2)*permission* can be ``read``/'``write``/``full``.

    3)*permission_type* can be ``allow``/``deny``.

    The fourth entry *provider_type* is optional (default is ``local``).

    4)*provider_type* can be ``local``/``file``/``ads``/``ldap``/``nis``.


  access_based_enumeration (optional, bool, None)
    Only enumerates files and folders for the requesting user has access to.


  access_based_enumeration_root_only (optional, bool, None)
    Access-based enumeration on only the root directory of the share.


  browsable (optional, bool, None)
    Share is visible in net view and the browse list.


  ntfs_acl_support (optional, bool, None)
    Support NTFS ACLs on files and directories.


  directory_create_mask (optional, str, None)
    Directory creates mask bits. Octal value for owner, group, and others against read, write, and execute.


  directory_create_mode (optional, str, None)
    Directory creates mode bits. Octal value for owner, group, and others against read, write, and execute.


  file_create_mask (optional, str, None)
    File creates mask bits. Octal value for owner, group, and others against read, write, and execute.


  file_create_mode (optional, str, None)
    File creates mode bits. Octal value for owner, group, and others against read, write, and execute.


  create_path (optional, bool, None)
    Create path if does not exist.


  allow_variable_expansion (optional, bool, None)
    Allow automatic expansion of variables for home directories.


  auto_create_directory (optional, bool, None)
    Automatically create home directories.


  continuously_available (optional, bool, None)
    Specify if persistent opens are allowed on the share.


  file_filter_extension (optional, dict, None)
    Details of file filter extensions.


    extensions (optional, list, None)
      Specifies the list of file extensions.


    type (optional, str, deny)
      Specifies if filter list is for ``deny`` or ``allow``. Default is ``deny``.


    state (optional, str, None)
      State of the file filter extensions.



  file_filtering_enabled (optional, bool, None)
    Enables file filtering on this zone.


  ca_timeout (optional, dict, None)
    Continuosly available timeout for the SMB share.


    value (optional, int, None)
      Persistent open timeout for the share.


    unit (optional, str, seconds)
      Unit of the *ca_timeout*.



  strict_ca_lockout (optional, bool, None)
    Specifies if persistent opens would do strict lockout on the share.


  smb3_encryption_enabled (optional, bool, None)
    Enables SMB3 encryption for the share.


  ca_write_integrity (optional, str, None)
    Specify the level of write-integrity on continuously available shares.


  change_notify (optional, str, None)
    Level of change notification alerts on the share.


  oplocks (optional, bool, None)
    Support oplocks.


  impersonate_guest (optional, str, None)
    Specify the condition in which user access is done as the guest account.


  impersonate_user (optional, str, None)
    User account to be used as guest account.


  host_acls (optional, list, None)
    An ACL expressing which hosts are allowed access. A deny clause must be the final entry.


    name (True, str, None)
      Name of the host ACL.


    access_type (True, str, None)
      The access type of the host ACL.



  run_as_root (optional, list, None)
    Allow account to run as root.


    name (True, str, None)
      Specifies the name of persona.


    type (True, str, None)
      Specifies the type of persona.


    provider_type (optional, str, local)
      Specifies the provider type of persona.

      The supported values for *provider_type* are ``local``, ``file``, ``ldap``, ``nis`` and ``ads``.


    state (optional, str, allow)
      Specifies whether to add or remove the persona.



  allow_delete_readonly (optional, bool, None)
    Allow deletion of read-only files in the share.


  allow_execute_always (optional, bool, None)
    Allow users to execute files they have rigths for.


  inheritable_path_acl (optional, bool, None)
    Set inheritable acl on share path.


  state (True, str, None)
    Defines whether the SMB share should exist or not.


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

    
    - name: Create SMB share for non system access zone
      dellemc.powerscale.smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        path: "<path>"
        access_zone: "{{non_system_access_zone}}"
        run_as_root:
          - name: "sample_user"
            type: "user"
            provider_type: "local"
            state: "present"
          - name: "sample_group"
            type: "group"
            provider_type: "nis"
            state: "present"
        state: "present"

    - name: Create SMB share for system access zone
      dellemc.powerscale.smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        path: "{{system_az_path}}"
        description: "{{description}}"
        create_path: false
        allow_variable_expansion: true
        auto_create_directory: true
        continuously_available: true
        file_filter_extension:
          extensions:
            - "sample_extension_1"
          type: "allow"
          state: "present-in-share"
        file_filtering_enabled: true
        ca_timeout:
          value: 60
          unit: "minutes"
        strict_ca_lockout: true
        smb3_encryption_enabled: true
        ca_write_integrity: "write-read-coherent"
        change_notify: "all"
        oplocks: true
        impersonate_guest: "never"
        impersonate_user: "sample_user"
        host_acls:
          - name: "sample_host_acl_1"
            access_type: "allow"
          - name: "sample_host_acl_2"
            access_type: "deny"
        state: "present"

    - name: Create SMB share for system access zone
      dellemc.powerscale.smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        path: "<system_az_path>"
        description: "{{description}}"
        permissions:
          - user_name: "{{system_az_user}}"
            permission: "full"
            permission_type: "allow"
          - group_name: "{{system_az_group}}"
            permission: "read"
            permission_type: "allow"
          - wellknown: "everyone"
            permission: "read"
            permission_type: "allow"
        state: "present"

    - name: Modify multiple params for an existing  SMB share
      dellemc.powerscale.smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        path: "/ifs"
        allow_variable_expansion: false
        auto_create_directory: false
        file_filter_extension:
          extensions:
            - 'sample_extension_2'
          type: "allow"
          state: "absent-in-share"
        file_filtering_enabled: true
        ca_timeout:
          value: 15
          unit: "minutes"
        strict_ca_lockout: false
        change_notify: "norecurse"
        oplocks: false
        impersonate_guest: "always"
        impersonate_user: "new_user_2"
        host_acls:
          - name: "sample_host_acl_1"
            access_type: "deny"
          - name: "sample_host_acl_2"
            access_type: "allow"
        state: "present"

    - name: Modify user permission for SMB share
      dellemc.powerscale.smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        path: "<system_az_path>"
        description: "{{description}}"
        permissions:
          - user_name: "{{system_az_user}}"
            permission: "full"
            permission_type: "allow"
          - group_name: "{{system_az_group}}"
            permission: "write"
            permission_type: "allow"
          - wellknown: "everyone"
            permission: "write"
            permission_type: "deny"
        run_as_root:
          - name: "ldap_user"
            type: "user"
            provider_type: "ldap"
            state: "absent"
          - name: "weknown_group"
            type: "wellknown"
            provider_type: "local"
            state: "present"
        allow_delete_readonly: true
        allow_execute_always: false
        inheritable_path_acl: true
        state: "present"

    - name: Delete system access zone SMB share
      dellemc.powerscale.smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        state: "absent"

    - name: Get SMB share details
      dellemc.powerscale.smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        state: "present"

    - name: Create SMB share for non system access zone
      dellemc.powerscale.smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        path: "<non_system_az_path>"
        access_zone: "{{non_system_access_zone}}"
        description: "{{description}}"
        permissions:
          - user_name: "{{non_system_az_user}}"
            permission: "full"
            permission_type: "allow"
          - group_name: "{{non_system_az_group}}"
            permission: "read"
            permission_type: "allow"
          - wellknown: "everyone"
            permission: "read"
            permission_type: "allow"
        state: "present"

    - name: Modify description for an non system access zone SMB share
      dellemc.powerscale.smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        access_zone: "{{non_system_access_zone}}"
        description: "new description"
        state: "present"

    - name: Modify name for an existing non system access zone SMB share
      dellemc.powerscale.smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        new_share_name: "{{new_name}}"
        access_zone: "{{non_system_access_zone}}"
        description: "new description"
        state: "present"



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


smb_details (always, complex, {'shares': [{'access_based_enumeration': False, 'access_based_enumeration_root_only': False, 'allow_delete_readonly': False, 'allow_execute_always': False, 'allow_variable_expansion': False, 'auto_create_directory': False, 'browsable': True, 'ca_timeout': 900, 'ca_write_integrity': 'write-read-coherent', 'change_notify': 'norecurse', 'continuously_available': True, 'create_permissions': 'default acl', 'csc_policy': 'manual', 'description': 'smb description updated', 'directory_create_mask': 448, 'directory_create_mask(octal)': '700', 'directory_create_mode': 0, 'directory_create_mode(octal)': '0', 'file_create_mask': 448, 'file_create_mask(octal)': '700', 'file_create_mode': 64, 'file_create_mode(octal)': '100', 'file_filter_extensions': ['sample_extension_1'], 'file_filter_type': 'allow', 'file_filtering_enabled': True, 'hide_dot_files': False, 'host_acl': ['deny: sample_host_acl_1', 'allow: sample_host_acl_2'], 'id': 'test_sample_smb', 'impersonate_guest': 'always', 'impersonate_user': 'new_user_2', 'inheritable_path_acl': False, 'mangle_byte_start': 60672, 'mangle_map': ['0x01-0x1F:-1', '0x22:-1', '0x2A:-1', '0x3A:-1', '0x3C:-1', '0x3E:-1', '0x3F:-1', '0x5C:-1'], 'name': 'test_sample_smb', 'ntfs_acl_support': True, 'oplocks': False, 'path': 'VALUE_SPECIFIED_IN_NO_LOG_PARAMETER', 'permissions': [{'permission': 'read', 'permission_type': 'allow', 'trustee': {'id': 'SID:S-1-1-0', 'name': 'Everyone', 'type': 'wellknown'}}], 'run_as_root': [{'id': 'SID:S-1-1-0', 'name': 'Everyone', 'type': 'wellknown'}, {'id': 'SID:S-1-5-32-545', 'name': 'sample_user', 'type': 'user'}], 'smb3_encryption_enabled': False, 'sparse_file': False, 'strict_ca_lockout': False, 'strict_flush': True, 'strict_locking': False, 'zid': 1}]})
  Details of the SMB Share.


  allow_delete_readonly (, bool, )
    Allow deletion of read-only files in the SMB Share.


  allow_execute_always (, bool, )
    Allow user to execute files they have rights for.


  name (, str, )
    Name of the SMB Share.


  id (, str, )
    Id of the SMB Share.


  description (, str, )
    Description of the SMB Share.


  path (, str, )
    Path of the SMB Share.


  permission (, list, )
    permission on the of the SMB Share for user/group/wellknown/


  file_create_mask (, int, )
    File create mask bit for SMB Share.


  file_create_mode (, int, )
    File create mode bit for SMB Share.


  directory_create_mask (, int, )
    Directory create mask bit for SMB Share.


  directory_create_mode (, int, )
    Directory create mode bit for SMB Share.


  browsable (, bool, )
    Share is visible in net view and the browse list.


  file_create_mask(octal) (, str, )
    File create mask bit for SMB Share in octal format.


  file_create_mode(octal) (, str, )
    File create mode bit for SMB Share in octal format.


  directory_create_mask(octal) (, str, )
    Directory create mask bit for SMB Share in octal format.


  directory_create_mode(octal) (, str, )
    Directory create mode bit for SMB Share in octal format.


  inheritable_path_acl (, bool, )
    Inheritable ACL on share path.


  run_as_root (, list, )
    Allow the account to run as root.


    name (, str, )
      Name of the persona.


    id (, str, )
      Id of the persona.


    type (, str, )
      Type of the persona.







Status
------





Authors
~~~~~~~

- Arindam Datta (@dattaarindam) <ansible.team@dell.com>
- Trisha Datta (@Trisha-Datta) <ansible.team@dell.com>
- Bhavneet Sharma (@Bhavneet-Sharma) <ansible.team@dell.com>

