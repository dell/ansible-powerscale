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

    Optional when I(state) is C(query).


  state (True, str, None)
    The desired state of the event alert suppression.

    C(suppressed) - suppress alerting for the specified event ID.

    C(unsuppressed) - un-suppress alerting for the specified event ID.

    C(query) - query the current suppression state.

    Choices: ['suppressed', 'unsuppressed', 'query']



Notes
-----

.. note::
  - This module operates on a single event ID per task.
  - Bulk suppression of multiple event IDs is not supported.
  - Time-based suppression or auto-revert is not supported by the OneFS API.
  - Querying with I(event_id) returns only the suppression state. Event metadata such as name, category and description is returned only when querying all suppressed events.



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
        state: "query"

    - name: Query a specific event's suppression state
      dellemc.powerscale.event_alert_suppression:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        event_id: "100010001"
        state: "query"



Return Values
-------------

changed
    Whether or not the resource has changed.

    Returned: always

    Type: bool

    Sample: false



event_alert_suppression_details
    Details of the event alert suppression.

    Returned: always

    Type: complex

    Contains:

        suppressions (list)
            List of suppressed events.

            Returned: when I(state) is C(query) and I(event_id) is not provided

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



        total (int)
            Total count of suppressed events.

            Returned: when I(state) is C(query) and I(event_id) is not provided

            Type: int



        event_id (str)
            Event ID.

            Returned: when I(event_id) is provided

            Type: str



        suppressed (bool)
            Whether the event is currently suppressed.

            Returned: when I(event_id) is provided

            Type: bool



        would_change_to (bool)
            The suppression state that would be applied.

            Returned: when run in check mode and a change is required

            Type: bool


    Sample: {"event_id": "100010001", "suppressed": true}



msg
    Status message describing the operation performed.

    Returned: always

    Type: str

    Sample: Successfully suppressed event 100010001



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
