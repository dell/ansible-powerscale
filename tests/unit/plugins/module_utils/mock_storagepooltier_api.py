# Copyright: (c) 2022, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock Api response for Unit tests of storagepooltier module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response import MockSDKResponse

__metaclass__ = type

from mock.mock import MagicMock


class MockStoragePoolTierApi:
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'
    STORAGE_TIER_COMMON_ARGS = {
        'onefs_host': '**.***.**.***',
        'tier_id': None,
        'tier_name': None,
        'nodepools': [],
        'state': None
    }
    STORAGE_TIER_LIST = \
        {'tiers': [{'children': ['test_nodepool'],
                    'name': 'test_tier',
                    'id': 31,
                    'lnns': [1, 2, 3]}],
         'total': 1}
    NODE_POOL_NAME_LIST = \
        MockSDKResponse({'nodepools': [{'name': 'test_nodepool'}]})

    @staticmethod
    def get_storage_tier_list():
        return MockSDKResponse(MockStoragePoolTierApi.STORAGE_TIER_LIST)

    @staticmethod
    def get_storage_tier_create_response():
        create_response = MagicMock()
        create_response.id = 32
        return create_response

    @staticmethod
    def get_storagetier_exception_response(response_type):
        if response_type == 'get_details_exception':
            return "Fetching storage pool tier details failed with error: SDK Error message"
        elif response_type == 'delete_exception':
            return "Deleting storage pool tier failed with error: SDK Error message"
        elif response_type == 'get_nodepools_exception':
            return "Getting list of nodepools names failed with error: SDK Error message"
        elif response_type == 'create_tier_exception':
            return "Creating storage pool tier failed with error: SDK Error message"

    @staticmethod
    def get_storagetier_error_response(response_type):
        if response_type == 'modify_error':
            return "Storage pool tier modification not supported."
        elif response_type == 'tier_name_error':
            return "'tier_name' is required to create a storage pool tier"
        elif response_type == 'nodepools_error':
            return "nodepool's {'test1'} are invalid."
