# Copyright: (c) 2021-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for groupnets module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.groupnet import Groupnet
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils \
    import mock_groupnet_api as MockGroupnetApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils \
    import test_utils


class TestGroupnet():
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'
    groupnet_name = 'groupnet_test'
    groupnet_args = {'groupnet_name': groupnet_name, 'state': 'present',
                     'description': None, 'dns_servers': [],
                     'dns_server_state': None, 'dns_search_suffix': None,
                     'dns_search_suffix_state': None, 'new_groupnet_name': None}

    @pytest.fixture
    def groupnet_module_mock(self, mocker):
        mocker.patch(self.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        groupnet_module_mock = Groupnet()
        return groupnet_module_mock

    def test_invalid_groupnet_name(self, groupnet_module_mock):
        groupnet_name = 'groupnet_test_**()'
        self.groupnet_args.update({'groupnet_name': groupnet_name})
        groupnet_module_mock.module.params = self.groupnet_args
        groupnet_module_mock.perform_module_operation()

        assert groupnet_module_mock.module.fail_json.call_args[1]['msg'] \
            == MockGroupnetApi.get_invalid_groupnet()

    def test_invalid_groupnet_name_len(self, groupnet_module_mock):
        groupnet_name = 'groupnet_test_groupnet_test_groupnet_test_'
        self.groupnet_args.update({'groupnet_name': groupnet_name})
        groupnet_module_mock.module.params = self.groupnet_args
        groupnet_module_mock.perform_module_operation()

        assert groupnet_module_mock.module.fail_json.call_args[1]['msg'] \
            == MockGroupnetApi.get_invalid_groupnet_len()

    def test_invalid_dns_servers(self, groupnet_module_mock):
        self.groupnet_args.update({'dns_servers': ['a.2.2.2'],
                                   'dns_server_state': 'remove'})
        groupnet_module_mock.module.params = self.groupnet_args
        groupnet_module_mock.perform_module_operation()

        assert groupnet_module_mock.module.fail_json.call_args[1]['msg'] \
            == MockGroupnetApi.get_invalid_dns()

    def test_invalid_description(self, groupnet_module_mock):
        self.groupnet_args.update({'description': test_utils.get_desc(129)})
        groupnet_module_mock.module.params = self.groupnet_args
        groupnet_module_mock.perform_module_operation()

        assert groupnet_module_mock.module.fail_json.call_args[1]['msg'] \
            == MockGroupnetApi.get_invalid_desc()

    def test_get_groupnet_details(self, groupnet_module_mock):
        groupnet_module_mock.module.params = self.groupnet_args
        groupnet_module_mock.network_api.get_network_groupnet(self.groupnet_name).to_dict \
            = MagicMock(return_value=MockGroupnetApi.get_groupnet_details(self.groupnet_name))
        groupnet_module_mock.perform_module_operation()

        assert (MockGroupnetApi.get_groupnet_details('groupnet_test')['groupnets'][0]
                == groupnet_module_mock.module.exit_json.call_args[1]["groupnet_details"])
        assert groupnet_module_mock.module.exit_json.call_args[1]["changed"] is False

    def test_get_groupnet_throws_generic_exception(self, groupnet_module_mock):
        groupnet_module_mock.module.params = self.groupnet_args
        groupnet_module_mock.network_api.get_network_groupnet \
            = MagicMock(side_effect=Exception)
        groupnet_module_mock.perform_module_operation()

        assert MockGroupnetApi.get_groupnet_ex_msg(self.groupnet_name) in \
            groupnet_module_mock.module.fail_json.call_args[1]['msg']

    def test_get_groupnet_throws_utils_exception(self, groupnet_module_mock):
        groupnet_module_mock.module.params = self.groupnet_args
        groupnet_module_mock.network_api.get_network_groupnet \
            = MagicMock(side_effect=utils.ApiException)
        groupnet_module_mock.perform_module_operation()

        assert MockGroupnetApi.get_groupnet_ex_msg(self.groupnet_name) in \
            groupnet_module_mock.module.fail_json.call_args[1]['msg']

    def test_get_groupnet_404_error(self, groupnet_module_mock):
        MockApiException.status = '404'
        groupnet_module_mock.module.params = self.groupnet_args
        groupnet_module_mock.network_api.get_network_groupnet \
            = MagicMock(side_effect=utils.ApiException)
        groupnet_module_mock.perform_module_operation()

        assert groupnet_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert groupnet_module_mock.module.exit_json.call_args[1]["create_groupnet"] is True

    def test_create_groupnet(self, groupnet_module_mock):
        groupnet_name = 'new_groupnet'
        self.groupnet_args.update({'groupnet_name': groupnet_name,
                                   'dns_servers': ['1.1.1.1', '1.1.1.2'],
                                   'description': 'Test Groupnet', 'dns_server_state': "add",
                                   'dns_search_suffix': ['ansibleneo.com', 'test.com'],
                                   'dns_search_suffix_state': "add"})
        groupnet_module_mock.module.params = self.groupnet_args
        groupnet_module_mock.get_groupnet_details \
            = MagicMock(return_value=MockGroupnetApi.get_groupnet_details(groupnet_name))
        groupnet_module_mock.network_api.create_network_groupnet = MagicMock(return_value=None)
        groupnet_module_mock.perform_module_operation()

        assert groupnet_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert groupnet_module_mock.module.exit_json.call_args[1]["create_groupnet"] is True

    def test_create_groupnet_throws_exception(self, groupnet_module_mock):
        groupnet_name = 'new_groupnet'
        self.groupnet_args.update({'groupnet_name': groupnet_name,
                                   'dns_servers': ['1.1.1.1', '1.1.1.2'],
                                   'dns_server_state': "add",
                                   'dns_search_suffix': ['ansibleneo.com', 'test.com'],
                                   'dns_search_suffix_state': "add"})
        groupnet_module_mock.module.params = self.groupnet_args
        groupnet_module_mock.get_groupnet_details \
            = MagicMock(return_value=MockGroupnetApi.get_groupnet_details(groupnet_name))
        groupnet_module_mock.network_api.create_network_groupnet \
            = MagicMock(side_effect=utils.ApiException)
        groupnet_module_mock.perform_module_operation()

        assert MockGroupnetApi.create_groupnet_ex_msg(groupnet_name) in \
            groupnet_module_mock.module.fail_json.call_args[1]['msg']

    def test_modify_groupnet(self, groupnet_module_mock):
        self.groupnet_args.update({'dns_servers': ['1.1.1.1', '1.1.1.2'],
                                   'description': 'Test desc', 'dns_server_state': "add",
                                   'new_groupnet_name': 'groupnet_new',
                                   'dns_search_suffix': ['test.com'],
                                   'dns_search_suffix_state': "remove"})
        groupnet_module_mock.module.params = self.groupnet_args
        groupnet_module_mock.get_groupnet_details \
            = MagicMock(return_value=MockGroupnetApi.get_groupnet_details(self.groupnet_name)
                        ['groupnets'][0])
        groupnet_module_mock.network_api.update_network_groupnet = MagicMock(return_value=None)
        groupnet_module_mock.perform_module_operation()

        assert groupnet_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert groupnet_module_mock.module.exit_json.call_args[1]["modify_groupnet"] is True

    def test_modify_groupnet_throws_exception(self, groupnet_module_mock):
        self.groupnet_args.update({'dns_servers': ['1.1.1.1', '1.1.1.2'],
                                   'dns_server_state': "add",
                                   'dns_search_suffix': ['test.com'],
                                   'dns_search_suffix_state': "remove"})
        groupnet_module_mock.module.params = self.groupnet_args
        groupnet_module_mock.get_groupnet_details \
            = MagicMock(return_value=MockGroupnetApi.get_groupnet_details(self.groupnet_name)
                        ['groupnets'][0])
        groupnet_module_mock.network_api.update_network_groupnet \
            = MagicMock(side_effect=utils.ApiException)
        groupnet_module_mock.perform_module_operation()

        assert MockGroupnetApi.modify_groupnet_ex_msg(self.groupnet_name) in \
            groupnet_module_mock.module.fail_json.call_args[1]['msg']

    def test_delete_groupnet(self, groupnet_module_mock):
        self.groupnet_args.update({'state': 'absent'})
        groupnet_module_mock.module.params = self.groupnet_args
        groupnet_module_mock.get_groupnet_details \
            = MagicMock(return_value=MockGroupnetApi.get_groupnet_details(self.groupnet_name)
                        ['groupnets'][0])
        groupnet_module_mock.network_api.delete_network_groupnet = MagicMock(return_value=None)
        groupnet_module_mock.perform_module_operation()

        assert groupnet_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert groupnet_module_mock.module.exit_json.call_args[1]['delete_groupnet'] is True

    def test_delete_groupnet_throws_exception(self, groupnet_module_mock):
        self.groupnet_args.update({'state': 'absent'})
        groupnet_module_mock.module.params = self.groupnet_args
        groupnet_module_mock.get_groupnet_details \
            = MagicMock(return_value=MockGroupnetApi.get_groupnet_details(self.groupnet_name)
                        ['groupnets'][0])
        groupnet_module_mock.network_api.delete_network_groupnet \
            = MagicMock(side_effect=utils.ApiException)
        groupnet_module_mock.perform_module_operation()

        assert MockGroupnetApi.delete_groupnet_ex_msg(self.groupnet_name) in \
            groupnet_module_mock.module.fail_json.call_args[1]['msg']
