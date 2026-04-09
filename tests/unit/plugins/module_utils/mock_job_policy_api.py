# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock API responses for PowerScale Job Policy module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


MODULE_UTILS_PATH = ('ansible_collections.dellemc.powerscale.'
    'plugins.modules.job_policy.utils')

COMMON_ARGS = {
    "onefs_host": "test.example.com",
    "api_user": "admin",
    "api_password": "test_password",
    "verify_ssl": False,
    "policy_name": None,
    "policy_id": None,
    "description": "",
    "intervals": None,
    "state": "present"
}

POLICY_1 = {
    "id": "policy_001",
    "name": "BusinessHours",
    "description": "Low impact during business hours",
    "system": False,
    "intervals": [
        {"begin": "Monday 08:00", "end": "Friday 17:00", "impact": "Low"},
        {"begin": "Saturday 00:00", "end": "Sunday 23:59", "impact": "High"}
    ]
}

POLICY_SYSTEM = {
    "id": "policy_sys_001",
    "name": "DEFAULT",
    "description": "System default policy",
    "system": True,
    "intervals": [
        {"begin": "Monday 00:00", "end": "Sunday 23:59", "impact": "Low"}
    ]
}

POLICY_2 = {
    "id": "policy_002",
    "name": "OffHours",
    "description": "High impact during off hours",
    "system": False,
    "intervals": [
        {"begin": "Monday 18:00", "end": "Friday 07:00", "impact": "High"}
    ]
}

POLICIES_LIST = {"policies": [POLICY_1, POLICY_SYSTEM, POLICY_2]}
CREATE_POLICY_RESPONSE = {"id": "policy_003"}

POLICY_MODIFIED = {
    "id": "policy_001",
    "name": "BusinessHours",
    "description": "Updated description",
    "system": False,
    "intervals": [
        {"begin": "Monday 09:00", "end": "Friday 18:00", "impact": "Medium"}
    ]
}

POLICIES_LIST_MODIFIED = {"policies": [
    POLICY_MODIFIED, POLICY_SYSTEM, POLICY_2]}


def create_policy_failed_msg():
    return 'Failed to create job policy'


def modify_policy_failed_msg():
    return 'Failed to modify job policy'


def delete_policy_failed_msg():
    return 'Failed to delete job policy'


def system_policy_protect_msg():
    return 'system policy'


def missing_policy_name_msg():
    return 'policy_name'


def invalid_interval_format_msg():
    return 'Invalid interval'


def bad_impact_value_msg():
    return 'Invalid impact'
