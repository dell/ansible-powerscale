# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock API responses for PowerScale Event Alert Suppression module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockEventAlertSuppressionApi:

    EVENT_ID = "100010001"
    INVALID_EVENT_ID = "999999999"
    EVENT_NAME = "SYS_DISK_VARFULL"
    EVENT_CATEGORY = "100000000"
    EVENT_DESCRIPTION = "The /var partition is near capacity (>{val:.1f}% used)"
    EVENT_NODE = True

    SUPPRESSION_COMMON_ARGS = {
        "event_id": None,
        "state": None
    }

    SUPPRESSED_EVENT = {
        "suppressed": True
    }

    UNSUPPRESSED_EVENT = {
        "suppressed": False
    }

    SUPPRESSION_ENTRY = {
        "id": EVENT_ID,
        "name": EVENT_NAME,
        "category": EVENT_CATEGORY,
        "description": EVENT_DESCRIPTION,
        "node": EVENT_NODE,
        "suppressed": True
    }

    SUPPRESSION_ENTRY_2 = {
        "id": "930100005",
        "name": "HW_INFINIBAND_LINK_DOWN",
        "category": "930000000",
        "description": "Infiniband link is down",
        "node": True,
        "suppressed": True
    }

    SUPPRESSED_EVENTS_LIST = {
        "resume": None,
        "suppressions": [SUPPRESSION_ENTRY],
        "total": 1
    }

    SUPPRESSED_EVENTS_LIST_PAGE_1 = {
        "resume": "1-suppress-token",
        "suppressions": [SUPPRESSION_ENTRY],
        "total": 2
    }

    SUPPRESSED_EVENTS_LIST_PAGE_2 = {
        "resume": None,
        "suppressions": [SUPPRESSION_ENTRY_2],
        "total": 2
    }

    EMPTY_SUPPRESSED_EVENTS = {
        "resume": None,
        "suppressions": [],
        "total": 0
    }

    @staticmethod
    def get_event_alert_suppression_exception(response_type):
        err_msg_dict = {
            'get_suppress_state': f'Fetching suppression state for event {MockEventAlertSuppressionApi.EVENT_ID} '
                                  f'failed with error: SDK Error message',
            'get_invalid_suppress_state': f'Fetching suppression state for event {MockEventAlertSuppressionApi.INVALID_EVENT_ID} '
                                          f'failed with error: SDK Error message',
            'set_suppress_state': f'Updating suppression state for event {MockEventAlertSuppressionApi.EVENT_ID} '
                                  f'failed with error: SDK Error message',
            'query_all_suppressed': 'Fetching suppressed events failed with error: SDK Error message'
        }
        return err_msg_dict.get(response_type)
