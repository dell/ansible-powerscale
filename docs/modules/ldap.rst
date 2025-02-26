.. _ldap_module:


ldap -- Manage LDAP authentication provider on PowerScale
=========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing LDAP authentication provider on PowerScale storage system includes creating, modifying, deleting and retrieving details of LDAP provider.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.15 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  ldap_name (True, str, None)
    Specifies the name of the LDAP provider.


  server_uris (optional, list, None)
    Specifies the server URIs.

    This parameter is mandatory during create.

    :emphasis:`server\_uris` should begin with ldap:// or ldaps:// if not validation error will be displayed.


  server_uri_state (optional, str, None)
    Specifies if the :emphasis:`server\_uris` need to be added or removed from the provider.

    This parameter is mandatory if :emphasis:`server\_uris` is specified.

    While creating LDAP provider, this parameter value should be specified as :literal:`present-in-ldap`.


  base_dn (optional, str, None)
    Specifies the root of the tree in which to search identities.

    This parameter is mandatory during create.


  ldap_parameters (optional, dict, None)
    Specify additional parameters to configure LDAP domain.


    groupnet (optional, str, None)
      Groupnet identifier.

      This is an optional parameter and defaults to groupnet0.


    bind_dn (optional, str, None)
      Specifies the distinguished name for binding to the LDAP server.


    bind_password (optional, str, None)
      Specifies the password for the distinguished name for binding to the LDAP server.



  state (True, str, None)
    The state of the LDAP provider after the task is performed.

    :literal:`present` - indicates that the LDAP provider should exist on the system.

    :literal:`absent` - indicates that the LDAP provider should not exist on the system.


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
   - This module does not support modification of :emphasis:`bind\_password` of LDAP provider.
   - The value specified for :emphasis:`bind\_password` will be ignored during modify.
   - The :emphasis:`check\_mode` is not supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Add an LDAP provider
      dellemc.powerscale.ldap:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        ldap_name: "ldap_test"
        server_uris:
          - "{{server_uri_1}}"
          - "{{server_uri_2}}"
        server_uri_state: 'present-in-ldap'
        base_dn: "DC=ansildap,DC=com"
        ldap_parameters:
          groupnet: "groupnet_ansildap"
          bind_dn: "cn=admin,dc=example,dc=com"
          bind_password: "{{bind_password}}"
        state: "present"

    - name: Add server_uris to an LDAP provider
      dellemc.powerscale.ldap:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        ldap_name: "ldap_test"
        server_uris:
          - "{{server_uri_1}}"
        server_uri_state: "present-in-ldap"
        state: "present"

    - name: Remove server_uris from an LDAP provider
      dellemc.powerscale.ldap:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        ldap_name: "ldap_test"
        server_uris:
          - "{{server_uri_1}}"
        server_uri_state: "absent-in-ldap"
        state: "present"

    - name: Modify LDAP provider
      dellemc.powerscale.ldap:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        ldap_name: "ldap_test"
        base_dn: "DC=ansi_ldap,DC=com"
        ldap_parameters:
          bind_dn: "cn=admin,dc=test,dc=com"
        state: "present"

    - name: Get LDAP provider details
      dellemc.powerscale.ldap:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        ldap_name: "ldap_test"
        state: "present"

    - name: Delete a LDAP provider
      dellemc.powerscale.ldap:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        ldap_name: "ldap_test"
        state: "absent"



Return Values
-------------

changed (always, bool, false)
  Whether or not the resource has changed.


ldap_provider_details (When LDAP provider exists, complex, {'linked_access_zones': ['System'], 'base_dn': 'dc=sample,dc=ldap,dc=domain,dc=com', 'bind_dn': 'cn=administrator,dc=sample,dc=ldap,dc=domain,dc=com', 'groupnet': 'groupnet', 'name': 'sample-ldap', 'server_uris': 'ldap://xx.xx.xx.xx', 'status': 'online'})
  The LDAP provider details.


  linked_access_zones (, list, )
    List of access zones linked to the authentication provider.


  base_dn (, str, )
    Specifies the root of the tree in which to search identities.


  bind_dn (, str, )
    Specifies the distinguished name for binding to the LDAP server.


  groupnet (, str, )
    Groupnet identifier.


  name (, str, )
    Specifies the name of the LDAP provider.


  server_uris (, str, )
    Specifies the server URIs.


  status (, str, )
    Specifies the status of the provider.






Status
------





Authors
~~~~~~~

- Jennifer John (@johnj9) <ansible.team@dell.com>

