#!/usr/bin/python
# Copyright: (c) 2021, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Ansible module for managing Network Rules on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: networkrule

version_added: '1.4.0'

short_description: Manages Network provisioning rules for PowerScale Storage System

description:
- Modify an existing network provisioning rule.
- Create a new network provisioning rule.
- Delete a network provisioning rule.
- View the details of a network provisioning rule.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
  - Spandita Panigrahi (@panigs7) <ansible.team@dell.com>

options:
    description:
        description:
            - Description for rule.
            - It can be no more than 128 bytes in length.
        type: str

    groupnet_name:
        description:  Groupnet name to which this provisioning rule applies.
        type: str
        required: true

    iface:
        description:
            - Interface to which the rule applies.
        type: str

    node_type:
        description:
            - Node types to which the provisioning rule applies.
        type: str
        choices: ['any', 'storage', 'accelerator', 'backup-accelerator']

    pool_name:
        description:  Pool to which this provisioning rule applies.
        type: str
        required: true

    rule_name:
        description: Name of provisioning rule.
        type: str
        required: true

    new_rule_name:
        description: Name of provisioning rule when renaming an existing rule.
        type: str

    subnet_name:
        description: Name of the subnet to which this provisioning rule applies.
        type: str
        required: true

    state:
        description: State of provisioning rule.
        type: str
        choices: ['absent', 'present']
        required: true
notes:
- The I(check_mode) is not supported.
'''

EXAMPLES = r'''

  - name: Get the details of a network rule
    dellemc.powerscale.networkrule:
      onefs_host: "{{onefs_host}}"
      port_no: "{{port_no}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      groupnet_name: "groupnet1"
      subnet_name: "subnet1"
      pool_name: "pool1"
      rule_name: "rule1"
      state: "present"

  - name: Create a new network provisioning rule
    dellemc.powerscale.networkrule:
      onefs_host: "{{onefs_host}}"
      port_no: "{{port_no}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      groupnet_name: "groupnet1"
      subnet_name: "subnet1"
      pool_name: "pool1"
      rule_name: "new_rule"
      description: "Rename existing rule"
      iface: "ext1"
      node_type: "storage"
      state: "present"

  - name: Modifying an existing network provisioning rule
    dellemc.powerscale.networkrule:
      onefs_host: "{{onefs_host}}"
      port_no: "{{port_no}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      groupnet_name: "groupnet1"
      subnet_name: "subnet1"
      pool_name: "pool1"
      rule_name: "rule_name"
      description: "Modify rule"
      iface: "ext1"
      node_type: "storage"
      state: "present"

  - name: Delete a network provisioning rule
    dellemc.powerscale.networkrule:
      onefs_host: "{{onefs_host}}"
      port_no: "{{port_no}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      groupnet_name: "groupnet1"
      subnet_name: "subnet1"
      pool_name: "pool1"
      rule_name: "rule"
      state: absent
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: Always
    type: bool
    sample: "false"

network_rule_details:
    description: Network provisioning rule details.
    returned: When a network provisioning rule exists
    type: complex
    contains:

        description:
            description: Description of network provisioning rule
            type: str

        groupnet:
            description: Name of groupnet to which this rule belongs
            type: str

        id:
            description: Unique ID for network provisioning rule
            type: str

        iface:
            description:
                - Interface name to which this rule belongs
                - For example, ext-1
            type: str

        name:
            description: Name of network provisioning rule
            type: str

        node_type:
            description:
                - Node type to which the provisioning rule applies
            type: str

        pool:
            description: Name of pool to which this rule belongs
            type: str

        subnet:
            description: Name of subnet to which this rule belongs
            type: str
    sample: {
        "description": "description",
        "groupnet": "groupnet0",
        "id": "groupnet0.subnet0.pool0.test_rule",
        "iface": "10gige-1",
        "name": "test_rule",
        "node_type": "any",
        "pool": "pool0",
        "subnet": "subnet0"
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('networkrule')


class NetworkRule(object):
    """Class with Network Provisioning Rule operations"""

    def __init__(self):
        """ Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_network_rule_parameters())

        # initialize the Ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False
        )

        # result is a dictionary that contains changed status
        self.result = {"changed": False}
        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.network_api_instance = utils.isi_sdk.NetworkGroupnetsSubnetsApi(self.api_client)
        LOG.info('Got the isi_sdk instance for Network for PowerScale')

    def create_network_rule(self, groupnet, subnet, pool, rule_details):
        """
        Create a network rule
        """
        name = rule_details['name']
        try:
            create_params = utils.isi_sdk.PoolsPoolRule(**rule_details)
            self.network_api_instance.create_pools_pool_rule(pools_pool_rule=create_params,
                                                             groupnet=groupnet,
                                                             subnet=subnet,
                                                             pool=pool)
        except ValueError as e:
            # On successful creation of network provisioning rule
            # the isi_sdk raises an exception
            # when trying to extract the id from an empty response.
            # Adding except clause to suppress this exception
            # as a workaround.
            if e.args[0] != "Invalid value for `id`, must not be `None`":
                raise e
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Unable to create network rule %s. ' \
                            'failed with error: %s' % (name, str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete_network_rule(self, groupnet, subnet, pool, rule):
        """
        Delete a network rule
        """
        try:
            self.network_api_instance.delete_pools_pool_rule(rule,
                                                             groupnet,
                                                             subnet,
                                                             pool)
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Unable to delete network rule %s. ' \
                            'failed with error: %s' % (rule, str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_network_rule(self, groupnet, subnet, pool, rule):
        """
        Get configuration details for a specific rule
        """
        rule_details = {}

        try:
            current_rule_details = self.network_api_instance.get_pools_pool_rule(rule,
                                                                                 groupnet,
                                                                                 subnet,
                                                                                 pool)
            current_rule_details = current_rule_details.to_dict()
            rule_details.update(current_rule_details['rules'][0])
        except utils.ApiException as e:
            if str(e.status) == "404":
                error_message = "Details of Network rule %s are not found" % rule
                LOG.info(error_message)
                return None

            else:
                error_msg = utils.determine_error(error_obj=e)
                error_message = 'Unable to retrieve details of rule %s. ' \
                                'failed with error: %s' % (rule, str(error_msg))
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Unable to retrieve details of rule %s. ' \
                            'failed with error: %s' % (rule, str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

        return rule_details

    def modify_network_rule(self, groupnet, subnet, pool, rule, new_rule_details):
        """
        Modify an existing network rule
        """
        try:
            desired_rule_details = utils.isi_sdk.PoolsPoolRule(**new_rule_details)
            self.network_api_instance.update_pools_pool_rule(desired_rule_details,
                                                             rule,
                                                             groupnet,
                                                             subnet,
                                                             pool)
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Unable to modify settings for rule %s. ' \
                            'failed with error: %s' % (rule, str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_settings_to_modify(self, current_rule_details, new_name=None):
        """
        Determine which settings need to be updated for the rule
        """
        need_update = {}

        keys = ['description', 'iface', 'node_type']

        name = self.module.params['rule_name']

        if not current_rule_details:
            need_update['name'] = name

            for key in keys:
                if self.module.params[key] is not None:
                    need_update[key] = self.module.params[key]
        else:
            current = current_rule_details

            for key in keys:
                if self.module.params[key] is not None \
                        and key in current \
                        and self.module.params[key] != current[key]:
                    need_update[key] = self.module.params[key]

            if new_name and not utils.is_input_empty(new_name) and new_name != name:
                need_update.update({'name': new_name})

        return need_update

    def validate_input(self, rule, description, new_rule_name):
        """
        Validate input.
        """

        rule_name_error_msg = utils.is_invalid_name(rule, 'rule_name')
        if rule_name_error_msg:
            self.module.fail_json(msg=rule_name_error_msg)

        new_rule_name_error_msg = utils.is_invalid_name(new_rule_name, 'new_rule_name')
        if new_rule_name_error_msg:
            self.module.fail_json(msg=new_rule_name_error_msg)

        if description and len(description) > 128:
            self.module.fail_json(msg="The maximum length for description is 128")

    def perform_module_operation(self):
        """
        Perform different actions based on parameters chosen in playbook
        """
        result = dict(
            changed=False,
            network_rule_details={},
            create_network_rule=False,
            modify_network_rule=False,
            delete_network_rule=False,
        )

        groupnet = self.module.params['groupnet_name']
        subnet = self.module.params['subnet_name']
        pool = self.module.params['pool_name']
        rule = self.module.params['rule_name']
        new_rule_name = self.module.params['new_rule_name']
        iface = self.module.params['iface']
        description = self.module.params['description']
        state = self.module.params['state']

        new_name = None
        self.validate_input(rule, description, new_rule_name)

        current_rule_details = self.get_network_rule(groupnet,
                                                     subnet,
                                                     pool,
                                                     rule)

        if new_rule_name and not utils.is_input_empty(new_rule_name):
            new_name = new_rule_name

        if state == 'absent' and current_rule_details:
            self.delete_network_rule(groupnet, subnet, pool, rule)
            result['delete_network_rule'] = True
        elif state == 'present':
            if not current_rule_details:

                # Validate mandatory parameters to create a network rule
                if (iface and utils.is_input_empty(iface)) or not iface:
                    self.module.fail_json(
                        msg="Please provide a valid interface type to create a network rule.")

                rule_settings_to_modify = \
                    self.get_settings_to_modify(current_rule_details, new_name)
                self.create_network_rule(groupnet,
                                         subnet,
                                         pool,
                                         rule_settings_to_modify)
                result['create_network_rule'] = True
            else:
                rule_settings_to_modify = \
                    self.get_settings_to_modify(current_rule_details, new_name)
                if rule_settings_to_modify:
                    self.modify_network_rule(groupnet,
                                             subnet,
                                             pool,
                                             rule,
                                             rule_settings_to_modify)
                    result['modify_network_rule'] = True

            if new_rule_name and not utils.is_input_empty(new_rule_name):
                rule = new_rule_name

            current_rule_details = self.get_network_rule(groupnet,
                                                         subnet,
                                                         pool,
                                                         rule)
            result['network_rule_details'] = current_rule_details
        if result['create_network_rule'] or result['modify_network_rule'] or result['delete_network_rule']:
            result['changed'] = True

        self.module.exit_json(**result)


def get_network_rule_parameters():
    """
    This method provides parameters required for the ansible Network Provisioning Rule
    module on PowerScale
    """
    return dict(
        groupnet_name=dict(type='str', required=True),
        subnet_name=dict(type='str', required=True),
        pool_name=dict(type='str', required=True),
        description=dict(type='str'),
        iface=dict(type='str'),
        rule_name=dict(type='str', required=True),
        new_rule_name=dict(type='str'),
        node_type=dict(type='str', choices=['any', 'storage', 'accelerator', 'backup-accelerator']),
        state=dict(required=True, type='str', choices=['present', 'absent'])
    )


def main():
    """ Create PowerScale Network Provisioning Rule object and perform action on it
        based on user input from playbook"""
    obj = NetworkRule()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
