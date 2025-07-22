.. _alert_rule_module:


alert_rule -- Manage alert rule on a PowerScale Storage System
==============================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage alert rule on a PowerScale Storage System includes create, modify and delete.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.17 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  state (optional, str, present)
    The state option is used to mention the existence of server certificate.


  name (True, str, None)
    The :emphasis:`name` of the rule is a unique that cannot be changed.


  condition (optional, str, None)
    Trigger condition for alert.


  categories (optional, list, None)
    Event group categories to be alerted.


  channels (optional, list, None)
    Channels for the alert.

    This is option is required for create alert condition.


  eventgroup_ids (optional, list, None)
    Event group ID is to be alerted.


  exclude_eventgroup_ids (optional, list, None)
    Event group categories to be excluded from alerts.


  interval (optional, int, None)
    Required with :literal:`ONGOING` condition only, period in seconds between alerts of ongoing conditions.


  limit (optional, int, None)
    Required with :literal:`NEW EVENTS` condition only, limits the number of alerts sent as events are added.


  severities (optional, list, None)
    Severities to be alerted.


  transient (optional, int, None)
    Any event group lasting less than this many seconds is deemed transient and will not generate alerts under this condition.


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
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: To create the a new alert condition
      dellemc.powerscale.alert_rule:
        onefs_host: "{{ onefs_host }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        validate_certs: "{{ validate_certs }}"
        state: present
        name: alert_rule_new
        condition: NEW
        categories:
          - all
          - SYS_DISK_EVENTS
        channels:
          - SupportAssist
        eventgroup_ids:
          - 100010001
          - 100010002
          - 100010003
        exclude_eventgroup_ids:
          - 100010005
        interval: 11
        transient: 10
        limit: 10
        severities:
          - emergency

    - name: To update the existing alert condition
      dellemc.powerscale.alert_rule:
        onefs_host: "{{ onefs_host }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        validate_certs: "{{ validate_certs }}"
        state: present
        name: alert_rule_new
        condition: NEW
        categories:
          - all
          - SYS_DISK_EVENTS
          - NODE_STATUS_EVENTS
        channels:
          - SupportAssist
        eventgroup_ids:
          - 100010001
          - 100010002
        exclude_eventgroup_ids:
          - 100010005
        interval: 1100
        transient: 10
        limit: 10
        severities:
          - emergency
          - critical

    - name: To delete the existing alert condition
      dellemc.powerscale.alert_rule:
        onefs_host: "{{ onefs_host }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        validate_certs: "{{ validate_certs }}"
        state: absent
        name: alert_rule_new



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


alert_conditions (always, dict, {'name': 'alert_rule_new', 'condition': 'NEW', 'categories': ['all', 'SYS_DISK_EVENTS'], 'channels': ['SupportAssist'], 'eventgroup_ids': ['100010001', '100010002', '100010003'], 'exclude_eventgroup_ids': ['100010005'], 'interval': 11, 'limit': 10, 'severities': ['emergency'], 'transient': 10})
  The alert condition details.


  name (, str, )
    The name of the alert condition.


  condition (, str, )
    The condition of the alert condition.


  categories (, list, )
    The categories of the alert condition.


  channels (, list, )
    The channels of the alert condition.


  eventgroup_ids (, list, )
    The event group IDs of the alert condition.


  exclude_eventgroup_ids (, list, )
    The event group categories of the alert condition.


  interval (, int, )
    The interval of the alert condition.


  limit (, int, )
    The limit of the alert condition.


  severities (, list, )
    The severities of the alert condition.


  transient (, int, )
    The transient of the alert condition.






Status
------





Authors
~~~~~~~

- Felix Stephen (@felixs88) <ansible.team@dell.com>
- Saksham Nautiyal (@Saksham-Nautiyal)

