# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for Group module on PowerScale"""

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

from ansible_collections.dellemc.powerscale.plugins.modules.group import Group
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_group_api \
    import MockGroupApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException


class TestGroup():
    group_args = MockGroupApi.GROUP_COMMON_ARGS

    @pytest.fixture
    def group_module_mock(self, mocker):
        mocker.patch(MockGroupApi.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        group_module_mock = Group()
        group_module_mock.module.check_mode = False
        return group_module_mock

    def test_create_group_with_id(self, group_module_mock):
        self.group_args.update({
            'group_name': "test_group",
            'group_id': 1000,
            'access_zone': "System",
            'provider_type': "local",
            'state': 'present'
        })
        group_module_mock.module.params = self.group_args
        group_module_mock.get_group_details = MagicMock(side_effect=[None, MockGroupApi.GET_GROUP_DETAILS])
        utils.isi_sdk.AuthGroupCreateParams = MagicMock(return_value=MockGroupApi.CREATE_GROUP_WITH_ID)
        group_module_mock.api_instance.create_auth_group = MagicMock(return_value=1000)
        group_module_mock.perform_module_operation()
        assert "1000" in group_module_mock.module.exit_json.call_args[1]['group_details']['gid']['id']

    def test_create_group_with_id_exception(self, group_module_mock):
        self.group_args.update({
            'group_name': "test_group",
            'group_id': 1000,
            'access_zone': "System",
            'provider_type': "local",
            'state': 'present'
        })
        group_module_mock.module.params = self.group_args
        group_module_mock.get_group_details = MagicMock(side_effect=[None, MockGroupApi.GET_GROUP_DETAILS])
        utils.isi_sdk.AuthGroupCreateParams = MagicMock(return_value=MockGroupApi.CREATE_GROUP_WITH_ID)
        group_module_mock.api_instance.create_auth_group = MagicMock(side_effect=Exception)
        group_module_mock.perform_module_operation()
        assert MockGroupApi.get_create_group_id_exception_response() in \
            group_module_mock.module.fail_json.call_args[1]['msg']
