# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock API responses for PowerScale Alert channel module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.smb.utils'


class MockAlertChannelApi:

    CHANNEL_NAME = "test"
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
        "address": ["powerscale@sample.com"],
        "send_as": "powerscale@sample.com",
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

    CHANNEL_DETAILS = {
        "channels": [
            {
                "allowed_nodes": [1],
                "enabled": "false",
                "excluded_nodes": [2],
                "id": "1",
                "name": CHANNEL_NAME,
                "rules": [],
                "type": "smtp"
            }
        ]
    }

    @staticmethod
    def get_alert_channel_exception(response_type):
        err_msg_dict = {
            'get_alert': "Fetching alert channel failed with error: SDK Error message",
            'modify_exp': "Modify alert settings failed with error: SDK Error message"
        }
        return err_msg_dict.get(response_type)
