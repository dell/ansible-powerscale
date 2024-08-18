#!/usr/bin/python
# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing alert channel on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: alert_channel

version_added: '3.3.0'

short_description: Manage alert channel on a PowerScale Storage System
description:
- Managing alert channel on a PowerScale system includes creating,
  modifying, deleting and retrieving details of alert channel.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
  - Bhavneet Sharma (@Bhavneet-Sharma) <ansible.team@dell.com>
options:
  allowed_nodes:
    description:
    - Nodes (LNNs) that can be masters for this channel.
    type: list
    elements: int
  enabled:
    description:
    - Enable or disable the channel.
    - C(True) indicates the channel is enabled.
    - C(False) indicates the channel is disabled.
    - If not specified when creating the channel, It will be
      enabled by default.
    type: bool
  excluded_nodes:
    description:
    - Nodes (LNNs) that cannot be masters for this channel.
    type: list
    elements: int
  name:
    description:
    - Name of the Channel.
    - Name should be unique and not modifiable.
    type: str
    required: true
  send_test_alert:
    description:
    - Send test alert to the channel.
    type: bool
    default: false
  smtp_parameters:
    description:
    - Parameters to be used for an SMTP channel.
    - The I(smtp_parameters) is required when I(type) is C(smtp).
    type: dict
    suboptions:
      address:
        description:
        - Email address to send to.
        type: list
        elements: str
        aliases:
          - send_to
      send_as:
        description:
        - Email address to use as from.
        type: str
        aliases:
          - send_from
      subject:
        description:
        - Subject for emails.
        type: str
      smtp_host:
        description:
        - SMTP relay host.
        type: str
      smtp_port:
        description:
        - SMTP relay port. It defaults to 25.
        type: int
      batch:
        description:
        - Batching criterion.
        type: str
        choices: ['NONE', 'ALL', 'CATEGORY', 'SEVERITY']
      batch_period:
        description:
        - Period over which batching is to be performed.
        type: int
      smtp_use_auth:
        description:
        - Enable SMTP authentication.
        - If I(smtp_use_auth) is not set during creation,
          then It defaults set to c(false).
        type: bool
      smtp_username:
        description:
        - Username for SMTP authentication, only if
          I(smtp_use_auth) is C(true).
        type: str
      smtp_password:
        description:
        - Password for SMTP authentication, only if
          I(smtp_use_auth) is C(true).
        type: str
      smtp_security:
        description:
        - Encryption protocol to use for SMTP.
        type: str
        choices: ['NONE', 'STARTTLS']
      update_password:
        description:
        - This parameter controls the way the I(smtp_password) is updated
          during the creation and modification of alert channel.
        - C(always) will update password for each execution.
        - C(on_create) will only set while creating a alert channel.
        - For modifying I(smtp_password), set the I(update_password) to
          C(always).
        choices: ['always', 'on_create']
        default: always
        type: str
  state:
    description:
    - State of the channel.
    type: str
    choices: ['present', 'absent']
    default: present
  type:
    description:
    - Type of the channel.
    - If I(type) is C(smtp), then I(smtp_parameters) is required.
    - If I(type) is not set during creation, then It defaults to C(connectemc).
    type: str
    choices: ['connectemc', 'smtp']
notes:
- The I(check_mode), I(check_diff) and idempotency is supported.
- Idempotency is not supported with I(send_test_alert) option.
'''

EXAMPLES = r'''
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
'''

RETURN = r'''
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
alert_channel_details:
    description: The updated alert channel details.
    type: dict
    returned: always
    contains:
      allowed_nodes:
        description: Nodes (LNNs) that can be masters for this channel.
        type: list
        elements: int
      enabled:
        description: Channel is to be used or not.
        type: bool
      excluded_nodes:
        description: Nodes (LNNs) that can NOT be the masters for this channel.
        type: list
        elements: int
      id:
        description: Unique identifier for the alert channel.
        type: str
      name:
        description: Channel name.
        type: str
      parameters:
        description: A collection of parameters dependent on the channel type.
        type: dict
        contains:
          address:
            description: Email addresses to send to.
            type: list
            elements: str
          batch:
            description: Batching criterion.
            type: str
          batch_period:
            description: Period over which batching is to be performed.
            type: int
          custom_template:
            description: Path to custom notification template.
            type: str
          send_as:
            description: Email address to use as from.
            type: str
          smtp_host:
            description: SMTP relay host.
            type: str
          smtp_password:
            description: Password for SMTP authentication - only if smtp_use_auth true.
            type: str
          smtp_port:
            description: SMTP relay port. It defaults to 25.
            type: int
          smtp_security:
            description: Encryption protocol to use for SMTP.
            type: str
          smtp_use_auth:
            description: Use SMTP authentication.
            type: bool
          smtp_username:
            description: Username for SMTP authentication - only if smtp_use_auth true.
            type: str
          subject:
            description: Subject for emails.
            type: str
      rules:
        description: Alert rules involving this alert channel.
        type: list
      system:
        description: Channel is a pre-defined system channel.
        type: bool
      type:
        description: The mechanism used by the channel.
        type: str
    sample: {
      "allowed_nodes": [1, 2],
      "enabled": true,
      "excluded_nodes": [3],
      "id": "1",
      "name": "sample_event_channel",
      "parameters": {
        "address": ["sample.com"],
        "batch": "ALL",
        "batch_period": 120,
        "custom_template": "sample",
        "send_as": "test@sample.com",
        "smtp_host": "sample.com",
        "smtp_password": "sample_password",
        "smtp_port": 25,
        "smtp_security": "none",
        "smtp_use_auth": false,
        "smtp_username": "sample-user",
        "subject": "sample"
      },
      "rules": [],
      "system": false,
      "type": "smtp"
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.powerscale_base \
    import PowerScaleBase
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.events \
    import Events
import copy

LOG = utils.get_logger('alert_channel')


class AlertChannel(PowerScaleBase):
    """Class with alert channel operations"""

    def __init__(self):
        """ Define all parameters required by the alert channel module"""

        requied_if_args = [
            ["type", "smtp", ["smtp_parameters"]],
        ]
        ansible_module_params = {
            'argument_spec': self.get_alert_channel_parameters(),
            'required_if': requied_if_args,
            'supports_check_mode': True
        }
        super().__init__(AnsibleModule, ansible_module_params)

        # Result is a dictionary that contains changed status and alert
        # channel details
        self.result.update({
            "changed": False,
            "alert_channel_details": {},
            "diff": {}
        })

    def prepare_smtp_parameters(self, smtp_parameters):
        """Prepare smtp parameters
        :param smtp_parameters: Dictionary of smtp parameters
        :return: Dictionary of prepared smtp parameters"""

        parameters = {k: v for k, v in smtp_parameters.items() if v is not None}
        if 'send_from' in parameters and parameters['send_from'] is not None:
            parameters['send_as'] = parameters['send_from']
            del parameters['send_from']
        if 'send_to' in parameters and parameters['send_to'] is not None:
            parameters['address'] = parameters['send_to']
            del parameters['send_to']
        if 'update_password' in parameters:
            del parameters['update_password']

        return parameters

    def create_alert_channel(self, channel_params):
        try:
            LOG.info("Creating alert channel.")
            pb_name = channel_params['name']

            pb_type = channel_params.get('type', "connectemc") or "connectemc"
            pb_enabled = channel_params.get('enabled', True) or True

            pb_parameters = {}
            if pb_type == 'smtp' and 'smtp_parameters' in channel_params:
                pb_parameters = self.prepare_smtp_parameters(channel_params['smtp_parameters'])
                if 'smtp_use_auth' not in channel_params or channel_params['smtp_use_auth'] is None:
                    pb_parameters['smtp_use_auth'] = False
            pb_allowed_nodes = channel_params['allowed_nodes']
            pb_excluded_nodes = channel_params['excluded_nodes']
            pb_enabled = channel_params['enabled']

            event_channel = self.isi_sdk.EventChannelCreateParams(
                name=pb_name, type=pb_type, parameters=pb_parameters,
                allowed_nodes=pb_allowed_nodes, excluded_nodes=pb_excluded_nodes,
                enabled=pb_enabled)
            if not self.module.check_mode:
                self.event_api.create_event_channel(event_channel)
            return True
        except Exception as e:
            msg = f"Failed to create alert channel {channel_params['name']} with error: {utils.determine_error(e)}"
            LOG.error(msg)
            self.module.fail_json(msg=msg)

    def modify_alert_channel(self, channel_params, channel_details):
        """Modify the the alert channel
        :param channel_params: Parameters of the alert channel to be modified
        :param channel_details: Dictionary of alert channel details
        :return: True if the operation is successful.
        """
        try:
            LOG.info("Modifying alert channel.")

            if 'parameters' in channel_params and channel_params['parameters'] is not None:
                # address/recipeient address is requied filed for smtp_parameters
                # if address none the adding the exiting addresses for smtp_parameters
                for k, v in channel_details['parameters'].items():
                    if v is not None and k not in channel_params['parameters']:
                        channel_params['parameters'][k] = v

            event_channel = self.isi_sdk.EventChannel(**channel_params)

            if not self.module.check_mode:
                self.event_api.update_event_channel(event_channel=event_channel, event_channel_id=channel_details['name'])
            return True
        except Exception as e:
            msg = f"Failed to modify alert channel {channel_details['name']} with error: {utils.determine_error(e)}"
            LOG.error(msg)
            self.module.fail_json(msg=msg)

    def send_test_alert_message(self, channel_details):
        """Send test alert message
        :param channel_details: Dictionary of alert channel details
        :return: True if test alert message sent successfully else error
        """
        try:
            LOG.info("Sending test alert.")
            event_channel = self.isi_sdk.Empty()
            event_channel_id = channel_details['name']
            if not self.module.check_mode:
                self.event_api.create_event_channel_0(event_channel, event_channel_id=event_channel_id)
            return True
        except Exception as e:
            msg = f"Failed to send test alert for alert channel {event_channel_id} with error: {utils.determine_error(e)}"
            LOG.error(msg)
            self.module.fail_json(msg=msg)

    def get_alert_channel_details(self, name):
        """Get alert channel details
        :param name: Name of the alert channel
        :return: Dictionary of alert channel details
        """
        LOG.info("Getting alert channel details.")
        channel_details = Events(self.event_api, self.module).get_alert_channel(alert_channel_id=name)
        if channel_details:
            return channel_details['channels'][0]
        return None

    def delete_alert_channel(self, channel_details):
        """
        Delete the alert channel.
        :param channel_details: Dictionary of alert channel details
        :return: True if the operation is successful.
        """
        try:
            LOG.info("Deleting alert channel.")
            event_channel_id = channel_details['name']
            if not self.module.check_mode:
                self.event_api.delete_event_channel(event_channel_id=event_channel_id)
            return True

        except Exception as e:
            msg = f"Failed to delete alert channel {event_channel_id} with error: {utils.determine_error(e)}"
            LOG.error(msg)
            self.module.fail_json(msg=msg)

    def get_diff_after(self, channel_params, channel_details):
        """Get diff between playbook input and alert channel details
        :param channel_params: Dictionary of parameters input from playbook
        :param channel_details: Dictionary of alert channel details
        :return: Dictionary of parameters of differences"""

        if channel_params["state"] == "absent":
            return {}
        else:
            if channel_details is None:
                diff_dict = {
                    "allowed_nodes": channel_params['allowed_nodes'],
                    "enabled": channel_params['enabled'],
                    "excluded_nodes": channel_params['excluded_nodes'],
                    "id": "",
                    "name": channel_params['name'],
                    "parameters": channel_params['smtp_parameters'],
                    "system": False,
                    "type": channel_params['type']
                }
                return diff_dict
            else:
                diff_dict = copy.deepcopy(channel_details)
                modify_dict = self.is_alert_channel_modify_required(channel_params, diff_dict)
                for key in modify_dict.keys():
                    diff_dict[key] = modify_dict[key]
                return diff_dict

    def is_smtp_modify_required(self, smtp_params, exiting_smtp_params):
        """Check if smtp modify is required
        :param smtp_params: Dictionary of parameters input from playbook
        :param exiting_smtp_params: Dictionary of exiting smtp parameters
        :return: modify dict if smtp modify is required else False
        """
        modify_smtp = {}

        updated_smtp = self.prepare_smtp_parameters(smtp_parameters=smtp_params)

        smtp_keys = ['address', 'batch', 'batch_period', 'send_as', 'smtp_host',
                     'smtp_port', 'smtp_security', 'smtp_use_auth', 'smtp_username',
                     'subject']
        for key in smtp_keys:
            if key in updated_smtp and updated_smtp[key] != exiting_smtp_params[key]:
                modify_smtp[key] = updated_smtp[key]

        if smtp_params['update_password'] == "always" and 'smtp_password' in updated_smtp and 'smtp_username' in updated_smtp:
            modify_smtp['smtp_password'] = updated_smtp['smtp_password']
            modify_smtp['smtp_username'] = updated_smtp['smtp_username']

        return modify_smtp

    def is_alert_channel_modify_required(self, channel_params, channel_details):
        """Check if alert channel modify is required
        :param channel_params: Dictionary of parameters input from playbook
        :param channel_details: Dictionary of alert channel details
        :return: True, modify dict if alert channel modify is required else False
        """
        modify_dict = {}
        key_list = ['enabled', 'type']
        for key in key_list:
            if key in channel_params and channel_params[key] is not None and channel_params[key] != channel_details[key]:
                modify_dict[key] = channel_params[key]

        list_keys = ['allowed_nodes', 'excluded_nodes']
        for key in list_keys:
            if key in channel_params and channel_params[key] is not None:
                if sorted(channel_params[key]) != sorted(channel_details[key]):
                    modify_dict[key] = channel_params[key]

        if 'smtp_parameters' in channel_params and channel_params['smtp_parameters'] is not None:
            smtp_params = copy.deepcopy(channel_params['smtp_parameters'])
            exting_parms = copy.deepcopy(channel_details['parameters'])
            param_smtp_dict = self.is_smtp_modify_required(smtp_params=smtp_params, exiting_smtp_params=exting_parms)
            if param_smtp_dict:
                modify_dict['parameters'] = param_smtp_dict
        return modify_dict

    def validate_name(self, name):
        """
        Validate the name of the alert channel
        :param name: Name of the alert channel
        :return: Error message if name is invalid else None
        """
        if (utils.is_input_empty(name)):
            msg = 'Invalid alert channel name. Provide valid name.'
            self.module.fail_json(msg=msg)

        if '/' in name:
            msg = 'Invalid alert channel name. Name cannot contain slashes. Provide valid name.'
            self.module.fail_json(msg=msg)

    def validate_input_params(self, channel_params):
        """
        Validate the parameters of the alert channel
        :param channel_params: Parameters of the alert channel
        :return:
        """
        self.validate_name(channel_params['name'])

        if 'smtp_parameters' in channel_params and channel_params['smtp_parameters'] is not None:
            smtp_params = channel_params['smtp_parameters']

            # self.validate_smtp_parameters(smtp_params)

            def validate_email_address(key, address):
                if utils.is_email_address_valid(address=address):
                    err_msg = f'Invalid {key}: {str(address)}. Provide valid address.'
                    self.module.fail_json(msg=err_msg)

            if 'address' in smtp_params and smtp_params['address'] is not None:
                all_addr = smtp_params['address']
                for tmp_address in all_addr:
                    validate_email_address('address', tmp_address)

            if 'send_as' in smtp_params and smtp_params['send_as'] is not None:
                validate_email_address('send_as', smtp_params['send_as'])
            self.validate_smtp_use_auth(smtp_params)

    def validate_smtp_use_auth(self, smtp_params):
        if 'smtp_use_auth' in smtp_params and smtp_params['smtp_use_auth']:
            auth_keys = ['smtp_username', 'smtp_password']
            for key in auth_keys:
                if key not in smtp_params or not smtp_params[key]:
                    msg = '%s is required while enabling smtp_use_auth. Provide valid %s.' % (key, key)
                    self.module.fail_json(msg=msg)

    def get_alert_channel_parameters(self):
        return dict(
            allowed_nodes=dict(type='list', elements='int'),
            enabled=dict(type='bool'),
            excluded_nodes=dict(type='list', elements='int'),
            name=dict(type='str', required=True),
            smtp_parameters=dict(
                type='dict',
                options=dict(address=dict(type='list', aliases=['send_to'], elements='str'),
                             batch=dict(type='str', choices=['NONE', 'ALL', 'CATEGORY', 'SEVERITY']),
                             batch_period=dict(type='int'),
                             send_as=dict(type='str', aliases=['send_from']),
                             smtp_host=dict(type='str'),
                             smtp_port=dict(type='int'),
                             smtp_security=dict(type='str', choices=['NONE', 'STARTTLS']),
                             subject=dict(type='str'),
                             smtp_use_auth=dict(type='bool'),
                             smtp_username=dict(type='str'),
                             smtp_password=dict(type='str', no_log=True),
                             update_password=dict(type='str', choices=['on_create', 'always'], default='always')
                             )),
            state=dict(type='str', choices=['present', 'absent'], default='present'),
            send_test_alert=dict(type='bool', default=False),
            type=dict(type='str', choices=['smtp', 'connectemc']))


class AlertChannelExitHandler:
    def handle(self, channel_obj, channel_details):
        if channel_details:
            channel_obj.result['alert_channel_details'] = channel_details
        else:
            channel_obj.result['alert_channel_details'] = {}
        channel_obj.module.exit_json(**channel_obj.result)


class AlertChannelDeleteHandler:
    def handle(self, channel_obj, channel_params, channel_details):
        if channel_params['state'] == 'absent' and channel_details:
            changed = channel_obj.delete_alert_channel(channel_details)
            channel_obj.result['changed'] = changed
            channel_details = channel_obj.get_alert_channel_details(name=channel_params['name'])
        AlertChannelExitHandler().handle(channel_obj, channel_details)


class AlertChannelSendAlertHandler:
    def handle(self, channel_obj, channel_params, channel_details):
        if channel_params['state'] == 'present' and channel_details and 'send_test_alert' in channel_params and channel_params['send_test_alert']:
            changed = channel_obj.send_test_alert_message(channel_details)
            channel_obj.result['changed'] = changed
        AlertChannelDeleteHandler().handle(channel_obj, channel_params, channel_details)


class AlertChannelModifyHandler:
    def handle(self, channel_obj, channel_params, channel_details):
        if channel_params['state'] == 'present' and channel_details:
            modify_dict = channel_obj.is_alert_channel_modify_required(channel_params, channel_details)
            if modify_dict:
                changed = channel_obj.modify_alert_channel(
                    channel_params=modify_dict, channel_details=channel_details)
                channel_obj.result['changed'] = changed
                channel_details = channel_obj.get_alert_channel_details(name=channel_params['name'])
        AlertChannelSendAlertHandler().handle(channel_obj, channel_params, channel_details)


class AlertChannelCreateHandler:
    def handle(self, channel_obj, channel_params, channel_details):
        if channel_params['state'] == 'present' and not channel_details:
            changed = channel_obj.create_alert_channel(channel_params)
            channel_details = channel_obj.get_alert_channel_details(name=channel_params['name'])
            channel_obj.result['changed'] = changed
        AlertChannelModifyHandler().handle(channel_obj, channel_params, channel_details)


class AlertChannelHandler:
    def handle(self, channel_obj, channel_params):
        channel_obj.validate_input_params(channel_params)
        channel_details = channel_obj.get_alert_channel_details(name=channel_params['name'])
        before_dict = {}
        diff_dict = {}
        diff_dict = channel_obj.get_diff_after(channel_params, channel_details)

        if channel_details is None:
            before_dict = {}
        else:

            before_dict = channel_details
        if channel_obj.module._diff:
            channel_obj.result['diff'] = dict(before=before_dict, after=diff_dict)

        AlertChannelCreateHandler().handle(channel_obj, channel_params, channel_details)


def main():
    """ perform action on PowerScale alert channel object and perform action on it
        based on user input from playbook."""
    obj = AlertChannel()
    AlertChannelHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
