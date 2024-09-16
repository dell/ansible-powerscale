# Copyright: (c) 2022-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for ADS module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
from ansible_collections.dellemc.powerscale.plugins.modules.ads import Ads, AdsHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils \
    import mock_ads_api as MockAdsApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase


class TestAds(PowerScaleUnitBase):
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'
    ads_args = MockAdsApi.ADS_COMMAN_ARG

    @pytest.fixture
    def module_object(self):
        return Ads

    def test_create_ads(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.ads_args,
            MockAdsApi.CREATE_ARGS)
        powerscale_module_mock.module._diff = True
        powerscale_module_mock.get_ads_details = MagicMock(
            return_value=None)
        AdsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.auth_api_instance.create_providers_ads_item.assert_called()

    def test_create_ads_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.ads_args,
            MockAdsApi.CREATE_ARGS)
        powerscale_module_mock.module._diff = True
        powerscale_module_mock.get_ads_details = MagicMock(
            return_value=None)
        powerscale_module_mock.auth_api_instance.create_providers_ads_item = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            "Add an Active Directory provider failed with SDK Error message",
            powerscale_module_mock, AdsHandler
        )

    def test_modify_ads(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.ads_args,
            MockAdsApi.MODIFY_ARGS)
        powerscale_module_mock.ads_name = [MockAdsApi.DOMAIN_NAME]
        powerscale_module_mock.module._diff = True
        powerscale_module_mock.get_ads_details = MagicMock(
            return_value=MockAdsApi.ADS_DETAILS["ads"])
        AdsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.auth_api_instance.update_providers_ads_by_id.assert_called()

    def test_modify_ads_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.ads_args,
            MockAdsApi.MODIFY_ARGS)
        powerscale_module_mock.ads_name = [MockAdsApi.DOMAIN_NAME]
        powerscale_module_mock.get_ads_details = MagicMock(
            return_value=MockAdsApi.ADS_DETAILS["ads"])
        powerscale_module_mock.auth_api_instance.update_providers_ads_by_id = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            "Modifying Active Directory provider failed with SDK Error message",
            powerscale_module_mock, AdsHandler)

    def test_delete_ads(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.ads_args,
            {"domain_name": MockAdsApi.DOMAIN_NAME, "state": "absent"})
        powerscale_module_mock.ads_name = [MockAdsApi.DOMAIN_NAME]
        powerscale_module_mock.module._diff = True
        powerscale_module_mock.get_ads_details = MagicMock(
            return_value=MockAdsApi.ADS_DETAILS["ads"])
        AdsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.auth_api_instance.delete_providers_ads_by_id.assert_called()

    def test_delete_ads_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.ads_args,
            {"domain_name": MockAdsApi.DOMAIN_NAME, "state": "absent"})
        powerscale_module_mock.ads_name = [MockAdsApi.DOMAIN_NAME]
        powerscale_module_mock.get_ads_details = MagicMock(
            return_value=MockAdsApi.ADS_DETAILS["ads"])
        powerscale_module_mock.auth_api_instance.delete_providers_ads_by_id = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            "Deleting ADS provider failed with SDK Error message",
            powerscale_module_mock, AdsHandler)

    def test_get_auth_providers_summary_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.ads_args,
            {"domain_name": MockAdsApi.DOMAIN_NAME, "state": "absent"})
        powerscale_module_mock.get_ads_details = MagicMock(
            return_value=MockAdsApi.ADS_DETAILS["ads"])
        powerscale_module_mock.auth_api_instance.get_providers_summary = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            "Get auth providers summary failed with SDK Error message",
            powerscale_module_mock, AdsHandler)

    def test_update_ads_zone_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.ads_args,
            {"domain_name": MockAdsApi.DOMAIN_NAME, "state": "present"})
        powerscale_module_mock.get_ads_details = MagicMock(
            return_value=MockAdsApi.ADS_DETAILS["ads"])
        powerscale_module_mock.zones_api_instance.list_zones = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            "Update ADS with access zone details failed with SDK Error message",
            powerscale_module_mock, AdsHandler)

    def test_get_ads_details(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock, self.ads_args,
            {"domain_name": MockAdsApi.DOMAIN_NAME, "state": "present"})
        powerscale_module_mock.ads_name = [MockAdsApi.DOMAIN_NAME]
        powerscale_module_mock.auth_api_instance.get_providers_ads_by_id.to_dict = MagicMock(
            return_value=MockAdsApi.ADS_DETAILS)
        AdsHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.auth_api_instance.get_providers_ads_by_id.assert_called()

    def test_get_ads_exception(self, powerscale_module_mock):
        powerscale_module_mock.ads_name = [MockAdsApi.DOMAIN_NAME]
        powerscale_module_mock.auth_api_instance.get_providers_ads_by_id = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            "failed with error: SDK Error message",
            powerscale_module_mock, AdsHandler)
