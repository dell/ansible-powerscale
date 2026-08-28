.. _filesystem_module:


filesystem -- Manage Filesystems on PowerScale
==============================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing Filesystems on PowerScale Storage System includes Create a new Filesystem, Delete a Filesystem, Get details of a filesystem, Modify a Filesystem (Quota, ACLs).



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible\-core 2.17 or later.
- Python 3.11, 3.12 or 3.13.



Parameters
----------

  path (True, str, None)
    This is the directory path. It is the absolute path for System access zone and is relative if using a non\-System access zone. For example, if your access zone is 'Ansible' and it has a base path '/ifs/ansible' and the path specified is '/user1', then the effective path would be '/ifs/ansible/user1'. If your access zone is System, and you have 'directory1' in the access zone, the path provided should be '/ifs/directory1'.


  access_zone (optional, str, System)
    The access zone. If no Access Zone is specified, the 'System' access zone would be taken by default.


  owner (optional, dict, None)
    The owner of the Filesystem.

    This parameter is required when creating a Filesystem.

    The following sub\-options are supported for Owner. \- :emphasis:`name(str`\ ), \- :emphasis:`provider\_type(str`\ ).

    If you specify owner, then the corresponding name is mandatory.

    The :emphasis:`provider\_type` is optional and it defaults to :literal:`local`.

    The supported values for :emphasis:`provider\_type` are :literal:`local`\ , :literal:`file`\ , :literal:`ldap` and :literal:`ads`.


  group (optional, dict, None)
    The group of the Filesystem.

    The following sub\-options are supported for Group. \- :emphasis:`name(str`\ ), \- :emphasis:`provider\_type(str`\ ).

    If you specify  a group, then the corresponding name is mandatory.

    The :emphasis:`provider\_type` is optional, it defaults to :literal:`local`.

    The supported values for :emphasis:`provider\_type` are :literal:`local`\ , :literal:`file`\ , :literal:`ldap` and :literal:`ads`.


  access_control (optional, str, None)
    The ACL value for the directory.

    At the time of creation, users can either provide input such as :literal:`private\_read` , :literal:`private` , :literal:`public\_read`\ , :literal:`public\_read\_write`\ , :literal:`public` or in :literal:`POSIX` format (eg 0700).

    Modification of ACL is only supported from :literal:`POSIX` to :literal:`POSIX` mode.

    This field is mutually exclusive with :emphasis:`access\_control\_rights`.


  access_control_rights (optional, raw, None)
    Manage user rights and set ACL permissions for files and directories.

    Accepts a single ACE dict (backward compatible) or a list of ACE dicts for multi\-ACE operations.

    When a single dict is provided, it is automatically wrapped into a single\-element list internally.

    :strong:`API Limitation`\ : The OneFS REST API consolidates multiple ACEs for the same trustee with the same :literal:`access\_type` into a single ACE by unioning :literal:`access\_rights` and :literal:`inherit\_flags`. This means you cannot maintain separate ACEs for the same trustee with the same access\_type but different inheritance flags. To maintain separate ACEs, use different :literal:`access\_type` values (one :literal:`allow` and one :literal:`deny`\ ) or different trustees.

    Multiple ACEs across :strong:`different` trustees are fully supported. A single :literal:`allow` ACE and a single :literal:`deny` ACE for the :strong:`same` trustee are also supported as separate entries.

    When managing multiple ACEs, use :literal:`replace` as the :emphasis:`access\_control\_rights\_state` to perform a declarative whole\-ACL replacement. The :literal:`add` and :literal:`remove` states operate on individual ACEs and may produce ambiguous results with multi\-ACE configurations.


    access_rights (optional, list, None)
      Provides the list of access rights that are defined for the directory.


    access_type (True, str, None)
      Allows or denies access to the directory based on the access rights set for the trustee.


    inherit_flags (optional, list, None)
      Provides the inherit flags set for the directory.

      :literal:`object\_inherit` \- permissions propagate to files within the directory.

      :literal:`container\_inherit` \- permissions propagate to subdirectories.

      :literal:`inherit\_only` \- permissions apply only to child objects, not to the directory itself. Must be combined with :literal:`object\_inherit` or :literal:`container\_inherit`.

      :literal:`no\_prop\_inherit` \- permissions propagate only to immediate children, not to deeper descendants.

      :literal:`inherited\_ace` \- indicates the ACE was inherited from a parent directory (read\-only; set by the system).


    trustee (True, dict, None)
      Provides the trustee (user or group) name and trustee :emphasis:`provider\_type`.


      name (True, str, None)
        Provides the trustee (user or group) name.


      type (optional, str, user)
        Provides the trustee type.


      provider_type (optional, str, local)
        The :emphasis:`provider\_type` is optional and it defaults to :literal:`local`.

        The supported values for :emphasis:`provider\_type` are :literal:`local`\ , :literal:`file`\ , :literal:`ldap` and :literal:`ads`.




  access_control_rights_state (optional, str, None)
    Specifies if the access rights are to be added, deleted, or replaced for the trustee.

    It is required together with :emphasis:`access\_control\_rights`.

    When set to :literal:`replace`\ , the module performs a whole\-ACL replacement using the complete list of ACEs provided. This is the recommended mode for managing ACLs with multiple trustees or allow+deny ACEs for the same trustee.

    The module performs post\-write verification to confirm the API stored the desired state, ensuring accurate :literal:`changed` reporting even when the API consolidates ACEs.


  recursive (optional, bool, True)
    Creates intermediate folders recursively when set to :literal:`true`.


  recursive_force_delete (optional, bool, False)
    Deletes sub files and folders recursively when set to :literal:`true` even if the filesystem is not empty.


  quota (optional, dict, None)
    The Smart Quota for the filesystem. Only directory Quotas are supported.

    The following sub\-options are supported for Quota.


    include_snap_data (optional, bool, False)
      Whether to include the snapshots in the quota or not.


    include_data_protection_overhead (optional, bool, None)
      Whether to include the data protection overheads in the quota or not.

      If not passed during quota creation then quota will be created excluding the overheads.

      This parameter is supported for SDK 8.1.1


    thresholds_on (optional, str, None)
      For SDK 9.1.0 the parameter :emphasis:`include\_overheads` is deprecated and :emphasis:`thresholds\_on` is used.


    advisory_limit_size (optional, int, None)
      The threshold value after which the advisory notification will be sent.


    soft_limit_size (optional, int, None)
      Threshold value after which the soft limit exceeded notification will be sent and the :emphasis:`soft\_grace` period will start.

      Write access will be restricted after the grace period expires.

      Both :emphasis:`soft\_grace\_period` and :emphasis:`soft\_limit\_size` are required to modify soft threshold for the quota.


    hard_limit_size (optional, int, None)
      Threshold value after which a hard limit exceeded notification will be sent.

      Write access will be restricted after the hard limit is exceeded.


    cap_unit (optional, str, None)
      Unit of storage for the hard, soft and advisory limits.

      This parameter is required if any of the hard, soft or advisory limits is specified.


    container (optional, bool, False)
      If :literal:`true`\ , SMB shares using the quota directory see the quota thresholds as share size.


    quota_state (optional, str, None)
      Defines whether the quota should exist or not



  state (True, str, None)
    Defines whether the Filesystem should exist or not.

    A filesystem with NFS exports or SMB shares cannot be deleted.

    Any Quotas on the Filesystem need to be removed before deleting the filesystem.


  list_snapshots (optional, bool, False)
    If set to :literal:`true`\ , the filesystem's snapshots are returned.


  onefs_host (True, str, None)
    IP address or FQDN of the PowerScale cluster.


  port_no (False, str, 8080)
    Port number of the PowerScale cluster.It defaults to 8080 if not specified.


  verify_ssl (True, bool, None)
    boolean variable to specify whether to validate SSL certificate or not.

    :literal:`true` \- indicates that the SSL certificate should be verified.

    :literal:`false` \- indicates that the SSL certificate should not be verified.


  api_user (True, str, None)
    username of the PowerScale cluster.


  api_password (True, str, None)
    the password of the PowerScale cluster.





Notes
-----

.. note::
   - While deleting a filesystem when recursive\_force\_delete is set as :literal:`true` it deletes all sub files and folders recursively. This is :literal:`true` even if the filesystem is not empty.
   - Modification of :emphasis:`inherit\_flags` of filesystem ACL is successful only if :emphasis:`access\_rights` is also specified in the :emphasis:`access\_control\_rights` dictionary.
   - When configuring multiple ACEs for the same trustee, always use :literal:`replace` as the :emphasis:`access\_control\_rights\_state`. The :literal:`add` and :literal:`remove` states may fail with an ambiguous\-match error when the existing ACL already contains multiple ACEs for the same trustee and access type.
   - Troubleshooting \- Non\-existent trustee: If the module fails with a trustee resolution error, verify that the trustee name exists in the specified provider (local, LDAP, or AD). Check the provider\_type setting in the trustee dict matches the actual identity source.
   - Troubleshooting \- ACL reset with empty list: Using :literal:`replace` with an empty :emphasis:`access\_control\_rights` list removes all custom ACEs from the directory. The directory retains its inherited ACEs and default owner/group permissions. This is the expected OneFS behavior.
   - Troubleshooting \- Ambiguous ACE matching: When using the legacy :literal:`add` or :literal:`remove` states on a directory that already has multiple ACEs for the same trustee and access type, the module raises an error because it cannot determine which ACE to modify. Switch to :literal:`replace` state with a complete list of desired ACEs to resolve this.
   - Migration from single\-ACE to multi\-ACE: Existing playbooks using :emphasis:`access\_control\_rights` as a single dict continue to work unchanged. To adopt multi\-ACE, change the parameter value from a dict to a list of dicts, and change :emphasis:`access\_control\_rights\_state` from :literal:`add` to :literal:`replace` for declarative whole\-ACL management. See the migration example in the EXAMPLES section for a before/after comparison.
   - :emphasis:`Check\_mode` is supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create Filesystem with Quota in given access zone
      dellemc.powerscale.filesystem:
        onefs_host: "{{onefs_host}}"
        port_no: "{{powerscaleport}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        path: "<path>"
        access_zone: "{{access_zone}}"
        owner:
          name: 'ansible_user'
          provider_type: 'ldap'
        group:
          name: 'ansible_group'
          provider_type: 'ldap'
          access_control: "{{access_control}}"
        quota:
          include_snap_data: false
          include_data_protection_overhead: false
          advisory_limit_size: 2
          soft_limit_size: 5
          hard_limit_size: 10
          cap_unit: "GB"
          quota_state: "present"
          container: true
          recursive: "{{recursive}}"
        state: "{{state_present}}"

    - name: Create Filesystem in default (system) access zone, without Quota
      dellemc.powerscale.filesystem:
        onefs_host: "{{onefs_host}}"
        port_no: "{{powerscaleport}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        path: "<path>"
        owner:
        name: 'ansible_user'
        provider_type: 'ldap'
        state: "{{state_present}}"

    - name: Get filesystem details
      dellemc.powerscale.filesystem:
        onefs_host: "{{onefs_host}}"
        port_no: "{{powerscaleport}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        access_zone: "{{access_zone}}"
        path: "<path>"
        state: "{{state_present}}"

    - name: Get filesystem details with snapshots
      dellemc.powerscale.filesystem:
        onefs_host: "{{onefs_host}}"
        port_no: "{{powerscaleport}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        access_zone: "{{access_zone}}"
        path: "<path>"
        list_snapshots: "{{list_snapshots_true}}"
        state: "{{state_present}}"

    - name: Modify Filesystem Hard Quota
      dellemc.powerscale.filesystem:
        onefs_host: "{{onefs_host}}"
        port_no: "{{powerscaleport}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        path: "<path>"
        access_zone: "{{access_zone}}"
        quota:
        hard_limit_size: 15
        cap_unit: "GB"
        quota_state: "present"
        container: true
        state: "{{state_present}}"

    - name: Modify Filesystem Owner, Group and ACL
      dellemc.powerscale.filesystem:
        onefs_host: "{{onefs_host}}"
        port_no: "{{powerscaleport}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        path: "<path>"
        access_zone: "{{access_zone}}"
        owner:
          name: 'ansible_user'
          provider_type: 'ldap'
        group:
          name: 'ansible_group'
          provider_type: 'ldap'
          access_control: "{{new_access_control}}"
        state: "{{state_present}}"

    - name: Modify Filesystem to add access control rights
      dellemc.powerscale.filesystem:
        onefs_host: "{{onefs_host}}"
        port_no: "{{powerscaleport}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        path: "/ifs/test"
        access_zone: "{{access_zone}}"
        access_control_rights:
        access_type: "allow"
        access_rights:
          - dir_gen_all
        inherit_flags:
          - container_inherit
        trustee:
          name: test_user
          provider_type: "ldap"
        access_control_rights_state: "add"
        state: "present"

    - name: Modify Filesystem to remove access control rights
      dellemc.powerscale.filesystem:
        onefs_host: "{{onefs_host}}"
        port_no: "{{powerscaleport}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        path: "/ifs/test"
        access_zone: "{{access_zone}}"
        access_control_rights:
        access_type: "allow"
        access_rights:
          - dir_gen_all
        inherit_flags:
          - container_inherit
        trustee:
          name: test_user
          provider_type: "ldap"
        access_control_rights_state: "remove"
        state: "present"

    - name: Remove Quota from FS
      dellemc.powerscale.filesystem:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        path: "<path>"
        access_zone: "{{access_zone}}"
        quota:
          quota_state: "absent"
        state: "{{state_present}}"

    - name: Create Filesystem with access control rights for everyone
      dellemc.powerscale.filesystem:
        onefs_host: "{{onefs_host}}"
        port_no: "{{powerscaleport}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        path: "/ifs/test"
        access_zone: "{{access_zone}}"
        access_control_rights:
        access_type: "allow"
        access_rights:
          - dir_gen_all
        inherit_flags:
          - container_inherit
        trustee:
          name: "everyone"
          type: "wellknown"
        access_control_rights_state: "add"
        state: "present"

    - name: Set multiple ACEs for different trustees with inheritance flags
      dellemc.powerscale.filesystem:
        onefs_host: "{{onefs_host}}"
        port_no: "{{powerscaleport}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        path: "/ifs/test"
        access_zone: "{{access_zone}}"
        access_control_rights:
          - access_type: "allow"
            access_rights:
              - dir_gen_all
            inherit_flags:
              - object_inherit
              - container_inherit
            trustee:
              name: admin_user
              provider_type: "ldap"
          - access_type: "allow"
            access_rights:
              - dir_gen_read
            inherit_flags:
              - container_inherit
            trustee:
              name: read_user
              provider_type: "ldap"
        access_control_rights_state: "replace"
        state: "present"

    - name: Set allow and deny ACEs for the same trustee (supported pattern)
      dellemc.powerscale.filesystem:
        onefs_host: "{{onefs_host}}"
        port_no: "{{powerscaleport}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        path: "/ifs/test"
        access_zone: "{{access_zone}}"
        access_control_rights:
          # Deny delete rights (evaluated first in canonical order)
          - access_type: "deny"
            access_rights:
              - std_delete
            inherit_flags:
              - object_inherit
              - container_inherit
            trustee:
              name: test_user
              provider_type: "ldap"
          # Allow read/traverse rights
          - access_type: "allow"
            access_rights:
              - dir_gen_read
            inherit_flags:
              - object_inherit
              - container_inherit
            trustee:
              name: test_user
              provider_type: "ldap"
        access_control_rights_state: "replace"
        state: "present"

    - name: Replace ACL with single trustee and full inheritance
      dellemc.powerscale.filesystem:
        onefs_host: "{{onefs_host}}"
        port_no: "{{powerscaleport}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        path: "/ifs/test"
        access_zone: "{{access_zone}}"
        access_control_rights:
          - access_type: "allow"
            access_rights:
              - dir_gen_all
            inherit_flags:
              - object_inherit
              - container_inherit
            trustee:
              name: test_user
              provider_type: "ldap"
        access_control_rights_state: "replace"
        state: "present"

    - name: Replace ACL with container_inherit and inherit_only (subfolders only)
      dellemc.powerscale.filesystem:
        onefs_host: "{{onefs_host}}"
        port_no: "{{powerscaleport}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        path: "/ifs/test"
        access_zone: "{{access_zone}}"
        access_control_rights:
          - access_type: "allow"
            access_rights:
              - dir_gen_all
            inherit_flags:
              - container_inherit
              - inherit_only
            trustee:
              name: test_user
              provider_type: "ldap"
        access_control_rights_state: "replace"
        state: "present"

    - name: Multi-trustee ACL with mixed inheritance patterns
      dellemc.powerscale.filesystem:
        onefs_host: "{{onefs_host}}"
        port_no: "{{powerscaleport}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        path: "/ifs/test"
        access_zone: "{{access_zone}}"
        access_control_rights:
          - access_type: "allow"
            access_rights:
              - dir_gen_all
            inherit_flags:
              - object_inherit
              - container_inherit
            trustee:
              name: admin_user
              provider_type: "ldap"
          - access_type: "allow"
            access_rights:
              - dir_gen_read
            inherit_flags:
              - container_inherit
              - inherit_only
            trustee:
              name: read_user
              provider_type: "ldap"
          - access_type: "allow"
            access_rights:
              - dir_gen_read
            inherit_flags:
              - object_inherit
              - no_prop_inherit
            trustee:
              name: file_reader
              provider_type: "ldap"
        access_control_rights_state: "replace"
        state: "present"

    - name: Remove a trustee ACE using remove state
      dellemc.powerscale.filesystem:
        onefs_host: "{{onefs_host}}"
        port_no: "{{powerscaleport}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        path: "/ifs/test"
        access_zone: "{{access_zone}}"
        access_control_rights:
          access_type: "allow"
          trustee:
            name: read_user
            provider_type: "ldap"
        access_control_rights_state: "remove"
        state: "present"

    - name: Migration example - single dict to list format
      dellemc.powerscale.filesystem:
        onefs_host: "{{onefs_host}}"
        port_no: "{{powerscaleport}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        path: "/ifs/test"
        access_zone: "{{access_zone}}"
        # Before (still supported): access_control_rights as a single dict
        # access_control_rights:
        #   access_type: "allow"
        #   access_rights:
        #     - dir_gen_all
        #   inherit_flags:
        #     - container_inherit
        #   trustee:
        #     name: test_user
        #     provider_type: "ldap"
        # access_control_rights_state: "add"
        # After: access_control_rights as a list with replace for declarative ACL
        access_control_rights:
          - access_type: "allow"
            access_rights:
              - dir_gen_all
            inherit_flags:
              - container_inherit
            trustee:
              name: test_user
              provider_type: "ldap"
        access_control_rights_state: "replace"
        state: "present"

    - name: Delete filesystem
      dellemc.powerscale.filesystem:
        onefs_host: "{{onefs_host}}"
        port_no: "{{powerscaleport}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{user}}"
        api_password: "{{api_password}}"
        access_zone: "{{access_zone}}"
        path: "<path>"
        recursive_force_delete: "{{recursive_force_delete}}"
        state: "{{state_absent}}"



Return Values
-------------

changed (always, bool, true)
  Whether or not the resource has changed.


diff (When I(diff=true) and ACL changes are detected., complex, {'before': {'acl': [{'trustee': {'id': 'UID:2000', 'name': 'user', 'type': 'user'}, 'access_type': 'allow', 'access_rights': ['dir_gen_read'], 'inherit_flags': []}]}, 'after': {'acl': [{'trustee': {'id': 'UID:2000', 'name': 'user', 'type': 'user'}, 'access_type': 'allow', 'access_rights': ['dir_gen_all'], 'inherit_flags': ['container_inherit']}]}})
  Before and after ACL state when running in diff mode.


  before (, dict, )
    The ACL before the change.


    acl (, list, )
      The list of ACEs before the change.



  after (, dict, )
    The ACL after the change.


    acl (, list, )
      The list of ACEs after the change.




filesystem_details (When Filesystem exists., complex, {'attrs': [{'name': 'owner', 'namespace': None, 'value': 'user'}, {'name': 'group', 'namespace': None, 'value': 'group'}, {'name': 'mode', 'namespace': None, 'value': '0750'}], 'namespace_acl': {'acl': [{'accessrights': ['dir_gen_all'], 'accesstype': 'allow', 'inherit_flags': ['container_inherit'], 'op': 'add', 'trustee': {'id': 'id:2001', 'name': 'user', 'type': 'user'}}], 'action': 'replace', 'authoritative': 'acl', 'group': {'id': '123', 'name': 'group', 'type': 'group'}, 'mode': '0750', 'owner': {'id': '123', 'name': 'user', 'type': 'user'}}})
  The filesystem details.


  attrs (, dict, )
    The attributes of the filesystem.



quota_details (When Quota exists., complex, {'inodes': 1, 'logical': 0, 'physical': 2048})
  The quota details.


  id (, str, 2nQKAAEAAAAAAAAAAAAAQIMCAAAAAAAA)
    The ID of the Quota.


  enforced (, bool, True)
    Whether the Quota is enforced.


  container (, bool, True)
    If (true), SMB shares using the quota directory see the quota thresholds as share size.


  type (, str, directory)
    The type of Quota.


  usage (, dict, )
    The Quota usage.



filesystem_snapshots (When I(list_snapshots) is true., complex, {'alias': None, 'created': 1636393464, 'expires': None, 'has_locks': False, 'id': 4, 'name': 'SIQ-latest', 'path': 'VALUE_SPECIFIED_IN_NO_LOG_PARAMETER', 'pct_filesystem': 2.435778242215747e-06, 'pct_reserve': 0.0, 'schedule': None, 'shadow_bytes': 0, 'size': 4096, 'state': 'active', 'target_id': None, 'target_name': None})
  The filesystem snapshot details.


  created (, int, 1581069354)
    The creation timestamp.


  expires (, int, 2581069354)
    The expiration timestamp.


  name (, str, ansible_snapshot)
    The name of the snapshot.


  path (, str, /ifs/ansible/ansible281825)
    The path of the snapshot.


  id (, int, 1524)
    The id of the snapshot.






Status
------





Authors
~~~~~~~

- Prashant Rakheja (@prashant-dell) <ansible.team@dell.com>
- Trisha Datta (@trisha-dell) <ansible.team@dell.com>
- Kritika Bhateja(@Kritika-Bhateja-03) <ansible.team.dell.com>)

