#!/usr/bin/python
# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing S3 keys on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: s3_key
version_added: "3.10.0"
short_description: Manage S3 Keys on a PowerScale Storage System
description:
- Managing S3 Keys on an PowerScale system includes retrieving details of
  S3 keys, creating S3 keys and deleting S3 keys.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
    - Fabian Brauner (@fpfuetsch)

options:
    user:
        description:
        - Specifies the user that owns the S3 key.
        - If users belongs to another provider domain, it should be mentioned along
          with domain name as "DOMAIN_NAME\\username" or DOMAIN_NAME\username.
        required: true
        type: str
    generate_new_key:
        description:
        - Wether a new S3 keys should be generated.
        - Value C(if_not_present) indicates that a new S3 key is only generated if there is no existing key.
        - Value C(always) indicates that a new S3 key is always generated, even if there is an existing key.
        required: false
        type: str
        default: if_not_present
        choices: ['if_not_present', 'always']
    existing_key_expiry_minutes:
        description: Duration in minutes for which old key should remain valid.
        required: false
        type: int
        default: 0
    access_zone:
        description:
        - Specifies the access zone in which the S3 bucket exists.
        - Access zone once set cannot be changed.
        required: false
        type: str
        default: System
    state:
        description:
        - Defines whether the S3 key should exist or not.
        - Value C(present) indicates that the S3 key should exist in system.
        - Value C(absent) indicates that the S3 key should not exist in system.
        required: false
        type: str
        default: present
        choices: ['absent', 'present']
"""

EXAMPLES = r"""
- name: Create S3 Key - Check_mode
  dellemc.powerscale.s3_key:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    access_zone: "{{access_zone}}"
    user: "{{user}}"
    state: "present"
  check_mode: true

- name: Create S3 Key - if not present
  dellemc.powerscale.s3_key:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    access_zone: "{{access_zone}}"
    user: "{{user}}"
    state: "present"
    generate_new_key: "if_not_present"

- name: Create S3 Key - even if already present
  dellemc.powerscale.s3_key:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    access_zone: "{{access_zone}}"
    user: "{{user}}"
    state: "present"
    generate_new_key: "always"

- name: Create S3 Key - even if already present, expire old key after 30 min
  dellemc.powerscale.s3_key:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    access_zone: "{{access_zone}}"
    user: "{{user}}"
    state: "present"
    generate_new_key: "always"
    existing_key_expiry_minutes: 30

- name: Delete S3 Key
  dellemc.powerscale.s3_key:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    access_zone: "{{access_zone}}"
    user: "{{user}}"
    state: "absent"
"""

RETURN = r"""
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
S3_key_details:
    description: The updated S3 Key details.
    type: complex
    returned: always
    contains:
        access_id:
            description: S3 access id.
            type: str
        secret_key:
            description: S3 secret key.
            type: str
        secret_key_timestamp:
            description: Creation timestamp of S3 secret key.
            type: str
        old_key_expiry:
            description: Expiry timestamp of old S3 key if existing.
            type: str
        old_key_timestamp:
            description: Creation timestamp of old S3 key if existing.
            type: str
        old_secret_key:
            description: Redacted old S3 key if existing.
            type: str
    sample: {
        "access_id": "sample_user_accid",
        "old_key_expiry": 1755783140,
        "old_key_timestamp": 1755781594,
        "old_secret_key": "****************************",
        "secret_key": "1234567890asdfhjkl",
        "secret_key_timestamp": 1755782540
    }
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell import (
    utils,
)


LOG = utils.get_logger("s3_key")


class S3Key(object):
    """Class with S3 Key operations"""

    def __init__(self):
        """Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(self.get_s3_key_parameters())

        self.module = AnsibleModule(
            argument_spec=self.module_params, supports_check_mode=True
        )

        self.result = {"changed": False, "S3_key_details": {}}

        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        LOG.info("Got python SDK instance for provisioning on PowerScale ")
        check_mode_msg = f"Check mode flag is {self.module.check_mode}"
        LOG.info(check_mode_msg)

        self.protocol_api = self.isi_sdk.ProtocolsApi(self.api_client)
        self.zone_summary_api = self.isi_sdk.ZonesSummaryApi(self.api_client)

    def get_key_details(self):
        """Get details of an S3 Key"""
        user = self.module.params.get("user")
        access_zone = self.module.params.get("access_zone")
        msg = (
            f"Getting S3 Key details for user {user} and access zone:" f" {access_zone}"
        )
        LOG.info(msg)
        try:
            s3_key_obj = self.protocol_api.get_s3_key(s3_key_id=user, zone=access_zone)
            if s3_key_obj is not None:
                s3_key_details = s3_key_obj.keys.to_dict()
                return s3_key_details

        except utils.ApiException as e:
            if str(e.status) == "404":
                log_msg = (
                    f"S3 Key status for user {user} in access zone"
                    f" {access_zone} is {e.status}"
                )
                LOG.info(log_msg)
            else:
                error_msg = utils.determine_error(error_obj=e)
                error_message = (
                    f"Failed to get details of S3 Key"
                    f" for user {user} in access zone {access_zone}"
                    f" with error: {str(error_msg)}"
                )
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
        except Exception as e:
            error_msg = (
                f"Got error {utils.determine_error(e)} while getting"
                f" S3 Key details for user {user} in"
                f" access zone: {access_zone}"
            )
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def create_key(self):
        """Create S3 key"""
        user = self.module.params.get("user")
        access_zone = self.module.params.get("access_zone")
        s3_key_params = {
            "s3_key": self.isi_sdk.S3Key(
                existing_key_expiry_time=self.module.params.get(
                    "existing_key_expiry_minutes"
                )
            ),
            "s3_key_id": user,
            "force": True,
        }
        try:
            msg = f"Creating S3 Key with parameters: {s3_key_params})"
            LOG.info(msg)
            key_details = {}
            if not self.module.check_mode:
                response = self.protocol_api.create_s3_key(
                    **s3_key_params, zone=access_zone
                )
                if response:
                    key_details = response.keys.to_dict()
                msg = (
                    f"Successfully created the S3 key with params: " f"{s3_key_params}"
                )
                LOG.info(msg)
            return key_details

        except Exception as e:
            error_msg = (
                f"Create S3 Key for user {user} in access zone"
                f" {access_zone} failed with error:"
                f" {utils.determine_error(e)}"
            )
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def delete_key(self):
        """Delete the S3 key"""
        user = self.module.params.get("user")
        access_zone = self.module.params.get("access_zone")
        try:
            msg = f"Deleting S3 Key for user {user} and zone {access_zone}"
            LOG.info(msg)
            if not self.module.check_mode:
                self.protocol_api.delete_s3_key(s3_key_id=user, zone=access_zone)
                msg = f"Successfully deleted the S3 key for user {user} and zone {access_zone}"
                LOG.info(msg)
            return self.get_key_details()

        except Exception as e:
            error_msg = (
                f"Delete S3 Key for user {user} in access zone"
                f" {access_zone} failed with "
                f"error: {utils.determine_error(e)}"
            )
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_s3_key_parameters(self):
        """Get module specific parameters"""
        return {
            "user": {"type": "str", "required": True},
            "generate_new_key": {
                "type": "str",
                "choices": ["if_not_present", "always"],
                "default": "if_not_present",
            },
            "existing_key_expiry_minutes": {
                "type": "int",
                "required": False,
                "default": 0,
                "no_log": False,
            },
            "access_zone": {"type": "str", "default": "System"},
            "state": {
                "type": "str",
                "choices": ["present", "absent"],
                "default": "present",
            },
        }

    def validate_params(self):
        """Validate parameters"""
        param_list = ["user", "access_zone"]
        for param in param_list:
            if self.module.params[param] is not None and (
                self.module.params[param].count(" ") > 0
                or len(self.module.params[param].strip()) == 0
            ):
                err_msg = f"Invalid {param} provided. Provide valid {param}."
                self.module.fail_json(msg=err_msg)


class S3KeyExitHandler:
    """Handle exit"""

    def handle(self, key_object, key_details):
        """Handle exit"""
        key_object.result["S3_key_details"] = key_details
        key_object.module.exit_json(**key_object.result)


class S3KeyDeleteHandler:
    """Handle deletion of S3 Key"""

    def handle(self, key_object, key_params, key_exists, key_details):
        """Handle deletion of S3 Key"""
        if key_params["state"] == "absent":
            if key_exists:
                key_details = key_object.delete_key()
                key_object.result["changed"] = True
            else:
                msg = (
                    f"Skipping S3 key deletion for user {key_params.get('user')} in"
                    f" access zone {key_params.get('access_zone')} since key does not exist"
                )
                LOG.info(msg)
        S3KeyExitHandler().handle(key_object, key_details)


class S3KeyCreateHandler:
    """Handle creation of S3 Key"""

    def handle(self, key_object, key_params, key_exists, key_details):
        """Handle creation of S3 Key"""
        if key_params["state"] == "present":
            if not key_exists or (
                key_exists and key_params.get("generate_new_key") == "always"
            ):
                key_details = key_object.create_key()
                key_object.result["changed"] = True
            else:
                msg = (
                    f"Skipping S3 key creation for user {key_params.get('user')} in access zone"
                    f" {key_params.get('access_zone')} since key exists and param"
                    f" generate_new_key is {key_params.get('generate_new_key')}"
                )
                LOG.info(msg)
        S3KeyDeleteHandler().handle(
            key_object=key_object,
            key_params=key_params,
            key_exists=key_exists,
            key_details=key_details,
        )


class S3KeyHandler:
    """Handle S3 Key module"""

    def handle(self, key_object, key_params):
        """Handle S3 Key module"""
        key_object.validate_params()
        key_details = key_object.get_key_details()
        key_exists = (
            key_details is not None and key_details.get("access_id") is not None
        )
        S3KeyCreateHandler().handle(
            key_object=key_object,
            key_params=key_params,
            key_exists=key_exists,
            key_details=key_details,
        )


def main():
    """Create PowerScale S3 Key object and perform action on it
    based on user input from playbook."""
    obj = S3Key()
    S3KeyHandler().handle(obj, obj.module.params)


if __name__ == "__main__":
    main()
