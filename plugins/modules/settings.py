#!/usr/bin/python
# Copyright: (c) 2021, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

""" Ansible module for managing genaral settings on PowerScale"""
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: settings

version_added: "1.4.0"

short_description: Manages general settings for PowerScale storage system
description:
- Managing general settings on the PowerScale storage system which includes the following.
- Get and update operations for email settings.
- Add remove and get operations for NTP servers.
- Get and update operation for cluster identity.
- Get and update operation for cluster owner.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Meenakshi Dembi (@dembim) <ansible.team@dell.com>

options:
  mail_relay:
    description:
    - The address of the SMTP server to be used for relaying the notification messages.
    - An SMTP server is required in order to send notifications.
    - If this str is empty, no emails will be sent.
    type: str
  mail_sender:
    description:
    - The full email address that will appear as the sender of notification messages.
    type: str
  mail_subject:
    description:
    - The subject line for notification messages from this cluster.
    type: str
  email_settings:
    description:
    - (deprecated) This is an addition flag to view the email settings.
    - This option is deprecated and will be removed in the later version.
    type: bool
  ntp_servers:
    description:
    - List of NTP servers which need to be configured.
    type: list
    elements: str
  state:
    description:
    - The state option is used to mention the existence of pool.
    type: str
    choices: [absent, present]
    default: present
  ntp_server_id:
    description:
    - ID of NTP server.
    type: str
  name:
    description:
    - Name of PowerScale Cluster.
    type: str
  description:
    description:
    - Description of PowerScale Cluster.
    type: str
  logon_details:
    description:
    - Details related to login to the Powerscale Cluster.
    type: dict
    suboptions:
      message_title:
        description:
        - Message to be shown on the login screen.
        type: str
      description:
        description:
        - Message description to be shown on the login screen.
        type: str
  company:
    description:
    - Name of the company.
    type: str
  location:
    description:
    - Location of the company.
    type: str
  primary_contact:
    description:
    - Contact details of primary system admin.
    type: dict
    suboptions:
      name:
        description:
        - Name of primary system admin.
        type: str
      phone1:
        description:
        - Phone1 of primary system admin.
        type: str
      phone2:
        description:
        - Phone2 of primary system admin.
        type: str
      email:
        description:
        - Email of primary system admin.
        type: str
  secondary_contact:
    description:
    - Contact details of secondary system admin.
    type: dict
    suboptions:
      name:
        description:
        - Name of secondary system admin.
        type: str
      phone1:
        description:
        - Phone1 of secondary system admin.
        type: str
      phone2:
        description:
        - Phone2 of secondary system admin.
        type: str
      email:
        description:
        - Email of secondary system admin.
        type: str
notes:
- The I(check_mode) is supported.
'''

EXAMPLES = r'''
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
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: Always
    type: bool
    sample: "false"

email_settings:
    description: Details of the email settings.
    type: dict
    returned: Always
    contains:
        settings:
            description: Details of the settings.
            returned: Always
            type: dict
            contains:
                batch_mode:
                    description: This setting determines how notifications will be batched together to be sent by email.
                    type: str
                mail_relay:
                    description: The address of the SMTP server to be used for relaying the notification messages.
                    type: str
                mail_sender:
                    description: The full email address that will appear as the sender of notification messages.
                    type: str
                mail_subject:
                    description: The subject line for notification messages from this cluster.
                    type: str
                smtp_auth_passwd_set:
                    description: Indicates if an SMTP authentication password is set.
                    type: bool
                smtp_auth_security:
                    description: The type of secure communication protocol to use if SMTP is being used.
                    type: str
                smtp_auth_username:
                    description: Username to authenticate with if SMTP authentication is being used.
                    type: str
                smtp_port:
                    description: The port on the SMTP server to be used for relaying the notification messages.
                    type: int
                use_smtp_auth:
                    description: If true, this cluster will send SMTP authentication credentials to the
                                SMTP relay server in order to send its notification emails.
                    type: bool
                user_template:
                    description: Location of a custom template file that can be used to specify the layout of the notification emails.
                    type: str
    sample:
        {
            "settings": {
                "batch_mode": "none",
                "mail_relay": "10.**.**.**",
                "mail_sender": "powerscale@dell.com",
                "mail_subject": "Powerscale Cluster notifications",
                "smtp_auth_passwd_set": false,
                "smtp_auth_security": "none",
                "smtp_auth_username": "",
                "smtp_port": 25,
                "use_smtp_auth": false,
                "user_template": ""
            }
        }

ntp_servers:
    description: List of NTP servers.
    type: dict
    returned: Always
    contains:
        servers:
            description: List of servers.
            type: list
            contains:
                id:
                    description: Field id.
                    type: str
                key:
                    description: Key value from I(key_file) that maps to this server.
                    type: str
                name:
                    description: NTP server name.
                    type: str
    sample:
        {
            "servers": [
                {
                    "id": "10.**.**.**",
                    "key": null,
                    "name": "10.**.**.**"
                }
            ]
        }
cluster_identity:
    description: Details related to cluster identity.
    type: dict
    returned: Always
    contains:
        description:
            description: Description of PowerScale cluster.
            type: str
        logon:
            description: Details of logon message shown on Powerscale login screen.
            type: dict
            contains:
                motd:
                    description: Details of logon message.
                    type: str
                motd_header:
                    description: Details of logon message title.
                    type: str
        mttdl_level_msg:
            description: mttdl_level_msg.
            type: str
        name:
            description: Name of PowerScale cluster.
            type: str
    sample:
        {
           "cluster_identity":
           {
                "description": "asdadasdasdasdadadadds",
                "logon":
                {
                    "motd": "This is new description",
                    "motd_header": "This is the new title"
                },
                "mttdl_level_msg": "none",
                "name": "PIE-IsilonS-24241-Clusterwrerwerwrewr"
            }
        }
cluster_owner:
    description: Details related to cluster identity.
    type: dict
    returned: Always
    contains:
        company:
            description: Name of the company.
            type: str
        location:
            description: Location of the company.
            type: str
        primary_email:
            description: Email of primary system admin.
            type: str
        primary_name:
            description: Name of primary system admin.
            type: str
        primary_phone1:
            description: Phone1 of primary system admin.
            type: str
        primary_phone2:
            description: Phone2 of primary system admin.
            type: str
        secondary_email:
            description: Email of secondary system admin.
            type: str
        secondary_name:
            description: Name of secondary system admin.
            type: str
        secondary_phone1:
            description: Phone1 of secondary system admin.
            type: str
        secondary_phone2:
            description: Phone2 of secondary system admin.
            type: str
    sample:
        {
           "cluster_owner":
           {
                "company": "Test company",
                "location": "Test location",
                "primary_email": "primary_email@email.com",
                "primary_name": "primary_name",
                "primary_phone1": "primary_phone1",
                "primary_phone2": "primary_phone2",
                "secondary_email": "secondary_email@email.com",
                "secondary_name": "secondary_name",
                "secondary_phone1": "secondary_phone1",
                "secondary_phone2": "secondary_phone2"
            }
        }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.powerscale_base \
    import PowerScaleBase
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.protocol \
    import Protocol
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.cluster \
    import Cluster
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('settings')


class Settings(PowerScaleBase):

    '''Class to manage Settings of Powerscale Cluster'''

    def __init__(self):
        ''' Define all parameters required by this module'''

        ansible_module_params = {
            'argument_spec': self.get_setting_parameters(),
            'supports_check_mode': True
        }

        super().__init__(AnsibleModule, ansible_module_params)

        self.result = {
            "changed": False,
            "email_settings": {},
            "ntp_servers": {},
            "cluster_owner": {},
            "cluster_identity": {}
        }

    def get_email_settings(self):
        """
        Get cluster email settings
        :return: Cluster email settings.
        """
        return Cluster(self.cluster_api, self.module).get_email_settings()

    def get_cluster_identity_details(self):
        """
        Get cluster identity details
        :return: Cluster identity details.
        """
        return Cluster(self.cluster_api, self.module).get_cluster_identity_details()

    def get_cluster_owner_details(self):
        """
        Get cluster owner details
        :return: Cluster owner details.
        """
        return Cluster(self.cluster_api, self.module).get_cluster_owner_details()

    def update_email_settings(self, email_params):
        """
        Update cluster email settings
        :param email_params: Cluster email body
        :return: True when email settings are updated successfully
        """
        try:
            if not self.module.check_mode:
                self.cluster_api.update_cluster_email(email_params)
            return self.get_email_settings()
        except Exception as e:
            error_message = f"Modifying email setting failed with error: {utils.determine_error(e)}"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def add_ntp_server(self, server):
        """
        Add NTP server
        :param server: Dictionary of parameters used for add NTP server
        :return: None
        """
        try:
            if not self.module.check_mode:
                self.protocol_api.create_ntp_server(server)
        except Exception as e:
            error_message = f"Failed to add NTP server: {utils.determine_error(e)}"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_ntp_server(self, server_id):
        """
        Get NTP server
        :param server_id: ID or name of NTP server
        :return: Details of the NTP Server
        """
        try:
            if server_id:
                server_details = self.protocol_api.get_ntp_server(server_id)
                return server_details.to_dict()
        except Exception as e:
            error_message = f"Failed to get NTP server: {utils.determine_error(e)}"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_ntp_servers(self):
        """
        Get NTP servers
        :return: List of all the NTP Servers
        """
        return Protocol(self.protocol_api, self.module).get_ntp_server_list()

    def delete_ntp_server(self, server_id):
        """
        Delete NTP server
        :param server_id: ID or name of NTP server
        :return: True when delete operation is successful
        """
        try:
            if not self.module.check_mode:
                self.protocol_api.delete_ntp_server(server_id)
            return True
        except Exception as e:
            error_message = f"Deleting NTP server failed with error {utils.determine_error(e)}"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_setting_parameters(self):
        return dict(
            state=dict(type='str', choices=['present', 'absent'], default='present'),
            mail_relay=dict(type='str'),
            mail_sender=dict(type='str'),
            mail_subject=dict(type='str'),
            email_settings=dict(type='bool'),
            ntp_servers=dict(type='list', elements='str'),
            ntp_server_id=dict(type='str'),
            name=dict(type='str'),
            description=dict(type='str'),
            logon_details=dict(type='dict', options=dict(
                message_title=dict(type='str'),
                description=dict(type='str'))),
            company=dict(type='str'),
            location=dict(type='str'),
            primary_contact=dict(type='dict', options=dict(
                name=dict(type='str'),
                phone1=dict(type='str'),
                phone2=dict(type='str'),
                email=dict(type='str'))),
            secondary_contact=dict(type='dict', options=dict(
                name=dict(type='str'),
                phone1=dict(type='str'),
                phone2=dict(type='str'),
                email=dict(type='str')))
        )

    def getting_configured_ntp_server(self):
        ntp_server_list_system = []
        ntp_servers = self.get_ntp_servers()
        if ntp_servers:
            for index in range(len(ntp_servers['servers'])):
                ntp_server_list_system.append(ntp_servers['servers'][index]['name'])
        return ntp_server_list_system

    def construct_ntp_server_payload(self, ntp_server_details, ntp_server):
        """
        Constructs NTP server body
        :param ntp_server: ID or Name of NTP server which is to be added.
        :return: Dictionary which has the details of the NTP server.
        """
        ntp_servers_list = self.getting_configured_ntp_server()
        ntp_servers_final = (list(set(ntp_server) - set(ntp_servers_list)))
        return ntp_servers_final

    def get_ntp_server_dict(self, ntp_server):
        ntp_server_dict = dict(name=ntp_server)
        return ntp_server_dict

    def validate_input(self, settings_params):
        """
        Validate input.
        :params settings_params: All the input params
        """
        if settings_params["ntp_servers"]:
            self.validate_ntp_server(settings_params)

        if settings_params['name'] and len(settings_params['name']) > 40:
            self.module.fail_json(msg="The maximum length for name is 40")

        if settings_params['description'] and len(settings_params['description']) > 255:
            self.module.fail_json(msg="The maximum length for description is 255")

        keys = ["primary_contact", "secondary_contact"]
        for item in keys:
            if settings_params[item] and settings_params[item]["email"] and utils.is_email_address_valid(settings_params[item]["email"]):
                error_message = item + ' email is not in the correct format'
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

        if settings_params["mail_sender"] and utils.is_email_address_valid(settings_params["mail_sender"]):
            error_message = 'Email address of mail_sender is not in the correct format'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def validate_ntp_server(self, settings_params):
        for server in settings_params["ntp_servers"]:
            if utils.is_input_empty(server):
                error_message = 'Please provide valid value for NTP server'
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

    def do_update(self, source, target):
        return source and source != target

    def form_modify_email_dict(self, settings_params, email_settings):
        email_setting_keys = ['mail_relay', 'mail_sender', 'mail_subject']
        email_params = {}
        for setting in email_setting_keys:
            if setting in email_setting_keys and \
                    self.do_update(settings_params[setting], email_settings['settings'][setting]):
                email_params[setting] = settings_params[setting]
        return email_params

    def form_modify_cluster_identity_dict(self, settings_params, cluster_identity_details):
        cluster_identity_keys = ['name', 'description']
        cluster_identity = {}
        if 'logon' not in cluster_identity:
            cluster_identity['logon'] = dict()

        for items in cluster_identity_keys:
            if items in cluster_identity_keys and \
                    self.do_update(settings_params[items], cluster_identity_details[items]):
                cluster_identity[items] = settings_params[items]

        test_dict = {'description': 'motd', 'message_title': 'motd_header'}

        if settings_params['logon_details']:
            for key in test_dict.keys():
                if key in settings_params['logon_details'] and settings_params['logon_details'][key] != cluster_identity_details['logon'][test_dict[key]]:
                    cluster_identity['logon'][test_dict[key]] = settings_params['logon_details'][key]

        if cluster_identity['logon'] == dict():
            del cluster_identity['logon']
        return cluster_identity

    def modify_cluster_identity(self, modify_dict):
        """
        Update cluster identity
        :param modify_dict: cluster identity dict
        :return: True when delete operation is successful
        """
        try:
            if not self.module.check_mode:
                self.cluster_api.update_cluster_identity(modify_dict)
            return self.get_cluster_identity_details()
        except Exception as e:
            error_message = f"Updating cluster identity failed with error {utils.determine_error(e)}"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def form_modify_cluster_owner_dict(self, settings_params, cluster_owner_details):
        cluster_owner_keys = ['company', 'location']
        cluster_owner = {}
        contact = ['primary_contact', 'secondary_contact']

        contact_dict_keys = ['name', 'phone1', 'phone2', 'email']

        for item in contact:
            if item not in cluster_owner:
                cluster_owner[item] = dict()

        for items in cluster_owner_keys:
            if items in cluster_owner_keys and \
                    self.do_update(settings_params[items], cluster_owner_details[items]):
                cluster_owner[items] = settings_params[items]

        for key in contact_dict_keys:
            self.get_modified_value(settings_params, key, cluster_owner, cluster_owner_details)

        for item in contact:
            if cluster_owner[item] == dict():
                del cluster_owner[item]

        return cluster_owner

    def get_modified_value(self, settings_params, key, cluster_owner, cluster_owner_details):
        if settings_params['primary_contact'] and settings_params['primary_contact'][key] \
                and settings_params['primary_contact'][key] != cluster_owner_details['primary_' + key]:
            cluster_owner['primary_' + key] = settings_params['primary_contact'][key]

        if settings_params['secondary_contact'] and settings_params['secondary_contact'][key] \
                and settings_params['secondary_contact'][key] != cluster_owner_details['secondary_' + key]:
            cluster_owner['secondary_' + key] = settings_params['secondary_contact'][key]

    def modify_cluster_owner(self, modify_dict):
        """
        Update cluster owner
        :param modify_dict: cluster owner dict
        :return: True when delete operation is successful
        """
        try:
            if not self.module.check_mode:
                self.cluster_api.update_cluster_owner(modify_dict)
            return self.get_cluster_owner_details()
        except Exception as e:
            error_message = f"Updating cluster owner failed with error {utils.determine_error(e)}"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)


class SettingsExitHandler():
    def handle(self, settings_obj, settings_details):
        settings_obj.result["cluster_identity"] = settings_details['cluster_identity_details']
        settings_obj.result["cluster_owner"] = settings_details['cluster_owner_details']
        settings_obj.result["email_settings"] = settings_details['email_settings']
        settings_obj.result["ntp_servers"] = settings_details['ntp_server_details']
        settings_obj.module.exit_json(**settings_obj.result)


class SettingsDeleteHandler():
    def handle(self, settings_obj, settings_params, settings_details):
        if settings_params['state'] == 'absent' and settings_details['ntp_server_details']:
            existing_ntp_servers = settings_obj.getting_configured_ntp_server()
            ntp_servers_to_be_removed = (list(set(settings_params['ntp_servers']).intersection(existing_ntp_servers)))
            for ntp_server in ntp_servers_to_be_removed:
                settings_obj.delete_ntp_server(ntp_server)
                settings_obj.result['changed'] = True
            settings_details['ntp_server_details'] = settings_obj.get_ntp_servers()

        SettingsExitHandler().handle(settings_obj, settings_details)


class SettingsModifyHandler():
    def handle_email_settings(self, settings_obj, settings_params, settings_details):
        if settings_params['state'] == 'present' and settings_details['email_settings']:
            modify_email_dict = settings_obj.form_modify_email_dict(settings_params, settings_details['email_settings'])
            if modify_email_dict:
                settings_params['email_settings'] = settings_obj.update_email_settings(modify_email_dict)
                settings_obj.result['changed'] = True

    def handle_cluster_identity(self, settings_obj, settings_params, settings_details):
        if settings_params['state'] == 'present' and settings_details['cluster_identity_details']:
            modify_cluster_identity_dict = settings_obj.form_modify_cluster_identity_dict(settings_params, settings_details['cluster_identity_details'])
            if modify_cluster_identity_dict:
                settings_details['cluster_identity_details'] = settings_obj.modify_cluster_identity(modify_cluster_identity_dict)
                settings_obj.result['changed'] = True

    def handle_cluster_owner(self, settings_obj, settings_params, settings_details):
        if settings_params['state'] == 'present' and settings_details['cluster_owner_details']:
            modify_cluster_owner_dict = settings_obj.form_modify_cluster_owner_dict(settings_params, settings_details['cluster_owner_details'])
            if modify_cluster_owner_dict:
                settings_details['cluster_owner_details'] = settings_obj.modify_cluster_owner(modify_cluster_owner_dict)
                settings_obj.result['changed'] = True

    def handle(self, settings_obj, settings_params, settings_details):
        self.handle_email_settings(settings_obj, settings_params, settings_details)
        self.handle_cluster_identity(settings_obj, settings_params, settings_details)
        self.handle_cluster_owner(settings_obj, settings_params, settings_details)

        SettingsDeleteHandler().handle(settings_obj, settings_params, settings_details)


class SettingsCreateHandler():
    def handle(self, settings_obj, settings_params, settings_details):
        if settings_params['state'] == 'present' and settings_params['ntp_servers']:
            add_ntp_server_payload = settings_obj.construct_ntp_server_payload(settings_details['ntp_server_details'], settings_params['ntp_servers'])
            for item in add_ntp_server_payload:
                list_to_be = settings_obj.get_ntp_server_dict(item)
                settings_obj.add_ntp_server(list_to_be)
                settings_obj.result['changed'] = True
            settings_details['ntp_server_details'] = settings_obj.get_ntp_servers()

        SettingsModifyHandler().handle(settings_obj, settings_params, settings_details)


class SettingsHandler():
    def set_initial_data(self, settings_obj):
        data_dict = {'email_settings': None,
                     'ntp_server_details': None,
                     'cluster_identity_details': None,
                     'cluster_owner_details': None}
        data_dict['email_settings'] = settings_obj.get_email_settings()
        data_dict['ntp_server_details'] = settings_obj.get_ntp_servers()
        data_dict['cluster_identity_details'] = settings_obj.get_cluster_identity_details()
        data_dict['cluster_owner_details'] = settings_obj.get_cluster_owner_details()
        return data_dict

    def handle(self, settings_obj, settings_params):
        settings_obj.validate_input(settings_params)
        settings_details = self.set_initial_data(settings_obj)
        SettingsCreateHandler().handle(settings_obj, settings_params, settings_details)


def main():
    """ Create PowerScale Settings object and perform action on it
        based on user input from playbook."""
    obj = Settings()
    SettingsHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
