# Copyright: (c) 2022, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for storagepooltier module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

utils.get_logger = MagicMock()
utils.isi_sdk = MagicMock()
from ansible.module_utils import basic
basic.AnsibleModule = MagicMock()

from ansible_collections.dellemc.powerscale.plugins.modules.storagepooltier import StoragePoolTier
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_storagepooltier_api \
    import MockStoragePoolTierApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse


class TestStorageTier():
    storagetier_args = MockStoragePoolTierApi.STORAGE_TIER_COMMON_ARGS

    @pytest.fixture
    def storagetier_module_mock(self, mocker):
        mocker.patch(MockStoragePoolTierApi.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        storagetier_module_mock = StoragePoolTier()
        storagetier_module_mock.module.check_mode = False
        return storagetier_module_mock

    def test_get_tier_details_exception(self, storagetier_module_mock):
        self.storagetier_args.update({
            'tier_name': 'test_tier',
            'state': 'present'
        })
        storagetier_module_mock.module.params = self.storagetier_args
        storagetier_module_mock.storagepool_api.list_storagepool_tiers = MagicMock(side_effect=MockApiException)
        storagetier_module_mock.validate_create_inputs = MagicMock(return_value=None)
        storagetier_module_mock.create_tier = MagicMock(return_value=None)
        storagetier_module_mock.perform_module_operation()
        assert MockStoragePoolTierApi.get_storagetier_exception_response('get_details_exception') == \
            storagetier_module_mock.module.fail_json.call_args[1]['msg']

    def test_modify_tier_error(self, storagetier_module_mock):
        self.storagetier_args.update({
            'tier_name': 'test_tier',
            'nodepools': ['test_node1'],
            'state': 'present'
        })
        storagetier_module_mock.module.params = self.storagetier_args
        storagetier_module_mock.storagepool_api.list_storagepool_tiers = MagicMock(return_value=MockStoragePoolTierApi.get_storage_tier_list())
        storagetier_module_mock.perform_module_operation()
        assert MockStoragePoolTierApi.get_storagetier_error_response('modify_error') == \
            storagetier_module_mock.module.fail_json.call_args[1]['msg']

    def test_delete_tier_exception(self, storagetier_module_mock):
        self.storagetier_args.update({
            'tier_name': 'test_tier',
            'state': 'absent'
        })
        storagetier_module_mock.module.params = self.storagetier_args
        storagetier_module_mock.storagepool_api.list_storagepool_tiers = MagicMock(return_value=MockStoragePoolTierApi.get_storage_tier_list())
        storagetier_module_mock.storagepool_api.delete_storagepool_tier = MagicMock(side_effect=MockApiException)
        storagetier_module_mock.perform_module_operation()
        assert MockStoragePoolTierApi.get_storagetier_exception_response('delete_exception') == \
            storagetier_module_mock.module.fail_json.call_args[1]['msg']

    def test_delete_tier(self, storagetier_module_mock):
        self.storagetier_args.update({
            'tier_name': 'test_tier',
            'state': 'absent'
        })
        storagetier_module_mock.module.params = self.storagetier_args
        storagetier_module_mock.storagepool_api.list_storagepool_tiers = MagicMock(return_value=MockStoragePoolTierApi.get_storage_tier_list())
        storagetier_module_mock.storagepool_api.delete_storagepool_tier = MagicMock(return_value=None)
        storagetier_module_mock.perform_module_operation()
        assert storagetier_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_validate_tier_name_negative(self, storagetier_module_mock):
        self.storagetier_args.update({
            'tier_name': '',
            'state': 'present'
        })
        storagetier_module_mock.module.params = self.storagetier_args
        storagetier_module_mock.storagepool_api.list_storagepool_tiers = MagicMock(return_value=MockSDKResponse({'tiers': []}))
        storagetier_module_mock.create_tier = MagicMock(return_value=None)
        storagetier_module_mock.perform_module_operation()
        assert MockStoragePoolTierApi.get_storagetier_error_response('tier_name_error') == \
            storagetier_module_mock.module.fail_json.call_args[1]['msg']

    def test_get_nodepools_error(self, storagetier_module_mock):
        self.storagetier_args.update({
            'tier_name': 'test_tier',
            'nodepools': ['test1'],
            'state': 'present'
        })
        storagetier_module_mock.module.params = self.storagetier_args
        storagetier_module_mock.storagepool_api.list_storagepool_tiers = MagicMock(return_value=MockSDKResponse({'tiers': []}))
        storagetier_module_mock.storagepool_api.list_storagepool_nodepools = MagicMock(return_value=MockStoragePoolTierApi.NODE_POOL_NAME_LIST)
        storagetier_module_mock.create_tier = MagicMock(return_value=None)
        storagetier_module_mock.perform_module_operation()
        assert MockStoragePoolTierApi.get_storagetier_error_response('nodepools_error') == \
            storagetier_module_mock.module.fail_json.call_args[1]['msg']

    def test_create_tier(self, storagetier_module_mock):
        self.storagetier_args.update({
            'tier_name': 'test_tier',
            'nodepools': ['test_nodepool'],
            'state': 'present'
        })
        storagetier_module_mock.module.params = self.storagetier_args
        storagetier_module_mock.storagepool_api.list_storagepool_tiers = MagicMock(side_effect=[MockSDKResponse({'tiers': []}),
                                                                                                MockStoragePoolTierApi.get_storage_tier_list()])
        storagetier_module_mock.storagepool_api.list_storagepool_nodepools = MagicMock(return_value=MockStoragePoolTierApi.NODE_POOL_NAME_LIST)
        utils.isi_sdk.StoragepoolTierCreateParams(return_value=None)
        storagetier_module_mock.storagepool_api.create_storagepool_tier = MagicMock(return_value=MockStoragePoolTierApi.get_storage_tier_create_response())
        storagetier_module_mock.perform_module_operation()
        assert MockStoragePoolTierApi.STORAGE_TIER_LIST['tiers'][0]['name'] == \
            storagetier_module_mock.module.exit_json.call_args[1]['storage_pool_tier_details']['name']

    def test_create_tier_exception(self, storagetier_module_mock):
        self.storagetier_args.update({
            'tier_name': 'test_tier',
            'nodepools': ['test_nodepool'],
            'state': 'present'
        })
        storagetier_module_mock.module.params = self.storagetier_args
        storagetier_module_mock.storagepool_api.list_storagepool_tiers = MagicMock(return_value=MockSDKResponse({'tiers': []}))
        storagetier_module_mock.storagepool_api.list_storagepool_nodepools = MagicMock(return_value=MockStoragePoolTierApi.NODE_POOL_NAME_LIST)
        utils.isi_sdk.StoragepoolTierCreateParams(return_value=None)
        storagetier_module_mock.storagepool_api.create_storagepool_tier = MagicMock(side_effect=MockApiException)
        storagetier_module_mock.perform_module_operation()
        assert MockStoragePoolTierApi.get_storagetier_exception_response('create_tier_exception') == \
            storagetier_module_mock.module.fail_json.call_args[1]['msg']
