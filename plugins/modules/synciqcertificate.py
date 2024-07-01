#!/usr/bin/python
# Copyright: (c) 2023, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing SyncIQ target cluster certificates"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: synciqcertificate
version_added: '2.3.0'
short_description:  Manage SyncIQ target cluster certificate on a PowerScale Storage System
description:
- Managing SyncIQ target cluster certificate on an PowerScale system includes getting, importing, modifying and
  deleting target cluster certificates.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Meenakshi Dembi(@dembim) <ansible.team@dell.com>

options:
  certificate_file:
    description:
    - Certificate file path.
    type: str
  alias_name:
    description:
    - Alias name for the certificate.
    type: str
  description:
    description:
    - Description of the certificate.
    - Map users to a specific user and/or group ID after a failed auth attempt.
    type: str
  certificate_id:
    description:
    - ID assigned by the system to certificate.
    - This parameter does not affect server behavior, but is included to accommodate legacy client requirements.
    type: str
  new_alias_name:
    description:
    - Alias name for the certificate in case of modify operation.
    type: str
  state:
    description:
    - The state option is used to mention the existence of SyncIQ certificate.
    type: str
    choices: [absent, present]
    default: present

notes:
- The I(check_mode) is supported.
'''

EXAMPLES = r'''
- name: Import SyncIQ certificate
  dellemc.powerscale.synciqcertificate:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    certificate_file: "/ifs/server.crt"
    description: "From python"
    alias_name: "Test_1"
    state: 'present'

- name: Get SyncIQ certificate details
  dellemc.powerscale.synciqcertificate:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    certificate_id: "a851d9f3d7b16985be6fcb0402"
    state: "present"

- name: Modify SyncIQ certificate details
  dellemc.powerscale.synciqcertificate:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    certificate_id: "a851d9f3d7b16985be6fcb0402"
    description: "test description"
    alias_name: "Modify_alias_name"
    state: "present"

- name: Delete SyncIQ certificate details
  dellemc.powerscale.synciqcertificate:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    certificate_id: "a851d9f3d7b16985be6fcb0402"
    state: "absent"
'''

RETURN = r'''
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
synciq_certificate_details:
    description: The synciq certificate details.
    type: dict
    returned: always
    contains:
        description:
            description: Description of the certificate.
            type: str
        fingerprints:
            description: Fingerprint details of the certificate.
            type: list
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
            description: Specifies the preferred size for directory read operations. This value is
                used to advise the client of optimal settings for the server, but is not
                enforced.
            type: str
        not_before:
            description: Validity date of the certificate.
            type: str
        status:
            description: Specifies the validity of the certificate.
            type: str
        subject:
            description: Validity date of the certificate.
            type: str

    sample: {
                "description": "SyncIQ Certificate details",
                "fingerprints": [
                    {
                        "type": "SHA1",
                        "value": "xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:5e:xx:xx:xx:xx:xx:xx:xx:xx"
                    },
                    {
                        "type": "SHA256",
                        "value": "xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:5e:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:"
                    }],
                "id": "479891a2b14eb6204b1b9975573fda0fea92cfa851d9f3d7b16985be6fcb0402",
                "issuer": "C=AU, ST=Some-State, O=Internet Widgits Pty Ltd",
                "name": "Test_1_modify",
                "not_after": 1753465054,
                "not_before": 1690393054,
                "status": "valid",
                "subject": "C=AU, ST=Some-State, O=Internet Widgits Pty Ltd"
            }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.powerscale_base \
    import PowerScaleBase
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('synciqcertificate')


class SyncIQCertificate(PowerScaleBase):

    '''Class with SyncIQ target Cluster operations'''

    def __init__(self):
        ''' Define all parameters required by this module'''

        mutually_exclusive = [['certificate_id', 'alias_name']]

        required_one_of = [['certificate_id', 'alias_name']]

        ansible_module_params = {
            'argument_spec': self.get_synciqcertificate_parameters(),
            'supports_check_mode': True,
            'mutually_exclusive': mutually_exclusive,
            'required_one_of': required_one_of
        }

        super().__init__(AnsibleModule, ansible_module_params)

        self.result = {
            "changed": False,
            "synciq_certificate_details": {}
        }

    def get_certificate(self, certificate_id):
        """
        Get details of an SyncIQ Certificates.
        :param certificate_id: system assigned certificate id
        :type certificate_id: str
        :return: Certificate details
        :rtype: dict
        """
        try:
            synciq_certificate_details = self.synciq_api.get_certificates_peer_by_id(certificates_peer_id=certificate_id).to_dict()
            if synciq_certificate_details:
                return synciq_certificate_details
            return None
        except Exception as e:
            error_message = f"Fetching SyncIQ certificate failed with error: {utils.determine_error(e)}"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_certificate_id(self, name, certificate_id):
        """
        Get SyncIQ target certificate id when alias name is mentioned.
        :param name: alias name of certificate
        :type name: str
        :return: certificate id
        :rtype: str
        """
        try:
            cert_id = None
            all_certificates = self.synciq_api.list_certificates_peer().to_dict()
            for items in range(len(all_certificates['certificates'])):
                if name is not None:
                    if all_certificates['certificates'][items]['name'] == name:
                        cert_id = all_certificates['certificates'][items]['id']
                        break
                if certificate_id is not None and \
                        certificate_id == all_certificates['certificates'][items]['id']:
                    cert_id = certificate_id
                    break

            return cert_id

        except Exception as e:
            error_message = f"Getting SyncIQ target certificate failed with error: {utils.determine_error(e)}"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def import_synciq_certificate(self, payload):
        """
        Import SyncIQ certificate.
        :param payload: import certificate params
        :type payload: dict
        :return: certificate details
        :rtype: str
        """
        try:
            certificate_details = dict()
            if not self.module.check_mode:
                certificate_details = self.synciq_api.create_certificates_peer_item(payload).to_dict()
                if certificate_details:
                    certificate_details = self.get_certificate(certificate_details['id'])
            return certificate_details
        except Exception as e:
            error_message = f"Importing SyncIQ target certificate failed with error: {utils.determine_error(e)}"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete_synciq_certificate(self, certificate_id):
        """
        Delete SyncIQ certificate.
        :param certificate_id: system assigned certificate id
        :type certificate_id: str
        :return: None
        :rtype: None
        """
        try:
            if not self.module.check_mode:
                if certificate_id is not None:
                    self.synciq_api.delete_certificates_peer_by_id(certificate_id)
                else:
                    return False
            return True
        except Exception as e:
            error_message = f"Deleting SyncIQ target certificate failed with error: {utils.determine_error(e)}"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def modify_synciq_certificate_details(self, modify_dict, certificate_id):
        """
        Modify SyncIQ certificate.
        :param modify_dict: modifiable parameters
        :type payload: dict
        :param certificate_id: system assigned certificate id
        :type certificate_id: str
        :return: updated certificate details
        :rtype: dict
        """
        try:
            if not self.module.check_mode:
                self.synciq_api.update_certificates_peer_by_id(modify_dict, certificate_id)
            return self.get_certificate(certificate_id)
        except Exception as e:
            error_message = f"Updating SyncIQ target certificate details failed with error: {utils.determine_error(e)}"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_synciqcertificate_parameters(self):
        return dict(
            state=dict(type='str', choices=['present', 'absent'], default='present'),
            description=dict(type='str'),
            certificate_file=dict(type='str'),
            certificate_id=dict(type='str'),
            alias_name=dict(type='str'),
            new_alias_name=dict(type='str')
        )

    def form_synciq_import_certificate_payload(self, input_params):
        synciq_cert_params = dict()
        if ((not input_params['certificate_file']) or (not input_params['alias_name'])):
            self.module.fail_json(msg="certificate_file and alias_name are required for Import certificate operation.")
        synciq_cert_params['certificate_path'] = input_params['certificate_file']
        synciq_cert_params['name'] = input_params['alias_name']
        if input_params['description']:
            synciq_cert_params['description'] = input_params['description']
        return synciq_cert_params

    def form_modify_dict(self, certificate_details, synciq_certificate_params):
        modify_dict = dict()
        if synciq_certificate_params['description'] and synciq_certificate_params['description'] != certificate_details['certificates'][0]['description']:
            modify_dict['description'] = synciq_certificate_params['description']
        if synciq_certificate_params['new_alias_name'] and synciq_certificate_params['new_alias_name'] != certificate_details['certificates'][0]['name']:
            modify_dict['name'] = synciq_certificate_params['new_alias_name']
        return modify_dict

    def validate_certificate_params(self, synciq_certificate_params):
        param_list = ['alias_name', 'new_alias_name']
        for items in param_list:
            error_msg = utils.is_invalid_name(synciq_certificate_params[items], items)
            if error_msg:
                self.module.fail_json(msg=error_msg)

        if synciq_certificate_params['description'] and len(synciq_certificate_params['description']) > 128:
            self.module.fail_json(msg="The maximum length for description is 128")

        if synciq_certificate_params['certificate_file'] and not synciq_certificate_params['certificate_file'].endswith(".crt"):
            self.module.fail_json(msg="File format is not supported")

    def get_cert_details(self, synciq_certificate_params):
        certificate_details = dict()
        certificate_id = None
        certificate_id = self.get_certificate_id(synciq_certificate_params['alias_name'], synciq_certificate_params['certificate_id'])
        if certificate_id is not None:
            certificate_details = self.get_certificate(certificate_id)
        return certificate_id, certificate_details


class SyncIQCertificateExitHandler():
    def handle(self, sync_iq_certificate_obj, synciq_certificate_details):
        sync_iq_certificate_obj.result["synciq_certificate_details"] = synciq_certificate_details
        sync_iq_certificate_obj.module.exit_json(**sync_iq_certificate_obj.result)


class SyncIQCertificateDeleteHandler():
    def handle(self, sync_iq_certificate_obj, synciq_certificate_params, synciq_certificate_details, certificate_id):
        if synciq_certificate_params['state'] == 'absent':
            changed = sync_iq_certificate_obj.delete_synciq_certificate(certificate_id)
            sync_iq_certificate_obj.result['changed'] = changed
            synciq_certificate_details = {}

        SyncIQCertificateExitHandler().handle(sync_iq_certificate_obj, synciq_certificate_details)


class SyncIQCertificateModifyHandler():
    def handle(self, sync_iq_certificate_obj, synciq_certificate_params, synciq_certificate_details, certificate_id):
        if synciq_certificate_params['state'] == 'present' and synciq_certificate_details:
            modify_dict = sync_iq_certificate_obj.form_modify_dict(synciq_certificate_details, synciq_certificate_params)
            if modify_dict:
                synciq_certificate_details = sync_iq_certificate_obj.modify_synciq_certificate_details(modify_dict, certificate_id)
                sync_iq_certificate_obj.result['changed'] = True

        SyncIQCertificateDeleteHandler().handle(sync_iq_certificate_obj, synciq_certificate_params, synciq_certificate_details, certificate_id)


class SyncIQCertificateCreateHandler():
    def handle(self, sync_iq_certificate_obj, synciq_certificate_params, synciq_certificate_details, certificate_id):
        if synciq_certificate_params['state'] == 'present' and not synciq_certificate_details:
            import_certificate_payload = sync_iq_certificate_obj.form_synciq_import_certificate_payload(synciq_certificate_params)
            synciq_certificate_details = sync_iq_certificate_obj.import_synciq_certificate(import_certificate_payload)
            sync_iq_certificate_obj.result['changed'] = True

        SyncIQCertificateModifyHandler().handle(sync_iq_certificate_obj, synciq_certificate_params, synciq_certificate_details, certificate_id)


class SyncIQCertificateHandler():
    def handle(self, sync_iq_certificate_obj, synciq_certificate_params):
        sync_iq_certificate_obj.validate_certificate_params(synciq_certificate_params)
        certificate_id, synciq_certificate_details = sync_iq_certificate_obj.get_cert_details(synciq_certificate_params)
        SyncIQCertificateCreateHandler().handle(sync_iq_certificate_obj, synciq_certificate_params, synciq_certificate_details, certificate_id)


def main():
    """ Create PowerScale SyncIQCertificate object and perform action on it
        based on user input from playbook."""
    obj = SyncIQCertificate()
    SyncIQCertificateHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
