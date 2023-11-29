# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for User module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.user import User
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_user_api \
    import MockUserApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException


class TestUser():
    user_args = MockUserApi.USER_COMMON_ARGS

    @pytest.fixture
    def user_module_mock(self, mocker):
        mocker.patch(MockUserApi.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        user_module_mock = User()
        user_module_mock.module.check_mode = False
        return user_module_mock

    def test_create_user_with_id(self, user_module_mock):
        self.user_args.update({
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': '1234567',
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': "Isilon Users",
            'state': 'present'
        })
        user_module_mock.module.params = self.user_args
        user_module_mock.get_user_details = MagicMock(side_effect=[None, MockUserApi.GET_USER_DETAILS])
        utils.isi_sdk.AuthUserCreateParams = MagicMock(return_value=MockUserApi.CREATE_USER_WITH_ID)
        user_module_mock.api_instance.create_auth_user = MagicMock(return_value=7000)
        user_module_mock.perform_module_operation()
        assert "7000" in user_module_mock.module.exit_json.call_args[1]['user_details']['uid']['id']

    def test_create_user_with_id_exception(self, user_module_mock):
        self.user_args.update({
            'user_name': "test_user_1",
            'user_id': 7000,
            'access_zone': "System",
            'provider_type': "local",
            'full_name': 'Test User',
            'password': '1234567',
            'email': 'test_user_2@gamil.com',
            'shell': "/usr/local/bin/zsh",
            'primary_group': "Isilon Users",
            'state': 'present'
        })
        user_module_mock.module.params = self.user_args
        user_module_mock.get_user_details = MagicMock(side_effect=[None, MockUserApi.GET_USER_DETAILS])
        utils.isi_sdk.AuthUserCreateParams = MagicMock(return_value=MockUserApi.CREATE_USER_WITH_ID)
        user_module_mock.api_instance.create_auth_user = MagicMock(side_effect=Exception)
        user_module_mock.perform_module_operation()
        assert MockUserApi.get_create_user_id_exception_response() in \
            user_module_mock.module.fail_json.call_args[1]['msg']
