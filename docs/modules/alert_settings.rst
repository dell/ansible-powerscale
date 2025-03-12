.. _alert_settings_module:


alert_settings -- Manage alert settings on a PowerScale Storage System
======================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing alert settings on a PowerScale system includes retrieving details of alert settings and enabling or disabling the alert settings.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.15 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  enable_celog_maintenance_mode (optional, bool, None)
    Enabling CELOG maintenance mode will start a CELOG maintenance window.

    During a CELOG maintenance window, the system will continue to log events, but no alerts will be generated.

    You will have the opportunity to review all events that took place during the maintenance window when disabling maintenance mode.

    Active event groups will automatically resume generating alerts when the scheduled maintenance period ends.


  prune (optional, int, None)
    Removes all maintenance mode history that is greater than set number of days.

    Range of :emphasis:`prune` is 0 to 4294967295.

    If :emphasis:`prune` is set in task, then :emphasis:`changed` will be :literal:`true` always.


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
   - The :emphasis:`check\_mode` and idempotency is supported.
   - Idempotency is not supported with :emphasis:`prune` option.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Enable CELOG maintenance mode
      dellemc.powerscale.alert_settings:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        enable_celog_maintenance_mode: true

    - name: Disable CELOG and prune all history of maintenance mode
      dellemc.powerscale.alert_settings:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        enable_celog_maintenance_mode: false
        prune: 0



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


alert_settings_details (always, dict, {'history': [{'end': 0, 'start': 1719822336}], 'maintenance': False})
  The updated alert settings details.


  history (, list, )
    History list of CELOG maintenance mode windows.


    end (, int, )
      End time of CELOG maintenance mode, as a UNIX timestamp in seconds.

      Value 0 indicates that maintenance mode is still enabled.

      Refer alert setting sample playbook examples to convert UNIX timestamp to human readable format.


    start (, int, )
      Start time of CELOG maintenance mode, as a UNIX timestamp in seconds.

      Refer alert setting sample playbook examples to convert UNIX timestamp to human readable format.



  maintenance (, bool, )
    Indicates if maintenance mode is enabled.






Status
------





Authors
~~~~~~~

- Bhavneet Sharma (@Bhavneet-Sharma) <ansible.team@dell.com>

