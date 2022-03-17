# Copyright: (c) 2022, DellEMC

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Unit Tests for filesystem module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import dellemc_ansible_powerscale_utils as utils

utils.get_logger = MagicMock()
utils.isi_sdk = MagicMock()
from ansible.module_utils import basic
basic.AnsibleModule = MagicMock()


from ansible_collections.dellemc.powerscale.plugins.modules.filesystem import FileSystem
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils.mock_filesystem_api import MockFileSystemApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException


class TestFileSystem():
    get_filesystem_args = {'path': None,
                           'access_zone': None,
                           'owner': None,
                           'group': None,
                           'access_control': None,
                           'recursive': None,
                           'recursive_force_delete': None,
                           'quota': None,
                           'state': None
                           }

    @pytest.fixture
    def filesystem_module_mock(self, mocker):
        filesystem_module_mock = FileSystem()
        filesystem_module_mock.module = MagicMock()
        return filesystem_module_mock

    def test_delete_file_system(self, filesystem_module_mock):
        self.get_filesystem_args.update({"path": "/ifs/ATest3", "recursive_force_delete": True, "access_zone": "System", "state": "absent"})
        filesystem_module_mock.module.params = self.get_filesystem_args
        filesystem_module_mock.protocol_api = MagicMock()
        filesystem_module_mock.namespace_api.delete_directory = MagicMock(return_value=True)
        filesystem_module_mock.perform_module_operation()
        assert filesystem_module_mock.module.exit_json.call_args[1]['changed']

    def test_test_delete_file_system_exception(self, filesystem_module_mock):
        self.get_filesystem_args.update({"path": "/ifs/ATest3", "recursive_force_delete": True, "access_zone": "System", "state": "absent"})
        filesystem_module_mock.module.params = self.get_filesystem_args
        filesystem_module_mock.protocol_api.list_nfs_exports = MagicMock(side_effect=MockApiException)
        filesystem_module_mock.determine_error = MagicMock()
        filesystem_module_mock.perform_module_operation()
        assert MockFileSystemApi.delete_file_system_response('error') in \
            filesystem_module_mock.module.fail_json.call_args[1]['msg']
