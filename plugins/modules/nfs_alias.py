#!/usr/bin/python
# Copyright: (c) 2022, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing NFS Aliases on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: nfs_alias
version_added: '1.7.0'
short_description:  Manage NFS aliases on a PowerScale Storage System
description:
- Managing NFS aliases on an PowerScale system includes creating NFS alias for
  NFS export, Getting details of an NFS alias,
  Modifying different attributes of the NFS alias and Deleting an NFS alias.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Trisha Datta(@Trisha-Datta) <ansible.team@dell.com>

options:
  nfs_alias_name:
    description:
    - Name of an NFS alias.
    required: true
    type: str
  path:
    description:
    - Specifies the path to which the alias points.
    - It is the absolute path for System access zone and it is relative if using non-system access zone.
    - If your access zone is System, and you have 'directory1' in the access zone, the path provided should be '/ifs/directory1'.
    - The directory on the path must exist, the NFS alias module will not create the directory.
    required: False
    type: str
  access_zone:
    description:
    - Specifies the zone in which the alias is valid.
    - Access zone once set cannot be changed.
    type: str
    default: System
  scope:
    description:
    - When specified as C(effective), or not specified, all fields are returned.
    - When specified as C(user), only fields with non-default values are shown.
    type: str
    default: 'effective'
    choices: [effective, user]
  check:
    description:
    - Check for conflicts when viewing alias.
    type: bool
    default: false
  new_alias_name:
    description:
    - New name of the alias.
    type: str
  state:
    description:
    - Defines whether the NFS alias should exist or not.
    - C(present) indicates that the NFS alias should exist in system.
    - C(absent) indicates that the NFS alias should not exist in system.
    default: "present"
    type: str
    choices: [absent, present]

notes:
- The I(check_mode) is supported.

'''

EXAMPLES = r'''
- name: Create NFS alias - check mode
  dellemc.powerscale.nfs_alias:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    nfs_alias_name: "/sample_alias_2"
    path: "/ifs"
    access_zone: 'System'
    state: "present"
  check_mode: true

- name: Create NFS alias
  dellemc.powerscale.nfs_alias:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    nfs_alias_name: "/sample_alias_2"
    path: "/ifs"
    access_zone: 'System'
    state: "present"

- name: Get NFS alias by name
  dellemc.powerscale.nfs_alias:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    nfs_alias_name: "/sample_alias_2"
    scope: "effective"
    check: true

- name: Modify NFS alias - check mode
  dellemc.powerscale.nfs_alias:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    nfs_alias_name: "/sample_alias_2"
    new_alias_name: "/Renamed_alias_2"
    path: "/ifs/Test"
    state: "present"
  check_mode: true

- name: Modify NFS alias
  dellemc.powerscale.nfs_alias:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    nfs_alias_name: "/sample_alias_2"
    new_alias_name: "/Renamed_alias_2"
    path: "/ifs/Test"
    state: "present"

- name: Delete NFS alias - check mode
  dellemc.powerscale.nfs_alias:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    nfs_alias_name: "/Renamed_alias_2"
    state: "absent"
  check_mode: true

- name: Delete NFS alias
  dellemc.powerscale.nfs_alias:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    nfs_alias_name: "/Renamed_alias_2"
    state: "absent"
'''

RETURN = r'''
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
nfs_alias_details:
    description: The NFS alias details.
    type: complex
    returned: always
    contains:
        health:
            description: The health of the NFS alias.
            type: str
            sample: 'unknown'
        id:
            description: The ID of the NFS alias.
            type: str
            sample: '/Sample_alias1'
        name:
            description: The name of the NFS alias.
            type: str
            sample: '/Sample_alias1'
        path:
            description: The path of the NFS alias.
            type: str
            sample:  '/ifs/dir/filepath'
        zone:
            description: Specifies the zone in which the NFS alias is valid.
            type: str
            sample: 'System'
    sample: {'aliases': [{'health': 'unknown',
                          'id': '/test_alias_1',
                          'name': '/test_alias_1',
                          'path': '/ifs/Test',
                          'zone': 'System'}]}
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('nfs_alias')


class NfsAlias(object):

    '''Class with NFS alias operations'''

    def __init__(self):
        ''' Define all parameters required by this module'''
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(self.get_nfs_alias_parameters())
        # Initialize the ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=True
        )
        # Result is a dictionary that contains changed status, NFS alias
        # details
        self.result = {
            "changed": False,
            "nfs_alias_details": {}
        }
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
        self.zone_summary_api = self.isi_sdk.ZonesSummaryApi(self.api_client)

    def get_nfs_alias(self, scope, check, access_zone, nfs_alias_name):
        '''
        Get details of an NFS alias using NFS alias ID
        '''
        LOG.info("Getting NFS alias details for name: %s", nfs_alias_name)
        try:

            nfsaliasobj = self.protocol_api.get_nfs_alias(
                nfs_alias_id=nfs_alias_name, zone=access_zone, scope=scope, check=check).to_dict()
            nfs_alias = nfsaliasobj['aliases'][0]
            return nfs_alias

        except utils.ApiException as e:
            if str(e.status) == '404':
                error_message = "NFS alias with name:{0} details are not found".\
                    format(nfs_alias_name)
                LOG.info(error_message)
                return None
            else:
                error_msg = utils.determine_error(error_obj=e)
                error_message = 'Get details of NFS alias with name:{0} failed with ' \
                                'error: {1}'.format(nfs_alias_name, error_msg)
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
        except Exception as e:
            error_message = 'Get details of NFS alias with name:{0} failed with ' \
                            'error: {1}'.format(nfs_alias_name, str(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def create_nfs_alias(self, path, access_zone, nfs_alias_name):
        '''
        Create NFS alias for given path and access_zone
        '''
        if nfs_alias_name is None:
            error_message = 'Provide a valid NFS alias name.'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

        if path is None:
            error_message = 'Provide a path for creating an NFS alias.'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

        nfs_alias = self.isi_sdk.NfsAliasCreateParams(
            path=path,
            name=nfs_alias_name,
            zone=access_zone)
        try:
            msg = ("Creating NFS alias with parameters:nfs_alias=%s",
                   nfs_alias)
            LOG.info(msg)
            if not self.module.check_mode:
                self.protocol_api.create_nfs_alias(nfs_alias, zone=access_zone)
            return True

        except Exception as e:
            error_message = 'Create NFS alias for path: {0}' \
                ' failed with error: {1}'.format(
                    path, utils.determine_error(error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def to_modify_nfs_alias(self, path, access_zone):
        '''
        To check if NFS alias needs to be modified or not
        '''
        new_path = None
        new_name = None
        to_modify = False
        nfs_alias_details = self.result['nfs_alias_details']

        if path is not None and path != nfs_alias_details['path']:
            new_path = path
            to_modify = True

        if self.module.params['new_alias_name'] and \
                self.module.params['new_alias_name'] != nfs_alias_details['name']:
            new_name = self.module.params['new_alias_name']
            to_modify = True

        if to_modify:
            nfs_alias = self.isi_sdk.NfsAlias(path=new_path, name=new_name)
            return nfs_alias
        return None

    def modify_nfs_alias(self, nfs_alias):
        '''
        Modify NFS alias in system
        '''
        try:
            if not self.module.check_mode:
                self.protocol_api.update_nfs_alias(
                    nfs_alias,
                    self.result['nfs_alias_details']['id'],
                    zone=self.result['nfs_alias_details']['zone'])
            return True

        except Exception as e:
            error_message = 'Modify NFS alias failed with error: {0}'.format(
                utils.determine_error(error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete_nfs_alias(self):
        '''
        Delete NFS alias from system
        '''
        nfs_alias = self.result['nfs_alias_details']

        try:
            msg = ('Deleting NFS alias with path: {0}, zone: {1} and ID: {2}'.format(
                nfs_alias['path'], nfs_alias['zone'], nfs_alias['id']))
            LOG.info(msg)
            if not self.module.check_mode:
                self.protocol_api.delete_nfs_alias(nfs_alias['id'], zone=nfs_alias['zone'])

            return True
        except Exception as e:
            error_message = (
                'Delete NFS alias with path: {0}, zone: {1}, id: {2} failed'
                'with error {3}'.format(
                    nfs_alias['path'][0],
                    nfs_alias['zone'],
                    nfs_alias['id'],
                    utils.determine_error(error_obj=e)))

            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_zone_base_path(self, access_zone):
        """Returns the base path of the Access Zone."""
        try:
            zone_path = (self.zone_summary_api.
                         get_zones_summary_zone(access_zone)).to_dict()
            return zone_path['summary']['path']
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Unable to fetch base path of Access Zone {0} ' \
                            'failed with error: {1}'.format(access_zone,
                                                            str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def determine_path(self):
        if self.module.params['path']:
            path = self.module.params['path'].rstrip("/")
            access_zone = self.module.params['access_zone']

            if access_zone.lower() != 'system':
                if not path.startswith('/'):
                    path = "/" + path
                path = self.get_zone_base_path(access_zone) + path

            return path

    def validate_params(self):

        param_list = ['nfs_alias_name', 'new_alias_name']
        for param in param_list:
            if self.module.params[param] and " " in self.module.params[param]:
                error_message = 'Spaces are not allowed in NFS alias name.' \
                    ' Provide a valid {0}'.format(param)
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

    def perform_module_operation(self):
        '''
        Perform different actions on NFS aliases based on user parameter
        chosen in playbook
        '''
        state = self.module.params['state']
        nfs_alias_name = self.module.params['nfs_alias_name']
        path = self.determine_path()
        access_zone = self.module.params['access_zone']
        scope = self.module.params['scope']
        check = self.module.params['check']
        new_alias_name = self.module.params['new_alias_name']
        changed = False
        modify_params = None

        self.validate_params()

        self.result['nfs_alias_details'] = self.get_nfs_alias(
            nfs_alias_name=nfs_alias_name, scope=scope, check=check, access_zone=access_zone)

        if self.result['nfs_alias_details']:
            # check for modification
            modify_params = self.to_modify_nfs_alias(path=path, access_zone=access_zone)

        if state == 'present' and self.result['nfs_alias_details'] and modify_params:
            # modify NFS alias
            changed = self.modify_nfs_alias(nfs_alias=modify_params) or changed

            if new_alias_name is not None and not self.module.check_mode:
                nfs_alias_name = new_alias_name

        if state == 'present' and not self.result['nfs_alias_details']:
            # create NFS alias
            if new_alias_name is not None:
                error_message = 'new_alias_name should not be provided during the creation of an NFS alias.'
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
            changed = self.create_nfs_alias(nfs_alias_name=nfs_alias_name, path=path, access_zone=access_zone)

        if state == 'absent' and self.result['nfs_alias_details']:
            # delete NFS alias
            changed = self.delete_nfs_alias()

        self.result['nfs_alias_details'] = self.get_nfs_alias(
            nfs_alias_name=nfs_alias_name, scope=scope, check=check, access_zone=access_zone)

        # Update the module's final state
        self.result['changed'] = changed
        self.module.exit_json(**self.result)

    def get_nfs_alias_parameters(self):
        return dict(
            nfs_alias_name=dict(type='str', required=True),
            path=dict(type='str'),
            access_zone=dict(type='str', default='System'),
            scope=dict(type='str', default="effective", choices=["effective", "user"]),
            check=dict(type='bool', default=False),
            new_alias_name=dict(type='str'),
            state=dict(default='present', type='str',
                       choices=['present', 'absent']))


def main():
    ''' Create PowerScale NFS alias object and perform action on it
        based on user input from playbook'''
    obj = NfsAlias()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
