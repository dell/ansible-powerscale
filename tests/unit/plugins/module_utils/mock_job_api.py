# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock API responses for PowerScale Job module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


MODULE_UTILS_PATH = ('ansible_collections.dellemc.powerscale.'
                     'plugins.modules.job.utils')

COMMON_ARGS = {
    "onefs_host": "test.example.com",
    "api_user": "admin",
    "api_password": "test_password",
    "verify_ssl": False,
    "job_id": None,
    "job_type": None,
    "job_state": None,
    "paths": None,
    "priority": None,
    "policy": None,
    "allow_dup": False,
    "job_params": None,
    "wait": False,
    "wait_timeout": 300,
    "wait_interval": 10,
    "state": "present"
}

JOB_RUNNING = {
    "jobs": [{
        "id": 42,
        "type": "SmartPools",
        "state": "running",
        "priority": 5,
        "policy": "LOW",
        "description": "SmartPools job",
        "start_time": 1700000000,
        "end_time": None,
        "progress": 45,
        "paths": ["/ifs/data"],
        "parameters": {}
    }]
}

JOB_PAUSED = {
    "jobs": [{
        "id": 42,
        "type": "SmartPools",
        "state": "paused_user",
        "priority": 5,
        "policy": "LOW",
        "description": "SmartPools job",
        "start_time": 1700000000,
        "end_time": None,
        "progress": 45,
        "paths": ["/ifs/data"],
        "parameters": {}
    }]
}

JOB_SUCCEEDED = {
    "jobs": [{
        "id": 42,
        "type": "SmartPools",
        "state": "succeeded",
        "priority": 5,
        "policy": "LOW",
        "description": "SmartPools job completed",
        "start_time": 1700000000,
        "end_time": 1700005000,
        "progress": 100,
        "paths": ["/ifs/data"],
        "parameters": {}
    }]
}

JOB_CANCELLED = {
    "jobs": [{
        "id": 42,
        "type": "SmartPools",
        "state": "cancelled_user",
        "priority": 5,
        "policy": "LOW",
        "description": "SmartPools job cancelled",
        "start_time": 1700000000,
        "end_time": 1700003000,
        "progress": 45,
        "paths": ["/ifs/data"],
        "parameters": {}
    }]
}

CREATE_JOB_RESPONSE = {"id": 45}

JOB_CREATED = {
    "jobs": [{
        "id": 45,
        "type": "TreeDelete",
        "state": "running",
        "priority": 5,
        "policy": "LOW",
        "paths": ["/ifs/data/archive"],
        "start_time": 1700010000,
        "end_time": None,
        "progress": 0,
        "parameters": {}
    }]
}

JOB_MODIFIED_PRIORITY = {
    "jobs": [{
        "id": 42,
        "type": "SmartPools",
        "state": "running",
        "priority": 2,
        "policy": "LOW",
        "paths": ["/ifs/data"],
        "start_time": 1700000000,
        "end_time": None,
        "progress": 50,
        "parameters": {}
    }]
}

JOB_MODIFIED_POLICY = {
    "jobs": [{
        "id": 42,
        "type": "SmartPools",
        "state": "running",
        "priority": 5,
        "policy": "HIGH",
        "paths": ["/ifs/data"],
        "start_time": 1700000000,
        "end_time": None,
        "progress": 50,
        "parameters": {}
    }]
}

JOBS_LIST_EMPTY = {"jobs": [], "resume": None}
JOBS_LIST_WITH_RUNNING = {"jobs": [JOB_RUNNING["jobs"][0]], "resume": None}


def start_job_failed_msg():
    return 'Failed to start job'


def modify_job_failed_msg():
    return 'Failed to modify job'


def get_job_failed_msg():
    return 'Failed to get job details'


def cancel_completed_job_msg():
    return 'Cannot cancel'


def start_invalid_type_error_msg():
    return 'Invalid job type'


def missing_paths_error_msg():
    return 'paths'


def none_job_id_error_msg():
    return 'job_id'


def negative_priority_error_msg():
    return 'Invalid priority'


def wrong_state_error_msg():
    return 'Cannot'


def wait_timeout_msg():
    return 'timed out'
