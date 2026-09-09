# Copyright: (c) 2022-2026, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of smartquota module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from mock.mock import MagicMock


class MockSmartQuotaApi:
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'
    PATH1 = "/Test/Test1"
    PATH2 = "Test / Test1"
    SID = "S-1-5-21-2130"

    SMART_QUOTA_COMMON_ARGS = {
        "unispherehost": "**.***.**.***",
        "path": None,
        "access_zone": None,
        "quota_type": None,
        "user_name": None,
        "group_name": None,
        "provider_type": None,
        "quota": None,
        "list_snapshots": None,
        "state": None,
        "description": None,
        "labels": None,
        "force": None
    }

    GET_QUOTA_WITH_NEW_PARAMS = {
        "id": "2nQKAAEAAAAAAAAAAAAAQIMCAAAAAAAA",
        "path": "/ifs/Test/Test1",
        "type": "directory",
        "enforced": True,
        "container": False,
        "include_snapshots": False,
        "description": "Test quota description",
        "labels": "test,prod",
        "thresholds": {
            "advisory": 3221225472,
            "hard": 10737418240,
            "soft": 5368709120,
            "soft_grace": 86400,
            "percent_soft": 80.0,
            "percent_advisory": 50.0,
            "advisory_exceeded": False,
            "advisory_last_exceeded": 0,
            "hard_exceeded": False,
            "hard_last_exceeded": 0,
            "soft_exceeded": False,
            "soft_last_exceeded": 0
        },
        "thresholds_on": "fs_logical_size"
    }

    GET_DEFAULT_DIRECTORY_QUOTA = {
        "id": "3nQKAAEAAAAAAAAAAAAAQIMCAAAAAAAA",
        "path": "/ifs/Test/Test1",
        "type": "default-directory",
        "enforced": True,
        "container": False,
        "include_snapshots": False,
        "description": "",
        "labels": "",
        "thresholds": {
            "advisory": None,
            "hard": 10737418240,
            "soft": None,
            "soft_grace": None,
            "percent_soft": None,
            "percent_advisory": None,
            "advisory_exceeded": False,
            "advisory_last_exceeded": None,
            "hard_exceeded": False,
            "hard_last_exceeded": None,
            "soft_exceeded": False,
            "soft_last_exceeded": None
        },
        "thresholds_on": "fs_logical_size"
    }

    @staticmethod
    def get_group_details():
        get_quota_response = MagicMock()
        get_quota_response.quotas = MagicMock()
        get_quota_response.quotas.id = MockSmartQuotaApi.SID
        group_details = MagicMock()
        group_details.quotas = [
            get_quota_response
        ]
        return group_details

    @staticmethod
    def get_user_sid():
        user1 = MagicMock()
        user1.sid = MagicMock()
        user1.sid.id = MockSmartQuotaApi.SID
        sample_user_response = MagicMock()
        sample_user_response.users = [
            user1
        ]
        return sample_user_response

    @staticmethod
    def get_group_sid():
        group1 = MagicMock()
        group1.sid = MagicMock()
        group1.sid.id = MockSmartQuotaApi.SID
        sample_group_response = MagicMock()
        sample_group_response.groups = [
            group1
        ]
        return sample_group_response

    @staticmethod
    def smartquota_create_quota_response(path):
        return "Create quota for " + path + " failed with"

    @staticmethod
    def smartquota_delete_quota_response(path):
        return "Delete quota for " + path + " failed with"

    @staticmethod
    def smartquota_get_sid_exception(name, az, provider):
        return "Failed to get " + name + \
               " details for AccessZone:" + az + " and Provider:" + provider + \
               " with error"

    @staticmethod
    def get_smartquota_dependent_response(response_type):
        if response_type == 'advisory':
            return 3221225472.0
        elif response_type == 'hard':
            return 10737418240.0
        else:
            return 5368709120.0

    NOTIFICATION_RULE_1 = {
        "id": "rule-0001",
        "condition": "exceeded",
        "threshold": "advisory",
        "action_alert": True,
        "action_email_owner": False,
        "action_email_address": None
    }

    NOTIFICATION_RULE_2 = {
        "id": "rule-0002",
        "condition": "exceeded",
        "threshold": "hard",
        "action_alert": False,
        "action_email_owner": True,
        "action_email_address": ["admin@example.com"]
    }

    @staticmethod
    def get_no_notification_rules_response():
        return {"notifications": [], "total": 0}

    @staticmethod
    def get_single_notification_rule_response():
        return {"notifications": [MockSmartQuotaApi.NOTIFICATION_RULE_1], "total": 1}

    @staticmethod
    def get_multiple_notification_rules_response():
        return {
            "notifications": [
                MockSmartQuotaApi.NOTIFICATION_RULE_1,
                MockSmartQuotaApi.NOTIFICATION_RULE_2
            ],
            "total": 2
        }

    @staticmethod
    def smartquota_notification_rule_create_response():
        return {"id": "rule-0001"}

    @staticmethod
    def smartquota_notification_list_error_response(quota_id):
        return "List notification rules for quota " + quota_id + " failed with"

    @staticmethod
    def smartquota_notification_create_error_response(quota_id):
        return "Create notification rule for quota " + quota_id + " failed with"

    @staticmethod
    def smartquota_notification_update_error_response(rule_id, quota_id):
        return "Update notification rule " + rule_id + " for quota " + quota_id + " failed with"

    @staticmethod
    def smartquota_notification_delete_error_response(rule_id, quota_id):
        return "Delete notification rule " + rule_id + " for quota " + quota_id + " failed with"

    @staticmethod
    def smartquota_notification_delete_all_error_response(quota_id):
        return "Delete notification rules for quota " + quota_id + " failed with"
