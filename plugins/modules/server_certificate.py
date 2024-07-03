#!/usr/bin/python
# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing Server certificates"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: server_certificate
version_added: '2.5.0'
short_description:  Manage server certificates on a PowerScale Storage System
description:
  - Manage server certificates on a PowerScale Storage System includes import, update, set certificate to default,
    and delete server certificates.
extends_documentation_fragment:
  - dellemc.powerscale.powerscale
author:
  - Felix Stephen (@felixs88) <ansible.team@dell.com>
options:
  state:
    description:
      - The state option is used to mention the existence of server certificate.
    type: str
    choices: [absent, present]
    default: present
  alias_name:
    description:
      - The name of the certificate.
      - I(alias_name) is mutually exclusive with I(certificate_id).
      - The maximum length for I(alias_name) is 128.
    type: str
  description:
    description:
      - The description of the certificate.
      - The maximum length for I(description) is 2048.
      - Setting an empty value is necessary to remove the certificate description.
    type: str
  new_alias_name:
    description:
      - The I(alias_name) of the certificate.
      - The maximum length for I(new_alias_name) is 128.
    type: str
  certificate_id:
    description:
      - The ID of the imported certificate.
      - I(certificate_id) is mutually exclusive with I(alias_name).
    type: str
  certificate_path:
    description:
      - The path of the certificate file.
    type: path
  certificate_key_path:
    description:
      - The path of the certificate key file.
    type: path
  certificate_key_password:
    description:
      - The password of the certificate key.
      - The maximum length for I(certificate_key_password) is 256.
    type: str
  is_default_certificate:
    description:
      - To set the certificate as the default.
      - If the C(True) is selected, the server certificate is set to default.
      - Another certificate must be selected as default to designate a certificate as non-default.
    type: bool
    default: false
  certificate_monitor_enabled:
    description:
      - Boolean value indicating whether certificate expiration monitoring is enabled.
      - This option is applicable if I(is_default_certificate) is C(True).
    type: bool
  certificate_pre_expiration_threshold:
    description:
      - The number of seconds before certificate expiration that the certificate expiration
        monitor will start raising alerts.
      - The range for this value is from 0 to 4294967295.
      - This option is applicable if I(is_default_certificate) is C(True).
    type: int
notes:
  - The I(check_mode) is supported.
  - The I(check_mode) and idempotency is not supported for I(certificate_path), I(certificate_key_path),
    and I(certificate_key_password) when updating certificates.
'''

EXAMPLES = r'''
- name: To import the new server certificate
  dellemc.powerscale.server_certificate:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    state: present
    alias_name: certificate_name
    description: The certificate description
    certificate_path: "/ifs/certificates/server.crt"
    certificate_key_path: "/ifs/certificates/server.key"
    certificate_key_password: "Secret@123"

- name: To import the new server certificate and set the certificate as default
  dellemc.powerscale.server_certificate:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    state: present
    alias_name: default_certificate
    description: The default certificate description
    certificate_path: "/ifs/certificates/server.crt"
    certificate_key_path: "/ifs/certificates/server.key"
    certificate_key_password: "Secret@123"
    is_default_certificate: true
    certificate_monitor_enabled: true
    certificate_pre_expiration_threshold: 300

- name: To update the server certificate
  dellemc.powerscale.server_certificate:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    state: present
    alias_name: certificate_new_name
    description: The updated certificate description

- name: To update the server certificate and set the certificate as default
  dellemc.powerscale.server_certificate:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    state: present
    certificate_id: "a851d9f3d7b16985be6fcb0402"
    description: The updated certificate description
    is_default_certificate: true
    certificate_monitor_enabled: true
    certificate_pre_expiration_threshold: 42949

- name: To delete the server certificate
  dellemc.powerscale.server_certificate:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    state: absent
    alias_name: certificate_new_name

- name: To delete the server certificate using certificate ID
  dellemc.powerscale.server_certificate:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    state: absent
    certificate_id: "a851d9f3d7b16985be6fcb0402"
'''

RETURN = r'''
changed:
  description: A boolean indicating if the task had to make changes.
  returned: always
  type: bool
  sample: "false"
certificate_details:
  description: The server certificate details.
  type: dict
  returned: always
  contains:
    description:
      description: Description of the certificate.
      type: str
    id:
      description: System assigned certificate id.
      type: str
    issuer:
      description: Name of the certificate issuer.
      type: str
    name:
      description: Name for the certificate.
      type: str
    not_after:
      description: The date and time from which the certificate becomes valid and
        can be used for authentication and encryption.
      type: str
    not_before:
      description: The date and time until which the certificate is valid and
        can be used for authentication and encryption.
      type: str
    status:
      description: Status of the certificate.
      type: str
    fingerprints:
      description: Fingerprint details of the certificate.
      type: str
    dnsnames:
      description: Subject alternative names of the certificate.
      type: list
    subject:
      description: Subject of the certificate.
      type: str
    certificate_monitor_enabled:
      description: Boolean value indicating whether certificate expiration monitoring is enabled.
      type: bool
    certificate_pre_expiration_threshold:
      description: The number of seconds before certificate expiration that the certificate expiration
        monitor will start raising alerts.
      type: int
  sample:
    {
      "certificate_monitor_enabled": true,
      "certificate_pre_expiration_threshold": 4294,
      "description": "This the example test description",
      "dnsnames": ["powerscale"],
      "fingerprints": [
        {
          "type": "SHA1",
          "value": "68:b2:d5:5d:cc:b0:70:f1:f0:39:3a:bb:e0:44:49:70:6e:05:c3:ed"
        },
        {
          "type": "SHA256",
          "value": "69:99:b9:c0:29:49:c9:62:e8:4b:60:05:60:a8:fa:f0:01:ab:24:43:8a:47:4c:2f:66:2c:95:a1:7c:d8:10:34"
        }],
      "id": "6999b9c02949c962e84b600560a8faf001ab24438a474c2f662c95a17cd81034",
      "issuer": "C=IN, ST=Karnataka, L=Bangalore, O=Dell, OU=ISG, CN=powerscale, emailAddress=contact@dell.com",
      "name": "test",
      "not_after": 1769586969,
      "not_before": 1706514969,
      "status": "valid",
      "subject": "C=IN, ST=Karnataka, L=Bangalore, O=Dell, OU=ISG, CN=powerscale, emailAddress=contact@dell.com"
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.powerscale_base \
    import PowerScaleBase
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('server_certificate')


class ServerCertificate(PowerScaleBase):

    def __init__(self):
        """
        Initializes the class instance.

        :param self: The class instance.
        """
        mutually_exclusive = [['certificate_id', 'alias_name']]
        required_one_of = [['certificate_id', 'alias_name']]

        ansible_module_params = {
            'argument_spec': self.get_certificate_parameters(),
            'mutually_exclusive': mutually_exclusive,
            'required_one_of': required_one_of,
            'supports_check_mode': True,
        }
        super().__init__(AnsibleModule, ansible_module_params)

        self.result.update({
            "certificate_details": {}
        })

    def get_certificate_parameters(self):
        """
        Returns a dictionary containing the parameters for a certificate.

        :return: A dictionary containing the parameters for a certificate.
        :rtype: dict
        """
        return dict(
            state=dict(type='str', choices=['present', 'absent'], default='present'),
            alias_name=dict(type='str'),
            new_alias_name=dict(type='str'),
            certificate_id=dict(type='str'),
            certificate_path=dict(type='path'),
            certificate_key_path=dict(type='path'),
            certificate_key_password=dict(type='str', no_log=True),
            description=dict(type='str'),
            is_default_certificate=dict(type='bool', default=False),
            certificate_monitor_enabled=dict(type='bool'),
            certificate_pre_expiration_threshold=dict(type='int'),
        )

    def validate_params(self, module_params):
        """
        Validates the parameters passed to the function.

        Args:
            module_params (dict): A dictionary containing the module parameters.
        """

        alias_name = module_params.get('alias_name')
        new_alias_name = module_params.get('new_alias_name')
        description = module_params.get('description')
        certificate_key_password = module_params.get('certificate_key_password')
        threshold = module_params.get('certificate_pre_expiration_threshold')

        if (alias_name is not None and len(alias_name) > 128) or (new_alias_name is not None and len(new_alias_name) > 128):
            self.module.fail_json(msg='The maximum length for alias_name|new_alias_name is 128.')
        if description is not None and len(description) > 2048:
            self.module.fail_json(msg='The maximum length for description is 2048.')
        if certificate_key_password is not None and len(certificate_key_password) > 256:
            self.module.fail_json(msg='The maximum length for certificate_key_password is 256.')
        if threshold is not None and not (0 < threshold < 4294967295):
            self.module.fail_json(msg='The range of certificate_pre_expiration_threshold is 0 - 4294967295.')

    def get_certificate_details(self, module_params):
        """
        Retrieves the details of a certificate based on the provided module parameters.

        Args:
            module_params (dict): A dictionary containing the module parameters.

        Returns:
            dict: A dictionary containing the certificate details.
        """
        alias_name = module_params.get('alias_name')
        certificate_id = module_params.get('certificate_id')
        certificate = {}
        try:
            if alias_name is not None:
                certificate_list = self.certificate_api.list_certificate_server().to_dict()
                for each in certificate_list['certificates']:
                    if each['name'] == alias_name:
                        certificate = each
                        break

            if certificate_id is not None:
                certificate_list = self.certificate_api.get_certificate_server_by_id(certificate_id).to_dict()
                if certificate_list:
                    certificate = certificate_list['certificates'][0]
        except Exception as e:
            error_message = f"Failed to retrieve the server certificate: {utils.determine_error(e)}"
            LOG.error(error_message)
        return certificate

    def get_default_certificate(self):
        """
        Get the default certificate settings.

        Returns:
            dict: The default certificate settings.
        """
        default_certificate = self.certificate_api.get_certificate_settings().to_dict()
        return default_certificate['settings']

    def make_certificate_default(self, module_params, certificate_id):
        """
        Make the certificate default by updating the certificate settings.

        Parameters:
            module_params (dict): A dictionary containing the module parameters.
            certificate_id (str): The ID of the certificate to be made default.

        Returns:
            bool: True if the certificate is successfully made default, False otherwise.
        """
        certificate_monitor = module_params.get('certificate_monitor_enabled')
        certificate_pre_expiration = module_params.get('certificate_pre_expiration_threshold')
        updated_values = {}

        updated_values['default_https_certificate'] = certificate_id
        if certificate_monitor is not None:
            updated_values['certificate_monitor_enabled'] = certificate_monitor
        if certificate_pre_expiration is not None:
            updated_values['certificate_pre_expiration_threshold'] = certificate_pre_expiration
        self.certificate_api.update_certificate_settings(updated_values)
        return True

    def import_certificate(self, module_params):
        """
        Import a certificate and its associated key to the server.

        Args:
            module_params (dict): A dictionary containing the module parameters.

        Returns:
            tuple: A tuple containing a boolean indicating success or failure and a dictionary containing the certificate details.
        """

        alias_name = module_params["alias_name"]
        new_alias_name = module_params.get("new_alias_name")
        certificate_path = module_params.get('certificate_path', None)
        certificate_key_path = module_params.get('certificate_key_path', None)
        is_certificate_default = module_params.get('is_default_certificate')

        if not alias_name.strip():
            self.module.fail_json(msg="alias_name is required for importing a certificate.")

        if certificate_path is None or certificate_key_path is None:
            self.module.fail_json(msg='Required both certificate_path|certificate_key_path for importing a new server certificate.')

        if self.module.check_mode:
            return True, {}

        description = module_params.get("description")
        certificate_path = module_params.get("certificate_path")
        certificate_key_path = module_params.get("certificate_key_path")
        certificate_key_password = module_params.get("certificate_key_password")

        certificate_server_item = {"name": alias_name, "certificate_path": certificate_path,
                                   "certificate_key_path": certificate_key_path}

        if description is not None:
            certificate_server_item["description"] = description
        if certificate_key_password is not None:
            certificate_server_item["certificate_key_password"] = certificate_key_password

        certificate = {}
        try:
            certificate_id = self.certificate_api.create_certificate_server_item(certificate_server_item).to_dict()
            if not certificate_id:
                error_message = "Failed to create the server certificate."
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
            if is_certificate_default:
                self.make_certificate_default(module_params, certificate_id['id'])
            certificate = self.get_certificate_details(module_params)
            if new_alias_name is not None and new_alias_name.strip():
                changed, certificate = self.update_certificate(module_params, certificate)
        except Exception as e:
            error_message = f"Failed to create the server certificate: {utils.determine_error(e)}"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
        return True, certificate

    def get_updated_diff(self, module_params, certificate_details):
        """
        Generates the updated diff and returns the changes and updated certificate details.

        Parameters:
            module_params (dict): The module parameters.
            certificate_details (dict): The details of the certificate.

        Returns:
            tuple: A tuple containing the following:
                - diff_changes (bool): True if there are any changes in the diff, False otherwise.
                - updated_cert (dict): The updated certificate details.
                - updated_values (dict): The updated values.
        """

        new_alias_name = module_params.get('new_alias_name')
        description = module_params.get('description', '')
        is_default_certificate = module_params.get('is_default_certificate')
        certificate_monitor = module_params.get('certificate_monitor_enabled')
        certificate_pre_expiration = module_params.get('certificate_pre_expiration_threshold')

        updated_values, default_cert_value = {}, {}
        diff_changes_lst, updated_default_cert = [], False
        if new_alias_name:
            updated_values['name'] = new_alias_name
        if description:
            updated_values['description'] = description

        default_cert_valid = certificate_details['id'] == self.get_default_certificate()['default_https_certificate']
        if is_default_certificate or (certificate_details and default_cert_valid):

            default_cert_value['default_https_certificate'] = certificate_details['id']
            if certificate_monitor is not None:
                default_cert_value['certificate_monitor_enabled'] = certificate_monitor
            if certificate_pre_expiration is not None:
                default_cert_value['certificate_pre_expiration_threshold'] = certificate_pre_expiration
            default_cert = self.get_default_certificate()
            default_cert_copy = default_cert.copy()
            default_cert_copy.update(default_cert_value)
            updated_default_cert = default_cert_copy != default_cert
            diff_changes_lst.append(updated_default_cert)

        updated_cert = certificate_details.copy()
        updated_cert.update(updated_values)
        diff_changes_lst.append(updated_cert != certificate_details)
        diff_changes = any(diff_changes_lst)
        return diff_changes, updated_cert, updated_values, updated_default_cert

    def update_certificate(self, module_params, certificate_details):
        """
        Update the certificate with the given module parameters and certificate details.

        Args:
            module_params (dict): The module parameters containing the new alias name, description, and is_default_certificate.
            certificate_details (dict): The details of the certificate to be updated.

        Returns:
            tuple: A tuple containing a boolean indicating if the certificate was updated and the updated certificate details.
        """

        updated, updated_cert, updated_new_cert, updated_default_cert = \
            self.get_updated_diff(module_params, certificate_details)

        if (self.module.check_mode) or not updated:
            return updated, certificate_details

        updated_values = {}
        updated_alias_name = updated_new_cert.get('name')
        updated_description = updated_new_cert.get('description')
        if updated_alias_name:
            updated_values['name'] = updated_alias_name
        if updated_description:
            updated_values['description'] = updated_description

        try:
            if updated_values:
                self.certificate_api.update_certificate_server_by_id(updated_values, certificate_details['id'])
            if updated_default_cert:
                self.make_certificate_default(module_params, certificate_details['id'])
        except Exception as e:
            error_message = f"Failed to update the server certificate: {utils.determine_error(e)}"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
        return True, updated_cert

    def delete_certificate(self, certificate_details, module_params):
        """
        Deletes a certificate from the server.

        Args:
            certificate_details (dict): A dictionary containing the details of the certificate to be deleted.

        Returns:
            tuple: A tuple containing a boolean indicating if the certificate was successfully deleted and a dictionary with the certificate details.
        """

        if certificate_details and (certificate_details['id'] == self.get_default_certificate()['default_https_certificate']):
            self.module.fail_json(msg="The removal of the default certificate is not allowed.")

        if not self.module.check_mode and certificate_details:
            self.certificate_api.delete_certificate_server_by_id(certificate_details['id'])
            certificate = self.get_certificate_details(module_params)
            return True, certificate

        if not certificate_details:
            return False, {}
        return True, certificate_details


class ServerCertificateExitHandler:

    def handle(self, certificate_obj, certificate_details):
        """
        Handles the certificate object and certificate details.

        Args:
            certificate_obj (Certificate): The certificate object.
            certificate_details (dict): The details of the certificate.

        Returns:
            None
        """
        certificate_obj.result['certificate_details'] = certificate_details
        certificate_obj.module.exit_json(**certificate_obj.result)


class ServerCertificateCreateHandler:

    def handle(self, certificate_obj, certificate_details, module_params):
        """
        Handles the certificate object and its details.

        Args:
            certificate_obj (Certificate): The certificate object to be handled.
            certificate_details (dict): The details of the certificate.

        Returns:
            None
        """
        state = module_params['state']
        details = {}
        if state == 'present' and not certificate_details:
            changed, details = certificate_obj.import_certificate(module_params)
            certificate_obj.result['changed'] = changed
        ServerCertificateUpdateHandler().handle(certificate_obj, module_params, certificate_details, details)


class ServerCertificateUpdateHandler:

    def handle(self, certificate_obj, module_params, certificate_details, details):
        """
        Handles the certificate object by updating the certificate and setting the result.

        Args:
            certificate_obj (Certificate): The certificate object to handle.
            module_params (dict): The module parameters.
            certificate_details (dict): The certificate details.

        Returns:
            None
        """
        state = module_params['state']
        certificate_id = module_params.get('certificate_id')
        alias_name = module_params.get('alias_name')
        if state == 'present' and certificate_details and (certificate_id is not None or alias_name is not None):
            changed, details = certificate_obj.update_certificate(module_params, certificate_details)
            certificate_obj.result['changed'] = changed
        ServerCertificateDeleteHandler().handle(certificate_obj, certificate_details, module_params, details)


class ServerCertificateDeleteHandler:

    def handle(self, certificate_obj, certificate_details, module_params, details):
        """
        Deletes a certificate using the provided certificate details.

        Args:
            certificate_obj (Certificate): The certificate object to delete.
            certificate_details (dict): The details of the certificate to delete.

        Returns:
            tuple: A tuple containing a boolean indicating if the certificate was deleted successfully, and a dictionary of details about the deletion process.
        """
        state = module_params['state']
        if state == 'absent':
            changed, details = certificate_obj.delete_certificate(certificate_details, module_params)
            certificate_obj.result['changed'] = changed
        ServerCertificateExitHandler().handle(certificate_obj, details)


class ServerCertificateHandler:

    def handle(self, certificate_obj, module_params):
        """
        Handles the certificate object based on the given module parameters.

        Args:
            certificate_obj (Certificate): The certificate object to be handled.
            module_params (dict): The module parameters containing the certificate details.

        Returns:
            None
        """
        certificate_obj.validate_params(module_params)
        certificate_details = certificate_obj.get_certificate_details(module_params)
        ServerCertificateCreateHandler().handle(certificate_obj, certificate_details, module_params)


def main():
    obj = ServerCertificate()
    ServerCertificateHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
