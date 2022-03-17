# Copyright:  (c) 2022,  DellEMC

# Apache License version 2.0 (see MODULE-LICENSE or http: //www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock Api response for Unit tests of filesystem module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockFileSystemApi:
    FILE_SYSTEM_MODULE_ARGS = {
        'unispherehost': '**.***.**.***',
        'path': None,
        'access_zone': None,
        'owner': None,
        'group': None,
        'access_control': None,
        'recursive': None,
        'recursive_force_delete': None,
        'quota': None,
        'state': None
    }

    @staticmethod
    def delete_file_system_response(response_type):
        if response_type == 'error':
            return "Deletion of Filesystem"
