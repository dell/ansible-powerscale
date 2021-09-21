#!/usr/bin/python
# Copyright: (c) 2020, DellEMC

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Ansible module for managing NFS Exports on DellEMC PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.2',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }


DOCUMENTATION = r'''
---
module: dellemc_powerscale_nfs
version_added: '1.2.0'
short_description:  Manage NFS exports on a DellEMC PowerScale system
description:
- Managing NFS exports on an PowerScale system includes creating NFS export for
  a directory in an access zone, adding or removing clients, modifying
  different parameters of the export and deleting export.

extends_documentation_fragment:
  - dellemc.powerscale.dellemc_powerscale.powerscale

author:
- Manisha Agrawal(@agrawm3) <ansible.team@dell.com>

options:
  path:
    description:
    - Specifies the filesystem path. It is the absolute path for System access zone
      and it is relative if using non-system access zone. For example, if your access
      zone is 'Ansible' and it has a base path '/ifs/ansible' and the path
      specified is '/user1', then the effective path would be '/ifs/ansible/user1'.
      If your access zone is System, and you have 'directory1' in the access
      zone, the path provided should be '/ifs/directory1'.
    - The directory on the path must exist - the NFS module will not create
      the directory.
    - Ansible module will only support exports with a unique path.
    - If there are multiple exports present with the same path, fetching details,
      creation, modification or deletion of such exports will fail.
    required: True
    type: str
  access_zone:
    description:
    - Specifies the zone in which the export is valid.
    - Access zone once set cannot be changed.
    type: str
    default: System
  clients:
    description:
    - Specifies the clients to the export. The type of access to clients in
      this list is determined by the 'read_only' parameter.
    - This list can be changed anytime during the lifetime of the NFS export.
    type: list
    elements: str
  root_clients:
    description:
    - Specifies the clients with root access to the export.
    - This list can be changed anytime during the lifetime of the NFS export.
    type: list
    elements: str
  read_only_clients:
    description:
    - Specifies the clients with read-only access to the export, even when the
      export is read/write.
    - This list can be changed anytime during the lifetime of the NFS export.
    type: list
    elements: str
  read_write_clients:
    description:
    - Specifies the clients with both read and write access to the export,
      even when the export is set to read-only.
    - This list can be changed anytime during the lifetime of the NFS export.
    type: list
    elements: str
  read_only:
    description:
    - Specifies whether the export is read-only or read-write. This parameter
      only has effect on the 'clients' list and not the other three types of
      clients.
    - This setting can be modified any time. If it is not set at the time of
      creation, the export will be of type read/write.
    type: bool
  sub_directories_mountable:
    description:
    - True if all directories under the specified paths are mountable. If not
      set, sub-directories will not be mountable.
    - This setting can be modified any time.
    type: bool
  description:
    description:
    - Optional description field for the NFS export.
    - Can be modified by passing a new value.
    type: str
  state:
    description:
    - Defines whether the NFS export should exist or not.
    - present indicates that the NFS export should exist in system.
    - absent indicates that the NFS export should not exist in system.
    required: True
    type: str
    choices: [absent, present]
  client_state:
    description:
    - Defines whether the clients can access the NFS export.
    - present-in-export indicates that the clients can access the NFS export.
    - absent-in-export indicates that the client cannot access the NFS export.
    - Required when adding or removing access of clients from the export.
    - While removing clients, only the specified clients will be removed from
      the export, others will remain as is.
    required: False
    type: str
    choices: [present-in-export, absent-in-export]
  '''

EXAMPLES = r'''

  - name: Create NFS Export
    dellemc_powerscale_nfs:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      path: "<path>"
      access_zone: "{{access_zone}}"
      read_only_clients:
      - "{{client1}}"
      - "{{client2}}"
      read_only: True
      clients: ["{{client3}}"]
      client_state: 'present-in-export'
      state: 'present'

  - name: Get NFS Export
    dellemc_powerscale_nfs:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      path: "<path>"
      access_zone: "{{access_zone}}"
      state: 'present'

  - name: Add a root client
    dellemc_powerscale_nfs:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      path: "<path>"
      access_zone: "{{access_zone}}"
      root_clients:
      - "{{client4}}"
      client_state: 'present-in-export'
      state: 'present'

  - name: Set sub_directories_mountable flag to True
    dellemc_powerscale_nfs:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      path: "<path>"
      access_zone: "{{access_zone}}"
      sub_directories_mountable: True
      state: 'present'

  - name: Remove a root client
    dellemc_powerscale_nfs:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      path: "<path>"
      access_zone: "{{access_zone}}"
      root_clients:
      - "{{client4}}"
      client_state: 'absent-in-export'
      state: 'present'

  - name: Modify description
    dellemc_powerscale_nfs:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      path: "<path>"
      access_zone: "{{access_zone}}"
      description: "new description"
      state: 'present'

  - name: Set read_only flag to False
    dellemc_powerscale_nfs:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      path: "<path>"
      access_zone: "{{access_zone}}"
      read_only: False
      state: 'present'

  - name: Delete NFS Export
    dellemc_powerscale_nfs:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      path: "<path>"
      access_zone: "{{access_zone}}"
      state: 'absent'

'''

RETURN = r'''
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
NFS_export_details:
    description: The updated NFS Export details.
    type: complex
    returned: always
    contains:
        all_dirs:
            description: sub_directories_mountable flag value.
            type: bool
        id:
            description: The ID of the NFS Export, generated by the array.
            type: int
            sample: 12
        paths:
            description: The filesystem path.
            type: list
            sample:  ['/ifs/dir/filepath']
        zone:
            description: Specifies the zone in which the export is valid.
            type: str
            sample: 'System'
        read_only:
            description: Specifies whether the export is read-only or read-write.
            type: bool
        read_only_clients:
            description: The list of read only clients for the NFS Export.
            type: list
            sample:  ['client_ip', 'client_ip']
        read_write_clients:
            description: The list of read write clients for the NFS Export.
            type: list
            sample:  ['client_ip', 'client_ip']
        root_clients:
            description: The list of root clients for the NFS Export.
            type: list
            sample:  ['client_ip', 'client_ip']
        clients:
            description: The list of clients for the NFS Export.
            type: list
            sample:  ['client_ip', 'client_ip']
        description:
            description: Description for the export.
            type: str
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import dellemc_ansible_powerscale_utils as utils
import logging
import re

LOG = utils.get_logger(
    module_name='dellemc_powerscale_nfs',
    log_devel=logging.INFO)


class PowerScaleNfsExport(object):

    '''Class with NFS export operations'''

    def __init__(self):
        ''' Define all parameters required by this module'''
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(self.get_powerscale_nfs_parameters())
        # Initialize the ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False
        )
        # Result is a dictionary that contains changed status, NFS export
        # details
        self.result = {
            "changed": False,
            "NFS_export_details": {}
        }
        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        LOG.info('Got python SDK instance for provisioning on PowerScale ')

        self.protocol_api = self.isi_sdk.ProtocolsApi(self.api_client)
        self.zone_summary_api = self.isi_sdk.ZonesSummaryApi(self.api_client)

    def get_zone_base_path(self, access_zone):
        """Returns the base path of the Access Zone."""
        try:
            zone_path = (self.zone_summary_api.
                         get_zones_summary_zone(access_zone)).to_dict()
            return zone_path['summary']['path']
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Unable to fetch base path of Access Zone {0} ' \
                            'failed with error: {1}'.format(access_zone,
                                                            str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_nfs_export(self, path, access_zone):
        '''
        Get details of an NFS export using filesystem path and access zone
        '''
        LOG.debug("Getting NFS export details for path: %s and access zone: "
                  "%s", path, access_zone)
        try:
            NfsExportsExtendedObj = self.protocol_api.list_nfs_exports(
                path=path, zone=access_zone)
            if NfsExportsExtendedObj.total > 1:
                error_msg = 'Multiple NFS Exports found'
                LOG.error(error_msg)
                self.module.fail_json(msg=error_msg)

            elif NfsExportsExtendedObj.total == 0:
                LOG.debug('NFS Export for given path: %s and access zone: %s '
                          'not found', path, access_zone)
                return {}

            else:
                nfs_export = NfsExportsExtendedObj.exports[0]
                return nfs_export.to_dict()

        except Exception as e:
            error_msg = (
                "Got error {0} while getting NFS export details for path: "
                "{1} and access zone: {2}" .format(
                    self.determine_error(e),
                    path,
                    access_zone))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def _create_client_lists_from_playbook(self):
        all_client_list = [
            self.module.params['clients'],
            self.module.params['read_only_clients'],
            self.module.params['read_write_clients'],
            self.module.params['root_clients']]
        return all_client_list

    def _get_nfs_export_from_id(self, nfs_export_id, access_zone):
        '''
        Get details of an NFS export using NFS export ID and access zone
        '''
        LOG.info("Getting NFS export details for id: %s and access zone: %s",
                 nfs_export_id, access_zone)
        try:
            NfsExportsObj = self.protocol_api.get_nfs_export(
                nfs_export_id, zone=access_zone)
            nfs_export = NfsExportsObj.exports[0]
            return nfs_export.to_dict()

        except Exception as e:
            error_msg = (
                "Got error {0} while getting NFS export details for ID: "
                "{1} and access zone: {2}" .format(
                    self.determine_error(e),
                    nfs_export_id,
                    access_zone))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def _create_nfs_export_create_params_object(self, path):
        try:
            nfs_export = self.isi_sdk.NfsExportCreateParams(
                paths=[path],
                clients=self.module.params['clients'],
                read_only_clients=self.module.params['read_only_clients'],
                read_write_clients=self.module.params['read_write_clients'],
                root_clients=self.module.params['root_clients'],
                read_only=self.module.params['read_only'],
                all_dirs=self.module.params['sub_directories_mountable'],
                description=self.module.params['description'],
                zone=self.module.params['access_zone'])
            return nfs_export
        except Exception as e:
            errorMsg = 'Create NfsExportCreateParams object for path {0}' \
                'failed with error {1}'.format(
                    path, self.determine_error(e))
            LOG.error(errorMsg)
            self.module.fail_json(msg=errorMsg)

    def create_nfs_export(self, path, access_zone):
        '''
        Create NFS export for given path and access_zone
        '''
        nfs_export = self._create_nfs_export_create_params_object(path)
        try:
            msg = ("Creating NFS export with parameters:nfs_export=%s",
                   nfs_export)
            LOG.info(msg)
            response = self.protocol_api.create_nfs_export(nfs_export, zone=access_zone)
            self.result['NFS_export_details'] = self._get_nfs_export_from_id(response.id, access_zone=access_zone)
            return True

        except Exception as e:
            errorMsg = 'Create NFS export for path: {0} and access zone: {1}' \
                ' failed with error: {2}'.format(
                    path, access_zone, self.determine_error(e))
            LOG.error(errorMsg)
            self.module.fail_json(msg=errorMsg)

    def _create_current_client_dict_from_playbook(self):
        client_dict_playbook_input = {
            'read_only_clients': self.module.params['read_only_clients'],
            'clients': self.module.params['clients'],
            'root_clients': self.module.params['root_clients'],
            'read_write_clients': self.module.params['read_write_clients']}

        return client_dict_playbook_input

    def _create_current_client_dict(self):
        current_client_dict = {
            'read_only_clients': self.result['NFS_export_details']['read_only_clients'],
            'clients': self.result['NFS_export_details']['clients'],
            'root_clients': self.result['NFS_export_details']['root_clients'],
            'read_write_clients': self.result['NFS_export_details']['read_write_clients']}

        return current_client_dict

    def _check_add_clients(self, nfs_export):
        '''
        Check if clients are to be added to NFS export
        '''
        playbook_client_dict = self._create_current_client_dict_from_playbook()
        current_client_dict = self._create_current_client_dict()
        mod_flag = False

        mod_flag1 = False
        if playbook_client_dict['clients']:
            for client in playbook_client_dict['clients']:
                if client not in current_client_dict['clients']:
                    current_client_dict['clients'].append(client)
                    mod_flag1 = True

            if mod_flag1:
                nfs_export.clients = current_client_dict['clients']

        mod_flag2 = False
        if playbook_client_dict['read_write_clients']:
            for client in playbook_client_dict['read_write_clients']:
                if client not in current_client_dict['read_write_clients']:
                    current_client_dict['read_write_clients'].append(client)
                    mod_flag2 = True

            if mod_flag2:
                nfs_export.read_write_clients = current_client_dict['read_write_clients']

        mod_flag3 = False
        if playbook_client_dict['read_only_clients']:
            for client in playbook_client_dict['read_only_clients']:
                if client not in current_client_dict['read_only_clients']:
                    current_client_dict['read_only_clients'].append(client)
                    mod_flag3 = True

            if mod_flag3:
                nfs_export.read_only_clients = current_client_dict['read_only_clients']

        mod_flag4 = False
        if playbook_client_dict['root_clients']:
            for client in playbook_client_dict['root_clients']:
                if client not in current_client_dict['root_clients']:
                    current_client_dict['root_clients'].append(client)
                    mod_flag4 = True

            if mod_flag4:
                nfs_export.root_clients = current_client_dict['root_clients']

        mod_flag = mod_flag1 or mod_flag2 or mod_flag3 or mod_flag4
        return mod_flag, nfs_export

    def _check_remove_clients(self, nfs_export):
        '''
        Check if clients are to be removed from NFS export
        '''
        playbook_client_dict = self._create_current_client_dict_from_playbook()
        current_client_dict = self._create_current_client_dict()
        mod_flag = False

        mod_flag1 = False
        if playbook_client_dict['clients']:
            for client in playbook_client_dict['clients']:
                if client in current_client_dict['clients']:
                    current_client_dict['clients'].remove(client)
                    mod_flag1 = True

            if mod_flag1:
                nfs_export.clients = current_client_dict['clients']

        mod_flag2 = False
        if playbook_client_dict['read_write_clients']:
            for client in playbook_client_dict['read_write_clients']:
                if client in current_client_dict['read_write_clients']:
                    current_client_dict['read_write_clients'].remove(client)
                    mod_flag2 = True

            if mod_flag2:
                nfs_export.read_write_clients = current_client_dict['read_write_clients']

        mod_flag3 = False
        if playbook_client_dict['read_only_clients']:
            for client in playbook_client_dict['read_only_clients']:
                if client in current_client_dict['read_only_clients']:
                    current_client_dict['read_only_clients'].remove(client)
                    mod_flag3 = True

            if mod_flag3:
                nfs_export.read_only_clients = current_client_dict['read_only_clients']

        mod_flag4 = False
        if playbook_client_dict['root_clients']:
            for client in playbook_client_dict['root_clients']:
                if client in current_client_dict['root_clients']:
                    current_client_dict['root_clients'].remove(client)
                    mod_flag4 = True

            if mod_flag4:
                nfs_export.root_clients = current_client_dict['root_clients']

        mod_flag = mod_flag1 or mod_flag2 or mod_flag3 or mod_flag4
        return mod_flag, nfs_export

    def _check_mod_field(self, field_name_playbook, field_name_powerscale):
        _field_mod = False
        if self.module.params[field_name_playbook] is None:
            field_value = self.result['NFS_export_details'][field_name_powerscale]
        elif self.module.params[field_name_playbook] == \
                self.result['NFS_export_details'][field_name_powerscale]:
            field_value = self.result['NFS_export_details'][field_name_powerscale]
        else:
            field_value = self.module.params[field_name_playbook]
            _field_mod = True
        return _field_mod, field_value

    def modify_nfs_export(self, path, access_zone):
        '''
        Modify NFS export in system
        '''
        nfs_export = self.isi_sdk.NfsExport()
        client_flag = False
        if self.module.params['client_state'] == 'present-in-export':
            client_flag, nfs_export = self._check_add_clients(nfs_export)
        if self.module.params['client_state'] == 'absent-in-export':
            client_flag, nfs_export = self._check_remove_clients(nfs_export)

        read_only_flag, read_only_value = self._check_mod_field(
            'read_only', 'read_only')
        all_dirs_flag, all_dirs_value = self._check_mod_field(
            'sub_directories_mountable', 'all_dirs')
        description_flag, description_value = self._check_mod_field(
            'description', 'description')

        if all(
            field_mod_flag is False for field_mod_flag in [
                client_flag,
                read_only_flag,
                all_dirs_flag,
                description_flag]):
            LOG.info(
                'No change detected for the NFS Export, returning changed = False')
            return False
        else:

            nfs_export.read_only = read_only_value if read_only_flag else None
            nfs_export.all_dirs = all_dirs_value if all_dirs_flag else None
            nfs_export.description = description_value if description_flag else None
            LOG.debug('Modifying NFS Export with  %s details', nfs_export)

            try:
                self.protocol_api.update_nfs_export(
                    nfs_export,
                    self.result['NFS_export_details']['id'],
                    zone=self.result['NFS_export_details']['zone'])
                # update result with updated details
                self.result['NFS_export_details'] = self.get_nfs_export(
                    path, access_zone)
                return True

            except Exception as e:
                errorMsg = 'Modify NFS export for path: {0} and access zone:' \
                    ' {1} failed with error: {2}'.format(
                        path, access_zone, self.determine_error(e))
                LOG.error(errorMsg)
                self.module.fail_json(msg=errorMsg)

    def delete_nfs_export(self):
        '''
        Delete NFS export from system
        '''
        nfs_export = self.result['NFS_export_details']
        try:
            msg = ('Deleting NFS export with path: {0}, zone: {1} and ID: {2}'.format(
                nfs_export['paths'][0], nfs_export['zone'], nfs_export['id']))
            LOG.info(msg)
            self.protocol_api.delete_nfs_export(
                nfs_export['id'], zone=nfs_export['zone'])

            self.result['NFS_export_details'] = {}
            return True
        except Exception as e:
            errorMsg = (
                'Delete NFS export with path: {0}, zone: {1}, id: {2} failed'
                'with error {3}'.format(
                    nfs_export['paths'][0],
                    nfs_export['zone'],
                    nfs_export['id'],
                    self.determine_error(e)))
            LOG.error(errorMsg)
            self.module.fail_json(msg=errorMsg)

    def determine_error(self, error_obj):
        '''Format the error object'''
        if isinstance(error_obj, utils.ApiException):
            error = re.sub("[\n \"]+", ' ', str(error_obj.body))
        else:
            error = str(error_obj)
        return error

    def determine_path(self):
        path = self.module.params['path'].rstrip("/")
        access_zone = self.module.params['access_zone']

        if access_zone.lower() != 'system':
            if not path.startswith('/'):
                path = "/" + path
            path = self.get_zone_base_path(access_zone) + path

        return path

    def _validate_input(self):
        all_client_list = self._create_client_lists_from_playbook()
        if self.module.params['client_state'] is not None and all(
                client_list is None for client_list in all_client_list):
            error_msg = 'Invalid input: Client state is given, clients not specified'
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)
        if self.module.params['client_state'] is None and any(
                client_list is not None for client_list in all_client_list):
            error_msg = 'Invalid input: Clients are given, client state not specified'
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def perform_module_operation(self):
        '''
        Perform different actions on NFS exports based on user parameter
        chosen in playbook
        '''
        state = self.module.params['state']
        access_zone = self.module.params['access_zone']
        path = self.determine_path()
        changed = False

        self.result['NFS_export_details'] = self.get_nfs_export(
            path, access_zone)

        self._validate_input()
        if state == 'present' and self.result['NFS_export_details']:
            # check for modification
            changed = self.modify_nfs_export(path, access_zone) or changed

        if state == 'present' and not self.result['NFS_export_details']:
            # create NFS export
            changed = self.create_nfs_export(path, access_zone)

        if state == 'absent' and self.result['NFS_export_details']:
            # delete nfs export
            changed = self.delete_nfs_export() or changed

        # Update the module's final state
        LOG.info('changed %s', changed)
        self.result['changed'] = changed
        self.module.exit_json(**self.result)

    def get_powerscale_nfs_parameters(self):
        return dict(
            path=dict(required=True, type='str', no_log=True),
            access_zone=dict(type='str', default='System'),
            clients=dict(type='list', elements='str'),
            root_clients=dict(type='list', elements='str'),
            read_only_clients=dict(type='list', elements='str'),
            read_write_clients=dict(type='list', elements='str'),
            client_state=dict(type='str',
                              choices=['present-in-export',
                                       'absent-in-export']),
            description=dict(type='str'),
            read_only=dict(type='bool'),
            sub_directories_mountable=dict(type='bool'),
            state=dict(required=True, type='str', choices=['present',
                                                           'absent'])
        )


def main():
    ''' Create PowerScale_NFS export object and perform action on it
        based on user input from playbook'''
    obj = PowerScaleNfsExport()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
