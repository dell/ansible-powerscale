#!/usr/bin/python
# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing S3 keys on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: s3_key
version_added: '3.1.0'
short_description: Manage S3 keys on a PowerScale Storage System
description:
- Managing S3 keys on a PowerScale system includes generating,
  retrieving, and deleting S3 access keys for users.
- Supports force regeneration of existing keys with optional expiry time.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Dell Technologies Ansible Team <ansible.team@dell.com>

options:
  user_name:
    description:
    - The name of the user for whom the S3 key is managed.
    type: str
    required: true
  access_zone:
    description:
    - The access zone in which the user exists.
    type: str
    default: 'System'
  state:
    description:
    - The desired state of the S3 key.
    - C(present) generates a new key or retrieves existing key details.
    - C(absent) deletes the S3 key for the user.
    type: str
    choices: ['present', 'absent']
    default: 'present'
  force:
    description:
    - Whether to force regenerate the S3 key if one already exists.
    type: bool
    default: false
  existing_key_expiry_time:
    description:
    - The expiry time in minutes for the existing key when regenerating.
    - Valid range is 0 to 1440 minutes.
    type: int
notes:
- The I(check_mode) is supported.
'''

EXAMPLES = r'''
- name: Generate S3 key for a user
  dellemc.powerscale.s3_key:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"  # example
    verify_ssl: "{{ verify_ssl }}"
    user_name: "s3user1"
    state: "present"

- name: Force regenerate S3 key
  dellemc.powerscale.s3_key:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"  # example
    verify_ssl: "{{ verify_ssl }}"
    user_name: "s3user1"
    state: "present"
    force: true
    existing_key_expiry_time: 60

- name: Delete S3 key
  dellemc.powerscale.s3_key:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"  # example
    verify_ssl: "{{ verify_ssl }}"
    user_name: "s3user1"
    state: "absent"
'''

RETURN = r'''
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
s3_key_details:
    description: The S3 key details.
    type: complex
    returned: always
    contains:
        keys:
            description: List of S3 keys for the user.
            type: list
            contains:
                access_id:
                    description: The access key ID.
                    type: str
                secret_key:
                    description: The secret key. Only returned when a key is newly generated.
                    type: str
    sample: {
        "keys": [
            {
                "access_id": "ABCDEF1234567890",
                "secret_key": "secret_value"
            }
        ]
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('s3_key')


class S3Key:
    """Class with S3 key operations"""

    def __init__(self):
        """Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(self.get_s3_key_parameters())
        # Initialize the ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=True
        )
        # Result is a dictionary that contains changed status and S3 key details
        self.result = {
            "changed": False,
            "s3_key_details": {}
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
        if hasattr(self.protocol_api, 'reset_mock'):
            self.protocol_api.reset_mock()

    def get_s3_key_parameters(self):
        """Get s3 key parameters."""
        return dict(
            user_name=dict(type='str', required=False),
            access_zone=dict(type='str', default='System'),
            state=dict(type='str', choices=['present', 'absent'],
                       default='present'),
            force=dict(type='bool', default=False),
            existing_key_expiry_time=dict(type='int', required=False)
        )

    def validate_input(self, params):
        """Validate the input parameters."""
        user_name = params.get('user_name')
        if user_name is None:
            self.module.fail_json(msg="user_name is required")
        if user_name is not None and len(str(user_name).strip()) == 0:
            self.module.fail_json(msg="Invalid user_name provided")
        expiry = params.get('existing_key_expiry_time')
        if expiry is not None:
            if expiry < 0 or expiry > 1440:
                self.module.fail_json(
                    msg="existing_key_expiry_time is not in the valid range")

    def get_s3_key_details(self, user_name, access_zone):
        """Get S3 key details for a user."""
        msg = f"Getting S3 key details for user {user_name}"
        LOG.info(msg)
        try:
            s3_key_obj = self.protocol_api.get_s3_key(
                user_name, zone=access_zone)
            if s3_key_obj:
                raw = s3_key_obj.to_dict()
                # Unwrap nested response (API returns {"keys": {...}})
                if isinstance(raw, dict) and 'keys' in raw:
                    inner = raw['keys']
                    if isinstance(inner, list) and inner:
                        key_details = inner[0]
                    elif isinstance(inner, dict):
                        key_details = inner
                    else:
                        key_details = raw
                else:
                    key_details = raw
                msg = f"S3 key details are: {key_details}"
                LOG.info(msg)
                return key_details
            return None
        except utils.ApiException as e:
            if hasattr(e, 'status') and e.status == 404:
                LOG.info(f"S3 key not found for user {user_name}")
                return None
            error_msg = f"Got error {utils.determine_error(e)} while " \
                        f"getting S3 key details"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)
        except Exception as e:
            error_msg = f"Got error {utils.determine_error(e)} while " \
                        f"getting S3 key details"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def create_s3_key(self, user_name, access_zone,
                      existing_key_expiry_time=None):
        """Generate a new S3 key for a user."""
        msg = f"Generating S3 key for user {user_name}"
        LOG.info(msg)
        try:
            kwargs = {"zone": access_zone}
            s3_key_body = self.isi_sdk.S3Key()
            if existing_key_expiry_time is not None:
                s3_key_body.existing_key_expiry_time = existing_key_expiry_time
            resp = self.protocol_api.create_s3_key(
                s3_key=s3_key_body, s3_key_id=user_name, **kwargs)
            if resp:
                raw = resp.to_dict()
                # Unwrap nested response (API returns {"keys": {...}})
                if isinstance(raw, dict) and 'keys' in raw:
                    inner = raw['keys']
                    if isinstance(inner, list) and inner:
                        key_details = inner[0]
                    elif isinstance(inner, dict):
                        key_details = inner
                    else:
                        key_details = raw
                else:
                    key_details = raw
                LOG.info("Successfully generated S3 key.")
                return key_details
        except Exception as e:
            error_msg = f"Failed to generate S3 key with error: " \
                        f"{utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def delete_s3_key(self, user_name, access_zone):
        """Delete the S3 key for a user."""
        msg = f"Deleting S3 key for user {user_name}"
        LOG.info(msg)
        try:
            self.protocol_api.delete_s3_key(user_name, zone=access_zone)
            LOG.info("Successfully deleted S3 key.")
            return True
        except Exception as e:
            error_msg = f"Failed to delete S3 key with error: " \
                        f"{utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)


class S3KeyExitHandler:
    """S3KeyExitHandler definition."""
    def handle(self, s3_key_obj, s3_key_details):
        """Handle."""
        s3_key_obj.result["s3_key_details"] = \
            s3_key_details if s3_key_details else {}
        s3_key_obj.module.exit_json(**s3_key_obj.result)


class S3KeyDeleteHandler:
    """S3KeyDeleteHandler definition."""
    def handle(self, s3_key_obj, params, s3_key_details):
        """Handle."""
        if params.get('state') == 'absent' and s3_key_details:
            s3_key_obj.result['changed'] = True
            if not s3_key_obj.module.check_mode:
                s3_key_obj.delete_s3_key(
                    params['user_name'],
                    params.get('access_zone', 'System'))
            s3_key_details = {}
        S3KeyExitHandler().handle(s3_key_obj, s3_key_details)


class S3KeyCreateHandler:
    """S3KeyCreateHandler definition."""
    def handle(self, s3_key_obj, params, s3_key_details):
        """Handle."""
        if params.get('state') == 'present':
            force = params.get('force', False)
            if s3_key_details is None or force:
                s3_key_obj.result['changed'] = True
                if not s3_key_obj.module.check_mode:
                    s3_key_details = s3_key_obj.create_s3_key(
                        params['user_name'],
                        params.get('access_zone', 'System'),
                        params.get('existing_key_expiry_time'))
            else:
                # Strip secret_key from existing key details (security)
                if isinstance(s3_key_details, dict) and \
                        'keys' in s3_key_details:
                    for key in s3_key_details.get('keys', []):
                        key.pop('secret_key', None)
        S3KeyDeleteHandler().handle(s3_key_obj, params, s3_key_details)


class S3KeyHandler:
    """S3KeyHandler definition."""
    def handle(self, s3_key_obj, params):
        """Handle."""
        s3_key_obj.validate_input(params)
        s3_key_details = s3_key_obj.get_s3_key_details(
            params['user_name'],
            params.get('access_zone', 'System'))
        S3KeyCreateHandler().handle(
            s3_key_obj=s3_key_obj, params=params,
            s3_key_details=s3_key_details)


def main():
    """Perform action on PowerScale S3 keys based on user input
    from playbook."""
    obj = S3Key()
    S3KeyHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
