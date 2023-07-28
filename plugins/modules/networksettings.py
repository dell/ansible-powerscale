#!/usr/bin/python
# Copyright: (c) 2022, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

""" Ansible module for managing network settings on PowerScale"""
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: networksettings

version_added: "1.5.0"

short_description: Manages Network Settings on PowerScale Storage System
description:
- Managing Network Settings on the PowerScale Storage System includes
  modifying and retrieving details of network settings.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Meenakshi Dembi (@dembim) <ansible.team@dell.com>

options:
  enable_source_routing:
    description:
    - The value for enabling or disabling source based routing.
    type: bool
  state:
    description:
    - State of network settings.
    type: str
    required: true
    choices: ["present"]
notes:
- The I(check_mode) is not supported.
'''

EXAMPLES = r'''
  - name: Get Network settings
    dellemc.powerscale.networksettings:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      state: "{{state_present}}"

  - name: Enable source based routing
    dellemc.powerscale.networksettings:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      enable_source_routing: true
      state: "{{state_present}}"

  - name: Disable source based routing
    dellemc.powerscale.networksettings:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      enable_source_routing: false
      state: "{{state_present}}"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
    sample: "false"
network_settings:
    description: Details of the network settings.
    returned: always
    type: complex
    contains:
        default_groupnet:
            description: Default client-side DNS settings for non-multitenancy aware programs.
            type: str
        sbr:
            description: Enable or disable source based routing.
            type: str
        sc_rebalance_delay:
            description: Delay in seconds for IP rebalance.
            type: int
        tcp_ports:
            description: List of client TCP ports.
            type: list
    sample: {
        "settings": {
            "default_groupnet": "groupnet0",
            "sbr": "false",
            "sc_rebalance_delay": "0",
            "tcp_ports": [
                "2049",
                "445"
            ]
        }
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

# initialize the logger
LOG = utils.get_logger('networksettings')


class NetworkSettings(object):
    """Class with  Network Settings operations"""

    def __init__(self):
        """ Define all parameters required by this module"""

        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_network_settings_parameters())

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
        self.network_api = self.isi_sdk.NetworkApi(self.api_client)

    def get_network_settings(self):
        """
        Get network settings details
        :return: If exists returns the details of the network settings
        """
        try:
            network_settings = self.network_api.get_network_external()
            return network_settings.to_dict()
        except Exception as e:
            error_message = 'Retrieving details of network settings failed ' \
                            'with error: %s ' % (e)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def modify_network_settings(self, settings):
        """
        Modify network settings.
        :param settings: Value of network settings which need to be updated
        :return: True if modify is successful
        """
        try:
            self.network_api.update_network_external(settings)
        except Exception as e:
            error_message = 'Modifying network settings failed with ' \
                            'error: %s' % (e)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_network_setting_parameters(self, enable_source_routing):
        """
        Construct dictionary of parameters for updating network settings
        :param enable_source_routing: Value of source based routing parameter
        :return: Dictionary of parameters for updating network settings
        """
        network_settings_params = {}
        network_settings_params['sbr'] = enable_source_routing
        return network_settings_params

    def perform_module_operation(self):
        """
        Perform different actions based on parameters chosen in playbook
        """
        result = dict(
            changed=False,
            network_settings=[]
        )
        enable_source_routing = self.module.params['enable_source_routing']

        existing_network_settings = self.get_network_settings()

        if enable_source_routing is not None and (existing_network_settings['settings']['sbr'] != enable_source_routing):
            network_setting_params = self.get_network_setting_parameters(enable_source_routing)
            self.modify_network_settings(network_setting_params)
            result['changed'] = True

        if result['changed']:
            result['network_settings'] = self.get_network_settings()
        else:
            result['network_settings'] = existing_network_settings

        self.module.exit_json(**result)


def get_network_settings_parameters():
    """This method provide parameter required for the ansible Network Settings
    module on PowerScale"""
    return dict(
        enable_source_routing=dict(type='bool'),
        state=dict(required=True, type='str', choices=['present']))


def main():
    """ Create PowerScale network settings object and perform actions on it
        based on user input from playbook"""
    obj = NetworkSettings()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
