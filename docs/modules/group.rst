.. _group_module:


group -- Manage Groups on the PowerScale Storage System
=======================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing Groups on the PowerScale Storage System includes create group, delete group,  get group, add users and remove users.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible\-core 2.17 or later.
- Python 3.11, 3.12 or 3.13.



Parameters
----------

  group_name (optional, str, None)
    The name of the group.


  group_id (optional, int, None)
    The :emphasis:`group\_id` is auto generated or can be assigned at the time of creation.

    For all other operations either :emphasis:`group\_name` or :emphasis:`group\_id` is needed.


  access_zone (optional, str, system)
    This option mentions the zone in which a group is created.

    For creation, :emphasis:`access\_zone` acts as an attribute for the group.

    For all other operations :emphasis:`access\_zone` acts as a filter.


  provider_type (optional, str, local)
    This option defines the type of the authentication provider for the group itself.

    Creation, Deletion and Modification is allowed only for local group.

    Details of groups of all provider types can be fetched.

    If the :emphasis:`provider\_type` is :literal:`ads` then the domain name of the Active Directory Server has to be mentioned in the group\_name. The format for the group\_name should be 'DOMAIN\_NAME\\group\_name' or "DOMAIN\_NAME\\\\group\_name".

    This option acts as a filter for all operations except creation.

    When a member in :emphasis:`users` omits its own :literal:`provider\_type`\ , this group\-level provider is used as the default for member resolution.


  state (True, str, None)
    The state option is used to determine whether the group will exist or not.


  users (optional, list, None)
    Either :emphasis:`user\_name` or :emphasis:`user\_id` is needed to add or remove the user from the group.

    Users can be part of multiple groups.

    Each element may optionally include a :literal:`provider\_type` key to add or remove a member from a different authentication provider (cross\-provider membership). This requires OneFS 9.11.0 or later.


    user_name (optional, str, None)
      The name of the user to add or remove.

      Mutually exclusive with :emphasis:`user\_id`.


    user_id (optional, str, None)
      The numeric UID of the user to add or remove.

      Mutually exclusive with :emphasis:`user\_name`.


    provider_type (optional, str, None)
      The authentication provider in which to resolve the user.

      When omitted the group\-level :emphasis:`provider\_type` is used.

      When specified the module validates that the provider is configured in the target :emphasis:`access\_zone` and that the cluster runs OneFS 9.11.0 or later.



  user_state (optional, str, None)
    The :emphasis:`user\_state` option is used to  determine whether the users will exist for a particular group or not.

    It is required when users are added or removed from a group.


  group_members (optional, list, None)
    List of child groups to add to or remove from the group.

    Each entry is a dictionary with a required :literal:`group\_name` key and an optional :literal:`provider\_type` key (defaults to the group\-level :emphasis:`provider\_type`\ ).

    The child group must already exist in the specified authentication provider and access zone.

    Requires :emphasis:`group\_member\_state` to be set.


    group_name (True, str, None)
      The name of the child group to add or remove.


    provider_type (optional, str, local)
      The authentication provider in which to resolve the child group.

      When omitted the group\-level :emphasis:`provider\_type` is used.



  group_member_state (optional, str, None)
    Determines whether the child groups listed in :emphasis:`group\_members` will be added to or removed from the group.

    Required when :emphasis:`group\_members` is specified.


  well_known_sids (optional, list, None)
    List of well\-known security identifiers (SIDs) to add to or remove from the group.

    Each element is a string — either a display name (case\-insensitive) or a SID string (exact match).

    Commonly used well\-known SIDs:

    :literal:`Everyone`           — S\-1\-1\-0

    :literal:`Authenticated Users` — S\-1\-5\-11

    :literal:`Batch`              — S\-1\-5\-3

    :literal:`Creator Owner`      — S\-1\-3\-0

    :literal:`Dialup`             — S\-1\-5\-1

    :literal:`Interactive`        — S\-1\-5\-4

    :literal:`Network`            — S\-1\-5\-2

    :literal:`Service`            — S\-1\-5\-6

    The authoritative list of supported SIDs for a specific cluster can be obtained via :literal:`GET /platform/1/auth/wellknowns`.

    Requires :emphasis:`well\_known\_sid\_state` to be set.


  well_known_sid_state (optional, str, None)
    Determines whether the well\-known SIDs listed in :emphasis:`well\_known\_sids` will be added to or removed from the group.

    Required when :emphasis:`well\_known\_sids` is specified.


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
   - Cross\-provider group membership requires OneFS 9.11.0 or later.
   - Existing playbooks using only :emphasis:`users` and :emphasis:`user\_state` continue to work unchanged. The :emphasis:`group\_members` and :emphasis:`well\_known\_sids` parameters are optional and default to empty when omitted.
   - :strong:`Troubleshooting`
   - If a child group cannot be resolved, verify that the group exists in the specified authentication provider and access zone. The module will fail with an error message identifying the unresolvable group.
   - If a well\-known SID is not recognised, verify the display name or SID string against the cluster's supported list via :literal:`GET /platform/1/auth/wellknowns`. The error message includes the full list of supported display names.
   - Circular membership (group A contains group B which contains group A) is not detected by the module. OneFS may reject or silently ignore such configurations depending on the version.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create a Group
      dellemc.powerscale.group:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        access_zone: "{{access_zone}}"
        provider_type: "{{provider_type}}"
        group_name: "{{group_name}}"
        state: "present"

    - name: Create a Group with group id
      dellemc.powerscale.group:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        access_zone: "{{access_zone}}"
        provider_type: "{{provider_type}}"
        group_name: "Test_group"
        group_id: 7000
        state: "present"

    - name: Create Group with Users
      dellemc.powerscale.group:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        provider_type: "{{provider_type}}"
        access_zone: "{{access_zone}}"
        group_name: "{{group_name}}"
        users:
          - user_name: "{{user_name}}"
          - user_id: "{{user_id}}"
          - user_name: "{{user_name_2}}"
        user_state: "present-in-group"
        state: "present"

    - name: Get Details of the Group using Group Id
      dellemc.powerscale.group:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        provider_type: "{{provider_type}}"
        access_zone: "{{access_zone}}"
        group_id: "{{group_id}}"
        state: "present"

    - name: Delete the Group using Group Name
      dellemc.powerscale.group:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        provider_type: "{{provider_type}}"
        access_zone: "{{access_zone}}"
        group_name: "{{group_name}}"
        state: "absent"

    - name: Add Users to a Group
      dellemc.powerscale.group:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        provider_type: "{{provider_type}}"
        access_zone: "{{access_zone}}"
        group_id: "{{group_id}}"
        users:
          - user_name: "{{user_name}}"
          - user_id: "{{user_id}}"
          - user_name: "{{user_name_2}}"
        user_state: "present-in-group"
        state: "present"

    - name: Remove Users from a Group
      dellemc.powerscale.group:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        provider_type: "{{provider_type}}"
        access_zone: "{{access_zone}}"
        group_id: "{{group_id}}"
        users:
          - user_name: "{{user_name_1}}"
          - user_id: "{{user_id}}"
          - user_name: "{{user_name_2}}"
        user_state: "absent-in-group"
        state: "present"

    - name: Add an LDAP user to a local group (cross-provider, requires OneFS 9.11+)
      dellemc.powerscale.group:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        provider_type: "local"
        access_zone: "{{access_zone}}"
        group_name: "{{group_name}}"
        users:
          - user_name: "{{ldap_user_name}}"
            provider_type: "ldap"
        user_state: "present-in-group"
        state: "present"

    - name: Add mixed-provider members in a single task
      dellemc.powerscale.group:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        provider_type: "local"
        access_zone: "{{access_zone}}"
        group_name: "{{group_name}}"
        users:
          - user_name: "{{user_name}}"
          - user_name: "{{ldap_user_name}}"
            provider_type: "ldap"
        user_state: "present-in-group"
        state: "present"

    - name: Remove an LDAP user from a local group
      dellemc.powerscale.group:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        provider_type: "local"
        access_zone: "{{access_zone}}"
        group_name: "{{group_name}}"
        users:
          - user_name: "{{ldap_user_name}}"
            provider_type: "ldap"
        user_state: "absent-in-group"
        state: "present"

    - name: Check mode with diff - preview cross-provider membership changes
      dellemc.powerscale.group:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        provider_type: "local"
        access_zone: "{{access_zone}}"
        group_name: "{{group_name}}"
        users:
          - user_name: "{{ldap_user_name}}"
            provider_type: "ldap"
        user_state: "present-in-group"
        state: "present"
      check_mode: true
      diff: true
      register: result

    - name: Backward-compatible legacy usage (no per-member provider_type)
      dellemc.powerscale.group:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        provider_type: "{{provider_type}}"
        access_zone: "{{access_zone}}"
        group_name: "{{group_name}}"
        users:
          - user_name: "{{user_name}}"
          - user_id: "{{user_id}}"
        user_state: "present-in-group"
        state: "present"

    - name: Add an AD group to a local group in an Access Zone
      dellemc.powerscale.group:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        provider_type: "local"
        access_zone: "{{access_zone}}"
        group_name: "{{group_name}}"
        group_members:
          - group_name: "DOMAIN\\ad_child_group"
            provider_type: "ads"
        group_member_state: "present-in-group"
        state: "present"

    - name: Add an LDAP group to a local group
      dellemc.powerscale.group:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        provider_type: "local"
        access_zone: "{{access_zone}}"
        group_name: "{{group_name}}"
        group_members:
          - group_name: "{{ldap_group_name}}"
            provider_type: "ldap"
        group_member_state: "present-in-group"
        state: "present"

    - name: Add a well-known SID by display name
      dellemc.powerscale.group:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        provider_type: "local"
        access_zone: "{{access_zone}}"
        group_name: "{{group_name}}"
        well_known_sids:
          - "Everyone"
        well_known_sid_state: "present-in-group"
        state: "present"

    - name: Add a well-known SID by SID string
      dellemc.powerscale.group:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        provider_type: "local"
        access_zone: "{{access_zone}}"
        group_name: "{{group_name}}"
        well_known_sids:
          - "S-1-1-0"
        well_known_sid_state: "present-in-group"
        state: "present"

    - name: Mixed member type management (users, groups, and SIDs)
      dellemc.powerscale.group:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        provider_type: "local"
        access_zone: "{{access_zone}}"
        group_name: "{{group_name}}"
        users:
          - user_name: "{{user_name}}"
        user_state: "present-in-group"
        group_members:
          - group_name: "{{ldap_group_name}}"
            provider_type: "ldap"
        group_member_state: "present-in-group"
        well_known_sids:
          - "Everyone"
        well_known_sid_state: "present-in-group"
        state: "present"

    - name: Remove group members and well-known SIDs
      dellemc.powerscale.group:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        provider_type: "local"
        access_zone: "{{access_zone}}"
        group_name: "{{group_name}}"
        group_members:
          - group_name: "{{ldap_group_name}}"
            provider_type: "ldap"
        group_member_state: "absent-in-group"
        well_known_sids:
          - "Everyone"
        well_known_sid_state: "absent-in-group"
        state: "present"

    - name: Check/diff mode - preview group and SID membership changes
      dellemc.powerscale.group:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        provider_type: "local"
        access_zone: "{{access_zone}}"
        group_name: "{{group_name}}"
        group_members:
          - group_name: "{{ldap_group_name}}"
            provider_type: "ldap"
        group_member_state: "present-in-group"
        well_known_sids:
          - "Everyone"
        well_known_sid_state: "present-in-group"
        state: "present"
      check_mode: true
      diff: true
      register: result



Return Values
-------------

changed (always, bool, false)
  Whether or not the resource has changed.


group_details (When group exists, complex, {'dn': 'CN=group_11,CN=Groups,DC=VXXXXX-CX', 'dns_domain': None, 'domain': 'VXXXXX-CX', 'generated_gid': False, 'gid': {'id': 'GID:2000', 'name': 'group_11', 'type': 'group'}, 'id': 'group_11', 'member_of': None, 'members': [], 'name': 'group_11', 'object_history': [], 'provider': 'lsa-local-provider:System', 'sam_account_name': 'group_11', 'sid': {'id': 'SID:S-1-0-11-1111111111-1111111111-1111111111-00000', 'name': 'group_11', 'type': 'group'}, 'type': 'group'})
  Details of the group.


  gid (, complex, )
    The details of the primary group for the user.


    id (, str, )
      The id of the group.


    name (, str, )
      The name of the group.


    type_of_resource (, str, group)
      The resource's type is mentioned.



  name (, str, )
    The name of the group.


  provider (, str, lsa-local-provider:system)
    The provider contains the provider type and access zone.


  members (, complex, )
    The list of all members of the group, including users, child groups, and well\-known SIDs. Each entry contains a :literal:`type` field indicating the member kind (\ :literal:`user`\ , :literal:`group`\ , or :literal:`wellknown`\ ).


    sid (, complex, )
      The details of the associated resource.


      id (, str, )
        The unique security identifier of the resource.


      name (, str, )
        The name of the resource.


      type_of_resource (, str, user)
        The resource's type — one of :literal:`user`\ , :literal:`group`\ , or :literal:`wellknown`.





diff (When diff mode is active and membership changes are requested., dict, {'before': {'members': ['Guest', 'ldap_user'], 'group_members': ['child_group'], 'well_known_sids': ['Everyone']}, 'after': {'members': ['Guest'], 'group_members': [], 'well_known_sids': []}})
  The membership diff computed when diff mode is enabled.


  before (, dict, )
    The group membership state before the operation.


    members (, list, )
      Sorted list of user member names before the operation.


    group_members (, list, )
      Sorted list of child group names before the operation.


    well_known_sids (, list, )
      Sorted list of well\-known SID display names before the operation.



  after (, dict, )
    The group membership state after the operation.


    members (, list, )
      Sorted list of user member names after the operation.


    group_members (, list, )
      Sorted list of child group names after the operation.


    well_known_sids (, list, )
      Sorted list of well\-known SID display names after the operation.







Status
------





Authors
~~~~~~~

- P Srinivas Rao (@srinivas-rao5) <ansible.team@dell.com>

