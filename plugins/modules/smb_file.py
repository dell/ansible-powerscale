#!/usr/bin/python
# Copyright: (c) 2023, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing SMB files on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: smb_file
version_added: '1.9.0'
short_description:  Manage SMB files on a PowerScale Storage System
description:
- Managing SMB files on a PowerScale Storage System includes getting
  details of all SMB open files and closing SMB files.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Pavan Mudunuri(@Pavan-Mudunuri) <ansible.team@dell.com>

options:
  file_id:
    description:
    - Unique id of SMB open file. Mutually exclusive with I(file_path).
    type: int
  file_path:
    description:
    - Path of SMB file. Mutually exclusive with I(file_id).
    - If file path is provided all the open file sessions in the path will be closed.
    type: str
  state:
    description:
    - Defines the state of SMB file.
    - C(present) indicates that the SMB file should exist in system.
    - C(absent) indicates that the SMB file is closed in system.
    default: "present"
    type: str
    choices: [absent, present]

notes:
- The I(check_mode) is supported.
- If I(state) is C(absent), the file will be closed.

'''

EXAMPLES = r'''
- name: Get list of SMB files of the PowerScale cluster
  dellemc.powerscale.smb_file:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    state: "present"

- name: Close SMB file of the PowerScale cluster
  dellemc.powerscale.smb_file:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    file_id: xxx
    state: "absent"

- name: Close smb file of the PowerScale cluster
  dellemc.powerscale.smb_file:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    file_path: "/ifs/ATest"
    state: "absent"
'''

RETURN = r'''
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
smb_file_details:
    description: The SMB file details.
    type: dict
    returned: always
    contains:
        file:
            description: Path of file within /ifs.
            type: str
            sample: 'C:\\ifs'
        id:
            description: The ID of the SMB open file.
            type: int
            sample: 950
        locks:
            description: The number of locks user holds on file.
            type: int
            sample: 3
        permissions:
            description: The user's permissions on file.
            type: list
            sample: ['read']
        user:
            description: User holding file open
            type: str
            sample: 'admin'
    sample:
        {
        "smb_file_details": [
            {
            "file": "C:\\ifs",
            "id": 1370,
            "locks": 0,
            "permissions": [
                "read"
            ],
            "user": "admin"
            }
        ]
        }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('smb_files')


class SmbFile(object):

    '''Class with SMB file operations'''

    def __init__(self):
        ''' Define all parameters required by this module'''
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(self.get_smb_files_parameters())
        mutually_exclusive = [['file_id', 'file_path']]
        # Initialize the ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            mutually_exclusive=mutually_exclusive,
            supports_check_mode=True
        )

        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        LOG.info('Got python SDK instance for provisioning on PowerScale ')
        LOG.info('Check Mode Flag: %s', self.module.check_mode)

        self.protocol_api = self.isi_sdk.ProtocolsApi(self.api_client)

    def get_smb_files(self):
        """
        Getting list of SMB open files
        :return: List SMB open files
        """
        try:
            smb_file_details = self.protocol_api.get_smb_openfiles().to_dict()
            return smb_file_details["openfiles"]
        except Exception as e:
            error_msg = f'Getting list of SMB open files failed with error: {utils.determine_error(e)}'
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_file_id(self, file_path=None, file_id=None):
        """Get SMB file id from file path"""
        file_id_list = []
        smb_file_details = self.get_smb_files()
        if file_path:
            file_path = file_path.replace("/", "\\")
            for file in smb_file_details:
                if file_path == file["file"][2:]:
                    file_id_list.append(file['id'])
            return file_id_list
        else:
            for file in smb_file_details:
                if file_id == file["id"]:
                    file_id_list.append(file_id)
            return file_id_list

    def close_smb_file(self, file_path=None, file_id=None):
        """Close the file in the SMB server"""
        try:
            file_id_list = self.get_file_id(file_path=file_path, file_id=file_id)
            if not self.module.check_mode:
                if file_id_list:
                    for file_id in file_id_list:
                        self.protocol_api.delete_smb_openfile(file_id)
                else:
                    return False
            return True
        except Exception as e:
            error_msg = f'Failed to close smb file: {utils.determine_error(e)}'
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def perform_module_operation(self):
        """
        Perform different actions based on parameters chosen in playbook
        """
        result = dict(
            changed=False,
            smb_file_details=dict()
        )
        changed = False
        state = self.module.params['state']
        file_id = self.module.params['file_id']
        file_path = self.module.params['file_path']

        result['smb_file_details'] = self.get_smb_files()

        if state == 'absent':
            changed = self.close_smb_file(file_id=file_id, file_path=file_path)

        if changed:
            result['smb_file_details'] = self.get_smb_files()
            result['changed'] = changed

        self.module.exit_json(**result)

    def get_smb_files_parameters(self):
        return dict(
            file_id=dict(type='int'),
            file_path=dict(type='str'),
            state=dict(default='present', type='str',
                       choices=['present', 'absent'])
        )


def main():
    """ Create PowerScale SmbFile object and perform actions
         on it based on user input from the playbook"""
    obj = SmbFile()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
