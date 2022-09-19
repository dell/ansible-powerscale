# Copyright: (c) 2022, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock API responses for PowerScale NFS Alias module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.nfs_alias.utils'

NFS_ALIAS = {'aliases': [{'health': 'unknown',
                          'id': '/test_alias_1',
                          'name': '/test_alias_1',
                          'path': '/ifs/Test',
                          'zone': 'System'}]}

CREATE_NFS_ALIAS_PARAMS = {"name": "/test_alias_1",
                           "path": "/ifs/Test"}

MODIFY_NFS_ALIAS_PARAMS = {"name": "/Renamed_test_alias_1",
                           "path": "/ifs/Test/sample1"}


def create_nfs_alias_failed_msg():
    return 'failed with error:'


def modify_nfs_alias_failed_msg():
    return 'failed with error:'
