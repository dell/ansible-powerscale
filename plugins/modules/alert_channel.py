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
    type: bool
    default: true
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
        type: bool
        default: false
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
        - This parameter controls the way the I(smtp_password) is updated during
          the creation and modification of alert channel.
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
    type: str
    choices: ['connectemc', 'smtp']
    default: connectemc
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

LOG = utils.get_logger('alert_channel')


class AlertChannel(PowerScaleBase):
    """Class with alert channel operations"""

    def __init__(self):
        """ Define all parameters required by the alert channel module"""

        ansible_module_params = {
            'argument_spec': self.get_alert_channel_parameters(),
            'supports_check_mode': True,
        }
        super().__init__(AnsibleModule, ansible_module_params)

        # Result is a dictionary that contains changed status and alert
        # channel details
        self.result.update({
            "alert_channel_details": {}
        })

    def get_alert_channel_details(self):
        """
        Get details of alert channel
        """
        msg = "Getting alert channel details"
        LOG.info(msg)
        return Events(self.event_api, self.module).get_event_maintenance()

    def get_alert_channel_parameters(self):
        return dict(
            allowed_nodes=dict(type='list', elements='int'),
            enabled=dict(type='bool', default=True),
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
                             smtp_use_auth=dict(type='bool', default=False),
                             smtp_username=dict(type='str'),
                             smtp_password=dict(type='str', no_log=True),
                             update_password=dict(type='str', choices=['on_create', 'always'], default='always')
                             )),
            state=dict(type='str', choices=['present', 'absent'], default='present'),
            send_test_alert=dict(type='bool', default=False),
            type=dict(type='str', choices=['smtp', 'connectemc'], default='connectemc'))


class AlertChannelHandler:
    def handle(self, alert_channel_obj, alert_channel_params):
        pass


def main():
    """ perform action on PowerScale alert channel object and perform action on it
        based on user input from playbook."""
    obj = AlertChannel()
    AlertChannelHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
