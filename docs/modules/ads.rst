.. _ads_module:


ads -- Manages the ADS authentication provider on PowerScale
============================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manages the Active Directory authentication provider on the PowerScale storage system. This includes adding spn, removing spn, fixing spn, checking spn, creating, modifying, deleting and retreiving the details of an ADS provider.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.14 or later.
- Python 3.9, 3.10 or 3.11.



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


    groupnet (optional, str, None)
      Groupnet identifier.

      This is an optional parameter and defaults to \ :literal:`groupnet0`\ .


    home_directory_template (optional, str, None)
      Specifies the path to the home directory template.

      This is an optional parameter and defaults to \ :literal:`/ifs/home/%D/%U`\ .


    login_shell (optional, str, None)
      Specifies the login shell path.

      This is an optional parameter and defaults to \ :literal:`/bin/zsh`\ .


    machine_account (optional, str, None)
      Specifies the machine account name when creating a SAM account with Active Directory.

      The default cluster name is called \ :literal:`default`\ .


    organizational_unit (optional, str, None)
      Specifies the organizational unit.



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
   - The \ :emphasis:`check\_mode`\  is not supported.
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


ads_provider_details (When Active Directory provider exists, complex, {'ads_provider_details': [{'forest': 'sample.com', 'groupnet': 'groupnet0', 'home_directory_template': '/ifs/home/%D/%U', 'hostname': 'v.sample.com', 'id': 'sample.com', 'linked_access_zones': [], 'login_shell': '/bin/abc', 'machine_account': 'm1', 'name': 'sample.com', 'extra_expected_spns': ['HOST/test5'], 'recommended_spns': ['HOST/test1', 'HOST/test2', 'HOST/test3', 'HOST/test4'], 'spns': ['HOST/test2', 'HOST/test3', 'HOST/test4', 'HOST/test5'], 'status': 'online'}]})
  The Active Directory provider details.


  linked_access_zones (, list, )
    List of access zones linked to the authentication provider.


  groupnet (, str, )
    Groupnet identifier.


  home_directory_template (, str, )
    Specifies the path to the home directory template.


  id (, str, )
    Specifies the ID of the Active Directory provider instance.


  name (, str, )
    Specifies the Active Directory provider name.


  login_shell (, str, )
    Specifies the login shell path.


  machine_account (, str, )
    Specifies the machine account name when creating a SAM account with Active Directory.






Status
------





Authors
~~~~~~~

- Jennifer John (@johnj9) <ansible.team@dell.com>

