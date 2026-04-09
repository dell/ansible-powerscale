# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock API responses for PowerScale Job Info module"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.job_info.utils'

COMMON_ARGS = {
    "onefs_host": "test.example.com",
    "api_user": "admin",
    "api_password": "test_password",
    "verify_ssl": False,
    "job_id": None,
    "state": None,
    "job_type": None,
    "sort": None,
    "dir": "ASC",
    "limit": None,
    "include_recent": False,
    "include_summary": False
}

JOB_1 = {
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
}

JOB_2 = {
    "id": 43,
    "type": "TreeDelete",
    "state": "paused_user",
    "priority": 3,
    "policy": "MEDIUM",
    "description": "TreeDelete job",
    "start_time": 1700001000,
    "end_time": None,
    "progress": 20,
    "paths": ["/ifs/data/archive"],
    "parameters": {}
}

JOB_3 = {
    "id": 44,
    "type": "SmartPools",
    "state": "succeeded",
    "priority": 5,
    "policy": "LOW",
    "description": "SmartPools job completed",
    "start_time": 1699990000,
    "end_time": 1699995000,
    "progress": 100,
    "paths": ["/ifs/data"],
    "parameters": {}
}

JOBS_LIST = {"jobs": [JOB_1, JOB_2, JOB_3], "resume": None}
JOBS_PAUSED_LIST = {
    "jobs": [{
        "id": 99,
        "type": "TreeDelete",
        "state": "paused_user",
        "priority": 3
    }],
    "resume": None
}
JOBS_RUNNING = {"jobs": [JOB_1], "resume": None}
JOBS_SMARTPOOLS = {"jobs": [JOB_1, JOB_3], "resume": None}
JOBS_SORTED_ASC = {"jobs": [JOB_1, JOB_2, JOB_3], "resume": None}
JOBS_SORTED_DESC = {"jobs": [JOB_3, JOB_2, JOB_1], "resume": None}
JOBS_LIMITED = {"jobs": [JOB_1], "resume": None}
JOBS_EMPTY = {"jobs": [], "resume": None}
JOBS_NULL_FIELDS = {"jobs": [{"id": 50, "type": "SmartPools", "state": None,
                             "priority": None, "policy": None, "description": None,
                             "start_time": None, "end_time": None, "progress": None,
                             "paths": None, "parameters": None}], "resume": None}

RECENT_JOBS = {"jobs": [
    {"id": 40, "type": "SmartPools", "state": "succeeded", "end_time": 1699999000},
    {"id": 41, "type": "TreeDelete", "state": "succeeded", "end_time": 1699998000}
]}

JOB_SUMMARY = {
    "active_jobs": 3,
    "paused_jobs": 1,
    "completed_jobs": 150,
    "failed_jobs": 2,
    "total_jobs": 156
}


def get_job_by_id_failed_msg():
    return 'Failed to get job details'


def list_jobs_failed_msg():
    return 'Failed to list jobs'


def get_recent_jobs_failed_msg():
    return 'Failed to get recent jobs'


def get_job_summary_failed_msg():
    return 'Failed to get job summary'


def get_job_invalid_id_error_msg():
    return 'Invalid job ID'
