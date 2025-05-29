.. _alert_channel_module:


alert_channel -- Manage alert channel on a PowerScale Storage System
====================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing alert channel on a PowerScale system includes creating, modifying, deleting and retrieving details of alert channel.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.16 or later.
- Python 3.10, 3.11 or 3.12.



Parameters
----------

  allowed_nodes (optional, list, None)
    Nodes (LNNs) that can be masters for this channel.


  enabled (optional, bool, None)
    Enable or disable the channel.

    \ :literal:`True`\  indicates the channel is enabled.

    \ :literal:`False`\  indicates the channel is disabled.

    If not specified when creating the channel, it will be enabled by default.


  excluded_nodes (optional, list, None)
    Nodes (LNNs) that cannot be masters for this channel.


  name (True, str, None)
    Name of the Channel.

    Name should be unique and cannot be changed.


  send_test_alert (optional, bool, False)
    Send test alert to the channel.


  smtp_parameters (optional, dict, None)
    Parameters to be used for an SMTP channel.

    The \ :emphasis:`smtp\_parameters`\  is required when \ :emphasis:`type`\  is \ :literal:`smtp`\ .


    address (optional, list, None)
      Email address to send to.


    send_as (optional, str, None)
      Email address to use as from.


    subject (optional, str, None)
      Subject for emails.


    smtp_host (optional, str, None)
      SMTP relay host.


    smtp_port (optional, int, None)
      SMTP relay port. It defaults to 25.


    batch (optional, str, None)
      Batching criterion.


    batch_period (optional, int, None)
      Period over which batching is to be performed.


    smtp_use_auth (optional, bool, None)
      Enable SMTP authentication.

      If \ :emphasis:`smtp\_use\_auth`\  is not set during creation, then it defaults set to \ :literal:`false`\ .


    smtp_username (optional, str, None)
      Username for SMTP authentication, only if \ :emphasis:`smtp\_use\_auth`\  is \ :literal:`true`\ .


    smtp_password (optional, str, None)
      Password for SMTP authentication, only if \ :emphasis:`smtp\_use\_auth`\  is \ :literal:`true`\ .


    smtp_security (optional, str, None)
      Encryption protocol to use for SMTP.


    update_password (optional, str, always)
      This parameter controls the way the \ :emphasis:`smtp\_password`\  is updated during the creation and modification of alert channel.

      \ :literal:`always`\  will update password for each execution.

      \ :literal:`on\_create`\  will only set while creating a alert channel.

      For modifying \ :emphasis:`smtp\_password`\ , set the \ :emphasis:`update\_password`\  to \ :literal:`always`\ .



  state (optional, str, present)
    State of the channel.


  type (optional, str, None)
    Type of the channel.

    If \ :emphasis:`type`\  is \ :literal:`smtp`\ , then \ :emphasis:`smtp\_parameters`\  is required.

    If \ :emphasis:`type`\  is not set during creation, then it defaults to \ :literal:`connectemc`\ .


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
   - Idempotency is not supported with \ :emphasis:`send\_test\_alert`\  option.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create the SMTP alert channel
      dellemc.powerscale.alert_channel:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        name: "sample_event_channel"
        enabled: true
        type: "smtp"
        allowed_nodes:
          - 1
        excluded_nodes:
          - 2
        smtp_parameters:
          address:
            - "powerscale@sample.com"
          send_as: "smtp_alert_channel@sample.com"
          subject: "SMTP event channel"
          smtp_host: "smaple.powersacale.com"
          smtp_port: 25
          batch: "ALL"
          batch_period: 120
          smtp_use_auth: false
          update_password: "on_create"

    - name: Create the ConnectEMC channel
      dellemc.powerscale.alert_channel:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        name: "connect_emc_alert_channel"
        enabled: true
        type: "connectemc"
        allowed_nodes:
          - 1
        excluded_nodes:
          - 2

    - name: Get the alert channel details
      dellemc.powerscale.alert_channel:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        name: "sample_event_channel"
        state: "present"

    - name: Send the test alert message
      dellemc.powerscale.alert_channel:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        name: "sample_event_channel"
        send_test_alert: true

    - name: Modify the alert channel
      dellemc.powerscale.alert_channel:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        name: "sample_event_channel"
        enabled: false
        allowed_nodes:
          - 2
          - 3
        excluded_nodes:
          - 1

    - name: Delete the alert channel
      dellemc.powerscale.alert_channel:
        onefs_host: "{{ onefs_host }}"
        port_no: "{{ port_no }}"
        api_user: "{{ api_user }}"
        api_password: "{{ api_password }}"
        verify_ssl: "{{ verify_ssl }}"
        name: "sample_event_channel"
        state: "absent"



Return Values
-------------

changed (always, bool, false)
  A boolean indicating if the task had to make changes.


alert_channel_details (always, dict, {'allowed_nodes': [1, 2], 'enabled': True, 'excluded_nodes': [3], 'id': '1', 'name': 'sample_event_channel', 'parameters': {'address': ['sample.com'], 'batch': 'ALL', 'batch_period': 120, 'custom_template': 'sample', 'send_as': 'test@sample.com', 'smtp_host': 'sample.com', 'smtp_password': 'sample_password', 'smtp_port': 25, 'smtp_security': 'none', 'smtp_use_auth': False, 'smtp_username': 'sample-user', 'subject': 'sample'}, 'rules': [], 'system': False, 'type': 'smtp'})
  The updated alert channel details.


  allowed_nodes (, list, )
    Nodes (LNNs) that can be masters for this channel.


  enabled (, bool, )
    Channel is to be used or not.


  excluded_nodes (, list, )
    Nodes (LNNs) that can NOT be the masters for this channel.


  id (, str, )
    Unique identifier for the alert channel.


  name (, str, )
    Channel name.


  parameters (, dict, )
    A collection of parameters dependent on the channel type.


    address (, list, )
      Email addresses to send to.


    batch (, str, )
      Batching criterion.


    batch_period (, int, )
      Period over which batching is to be performed.


    custom_template (, str, )
      Path to custom notification template.


    send_as (, str, )
      Email address to use as from.


    smtp_host (, str, )
      SMTP relay host.


    smtp_password (, str, )
      Password for SMTP authentication - only if smtp\_use\_auth true.


    smtp_port (, int, )
      SMTP relay port. It defaults to 25.


    smtp_security (, str, )
      Encryption protocol to use for SMTP.


    smtp_use_auth (, bool, )
      Use SMTP authentication.


    smtp_username (, str, )
      Username for SMTP authentication - only if smtp\_use\_auth true.


    subject (, str, )
      Subject for emails.



  rules (, list, )
    Alert rules involving this alert channel.


  system (, bool, )
    Channel is a pre-defined system channel.


  type (, str, )
    The mechanism used by the channel.






Status
------





Authors
~~~~~~~

- Bhavneet Sharma (@Bhavneet-Sharma) <ansible.team@dell.com>

