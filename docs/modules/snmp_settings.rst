.. _snmp_settings_module:


snmp_settings -- Manage SNMP settings on PowerScale storage systems
===================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage SNMP settings on PowerScale storage systems includes retrieving, and updating SNMP settings.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.14 or later.
- Python 3.9, 3.10 or 3.11.



Parameters
----------

  read_only_community (optional, str, None)
    SNMP read-only community name.

    The system default value of the read-only community name is ``I$ilonpublic``.

    Update the read-only community name while enabling SNMP v2c.


  service (optional, bool, None)
    Whether the SNMP service is enabled.


  snmp_v2c_access (optional, bool, None)
    Whether the SNMP v2c is enabled.

    OneFS support SNMP v2c and later.


  snmp_v3 (optional, dict, None)
    Specify the access, privacy, and security level for SNMP v3.


    access (optional, bool, None)
      Whether SNMP v3 is enabled.


    auth_protocol (optional, str, None)
      SNMP v3 authentication protocol.


    privacy_password (optional, str, None)
      SNMP v3 privacy password.


    password (optional, str, None)
      SNMP v3 authentication password.


    privacy_protocol (optional, str, None)
      SNMP v3 privacy protocol.


    security_level (optional, str, None)
      SNMP v3 security level.


    read_only_user (optional, str, None)
      The read-only user for SNMP v3 requests.

      The system default value of read-only user is ``general``.



  system_contact (optional, str, None)
    SNMP system owner contact information.

    This must be a valid email address.

    The contact information is set for the reporting purpose.


  system_location (optional, str, None)
    The cluster description for SNMP system.

    The cluster description is set for the reporting purpose.


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
   - The *check_mode* is supported.
   - Users can configure SNMP version 3 alone or in combination with version 2c.
   - Idempotency is not supported for SNMP v3's password and privacy password.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get SNMP settings
      dellemc.powerscale.snmp_settings:
        onefs_host: "{{ onefs_host }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"

    - name: Update SNMP settings
      dellemc.powerscale.snmp_settings:
        onefs_host: "{{ onefs_host }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        read_only_community: "community-name"
        snmp_v3:
          access: true
          auth_protocol: "SHA"
          privacy_password: "password"
          password: "auth_password"
          privacy_protocol: "AES"
          security_level: "noAuthNoPriv"
          read_only_user: "user"
        system_contact: "contact@domain.com"
        system_location: "Enabled SNMP"



Return Values
-------------

changed (always, bool, true)
  A Boolean value indicating if task had to make changes.


snmp_settings (always, dict, {'read_only_community': 'community-name', 'service': True, 'snmp_v1_v2c_access': True, 'snmp_v3_access': True, 'snmp_v3_auth_protocol': 'SHA', 'snmp_v3_priv_protocol': 'AES', 'snmp_v3_read_only_user': 'user', 'snmp_v3_security_level': 'noAuthNoPriv', 'system_contact': 'contact@domain.com', 'system_location': 'Enabled SNMP'})
  The details of SNMP settings.


  read_only_community (, str, )
    SNMP read-only community name.


  service (, bool, )
    Whether the SNMP service is enabled.


  snmp_v1_v2c_access (, bool, )
    Whether the SNMP v2c access is enabled.


  snmp_v3_access (, bool, )
    Whether the SNMP v3 is enabled.


  snmp_v3_auth_protocol (, str, )
    SNMP v3 authentication protocol.


  snmp_v3_priv_protocol (, str, )
    SNMP v3 privacy protocol.


  smnmp_v3_read_only_user (, str, )
    SNMP v3 read-only user.


  snmp_v3_security_level (, str, )
    SNMP v3 security level.


  system_contact (, str, )
    SNMP system owner contact information.


  system_location (, str, )
    The cluster description for SNMP system.






Status
------





Authors
~~~~~~~

- Bhavneet Sharma(@Bhavneet-Sharma) <ansible.team@dell.com>

