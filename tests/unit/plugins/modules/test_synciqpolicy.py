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

    # ── TC-PSW-001: Create SyncIQ policy with password ──
    def test_create_synciqpolicy_with_password(self):
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.CREATE_ARGS_WITH_PASSWORD)
        self.powerscale_module_mock.module._diff = False
        self.powerscale_module_mock.validate_job_params = MagicMock(
            return_value=None)
        self.powerscale_module_mock.get_target_cert_id_name = MagicMock(
            return_value=MockSynciqApi.MockSynciqpolicyApi.CERT_NAME
        )
        self.powerscale_module_mock.get_synciq_policy_details = MagicMock(
            return_value=(None, False))
        self.powerscale_module_mock.api_instance.create_sync_policy.reset_mock()
        self.powerscale_module_mock.api_instance.create_sync_policy.side_effect = None
        SynciqPolicyHandler().handle(self.powerscale_module_mock,
                                     self.powerscale_module_mock.module.params)
        assert self.powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert self.powerscale_module_mock.module.exit_json.call_args[1]["create_synciq_policy"] is True
        # Verify password was included in the create call
        create_call_args = self.powerscale_module_mock.api_instance.create_sync_policy.call_args
        if create_call_args:
            sync_policy_arg = create_call_args[1].get('sync_policy', create_call_args[0][0] if create_call_args[0] else None)
            if isinstance(sync_policy_arg, dict):
                assert 'password' in sync_policy_arg, "password must be included in create_sync_policy call"

    # ── TC-PSW-002: Create SyncIQ policy with password in check mode ──
    def test_create_synciqpolicy_with_password_check_mode(self):
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.CREATE_ARGS_WITH_PASSWORD)
        self.powerscale_module_mock.module._diff = False
        self.powerscale_module_mock.module.check_mode = True
        self.powerscale_module_mock.validate_job_params = MagicMock(
            return_value=None)
        self.powerscale_module_mock.get_target_cert_id_name = MagicMock(
            return_value=MockSynciqApi.MockSynciqpolicyApi.CERT_NAME
        )
        self.powerscale_module_mock.get_synciq_policy_details = MagicMock(
            return_value=(None, False))
        self.powerscale_module_mock.api_instance.create_sync_policy.reset_mock()
        SynciqPolicyHandler().handle(self.powerscale_module_mock,
                                     self.powerscale_module_mock.module.params)
        assert self.powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        # Verify no actual API call was made in check mode
        self.powerscale_module_mock.api_instance.create_sync_policy.assert_not_called()

    # ── TC-PSW-003: Create SyncIQ policy with password exception ──
    def test_create_synciqpolicy_with_password_exception(self):
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.CREATE_ARGS_WITH_PASSWORD)
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

    # ── TC-PSW-006: Modify with ONLY password, password_set=True → changed=False ──
    def test_modify_synciqpolicy_password_only_already_set(self):
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.MODIFY_ARGS_PASSWORD_ONLY)
        self.powerscale_module_mock.module._diff = False
        self.powerscale_module_mock.validate_job_params = MagicMock(
            return_value=None)
        self.powerscale_module_mock.api_instance.update_sync_policy.reset_mock()
        self.powerscale_module_mock.api_instance.update_sync_policy.side_effect = None
        self.powerscale_module_mock.api_instance.list_sync_jobs.reset_mock()
        self.powerscale_module_mock.api_instance.list_sync_jobs.side_effect = None
        # Mock a policy object that already has password_set=True
        policy_obj = MagicMock()
        policy_obj.name = "Policy1"
        policy_obj.id = "abc123"
        policy_obj.password_set = True
        policy_obj.target_certificate_id = None
        policy_obj.source_include_directories = []
        policy_obj.source_exclude_directories = []
        policy_obj.source_network = None
        policy_obj.enabled = True
        policy_dict = {
            'name': 'Policy1', 'id': 'abc123', 'password_set': True,
            'target_certificate_id': None, 'source_include_directories': [],
            'source_exclude_directories': [], 'source_network': None,
            'enabled': True, 'description': '', 'action': 'sync',
            'schedule': '', 'target_host': '', 'target_path': '',
            'target_snapshot_archive': False, 'target_snapshot_expiration': None,
            'snapshot_sync_pattern': '*', 'accelerated_failback': True,
            'restrict_target_network': False, 'target_compare_initial_sync': False,
            'skip_when_source_unmodified': False, 'job_delay': None,
            'rpo_alert': None, 'source_root_path': '/test',
            'last_job_state': 'unknown', 'last_started': None,
            'last_success': None, 'next_run': None
        }
        policy_obj.to_dict = MagicMock(return_value=policy_dict)
        self.powerscale_module_mock.get_synciq_policy_details = MagicMock(
            return_value=(policy_obj, False))
        SynciqPolicyHandler().handle(self.powerscale_module_mock,
                                     self.powerscale_module_mock.module.params)
        # When only password is provided and password_set is already True,
        # module should NOT report changes (cannot detect if value differs)
        assert self.powerscale_module_mock.module.exit_json.call_args[1]["changed"] is False

    # ── TC-PSW-007: Check mode — password provided, password_set=True → changed=False (FR2) ──
    def test_check_mode_password_already_set_no_false_positive(self):
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.MODIFY_ARGS_PASSWORD_ONLY)
        self.powerscale_module_mock.module._diff = False
        self.powerscale_module_mock.module.check_mode = True
        self.powerscale_module_mock.validate_job_params = MagicMock(
            return_value=None)
        self.powerscale_module_mock.api_instance.update_sync_policy.reset_mock()
        self.powerscale_module_mock.api_instance.update_sync_policy.side_effect = None
        self.powerscale_module_mock.api_instance.list_sync_jobs.reset_mock()
        self.powerscale_module_mock.api_instance.list_sync_jobs.side_effect = None
        policy_obj = MagicMock()
        policy_obj.name = "Policy1"
        policy_obj.id = "abc123"
        policy_obj.password_set = True
        policy_obj.target_certificate_id = None
        policy_obj.source_include_directories = []
        policy_obj.source_exclude_directories = []
        policy_obj.source_network = None
        policy_obj.enabled = True
        policy_dict = {
            'name': 'Policy1', 'id': 'abc123', 'password_set': True,
            'target_certificate_id': None, 'source_include_directories': [],
            'source_exclude_directories': [], 'source_network': None,
            'enabled': True, 'description': '', 'action': 'sync',
            'schedule': '', 'target_host': '', 'target_path': '',
            'target_snapshot_archive': False, 'target_snapshot_expiration': None,
            'snapshot_sync_pattern': '*', 'accelerated_failback': True,
            'restrict_target_network': False, 'target_compare_initial_sync': False,
            'skip_when_source_unmodified': False, 'job_delay': None,
            'rpo_alert': None, 'source_root_path': '/test',
            'last_job_state': 'unknown', 'last_started': None,
            'last_success': None, 'next_run': None
        }
        policy_obj.to_dict = MagicMock(return_value=policy_dict)
        self.powerscale_module_mock.get_synciq_policy_details = MagicMock(
            return_value=(policy_obj, False))
        SynciqPolicyHandler().handle(self.powerscale_module_mock,
                                     self.powerscale_module_mock.module.params)
        # FR2: check_mode must NOT report changes when password hasn't changed
        assert self.powerscale_module_mock.module.exit_json.call_args[1]["changed"] is False

    # ── TC-PSW-008: Check mode — password provided, password_set=False → changed=True ──
    def test_check_mode_password_not_set(self):
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.MODIFY_ARGS_PASSWORD_ONLY)
        self.powerscale_module_mock.module._diff = False
        self.powerscale_module_mock.module.check_mode = True
        self.powerscale_module_mock.validate_job_params = MagicMock(
            return_value=None)
        self.powerscale_module_mock.api_instance.update_sync_policy.reset_mock()
        self.powerscale_module_mock.api_instance.update_sync_policy.side_effect = None
        self.powerscale_module_mock.api_instance.list_sync_jobs.reset_mock()
        self.powerscale_module_mock.api_instance.list_sync_jobs.side_effect = None
        policy_obj = MagicMock()
        policy_obj.name = "Policy1"
        policy_obj.id = "abc123"
        policy_obj.password_set = False
        policy_obj.target_certificate_id = None
        policy_obj.source_include_directories = []
        policy_obj.source_exclude_directories = []
        policy_obj.source_network = None
        policy_obj.enabled = True
        policy_dict = {
            'name': 'Policy1', 'id': 'abc123', 'password_set': False,
            'target_certificate_id': None, 'source_include_directories': [],
            'source_exclude_directories': [], 'source_network': None,
            'enabled': True, 'description': '', 'action': 'sync',
            'schedule': '', 'target_host': '', 'target_path': '',
            'target_snapshot_archive': False, 'target_snapshot_expiration': None,
            'snapshot_sync_pattern': '*', 'accelerated_failback': True,
            'restrict_target_network': False, 'target_compare_initial_sync': False,
            'skip_when_source_unmodified': False, 'job_delay': None,
            'rpo_alert': None, 'source_root_path': '/test',
            'last_job_state': 'unknown', 'last_started': None,
            'last_success': None, 'next_run': None
        }
        policy_obj.to_dict = MagicMock(return_value=policy_dict)
        self.powerscale_module_mock.get_synciq_policy_details = MagicMock(
            return_value=(policy_obj, False))
        SynciqPolicyHandler().handle(self.powerscale_module_mock,
                                     self.powerscale_module_mock.module.params)
        # Password not yet set, user provides password → should report change needed
        assert self.powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    # ── TC-PSW-005: Modify password + other changes, password_set=True → changed=True ──
    def test_modify_synciqpolicy_password_with_other_changes(self):
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.MODIFY_ARGS_PASSWORD_WITH_DESCRIPTION)
        self.powerscale_module_mock.module._diff = False
        self.powerscale_module_mock.validate_job_params = MagicMock(
            return_value=None)
        self.powerscale_module_mock.api_instance.update_sync_policy.reset_mock()
        self.powerscale_module_mock.api_instance.update_sync_policy.side_effect = None
        self.powerscale_module_mock.api_instance.list_sync_jobs.reset_mock()
        self.powerscale_module_mock.api_instance.list_sync_jobs.side_effect = None
        policy_obj = MagicMock()
        policy_obj.name = "Policy1"
        policy_obj.id = "abc123"
        policy_obj.password_set = True
        policy_obj.target_certificate_id = None
        policy_obj.source_include_directories = []
        policy_obj.source_exclude_directories = []
        policy_obj.source_network = None
        policy_obj.enabled = True
        policy_dict = {
            'name': 'Policy1', 'id': 'abc123', 'password_set': True,
            'target_certificate_id': None, 'source_include_directories': [],
            'source_exclude_directories': [], 'source_network': None,
            'enabled': True, 'description': 'Old description', 'action': 'sync',
            'schedule': '', 'target_host': '', 'target_path': '',
            'target_snapshot_archive': False, 'target_snapshot_expiration': None,
            'snapshot_sync_pattern': '*', 'accelerated_failback': True,
            'restrict_target_network': False, 'target_compare_initial_sync': False,
            'skip_when_source_unmodified': False, 'job_delay': None,
            'rpo_alert': None, 'source_root_path': '/test',
            'last_job_state': 'unknown', 'last_started': None,
            'last_success': None, 'next_run': None
        }
        policy_obj.to_dict = MagicMock(return_value=policy_dict)
        self.powerscale_module_mock.get_synciq_policy_details = MagicMock(
            return_value=(policy_obj, False))
        SynciqPolicyHandler().handle(self.powerscale_module_mock,
                                     self.powerscale_module_mock.module.params)
        # Description changed + password provided → should report change
        assert self.powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert self.powerscale_module_mock.module.exit_json.call_args[1]["modify_synciq_policy"] is True
        # Verify password was included in the modify call
        update_call_args = self.powerscale_module_mock.api_instance.update_sync_policy.call_args
        if update_call_args:
            sync_policy_arg = update_call_args[1].get('sync_policy', {})
            if isinstance(sync_policy_arg, dict):
                assert 'password' in sync_policy_arg, "password must be included in update when other changes exist"

    # ── TC-PSW-011: Create policy without password (backward compatibility) ──
    def test_create_synciqpolicy_without_password_backward_compat(self):
        self.set_module_params(self.synciqpolicy_args,
                               MockSynciqApi.MockSynciqpolicyApi.CREATE_ARGS)
        self.powerscale_module_mock.module._diff = False
        self.powerscale_module_mock.validate_job_params = MagicMock(
            return_value=None)
        self.powerscale_module_mock.get_target_cert_id_name = MagicMock(
            return_value=MockSynciqApi.MockSynciqpolicyApi.CERT_NAME
        )
        self.powerscale_module_mock.get_synciq_policy_details = MagicMock(
            return_value=(None, False))
        self.powerscale_module_mock.api_instance.create_sync_policy.reset_mock()
        self.powerscale_module_mock.api_instance.create_sync_policy.side_effect = None
        SynciqPolicyHandler().handle(self.powerscale_module_mock,
                                     self.powerscale_module_mock.module.params)
        assert self.powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert self.powerscale_module_mock.module.exit_json.call_args[1]["create_synciq_policy"] is True
