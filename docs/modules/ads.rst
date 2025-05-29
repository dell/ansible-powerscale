.. _ads_module:


ads -- Manages the ADS authentication provider on PowerScale
============================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manages the Active Directory authentication provider on the PowerScale storage system.

This includes adding spn, removing spn, fixing spn, checking spn, creating, modifying, deleting and retreiving the details of an ADS provider.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.16 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  domain_name (optional, str, None)
    Specifies the domain name of an Active Directory provider.

    This parameter is mandatory during create.


  instance_name (optional, str, None)
    Specifies the instance name of Active Directory provider.

    This is an optional parameter during create, and defaults to the provider name if it is not specified during the create operation.

    Get, modify and delete operations can also be performed through instance\_name.

    It is mutually exclusive with \ :emphasis:`domain\_name`\  for get, modify and delete operations.


  ads_user (optional, str, None)
    Specifies the user name that has permission to join a machine to the given domain.

    This parameter is mandatory during create.


  ads_password (optional, str, None)
    Specifies the password used during domain join.

    This parameter is mandatory during create.


  ads_parameters (optional, dict, None)
    Specify additional parameters to configure ADS domain.


    allocate_gids (optional, bool, None)
      Allocates an ID for an unmapped Active Directory (ADS) group.

      ADS groups without GIDs can be proactively assigned a GID by the ID mapper.

      If the ID mapper option is disabled, GIDs are not proactively assigned, and when a primary group for a user does not include a GID, the system may allocate one.


    allocate_uids (optional, bool, None)
      Allocates a user ID for an unmapped Active Directory (ADS) user.

      ADS users without UIDs can be proactively assigned a UID by the ID mapper.

      IF the ID mapper option is disabled, UIDs are not proactively assigned, and when an identify for a user does not include a UID, the system may allocate one.


    assume_default_domain (optional, bool, None)
      Enables lookup of unqualified user names in the primary domain.


    authentication (optional, bool, None)
      Enables authentication and identity management through the authentication provider.


    create_home_directory (optional, bool, None)
      Automatically creates a home directory on the first login.


    check_online_interval (optional, int, None)
      Specifies the time in seconds between provider online checks.


    domain_offline_alerts (optional, bool, None)
      Sends an alert if the domain goes offline.


    extra_expected_spns (optional, list, None)
      List of additional SPNs to expect beyond what automatic checking routines might find.


    findable_groups (optional, list, None)
      Sets list of groups that can be resolved.


    findable_users (optional, list, None)
      Sets list of users that can be resolved.


    groupnet (optional, str, None)
      Groupnet identifier.

      This is an optional parameter and defaults to \ :literal:`groupnet0`\ .


    home_directory_template (optional, str, None)
      Specifies the path to the home directory template.

      This is an optional parameter and defaults to \ :literal:`/ifs/home/%D/%U`\ .


    ignore_all_trusts (optional, bool, None)
      If set to true, ignores all trusted domains.


    ignored_trusted_domains (optional, list, None)
      Includes trusted domains when \ :emphasis:`ignore\_all\_trusts`\  is set to \ :literal:`False`\ .


    include_trusted_domains (optional, list, None)
      Includes trusted domains when 'ignore\_all\_trusts' is set to \ :literal:`True`\ .


    login_shell (optional, str, None)
      Specifies the login shell path.

      This is an optional parameter and defaults to \ :literal:`/bin/zsh`\ .


    ldap_sign_and_seal (optional, bool, None)
      Enables encryption and signing on LDAP requests.


    lookup_groups (optional, bool, None)
      Looks up AD groups in other providers before allocating a group ID.


    lookup_normalize_groups (optional, bool, None)
      Normalizes AD group names to lowercase before look up.


    lookup_normalize_users (optional, bool, None)
      Normalize AD user names to lowercase before look up.


    lookup_users (optional, bool, None)
      Looks up AD users in other providers before allocating a user ID.


    lookup_domains (optional, list, None)
      Limits user and group lookups to the specified domains.


    machine_account (optional, str, None)
      Specifies the machine account name when creating a SAM account with Active Directory.

      The default cluster name is called \ :literal:`default`\ .


    machine_password_changes (optional, bool, None)
      Enables periodic changes of the machine password for security.


    machine_password_lifespan (optional, int, None)
      Sets maximum age of a password in seconds.


    nss_enumeration (optional, bool, None)
      Enables the Active Directory provider to respond to 'getpwent' and 'getgrent' requests.


    organizational_unit (optional, str, None)
      Specifies the organizational unit.


    restrict_findable (optional, bool, None)
      Check the provider for filtered lists of findable and unfindable users and groups.


    rpc_call_timeout (optional, int, None)
      The maximum amount of time (in seconds) an RPC call to Active Directory is allowed to take.


    store_sfu_mappings (optional, bool, None)
      Stores SFU mappings permanently in the ID mapper.


    server_retry_limit (optional, int, None)
      The number of retries attempted when a call to Active Directory fails due to network error.


    sfu_support (optional, str, None)
      Specifies whether to support RFC 2307 attributes on ADS domain controllers.


    unfindable_groups (optional, list, None)
      Specifies groups that cannot be resolved by the provider.


    unfindable_users (optional, list, None)
      Specifies users that cannot be resolved by the provider.



  spns (optional, list, None)
    List of SPN's to configure.


    spn (True, str, None)
      Service Principle Name(SPN).


    state (optional, str, present)
      The state of the SPN.

      \ :literal:`present`\  - indicates that the SPN should exist on the machine account.

      \ :literal:`absent`\  - indicates that the SPN should not exist on the machine account.



  spn_command (optional, str, None)
    Specify command of SPN.

    \ :literal:`check`\  - Check for missing SPNs for an AD provider.

    \ :literal:`fix`\  - Adds missing SPNs for an AD provider.


  state (True, str, None)
    The state of the ads provider after the task is performed.

    \ :literal:`present`\  - indicates that the ADS provider should exist on the system.

    \ :literal:`absent`\  - indicates that the ADS provider should not exist on the system.


  onefs_host (True, str, None)
    IP address or FQDN of the PowerScale cluster.


  port_no (False, str, 8080)
    Port number of the PowerScale cluster.It defaults to 8080 if not specified.


  verify_ssl (True, bool, None)
    boolean variable to specify whether to validate SSL certificate or not.

    \ :literal:`true`\  - indicates that the SSL certificate should be verified.

    \ :literal:`false`\  - indicates that the SSL certificate should not be verified.


  api_user (True, str, None)
    username of the PowerScale cluster.


  api_password (True, str, None)
    the password of the PowerScale cluster.





Notes
-----

.. note::
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Add an Active Directory provider
      dellemc.powerscale.ads:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        domain_name: "ansibleneo.com"
        instance_name: "ansibleneo.com"
        ads_user: "administrator"
        ads_password: "*****"
        ads_parameters:
          groupnet: "groupnet5"
          home_directory_template: "/ifs/home/%D/%U"
          login_shell: "/bin/zsh"
          machine_account: "test_account"
          organizational_unit: "org/sub_org"
          allocate_gids: true
          allocate_uids: false
          assume_default_domain: false
          authentication: true
          create_home_directory: true
          domain_offline_alerts: true
          ignore_all_trusts: true
          ignored_trusted_domains:
            - "example.com"
            - "example1.com"
          include_trusted_domains:
            - "trusted.com"
          ldap_sign_and_seal: true
          lookup_groups: true
          lookup_normalize_groups: true
          lookup_normalize_users: true
          lookup_users: true
          machine_password_changes: true
          nss_enumeration: true
          restrict_findable: true
          store_sfu_mappings: true
          check_online_interval: 7600
          machine_password_lifespan: 34567
          rpc_call_timeout: 45
          server_retry_limit: 789
          sfu_support: "rfc2307"
          extra_expected_spns:
            - span
          findable_groups:
            - "groupone"
          findable_users:
            - "userone"
          lookup_domains:
            - "example.com"
          unfindable_groups:
            - "nogroups"
          unfindable_users:
            - "nouser"
        state: "present"

    - name: Modify an Active Directory provider with domain name
      dellemc.powerscale.ads:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        domain_name: "ansibleneo.com"
        ads_parameters:
          home_directory_template: "/ifs/usr_home/%D/%U"
          login_shell: "/bin/rbash"
        state: "present"

    - name: Modify an Active Directory provider with instance name
      dellemc.powerscale.ads:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        instance_name: "ansibleneo.com"
        ads_parameters:
          home_directory_template: "/ifs/usr_home/%D/%U"
          login_shell: "/bin/rbash"
          allocate_gids: false
          allocate_uids: true
          assume_default_domain: true
          authentication: false
        state: "present"

    - name: Get Active Directory provider details with domain name
      dellemc.powerscale.ads:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        domain_name: "ansibleneo.com"
        state: "present"

    - name: Add an SPN
      dellemc.powerscale.ads:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        ads_user: "{{ ads_user }}"
        ads_password: "{{ ads_password }}"
        verify_ssl: "{{verify_ssl}}"
        domain_name: "ansibleneo.com"
        spns:
          - spn: "HOST/test1"
        state: "present"

    - name: Remove an SPN
      dellemc.powerscale.ads:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        ads_user: "{{ ads_user }}"
        ads_password: "{{ ads_password }}"
        verify_ssl: "{{verify_ssl}}"
        domain_name: "ansibleneo.com"
        spns:
          - spn: "HOST/test1"
            state: "absent"
        state: "present"

    - name: Check an SPN
      dellemc.powerscale.ads:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        domain_name: "ansibleneo.com"
        spn_command: "check"
        state: "present"

    - name: Fix an SPN
      dellemc.powerscale.ads:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        ads_user: "{{ ads_user }}"
        ads_password: "{{ ads_password }}"
        verify_ssl: "{{verify_ssl}}"
        domain_name: "ansibleneo.com"
        spn_command: "fix"
        state: "present"

    - name: Get Active Directory provider details with instance name
      dellemc.powerscale.ads:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        instance_name: "ansibleneo.com"
        state: "present"

    - name: Delete an Active Directory provider with domain name
      dellemc.powerscale.ads:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        domain_name: "ansibleneo.com"
        state: "absent"

    - name: Delete an Active Directory provider with instance name
      dellemc.powerscale.ads:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        instance_name: "ansibleneo.com"
        state: "absent"



Return Values
-------------

changed (always, bool, false)
  Whether or not the resource has changed.


spn_check (When check operation is done., list, ['host/test1'])
  Missing SPNs for an AD provider.


ads_provider_details (When Active Directory provider exists, complex, {'ads_provider_details': [{'allocate_gids': True, 'allocate_uids': True, 'assume_default_domain': False, 'authentication': True, 'check_online_interval': 300, 'controller_time': 1725339127, 'create_home_directory': False, 'domain_offline_alerts': False, 'extra_expected_spns': ['HOST/test5'], 'findable_groups': [], 'findable_users': [], 'forest': 'sample.emc.com', 'groupnet': 'groupnet0', 'home_directory_template': '/ifs/home/%D/%U', 'hostname': 'sample.emc.com', 'id': 'SAMPLE.COM', 'ignore_all_trusts': False, 'ignored_trusted_domains': [], 'include_trusted_domains': [], 'instance': '', 'ldap_sign_and_seal': False, 'linked_access_zones': ['System'], 'login_shell': '/bin/zsh', 'lookup_domains': [], 'lookup_groups': True, 'lookup_normalize_groups': True, 'lookup_normalize_users': True, 'lookup_users': True, 'machine_account': 'PI98S$$', 'machine_password_changes': True, 'machine_password_lifespan': 31536000, 'name': 'SAMPLE.COM', 'netbios_domain': 'PIERTP', 'node_dc_affinity': None, 'node_dc_affinity_timeout': None, 'nss_enumeration': False, 'primary_domain': 'SAMPLE.COM', 'recommended_spns': ['HOST/test1', 'HOST/test2', 'HOST/test3', 'HOST/test4'], 'restrict_findable': False, 'sfu_support': 'none', 'site': 'Default-First-Site-Name', 'spns': ['HOST/test2', 'HOST/test3', 'HOST/test4', 'HOST/test5'], 'status': 'online', 'store_sfu_mappings': False, 'system': False, 'unfindable_groups': [], 'unfindable_users': [], 'zone_name': 'System'}]})
  The Active Directory provider details.


  allocate_gids (, bool, )
    Allocates an ID for an unmapped Active Directory (ADS) group.


  allocate_uids (, bool, )
    Allocates an ID for an unmapped Active Directory (ADS) user.


  assume_default_domain (, bool, )
    Enables lookup of unqualified user names in the primary domain.


  authentication (, bool, )
    Enables authentication and identity management through the authentication provider.


  check_online_interval (, int, )
    Specifies the time in seconds between provider online checks.


  controller_time (, int, )
    Specifies the current time for the domain controllers.


  create_home_directory (, bool, )
    Automatically creates a home directory on the first login.


  domain_offline_alerts (, bool, )
    Sends an alert if the domain goes offline.


  dup_spns (, list, )
    Get duplicate SPNs in the provider domain.


  extra_expected_spns (, list, )
    List of additional SPNs to expect beyond what automatic checking routines might find.


  findable_groups (, list, )
    Sets list of groups that can be resolved.


  findable_users (, list, )
    Sets list of users that can be resolved.


  forest (, str, )
    Specifies the Active Directory forest.


  groupnet (, str, )
    Groupnet identifier.


  home_directory_template (, str, )
    Specifies the path to the home directory template.


  hostname (, str, )
    Specifies the fully qualified hostname stored in the machine account.


  id (, str, )
    Specifies the ID of the Active Directory provider instance.


  ignore_all_trusts (, bool, )
    If set to \ :literal:`true`\ , ignores all trusted domains.


  ignored_trusted_domains (, list, )
    Includes trusted domains when \ :emphasis:`ignore\_all\_trusts`\  is set to \ :literal:`false.`\ 


  include_trusted_domains (, list, )
    Includes trusted domains when \ :emphasis:`ignore\_all\_trusts`\  is set to \ :literal:`true.`\ 


  instance (, str, )
    Specifies Active Directory provider instance.


  ldap_sign_and_seal (, bool, )
    Enables encryption and signing on LDAP requests.


  login_shell (, str, )
    Specifies the login shell path.


  lookup_domains (, list, )
    Limits user and group lookups to the specified domains.


  linked_access_zones (, list, )
    List of access zones linked to the authentication provider.


  lookup_groups (, bool, )
    Looks up AD groups in other providers before allocating a group ID.


  lookup_normalize_groups (, bool, )
    Normalizes AD group names to lowercase before look up.


  lookup_normalize_users (, bool, )
    Normalizes AD user names to lowercase before look up.


  lookup_users (, bool, )
    Looks up AD users in other providers before allocating a user ID.


  machine_account (, str, )
    Specifies the machine account name when creating a SAM account with Active Directory.


  machine_password_changes (, bool, )
    Enables periodic changes of the machine password for security.


  machine_password_lifespan (, int, )
    Sets maximum age of a password in seconds.


  name (, str, )
    Specifies the Active Directory provider name.


  netbios_domain (, str, )
    Specifies the NetBIOS domain name associated with the machine account.


  node_dc_affinity (, str, )
    Specifies the domain controller for which the node has affinity.


  node_dc_affinity_timeout (, int, )
    pecifies the timeout for the domain controller for which the local node has affinity.


  nss_enumeration (, bool, )
    Enables the Active Directory provider to respond to 'getpwent' and 'getgrent' requests.


  primary_domain (, str, )
    Specifies the AD domain to which the provider is joined.


  restrict_findable (, bool, )
    Check the provider for filtered lists of findable and unfindable users and groups.


  rpc_call_timeout (, int, )
    The maximum amount of time (in seconds) an RPC call to Active Directory is allowed to take.


  server_retry_limit (, int, )
    The number of retries attempted when a call to Active Directory fails due to network error.


  sfu_support (, str, )
    Specifies whether to support RFC 2307 attributes on ADS domain controllers.


  site (, str, )
    Specifies the site for the Active Directory.


  status (, str, )
    Specifies the status of the provider.


  store_sfu_mappings (, bool, )
    Stores SFU mappings permanently in the ID mapper.


  system (, bool, )
    If set to \ :literal:`true`\ , indicates that this provider instance was created by OneFS and cannot be removed.


  unfindable_groups (, list, )
    Sets list of groups that cannot be resolved.


  unfindable_users (, list, )
    Sets list of users that cannot be resolved.


  zone_name (, str, )
    Specifies the name of the access zone in which this provider was created.


  recommended_spns (, list, )
    Configuration recommended SPNs.


  spns (, list, )
    Currently configured SPNs.






Status
------





Authors
~~~~~~~

- Jennifer John (@johnj9) <ansible.team@dell.com>
- Bhavneet Sharma (@Bhavneet-Sharma) <ansible.team@dell.com>

