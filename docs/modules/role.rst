.. _role_module:


role -- Manage Auth Roles on a PowerScale Storage System
========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing Auth Roles on an PowerScale system includes retrieving details of auth role, creating auth role, modifying and deleting auth role.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.16 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  access_zone (optional, str, System)
    Specifies the access zone in which the auth role exists.

    Access zone once set cannot be changed.


  role_name (True, str, None)
    Name of the Auth Role.


  new_role_name (optional, str, None)
    Name of the Auth Role to be used for modify or copy the role.


  description (optional, str, None)
    Specifies the description of the auth role.

    Pass empty string to remove the :emphasis:`description`.


  copy_role (optional, bool, None)
    Copy the role

    :literal:`true` will copy the role from the :emphasis:`role\_name`.


  privileges (optional, list, None)
    Specifies the privileges granted for this role.


    permission (optional, str, None)
      Specifies the permission being allowed for auth role.

      :literal:`+` indicates enabled permission, only for unary permission.

      :literal:`r` indicates read permission.

      :literal:`w` indicates writepermission.

      :literal:`x` indicates execute permission.

      :literal:`-` indicates none permission.


    name (optional, str, None)
      Specifies the name of the permission.


    state (optional, str, present)
      Specifies if the permission is to be added or removed.



  members (optional, list, None)
    Specifies the members of the auth role.


    name (optional, str, None)
      Specifies the name of the member.


    state (optional, str, present)
      Specifies if the member is to be added or removed.


    provider_type (optional, str, local)
      Specifies the provider type of the member.


    type (optional, str, None)
      Specifies the type of the member.



  state (optional, str, present)
    Defines whether the auth role should exist or not.

    Value :literal:`present` indicates that the auth role should exist in system.

    Value :literal:`absent` indicates that the auth role should not exist in system.


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
   - The :emphasis:`check\_mode` is supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create Role
      dellemc.powerscale.role:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        role_name: "Test_Role123sdfsdfsdf"
        description: "Test_Description"
        access_zone: "System"
        privileges:
          - name: "Antivirus"
            permission: "w"
            state: "present"
        members:
          - name: "esa"
            provider_type: "local"
            type: "user"
            state: "present"
          - name: "admin"
            provider_type: "local"
            type: "user"
            state: "present"
        state: "present"

    - name: Get Role
      dellemc.powerscale.role:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        role_name: "Test_Role"
        access_zone: "{{access_zone}}"

    - name: Modify Role
      dellemc.powerscale.role:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        role_name: "Test_Role"
        new_role_name: "Test_Role2"
        description: "Test_Description_Modify"
        access_zone: "System"
        privileges:
          - name: "Antivirus"
            permission: "w"
            state: "absent"
        members:
          - name: "User11_Ansible_Test_SMB"
            type: "user"
            state: "absent"
        state: "present"

    - name: Delete Role
      dellemc.powerscale.role:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        role_name: "Test_Role"
        access_zone: "{{access_zone}}"
        state: "absent"



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


role_details (always, complex, {'description': 'Test_Description', 'id': 'Test_Role2', 'members': [{'id': 'UID:1XXX', 'name': 'admin', 'type': 'user'}, {'id': 'UID:2XXX', 'name': 'esa', 'type': 'user'}], 'name': 'Test_Role2', 'privileges': [{'id': 'ISI_PRIV_ANTIVIRUS', 'name': 'Antivirus', 'permission': 'w'}]})
  The updated auth role details.


  description (, str, )
    Specifies the description of the auth role.


  id (, str, )
    Auth Role ID.


  name (, str, )
    Auth Role name.


  members (, list, )
    Specifies the members of auth role.


    id (, str, )
      ID of the member.


    name (, str, )
      Name of the member.


    type (, str, )
      Specifies the type of the member.



  privileges (, list, )
    Specifies the privileges of auth role.


    id (, str, )
      ID of the privilege.


    name (, str, )
      Name of the privilege.


    permission (, str, )
      Specifies the permission of the privilege.







Status
------





Authors
~~~~~~~

- Meenakshi Dembi (@dembim) <ansible.team@dell.com>

