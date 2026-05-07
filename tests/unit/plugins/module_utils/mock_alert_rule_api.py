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

    GET_EXISTING_ALERT_RULE_OPTIONS = [
        {
            "alert_conditions": [{
                "state": 'present',
                "name": "alert_rule",
                "id": "alert_rule",
                "categories": ["100000000"],
                "channels": ["SupportAssist"],
                "condition": "NEW",
                "eventgroup_ids": ["100010001", "100010002"],
                "exclude_eventgroup_ids": ["100010005"],
                "interval": 10,
                "limit": 10,
                "severities": ["emergency"],
                "transient": 10}]}]

    DELETE_EXISTING_ALERT_RULE_OPTIONS = {
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

    EVENT_CATEGORY = {
        'categories': [
            {'id': '100000000', 'id_name': 'SYS_DISK_EVENTS'},
            {'id': '1100000000', 'id_name': 'CPOOL_EVENTS'},
            {'id': '200000000', 'id_name': 'NODE_STATUS_EVENTS'},
            {'id': '300000000', 'id_name': 'REBOOT_EVENTS'},
            {'id': '400000000', 'id_name': 'SW_EVENTS'},
            {'id': '500000000', 'id_name': 'QUOTA_EVENTS'},
            {'id': '600000000', 'id_name': 'SNAP_EVENTS'},
            {'id': '700000000', 'id_name': 'WINNET_EVENTS'},
            {'id': '800000000', 'id_name': 'FILESYS_EVENTS'},
            {'id': '900000000', 'id_name': 'HW_EVENTS'}]}
