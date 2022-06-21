# Copyright: (c) 2022, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http: //www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock Api response for Unit tests of smartquota module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockSmartQuotaApi:
    Smart_Quota_MODULE_ARGS = {"unispherehost": "**.***.**.***",
                               "path": None,
                               "access_zone": None,
                               "quota": None,
                               "list_snapshots": None,
                               "state": None
                               }

    @staticmethod
    def smartquota_create_quota_response(error, path):
        return "Create quota for" + path + "failed with"

    @staticmethod
    def get_smartquota_dependent_response(response_type):
        if response_type == 'advisory':
            return 3221225472.0
        elif response_type == 'hard':
            return 10737418240.0
        else:
            return 5368709120.0
