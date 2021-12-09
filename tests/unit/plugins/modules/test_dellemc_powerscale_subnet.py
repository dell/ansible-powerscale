# Copyright: (c) 2021, DellEMC

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for subnets module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import dellemc_ansible_powerscale_utils as utils

utils.get_logger = MagicMock()
utils.isi_sdk = MagicMock()
from ansible.module_utils import basic
basic.AnsibleModule = MagicMock()

from ansible_collections.dellemc.powerscale.plugins.modules.dellemc_powerscale_subnet import PowerScaleSubnet
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils \
    import mock_subnet_api as MockSubnetApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils \
    import test_utils


class TestPowerScaleSubnet():
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.dellemc_ansible_powerscale_utils'
    subnet_name = 'subnet_test'
    groupnet_name = 'groupnet_test'
    subnet_args = {'subnet_name': subnet_name, 'groupnet_name': groupnet_name,
                   'state': 'present', 'netmask': None, 'description': None,
                   'gateway_priority': None, 'new_subnet_name': None,
                   'subnet_params': {'gateway': None, 'vlan_id': None, 'mtu': None,
                                     'vlan_enabled': None, 'sc_service_addrs': [],
                                     'sc_service_addrs_state': None}}

    @pytest.fixture
    def subnet_module_mock(self, mocker):
        mocker.patch(self.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        subnet_module_mock = PowerScaleSubnet()
        return subnet_module_mock

    def test_invalid_subnet_name(self, subnet_module_mock):
        subnet_name = 'subnet_test_*()'
        self.subnet_args.update({'subnet_name': subnet_name})
        subnet_module_mock.module.params = self.subnet_args
        subnet_module_mock.perform_module_operation()

        assert subnet_module_mock.module.fail_json.call_args[1]['msg'] \
            == MockSubnetApi.get_invalid_subnet()

    def test_invalid_netmask(self, subnet_module_mock):
        self.subnet_args.update({'netmask': '102.33333333333.22.1'})
        subnet_module_mock.module.params = self.subnet_args
        subnet_module_mock.perform_module_operation()

        assert subnet_module_mock.module.fail_json.call_args[1]['msg'] \
            == MockSubnetApi.get_invalid_netmask()

    def test_invalid_gateway_priority(self, subnet_module_mock):
        self.subnet_args.update({'gateway_priority': -1})
        subnet_module_mock.module.params = self.subnet_args
        subnet_module_mock.perform_module_operation()

        assert subnet_module_mock.module.fail_json.call_args[1]['msg'] \
            == MockSubnetApi.get_invalid_gateway_priority()

    def test_invalid_subnet_nameLen(self, subnet_module_mock):
        subnet_name = 'subnet_test_subnet_test_subnet_test_'
        self.subnet_args.update({'subnet_name': subnet_name})
        subnet_module_mock.module.params = self.subnet_args
        subnet_module_mock.perform_module_operation()

        assert subnet_module_mock.module.fail_json.call_args[1]['msg'] \
            == MockSubnetApi.get_invalid_len()

    def test_invalid_subnet_desc(self, subnet_module_mock):
        self.subnet_args.update({'description': test_utils.get_desc(129)})
        subnet_module_mock.module.params = self.subnet_args
        subnet_module_mock.perform_module_operation()

        assert subnet_module_mock.module.fail_json.call_args[1]['msg'] \
            == MockSubnetApi.get_invalid_desc()

    def test_invalid_mtu(self, subnet_module_mock):
        self.subnet_args.update({'subnet_params':
                                {'gateway': None, 'vlan_id': None, 'mtu': 575,
                                 'vlan_enabled': None, 'sc_service_addrs': [],
                                 'sc_service_addrs_state': None}})
        subnet_module_mock.module.params = self.subnet_args
        subnet_module_mock.perform_module_operation()

        assert subnet_module_mock.module.fail_json.call_args[1]['msg'] \
            == MockSubnetApi.get_invalid_mtu()

    def test_get_subnet_details(self, subnet_module_mock):
        subnet_module_mock.module.params = self.subnet_args
        subnet_module_mock.groupnet_api.get_groupnet_subnet(self.subnet_name).to_dict \
            = MagicMock(return_value=MockSubnetApi.get_subnet_details(self.subnet_name))
        subnet_module_mock.perform_module_operation()

        assert (MockSubnetApi.get_subnet_details(self.subnet_name)['subnets'][0]
                == subnet_module_mock.module.exit_json.call_args[1]["subnet_details"])
        assert subnet_module_mock.module.exit_json.call_args[1]["changed"] is False

    def test_get_subnet_throws_generic_exception(self, subnet_module_mock):
        subnet_module_mock.module.params = self.subnet_args
        subnet_module_mock.groupnet_api.get_groupnet_subnet \
            = MagicMock(side_effect=Exception)
        subnet_module_mock.perform_module_operation()

        assert MockSubnetApi.get_subnet_ex_msg(self.subnet_name) in \
            subnet_module_mock.module.fail_json.call_args[1]['msg']

    def test_get_subnet_throws_exception(self, subnet_module_mock):
        subnet_module_mock.module.params = self.subnet_args
        subnet_module_mock.groupnet_api.get_groupnet_subnet \
            = MagicMock(side_effect=utils.ApiException)
        subnet_module_mock.perform_module_operation()

        assert MockSubnetApi.get_subnet_ex_msg(self.subnet_name) in \
            subnet_module_mock.module.fail_json.call_args[1]['msg']

    def test_get_subnet_404_error(self, subnet_module_mock):
        MockApiException.status = '404'
        subnet_module_mock.module.params = self.subnet_args
        subnet_module_mock.groupnet_api.get_groupnet_subnet(self.subnet_name).to_dict \
            = MagicMock(side_effect=utils.ApiException)
        subnet_module_mock.perform_module_operation()

        assert subnet_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert subnet_module_mock.module.exit_json.call_args[1]["create_subnet"] is True

    def test_create_subnet_details(self, subnet_module_mock):
        subnet_name = 'new_subnet'
        self.subnet_args.update({'netmask': '1.1.1.1', 'gateway_priority': 1,
                                 'subnet_params':
                                 {'gateway': None, 'vlan_id': 5, 'mtu': None,
                                  'vlan_enabled': True, 'sc_service_addrs':
                                  [{'start_range': '1.1.1.1', 'end_range': '1.1.1.2'},
                                   {'start_range': '1.1.1.3', 'end_range': '1.1.1.4'}],
                                  'sc_service_addrs_state': 'add'}})

        subnet_module_mock.module.params = self.subnet_args
        subnet_module_mock.get_subnet_details \
            = MagicMock(return_value=MockSubnetApi.get_subnet_details(subnet_name))
        subnet_module_mock.groupnet_api.create_groupnet_subnet = MagicMock(return_value=None)
        subnet_module_mock.perform_module_operation()

        assert subnet_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert subnet_module_mock.module.exit_json.call_args[1]["create_subnet"] is True

    def test_create_subnet_throws_exception(self, subnet_module_mock):
        subnet_name = 'new_subnet'
        self.subnet_args.update({'subnet_name': subnet_name,
                                 'netmask': '1.1.1.1', 'gateway_priority': 1})
        subnet_module_mock.module.params = self.subnet_args
        subnet_module_mock.get_subnet_details \
            = MagicMock(return_value=None)
        subnet_module_mock.groupnet_api.create_groupnet_subnet \
            = MagicMock(side_effect=utils.ApiException)
        subnet_module_mock.perform_module_operation()

        assert MockSubnetApi.create_subnet_ex_msg(subnet_name) in \
            subnet_module_mock.module.fail_json.call_args[1]['msg']

    def test_modify_subnet_details_remove_sc_ips(self, subnet_module_mock):
        self.subnet_args.update({'netmask': '1.1.1.1', 'gateway_priority': 1,
                                 'new_subnet_name': 'subnet_new',
                                 'subnet_params':
                                 {'gateway': None, 'vlan_id': 3, 'mtu': None,
                                  'vlan_enabled': True, 'sc_service_addrs':
                                  [{'start_range': '1.1.1.1', 'end_range': '1.1.1.2'}],
                                  'sc_service_addrs_state': 'remove'}})

        subnet_module_mock.module.params = self.subnet_args
        subnet_module_mock.get_subnet_details \
            = MagicMock(return_value=MockSubnetApi.get_subnet_details(self.subnet_name)['subnets'][0])
        subnet_module_mock.groupnet_api.update_groupnet_subnet = MagicMock(return_value=None)
        subnet_module_mock.perform_module_operation()

        assert subnet_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert subnet_module_mock.module.exit_json.call_args[1]["modify_subnet"] is True

    def test_modify_subnet_add_sc_ips(self, subnet_module_mock):
        self.subnet_args.update({'netmask': '1.1.1.1', 'gateway_priority': 1,
                                 'subnet_params':
                                 {'gateway': None, 'vlan_id': None, 'mtu': None,
                                  'vlan_enabled': False, 'sc_service_addrs':
                                  [{'start_range': '1.1.1.1', 'end_range': '1.1.1.2'}],
                                  'sc_service_addrs_state': 'add'}})

        subnet_module_mock.module.params = self.subnet_args
        subnet_module_mock.get_subnet_details \
            = MagicMock(return_value=MockSubnetApi.get_subnet_details(self.subnet_name)['subnets'][0])
        subnet_module_mock.groupnet_api.update_groupnet_subnet = MagicMock(return_value=None)
        subnet_module_mock.perform_module_operation()

        assert subnet_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert subnet_module_mock.module.exit_json.call_args[1]["modify_subnet"] is True

    def test_modify_subnet_throws_exception(self, subnet_module_mock):
        self.subnet_args.update({'gateway_priority': 5})

        subnet_module_mock.module.params = self.subnet_args
        subnet_module_mock.get_subnet_details \
            = MagicMock(return_value=MockSubnetApi.get_subnet_details(self.subnet_name)['subnets'][0])
        subnet_module_mock.groupnet_api.update_groupnet_subnet \
            = MagicMock(side_effect=utils.ApiException)
        subnet_module_mock.perform_module_operation()

        assert MockSubnetApi.modify_subnet_ex_msg(self.subnet_name) in \
            subnet_module_mock.module.fail_json.call_args[1]['msg']

    def test_modify_subnet_invalid_gateway(self, subnet_module_mock):
        self.subnet_args.update({'subnet_params':
                                {'gateway': 'a.1.1.1', 'vlan_id': None, 'mtu': None,
                                 'vlan_enabled': None, 'sc_service_addrs': [],
                                 'sc_service_addrs_state': None}})

        subnet_module_mock.module.params = self.subnet_args
        subnet_module_mock.get_subnet_details \
            = MagicMock(return_value=MockSubnetApi.get_subnet_details(self.subnet_name)['subnets'][0])
        subnet_module_mock.groupnet_api.update_groupnet_subnet = MagicMock(return_value=None)
        subnet_module_mock.perform_module_operation()

        assert MockSubnetApi.get_invalid_gateway() in \
            subnet_module_mock.module.fail_json.call_args[1]['msg']

    def test_modify_subnet_invalid_vlan_id(self, subnet_module_mock):
        self.subnet_args.update({'subnet_params':
                                {'gateway': 'a.1.1.1', 'vlan_id': -1, 'mtu': None,
                                 'vlan_enabled': True, 'sc_service_addrs': [],
                                 'sc_service_addrs_state': None}})

        subnet_module_mock.module.params = self.subnet_args
        subnet_module_mock.get_subnet_details \
            = MagicMock(return_value=MockSubnetApi.get_subnet_details(self.subnet_name)['subnets'][0])
        subnet_module_mock.groupnet_api.update_groupnet_subnet = MagicMock(return_value=None)
        subnet_module_mock.perform_module_operation()

        assert MockSubnetApi.get_invalid_vlan_id() in \
            subnet_module_mock.module.fail_json.call_args[1]['msg']

    def test_modify_subnet_invalid_sc_ip(self, subnet_module_mock):
        self.subnet_args.update({'subnet_params':
                                {'gateway': 'a.1.1.1', 'vlan_id': None, 'mtu': None,
                                 'vlan_enabled': None,
                                 'sc_service_addrs':
                                 [{'start_range': 'a.1.1.1', 'end_range': '1.1.1.2'}],
                                 'sc_service_addrs_state': 'add'}})

        subnet_module_mock.module.params = self.subnet_args
        subnet_module_mock.get_subnet_details \
            = MagicMock(return_value=MockSubnetApi.get_subnet_details(self.subnet_name)['subnets'][0])
        subnet_module_mock.groupnet_api.update_groupnet_subnet = MagicMock(return_value=None)
        subnet_module_mock.perform_module_operation()
        assert MockSubnetApi.get_invalid_sc_ip() in \
            subnet_module_mock.module.fail_json.call_args[1]['msg']

    def test_delete_subnet_details(self, subnet_module_mock):
        self.subnet_args.update({'state': 'absent'})
        subnet_module_mock.module.params = self.subnet_args
        subnet_module_mock.get_subnet_details \
            = MagicMock(return_value=MockSubnetApi.get_subnet_details(self.subnet_name)['subnets'][0])
        subnet_module_mock.groupnet_api.delete_groupnet_subnet = MagicMock(return_value=None)
        subnet_module_mock.perform_module_operation()

        assert subnet_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert subnet_module_mock.module.exit_json.call_args[1]["delete_subnet"] is True

    def test_delete_subnet_throws_exception(self, subnet_module_mock):
        self.subnet_args.update({'state': 'absent'})
        subnet_module_mock.module.params = self.subnet_args
        subnet_module_mock.get_subnet_details \
            = MagicMock(return_value=MockSubnetApi.get_subnet_details(self.subnet_name)['subnets'][0])
        subnet_module_mock.groupnet_api.delete_groupnet_subnet \
            = MagicMock(side_effect=utils.ApiException)
        subnet_module_mock.perform_module_operation()

        assert MockSubnetApi.delete_subnet_ex_msg(self.subnet_name) in \
            subnet_module_mock.module.fail_json.call_args[1]['msg']
