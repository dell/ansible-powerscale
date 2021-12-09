#!/usr/bin/python
# Copyright: (c) 2019, DellEMC

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Ansible module for managing access zones on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r'''
---
module: dellemc_powerscale_accesszone

version_added: '1.2.0'

short_description: Manages access zones on PowerScale

description:
- Managing access zones on the PowerScale storage system includes getting details of the
  access zone and modifying the smb and nfs settings.

extends_documentation_fragment:
  - dellemc.powerscale.dellemc_powerscale.powerscale

author:
- Akash Shendge (@shenda1) <ansible.team@dell.com>

options:
  az_name:
    description:
    - The name of the access zone.
    type: str
    required: True
  path:
    description:
    - Specifies the access zone base directory path.
    type: str
  groupnet:
    description:
    - Name of the groupnet for create access zone
    type: str
    default: groupnet0
  create_path:
    description:
    - Determines if a path is created when a path does not exist.
    type: bool
  smb:
    description:
    - Specifies the default SMB setting parameters of access zone.
    type: dict
    suboptions:
      create_permissions:
        description:
        - Sets the default source permissions to apply when a file or
          directory is created.
        type: str
        choices: [default acl, Inherit mode bits, Use create mask and mode]
        default: default acl
      directory_create_mask:
        description:
        - Specifies the UNIX mask bits (octal) that are removed when a directory
          is created, restricting permissions.
        - Mask bits are applied before mode bits are applied.
        type: str
      directory_create_mode:
        description:
        - Specifies the UNIX mode bits (octal) that are added when a directory is
          created, enabling permissions.
        type: str
      file_create_mask:
        description:
        - Specifies the UNIX mask bits (octal) that are removed when a file is
          created, restricting permissions.
        type: str
      file_create_mode:
        description:
        - Specifies the UNIX mode bits (octal) that are added when a file is
          created, enabling permissions.
        type: str
      access_based_enumeration:
        description:
        - Allows access based enumeration only on the files and folders that
          the requesting user can access.
        type: bool
      access_based_enumeration_root_only:
        description:
        - Access-based enumeration on only the root directory of the share.
        type: bool
      ntfs_acl_support:
        description:
        - Allows ACLs to be stored and edited from SMB clients.
        type: bool
      oplocks:
        description:
        - An oplock allows clients to provide performance improvements by
          using locally-cached information.
        type: bool

  nfs:
    description:
    - Specifies the default NFS setting parameters of access zone.
    type: dict
    suboptions:
      commit_asynchronous:
        description:
        - Set to True if NFS commit requests execute asynchronously.
        type: bool
      nfsv4_domain:
        description:
        - Specifies the domain or realm through which users and groups are
          associated.
        type: str
      nfsv4_allow_numeric_ids:
        description:
        - If true, sends owners and groups as UIDs and GIDs when look up
          fails or if the 'nfsv4_no_name' property is set to 1.
        type: bool
      nfsv4_no_domain:
        description:
        - If true, sends owners and groups without a domain name.
        type: bool
      nfsv4_no_domain_uids:
        description:
        - If true, sends UIDs and GIDs without a domain name.
        type: bool
      nfsv4_no_names:
        description:
        - If true, sends owners and groups as UIDs and GIDs.
        type: bool
  provider_state:
    description:
    - Defines whether the auth providers should be added or removed from access zone.
    - If auth_providers are given, then provider_state should also be specified.
    - add - indicates that the auth providers should be added to the access zone.
    - remove - indicates that auth providers should be removed from the access zone.
    choices: [add, remove]
    type: str
    required: False
  auth_providers:
    description:
    - Specifies the auth providers which need to be added or removed from access zone.
    - If auth_providers are given, then provider_state should also be specified.
    type: list
    elements: dict
    suboptions:
      provider_name:
        description:
        - Specifies the auth provider name which needs to be added or removed from access zone.
        type: str
        required: True
      provider_type:
        description:
        - Specifies the auth provider type which needs to be added or removed from access zone.
        choices: ['local', 'file', 'ldap', 'ads']
        type: str
        required: True
  state:
    description:
    - Defines whether the access zone should exist or not.
    - present - indicates that the access zone should exist on the system.
    - absent - indicates that the access zone should not exist on the system.
    choices: ['present', 'absent']
    type: str
    required: True

notes:
- Deletion of access zone is not allowed through the Ansible module.
'''

EXAMPLES = r'''
- name: Get details of access zone including smb and nfs settings
  dellemc_powerscale_accesszone:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      az_name: "{{access zone}}"
      state: "present"

- name: Modify smb settings of access zone
  dellemc_powerscale_accesszone:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      az_name: "{{access zone}}"
      state: "present"
      smb:
        create_permissions: 'default acl'
        directory_create_mask: '777'
        directory_create_mode: '700'
        file_create_mask: '700'
        file_create_mode: '100'
        access_based_enumeration: true
        access_based_enumeration_root_only: false
        ntfs_acl_support: true
        oplocks: true

- name: Modify nfs settings of access zone
  dellemc_powerscale_accesszone:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      az_name: "{{access zone}}"
      state: "present"
      nfs:
        commit_asynchronous: false
        nfsv4_allow_numeric_ids: false
        nfsv4_domain: 'localhost'
        nfsv4_no_domain: false
        nfsv4_no_domain_uids: false
        nfsv4_no_names: false

- name: Modify smb and nfs settings of access zone
  dellemc_powerscale_accesszone:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      az_name: "{{access zone}}"
      state: "present"
      smb:
        create_permissions: 'default acl'
        directory_create_mask: '777'
        directory_create_mode: '700'
        file_create_mask: '700'
        file_create_mode: '100'
        access_based_enumeration: true
        access_based_enumeration_root_only: false
        ntfs_acl_support: true
        oplocks: true
      nfs:
        commit_asynchronous: false
        nfsv4_allow_numeric_ids: false
        nfsv4_domain: 'localhost'
        nfsv4_no_domain: false
        nfsv4_no_domain_uids: false
        nfsv4_no_names: false

- name: Add Auth Providers to the  access zone
  dellemc_powerscale_accesszone:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      az_name: "{{access zone}}"
      provider_state: "add"
      auth_providers:
         - provider_name: "System"
           provider_type: "file"
         - provider_name: "ldap-prashant"
           provider_type: "ldap"
      state: "present"

- name: Remove Auth Providers from the  access zone
  dellemc_powerscale_accesszone:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      az_name: "{{access zone}}"
      provider_state: "remove"
      auth_providers:
         - provider_name: "System"
           provider_type: "file"
      state: "present"

- name: Create New Access Zone
  dellemc_powerscale_accesszone:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      az_name: "{{access zone}}"
      path: "/ifs/test_dir"
      groupnet: "groupnet1"
      create_path: True
      provider_state: "add"
      auth_providers:
        - provider_name: "System"
          provider_type: "file"
      state: "present"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed
    returned: always
    type: bool

smb_modify_flag:
    description: Whether or not the default SMB settings of access zone has
                 changed
    returned: on success
    type: bool

nfs_modify_flag:
    description: Whether or not the default NFS settings of access zone has
                 changed
    returned: on success
    type: bool

access_zone_modify_flag:
    description: Whether auth providers linked to access zone has changed
    returned: on success
    type: bool

access_zone_details:
    description: The access zone details
    returned: When access zone exists
    type: complex
    contains:
        nfs_settings:
            description: NFS settings of access zone
            type: complex
            contains:
                export_settings:
                    description: Default values for NFS exports
                    type: complex
                    contains:
                        commit_asynchronous:
                            description: Set to True if NFS commit requests execute asynchronously
                            type: bool
                zone_settings:
                    description: NFS server settings for this zone
                    type: complex
                    contains:
                        nfsv4_domain:
                            description: Specifies the domain or realm through which
                                         users and groups are associated
                            type: str
                        nfsv4_allow_numeric_ids:
                            description: If true, sends owners and groups as UIDs and GIDs when
                                         look up fails or if the 'nfsv4_no_name' property
                                         is set to 1
                            type: bool
                        nfsv4_no_domain:
                            description: If true, sends owners and groups without a domain name
                            type: bool
                        nfsv4_no_domain_uids:
                            description: If true, sends UIDs and GIDs without a domain name
                            type: bool
                        nfsv4_no_names:
                            description: If true, sends owners and groups as UIDs and GIDs
                            type: bool
        smb_settings:
            description: SMB settings of access zone
            type: complex
            contains:
                directory_create_mask(octal):
                    description: UNIX mask bits for directory in octal format
                    type: str
                directory_create_mode(octal):
                     description: UNIX mode bits for directory in octal format
                     type: str
                file_create_mask(octal):
                    description: UNIX mask bits for file in octal format
                    type: str
                file_create_mode(octal):
                     description: UNIX mode bits for file in octal format
                     type: str
'''
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import dellemc_ansible_powerscale_utils as utils

LOG = utils.get_logger('dellemc_powerscale_accesszone')


class PowerScaleAccessZone(object):
    """Class with access zone operations"""

    def __init__(self):
        """ Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_powerscale_accesszone_parameters())

        required_together = [['auth_providers', 'provider_state']]

        # initialize the Ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False,
            required_together=required_together
        )

        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.api_instance = utils.isi_sdk.ZonesApi(self.api_client)
        self.api_protocol = utils.isi_sdk.ProtocolsApi(self.api_client)
        self.api_auth = utils.isi_sdk.AuthApi(self.api_client)
        LOG.info('Got the isi_sdk instance for authorization on to PowerScale')

    def get_details(self, name):
        """ Get access zone details"""
        try:
            nfs_settings = {}
            api_response = self.api_instance.get_zone(name).to_dict()
            nfs_export_settings = self.api_protocol.get_nfs_settings_export(
                zone=name).to_dict()
            nfs_export_settings['export_settings'] = nfs_export_settings[
                'settings']
            del nfs_export_settings['settings']
            nfs_zone_settings = self.api_protocol.get_nfs_settings_zone(
                zone=name).to_dict()
            nfs_zone_settings['zone_settings'] = nfs_zone_settings['settings']
            del nfs_zone_settings['settings']

            nfs_settings['nfs_settings'] = nfs_export_settings
            nfs_settings['nfs_settings'].update(nfs_zone_settings)

            api_response.update(nfs_settings)
            smb_settings = self.api_protocol.get_smb_settings_share(
                zone=name).to_dict()
            smb_settings['settings']['directory_create_mask(octal)'] = \
                "{0:o}".format(smb_settings['settings']
                               ['directory_create_mask'])
            smb_settings['settings']['directory_create_mode(octal)'] = \
                "{0:o}".format(smb_settings['settings']
                               ['directory_create_mode'])
            smb_settings['settings']['file_create_mask(octal)'] = \
                "{0:o}".format(smb_settings['settings']
                               ['file_create_mask'])
            smb_settings['settings']['file_create_mode(octal)'] = \
                "{0:o}".format(smb_settings['settings']
                               ['file_create_mode'])
            smb_settings['smb_settings'] = smb_settings['settings']
            del smb_settings['settings']
            api_response.update(smb_settings)
            return api_response
        except utils.ApiException as e:
            if str(e.status) == '404':
                error_message = "Access zone {0} details are not found".\
                    format(name)
                LOG.info(error_message)
                return None
            else:
                error_msg = utils.determine_error(error_obj=e)
                error_message = 'Get details of access zone {0} failed with ' \
                                'error: {1}'.format(name, error_msg)
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
        except Exception as e:
            error_message = 'Get details of access zone {0} failed with ' \
                            'error: {1}'.format(name, str(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def is_smb_modification_required(self, smb_playbook, access_zone_details):
        """ Check if default smb settings of access zone needs to be modified
        """
        # Convert octal parameters to decimal for comparison
        try:
            if 'directory_create_mask' in smb_playbook and \
                    smb_playbook['directory_create_mask'] is not None:
                smb_playbook['directory_create_mask'] = int(
                    smb_playbook['directory_create_mask'], 8)
            if 'directory_create_mode' in smb_playbook and \
                    smb_playbook['directory_create_mode'] is not None:
                smb_playbook['directory_create_mode'] = int(
                    smb_playbook['directory_create_mode'], 8)
            if 'file_create_mask' in smb_playbook and \
                    smb_playbook['file_create_mask'] is not None:
                smb_playbook['file_create_mask'] = int(
                    smb_playbook['file_create_mask'], 8)
            if 'file_create_mode' in smb_playbook and \
                    smb_playbook['file_create_mode'] is not None:
                smb_playbook['file_create_mode'] = int(
                    smb_playbook['file_create_mode'], 8)
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Conversion from octal to decimal failed with ' \
                            'error: {0}'.format(error_msg)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

        for key in smb_playbook.keys():
            if smb_playbook[key] != access_zone_details['smb_settings'][key]:
                LOG.info("First Key Modification %s", key)
                return True
        return False

    def smb_modify(self, name, smb):
        """ Modify smb settings of access zone """
        try:
            self.api_protocol.update_smb_settings_share(smb, zone=name)
            LOG.info("Modification Successful")
            return True
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Modify SMB share settings of access zone {0} ' \
                'failed with error: {1}'.format(name, error_msg)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def is_nfs_modification_required(self, nfs_playbook, access_zone_details):
        """ Check if default nfs settings of access zone needs to be modified
         """
        nfs_export_flag = False
        nfs_zone_flag = False

        for key in nfs_playbook.keys():
            if key in access_zone_details['nfs_settings']['export_settings'].\
                    keys():
                if nfs_playbook[key] != access_zone_details['nfs_settings'][
                        'export_settings'][key]:
                    LOG.info("First Key Modification %s", key)
                    nfs_export_flag = True

        for key in nfs_playbook.keys():
            if key in access_zone_details['nfs_settings']['zone_settings'].\
                    keys():
                if nfs_playbook[key] != access_zone_details['nfs_settings'][
                        'zone_settings'][key]:
                    LOG.info("First Key Modification %s", key)
                    nfs_zone_flag = True

        return nfs_export_flag, nfs_zone_flag

    def nfs_modify(self, name, nfs, nfs_export_flag, nfs_zone_flag):
        """ Modify nfs settings of access zone """
        nfs_export_dict = {}
        nfs_zone_dict = {}

        if nfs_export_flag:
            if 'commit_asynchronous' in nfs:
                nfs_export_dict['commit_asynchronous'] = nfs[
                    'commit_asynchronous']

        if nfs_zone_flag:
            if 'nfsv4_domain' in nfs:
                nfs_zone_dict['nfsv4_domain'] = nfs['nfsv4_domain']
            if 'nfsv4_allow_numeric_ids' in nfs:
                nfs_zone_dict['nfsv4_allow_numeric_ids'] = nfs[
                    'nfsv4_allow_numeric_ids']
            if 'nfsv4_no_domain' in nfs:
                nfs_zone_dict['nfsv4_no_domain'] = nfs['nfsv4_no_domain']
            if 'nfsv4_no_domain_uids' in nfs:
                nfs_zone_dict['nfsv4_no_domain_uids'] = nfs[
                    'nfsv4_no_domain_uids']
            if 'nfsv4_no_names' in nfs:
                nfs_zone_dict['nfsv4_no_names'] = nfs['nfsv4_no_names']

        try:
            if nfs_export_flag:
                self.api_protocol.update_nfs_settings_export(nfs_export_dict,
                                                             zone=name)

            if nfs_zone_flag:
                self.api_protocol.update_nfs_settings_zone(nfs_zone_dict,
                                                           zone=name)
            return True
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Modify NFS export settings of access zone {0} ' \
                            'failed with error: {1}'.format(name, error_msg)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def add_auth_providers_to_access_zone(self, name, auth_providers, existing_auth_providers):
        """ Add auth providers to access zone """
        try:
            updated_auth_providers_list = existing_auth_providers
            add_auth_providers_required = False
            provider_summary = self.api_auth.get_providers_summary()
            all_providers = provider_summary.provider_instances
            for i in range(len(auth_providers)):
                provider = [provider.id for provider in all_providers
                            if provider.name == auth_providers[i]['provider_name'] and
                            provider.type == auth_providers[i]['provider_type']]
                if not provider:
                    error_message = 'Provider: {0} of type: {1} does not exist'.format(
                        auth_providers[i]['provider_name'], auth_providers[i]['provider_type'])
                    LOG.error(error_message)
                    self.module.fail_json(msg=error_message)
                if provider[0] not in updated_auth_providers_list:
                    add_auth_providers_required = True
                    updated_auth_providers_list.append(provider[0])
            if not add_auth_providers_required:
                return False
            update_zone = utils.isi_sdk.Zone(auth_providers=updated_auth_providers_list)
            self.api_instance.update_zone(zone=update_zone, zone_id=name)
            return True
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Add auth providers to access zone {0} ' \
                            'failed with error: {1}'.format(name, error_msg)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def remove_auth_providers_to_access_zone(self, name, auth_providers, existing_auth_providers):
        """ Remove auth providers from access zone """
        try:
            updated_auth_providers_list = existing_auth_providers
            remove_auth_providers_required = False
            provider_summary = self.api_auth.get_providers_summary()
            all_providers = provider_summary.provider_instances
            for i in range(len(auth_providers)):
                provider = [provider.id for provider in all_providers
                            if provider.name == auth_providers[i]['provider_name'] and
                            provider.type == auth_providers[i]['provider_type']]
                if not provider:
                    error_message = 'Provider: {0} of type: {1}' \
                                    ' does not exist'.format(auth_providers[i]['provider_name'], auth_providers[i]['provider_type'])
                    LOG.error(error_message)
                    self.module.fail_json(msg=error_message)
                if provider[0] in updated_auth_providers_list:
                    remove_auth_providers_required = True
                    updated_auth_providers_list.remove(provider[0])
            if not remove_auth_providers_required:
                return False
            update_zone = utils.isi_sdk.Zone(auth_providers=updated_auth_providers_list)
            self.api_instance.update_zone(zone=update_zone, zone_id=name)
            return True
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Remove auth providers to access zone {0} ' \
                            'failed with error: {1}'.format(name, error_msg)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def construct_az_params(self, az_params):
        az_params_create = {}
        az_params_create['auth_providers'] = []

        az_params_create['name'] = az_params['az_name']
        az_params_create['groupnet'] = az_params['groupnet']

        # force_overlap flag is defaulted to true,
        # since this parameter is required to be true for access zone creation.
        az_params_create['force_overlap'] = True
        az_params_create['path'] = az_params['path']

        if az_params['auth_providers']:
            for providers in az_params['auth_providers']:
                if providers['provider_type']:
                    az_params_create['auth_providers'].append(providers['provider_type'] + ":" + providers['provider_name'])
        if az_params['create_path']:
            az_params_create['create_path'] = True
        return az_params_create

    def create_access_zone(self, access_zone_params):
        try:
            self.api_instance.create_zone(access_zone_params)
            return True
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Creation of access zone %s ' \
                'failed with error: %s' % (access_zone_params['name'], error_msg)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def validate_input(self, az_params):
        if not az_params['path']:
            error_message = 'Please provide a valid path to create an access zone'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def perform_module_operation(self):
        """
        Perform different actions on access zone module based on parameters
        chosen in playbook
        """
        name = self.module.params['az_name']
        state = self.module.params['state']
        smb = self.module.params['smb']
        nfs = self.module.params['nfs']
        provider_state = self.module.params['provider_state']
        auth_providers = self.module.params['auth_providers']
        path = self.module.params['path']
        groupnet = self.module.params['groupnet']
        create_path = self.module.params['create_path']
        az_params = self.module.params

        # result is a dictionary that contains changed status and access zone
        # details
        result = dict(
            changed=False,
            smb_modify_flag=False,
            nfs_modify_flag=False,
            access_zone_modify_flag=False,
            access_zone_details=''
        )

        access_zone_details = self.get_details(name)
        if state == 'present' and provider_state == 'add' and access_zone_details:
            existing_auth_providers = access_zone_details['zones'][0]['auth_providers']
            access_zone_modify_flag = self.add_auth_providers_to_access_zone(name, auth_providers, existing_auth_providers)
            access_zone_details = self.get_details(name)
            LOG.info("added auth providers to access zone")
            result['access_zone_modify_flag'] = access_zone_modify_flag

        if state == 'present' and provider_state == 'remove' and access_zone_details:
            existing_auth_providers = access_zone_details['zones'][0]['auth_providers']
            access_zone_modify_flag = self.remove_auth_providers_to_access_zone(name, auth_providers, existing_auth_providers)
            access_zone_details = self.get_details(name)
            LOG.info("removed auth providers from access zone")
            result['access_zone_modify_flag'] = access_zone_modify_flag

        if state == 'present' and not access_zone_details:
            self.validate_input(az_params)
            access_zone_params = self.construct_az_params(az_params)
            access_zone = self.create_access_zone(access_zone_params)
            result['changed'] = access_zone
            if result['changed']:
                access_zone_details = self.get_details(name)
                result['access_zone_details'] = self.get_details(name)

        if state == 'absent' and access_zone_details:
            error_message = 'Deletion of access zone is not allowed through' \
                            ' Ansible module'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

        if state == 'present' and smb is not None:
            smb_modify_flag = self.is_smb_modification_required(
                smb, access_zone_details)
            LOG.info("SMB modification flag %s", smb_modify_flag)

            if smb_modify_flag:
                result['smb_modify_flag'] = self.smb_modify(name, smb)

        if state == 'present' and nfs is not None:
            nfs_export_flag, nfs_zone_flag = self.\
                is_nfs_modification_required(nfs, access_zone_details)
            LOG.info("NFS modification flag %s %s", nfs_export_flag,
                     nfs_zone_flag)

            if nfs_export_flag or nfs_zone_flag:
                result['nfs_modify_flag'] = self.nfs_modify(
                    name, nfs, nfs_export_flag, nfs_zone_flag)
        result['access_zone_details'] = access_zone_details
        if result['smb_modify_flag'] or result['nfs_modify_flag'] or \
                result['access_zone_modify_flag']:
            access_zone_details = self.get_details(name)
            result['access_zone_details'] = access_zone_details
            result['changed'] = True
        self.module.exit_json(**result)


def get_powerscale_accesszone_parameters():
    """This method provide parameter required for the ansible access zone
    modules on PowerScale"""
    return dict(
        az_name=dict(required=True, type='str'),
        path=dict(required=False, type='str'),
        groupnet=dict(required=False, type='str', default='groupnet0'),
        create_path=dict(required=False, type='bool'),
        smb=dict(required=False, type='dict'),
        nfs=dict(required=False, type='dict'),
        provider_state=dict(required=False, type='str', choices=['add', 'remove']),
        auth_providers=dict(required=False, type='list', elements='dict', options=dict(
            provider_name=dict(type='str', required=True),
            provider_type=dict(type='str', required=True, choices=['local', 'file', 'ldap', 'ads'])
        )),
        state=dict(required=True, type='str', choices=['present', 'absent'])
    )


def main():
    """ Create PowerScale access zone object and perform action on it
        based on user input from playbook"""
    obj = PowerScaleAccessZone()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
