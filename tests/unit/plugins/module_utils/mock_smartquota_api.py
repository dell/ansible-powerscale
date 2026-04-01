# Copyright: (c) 2022-2024, Dell Technologies

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
