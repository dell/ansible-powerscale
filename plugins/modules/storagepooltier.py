#!/usr/bin/python
# Copyright: (c) 2022, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing storage pool tier on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: storagepooltier

version_added: '1.6.0'

short_description: Manages storage pool tier on PowerScale
description:
- Managing storage pool tier on PowerScale Storage System. This includes
  creating a new storage pool tier, deleting a storage pool tier and
  retrieving the details of a storage pool tier.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Ananthu S Kuttattu (@kuttattz) <ansible.team@dell.com>

options:
  tier_id:
    description:
    - Unique Id of the storage pool tier.
    - It is mutually exclusive with I(tier_name).
    type: int

  tier_name:
    description:
    - Unique name of the storage pool tier.
    - It is mutually exclusive with I(tier_id).
    - Mandatory for storage pool tier creation.
    type: str

  nodepools:
    description:
    - List of names of the nodepool's.
    type: list
    elements: str

  state:
    description:
    - The state option is used to mention the existence of storage pool tier.
    type: str
    required: true
    choices: [absent, present]
notes:
- Modifying a storage pool tier is not supported.
- The I(check_mode) is supported.
'''

EXAMPLES = r'''
- name: Get storage pool tier details
  dellemc.powerscale.storagepooltier:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    tier_name: "test_tier"
    state: 'present'

- name: Create a storage pool tier
  dellemc.powerscale.storagepooltier:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    tier_name: "test_tier"
    nodepools:
      - "test_nodepool"
    state: 'present'

- name: Delete a storage pool tier
  dellemc.powerscale.storagepooltier:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    tier_name: "test_tier"
    state: 'absent'
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
    sample: "false"
storage_pool_tier_details:
    description: Storage pool tier details.
    returned: When a tier exists
    type: complex
    contains:
        "id":
            description: Unique ID of the storage pool tier.
            type: int
        "name":
            description: Unique name of the storage pool tier.
            type: str
        "children":
            description: Nodepool's of the storage pool tier.
            type: list
        "lnns":
            description: The nodes that are part of this tier.
            type: list

    sample:
        {"storage_pool_tier_details": {
            "children": [
                "test_nodepool"
            ],
            "id": 1,
            "lnns": [
                1,
                2,
                3
            ],
            "name": "test_tier"
            }
        }
'''

from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
from ansible.module_utils.basic import AnsibleModule

LOG = utils.get_logger('storagepooltier')


class StoragePoolTier(object):
    """Class with operations on storage pool tier"""

    def __init__(self):
        """ Define all parameters required by this module"""

        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(self.get_tier_parameters())
        # initialize the Ansible module
        mutually_exclusive = [['tier_name', 'tier_id']]
        self.module = AnsibleModule(argument_spec=self.module_params,
                                    mutually_exclusive=mutually_exclusive,
                                    supports_check_mode=True)

        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.storagepool_api = utils.isi_sdk.StoragepoolApi(self.api_client)
        LOG.info('Got the isi_sdk instance for authorization on to PowerScale')
        check_mode_msg = f'Check mode flag is {self.module.check_mode}'
        LOG.info(check_mode_msg)

    def get_tier_details(self, tier_name=None, tier_id=None):
        """
        Get storage pool tier details
        :param tier_name: Storagepool tier name
        :param tier_id: Storagepool tier id
        :return: storage pool tier details
        """
        try:
            if tier_id:
                api_response = self.storagepool_api.get_storagepool_tier(tier_id).to_dict()
                return api_response['tiers'][0]
            else:
                list_of_storagepool_tiers = self.storagepool_api.list_storagepool_tiers().to_dict()
                for storagepool_tier in list_of_storagepool_tiers['tiers']:
                    if storagepool_tier['name'] == tier_name:
                        return storagepool_tier
                return None
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Fetching storage pool tier details failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_node_pool_name_list(self):
        """
        Getting list of node pools name's
        :return: List nodepool's name
        """
        try:
            node_pool_list = []
            node_pool_details = (self.storagepool_api.list_storagepool_nodepools()).to_dict()
            node_pools = node_pool_details['nodepools']
            if node_pools:
                for item in node_pools:
                    node_pool_list.append(item["name"])
            return node_pool_list
        except Exception as e:
            error_msg = f'Getting list of nodepools names failed with error: {utils.determine_error(e)}'
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def create_tier(self, tier_name, nodepools):
        """
        Create storage pool tier
        :param tier_name: Storage pool tier name.
        :param nodepools: List of nodepool's.
        :return: create tier response.
        """
        try:
            tier_data = {
                "name": tier_name,
                "children": nodepools
            }
            create_msg = f'Creating storage pool tier {tier_name}'
            LOG.info(create_msg)
            if not self.module.check_mode:
                tier_object = utils.isi_sdk.StoragepoolTierCreateParams(**tier_data)
                create_tier_response = self.storagepool_api.create_storagepool_tier(tier_object)
                return create_tier_response
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Creating storage pool tier failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete_tier(self, tier_id):
        """
        Delete storage pool tier based on id
        :param tier_id: Storage pool tier id.
        :return: None.
        """
        try:
            LOG.info('Deleting storage pool tier')
            if not self.module.check_mode:
                self.storagepool_api.delete_storagepool_tier(tier_id)
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Deleting storage pool tier failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def is_tier_modified(self, tier_details, nodepools):
        """
        Check if tier is modified or not
        :param tier_details: tier details
        :param nodepools: List of nodepool's.
        :return: tier modified values
        """
        modified_fields = {}
        if nodepools is not None and tier_details['children'] != nodepools:
            modified_fields['nodepools'] = nodepools
        return modified_fields

    def validate_create_inputs(self, tier_name, nodepools):
        """
        Validate create inputs
        :param tier_name: Storage pool tier name.
        :param nodepools: List of nodepools
        :return: None.
        """
        if not tier_name:
            err_msg = "'tier_name' is required to create a storage pool tier"
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)
        if nodepools is not None and nodepools != []:
            nodepool_name_list = self.get_node_pool_name_list()
            diff = set(nodepools) - set(nodepool_name_list)
            if diff != set():
                err_msg = f"nodepool's {diff} are invalid."
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)

    def perform_module_operation(self):
        """
        Perform different actions based on parameters chosen in playbook
        """
        result = dict(
            changed=False
        )
        tier_id = self.module.params['tier_id']
        tier_name = self.module.params['tier_name']
        nodepools = self.module.params['nodepools']
        state = self.module.params['state']

        tier_details = self.get_tier_details(tier_name=tier_name, tier_id=tier_id)

        if state == 'present':
            if not tier_details:
                self.validate_create_inputs(tier_name, nodepools)
                self.create_tier(tier_name, nodepools)
                result['changed'] = True
            else:
                tier_name = tier_details['name']
                modified_fields = self.is_tier_modified(tier_details, nodepools)
                if modified_fields != {}:
                    err_msg = "Storage pool tier modification not supported."
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)

        elif state == 'absent' and tier_details:
            tier_name = tier_details['name']
            self.delete_tier(tier_details['id'])
            result['changed'] = True

        if result['changed']:
            result['storage_pool_tier_details'] = self.get_tier_details(tier_name=tier_name)
        else:
            result['storage_pool_tier_details'] = tier_details

        self.module.exit_json(**result)

    def get_tier_parameters(self):
        return dict(
            tier_id=dict(type='int'),
            tier_name=dict(type='str'),
            nodepools=dict(type='list', elements='str'),
            state=dict(required=True, type='str',
                       choices=['present', 'absent'])
        )


def main():
    """ Create PowerScale StoragePoolTier object and perform actions
         on it based on user input from the playbook"""
    obj = StoragePoolTier()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
