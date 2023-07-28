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
- Managing general settings on the PowerScale storage system which includes get and update operations for
  email settings and add, remove and get operations for NTP servers.

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
    - This is an addition flag to view the email settings.
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
    required: true
    choices: [absent, present]
  ntp_server_id:
    description:
    - ID of NTP server.
    type: str
notes:
- The I(check_mode) is not supported.
'''

EXAMPLES = r'''
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

ntp_server:
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
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('settings')


class Settings(object):
    """Class with general setting operations"""

    def __init__(self):
        """ Define all parameters required by this module"""

        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_setting_parameters())

        # initialize the ansible module
        self.module = AnsibleModule(argument_spec=self.module_params)

        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        LOG.info('Got python SDK instance for provisioning on PowerScale')
        self.cluster_api = self.isi_sdk.ClusterApi(self.api_client)
        self.protocol_api = self.isi_sdk.ProtocolsApi(self.api_client)

    def get_email_settings(self):
        """
        Get cluster email settings
        :return: Cluster email settings.
        """
        try:
            email_details = self.cluster_api.get_cluster_email()
            return email_details.to_dict()
        except Exception as e:
            error_message = 'Failed to get the details of email settings %s,' % (str(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def update_email_settings(self, email_params):
        """
        Update cluster email settings
        :param email_params: Cluster email body
        :return: True when email settings are updated successfully
        """
        try:
            self.cluster_api.update_cluster_email(email_params)
            return True
        except Exception as e:
            error_message = 'Modifying email setting failed with error %s,' % (str(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def add_ntp_server(self, server):
        """
        Add NTP server
        :param server: Dictionary of parameters used for add NTP server
        :return: None
        """
        try:
            self.protocol_api.create_ntp_server(server)
        except Exception as e:
            error_message = 'Failed to add NTP server %s %s' % (server, str(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_ntp_server(self, server_id):
        """
        Get NTP server
        :param server_id: ID or name of NTP server
        :return: Details of the NTP Server
        """
        try:
            server_details = self.protocol_api.get_ntp_server(server_id)
            return server_details.to_dict()
        except Exception as e:
            error_message = 'Failed to get NTP server %s %s' % (server_id, str(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_ntp_servers(self):
        """
        Get NTP servers
        :return: List of all the NTP Servers
        """
        try:
            server_details = self.protocol_api.list_ntp_servers()
            return server_details.to_dict()
        except Exception as e:
            error_message = 'Failed to get NTP servers %s' % (str(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete_ntp_server(self, server_id):
        """
        Delete NTP server
        :param server_id: ID or name of NTP server
        :return: True when delete operation is successful
        """
        try:
            self.protocol_api.delete_ntp_server(server_id)
            return True
        except Exception as e:
            error_message = 'Deleting NTP server %s failed with error %s' % (server_id, str(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def construct_ntp_server_body(self, ntp_server):
        """
        Constructs NTP server body
        :param ntp_server: ID or Name of NTP server which is to be added.
        :return: Dictionary which has the details of the NTP server.
        """
        ntp_server_dict = dict(name=ntp_server)
        return ntp_server_dict

    def validate_input(self, ntp_servers):
        """
        Validate input.
        :params ntp_servers: ID or Name of NTP server
        """
        for server in ntp_servers:
            if utils.is_input_empty(server):
                error_message = 'Please provide valid value for NTP server'
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

    def do_update(self, source, target):
        return source and source != target

    def perform_module_operation(self):
        """
        Perform different actions based on parameters chosen in playbook
        """
        result = dict(
            changed=False,
            email_settings='',
            ntp_server='',
        )
        state = self.module.params['state']
        mail_relay = self.module.params['mail_relay']
        mail_sender = self.module.params['mail_sender']
        mail_subject = self.module.params['mail_subject']
        ntp_servers = self.module.params['ntp_servers']
        ntp_server_id = self.module.params['ntp_server_id']
        email_settings = self.module.params['email_settings']

        email_setting_keys = ['mail_relay', 'mail_sender', 'mail_subject']
        ntp_server_list_system = []
        ntp_servers_final = None
        ntp_server_details = self.get_ntp_servers()
        existing_email_settings = self.get_email_settings()

        email_params = {}
        if existing_email_settings:
            for setting in email_setting_keys:
                if setting in self.module.params.keys() and \
                        self.do_update(self.module.params[setting], existing_email_settings['settings'][setting]):
                    email_params[setting] = self.module.params[setting]

        if ntp_server_details:
            for index in range(len(ntp_server_details['servers'])):
                ntp_server_list_system.append(ntp_server_details['servers'][index]['name'])

        if state == "absent" and (email_settings or mail_relay or mail_sender or mail_subject):
            error_message = 'Deletion of email settings is not valid operation'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

        if email_params and state == 'present':
            result['changed'] = self.update_email_settings(email_params)
            result['email_settings'] = self.get_email_settings()

        if ntp_servers and state == 'present':
            self.validate_input(ntp_servers)
            ntp_servers_final = (list(set(ntp_servers) - set(ntp_server_list_system)))
            for ntp_server in ntp_servers_final:
                server_details_to_update = self.construct_ntp_server_body(ntp_server)
                self.add_ntp_server(server_details_to_update)
                result['changed'] = True
            result['ntp_server'] = self.get_ntp_servers()

        if (ntp_server_details['total'] != 0) and state == 'absent' and ntp_servers:
            ntp_servers_to_be_removed = (list(set(ntp_servers).intersection(ntp_server_list_system)))
            if ntp_servers_to_be_removed:
                for ntp_server in ntp_servers_to_be_removed:
                    self.delete_ntp_server(ntp_server)
                result['changed'] = True
            result['ntp_server'] = self.get_ntp_servers()

        if email_settings and state == 'present':
            result['email_settings'] = existing_email_settings

        if ntp_server_id and state == 'present':
            result['ntp_server'] = self.get_ntp_server(ntp_server_id)

        self.module.exit_json(**result)


def get_setting_parameters():
    """This method provide parameter required for the managing genaral
    settings on PowerScale"""
    return dict(
        state=dict(required=True, type='str', choices=['absent', 'present']),
        mail_relay=dict(type='str'),
        mail_sender=dict(type='str'),
        mail_subject=dict(type='str'),
        ntp_servers=dict(type='list', elements='str'),
        ntp_server_id=dict(type='str'),
        email_settings=dict(type='bool')
    )


def main():
    """ Create PowerScale Setting object and perform actions on it
        based on user input from playbook"""
    obj = Settings()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
