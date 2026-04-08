# Copyright: (c) 2026, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of cluster services module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockClusterServicesApi:
    """MockClusterServicesApi definition."""
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'

    CLUSTER_SERVICES_COMMON_ARGS = {
        "onefs_host": "**.***.**.***",
        "nfs_service": None,
        "smb_service": None,
        "s3_service": None,
        "hdfs_service": None,
        "antivirus_service": None,
    }

    GET_NFS_RESPONSE = {"service": True}
    GET_SMB_RESPONSE = {"service": True}
    GET_S3_RESPONSE = {"service": False}
    GET_HDFS_RESPONSE = {"service": False}
    GET_ANTIVIRUS_RESPONSE = {"service": True}

    GET_NFS_DISABLED_RESPONSE = {"service": False}
    GET_SMB_DISABLED_RESPONSE = {"service": False}
    GET_S3_ENABLED_RESPONSE = {"service": True}
    GET_HDFS_ENABLED_RESPONSE = {"service": True}
    GET_ANTIVIRUS_DISABLED_RESPONSE = {"service": False}

    ENABLE_NFS_ARGS = {"nfs_service": True}
    DISABLE_NFS_ARGS = {"nfs_service": False}
    DISABLE_SMB_ARGS = {"smb_service": False}
    ENABLE_S3_ARGS = {"s3_service": True}
    ENABLE_HDFS_ARGS = {"hdfs_service": True}
    ENABLE_ANTIVIRUS_ARGS = {"antivirus_service": True}

    ENABLE_ALL_ARGS = {
        "nfs_service": True,
        "smb_service": True,
        "s3_service": True,
        "hdfs_service": True,
        "antivirus_service": True,
    }

    DISABLE_ALL_ARGS = {
        "nfs_service": False,
        "smb_service": False,
        "s3_service": False,
        "hdfs_service": False,
        "antivirus_service": False,
    }

    PARTIAL_ARGS = {
        "nfs_service": True,
        "s3_service": False,
    }

    PREREQS_VALIDATE_FAILURE = {
        "all_packages_found": False,
        "error_message": "Required SDK packages not found",
    }

    @staticmethod
    def get_cluster_services_exception_response(response_type):
        """Get cluster services exception response."""
        if response_type == 'get_nfs_exception':
            return "getting NFS service"
        elif response_type == 'get_smb_exception':
            return "getting SMB service"
        elif response_type == 'get_antivirus_exception':
            return "getting Antivirus service"
        elif response_type == 'modify_nfs_exception':
            return "Modify NFS service failed"
        elif response_type == 'modify_s3_exception':
            return "Modify S3 service failed"
        elif response_type == 'modify_antivirus_exception':
            return "Modify Antivirus service failed"
