# Copyright: (c) 2022-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for smartquota module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils


from ansible_collections.dellemc.powerscale.plugins.modules.smartquota import SmartQuota
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils.mock_smartquota_api import MockSmartQuotaApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException


class TestSmartQuota():
    get_smartquota_args = MockSmartQuotaApi.SMART_QUOTA_COMMON_ARGS

    @pytest.fixture
    def smartquota_module_mock(self, mocker):
        smartquota_module_mock = SmartQuota()
        smartquota_module_mock.module = MagicMock()
        utils.convert_size_with_unit = MagicMock()
        mocker.patch(MockSmartQuotaApi.MODULE_UTILS_PATH + '.ApiException',
                     new=MockApiException)
        return smartquota_module_mock

    @pytest.mark.parametrize("params", [{"path": MockSmartQuotaApi.PATH1,
                                         "access_zone": "System",
                                         "quota_type": "directory",
                                         "user_name": "sample",
                                         "group_name": "sample_group",
                                         "provider_type": "local",
                                         "quota": {
                                             "thresholds_on": "fs_logical_size",
                                             "soft_limit_size": 5,
                                             "hard_limit_size": 10,
                                             "cap_unit": "GB",
                                             "soft_grace_period": 1,
                                             "period_unit": "days",
                                             "advisory_limit_size": 3,
                                             "include_overheads": True,
                                             "container": True,
                                         },
                                         "list_snapshots": True,
                                         "state": "present"},
                                        {
                                        "path": MockSmartQuotaApi.PATH1,
                                        "access_zone": "System",
                                        "quota_type": "directory",
                                        "user_name": "sample",
                                        "group_name": "sample_group",
                                        "provider_type": "nis",
                                        "quota": {
                                            "thresholds_on": "fs_logical_size",
                                            "soft_limit_size": 5,
                                            "hard_limit_size": 10,
                                            "cap_unit": "GB",
                                            "soft_grace_period": 1,
                                            "period_unit": "months",
                                            "advisory_limit_size": 3,
                                            "include_overheads": True,
                                            "container": True,
                                        },
                                        "list_snapshots": True,
                                        "state": "present"}
                                        ])
    def test_smartquota_create_quota(self, params, smartquota_module_mock):
        self.get_smartquota_args.update(params)
        smartquota_module_mock.module.params = self.get_smartquota_args
        smartquota_module_mock.get_quota_params = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaThresholds = MagicMock(return_value=None)
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaCreateParams = MagicMock(return_value=None)
        smartquota_module_mock.add_limits_with_unit = MagicMock()
        smartquota_module_mock.quota_api_instance.create_quota_quota = MagicMock(return_value=None)
        smartquota_module_mock.determine_error = MagicMock(return_value=None)
        smartquota_module_mock.module.check_mode = False
        smartquota_module_mock.perform_module_operation()
        assert smartquota_module_mock.module.exit_json.call_args[1]["changed"] is True

    @pytest.mark.parametrize("params", [{"path": MockSmartQuotaApi.PATH1,
                                         "access_zone": "System",
                                         "quota_type": "directory",
                                         "user_name": "sample",
                                         "group_name": "sample_group",
                                         "provider_type": "local",
                                         "quota": {
                                             "include_snapshots": True,
                                             "thresholds_on": "fs_logical_size",
                                             "soft_limit_size": 5,
                                             "hard_limit_size": 10,
                                             "cap_unit": "GB",
                                             "soft_grace_period": 1,
                                             "period_unit": "days",
                                             "advisory_limit_size": 3,
                                             "include_overheads": True,
                                             "container": True
                                         },
                                         "list_snapshots": True,
                                         "state": "present"}])
    def test_smartquota_create_quota_check_mode(self, params, smartquota_module_mock):
        smartquota_module_mock.module.check_mode = True
        self.get_smartquota_args.update(params)
        smartquota_module_mock.module.params = self.get_smartquota_args
        smartquota_module_mock.get_quota_params = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaThresholds = MagicMock(return_value=None)
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaCreateParams = MagicMock(return_value=None)
        smartquota_module_mock.add_limits_with_unit = MagicMock()
        smartquota_module_mock.quota_api_instance.create_quota_quota = MagicMock(return_value=None)
        smartquota_module_mock.determine_error = MagicMock(return_value=None)
        smartquota_module_mock.get_quota_details = MagicMock(return_value=(None, None))
        smartquota_module_mock.perform_module_operation()
        assert smartquota_module_mock.module.exit_json.call_args[1]["changed"] is True

    @pytest.mark.parametrize("params", [{"path": MockSmartQuotaApi.PATH1,
                                         "access_zone": "System",
                                         "quota_type": "directory",
                                         "user_name": "sample",
                                         "group_name": "sample_group",
                                         "provider_type": "local",
                                         "quota": {
                                             "include_snapshots": False,
                                             "thresholds_on": "fs_logical_size",
                                             "soft_limit_size": 6,
                                             "hard_limit_size": 9,
                                             "cap_unit": "GB",
                                             "soft_grace_period": 1,
                                             "period_unit": "days",
                                             "advisory_limit_size": 3,
                                             "include_overheads": False,
                                             "container": False
                                         },
                                         "list_snapshots": False,
                                         "state": "present"}])
    def test_smartquota_update_quota_check_mode(self, params, smartquota_module_mock):
        smartquota_module_mock.module.check_mode = True
        self.get_smartquota_args.update(params)
        smartquota_module_mock.module.params = self.get_smartquota_args
        smartquota_module_mock.get_quota_params = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaThresholds = MagicMock(return_value=None)
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuota = MagicMock(return_value=None)
        smartquota_module_mock.quota_api_instance.update_quota_quota = MagicMock(return_value=None)
        smartquota_module_mock.determine_error = MagicMock(return_value=None)
        smartquota_module_mock.perform_module_operation()
        assert smartquota_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_smartquota_create_quota_exception(self, smartquota_module_mock):
        self.get_smartquota_args.update({"path": "/ifs/ATest3",
                                         "access_zone": "System",
                                         "quota_type": "directory",
                                         "quota": {
                                             "include_snapshots": True,
                                             "thresholds_on": "fs_logical_size",
                                             "soft_limit_size": 5,
                                             "hard_limit_size": 10,
                                             "cap_unit": "GB",
                                             "soft_grace_period": 1,
                                             "period_unit": "weeks",
                                             "persona": None,
                                             "advisory_limit_size": 3,
                                             "include_overheads": True,
                                             "container": True,
                                         },
                                         "list_snapshots": True,
                                         "state": "present"})
        smartquota_module_mock.module.check_mode = False
        smartquota_module_mock.module.params = self.get_smartquota_args
        utils.get_size_bytes = MagicMock(side_effect=[
            MockSmartQuotaApi.get_smartquota_dependent_response("advisory"),
            MockSmartQuotaApi.get_smartquota_dependent_response("hard"),
            MockSmartQuotaApi.get_smartquota_dependent_response("soft")])
        api_response = MagicMock()
        api_response.quotas = None
        smartquota_module_mock.quota_api_instance.list_quota_quotas = MagicMock(return_value=api_response)
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaThresholds = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaCreateParams = MagicMock(return_value=None)
        smartquota_module_mock.add_limits_with_unit = MagicMock()
        utils.convert_size_with_unit = MagicMock(return_value=None)
        smartquota_module_mock.quota_api_instance.update_quota_quota = MagicMock()
        utils.isi_sdk.AuthAccessAccessItemFileGroup = MagicMock(return_value=[])
        smartquota_module_mock.determine_error = MagicMock(return_value=None)
        smartquota_module_mock.quota_api_instance.create_quota_quota = MagicMock(side_effect=utils.ApiException)
        smartquota_module_mock.perform_module_operation()
        assert MockSmartQuotaApi.smartquota_create_quota_response(path="Mock_Path") not in \
            smartquota_module_mock.module.fail_json.call_args[1]["msg"]

    def test_invalid_access_zone(self, smartquota_module_mock):
        self.get_smartquota_args.update({"path": MockSmartQuotaApi.PATH1,
                                         "access_zone": "Sys tem",
                                         "quota_type": "directory",
                                         "state": "present"})
        smartquota_module_mock.module.params = self.get_smartquota_args
        smartquota_module_mock.perform_module_operation()
        assert "Invalid access_zone provided. Provide valid access_zone" \
               not in smartquota_module_mock.module.fail_json.call_args[1]

    def test_invalid_path(self, smartquota_module_mock):
        self.get_smartquota_args.update({"path": MockSmartQuotaApi.PATH2,
                                         "access_zone": "System",
                                         "quota_type": "directory",
                                         "state": "present"})
        smartquota_module_mock.module.params = self.get_smartquota_args
        smartquota_module_mock.perform_module_operation()
        assert "Invalid path Test/Test1, Path must start with '/'" \
               not in smartquota_module_mock.module.fail_json.call_args[1]

    def test_create_user_quota(self, smartquota_module_mock):
        self.get_smartquota_args.update({"path": MockSmartQuotaApi.PATH2,
                                         "access_zone": "sample-zone",
                                         "quota_type": "user",
                                         "provider_type": "local",
                                         "user_name": "sample-user",
                                         "quota": {
                                             "thresholds_on": "app_logical_size",
                                             "soft_limit_size": 5,
                                             "hard_limit_size": 10,
                                             "cap_unit": "TB",
                                             "soft_grace_period": 1,
                                             "period_unit": "weeks",
                                             "advisory_limit_size": 3,
                                             "include_overheads": True,
                                             "include_snapshots": True
                                         },
                                         "state": "present"})
        smartquota_module_mock.module.check_mode = False
        smartquota_module_mock.module.params = self.get_smartquota_args
        smartquota_module_mock.auth_api_instance.get_auth_user = MagicMock(
            return_value=MockSmartQuotaApi.get_user_sid())
        get_quota_response = MagicMock()
        get_quota_response.quotas = None
        smartquota_module_mock.quota_api_instance.list_quota_quotas = \
            MagicMock(return_value=get_quota_response)
        smartquota_module_mock.perform_module_operation()
        smartquota_module_mock.quota_api_instance.create_quota_quota.\
            assert_called()
        assert smartquota_module_mock.module.exit_json.call_args[1]["changed"]\
               is True

    def test_delete_group_quota(self, smartquota_module_mock):
        self.get_smartquota_args.update({"path": MockSmartQuotaApi.PATH1,
                                         "access_zone": "sample-zone",
                                         "quota_type": "group_test",
                                         "provider_type": "ldp",
                                         "group_name": "sample-group",
                                         "state": "absent"})
        smartquota_module_mock.module.check_mode = False
        smartquota_module_mock.module.params = self.get_smartquota_args
        smartquota_module_mock.auth_api_instance.get_auth_group = MagicMock(
            return_value=MockSmartQuotaApi.get_group_sid())
        smartquota_module_mock.quota_api_instance.list_quota_quotas = \
            MagicMock(return_value=MockSmartQuotaApi.get_group_details())
        smartquota_module_mock.quota_api_instance.delete_quota_quota = \
            MagicMock(return_value=True)
        smartquota_module_mock.perform_module_operation()
        smartquota_module_mock.quota_api_instance.delete_quota_quota. \
            assert_called()
        assert smartquota_module_mock.module.exit_json.call_args[1]["changed"] \
               is True

    def test_delete_group_quota_exception(self, smartquota_module_mock):
        self.get_smartquota_args.update({"path": MockSmartQuotaApi.PATH2,
                                         "access_zone": "sample-zone",
                                         "quota_type": "group",
                                         "provider_type": "local",
                                         "group_name": "sample-user",
                                         "quota": {
                                             "thresholds_on": None,
                                             "soft_limit_size": None,
                                             "hard_limit_size": None,
                                             "advisory_limit_size": None,
                                             "cap_unit": None,
                                             "soft_grace_period": None,
                                             "period_unit": None,
                                             "include_snapshots": True
                                         },
                                         "state": "absent"})
        smartquota_module_mock.module.check_mode = False
        smartquota_module_mock.module.params = self.get_smartquota_args
        smartquota_module_mock.auth_api_instance.get_auth_group = MagicMock(
            return_value=MockSmartQuotaApi.get_group_sid())
        smartquota_module_mock.quota_api_instance.list_quota_quotas = \
            MagicMock(return_value=MockSmartQuotaApi.get_group_details())
        smartquota_module_mock.quota_api_instance.delete_quota_quota = \
            MagicMock(side_effect=MockApiException)
        smartquota_module_mock.perform_module_operation()
        smartquota_module_mock.quota_api_instance.delete_quota_quota. \
            assert_called()
        assert MockSmartQuotaApi.smartquota_delete_quota_response(path="Mock_Path") \
               not in smartquota_module_mock.module.fail_json.call_args[1]['msg']

    def test_get_sid_exception(self, smartquota_module_mock):
        self.get_smartquota_args.update({"path": MockSmartQuotaApi.PATH2,
                                         "access_zone": "sample-zone",
                                         "quota_type": "group",
                                         "provider_type": "local",
                                         "group_name": "sample-user",
                                         "quota": {
                                             "thresholds_on": None,
                                             "soft_limit_size": None,
                                             "hard_limit_size": None,
                                             "advisory_limit_size": None,
                                             "cap_unit": None,
                                             "soft_grace_period": None,
                                             "period_unit": None,
                                             "include_snapshots": True
                                         },
                                         "state": "absent"})
        smartquota_module_mock.module.params = self.get_smartquota_args
        smartquota_module_mock.auth_api_instance.get_auth_group = MagicMock(
            side_effect=MockApiException)
        smartquota_module_mock.perform_module_operation()
        smartquota_module_mock.auth_api_instance.get_auth_group.assert_called()
        assert \
            MockSmartQuotaApi.smartquota_get_sid_exception(name="sample-user",
                                                           az="sample-zone",
                                                           provider="local") \
            not in smartquota_module_mock.module.fail_json.call_args[1]['msg']
