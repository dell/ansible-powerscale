# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of IPMI module on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class MockIpmiApi:
    MODULE_UTILS_PATH = (
        "ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils"
    )

    IPMI_COMMON_ARGS = {
        "onefs_host": "**.***.**.***",
        "settings": None,
        "network": None,
        "user": None,
        "features": None,
        "state": "present",
    }

    IPMI_SETTINGS_RESPONSE = {
        "enabled": True,
        "allocation_type": "static",
    }

    IPMI_SETTINGS_EMPTY_RESPONSE = {}

    IPMI_NETWORK_RESPONSE = {
        "gateway": "10.0.0.1",
        "prefixlen": 24,
        "ip_ranges": [
            {"low": "10.0.0.100", "high": "10.0.0.200"}
        ],
    }

    IPMI_NETWORK_EMPTY_RESPONSE = {}

    IPMI_USER_RESPONSE = {
        "username": "admin",
    }

    IPMI_USER_EMPTY_RESPONSE = {}

    IPMI_FEATURES_RESPONSE = [
        {"id": "power_control", "enabled": True},
        {"id": "sol", "enabled": False},
    ]

    IPMI_FEATURES_EMPTY_RESPONSE = []

    IPMI_NODES_RESPONSE = [
        {"id": 1, "name": "node1", "ipmi_address": "10.0.0.101"},
    ]

    IPMI_FULL_CONFIG_RESPONSE = {
        "settings": IPMI_SETTINGS_RESPONSE,
        "network": IPMI_NETWORK_RESPONSE,
        "user": IPMI_USER_RESPONSE,
        "features": IPMI_FEATURES_RESPONSE,
        "nodes": IPMI_NODES_RESPONSE,
    }

    IPMI_EMPTY_CONFIG_RESPONSE = {
        "settings": IPMI_SETTINGS_EMPTY_RESPONSE,
        "network": IPMI_NETWORK_EMPTY_RESPONSE,
        "user": IPMI_USER_EMPTY_RESPONSE,
        "features": IPMI_FEATURES_EMPTY_RESPONSE,
        "nodes": [],
    }

    @staticmethod
    def get_ipmi_exception_response(response_type):
        if response_type == "get_settings_exception":
            return "Failed to get IPMI settings"
        elif response_type == "update_settings_exception":
            return "Failed to update IPMI settings"
        elif response_type == "get_network_exception":
            return "Failed to get IPMI network config"
        elif response_type == "update_network_exception":
            return "Failed to update IPMI network config"
        elif response_type == "get_user_exception":
            return "Failed to get IPMI user config"
        elif response_type == "update_user_exception":
            return "Failed to update IPMI user config"
        elif response_type == "get_features_exception":
            return "Failed to get IPMI features"
        elif response_type == "update_feature_exception":
            return "Failed to update IPMI feature"
