# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Node module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils


from ansible_collections.dellemc.powerscale.plugins.modules.node import ClusterNode, main
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_node_api as MockNodeApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase


class TestClusterNode(PowerScaleUnitBase):
    get_node_args = {
        'node_id': None,
    }

    @pytest.fixture
    def module_object(self):
        return ClusterNode

    def test_get_node_info(self, powerscale_module_mock):
        self.get_node_args.update({
            'node_id': 1,
            'state': 'present',
            'onefs_host': '1.2.3.4'
        })
        ob = MagicMock()
        ob.node_info = {
            'id': 1,
            'lnn': 1,
            'partitions': {
                'count': 1,
                'partitions': [
                    {
                        'block_size': 1024,
                        'capacity': 1957516,
                        'component_devices': 'ada0p2',
                        'mount_point': '/',
                        'percent_used': '50%',
                        'statfs': {
                            'f_namemax': 255,
                            'f_owner': 0,
                            'f_type': 53,
                            'f_version': 538182936
                        },
                        'used': 909066
                    }
                ]
            }
        }
        powerscale_module_mock.module.params = self.get_node_args
        powerscale_module_mock.cluster_api.get_cluster_node = MagicMock(
            return_value=ob)
        powerscale_module_mock.perform_module_operation()

        assert (
            powerscale_module_mock.module.exit_json.call_args[1]['cluster_node_details'])
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

        # Scenario 2: When exception occured
        powerscale_module_mock.cluster_api.get_cluster_node = \
            MagicMock(side_effect=utils.ApiException)

        self.capture_fail_json_call(MockNodeApi.api_exception_msg(), invoke_perform_module=True)

    def test_get_node_info_absent(self, powerscale_module_mock):
        self.get_node_args.update({
            'node_id': 1,
            'state': 'absent',
        })
        powerscale_module_mock.module.params = self.get_node_args
        powerscale_module_mock.cluster_api.get_cluster_node = MagicMock(
            return_value={})
        self.capture_fail_json_call(MockNodeApi.disallow_delete_node_msg(), invoke_perform_module=True)

    def test_main(self):
        ob = main()
        assert ob is None  # nothing to assert as it doesn't return anything
