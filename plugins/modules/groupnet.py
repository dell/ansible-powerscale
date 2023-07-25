#!/usr/bin/python
# Copyright: (c) 2021, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Ansible module for managing groupnets on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: groupnet

version_added: '1.4.0'

short_description: Manages groupnet configuration on PowerScale
description:
- Manages the groupnet configuration on the PowerScale storage system. This
  includes creating, modifying, deleting and retrieving the details of the
  groupnet.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Jennifer John (@johnj9) <ansible.team@dell.com>

options:
  groupnet_name:
    description:
    - The name of the groupnet.
    type: str
    required: true

  description:
    description: A description of the groupnet.
    type: str

  new_groupnet_name:
    description: Name of the groupnet when renaming an existing groupnet.
    type: str

  dns_servers:
    description:
    - List of Domain Name Server IP addresses.
    type: list
    elements: str

  dns_server_state:
    description:
    - Specifies if the I(dns_servers) should be added or removed from the groupnet.
    type: str
    choices: ['add', 'remove']

  dns_search_suffix:
    description:
    - List of DNS search suffixes.
    type: list
    elements: str

  dns_search_suffix_state:
    description:
    - Specifies if the dns search suffix should be added or removed from the
      groupnet.
    type: str
    choices: ['add', 'remove']

  state:
    description:
    - The state of the groupnet after the task is performed.
    - C(present) - indicates that the groupnet should exist on the system.
    - C(absent) - indicates that the groupnet should not exist on the system.
    choices: ['present', 'absent']
    type: str
    required: true
notes:
- The I(check_mode) is not supported.
'''

EXAMPLES = r'''
- name: Create a groupnet
  dellemc.powerscale.groupnet:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    groupnet_name: "groupnet_test"
    description: "Test Groupnet"
    dns_servers:
      - '198.10.**.***'
    dns_server_state: 'add'
    dns_search_suffix:
      - 'samplesearch.com'
    dns_search_suffix_state: 'add'
    state: "present"

- name: Add dns servers to a groupnet
  dellemc.powerscale.groupnet:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    groupnet_name: "groupnet_test"
    dns_servers:
      - '198.10.**.***'
    dns_server_state: 'add'
    state: "present"

- name: Remove dns servers from a groupnet
  dellemc.powerscale.groupnet:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    groupnet_name: "groupnet_test"
    dns_servers:
      - '198.10.**.***'
    dns_server_state: 'remove'
    state: "present"

- name: Add dns search suffix to a groupnet
  dellemc.powerscale.groupnet:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    groupnet_name: "groupnet_test"
    dns_search_suffix:
      - 'samplesearch.com'
    dns_search_suffix_state: 'add'
    state: "present"

- name: Remove dns search suffix from a groupnet
  dellemc.powerscale.groupnet:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    groupnet_name: "groupnet_test"
    dns_search_suffix:
      - 'samplesearch.com'
    dns_search_suffix_state: 'remove'
    state: "present"

- name: Rename a groupnet
  dellemc.powerscale.groupnet:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    groupnet_name: "groupnet_test"
    new_groupnet_name: "groupnet_test_rename"

- name: Get groupnet details
  dellemc.powerscale.groupnet:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    groupnet_name: "groupnet_test"
    state: "present"

- name: Delete a groupnet
  dellemc.powerscale.groupnet:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    groupnet_name: "groupnet_test"
    state: "absent"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
    sample: "false"

groupnet_details:
    description: Groupnet details.
    returned: When a groupnet exists
    type: complex
    contains:
        dns_search:
            description: List of DNS search suffixes
            type: list
        dns_servers:
            description:  List of Domain Name Server IP addresses
            type: list
        id:
            description: Unique Groupnet ID.
            type: str
        name:
            description: Name of groupnet
            type: str
        subnets:
            description: List of names of the subnets in the groupnet
            type: list
    sample:
        {
            "allow_wildcard_subdomains": true,
            "description": "Initial groupnet",
            "dns_cache_enabled": true,
            "dns_options": [],
            "dns_search": [
                "ansible.com"
            ],
            "dns_servers": [
                "10.**.**.***"
            ],
            "id": "groupnet0",
            "name": "groupnet0",
            "server_side_dns_search": true,
            "subnets": [
                "subnet0"
            ]
        }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
import ipaddress

LOG = utils.get_logger('groupnet')


class Groupnet(object):
    """Class with operations on groupnet"""

    def __init__(self):
        """ Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(self.get_groupnet_parameters())
        required_together = [['dns_servers', 'dns_server_state'],
                             ['dns_search_suffix', 'dns_search_suffix_state']]

        # initialize the Ansible module
        self.module = AnsibleModule(argument_spec=self.module_params,
                                    supports_check_mode=False,
                                    required_together=required_together)

        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.network_api = utils.isi_sdk.NetworkApi(self.api_client)
        self.groupnet_api = utils.isi_sdk.NetworkGroupnetsApi(self.api_client)
        LOG.info('Got the isi_sdk instance for authorization on to PowerScale')

    def get_groupnet_details(self, groupnet_name):
        """
        Get the details of the groupnet.
        :param groupnet_name: Specifies the groupnet name.
        :return: If exists returns details of the groupnet
        else returns None.
        """
        try:
            api_response = \
                self.network_api.get_network_groupnet(groupnet_name).to_dict()
            if api_response:
                api_response = api_response['groupnets'][0]

            return api_response
        except utils.ApiException as e:
            if str(e.status) == '404':
                error_message = "Groupnet %s details are not found"\
                    % groupnet_name
                LOG.info(error_message)
                return []

            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Getting details of groupnet %s ' \
                            'failed with error: %s' % (groupnet_name,
                                                       str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Getting details of groupnet %s ' \
                            'failed with error: %s' % (groupnet_name,
                                                       str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def create_groupnet(self, groupnet_name, groupnet_params):
        """
        Create a groupnet.
        :param groupnet_name: Specifies the groupnet name.
        :param groupnet_params: Specifies additional parameters to
        create a groupnet.
        :return: Groupnet Id.
        """
        try:
            if groupnet_params['dns_server_state'] and \
                    groupnet_params['dns_server_state'] != 'add':
                self.module.fail_json(
                    msg="Please specify the dns_server_state as 'add' to "
                        "create a groupnet.")

            if groupnet_params['dns_search_suffix_state'] and \
                    groupnet_params['dns_search_suffix_state'] != 'add':
                self.module.fail_json(
                    msg="Please specify the dns_search_suffix_state as 'add' "
                        "to create a groupnet.")

            groupnet_create_params = \
                {'name': groupnet_name,
                 'description': groupnet_params['description'],
                 'dns_servers': groupnet_params['dns_servers'],
                 'dns_search': groupnet_params['dns_search_suffix']}
            create_params = \
                utils.isi_sdk.NetworkGroupnetCreateParams(**groupnet_create_params)
            api_response = self.network_api.create_network_groupnet(create_params)
            return api_response
        except ValueError as e:
            # On successful creation of groupnet the isi_sdk raises an exception
            # when trying to extract the id from an empty response.
            # Adding except clause to suppress this exception
            # as a workaround.
            if e.args[0] != "Invalid value for `id`, must not be `None`":
                raise e
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Creating groupnet %s ' \
                            'failed with error: %s' % (groupnet_name,
                                                       str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete_groupnet(self, groupnet_name):
        """
         Delete a groupnet.
        :param groupnet_name: Specifies the groupnet name.
        :return: True if the operation is successful.
        """
        try:
            self.network_api.delete_network_groupnet(groupnet_name)
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Deleting groupnet %s ' \
                            'failed with error: %s' % (groupnet_name,
                                                       str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def modify_groupnet(self, groupnet, groupnet_params):
        """
         Modify the groupnet.
        :param groupnet: Specifies the groupnet name.
        :param groupnet_params: Parameters to modify.
        :return: True if the operation is successful.
        """
        try:
            groupnet_params = utils.isi_sdk.NetworkGroupnet(**groupnet_params)
            self.network_api.update_network_groupnet(groupnet_params,
                                                     groupnet)
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Modifying groupnet %s ' \
                            'failed with error: %s' % (groupnet,
                                                       str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def is_groupnet_modified(self, groupnet_details, groupnet_params):
        """
        :param groupnet_details: Groupnet details returned from the PowerScale array.
        :param groupnet_params: Groupnet details passed by the user.
        :return: Groupnet dictionary with values that are modified.
        """
        params_to_modify = {}

        if groupnet_params:
            if groupnet_params['description'] and \
                    groupnet_params['description'] != groupnet_details['description']:
                params_to_modify['description'] = groupnet_params['description']
            if groupnet_params['new_groupnet_name'] and \
                    groupnet_params['new_groupnet_name'] != groupnet_details['name']:
                params_to_modify['name'] = groupnet_params['new_groupnet_name']
            params = get_params_to_modify(groupnet_params, groupnet_details)
            if params:
                params_to_modify.update(params)

        return params_to_modify

    def validate_input(self, groupnet_name, groupnet_params):
        description = groupnet_params['description']
        new_groupnet_name = groupnet_params['new_groupnet_name']
        dns_servers = groupnet_params['dns_servers']

        error_msg = utils.is_invalid_name(groupnet_name, 'groupnet_name')
        if error_msg:
            self.module.fail_json(msg=error_msg)

        if description and len(description) > 128:
            self.module.fail_json(msg="The maximum length for description is 128")

        if new_groupnet_name is not None:
            error_msg = utils.is_invalid_name(new_groupnet_name, 'new_groupnet_name')
            if error_msg:
                self.module.fail_json(msg=error_msg)

        if dns_servers:
            for server in dns_servers:
                if not is_valid_ip(server):
                    self.module.fail_json(msg='The value for dns_servers is invalid')

    def perform_module_operation(self):
        """
        Perform different actions based on parameters chosen in playbook
        """
        # result is a dictionary that contains changed status and groupnet
        # details
        result = dict(
            changed=False,
            create_groupnet=False,
            modify_groupnet=False,
            delete_groupnet=False,
            groupnet_details=[]
        )

        groupnet_name = self.module.params['groupnet_name']
        groupnet_params = self.module.params
        state = self.module.params['state']

        self.validate_input(groupnet_name, groupnet_params)

        groupnet_details = \
            self.get_groupnet_details(groupnet_name)

        if state == 'absent':
            if groupnet_details:
                self.delete_groupnet(groupnet_name)
                result['changed'] = result['delete_groupnet'] = True
        elif state == 'present':
            if not groupnet_details:
                self.create_groupnet(groupnet_name, groupnet_params)
                result['changed'] = result['create_groupnet'] = True
            else:
                params_to_modify = \
                    self.is_groupnet_modified(groupnet_details, groupnet_params)
                if params_to_modify:
                    self.modify_groupnet(groupnet_name, params_to_modify)
                    if groupnet_params['new_groupnet_name']:
                        groupnet_name = groupnet_params['new_groupnet_name']
                    result['changed'] = result['modify_groupnet'] = True

        if result['changed']:
            groupnet_details = self.get_groupnet_details(groupnet_name)

        result['groupnet_details'] = groupnet_details
        self.module.exit_json(**result)

    def get_groupnet_parameters(self):
        return dict(
            groupnet_name=dict(type='str', required=True),
            description=dict(type='str'),
            new_groupnet_name=dict(type='str'),
            dns_servers=dict(type='list', elements='str', no_log=True),
            dns_server_state=dict(type='str', choices=['add', 'remove']),
            dns_search_suffix=dict(type='list', elements='str'),
            dns_search_suffix_state=dict(type='str', choices=['add', 'remove']),
            state=dict(required=True, type='str', choices=['present', 'absent'])
        )


def is_valid_ip(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False


def get_params_to_modify(groupnet_params, groupnet_details):
    params_to_modify = {}
    groupnet_keys = {'dns_servers': 'dns_server_state',
                     'dns_search_suffix': 'dns_search_suffix_state'}
    for key in groupnet_keys:
        if groupnet_params[key]:
            array_key = "dns_search" if key == "dns_search_suffix" \
                else key
            modified_dns = list(set(groupnet_params[key]) -
                                set(groupnet_details[array_key]))
            if groupnet_params[groupnet_keys[key]] == 'add' and \
                    modified_dns:
                params_to_modify[array_key] = \
                    groupnet_details[array_key] + modified_dns
            elif groupnet_params[groupnet_keys[key]] == 'remove':
                dns_exists = any(dns in groupnet_details[array_key]
                                 for dns
                                 in groupnet_params[key])
                if dns_exists:
                    modified_dns = list(set(groupnet_details[array_key]) -
                                        set(groupnet_params[key]))
                    params_to_modify[array_key] = modified_dns
    return params_to_modify


def main():
    """ Create PowerScale groupnet object and perform actions
         on it based on user input from the playbook"""
    obj = Groupnet()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
