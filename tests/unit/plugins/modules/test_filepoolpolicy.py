# Copyright: (c) 2022-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for filepoolpolicy module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.filepoolpolicy import FilePoolPolicy
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_filepoolpolicy_api \
    import MockFilepoolpolicyApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase


class TestFilepoolpolicy(PowerScaleUnitBase):
    filepoolpolicy_args = MockFilepoolpolicyApi.FILEPOOLPOLICY_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return FilePoolPolicy

    def test_get_filepoolpolicy_by_id(self, powerscale_module_mock):
        filepoolpolicy_details = MockFilepoolpolicyApi.GET_FILEPOOLPOLICY_RESPONSE
        self.filepoolpolicy_args.update({
            'policy_id': 40,
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.filepoolpolicy_args
        powerscale_module_mock.filepool_api.get_filepool_policy = MagicMock(
            return_value=MockSDKResponse(filepoolpolicy_details))
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False
        assert filepoolpolicy_details['policies'][0] == powerscale_module_mock.module.exit_json.call_args[1][
            'filepool_policy_details']

    def test_get_filepoolpolicy_by_id_exception(self, powerscale_module_mock):
        self.filepoolpolicy_args.update({
            'policy_id': 40,
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.filepoolpolicy_args
        powerscale_module_mock.filepool_api.get_filepool_policy = MagicMock(side_effect=MockApiException)
        mock_none_response = MagicMock(return_value=None)
        powerscale_module_mock.validate_create_inputs = mock_none_response
        powerscale_module_mock.validate_file_matching_criteria = mock_none_response
        powerscale_module_mock.form_actions_payload = mock_none_response
        powerscale_module_mock.create_file_pool_policy = mock_none_response
        self.capture_fail_json_call(
            MockFilepoolpolicyApi.get_filepoolpolicy_exception_response('get_details_exception'),
            invoke_perform_module=True)

    def test_create_filepoolpolicy_id_exception(self, powerscale_module_mock):
        self.filepoolpolicy_args.update({
            'policy_id': 4,
            'policy_name': "test_policy_dummy",
            'file_matching_pattern': {
                'or_criteria': []
            },
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.filepoolpolicy_args
        powerscale_module_mock.filepool_api.get_filepool_policy = MagicMock(
            return_value=MockSDKResponse({'policies': [None]}))
        mock_none_response = MagicMock(return_value=None)
        powerscale_module_mock.validate_file_matching_criteria = mock_none_response
        powerscale_module_mock.form_actions_payload = mock_none_response
        powerscale_module_mock.create_file_pool_policy = mock_none_response
        self.capture_fail_json_call(MockFilepoolpolicyApi.get_filepoolpolicy_error_response('create_id_exception'),
                                    invoke_perform_module=True)

    def test_create_filepoolpolicy_name_exception(self, powerscale_module_mock):
        self.filepoolpolicy_args.update({
            'file_matching_pattern': {
                'or_criteria': []
            },
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.filepoolpolicy_args
        powerscale_module_mock.filepool_api.list_filepool_policies = MagicMock(
            return_value=MockSDKResponse({'policies': []}))
        mock_none_response = MagicMock(return_value=None)
        powerscale_module_mock.validate_file_matching_criteria = mock_none_response
        powerscale_module_mock.form_actions_payload = mock_none_response
        powerscale_module_mock.create_file_pool_policy = mock_none_response
        self.capture_fail_json_call(MockFilepoolpolicyApi.get_filepoolpolicy_error_response('create_name_exception'),
                                    invoke_perform_module=True)

    def test_create_filepoolpolicy_file_matching_pattern_exception(self, powerscale_module_mock):
        self.filepoolpolicy_args.update({
            'policy_name': "test_policy_dummy",
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.filepoolpolicy_args
        powerscale_module_mock.filepool_api.list_filepool_policies = MagicMock(
            return_value=MockSDKResponse({'policies': []}))
        mock_none_response = MagicMock(return_value=None)
        powerscale_module_mock.validate_file_matching_criteria = mock_none_response
        powerscale_module_mock.form_actions_payload = mock_none_response
        powerscale_module_mock.create_file_pool_policy = mock_none_response
        self.capture_fail_json_call(
            MockFilepoolpolicyApi.get_filepoolpolicy_error_response('create_file_matching_pattern_exception'),
            invoke_perform_module=True)

    def test_create_filepoolpolicy_filematchingpattern_or_exception(self, powerscale_module_mock):
        self.filepoolpolicy_args.update({
            'policy_name': "test_policy_dummy",
            'file_matching_pattern': {
                'or_criteria': []
            },
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.filepoolpolicy_args
        powerscale_module_mock.filepool_api.list_filepool_policies = MagicMock(
            return_value=MockSDKResponse({'policies': []}))
        mock_none_response = MagicMock(return_value=None)
        powerscale_module_mock.validate_create_inputs = mock_none_response
        powerscale_module_mock.form_actions_payload = mock_none_response
        powerscale_module_mock.create_file_pool_policy = mock_none_response
        self.capture_fail_json_call(
            MockFilepoolpolicyApi.get_filepoolpolicy_error_response('create_filematchingpattern_or_exception'),
            invoke_perform_module=True)

    def test_create_filepoolpolicy_filematchingpattern_and_exception(self, powerscale_module_mock):
        self.filepoolpolicy_args.update({
            'policy_name': "test_policy_dummy",
            'file_matching_pattern': {
                'or_criteria': [{
                    'and_criteria': []
                }]
            },
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.filepoolpolicy_args
        powerscale_module_mock.filepool_api.list_filepool_policies = MagicMock(
            return_value=MockSDKResponse({'policies': []}))
        mock_none_response = MagicMock(return_value=None)
        powerscale_module_mock.validate_create_inputs = mock_none_response
        powerscale_module_mock.form_actions_payload = mock_none_response
        powerscale_module_mock.create_file_pool_policy = mock_none_response
        self.capture_fail_json_call(
            MockFilepoolpolicyApi.get_filepoolpolicy_error_response('create_filematchingpattern_and_exception'),
            invoke_perform_module=True)

    def test_create_filepoolpolicy_filematchingpattern_type_exception(self, powerscale_module_mock):
        self.filepoolpolicy_args.update({
            'policy_name': "test_policy_dummy",
            'file_matching_pattern': {
                'or_criteria': [{
                    'and_criteria': [{}]
                }]
            },
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.filepoolpolicy_args
        powerscale_module_mock.filepool_api.list_filepool_policies = MagicMock(
            return_value=MockSDKResponse({'policies': []}))
        mock_none_response = MagicMock(return_value=None)
        powerscale_module_mock.validate_create_inputs = mock_none_response
        powerscale_module_mock.form_criteria_item_and = mock_none_response
        powerscale_module_mock.form_actions_payload = mock_none_response
        powerscale_module_mock.create_file_pool_policy = mock_none_response
        self.capture_fail_json_call(
            MockFilepoolpolicyApi.get_filepoolpolicy_error_response('create_filematchingpattern_type_exception'),
            invoke_perform_module=True)

    def test_create_filepoolpolicy_extra_field_exception(self, powerscale_module_mock):
        self.filepoolpolicy_args.update({
            'policy_name': "test_policy_dummy",
            'file_matching_pattern': {
                'or_criteria': [{
                    'and_criteria': [{
                        'type': "file_name",
                        'condition': "matches",
                        'value': "we",
                        'case_sensitive': False,
                        'file_type_option': "file"
                    }]
                }]
            },
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.filepoolpolicy_args
        powerscale_module_mock.filepool_api.list_filepool_policies = MagicMock(
            return_value=MockSDKResponse({'policies': []}))
        mock_none_response = MagicMock(return_value=None)
        powerscale_module_mock.create_file_pool_policy = mock_none_response
        self.capture_fail_json_call(
            MockFilepoolpolicyApi.get_filepoolpolicy_error_response('create_extra_field_exception'),
            invoke_perform_module=True)

    def test_create_filepoolpolicy_required_field_exception(self, powerscale_module_mock):
        self.set_module_params(self.filepoolpolicy_args, {
            'policy_name': "test_policy_dummy",
            'file_matching_pattern': {
                'or_criteria': [{
                    'and_criteria': [{
                        'type': "file_name",
                        'condition': "matches",
                        'value': "we",
                        'case_sensitive': False,
                    }]
                }]
            },
            'state': 'present'
        })

        powerscale_module_mock.module.params = self.filepoolpolicy_args
        powerscale_module_mock.filepool_api.list_filepool_policies = MagicMock(
            return_value=MockSDKResponse({'policies': []}))
        with pytest.raises(SystemExit):
            powerscale_module_mock.validate_extra_fields_and_required_fields('file_name',
                                                                             ['type', 'value', 'condition', 'case_sensitive'],
                                                                             ['value', 'condition'],
                                                                             ['condition'])
        assert MockFilepoolpolicyApi.get_filepoolpolicy_error_response('create_required_field_exception') \
               == powerscale_module_mock.module.fail_json.call_args[1][
                   'msg']

    def test_create_filepoolpolicy_condition_field_exception(self, powerscale_module_mock):
        self.filepoolpolicy_args.update({
            'policy_name': "test_policy_dummy",
            'file_matching_pattern': {
                'or_criteria': [{
                    'and_criteria': [{
                        'type': "file_name",
                        'condition': "matches",
                        'value': "we",
                        'case_sensitive': False,
                    }]
                }]
            },
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.filepoolpolicy_args
        powerscale_module_mock.filepool_api.list_filepool_policies = MagicMock(
            return_value=MockSDKResponse({'policies': []}))
        with pytest.raises(SystemExit):
            powerscale_module_mock.validate_conditions_on_file_attribute('file_name',
                                                                         'dummy',
                                                                         ['matches', 'does_not_match'])
        assert MockFilepoolpolicyApi.get_filepoolpolicy_error_response('create_condition_field_exception') \
               == powerscale_module_mock.module.fail_json.call_args[1][
                   'msg']

    def test_create_filepoolpolicy_custom_field_add_value_exception(self, powerscale_module_mock):
        self.filepoolpolicy_args.update({
            'policy_name': "test_policy_dummy",
            'file_matching_pattern': {
                'or_criteria': [{
                    'and_criteria': [{
                        'type': "file_attribute",
                        'condition': "does_not_exist",
                        'field': "test",
                        'value': "dummy_field"
                    }]
                }]
            },
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.filepoolpolicy_args
        powerscale_module_mock.filepool_api.list_filepool_policies = MagicMock(
            return_value=MockSDKResponse({'policies': []}))
        mock_none_response = MagicMock(return_value=None)
        powerscale_module_mock.create_file_pool_policy = mock_none_response
        self.capture_fail_json_call(
            MockFilepoolpolicyApi.get_filepoolpolicy_error_response('custom_field_add_value_exception'),
            invoke_perform_module=True)

    def test_create_filepoolpolicy_datetime_field_has_relative_datetime_count_exception(self, powerscale_module_mock):
        self.filepoolpolicy_args.update({
            'policy_name': "test_policy_dummy",
            'file_matching_pattern': {
                'or_criteria': [{
                    'and_criteria': [{
                        'type': "accessed",
                        'condition': "after",
                        'relative_datetime_count': {
                            'time_value': 60,
                            'time_unit': "days"
                        },
                        'datetime_value': "2022-04-04 23:30"
                    }]
                }]
            },
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.filepoolpolicy_args
        powerscale_module_mock.filepool_api.list_filepool_policies = MagicMock(
            return_value=MockSDKResponse({'policies': []}))
        mock_none_response = MagicMock(return_value=None)
        powerscale_module_mock.create_file_pool_policy = mock_none_response
        self.capture_fail_json_call(
            MockFilepoolpolicyApi.get_filepoolpolicy_error_response('has_relative_datetime_count_exception'),
            invoke_perform_module=True)

    def test_create_filepoolpolicy_datetime_field_has_datetime_time_exception(self, powerscale_module_mock):
        self.filepoolpolicy_args.update({
            'policy_name': "test_policy_dummy",
            'file_matching_pattern': {
                'or_criteria': [{
                    'and_criteria': [{
                        'type': "accessed",
                        'condition': "is_older_than",
                        'relative_datetime_count': {
                            'time_value': 60,
                            'time_unit': "days"
                        },
                        'datetime_value': "2022-04-04 23:30"
                    }]
                }]
            },
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.filepoolpolicy_args
        powerscale_module_mock.filepool_api.list_filepool_policies = MagicMock(
            return_value=MockSDKResponse({'policies': []}))
        mock_none_response = MagicMock(return_value=None)
        powerscale_module_mock.create_file_pool_policy = mock_none_response
        self.capture_fail_json_call(
            MockFilepoolpolicyApi.get_filepoolpolicy_error_response('has_datetime_time_exception'),
            invoke_perform_module=True)

    def test_create_filepoolpolicy_datetime_field_wrong_strptime_fmt_exception(self, powerscale_module_mock):
        self.filepoolpolicy_args.update({
            'policy_name': "test_policy_dummy",
            'file_matching_pattern': {
                'or_criteria': [{
                    'and_criteria': [{
                        'type': "accessed",
                        'condition': "after",
                        'datetime_value': "2022-04-04 23:30:01"
                    }]
                }]
            },
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.filepoolpolicy_args
        powerscale_module_mock.filepool_api.list_filepool_policies = MagicMock(
            return_value=MockSDKResponse({'policies': []}))
        mock_none_response = MagicMock(return_value=None)
        powerscale_module_mock.create_file_pool_policy = mock_none_response
        self.capture_fail_json_call(
            MockFilepoolpolicyApi.get_filepoolpolicy_error_response('wrong_strptime_fmt_exception'),
            invoke_perform_module=True)

    def test_create_filepoolpolicy_data_storage_invalid_tier_exception(self, powerscale_module_mock):
        self.filepoolpolicy_args.update({
            'policy_name': "test_policy_dummy",
            'apply_data_storage_policy': {
                'ssd_strategy': "SSD_metadata_read_acceleration",
                'storagepool': "dummy_tier"
            },
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.filepoolpolicy_args
        storage_tiers_mock_data = MockFilepoolpolicyApi.get_storage_tiers_response()
        storage_nodepools_mock_data = MockFilepoolpolicyApi.get_storage_nodepools_response()
        powerscale_module_mock.filepool_api.list_filepool_policies = MagicMock(
            return_value=MockSDKResponse({'policies': []}))
        powerscale_module_mock.storagepool_api.list_storagepool_tiers = MagicMock(return_value=storage_tiers_mock_data)
        powerscale_module_mock.storagepool_api.list_storagepool_nodepools = MagicMock(
            return_value=storage_nodepools_mock_data)
        mock_none_response = MagicMock(return_value=None)
        powerscale_module_mock.validate_create_inputs = mock_none_response
        powerscale_module_mock.validate_file_matching_criteria = mock_none_response
        powerscale_module_mock.create_file_pool_policy = mock_none_response
        self.capture_fail_json_call(
            MockFilepoolpolicyApi.get_filepoolpolicy_error_response('data_storage_invalid_tier_exception'),
            invoke_perform_module=True)

    def test_create_filepoolpolicy_snapshot_storage_invalid_tier_exception(self, powerscale_module_mock):
        self.filepoolpolicy_args.update({
            'policy_name': "test_policy_dummy",
            'apply_snapshot_storage_policy': {
                'ssd_strategy': "SSD_metadata_read_acceleration",
                'storagepool': "dummy_tier"
            },
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.filepoolpolicy_args
        storage_tiers_mock_data = MockFilepoolpolicyApi.get_storage_tiers_response()
        storage_nodepools_mock_data = MockFilepoolpolicyApi.get_storage_nodepools_response()
        powerscale_module_mock.filepool_api.list_filepool_policies = MagicMock(
            return_value=MockSDKResponse({'policies': []}))
        powerscale_module_mock.storagepool_api.list_storagepool_tiers = MagicMock(return_value=storage_tiers_mock_data)
        powerscale_module_mock.storagepool_api.list_storagepool_nodepools = MagicMock(
            return_value=storage_nodepools_mock_data)
        mock_none_response = MagicMock(return_value=None)
        powerscale_module_mock.validate_create_inputs = mock_none_response
        powerscale_module_mock.validate_file_matching_criteria = mock_none_response
        powerscale_module_mock.create_file_pool_policy = mock_none_response
        self.capture_fail_json_call(
            MockFilepoolpolicyApi.get_filepoolpolicy_error_response('snapshot_storage_invalid_tier_exception'),
            invoke_perform_module=True)

    def test_create_filepoolpolicy_criteria(self, powerscale_module_mock):
        create_args = MockFilepoolpolicyApi.FILEPOOLPOLICY_COMMON_CREATE_ARGS
        self.set_module_params(self.filepoolpolicy_args, create_args)
        new_filepoolpolicy_details = MockFilepoolpolicyApi.NEW_FILEPOOLPOLICY_RESPONSE
        storage_tiers_mock_data = MockFilepoolpolicyApi.get_storage_tiers_response()
        storage_nodepools_mock_data = MockFilepoolpolicyApi.get_storage_nodepools_response()
        powerscale_module_mock.storagepool_api.list_storagepool_tiers = MagicMock(return_value=storage_tiers_mock_data)
        powerscale_module_mock.storagepool_api.list_storagepool_nodepools = MagicMock(
            return_value=storage_nodepools_mock_data)
        powerscale_module_mock.filepool_api.list_filepool_policies = MagicMock(
            return_value=MockSDKResponse({'policies': []}))
        powerscale_module_mock.filepool_api.get_filepool_policy = MagicMock(
            return_value=MockSDKResponse(new_filepoolpolicy_details))
        create_response = MagicMock()
        create_response.id = '42'
        powerscale_module_mock.filepool_api.create_filepool_policy = MagicMock(return_value=create_response)
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        assert new_filepoolpolicy_details['policies'][0] == powerscale_module_mock.module.exit_json.call_args[1][
            'filepool_policy_details']

    def test_delete_filepoolpolicy(self, powerscale_module_mock):
        filepoolpolicy_details = MockFilepoolpolicyApi.GET_FILEPOOLPOLICY_RESPONSE
        self.filepoolpolicy_args.update({
            'policy_id': 40,
            'state': 'absent'
        })
        powerscale_module_mock.module.params = self.filepoolpolicy_args
        powerscale_module_mock.filepool_api.get_filepool_policy = MagicMock(
            return_value=MockSDKResponse(filepoolpolicy_details))
        powerscale_module_mock.filepool_api.delete_filepool_policy = MagicMock(return_value=None)
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_filepoolpolicy_exception(self, powerscale_module_mock):
        self.filepoolpolicy_args.update({
            'policy_id': 40,
            'state': 'absent'
        })
        powerscale_module_mock.module.params = self.filepoolpolicy_args
        filepoolpolicy_details = MockFilepoolpolicyApi.GET_FILEPOOLPOLICY_RESPONSE
        powerscale_module_mock.filepool_api.get_filepool_policy = MagicMock(
            return_value=MockSDKResponse(filepoolpolicy_details))
        powerscale_module_mock.filepool_api.delete_filepool_policy = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(MockFilepoolpolicyApi.get_filepoolpolicy_exception_response('delete_exception'),
                                    invoke_perform_module=True)
