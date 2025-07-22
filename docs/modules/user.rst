.. _user_module:


user -- Manage users on the PowerScale Storage System
=====================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing Users on the PowerScale Storage System includes create user, delete user, update user, get user, add role and remove role.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.17 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  user_name (optional, str, None)
    The name of the user account.


  user_id (optional, int, None)
    The :emphasis:`user\_id` is auto generated or can be assigned at the time of creation.

    For all other operations either :emphasis:`user\_name` or :emphasis:`user\_id` is needed.


  password (optional, str, None)
    The password for the user account.

    Required only in the creation of a user account.

    If given in other operations then the password will be ignored.


  access_zone (optional, str, system)
    This option mentions the zone in which a user is created.

    For creation, :emphasis:`access\_zone` acts as an attribute for the user.

    For all other operations :emphasis:`access\_zone` acts as a filter.


  provider_type (optional, str, local)
    This option defines the type which will be used to authenticate the user.

    Creation, Modification and Deletion is allowed for local users.

    Adding and removing roles is allowed for all users of the system access zone.

    Getting user details is allowed for all users.

    If the :emphasis:`provider\_type` is 'ads' then domain name of the Active Directory Server has to be mentioned in the :emphasis:`user\_name`. The format for the :emphasis:`user\_name` should be 'DOMAIN\_NAME\\user\_name' or "DOMAIN\_NAME\\\\user\_name".

    This option acts as a filter for all operations except creation.


  enabled (optional, bool, None)
    Enabled is a bool variable which is used to enable or disable the user account.


  primary_group (optional, str, None)
    A user can be member of multiple groups of which one group has to be assigned as primary group.

    This group will be used for access checks and can also be used when creating files.

    A user can be added to the group using Group Name.


  home_directory (optional, str, None)
    The path specified in this option acts as a home directory for the user.

    The directory which is given should not be already in use.

    For a user in a system access zone, the absolute path has to be given.

    For users in a non-system access zone, the path relative to the non-system Access Zone's base directory has to be given.


  shell (optional, str, None)
    This option is for choosing the type of shell for the user account.


  full_name (optional, str, None)
    The additional information about the user can be provided using full\_name option.


  email (optional, str, None)
    The email id of the user can be added using email option.

    The email id can be set at the time of creation and modified later.


  state (True, str, None)
    The state option is used to mention the existence of the user account.


  role_name (optional, str, None)
    The name of the role which a user will be assigned.

    User can be added to multiple roles.


  role_state (optional, str, None)
    The :emphasis:`role\_state` option is used to mention the existence of the role for a particular user.

    It is required when a role is added or removed from user.


  update_password (optional, str, always)
    This parameter controls the way the :emphasis:`password` is updated during the creation and modification of a user.

    :literal:`always` will update password for each execution.

    :literal:`on\_create` will only set while creating a user.

    For modifying :emphasis:`password`\ , set the :emphasis:`update\_password` to :literal:`always`.


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

    
    - name: Get User Details using user name
      dellemc.powerscale.user:
        onefs_host: "{{onefs_host}}"
        port_no: "{{port_no}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        access_zone: "{{access_zone}}"
        provider_type: "{{provider_type}}"
        user_name: "{{account_name}}"
        state: "present"

    - name: Create User
      dellemc.powerscale.user:
        onefs_host: "{{onefs_host}}"
        port_no: "{{port_no}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        access_zone: "{{access_zone}}"
        provider_type: "{{provider_type}}"
        user_name: "{{account_name}}"
        password: "{{account_password}}"
        primary_group: "{{primary_group}}"
        enabled: "{{enabled}}"
        email: "{{email}}"
        full_name: "{{full_name}}"
        home_directory: "{{home_directory}}"
        shell: "{{shell}}"
        role_name: "{{role_name}}"
        role_state: "present-for-user"
        state: "present"

    - name: Create User with user id
      dellemc.powerscale.user:
        onefs_host: "{{onefs_host}}"
        port_no: "{{port_no}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        access_zone: "{{access_zone}}"
        provider_type: "{{provider_type}}"
        user_name: "Test_User"
        user_id: 7000
        password: "{{account_password}}"
        primary_group: "{{primary_group}}"
        enabled: "{{enabled}}"
        email: "{{email}}"
        full_name: "{{full_name}}"
        home_directory: "{{home_directory}}"
        shell: "{{shell}}"
        role_name: "{{role_name}}"
        role_state: "present-for-user"
        state: "present"

    - name: Update User's Full Name and email using user name
      dellemc.powerscale.user:
        onefs_host: "{{onefs_host}}"
        port_no: "{{port_no}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        access_zone: "{{access_zone}}"
        provider_type: "{{provider_type}}"
        user_name: "{{account_name}}"
        email: "{{new_email}}"
        full_name: "{{full_name}}"
        state: "present"

    - name: Disable User Account using User Id
      dellemc.powerscale.user:
        onefs_host: "{{onefs_host}}"
        port_no: "{{port_no}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        access_zone: "{{access_zone}}"
        provider_type: "{{provider_type}}"
        user_id: "{{id}}"
        enabled: false
        state: "present"

    - name: Add user to a role using Username
      dellemc.powerscale.user:
        onefs_host: "{{onefs_host}}"
        port_no: "{{port_no}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        user_name: "{{account_name}}"
        provider_type: "{{provider_type}}"
        role_name: "{{role_name}}"
        role_state: "present-for-user"
        state: "present"

    - name: Remove user from a role using User id
      dellemc.powerscale.user:
        onefs_host: "{{onefs_host}}"
        port_no: "{{port_no}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        user_id: "{{id}}"
        role_name: "{{role_name}}"
        role_state: "absent-for-user"
        state: "present"

    - name: Delete User using user name
      dellemc.powerscale.user:
        onefs_host: "{{onefs_host}}"
        port_no: "{{port_no}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        access_zone: "{{access_zone}}"
        provider_type: "{{provider_type}}"
        user_name: "{{account_name}}"
        state: "absent"

    - name: Modify password in non-system access zone update_password as "always"
      dellemc.powerscale.user:
        onefs_host: "{{onefs_host}}"
        port_no: "{{port_no}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        access_zone: "{{access_zone}}"
        provider_type: "{{provider_type}}"
        user_name: "{{account_name}}"
        password: "new_password"
        update_password: "always"
        state: "present"



Return Values
-------------

changed (always, bool, )
  Whether or not the resource has changed.


user_details (When user exists, complex, )
  Details of the user.


  email (, str, )
    The email of the user.


  enabled (, bool, )
    Enabled is a bool variable which is used to enable or disable the user account.


  gecos (, str, )
    The full description of the user.


  gid (, complex, )
    The details of the primary group for the user.


    id (, str, )
      The id of the primary group.


    name (, str, )
      The name of the primary group.


    type (, str, )
      The resource's type is mentioned.



  home_directory (, str, )
    The directory path acts as the home directory for the user's account.


  name (, str, )
    The name of the user.


  provider (, str, )
    The provider contains the provider type and access zone.


  roles (For all users in system access zone., list, )
    The list of all the roles of which user is a member.


  shell (, str, )
    The type of shell for the user account.


  uid (, complex, )
    Details about the id and name of the user.


    id (, str, )
      The id of the user.


    name (, str, )
      The name of the user.


    type (, str, )
      The resource's type is mentioned.







Status
------





Authors
~~~~~~~

- P Srinivas Rao (@srinivas-rao5) <ansible.team@dell.com>
- Trisha Datta (@trisha-dell) <ansible.team@dell.com>

