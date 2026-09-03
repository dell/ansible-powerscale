.. _event_alert_suppression_module:


event_alert_suppression -- Manage event alert suppression on a PowerScale Storage System
========================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing event alert suppression on a PowerScale system includes suppressing, un-suppressing, and querying per-event alert suppression.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.17 or later.
- Python 3.11, 3.12 or 3.13.



Parameters
----------

  event_id (optional, str, None)
    The event type ID to suppress or un-suppress.

    Required when I(state) is C(suppressed) or C(unsuppressed).

    Optional when I(state) is C(get).


  state (True, str, None)
    The desired state of the event alert suppression.

    C(suppressed) - suppress alerting for the specified event ID.

    C(unsuppressed) - un-suppress alerting for the specified event ID.

    C(get) - query the current suppression state.

    Choices: ['suppressed', 'unsuppressed', 'get']



Notes
-----

.. note::
  - This module operates on a single event ID per task.
  - Bulk suppression of multiple event IDs is not supported.
  - Time-based suppression or auto-revert is not supported by the OneFS API.



Examples
--------

.. code-block:: yaml

    - name: Suppress an event alert
      dellemc.powerscale.event_alert_suppression:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        event_id: "100010001"
        state: "suppressed"

    - name: Un-suppress an event alert
      dellemc.powerscale.event_alert_suppression:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        event_id: "100010001"
        state: "unsuppressed"

    - name: Query all suppressed events
      dellemc.powerscale.event_alert_suppression:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        state: "get"

    - name: Query a specific event's suppression state
      dellemc.powerscale.event_alert_suppression:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        event_id: "100010001"
        state: "get"



Return Values
-------------

event_alert_suppression_details
    Details of the event alert suppression.

    Returned: always

    Type: complex

    Contains:

        suppressions (list)
            List of suppressed events (when querying all events).

            Returned: when state is C(get) and event_id is not provided

            Type: list

            Elements: dict

            Contains:

                id (str)
                    Event ID.


                name (str)
                    Event name.


                category (str)
                    Event category.


                description (str)
                    Event description.


                node (bool)
                    Whether the event is node-specific.


                suppressed (bool)
                    Whether the event is suppressed.



        event_id (str)
            Event ID (when querying a specific event).

            Returned: when state is C(get) and event_id is provided

            Type: str



        name (str)
            Event name (when querying a specific event).

            Returned: when state is C(get) and event_id is provided

            Type: str



        category (str)
            Event category (when querying a specific event).

            Returned: when state is C(get) and event_id is provided

            Type: str



        description (str)
            Event description (when querying a specific event).

            Returned: when state is C(get) and event_id is provided

            Type: str



        node (bool)
            Whether the event is node-specific (when querying a specific event).

            Returned: when state is C(get) and event_id is provided

            Type: bool



        suppressed (bool)
            Whether the event is suppressed (when querying a specific event).

            Returned: when state is C(get) and event_id is provided

            Type: bool



        total (int)
            Total count of suppressed events.

            Returned: when state is C(get) and event_id is not provided

            Type: int



changed
    Whether the module made any changes.

    Returned: always

    Type: bool



msg
    Status message.

    Returned: always

    Type: str



Status
------

.. module-support:: check-mode
.. module-support:: diff-mode

This module supports check mode.



Authors
------

Dell Technologies Ansible Team <ansible.team@dell.com>



See Also
--------

.. seealso::
   :ref:`alert_channel_module`


.. seealso::
   :ref:`alert_rule_module`
