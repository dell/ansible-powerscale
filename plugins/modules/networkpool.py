#!/usr/bin/python
# Copyright: (c) 2021, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

""" Ansible module for managing network pool on PowerScale"""
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: networkpool

version_added: "1.4.0"

short_description: Manages Network Pools on PowerScale Storage System
description:
- Managing Network Pools on the PowerScale Storage System includes creating,
  modifying, deleting and reterving details of network pool.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Meenakshi Dembi (@dembim) <ansible.team@dell.com>
- Pavan Mudunuri(@Pavan-Mudunuri) <ansible.team@dell.com>

options:
  pool_name:
    description:
    - The Name of the pool.
    type: str
    required: true
  new_pool_name:
    description:
    - Name of the pool when renaming an existing pool.
    type: str
  groupnet_name:
    description:
    - The name of the groupnet.
    type: str
    required: true
  subnet_name:
    description:
    - The name of the subnet.
    type: str
    required:  true
  description:
    description:
    - Description of the pool.
    type: str
  access_zone:
    description:
    - Name of access zone to be associated with pool.
    type: str
  state:
    description:
    - The state option is used to mention the existence of pool.
    type: str
    required: true
    choices: [absent, present]
  additional_pool_params:
    description:
    - Define additional parameters for pool.
    type: dict
    suboptions:
        ranges:
            description:
            - List of IP address ranges in this pool.
            type: list
            elements: dict
            suboptions:
                low:
                    description:
                    - Lower limit.
                    type: str
                high:
                    description:
                    - Upper limit.
                    type: str
        range_state:
            description:
            - This signifies if range needs to be added or removed.
            type: str
            choices: ['add', 'remove']
        ifaces:
            description:
            - List of Pool interface members.
            type: list
            elements: dict
            suboptions:
                iface:
                    description:
                    - Pool interface members
                    type: str
                lnn:
                    description:
                    - Logical Node Number
                    type: int
        iface_state:
            description:
            - This signifies if interface needs to be added or removed.
            type: str
            choices: ['add', 'remove']
  sc_params:
    description:
    - SmartConnect Parameters.
    type: dict
    suboptions:
        static_routes:
            description:
            - List of static routes in the pool.
            type: list
            elements: dict
            suboptions:
                gateway:
                    description:
                    - Address of the gateway in the format yyy.yyy.yyy.yyy.
                    type: str
                    required: true
                prefix_len:
                    description:
                    - The subnet mask length.
                    type: int
                    required: true
                subnet:
                    description:
                    - Network address in the format xxx.xxx.xxx.xxx.
                    type: str
                    required: true
        sc_dns_zone:
            description:
            - SmartConnect zone name for the pool.
            type: str
        sc_dns_zone_aliases:
            description:
            - List of SmartConnect zone aliases (DNS names) to the pool.
            type: list
            elements: str
        sc_subnet:
            description:
            - Name of SmartConnect service subnet for this pool.
            type: str
        sc_connect_policy:
            description:
            - SmartConnect client connection balancing policy.
            type: str
            choices: ['round_robin', 'conn_count', 'throughput', 'cpu_usage']
        sc_failover_policy:
            description:
            - SmartConnect IP failover policy.
            type: str
            choices: ['round_robin', 'conn_count', 'throughput', 'cpu_usage']
        rebalance_policy:
            description:
            - Rebalance policy.
            type: str
            choices: ['auto', 'manual']
        alloc_method:
            description:
            - Specifies how IP address allocation is done among pool members.
            type: str
            choices: ['dynamic', 'static']
        sc_auto_unsuspend_delay:
            description:
            - Time delay in seconds before a node which has been automatically
              unsuspended becomes usable in SmartConnect responses for pool zones.
            type: int
        sc_ttl:
            description:
            - Time to live value for SmartConnect DNS query responses in seconds.
            type: int
        aggregation_mode:
            description:
            - OneFS supports the following C(NIC) aggregation modes.
            choices: ['roundrobin', 'failover', 'lacp', 'fec']
            type: str
notes:
- The I(check_mode) is not supported.
- Removal of static routes and I(sc_dns_zone_aliases) is not supported.
'''

EXAMPLES = r'''
  - name: Create Network Pool
    dellemc.powerscale.networkpool:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      groupnet: "groupnet0"
      subnet: "subnet0"
      additional_pool_params:
        ranges:
        - low: "10.230.**.***"
          high: "10.230.**.***"
        range_state: "add"
        ifaces:
        - iface: "ext-1"
          lnn: 1
        iface_state: "add"
      sc_params:
        sc_dns_zone: "10.230.**.***"
        sc_connect_policy: "throughput"
        sc_failover_policy: "throughput"
        rebalance_policy: "auto"
        alloc_method: "static"
        sc_auto_unsuspend_delay: 200
        sc_ttl: 200
        sc_dns_zone_aliases:
        - "Test"
        static_routes:
        - gateway: "10.**.**.**"
          prefix_len: 21
          subnet: "10.**.**.**"
      pool: "Test_Pool_2"
      access_zone: "system"
      state: "present"

  - name: Get Network Pool
    dellemc.powerscale.networkpool:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      groupnet: "groupnet0"
      subnet: "subnet0"
      pool: "Test_Pool_2"
      state: "present"

  - name: Modify Network Pool
    dellemc.powerscale.networkpool:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      groupnet: "groupnet0"
      subnet: "subnet0"
      pool: "Test_Pool_2"
      additional_pool_params:
        ranges:
        - low: "10.230.**.***"
          high: "10.230.**.***"
        range_state: "add"
        ifaces:
        - iface: "ext-1"
          lnn: 1
        iface_state: "add"
      sc_params:
        sc_dns_zone: "10.230.**.***"
        sc_connect_policy: "throughput"
        sc_failover_policy: "throughput"
        rebalance_policy: "auto"
        alloc_method: "static"
        sc_auto_unsuspend_delay: 200
        sc_ttl: 200
        sc_dns_zone_aliases:
        - "Test"
        static_routes:
        - gateway: "10.**.**.**"
          prefix_len: 21
          subnet: "10.**.**.**"
      aggregation_mode: "fec"
      description: "Pool Created by Ansible Modify"
      state: "present"

  - name: Delete Network Pool
    dellemc.powerscale.networkpool:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      groupnet: "groupnet0"
      subnet: "subnet0"
      pool: "Test_Pool_2"
      state: "absent"

  - name: Rename a network Pool
    dellemc.powerscale.networkpool:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      groupnet_name: "groupnet0"
      subnet_name: "subnet0"
      pool_name: "Test_Pool"
      new_pool_name: "Test_Pool_Rename"
      state: "present"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
    sample: "false"
pools:
    description: Details of the network pool.
    returned: always
    type: complex
    contains:
        access_zone:
            description: Name of a valid access zone to map IP address pool to the zone.
            type: str
        addr_family:
            description: IP address format.
            type: str
        aggregation_mode:
            description: OneFS supports the following NIC aggregation modes.
            type: str
        alloc_method:
            description: Specifies how IP address allocation is done among pool members.
            type: str
        description:
            description: A description of the pool.
            type: str
        groupnet:
            description: Name of the groupnet this pool belongs to.
            type: str
        id:
            description: Unique Pool ID.
            type: str
        ifaces:
            description: List of interface members in this pool.
            type: str
        name:
            description: The name of the pool. It must be unique throughout the given subnet.
                         It's a required field with POST method.
            type: str
        ranges:
            description: List of IP address ranges in this pool.
            type: str
        rebalance_policy:
            description: Rebalance policy.
            type: str
        sc_auto_unsuspend_delay:
            description: Time delay in seconds before a node which has been automatically
                         unsuspended becomes usable in SmartConnect responses for pool zones.
            type: int
        sc_connect_policy:
            description: SmartConnect client connection balancing policy.
            type: str
        sc_dns_zone:
            description: SmartConnect zone name for the pool.
            type: str
        sc_dns_zone_aliases:
            description: List of SmartConnect zone aliases (DNS names) to the pool.
            type: list
        sc_failover_policy:
            description: SmartConnect IP failover policy.
            type: str
        sc_subnet:
            description: Name of SmartConnect service subnet for this pool.
            type: str
        sc_suspended_nodes:
            description: List of LNNs showing currently suspended nodes in SmartConnect.
            type: list
        sc_ttl:
            description: Time to live value for SmartConnect DNS query responses in seconds.
            type: int
        static_routes:
            description: List of static routes in the pool.
            type: list
        subnet:
            description: The name of the subnet.
            type: str
    sample:
        {
        "pools": [
            {
                "access_zone": "System",
                "addr_family": "ipv4",
                "aggregation_mode": "roundrobin",
                "alloc_method": "static",
                "description": "",
                "groupnet": "groupnet0",
                "id": "groupnet0.subnet0.Test_10",
                "ifaces": [],
                "name": "Test_10",
                "nfsv3_rroce_only": false,
                "ranges": [],
                "rebalance_policy": "auto",
                "rules": [],
                "sc_auto_unsuspend_delay": 0,
                "sc_connect_policy": "round_robin",
                "sc_dns_zone": "10.**.**.**",
                "sc_dns_zone_aliases": [
                    "Testststst",
                    "tesrtdsb1"
                ],
                "sc_failover_policy": "round_robin",
                "sc_subnet": "",
                "sc_suspended_nodes": [],
                "sc_ttl": 0,
                "static_routes": [
                    {
                        "gateway": "10.**.**.**",
                        "prefixlen": 21,
                        "subnet": "10.**.**.**"
                    }
                ],
                "subnet": "subnet0"
            }
        ]
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
import ipaddress

# initialize the logger
LOG = utils.get_logger('networkpool')


class NetworkPool(object):
    """Class with  Network Pool operations"""

    def __init__(self):
        """ Define all parameters required by this module"""

        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_network_pool_parameters())

        # initialize the ansible module
        self.module = AnsibleModule(argument_spec=self.module_params)

        # result is a dictionary that contains changed status and
        self.result = {"changed": False}
        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        LOG.info('Got python SDK instance for provisioning on PowerScale')
        self.network_groupnet_api = self.isi_sdk.NetworkGroupnetsApi(self.api_client)

    def create_network_pool(self, groupnet, subnet, pool_params):
        """
        Create a network pool
        :param groupnet: Name of the groupnet
        :param subnet: Name of the subnet
        :param pool_params: Dictionary of parameters to be set while creating a network pool
        :return: None
        """
        try:
            self.network_groupnet_api.create_subnets_subnet_pool(pool_params, groupnet, subnet)
        except ValueError as e:
            # Work around an issue in the underlying api call used in
            # most versions of the isi_sdk.  The network pool is created, but
            # api call to has no response.  The isi_sdk raises an exception
            # when trying to extract the id from an empty response.
            if e.args[0] != "Invalid value for `id`, must not be `None`":
                self.module.fail_json(msg=e)
        except utils.ApiException as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Unable to create network pool %s %s' % (pool_params['name'], str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_network_pool(self, groupnet, subnet, pool):
        """
        Get network pool details
        :param groupnet: Name of the groupnet
        :param subnet: Name of the subnet
        :param pool: Name of the pool
        :return: If exists retuns the details of the network pool
        """
        try:
            details = self.network_groupnet_api.get_subnets_subnet_pool(pool, groupnet, subnet)
            return details.to_dict()
        except utils.ApiException as e:
            if str(e.status) == "404":
                error_message = "Details not found for network pool %s" % (pool)
                LOG.error(error_message)
                return None
            else:
                error_msg = utils.determine_error(error_obj=e)
                error_message = 'Unable to get network pool %s ' \
                                'failed with error: %s ' % (pool, str(error_msg))
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

    def delete_network_pool(self, groupnet, subnet, pool):
        """
        Delete network pool
        :param groupnet: Name of the groupnet
        :param subnet: Name of the subnet
        :param pool: Name of the pool
        :return: True if deletion is successful
        """
        try:
            self.network_groupnet_api.delete_subnets_subnet_pool(pool, groupnet, subnet)
            return True
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Failed to delete network pool: %s with ' \
                            'error: %s' % (pool, error_msg)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def do_update(self, source, target):
        return source != target

    def get_modify_list(self, source, target, key, state):
        if state == 'add':
            delta = [item for item in source[key] if item not in target[key]]
            if delta:
                return target[key] + delta
        elif state == 'remove':
            return [item for item in target[key] if item not in source[key]]

    def is_pool_modifiable(self, pool_details, pool_params):
        """
        Check whether network pool is modifiable
        :param pool_details: Network pool object of existing pool
        :param pool_param: Dictionary of parameters input from playbook
        :return :Dictionary of parameters that needs to be modified,
        if no parameters are to be modified dict is empty
        """
        modify_pool_dict = {}
        network_pool_keys = ['description', 'access_zone']

        for keys in network_pool_keys:
            if pool_params[keys] and self.do_update(pool_details['pools'][0][keys], pool_params[keys]):
                modify_pool_dict[keys] = pool_params[keys]

        if pool_params['new_pool_name'] and pool_params['new_pool_name'] != pool_details['pools'][0]['name']:
            modify_pool_dict['name'] = pool_params['new_pool_name']

        if pool_params['additional_pool_params']:
            ifaces = self.get_modify_list(pool_params['additional_pool_params'],
                                          pool_details['pools'][0], 'ifaces',
                                          pool_params['additional_pool_params']['iface_state'])
            if pool_params['additional_pool_params']['iface_state'] == "remove" or \
               pool_params['additional_pool_params']['iface_state'] == "add" and ifaces:
                modify_pool_dict['ifaces'] = ifaces

            ranges = self.get_modify_list(pool_params['additional_pool_params'],
                                          pool_details['pools'][0], 'ranges',
                                          pool_params['additional_pool_params']['range_state'])
            if pool_params['additional_pool_params']['range_state'] == "remove" or \
               pool_params['additional_pool_params']['range_state'] == "add" and ranges:
                modify_pool_dict['ranges'] = ranges

        if pool_params['sc_params']:
            sc_params_modify = pool_params['sc_params']
            if sc_params_modify['sc_dns_zone_aliases']:
                sc_params_modify['sc_dns_zone_aliases'] = \
                    self.remove_duplicate_aliases(sc_params_modify['sc_dns_zone_aliases'])
            if sc_params_modify['static_routes']:
                sc_params_modify['static_routes'] = \
                    self.remove_duplicate_static_routes(sc_params_modify['static_routes'])
                self.replace_prefix_len(sc_params_modify['static_routes'])
            for key in sc_params_modify:
                if sc_params_modify[key] is not None and sc_params_modify[key] != pool_details['pools'][0][key]:
                    modify_pool_dict[key] = sc_params_modify[key]
        return modify_pool_dict

    def remove_duplicate_static_routes(self, routes):

        route_dict = {(route["gateway"], route["prefix_len"], route["subnet"]): route for route in routes}
        route_list = list(route_dict.values())
        return route_list

    def modify_network_pool(self, modify_pool_param, pool, groupnet, subnet):
        """
        Modify network pool.
        :param modify_pool_param: Dictionary of parameters to be modified for network pool
        :param groupnet: Name of the groupnet
        :param subnet: Name of the subnet
        :param pool: Name of the pool to be modified
        :return: True if modify is successful
        """
        try:
            self.network_groupnet_api.update_subnets_subnet_pool(modify_pool_param, pool, groupnet, subnet)
            return True
        except Exception as e:
            error_message = 'Failed to update network pool: %s with ' \
                            'error: %s' % (pool, e)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def remove_duplicate_aliases(self, aliases):

        aliases_list = []
        [aliases_list.append(item) for item in aliases if item not in aliases_list]
        return aliases_list

    def construct_pool_parameters(self, input_param):
        """
        Construct dictionary of parameters to be set for create network pool
        :param input_param: Dictionary of parameters provided from playbook
        :param network_pool_param: Network pool object of existing pool
        :return: Dictionary of parameters to be set for create network pool
        """
        network_pool_param = {}
        if input_param['pool_name']:
            network_pool_param['name'] = input_param['pool_name']
        if input_param['access_zone']:
            network_pool_param['access_zone'] = input_param['access_zone']
        if input_param['description']:
            network_pool_param['description'] = input_param['description']
        if input_param['sc_params']:
            sc_params = input_param['sc_params']
            if sc_params['sc_dns_zone_aliases']:
                sc_params['sc_dns_zone_aliases'] = self.remove_duplicate_aliases(sc_params['sc_dns_zone_aliases'])
            if sc_params['static_routes']:
                sc_params['static_routes'] = self.remove_duplicate_static_routes(sc_params['static_routes'])
                network_pool_param["static_routes"] = self.replace_prefix_len(sc_params['static_routes'])
            for key in sc_params:
                if sc_params[key]:
                    network_pool_param[key] = sc_params[key]
        if input_param['additional_pool_params']:
            additional_params = input_param['additional_pool_params']
            if additional_params['ifaces'] and additional_params['iface_state'] == "add":
                network_pool_param['ifaces'] = []
                for ifaces in additional_params['ifaces']:
                    network_pool_param['ifaces'].append(ifaces)
            if additional_params['ranges'] and additional_params['range_state'] == "add":
                network_pool_param['ranges'] = []
                for ranges in additional_params['ranges']:
                    network_pool_param['ranges'].append(ranges)
        return network_pool_param

    def replace_prefix_len(self, routes):

        for route in routes:
            if "prefix_len" in route:
                route["prefixlen"] = route.pop("prefix_len")
        return routes

    def validate_input(self, pool_params):

        error_msg = utils.is_invalid_name(pool_params['pool_name'], 'pool_name')
        if error_msg:
            self.module.fail_json(msg=error_msg)

        if pool_params['description'] and len(pool_params['description']) > 128:
            self.module.fail_json(msg="The maximum length for description is 128")

        if pool_params['new_pool_name']:
            error_msg = utils.is_invalid_name(pool_params['new_pool_name'], 'new_pool_name')
            if error_msg:
                self.module.fail_json(msg=error_msg)

        if pool_params['sc_params']:
            if pool_params['sc_params']['static_routes']:
                for index in pool_params['sc_params']['static_routes']:
                    for value in index.values():
                        if value == "" or value is None:
                            msg = 'Invalid static route value'
                            self.module.fail_json(msg=f'{msg}')

        if pool_params['additional_pool_params']:
            if pool_params['additional_pool_params']['ranges']:
                for index in pool_params['additional_pool_params']['ranges']:
                    for value in index.values():
                        if not is_valid_ip(value):
                            self.module.fail_json(msg='The value for IP range is invalid')

            if pool_params['additional_pool_params']['ifaces']:
                for index in pool_params['additional_pool_params']['ifaces']:
                    for value in index.values():
                        if value == "" or value is None:
                            self.module.fail_json(msg='Please enter valid value for iface')

    def perform_module_operation(self):
        """
        Perform different actions based on parameters chosen in playbook
        """
        result = dict(
            changed=False,
            network_pool=[]
        )
        groupnet_name = self.module.params['groupnet_name']
        subnet_name = self.module.params['subnet_name']
        pool_name = self.module.params['pool_name']
        state = self.module.params['state']
        access_zone = self.module.params['access_zone']
        sc_params = self.module.params['sc_params']
        additional_pool_params = self.module.params['additional_pool_params']
        pool_params = self.module.params
        modify_pool_param = None
        new_pool_name = self.module.params['new_pool_name']

        self.validate_input(pool_params)

        input_param = {}
        for param in self.module.params:
            input_param[param] = self.module.params[param]

        pool_details = self.get_network_pool(groupnet_name, subnet_name, pool_name)

        if state == "absent" and pool_details:
            result['changed'] = self.delete_network_pool(groupnet_name, subnet_name, pool_name)
            result['network_pool'] = []

        if state == "present" and not pool_details:
            pool_params = self.construct_pool_parameters(input_param)
            if pool_params:
                self.create_network_pool(groupnet_name, subnet_name, pool_params)
                result['changed'] = True

        # Form dictionary of modifiable parameters for a pool
        if pool_details and input_param:
            modify_pool_param = \
                self.is_pool_modifiable(pool_details, pool_params)

        # Modify network pool
        if modify_pool_param and state == "present":
            self.modify_network_pool(modify_pool_param, pool_name, groupnet_name, subnet_name)
            if new_pool_name:
                pool_name = new_pool_name
            result['changed'] = result['modify_network_pool'] = True

        if state == 'present':
            result['network_pool'] = \
                self.get_network_pool(groupnet_name, subnet_name, pool_name)

        self.module.exit_json(**result)


def get_network_pool_parameters():
    """This method provide parameter required for the ansible Network Pool
    modules on PowerScale"""
    return dict(
        access_zone=dict(type='str'),
        description=dict(type='str'),
        groupnet_name=dict(required=True, type='str'),
        pool_name=dict(required=True, type='str'),
        new_pool_name=dict(type='str'),
        sc_params=dict(type='dict', options=dict(
            sc_dns_zone=dict(type='str'),
            sc_connect_policy=dict(type='str', choices=['round_robin', 'conn_count', 'throughput', 'cpu_usage']),
            sc_failover_policy=dict(type='str', choices=['round_robin', 'conn_count', 'throughput', 'cpu_usage']),
            rebalance_policy=dict(type='str', choices=['auto', 'manual']),
            alloc_method=dict(type='str', choices=['dynamic', 'static']),
            aggregation_mode=dict(type='str', choices=['roundrobin', 'failover', 'lacp', 'fec']),
            sc_subnet=dict(type='str'),
            sc_auto_unsuspend_delay=dict(type='int'),
            static_routes=dict(type='list', elements='dict', options=dict(
                               gateway=dict(type='str', required=True),
                               prefix_len=dict(type='int', required=True),
                               subnet=dict(type='str', required=True))),
            sc_dns_zone_aliases=dict(type='list', elements='str'),
            sc_ttl=dict(type='int'))),
        state=dict(required=True, type='str', choices=['absent', 'present']),
        subnet_name=dict(required=True, type='str'),
        additional_pool_params=dict(type='dict', options=dict(
            ranges=dict(type='list', elements='dict', options=dict(
                        low=dict(type='str'),
                        high=dict(type='str'))),
            range_state=dict(type='str', choices=['add', 'remove']),
            ifaces=dict(type='list', elements='dict', options=dict(
                        iface=dict(type='str'),
                        lnn=dict(type='int'))),
            iface_state=dict(type='str', choices=['add', 'remove']))))


def is_valid_ip(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False


def main():
    """ Create PowerScale network pool object and perform actions on it
        based on user input from playbook"""
    obj = NetworkPool()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
