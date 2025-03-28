# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for smb file module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils


from ansible_collections.dellemc.powerscale.plugins.modules.smb_file import SmbFile, main
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_smb_file_api as MockSmbFileApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase


class TestSmbFile(PowerScaleUnitBase):
    get_smb_file_args = {
        "state": None,
        "file_id": None,
        "file_path": None}

    @pytest.fixture
    def module_object(self, mocker):
        return SmbFile

    def test_get_smb_file_response(self, powerscale_module_mock):
        self.get_smb_file_args.update({"file_id": 123,
                                       "state": "present"})
        powerscale_module_mock.module.params = self.get_smb_file_args
        powerscale_module_mock.protocol_api = MagicMock()
        powerscale_module_mock.protocol_api.get_smb_openfiles.to_dict = MagicMock(
            return_value=MockSDKResponse(MockSmbFileApi.SmbFile))
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.protocol_api.get_smb_openfiles.assert_called()

    def test_get_smb_file_exception(self, powerscale_module_mock):
        self.get_smb_file_args.update({"file_id": 123,
                                       "state": "present"})
        powerscale_module_mock.module.params = self.get_smb_file_args
        powerscale_module_mock.protocol_api.get_smb_openfiles = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(MockSmbFileApi.get_smb_file_failed_msg(), invoke_perform_module=True)

    def test_close_smb_file_response(self, powerscale_module_mock):
        self.get_smb_file_args.update({"file_id": 123,
                                       "state": "absent"})
        powerscale_module_mock.module.params = self.get_smb_file_args
        powerscale_module_mock.protocol_api = MagicMock()
        powerscale_module_mock.protocol_api.get_smb_openfiles.to_dict = MagicMock(
            return_value=MockSmbFileApi.SmbFile)
        powerscale_module_mock.get_file_id = MagicMock(return_value=[123])
        powerscale_module_mock.protocol_api.delete_smb_openfile = MagicMock(
            return_value=None)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.protocol_api.delete_smb_openfile.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_close_smb_file_exception(self, powerscale_module_mock):
        self.get_smb_file_args.update({"file_id": 123,
                                       "state": "absent"})
        powerscale_module_mock.module.params = self.get_smb_file_args
        powerscale_module_mock.protocol_api = MagicMock()
        powerscale_module_mock.protocol_api.get_smb_openfiles.to_dict = MagicMock(
            return_value=MockSmbFileApi.SmbFile)
        powerscale_module_mock.get_file_id = MagicMock(return_value=[123])
        powerscale_module_mock.protocol_api.delete_smb_openfile = MagicMock(
            side_effect=utils.ApiException)
        self.capture_fail_json_call(MockSmbFileApi.close_smb_file_failed_msg(), invoke_perform_module=True)

    def test_get_file_id_with_file_path(self, powerscale_module_mock):
        file_path = "C:\\ifs"
        powerscale_module_mock.get_smb_files = MagicMock(
            return_value=MockSmbFileApi.SmbFile["openfiles"])
        resp = powerscale_module_mock.get_file_id(file_path=file_path)
        assert resp is not None

    def test_get_file_id_with_file_id(self, powerscale_module_mock):
        file_id = 1593
        powerscale_module_mock.get_smb_files = MagicMock(
            return_value=MockSmbFileApi.SmbFile["openfiles"])
        resp = powerscale_module_mock.get_file_id(file_id=file_id)
        assert resp is not None

    def test_main(self):
        main()
