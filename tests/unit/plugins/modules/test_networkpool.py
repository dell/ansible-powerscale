# Copyright: (c) 2021-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Network pool module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library \
    import initial_mock
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.networkpool import NetworkPool, NetworkPoolHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_networkpool_api as MockNetworkPoolApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse

from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import PowerScaleUnitBase

class TestNetworkPool(PowerScaleUnitBase):
    get_network_pool_args = {
        "api_user": "user",
        "api_password": "password",
        "onefs_host": "10.10.10.10",
        "port_no": 8080,
        "verify_ssl": False,
        "groupnet_name": "groupnet0",
        "subnet_name": "subnet0",
        "pool_name": "Test_pool1",
        "state": None,
        "description": None,
        "access_zone": "ansible-neo",
        "new_pool_name": None,
        "additional_pool_params": {"ranges": [],
        "range_state": None,
        "ifaces": [],
        "iface_state": None},
        "sc_params": {
            "static_routes": [],
            "sc_dns_zone_aliases": []
            }
        }

    @pytest.fixture
    def module_object(self):
        return NetworkPool

    def test_get_network_pool(self, powerscale_module_mock):
        network_pool = MockNetworkPoolApi.GET_NETWORK_POOLS
        self.get_network_pool_args.update({"state": "present"})
        powerscale_module_mock.module.params = self.get_network_pool_args
        utils.get_network_pool_details = MagicMock(
            return_value=MockNetworkPoolApi.GET_NETWORK_POOLS)
        NetworkPoolHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False
        assert network_pool == powerscale_module_mock.module.exit_json.call_args[1]['network_pool']

    def test_get_network_pool_with_exception(self, powerscale_module_mock):
        MockNetworkPoolApi.GET_NETWORK_POOLS
        self.get_network_pool_args.update({"state": "present"})
        powerscale_module_mock.module.params = self.get_network_pool_args
        utils.get_network_pool_details = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(MockNetworkPoolApi.get_networkpool_failed_msg(
            MockNetworkPoolApi.GET_NETWORK_POOLS['pools'][0]['name']),
            powerscale_module_mock, NetworkPoolHandler)

    def common_create_pool_params(self, powerscale_module_mock):
        self.get_network_pool_args.update({"state": "present",
                                           "description": "Test_pool1",
                                           "additional_pool_params": {"ranges": [{"low": MockNetworkPoolApi.RANGE1,
                                                                                  "high": MockNetworkPoolApi.RANGE1}],
                                                                      "range_state": "add",
                                                                      "ifaces": [{"iface": "ext-1",
                                                                                  "lnn": 4}],
                                                                      "iface_state": "add"},
                                           "sc_params": {"sc_dns_zone": MockNetworkPoolApi.RANGE1,
                                                         "sc_connect_policy": "throughput",
                                                         "sc_failover_policy": "throughput",
                                                         "rebalance_policy": "auto",
                                                         "alloc_method": "dynamic",
                                                         "sc_auto_unsuspend_delay": 200,
                                                         "sc_ttl": 300,
                                                         "aggregation_mode": "lacp",
                                                         "sc_dns_zone_aliases": ["smartconn-zone"],
                                                         "sc_subnet": "subnet_test",
                                                         "static_routes": [{"gateway": MockNetworkPoolApi.RANGE1,
                                                                            "prefix_len": 4,
                                                                            "subnet": MockNetworkPoolApi.RANGE1,
                                                                            "route_state": "add"}]}})
        powerscale_module_mock.module.params = self.get_network_pool_args
        powerscale_module_mock.get_network_pool = MagicMock(return_value=None)

    def test_create_network_pool(self, powerscale_module_mock):
        self.common_create_pool_params(powerscale_module_mock)
        powerscale_module_mock.network_groupnet_api.create_subnets_subnet_pool = MagicMock(
            return_value=MockSDKResponse(MockNetworkPoolApi.CREATE_NETWORK_POOL))
        NetworkPoolHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.network_groupnet_api.create_subnets_subnet_pool.assert_called()

    def test_create_network_pool_with_exception(self, powerscale_module_mock):
        self.common_create_pool_params(powerscale_module_mock)
        powerscale_module_mock.network_groupnet_api.create_subnets_subnet_pool = MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNetworkPoolApi.create_networkpool_failed_msg(
            MockNetworkPoolApi.GET_NETWORK_POOLS['pools'][0]['name']),
            powerscale_module_mock, NetworkPoolHandler)

    def test_delete_network_pool(self, powerscale_module_mock):
        self.get_network_pool_args.update({"state": "absent"})
        powerscale_module_mock.module.params = self.get_network_pool_args
        utils.get_network_pool_details = MagicMock(
            return_value=MockNetworkPoolApi.GET_NETWORK_POOLS)
        powerscale_module_mock.network_groupnet_api.delete_subnets_subnet_pool = MagicMock(return_value=None)
        NetworkPoolHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert (powerscale_module_mock.module.exit_json.call_args[1]['changed'])
        powerscale_module_mock.network_groupnet_api.delete_subnets_subnet_pool.assert_called()

    def test_delete_network_pool_with_exception(self, powerscale_module_mock):
        self.get_network_pool_args.update({"state": "absent"})
        powerscale_module_mock.module.params = self.get_network_pool_args
        utils.get_network_pool_details = MagicMock(
            return_value=MockNetworkPoolApi.GET_NETWORK_POOLS)
        powerscale_module_mock.network_groupnet_api.delete_subnets_subnet_pool = MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNetworkPoolApi.delete_networkpool_failed_msg(
            MockNetworkPoolApi.GET_NETWORK_POOLS['pools'][0]['name']),
            powerscale_module_mock, NetworkPoolHandler)

    def common_modify_pool_params(self, powerscale_module_mock):
        self.get_network_pool_args.update({"state": "present",
                                           "description": "Test_pool2",
                                           "new_pool_name": "Test_pool2",
                                           "additional_pool_params": {"ranges": [{"low": MockNetworkPoolApi.RANGE1,
                                                                                  "high": MockNetworkPoolApi.RANGE1}],
                                                                      "range_state": "remove",
                                                                      "ifaces": [{"iface": "ext-2",
                                                                                  "lnn": 5}],
                                                                      "iface_state": "add"},
                                           "sc_params": {"sc_dns_zone": MockNetworkPoolApi.RANGE2,
                                                         "sc_connect_policy": "round_robin",
                                                         "sc_failover_policy": "round_robin",
                                                         "rebalance_policy": "manual",
                                                         "alloc_method": "static",
                                                         "sc_auto_unsuspend_delay": 100,
                                                         "sc_ttl": 200,
                                                         "aggregation_mode": "failover",
                                                         "sc_dns_zone_aliases": ["smartconn-zone2"],
                                                         "sc_subnet": "subnet_test2",
                                                         "static_routes": [{"gateway": MockNetworkPoolApi.RANGE1,
                                                                            "prefix_len": 4,
                                                                            "subnet": MockNetworkPoolApi.RANGE1,
                                                                            "route_state": "remove"},
                                                                           {"gateway": MockNetworkPoolApi.RANGE2,
                                                                            "prefix_len": 2,
                                                                            "subnet": MockNetworkPoolApi.RANGE2,
                                                                            "route_state": "add"}]}})
        powerscale_module_mock.module.params = self.get_network_pool_args
        utils.get_network_pool_details = MagicMock(
            return_value=MockNetworkPoolApi.CREATE_NETWORK_POOL)

    def test_modify_network_pool(self, powerscale_module_mock):
        self.common_modify_pool_params(powerscale_module_mock)
        powerscale_module_mock.network_groupnet_api.update_subnets_subnet_pool = MagicMock(return_value=None)
        NetworkPoolHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert (powerscale_module_mock.module.exit_json.call_args[1]['changed'])
        powerscale_module_mock.network_groupnet_api.update_subnets_subnet_pool.assert_called()

    def test_modify_network_pool_with_exception(self, powerscale_module_mock):
        self.common_modify_pool_params(powerscale_module_mock)
        powerscale_module_mock.network_groupnet_api.update_subnets_subnet_pool = MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockNetworkPoolApi.modify_networkpool_failed_msg(
            MockNetworkPoolApi.GET_NETWORK_POOLS['pools'][0]['name']),
            powerscale_module_mock, NetworkPoolHandler)

    def test_create_network_pool_with_blank_name(self, powerscale_module_mock):
        self.get_network_pool_args.update({"state": "present",
                                           "pool_name": ""})
        powerscale_module_mock.module.params = self.get_network_pool_args
        utils.get_network_pool_details = MagicMock(
            return_value=MockNetworkPoolApi.GET_NETWORK_POOLS)
        self.capture_fail_json_call(MockNetworkPoolApi.network_pool_failed_msg('invalid_pool_name'),
                                    powerscale_module_mock, NetworkPoolHandler)

    def test_modify_description_morethan_128(self, powerscale_module_mock):
        self.get_network_pool_args.update({"state": "present",
                                           "description": "a" * 129})
        powerscale_module_mock.module.params = self.get_network_pool_args
        utils.get_network_pool_details = MagicMock(
            return_value=MockNetworkPoolApi.GET_NETWORK_POOLS)
        self.capture_fail_json_call(MockNetworkPoolApi.network_pool_failed_msg('invalid_pool_description'),
                                    powerscale_module_mock, NetworkPoolHandler)

    def test_modify_invalid_ip_range(self, powerscale_module_mock):
        self.get_network_pool_args.update({"state": "present",
                                           "additional_pool_params": {"ranges": [{"low": "x.x.x.1",
                                                                                  "high": "x.x.x.*"}],
                                                                      "range_state": "add"}})
        powerscale_module_mock.module.params = self.get_network_pool_args
        utils.get_network_pool_details = MagicMock(
            return_value=MockNetworkPoolApi.GET_NETWORK_POOLS)
        self.capture_fail_json_call(MockNetworkPoolApi.network_pool_failed_msg('invalid_ip_range'),
                                    powerscale_module_mock, NetworkPoolHandler)

    def test_modify_invalid_iface(self, powerscale_module_mock):
        self.get_network_pool_args.update({"state": "present",
                                           "additional_pool_params": {"ifaces": [{"iface": "",
                                                                                  "lnn": ""}],
                                                                      "iface_state": "add"}})
        powerscale_module_mock.module.params = self.get_network_pool_args
        utils.get_network_pool_details = MagicMock(
            return_value=MockNetworkPoolApi.GET_NETWORK_POOLS)
        self.capture_fail_json_call(MockNetworkPoolApi.network_pool_failed_msg('invalid_iface'),
                                    powerscale_module_mock, NetworkPoolHandler)

    def test_modify_invalid_route(self, powerscale_module_mock):
        self.get_network_pool_args.update({"state": "present",
                                           "sc_params": {"static_routes": [{"gateway": "",
                                                                            "prefix_len": 4,
                                                                            "subnet": "",
                                                                            "route_state": "remove"}]}})
        powerscale_module_mock.module.params = self.get_network_pool_args
        utils.get_network_pool_details = MagicMock(
            return_value=MockNetworkPoolApi.GET_NETWORK_POOLS)
        self.capture_fail_json_call(MockNetworkPoolApi.network_pool_failed_msg('invalid_route'),
                                    powerscale_module_mock, NetworkPoolHandler)
