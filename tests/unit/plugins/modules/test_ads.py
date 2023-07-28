# Copyright: (c) 2022, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for ADS module on PowerScale"""

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

from ansible_collections.dellemc.powerscale.plugins.modules.ads import Ads
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils \
    import mock_ads_api as MockAdsApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException


class TestAds():
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'
    ads_args = {'domain_name': 'ads_domain', 'instance_name': 'ads_instance',
                'ads_user': 'user', 'ads_password': '***', 'state': 'present',
                'ads_parameters': {'groupnet': None, 'home_directory_template': None,
                                   'login_shell': None, 'machine_account': None, 'organizational_unit': None},
                'spns': None, 'spn_command': None}

    @pytest.fixture
    def ads_module_mock(self, mocker):
        mocker.patch(self.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        ads_module_mock = Ads()
        return ads_module_mock

    def test_create_ads(self, ads_module_mock):
        self.ads_args.update({'ads_parameters': {'groupnet': 'groupnet0', 'home_directory_template': '/home',
                                                 'login_shell': '/bin/zsh', 'machine_account': 'test_account',
                                                 'organizational_unit': 'OU', 'spns': [], 'spn_state': None}})

        ads_module_mock.module.params = self.ads_args
        ads_module_mock.get_ads_details = MagicMock(return_value=None)
        ads_module_mock.auth_api_instance.create_providers_ads_item = MagicMock(return_value=MockAdsApi.get_ads_response())
        ads_module_mock.perform_module_operation()

        assert ads_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_create_ads_throws_exception(self, ads_module_mock):
        ads_module_mock.module.params = self.ads_args
        ads_module_mock.get_ads_details = MagicMock(return_value=None)
        ads_module_mock.auth_api_instance.create_providers_ads_item = MagicMock(side_effect=utils.ApiException)
        ads_module_mock.create(self.ads_args['domain_name'], self.ads_args['instance_name'],
                               self.ads_args['ads_user'], self.ads_args['ads_password'],
                               self.ads_args['ads_parameters'])

        assert MockAdsApi.create_ads_ex_msg() in \
            ads_module_mock.module.fail_json.call_args[1]['msg']

    def test_add_spn(self, ads_module_mock):
        self.ads_args.update({'instance_name': None, 'spns': [{'spn': 'klm', 'state': 'present'}]})
        ads_module_mock.module.params = self.ads_args
        ads_module_mock.get_ads_details = MagicMock(return_value=MockAdsApi.get_ads_response_for_spn())
        ads_module_mock.get_auth_providers_summary = MagicMock(return_value=MockAdsApi.get_provider_summary())
        ads_module_mock.auth_api_instance.update_providers_ads_by_id = MagicMock(return_value=None)
        ads_module_mock.zones_api_instance.list_zones = MagicMock(return_value=None)
        ads_module_mock.perform_module_operation()
        assert ads_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_remove_spn(self, ads_module_mock):
        self.ads_args.update({'instance_name': None, 'spns': [{'spn': 'abc', 'state': 'absent'}]})
        ads_module_mock.module.params = self.ads_args
        ads_module_mock.get_ads_details = MagicMock(return_value=MockAdsApi.get_ads_response_for_spn())
        ads_module_mock.get_auth_providers_summary = MagicMock(return_value=MockAdsApi.get_provider_summary())
        ads_module_mock.auth_api_instance.update_providers_ads_by_id = MagicMock(return_value=None)
        ads_module_mock.zones_api_instance.list_zones = MagicMock(return_value=None)
        ads_module_mock.perform_module_operation()
        assert ads_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_fix_spn(self, ads_module_mock):
        self.ads_args.update({'instance_name': None, 'spn_command': 'fix'})
        ads_module_mock.module.params = self.ads_args
        ads_module_mock.get_ads_details = MagicMock(return_value=MockAdsApi.get_ads_response_for_spn())
        ads_module_mock.get_auth_providers_summary = MagicMock(return_value=MockAdsApi.get_provider_summary())
        ads_module_mock.auth_api_instance.update_providers_ads_by_id = MagicMock(return_value=None)
        ads_module_mock.zones_api_instance.list_zones = MagicMock(return_value=None)
        ads_module_mock.perform_module_operation()
        assert ads_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_check_spn(self, ads_module_mock):
        self.ads_args.update({'instance_name': None, 'spn_command': 'check'})
        ads_module_mock.module.params = self.ads_args
        ads_module_mock.get_ads_details = MagicMock(return_value=MockAdsApi.get_ads_response_for_spn())
        ads_module_mock.get_auth_providers_summary = MagicMock(return_value=MockAdsApi.get_provider_summary())
        ads_module_mock.auth_api_instance.update_providers_ads_by_id = MagicMock(return_value=None)
        ads_module_mock.zones_api_instance.list_zones = MagicMock(return_value=None)
        ads_module_mock.perform_module_operation()
        assert 'klm' in ads_module_mock.module.exit_json.call_args[1]["spn_check"]
