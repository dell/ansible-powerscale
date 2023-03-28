# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock API responses for PowerScale SMB file module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.smb_file.utils'

SmbFile = {'openfiles': [{
    'file': 'C:\\ifs',
    'id': 1593,
    'locks': 0,
    'permissions': ['read'],
    'user': 'admin'}]}


def get_smb_file_failed_msg():
    return 'Getting list of SMB open files failed'


def close_smb_file_failed_msg():
    return 'Failed to close smb file'
