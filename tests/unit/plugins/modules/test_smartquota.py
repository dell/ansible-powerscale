# Copyright: (c) 2022, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for smartquota module on PowerScale"""

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


from ansible_collections.dellemc.powerscale.plugins.modules.smartquota import SmartQuota
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils.mock_smartquota_api import MockSmartQuotaApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException


class TestSmartQuota():
    get_smartquota_args = {"path": None,
                           "access_zone": None,
                           "quota_type": None,
                           "user_name": None,
                           "group_name": None,
                           "provider_type": None,
                           "quota": None,
                           "list_snapshots": None,
                           "state": None
                           }
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'

    @pytest.fixture
    def smartquota_module_mock(self, mocker):
        smartquota_module_mock = SmartQuota()
        smartquota_module_mock.module = MagicMock()
        mocker.patch(self.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        return smartquota_module_mock

    def test_smartquota_create_quota(self, smartquota_module_mock):
        self.get_smartquota_args.update({"path": "/Test/Test1",
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
                                         "state": "present"})
        smartquota_module_mock.module.params = self.get_smartquota_args
        smartquota_module_mock.get_quota_params = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaThresholds = MagicMock(return_value=None)
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaCreateParams = MagicMock(return_value=None)
        smartquota_module_mock.add_limits_with_unit = MagicMock()
        utils.convert_size_with_unit = MagicMock()
        smartquota_module_mock.quota_api_instance.create_quota_quota = MagicMock(return_value=None)
        smartquota_module_mock.determine_error = MagicMock(return_value=None)
        smartquota_module_mock.perform_module_operation()
        assert smartquota_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_smartquota_create_quota_paramset1(self, smartquota_module_mock):
        self.get_smartquota_args.update({"path": "/Test/Test1",
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
                                             "period_unit": "days",
                                             "advisory_limit_size": 3,
                                             "include_overheads": True,
                                             "container": True,
                                         },
                                         "list_snapshots": True,
                                         "state": "present"})
        smartquota_module_mock.module.params = self.get_smartquota_args
        smartquota_module_mock.get_quota_params = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaThresholds = MagicMock(return_value=None)
        utils.validate_threshold_overhead_parameter = MagicMock(return_value=None)
        utils.isi_sdk.QuotaQuotaCreateParams = MagicMock(return_value=None)
        smartquota_module_mock.add_limits_with_unit = MagicMock()
        utils.convert_size_with_unit = MagicMock()
        smartquota_module_mock.quota_api_instance.create_quota_quota = MagicMock(return_value=None)
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
                                             "period_unit": "days",
                                             "persona": None,
                                             "advisory_limit_size": 3,
                                             "include_overheads": True,
                                             "container": True,
                                         },
                                         "list_snapshots": True,
                                         "state": "present"})
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
        assert MockSmartQuotaApi.smartquota_create_quota_response("error", path="Mock_Path") not in \
            smartquota_module_mock.module.fail_json.call_args[1]["msg"]
