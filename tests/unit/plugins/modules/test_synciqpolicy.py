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
from ansible_collections.dellemc.powerscale.plugins.modules.synciqpolicy import SynciqPolicy, SynciqPolicyHandler, main
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils \
    import mock_synciqpolicy_api as MockSynciqApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase


class Policy:
    def __init__(self, name, id, target_certificate_id):
        self.name = name
        self.id = id
        self.target_certificate_id = target_certificate_id

    def to_dict(self):
        return vars(self)


class PolicyDict:
    def __init__(self, policy):
        self.policies = policy


class TestSynciqPolicy(PowerScaleUnitBase):
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'
    synciqpolicy_args = MockSynciqApi.MockSynciqpolicyApi.SYNCIQPOLICY_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return SynciqPolicy

    def test_create_synciqpolicy_check_mode(self):
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.CREATE_ARGS)
        self.powerscale_module_mock.module._diff = True
        self.powerscale_module_mock.module.check_mode = True
        self.powerscale_module_mock.validate_job_params = MagicMock(
            return_value=None)
        self.powerscale_module_mock.get_target_cert_id_name = MagicMock(
            return_value=MockSynciqApi.MockSynciqpolicyApi.CERT_NAME
        )
        self.powerscale_module_mock.get_synciq_policy_details = MagicMock(
            return_value=(None, False))
        SynciqPolicyHandler().handle(self.powerscale_module_mock,
                                     self.powerscale_module_mock.module.params)
        assert self.powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_create_synciqpolicy_exception(self):
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.CREATE_ARGS)
        self.powerscale_module_mock.get_target_cert_id_name = MagicMock(
            return_value=MockSynciqApi.MockSynciqpolicyApi.CERT_NAME
        )
        self.powerscale_module_mock.get_synciq_policy_details = MagicMock(
            return_value=(None, False))
        self.powerscale_module_mock.api_instance.create_sync_policy = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            "Creating SyncIQ policy",
            SynciqPolicyHandler
        )

    def test_modify_synciqpolicy(self):
        self.set_module_params(
            self.synciqpolicy_args,
            MockSynciqApi.MockSynciqpolicyApi.CREATE_ARGS)
        self.powerscale_module_mock.module._diff = True
        self.powerscale_module_mock.validate_job_params = MagicMock(
            return_value=None)
        SynciqPolicyHandler().handle(self.powerscale_module_mock,
                                     self.powerscale_module_mock.module.params)
        assert self.powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert self.powerscale_module_mock.module.exit_json.call_args[
            1]["create_synciq_policy"] is False
        assert self.powerscale_module_mock.module.exit_json.call_args[
            1]["create_job_synciq_policy"] is False
        assert self.powerscale_module_mock.module.exit_json.call_args[
            1]["delete_synciq_policy"] is False
        assert self.powerscale_module_mock.module.exit_json.call_args[
            1]["modify_synciq_policy"] is True

    def test_modify_synciqpolicy_check_mode(self):
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.CREATE_ARGS)
        self.powerscale_module_mock.module._diff = True
        self.powerscale_module_mock.module.check_mode = True
        self.powerscale_module_mock.validate_job_params = MagicMock(
            return_value=None)
        SynciqPolicyHandler().handle(self.powerscale_module_mock,
                                     self.powerscale_module_mock.module.params)
        assert self.powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_modify_synciqpolicy_exception(self):
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.CREATE_ARGS)
        self.powerscale_module_mock.module._diff = True
        self.powerscale_module_mock.api_instance.update_sync_policy = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            "Failed to modify SyncIQ policy with error",
            SynciqPolicyHandler
        )

    def test_delete_synciqpolicy(self):
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.DELETE_ARGS)
        self.powerscale_module_mock.module._diff = True
        self.powerscale_module_mock.validate_job_params = MagicMock(
            return_value=None)
        SynciqPolicyHandler().handle(self.powerscale_module_mock,
                                     self.powerscale_module_mock.module.params)
        assert self.powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert self.powerscale_module_mock.module.exit_json.call_args[
            1]["create_synciq_policy"] is False
        assert self.powerscale_module_mock.module.exit_json.call_args[
            1]["create_job_synciq_policy"] is False
        assert self.powerscale_module_mock.module.exit_json.call_args[
            1]["delete_synciq_policy"] is True
        assert self.powerscale_module_mock.module.exit_json.call_args[
            1]["modify_synciq_policy"] is False

    def test_delete_synciqpolicy_checkmode(self):
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.DELETE_ARGS)
        self.powerscale_module_mock.module._diff = True
        self.powerscale_module_mock.module.check_mode = True
        self.powerscale_module_mock.validate_job_params = MagicMock(
            return_value=None)
        SynciqPolicyHandler().handle(self.powerscale_module_mock,
                                     self.powerscale_module_mock.module.params)
        assert self.powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_delete_synciqpolicy_exception(self):
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.DELETE_ARGS)
        self.powerscale_module_mock.api_instance.delete_sync_policy = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            "Deleting SyncIQ policy",
            SynciqPolicyHandler
        )

    @pytest.mark.parametrize("params",
                             [MockSynciqApi.MockSynciqpolicyApi.CREATE_JOB_ARGS])
    def test_create_job_on_synciqpolicy(self, params):
        self.set_module_params(self.synciqpolicy_args,
                               params)
        self.powerscale_module_mock.module._diff = True
        SynciqPolicyHandler().handle(self.powerscale_module_mock,
                                     self.powerscale_module_mock.module.params)
        assert self.powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert self.powerscale_module_mock.module.exit_json.call_args[
            1]["create_synciq_policy"] is False
        assert self.powerscale_module_mock.module.exit_json.call_args[
            1]["create_job_synciq_policy"] is True
        assert self.powerscale_module_mock.module.exit_json.call_args[
            1]["delete_synciq_policy"] is False
        assert self.powerscale_module_mock.module.exit_json.call_args[
            1]["modify_synciq_policy"] is True

    def test_create_job_on_synciqpolicy_failure_case(self):
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.CREATE_JOB_ARGS)
        self.powerscale_module_mock.get_synciq_policy_details = MagicMock(
            return_value=(None, False))
        self.capture_fail_json_call(
            "Please provide a valid certificate.", SynciqPolicyHandler)

    def test_create_job_on_synciqpolicy_exception(self):
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.CREATE_JOB_ARGS)
        self.powerscale_module_mock.api_instance.create_sync_job = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            "Failed to create job on SyncIQ policy with error",
            SynciqPolicyHandler
        )

    def test_rename_synciqpolicy(self):
        self.set_module_params(self.synciqpolicy_args,
                               {"policy_name": "policy1", "new_policy_name": "new_policy_name"})
        SynciqPolicyHandler().handle(self.powerscale_module_mock,
                                     self.powerscale_module_mock.module.params)
        assert self.powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert self.powerscale_module_mock.module.exit_json.call_args[
            1]["create_synciq_policy"] is False
        assert self.powerscale_module_mock.module.exit_json.call_args[
            1]["create_job_synciq_policy"] is False
        assert self.powerscale_module_mock.module.exit_json.call_args[
            1]["delete_synciq_policy"] is False
        assert self.powerscale_module_mock.module.exit_json.call_args[
            1]["modify_synciq_policy"] is True

    def test_rename_synciqpolicy_failure_case(self):
        self.set_module_params(self.synciqpolicy_args,
                               {"policy_name": "policy1", "new_policy_name": ""})
        self.powerscale_module_mock.module._diff = True
        self.capture_fail_json_call(
            "new_policy_name cannot be empty. Please provide a valid new_policy_name to rename policy.", SynciqPolicyHandler)

    def test_get_synciqpolicy_details(self):
        policy_obj = Policy(name="policy1", id="ab12",
                            target_certificate_id=12)
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.CREATE_ARGS2)
        self.powerscale_module_mock.get_target_cert_id_name = MagicMock(
            return_value=MockSynciqApi.MockSynciqpolicyApi.CERT_NAME
        )
        self.powerscale_module_mock.get_synciq_policy_details = MagicMock(
            return_value=(policy_obj, True))
        self.powerscale_module_mock.validate_job_params = MagicMock(
            return_value=None)
        SynciqPolicyHandler().handle(self.powerscale_module_mock,
                                     self.powerscale_module_mock.module.params)
        assert self.powerscale_module_mock.module.exit_json.call_args[1]["changed"] is False

    def test_get_synciqpolicy_details2(self):
        policy = PolicyDict({})
        self.powerscale_module_mock.api_instance.get_sync_policy = MagicMock(
            return_value=policy)
        result = self.powerscale_module_mock.get_synciq_policy_details(
            MockSynciqApi.MockSynciqpolicyApi.GET_ARGS2.get("policy_name"),
            MockSynciqApi.MockSynciqpolicyApi.GET_ARGS2.get("policy_id"))
        assert result == (None, False)

    def test_get_synciq_policy_details_exception(self):
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.CREATE_ARGS)
        self.powerscale_module_mock.api_instance.get_sync_policy = MagicMock(
            side_effect=Exception("Test_exception"))
        self.capture_fail_json_call(
            MockSynciqApi.MockSynciqpolicyApi.EXCEPTION_MSG,
            SynciqPolicyHandler
        )

    def test_get_synciqpolicy_details_api_exception(self):
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.CREATE_ARGS)
        self.powerscale_module_mock.get_target_policy = MagicMock(
            return_value=({}, True))
        self.powerscale_module_mock.api_instance.get_sync_policy = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSynciqApi.MockSynciqpolicyApi.EXCEPTION_MSG,
            SynciqPolicyHandler
        )

    def test_get_synciqpolicy_details_404error(self):
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.CREATE_ARGS)
        policy_obj = Policy(name="policy2", id="ab", target_certificate_id=14)
        self.powerscale_module_mock.get_target_policy = MagicMock(
            return_value=(policy_obj, True))
        self.powerscale_module_mock.api_instance.get_sync_policy = MagicMock(
            side_effect=MockApiException(404))
        self.capture_fail_json_call(
            "Please provide a valid certificate",
            SynciqPolicyHandler
        )

    def test_get_policy_jobs_exception_case(self):
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.GET_ARGS)
        self.powerscale_module_mock.api_instance.list_sync_jobs = MagicMock(
            side_effect=Exception("Test_exception1"))
        self.capture_fail_json_call(
            MockSynciqApi.MockSynciqpolicyApi.EXCEPTION_MSG,
            SynciqPolicyHandler
        )

    def test_get_target_policy(self):
        job_params = MockSynciqApi.MockSynciqpolicyApi.JOB_ARGS1["job_params"]
        policy_id = MockSynciqApi.MockSynciqpolicyApi.POLICY_ID
        result = self.powerscale_module_mock.get_synciq_target_policy(
            policy_id, job_params)
        assert result[1] is True
        job_params = MockSynciqApi.MockSynciqpolicyApi.JOB_ARGS2["job_params"]
        result = self.powerscale_module_mock.get_synciq_target_policy(
            policy_id, job_params)
        assert result[1] is False
        assert result[0] is None

    def test_get_target_policy_exception(self):
        job_params = MockSynciqApi.MockSynciqpolicyApi.JOB_ARGS1["job_params"]
        policy_id = MockSynciqApi.MockSynciqpolicyApi.POLICY_ID
        self.powerscale_module_mock.api_instance.get_target_policy = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_method("Get details of target SyncIQ policy",
                                      self.powerscale_module_mock, "get_synciq_target_policy", policy_id, job_params)

    def test_get_policy_jobs_exception(self):
        self.powerscale_module_mock.api_instance.get_policy_jobs = MagicMock(
            side_effect=Exception("Testexception2"))
        self.capture_fail_json_call(
            "Please specify policy_name or policy_id",
            SynciqPolicyHandler
        )

    def test_validate_job_params_invalid_mode(self):
        job_params = MockSynciqApi.MockSynciqpolicyApi.JOB_ARGS3["job_params"]
        self.capture_fail_json_method("workers_per_node is valid only for allow_write and allow_write_revert operation.",
                                      self.powerscale_module_mock, "validate_job_params", job_params)

    def test_validate_job_params_invalid_workersnode(self):
        job_params = MockSynciqApi.MockSynciqpolicyApi.JOB_ARGS4["job_params"]
        self.capture_fail_json_method("Please enter a value greater than 0 for workers_per_node.",
                                      self.powerscale_module_mock, "validate_job_params", job_params)

    def test_get_synciq_policy_display_attributes_exception(self, mocker):
        policy_obj = Policy(name="policy1", id="ab12",
                            target_certificate_id=12)
        self.powerscale_module_mock.api_instance.get_target_cert_id_name = MagicMock(
            side_effect=Exception("Test exception"))
        self.capture_fail_json_method("Please provide a valid certificate",
                                      self.powerscale_module_mock, "get_synciq_policy_display_attributes", policy_obj)
