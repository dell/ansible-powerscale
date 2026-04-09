# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock API responses for PowerScale Job Event Info module"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


MODULE_UTILS_PATH = ('ansible_collections.dellemc.powerscale.'
    'plugins.modules.job_event_info.utils')

COMMON_ARGS = {
    "onefs_host": "test.example.com",
    "api_user": "admin",
    "api_password": "test_password",
    "verify_ssl": False,
    "state": None,
    "begin_time": None,
    "end_time": None,
    "duration": None,
    "job_id": None,
    "job_type": None,
    "event_key": None,
    "ended_jobs_only": None,
    "limit": None
}

EVENT_1 = {
    "id": "event_456",
    "job_id": 42,
    "job_type": "SmartPools",
    "state": "running",
    "event_key": "job_started",
    "timestamp": 1700000000,
    "message": "Job started successfully"
}

EVENT_2 = {
    "id": "event_457",
    "job_id": 42,
    "job_type": "SmartPools",
    "state": "succeeded",
    "event_key": "job_complete",
    "timestamp": 1700001000,
    "message": "Job completed successfully"
}

EVENT_3 = {
    "id": "event_458",
    "job_id": 43,
    "job_type": "TreeDelete",
    "state": "running",
    "event_key": "phase_start",
    "timestamp": 1700002000,
    "message": "Phase started"
}

EVENT_4 = {
    "id": "event_459",
    "job_id": 43,
    "job_type": "TreeDelete",
    "state": "failed",
    "event_key": "job_failed",
    "timestamp": 1700003000,
    "message": "Job failed due to permission error"
}

EVENTS_ALL = {"events": [EVENT_1, EVENT_2, EVENT_3, EVENT_4], "resume": None}
EVENTS_RUNNING = {"events": [EVENT_1, EVENT_3], "resume": None}
EVENTS_BY_JOB_ID = {"events": [EVENT_1, EVENT_2], "resume": None}
EVENTS_BY_TYPE = {"events": [EVENT_1, EVENT_2], "resume": None}
EVENTS_ENDED = {"events": [EVENT_2, EVENT_4], "resume": None}
EVENTS_EMPTY = {"events": [], "resume": None}
EVENTS_PAGE1 = {"events": [EVENT_1, EVENT_2], "resume": "token_abc"}
EVENTS_PAGE2 = {"events": [EVENT_3, EVENT_4], "resume": None}
EVENTS_TIME_RANGE = {"events": [EVENT_1, EVENT_2], "resume": None}


def get_events_failed_msg():
    return 'Failed to get job events'


def invalid_time_format_msg():
    return 'Invalid time format'


def negative_limit_msg():
    return 'Invalid limit value'
