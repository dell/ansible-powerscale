# Copyright: (c) 2023, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of NFS global settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockNFSGlobalSettingsApi:
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'

    NFS_GLOBAL_COMMON_ARGS = {
        "onefs_host": "**.***.**.***",
        "nfsv3_enabled": None,
        "nfsv3": None,
        "nfsv4": None,
        "rpc_maxthreads": 20,
        "rpc_minthreads": 17,
        "rquota_enabled": None,
        "service": None
    }
    GET_NFS_GLOBAL_RESPONSE = {
        "nfsv3_enabled": False,
        "nfsv3_rdma_enabled": True,
        "nfsv40_enabled": True,
        "nfsv41_enabled": True,
        "nfsv42_enabled": False,
        "nfsv4_enabled": True,
        "rpc_maxthreads": 20,
        "rpc_minthreads": 17,
        "rquota_enabled": True,
        "service": True
    }

    @staticmethod
    def get_nfs_global_settings_exception_response(response_type):
        if response_type == 'get_details_exception':
            return "Got error SDK Error message while getting NFS global setings details "
        elif response_type == 'update_exception':
            return "Modify NFS global settings failed with error: SDK Error message"
