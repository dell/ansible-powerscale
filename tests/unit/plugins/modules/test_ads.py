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
from ansible_collections.dellemc.powerscale.plugins.modules.ads import Ads, AdsHandler, main
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils \
    import mock_ads_api as MockAdsApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library. \
    fail_json import FailJsonException


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

    def test_get_ads_details(self, powerscale_module_mock, mocker):
        mocker.patch.object(utils, "get_ads_provider_details", return_value={"ads": [{"id": "ads_id"}]})
        ads_name = ["ads_name"]
        result = powerscale_module_mock.get_ads_details(ads_name)
        print("result is ", result)
        assert result == [{"id": "ads_id"}]

    def test_get_ads_details_exception(self, powerscale_module_mock, mocker):
        mocker.patch.object(utils, "get_ads_provider_details", side_effect=Exception("Test exception"))
        ads_name = ["ads_name"]
        with pytest.raises(Exception) as exc_info:
            powerscale_module_mock.get_ads_details(ads_name)
        assert str(exc_info.value) == "Get details of ADS provider ['ads_name'] failed with error: Test exception"

    def test_get_ads_details_not_found(self, powerscale_module_mock, mocker):
        mocker.patch.object(utils, "get_ads_provider_details", side_effect=Exception("404"))
        ads_name = ["ads_name"]
        result = powerscale_module_mock.get_ads_details(ads_name)
        assert result is None

    def test_validate_create_params_with_invalid_domain(self, powerscale_module_mock):
        # Test case: Validate with invalid domain
        domain = ''
        ads_user = MockAdsApi.USER1
        ads_password = MockAdsApi.PASS1
        ads_parameters = {}

        with pytest.raises(FailJsonException) as exc:
            powerscale_module_mock.validate_create_params(domain, ads_user, ads_password, ads_parameters)

        assert exc.value.args[0] == "The parameter domain_name is mandatory while creating ADS provider"

    def test_validate_create_params_with_invalid_ads_user(self, powerscale_module_mock):
        # Test case: Validate with invalid ads_user
        domain = MockAdsApi.DOMAIN_NAME
        ads_user = ''
        ads_password = MockAdsApi.PASS1
        ads_parameters = {}

        with pytest.raises(FailJsonException) as exc:
            powerscale_module_mock.validate_create_params(domain, ads_user, ads_password, ads_parameters)

        assert exc.value.args[0] == "The parameter ads_user is mandatory while creating ADS provider"

    def test_validate_create_params_with_invalid_ads_password(self, powerscale_module_mock):
        # Test case: Validate with invalid ads_password
        domain = MockAdsApi.DOMAIN_NAME
        ads_user = MockAdsApi.USER1
        ads_password = ''
        ads_parameters = {}

        with pytest.raises(FailJsonException) as exc:
            powerscale_module_mock.validate_create_params(domain, ads_user, ads_password, ads_parameters)

        assert exc.value.args[0] == "The parameter ads_password is mandatory while creating ADS provider"

    def test_validate_create_params_with_invalid_machine_account(self, powerscale_module_mock):
        # Test case: Validate with invalid machine_account
        domain = MockAdsApi.DOMAIN_NAME
        ads_user = MockAdsApi.USER1
        ads_password = MockAdsApi.PASS1
        ads_parameters = {'machine_account': ''}

        with pytest.raises(FailJsonException) as exc:
            powerscale_module_mock.validate_create_params(domain, ads_user, ads_password, ads_parameters)

        assert exc.value.args[0] == "Please specify a valid machine_account"

    def test_validate_create_params_with_invalid_organizational_unit(self, powerscale_module_mock):
        # Test case: Validate with invalid organizational_unit
        domain = MockAdsApi.DOMAIN_NAME
        ads_user = MockAdsApi.USER1
        ads_password = MockAdsApi.PASS1
        ads_parameters = {'organizational_unit': ''}

        with pytest.raises(FailJsonException) as exc:
            powerscale_module_mock.validate_create_params(domain, ads_user, ads_password, ads_parameters)

        assert exc.value.args[0] == "Please specify a valid organizational_unit"

    def test_validate_create_params_with_invalid_domain_regex(self, powerscale_module_mock):
        # Test case: Validate with invalid domain regex
        domain = 'example.com.'
        ads_user = MockAdsApi.USER1
        ads_password = MockAdsApi.PASS1
        ads_parameters = {}

        with pytest.raises(FailJsonException) as exc:
            powerscale_module_mock.validate_create_params(domain, ads_user, ads_password, ads_parameters)

        assert exc.value.args[0] == 'The value for domain_name is invalid'

    def test_validate_input_with_domain_and_instance(self, powerscale_module_mock):
        ads_details = []
        domain = MockAdsApi.DOMAIN_NAME
        instance = "example_instance"

        with pytest.raises(FailJsonException) as exc:
            powerscale_module_mock.validate_input(ads_details, domain, instance)

        assert exc.value.args[0] == "parameters are mutually exclusive: domain_name|instance_name"

    def test_validate_input_without_domain_and_instance(self, powerscale_module_mock):
        ads_details = []
        domain = None
        instance = None

        with pytest.raises(FailJsonException) as exc:
            powerscale_module_mock.validate_input(ads_details, domain, instance)

        assert exc.value.args[0] == "Please specify domain_name or instance_name"

    def test_validate_input_with_multiple_ads_details(self, powerscale_module_mock):
        ads_details = [
            {"id": "example_id1"},
            {"id": "example_id2"}
        ]
        domain = MockAdsApi.DOMAIN_NAME
        instance = None

        with pytest.raises(FailJsonException) as exc:
            powerscale_module_mock.validate_input(ads_details, domain, instance)

        assert exc.value.args[0] == "Multiple ADS instances are returned for the given domain_name. Please specify instance_name"

    def test_check_for_groupnet_with_mismatch(self, powerscale_module_mock):
        array_ads = [{
            'groupnet': 'example_groupnet',
        }]
        input_ads = {
            'groupnet': 'different_groupnet',
        }

        with pytest.raises(FailJsonException) as exc:
            powerscale_module_mock.check_for_groupnet('groupnet', array_ads, input_ads)

        assert exc.value.args[0] == "Modification of groupnet is not supported."

    def test_main(self, powerscale_module_mock):
        main()
