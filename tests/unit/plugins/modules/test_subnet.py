# Copyright: (c) 2021-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for subnets module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.subnet import Subnet
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils \
    import mock_subnet_api as MockSubnetApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils \
    import test_utils
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase


class TestSubnet(PowerScaleUnitBase):
    subnet_name = 'subnet_test'
    groupnet_name = 'groupnet_test'
    subnet_args = {'subnet_name': subnet_name, 'groupnet_name': groupnet_name,
                   'state': 'present', 'netmask': None, 'description': None,
                   'gateway_priority': None, 'new_subnet_name': None,
                   'subnet_params': {'gateway': None, 'vlan_id': None, 'mtu': None,
                                     'vlan_enabled': None, 'sc_service_addrs': [],
                                     'sc_service_addrs_state': None}}

    @pytest.fixture
    def module_object(self, mocker):
        return Subnet

    def test_invalid_subnet_name_exception(self, powerscale_module_mock):
        subnet_name = 'subnet_test_*()'
        self.subnet_args.update({'subnet_name': subnet_name})
        powerscale_module_mock.module.params = self.subnet_args
        self.capture_fail_json_call(MockSubnetApi.get_invalid_subnet(), invoke_perform_module=True)

    def test_invalid_netmask_exception(self, powerscale_module_mock):
        self.subnet_args.update({'netmask': '102.33333333333.22.1'})
        powerscale_module_mock.module.params = self.subnet_args
        self.capture_fail_json_call(MockSubnetApi.get_invalid_netmask(), invoke_perform_module=True)

    def test_invalid_gateway_priority_exception(self, powerscale_module_mock):
        self.subnet_args.update({'gateway_priority': -1})
        powerscale_module_mock.module.params = self.subnet_args
        self.capture_fail_json_call(MockSubnetApi.get_invalid_gateway_priority(), invoke_perform_module=True)

    def test_invalid_subnet_name_len_exception(self, powerscale_module_mock):
        subnet_name = 'subnet_test_subnet_test_subnet_test_'
        self.subnet_args.update({'subnet_name': subnet_name})
        powerscale_module_mock.module.params = self.subnet_args
        self.capture_fail_json_call(MockSubnetApi.get_invalid_len(), invoke_perform_module=True)

    def test_invalid_subnet_desc_exception(self, powerscale_module_mock):
        self.subnet_args.update({'description': test_utils.get_desc(129)})
        powerscale_module_mock.module.params = self.subnet_args
        self.capture_fail_json_call(MockSubnetApi.get_invalid_desc(), invoke_perform_module=True)

    def test_invalid_mtu_exception(self, powerscale_module_mock):
        self.subnet_args.update({'subnet_params':
                                {'gateway': None, 'vlan_id': None, 'mtu': 575,
                                 'vlan_enabled': None, 'sc_service_addrs': [],
                                 'sc_service_addrs_state': None}})
        powerscale_module_mock.module.params = self.subnet_args
        self.capture_fail_json_call(MockSubnetApi.get_invalid_mtu(), invoke_perform_module=True)

    def test_get_subnet_details(self, powerscale_module_mock):
        powerscale_module_mock.module.params = self.subnet_args
        powerscale_module_mock.groupnet_api.get_groupnet_subnet(self.subnet_name).to_dict \
            = MagicMock(return_value=MockSubnetApi.get_subnet_details(self.subnet_name))
        powerscale_module_mock.perform_module_operation()

        assert (MockSubnetApi.get_subnet_details(self.subnet_name)['subnets'][0]
                == powerscale_module_mock.module.exit_json.call_args[1]["subnet_details"])
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is False

    def test_get_subnet_throws_generic_exception(self, powerscale_module_mock):
        powerscale_module_mock.module.params = self.subnet_args
        powerscale_module_mock.groupnet_api.get_groupnet_subnet \
            = MagicMock(side_effect=Exception)
        self.capture_fail_json_call(MockSubnetApi.get_subnet_ex_msg(self.subnet_name), invoke_perform_module=True)

    def test_get_subnet_throws_exception(self, powerscale_module_mock):
        powerscale_module_mock.module.params = self.subnet_args
        powerscale_module_mock.groupnet_api.get_groupnet_subnet \
            = MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockSubnetApi.get_subnet_ex_msg(self.subnet_name), invoke_perform_module=True)

    def test_get_subnet_404_error(self, powerscale_module_mock):
        self.subnet_args.update({'netmask': '255.255.0.0', 'gateway_priority': 1,
                                 'subnet_params':
                                     {'gateway': None, 'vlan_id': 5, 'mtu': None,
                                      'vlan_enabled': True, 'sc_service_addrs':
                                          [{'start_range': '1.1.1.1', 'end_range': '1.1.1.2'},
                                           {'start_range': '1.1.1.3', 'end_range': '1.1.1.4'}],
                                      'sc_service_addrs_state': 'add'}})
        powerscale_module_mock.module.params = self.subnet_args
        powerscale_module_mock.groupnet_api.get_groupnet_subnet(self.subnet_name).to_dict \
            = MagicMock(side_effect=MockApiException(404))
        powerscale_module_mock.perform_module_operation()

        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert powerscale_module_mock.module.exit_json.call_args[1]["create_subnet"] is True

    def test_create_subnet_details(self, powerscale_module_mock):
        subnet_name = 'new_subnet'
        self.subnet_args.update({'netmask': '255.255.0.0', 'gateway_priority': 1,
                                 'subnet_params':
                                 {'gateway': None, 'vlan_id': 5, 'mtu': None,
                                  'vlan_enabled': True, 'sc_service_addrs':
                                  [{'start_range': '1.1.1.1', 'end_range': '1.1.1.2'},
                                   {'start_range': '1.1.1.3', 'end_range': '1.1.1.4'}],
                                  'sc_service_addrs_state': 'add'}})

        powerscale_module_mock.module.params = self.subnet_args
        powerscale_module_mock.get_subnet_details \
            = MagicMock(return_value=MockSubnetApi.get_subnet_details(subnet_name))
        powerscale_module_mock.groupnet_api.create_groupnet_subnet = MagicMock(return_value=None)
        powerscale_module_mock.perform_module_operation()

        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert powerscale_module_mock.module.exit_json.call_args[1]["create_subnet"] is True

    def test_create_subnet_throws_exception(self, powerscale_module_mock):
        subnet_name = 'new_subnet'
        self.subnet_args.update({'subnet_name': subnet_name,
                                 'netmask': '255.255.0.0', 'gateway_priority': 1})
        powerscale_module_mock.module.params = self.subnet_args
        powerscale_module_mock.get_subnet_details \
            = MagicMock(return_value=None)
        powerscale_module_mock.groupnet_api.create_groupnet_subnet \
            = MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockSubnetApi.create_subnet_ex_msg(subnet_name), invoke_perform_module=True)

    def test_modify_subnet_details_remove_sc_ips(self, powerscale_module_mock):
        self.subnet_args.update({'netmask': '255.255.0.0', 'gateway_priority': 1,
                                 'new_subnet_name': 'subnet_new',
                                 'subnet_params':
                                 {'gateway': None, 'vlan_id': 3, 'mtu': None,
                                  'vlan_enabled': True, 'sc_service_addrs':
                                  [{'start_range': '1.1.1.1', 'end_range': '1.1.1.2'}],
                                  'sc_service_addrs_state': 'remove'}})

        powerscale_module_mock.module.params = self.subnet_args
        powerscale_module_mock.get_subnet_details \
            = MagicMock(return_value=MockSubnetApi.get_subnet_details(self.subnet_name)['subnets'][0])
        powerscale_module_mock.groupnet_api.update_groupnet_subnet = MagicMock(return_value=None)
        powerscale_module_mock.perform_module_operation()

        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert powerscale_module_mock.module.exit_json.call_args[1]["modify_subnet"] is True

    def test_modify_subnet_add_sc_ips(self, powerscale_module_mock):
        self.subnet_args.update({'netmask': '255.255.0.0', 'gateway_priority': 1,
                                 'subnet_params':
                                 {'gateway': None, 'vlan_id': None, 'mtu': None,
                                  'vlan_enabled': False, 'sc_service_addrs':
                                  [{'start_range': '1.1.1.1', 'end_range': '1.1.1.2'}],
                                  'sc_service_addrs_state': 'add'}})

        powerscale_module_mock.module.params = self.subnet_args
        powerscale_module_mock.get_subnet_details \
            = MagicMock(return_value=MockSubnetApi.get_subnet_details(self.subnet_name)['subnets'][0])
        powerscale_module_mock.groupnet_api.update_groupnet_subnet = MagicMock(return_value=None)
        powerscale_module_mock.perform_module_operation()

        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert powerscale_module_mock.module.exit_json.call_args[1]["modify_subnet"] is True

    def test_modify_subnet_throws_exception(self, powerscale_module_mock):
        self.subnet_args.update({'gateway_priority': 5})

        powerscale_module_mock.module.params = self.subnet_args
        powerscale_module_mock.get_subnet_details \
            = MagicMock(return_value=MockSubnetApi.get_subnet_details(self.subnet_name)['subnets'][0])
        powerscale_module_mock.groupnet_api.update_groupnet_subnet \
            = MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockSubnetApi.modify_subnet_ex_msg(self.subnet_name), invoke_perform_module=True)

    def test_modify_subnet_invalid_gateway_exception(self, powerscale_module_mock):
        self.subnet_args.update({'subnet_params':
                                {'gateway': 'a.1.1.1', 'vlan_id': None, 'mtu': None,
                                 'vlan_enabled': None, 'sc_service_addrs': [],
                                 'sc_service_addrs_state': None}})

        powerscale_module_mock.module.params = self.subnet_args
        powerscale_module_mock.get_subnet_details \
            = MagicMock(return_value=MockSubnetApi.get_subnet_details(self.subnet_name)['subnets'][0])
        powerscale_module_mock.groupnet_api.update_groupnet_subnet = MagicMock(return_value=None)
        self.capture_fail_json_call(MockSubnetApi.get_invalid_gateway(), invoke_perform_module=True)

    def test_modify_subnet_invalid_vlan_id_exception(self, powerscale_module_mock):
        self.subnet_args.update({'subnet_params':
                                {'gateway': '1.1.1.1', 'vlan_id': -1, 'mtu': None,
                                 'vlan_enabled': True, 'sc_service_addrs': [],
                                 'sc_service_addrs_state': None}})

        powerscale_module_mock.module.params = self.subnet_args
        powerscale_module_mock.get_subnet_details \
            = MagicMock(return_value=MockSubnetApi.get_subnet_details(self.subnet_name)['subnets'][0])
        powerscale_module_mock.groupnet_api.update_groupnet_subnet = MagicMock(return_value=None)
        self.capture_fail_json_call(MockSubnetApi.get_invalid_vlan_id(), invoke_perform_module=True)

    def test_modify_subnet_invalid_sc_ip_exception(self, powerscale_module_mock):
        self.subnet_args.update({'subnet_params':
                                {'gateway': '1.1.1.1', 'vlan_id': None, 'mtu': None,
                                 'vlan_enabled': None,
                                 'sc_service_addrs':
                                 [{'start_range': 'a.1.1.1', 'end_range': '1.1.1.2'}],
                                 'sc_service_addrs_state': 'add'}})

        powerscale_module_mock.module.params = self.subnet_args
        powerscale_module_mock.get_subnet_details \
            = MagicMock(return_value=MockSubnetApi.get_subnet_details(self.subnet_name)['subnets'][0])
        powerscale_module_mock.groupnet_api.update_groupnet_subnet = MagicMock(return_value=None)
        self.capture_fail_json_call(MockSubnetApi.get_invalid_sc_ip(), invoke_perform_module=True)

    def test_delete_subnet_details(self, powerscale_module_mock):
        self.subnet_args.update({'state': 'absent'})
        powerscale_module_mock.module.params = self.subnet_args
        powerscale_module_mock.get_subnet_details \
            = MagicMock(return_value=MockSubnetApi.get_subnet_details(self.subnet_name)['subnets'][0])
        powerscale_module_mock.groupnet_api.delete_groupnet_subnet = MagicMock(return_value=None)
        powerscale_module_mock.perform_module_operation()

        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert powerscale_module_mock.module.exit_json.call_args[1]["delete_subnet"] is True

    def test_delete_subnet_throws_exception(self, powerscale_module_mock):
        self.subnet_args.update({'state': 'absent'})
        powerscale_module_mock.module.params = self.subnet_args
        powerscale_module_mock.get_subnet_details \
            = MagicMock(return_value=MockSubnetApi.get_subnet_details(self.subnet_name)['subnets'][0])
        powerscale_module_mock.groupnet_api.delete_groupnet_subnet \
            = MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockSubnetApi.delete_subnet_ex_msg(self.subnet_name), invoke_perform_module=True)
