.. _ipmi_module:


ipmi -- Manage IPMI configuration on a PowerScale Storage System
================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing IPMI (Intelligent Platform Management Interface) configuration on a PowerScale system includes retrieving and updating IPMI settings, network, user, and features.

IPMI provides a dedicated management channel for lights-out management (power control and Serial-over-LAN) via the node BMC interface, external to OneFS. Supported on Gen6/PowerScale nodes from OneFS 9.0 onward.

This module supports idempotent execution, check mode, and diff mode.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.17 or later.
- Python 3.11, 3.12 or 3.13.



Parameters
----------

  settings (optional, dict, None)
    IPMI settings configuration.

    Used to enable/disable remote IPMI management and set the allocation type.


    enabled (optional, bool, None)
      Whether remote IPMI management is enabled.


    allocation_type (optional, str, None)
      The IP allocation type for IPMI.

      Valid choices are :literal:`dhcp`, :literal:`static`, :literal:`range`.



  network (optional, dict, None)
    IPMI network configuration for BMC.


    gateway (optional, str, None)
      The gateway IP address for the IPMI network.


    prefixlen (optional, int, None)
      The network prefix length for the IPMI network.


    ip_ranges (optional, list, None)
      List of IP address ranges for IPMI.

      Each range is a dict with :emphasis:`low` and :emphasis:`high` keys.


      low (True, str, None)
        The low end of the IP address range.


      high (True, str, None)
        The high end of the IP address range.



  user (optional, dict, None)
    IPMI BMC user configuration.


    username (optional, str, None)
      The BMC username.


    password (optional, str, None)
      The BMC password.



  features (optional, list, None)
    List of IPMI features to configure.

    Each feature is identified by :emphasis:`id` and can be enabled or disabled.


    id (True, str, None)
      The feature identifier (e.g. :literal:`power_control`, :literal:`sol`).


    enabled (True, bool, None)
      Whether the feature is enabled.



  state (optional, str, present)
    The desired state of the IPMI configuration.

    Value :literal:`present` indicates that the specified IPMI configuration should be applied.


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
   - The :emphasis:`diff` mode is supported.
   - Idempotency is not supported for user password since the API does not return passwords for comparison.
   - Requires OneFS 9.0 or later on Gen6/PowerScale nodes.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get current IPMI configuration
      dellemc.powerscale.ipmi:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"

    - name: Enable IPMI with static allocation
      dellemc.powerscale.ipmi:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        settings:
          enabled: true
          allocation_type: "static"
        state: "present"

    - name: Configure IPMI network
      dellemc.powerscale.ipmi:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        network:
          gateway: "10.0.0.1"
          prefixlen: 24
          ip_ranges:
            - low: "10.0.0.100"
              high: "10.0.0.200"
        state: "present"

    - name: Configure IPMI user
      dellemc.powerscale.ipmi:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        user:
          username: "admin"
          password: "{{ vault_ipmi_password }}"
        state: "present"

    - name: Enable power control feature
      dellemc.powerscale.ipmi:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        features:
          - id: "power_control"
            enabled: true
        state: "present"

    - name: Configure all IPMI domains at once
      dellemc.powerscale.ipmi:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        settings:
          enabled: true
          allocation_type: "static"
        network:
          gateway: "10.0.0.1"
          prefixlen: 24
          ip_ranges:
            - low: "10.0.0.100"
              high: "10.0.0.200"
        user:
          username: "admin"
          password: "{{ vault_ipmi_password }}"
        features:
          - id: "power_control"
            enabled: true
          - id: "sol"
            enabled: true
        state: "present"

    - name: Configure IPMI settings in check mode
      dellemc.powerscale.ipmi:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        settings:
          enabled: true
          allocation_type: "dhcp"
        state: "present"
      check_mode: true



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


diff (when diff mode is enabled and changes are made, dict, {'after': {'features': [{'enabled': True, 'id': 'power_control'}], 'network': {'gateway': '10.0.0.1', 'prefixlen': 24}, 'settings': {'allocation_type': 'static', 'enabled': True}, 'user': {'username': 'admin'}}, 'before': {'features': [{'enabled': False, 'id': 'power_control'}], 'network': {'gateway': '', 'prefixlen': 0}, 'settings': {'allocation_type': 'dhcp', 'enabled': False}, 'user': {'username': 'admin'}}})
  The differences between the before and after states.


  before (, dict, )
    The IPMI configuration before changes.


  after (, dict, )
    The IPMI configuration after changes.



ipmi_details (always, dict, {'features': [{'enabled': True, 'id': 'power_control'}, {'enabled': True, 'id': 'sol'}], 'network': {'gateway': '10.0.0.1', 'ip_ranges': [{'high': '10.0.0.200', 'low': '10.0.0.100'}], 'prefixlen': 24}, 'nodes': [], 'settings': {'allocation_type': 'static', 'enabled': True}, 'user': {'username': 'admin'}})
  The current IPMI configuration after module execution.


  settings (, dict, )
    IPMI settings (enabled, allocation_type).


    enabled (, bool, )
      Whether remote IPMI management is enabled.


    allocation_type (, str, )
      The IP allocation type for IPMI.



  network (, dict, )
    IPMI network configuration.


    gateway (, str, )
      The gateway IP address for the IPMI network.


    prefixlen (, int, )
      The network prefix length for the IPMI network.


    ip_ranges (, list, )
      List of IP address ranges for IPMI.


      low (, str, )
        The low end of the IP address range.


      high (, str, )
        The high end of the IP address range.



  user (, dict, )
    IPMI user configuration (password is redacted).


    username (, str, )
      The BMC username.



  features (, list, )
    IPMI features list.


    id (, str, )
      The feature identifier.


    enabled (, bool, )
      Whether the feature is enabled.



  nodes (, list, )
    IPMI nodes information (read-only).






Status
------





Authors
~~~~~~~

- Shrinidhi Rao (@shrinidhirao) <ansible.team@dell.com>
