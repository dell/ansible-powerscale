# Copyright: (c) 2025 Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for SyncIQ Job module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils


from ansible_collections.dellemc.powerscale.plugins.modules.synciqjob import SyncIQJob
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_synciqjob_api as MockSyncIQJobApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_fail_json \
    import FailJsonException, fail_json


class TestSyncIQJob(PowerScaleUnitBase):
    get_synciq_job_args = {
        "job_id": None,
        "job_state": None,
        "state": None
    }

    snapshot_name_1 = "ansible_test_snapshot"

    @pytest.fixture
    def synciq_job_module_mock(self, mocker):
        mocker.patch(MockSyncIQJobApi.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        synciq_job_module_mock = SyncIQJob()
        synciq_job_module_mock.module = MagicMock()
        synciq_job_module_mock.module.check_mode = False
        synciq_job_module_mock.module.fail_json = fail_json
        synciq_job_module_mock.sync_api_instance = MagicMock()
        return synciq_job_module_mock

    def capture_fail_json_call(self, error_msg, synciq_job_module_mock):
        try:
            synciq_job_module_mock.perform_module_operation()
        except FailJsonException as fj_object:
            assert error_msg in fj_object.message

    # def test_get_job_details_by_id_response(self, synciq_job_module_mock):
    #     self.get_synciq_job_args.update({"job_id": "test",
    #                                      "state": "present"})
    #     synciq_job_module_mock.module.params = self.get_synciq_job_args
    #     synciq_job_module_mock.sync_api_instance.list_sync_jobs.jobs = MagicMock(
    #         return_value=MockSDKResponse(MockSyncIQJobApi.SYNCIQ_JOB["job_details"]))
    #     synciq_job_module_mock.perform_module_operation()
    #     synciq_job_module_mock.sync_api_instance.list_sync_jobs.assert_called()

    # def test_get_synciq_404_exception(self, snapshot_module_mock):
    #     self.get_snapshot_args.update({"path": "/ifs/ansible_test_snapshot",
    #                                    "access_zone": "sample_zone",
    #                                    "snapshot_name": "ansible_test_snapshot",
    #                                    "desired_retention": "2",
    #                                    "retention_unit": "days",
    #                                    "alias": "snap_alias_1",
    #                                    "state": "present"})
    #     snapshot_module_mock.module.params = self.get_snapshot_args
    #     MockApiException.status = '404'
    #     snapshot_module_mock.snapshot_api.get_snapshot_snapshot = MagicMock(
    #         side_effect=utils.ApiException)
    #     snapshot_module_mock.isi_sdk.SnapshotSnapshotCreateParams = MagicMock(
    #         return_value=MockSDKResponse(MockSnapshotApi.CREATE_SNAPSHOT_PARAMS))
    #     snapshot_module_mock.perform_module_operation()
    #     snapshot_module_mock.snapshot_api.create_snapshot_snapshot.assert_called()
    #     assert snapshot_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_get_job_details_exception(self, synciq_job_module_mock):
        self.get_synciq_job_args.update({
            "job_id": "test",
            "state": "present"})
        synciq_job_module_mock.module.params = self.get_synciq_job_args
        synciq_job_module_mock.sync_api_instance.list_sync_jobs = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(
            MockSyncIQJobApi.get_synciq_job_failed_msg(), synciq_job_module_mock)

    def test_get_job_details_empty_id_exception(self, synciq_job_module_mock):
        self.get_synciq_job_args.update({
            "job_id": "",
            "state": "present"})
        synciq_job_module_mock.module.params = self.get_synciq_job_args
        self.capture_fail_json_call(
            MockSyncIQJobApi.get_synciq_job_empty_id_failed_msg(), synciq_job_module_mock)

    def test_modify_synciq_job_state_cancel_exception(self, synciq_job_module_mock):
        self.get_synciq_job_args.update({
            "job_id": "Test",
            "job_state": 'cancel',
            "state": "present"})
        synciq_job_module_mock.module.params = self.get_synciq_job_args
        self.capture_fail_json_call(
            MockSyncIQJobApi.modify_synciq_job_state_cancel_failed_msg(), synciq_job_module_mock)

    def test_delete_synciq_job_exception(self, synciq_job_module_mock):
        self.get_synciq_job_args.update({
            "job_id": "Test",
            "state": "absent"})
        synciq_job_module_mock.module.params = self.get_synciq_job_args
        self.capture_fail_json_call(
            MockSyncIQJobApi.delete_synciq_job_failed_msg(), synciq_job_module_mock)

    def test_create_synciq_job_exception(self, synciq_job_module_mock):
        self.get_synciq_job_args.update({"job_id": "non_existing_job",
                                         "state": "present"})
        synciq_job_module_mock.module.params = self.get_synciq_job_args
        synciq_job_module_mock.sync_api_instance.list_sync_jobs = MagicMock(
            side_effect=MockApiException(404))
        self.capture_fail_json_call(
            MockSyncIQJobApi.create_synciq_job_failed_msg(), synciq_job_module_mock)

    def test_modify_synciq_job_state_response(self, synciq_job_module_mock):
        self.get_synciq_job_args.update({"job_id": "test",
                                         "job_state": 'pause',
                                         "state": "present"})

        synciq_job_module_mock.module.params = self.get_synciq_job_args
        synciq_job_module_mock.get_job_details = MagicMock(
            return_value=MockSyncIQJobApi.SYNCIQ_JOB["job_details"])
        utils.isi_sdk.SyncJob = MagicMock(
            return_value=MockSDKResponse(MockSyncIQJobApi.MODIFY_SYNCIQ_JOB_PARAMS))
        synciq_job_module_mock.perform_module_operation()
        synciq_job_module_mock.sync_api_instance.update_sync_job.assert_called()
        assert synciq_job_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_synciq_job_state_exception(self, synciq_job_module_mock):
        self.get_synciq_job_args.update({"job_id": "test",
                                         "job_state": 'pause',
                                         "state": "present"})

        synciq_job_module_mock.module.params = self.get_synciq_job_args
        synciq_job_module_mock.get_job_details = MagicMock(
            return_value=MockSyncIQJobApi.SYNCIQ_JOB["job_details"])
        utils.isi_sdk.SyncJob = MagicMock(
            return_value=MockSDKResponse(MockSyncIQJobApi.MODIFY_SYNCIQ_JOB_PARAMS))
        synciq_job_module_mock.sync_api_instance.update_sync_job = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(
            MockSyncIQJobApi.modify_synciq_job_failed_msg(), synciq_job_module_mock)
