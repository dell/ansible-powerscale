# Copyright: (c) 2022-2026, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for smartquota module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import copy
import pytest
from mock.mock import MagicMock, PropertyMock
from ansible.module_utils.common.arg_spec import ArgumentSpecValidator
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils


from ansible_collections.dellemc.powerscale.plugins.modules.smartquota import SmartQuota, \
    get_smartquota_parameters
from ansible_collections.dellemc.powerscale.tests.unit.plugins. \
    module_utils.mock_smartquota_api import MockSmartQuotaApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase


class TestSmartQuota(PowerScaleUnitBase):
    get_smartquota_args = MockSmartQuotaApi.SMART_QUOTA_COMMON_ARGS

    @pytest.fixture(autouse=True)
    def reset_smartquota_args(self):
        # `get_smartquota_args` is a class-level dict mutated in-place via
        # `.update()` by many tests below. Without resetting it per test,
        # keys set by one test (e.g. user_name/group_name/provider_type)
        # silently leak into later tests that don't set/clear them,
        # producing order-dependent failures. Give each test its own
        # isolated copy, shadowing the class attribute on the instance.
        self.get_smartquota_args = copy.deepcopy(
            MockSmartQuotaApi.SMART_QUOTA_COMMON_ARGS)

    @pytest.fixture(autouse=True)
    def default_diff_mode(self, powerscale_module_mock):
        # `powerscale_module_mock.module` is a bare MagicMock, so accessing
        # `.module._diff` (unset by the shared base fixture, unlike
        # `.module.check_mode`) auto-vivifies a truthy child MagicMock.
        # That would make every test exercise the new diff-mode code path
        # in perform_module_operation, changing call signatures asserted
        # by pre-existing tests. Default it to False here; diff-mode tests
        # override it explicitly to True.
        powerscale_module_mock.module._diff = False

    @pytest.fixture
    def module_object(self, mocker):
        # utils.isi_sdk is a single shared MagicMock (see initial_mock.py).
        # Because MagicMock auto-caches child attributes/return_values, API
        # instances such as utils.isi_sdk.QuotaApi(...).return_value are the
        # SAME object across every SmartQuota instance unless reset here.
        # Without this, a mutation like `quota_api_instance.create_quota_quota
        # = MagicMock(side_effect=...)` in one test silently leaks into every
        # test that runs afterwards in this file. Reset before every test,
        # before SmartQuota() (and its SDK API instances) is constructed.
        # Scoped to this test module only to avoid affecting other modules'
        # test fixtures that may rely on isi_sdk state set up elsewhere.
        utils.isi_sdk = MagicMock()
        type(utils.isi_sdk).major = PropertyMock(return_value=9)
        type(utils.isi_sdk).minor = PropertyMock(return_value=7)
        utils.get_size_bytes = MagicMock(return_value=10737418240.0)
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
        utils.get_size_bytes = MagicMock(return_value=10737418240.0)
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
        utils.get_size_bytes = MagicMock(return_value=10737418240.0)
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

    def test_smartquota_create_quota_exception(self, powerscale_module_mock, mocker):
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
        mocker.patch('ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock.utils.get_size_bytes', side_effect=[
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
        mocker.patch('ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock.utils.convert_size_with_unit', return_value=None)
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

    def _mock_perform_module_operation_internals(self, powerscale_module_mock, quota_details, quota_id):
        """Common wiring-test setup: stub out already-tested internals."""
        powerscale_module_mock._prepare_quota_parameters = MagicMock(return_value=(
            "directory", None, None, "present", "System", MockSmartQuotaApi.PATH1, None, None, False))
        powerscale_module_mock._validate_quota_type_params = MagicMock()
        powerscale_module_mock.validate_quota_cap_unit = MagicMock()
        powerscale_module_mock.get_quota_details = MagicMock(return_value=(quota_details, quota_id))
        powerscale_module_mock._handle_quota_creation = MagicMock(return_value=True)
        powerscale_module_mock._handle_quota_update = MagicMock(return_value=False)
        powerscale_module_mock._handle_quota_deletion = MagicMock(return_value=True)
        powerscale_module_mock._process_final_quota_details = MagicMock(return_value={"id": quota_id})
        powerscale_module_mock.reconcile_quota_notification_rules = MagicMock(return_value=True)

    def test_perform_module_operation_reconciles_notifications_for_existing_quota(self, powerscale_module_mock):
        """When the quota already exists, notification reconciliation uses its known id."""
        powerscale_module_mock.module.check_mode = False
        self._mock_perform_module_operation_internals(
            powerscale_module_mock, {"id": self.QUOTA_ID}, self.QUOTA_ID)
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1, "quota_type": "directory", "state": "present",
            "quota_notification_rules": [{"condition": "exceeded", "threshold": "advisory", "action_alert": True}]})
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.reconcile_quota_notification_rules.assert_called_once_with(
            self.QUOTA_ID, [{"condition": "exceeded", "threshold": "advisory", "action_alert": True}])
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_perform_module_operation_reconciles_notifications_after_create(self, powerscale_module_mock):
        """When the quota is newly created, the freshly resolved id is used for reconciliation."""
        powerscale_module_mock.module.check_mode = False
        self._mock_perform_module_operation_internals(powerscale_module_mock, None, None)
        powerscale_module_mock.get_quota_details = MagicMock(side_effect=[
            (None, None), (dict(id=self.QUOTA_ID), self.QUOTA_ID)])
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1, "quota_type": "directory", "state": "present",
            "quota_notification_rules": [{"condition": "exceeded", "threshold": "advisory", "action_alert": True}]})
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.reconcile_quota_notification_rules.assert_called_once_with(
            self.QUOTA_ID, [{"condition": "exceeded", "threshold": "advisory", "action_alert": True}])

    def test_perform_module_operation_skips_reconciliation_when_param_absent(self, powerscale_module_mock):
        """Existing playbooks without quota_notification_rules are unaffected (NFR-1)."""
        powerscale_module_mock.module.check_mode = False
        self._mock_perform_module_operation_internals(
            powerscale_module_mock, {"id": self.QUOTA_ID}, self.QUOTA_ID)
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1, "quota_type": "directory", "state": "present",
            "quota_notification_rules": None})
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.reconcile_quota_notification_rules.assert_not_called()

    def test_perform_module_operation_skips_reconciliation_new_quota_check_mode(self, powerscale_module_mock):
        """A brand-new quota's notifications cannot be reconciled under check_mode (no id yet)."""
        powerscale_module_mock.module.check_mode = True
        self._mock_perform_module_operation_internals(powerscale_module_mock, None, None)
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1, "quota_type": "directory", "state": "present",
            "quota_notification_rules": [{"condition": "exceeded", "threshold": "advisory", "action_alert": True}]})
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.reconcile_quota_notification_rules.assert_not_called()

    def test_final_quota_details_includes_notification_rules(self, powerscale_module_mock):
        """The final quota details output includes the current notification rules."""
        powerscale_module_mock.get_quota_details = MagicMock(
            return_value=(dict(MockSmartQuotaApi.GET_QUOTA_WITH_NEW_PARAMS), self.QUOTA_ID))
        powerscale_module_mock.list_quota_notification_rules = MagicMock(
            return_value=[MockSmartQuotaApi.NOTIFICATION_RULE_1])
        result = powerscale_module_mock._process_final_quota_details(
            "directory", None, None, False, "System", MockSmartQuotaApi.PATH1, None)
        assert result['notification_rules'] == [MockSmartQuotaApi.NOTIFICATION_RULE_1]
        powerscale_module_mock.list_quota_notification_rules.assert_called_once_with(self.QUOTA_ID)

    def test_final_quota_details_no_quota_skips_notification_lookup(self, powerscale_module_mock):
        """When the quota does not exist, notification rules are not looked up."""
        powerscale_module_mock.get_quota_details = MagicMock(return_value=(None, None))
        powerscale_module_mock.list_quota_notification_rules = MagicMock()
        result = powerscale_module_mock._process_final_quota_details(
            "directory", None, None, False, "System", MockSmartQuotaApi.PATH1, None)
        assert result is None
        powerscale_module_mock.list_quota_notification_rules.assert_not_called()

    def test_reconcile_notification_rules_all_new(self, powerscale_module_mock):
        """All-new rules (no id) are created; changed is True."""
        powerscale_module_mock.list_quota_notification_rules = MagicMock(return_value=[])
        powerscale_module_mock.create_quota_notification_rule = MagicMock(return_value="rule-new")
        powerscale_module_mock.update_quota_notification_rule = MagicMock()
        powerscale_module_mock.delete_quota_notification_rule = MagicMock()
        powerscale_module_mock.delete_all_quota_notification_rules = MagicMock()
        desired = [{"condition": "exceeded", "threshold": "advisory", "action_alert": True, "holdoff": 3600, "state": "present"}]
        changed = powerscale_module_mock.reconcile_quota_notification_rules(self.QUOTA_ID, desired)
        assert changed is True
        powerscale_module_mock.create_quota_notification_rule.assert_called_once_with(self.QUOTA_ID, desired[0])
        powerscale_module_mock.update_quota_notification_rule.assert_not_called()
        powerscale_module_mock.delete_quota_notification_rule.assert_not_called()

    def test_reconcile_notification_rules_partial_overlap(self, powerscale_module_mock):
        """One rule updates (action field), one is deleted (state absent), one is created."""
        powerscale_module_mock.list_quota_notification_rules = MagicMock(return_value=[
            dict(MockSmartQuotaApi.NOTIFICATION_RULE_1),
            dict(MockSmartQuotaApi.NOTIFICATION_RULE_2)
        ])
        powerscale_module_mock.create_quota_notification_rule = MagicMock(return_value="rule-0003")
        powerscale_module_mock.update_quota_notification_rule = MagicMock(return_value=True)
        powerscale_module_mock.delete_quota_notification_rule = MagicMock(return_value=True)
        powerscale_module_mock.delete_all_quota_notification_rules = MagicMock()
        desired = [
            {"id": "rule-0001", "action_alert": False, "state": "present"},
            {"id": "rule-0002", "state": "absent"},
            {"condition": "violated", "threshold": "soft", "action_email_owner": True, "state": "present"}
        ]
        changed = powerscale_module_mock.reconcile_quota_notification_rules(self.QUOTA_ID, desired)
        assert changed is True
        powerscale_module_mock.update_quota_notification_rule.assert_called_once_with(
            self.QUOTA_ID, "rule-0001", desired[0])
        powerscale_module_mock.delete_quota_notification_rule.assert_called_once_with(
            self.QUOTA_ID, "rule-0002")
        powerscale_module_mock.create_quota_notification_rule.assert_called_once_with(
            self.QUOTA_ID, desired[2])

    def test_reconcile_notification_rules_exact_match_no_op(self, powerscale_module_mock):
        """Requested rules matching current state exactly result in no API calls."""
        powerscale_module_mock.list_quota_notification_rules = MagicMock(return_value=[
            dict(MockSmartQuotaApi.NOTIFICATION_RULE_1)
        ])
        powerscale_module_mock.create_quota_notification_rule = MagicMock()
        powerscale_module_mock.update_quota_notification_rule = MagicMock()
        powerscale_module_mock.delete_quota_notification_rule = MagicMock()
        powerscale_module_mock.delete_all_quota_notification_rules = MagicMock()
        desired = [{
            "id": "rule-0001", "condition": "exceeded", "threshold": "advisory",
            "action_alert": True, "action_email_owner": False, "action_email_address": None,
            "state": "present"
        }]
        changed = powerscale_module_mock.reconcile_quota_notification_rules(self.QUOTA_ID, desired)
        assert changed is False
        powerscale_module_mock.create_quota_notification_rule.assert_not_called()
        powerscale_module_mock.update_quota_notification_rule.assert_not_called()
        powerscale_module_mock.delete_quota_notification_rule.assert_not_called()

    def test_reconcile_notification_rules_empty_list_deletes_all(self, powerscale_module_mock):
        """An empty quota_notification_rules list deletes all existing rules."""
        powerscale_module_mock.list_quota_notification_rules = MagicMock(return_value=[
            dict(MockSmartQuotaApi.NOTIFICATION_RULE_1),
            dict(MockSmartQuotaApi.NOTIFICATION_RULE_2)
        ])
        powerscale_module_mock.delete_all_quota_notification_rules = MagicMock(return_value=True)
        powerscale_module_mock.create_quota_notification_rule = MagicMock()
        powerscale_module_mock.update_quota_notification_rule = MagicMock()
        powerscale_module_mock.delete_quota_notification_rule = MagicMock()
        changed = powerscale_module_mock.reconcile_quota_notification_rules(self.QUOTA_ID, [])
        assert changed is True
        powerscale_module_mock.delete_all_quota_notification_rules.assert_called_once_with(self.QUOTA_ID)

    def test_reconcile_notification_rules_empty_list_no_op_when_already_empty(self, powerscale_module_mock):
        """An empty quota_notification_rules list is a no-op when no rules currently exist."""
        powerscale_module_mock.list_quota_notification_rules = MagicMock(return_value=[])
        powerscale_module_mock.delete_all_quota_notification_rules = MagicMock()
        changed = powerscale_module_mock.reconcile_quota_notification_rules(self.QUOTA_ID, [])
        assert changed is False
        powerscale_module_mock.delete_all_quota_notification_rules.assert_not_called()

    def test_reconcile_notification_rules_condition_change_deletes_and_recreates(self, powerscale_module_mock):
        """Changing condition/threshold on an existing rule deletes and recreates it."""
        powerscale_module_mock.list_quota_notification_rules = MagicMock(return_value=[
            dict(MockSmartQuotaApi.NOTIFICATION_RULE_1)
        ])
        powerscale_module_mock.create_quota_notification_rule = MagicMock(return_value="rule-0003")
        powerscale_module_mock.update_quota_notification_rule = MagicMock()
        powerscale_module_mock.delete_quota_notification_rule = MagicMock(return_value=True)
        desired = [{
            "id": "rule-0001", "condition": "exceeded", "threshold": "hard",
            "action_alert": True, "state": "present"
        }]
        changed = powerscale_module_mock.reconcile_quota_notification_rules(self.QUOTA_ID, desired)
        assert changed is True
        powerscale_module_mock.delete_quota_notification_rule.assert_called_once_with(self.QUOTA_ID, "rule-0001")
        powerscale_module_mock.create_quota_notification_rule.assert_called_once_with(self.QUOTA_ID, desired[0])
        powerscale_module_mock.update_quota_notification_rule.assert_not_called()

    def test_reconcile_notification_rules_absent_unknown_id_fails(self, powerscale_module_mock):
        """Deleting a rule id that doesn't currently exist fails with a descriptive error (FR-12)."""
        powerscale_module_mock.list_quota_notification_rules = MagicMock(return_value=[])
        powerscale_module_mock.delete_quota_notification_rule = MagicMock()
        desired = [{"id": "rule-unknown", "state": "absent"}]
        self.capture_fail_json_method(
            "Notification rule with id rule-unknown does not exist for quota %s" % self.QUOTA_ID,
            powerscale_module_mock, 'reconcile_quota_notification_rules', self.QUOTA_ID, desired)
        powerscale_module_mock.delete_quota_notification_rule.assert_not_called()

    def test_reconcile_notification_rules_update_unknown_id_fails(self, powerscale_module_mock):
        """Updating a rule id that doesn't currently exist fails with a descriptive error (FR-12)."""
        powerscale_module_mock.list_quota_notification_rules = MagicMock(return_value=[])
        powerscale_module_mock.create_quota_notification_rule = MagicMock()
        desired = [{"id": "rule-unknown", "action_alert": True, "state": "present"}]
        self.capture_fail_json_method(
            "Notification rule with id rule-unknown does not exist for quota %s" % self.QUOTA_ID,
            powerscale_module_mock, 'reconcile_quota_notification_rules', self.QUOTA_ID, desired)
        powerscale_module_mock.create_quota_notification_rule.assert_not_called()

    def test_reconcile_notification_rules_check_mode_create_makes_no_write_call(self, powerscale_module_mock):
        """FR-8: under check_mode, a new-rule create computes changed=True
        without any create/update/delete API call (only the read-only list
        GET call, common to both modes, is made)."""
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.quota_api_instance.api_client.call_api = MagicMock(
            return_value=MockSmartQuotaApi.get_no_notification_rules_response())
        desired = [{"condition": "exceeded", "threshold": "advisory", "action_alert": True, "state": "present"}]
        changed = powerscale_module_mock.reconcile_quota_notification_rules(self.QUOTA_ID, desired)
        assert changed is True
        # Only the GET (list) call is made; no POST/PUT/DELETE happens.
        powerscale_module_mock.quota_api_instance.api_client.call_api.assert_called_once()
        called_method = powerscale_module_mock.quota_api_instance.api_client.call_api.call_args[0][1]
        assert called_method == 'GET'

    def test_reconcile_notification_rules_check_mode_update_makes_no_write_call(self, powerscale_module_mock):
        """FR-8: under check_mode, updating an existing rule computes
        changed=True without any create/update/delete API call."""
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.quota_api_instance.api_client.call_api = MagicMock(
            return_value=MockSmartQuotaApi.get_single_notification_rule_response())
        desired = [{"id": "rule-0001", "action_alert": False, "state": "present"}]
        changed = powerscale_module_mock.reconcile_quota_notification_rules(self.QUOTA_ID, desired)
        assert changed is True
        powerscale_module_mock.quota_api_instance.api_client.call_api.assert_called_once()
        called_method = powerscale_module_mock.quota_api_instance.api_client.call_api.call_args[0][1]
        assert called_method == 'GET'

    def test_reconcile_notification_rules_check_mode_delete_makes_no_write_call(self, powerscale_module_mock):
        """FR-8: under check_mode, deleting a rule computes changed=True
        without any create/update/delete API call."""
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.quota_api_instance.api_client.call_api = MagicMock(
            return_value=MockSmartQuotaApi.get_single_notification_rule_response())
        desired = [{"id": "rule-0001", "state": "absent"}]
        changed = powerscale_module_mock.reconcile_quota_notification_rules(self.QUOTA_ID, desired)
        assert changed is True
        powerscale_module_mock.quota_api_instance.api_client.call_api.assert_called_once()
        called_method = powerscale_module_mock.quota_api_instance.api_client.call_api.call_args[0][1]
        assert called_method == 'GET'

    def test_reconcile_notification_rules_check_mode_delete_all_makes_no_write_call(self, powerscale_module_mock):
        """FR-8: under check_mode, deleting all rules computes changed=True
        without any create/update/delete API call."""
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.quota_api_instance.api_client.call_api = MagicMock(
            return_value=MockSmartQuotaApi.get_multiple_notification_rules_response())
        changed = powerscale_module_mock.reconcile_quota_notification_rules(self.QUOTA_ID, [])
        assert changed is True
        powerscale_module_mock.quota_api_instance.api_client.call_api.assert_called_once()
        called_method = powerscale_module_mock.quota_api_instance.api_client.call_api.call_args[0][1]
        assert called_method == 'GET'

    def test_reconcile_notification_rules_diff_create(self, powerscale_module_mock):
        """FR-9: diff.before/after accurately reflect a rule creation."""
        powerscale_module_mock.list_quota_notification_rules = MagicMock(return_value=[])
        powerscale_module_mock.create_quota_notification_rule = MagicMock(return_value="rule-new")
        desired = [{"condition": "exceeded", "threshold": "advisory", "action_alert": True, "state": "present"}]
        diff_dict = {}
        changed = powerscale_module_mock.reconcile_quota_notification_rules(
            self.QUOTA_ID, desired, diff_dict=diff_dict)
        assert changed is True
        assert diff_dict['before'] == []
        assert diff_dict['after'] == [dict(desired[0], id="rule-new")]

    def test_reconcile_notification_rules_diff_update(self, powerscale_module_mock):
        """FR-9: diff.before/after accurately reflect a rule update."""
        powerscale_module_mock.list_quota_notification_rules = MagicMock(
            return_value=[dict(MockSmartQuotaApi.NOTIFICATION_RULE_1)])
        powerscale_module_mock.update_quota_notification_rule = MagicMock(return_value=True)
        desired = [{"id": "rule-0001", "action_alert": False, "state": "present"}]
        diff_dict = {}
        changed = powerscale_module_mock.reconcile_quota_notification_rules(
            self.QUOTA_ID, desired, diff_dict=diff_dict)
        assert changed is True
        assert diff_dict['before'] == [dict(MockSmartQuotaApi.NOTIFICATION_RULE_1)]
        assert diff_dict['after'][0]['action_alert'] is False
        assert diff_dict['after'][0]['id'] == "rule-0001"

    def test_reconcile_notification_rules_diff_delete(self, powerscale_module_mock):
        """FR-9: diff.before/after accurately reflect a rule deletion."""
        powerscale_module_mock.list_quota_notification_rules = MagicMock(
            return_value=[dict(MockSmartQuotaApi.NOTIFICATION_RULE_1)])
        powerscale_module_mock.delete_quota_notification_rule = MagicMock(return_value=True)
        desired = [{"id": "rule-0001", "state": "absent"}]
        diff_dict = {}
        changed = powerscale_module_mock.reconcile_quota_notification_rules(
            self.QUOTA_ID, desired, diff_dict=diff_dict)
        assert changed is True
        assert diff_dict['before'] == [dict(MockSmartQuotaApi.NOTIFICATION_RULE_1)]
        assert diff_dict['after'] == []

    def test_reconcile_notification_rules_diff_delete_all(self, powerscale_module_mock):
        """FR-9: diff.before/after accurately reflect deleting all rules."""
        powerscale_module_mock.list_quota_notification_rules = MagicMock(return_value=[
            dict(MockSmartQuotaApi.NOTIFICATION_RULE_1), dict(MockSmartQuotaApi.NOTIFICATION_RULE_2)])
        powerscale_module_mock.delete_all_quota_notification_rules = MagicMock(return_value=True)
        diff_dict = {}
        changed = powerscale_module_mock.reconcile_quota_notification_rules(
            self.QUOTA_ID, [], diff_dict=diff_dict)
        assert changed is True
        assert len(diff_dict['before']) == 2
        assert diff_dict['after'] == []

    def test_reconcile_notification_rules_diff_no_op(self, powerscale_module_mock):
        """FR-9: diff.before/after are equal when there is no effective change."""
        powerscale_module_mock.list_quota_notification_rules = MagicMock(
            return_value=[dict(MockSmartQuotaApi.NOTIFICATION_RULE_1)])
        desired = [{
            "id": "rule-0001", "condition": "exceeded", "threshold": "advisory",
            "action_alert": True, "action_email_owner": False, "action_email_address": None,
            "state": "present"
        }]
        diff_dict = {}
        changed = powerscale_module_mock.reconcile_quota_notification_rules(
            self.QUOTA_ID, desired, diff_dict=diff_dict)
        assert changed is False
        assert diff_dict['before'] == diff_dict['after']

    def test_perform_module_operation_includes_diff_when_diff_mode_enabled(self, powerscale_module_mock):
        """FR-9: perform_module_operation surfaces diff.before/after in the result when --diff is used."""
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.module._diff = True
        self._mock_perform_module_operation_internals(
            powerscale_module_mock, {"id": self.QUOTA_ID}, self.QUOTA_ID)

        def fake_reconcile(quota_id, rules, diff_dict=None):
            if diff_dict is not None:
                diff_dict['before'] = []
                diff_dict['after'] = [dict(rules[0], id="rule-new")]
            return True
        powerscale_module_mock.reconcile_quota_notification_rules = MagicMock(side_effect=fake_reconcile)
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1, "quota_type": "directory", "state": "present",
            "quota_notification_rules": [{"condition": "exceeded", "threshold": "advisory", "action_alert": True}]})
        powerscale_module_mock.perform_module_operation()
        result_kwargs = powerscale_module_mock.module.exit_json.call_args[1]
        assert result_kwargs["diff"]["before"] == []
        assert result_kwargs["diff"]["after"][0]["id"] == "rule-new"

    def test_perform_module_operation_omits_diff_when_diff_mode_disabled(self, powerscale_module_mock):
        """When --diff is not used, no diff key is added to the result."""
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.module._diff = False
        self._mock_perform_module_operation_internals(
            powerscale_module_mock, {"id": self.QUOTA_ID}, self.QUOTA_ID)
        self.set_module_params(self.get_smartquota_args, {
            "path": MockSmartQuotaApi.PATH1, "quota_type": "directory", "state": "present",
            "quota_notification_rules": [{"condition": "exceeded", "threshold": "advisory", "action_alert": True}]})
        powerscale_module_mock.perform_module_operation()
        result_kwargs = powerscale_module_mock.module.exit_json.call_args[1]
        assert "diff" not in result_kwargs

    def test_quota_notification_rules_argument_spec(self):
        """The argument spec exposes quota_notification_rules with the expected suboptions."""
        params = get_smartquota_parameters()
        assert 'quota_notification_rules' in params
        spec = params['quota_notification_rules']
        assert spec['type'] == 'list'
        assert spec['elements'] == 'dict'
        options = spec['options']
        assert options['id']['type'] == 'str'
        assert options['condition']['choices'] == ['exceeded', 'denied', 'violated', 'expired']
        assert options['threshold']['choices'] == ['hard', 'soft', 'advisory']
        assert options['action_alert']['type'] == 'bool'
        assert options['action_email_owner']['type'] == 'bool'
        assert options['action_email_address']['type'] == 'list'
        assert options['action_email_address']['elements'] == 'str'
        assert options['holdoff']['type'] == 'int'
        assert options['state']['choices'] == ['present', 'absent']
        assert options['state']['default'] == 'present'

    def test_reconcile_notification_rules_with_holdoff(self, powerscale_module_mock):
        """Notification rules with holdoff parameter are created correctly."""
        powerscale_module_mock.list_quota_notification_rules = MagicMock(return_value=[])
        powerscale_module_mock.create_quota_notification_rule = MagicMock(return_value="rule-new")
        powerscale_module_mock.update_quota_notification_rule = MagicMock()
        powerscale_module_mock.delete_quota_notification_rule = MagicMock()
        powerscale_module_mock.delete_all_quota_notification_rules = MagicMock()
        desired = [{"condition": "exceeded", "threshold": "hard", "action_alert": True, "holdoff": 3600, "state": "present"}]
        changed = powerscale_module_mock.reconcile_quota_notification_rules(self.QUOTA_ID, desired)
        assert changed is True
        powerscale_module_mock.create_quota_notification_rule.assert_called_once_with(self.QUOTA_ID, desired[0])
        # Verify holdoff is included in the call
        call_args = powerscale_module_mock.create_quota_notification_rule.call_args[0]
        assert call_args[1]['holdoff'] == 3600

    def test_invalid_condition_choice_fails_argument_spec_validation(self):
        """FR-10: an out-of-choices `condition` value fails argument-spec
        validation, which Ansible performs inside AnsibleModule.__init__
        before any module code (and thus before any API call) executes.
        Validated directly against the real argument_spec via
        ArgumentSpecValidator, independent of any AnsibleModule mocking
        elsewhere in this test suite (see initial_mock.py, which globally
        replaces ansible.module_utils.basic.AnsibleModule for other tests)."""
        params = {"quota_notification_rules": [
            {"condition": "not-a-real-condition", "threshold": "advisory", "action_alert": True}]}
        result = ArgumentSpecValidator(get_smartquota_parameters()).validate(params)
        assert result.error_messages
        assert any("condition" in msg for msg in result.error_messages)

    def test_invalid_threshold_choice_fails_argument_spec_validation(self):
        """FR-10: an out-of-choices `threshold` value fails argument-spec
        validation before any module code executes."""
        params = {"quota_notification_rules": [
            {"condition": "exceeded", "threshold": "not-a-real-threshold", "action_alert": True}]}
        result = ArgumentSpecValidator(get_smartquota_parameters()).validate(params)
        assert result.error_messages
        assert any("threshold" in msg for msg in result.error_messages)

    def test_valid_condition_and_threshold_choices_pass_argument_spec_validation(self):
        """A rule using documented `condition`/`threshold` choices passes
        argument-spec validation without error."""
        params = {
            "path": MockSmartQuotaApi.PATH1, "quota_type": "directory", "state": "present",
            "quota_notification_rules": [
                {"condition": "exceeded", "threshold": "advisory", "action_alert": True}]}
        result = ArgumentSpecValidator(get_smartquota_parameters()).validate(params)
        assert not result.error_messages

    def test_validate_notification_rules_missing_action_fails(self, powerscale_module_mock):
        """FR-11: a rule with no action fields set fails before any API call."""
        rules = [{"condition": "exceeded", "threshold": "advisory"}]
        self.capture_fail_json_method(
            "quota_notification_rules[0] requires at least one of "
            "action_alert, action_email_owner, or action_email_address to be set",
            powerscale_module_mock, '_validate_notification_rules', rules)

    def test_validate_notification_rules_action_alert_present_passes(self, powerscale_module_mock):
        """A rule with action_alert set passes validation without raising."""
        rules = [{"condition": "exceeded", "threshold": "advisory", "action_alert": True}]
        powerscale_module_mock._validate_notification_rules(rules)
        powerscale_module_mock.module.fail_json.assert_not_called()

    def test_validate_notification_rules_action_email_address_passes(self, powerscale_module_mock):
        """A rule with only action_email_address set passes validation."""
        rules = [{"condition": "exceeded", "threshold": "advisory",
                  "action_email_address": ["admin@example.com"]}]
        powerscale_module_mock._validate_notification_rules(rules)
        powerscale_module_mock.module.fail_json.assert_not_called()

    def test_validate_notification_rules_absent_skips_action_check(self, powerscale_module_mock):
        """A rule being deleted (state=absent) does not require an action field."""
        rules = [{"id": "rule-0001", "state": "absent"}]
        powerscale_module_mock._validate_notification_rules(rules)
        powerscale_module_mock.module.fail_json.assert_not_called()

    def test_validate_notification_rules_none_is_noop(self, powerscale_module_mock):
        """No quota_notification_rules parameter supplied is a no-op."""
        powerscale_module_mock._validate_notification_rules(None)
        powerscale_module_mock.module.fail_json.assert_not_called()

    QUOTA_ID = "2nQKAAEAAAAAAAAAAAAAQIMCAAAAAAAA"

    def test_list_quota_notification_rules_empty(self, powerscale_module_mock):
        """Listing notification rules for a quota with none configured returns []."""
        powerscale_module_mock.quota_api_instance.api_client.call_api = MagicMock(
            return_value=MockSmartQuotaApi.get_no_notification_rules_response())
        result = powerscale_module_mock.list_quota_notification_rules(self.QUOTA_ID)
        assert result == []

    def test_list_quota_notification_rules_single(self, powerscale_module_mock):
        """Listing notification rules for a quota with one rule returns that rule."""
        powerscale_module_mock.quota_api_instance.api_client.call_api = MagicMock(
            return_value=MockSmartQuotaApi.get_single_notification_rule_response())
        result = powerscale_module_mock.list_quota_notification_rules(self.QUOTA_ID)
        assert result == [MockSmartQuotaApi.NOTIFICATION_RULE_1]

    def test_list_quota_notification_rules_multiple(self, powerscale_module_mock):
        """Listing notification rules for a quota with multiple rules returns all of them."""
        powerscale_module_mock.quota_api_instance.api_client.call_api = MagicMock(
            return_value=MockSmartQuotaApi.get_multiple_notification_rules_response())
        result = powerscale_module_mock.list_quota_notification_rules(self.QUOTA_ID)
        assert result == [MockSmartQuotaApi.NOTIFICATION_RULE_1, MockSmartQuotaApi.NOTIFICATION_RULE_2]

    def test_list_quota_notification_rules_exception(self, powerscale_module_mock):
        """SDK ApiException while listing notification rules fails the module."""
        powerscale_module_mock.quota_api_instance.api_client.call_api = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_method(
            MockSmartQuotaApi.smartquota_notification_list_error_response(self.QUOTA_ID),
            powerscale_module_mock, 'list_quota_notification_rules', self.QUOTA_ID)

    def test_create_quota_notification_rule_success(self, powerscale_module_mock):
        """Creating a notification rule calls the API and returns the new rule id."""
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.quota_api_instance.api_client.call_api = MagicMock(
            return_value=MockSmartQuotaApi.smartquota_notification_rule_create_response())
        rule = {"condition": "exceeded", "threshold": "advisory", "action_alert": True}
        result = powerscale_module_mock.create_quota_notification_rule(self.QUOTA_ID, rule)
        assert result == "rule-0001"

    def test_create_quota_notification_rule_check_mode(self, powerscale_module_mock):
        """Creating a notification rule under check_mode makes no API call."""
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.quota_api_instance.api_client.call_api = MagicMock()
        rule = {"condition": "exceeded", "threshold": "advisory", "action_alert": True}
        result = powerscale_module_mock.create_quota_notification_rule(self.QUOTA_ID, rule)
        assert result is True
        powerscale_module_mock.quota_api_instance.api_client.call_api.assert_not_called()

    def test_create_quota_notification_rule_exception(self, powerscale_module_mock):
        """SDK ApiException while creating a notification rule fails the module."""
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.quota_api_instance.api_client.call_api = MagicMock(
            side_effect=utils.ApiException)
        rule = {"condition": "exceeded", "threshold": "advisory", "action_alert": True}
        self.capture_fail_json_method(
            MockSmartQuotaApi.smartquota_notification_create_error_response(self.QUOTA_ID),
            powerscale_module_mock, 'create_quota_notification_rule', self.QUOTA_ID, rule)

    def test_create_quota_notification_rule_exception_after_combined_quota_creation(self, powerscale_module_mock):
        """Combined-create partial failure: if the quota was just created in
        this invocation but its notification rule fails, the error clearly
        states the quota was created but the rule was not."""
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock._quota_just_created = True
        powerscale_module_mock.quota_api_instance.api_client.call_api = MagicMock(
            side_effect=utils.ApiException)
        rule = {"condition": "exceeded", "threshold": "advisory", "action_alert": True}
        self.capture_fail_json_method(
            "Quota was created successfully, but " +
            MockSmartQuotaApi.smartquota_notification_create_error_response(
                self.QUOTA_ID)[0].lower() +
            MockSmartQuotaApi.smartquota_notification_create_error_response(self.QUOTA_ID)[1:],
            powerscale_module_mock, 'create_quota_notification_rule', self.QUOTA_ID, rule)

    def test_handle_quota_creation_sets_just_created_flag(self, powerscale_module_mock):
        """FR-13: a real (non-check_mode) quota creation records that the
        quota was created in this invocation, so a combined-create
        notification-rule failure can report clearly (see above)."""
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.create = MagicMock(return_value=None)
        assert powerscale_module_mock._quota_just_created is False
        powerscale_module_mock._handle_quota_creation(
            "directory", "System", MockSmartQuotaApi.PATH1, None, {})
        assert powerscale_module_mock._quota_just_created is True

    def test_handle_quota_creation_check_mode_does_not_set_flag(self, powerscale_module_mock):
        """Under check_mode, no quota is actually created, so the flag stays False."""
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.create = MagicMock(return_value=True)
        powerscale_module_mock._handle_quota_creation(
            "directory", "System", MockSmartQuotaApi.PATH1, None, {})
        assert powerscale_module_mock._quota_just_created is False

    def test_update_quota_notification_rule_success(self, powerscale_module_mock):
        """Updating a notification rule's action fields calls the API and returns True."""
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.quota_api_instance.api_client.call_api = MagicMock(
            return_value=None)
        rule = {"action_alert": False, "action_email_owner": True}
        result = powerscale_module_mock.update_quota_notification_rule(
            self.QUOTA_ID, "rule-0001", rule)
        assert result is True

    def test_update_quota_notification_rule_check_mode(self, powerscale_module_mock):
        """Updating a notification rule under check_mode makes no API call."""
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.quota_api_instance.api_client.call_api = MagicMock()
        rule = {"action_alert": False}
        result = powerscale_module_mock.update_quota_notification_rule(
            self.QUOTA_ID, "rule-0001", rule)
        assert result is True
        powerscale_module_mock.quota_api_instance.api_client.call_api.assert_not_called()

    def test_update_quota_notification_rule_exception(self, powerscale_module_mock):
        """SDK ApiException while updating a notification rule fails the module."""
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.quota_api_instance.api_client.call_api = MagicMock(
            side_effect=utils.ApiException)
        rule = {"action_alert": False}
        self.capture_fail_json_method(
            MockSmartQuotaApi.smartquota_notification_update_error_response("rule-0001", self.QUOTA_ID),
            powerscale_module_mock, 'update_quota_notification_rule', self.QUOTA_ID, "rule-0001", rule)

    def test_delete_quota_notification_rule_success(self, powerscale_module_mock):
        """Deleting a specific notification rule calls the API and returns True."""
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.quota_api_instance.api_client.call_api = MagicMock(
            return_value=None)
        result = powerscale_module_mock.delete_quota_notification_rule(self.QUOTA_ID, "rule-0001")
        assert result is True

    def test_delete_quota_notification_rule_check_mode(self, powerscale_module_mock):
        """Deleting a specific notification rule under check_mode makes no API call."""
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.quota_api_instance.api_client.call_api = MagicMock()
        result = powerscale_module_mock.delete_quota_notification_rule(self.QUOTA_ID, "rule-0001")
        assert result is True
        powerscale_module_mock.quota_api_instance.api_client.call_api.assert_not_called()

    def test_delete_quota_notification_rule_exception(self, powerscale_module_mock):
        """SDK ApiException while deleting a specific notification rule fails the module."""
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.quota_api_instance.api_client.call_api = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_method(
            MockSmartQuotaApi.smartquota_notification_delete_error_response("rule-0001", self.QUOTA_ID),
            powerscale_module_mock, 'delete_quota_notification_rule', self.QUOTA_ID, "rule-0001")

    def test_delete_all_quota_notification_rules_success(self, powerscale_module_mock):
        """Deleting all notification rules for a quota calls the API and returns True."""
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.quota_api_instance.api_client.call_api = MagicMock(
            return_value=None)
        result = powerscale_module_mock.delete_all_quota_notification_rules(self.QUOTA_ID)
        assert result is True

    def test_delete_all_quota_notification_rules_check_mode(self, powerscale_module_mock):
        """Deleting all notification rules under check_mode makes no API call."""
        powerscale_module_mock.module.check_mode = True
        powerscale_module_mock.quota_api_instance.api_client.call_api = MagicMock()
        result = powerscale_module_mock.delete_all_quota_notification_rules(self.QUOTA_ID)
        assert result is True
        powerscale_module_mock.quota_api_instance.api_client.call_api.assert_not_called()

    def test_delete_all_quota_notification_rules_exception(self, powerscale_module_mock):
        """SDK ApiException while deleting all notification rules fails the module."""
        powerscale_module_mock.module.check_mode = False
        powerscale_module_mock.quota_api_instance.api_client.call_api = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_method(
            MockSmartQuotaApi.smartquota_notification_delete_all_error_response(self.QUOTA_ID),
            powerscale_module_mock, 'delete_all_quota_notification_rules', self.QUOTA_ID)
