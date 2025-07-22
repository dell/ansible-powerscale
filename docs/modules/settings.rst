.. _settings_module:


settings -- Manages general settings for PowerScale storage system
==================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Managing general settings on the PowerScale storage system which includes the following.

Get and update operations for email settings.

Add remove and get operations for NTP servers.

Get and update operation for cluster identity.

Get and update operation for cluster owner.



Requirements
------------
The below requirements are needed on the host that executes this module.

- A Dell PowerScale Storage system.
- Ansible-core 2.17 or later.
- Python 3.10, 3.11 or 3.12.



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
    (deprecated) This is an addition flag to view the email settings.

    This option is deprecated and will be removed in the later version.


  ntp_servers (optional, list, None)
    List of NTP servers which need to be configured.


  state (optional, str, present)
    The state option is used to mention the existence of pool.


  ntp_server_id (optional, str, None)
    ID of NTP server.


  name (optional, str, None)
    Name of PowerScale Cluster.


  description (optional, str, None)
    Description of PowerScale Cluster.


  logon_details (optional, dict, None)
    Details related to login to the Powerscale Cluster.


    message_title (optional, str, None)
      Message to be shown on the login screen.


    description (optional, str, None)
      Message description to be shown on the login screen.



  company (optional, str, None)
    Name of the company.


  location (optional, str, None)
    Location of the company.


  primary_contact (optional, dict, None)
    Contact details of primary system admin.


    name (optional, str, None)
      Name of primary system admin.


    phone1 (optional, str, None)
      Phone1 of primary system admin.


    phone2 (optional, str, None)
      Phone2 of primary system admin.


    email (optional, str, None)
      Email of primary system admin.



  secondary_contact (optional, dict, None)
    Contact details of secondary system admin.


    name (optional, str, None)
      Name of secondary system admin.


    phone1 (optional, str, None)
      Phone1 of secondary system admin.


    phone2 (optional, str, None)
      Phone2 of secondary system admin.


    email (optional, str, None)
      Email of secondary system admin.



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

    - name: Update cluster owner details
      dellemc.powerscale.settings:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        state: "{{state_present}}"
        company: "Test company"
        location: "Test location"
        primary_contact:
          name: "primary_name11"
          phone1: "primary_phone11"
          phone2: "primary_phone21"
          email: "primary_email1@email.com"
        secondary_contact:
          name: "secondary_name11"
          phone1: "secondary_phone11"
          phone2: "secondary_phone21"
          email: "secondary_email1@email.com"

    - name: Update cluster identity details
      dellemc.powerscale.settings:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        state: "{{state_present}}"
        name: "PIE-IsilonS-24241-Cluster"
        description: "This is new description for the cluster"
        logon_details:
          message_title: "This is the new title"
          description: "This is new description"

    - name: Update all settings
      dellemc.powerscale.settings:
        onefs_host: "{{onefs_host}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        verify_ssl: "{{verify_ssl}}"
        state: "{{state_present}}"
        name: "PIE-IsilonS-24241-Cluster"
        description: "This is new description for the cluster"
        logon_details:
          message_title: "This is the new title"
          description: "This is new description"
        company: "Test company"
        location: "Test location"
        primary_contact:
          name: "primary_name11"
          phone1: "primary_phone11"
          phone2: "primary_phone21"
          email: "primary_email1@email.com"
        secondary_contact:
          name: "secondary_name11"
          phone1: "secondary_phone11"
          phone2: "secondary_phone21"
          email: "secondary_email1@email.com"
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




ntp_servers (Always, dict, {'servers': [{'id': '10.**.**.**', 'key': None, 'name': '10.**.**.**'}]})
  List of NTP servers.


  servers (, list, )
    List of servers.


    id (, str, )
      Field id.


    key (, str, )
      Key value from :emphasis:`key\_file` that maps to this server.


    name (, str, )
      NTP server name.




cluster_identity (Always, dict, {'cluster_identity': {'description': 'asdadasdasdasdadadadds', 'logon': {'motd': 'This is new description', 'motd_header': 'This is the new title'}, 'mttdl_level_msg': 'none', 'name': 'PIE-IsilonS-24241-Clusterwrerwerwrewr'}})
  Details related to cluster identity.


  description (, str, )
    Description of PowerScale cluster.


  logon (, dict, )
    Details of logon message shown on Powerscale login screen.


    motd (, str, )
      Details of logon message.


    motd_header (, str, )
      Details of logon message title.



  mttdl_level_msg (, str, )
    mttdl\_level\_msg.


  name (, str, )
    Name of PowerScale cluster.



cluster_owner (Always, dict, {'cluster_owner': {'company': 'Test company', 'location': 'Test location', 'primary_email': 'primary_email@email.com', 'primary_name': 'primary_name', 'primary_phone1': 'primary_phone1', 'primary_phone2': 'primary_phone2', 'secondary_email': 'secondary_email@email.com', 'secondary_name': 'secondary_name', 'secondary_phone1': 'secondary_phone1', 'secondary_phone2': 'secondary_phone2'}})
  Details related to cluster identity.


  company (, str, )
    Name of the company.


  location (, str, )
    Location of the company.


  primary_email (, str, )
    Email of primary system admin.


  primary_name (, str, )
    Name of primary system admin.


  primary_phone1 (, str, )
    Phone1 of primary system admin.


  primary_phone2 (, str, )
    Phone2 of primary system admin.


  secondary_email (, str, )
    Email of secondary system admin.


  secondary_name (, str, )
    Name of secondary system admin.


  secondary_phone1 (, str, )
    Phone1 of secondary system admin.


  secondary_phone2 (, str, )
    Phone2 of secondary system admin.






Status
------





Authors
~~~~~~~

- Meenakshi Dembi (@dembim) <ansible.team@dell.com>

