#!/usr/bin/python
# Copyright: (c) 2021, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Ansible module for managing subnets on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: subnet

version_added: '1.4.0'

short_description: Manages subnet configuration on PowerScale
description:
- Manages the subnet configuration on the PowerScale storage system. This
  includes creating, modifying, deleting and retrieving the details of the
  subnet.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Jennifer John (@johnj9) <ansible.team@dell.com>

options:
  subnet_name:
    description: Name of the subnet.
    type: str
    required: true

  groupnet_name:
    description: Name of the groupnet.
    type: str
    required: true

  description:
    description: A description of the subnet.
    type: str

  netmask:
    description: Netmask of the subnet.
    type: str

  gateway_priority:
    description: Gateway priority.
    type: int

  new_subnet_name:
    description: Name of the subnet when renaming an existing subnet.
    type: str

  subnet_params:
    description:
    - Specify additional parameters to configure the subnet.
    type: dict
    suboptions:
      gateway:
        description: Gateway IP address.
        type: str
      sc_service_addrs:
        description: List of IP addresses that SmartConnect listens
                     for DNS requests.
        type: list
        elements: dict
        suboptions:
          start_range:
            description:
            - Specifies the start range for I(sc_service_addrs).
            type: str
            required: true
          end_range:
            description:
            - Specifies the end range for I(sc_service_addrs).
            type: str
            required: true
      sc_service_addrs_state:
        description: Specifies if the I(sc_service_addrs) range need to be added or
                     removed from the subnet.
        type: str
        choices: ['add', 'remove']
      mtu:
        description: MTU of the subnet.
        type: int
      vlan_enabled:
        description: VLAN tagging enabled or disabled
        type: bool
      vlan_id:
        description: VLAN ID for all interfaces in the subnet.
        type: int

  state:
    description:
    - The state of the subnet after the task is performed.
    - C(present) - indicates that the subnet should exist on the system.
    - C(absent) - indicates that the subnet should not exist on the system.
    choices: ['absent', 'present']
    type: str
    required: true
notes:
- The I(check_mode) is not supported.
'''

EXAMPLES = r'''
- name: Create a subnet
  dellemc.powerscale.subnet:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    groupnet_name: "groupnet_test"
    subnet_name: "subnet_test"
    description: "Test subnet"
    netmask: '198.10.**.***'
    gateway_priority: 1
    subnet_params:
      gateway: '198.10.**.***'
      sc_service_addrs:
        - start_range : '198.10.**.***'
          end_range: '198.10.**.***'
      sc_service_addrs_state: "add"
      mtu: 1500
      vlan_enabled: true
      vlan_id: 22
    state: 'present'

- name: Modify a subnet
  dellemc.powerscale.subnet:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    groupnet_name: "groupnet_test"
    subnet_name: "subnet_test"
    description: "Test subnet"
    netmask: '198.10.**.***'
    gateway_priority: 2
    subnet_params:
      gateway: '198.10.**.***'
      mtu: 1500
      vlan_enabled: true
      vlan_id: 22
    state: 'present'

- name: Rename a subnet
  dellemc.powerscale.subnet:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    groupnet_name: "groupnet_test"
    subnet_name: "subnet_test"
    new_subnet_name: "subnet_test_rename"

- name: Add smart connect service ip range to subnet
  dellemc.powerscale.subnet:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    groupnet_name: "groupnet_test"
    subnet_name: "subnet_test"
    subnet_params:
      sc_service_addrs:
        - start_range : '198.10.**.***'
          end_range: '198.10.**.***'
      sc_service_addrs_state: "add"
    state: 'present'

- name: Remove smart connect service ip range from subnet
  dellemc.powerscale.subnet:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    groupnet_name: "groupnet_test"
    subnet_name: "subnet_test"
    subnet_params:
      sc_service_addrs:
        - start_range : '198.10.**.***'
          end_range: '198.10.**.***'
      sc_service_addrs_state: "remove"
    state: 'present'

- name: Delete a subnet
  dellemc.powerscale.subnet:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    groupnet_name: "groupnet_test"
    subnet_name: "subnet_test"
    state: 'absent'
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool

subnet_details:
    description: Subnet details.
    returned: When a subnet exists
    type: complex
    contains:
        id:
            description: Unique subnet id.
            type: str
        name:
            description: The name of the subnet.
            type: str
        mtu:
            description: MTU of the subnet.
            type: int
        prefixlen:
            description: Subnet prefix length.
            type: int
        sc_service_addr:
            description: The address that SmartConnect listens for DNS requests.
            type: list
        addr_family:
            description: IP address format.
            type: str
        groupnet:
            description: Name of the groupnet this subnet belongs to.
            type: str
        pools:
            description: List of names of pools in the subnet.
            type: list
    sample: {
        "addr_family": "ipv4",
        "base_addr": "10.**.**.*",
        "description": "Initial subnet",
        "dsr_addrs": [],
        "gateway": "10.**.**.**",
        "gateway_priority": 10,
        "groupnet": "groupnet0",
        "id": "groupnet0.subnet0",
        "mtu": 1500,
        "name": "subnet0",
        "pools": [
            "pool0"
        ],
        "prefixlen": 21,
        "sc_service_addrs": [],
        "sc_service_name": "",
        "vlan_enabled": false,
        "vlan_id": null
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
import ipaddress

LOG = utils.get_logger('subnet')


class Subnet(object):
    """Class with operations on subnet"""

    def __init__(self):
        """ Define all parameters required by this module"""

        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(self.get_subnet_parameters())

        # initialize the Ansible module
        self.module = AnsibleModule(argument_spec=self.module_params,
                                    supports_check_mode=False)

        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.groupnet_api = utils.isi_sdk.NetworkGroupnetsApi(self.api_client)
        LOG.info('Got the isi_sdk instance for authorization on to PowerScale')

    def get_subnet_details(self, groupnet_name, subnet_name):
        """
        Get the details of the subnet.
        :param groupnet_name: Specifies the groupnet name.
        :param subnet_name: Specifies the subnet name.
        :return: if exists returns details of the subnet
        else returns None.
        """
        try:
            api_response = \
                self.groupnet_api.get_groupnet_subnet(subnet_name,
                                                      groupnet_name).to_dict()
            if api_response:
                api_response = api_response['subnets'][0]
            return api_response
        except utils.ApiException as e:
            if str(e.status) == '404':
                error_message = "Subnet %s details are not found" \
                    % subnet_name
                LOG.info(error_message)
                return []

            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Getting details of subnet %s ' \
                            'failed with error: %s' % (subnet_name,
                                                       str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Getting details of subnet %s ' \
                            'failed with error: %s' % (subnet_name,
                                                       str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def create_subnet(self, groupnet_name, subnet_name, subnet_params):
        """
        Create a subnet.
        :param groupnet_name: Specifies the groupnet name.
        :param subnet_name: Specifies the groupnet name.
        :param subnet_params: Specifies additional parameters to create a subnet.
        :return: Subnet Id.
        """
        try:
            if not subnet_params['netmask']:
                self.module.fail_json(
                    msg="Please enter a valid netmask.")

            if not subnet_params['gateway_priority']:
                self.module.fail_json(
                    msg="Please enter a valid gateway_priority.")

            subnet_create_params = \
                {'name': subnet_name, 'addr_family': 'ipv4',
                 'gateway_priority': subnet_params['gateway_priority'],
                 'description': subnet_params['description']}
            prefixlen = get_prefix_len(subnet_params['netmask'])
            subnet_create_params['prefixlen'] = prefixlen

            subnet_params = subnet_params['subnet_params']
            if subnet_params:
                if subnet_params['sc_service_addrs_state'] and \
                        subnet_params['sc_service_addrs_state'] != 'add':
                    self.module.fail_json(
                        msg="Please specify the sc_service_addrs_state as 'add'"
                            " to create a subnet.")

                params_to_create = get_subnet_create_params(subnet_params)
                if params_to_create:
                    subnet_create_params.update(params_to_create)

            subnet_create_params = \
                utils.isi_sdk.GroupnetSubnetCreateParams(**subnet_create_params)
            api_response = \
                self.groupnet_api.create_groupnet_subnet(subnet_create_params,
                                                         groupnet_name)
            return api_response
        except ValueError as e:
            # On successful creation of subnet the isi_sdk raises an exception
            # when trying to extract the id from an empty response.
            # Adding except clause to suppress this exception
            # as a workaround.
            if e.args[0] != "Invalid value for `id`, must not be `None`":
                raise e
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Creating subnet %s ' \
                            'failed with error: %s' % (subnet_name,
                                                       str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete_subnet(self, groupnet_name, subnet_name):
        """
         Delete a subnet.
        :param groupnet_name: Specifies the groupnet name.
        :param subnet_name: Specifies the subnet name.
        :return: True if the operation is successful.
        """
        try:
            self.groupnet_api.delete_groupnet_subnet(subnet_name,
                                                     groupnet_name)
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Deleting subnet %s ' \
                            'failed with error: %s' % (subnet_name,
                                                       str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def modify_subnet(self, groupnet_name, subnet_name, subnet_params):
        """
         Modify the subnet.
        :param groupnet_name: Specifies the groupnet name.
        :param subnet_name: Specifies the subnet name.
        :param subnet_params: Parameters to modify.
        :return: True if the operation is successful.
        """
        try:
            subnet_params = utils.isi_sdk.GroupnetSubnet(**subnet_params)
            self.groupnet_api.update_groupnet_subnet(subnet_params,
                                                     subnet_name,
                                                     groupnet_name)
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Modifying subnet %s ' \
                            'failed with error: %s' % (subnet_name,
                                                       str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def is_subnet_modified(self, subnet_details, subnet_params):
        """
        :param subnet_details: Subnet details returned from the PowerScale array.
        :param subnet_params: Subnet details passed by the user.
        :return: Subnet dictionary with values that are modified.
        """
        modify_params = {}
        if subnet_params['netmask']:
            prefixlen = get_prefix_len(subnet_params['netmask'])
            if subnet_details['prefixlen'] != prefixlen:
                modify_params['prefixlen'] = prefixlen
        if subnet_params['new_subnet_name'] and subnet_details['name'] != \
                subnet_params['new_subnet_name']:
            modify_params['name'] = subnet_params['new_subnet_name']
        subnet_keys = ['gateway_priority', 'description']
        for key in subnet_keys:
            if subnet_params[key] and subnet_params[key] != subnet_details[key]:
                modify_params[key] = subnet_params[key]
        subnet_params = subnet_params['subnet_params']
        if subnet_params:
            params_to_modify = get_subnet_modify_params(subnet_params, subnet_details)
            if params_to_modify:
                modify_params.update(params_to_modify)

        return modify_params

    def validate_input(self, subnet_name, groupnet_name, subnet_details, subnet_params):
        error_msg = utils.is_invalid_name(groupnet_name, 'groupnet_name')
        if error_msg:
            self.module.fail_json(msg=error_msg)

        error_msg = utils.is_invalid_name(subnet_name, 'subnet_name')
        if error_msg:
            self.module.fail_json(msg=error_msg)

        if subnet_params['new_subnet_name'] is not None:
            error_msg = utils.is_invalid_name(subnet_params['new_subnet_name'],
                                              'new_subnet_name')
            if error_msg:
                self.module.fail_json(msg=error_msg)

        if subnet_params['gateway_priority'] and \
                subnet_params['gateway_priority'] < 0:
            self.module.fail_json(msg='Please enter a valid value for '
                                      'gateway_priority')

        if subnet_params['netmask'] and not \
                utils.is_valid_netmask(subnet_params['netmask']):
            self.module.fail_json(msg='Invalid IPV4 address '
                                      'specified for netmask')

        if subnet_params['description'] and \
                len(subnet_params['description']) > 128:
            self.module.fail_json(msg="The maximum length for description is 128")

        subnet_params = subnet_params['subnet_params']
        if subnet_params:
            self.validate_subnet_params(subnet_params, subnet_details)

    def validate_subnet_params(self, subnet_params, subnet_details):
        if subnet_params['gateway'] and not is_valid_ip(subnet_params['gateway']):
            self.module.fail_json(msg='Invalid address specified for gateway')

        if subnet_params['sc_service_addrs']:
            self.validate_sc_service_addrs(subnet_params['sc_service_addrs'])

        vlan_enabled = subnet_params['vlan_enabled']
        vlan_id = subnet_params['vlan_id']
        mtu = subnet_params['mtu']

        if mtu is not None:
            self.validate_mtu(mtu)

        if vlan_id is not None:
            self.validate_vlan(vlan_id, vlan_enabled, subnet_details)

    def validate_mtu(self, mtu):
        if mtu < 576:
            self.module.fail_json(msg="The minimum value for mtu is 576")
        if mtu > 9000:
            self.module.fail_json(msg="The maximum value for mtu is 9000")

    def validate_sc_service_addrs(self, sc_service_addrs):
        for index in range(len(sc_service_addrs)):
            if not is_valid_ip(sc_service_addrs[index]['start_range']):
                self.module.fail_json(msg='The value for start_range is invalid')

            if not is_valid_ip(sc_service_addrs[index]['end_range']):
                self.module.fail_json(msg='The value for end_range is invalid')

    def validate_vlan(self, vlan_id, vlan_enabled, subnet_details):
        if vlan_enabled is False or (vlan_enabled is None and (not subnet_details
                                     or (subnet_details and
                                         subnet_details['vlan_enabled'] is False))):
            self.module.fail_json(msg='Please enable vlan_tagging to '
                                      'specify vlan_id')

        if vlan_id < 2:
            self.module.fail_json(msg='The minimum value for vlan_id is 2')

        if vlan_id > 4094:
            self.module.fail_json(msg='The maximum value for vlan_id is 4094')

    def perform_module_operation(self):
        """
        Perform different actions based on parameters chosen in playbook
        """
        # result is a dictionary that contains changed status and subnet
        # details
        result = dict(
            changed=False,
            create_subnet=False,
            modify_subnet=False,
            delete_subnet=False,
            subnet_details=[]
        )

        groupnet_name = self.module.params['groupnet_name']
        subnet_name = self.module.params['subnet_name']
        subnet_params = self.module.params
        state = self.module.params['state']

        subnet_details = \
            self.get_subnet_details(groupnet_name, subnet_name)

        self.validate_input(subnet_name, groupnet_name, subnet_details,
                            subnet_params)

        if state == 'absent':
            if subnet_details:
                self.delete_subnet(groupnet_name, subnet_name)
                result['changed'] = result['delete_subnet'] = True
        elif state == 'present':
            if not subnet_details:
                self.create_subnet(groupnet_name, subnet_name, subnet_params)
                result['changed'] = result['create_subnet'] = True
            else:
                params_to_modify = \
                    self.is_subnet_modified(subnet_details, subnet_params)
                if params_to_modify:
                    self.modify_subnet(groupnet_name, subnet_name,
                                       params_to_modify)
                    if subnet_params['new_subnet_name']:
                        subnet_name = subnet_params['new_subnet_name']
                    result['changed'] = result['modify_subnet'] = True

        if result['changed']:
            subnet_details = self.get_subnet_details(groupnet_name, subnet_name)

        result['subnet_details'] = subnet_details
        self.module.exit_json(**result)

    def get_subnet_parameters(self):
        return dict(
            groupnet_name=dict(type='str', required=True),
            subnet_name=dict(type='str', required=True),
            description=dict(type='str'),
            netmask=dict(type='str', no_log=True),
            gateway_priority=dict(type='int'),
            new_subnet_name=dict(type='str'),
            subnet_params=dict(type='dict', options=dict(
                gateway=dict(type='str', no_log=True),
                mtu=dict(type='int'),
                sc_service_addrs=dict(type='list', elements='dict', options=dict(
                    start_range=dict(type='str', required=True, no_log=True),
                    end_range=dict(type='str', required=True, no_log=True)
                )),
                sc_service_addrs_state=dict(type='str', choices=['add', 'remove']),
                vlan_enabled=dict(type='bool'),
                vlan_id=dict(type='int')),
                required_together=[['sc_service_addrs', 'sc_service_addrs_state']]),
            state=dict(required=True, type='str', choices=['present', 'absent'])
        )


def get_prefix_len(netmask):
    return sum(bin(int(x)).count('1') for x in netmask.split('.'))


def get_sc_addrs_to_modify(sc_addrs, sc_addrs_state, array_sc_addrs):
    for index in range(len(sc_addrs)):
        for key in list(sc_addrs[index]):
            if key == 'start_range':
                sc_addrs[index]['low'] = \
                    sc_addrs[index].pop(key)
            else:
                sc_addrs[index]['high'] = \
                    sc_addrs[index].pop(key)

    if sc_addrs_state == 'add':
        addrs_to_add = [addrs for addrs in
                        sc_addrs if
                        addrs not in array_sc_addrs]
        if addrs_to_add:
            return array_sc_addrs + addrs_to_add
    else:
        addrs_to_remove = [addrs for addrs in array_sc_addrs
                           if addrs not in sc_addrs]
        if addrs_to_remove != array_sc_addrs:
            return addrs_to_remove


def get_subnet_create_params(subnet_params):
    subnet_create_params = {}
    for key in subnet_params:
        if key == 'sc_service_addrs_state':
            continue
        elif key == 'sc_service_addrs':
            sc_service_addrs = subnet_params[key]
            if sc_service_addrs:
                sc_service_addrs_list = []
                for i in range(len(sc_service_addrs)):
                    network_range = utils.isi_sdk.ConfigNetworkRange()
                    network_range.low = sc_service_addrs[i]['start_range']
                    network_range.high = sc_service_addrs[i]['end_range']
                    sc_service_addrs_list.append(network_range)
                    subnet_create_params['sc_service_addrs'] = sc_service_addrs_list
        else:
            if subnet_params[key] is not None:
                subnet_create_params[key] = subnet_params[key]
    return subnet_create_params


def get_subnet_modify_params(subnet_params, subnet_details):
    modify_params = {}
    for key in list(subnet_params):
        if subnet_params[key] is None or key == 'sc_service_addrs_state':
            continue
        elif key == 'sc_service_addrs':
            subnet_sc_service_addrs = subnet_params[key]
            sc_addrs_to_modify = \
                get_sc_addrs_to_modify(subnet_sc_service_addrs,
                                       subnet_params['sc_service_addrs_state'],
                                       subnet_details['sc_service_addrs'])
            if sc_addrs_to_modify is not None:
                modify_params['sc_service_addrs'] = sc_addrs_to_modify
        elif subnet_params[key] != subnet_details[key]:
            modify_params[key] = subnet_params[key]
    return modify_params


def is_valid_ip(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False


def main():
    """ Create PowerScale subnet object and perform actions
         on it based on user input from the playbook"""
    obj = Subnet()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
