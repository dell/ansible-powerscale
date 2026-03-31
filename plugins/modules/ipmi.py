#!/usr/bin/python
# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing IPMI configuration on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ipmi
version_added: "3.10.0"
short_description: Manage IPMI configuration on a PowerScale Storage System
description:
- Managing IPMI (Intelligent Platform Management Interface) configuration on
  a PowerScale system includes configuring IPMI settings, network, user,
  and features.
- IPMI provides a dedicated management channel for lights-out management
  (power control and Serial-over-LAN) via the node BMC interface, external
  to OneFS. Supported on Gen6/PowerScale nodes from OneFS 9.0 onward.
- This module supports idempotent execution, check mode, and diff mode.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
    - Shrinidhi Rao (@shrinidhirao)

options:
    settings:
        description:
        - IPMI settings configuration.
        - Used to enable/disable remote IPMI management and set the
          allocation type.
        required: false
        type: dict
        suboptions:
            enabled:
                description:
                - Whether remote IPMI management is enabled.
                type: bool
            allocation_type:
                description:
                - The IP allocation type for IPMI.
                type: str
                choices: ['dhcp', 'static', 'range']
    network:
        description:
        - IPMI network configuration for BMC.
        required: false
        type: dict
        suboptions:
            gateway:
                description:
                - The gateway IP address for the IPMI network.
                type: str
            prefixlen:
                description:
                - The network prefix length for the IPMI network.
                type: int
            ip_ranges:
                description:
                - List of IP address ranges for IPMI.
                - Each range is a dict with I(low) and I(high) keys.
                required: false
                type: list
                elements: dict
                suboptions:
                    low:
                        description:
                        - The low end of the IP address range.
                        type: str
                        required: true
                    high:
                        description:
                        - The high end of the IP address range.
                        type: str
                        required: true
    user:
        description:
        - IPMI BMC user configuration.
        required: false
        type: dict
        suboptions:
            username:
                description:
                - The BMC username.
                type: str
            password:
                description:
                - The BMC password.
                type: str
                no_log: true
    features:
        description:
        - List of IPMI features to configure.
        - Each feature is identified by I(id) and can be enabled or disabled.
        required: false
        type: list
        elements: dict
        suboptions:
            id:
                description:
                - The feature identifier (e.g. C(power_control), C(sol)).
                type: str
                required: true
            enabled:
                description:
                - Whether the feature is enabled.
                type: bool
                required: true
    state:
        description:
        - The desired state of the IPMI configuration.
        - Value C(present) indicates that the specified IPMI configuration
          should be applied.
        required: false
        type: str
        default: present
        choices: ['present']
notes:
    - The I(check_mode) is supported.
    - The I(diff) mode is supported.
    - Requires OneFS 9.0 or later on Gen6/PowerScale nodes.
    - The modules present in this collection named as 'dellemc.powerscale'
      are built to support the Dell PowerScale storage platform.
"""

EXAMPLES = r"""
- name: Get current IPMI configuration
  dellemc.powerscale.ipmi:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"

- name: Enable IPMI with static allocation
  dellemc.powerscale.ipmi:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    settings:
      enabled: true
      allocation_type: "static"
    state: "present"

- name: Configure IPMI network
  dellemc.powerscale.ipmi:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    network:
      gateway: "10.0.0.1"
      prefixlen: 24
      ip_ranges:
        - low: "10.0.0.100"
          high: "10.0.0.200"
    state: "present"

- name: Configure IPMI user
  dellemc.powerscale.ipmi:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    user:
      username: "admin"
      password: "{{ vault_ipmi_password }}"
    state: "present"

- name: Enable power control feature
  dellemc.powerscale.ipmi:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    features:
      - id: "power_control"
        enabled: true
    state: "present"

- name: Configure all IPMI domains at once
  dellemc.powerscale.ipmi:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    settings:
      enabled: true
      allocation_type: "static"
    network:
      gateway: "10.0.0.1"
      prefixlen: 24
      ip_ranges:
        - low: "10.0.0.100"
          high: "10.0.0.200"
    user:
      username: "admin"
      password: "{{ vault_ipmi_password }}"
    features:
      - id: "power_control"
        enabled: true
      - id: "sol"
        enabled: true
    state: "present"

- name: Configure IPMI settings in check mode
  dellemc.powerscale.ipmi:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    settings:
      enabled: true
      allocation_type: "dhcp"
    state: "present"
  check_mode: true
"""

RETURN = r"""
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: false
diff:
    description: The differences between the before and after states.
    returned: when diff mode is enabled and changes are made
    type: dict
    contains:
        before:
            description: The IPMI configuration before changes.
            type: dict
        after:
            description: The IPMI configuration after changes.
            type: dict
ipmi_details:
    description: The current IPMI configuration after module execution.
    type: dict
    returned: always
    contains:
        settings:
            description: IPMI settings (enabled, allocation_type).
            type: dict
            sample: {
                "enabled": true,
                "allocation_type": "static"
            }
        network:
            description: IPMI network configuration.
            type: dict
            sample: {
                "gateway": "10.0.0.1",
                "prefixlen": 24,
                "ip_ranges": [
                    {"low": "10.0.0.100", "high": "10.0.0.200"}
                ]
            }
        user:
            description: IPMI user configuration (password is redacted).
            type: dict
            sample: {
                "username": "admin"
            }
        features:
            description: IPMI features list.
            type: list
            sample: [
                {"id": "power_control", "enabled": true},
                {"id": "sol", "enabled": true}
            ]
        nodes:
            description: IPMI nodes information (read-only).
            type: list
    sample: {
        "settings": {"enabled": true, "allocation_type": "static"},
        "network": {"gateway": "10.0.0.1", "prefixlen": 24},
        "user": {"username": "admin"},
        "features": [{"id": "power_control", "enabled": true}],
        "nodes": []
    }
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell import (
    utils,
)
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.ipmi import (
    IpmiApi,
)

LOG = utils.get_logger("ipmi")


class Ipmi(object):
    """Class with IPMI configuration operations"""

    def __init__(self):
        """Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(self.get_ipmi_parameters())

        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=True,
        )

        self.result = {"changed": False, "ipmi_details": {}}

        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(msg=PREREQS_VALIDATE["error_message"])

        self.ipmi_api = IpmiApi(self.module)
        LOG.info("Got IPMI API instance for PowerScale")
        check_mode_msg = f"Check mode flag is {self.module.check_mode}"
        LOG.info(check_mode_msg)

    def get_ipmi_config(self):
        """Get full IPMI configuration."""
        msg = "Getting IPMI configuration details"
        LOG.info(msg)
        return self.ipmi_api.get_all_ipmi_config()

    def is_settings_modify_required(self, desired, current):
        """Check if settings modification is required."""
        if desired is None:
            return {}
        modify = {}
        for key in ('enabled', 'allocation_type'):
            if desired.get(key) is not None and desired[key] != current.get(key):
                modify[key] = desired[key]
        return modify

    def is_network_modify_required(self, desired, current):
        """Check if network modification is required."""
        if desired is None:
            return {}
        modify = {}
        for key in ('gateway', 'prefixlen'):
            if desired.get(key) is not None and desired[key] != current.get(key):
                modify[key] = desired[key]
        if desired.get('ip_ranges') is not None:
            desired_ranges = desired['ip_ranges']
            current_ranges = current.get('ip_ranges', [])
            if desired_ranges != current_ranges:
                modify['ip_ranges'] = desired_ranges
        return modify

    def is_user_modify_required(self, desired, current):
        """Check if user modification is required.
        Note: password is always considered changed since the API
        does not return passwords for comparison."""
        if desired is None:
            return {}
        modify = {}
        if desired.get('username') is not None and \
                desired['username'] != current.get('username'):
            modify['username'] = desired['username']
        if desired.get('password') is not None:
            modify['password'] = desired['password']
        return modify

    def is_features_modify_required(self, desired, current_features):
        """Check if features modification is required."""
        if desired is None:
            return []
        current_map = {}
        for feat in current_features:
            feat_id = feat.get('id', feat.get('name', ''))
            current_map[feat_id] = feat
        changes = []
        for feat in desired:
            feat_id = feat['id']
            current = current_map.get(feat_id, {})
            if feat.get('enabled') is not None and \
                    feat['enabled'] != current.get('enabled'):
                changes.append(feat)
        return changes

    def get_ipmi_parameters(self):
        """Get module-specific parameters."""
        return {
            "settings": {
                "type": "dict",
                "required": False,
                "options": {
                    "enabled": {"type": "bool"},
                    "allocation_type": {
                        "type": "str",
                        "choices": ["dhcp", "static", "range"],
                    },
                },
            },
            "network": {
                "type": "dict",
                "required": False,
                "options": {
                    "gateway": {"type": "str"},
                    "prefixlen": {"type": "int"},
                    "ip_ranges": {
                        "type": "list",
                        "elements": "dict",
                        "required": False,
                        "options": {
                            "low": {"type": "str", "required": True},
                            "high": {"type": "str", "required": True},
                        },
                    },
                },
            },
            "user": {
                "type": "dict",
                "required": False,
                "options": {
                    "username": {"type": "str"},
                    "password": {"type": "str", "no_log": True},
                },
            },
            "features": {
                "type": "list",
                "elements": "dict",
                "required": False,
                "options": {
                    "id": {"type": "str", "required": True},
                    "enabled": {"type": "bool", "required": True},
                },
            },
            "state": {
                "type": "str",
                "choices": ["present"],
                "default": "present",
            },
        }


class IpmiExitHandler:
    """Handle exit"""

    def handle(self, ipmi_object, ipmi_details):
        """Handle exit"""
        ipmi_object.result["ipmi_details"] = ipmi_details
        ipmi_object.module.exit_json(**ipmi_object.result)


class IpmiModifyHandler:
    """Handle modification of IPMI configuration"""

    def handle(self, ipmi_object, ipmi_params, ipmi_details):
        """Handle modification of IPMI configuration"""
        changed = False
        before_state = {
            'settings': dict(ipmi_details.get('settings', {})),
            'network': dict(ipmi_details.get('network', {})),
            'user': {k: v for k, v in ipmi_details.get('user', {}).items()
                     if k != 'password'},
            'features': list(ipmi_details.get('features', [])),
        }

        settings_modify = ipmi_object.is_settings_modify_required(
            ipmi_params.get('settings'), ipmi_details.get('settings', {})
        )
        network_modify = ipmi_object.is_network_modify_required(
            ipmi_params.get('network'), ipmi_details.get('network', {})
        )
        user_modify = ipmi_object.is_user_modify_required(
            ipmi_params.get('user'), ipmi_details.get('user', {})
        )
        features_modify = ipmi_object.is_features_modify_required(
            ipmi_params.get('features'), ipmi_details.get('features', [])
        )

        if settings_modify or network_modify or user_modify or features_modify:
            changed = True
            if not ipmi_object.module.check_mode:
                if settings_modify:
                    msg = f"Updating IPMI settings: {settings_modify}"
                    LOG.info(msg)
                    ipmi_object.ipmi_api.update_ipmi_settings(settings_modify)

                if network_modify:
                    msg = f"Updating IPMI network: {network_modify}"
                    LOG.info(msg)
                    ipmi_object.ipmi_api.update_ipmi_network(network_modify)

                if user_modify:
                    LOG.info("Updating IPMI user configuration")
                    ipmi_object.ipmi_api.update_ipmi_user(user_modify)

                if features_modify:
                    for feat in features_modify:
                        msg = f"Updating IPMI feature: {feat['id']}"
                        LOG.info(msg)
                        ipmi_object.ipmi_api.update_ipmi_feature(
                            feat['id'], {'enabled': feat['enabled']}
                        )

                ipmi_details = ipmi_object.get_ipmi_config()
                LOG.info("Successfully updated IPMI configuration.")

            ipmi_object.result["changed"] = changed

            if ipmi_object.module._diff:
                after_state = {
                    'settings': dict(ipmi_details.get('settings', {})),
                    'network': dict(ipmi_details.get('network', {})),
                    'user': {
                        k: v for k, v
                        in ipmi_details.get('user', {}).items()
                        if k != 'password'
                    },
                    'features': list(ipmi_details.get('features', [])),
                }
                ipmi_object.result['diff'] = {
                    'before': before_state,
                    'after': after_state,
                }

        IpmiExitHandler().handle(ipmi_object, ipmi_details)


class IpmiHandler:
    """Handle IPMI module"""

    def handle(self, ipmi_object, ipmi_params):
        """Handle IPMI module"""
        ipmi_details = ipmi_object.get_ipmi_config()
        IpmiModifyHandler().handle(
            ipmi_object=ipmi_object,
            ipmi_params=ipmi_params,
            ipmi_details=ipmi_details,
        )


def main():
    """Create PowerScale IPMI object and perform action on it
    based on user input from playbook."""
    obj = Ipmi()
    IpmiHandler().handle(obj, obj.module.params)


if __name__ == "__main__":
    main()
