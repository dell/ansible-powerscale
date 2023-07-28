#!/usr/bin/python
# Copyright: (c) 2021, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

""" Ansible module for managing nodes on PowerScale"""
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: node
version_added: '1.2.0'

short_description: Get node info of PowerScale Storage System

description:
- Get information of a node belonging to the PowerScale cluster.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Ganesh Prabhu(@prabhg5) <ansible.team@dell.com>>

options:
  node_id:
    description:
    - The Logical node Number of a PowerScale cluster node.
    required: true
    type: int
  state:
    description:
    - Defines whether the node should exist or not.
    required: true
    choices: [absent, present]
    type: str
notes:
- The I(check_mode) is not supported.
'''
EXAMPLES = r'''
- name: Get node info of the PowerScale cluster node
  dellemc.powerscale.node:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    node_id: "{{cluster_node_id}}"
    state: "present"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
    sample: "false"

cluster_node_details:
    description: The cluster node details.
    type: dict
    returned: When cluster node exists
    contains:
        id:
            description: Node id (device number) of a node.
            type: int
        lnn:
            description: Logical Node Number (LNN) of a node.
            type: int
        partitions:
            description: Node partition information.
            type: complex
            contains:
                count:
                    description: Count of how many partitions are included.
                    type: int
    sample:
        {
            "id": 1,
            "lnn": 1,
            "partitions": {
                "count": 1,
                "partitions": [
                    {
                        "block_size": 1024,
                        "capacity": 1957516,
                        "component_devices": "ada0p2",
                        "mount_point": "/",
                        "percent_used": "50%",
                        "statfs": {
                        "f_namemax": 255,
                        "f_owner": 0,
                        "f_type": 53,
                        "f_version": 538182936
                        },
                        "used": 909066
                    }
                ]
            }
        }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('node')


class ClusterNode(object):
    def __init__(self):
        """Define all the parameters required by this module"""

        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_node_parameters())

        # initialize the Ansible module
        self.module = AnsibleModule(argument_spec=self.module_params,
                                    supports_check_mode=False
                                    )
        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        LOG.info('Got python SDK instance for provisioning on PowerScale ')
        self.cluster_api = self.isi_sdk.ClusterApi(self.api_client)

    def get_node_info(self, node_id):
        """get the specific cluster node information from PowerScale storage"""
        try:
            node_info = (self.cluster_api.get_cluster_node(node_id)).to_dict()
            LOG.info('Got node information from PowerScale cluster %s', self.module.params['onefs_host'])
            return node_info
        except Exception as e:
            error_msg = (
                'get node info for PowerScale cluster: {0} failed with'
                'error: {1} ' .format(
                    self.module.params['onefs_host'], utils.determine_error(error_obj=e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def perform_module_operation(self):
        node_id = self.module.params['node_id']
        state = self.module.params['state']
        result = dict(
            changed=False
        )
        if state == 'absent':
            error_message = 'Deletion of node is not allowed through' \
                            ' Ansible module'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
        if node_id and state == 'present':
            info_message = 'getting Cluster Node: ' \
                           '{0} info'.format(node_id)
            LOG.info(info_message)
            result['cluster_node_details'] = \
                self.get_node_info(node_id)
        else:
            error_message = 'Please provide a valid Node Id'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
        # Finally update the module result!
        self.module.exit_json(**result)


def get_node_parameters():
    """This method provides parameters required for the ansible cluster
                modules on PowerScale"""
    return dict(
        node_id=dict(required=True, type='int'),
        state=dict(required=True, type='str',
                   choices=['present', 'absent'])
    )


def main():
    """Create PowerScale cluster node object and perform action on it
        based on user input from playbook"""
    obj = ClusterNode()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
