# Copyright: (c) 2026, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock API responses for PowerScale Job Type Info module"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


MODULE_UTILS_PATH = ('ansible_collections.dellemc.powerscale.'
                     'plugins.modules.job_type_info.utils')

COMMON_ARGS = {
    "onefs_host": "test.example.com",
    "api_user": "admin",
    "api_password": "test_password",
    "verify_ssl": False,
    "job_type_id": None,
    "include_hidden": False,
    "sort": None,
    "dir": None
}

TYPE_TREE_DELETE = {
    "id": "TreeDelete",
    "name": "Tree Delete",
    "description": "Delete directory trees",
    "is_hidden": False,
    "enabled": True,
    "priority": 5,
    "policy": "LOW",
    "schedule": None,
    "allow_multiple_instances": False,
    "exclusion_set": "filesystem_ops"
}

TYPE_SMARTPOOLS = {
    "id": "SmartPools",
    "name": "SmartPools",
    "description": "SmartPools tiering operations",
    "is_hidden": False,
    "enabled": True,
    "priority": 4,
    "policy": "LOW",
    "schedule": "0 0 * * *",
    "allow_multiple_instances": False,
    "exclusion_set": "restripe_ops"
}

TYPE_HIDDEN = {
    "id": "IntegrityCheck",
    "name": "Integrity Check",
    "description": "Internal integrity check",
    "is_hidden": True,
    "enabled": True,
    "priority": 1,
    "policy": "HIGH",
    "schedule": None,
    "allow_multiple_instances": False,
    "exclusion_set": "system_ops"
}

TYPES_VISIBLE = {"types": [TYPE_TREE_DELETE, TYPE_SMARTPOOLS]}
TYPES_ALL = {"types": [TYPE_TREE_DELETE, TYPE_SMARTPOOLS, TYPE_HIDDEN]}
TYPES_SORTED = {"types": [TYPE_SMARTPOOLS, TYPE_TREE_DELETE]}
TYPES_EMPTY = {"types": []}


def get_job_types_failed_msg():
    return 'Failed to get job types'


def get_job_type_failed_msg():
    return 'Failed to get job type details'
