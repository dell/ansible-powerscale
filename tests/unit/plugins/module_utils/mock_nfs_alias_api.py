# Copyright: (c) 2022-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
