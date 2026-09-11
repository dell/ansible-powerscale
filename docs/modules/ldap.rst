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
- Ansible-core 2.17 or later.
- Python 3.11, 3.12 or 3.13.



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


    group_base_dn (optional, str, None)
      Specifies the LDAP search base DN used exclusively for group lookups.

      When set, group searches use this DN instead of the provider-level :emphasis:`base\_dn`. This is useful when groups reside in a different subtree from users.

      Unlike :emphasis:`base\_dn`\ , which controls the overall search root for all identity lookups, :emphasis:`group\_base\_dn` narrows only the group search scope.

      Maximum length is 255 characters. DN syntax validation is delegated to OneFS.

      Omission (\ :literal:`None`\ ) preserves the current server value. An explicit empty string :literal:`""` clears the override so group lookups fall back to :emphasis:`base\_dn`.

      Comparison is byte-exact; a case-only change (e.g. :literal:`OU=Groups` to :literal:`ou=groups`\ ) is treated as a modification.


    provider_domain (optional, str, None)
      Specifies an explicit domain name used to qualify users and groups returned by this LDAP provider.

      In multi-domain environments, this prevents ambiguity when multiple providers return identities with the same short name.

      Unlike :literal:`user\_domain` and :literal:`group\_domain`\ , which are read-only attributes auto-populated by OneFS, :emphasis:`provider\_domain` is a user-configurable setting that overrides the auto-detected domain qualifier.

      No client-side format check or auto-detection is applied; the value is passed to OneFS as-is. Maximum length is 255 characters.

      Omission (\ :literal:`None`\ ) preserves the current server value. An explicit empty string :literal:`""` clears the override.


    authentication (optional, bool, None)
      Controls whether the LDAP provider is used for authentication.

      When set to :literal:`true`\ , the provider participates in both identity resolution and user authentication (the default OneFS behavior).

      When set to :literal:`false`\ , the provider becomes an :strong:`identity-only provider`. It remains fully usable for identity lookups and authorization decisions, but is excluded from the authentication process. This is not the same as disabling the provider — identity and authorization continue to function.

      Omission (\ :literal:`None`\ ) preserves the current server value. An explicit :literal:`false` is a valid, distinct value and is transmitted to OneFS.



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
   - :strong:`Troubleshooting` — If OneFS returns an error about invalid DN syntax for :emphasis:`group\_base\_dn`\ , verify the value is a well-formed LDAP distinguished name (e.g. :literal:`ou=groups,dc=example,dc=com`\ ). The module does not validate DN syntax client-side; all validation is performed by the OneFS API.
   - :strong:`Troubleshooting` — If group or user lookups fail with domain-qualification errors in a multi-domain environment, verify that :emphasis:`provider\_domain` is set to the correct domain name. The value must match the domain expected by OneFS; no auto-detection or format normalization is performed.
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

    - name: Configure a separate group search hierarchy
      dellemc.powerscale.ldap:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        ldap_name: "ldap_test"
        base_dn: "DC=ansildap,DC=com"
        ldap_parameters:
          group_base_dn: "OU=Groups,DC=ansildap,DC=com"
        state: "present"

    - name: Create an identity-only LDAP provider (excluded from authentication)
      dellemc.powerscale.ldap:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        ldap_name: "ldap_identity_only"
        server_uris:
          - "{{server_uri_1}}"
        server_uri_state: 'present-in-ldap'
        base_dn: "DC=ansildap,DC=com"
        ldap_parameters:
          groupnet: "groupnet0"
          bind_dn: "cn=admin,dc=ansildap,dc=com"
          bind_password: "{{bind_password}}"
          authentication: false
        state: "present"

    - name: Qualify users and groups with an explicit domain in a multi-domain environment
      dellemc.powerscale.ldap:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        ldap_name: "ldap_test"
        ldap_parameters:
          provider_domain: "corp.example.com"
        state: "present"

    - name: Preview LDAP changes without applying them (check mode + diff)
      dellemc.powerscale.ldap:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        ldap_name: "ldap_test"
        ldap_parameters:
          group_base_dn: "OU=NewGroups,DC=ansildap,DC=com"
          authentication: true
        state: "present"
      check_mode: true
      diff: true
      register: ldap_preview

    - name: Show the preview diff
      ansible.builtin.debug:
        var: ldap_preview.diff



Return Values
-------------

changed (always, bool, false)
  Whether or not the resource has changed.


ldap_provider_details (When LDAP provider exists, complex, {'linked_access_zones': ['System'], 'base_dn': 'dc=sample,dc=ldap,dc=domain,dc=com', 'bind_dn': 'cn=administrator,dc=sample,dc=ldap,dc=domain,dc=com', 'groupnet': 'groupnet', 'name': 'sample-ldap', 'server_uris': 'ldap://xx.xx.xx.xx', 'status': 'online', 'group_base_dn': '', 'provider_domain': '', 'authentication': True})
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


  group_base_dn (, str, )
    Specifies the LDAP group search base DN.


  provider_domain (, str, )
    Specifies the LDAP provider domain qualifier.


  authentication (, bool, )
    Whether authentication is enabled for the LDAP provider.






Status
------





Authors
~~~~~~~

- Jennifer John (@johnj9) <ansible.team@dell.com>

