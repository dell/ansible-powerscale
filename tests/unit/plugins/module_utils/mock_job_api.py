# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of Job module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockJobApi:
    """MockJobApi definition."""
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'

    JOB_COMMON_ARGS = {
        "onefs_host": "**.***.**.***",
        "job_id": None,
        "job_type": None,
        "job_state": None,
        "state": "present",
        "paths": None,
        "policy": None,
        "priority": None,
        "gather_subset": None,
        "filter_state": None,
        "sort": None,
        "sort_dir": None,
        "limit": None,
        "begin": None,
        "end": None,
        "event_key": None,
        "show_all": False,
        "verbose": False
    }

    CREATE_JOB_ARGS = {
        "job_type": "TreeDelete",
        "paths": ["/ifs/data"],
        "state": "present"
    }

    CREATE_JOB_WITH_POLICY_ARGS = {
        "job_type": "QuotaScan",
        "paths": ["/ifs/data"],
        "policy": "LOW_IMPACT",
        "state": "present"
    }

    CREATE_JOB_WITH_PRIORITY_ARGS = {
        "job_type": "TreeDelete",
        "paths": ["/ifs/data"],
        "priority": 5,
        "state": "present"
    }

    MODIFY_JOB_PAUSE_ARGS = {
        "job_id": 12345,
        "job_state": "pause",
        "state": "present"
    }

    MODIFY_JOB_RESUME_ARGS = {
        "job_id": 12345,
        "job_state": "run",
        "state": "present"
    }

    MODIFY_JOB_CANCEL_ARGS = {
        "job_id": 12345,
        "job_state": "cancel",
        "state": "present"
    }

    MODIFY_JOB_POLICY_ARGS = {
        "job_id": 12345,
        "policy": "HIGH_IMPACT",
        "state": "present"
    }

    MODIFY_JOB_PRIORITY_ARGS = {
        "job_id": 12345,
        "priority": 3,
        "state": "present"
    }

    GET_JOB_DETAILS_ARGS = {
        "job_id": 12345,
        "state": "present"
    }

    CREATE_JOB_RESPONSE = {"id": 12345}

    GET_JOB_RESPONSE = {
        "id": 12345,
        "type": "TreeDelete",
        "state": "running",
        "progress": "Phase 1 of 2",
        "policy": "LOW_IMPACT",
        "priority": 5
    }

    GET_JOB_PAUSED_RESPONSE = {
        "id": 12345,
        "type": "TreeDelete",
        "state": "paused_user",
        "progress": "Phase 1 of 2",
        "policy": "LOW_IMPACT",
        "priority": 5
    }

    LIST_JOBS_RESPONSE = {
        "jobs": [
            {
                "id": 12345,
                "type": "TreeDelete",
                "state": "running",
                "progress": "Phase 1 of 2"
            },
            {
                "id": 12346,
                "type": "QuotaScan",
                "state": "succeeded",
                "progress": "Complete"
            }
        ]
    }

    GET_EVENTS_RESPONSE = {
        "events": [
            {
                "id": 1,
                "job_id": 12345,
                "job_type": "TreeDelete",
                "state": "running",
                "time": 1700000000
            }
        ]
    }

    GET_REPORTS_RESPONSE = {
        "reports": [
            {
                "id": 1,
                "job_id": 12345,
                "job_type": "TreeDelete",
                "phase": 1,
                "elapsed": 120
            }
        ]
    }

    GET_TYPES_RESPONSE = {
        "types": [
            {
                "id": "TreeDelete",
                "description": "Delete a directory tree",
                "enabled": True,
                "hidden": False,
                "policy": "LOW_IMPACT",
                "priority": 5,
                "schedule": None
            },
            {
                "id": "QuotaScan",
                "description": "Scan quota usage",
                "enabled": True,
                "hidden": False,
                "policy": "LOW_IMPACT",
                "priority": 6,
                "schedule": None
            }
        ]
    }

    GET_STATISTICS_RESPONSE = {
        "statistics": [
            {
                "job_type": "TreeDelete",
                "total": 10,
                "running": 1,
                "succeeded": 8,
                "failed": 1
            }
        ]
    }

    GET_RECENT_RESPONSE = {
        "recent": [
            {
                "id": 12340,
                "type": "TreeDelete",
                "state": "succeeded",
                "end_time": 1700000000
            }
        ]
    }

    GET_SUMMARY_RESPONSE = {
        "summary": {
            "cluster_is_paused": False,
            "next": "TreeDelete (12345)",
            "running": 1,
            "paused_system": 0,
            "paused_user": 0,
            "waiting": 3
        }
    }

    GATHER_JOBS_ARGS = {
        "gather_subset": ["jobs"]
    }

    GATHER_EVENTS_ARGS = {
        "gather_subset": ["events"]
    }

    GATHER_EVENTS_FILTERED_ARGS = {
        "gather_subset": ["events"],
        "filter_state": "running",
        "begin": 1700000000
    }

    GATHER_REPORTS_ARGS = {
        "gather_subset": ["reports"]
    }

    GATHER_TYPES_ARGS = {
        "gather_subset": ["types"]
    }

    GATHER_TYPES_SHOW_ALL_ARGS = {
        "gather_subset": ["types"],
        "show_all": True
    }

    GATHER_STATISTICS_ARGS = {
        "gather_subset": ["statistics"]
    }

    GATHER_RECENT_ARGS = {
        "gather_subset": ["recent"]
    }

    GATHER_RECENT_WITH_LIMIT_ARGS = {
        "gather_subset": ["recent"],
        "limit": 5
    }

    GATHER_SUMMARY_ARGS = {
        "gather_subset": ["summary"]
    }

    GATHER_MULTIPLE_ARGS = {
        "gather_subset": ["jobs", "events", "types"]
    }

    LIST_JOBS_FILTERED_ARGS = {
        "gather_subset": ["jobs"],
        "filter_state": "running"
    }

    LIST_JOBS_SORTED_ARGS = {
        "gather_subset": ["jobs"],
        "sort": "id",
        "sort_dir": "DESC",
        "limit": 10
    }

    @staticmethod
    def get_job_exception_response(response_type):
        """Get job exception response."""
        responses = {
            'create_exception': "Failed to create job with error:",
            'get_exception': "Failed to get job details with error:",
            'modify_exception': "Failed to modify job with error:",
            'list_exception': "Failed to list jobs with error:",
            'events_exception': "Failed to get job events with error:",
            'reports_exception': "Failed to get job reports with error:",
            'types_exception': "Failed to get job types with error:",
            'statistics_exception': "Failed to get job statistics with error:",
            'recent_exception': "Failed to get recent jobs with error:",
            'summary_exception': "Failed to get job summary with error:",
            'job_type_required': "job_type is required to create a job",
            'job_id_required': "job_id is required to modify a job",
            'invalid_limit': "limit must be a positive integer",
        }
        return responses.get(response_type)
