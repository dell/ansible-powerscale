# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of alert rule module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockAlertRuleApi:

    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'

    ALERT_RULE_COMMON_ARGS = {
        "onefs_host": "***.***.***.***",
        "validate_certs": False,
        "state": 'present',
        "name": "alert_rule",
        "categories": [],
        "channels": ["SupportAssist"],
        "condition": "NEW",
        "eventgroup_ids": ["100010001"],
        "exclude_eventgroup_ids": [],
        "interval": 0,
        "limit": 0,
        "severities": [],
        "transient": 0,
    }

    UPDATE_ALERT_RULE_OPTIONS = {
        "state": 'present',
        "name": "alert_rule",
        "categories": ["SYS_DISK_EVENTS", "NODE_STATUS_EVENTS"],
        "channels": ["SupportAssist"],
        "condition": "NEW",
        "eventgroup_ids": ["100010001", "100010002", "100010003"],
        "exclude_eventgroup_ids": ["100010005"],
        "interval": 10,
        "limit": 10,
        "severities": ["emergency", "critical"],
        "transient": 10,
    }

    EXISTING_ALERT_RULE_OPTIONS = {
        "state": 'present',
        "name": "alert_rule",
        "id": "alert_rule",
        "categories": ["SYS_DISK_EVENTS"],
        "channels": ["SupportAssist"],
        "condition": "NEW",
        "eventgroup_ids": ["100010001", "100010002"],
        "exclude_eventgroup_ids": ["100010005"],
        "interval": 10,
        "limit": 10,
        "severities": ["emergency"],
        "transient": 10,
    }

    DELETE_ALERT_RULE_OPTIONS = {
        "state": 'absent',
        "name": "alert_rule"
    }
