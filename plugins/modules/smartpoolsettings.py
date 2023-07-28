#!/usr/bin/python
# Copyright: (c) 2022, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

""" Ansible module for managing smartpool settings on PowerScale"""
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: smartpoolsettings

version_added: "1.5.0"

short_description: Manages Smartpool Settings on PowerScale Storage System
description:
- Managing Smartpool Settings on the PowerScale Storage System includes
  modifying and retrieving details of Smartpool settings.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Meenakshi Dembi (@dembim) <ansible.team@dell.com>

options:
  virtual_hot_spare_hide_spare:
    description:
    - Hide reserved virtual hot spare space from free space counts.
    type: bool
  virtual_hot_spare_limit_percent:
    description:
    - The percent space to reserve for the virtual hot spare, from 0-20.
    type: int
  state:
    description:
    - State of smartpool settings.
    type: str
    required: true
    choices: ["present"]
notes:
- The I(check_mode) is not supported.
'''

EXAMPLES = r'''
  - name: Get SmartPool settings
    dellemc.powerscale.smartpoolsettings:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      state: "{{state_present}}"

  - name: Modify SmartPool setting
    dellemc.powerscale.smartpoolsettings:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      virtual_hot_spare_limit_percent: 10
      virtual_hot_spare_hide_spare: true
      state: "present"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
    sample: "false"

smartpool_settings:
    description: Details of the smartpool settings.
    returned: always
    type: dict
    contains:
        settings:
            description: Details of the settings.
            returned: Always
            type: dict
            contains:
                automatically_manage_io_optimization:
                    description: Automatically manage IO optimization settings on files.
                    type: str
                automatically_manage_protection:
                    description: Automatically manage protection settings on files.
                    type: str
                global_namespace_acceleration_enabled:
                    description: Optimize namespace operations by storing metadata on SSDs.
                    type: bool
                global_namespace_acceleration_state:
                    description: Whether or not namespace operation optimizations are currently in effect.
                    type: str
                protect_directories_one_level_higher:
                    description: Automatically add additional protection level to all directories.
                    type: bool
                spillover_enabled:
                    description: Spill writes into other pools as needed.
                    type: bool
                spillover_target:
                    description: Target pool for spilled writes.
                    type: dict
                ssd_l3_cache_default_enabled:
                    description: The L3 Cache default enabled state. This specifies whether L3 Cache should be enabled on new node pools.
                    type: bool
                ssd_qab_mirrors:
                    description: Controls number of mirrors of QAB blocks to place on SSDs.
                    type: str
                ssd_system_btree_mirrors:
                    description: Controls number of mirrors of system B-tree blocks to place on SSDs.
                    type: str
                ssd_system_delta_mirrors:
                    description: Controls number of mirrors of system delta blocks to place on SSDs.
                    type: str
                virtual_hot_spare_deny_writes:
                    description: Deny writes into reserved virtual hot spare space.
                    type: bool
                virtual_hot_spare_hide_spare:
                    description: Hide reserved virtual hot spare space from free space counts.
                    type: bool
                virtual_hot_spare_limit_drives:
                    description: The number of drives to reserve for the virtual hot spare, from 0-4.
                    type: int
                virtual_hot_spare_limit_percent:
                    description: The percent space to reserve for the virtual hot spare, from 0-20.
                    type: int
    sample:
        {
            "settings": {
                "automatically_manage_io_optimization": "files_at_default",
                "automatically_manage_protection": "files_at_default",
                "global_namespace_acceleration_enabled": false,
                "global_namespace_acceleration_state": "inactive",
                "protect_directories_one_level_higher": true,
                "spillover_enabled": true,
                "spillover_target": {
                    "id": null,
                    "name": null,
                    "type": "anywhere"
                },
                "ssd_l3_cache_default_enabled": true,
                "ssd_qab_mirrors": "one",
                "ssd_system_btree_mirrors": "one",
                "ssd_system_delta_mirrors": "one",
                "virtual_hot_spare_deny_writes": false,
                "virtual_hot_spare_hide_spare": true,
                "virtual_hot_spare_limit_drives": 0,
                "virtual_hot_spare_limit_percent": 20
            }
        }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

# initialize the logger
LOG = utils.get_logger('smartpoolsettings')


class SmartPoolSettings(object):
    """Class with  Smartpool Settings operations"""

    def __init__(self):
        """ Define all parameters required by this module"""

        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_smartpool_settings_parameters())

        # initialize the ansible module
        self.module = AnsibleModule(argument_spec=self.module_params)

        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        LOG.info('Got python SDK instance for provisioning on PowerScale for smartpool')
        self.storagepool_api = self.isi_sdk.StoragepoolApi(self.api_client)

    def get_smartpool_settings(self):
        """
        Get smartpool settings details
        :return: If exists returns the details of the smartpool settings
        """
        try:
            smartpool_settings = self.storagepool_api.get_storagepool_settings()
            return smartpool_settings.to_dict()
        except Exception as e:
            error_message = 'Retrieving details of smartpool settings failed ' \
                            'with error: %s ' % (e)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def modify_smartpool_settings(self, settings):
        """
        Modify smartpool settings.
        :param settings: Value of smartpool settings which need to be updated
        :return: True if modify is successful
        """
        try:
            self.storagepool_api.update_storagepool_settings(settings)
        except Exception as e:
            error_message = 'Modifying smartpool settings failed with ' \
                            'error: %s' % (e)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def validate_input(self, params):
        if params['virtual_hot_spare_limit_percent'] and (params['virtual_hot_spare_limit_percent'] < 0 or params['virtual_hot_spare_limit_percent'] > 20):
            self.module.fail_json(msg="Value of VHS has to be between 0 and 20%, "
                                  "please specify valid value.")

    def get_smartpool_setting_parameters(self, virtual_hot_spare_limit_percent):
        """
        Construct dictionary of parameters for updating smartpool settings.
        :param virtual_hot_spare_limit_percent: % space to reserve for virtual hot spare.
        :return: Dictionary of parameters for updating smartpool settings
        """
        storagepool_settings_params = {}
        storagepool_settings_params['virtual_hot_spare_limit_percent'] = virtual_hot_spare_limit_percent
        storagepool_settings_params['virtual_hot_spare_hide_spare'] = True
        return storagepool_settings_params

    def perform_module_operation(self):
        """
        Perform different actions based on parameters chosen in playbook
        """
        result = dict(
            changed=False,
            smartpool_settings=[]
        )
        virtual_hot_spare_hide_spare = self.module.params['virtual_hot_spare_hide_spare']
        virtual_hot_spare_limit_percent = self.module.params['virtual_hot_spare_limit_percent']
        input_params = self.module.params

        self.validate_input(input_params)

        existing_smartpool_settings = self.get_smartpool_settings()

        if virtual_hot_spare_limit_percent is not None and \
           (existing_smartpool_settings['settings']['virtual_hot_spare_limit_percent'] != virtual_hot_spare_limit_percent) \
           and virtual_hot_spare_hide_spare:
            smartpool_setting_params = self.get_smartpool_setting_parameters(virtual_hot_spare_limit_percent)
            self.modify_smartpool_settings(smartpool_setting_params)
            result['changed'] = True

        if result['changed']:
            result['smartpool_settings'] = self.get_smartpool_settings()
        else:
            result['smartpool_settings'] = existing_smartpool_settings

        self.module.exit_json(**result)


def get_smartpool_settings_parameters():
    """This method provide parameter required for the ansible Smartpool Settings
    module on PowerScale"""
    return dict(
        virtual_hot_spare_hide_spare=dict(type='bool'),
        virtual_hot_spare_limit_percent=dict(type='int'),
        state=dict(required=True, type='str', choices=['present']))


def main():
    """ Create PowerScale smartpool settings object and perform actions on it
        based on user input from playbook"""
    obj = SmartPoolSettings()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
