# Copyright: (c) 2022, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock Api response for Unit tests of filepoolpolicy module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from mock.mock import MagicMock


class MockFilepoolpolicyApi:
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'
    SSD_ACTION_VALUE = "{'ssd_strategy': 'metadata', 'storagepool': 'esa_tier'}"
    FILEPOOLPOLICY_DESC_VALUE = 'Creating a policy'
    FILEPOOLPOLICY_COMMON_ARGS = {
        'onefs_host': '**.***.**.***',
        'policy_id': None,
        'policy_name': None,
        'description': None,
        'apply_order': None,
        'file_matching_pattern': None,
        'state': None
    }
    FILEPOOLPOLICY_COMMON_CREATE_ARGS = {
        'policy_name': "test_policy_dummy",
        'description': FILEPOOLPOLICY_DESC_VALUE,
        'apply_order': 2,
        'apply_data_storage_policy': {
            'ssd_strategy': "SSD_metadata_read_acceleration",
            'storagepool': "esa_tier"
        },
        'apply_snapshot_storage_policy': {
            'ssd_strategy': "SSD_metadata_read_acceleration",
            'storagepool': "test_nodepool"
        },
        'set_data_access_pattern': "concurrency",
        'set_requested_protection': "mirrored_over_3_nodes",
        'set_write_performance_optimization': "enable_smartcache",
        'file_matching_pattern': {
            'or_criteria': [
                {
                    'and_criteria': [
                        {
                            'type': "file_name",
                            'condition': "matches",
                            'value': "we",
                            'case_sensitive': False
                        },
                        {
                            'type': "file_path",
                            'condition': "contains",
                            'value': "we",
                            'case_sensitive': True
                        },
                        {
                            'type': "file_path",
                            'condition': "does_not_contain",
                            'value': "dummy",
                            'case_sensitive': False
                        },
                        {
                            'type': "file_type",
                            'condition': "matches",
                            'file_type_option': "directory"
                        },
                        {
                            'type': "size",
                            'condition': "greater_than",
                            'size_info': {
                                'size_value': 60,
                                'size_unit': "PB"
                            }
                        }
                    ]
                },
                {
                    'and_criteria': [
                        {
                            'type': "accessed",
                            'condition': "after",
                            'datetime_value': "2022-04-04 23:30"
                        },
                        {
                            'type': "modified",
                            'condition': "is_older_than",
                            'relative_datetime_count': {
                                'time_value': 60,
                                'time_unit': "days"
                            }
                        }
                    ]
                },
                {
                    'and_criteria': [
                        {
                            'type': "file_attribute",
                            'condition': "matches",
                            'field': "test",
                            'value': "dummy_field"
                        },
                        {
                            'type': "file_attribute",
                            'condition': "does_not_exist",
                            'field': "dummy_field"
                        }
                    ],
                }
            ]
        },
        'state': 'present'
    }
    NEW_FILEPOOLPOLICY_RESPONSE = \
        {'policies': [{'actions': [{'action_param': '3x', 'action_type': 'set_requested_protection'},
                                   {'action_param': 'concurrency', 'action_type': 'set_data_access_pattern'},
                                   {'action_param': 'True', 'action_type': 'enable_coalescer'},
                                   {'action_param': SSD_ACTION_VALUE, 'action_type': 'apply_data_storage_policy'},
                                   {'action_param': SSD_ACTION_VALUE, 'action_type': 'apply_snapshot_storage_policy'}],
                       'apply_order': 2,
                       'birth_cluster_id': '000e1e84be901a2bfe5c04251b249d087519',
                       'description': FILEPOOLPOLICY_DESC_VALUE,
                       'file_matching_pattern': {'or_criteria': [{'and_criteria': [{'attribute_exists': False,
                                                                                    'begins_with': None,
                                                                                    'case_sensitive': None,
                                                                                    'field': 'dummy_field',
                                                                                    'operator': None,
                                                                                    'type': 'custom_attribute',
                                                                                    'units': None,
                                                                                    'use_relative_time': None,
                                                                                    'value': ''},
                                                                                   {'attribute_exists': True,
                                                                                    'begins_with': None,
                                                                                    'case_sensitive': None,
                                                                                    'field': 'test',
                                                                                    'operator': '==',
                                                                                    'type': 'custom_attribute',
                                                                                    'units': None,
                                                                                    'use_relative_time': None,
                                                                                    'value': 'dummy_field'}]},
                                                                 {'and_criteria': [{'attribute_exists': None,
                                                                                    'begins_with': None,
                                                                                    'case_sensitive': None,
                                                                                    'field': None,
                                                                                    'operator': '>',
                                                                                    'type': 'accessed_time',
                                                                                    'units': None,
                                                                                    'use_relative_time': False,
                                                                                    'value': '1649095200'},
                                                                                   {'attribute_exists': None,
                                                                                    'begins_with': None,
                                                                                    'case_sensitive': None,
                                                                                    'field': None,
                                                                                    'operator': '>',
                                                                                    'type': 'changed_time',
                                                                                    'units': None,
                                                                                    'use_relative_time': True,
                                                                                    'value': '5184000'}]},
                                                                 {'and_criteria': [{'attribute_exists': None,
                                                                                    'begins_with': None,
                                                                                    'case_sensitive': None,
                                                                                    'field': None,
                                                                                    'operator': '>',
                                                                                    'type': 'size',
                                                                                    'units': 'B',
                                                                                    'use_relative_time': None,
                                                                                    'value': '60'},
                                                                                   {'attribute_exists': None,
                                                                                    'begins_with': None,
                                                                                    'case_sensitive': None,
                                                                                    'field': None,
                                                                                    'operator': '==',
                                                                                    'type': 'file_type',
                                                                                    'units': None,
                                                                                    'use_relative_time': None,
                                                                                    'value': 'directory'},
                                                                                   {'attribute_exists': None,
                                                                                    'begins_with': False,
                                                                                    'case_sensitive': False,
                                                                                    'field': None,
                                                                                    'operator': '!=',
                                                                                    'type': 'path',
                                                                                    'units': None,
                                                                                    'use_relative_time': None,
                                                                                    'value': 'dummy'},
                                                                                   {'attribute_exists': None,
                                                                                    'begins_with': False,
                                                                                    'case_sensitive': True,
                                                                                    'field': None,
                                                                                    'operator': '==',
                                                                                    'type': 'path',
                                                                                    'units': None,
                                                                                    'use_relative_time': None,
                                                                                    'value': 'we'},
                                                                                   {'attribute_exists': None,
                                                                                    'begins_with': None,
                                                                                    'case_sensitive': False,
                                                                                    'field': None,
                                                                                    'operator': '==',
                                                                                    'type': 'name',
                                                                                    'units': None,
                                                                                    'use_relative_time': None,
                                                                                    'value': 'we'}]}]},
                       'id': 42,
                       'name': 'test_policy_dummy', 'state': 'disabled', 'state_details': 'Policy has no CloudPools actions'}]}
    GET_FILEPOOLPOLICY_RESPONSE = \
        {'policies': [{'actions': [{'action_param': '3x', 'action_type': 'set_requested_protection'},
                                   {'action_param': 'concurrency', 'action_type': 'set_data_access_pattern'},
                                   {'action_param': 'True', 'action_type': 'enable_coalescer'},
                                   {'action_param': SSD_ACTION_VALUE, 'action_type': 'apply_data_storage_policy'}],
                       'apply_order': 1,
                       'description': FILEPOOLPOLICY_DESC_VALUE,
                       'file_matching_pattern': {'or_criteria': [{'and_criteria': [{'attribute_exists': None,
                                                                                    'begins_with': None,
                                                                                    'case_sensitive': None,
                                                                                    'field': None,
                                                                                    'operator': '<=',
                                                                                    'type': 'size',
                                                                                    'units': 'B',
                                                                                    'use_relative_time': None,
                                                                                    'value': '62914560'},
                                                                                   {'attribute_exists': None,
                                                                                    'begins_with': None,
                                                                                    'case_sensitive': None,
                                                                                    'field': None,
                                                                                    'operator': '<',
                                                                                    'type': 'size',
                                                                                    'units': 'B',
                                                                                    'use_relative_time': None,
                                                                                    'value': '65970697666560'}]},
                                                                 {'and_criteria': [{'attribute_exists': None,
                                                                                    'begins_with': None,
                                                                                    'case_sensitive': None,
                                                                                    'field': None,
                                                                                    'operator': '>',
                                                                                    'type': 'size',
                                                                                    'units': 'B',
                                                                                    'use_relative_time': None,
                                                                                    'value': '60'},
                                                                                   {'attribute_exists': None,
                                                                                    'begins_with': None,
                                                                                    'case_sensitive': None,
                                                                                    'field': None,
                                                                                    'operator': '!=',
                                                                                    'type': 'size',
                                                                                    'units': 'B',
                                                                                    'use_relative_time': None,
                                                                                    'value': '60'}]},
                                                                 {'and_criteria': [{'attribute_exists': None,
                                                                                    'begins_with': None,
                                                                                    'case_sensitive': None,
                                                                                    'field': None,
                                                                                    'operator': '>=',
                                                                                    'type': 'size',
                                                                                    'units': 'B',
                                                                                    'use_relative_time': None,
                                                                                    'value': '61440'},
                                                                                   {'attribute_exists': None,
                                                                                    'begins_with': None,
                                                                                    'case_sensitive': None,
                                                                                    'field': None,
                                                                                    'operator': '==',
                                                                                    'type': 'size',
                                                                                    'units': 'B',
                                                                                    'use_relative_time': None,
                                                                                    'value': '64424509440'}]}]},
                       'id': 40, 'name': 'test_113', 'state': 'disabled', 'state_details': 'Policy has no CloudPools actions'}]}

    @staticmethod
    def get_filepoolpolicy_exception_response(response_type):
        if response_type == 'get_details_exception':
            return "Fetching file pool policies failed with error: SDK Error message"
        elif response_type == 'delete_exception':
            return "Deleting file pool policies failed with error: SDK Error message"

    @staticmethod
    def get_filepoolpolicy_error_response(response_type):
        if response_type == 'create_id_exception':
            return "Invalid argument 'policy_id' while creating a file pool policy"
        elif response_type == 'create_name_exception':
            return "'policy_name' is required to create a file pool policy"
        elif response_type == 'create_file_matching_pattern_exception':
            return "file_matching_pattern should not be None"
        elif response_type == 'create_filematchingpattern_or_exception':
            return "Number of 'or_criteria' item should be in range of 1 to 3"
        elif response_type == 'create_filematchingpattern_and_exception':
            return "Number of 'and_criteria' item should be in range of 1 to 5"
        elif response_type == 'create_filematchingpattern_type_exception':
            return "'type' field should be present in 'and_criteria' item"
        elif response_type == 'create_extra_field_exception':
            return "Criteria option 'file_name' should have only these field's ['type', 'value', 'condition', 'case_sensitive']"
        elif response_type == 'create_required_field_exception':
            return "Criteria option 'file_name' should have these field's ['value', 'condition'] and it should not be empty"
        elif response_type == 'create_condition_field_exception':
            return "Criteria option 'file_name' should only have these '['matches', 'does_not_match']' values in 'condition'"
        elif response_type == 'custom_field_add_value_exception':
            return "Criteria option 'file_attribute' should not have 'value' option if 'condition' is exists or does_not_exist"
        elif response_type == 'has_relative_datetime_count_exception':
            return "Criteria option accessed should not have 'relative_datetime_count' option if 'condition' is after or before"
        elif response_type == 'has_datetime_time_exception':
            return "Criteria option accessed should not have 'datetime_value' option if 'condition' is is_newer_than or is_older_than"
        elif response_type == 'wrong_strptime_fmt_exception':
            return "Criteria option accessed should have 'datetime_value' in format 'YYYY-MM-DD HOUR:MINUTE'"
        elif response_type == 'data_storage_invalid_tier_exception':
            return "Processing action 'apply_data_storage_policy' failed with error: dummy_tier not found"
        elif response_type == 'snapshot_storage_invalid_tier_exception':
            return "Processing action 'apply_snapshot_storage_policy' failed with error: dummy_tier not found"

    @staticmethod
    def get_storage_tiers_response():
        """
        Return MagicMock object for storage tier
        """
        tiers_list = MagicMock()
        tiers_list.tiers = MagicMock()
        tier_one = MagicMock()
        tier_one.name = 'test_ansible_neo_tier'
        tier_one.lnns = [1, 2, 3]
        tiers_list.tiers = [tier_one]
        return tiers_list

    @staticmethod
    def get_storage_nodepools_response():
        """
        Return MagicMock object for storage nodepool
        """
        nodepools_list = MagicMock()
        nodepools_list.nodepools = MagicMock()
        nodepool_one = MagicMock()
        nodepool_one.name = 'test_nodepool'
        nodepool_one.tier = None
        nodepools_list.nodepools = [nodepool_one]
        return nodepools_list
