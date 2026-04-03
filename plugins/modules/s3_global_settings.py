#!/usr/bin/python
# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing S3 global settings on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: s3_global_settings
version_added: '3.2.0'
short_description: Manage S3 global settings on a PowerScale Storage System
description:
- Managing S3 global settings on a PowerScale system includes retrieving details of
  S3 global settings and modifying S3 global settings.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Dell Technologies Ansible Team <ansible.team@dell.com>

options:
  http_port:
    description:
    - Specifies the HTTP port for S3 service.
    - Valid range is 1024-65535.
    type: int
  https_port:
    description:
    - Specifies the HTTPS port for S3 service.
    - Valid range is 1024-65535.
    type: int
  https_only:
    description:
    - Specifies if HTTPS only mode is enabled for S3 service.
    type: bool
  service:
    description:
    - Specifies if the S3 service is enabled.
    type: bool
notes:
- The I(check_mode) is supported.
'''

EXAMPLES = r'''
- name: Get S3 global settings
  dellemc.powerscale.s3_global_settings:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"  # example
    verify_ssl: "{{ verify_ssl }}"

- name: Update S3 global settings
  dellemc.powerscale.s3_global_settings:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"  # example
    verify_ssl: "{{ verify_ssl }}"
    http_port: 9020
    https_port: 9021
    https_only: true
    service: true
'''

RETURN = r'''
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
s3_global_settings_details:
    description: The updated S3 global settings details.
    type: dict
    returned: always
    contains:
        http_port:
            description: The HTTP port for S3 service.
            type: int
        https_port:
            description: The HTTPS port for S3 service.
            type: int
        https_only:
            description: Whether HTTPS only mode is enabled.
            type: bool
        service:
            description: Whether the S3 service is enabled.
            type: bool
    sample: {
        "http_port": 9020,
        "https_port": 9021,
        "https_only": false,
        "service": true
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('s3_global_settings')


class S3GlobalSettings:
    """Class with S3 global settings operations"""

    def __init__(self):
        """Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(self.get_s3_global_settings_parameters())
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=True
        )
        self.result = {
            "changed": False,
            "s3_global_settings_details": {}
        }

        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        LOG.info('Got python SDK instance for provisioning on PowerScale ')
        check_mode_msg = f'Check mode flag is {self.module.check_mode}'
        LOG.info(check_mode_msg)

        self.protocol_api = self.isi_sdk.ProtocolsApi(self.api_client)

    def validate_input(self):
        """Validate port range parameters."""
        params = self.module.params
        for port_param in ['http_port', 'https_port']:
            port_val = params.get(port_param)
            if port_val is not None and (port_val < 1024 or port_val > 65535):
                self.module.fail_json(
                    msg=f"{port_param} value {port_val} is not in the valid port range (1024-65535).")

    def get_s3_global_settings_details(self):
        """Get details of S3 global settings."""
        msg = "Getting S3 global settings details"
        LOG.info(msg)
        try:
            s3_global_obj = self.protocol_api.get_s3_settings_global()
            if s3_global_obj:
                raw = s3_global_obj.to_dict() if hasattr(s3_global_obj, 'to_dict') else s3_global_obj.settings.to_dict()
                settings = raw.get('settings', raw) if isinstance(raw, dict) else raw
                msg = f"S3 global settings details are: {settings}"
                LOG.info(msg)
                return settings
        except Exception as e:
            error_msg = f"Got error {utils.determine_error(e)} while getting" \
                        f" S3 global settings details"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def modify_s3_global_settings(self, modify_dict):
        """Modify the S3 global settings."""
        try:
            msg = "Modify S3 global settings with parameters"
            LOG.info(msg)
            if not self.module.check_mode:
                self.protocol_api.update_s3_settings_global(
                    s3_settings_global=modify_dict)
                LOG.info("Successfully modified the S3 global settings.")
            return True
        except Exception as e:
            error_msg = f"Modify S3 global settings failed with " \
                        f"error: {utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def is_s3_global_modify_required(self, settings_params, settings_details):
        """Check whether modification is required."""
        modify_dict = {}
        keys = ["http_port", "https_port", "https_only", "service"]
        for key in keys:
            if key in settings_params and settings_params[key] is not None and \
                    settings_details.get(key) != settings_params[key]:
                modify_dict[key] = settings_params[key]
        return modify_dict

    def get_s3_global_settings_parameters(self):
        """Get s3 global settings parameters."""
        return dict(
            http_port=dict(type='int'),
            https_port=dict(type='int'),
            https_only=dict(type='bool'),
            service=dict(type='bool')
        )


class S3GlobalSettingsExitHandler:
    """S3GlobalSettingsExitHandler definition."""
    def handle(self, s3_global_obj, s3_global_details):
        """Handle."""
        s3_global_obj.result["s3_global_settings_details"] = s3_global_details
        s3_global_obj.module.exit_json(**s3_global_obj.result)


class S3GlobalSettingsModifyHandler:
    """S3GlobalSettingsModifyHandler definition."""
    def handle(self, s3_global_obj, s3_global_params, s3_global_details):
        """Handle."""
        modify_params = s3_global_obj.is_s3_global_modify_required(
            s3_global_params, s3_global_details)
        if modify_params:
            if hasattr(s3_global_obj.module, '_diff') and s3_global_obj.module._diff:
                s3_global_obj.result['diff'] = {
                    'before': dict(s3_global_details),
                    'after': {**s3_global_details, **modify_params}
                }
            changed = s3_global_obj.modify_s3_global_settings(
                modify_dict=modify_params)
            s3_global_details = s3_global_obj.get_s3_global_settings_details()
            s3_global_obj.result["changed"] = changed
            s3_global_obj.result["s3_global_settings_details"] = s3_global_details

        S3GlobalSettingsExitHandler().handle(s3_global_obj, s3_global_details)


class S3GlobalSettingsHandler:
    """S3GlobalSettingsHandler definition."""
    def handle(self, s3_global_obj, s3_global_params):
        """Handle."""
        s3_global_obj.validate_input()
        s3_global_details = s3_global_obj.get_s3_global_settings_details()
        S3GlobalSettingsModifyHandler().handle(
            s3_global_obj=s3_global_obj, s3_global_params=s3_global_params,
            s3_global_details=s3_global_details)


def main():
    """Perform action on PowerScale S3 Global settings."""
    obj = S3GlobalSettings()
    S3GlobalSettingsHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
