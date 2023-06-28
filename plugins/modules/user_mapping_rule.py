#!/usr/bin/python
# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

""" Ansible module for managing user mapping rules on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: user_mapping_rule

version_added: '2.0.0'

short_description: Manages user mapping rules on PowerScale
description:
- Manages user mapping rules on PowerScale Storage System. This includes
  creating a new user mapping rule, modifying a user mapping rule,
  changing order of a user mapping rule, deleting a user mapping rule and
  retrieving the details of a user mapping rule.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Ananthu S Kuttattu (@kuttattz) <ansible.team@dell.com>

options:
  apply_order:
    description:
    - Current order in which the user mapping rule is applied.
    type: int

  new_order:
    description:
    - New order in which the user mapping rule should be applied.
    type: int

  access_zone:
    description: The zone to which the user mapping applies.
    type: str
    default: 'System'

  rule:
    description: The user mapping rule.
    type: dict
    suboptions:
      operator:
        description:
        - The operation that a rule carries out.
        type: str
        choices: ['insert', 'append', 'union', 'replace', 'trim']
      options:
        description:
        - Specifies the properties for user mapping rules.
        type: dict
        suboptions:
          break_on_match:
            description:
            - If C(true), and the rule was applied successfuly, stop processing further.
            type: bool
          default_user:
                description:
                - If the mapping service fails to find the second user in a rule, the service tries to find the username of the default user.
                type: dict
                suboptions:
                  domain:
                    description: The name of domain.
                    type: str
                  user:
                    description: The username of the user.
                    type: str
                    required: true
          group:
            description:
            - If C(true), the primary GID and primary group SID should be copied to the existing credential.
            type: bool
          groups:
            description:
            - If C(true), all additional identifiers should be copied to the existing credential.
            type: bool
          user:
            description:
            - If C(true), the primary UID and primary user SID should be copied to the existing credential.
            type: bool
      user1:
        description:
        - A UNIX user or an Active Directory user.
        - The user for which the identifier changes are applied.
        type: dict
        suboptions:
            domain:
                description: The name of domain.
                type: str
            user:
                description: The username of the user.
                type: str
                required: true
      user2:
        description:
        - A UNIX user or an Active Directory user.
        - The user from which the identifier are taken.
        type: dict
        suboptions:
            domain:
                description: The name of domain.
                type: str
            user:
                description: The username of the user.
                type: str
                required: true
  state:
    description:
    - The state option is used to mention the existence of user mapping rule.
    type: str
    choices: ['absent', 'present']
    default: 'present'
notes:
- Idempotency is not supported for create and delete operations.
- The I(check_mode) is supported.
'''

EXAMPLES = r'''
  - name: Get a user mapping rule
    dellemc.powerscale.user_mapping_rule:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      apply_order: 1

  - name: Delete a user mapping rule
    dellemc.powerscale.user_mapping_rule:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      apply_order: 1
      state: 'absent'

  - name: Create a user mapping rule
    dellemc.powerscale.user_mapping_rule:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      rule:
        operator: "insert"
        options:
          break: false
          group: true
          groups: true
          user: true
        user1:
          domain: "ansibleneo.com"
          user: "test_user"
        user2:
          user: "ans_user"
      state: 'present'

  - name: Update a user mapping rule
    dellemc.powerscale.user_mapping_rule:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      apply_order: 1
      rule:
        options:
          break: true
      state: 'present'

  - name: Apply a new order to the user mapping rule
    dellemc.powerscale.user_mapping_rule:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      apply_order: 1
      new_order: 2
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
    sample: "false"
user_mapping_rule_details:
    description: Rule details.
    returned: When a rule exists
    type: dict
    contains:
        apply_order:
            description: Current order of the rule.
            type: int
        operator:
            description: The operation that a rule carries out.
            type: str
        options:
            description: Specifies the properties for user mapping rules.
            type: dict
            contains:
                _break:
                    description: If C(true), and the rule was applied successfuly, stop processing further.
                    type: bool
                group:
                    description: If C(true), the primary GID and primary group SID should be copied to the existing credential.
                    type: bool
                groups:
                    description: If C(true), all additional identifiers should be copied to the existing credential.
                    type: bool
                user:
                    description: If C(true), the primary UID and primary user SID should be copied to the existing credential.
                    type: bool
                default_user:
                    description: If the mapping service fails to find the second user in a rule, the service tries to find the username of the default user..
                    type: dict
                    contains:
                        user:
                           description: The username of the user.
                           type: str
                        domain:
                           description: The name of domain.
                           type: str
        user1:
            description: A UNIX user or an Active Directory user.
            type: dict
            contains:
                user:
                    description: The username of the user.
                    type: str
                domain:
                    description: The name of domain.
                    type: str
        user2:
            description: A UNIX user or an Active Directory user.
            type: dict
            contains:
                user:
                    description: The username of the user.
                    type: str
                domain:
                    description: The name of domain.
                    type: str
    sample:
        {"user_mapping_rule_details": {
            "apply_order": 7,
            "operator": "insert",
            "options": {
                "_break": false,
                "default_user": null,
                "group": true,
                "groups": true,
                "user": true
            },
            "user1": {
                "domain": null,
                "user": "test_ans_user"
            },
            "user2": {
                "domain": null,
                "user": "Test_userAnand"
            }
        }}
'''

from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
from ansible.module_utils.basic import AnsibleModule
import copy

LOG = utils.get_logger('user_mapping_rule')


class UserMappingRule(object):
    """Class with operations on user mapping rule"""

    def __init__(self):
        """ Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(self.get_user_mapping_rule_parameters())
        # initialize the Ansible module
        self.module = AnsibleModule(argument_spec=self.module_params,
                                    supports_check_mode=True)
        self.result = dict(
            changed=False,
            user_mapping_rule_details={}
        )
        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.auth_api = utils.isi_sdk.AuthApi(self.api_client)
        LOG.info('Got the isi_sdk instance for authorization on to PowerScale')
        check_mode_msg = f'Check mode flag is {self.module.check_mode}'
        LOG.info(check_mode_msg)

    def form_rule_operations_payload(self, rule_operations):
        """
        Form rule operations payload
        :param rule_operations: Rule operations
        :return: formatted rule operations.
        """
        formatted_rule_operations = {}
        if 'break_on_match' in rule_operations:
            formatted_rule_operations['_break'] = rule_operations['break_on_match'] if rule_operations['break_on_match'] else False
        elif '_break' in rule_operations:
            formatted_rule_operations['_break'] = rule_operations['_break'] if rule_operations['_break'] else False
        formatted_rule_operations['default_user'] = rule_operations['default_user']
        sub_ops = ['group', 'groups', 'user']
        for ops in sub_ops:
            formatted_rule_operations[ops] = rule_operations[ops] if rule_operations[ops] else False
        return formatted_rule_operations

    def form_rule_payload(self, rule):
        """
        Form rule payload
        :param rule: Rule data
        :return: formatted rule.
        """
        formatted_rule = {
            'operator': rule['operator']
        }

        if 'options' in rule and rule['options'] is not None:
            formatted_rule['options'] = self.form_rule_operations_payload(rule['options'])
        else:
            formatted_rule['options'] = None

        if 'user1' in rule and rule['user1'] is not None:
            formatted_rule['user1'] = rule['user1']

        if 'user2' in rule and rule['user2'] is not None:
            formatted_rule['user2'] = rule['user2']
        else:
            formatted_rule['user2'] = None

        return formatted_rule

    def form_create_user_mapping_rule_object(self, rules_list):
        """
        Form mapping user rules object
        :param rules_list: Rule list
        :return: Mapping user rules object.
        """
        LOG.info('Forming user mapping rule object')
        rule_object_list = []
        for rule in rules_list:
            rule_object_payload = {
                'operator': rule['operator']
            }
            if rule['options'] is not None:
                options_object_payload = {}
                if rule['options']['default_user'] is not None:
                    options_object_payload['default_user'] = utils.isi_sdk.MappingUsersRulesRuleOptionsDefaultUser(**rule['options']['default_user'])
                options_object_payload['_break'] = rule['options']['_break']
                options_object_payload['group'] = rule['options']['group']
                options_object_payload['groups'] = rule['options']['groups']
                options_object_payload['user'] = rule['options']['user']
                options_object = utils.isi_sdk.MappingUsersRulesRuleOptionsExtended(**options_object_payload)
                rule_object_payload['options'] = options_object
            rule_object_payload['user1'] = utils.isi_sdk.MappingUsersRulesRuleUser1(**rule['user1'])
            if rule['user2']:
                rule_object_payload['user2'] = utils.isi_sdk.MappingUsersRulesRuleUser2Extended(**rule['user2'])
            rule_object = utils.isi_sdk.MappingUsersRulesRuleExtended(
                **rule_object_payload
            )
            rule_object_list.append(rule_object)
        mapping_users_rules_object = utils.isi_sdk.MappingUsersRulesExtended(rules=rule_object_list)
        LOG.info('Forming user mapping rule object completed')
        return mapping_users_rules_object

    def validate_for_trim_operator(self, rule):
        """
        Validate for trim operator
        :param rule: Rule data.
        :return: None.
        """
        sub_ops = ['group', 'groups', 'user', 'default_user']
        for ops in sub_ops:
            if 'options' in rule and ops in rule['options'] and rule['options'][ops] is not None:
                err_msg = f" '{sub_ops}' cannot be given with 'trim' operator."
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
        if 'user2' in rule and rule['user2'] is not None:
            err_msg = "'user2' cannot be given with 'trim' operator."
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)

    def validate_for_specific_operators(self, rule):
        """
        Validate for specific operators
        :param rule: Rule data.
        :return: None.
        """
        subset_operators = ['replace', 'union']
        if 'operator' in rule and rule['operator'] in subset_operators and rule['options'] is not None:
            sub_ops = ['group', 'groups', 'user']
            for ops in sub_ops:
                if 'options' in rule and ops in rule['options'] and rule['options'][ops] is not None:
                    err_msg = f" '{sub_ops}' cannot be given with '{subset_operators}' operators."
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)
        if 'operator' in rule and rule['operator'] == 'trim':
            self.validate_for_trim_operator(rule)

    def validate_inputs(self, rule):
        """
        Validate create inputs
        :param rule: Rule data.
        :return: None.
        """
        if rule:
            if 'operator' not in rule or rule['operator'] is None:
                err_msg = " 'operator' is required for creation of user mapping rule."
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
            if 'user1' not in rule or rule['user1'] is None:
                err_msg = " 'user1' is required for creation of user mapping rule."
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
            if 'operator' in rule and rule['operator'] != 'trim' and ('user2' not in rule or rule['user2'] is None):
                err_msg = " 'user2' is required for creation of user mapping rule."
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
            self.validate_for_specific_operators(rule)

    def form_rule_for_operator_update(self, update_rule, new_rule_data, rule_details):
        """
        Check and form rule for operator update
        :param update_rule: Updated rule data
        :param new_rule_data: New rule data.
        :param rule_details: Existing rule data.
        :return: Updated rule data.
        """
        self.validate_for_specific_operators(new_rule_data)
        if rule_details['operator'] == 'trim':
            if 'user2' not in new_rule_data or new_rule_data['user2'] is None:
                operator = new_rule_data['operator']
                err_msg = f" 'user2' is required for {operator}."
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
            else:
                update_rule['user2'] = new_rule_data['user2']
        if new_rule_data['operator'] in ['replace', 'union', 'trim']:
            update_rule['options']['group'] = False
            update_rule['options']['groups'] = False
            update_rule['options']['user'] = False
        if new_rule_data['operator'] == 'trim':
            update_rule['user2'] = None
            update_rule['options']['default_user'] = None
        return update_rule

    def form_rule_for_operations_update(self, update_rule, new_rule_data, do_update):
        """
        Check and form rule for operations update
        :param update_rule: Updated rule data
        :param new_rule_data: New rule data.
        :param do_update: Is update required.
        :return: True if update is needed and and the new updated rule.
        """
        sub_ops = ['_break', 'group', 'groups', 'user']
        for ops in sub_ops:
            if ops != '_break' and ops in new_rule_data['options'] and new_rule_data['options'][ops] is not None \
               and new_rule_data['options'][ops] != update_rule['options'][ops]:
                update_rule['options'][ops] = new_rule_data['options'][ops]
                do_update = True
            elif ops == '_break' and 'break_on_match' in new_rule_data['options'] and new_rule_data['options']['break_on_match'] is not None and \
                        new_rule_data['options']['break_on_match'] != update_rule['options'][ops]:
                update_rule['options'][ops] = new_rule_data['options']['break_on_match']
                do_update = True

        if 'default_user' in new_rule_data['options'] and new_rule_data['options']['default_user'] is not None:
            if update_rule['options']['default_user'] is None:
                update_rule['options']['default_user'] = {
                    'user': None,
                    'domain': None
                }
            if 'domain' in new_rule_data['options']['default_user'] and \
                    new_rule_data['options']['default_user']['domain'] != update_rule['options']['default_user']['domain']:
                update_rule['options']['default_user']['domain'] = new_rule_data['options']['default_user']['domain']
                do_update = True
            if new_rule_data['options']['default_user']['user'] != update_rule['options']['default_user']['user']:
                update_rule['options']['default_user']['user'] = new_rule_data['options']['default_user']['user']
                do_update = True
        return do_update, update_rule

    def form_rule_for_user_update(self, key, update_rule, new_rule_data, do_update):
        """
        Check and form rule for user update
        :param update_rule: Updated rule data
        :param new_rule_data: New rule data.
        :param do_update: Is update required.
        :return: True if update is needed and and the new updated rule.
        """
        if 'domain' in new_rule_data[key] and new_rule_data[key]['domain'] != update_rule[key]['domain']:
            update_rule[key]['domain'] = new_rule_data[key]['domain']
            do_update = True
        if new_rule_data[key]['user'] != update_rule[key]['user']:
            update_rule[key]['user'] = new_rule_data[key]['user']
            do_update = True
        return do_update, update_rule

    def check_new_order_update(self, apply_order, new_order, do_update):
        """
        Check for order update
        :param apply_order: Updated rule data
        :param new_order: New rule data.
        :param do_update: Is update required.
        :return: do_update.
        """
        if new_order <= 0:
            error_message = "new_order should be greater than 0."
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
        if new_order != apply_order:
            return True
        return do_update

    def check_and_form_rule_for_update(self, new_rule_params, rule_details):
        """
        Check for rule update
        :param new_rule_params: New rule params.
        :param rule_details: Existing Rule data.
        :return: True if update is needed and and the new updated rule.
        """
        LOG.info("Check for rule update")
        update_rule = copy.deepcopy(rule_details)
        do_update = False
        new_rule_data = new_rule_params['rule']
        if new_rule_data:
            if 'operator' in new_rule_data and new_rule_data['operator'] is not None and new_rule_data['operator'] != rule_details['operator']:
                update_rule['operator'] = new_rule_data['operator']
                update_rule = self.form_rule_for_operator_update(update_rule, new_rule_data, rule_details)
                do_update = True
            if 'options' in new_rule_data and new_rule_data['options'] is not None:
                do_update, update_rule = self.form_rule_for_operations_update(update_rule, new_rule_data, do_update)
            if 'user1' in new_rule_data and new_rule_data['user1'] is not None:
                do_update, update_rule = self.form_rule_for_user_update('user1', update_rule, new_rule_data, do_update)
            if 'user2' in new_rule_data and new_rule_data['user1'] is not None:
                do_update, update_rule = self.form_rule_for_user_update('user2', update_rule, new_rule_data, do_update)
        if 'new_order' in new_rule_params and new_rule_params['new_order'] is not None:
            do_update = self.check_new_order_update(new_rule_params['apply_order'], new_rule_params['new_order'], do_update)
        return do_update, update_rule

    def update_sdk_call(self, rules_list, access_zone):
        """
        Execute SDK call for create, update and delete of user mapping rule
        :param rules_list: List of user mapping rules
        :param access_zone: Access zone.
        :return: None
        """
        mapping_users_rules_object = self.form_create_user_mapping_rule_object(rules_list)
        self.auth_api.update_mapping_users_rules(mapping_users_rules_object, zone=access_zone)

    def get_rule_details(self, apply_order=None, access_zone=None, rule_list=False):
        """
        Get user mapping rule by apply_order
        :param apply_order: Current user mapping rule order.
        :param access_zone: Access zone.
        :param rule_list: To get the complete rules list.
        :return: rule details.
        """
        try:
            api_response = self.auth_api.get_mapping_users_rules(zone=access_zone).to_dict()
            if api_response and 'rules' in api_response:
                if rule_list:
                    user_mapping_rules_list = []
                    for count, rule in enumerate(api_response['rules']['rules']):
                        rule['apply_order'] = count + 1
                        user_mapping_rules_list.append(rule)
                    return user_mapping_rules_list
                total_count_of_rules = len(api_response['rules']['rules'])
                if total_count_of_rules >= apply_order:
                    rule = api_response['rules']['rules'][apply_order - 1]
                    rule['apply_order'] = apply_order
                    LOG.info("Fetching user mapping rule successful")
                    return rule
                else:
                    error_message = f"apply order should be in range of 1 to {total_count_of_rules}"
                    LOG.error(error_message)
                    self.module.fail_json(msg=error_message)
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Fetching user mapping rule failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def create_user_mapping_rule(self, rule_payload, access_zone):
        """
        Create user mapping rule
        :param rule_payload: User mapping rule payload.
        :param access_zone: Access zone.
        :return: Rule details.
        """
        try:
            LOG.info('Creating user mapping rule')
            rule_details = None
            if not self.module.check_mode:
                rules_list = self.get_rule_details(access_zone=access_zone, rule_list=True)
                total_rules = len(rules_list)
                rules_list.append(rule_payload)
                self.update_sdk_call(rules_list, access_zone)
                rule_details = self.get_rule_details(apply_order=total_rules + 1, access_zone=access_zone)
            LOG.info('Creating user mapping rule is successful')
            return rule_details
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Creating user mapping rule failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def update_user_mapping_rule(self, apply_order, new_order, rule_payload, access_zone):
        """
        Update user mapping rule
        :param apply_order: Current order of the rule.
        :param new_order: New order of the rule.
        :param rule_payload: User mapping rule payload.
        :param access_zone: Access zone.
        :return: Rule details.
        """
        try:
            LOG.info('Updating user mapping rule')
            if not self.module.check_mode:
                rules_list = self.get_rule_details(access_zone=access_zone, rule_list=True)
                total_rules = len(rules_list)
                if new_order:
                    if total_rules < new_order:
                        error_message = f"new_order should be in range of 1 to {total_rules}"
                        LOG.error(error_message)
                        self.module.fail_json(msg=error_message)
                    else:
                        rules_list.pop(apply_order - 1)
                        rules_list.insert(new_order - 1, rule_payload)
                        apply_order = new_order
                else:
                    rules_list[apply_order - 1] = rule_payload
                self.update_sdk_call(rules_list, access_zone)
            rule_details = self.get_rule_details(apply_order=apply_order, access_zone=access_zone)
            LOG.info('Updating user mapping rule is successful')
            return rule_details
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Updating user mapping rule failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete_user_mapping_rule(self, apply_order, access_zone):
        """
        Delete user mapping rule based on apply order
        :param apply_order: Current order of the rule.
        :param access_zone: Access zone.
        :return: True if delete is successful.
        """
        try:
            LOG.info('Deleting user mapping rule')
            if not self.module.check_mode:
                rules_list = self.get_rule_details(access_zone=access_zone, rule_list=True)
                total_rules = len(rules_list)
                if total_rules < apply_order:
                    return False
                rules_list.pop(apply_order - 1)
                self.update_sdk_call(rules_list, access_zone)
            LOG.info('Deleting user mapping rule is successful')
            return True
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Deleting user mapping rule failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_user_mapping_rule_parameters(self):
        return dict(
            apply_order=dict(type='int'),
            new_order=dict(type='int'),
            access_zone=dict(type='str', default='System'),
            rule=dict(
                type='dict', options=dict(
                    operator=dict(type='str', choices=['insert', 'append', 'union', 'replace', 'trim']),
                    options=dict(
                        type='dict', options=dict(
                            break_on_match=dict(type='bool'),
                            group=dict(type='bool'),
                            groups=dict(type='bool'),
                            user=dict(type='bool'),
                            default_user=dict(type='dict', options=dict(
                                domain=dict(type='str'),
                                user=dict(type='str', required=True)
                            ))
                        )
                    ),
                    user1=dict(type='dict', options=dict(
                        domain=dict(type='str'),
                        user=dict(type='str', required=True)
                    )),
                    user2=dict(type='dict', options=dict(
                        domain=dict(type='str'),
                        user=dict(type='str', required=True)
                    ))
                )
            ),
            state=dict(type='str', choices=['present', 'absent'], default='present')
        )


class UserMappingRuleExitHandler():
    def handle(self, user_mapping_rule_object):
        user_mapping_rule_object.module.exit_json(**user_mapping_rule_object.result)


class UserMappingRuleDeleteHandler():
    def handle(self, user_mapping_rule_object, user_mapping_rule_params):
        if user_mapping_rule_params['state'] == 'absent':
            if user_mapping_rule_params['apply_order'] is None:
                error_message = "'apply_order' is required to delete the rule"
                LOG.error(error_message)
                user_mapping_rule_object.module.fail_json(msg=error_message)
            changed = user_mapping_rule_object.delete_user_mapping_rule(user_mapping_rule_params['apply_order'], user_mapping_rule_params['access_zone'])
            user_mapping_rule_object.result['changed'] = changed
        UserMappingRuleExitHandler().handle(user_mapping_rule_object)


class UserMappingRuleModifyHandler():
    def handle(self, user_mapping_rule_object, user_mapping_rule_params, user_mapping_rule_details):
        if user_mapping_rule_params['apply_order'] is not None and user_mapping_rule_params['state'] == 'present':
            do_update, updated_rule = user_mapping_rule_object.check_and_form_rule_for_update(user_mapping_rule_params, user_mapping_rule_details)
            if do_update:
                formatted_rule_payload = user_mapping_rule_object.form_rule_payload(updated_rule)
                user_mapping_rule_details = user_mapping_rule_object.update_user_mapping_rule(
                    user_mapping_rule_params['apply_order'], user_mapping_rule_params['new_order'],
                    formatted_rule_payload, user_mapping_rule_params['access_zone'])
                user_mapping_rule_object.result['user_mapping_rule_details'] = user_mapping_rule_details
                user_mapping_rule_object.result['changed'] = True

        UserMappingRuleDeleteHandler().handle(user_mapping_rule_object, user_mapping_rule_params)


class UserMappingRuleCreateHandler():
    def handle(self, user_mapping_rule_object, user_mapping_rule_params, user_mapping_rule_details):
        if user_mapping_rule_params['state'] == 'present' and not user_mapping_rule_details:
            user_mapping_rule_object.validate_inputs(user_mapping_rule_params['rule'])
            formatted_rule_payload = user_mapping_rule_object.form_rule_payload(user_mapping_rule_params['rule'])
            user_mapping_rule_details = user_mapping_rule_object.create_user_mapping_rule(formatted_rule_payload, user_mapping_rule_params['access_zone'])
            user_mapping_rule_object.result['user_mapping_rule_details'] = user_mapping_rule_details
            user_mapping_rule_object.result['changed'] = True

        UserMappingRuleModifyHandler().handle(user_mapping_rule_object, user_mapping_rule_params, user_mapping_rule_details)


class UserMappingRuleHandler():
    def handle(self, user_mapping_rule_object, user_mapping_rule_params):
        user_mapping_rule_details = {}
        if 'apply_order' in user_mapping_rule_params and user_mapping_rule_params['apply_order'] is not None and user_mapping_rule_params['apply_order'] <= 0:
            error_message = "apply_order should be greater than 0."
            LOG.error(error_message)
            user_mapping_rule_object.module.fail_json(msg=error_message)
        if user_mapping_rule_params['apply_order'] is not None and user_mapping_rule_params['state'] == 'present':
            user_mapping_rule_details = user_mapping_rule_object.get_rule_details(
                user_mapping_rule_params['apply_order'], user_mapping_rule_params['access_zone'])
            user_mapping_rule_object.result['user_mapping_rule_details'] = user_mapping_rule_details
        UserMappingRuleCreateHandler().handle(user_mapping_rule_object, user_mapping_rule_params, user_mapping_rule_details)


def main():
    """ Create PowerScale UserMappingRule object and perform actions
         on it based on user input from the playbook"""
    obj = UserMappingRule()
    UserMappingRuleHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
