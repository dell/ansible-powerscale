.. _networksettings_module:


networksettings -- Manages Network Settings on PowerScale Storage System
========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing Network Settings on the PowerScale Storage System includes modifying and retrieving details of network settings.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system. Ansible 2.12, 2.13 or 2.14.



Parameters
----------

  enable_source_routing (optional, bool, None)
    The value for enabling or disabling source based routing.


  state (True, str, None)
    State of network settings.


  onefs_host (True, str, None)
    IP address or FQDN of the PowerScale cluster.


  port_no (False, str, 8080)
    Port number of the PowerScale cluster.It defaults to 8080 if not specified.


  verify_ssl (True, bool, None)
    boolean variable to specify whether to validate SSL certificate or not.

    True - indicates that the SSL certificate should be verified.

    False - indicates that the SSL certificate should not be verified.


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

    
        - name: Get Network settings
          dellemc.powerscale.networksettings:
          onefs_host: "{{onefs_host}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          state: "{{state_present}}"

        - name: Enable source based routing
          dellemc.powerscale.networksettings:
          onefs_host: "{{onefs_host}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          enable_source_routing: True
          state: "{{state_present}}"

        - name: Disable source based routing
          dellemc.powerscale.networksettings:
          onefs_host: "{{onefs_host}}"
          api_user: "{{api_user}}"
          api_password: "{{api_password}}"
          verify_ssl: "{{verify_ssl}}"
          enable_source_routing: False
          state: "{{state_present}}"



Return Values
-------------

changed (always, bool, )
  Whether or not the resource has changed.


network_settings (always, complex, )
  Details of the network settings.


  default_groupnet (, str, )
    Default client-side DNS settings for non-multitenancy aware programs.


  sbr (, str, )
    Enable or disable source based routing.


  sc_rebalance_delay (, int, )
    Delay in seconds for IP rebalance.


  tcp_ports (, list, )
    List of client TCP ports.






Status
------





Authors
~~~~~~~

- Meenakshi Dembi (@dembim) <ansible.team@dell.com>

