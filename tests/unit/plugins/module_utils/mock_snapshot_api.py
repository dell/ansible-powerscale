# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock API responses for PowerScale Snapshot module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.snapshot.utils'

SNAPSHOT = {
    "snapshots": [
        {
            "alias": "alias_name_1",
            "created": 1628155527,
            "expires": 10,
            "has_locks": False,
            "id": 936,
            "name": "ansible_test_snapshot",
            "path": "/ifs/ansible_test_snapshot",
            "pct_filesystem": 2.435778242215747e-06,
            "pct_reserve": 0.0,
            "schedule": None,
            "shadow_bytes": 0,
            "size": 4096,
            "state": "active",
            "target_id": None,
            "target_name": None
        }
    ]
}

SNAPSHOT_WO_EXPIRES = {
    "snapshots": [
        {
            "alias": "alias_name_1",
            "created": 1628155527,
            "has_locks": False,
            "id": 936,
            "name": "ansible_test_snapshot",
            "path": "/ifs/ansible_test_snapshot",
            "pct_filesystem": 2.435778242215747e-06,
            "pct_reserve": 0.0,
            "schedule": None,
            "shadow_bytes": 0,
            "size": 4096,
            "state": "active",
            "target_id": None,
            "target_name": None
        }
    ]
}

ALIAS = {
    "snapshots": [
        {
            "target_name": "ansible_test_snapshot",
            "name": "alias_name_1"
        }
    ]
}

CREATE_SNAPSHOT_PARAMS = {
    "name": "ansible_test_snapshot",
    "path": "/ifs/ansible_test_snapshot",
    "alias": "snap_alias_1",
    "expires": 60}

MODIFY_SNAPSHOT_PARAMS = {"expires": 60}

RENAME_SNAPSHOT_PARAMS = {"name": "renamed_snapshot_name_1"}


def create_snapshot_failed_msg():
    return 'Failed to create snapshot'


def modify_snapshot_failed_msg():
    return 'Failed to modify snapshot'


def rename_snapshot_failed_msg():
    return 'Failed to rename snapshot'


def invalid_access_zone_failed_msg():
    return 'Unable to fetch base path of Access Zone invalid_zone ,failed with error: SDK Error message'


def get_snapshot_wo_name_failed_msg():
    return 'Please provide a valid snapshot name'


def modify_snapshot_wo_desired_retention_failed_msg():
    return 'Specify desired retention along with retention unit.'


def delete_snapshot_exception_failed_msg():
    return 'Failed to delete snapshot'


def get_snapshot_alias_failed_msg():
    return 'Failed to get alias for snapshot'


def create_snapshot_wo_retention_failed_msg():
    return 'Please provide either desired_retention or expiration_timestamp for creating a snapshot'


def create_snapshot_with_new_name_failed_msg():
    return 'Invalid param: new_name while creating a new snapshot.'


def create_snapshot_without_path_failed_msg():
    return 'Please provide a valid path for snapshot creation'


def create_snapshot_wo_desired_retention_failed_msg():
    return 'Desired retention is set to'


def create_snapshot_invalid_desired_retention_failed_msg():
    return 'Please provide a valid integer as the desired retention.'


def modify_non_existing_path_failed_msg():
    return 'specified in the playbook does not match the path of the snapshot'


def get_snapshot_failed_msg():
    return 'Failed to get details of Snapshot'
