# Copyright: (c) 2026, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock API responses for PowerScale Job Report Info module"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


MODULE_UTILS_PATH = ('ansible_collections.dellemc.powerscale.'
                     'plugins.modules.job_report_info.utils')

COMMON_ARGS = {
    "onefs_host": "test.example.com",
    "api_user": "admin",
    "api_password": "test_password",
    "verify_ssl": False,
    "job_type": None,
    "job_id": None,
    "event_key": None,
    "begin": None,
    "end": None,
    "last_phase_only": None,
    "verbose": None,
    "limit": None
}

REPORT_1 = {
    "id": "report_123",
    "job_id": 42,
    "job_type": "SmartPools",
    "event_key": "phase_complete",
    "phase": "analyze",
    "timestamp": 1700000000,
    "statistics": {"files_processed": 10000, "errors": 0, "warnings": 5}
}

REPORT_2 = {
    "id": "report_124",
    "job_id": 42,
    "job_type": "SmartPools",
    "event_key": "job_complete",
    "phase": "finalize",
    "timestamp": 1700001000,
    "statistics": {"files_processed": 10000, "errors": 0, "warnings": 0}
}

REPORT_3 = {
    "id": "report_125",
    "job_id": 43,
    "job_type": "TreeDelete",
    "event_key": "phase_complete",
    "phase": "delete",
    "timestamp": 1700002000,
    "statistics": {"files_processed": 500, "errors": 1, "warnings": 0}
}

REPORTS_ALL = {"reports": [REPORT_1, REPORT_2, REPORT_3], "resume": None}
REPORTS_BY_TYPE = {"reports": [REPORT_1, REPORT_2], "resume": None}
REPORTS_BY_JOB_ID = {"reports": [REPORT_1, REPORT_2], "resume": None}
REPORTS_BY_EVENT_KEY = {"reports": [REPORT_1, REPORT_3], "resume": None}
REPORTS_LAST_PHASE = {"reports": [REPORT_2], "resume": None}
REPORTS_VERBOSE = {"reports": [REPORT_1, REPORT_2, REPORT_3], "resume": None}
REPORTS_LIMITED = {"reports": [REPORT_1], "resume": None}
REPORTS_EMPTY = {"reports": [], "resume": None}
REPORTS_PAGE1 = {"reports": [REPORT_1, REPORT_2], "resume": "token_xyz"}
REPORTS_PAGE2 = {"reports": [REPORT_3], "resume": None}


def get_reports_failed_msg():
    return 'Failed to get job reports'
