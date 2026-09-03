# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock API responses for PowerScale Event Alert Suppression module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockEventAlertSuppressionApi:

    EVENT_ID = "100010001"
    EVENT_NAME = "SYS_DISK_VARFULL"
    EVENT_CATEGORY = "100000000"
    EVENT_DESCRIPTION = "The /var partition is near capacity (>{val:.1f}% used)"
    EVENT_NODE = True

    COMMON_ARGS = {
        "event_id": None,
        "state": None
    }

    SUPPRESSED_EVENT = {
        "suppressed": True
    }

    UNSUPPRESSED_EVENT = {
        "suppressed": False
    }

    EVENT_DETAILS = {
        "id": EVENT_ID,
        "name": EVENT_NAME,
        "category": EVENT_CATEGORY,
        "description": EVENT_DESCRIPTION,
        "node": EVENT_NODE,
        "suppressed": False
    }

    SUPPRESSED_EVENTS_LIST = {
        "resume": None,
        "suppressions": [
            {
                "id": EVENT_ID,
                "name": EVENT_NAME,
                "category": EVENT_CATEGORY,
                "description": EVENT_DESCRIPTION,
                "node": EVENT_NODE,
                "suppressed": True
            }
        ],
        "total": 1
    }

    EMPTY_SUPPRESSED_EVENTS = {
        "resume": None,
        "suppressions": [],
        "total": 0
    }

    EVENTGROUP_DEFINITIONS = {
        "eventgroup-definitions": [
            {
                "id": EVENT_ID,
                "name": EVENT_NAME,
                "category": EVENT_CATEGORY,
                "description": EVENT_DESCRIPTION,
                "node": EVENT_NODE,
                "suppressed": False
            }
        ]
    }

    @staticmethod
    def get_event_alert_suppression_exception(response_type):
        err_msg_dict = {
            'get_suppress_state': f'Fetching suppression state for event {MockEventAlertSuppressionApi.EVENT_ID} failed with error: SDK Error message',
            'set_suppress_state': f'Updating suppression state for event {MockEventAlertSuppressionApi.EVENT_ID} failed with error: SDK Error message',
            'query_all_suppressed': 'Fetching suppressed events failed with error: SDK Error message',
            'query_specific_event': f'Fetching event details for {MockEventAlertSuppressionApi.EVENT_ID} failed with error: SDK Error message',
            'invalid_event_id': f'Event {MockEventAlertSuppressionApi.EVENT_ID} is not a valid event type ID',
            'missing_event_id': 'event_id is required when state is suppressed or unsuppressed'
        }
        return err_msg_dict.get(response_type)
