# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock API responses for PowerScale Alert channel module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.smb.utils'


class MockAlertChannelApi:

    CHANNEL_NAME = "test"
    ENABLED = True
    ALERT_COMMON_ARGS = {
        "state": "present",
        "enabled": None,
        "name": None,
        "type": None,
        "allowed_nodes": None,
        "excluded_nodes": None,
        "send_test_alert": None,
        "smtp_parameters": None
    }

    SMTP_ARGS = {
        "send_to": ["powerscale@sample.com"],
        "send_from": "powerscale@sample.com",
        "smtp_port": 25,
        "subject": "test subject",
        "smtp_host": "sample.com",
        "batch": "ALL",
        "batch_period": 3600,
        "smtp_use_auth": True,
        "smtp_username": "powerscale",
        "smtp_password": "powerscale",
        "smtp_security": "STARTTLS",
        "update_password": "on_create"
    }

    INVALID_USE_AUTH = {
        "smtp_use_auth": True
    }

    SMTP_ARGS2 = {
        "smtp_use_auth": True,
        "smtp_username": "powerscale1",
        "smtp_password": "powerscale1",
        "update_password": "always"
    }

    CHANNEL_DETAILS = {
        "channels": [
            {
                "allowed_nodes": [1],
                "enabled": "false",
                "excluded_nodes": [2],
                "id": "1",
                "name": CHANNEL_NAME,
                "parameters": {
                    "address": ["sample1@sample.com"],
                    "batch": "ALL",
                    "batch_period": 3600,
                    "send_as": "sample1@sample.com",
                    "smtp_port": 587,
                    "smtp_host": "pscalehost.com",
                    "smtp_use_auth": False,
                    "smtp_username": "pscle_user",
                    "subject": "sample subject",
                    "smtp_security": "NONE"
                },
                "rules": [],
                "type": "smtp"
            }
        ]
    }

    @staticmethod
    def get_alert_channel_exception(response_type):
        err_msg_dict = {
            'get_alert': "Fetching alert channel failed with error: SDK Error message",
            'create_exp': "Failed to create alert channel test with error: SDK Error message",
            'test_alert_exp': "Failed to send test alert for alert channel test with error: SDK Error message",
            'delete_exp': "Failed to delete alert channel test with error: SDK Error messag",
            'modify_exp': "Failed to modify alert channel test with error: SDK Error message",
            'invalid_name1': "Invalid alert channel name. Provide valid name",
            'invalid_name2': "Invalid alert channel name. Name cannot contain slashes. Provide valid name",
            'smtp_auth_err': "smtp_username is required while enabling smtp_use_auth. Provide valid smtp_username"
        }
        return err_msg_dict.get(response_type)
