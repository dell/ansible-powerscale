#!/usr/bin/python
# Copyright: (c) 2021, Dell Technologies

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

    def get_sync_rule(self, sync_rule_id=None, sync_rule_dict=None):
        """
        Get SyncIQ performance rule details. If multiple instances are found for same
        performance rule configuration, error is thrown.
        :param sync_rule_id: ID of the performance rule
        :param sync_rule_dict: Dictionary of details of a performance rule
        :return: Dictionary of performance rule details if exists else none
        """
        duplicate_rule = []
        sync_rule_obj = None

        try:
            if sync_rule_id:
                sync_rule_obj = self.api_instance.get_sync_rule(sync_rule_id=sync_rule_id).rules[0]
                sync_rule_obj = sync_rule_obj.to_dict()
            else:
                sync_rule_list = self.api_instance.list_sync_rules().rules
                for rule in sync_rule_list:
                    rule = rule.to_dict()
                    if all(rule.get(key, None) == val for key, val in sync_rule_dict.items()) \
                            and rule['schedule'] == sync_rule_dict['schedule']:
                        duplicate_rule.append(rule)
                if len(duplicate_rule) > 1:
                    self.module.fail_json("Operation is not successful as "
                                          "more than one instance of "
                                          "SyncIQ performance rule is present with same configuration")
                elif len(duplicate_rule) == 1:
                    sync_rule_obj = duplicate_rule[0]
            return sync_rule_obj
        except utils.ApiException as e:
            if str(e.status) == '404':
                error_message = " Sync rule: %s not found." % sync_rule_id
                LOG.info(error_message)
                return None
            else:
                error_msg = utils.determine_error(error_obj=e)
                error_message = 'Failed to get SyncIQ rule with ' \
                                'error : %s' % str(error_msg)
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Failed to get SyncIQ rule with ' \
                            'error : %s' % str(error_msg)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

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

    def is_sync_rule_modifiable(self, existing_rule_dict, input_rule_dict):
        """
        Form dictionary of parameters for performance rule that is modifiable
        :param existing_rule_dict: Existing performance rule details dictionary
        :param input_rule_dict: Performance rule details dictionary provided by user
        :return: Dictionary of performance rule parameters that are modifiable
        """

        modify_rule_param = {}

        has_schedule_key = ['monday', 'tuesday', 'wednesday', 'thursday',
                            'friday', 'saturday', 'sunday', 'begin', 'end']

        if 'description' in input_rule_dict and input_rule_dict['description'] != existing_rule_dict['description']:
            modify_rule_param['description'] = input_rule_dict['description']

        if 'limit' in input_rule_dict and input_rule_dict['limit'] != existing_rule_dict['limit']:
            modify_rule_param['limit'] = input_rule_dict['limit']

        if 'enabled' in input_rule_dict and input_rule_dict['enabled'] != existing_rule_dict['enabled']:
            modify_rule_param['enabled'] = input_rule_dict['enabled']

        if 'schedule' in input_rule_dict:
            for key in has_schedule_key:
                if key not in input_rule_dict['schedule']:
                    input_rule_dict['schedule'].update({key: existing_rule_dict['schedule'][key]})

            if input_rule_dict['schedule'] != existing_rule_dict['schedule']:
                modify_rule_param['schedule'] = input_rule_dict['schedule']

        if 'type' in input_rule_dict and input_rule_dict['type'] != existing_rule_dict['type']:
            self.module.fail_json(msg="rule_type is not modifiable. Please create new SyncIQ rule for the rule_type.")

        return modify_rule_param

    def perform_module_operation(self):
        """
        Perform different actions on SyncIQ performance rule module based on
        parameters chosen in playbook
        """
        sync_rule_id = self.module.params['sync_rule_id']
        description = self.module.params['description']
        rule_type = self.module.params['rule_type']
        schedule = self.module.params['schedule']
        limit = self.module.params['limit']
        enabled = self.module.params['enabled']
        state = self.module.params['state']

        result = dict(
            changed=False,
            synciq_rule_details='',
            create_synciq_rule=False,
            modify_synciq_rule=False,
            delete_synciq_rule=False
        )

        # Check mandatory parameters for creating/ deleting a performance rule
        if sync_rule_id is None or state == 'absent':
            if rule_type is None or utils.is_input_empty(rule_type):
                self.module.fail_json(msg="Please provide rule_type to "
                                          "create/delete a SyncIQ performance rule.")
            if limit is None:
                self.module.fail_json(msg="Please provide limit to "
                                          "create/delete a SyncIQ performance rule.")
            if schedule is None:
                self.module.fail_json(msg="Please provide schedule to "
                                          "create/delete a SyncIQ performance rule.")
            if schedule is not None:
                if schedule['days_of_week'] is None:
                    self.module.fail_json(msg="Please provide days of a week, when an enabled rule is active,"
                                              " to create/delete a SyncIQ performance rule.")

                if schedule['begin'] is None:
                    self.module.fail_json(msg="Please provide scheduled begin time to "
                                              "create/delete a SyncIQ performance rule.")

                if schedule['end'] is None:
                    self.module.fail_json(msg="Please provide scheduled end time to "
                                              "create/delete a SyncIQ performance rule.")

            if enabled is None:
                self.module.fail_json(msg="Please provide whether performance rule is "
                                          "enabled to create/delete a SyncIQ rule.")

        if sync_rule_id is None and state == 'absent':
            self.module.fail_json(msg="Please provide sync_rule_id to delete a SyncIQ performance rule.")

        # Construct a dictionary for the parameters entered from playbook
        sync_rule_dict = construct_sync_rule_dict(description, rule_type, schedule, limit, enabled)

        rule_details = self.get_sync_rule(sync_rule_id, sync_rule_dict)

        if rule_details:
            sync_rule_id = rule_details['id']
        elif rule_details is None and sync_rule_id:
            sync_rule_id = None

        # Create a Rule
        if rule_details is None and state == 'present':
            sync_rule_id = self.create_sync_rule(sync_rule_dict)
            result['create_synciq_rule'] = True
        # Modify a rule
        elif sync_rule_id and state == 'present':
            modify_rule_dict = self.is_sync_rule_modifiable(rule_details, sync_rule_dict)
            if modify_rule_dict:
                result['modify_synciq_rule'] = self.modify_sync_rule(sync_rule_id, modify_rule_dict)
        # Delete a rule
        elif sync_rule_id and state == 'absent':
            if not self.is_sync_rule_modifiable(rule_details, sync_rule_dict):
                result['delete_synciq_rule'] = self.delete_sync_rule(sync_rule_id)

        # Display rule details
        if sync_rule_id and state == 'present':
            rule_details = self.get_sync_rule(sync_rule_id=sync_rule_id)
            result['synciq_rule_details'] = display_rule_details(rule_details)
        if result['create_synciq_rule'] or result['modify_synciq_rule'] or result['delete_synciq_rule']:
            result['changed'] = True

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
