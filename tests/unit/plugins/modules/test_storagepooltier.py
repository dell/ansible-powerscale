# Copyright: (c) 2022-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for storagepooltier module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.storagepooltier import StoragePoolTier
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_storagepooltier_api \
    import MockStoragePoolTierApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase


class TestStorageTier(PowerScaleUnitBase):
    storagetier_args = MockStoragePoolTierApi.STORAGE_TIER_COMMON_ARGS

    @pytest.fixture
    def module_object(self, mocker):
        return StoragePoolTier

    def test_get_tier_details_exception(self, powerscale_module_mock):
        self.storagetier_args.update({
            'tier_name': 'test_tier',
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.storagetier_args
        powerscale_module_mock.storagepool_api.list_storagepool_tiers = MagicMock(
            side_effect=MockApiException)
        powerscale_module_mock.validate_create_inputs = MagicMock(
            return_value=None)
        powerscale_module_mock.create_tier = MagicMock(return_value=None)
        self.capture_fail_json_call(MockStoragePoolTierApi.get_storagetier_exception_response('get_details_exception'),
                                    powerscale_module_mock, True)

    def test_modify_tier_error(self, powerscale_module_mock):
        self.storagetier_args.update({
            'tier_name': 'test_tier',
            'nodepools': ['test_node1'],
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.storagetier_args
        powerscale_module_mock.storagepool_api.list_storagepool_tiers = MagicMock(
            return_value=MockStoragePoolTierApi.get_storage_tier_list())
        self.capture_fail_json_call(MockStoragePoolTierApi.get_storagetier_error_response('modify_error'),
                                    powerscale_module_mock, True)

    def test_delete_tier_exception(self, powerscale_module_mock):
        self.storagetier_args.update({
            'tier_name': 'test_tier',
            'state': 'absent'
        })
        powerscale_module_mock.module.params = self.storagetier_args
        powerscale_module_mock.storagepool_api.list_storagepool_tiers = MagicMock(
            return_value=MockStoragePoolTierApi.get_storage_tier_list())
        powerscale_module_mock.storagepool_api.delete_storagepool_tier = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(MockStoragePoolTierApi.get_storagetier_exception_response('delete_exception'),
                                    powerscale_module_mock, True)

    def test_delete_tier(self, powerscale_module_mock):
        self.storagetier_args.update({
            'tier_name': 'test_tier',
            'state': 'absent'
        })
        powerscale_module_mock.module.params = self.storagetier_args
        powerscale_module_mock.storagepool_api.list_storagepool_tiers = MagicMock(
            return_value=MockStoragePoolTierApi.get_storage_tier_list())
        powerscale_module_mock.storagepool_api.delete_storagepool_tier = MagicMock(
            return_value=None)
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_validate_tier_name_negative(self, powerscale_module_mock):
        self.storagetier_args.update({
            'tier_name': '',
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.storagetier_args
        powerscale_module_mock.storagepool_api.list_storagepool_tiers = MagicMock(
            return_value=MockSDKResponse({'tiers': []}))
        powerscale_module_mock.create_tier = MagicMock(return_value=None)
        self.capture_fail_json_call(MockStoragePoolTierApi.get_storagetier_error_response('tier_name_error'),
                                    powerscale_module_mock, True)

    def test_get_nodepools_error(self, powerscale_module_mock):
        self.storagetier_args.update({
            'tier_name': 'test_tier',
            'nodepools': ['test1'],
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.storagetier_args
        powerscale_module_mock.storagepool_api.list_storagepool_tiers = MagicMock(
            return_value=MockSDKResponse({'tiers': []}))
        powerscale_module_mock.storagepool_api.list_storagepool_nodepools = MagicMock(
            return_value=MockStoragePoolTierApi.NODE_POOL_NAME_LIST)
        powerscale_module_mock.create_tier = MagicMock(return_value=None)
        self.capture_fail_json_call(MockStoragePoolTierApi.get_storagetier_error_response('nodepools_error'),
                                    powerscale_module_mock, True)

    def test_create_tier(self, powerscale_module_mock):
        self.storagetier_args.update({
            'tier_name': 'test_tier',
            'nodepools': ['test_nodepool'],
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.storagetier_args
        powerscale_module_mock.storagepool_api.list_storagepool_tiers = MagicMock(side_effect=[MockSDKResponse({'tiers': []}),
                                                                                               MockStoragePoolTierApi.get_storage_tier_list()])
        powerscale_module_mock.storagepool_api.list_storagepool_nodepools = MagicMock(
            return_value=MockStoragePoolTierApi.NODE_POOL_NAME_LIST)
        utils.isi_sdk.StoragepoolTierCreateParams(return_value=None)
        powerscale_module_mock.storagepool_api.create_storagepool_tier = MagicMock(
            return_value=MockStoragePoolTierApi.get_storage_tier_create_response())
        powerscale_module_mock.perform_module_operation()
        assert MockStoragePoolTierApi.STORAGE_TIER_LIST['tiers'][0]['name'] == \
            powerscale_module_mock.module.exit_json.call_args[1]['storage_pool_tier_details']['name']

    def test_create_tier_exception(self, powerscale_module_mock):
        self.storagetier_args.update({
            'tier_name': 'test_tier',
            'nodepools': ['test_nodepool'],
            'state': 'present'
        })
        powerscale_module_mock.module.params = self.storagetier_args
        powerscale_module_mock.storagepool_api.list_storagepool_tiers = MagicMock(
            return_value=MockSDKResponse({'tiers': []}))
        powerscale_module_mock.storagepool_api.list_storagepool_nodepools = MagicMock(
            return_value=MockStoragePoolTierApi.NODE_POOL_NAME_LIST)
        utils.isi_sdk.StoragepoolTierCreateParams(return_value=None)
        powerscale_module_mock.storagepool_api.create_storagepool_tier = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(MockStoragePoolTierApi.get_storagetier_exception_response('create_tier_exception'),
                                    powerscale_module_mock, True)
