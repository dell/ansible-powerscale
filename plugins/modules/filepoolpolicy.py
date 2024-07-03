#!/usr/bin/python
# Copyright: (c) 2022-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing file pool policy on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: filepoolpolicy

version_added: '1.6.0'

short_description: Manages file pool policy on PowerScale
description:
- Managing file pool policy on PowerScale Storage System. This includes
  creating a new file pool policy, deleting a file pool policy and
  retrieving the details of a file pool policy.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Ananthu S Kuttattu (@kuttattz) <ansible.team@dell.com>

options:
  policy_id:
    description:
    - Unique Id of the file pool policy.
    - It is mutually exclusive with I(policy_name).
    type: str

  policy_name:
    description:
    - Unique name of the file pool policy.
    - It is mutually exclusive with I(policy_id).
    - Mandatory for file pool policy creation.
    type: str

  description:
    description: A description of the file pool policy.
    type: str

  apply_order:
    description:
    - The order in which the policy should be applied.
    - It is relative to other policies.
    type: int

  apply_data_storage_policy:
    description: Action to move files to storage pool or tier.
    type: dict
    suboptions:
      ssd_strategy:
        description: Strategy for ssd.
        type: str
        choices: ['SSD_metadata_read_acceleration', 'SSD_metadata_read_write_acceleration', 'avoid_SSD', 'SSD_for_metadata_and_data']
      storagepool:
        description: Name of the storage pool.
        type: str
        default: 'anywhere'

  apply_snapshot_storage_policy:
    description: Action to move snapshots to storage pool or tier.
    type: dict
    suboptions:
      ssd_strategy:
        description: Strategy for ssd.
        type: str
        choices: ['SSD_metadata_read_acceleration', 'SSD_metadata_read_write_acceleration', 'avoid_SSD', 'SSD_for_metadata_and_data']
      storagepool:
        description: Name of the storage pool.
        type: str
        default: 'anywhere'

  set_requested_protection:
    description: Action to change requested protection.
    type: str
    choices: ['default_protection_of_node_pool_or_tier', 'tolerate_failure_of_1_drive_or_1_node',
              'tolerate_failure_of_2_drives_or_1_node', 'tolerate_failure_of_2_drives_or_2_nodes',
              'tolerate_failure_of_3_drives_or_1_node',
              'tolerate_failure_of_3_drives_or_(1_node_and_1drive)',
              'tolerate_failure_of_3_drives_or_3_nodes', 'tolerate_failure_of_4_drives_or_1_node',
              'tolerate_failure_of_4_drives_or_2_nodes', 'tolerate_failure_of_4_drives_or_4_nodes',
              'mirrored_over_2_nodes', 'mirrored_over_3_nodes', 'mirrored_over_4_nodes',
              'mirrored_over_5_nodes', 'mirrored_over_6_nodes', 'mirrored_over_7_nodes',
              'mirrored_over_8_nodes']

  set_data_access_pattern:
    description: Action to set data access pattern optimization.
    type: str
    choices: ['random', 'concurrency', 'streaming']

  set_write_performance_optimization:
    description: Action to set write performance optimization.
    type: str
    choices: ["enable_smartcache","disable_smartcache"]

  file_matching_pattern:
    description: The file matching rules for the policy.
    type: dict
    suboptions:
      or_criteria:
        description:
        - or criteria conditions for the file policy.
        - Maximum of 3 criteria's is possible.
        type: list
        elements: dict
        required: true
        suboptions:
          and_criteria:
            description:
            - The and criteria conditions for the file policy.
            - Maximum of 5 criteria is possible.
            type: list
            elements: dict
            required: true
            suboptions:
              type:
                description: The file criteria to be compared to a given value.
                type: str
                required: true
                choices: ['file_name', 'file_type', 'file_path', 'file_attribute', 'accessed', 'created', 'modified', 'metadata_changed', 'size']
              condition:
                description:
                - The condition to use while comparing an attribute with its value.
                - If I(type) is C(size) then the conditions are ['equal', 'not_equal', 'greater_than', 'greater_than_equal_to',
                                                               'less_than', 'less_than_equal_to'].
                - If I(type) is C(accessed) or C(created) or C(modified) or C(metadata_changed) then the conditions are
                  ['after','before', 'is_newer_than', 'is_older_than'].
                - If I(type) is C(file_attribute) then the conditions are ['matches','does_not_match', 'exists', 'does_not_exist'].
                - If I(type) is C(file_path) then the conditions are ['matches','does_not_match', 'contains', 'does_not_contain'].
                - If I(type) is C(file_type) or  C(file_name) then the conditions are ['matches','does_not_match'].
                type: str
                choices: ['matches', 'does_not_match', 'contains', 'does_not_contain', 'after', 'before', 'is_newer_than', 'is_older_than',
                          'equal', 'not_equal', 'greater_than', 'greater_than_equal_to', 'less_than', 'less_than_equal_to', 'exists',
                          'does_not_exist']
              value:
                description:
                - The value to be compared against a file criteria.
                - Required in case if I(type) is C(file_name) or C(file_path) or C(file_attribute).
                - If I(type) is C(file_name) then value wil have file name.
                - If I(type) is C(file_path) then value wil have file path.
                - If I(type) is C(file_attribute) then value wil have file attribute field value.
                type: str
              field:
                description:
                - File attribute field name to be compared in a custom comparison.
                - Required only if the I(type) is C(file_attribute).
                type: str
              case_sensitive:
                description:
                - C(true) to indicate case sensitivity when comparing file attributes.
                - Required only if the I(type) is C(file_name) or C(file_path).
                type: bool
              file_type_option:
                description:
                - File type option.
                - Required only if the I(type) is C(file_type).
                type: str
                choices: ['directory', 'file', 'other']
              size_info:
                description:
                - File size value and unit.
                - Required only if the I(type) is C(size).
                type: dict
                suboptions:
                  size_value:
                    description: Size value.
                    type: int
                    required: true
                  size_unit:
                    description: Unit for the size value
                    type: str
                    required: true
                    choices: ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
              datetime_value:
                description:
                - Date and Time value.
                - Format is 'YYYY-MM-DD HOUR:MINUTE'
                - Required only if the I(type) is C(accessed) or C(created) or C(modified) or C(metadata_changed) and \
                  the I(condition) is C(after) or C(before)
                type: str
              relative_datetime_count:
                description:
                - A relative duration (e.g., 2 years, 3 weeks, 50 seconds).
                - Required only if the I(type) is C(accessed) or C(created) or C(modified) or C(metadata_changed) and \
                  the C(condition) is C(is_newer_than) or C(is_older_than)
                type: dict
                suboptions:
                  time_value:
                    description: Relative time count.
                    type: int
                    required: true
                  time_unit:
                    description: Unit for the relative time count
                    type: str
                    required: true
                    choices: ['years', 'months', 'weeks', 'days', 'hours', 'minutes', 'seconds']

  state:
    description:
    - The state option is used to mention the existence of file pool policy.
    type: str
    required: true
    choices: [absent, present]
notes:
- Modifying a file pool policy is not supported.
- The I(check_mode) is supported.
'''

EXAMPLES = r'''
- name: Get a file pool policy
  dellemc.powerscale.filepoolpolicy:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    policy_name: "test_11"
    state: 'present'

- name: Delete a file pool policy
  dellemc.powerscale.filepoolpolicy:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    policy_name: "test_11"
    state: 'absent'

- name: Create a file pool policy
  dellemc.powerscale.filepoolpolicy:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    policy_name: "test_policy_1"
    description: 'Creating a policy'
    apply_order: 1
    apply_data_storage_policy:
      ssd_strategy: "SSD_metadata_read_acceleration"
      storagepool: "test_tier"
    set_data_access_pattern: "concurrency"
    set_requested_protection: "mirrored_over_3_nodes"
    set_write_performance_optimization: "enable_smartcache"
    file_matching_pattern:
      or_criteria:
        - and_criteria:
            - type: "file_name"
              condition: "does_not_match"
              value: "file_name_test"
              case_sensitive: true
            - type: "accessed"
              condition: "after"
              datetime_value: "2022-04-04 23:30"
            - type: "created"
              condition: "is_newer_than"
              relative_datetime_count:
                time_value: 12
                time_unit: "years"
        - and_criteria:
            - type: "size"
              condition: "not_equal"
              size_info:
                size_value: 60
                size_unit: "MB"
            - type: "file_attribute"
              condition: "does_not_match"
              field: "test_field"
              value: "uni"
            - type: "file_attribute"
              condition: "exists"
              field: "test"
    state: 'present'
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
    sample: "false"
filepool_policy_details:
    description: Policy details.
    returned: When a Policy exists
    type: complex
    contains:
        "id":
            description: Unique ID of the policy.
            type: int
        "name":
            description: Unique name of the policy.
            type: str
        "description":
            description: Description of the policy.
            type: str
        "apply_order":
            description: The order in which policy is present with respect to other policies.
            type: int
        "actions":
            description: List of action's available for the policy.
            type: list
        "file_matching_pattern":
            description: File matching pattern of the policy.
            type: complex
            contains:
                "or_criteria":
                    description: or criteria conditions for the file policy.
                    type: list

    sample:
        {"filepool_policy_details": {
            "actions": [
                {
                    "action_param": "3x",
                    "action_type": "set_requested_protection"
                },
                {
                    "action_param": "concurrency",
                    "action_type": "set_data_access_pattern"
                },
                {
                    "action_param": "True",
                    "action_type": "enable_coalescer"
                },
                {
                    "action_param": "{'ssd_strategy': 'metadata', 'storagepool': 'test_tier'}",
                    "action_type": "apply_data_storage_policy"
                }
            ],
            "apply_order": 1,
            "description": "Creating a policy",
            "file_matching_pattern": {
                "or_criteria": [
                    {
                        "and_criteria": [
                            {
                                "attribute_exists": null,
                                "begins_with": null,
                                "case_sensitive": true,
                                "field": null,
                                "operator": "!=",
                                "type": "name",
                                "units": null,
                                "use_relative_time": null,
                                "value": "we"
                            }
                        ]
                    },
                    {
                        "and_criteria": [
                            {
                                "attribute_exists": null,
                                "begins_with": null,
                                "case_sensitive": false,
                                "field": null,
                                "operator": "!=",
                                "type": "name",
                                "units": null,
                                "use_relative_time": null,
                                "value": "we"
                            },
                            {
                                "attribute_exists": null,
                                "begins_with": null,
                                "case_sensitive": false,
                                "field": null,
                                "operator": "==",
                                "type": "name",
                                "units": null,
                                "use_relative_time": null,
                                "value": "we"
                            }
                        ]
                    }
                ]
            },
            "id": 25,
            "name": "test_policy"}
        }
'''

from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
from ansible.module_utils.basic import AnsibleModule

LOG = utils.get_logger('filepoolpolicy')


class FilePoolPolicy(object):
    """Class with operations on file pool policy"""

    def __init__(self):
        """ Define all parameters required by this module"""

        self.requested_protection_map = {
            'default_protection_of_node_pool_or_tier': 'default',
            'tolerate_failure_of_1_drive_or_1_node': '+1n',
            'tolerate_failure_of_2_drives_or_1_node': '+2d:1n',
            'tolerate_failure_of_2_drives_or_2_nodes': '+2n',
            'tolerate_failure_of_3_drives_or_1_node': '+3d:1n',
            'tolerate_failure_of_3_drives_or_(1_node_and_1drive)': '+3d:1n1d',
            'tolerate_failure_of_3_drives_or_3_nodes': '+3n',
            'tolerate_failure_of_4_drives_or_1_node': '+4d:1n',
            'tolerate_failure_of_4_drives_or_2_nodes': '+4d:2n',
            'tolerate_failure_of_4_drives_or_4_nodes': '+4n',
            'mirrored_over_2_nodes': '2x',
            'mirrored_over_3_nodes': '3x',
            'mirrored_over_4_nodes': '4x',
            'mirrored_over_5_nodes': '5x',
            'mirrored_over_6_nodes': '6x',
            'mirrored_over_7_nodes': '7x',
            'mirrored_over_8_nodes': '8x'
        }
        self.ssd_strategy_map = {
            'SSD_metadata_read_acceleration': 'metadata',
            'SSD_metadata_read_write_acceleration': 'metadata-write',
            'avoid_SSD': 'avoid',
            'SSD_for_metadata_and_data': 'data'
        }
        self.smartcache_map = {
            'enable_smartcache': True,
            'disable_smartcache': False
        }
        self.operators_map = {
            'matches': '==',
            'does_not_match': '!=',
            'contains': '==',
            'does_not_contain': '!=',
            'after': '>',
            'before': '<',
            'is_newer_than': '<',
            'is_older_than': '>',
            'equal': '==',
            'not_equal': '!=',
            'greater_than': '>',
            'greater_than_equal_to': '>=',
            'less_than': '<',
            'less_than_equal_to': '<=',
        }
        self.datetime_field_map = {
            'modified': 'changed_time',
            'accessed': 'accessed_time',
            'metadata_changed': 'metadata_changed_time',
            'created': 'birth_time'
        }
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(self.get_file_pool_policy_parameters())
        mutually_exclusive = [['policy_name', 'policy_id']]
        required_one_of = [['policy_name', 'policy_id']]
        # initialize the Ansible module
        self.module = AnsibleModule(argument_spec=self.module_params,
                                    supports_check_mode=True,
                                    mutually_exclusive=mutually_exclusive,
                                    required_one_of=required_one_of)

        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.filepool_api = utils.isi_sdk.FilepoolApi(self.api_client)
        self.storagepool_api = utils.isi_sdk.StoragepoolApi(self.api_client)
        LOG.info('Got the isi_sdk instance for authorization on to PowerScale')
        check_mode_msg = f'Check mode flag is {self.module.check_mode}'
        LOG.info(check_mode_msg)

    def validate_node_pools(self, storage_nodepool):
        """
        Validate storage nodepool
        :param storage_nodepool: Storagepool nodepool name
        :return: True/False.
        """
        try:
            list_of_storagenodepools = self.storagepool_api.list_storagepool_nodepools()
            for nodepools in list_of_storagenodepools.nodepools:
                if nodepools.name == storage_nodepool and not nodepools.tier:
                    return True
            return False
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Validating storage nodepools failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def validate_storage_pool_tiers(self, storagepool_tier_name):
        """
        Validate storage pool tier
        :param storagepool_tier_name: Storagepool tier name
        :return: True/False.
        """
        try:
            list_of_storagepool_tiers = self.storagepool_api.list_storagepool_tiers()
            for storagepool_tier in list_of_storagepool_tiers.tiers:
                if storagepool_tier.name == storagepool_tier_name:
                    if storagepool_tier.lnns:
                        return True
                    else:
                        return False
            return False
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Validating storage pool tier failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def validate_storage_pool(self, storagepool):
        """
        Validate storage pool
        :param storagepool: Storagepool name
        :return: True/False.
        """
        if storagepool == 'anywhere':
            return True
        else:
            result = self.validate_storage_pool_tiers(storagepool)
            if not result:
                result = self.validate_node_pools(storagepool)
            return result

    def form_actions_payload(self, file_pool_policy_params):
        """
        Form actions list
        :param file_pool_policy_params: Module params
        :return: Valid and formatted actions list.
        """
        actions = []
        if 'apply_data_storage_policy' in file_pool_policy_params and file_pool_policy_params['apply_data_storage_policy']:
            storagepool = file_pool_policy_params['apply_data_storage_policy']['storagepool']
            result = self.validate_storage_pool(storagepool)
            if not result:
                error_message = f"Processing action 'apply_data_storage_policy' failed with error: {storagepool} not found"
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
            actions.append({
                "action_param": {
                    "ssd_strategy": self.ssd_strategy_map[file_pool_policy_params['apply_data_storage_policy']['ssd_strategy']],
                    "storagepool": storagepool
                },
                "action_type": "apply_data_storage_policy"
            })
        if 'apply_snapshot_storage_policy' in file_pool_policy_params and file_pool_policy_params['apply_snapshot_storage_policy']:
            storagepool = file_pool_policy_params['apply_snapshot_storage_policy']['storagepool']
            result = self.validate_storage_pool(storagepool)
            if not result:
                error_message = f"Processing action 'apply_snapshot_storage_policy' failed with error: {storagepool} not found"
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
            actions.append({
                "action_param": {
                    "ssd_strategy": self.ssd_strategy_map[file_pool_policy_params['apply_snapshot_storage_policy']['ssd_strategy']],
                    "storagepool": storagepool
                },
                "action_type": "apply_snapshot_storage_policy"
            })
        if 'set_requested_protection' in file_pool_policy_params and file_pool_policy_params['set_requested_protection']:
            actions.append({
                "action_param": self.requested_protection_map[file_pool_policy_params['set_requested_protection']],
                "action_type": "set_requested_protection"
            })
        if 'set_data_access_pattern' in file_pool_policy_params and file_pool_policy_params['set_data_access_pattern']:
            actions.append({
                "action_param": file_pool_policy_params['set_data_access_pattern'],
                "action_type": "set_data_access_pattern"
            })
        if 'set_write_performance_optimization' in file_pool_policy_params and file_pool_policy_params['set_write_performance_optimization']:
            actions.append({
                "action_param": self.smartcache_map[file_pool_policy_params['set_write_performance_optimization']],
                "action_type": "enable_coalescer"
            })
        return actions

    def get_datetime_timestamp(self, datetime_string, file_attribute):
        """
        :param datetime_string: String with data and time.
        :param file_attribute: File matching pattern and_criteria item 'type' value.
        :return: Timestamp for given date time.
        """
        try:
            timestamp = utils.get_datetime_timestamp(datetime_string, "%Y-%m-%d %H:%M")
            return int(timestamp)
        except ValueError:
            error_message = f"Criteria option {file_attribute} should have 'datetime_value' in format 'YYYY-MM-DD HOUR:MINUTE'"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def validate_conditions_on_file_attribute(self, file_attribute, given_condition, available_conditions):
        """
        Validate if the given conditions are available for the requested criteria type
        :param file_attribute: File matching pattern and_criteria item 'type' value.
        :param given_condition: Given conditions for respective file matching pattern and_criteria item.
        :param available_conditions: Available conditions for respective file matching pattern and_criteria item.
        :return: None.
        """
        if given_condition not in available_conditions:
            error_message = f"Criteria option '{file_attribute}' should only have these '{available_conditions}' values in 'condition'"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def validate_extra_fields_and_required_fields(self, file_attribute, fields_available, required_fields, provided_fields):
        """
        Validate if there are any extra fields in a criteria item based on criteria type.
        Check if required fields are all available in a criteria item based on criteria type.
        :param file_attribute: File matching pattern and_criteria item 'type' value.
        :param fields_available: Available fields for respective file matching pattern and_criteria item.
        :param required_fields: Mandatory fields for respective file matching pattern and_criteria item.
        :param provided_fields: Provided fields for respective file matching pattern and_criteria item.
        :return: None.
        """
        extra_fields = set(provided_fields) - set(fields_available)
        if extra_fields != set():
            error_message = f"Criteria option '{file_attribute}' should have only these field's {fields_available}"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

        missing_fields = set(required_fields) - set(provided_fields)
        if missing_fields != set():
            error_message = f"Criteria option '{file_attribute}' should have these field's {required_fields} and it should not be empty"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def validate_and_get_criteria_size_item(self, item):
        """
        Validate and return formatted data for criteria 'size'
        :param item: File matching pattern and_criteria item with 'type' as 'size'
        :return: Valid and formatted criteria 'size' item.
        """
        fields_available = ['type', 'size_info', 'condition']
        required_fields = ['size_info', 'condition']
        provided_fields = item.keys()
        available_conditions = ['equal', 'not_equal', 'greater_than', 'greater_than_equal_to', 'less_than', 'less_than_equal_to']
        self.validate_extra_fields_and_required_fields('size', fields_available, required_fields, provided_fields)
        self.validate_conditions_on_file_attribute('size', item['condition'], available_conditions)

        formatted_item = {
            "type": item['type'],
            "operator": self.operators_map[item['condition']],
            "value": utils.get_size_bytes(item['size_info']['size_value'], item['size_info']['size_unit'])
        }
        return formatted_item

    def validate_and_get_criteria_datetime_item(self, item):
        """
        Validate and return formatted data for the criteria's 'accessed' or 'created' or 'modified' or 'metadata_changed'.
        :param item: File matching pattern and_criteria item with 'type' as 'accessed' or 'created' or 'modified' or 'metadata_changed'
        :return: Valid and formatted criteria item.
        """
        file_attribute = item['type']
        fields_available = ['type', 'datetime_value', 'condition', 'relative_datetime_count']
        required_fields = ['condition']
        provided_fields = item.keys()
        available_conditions = ['after', 'before', 'is_newer_than', 'is_older_than']
        self.validate_extra_fields_and_required_fields(file_attribute, fields_available, required_fields, provided_fields)
        self.validate_conditions_on_file_attribute(file_attribute, item['condition'], available_conditions)

        value = None
        use_relative_time = False
        if item['condition'] == 'is_newer_than' or item['condition'] == 'is_older_than':
            use_relative_time = True
            if 'relative_datetime_count' not in provided_fields:
                error_message = (f"Criteria option {file_attribute} should have "
                                 "'relative_datetime_count' option if 'condition' is is_newer_than or "
                                 "is_older_than")
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
            if 'datetime_value' in provided_fields:
                error_message = (f"Criteria option {file_attribute} should not have "
                                 "'datetime_value' option if 'condition' is is_newer_than or "
                                 "is_older_than")
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
            value = utils.get_time_in_seconds(item['relative_datetime_count']['time_value'], item['relative_datetime_count']['time_unit'])
        else:
            if 'datetime_value' not in provided_fields:
                error_message = f"Criteria option {file_attribute} should have 'datetime_value' option if 'condition' is after or before"
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
            if 'relative_datetime_count' in provided_fields:
                error_message = f"Criteria option {file_attribute} should not have 'relative_datetime_count' option if 'condition' is after or before"
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
            value = self.get_datetime_timestamp(item['datetime_value'], file_attribute)

        formatted_item = {
            "type": self.datetime_field_map[file_attribute],
            "operator": self.operators_map[item['condition']],
            "value": value,
            "use_relative_time": use_relative_time
        }
        return formatted_item

    def validate_and_get_criteria_custom_field_item(self, item):
        """
        Validate and return formatted data for criteria 'file_attribute'
        :param item: File matching pattern and_criteria item with 'type' as 'file_attribute'.
        :return: Valid and formatted criteria 'file_attribute' item.
        """
        fields_available = ['type', 'value', 'condition', 'field']
        required_fields = ['field', 'condition']
        provided_fields = item.keys()
        available_conditions = ['matches', 'does_not_match', 'exists', 'does_not_exist']
        self.validate_extra_fields_and_required_fields('file_attribute', fields_available, required_fields, provided_fields)
        self.validate_conditions_on_file_attribute('file_attribute', item['condition'], available_conditions)

        formatted_item = {
            "type": 'custom_attribute',
            "field": item['field'],
        }

        if item['condition'] == 'exists' or item['condition'] == 'does_not_exist':
            formatted_item['attribute_exists'] = True if item['condition'] == 'exists' else False
            if 'value' in provided_fields:
                error_message = "Criteria option 'file_attribute' should not have 'value' option if 'condition' is exists or does_not_exist"
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
            formatted_item['value'] = ""
        else:
            if 'value' not in provided_fields:
                error_message = "Criteria option 'file_attribute' should have 'value' option if 'condition' is does_not_match or matches"
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
            formatted_item['operator'] = self.operators_map[item['condition']]
            formatted_item['value'] = item['value']
        return formatted_item

    def validate_and_get_criteria_type_item(self, item):
        """
        Validate and return formatted data for criteria 'file_type'
        :param item: File matching pattern and_criteria item with 'type' as 'file_type'.
        :return: Valid and formatted criteria 'file_type' item.
        """
        fields_available = ['type', 'file_type_option', 'condition']
        required_fields = ['file_type_option', 'condition']
        provided_fields = item.keys()
        available_conditions = ['matches', 'does_not_match']
        self.validate_extra_fields_and_required_fields('file_type', fields_available, required_fields, provided_fields)
        self.validate_conditions_on_file_attribute('file_type', item['condition'], available_conditions)

        formatted_item = {
            "type": item['type'],
            "operator": self.operators_map[item['condition']],
            "value": item['file_type_option']
        }
        return formatted_item

    def validate_and_get_criteria_path_item(self, item):
        """
        Validate and return formatted data for criteria 'file_path'
        :param item: File matching pattern and_criteria item with 'type' as 'file_path'.
        :return: Valid and formatted criteria 'file_path' item.
        """
        fields_available = ['type', 'value', 'condition', 'case_sensitive']
        required_fields = ['value', 'condition']
        provided_fields = item.keys()
        available_conditions = ['matches', 'does_not_match', 'contains', 'does_not_contain']
        self.validate_extra_fields_and_required_fields('file_path', fields_available, required_fields, provided_fields)
        self.validate_conditions_on_file_attribute('file_path', item['condition'], available_conditions)

        if item['condition'] in ['contains', 'does_not_contain']:
            begins_with = False
        else:
            begins_with = True

        formatted_item = {
            "type": 'path',
            "operator": self.operators_map[item['condition']],
            "value": item['value'],
            "case_sensitive": item['case_sensitive'] if 'case_sensitive' in provided_fields else False,
            "begins_with": begins_with
        }

        return formatted_item

    def validate_and_get_criteria_name_item(self, item):
        """
        Validate and return formatted data for criteria 'file_name'
        :param item: File matching pattern and_criteria item with 'type' as 'file_name'.
        :return: Valid and formatted criteria 'file_name' item.
        """
        fields_available = ['type', 'value', 'condition', 'case_sensitive']
        required_fields = ['value', 'condition']
        provided_fields = item.keys()
        available_conditions = ['matches', 'does_not_match']
        self.validate_extra_fields_and_required_fields('file_name', fields_available, required_fields, provided_fields)
        self.validate_conditions_on_file_attribute('file_name', item['condition'], available_conditions)

        formatted_item = {
            "type": 'name',
            "operator": self.operators_map[item['condition']],
            "value": item['value'],
            "case_sensitive": item['case_sensitive'] if 'case_sensitive' in provided_fields else False
        }

        return formatted_item

    def form_criteria_item_and(self, item):
        """
        Validate and form criteria options based on the type
        :param item: File matching pattern and_criteria item.
        :return: Valid and formatted criteria item.
        """
        item = {k: v for k, v in item.items() if v}
        if item['type'] == "file_name":
            return self.validate_and_get_criteria_name_item(item)
        elif item['type'] == "file_path":
            return self.validate_and_get_criteria_path_item(item)
        elif item['type'] == "file_type":
            return self.validate_and_get_criteria_type_item(item)
        elif item['type'] == "file_attribute":
            return self.validate_and_get_criteria_custom_field_item(item)
        elif item['type'] in ['accessed', 'created', 'modified', 'metadata_changed']:
            return self.validate_and_get_criteria_datetime_item(item)
        elif item['type'] == "size":
            return self.validate_and_get_criteria_size_item(item)

    def validate_file_matching_criteria(self, file_matching_criteria):
        """
        Validate file matching criteria
        :param file_matching_criteria: File matching pattern data.
        :return: Valid and formatted file matching pattern.
        """
        or_criteria_list = file_matching_criteria['or_criteria']
        if not or_criteria_list or len(or_criteria_list) > 3:
            error_message = "Number of 'or_criteria' item should be in range of 1 to 3"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

        formatted_or_criteria_list = []
        for or_criteria_item in or_criteria_list:
            and_criteria_list = or_criteria_item['and_criteria']
            if not and_criteria_list or len(and_criteria_list) > 5:
                error_message = "Number of 'and_criteria' item should be in range of 1 to 5"
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
            formatted_and_criteria_list = []
            for and_criteria_item in and_criteria_list:
                if 'type' not in and_criteria_item.keys():
                    error_message = "'type' field should be present in 'and_criteria' item"
                    LOG.error(error_message)
                    self.module.fail_json(msg=error_message)
                # Get formatted criteria option item
                formatted_and_criteria_list.append(self.form_criteria_item_and(and_criteria_item))
            formatted_or_criteria_list.append({
                'and_criteria': formatted_and_criteria_list
            })
        formatted_file_matching_criteria = {'or_criteria': formatted_or_criteria_list}
        return formatted_file_matching_criteria

    def get_file_pool_policy_details(self, policy_name=None, policy_id=None):
        """
        Get file pool policy either by policy_name or policy_id
        :param policy_name: File pool policy name.
        :param policy_id: File pool policy Id.
        :return: Policy details.
        """
        try:
            if policy_id:
                api_response = self.filepool_api.get_filepool_policy(policy_id).to_dict()
                return api_response['policies'][0]
            else:
                api_response = self.filepool_api.list_filepool_policies().to_dict()
                if api_response:
                    for policy in api_response['policies']:
                        if policy['name'] == policy_name:
                            return policy
                return None
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Fetching file pool policies failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def create_file_pool_policy(self, policy_name, description, apply_order, actions, file_matching_criteria):
        """
        Create file pool policy
        :param policy_name: File pool policy name.
        :param description: Description of the policy.
        :param apply_order: Order of the policy with relative to the existing policies.
        :param actions: List of actions formed for the policy.
        :param file_matching_criteria: file matching pattern formed from the criteria's
        :return: Policy details.
        """
        try:
            file_pool_policy_data = {
                "name": policy_name,
                "description": description,
                "apply_order": apply_order,
                "actions": actions,
                'file_matching_pattern': file_matching_criteria
            }
            create_msg = f'Creating file pool policy {policy_name}'
            LOG.info(create_msg)
            if not self.module.check_mode:
                file_pool_policy_object = utils.isi_sdk.FilepoolPolicyCreateParams(**file_pool_policy_data)
                create_filepool_policy_response = self.filepool_api.create_filepool_policy(file_pool_policy_object)
                policy_details = self.get_file_pool_policy_details(policy_id=create_filepool_policy_response.id)
                return policy_details
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Creating file pool policies failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete_file_pool_policy(self, policy_id):
        """
        Delete file pool policy based on id
        :param policy_id: File pool policy id.
        :return: None.
        """
        try:
            if not self.module.check_mode:
                self.filepool_api.delete_filepool_policy(policy_id)
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Deleting file pool policies failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def validate_create_inputs(self, policy_id, policy_name, file_matching_criteria):
        """
        Validate create inputs
        :param policy_id: File pool policy id.
        :param policy_name: File pool policy name.
        :param file_matching_criteria: file matching pattern formed from the criteria's
        :return: None.
        """
        if policy_id:
            err_msg = "Invalid argument 'policy_id' while creating a file pool policy"
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)
        if not policy_name:
            err_msg = "'policy_name' is required to create a file pool policy"
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)
        if not file_matching_criteria:
            error_message = "file_matching_pattern should not be None"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def perform_module_operation(self):
        """
        Perform different actions based on parameters chosen in playbook
        """
        result = dict(
            changed=False
        )
        policy_id = self.module.params['policy_id']
        policy_name = self.module.params['policy_name']
        description = self.module.params['description']
        apply_order = self.module.params['apply_order']
        file_matching_criteria = self.module.params['file_matching_pattern']
        file_pool_policy_params = self.module.params
        state = self.module.params['state']

        policy_details = self.get_file_pool_policy_details(policy_name=policy_name, policy_id=policy_id)

        if state == 'present':
            if not policy_details:
                self.validate_create_inputs(policy_id, policy_name, file_matching_criteria)
                formatted_file_matching_criteria = self.validate_file_matching_criteria(file_matching_criteria)
                actions = self.form_actions_payload(file_pool_policy_params)
                policy_details = self.create_file_pool_policy(policy_name, description,
                                                              apply_order, actions,
                                                              formatted_file_matching_criteria)
                result['changed'] = True
            result['filepool_policy_details'] = policy_details
        elif state == 'absent' and policy_details:
            self.delete_file_pool_policy(policy_details['id'])
            result['changed'] = True

        self.module.exit_json(**result)

    def get_ssd_action_parameters(self):
        return dict(type='dict', options=dict(
            ssd_strategy=dict(type='str', choices=list(
                self.ssd_strategy_map.keys())),
            storagepool=dict(type='str', default='anywhere')))

    def get_file_pool_policy_parameters(self):
        return dict(
            policy_id=dict(type='str'),
            policy_name=dict(type='str'),
            description=dict(type='str'),
            apply_order=dict(type='int'),
            apply_data_storage_policy=self.get_ssd_action_parameters(),
            apply_snapshot_storage_policy=self.get_ssd_action_parameters(),
            set_requested_protection=dict(type='str', choices=list(
                self.requested_protection_map.keys())),
            set_data_access_pattern=dict(
                type='str', choices=['random', 'concurrency', 'streaming']),
            set_write_performance_optimization=dict(
                type='str', choices=list(self.smartcache_map.keys())),
            file_matching_pattern=dict(type='dict', options=dict(
                or_criteria=dict(type='list', elements='dict', required=True, options=dict(
                    and_criteria=dict(type='list', elements='dict', required=True, options=dict(
                        type=dict(type='str', required=True, choices=['file_name', 'file_type', 'file_path', 'file_attribute',
                                                                      'accessed', 'created', 'modified',
                                                                      'metadata_changed', 'size']),
                        size_info=dict(type='dict', options=dict(
                            size_value=dict(type='int', required=True),
                            size_unit=dict(type='str', required=True, choices=['B', 'KB', 'MB', 'GB', 'TB', 'PB']),
                        )),
                        condition=dict(type='str', choices=list(self.operators_map.keys()) + ['exists', 'does_not_exist']),
                        value=dict(type='str'),
                        field=dict(type='str'),
                        case_sensitive=dict(type='bool'),
                        file_type_option=dict(type='str', choices=['directory', 'file', 'other']),
                        datetime_value=dict(type='str'),
                        relative_datetime_count=dict(type='dict', options=dict(
                            time_value=dict(type='int', required=True),
                            time_unit=dict(type='str', required=True, choices=['years', 'months', 'weeks', 'days', 'hours', 'minutes', 'seconds']),
                        ))
                    ))
                )))),
            state=dict(required=True, type='str',
                       choices=['present', 'absent'])
        )


def main():
    """ Create PowerScale FilePoolPolicy object and perform actions
         on it based on user input from the playbook"""
    obj = FilePoolPolicy()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
