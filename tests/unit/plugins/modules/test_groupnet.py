# Copyright: (c) 2021-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for groupnets module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import patch, MagicMock
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.groupnet import Groupnet
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils \
    import mock_groupnet_api as MockGroupnetApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils \
    import test_utils
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase


class TestGroupnet(PowerScaleUnitBase):
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'
    groupnet_name = 'groupnet_test'
    groupnet_args = {'groupnet_name': groupnet_name, 'state': 'present',
                     'description': None, 'dns_servers': [],
                     'dns_server_state': None, 'dns_search_suffix': None,
                     'dns_search_suffix_state': None, 'new_groupnet_name': None}

    @pytest.fixture
    def module_object(self, mocker):
        return Groupnet

    def test_invalid_groupnet_name(self, powerscale_module_mock):
        groupnet_name = 'groupnet_test_**()'
        self.groupnet_args.update({'groupnet_name': groupnet_name})
        powerscale_module_mock.module.params = self.groupnet_args
        self.capture_fail_json_call(MockGroupnetApi.get_invalid_groupnet(), invoke_perform_module=True)

    def test_invalid_groupnet_name_len(self, powerscale_module_mock):
        groupnet_name = 'groupnet_test_groupnet_test_groupnet_test_'
        self.groupnet_args.update({'groupnet_name': groupnet_name})
        powerscale_module_mock.module.params = self.groupnet_args
        self.capture_fail_json_call(MockGroupnetApi.get_invalid_groupnet_len(), invoke_perform_module=True)

    def test_invalid_dns_servers(self, powerscale_module_mock):
        self.groupnet_args.update({'dns_servers': ['a.2.2.2'],
                                   'dns_server_state': 'remove'})
        powerscale_module_mock.module.params = self.groupnet_args
        self.capture_fail_json_call(MockGroupnetApi.get_invalid_dns(), invoke_perform_module=True)

    def test_invalid_description(self, powerscale_module_mock):
        self.groupnet_args.update({'description': test_utils.get_desc(129)})
        powerscale_module_mock.module.params = self.groupnet_args
        self.capture_fail_json_call(MockGroupnetApi.get_invalid_desc(), invoke_perform_module=True)

    def test_get_groupnet_details(self, powerscale_module_mock):
        powerscale_module_mock.module.params = self.groupnet_args
        powerscale_module_mock.network_api.get_network_groupnet(self.groupnet_name).to_dict \
            = MagicMock(return_value=MockGroupnetApi.get_groupnet_details(self.groupnet_name))
        powerscale_module_mock.perform_module_operation()

        assert (MockGroupnetApi.get_groupnet_details('groupnet_test')['groupnets'][0]
                == powerscale_module_mock.module.exit_json.call_args[1]["groupnet_details"])
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is False

    def test_get_groupnet_throws_generic_exception(self, powerscale_module_mock):
        powerscale_module_mock.module.params = self.groupnet_args
        powerscale_module_mock.network_api.get_network_groupnet \
            = MagicMock(side_effect=Exception)
        self.capture_fail_json_call(MockGroupnetApi.get_groupnet_ex_msg(self.groupnet_name), invoke_perform_module=True)

    def test_get_groupnet_throws_utils_exception(self, powerscale_module_mock):
        powerscale_module_mock.module.params = self.groupnet_args
        powerscale_module_mock.network_api.get_network_groupnet \
            = MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockGroupnetApi.get_groupnet_ex_msg(self.groupnet_name), invoke_perform_module=True)

    def test_get_groupnet_404_error(self, powerscale_module_mock):
        powerscale_module_mock.module.params = self.groupnet_args
        with patch.object(powerscale_module_mock.network_api,
                          'get_network_groupnet',
                          side_effect=MockApiException(404)):
            powerscale_module_mock.perform_module_operation()
            assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
            assert powerscale_module_mock.module.exit_json.call_args[1]["create_groupnet"] is True

    def test_create_groupnet(self, powerscale_module_mock):
        groupnet_name = 'new_groupnet'
        self.groupnet_args.update({'groupnet_name': groupnet_name,
                                   'dns_servers': ['1.1.1.1', '1.1.1.2'],
                                   'description': 'Test Groupnet', 'dns_server_state': "add",
                                   'dns_search_suffix': ['ansibleneo.com', 'test.com'],
                                   'dns_search_suffix_state': "add"})
        powerscale_module_mock.module.params = self.groupnet_args
        powerscale_module_mock.get_groupnet_details \
            = MagicMock(return_value=MockGroupnetApi.get_groupnet_details(groupnet_name))
        powerscale_module_mock.network_api.create_network_groupnet = MagicMock(return_value=None)
        powerscale_module_mock.perform_module_operation()

        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert powerscale_module_mock.module.exit_json.call_args[1]["create_groupnet"] is True

    def test_create_groupnet_throws_exception(self, powerscale_module_mock):
        groupnet_name = 'new_groupnet'
        self.groupnet_args.update({'groupnet_name': groupnet_name,
                                   'dns_servers': ['1.1.1.1', '1.1.1.2'],
                                   'dns_server_state': "add",
                                   'dns_search_suffix': ['ansibleneo.com', 'test.com'],
                                   'dns_search_suffix_state': "add"})
        powerscale_module_mock.module.params = self.groupnet_args
        powerscale_module_mock.get_groupnet_details \
            = MagicMock(return_value=MockGroupnetApi.get_groupnet_details(groupnet_name))
        powerscale_module_mock.network_api.create_network_groupnet \
            = MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockGroupnetApi.create_groupnet_ex_msg(groupnet_name),
                                    invoke_perform_module=True)

    def test_modify_groupnet(self, powerscale_module_mock):
        self.groupnet_args.update({'dns_servers': ['1.1.1.1', '1.1.1.2'],
                                   'description': 'Test desc', 'dns_server_state': "add",
                                   'new_groupnet_name': 'groupnet_new',
                                   'dns_search_suffix': ['test.com'],
                                   'dns_search_suffix_state': "remove"})
        powerscale_module_mock.module.params = self.groupnet_args
        powerscale_module_mock.get_groupnet_details \
            = MagicMock(return_value=MockGroupnetApi.get_groupnet_details(self.groupnet_name)
                        ['groupnets'][0])
        powerscale_module_mock.network_api.update_network_groupnet = MagicMock(return_value=None)
        powerscale_module_mock.perform_module_operation()

        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert powerscale_module_mock.module.exit_json.call_args[1]["modify_groupnet"] is True

    def test_modify_groupnet_throws_exception(self, powerscale_module_mock):
        self.groupnet_args.update({'dns_servers': ['1.1.1.1', '1.1.1.2'],
                                   'dns_server_state': "add",
                                   'dns_search_suffix': ['test.com'],
                                   'dns_search_suffix_state': "remove"})
        powerscale_module_mock.module.params = self.groupnet_args
        powerscale_module_mock.get_groupnet_details \
            = MagicMock(return_value=MockGroupnetApi.get_groupnet_details(self.groupnet_name)
                        ['groupnets'][0])
        powerscale_module_mock.network_api.update_network_groupnet \
            = MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockGroupnetApi.modify_groupnet_ex_msg(self.groupnet_name),
                                    invoke_perform_module=True)

    def test_delete_groupnet(self, powerscale_module_mock):
        self.groupnet_args.update({'state': 'absent'})
        powerscale_module_mock.module.params = self.groupnet_args
        powerscale_module_mock.get_groupnet_details \
            = MagicMock(return_value=MockGroupnetApi.get_groupnet_details(self.groupnet_name)
                        ['groupnets'][0])
        powerscale_module_mock.network_api.delete_network_groupnet = MagicMock(return_value=None)
        powerscale_module_mock.perform_module_operation()

        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert powerscale_module_mock.module.exit_json.call_args[1]['delete_groupnet'] is True

    def test_delete_groupnet_throws_exception(self, powerscale_module_mock):
        self.groupnet_args.update({'state': 'absent'})
        powerscale_module_mock.module.params = self.groupnet_args
        powerscale_module_mock.get_groupnet_details \
            = MagicMock(return_value=MockGroupnetApi.get_groupnet_details(self.groupnet_name)
                        ['groupnets'][0])
        powerscale_module_mock.network_api.delete_network_groupnet \
            = MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockGroupnetApi.delete_groupnet_ex_msg(self.groupnet_name),
                                    invoke_perform_module=True)
