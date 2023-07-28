# Copyright: (c) 2021, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for Network pool module on PowerScale"""

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


from ansible_collections.dellemc.powerscale.plugins.modules.networkpool import NetworkPool
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_networkpool_api as MockNetworkPoolApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException


class TestNetworkPool():
    get_network_pool_args = {"groupnet_name": "groupnet0",
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
                             "sc_params": {"static_routes": [],
                                           "sc_dns_zone_aliases": []}}

    @pytest.fixture
    def network_pool_module_mock(self, mocker):
        mocker.patch(MockNetworkPoolApi.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        networkpool_module_mock = NetworkPool()
        networkpool_module_mock.module = MagicMock()
        return networkpool_module_mock

    def test_get_network_pool(self, network_pool_module_mock):
        network_pool = MockNetworkPoolApi.GET_NETWORK_POOLS
        self.get_network_pool_args.update({"state": "present"})
        network_pool_module_mock.module.params = self.get_network_pool_args
        network_pool_module_mock.network_groupnet_api.get_subnets_subnet_pool = MagicMock(
            return_value=MockSDKResponse(MockNetworkPoolApi.GET_NETWORK_POOLS))
        network_pool_module_mock.perform_module_operation()
        assert network_pool_module_mock.module.exit_json.call_args[1]['changed'] is False
        assert network_pool == network_pool_module_mock.module.exit_json.call_args[1]['network_pool']

    def test_get_network_pool_with_exception(self, network_pool_module_mock):
        MockNetworkPoolApi.GET_NETWORK_POOLS
        self.get_network_pool_args.update({"state": "present"})
        network_pool_module_mock.module.params = self.get_network_pool_args
        network_pool_module_mock.network_groupnet_api.get_subnets_subnet_pool = MagicMock(side_effect=utils.ApiException)
        network_pool_module_mock.perform_module_operation()
        assert MockNetworkPoolApi.get_networkpool_failed_msg(MockNetworkPoolApi.GET_NETWORK_POOLS['pools'][0]['name']) in \
            network_pool_module_mock.module.fail_json.call_args[1]['msg']

    def test_get_network_pool_with_404_exception(self, network_pool_module_mock):
        MockNetworkPoolApi.GET_NETWORK_POOLS
        self.get_network_pool_args.update({"state": "present"})
        MockApiException.status = '404'
        network_pool_module_mock.module.params = self.get_network_pool_args
        network_pool_module_mock.network_groupnet_api.get_subnets_subnet_pool = MagicMock(side_effect=utils.ApiException)
        network_pool_module_mock.perform_module_operation()
        assert network_pool_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_network_pool(self, network_pool_module_mock):
        self.get_network_pool_args.update({"state": "present",
                                           "description": "Test_pool1",
                                           "additional_pool_params": {"ranges": [{"low": "1.*.*.*",
                                                                                  "high": "1.*.*.*"}],
                                                                      "range_state": "add",
                                                                      "ifaces": [{"iface": "ext-1",
                                                                                  "lnn": 4}],
                                                                      "iface_state": "add"},
                                           "sc_params": {"sc_dns_zone": "1.*.*.*",
                                                         "sc_connect_policy": "throughput",
                                                         "sc_failover_policy": "throughput",
                                                         "rebalance_policy": "auto",
                                                         "alloc_method": "dynamic",
                                                         "sc_auto_unsuspend_delay": 200,
                                                         "sc_ttl": 300,
                                                         "aggregation_mode": "lacp",
                                                         "sc_dns_zone_aliases": ["smartconn-zone"],
                                                         "sc_subnet": "subnet_test",
                                                         "static_routes": [{"gateway": "1.*.*.*",
                                                                            "prefix_len": 4,
                                                                            "subnet": "1.*.*.*"}]}})
        network_pool_module_mock.module.params = self.get_network_pool_args
        network_pool_module_mock.get_network_pool = MagicMock(return_value=None)
        network_pool_module_mock.network_groupnet_api.create_subnets_subnet_pool = MagicMock(
            return_value=MockSDKResponse(MockNetworkPoolApi.CREATE_NETWORK_POOL))
        network_pool_module_mock.perform_module_operation()
        assert network_pool_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_create_network_pool_with_exception(self, network_pool_module_mock):
        self.get_network_pool_args.update({"state": "present",
                                           "description": "Test_pool1",
                                           "additional_pool_params": {"ranges": [{"low": "1.*.*.*",
                                                                                  "high": "1.*.*.*"}],
                                                                      "range_state": "add",
                                                                      "ifaces": [{"iface": "ext-1",
                                                                                  "lnn": 4}],
                                                                      "iface_state": "add"},
                                           "sc_params": {"sc_dns_zone": "1.*.*.*",
                                                         "sc_connect_policy": "throughput",
                                                         "sc_failover_policy": "throughput",
                                                         "rebalance_policy": "auto",
                                                         "alloc_method": "dynamic",
                                                         "sc_auto_unsuspend_delay": 200,
                                                         "sc_ttl": 300,
                                                         "aggregation_mode": "lacp",
                                                         "sc_dns_zone_aliases": ["smartconn-zone"],
                                                         "sc_subnet": "subnet_test",
                                                         "static_routes": [{"gateway": "1.*.*.*",
                                                                            "prefix_len": 4,
                                                                            "subnet": "1.*.*.*"}]}})
        network_pool_module_mock.module.params = self.get_network_pool_args
        network_pool_module_mock.get_network_pool = MagicMock(return_value=None)
        network_pool_module_mock.network_groupnet_api.create_subnets_subnet_pool = MagicMock(side_effect=utils.ApiException)
        network_pool_module_mock.perform_module_operation()
        assert MockNetworkPoolApi.create_networkpool_failed_msg(MockNetworkPoolApi.GET_NETWORK_POOLS['pools'][0]['name']) in \
            network_pool_module_mock.module.fail_json.call_args[1]['msg']

    def test_create_network_pool_with_blank_values(self, network_pool_module_mock):
        self.get_network_pool_args.update({"state": "present",
                                           "pool_name": "",
                                           "description": "",
                                           "access_zone": None,
                                           "additional_pool_params": {"ranges": [],
                                                                      "range_state": None,
                                                                      "ifaces": [],
                                                                      "iface_state": None},
                                           "sc_params": {"sc_dns_zone": "",
                                                          "sc_connect_policy": "",
                                                          "sc_failover_policy": "",
                                                          "rebalance_policy": "",
                                                          "alloc_method": "",
                                                          "sc_auto_unsuspend_delay": None,
                                                          "sc_ttl": None,
                                                          "aggregation_mode": "",
                                                          "sc_dns_zone_aliases": "",
                                                          "sc_subnet": "",
                                                          "static_routes": None}})
        network_pool_module_mock.module.params = self.get_network_pool_args
        network_pool_module_mock.get_network_pool = MagicMock(return_value=None)
        network_pool_module_mock.network_groupnet_api.create_subnets_subnet_pool = MagicMock(side_effect=utils.ApiException)
        network_pool_module_mock.perform_module_operation()
        assert network_pool_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_delete_network_pool(self, network_pool_module_mock):
        self.get_network_pool_args.update({"state": "absent"})
        network_pool_module_mock.module.params = self.get_network_pool_args
        network_pool_module_mock.network_groupnet_api.get_subnets_subnet_pool = MagicMock(
            return_value=MockSDKResponse(MockNetworkPoolApi.GET_NETWORK_POOLS))
        network_pool_module_mock.network_groupnet_api.delete_subnets_subnet_pool = MagicMock(return_value=None)
        network_pool_module_mock.perform_module_operation()
        assert (network_pool_module_mock.module.exit_json.call_args[1]['changed'])

    def test_delete_network_pool_with_exception(self, network_pool_module_mock):
        self.get_network_pool_args.update({"state": "absent"})
        network_pool_module_mock.module.params = self.get_network_pool_args
        network_pool_module_mock.network_groupnet_api.get_subnets_subnet_pool = MagicMock(
            return_value=MockSDKResponse(MockNetworkPoolApi.GET_NETWORK_POOLS))
        network_pool_module_mock.network_groupnet_api.delete_subnets_subnet_pool = MagicMock(side_effect=utils.ApiException)
        network_pool_module_mock.perform_module_operation()
        assert MockNetworkPoolApi.delete_networkpool_failed_msg(MockNetworkPoolApi.GET_NETWORK_POOLS['pools'][0]['name']) in \
            network_pool_module_mock.module.fail_json.call_args[1]['msg']

    def test_modify_network_pool(self, network_pool_module_mock):
        self.get_network_pool_args.update({"state": "present",
                                           "description": "Test_pool1",
                                           "additional_pool_params": {"ranges": [{"low": "1.*.*.*",
                                                                                  "high": "1.*.*.*"}],
                                                                      "range_state": "add",
                                                                      "ifaces": [{"iface": "ext-1",
                                                                                  "lnn": 4}],
                                                                      "iface_state": "add"},
                                           "sc_params": {"sc_dns_zone": "1.*.*.*",
                                                         "sc_connect_policy": "throughput",
                                                         "sc_failover_policy": "throughput",
                                                         "rebalance_policy": "auto",
                                                         "alloc_method": "dynamic",
                                                         "sc_auto_unsuspend_delay": 200,
                                                         "sc_ttl": 300,
                                                         "aggregation_mode": "lacp",
                                                         "sc_dns_zone_aliases": ["smartconn-zone"],
                                                         "sc_subnet": "subnet_test",
                                                         "static_routes": [{"gateway": "1.*.*.*",
                                                                            "prefix_len": 4,
                                                                            "subnet": "1.*.*.*"}]}})
        network_pool_module_mock.module.params = self.get_network_pool_args
        network_pool_module_mock.network_groupnet_api.get_subnets_subnet_pool = MagicMock(
            return_value=MockSDKResponse(MockNetworkPoolApi.CREATE_NETWORK_POOL))
        network_pool_module_mock.network_groupnet_api.update_subnets_subnet_pool = MagicMock(return_value=None)
        network_pool_module_mock.perform_module_operation()
        assert (network_pool_module_mock.module.exit_json.call_args[1]['changed'])

    def test_modify_network_pool_with_exception(self, network_pool_module_mock):
        self.get_network_pool_args.update({"state": "present",
                                           "description": "Test_pool1",
                                           "additional_pool_params": {"ranges": [{"low": "1.*.*.*",
                                                                                  "high": "1.*.*.*"}],
                                                                      "range_state": "add",
                                                                      "ifaces": [{"iface": "ext-1",
                                                                                  "lnn": 4}],
                                                                      "iface_state": "add"},
                                           "sc_params": {"sc_dns_zone": "1.*.*.*",
                                                         "sc_connect_policy": "throughput",
                                                         "sc_failover_policy": "throughput",
                                                         "rebalance_policy": "auto",
                                                         "alloc_method": "dynamic",
                                                         "sc_auto_unsuspend_delay": 200,
                                                         "sc_ttl": 300,
                                                         "aggregation_mode": "lacp",
                                                         "sc_dns_zone_aliases": ["smartconn-zone"],
                                                         "sc_subnet": "subnet_test",
                                                         "static_routes": [{"gateway": "1.*.*.*",
                                                                            "prefix_len": 4,
                                                                            "subnet": "1.*.*.*"}]}})
        network_pool_module_mock.module.params = self.get_network_pool_args
        network_pool_module_mock.network_groupnet_api.get_subnets_subnet_pool = MagicMock(
            return_value=MockSDKResponse(MockNetworkPoolApi.CREATE_NETWORK_POOL))
        network_pool_module_mock.network_groupnet_api.update_subnets_subnet_pool = MagicMock(side_effect=utils.ApiException)
        network_pool_module_mock.perform_module_operation()
        assert MockNetworkPoolApi.modify_networkpool_failed_msg(MockNetworkPoolApi.GET_NETWORK_POOLS['pools'][0]['name']) in \
            network_pool_module_mock.module.fail_json.call_args[1]['msg']
