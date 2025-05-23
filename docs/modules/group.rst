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
- Ansible-core 2.16 or later.
- Python 3.10, 3.11 or 3.12.



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
    This option defines the type which will be used to authenticate the group members.

    Creation, Deletion and Modification is allowed only for local group.

    Details of groups of all provider types can be fetched.

    If the :emphasis:`provider\_type` is :literal:`ads` then the domain name of the Active Directory Server has to be mentioned in the group\_name. The format for the group\_name should be 'DOMAIN\_NAME\\group\_name' or "DOMAIN\_NAME\\\\group\_name".

    This option acts as a filter for all operations except creation.


  state (True, str, None)
    The state option is used to determine whether the group will exist or not.


  users (optional, list, None)
    Either :emphasis:`user\_name` or :emphasis:`user\_id` is needed to add or remove the user from the group.

    Users can be part of multiple groups.


  user_state (optional, str, None)
    The :emphasis:`user\_state` option is used to  determine whether the users will exist for a particular group or not.

    It is required when users are added or removed from a group.


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
    The list of sid's the members of group.


    sid (, complex, )
      The details of the associated resource.


      id (, str, )
        The unique security identifier of the resource.


      name (, str, )
        The name of the resource.


      type_of_resource (, str, user)
        The resource's type is mentioned.








Status
------





Authors
~~~~~~~

- P Srinivas Rao (@srinivas-rao5) <ansible.team@dell.com>

