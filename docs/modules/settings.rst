.. _settings_module:


settings -- Manages general settings for PowerScale storage system
==================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing general settings on the PowerScale storage system which includes get and update operations for email settings and add, remove and get operations for NTP servers.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.14 or later.
- Python 3.9, 3.10 or 3.11.



Parameters
----------

  mail_relay (optional, str, None)
    The address of the SMTP server to be used for relaying the notification messages.

    An SMTP server is required in order to send notifications.

    If this str is empty, no emails will be sent.


  mail_sender (optional, str, None)
    The full email address that will appear as the sender of notification messages.


  mail_subject (optional, str, None)
    The subject line for notification messages from this cluster.


  email_settings (optional, bool, None)
    This is an addition flag to view the email settings.


  ntp_servers (optional, list, None)
    List of NTP servers which need to be configured.


  state (True, str, None)
    The state option is used to mention the existence of pool.


  ntp_server_id (optional, str, None)
    ID of NTP server.


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
   - The *check_mode* is not supported.
   - The modules present in this collection named as 'dellemc.powerscale' are built to support the Dell PowerScale storage platform.




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get email settings
      dellemc.powerscale.settings:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        email_settings: "{{email_settings}}"
        state: "{{state_present}}"

    - name: Update email settings
      dellemc.powerscale.settings:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        state: "{{state_present}}"
        mail_relay: "mailrelay.itp.dell.com"
        mail_sender: "lab-a2@dell.com"
        mail_subject: "lab-a2-alerts"

    - name: Add NTP server
      dellemc.powerscale.settings:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        ntp_servers:
          - "10.106.**.***"
          - "10.106.**.***"
        state: "{{state_present}}"

    - name: Add NTP server - Idempotency
      dellemc.powerscale.settings:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        ntp_servers:
          - "10.106.**.***"
          - "10.106.**.***"
        state: "{{state_present}}"

    - name: Get NTP server
      dellemc.powerscale.settings:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        ntp_server_id: "10.106.**.***"
        state: "{{state_present}}"

    - name: Remove NTP server
      dellemc.powerscale.settings:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        ntp_servers:
          - "10.106.**.***"
          - "10.106.**.***"
        state: "{{state_absent}}"

    - name: Remove NTP server - Idempotency
      dellemc.powerscale.settings:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        ntp_servers:
          - "10.106.**.***"
          - "10.106.**.***"
        state: "{{state_absent}}"

    - name: Update email settings and add NTP server
      dellemc.powerscale.settings:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        state: "{{state_present}}"
        mail_relay: "mailrelay.itp.dell.com"
        mail_sender: "lab-a2@dell.com"
        mail_subject: "lab-a2-alerts"
        ntp_servers:
          - "10.106.**.***"
          - "10.106.**.***"



Return Values
-------------

changed (Always, bool, false)
  Whether or not the resource has changed.


email_settings (Always, dict, {'settings': {'batch_mode': 'none', 'mail_relay': '10.**.**.**', 'mail_sender': 'powerscale@dell.com', 'mail_subject': 'Powerscale Cluster notifications', 'smtp_auth_passwd_set': False, 'smtp_auth_security': 'none', 'smtp_auth_username': '', 'smtp_port': 25, 'use_smtp_auth': False, 'user_template': ''}})
  Details of the email settings.


  settings (Always, dict, )
    Details of the settings.


    batch_mode (, str, )
      This setting determines how notifications will be batched together to be sent by email.


    mail_relay (, str, )
      The address of the SMTP server to be used for relaying the notification messages.


    mail_sender (, str, )
      The full email address that will appear as the sender of notification messages.


    mail_subject (, str, )
      The subject line for notification messages from this cluster.


    smtp_auth_passwd_set (, bool, )
      Indicates if an SMTP authentication password is set.


    smtp_auth_security (, str, )
      The type of secure communication protocol to use if SMTP is being used.


    smtp_auth_username (, str, )
      Username to authenticate with if SMTP authentication is being used.


    smtp_port (, int, )
      The port on the SMTP server to be used for relaying the notification messages.


    use_smtp_auth (, bool, )
      If true, this cluster will send SMTP authentication credentials to the SMTP relay server in order to send its notification emails.


    user_template (, str, )
      Location of a custom template file that can be used to specify the layout of the notification emails.




ntp_server (Always, dict, {'servers': [{'id': '10.**.**.**', 'key': None, 'name': '10.**.**.**'}]})
  List of NTP servers.


  servers (, list, )
    List of servers.


    id (, str, )
      Field id.


    key (, str, )
      Key value from *key_file* that maps to this server.


    name (, str, )
      NTP server name.







Status
------





Authors
~~~~~~~

- Meenakshi Dembi (@dembim) <ansible.team@dell.com>

