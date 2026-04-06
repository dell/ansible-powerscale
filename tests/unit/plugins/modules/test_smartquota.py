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
from ansible_collections.dellemc.powerscale.tests.unit.plugins. \
    module_utils.mock_smartquota_api import MockSmartQuotaApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase


class TestSmartQuota(PowerScaleUnitBase):
    get_smartquota_args = MockSmartQuotaApi.SMART_QUOTA_COMMON_ARGS

    @pytest.fixture
    def module_object(self, mocker):
        utils.convert_size_with_unit = MagicMock()
        return SmartQuota

    @pytest.mark.parametrize("params", [{"path": MockSmartQuotaApi.PATH1,
                                         "access_zone": "System",
                                         "quota_type": "user",
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
                                            "quota_type": "user",
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
    def test_smartquota_create_quota(self, params, powerscale_module_mock):
        self.get_smartquota_args.update(params)
        powerscale_module_mock.module.params = self.get_smartquota_args
        powerscale_module_mock.get_quota_params = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaThresholds = MagicMock(return_value=None)
        utils.validate_threshold_overhead_parameter = MagicMock(
            return_value=None)
        utils.isi_sdk.QuotaQuotaCreateParams = MagicMock(return_value=None)
        powerscale_module_mock.add_limits_with_unit = MagicMock()
        powerscale_module_mock.quota_api_instance.create_quota_quota = MagicMock(
            return_value=None)
        powerscale_module_mock.determine_error = MagicMock(return_value=None)
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    @pytest.mark.parametrize("params", [{"path": MockSmartQuotaApi.PATH1,
                                         "access_zone": "System",
                                         "quota_type": "user",
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
    def test_smartquota_create_quota_check_mode(self, params, powerscale_module_mock):
        powerscale_module_mock.module.check_mode = True
        self.get_smartquota_args.update(params)
        powerscale_module_mock.module.params = self.get_smartquota_args
        powerscale_module_mock.get_quota_params = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaThresholds = MagicMock(return_value=None)
        utils.validate_threshold_overhead_parameter = MagicMock(
            return_value=None)
        utils.isi_sdk.QuotaQuotaCreateParams = MagicMock(return_value=None)
        powerscale_module_mock.add_limits_with_unit = MagicMock()
        powerscale_module_mock.quota_api_instance.create_quota_quota = MagicMock(
            return_value=None)
        powerscale_module_mock.determine_error = MagicMock(return_value=None)
        powerscale_module_mock.get_quota_details = MagicMock(
            return_value=(None, None))
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    @pytest.mark.parametrize("params", [{"path": MockSmartQuotaApi.PATH1,
                                         "access_zone": "System",
                                         "quota_type": "user",
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
    def test_smartquota_update_quota_check_mode(self, params, powerscale_module_mock):
        powerscale_module_mock.module.check_mode = True
        self.get_smartquota_args.update(params)
        powerscale_module_mock.module.params = self.get_smartquota_args
        powerscale_module_mock.get_quota_params = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaThresholds = MagicMock(return_value=None)
        utils.validate_threshold_overhead_parameter = MagicMock(
            return_value=None)
        utils.isi_sdk.QuotaQuota = MagicMock(return_value=None)
        powerscale_module_mock.quota_api_instance.update_quota_quota = MagicMock(
            return_value=None)
        powerscale_module_mock.determine_error = MagicMock(return_value=None)
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_smartquota_create_quota_exception(self, powerscale_module_mock):
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
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.module.params = self.get_smartquota_args
        utils.get_size_bytes = MagicMock(side_effect=[
            MockSmartQuotaApi.get_smartquota_dependent_response("advisory"),
            MockSmartQuotaApi.get_smartquota_dependent_response("hard"),
            MockSmartQuotaApi.get_smartquota_dependent_response("soft")])
        api_response = MagicMock()
        api_response.quotas = None
        powerscale_module_mock.quota_api_instance.list_quota_quotas = MagicMock(
            return_value=api_response)
        utils.validate_threshold_overhead_parameter = MagicMock(
            return_value=None)
        utils.isi_sdk.QuotaQuotaThresholds = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaCreateParams = MagicMock(return_value=None)
        powerscale_module_mock.add_limits_with_unit = MagicMock()
        utils.convert_size_with_unit = MagicMock(return_value=None)
        powerscale_module_mock.quota_api_instance.update_quota_quota = MagicMock()
        utils.isi_sdk.AuthAccessAccessItemFileGroup = MagicMock(
            return_value=[])
        powerscale_module_mock.determine_error = MagicMock(return_value=None)
        powerscale_module_mock.quota_api_instance.create_quota_quota = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(MockSmartQuotaApi.smartquota_create_quota_response(
            path=powerscale_module_mock.module.params.get("path")), invoke_perform_module=True)

    def test_invalid_access_zone_exception(self, powerscale_module_mock):
        self.get_smartquota_args.update({"path": MockSmartQuotaApi.PATH1,
                                         "access_zone": "Sys tem",
                                         "quota_type": "directory",
                                         "state": "present"})
        powerscale_module_mock.module.params = self.get_smartquota_args
        self.capture_fail_json_call(
            "Invalid access_zone provided. Provide valid access_zone", invoke_perform_module=True)

    def test_invalid_path_exception(self, powerscale_module_mock):
        self.get_smartquota_args.update({"path": MockSmartQuotaApi.PATH2,
                                         "access_zone": "System",
                                         "quota_type": "directory",
                                         "state": "present"})
        powerscale_module_mock.module.params = self.get_smartquota_args
        self.capture_fail_json_call(
            "Invalid path provided. Provide valid path.", invoke_perform_module=True)

    def test_create_user_quota(self, powerscale_module_mock):
        self.set_module_params(self.get_smartquota_args, {"path": MockSmartQuotaApi.PATH1,
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
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.auth_api_instance.get_auth_user = MagicMock(
            return_value=MockSmartQuotaApi.get_user_sid())
        get_quota_response = MagicMock()
        get_quota_response.quotas = None
        powerscale_module_mock.quota_api_instance.list_quota_quotas = \
            MagicMock(return_value=get_quota_response)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.quota_api_instance.create_quota_quota. \
            assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] \
            is True

    def test_delete_group_quota(self, powerscale_module_mock):
        self.get_smartquota_args.update({"path": MockSmartQuotaApi.PATH1,
                                         "access_zone": "sample-zone",
                                         "quota_type": "group",
                                         "provider_type": "ldp",
                                         "group_name": "sample-group",
                                         "state": "absent"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.module.params = self.get_smartquota_args
        powerscale_module_mock.auth_api_instance.get_auth_group = MagicMock(
            return_value=MockSmartQuotaApi.get_group_sid())
        powerscale_module_mock.quota_api_instance.list_quota_quotas = \
            MagicMock(return_value=MockSmartQuotaApi.get_group_details())
        powerscale_module_mock.quota_api_instance.delete_quota_quota = \
            MagicMock(return_value=True)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.quota_api_instance.delete_quota_quota. \
            assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] \
            is True

    def test_delete_group_quota_exception(self, powerscale_module_mock):
        self.set_module_params(self.get_smartquota_args,
                               {"path": MockSmartQuotaApi.PATH1,
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
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_zone_base_path = MagicMock(
            return_value="/ifs")
        powerscale_module_mock.auth_api_instance.get_auth_group = MagicMock(
            return_value=MockSmartQuotaApi.get_group_sid())
        powerscale_module_mock.quota_api_instance.list_quota_quotas = \
            MagicMock(return_value=MockSmartQuotaApi.get_group_details())
        powerscale_module_mock.quota_api_instance.delete_quota_quota = \
            MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(MockSmartQuotaApi.smartquota_delete_quota_response(
            path="/ifs%s" % MockSmartQuotaApi.PATH1), invoke_perform_module=True)

    def test_get_sid_exception(self, powerscale_module_mock):
        self.get_smartquota_args.update({"path": MockSmartQuotaApi.PATH1,
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
        powerscale_module_mock.module.params = self.get_smartquota_args
        powerscale_module_mock.auth_api_instance.get_auth_group = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(MockSmartQuotaApi.smartquota_get_sid_exception(name="sample-user",
                                                                                   az="sample-zone",
                                                                                   provider="local"),
                                    invoke_perform_module=True)

    # =========================================================================
    # NEW PARAMETER TESTS — Stage 07 TDD Writer
    # These tests cover FR-001 through FR-011 (missing SmartQuota parameters)
    # =========================================================================

    def test_create_quota_with_description_labels(self, powerscale_module_mock):
        """UT-001: Create quota with description and labels."""
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "directory",
            "description": "Test quota description",
            "labels": "test,prod",
            "quota": {
                "thresholds_on": "fs_logical_size",
                "hard_limit_size": 10,
                "cap_unit": "GB",
                "soft_limit_size": 5,
                "soft_grace_period": 1,
                "period_unit": "days",
                "advisory_limit_size": 3,
                "include_overheads": True,
                "include_snapshots": False,
                "container": False,
            },
            "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_quota_details = MagicMock(
            return_value=(None, None))
        utils.isi_sdk.QuotaQuotaThresholds = MagicMock(return_value=None)
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaCreateParams = MagicMock(return_value=None)
        powerscale_module_mock.quota_api_instance.create_quota_quota = MagicMock(
            return_value=MagicMock())
        powerscale_module_mock.perform_module_operation()
        # Verify create was called and description/labels were included
        create_call_kwargs = utils.isi_sdk.QuotaQuotaCreateParams.call_args
        assert create_call_kwargs is not None
        call_kwargs = create_call_kwargs[1] if create_call_kwargs[1] else {}
        assert call_kwargs.get('description') == "Test quota description"
        assert call_kwargs.get('labels') == "test,prod"
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_create_default_directory_quota(self, powerscale_module_mock):
        """UT-002: Create default-directory type quota."""
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "default-directory",
            "quota": {
                "thresholds_on": "fs_logical_size",
                "hard_limit_size": 10,
                "cap_unit": "GB",
                "include_snapshots": False,
            },
            "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_quota_details = MagicMock(
            return_value=(None, None))
        utils.isi_sdk.QuotaQuotaThresholds = MagicMock(return_value=None)
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaCreateParams = MagicMock(return_value=None)
        powerscale_module_mock.quota_api_instance.create_quota_quota = MagicMock(
            return_value=MagicMock())
        powerscale_module_mock.perform_module_operation()
        create_call_kwargs = utils.isi_sdk.QuotaQuotaCreateParams.call_args
        assert create_call_kwargs is not None
        call_kwargs = create_call_kwargs[1] if create_call_kwargs[1] else {}
        assert call_kwargs.get('type') == "default-directory"
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_create_quota_with_percent_thresholds(self, powerscale_module_mock):
        """UT-003: Create quota with percent_soft and percent_advisory."""
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "directory",
            "force": True,
            "quota": {
                "thresholds_on": "fs_logical_size",
                "hard_limit_size": 10,
                "cap_unit": "GB",
                "percent_soft": 80.0,
                "percent_advisory": 50.0,
                "soft_grace_period": 14,
                "period_unit": "days",
                "include_snapshots": False,
            },
            "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_quota_details = MagicMock(
            return_value=(None, None))
        utils.isi_sdk.QuotaQuotaThresholds = MagicMock(return_value=None)
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaCreateParams = MagicMock(return_value=None)
        powerscale_module_mock.quota_api_instance.create_quota_quota = MagicMock(
            return_value=MagicMock())
        powerscale_module_mock.perform_module_operation()
        threshold_call = utils.isi_sdk.QuotaQuotaThresholds.call_args
        assert threshold_call is not None
        t_kwargs = threshold_call[1] if threshold_call[1] else {}
        assert t_kwargs.get('percent_soft') == 80.0
        assert t_kwargs.get('percent_advisory') == 50.0
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_create_quota_with_force(self, powerscale_module_mock):
        """UT-004: Create quota with force=True."""
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "directory",
            "force": True,
            "quota": {
                "thresholds_on": "fs_logical_size",
                "hard_limit_size": 10,
                "cap_unit": "GB",
                "include_snapshots": False,
            },
            "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_quota_details = MagicMock(
            return_value=(None, None))
        utils.isi_sdk.QuotaQuotaThresholds = MagicMock(return_value=None)
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaCreateParams = MagicMock(return_value=None)
        powerscale_module_mock.quota_api_instance.create_quota_quota = MagicMock(
            return_value=MagicMock())
        powerscale_module_mock.perform_module_operation()
        create_call_kwargs = utils.isi_sdk.QuotaQuotaCreateParams.call_args
        assert create_call_kwargs is not None
        call_kwargs = create_call_kwargs[1] if create_call_kwargs[1] else {}
        assert call_kwargs.get('force') is True
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_update_quota_description_labels(self, powerscale_module_mock):
        """UT-005: Update description and labels on existing quota."""
        import copy
        existing_quota = copy.deepcopy(MockSmartQuotaApi.GET_QUOTA_WITH_NEW_PARAMS)
        existing_quota["description"] = "Old description"
        existing_quota["labels"] = "old"
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "directory",
            "description": "New description",
            "labels": "new,tags",
            "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_quota_details = MagicMock(
            return_value=(existing_quota, existing_quota["id"]))
        utils.isi_sdk.QuotaQuotaThresholds = MagicMock(return_value=None)
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuota = MagicMock(return_value=None)
        powerscale_module_mock.quota_api_instance.update_quota_quota = MagicMock(
            return_value=None)
        utils.convert_size_with_unit = MagicMock(return_value="10.0 GB")
        powerscale_module_mock.perform_module_operation()
        update_call = utils.isi_sdk.QuotaQuota.call_args
        assert update_call is not None
        u_kwargs = update_call[1] if update_call[1] else {}
        assert u_kwargs.get('description') == "New description"
        assert u_kwargs.get('labels') == "new,tags"
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_update_quota_percent_thresholds(self, powerscale_module_mock):
        """UT-006: Update percent_soft and percent_advisory on existing quota."""
        import copy
        existing_quota = copy.deepcopy(MockSmartQuotaApi.GET_QUOTA_WITH_NEW_PARAMS)
        existing_quota["thresholds"]["percent_soft"] = 70.0
        existing_quota["thresholds"]["percent_advisory"] = 40.0
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "directory",
            "quota": {
                "thresholds_on": "fs_logical_size",
                "hard_limit_size": 10,
                "cap_unit": "GB",
                "percent_soft": 85.0,
                "percent_advisory": 55.0,
                "soft_grace_period": 14,
                "period_unit": "days",
                "include_snapshots": False,
            },
            "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_quota_details = MagicMock(
            return_value=(existing_quota, existing_quota["id"]))
        utils.isi_sdk.QuotaQuotaThresholds = MagicMock(return_value=None)
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuota = MagicMock(return_value=None)
        powerscale_module_mock.quota_api_instance.update_quota_quota = MagicMock(
            return_value=None)
        utils.convert_size_with_unit = MagicMock(return_value="10.0 GB")
        powerscale_module_mock.perform_module_operation()
        threshold_call = utils.isi_sdk.QuotaQuotaThresholds.call_args
        assert threshold_call is not None
        t_kwargs = threshold_call[1] if threshold_call[1] else {}
        assert t_kwargs.get('percent_soft') == 85.0
        assert t_kwargs.get('percent_advisory') == 55.0
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_idempotency_description_no_change(self, powerscale_module_mock):
        """UT-007: Same description should result in changed=False."""
        import copy
        existing_quota = copy.deepcopy(MockSmartQuotaApi.GET_QUOTA_WITH_NEW_PARAMS)
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "directory",
            "description": "Test quota description",
            "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_quota_details = MagicMock(
            return_value=(existing_quota, existing_quota["id"]))
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        utils.convert_size_with_unit = MagicMock(return_value="10.0 GB")
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is False

    def test_idempotency_labels_no_change(self, powerscale_module_mock):
        """UT-008: Same labels should result in changed=False."""
        import copy
        existing_quota = copy.deepcopy(MockSmartQuotaApi.GET_QUOTA_WITH_NEW_PARAMS)
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "directory",
            "labels": "test,prod",
            "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_quota_details = MagicMock(
            return_value=(existing_quota, existing_quota["id"]))
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        utils.convert_size_with_unit = MagicMock(return_value="10.0 GB")
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is False

    def test_idempotency_percent_thresholds_no_change(self, powerscale_module_mock):
        """UT-009: Same percent_soft/percent_advisory should result in changed=False."""
        import copy
        existing_quota = copy.deepcopy(MockSmartQuotaApi.GET_QUOTA_WITH_NEW_PARAMS)
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "directory",
            "quota": {
                "thresholds_on": "fs_logical_size",
                "hard_limit_size": 10,
                "cap_unit": "GB",
                "percent_soft": 80.0,
                "percent_advisory": 50.0,
                "soft_grace_period": 1,
                "period_unit": "days",
                "include_snapshots": False,
            },
            "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_quota_details = MagicMock(
            return_value=(existing_quota, existing_quota["id"]))
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        utils.convert_size_with_unit = MagicMock(return_value="10.0 GB")
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is False

    def test_check_mode_create_with_new_params(self, powerscale_module_mock):
        """UT-010: Check mode correctly reports changed state with new params."""
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "directory",
            "description": "Check mode test",
            "labels": "check",
            "force": True,
            "quota": {
                "thresholds_on": "fs_logical_size",
                "hard_limit_size": 10,
                "cap_unit": "GB",
                "percent_soft": 80.0,
                "percent_advisory": 50.0,
                "soft_grace_period": 14,
                "period_unit": "days",
                "include_snapshots": False,
            },
            "state": "present"})
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.get_quota_details = MagicMock(
            return_value=(None, None))
        utils.isi_sdk.QuotaQuotaThresholds = MagicMock(return_value=None)
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaCreateParams = MagicMock(return_value=None)
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        # Verify create API was NOT called in check mode
        powerscale_module_mock.quota_api_instance.create_quota_quota.assert_not_called()

    def test_create_quota_with_all_new_params(self, powerscale_module_mock):
        """UT-011: Create with all 6 new params simultaneously."""
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "default-directory",
            "description": "Full test",
            "labels": "all,params",
            "force": True,
            "quota": {
                "thresholds_on": "fs_logical_size",
                "hard_limit_size": 10,
                "cap_unit": "GB",
                "percent_soft": 80.0,
                "percent_advisory": 50.0,
                "soft_grace_period": 14,
                "period_unit": "days",
                "include_snapshots": False,
            },
            "state": "present"})
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.get_quota_details = MagicMock(
            return_value=(None, None))
        utils.isi_sdk.QuotaQuotaThresholds = MagicMock(return_value=None)
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaCreateParams = MagicMock(return_value=None)
        powerscale_module_mock.quota_api_instance.create_quota_quota = MagicMock(
            return_value=MagicMock())
        powerscale_module_mock.perform_module_operation()
        create_call = utils.isi_sdk.QuotaQuotaCreateParams.call_args
        assert create_call is not None
        ck = create_call[1] if create_call[1] else {}
        assert ck.get('type') == "default-directory"
        assert ck.get('description') == "Full test"
        assert ck.get('labels') == "all,params"
        assert ck.get('force') is True
        tk = utils.isi_sdk.QuotaQuotaThresholds.call_args
        assert tk is not None
        tkw = tk[1] if tk[1] else {}
        assert tkw.get('percent_soft') == 80.0
        assert tkw.get('percent_advisory') == 50.0
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_description_exceeds_max_length(self, powerscale_module_mock):
        """UT-014: description > 1024 chars should be rejected."""
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "directory",
            "description": "a" * 1025,
            "state": "present"})
        powerscale_module_mock.module.check_mode = False
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        self.capture_fail_json_call(
            "exceeds maximum length", invoke_perform_module=True)

    def test_labels_exceeds_max_length(self, powerscale_module_mock):
        """UT-015: labels > 1024 chars should be rejected."""
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "directory",
            "labels": "a" * 1025,
            "state": "present"})
        powerscale_module_mock.module.check_mode = False
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        self.capture_fail_json_call(
            "exceeds maximum length", invoke_perform_module=True)

    def test_percent_soft_below_minimum(self, powerscale_module_mock):
        """UT-016: percent_soft < 0.01 should be rejected."""
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "directory",
            "quota": {
                "percent_soft": 0.001,
                "hard_limit_size": 10,
                "cap_unit": "GB",
                "include_snapshots": False,
            },
            "state": "present"})
        powerscale_module_mock.module.check_mode = False
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        self.capture_fail_json_call(
            "must be between 0.01 and 99.99", invoke_perform_module=True)

    def test_percent_soft_above_maximum(self, powerscale_module_mock):
        """UT-017: percent_soft > 99.99 should be rejected."""
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "directory",
            "quota": {
                "percent_soft": 100.0,
                "hard_limit_size": 10,
                "cap_unit": "GB",
                "include_snapshots": False,
            },
            "state": "present"})
        powerscale_module_mock.module.check_mode = False
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        self.capture_fail_json_call(
            "must be between 0.01 and 99.99", invoke_perform_module=True)

    def test_percent_advisory_below_minimum(self, powerscale_module_mock):
        """UT-018: percent_advisory < 0.01 should be rejected."""
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "directory",
            "quota": {
                "percent_advisory": 0.001,
                "hard_limit_size": 10,
                "cap_unit": "GB",
                "include_snapshots": False,
            },
            "state": "present"})
        powerscale_module_mock.module.check_mode = False
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        self.capture_fail_json_call(
            "must be between 0.01 and 99.99", invoke_perform_module=True)

    def test_percent_advisory_above_maximum(self, powerscale_module_mock):
        """UT-019: percent_advisory > 99.99 should be rejected."""
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "directory",
            "quota": {
                "percent_advisory": 100.0,
                "hard_limit_size": 10,
                "cap_unit": "GB",
                "include_snapshots": False,
            },
            "state": "present"})
        powerscale_module_mock.module.check_mode = False
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        self.capture_fail_json_call(
            "must be between 0.01 and 99.99", invoke_perform_module=True)

    def test_percent_soft_without_hard_limit(self, powerscale_module_mock):
        """UT-020: percent_soft without hard_limit_size should be rejected."""
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "directory",
            "quota": {
                "percent_soft": 80.0,
                "include_snapshots": False,
            },
            "state": "present"})
        powerscale_module_mock.module.check_mode = False
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        self.capture_fail_json_call(
            "requires hard_limit_size to be set", invoke_perform_module=True)

    def test_percent_advisory_without_hard_limit(self, powerscale_module_mock):
        """UT-021: percent_advisory without hard_limit_size should be rejected."""
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "directory",
            "quota": {
                "percent_advisory": 50.0,
                "include_snapshots": False,
            },
            "state": "present"})
        powerscale_module_mock.module.check_mode = False
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        self.capture_fail_json_call(
            "requires hard_limit_size to be set", invoke_perform_module=True)

    def test_default_directory_with_user_name_rejected(self, powerscale_module_mock):
        """UT-022: default-directory with user_name should be rejected."""
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "default-directory",
            "user_name": "testuser",
            "state": "present"})
        powerscale_module_mock.module.check_mode = False
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        self.capture_fail_json_call(
            "not required", invoke_perform_module=True)

    def test_default_directory_with_group_name_rejected(self, powerscale_module_mock):
        """UT-023: default-directory with group_name should be rejected."""
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "default-directory",
            "group_name": "testgroup",
            "state": "present"})
        powerscale_module_mock.module.check_mode = False
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        self.capture_fail_json_call(
            "not required", invoke_perform_module=True)

    def test_create_default_directory_quota_exception(self, powerscale_module_mock):
        """UT-027: SDK ApiException on default-directory create."""
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1,
            "access_zone": "System",
            "quota_type": "default-directory",
            "quota": {
                "thresholds_on": "fs_logical_size",
                "hard_limit_size": 10,
                "cap_unit": "GB",
                "include_snapshots": False,
            },
            "state": "present"})
        powerscale_module_mock.module.check_mode = False
        api_response = MagicMock()
        api_response.quotas = None
        powerscale_module_mock.quota_api_instance.list_quota_quotas = MagicMock(
            return_value=api_response)
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaThresholds = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaCreateParams = MagicMock(return_value=None)
        utils.get_size_bytes = MagicMock(return_value=10737418240.0)
        powerscale_module_mock.quota_api_instance.create_quota_quota = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(
            MockSmartQuotaApi.smartquota_create_quota_response(
                path=MockSmartQuotaApi.PATH1),
            invoke_perform_module=True)
