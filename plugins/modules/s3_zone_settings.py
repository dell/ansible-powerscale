#!/usr/bin/python
# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing S3 zone settings on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: s3_zone_settings
version_added: '3.2.0'
short_description: Manage S3 zone settings on a PowerScale Storage System
description:
- Managing S3 zone settings on a PowerScale system includes
  retrieving details and modifying S3 zone settings.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Ansible Team (@dell-ansible-team) <ansible.team@dell.com>

options:
  access_zone:
    description:
    - Specifies the access zone in which the S3 zone settings apply.
    type: str
    default: System
  base_domain:
    description:
    - Specifies the base domain name used for the S3 service.
    type: str
  root_path:
    description:
    - Specifies the root path for the S3 service.
    type: str
  object_acl_policy:
    description:
    - Specifies the object ACL policy for S3.
    type: str
  bucket_directory_create_mode:
    description:
    - Specifies the UNIX mode bits for bucket directory creation.
    - Valid range is 0-511.
    type: int
  use_md5_for_etag:
    description:
    - If C(true), use MD5 for ETag generation.
    type: bool
  validate_content_md5:
    description:
    - If C(true), validate Content-MD5 headers on upload.
    type: bool
notes:
- The I(check_mode) is supported.
'''

EXAMPLES = r'''
- name: Get S3 zone settings
  dellemc.powerscale.s3_zone_settings:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"  # example
    verify_ssl: "{{ verify_ssl }}"
    access_zone: "System"

- name: Modify S3 zone settings
  dellemc.powerscale.s3_zone_settings:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"  # example
    verify_ssl: "{{ verify_ssl }}"
    access_zone: "System"
    base_domain: "s3.example.com"
    root_path: "/ifs/data/s3"
    object_acl_policy: "replace"
    bucket_directory_create_mode: 448
    use_md5_for_etag: true
    validate_content_md5: true
'''

RETURN = r'''
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
s3_zone_settings_details:
    description: The S3 zone settings details.
    type: dict
    returned: always
    contains:
        base_domain:
            description: The base domain name used for the S3 service.
            type: str
        root_path:
            description: The root path for the S3 service.
            type: str
        object_acl_policy:
            description: The object ACL policy for S3.
            type: str
        bucket_directory_create_mode:
            description: The UNIX mode bits for bucket directory creation.
            type: int
        use_md5_for_etag:
            description: Whether MD5 is used for ETag generation.
            type: bool
        validate_content_md5:
            description: Whether Content-MD5 headers are validated on upload.
            type: bool
        zone:
            description: Specifies the access zone in which the S3 zone
                         settings apply.
            type: str
    sample: {
        "base_domain": "",
        "bucket_directory_create_mode": 448,
        "object_acl_policy": "replace",
        "root_path": "/ifs",
        "use_md5_for_etag": false,
        "validate_content_md5": false,
        "zone": "System"
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('s3_zone_settings')


class S3ZoneSettings:
    """Class with S3 zone settings operations"""

    def __init__(self):
        """Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(self.get_s3_zone_settings_parameters())
        # Initialize the ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=True
        )
        # Result is a dictionary that contains changed status, S3 zone
        # settings details
        self.result = {
            "changed": False,
            "s3_zone_settings_details": {}
        }

        # Validate the pre-requisites packages for the module
        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        # Initialize the connection to PowerScale
        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        LOG.info('Got python SDK instance for provisioning on PowerScale ')
        check_mode_msg = f'Check mode flag is {self.module.check_mode}'
        LOG.info(check_mode_msg)

        # Initialize the APIs
        self.protocol_api = self.isi_sdk.ProtocolsApi(self.api_client)

    def get_s3_zone_settings_details(self, access_zone):
        """
        Get details of S3 zone settings for a given access zone.
        :param access_zone: Access zone
        :type access_zone: str
        :return: S3 zone settings details
        :rtype: dict
        """
        msg = f"Getting S3 zone settings details for {access_zone}" \
              f" access zone"
        LOG.info(msg)
        try:
            s3_settings_obj = self.protocol_api.get_s3_settings_zone(
                zone=access_zone)
            if s3_settings_obj:
                raw = s3_settings_obj.to_dict() \
                    if hasattr(s3_settings_obj, 'to_dict') \
                    else s3_settings_obj.settings.to_dict()
                zone_settings = raw.get('settings', raw) if isinstance(raw, dict) else raw

                # Appending the Access zone
                zone_settings["zone"] = access_zone
                msg = f"S3 zone settings details are: {zone_settings}"
                LOG.info(msg)
                return zone_settings

        except Exception as e:
            error_msg = f"Got error {utils.determine_error(e)} while getting" \
                        f" S3 zone settings details for access zone" \
                        f": {access_zone}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def modify_zone_settings(self, modify_dict, access_zone):
        """
        Modify the S3 zone settings.
        :param modify_dict: contains parameters to modify
        :type modify_dict: dict
        :param access_zone: Access zone
        :type access_zone: str
        :return: True if successful
        :rtype: bool
        """
        try:
            msg = f"Modify S3 zone settings with parameters: " \
                  f"{modify_dict}"
            LOG.info(msg)
            if not self.module.check_mode:
                self.protocol_api.update_s3_settings_zone(
                    modify_dict, zone=access_zone)
                LOG.info("Successfully modified the S3 zone settings.")
            return True
        except Exception as e:
            error_msg = f"Modify S3 zone settings failed with " \
                        f"error: {utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def is_settings_modify_required(self, settings_params, settings_details):
        """
        Check if S3 zone settings modification is required.
        :param settings_params: contains params passed through playbook
        :param settings_details: contains details of the S3 zone settings
        :return: dict of parameters that need modification, empty if none
        :rtype: dict
        """
        modify_dict = {}
        keys = ['base_domain', 'root_path', 'object_acl_policy',
                'bucket_directory_create_mode', 'use_md5_for_etag',
                'validate_content_md5']
        for key in keys:
            if settings_params.get(key) is not None \
                    and settings_params[key] != settings_details.get(key):
                modify_dict[key] = settings_params[key]
        return modify_dict

    def validate_zone_params(self):
        """Validate access zone parameter."""

        if utils.is_param_empty_spaces(self.module.params["access_zone"]):
            err_msg = "Invalid access zone provided. Provide valid access" \
                      " zone."
            self.module.fail_json(msg=err_msg)

    def validate_input(self):
        """Validate input parameters."""
        params = self.module.params

        mode = params.get("bucket_directory_create_mode")
        if mode is not None and (mode < 0 or mode > 511):
            self.module.fail_json(
                msg="bucket_directory_create_mode is not in the valid "
                    "range (0-511).")

        base_domain = params.get("base_domain")
        if base_domain is not None and len(base_domain) > 255:
            self.module.fail_json(
                msg="base_domain must not exceed 255 characters.")

        root_path = params.get("root_path")
        if root_path is not None and len(root_path) > 4096:
            self.module.fail_json(
                msg="root_path must not exceed 4096 characters.")

    def get_s3_zone_settings_parameters(self):
        """Get s3 zone settings parameters."""
        return dict(
            access_zone=dict(default='System'),
            base_domain=dict(type='str'),
            root_path=dict(type='str'),
            object_acl_policy=dict(type='str'),
            bucket_directory_create_mode=dict(type='int'),
            use_md5_for_etag=dict(type='bool'),
            validate_content_md5=dict(type='bool'))


class S3ZoneSettingsExitHandler:
    """S3ZoneSettingsExitHandler definition."""
    def handle(self, settings_obj, settings_details):
        """Handle."""
        settings_obj.result["s3_zone_settings_details"] = settings_details
        settings_obj.module.exit_json(**settings_obj.result)


class S3ZoneSettingsModifyHandler:
    """S3ZoneSettingsModifyHandler definition."""
    def handle(self, settings_obj, settings_params, settings_details):
        """Handle."""
        if settings_details:
            modify_dict = settings_obj.is_settings_modify_required(
                settings_params, settings_details)
            if modify_dict:
                if hasattr(settings_obj.module, '_diff') \
                        and settings_obj.module._diff:
                    settings_obj.result['diff'] = {
                        'before': dict(settings_details),
                        'after': {**settings_details, **modify_dict}
                    }
                changed = settings_obj.modify_zone_settings(
                    modify_dict, settings_params["access_zone"])
                settings_details = \
                    settings_obj.get_s3_zone_settings_details(
                        access_zone=settings_params["access_zone"])
                settings_obj.result["changed"] = changed
                settings_obj.result["s3_zone_settings_details"] = \
                    settings_details

        S3ZoneSettingsExitHandler().handle(settings_obj, settings_details)


class S3ZoneSettingsHandler:
    """S3ZoneSettingsHandler definition."""
    def handle(self, settings_obj, settings_params):
        """Handle."""
        settings_obj.validate_zone_params()
        settings_obj.validate_input()
        settings_details = settings_obj.get_s3_zone_settings_details(
            access_zone=settings_params["access_zone"])

        S3ZoneSettingsModifyHandler().handle(
            settings_obj=settings_obj, settings_params=settings_params,
            settings_details=settings_details)


def main():
    """ Create PowerScale S3 zone settings object and perform action on it
        based on user input from playbook."""
    obj = S3ZoneSettings()
    S3ZoneSettingsHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
