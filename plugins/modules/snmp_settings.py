#!/usr/bin/python
# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Ansible module for managing SNMP settings on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: snmp_settings
version_added: '2.4.0'

short_description: Manage SNMP settings on PowerScale storage systems

description:
- Manage SNMP settings on PowerScale storage systems includes
  retrieving, and updating SNMP settings.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Bhavneet Sharma(@Bhavneet-Sharma) <ansible.team@dell.com>

options:
  read_only_community:
    description:
    - SNMP read-only community name.
    - The system default value of the read-only community name is
      C(I$ilonpublic).
    - Update the read-only community name while enabling SNMP v2c.
    type: str
  service:
    description:
    - Whether the SNMP service is enabled.
    type: bool
  snmp_v2c_access:
    description:
    - Whether the SNMP v2c is enabled.
    - OneFS support SNMP v2c and later.
    type: bool
  snmp_v3:
    description:
    - Specify the access, privacy, and security level for SNMP v3.
    type: dict
    suboptions:
      access:
        description:
        - Whether SNMP v3 is enabled.
        type: bool
      auth_protocol:
        description:
        - SNMP v3 authentication protocol.
        type: str
        choices: ['SHA', 'MD5']
      privacy_password:
        description:
        - SNMP v3 privacy password.
        type: str
      password:
        description:
        - SNMP v3 authentication password.
        type: str
      privacy_protocol:
        description:
        - SNMP v3 privacy protocol.
        type: str
        choices: ['AES', 'DES']
      security_level:
        description:
        - SNMP v3 security level.
        type: str
        choices: ['noAuthNoPriv', 'authNoPriv', 'authPriv']
      read_only_user:
        description:
        - The read-only user for SNMP v3 requests.
        - The system default value of read-only user is C(general).
        type: str
  system_contact:
    description:
    - SNMP system owner contact information.
    - This must be a valid email address.
    - The contact information is set for the reporting purpose.
    type: str
  system_location:
    description:
    - The cluster description for SNMP system.
    - The cluster description is set for the reporting purpose.
    type: str
notes:
- The I(check_mode) is supported.
- Users can configure SNMP version 3 alone or in combination with version 2c.
- Idempotency is not supported for SNMP v3's password and privacy password.
'''

EXAMPLES = r'''
- name: Get SNMP settings
  dellemc.powerscale.snmp_settings:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"

- name: Update SNMP settings
  dellemc.powerscale.snmp_settings:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    read_only_community: "community-name"
    snmp_v3:
      access: true
      auth_protocol: "SHA"
      privacy_password: "password"
      password: "auth_password"
      privacy_protocol: "AES"
      security_level: "noAuthNoPriv"
      read_only_user: "user"
    system_contact: "contact@domain.com"
    system_location: "Enabled SNMP"
'''

RETURN = r'''
changed:
    description: A Boolean value indicating if task had to make changes.
    returned: always
    type: bool
    sample: "true"
snmp_settings:
    description: The details of SNMP settings.
    returned: always
    type: dict
    contains:
        read_only_community:
            description: SNMP read-only community name.
            type: str
        service:
            description: Whether the SNMP service is enabled.
            type: bool
        snmp_v1_v2c_access:
            description: Whether the SNMP v2c access is enabled.
            type: bool
        snmp_v3_access:
            description: Whether the SNMP v3 is enabled.
            type: bool
        snmp_v3_auth_protocol:
            description: SNMP v3 authentication protocol.
            type: str
        snmp_v3_priv_protocol:
            description: SNMP v3 privacy protocol.
            type: str
        smnmp_v3_read_only_user:
            description: SNMP v3 read-only user.
            type: str
        snmp_v3_security_level:
            description: SNMP v3 security level.
            type: str
        system_contact:
            description: SNMP system owner contact information.
            type: str
        system_location:
            description: The cluster description for SNMP system.
            type: str
    sample: {
        "read_only_community": "community-name",
        "service": true,
        "snmp_v1_v2c_access": true,
        "snmp_v3_access": true,
        "snmp_v3_auth_protocol": "SHA",
        "snmp_v3_priv_protocol": "AES",
        "snmp_v3_read_only_user": "user",
        "snmp_v3_security_level": "noAuthNoPriv",
        "system_contact": "contact@domain.com",
        "system_location": "Enabled SNMP"
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.powerscale_base \
    import PowerScaleBase
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.protocol \
    import Protocol
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('snmp_settings')


class SNMPSettings(PowerScaleBase):

    """SNMP Settings operations."""

    def __init__(self):
        """Define all parameters for this module."""

        ansible_module_params = {
            'argument_spec': self.get_snmp_settings_parameters(),
            'supports_check_mode': True
        }

        super().__init__(AnsibleModule, ansible_module_params)

        self.result = {
            "changed": False,
            "snmp_settings_details": {}
        }

    def get_snmp_settings(self):
        """
        Get SNMP settings.
        returns: Details of SNMP settings
        rtype: dict
        """
        return Protocol(self.protocol_api, self.module).get_snmp_settings()

    def get_snmp_settings_parameters(self):
        """
        Returns a dictionary containing the SNMP settings parameters.
        :rtype: dict
        """
        return dict(
            read_only_community=dict(type='str'), service=dict(type='bool'),
            snmp_v2c_access=dict(type='bool'), snmp_v3=dict(
                type='dict', options=dict(
                    access=dict(type='bool'),
                    auth_protocol=dict(type='str', choices=['SHA', 'MD5']),
                    privacy_password=dict(type='str', no_log=True),
                    password=dict(type='str', no_log=True),
                    privacy_protocol=dict(type='str', choices=['AES', 'DES']),
                    security_level=dict(type='str', choices=[
                        'noAuthNoPriv', 'authNoPriv', 'authPriv']),
                    read_only_user=dict(type='str')
                )
            ), system_contact=dict(type='str'),
            system_location=dict(type='str'))

    def is_snmp_v3_required(self, v3_params, snmp_details):
        """
        Check if SNMP settings need to be updated.
        :param v3_params: SNMP v3 parameters
        :type v3_params: dict
        :param snmp_details: SNMP details
        :type snmp_details: dict
        :rtype: dict
        """
        modify_dict = {}
        v3_pbs_keys = ['access', 'auth_protocol', 'read_only_user',
                       'security_level']

        for key in v3_pbs_keys:
            if v3_params.get(key) is not None and v3_params.get(key) != snmp_details.get(f'snmp_v3_{key}'):
                modify_dict[f'snmp_v3_{key}'] = v3_params.get(key)
        if v3_params.get('password') is not None and v3_params.get('password'):
            modify_dict['snmp_v3_password'] = v3_params.get('password')
        if v3_params.get('privacy_password') is not None and v3_params.get('privacy_password'):
            modify_dict['snmp_v3_priv_password'] = v3_params.get(
                'privacy_password')
        if v3_params.get('privacy_protocol') is not None and v3_params.get('privacy_protocol') and \
                v3_params.get('privacy_protocol') != snmp_details.get('snmp_v3_priv_protocol'):
            modify_dict['snmp_v3_priv_protocol'] = v3_params.get(
                'privacy_protocol')

        return modify_dict

    def is_snmp_modify_required(self, snmp_params, snmp_details):
        """
        Check if SNMP settings need to be updated.
        :param snmp_params: SNMP parameters
        :type snmp_params: dict
        :param snmp_details: SNMP details
        :type snmp_details: dict
        :rtype: dict
        """
        modify_dict = {}
        settings_keys = ['read_only_community', 'service', 'system_contact',
                         'system_location']

        for key in settings_keys:
            if snmp_params.get(key) is not None and snmp_params.get(key) != snmp_details.get(key):
                modify_dict[key] = snmp_params.get(key)

        if snmp_params.get('snmp_v2c_access') is not None and snmp_params.get('snmp_v2c_access') != snmp_details.get('snmp_v1_v2c_access'):
            modify_dict['snmp_v1_v2c_access'] = snmp_params.get(
                'snmp_v2c_access')

        if snmp_params.get('snmp_v3') is not None:
            v3_params = snmp_params.get('snmp_v3')
            modify_dict.update(self.is_snmp_v3_required(v3_params, snmp_details))

        return modify_dict

    def update_snmp_settings(self, modify_dict):
        """Update SNMP settings.
        :param kwargs: Params to update.
        :type kwargs: dict
        :rtype: bool
        """
        try:
            LOG.info("Modifying SNMP settings")
            snmp_settings = self.isi_sdk.SnmpSettingsExtended(**modify_dict)
            if not self.module.check_mode:
                self.protocol_api.update_snmp_settings(snmp_settings)
                LOG.info("Successfully modified the SNMP settings.")
            return True
        except Exception as e:
            error_msg = f"Modifying SNMP settings failed with " \
                        f"error: {utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def validate_snmp_params(self, module_params):
        """Validate SNMP parameters.
        :param module_params: SNMP parameters.
        :type module_params: dict
        :rtype: bool
        """
        params = ['read_only_community', 'system_contact']
        for param in params:
            if utils.is_param_empty_spaces(module_params.get(param)):
                err_msg = f"Provide valid {param} parameter."
                self.module.fail_json(msg=err_msg)
        if module_params.get('system_location') and \
                utils.is_input_empty(module_params.get('system_location')):
            err_msg = "Provide valid system_location parameter."
            self.module.fail_json(msg=err_msg)


class SNMPSettingsExitHandler:
    def handle(self, settings_obj):
        settings_obj.result['snmp_settings_details'] = settings_obj.get_snmp_settings()
        settings_obj.module.exit_json(**settings_obj.result)


class SNMPSettingsUpdateHandler:
    def handle(self, settings_obj, module_params, snmp_details):
        settings_obj.validate_snmp_params(module_params)
        modify_dict = settings_obj.is_snmp_modify_required(
            snmp_params=module_params, snmp_details=snmp_details)

        if modify_dict:
            changed = settings_obj.update_snmp_settings(modify_dict)
            settings_obj.result['changed'] = changed
        SNMPSettingsExitHandler().handle(settings_obj)


class SNMPSettingsHandler:
    def handle(self, settings_obj, module_params):
        snmp_details = settings_obj.get_snmp_settings()
        SNMPSettingsUpdateHandler().handle(
            settings_obj=settings_obj, module_params=module_params,
            snmp_details=snmp_details)


def main():
    """ Create the PowerScale SNMP settings object and perform
    action on it based on the user input from playbook.
    """
    obj = SNMPSettings()
    SNMPSettingsHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
