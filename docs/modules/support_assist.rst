.. _support_assist_module:


support_assist -- Manage support assist settings on a PowerScale Storage System
===============================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing support assist settings on a PowerScale system includes retrieving details of support assist settings and modifying support assist settings.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.14 or later.
- Python 3.9, 3.10 or 3.11.



Parameters
----------

  automatic_case_creation (optional, bool, None)
    ``True`` indicates automatic case creation is enabled.


  connection (optional, dict, None)
    Support assist connection details.


    gateway_endpoints (optional, list, None)
      List of gateway endpoints.


      gateway_host (True, str, None)
        Hostname or IP address of the gateway endpoint.


      gateway_port (optional, int, 9443)
        Port number of the gateway endpoint.


      priority (optional, int, 1)
        Priority of the gateway endpoint.


      use_proxy (optional, bool, False)
        Use proxy.


      validate_ssl (optional, bool, False)
        Validate SSL.


      enabled (optional, bool, True)
        Enable the gateway endpoint.


      state (optional, str, present)
        State of the gateway endpoint.



    mode (optional, str, None)
      Connection mode.


    network_pools (optional, list, None)
      List of network pools.


      pool_name (optional, str, None)
        Name of the network pool.


      state (optional, str, present)
        State of the network pool.




  connection_state (optional, str, None)
    Set connectivity state.


  contact (optional, dict, None)
    Information on the remote support contact.


    primary (optional, dict, None)
      Primary contact details.


      first_name (optional, str, None)
        First name of the primary contact.


      last_name (optional, str, None)
        Last name of the primary contact.


      email (optional, str, None)
        Email address of the primary contact.


      phone (optional, str, None)
        Phone number of the primary contact.



    secondary (optional, dict, None)
      Secondary contact details.


      first_name (optional, str, None)
        First name of the secondary contact.


      last_name (optional, str, None)
        Last name of the secondary contact.


      email (optional, str, None)
        Email address of the secondary contact.


      phone (optional, str, None)
        Phone number of the secondary contact.




  telemetry (optional, dict, None)
    Enable telemetry.


    offline_collection_period (optional, int, None)
      Change the offline collection period for when the connection to gateway is down.

      The range is 0 to 86400.


    telemetry_enabled (optional, bool, None)
      Change the status of telemetry.

      When set to ``False``, modification of other telemetry suboptions will be idempotent.


    telemetry_persist (optional, bool, None)
      Change if files are kept after upload.


    telemetry_threads (optional, int, None)
      Change the number of threads for telemetry gathers.

      The range is 1 to 64.



  enable_download (optional, bool, None)
    ``True`` indicates downloads are enabled.


  enable_remote_support (optional, bool, None)
    Allow remote support.


  enable_service (optional, bool, None)
    Enable/disable SupportAssist service.


  accepted_terms (optional, bool, None)
    Whether to accept or reject the terms and conditions for remote support.


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
   - The *check_mode* and idempotency is supported.
   - This module is supported for PowerScale One FS version 9.5 and above.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get support assist setiings
      dellemc.powerscale.support_assist:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"

    - name: Update support assist settings
      dellemc.powerscale.support_assist:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        enable_download: false
        enable_remote_support: false
        automatic_case_creation: false
        connection:
          gateway_endpoints:
            - enabled: true
              gateway_host: "XX.XX.XX.XX"
              gateway_port: 9443
              priority: 1
              use_proxy: false
              validate_ssl: false
              state: present
          network_pools:
            - pool_name: "subnet0:pool0"
              state: absent
            - pool_name: "subnet0:pool1"
        connection_state: "enabled"
        contact:
          primary:
            first_name: "John"
            last_name: "Doe"
            email: "john.doe@example.com"
            phone: "1234567890"
          secondary:
            first_name: "Jane"
            last_name: "Doe"
            email: "jane.doe@example.com"
            phone: "1234567891"
        telemetry:
          offline_collection_period: 60
          telemetry_enabled: true
          telemetry_persist: true
          telemetry_threads: 10

    - name: Accept support assist terms
      dellemc.powerscale.support_assist:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        accepted_terms: true



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


support_assist_details (always, dict, {'automatic_case_creation': False, 'connection': {'gateway_endpoints': [{'enabled': True, 'host': 'XX.XX.XX.XX', 'port': 9443, 'priority': 1, 'use_proxy': False, 'validate_ssl': False}, {'enabled': True, 'host': 'XX.XX.XX.XY', 'port': 9443, 'priority': 2, 'use_proxy': False, 'validate_ssl': False}], 'mode': 'gateway', 'network_pools': [{'pool': 'pool1', 'subnet': 'subnet0'}]}, 'connection_state': 'disabled', 'contact': {'primary': {'email': 'p7VYg@example.com', 'first_name': 'Eric', 'last_name': 'Nam', 'phone': '1234567890'}, 'secondary': {'email': 'kangD@example.com', 'first_name': 'Daniel', 'last_name': 'Kang', 'phone': '1234567891'}}, 'enable_download': False, 'enable_remote_support': False, 'onefs_software_id': 'ELMISL1019H4GY', 'supportassist_enabled': True, 'telemetry': {'offline_collection_period': 60, 'telemetry_enabled': True, 'telemetry_persist': True, 'telemetry_threads': 10}})
  The updated support assist settings details.


  automatic_case_creation (, bool, )
    True indicates automatic case creation is enabled.


  connection (, complex, )
    The server connections.


    gateway_endpoints (, list, )
      List of gateway endpoints.


      enabled (, bool, )
        True indicates gateway endpoint is enabled.


      host (, str, )
        Specify the gateway host.


      port (, int, )
        Specify the gateway port.


      priority (, int, )
        Specify the gateway priority.


      use_proxy (, bool, )
        Specify whether to use proxy.


      validate_ssl (, bool, )
        Specify whether to validate SSL.



    mode (, str, )
      Specify the mode.


    network_pools (, list, )
      List of network pools.


      pool (, str, )
        The network pool name.


      subnet (, str, )
        The network pool subnet.




  connection_state (, str, )
    Specify the connection state.


  contact (, complex, )
    Specify the contact details.


    primary (, complex, )
      Specify the primary contact details.


      first_name (, str, )
        First name of the primary contact.


      last_name (, str, )
        Last name of the primary contact.


      email (, str, )
        Email address of the primary contact.


      phone (, str, )
        Phone number of the primary contact.



    secondary (, complex, )
      Specify the secondary contact details.


      first_name (, str, )
        First name of the secondary contact.


      last_name (, str, )
        Last name of the secondary contact.


      email (, str, )
        Email address of the secondary contact.


      phone (, str, )
        Phone number of the secondary contact.




  enable_download (, bool, )
    True indicates downloads are enabled.


  enable_remote_support (, bool, )
    Whether remoteAccessEnabled is enabled.


  onefs_software_id (, str, )
    The software ID used by SupportAssist


  supportassist_enabled (, bool, )
    Whether SupportAssist is enabled.


  telemetry (, complex, )
    Telemetry settings.


    offline_collection_period (, int, )
      Specify the offline collection period.


    telemetry_enabled (, bool, )
      Specify whether telemetry is enabled.


    telemetry_persist (, bool, )
      Specify whether telemetry is persisted.


    telemetry_threads (, int, )
      Specify the number of telemetry threads.







Status
------





Authors
~~~~~~~

- Trisha Datta (@trisha-dell) <ansible.team@dell.com>

