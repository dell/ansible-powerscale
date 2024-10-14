# Copyright: (c) 2022-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for synciqpolicy module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.synciqpolicy import SynciqPolicy
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_synciqpolicy_api \
    import MockSynciqpolicyApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException


class TestSynciqPolicy():
    synciqpolicy_args = MockSynciqpolicyApi.SYNCIQPOLICY_COMMON_ARGS

    @pytest.fixture
    def synciqpolicy_module_mock(self, mocker):
        mocker.patch(MockSynciqpolicyApi.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        synciqpolicy_module_mock = SynciqPolicy()
        synciqpolicy_module_mock.module.check_mode = False
        return synciqpolicy_module_mock

    def test_create_synciqpolicy(self, synciqpolicy_module_mock):
        self.synciqpolicy_args.update({
            'policy_name': 'Policy_SP',
            'action': 'copy',
            'description': 'Creating a policy',
            'source_cluster': {
                'source_root_path': '/test/home'
            },
            'target_cluster': {
                'target_host': "target_host-1",
                'target_path': "/test/target"
            },
            'accelerated_failback': False,
            'restrict_target_network': True,
            'state': 'present'
        })
        synciqpolicy_module_mock.module.params = self.synciqpolicy_args
        synciq_policy_details = MockSynciqpolicyApi.GET_SYNCIQPOLICY_RESPONSE[0]
        policy_obj = MagicMock()
        policy_obj.name = synciq_policy_details['name']
        policy_obj.update = MagicMock(return_value=None)
        initial_policy_none_response = MagicMock()
        initial_policy_none_response.policies = None
        synciqpolicy_module_mock.api_instance.get_sync_policy = MagicMock(side_effect=[initial_policy_none_response, policy_obj])
        synciqpolicy_module_mock.api_instance.create_sync_policy = MagicMock(return_value=synciq_policy_details['id'])
        synciqpolicy_module_mock.get_synciq_policy_display_attributes = MagicMock(return_value=synciq_policy_details)
        synciqpolicy_module_mock.get_policy_jobs = MagicMock(return_value=[])
        synciqpolicy_module_mock.perform_module_operation()
        assert synciqpolicy_module_mock.module.exit_json.call_args[1]['changed'] is True
        assert synciqpolicy_module_mock.module.exit_json.call_args[1]['create_synciq_policy'] is True

    def test_create_synciqpolicy_exception(self, synciqpolicy_module_mock):
        self.synciqpolicy_args.update({
            'policy_name': 'Policy_SP',
            'action': 'copy',
            'description': 'Creating a policy for getting exception',
            'source_cluster': {
                'source_root_path': '/test/home_exception'
            },
            'target_cluster': {
                'target_host': "target_host-1",
                'target_path': "/test/target_exception"
            },
            'accelerated_failback': False,
            'restrict_target_network': True,
            'state': 'present'
        })
        synciqpolicy_module_mock.module.params = self.synciqpolicy_args
        synciq_policy_details = MockSynciqpolicyApi.GET_SYNCIQPOLICY_RESPONSE[0]
        policy_obj = MagicMock()
        policy_obj.name = synciq_policy_details['name']
        policy_obj.update = MagicMock(return_value=None)
        initial_policy_none_response = MagicMock()
        initial_policy_none_response.policies = None
        synciqpolicy_module_mock.api_instance.get_sync_policy = MagicMock(side_effect=[initial_policy_none_response, policy_obj])
        synciqpolicy_module_mock.api_instance.create_sync_policy = MagicMock(side_effect=MockApiException())
        synciqpolicy_module_mock.get_synciq_policy_display_attributes = MagicMock(return_value=synciq_policy_details)
        synciqpolicy_module_mock.get_policy_jobs = MagicMock(return_value=[])
        synciqpolicy_module_mock.perform_module_operation()
        assert synciqpolicy_module_mock.module.fail_json.call_args[1]['msg'] == MockSynciqpolicyApi.get_api_exception_messages('create')

    def test_modify_synciqpolicy(self, synciqpolicy_module_mock):
        self.synciqpolicy_args.update({
            'policy_name': 'Policy_SP',
            'accelerated_failback': True,
            'state': 'present'
        })
        synciqpolicy_module_mock.module.params = self.synciqpolicy_args
        synciq_policy_details = MockSynciqpolicyApi.GET_SYNCIQPOLICY_RESPONSE[0]
        policy_obj = MagicMock()
        policy_obj.name = synciq_policy_details['name']
        policy_obj.id = synciq_policy_details['id']
        policy_obj.update = MagicMock(return_value=None)
        synciqpolicy_module_mock.get_synciq_policy_details = MagicMock(return_value=(policy_obj, None))
        synciqpolicy_module_mock.get_synciq_policy_display_attributes = MagicMock(return_value=MockSynciqpolicyApi.get_synciqpolicy_modify_response())
        synciqpolicy_module_mock.api_instance.update_sync_policy = MagicMock(return_value=None)
        synciqpolicy_module_mock.get_policy_jobs = MagicMock(return_value=[])
        synciqpolicy_module_mock.perform_module_operation()
        assert synciqpolicy_module_mock.module.exit_json.call_args[1]['changed'] is True
        assert synciqpolicy_module_mock.module.exit_json.call_args[1]['modify_synciq_policy'] is True

    def test_modify_synciqpolicy_exception(self, synciqpolicy_module_mock):
        self.synciqpolicy_args.update({
            'policy_name': 'Policy_SP',
            'accelerated_failback': True,
            'state': 'present'
        })
        synciqpolicy_module_mock.module.params = self.synciqpolicy_args
        synciq_policy_details = MockSynciqpolicyApi.GET_SYNCIQPOLICY_RESPONSE[0]
        policy_obj = MagicMock()
        policy_obj.name = synciq_policy_details['name']
        policy_obj.id = synciq_policy_details['id']
        policy_obj.update = MagicMock(return_value=None)
        synciqpolicy_module_mock.get_synciq_policy_details = MagicMock(return_value=(policy_obj, None))
        synciqpolicy_module_mock.get_synciq_policy_display_attributes = MagicMock(return_value=MockSynciqpolicyApi.get_synciqpolicy_modify_response())
        synciqpolicy_module_mock.api_instance.update_sync_policy = MagicMock(side_effect=MockApiException())
        synciqpolicy_module_mock.get_policy_jobs = MagicMock(return_value=[])
        synciqpolicy_module_mock.perform_module_operation()
        assert synciqpolicy_module_mock.module.fail_json.call_args[1]['msg'] == MockSynciqpolicyApi.get_api_exception_messages('modify')
