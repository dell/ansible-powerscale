# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock API responses for PowerScale Alert Settings module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.smb.utils'


class MockAlertSettingsApi:

    ALERT_COMMON_ARGS = {
        "enable_celog_maintenance_mode": None
    }

    SETTING_DETAILS = {
        "history": {
            "end": 0,
            "start": 1719831994
        },
        "maintenance": "false"
    }

    CLUSTER_MAINTENANCE_SETTINGS = {
        "active": False,
        "auto_enable": True,
        "components": [
            {
                "active": False,
                "enabled": True,
                "name": "celog"
            }
        ],
        "history": [
            {
                "end": 1750140390,
                "mode": "auto",
                "start": 1750139155
            },
            {
                "end": 1750344097,
                "mode": "manual",
                "start": 1750344011
            }
        ],
        "manual_window_enabled": False,
        "manual_window_hours": 8,
        "manual_window_start": 0
    }

    @staticmethod
    def get_alert_exception_response(response_type):
        err_msg_dict = {
            'get_alert': "Fetching maintenance events failed with error",
            'modify_exp': "Modify alert settings failed with error: SDK Error message"
        }
        return err_msg_dict.get(response_type)
