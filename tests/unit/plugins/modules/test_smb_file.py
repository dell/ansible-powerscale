# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for smb file module on PowerScale"""

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


from ansible_collections.dellemc.powerscale.plugins.modules.smb_file import SmbFile
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_smb_file_api as MockSmbFileApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response \
    import MockSDKResponse
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException


class TestSmbFile():
    get_smb_file_args = {
        "state": None,
        "file_id": None,
        "file_path": None}

    @pytest.fixture
    def smb_file_module_mock(self, mocker):
        mocker.patch(MockSmbFileApi.MODULE_UTILS_PATH + '.ApiException', new=MockApiException)
        smb_file_module_mock = SmbFile()
        smb_file_module_mock.module = MagicMock()
        smb_file_module_mock.module.check_mode = False
        return smb_file_module_mock

    def test_get_smb_file_response(self, smb_file_module_mock):
        self.get_smb_file_args.update({"file_id": 123,
                                       "state": "present"})
        smb_file_module_mock.module.params = self.get_smb_file_args
        smb_file_module_mock.protocol_api = MagicMock()
        smb_file_module_mock.protocol_api.get_smb_openfiles.to_dict = MagicMock(
            return_value=MockSDKResponse(MockSmbFileApi.SmbFile))
        smb_file_module_mock.perform_module_operation()
        smb_file_module_mock.protocol_api.get_smb_openfiles.assert_called()

    def test_get_smb_file_exception(self, smb_file_module_mock):
        self.get_smb_file_args.update({"file_id": 123,
                                       "state": "present"})
        smb_file_module_mock.module.params = self.get_smb_file_args
        smb_file_module_mock.protocol_api.get_smb_openfiles = MagicMock(side_effect=MockApiException)
        smb_file_module_mock.perform_module_operation()
        assert MockSmbFileApi.get_smb_file_failed_msg() in \
            smb_file_module_mock.module.fail_json.call_args[1]['msg']

    def test_close_smb_file_response(self, smb_file_module_mock):
        self.get_smb_file_args.update({"file_id": 123,
                                       "state": "absent"})
        smb_file_module_mock.module.params = self.get_smb_file_args
        smb_file_module_mock.protocol_api = MagicMock()
        smb_file_module_mock.protocol_api.get_smb_openfiles.to_dict = MagicMock(return_value=MockSmbFileApi.SmbFile)
        smb_file_module_mock.get_file_id = MagicMock(return_value=[123])
        smb_file_module_mock.protocol_api.delete_smb_openfile = MagicMock(return_value=None)
        smb_file_module_mock.perform_module_operation()
        smb_file_module_mock.protocol_api.delete_smb_openfile.assert_called()
        assert smb_file_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_close_smb_file_exception(self, smb_file_module_mock):
        self.get_smb_file_args.update({"file_id": 123,
                                       "state": "absent"})
        smb_file_module_mock.module.params = self.get_smb_file_args
        smb_file_module_mock.protocol_api = MagicMock()
        smb_file_module_mock.protocol_api.get_smb_openfiles.to_dict = MagicMock(return_value=MockSmbFileApi.SmbFile)
        smb_file_module_mock.get_file_id = MagicMock(return_value=[123])
        smb_file_module_mock.protocol_api.delete_smb_openfile = MagicMock(side_effect=utils.ApiException)
        smb_file_module_mock.perform_module_operation()
        smb_file_module_mock.protocol_api.delete_smb_openfile.assert_called()
        assert MockSmbFileApi.close_smb_file_failed_msg() in \
            smb_file_module_mock.module.fail_json.call_args[1]['msg']
