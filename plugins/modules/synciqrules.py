#!/usr/bin/python
# Copyright: (c) 2021-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

""" Ansible module for managing SyncIQ Performance Rules on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: synciqrules

version_added: "1.3.0"

short_description: Manage SyncIQ performance rules on PowerScale Storage System
description:
- Managing SyncIQ performance rules on PowerScale includes
  create a SyncIQ performance rule,
  modify a SyncIQ performance rule,
  get details of a SyncIQ performance rule,
  delete a SyncIQ performance rule.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale
author:
- Spandita Panigrahi (@panigs7) <ansible.team@dell.com>

options:
  rule_type:
    description:
    - The type of system resource this rule limits.
    - This is mandatory parameter while creating/deleting a performance rule.
    - This cannot be modified.
    type: str
    choices: ["bandwidth", "file_count", "cpu", "worker"]
  sync_rule_id:
    description:
    - This is an auto generated ID at the time of creation of SyncIQ performance rule.
    - For get/modify/delete operations I(sync_rule_id) is required.
    - The ID of a performance rule is not absolute to a particular existing rule configuration. The
      IDs are auto-sequenced during creation/deletion of a performance rule.
    type: str
  limit:
    description:
    - It tells the amount the specified system resource type is limited by this rule.
    - Units are kb/s for bandwidth, files/s for file-count, processing percentage used for cpu,
      or percentage of maximum available workers.
    - This is a mandatory parameter while creating/deleting a performance rule.
    type: int
  description:
    description:
    - User entered description of the performance rule.
    type: str
  enabled:
    description:
    - Indicates whether the performance rule is currently in effect during its specified interval.
    - This mandatory while creating/deleting a performance rule.
    type: bool
  schedule:
    description:
    - A schedule defining when during a week this performance rule is in effect.
    - It is mandatory to enter schedule while creating/deleting a performance rule.
    type: dict
    suboptions:
        begin:
            description:
            - Start time for this schedule, during its specified days.
            - It is of the format hh:mm (24 hour format).
            type: str
        end:
            description:
            - End time for this schedule, during its specified days.
            - It is of the format hh:mm (24 hour format).
            type: str
        days_of_week:
            description:
            - The days in a week when the performance rule is effective.
            type: list
            choices: ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            elements: str
  state:
    description:
    - The state option is used to determine whether the performance rule
      exists or not.
    type: str
    required: true
    choices: [ 'absent', 'present']

notes:
- Operations performed in parallel from other interfaces apart from
  playbook cannot guarantee desirable results.
- The I(check_mode) is not supported.
'''
EXAMPLES = r'''
- name: Create SyncIQ performance rule
  dellemc.powerscale.synciqrules:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    description: "Create a rule"
    enabled: true
    schedule:
    begin: "00:00"
    end: "13:30"
    days_of_week:
      - "monday"
      - "tuesday"
      - "sunday"
    rule_type: "cpu"
    limit: "80"
    state: "present"

- name: Modify SyncIQ performance rule
  dellemc.powerscale.synciqrules:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    sync_rule_id: "cpu-0"
    limit: "85"
    description: "Modify the performance rule"
    state: "present"

- name: Get SyncIQ performance rule details
  dellemc.powerscale.synciqrules:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    sync_rule_id: "cpu-0"
    state: "present"

- name: Delete SyncIQ performance rule
  dellemc.powerscale.synciqrules:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    sync_rule_id: "cpu-0"
    enabled: true
    schedule:
    begin: "00:00"
    end: "13:30"
    days_of_week:
      - "monday"
      - "tuesday"
      - "sunday"
    rule_type: "bandwidth"
    limit: "85"
    state: "absent"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
sync_rule_details:
    description: Details of the SyncIQ performance rule.
    returned: When SyncIQ performance rule exists
    type: complex
    contains:
        description:
            description: Description of the performance rule.
            type: str
        id:
            description: ID of the performance rule.
            type: str
        enabled:
            description: Indicates whether performance rule is enabled
            type: bool
        type:
            description: Type of performance rule
            type: str
        schedule:
            description: Duration when performance rule is effective
            type: str
        limit:
            description: Amount the specified system resource type is limited by this rule
            type: int
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('synciqrules')


class SynciqRules(object):

    """Class with SyncIQ Performance Rules operations"""

    def __init__(self):
        """ Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_synciqrules_parameters())

        # initialize the Ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False
        )
        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)

        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        self.api_instance = utils.isi_sdk.SyncApi(self.api_client)
        LOG.info('Got python SDK instance for provisioning on PowerScale')

    def _get_sync_rule_by_id(self, sync_rule_id):
        """Get sync rule by ID."""
        sync_rule_obj = self.api_instance.get_sync_rule(sync_rule_id=sync_rule_id).rules[0]
        return sync_rule_obj.to_dict()

    def _find_matching_sync_rule(self, sync_rule_dict):
        """Find matching sync rule from list based on dictionary criteria."""
        duplicate_rule = []
        sync_rule_list = self.api_instance.list_sync_rules().rules

        for rule in sync_rule_list:
            rule = rule.to_dict()
            if all(rule.get(key, None) == val for key, val in sync_rule_dict.items()) \
                    and rule['schedule'] == sync_rule_dict['schedule']:
                duplicate_rule.append(rule)

        return duplicate_rule

    def _validate_single_match(self, duplicate_rule):
        """Validate that only one matching rule exists."""
        if len(duplicate_rule) > 1:
            self.module.fail_json("Operation is not successful as "
                                  "more than one instance of "
                                  "SyncIQ performance rule is present with same configuration")
        elif len(duplicate_rule) == 1:
            return duplicate_rule[0]
        return None

    def _handle_api_exception(self, e, sync_rule_id):
        """Handle API exceptions when getting sync rule."""
        if str(e.status) == '404':
            error_message = " Sync rule: %s not found." % sync_rule_id
            LOG.info(error_message)
            return None
        else:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Failed to get SyncIQ rule with error : %s' % str(error_msg)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def _handle_general_exception(self, e):
        """Handle general exceptions when getting sync rule."""
        error_msg = utils.determine_error(error_obj=e)
        error_message = 'Failed to get SyncIQ rule with error : %s' % str(error_msg)
        LOG.error(error_message)
        self.module.fail_json(msg=error_message)

    def get_sync_rule(self, sync_rule_id=None, sync_rule_dict=None):
        """
        Get SyncIQ performance rule details. If multiple instances are found for same
        performance rule configuration, error is thrown.
        :param sync_rule_id: ID of the performance rule
        :param sync_rule_dict: Dictionary of details of a performance rule
        :return: Dictionary of performance rule details if exists else none
        """
        sync_rule_obj = None

        try:
            if sync_rule_id:
                sync_rule_obj = self._get_sync_rule_by_id(sync_rule_id)
            else:
                duplicate_rule = self._find_matching_sync_rule(sync_rule_dict)
                sync_rule_obj = self._validate_single_match(duplicate_rule)
            return sync_rule_obj
        except utils.ApiException as e:
            return self._handle_api_exception(e, sync_rule_id)
        except Exception as e:
            self._handle_general_exception(e)

    def create_sync_rule(self, sync_rule_param):
        """
        Create a performance rule.
        :param sync_rule_param: Dict of details to create a performance rule
        :return: ID of the newly created performance rule
        """
        try:
            LOG.info("Create syncIQ performance rule params %s", sync_rule_param)
            sync_rule_id = self.api_instance.create_sync_rule(sync_rule=sync_rule_param).id
            return sync_rule_id
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Failed to create SyncIQ rule with ' \
                            'error : %s' % str(error_msg)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def modify_sync_rule(self, sync_rule_id, sync_rule_param):
        """
        Modify  performance rule.
        :param sync_rule_id: ID of the performance rule that is to be modified
        :param sync_rule_param: Dict of parameters of performance rule that is to be modified
        :return: True if modification is successful
        """
        try:
            LOG.info("Modify SyncIQ performance rule params %s", sync_rule_param)
            self.api_instance.update_sync_rule(sync_rule_id=sync_rule_id, sync_rule=sync_rule_param)
            return True
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Failed to modify SyncIQ rule with ' \
                            'error : %s' % str(error_msg)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete_sync_rule(self, sync_rule_id):
        """
        Delete a performance rule
        :param sync_rule_id: ID of the performance rule to be deleted
        :return: True if delete operation is successful
        """
        try:
            LOG.info("Delete SyncIQ performance rule with id %s", sync_rule_id)
            self.api_instance.delete_sync_rule(sync_rule_id=sync_rule_id)
            return True
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Failed to delete SyncIQ rule with ' \
                            'error : %s' % str(error_msg)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def _check_field_modification(self, existing_rule_dict, input_rule_dict, field_name):
        """Check if a field has been modified and add to modify parameters."""
        if field_name in input_rule_dict and input_rule_dict[field_name] != existing_rule_dict[field_name]:
            return input_rule_dict[field_name]
        return None

    def _merge_schedule_keys(self, input_rule_dict, existing_rule_dict):
        """Merge missing schedule keys from existing rule into input rule."""
        has_schedule_key = ['monday', 'tuesday', 'wednesday', 'thursday',
                            'friday', 'saturday', 'sunday', 'begin', 'end']

        for key in has_schedule_key:
            if key not in input_rule_dict['schedule']:
                input_rule_dict['schedule'].update({key: existing_rule_dict['schedule'][key]})

    def _check_schedule_modification(self, existing_rule_dict, input_rule_dict):
        """Check if schedule has been modified and return modified schedule."""
        if 'schedule' not in input_rule_dict:
            return None

        self._merge_schedule_keys(input_rule_dict, existing_rule_dict)

        if input_rule_dict['schedule'] != existing_rule_dict['schedule']:
            return input_rule_dict['schedule']
        return None

    def _validate_type_not_modified(self, existing_rule_dict, input_rule_dict):
        """Validate that type field is not being modified (not allowed)."""
        if 'type' in input_rule_dict and input_rule_dict['type'] != existing_rule_dict['type']:
            self.module.fail_json(msg="rule_type is not modifiable. Please create new SyncIQ rule for the rule_type.")

    def is_sync_rule_modifiable(self, existing_rule_dict, input_rule_dict):
        """
        Form dictionary of parameters for performance rule that is modifiable
        :param existing_rule_dict: Existing performance rule details dictionary
        :param input_rule_dict: Performance rule details dictionary provided by user
        :return: Dictionary of performance rule parameters that are modifiable
        """
        modify_rule_param = {}

        # Check simple field modifications
        description = self._check_field_modification(existing_rule_dict, input_rule_dict, 'description')
        if description:
            modify_rule_param['description'] = description

        limit = self._check_field_modification(existing_rule_dict, input_rule_dict, 'limit')
        if limit:
            modify_rule_param['limit'] = limit

        enabled = self._check_field_modification(existing_rule_dict, input_rule_dict, 'enabled')
        if enabled:
            modify_rule_param['enabled'] = enabled

        # Check schedule modification
        schedule = self._check_schedule_modification(existing_rule_dict, input_rule_dict)
        if schedule:
            modify_rule_param['schedule'] = schedule

        # Validate type is not being modified
        self._validate_type_not_modified(existing_rule_dict, input_rule_dict)

        return modify_rule_param

    def _validate_sync_rule_params(self, sync_rule_id, rule_type, limit, schedule, enabled, state):
        """Validate mandatory parameters for creating/deleting a performance rule."""
        if sync_rule_id is not None and state != 'absent':
            return
        if rule_type is None or utils.is_input_empty(rule_type):
            self.module.fail_json(msg="Please provide rule_type to "
                                      "create/delete a SyncIQ performance rule.")
        if limit is None:
            self.module.fail_json(msg="Please provide limit to "
                                      "create/delete a SyncIQ performance rule.")
        if schedule is None:
            self.module.fail_json(msg="Please provide schedule to "
                                      "create/delete a SyncIQ performance rule.")
        if schedule is not None and schedule['days_of_week'] is None:
            self.module.fail_json(msg="Please provide days of a week, when an enabled rule is active,"
                                      " to create/delete a SyncIQ performance rule.")
        if schedule is not None and schedule['begin'] is None:
            self.module.fail_json(msg="Please provide scheduled begin time to "
                                      "create/delete a SyncIQ performance rule.")
        if schedule is not None and schedule['end'] is None:
            self.module.fail_json(msg="Please provide scheduled end time to "
                                      "create/delete a SyncIQ performance rule.")
        if enabled is None:
            self.module.fail_json(msg="Please provide whether performance rule is "
                                      "enabled to create/delete a SyncIQ rule.")
        if sync_rule_id is None and state == 'absent':
            self.module.fail_json(msg="Please provide sync_rule_id to delete a SyncIQ performance rule.")

    def _initialize_result_dict(self):
        """Initialize the result dictionary with default values."""
        return dict(
            changed=False,
            synciq_rule_details='',
            create_synciq_rule=False,
            modify_synciq_rule=False,
            delete_synciq_rule=False
        )

    def _get_module_params(self):
        """Get all module parameters."""
        return {
            'sync_rule_id': self.module.params['sync_rule_id'],
            'description': self.module.params['description'],
            'rule_type': self.module.params['rule_type'],
            'schedule': self.module.params['schedule'],
            'limit': self.module.params['limit'],
            'enabled': self.module.params['enabled'],
            'state': self.module.params['state']
        }

    def _resolve_sync_rule_id(self, sync_rule_id, rule_details):
        """Resolve the sync rule ID based on rule details."""
        if rule_details:
            return rule_details['id']
        elif rule_details is None and sync_rule_id:
            return None
        return sync_rule_id

    def _handle_rule_creation(self, sync_rule_dict, result):
        """Handle sync rule creation when state is present and rule doesn't exist."""
        sync_rule_id = self.create_sync_rule(sync_rule_dict)
        result['create_synciq_rule'] = True
        return sync_rule_id

    def _handle_rule_modification(self, sync_rule_id, rule_details, sync_rule_dict, result):
        """Handle sync rule modification when state is present and rule exists."""
        modify_rule_dict = self.is_sync_rule_modifiable(rule_details, sync_rule_dict)
        if modify_rule_dict:
            result['modify_synciq_rule'] = self.modify_sync_rule(sync_rule_id, modify_rule_dict)

    def _handle_rule_deletion(self, sync_rule_id, rule_details, sync_rule_dict, result):
        """Handle sync rule deletion when state is absent and rule exists."""
        if not self.is_sync_rule_modifiable(rule_details, sync_rule_dict):
            result['delete_synciq_rule'] = self.delete_sync_rule(sync_rule_id)

    def _update_rule_details_display(self, sync_rule_id, result):
        """Update result with rule details for display when state is present."""
        if sync_rule_id:
            rule_details = self.get_sync_rule(sync_rule_id=sync_rule_id)
            result['synciq_rule_details'] = display_rule_details(rule_details)

    def _update_changed_status(self, result):
        """Update changed status based on operations performed."""
        if result['create_synciq_rule'] or result['modify_synciq_rule'] or result['delete_synciq_rule']:
            result['changed'] = True

    def perform_module_operation(self):
        """
        Perform different actions on SyncIQ performance rule module based on
        parameters chosen in playbook
        """
        params = self._get_module_params()
        result = self._initialize_result_dict()

        self._validate_sync_rule_params(params['sync_rule_id'], params['rule_type'],
                                        params['limit'], params['schedule'],
                                        params['enabled'], params['state'])

        # Construct a dictionary for the parameters entered from playbook
        sync_rule_dict = construct_sync_rule_dict(
            params['description'], params['rule_type'],
            params['schedule'], params['limit'],
            params['enabled'])

        rule_details = self.get_sync_rule(params['sync_rule_id'], sync_rule_dict)
        sync_rule_id = self._resolve_sync_rule_id(params['sync_rule_id'], rule_details)

        # Create a Rule
        if rule_details is None and params['state'] == 'present':
            sync_rule_id = self._handle_rule_creation(sync_rule_dict, result)

        # Modify a rule
        elif sync_rule_id and params['state'] == 'present':
            self._handle_rule_modification(sync_rule_id, rule_details, sync_rule_dict, result)

        # Delete a rule
        elif sync_rule_id and params['state'] == 'absent':
            self._handle_rule_deletion(sync_rule_id, rule_details, sync_rule_dict, result)

        # Display rule details
        if params['state'] == 'present':
            self._update_rule_details_display(sync_rule_id, result)

        self._update_changed_status(result)
        self.module.exit_json(**result)


def get_sync_rule_limit_unit(limit, type):
    """Get performance rule limit with unit"""
    if type == 'bandwidth':
        unit = 'kb/s'
    elif type == 'cpu':
        unit = '%'
    elif type == 'file_count':
        unit = 'files/sec'
    elif type == 'worker':
        unit = '%'

    return str(limit) + unit


def display_rule_details(rule_details):
    """
    Display attributes of performance rules in the output
    :param rule_details: Dict of performance rule details to be displayed
    :return: Dict of performance rule details
    """
    rule_details['limit'] = get_sync_rule_limit_unit(rule_details['limit'], rule_details['type'])
    return rule_details


def construct_sync_rule_dict(description, rule_type, schedule, limit, enabled):
    """
    Construct SyncIQ rule dictionary
    :param description: Description of performance rule
    :param rule_type: Type of the performance rule
    :param schedule: Schedule of the performance rule
    :param limit: Limit for the rule_type
    :param enabled: Indicates whether rule is enabled
    :return: Dictionary of rule details
    """
    sync_rule_dict = {}
    days_of_week_list = ['monday', 'tuesday', 'wednesday', 'thursday',
                         'friday', 'saturday', 'sunday']
    days_of_week_dict = {'monday': False,
                         'tuesday': False,
                         'wednesday': False,
                         'thursday': False,
                         'friday': False,
                         'saturday': False,
                         'sunday': False}

    if description is not None:
        sync_rule_dict['description'] = description

    if rule_type and not utils.is_input_empty(rule_type):
        sync_rule_dict['type'] = rule_type

    if limit is not None:
        sync_rule_dict['limit'] = limit

    if enabled is not None:
        sync_rule_dict['enabled'] = enabled

    if schedule is not None:
        sync_rule_dict['schedule'] = {}
        if schedule['days_of_week'] is not None:
            for day in schedule['days_of_week']:
                if day in days_of_week_list:
                    days_of_week_dict[day] = True
            sync_rule_dict['schedule'] = days_of_week_dict
        if schedule['begin'] and not utils.is_input_empty(schedule['begin']):
            sync_rule_dict['schedule'].update({'begin': schedule['begin']})

        if schedule['end'] and not utils.is_input_empty(schedule['end']):
            sync_rule_dict['schedule'].update({'end': schedule['end']})

    return sync_rule_dict


def get_synciqrules_parameters():
    """This method provides parameters required for the ansible SyncIQ performance rule
       module on PowerScale"""
    return dict(
        description=dict(type='str'),
        enabled=dict(type='bool'),
        limit=dict(type='int'),
        rule_type=dict(type='str', choices=['bandwidth', 'file_count', 'cpu', 'worker']),
        schedule=dict(type='dict', options=dict(begin=dict(type='str'),
                                                end=dict(type='str'),
                                                days_of_week=dict(type='list',
                                                                  choices=['monday', 'tuesday',
                                                                           'wednesday', 'thursday', 'friday',
                                                                           'saturday', 'sunday'], elements='str')
                                                )),
        sync_rule_id=dict(type='str'),
        state=dict(required=True, type='str', choices=['present', 'absent'])
    )


def main():
    """ Create PowerScale SyncIQ performance rule object and perform action on it
        based on user input from playbook"""
    obj = SynciqRules()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
