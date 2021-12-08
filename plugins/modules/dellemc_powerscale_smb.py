#!/usr/bin/python
# Copyright: (c) 2019, DellEMC

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.2',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r'''
---
module: dellemc_powerscale_smb

version_added: '1.2.0'

short_description: Manage SMB shares on Dell EMC PowerScale. You can perform the following operations
description:
- Managing SMB share on PowerScale.
- Create a new SMB share.
- Modify an existing SMB share.
- Get details of an existing SMB share.
- Delete an existing SMB share.

extends_documentation_fragment:
  - dellemc.powerscale.dellemc_powerscale.powerscale

author:
- Arindam Datta (@dattaarindam) <ansible.team@dell.com>

options:
  share_name:
    description:
    - The name of the SMB share.
    type: str
    required: true
  path:
    description:
    - The path of the SMB share. This parameter will be mandatory only
      for the create operation. This is the absolute path for System Access Zone and
      the relative path for non-System Access Zone.
    type: str
  access_zone:
    description:
    - Access zone which contains this share. If not specified it will be
      considered as a System Access Zone.
    - For a non-System Access Zone the effective path where the SMB is
      created will be determined by the base path of the Access Zone and
      the path provided by the user in the playbook.
    - For a System Access Zone the effective path will be the absolute path
      provided by the user in the playbook.
    type: str
    default: 'System'
  new_share_name:
    description:
    - The new name of the SMB share.
    type: str
  description:
    description:
    - Description about the SMB share.
    type: str
  permissions:
    description:
    - Specifies permission for specific user, group, or trustee. Valid options
      read, write, and full.
    - This is a list of dictionaries. Each dictionry entry has 3
      mandatory values-
    - a)'user_name'/'group_name'/'wellknown' can have actual name of
      the trustee like 'user'/'group'/'wellknown'
    - b)'permission' can be 'read'/''write'/'full'
    - c)'permission_type' can be 'allow'/'deny'
    - The fourth entry 'provider_type' is optional (default is 'local')
    - d)'provider_type' can be 'local'/'file'/'ads'/'ldap'/'nis'
    type: list
    elements: dict
  access_based_enumeration:
    description:
    - Only enumerates files and folders for the requesting user has access to.
    type: bool
  access_based_enumeration_root_only:
    description:
    - Access-based enumeration on only the root directory of the share.
    type: bool
  browsable:
    description:
    - Share is visible in net view and the browse list.
    type: bool
  ntfs_acl_support:
    description:
    - Support NTFS ACLs on files and directories.
    type: bool
  directory_create_mask:
    description:
    - Directory creates mask bits. Octal value for owner, group, and others vs
      read, write, and execute
    type: str
  directory_create_mode:
    description:
    - Directory creates mode bits. Octal value for owner, group, and others vs
      read, write, and execute
    type: str
  file_create_mask:
    description:
    - File creates mask bits. Octal value for owner, group, and others vs
      read, write, and execute
    type: str
  file_create_mode:
    description:
    - File creates mode bits. Octal value for owner, group, and others vs
      read, write, and execute
    type: str
  state:
    description:
    - Defines whether the SMB share should exist or not.
    required: true
    type: str
    choices: [absent, present]
  '''

EXAMPLES = r'''

    - name: Create SMB share for non system access zone
      dellemc_powerscale_smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        path: "<path>"
        access_zone: "{{non_system_access_zone}}"
        state: "{{state_present}}"

    - name: Create SMB share for system access zone
      dellemc_powerscale_smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        path: "<system_az_path>"
        description: "{{description}}"
        permissions:
          - user_name: "{{system_az_user}}"
            permission: "full"
            permission_type: "allow"
          - group_name: "{{system_az_group}}"
            permission: "read"
            permission_type: "allow"
          - wellknown: "everyone"
            permission: "read"
            permission_type: "allow"
      state: "{{state_present}}"

    - name: Modify user permission for SMB share
      dellemc_powerscale_smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        path: "<system_az_path>"
        description: "{{description}}"
        permissions:
          - user_name: "{{system_az_user}}"
            permission: "full"
            permission_type: "allow"
          - group_name: "{{system_az_group}}"
            permission: "write"
            permission_type: "allow"
          - wellknown: "everyone"
            permission: "write"
            permission_type: "deny"
        state: "{{state_present}}"

    - name: Delete system access zone SMB share
      dellemc_powerscale_smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        state: "{{state_absent}}"

    - name: Get SMB share details
      dellemc_powerscale_smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        state: "{{state_present}}"

    - name: Create SMB share for non system access zone
      dellemc_powerscale_smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        path: "<non_system_az_path>"
        access_zone: "{{non_system_access_zone}}"
        description: "{{description}}"
        permissions:
          - user_name: "{{non_system_az_user}}"
            permission: "full"
            permission_type: "allow"
          - group_name: "{{non_system_az_group}}"
            permission: "read"
            permission_type: "allow"
          - wellknown: "everyone"
            permission: "read"
            permission_type: "allow"
        state: "{{state_present}}"

    - name: Modify description for an non system access zone SMB share
      dellemc_powerscale_smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        access_zone: "{{non_system_access_zone}}"
        description: "new description"
        state: "{{state_present}}"

    - name: Modify name for an existing non system access zone SMB share
      dellemc_powerscale_smb:
        onefs_host: "{{onefs_host}}"
        verify_ssl: "{{verify_ssl}}"
        api_user: "{{api_user}}"
        api_password: "{{api_password}}"
        share_name: "{{name}}"
        new_share_name: "{{new_name}}"
        access_zone: "{{non_system_access_zone}}"
        description: "new description"
        state: "{{state_present}}"
'''

RETURN = r'''

changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
smb_details:
    description: Details of the SMB Share.
    returned: always
    type: complex
    contains:
        name:
            description: Name of the SMB Share
            type: str
        id:
            description: Id of the SMB Share
            type: str
        description:
            description: Description of the SMB Share
            type: str
        path:
            description: Path of the SMB Share
            type: str
        permission:
            description: permission on the of the SMB Share for user/group/wellknown
            type: list
        file_create_mask:
            description: File create mask bit for SMB Share
            type: int
        file_create_mode:
            description: File create mode bit for SMB Share
            type: int
        directory_create_mask:
            description: Directory create mask bit for SMB Share
            type: int
        directory_create_mode:
            description: Directory create mode bit for SMB Share
            type: int
        browsable:
            description: Share is visible in net view and the browse list
            type: bool
        file_create_mask(octal):
            description: File create mask bit for SMB Share in octal format
            type: str
        file_create_mode(octal):
            description: File create mode bit for SMB Share in octal format
            type: str
        directory_create_mask(octal):
            description: Directory create mask bit for SMB Share in octal format
            type: str
        directory_create_mode(octal):
            description: Directory create mode bit for SMB Share in octal format
            type: str
'''

import re
import logging
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import dellemc_ansible_powerscale_utils as utils
from ansible.module_utils.basic import AnsibleModule

LOG = utils.get_logger('dellemc_powerscale_smb', log_devel=logging.INFO)


class PowerScaleSMB(object):
    """Class with SMB share operations"""

    def __init__(self):
        """Define all the parameters required by this module"""

        self.module_params = utils \
            .get_powerscale_management_host_parameters()
        self.module_params.update(get_powerscale_smb_parameters())

        # initialize the Ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False)

        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(
            self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        LOG.info('Got python SDK instance for provisioning on PowerScale ')
        self.protocol_api = self.isi_sdk.ProtocolsApi(
            self.api_client)
        LOG.info('Got instance for ProtocolsApi on PowerScale ')
        self.zone_summary_api = self.isi_sdk.ZonesSummaryApi(self.api_client)
        LOG.info('Got instance for ZonesSummaryApi on PowerScale ')
        self.auth_api_instance = utils.isi_sdk.AuthApi(self.api_client)
        LOG.info('Got instance for AuthApi on PowerScale')

    def get_smb_details(self, share_name, access_zone):
        """Returns details of a SMB share"""
        try:
            smb_details = self.protocol_api.get_smb_share(
                smb_share_id=share_name, resolve_names=True, zone=access_zone)
            if smb_details:
                smb_dict = smb_details.to_dict()
                LOG.info("Successfully got SMB details for %s", share_name)
                return smb_dict
            else:
                return None

        except utils.ApiException as e:
            if str(e.status) == "404":
                log_msg = "SMB Share {0} status is " \
                          "{1}".format(share_name, e.status)
                LOG.info(log_msg)
                return None
            else:
                error_message = "Failed to get details of SMB Share " \
                                "{0} with error {1} ".format(
                                    share_name,
                                    self.determine_error(e))
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

        except Exception as e:
            error_message = "Failed to get details of SMB Share {0} with" \
                " error {1} ".format(share_name, str(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_zone_base_path(self, access_zone):
        """Returns the base path of the Access Zone."""
        try:
            LOG.info("Attempting to get access zone base path for %s",
                     access_zone)
            zone_path = (self.zone_summary_api.
                         get_zones_summary_zone(access_zone)).to_dict()
            zone_base_path = zone_path['summary']['path']
            LOG.debug("Successfully got zone_base_path for %s is %s",
                      access_zone, zone_base_path)
            return zone_base_path
        except Exception as e:
            error_message = "Unable to fetch base path of Access Zone {0} ," \
                            " failed with error: {1}"\
                .format(access_zone, self.determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def create_smb_share(self):
        """Creates  a new SMB share & return the Share ID"""

        try:
            LOG.info('Attempting to create new SMB '
                     'share %s', self.module.params['share_name'])

            permissions = self.module.params['permissions']
            if permissions:
                permissions = self.make_permissions(permissions, [])
            LOG.info("create new SMB , Permissions Object : %s", permissions)

            smb_share = self.isi_sdk.SmbShareCreateParams(
                name=self.module.params['share_name'],
                path=self.module.params['path'])

            smb_share.permissions = permissions

            if self.module.params['description']:
                smb_share.description = self.module.params['description']

            if self.module.params['directory_create_mask']:
                smb_share.directory_create_mask = int(
                    self.module.params['directory_create_mask'], 8)

            if self.module.params['directory_create_mode']:
                smb_share.directory_create_mode = int(
                    self.module.params['directory_create_mode'], 8)

            if self.module.params['file_create_mask']:
                smb_share.file_create_mask = int(
                    self.module.params['file_create_mask'], 8)

            if self.module.params['file_create_mode']:
                smb_share.file_create_mode = int(
                    self.module.params['file_create_mode'], 8)

            if self.module.params['ntfs_acl_support']:
                smb_share.ntfs_acl_support = \
                    self.module.params['ntfs_acl_support']

            if self.module.params['access_based_enumeration']:
                smb_share.access_based_enumeration = \
                    self.module.params['access_based_enumeration']

            if self.module.params['access_based_enumeration_root_only']:
                smb_share.access_based_enumeration_root_only = \
                    self.module.params['access_based_enumeration_root_only']

            if self.module.params['browsable']:
                smb_share.browsable = self.module.params['browsable']

            zone = self.module.params['access_zone']

            smb_share = self.protocol_api.create_smb_share(
                smb_share, zone=zone)

            if smb_share:
                return smb_share.to_dict()
            return None

        except Exception as e:
            name = self.module.params['share_name']
            error_message = 'Failed to create SMB share {0} with ' \
                            'error: {1}'.format(name, self.determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def create_permissions_object(self, permission_names, permissions, type):
        """creating permission dict"""
        try:
            list_permissions = []
            LOG.info("Creating_permissions object")
            name_access_obj = None
            for sid in permission_names:
                if type == 'USER':
                    name_access_obj = \
                        self.isi_sdk.AuthAccessAccessItemFileGroup(id=sid)

                elif type == 'GROUP':
                    name_access_obj = \
                        self.isi_sdk.AuthAccessAccessItemFileGroup(id=sid)

                elif type == 'WELLKNOWN':
                    name_access_obj = \
                        self.isi_sdk.AuthAccessAccessItemFileGroup(
                            name=sid, type="wellknown")

                if permissions[sid]['permission'] == 'write':
                    permission = 'change'
                else:
                    permission = permissions[sid]['permission']

                share = utils.isi_sdk.SmbSharePermission(
                    permission=permission,
                    permission_type=permissions[sid]['permission_type'],
                    trustee=name_access_obj)

                list_permissions.append(share)

            LOG.info("Exit create_permissions list_permissions : %s",
                     list_permissions)

            return list_permissions

        except Exception as e:

            err_msg = "Creating permission dict failed with " \
                      "error {0}".format(self.determine_error(e))
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)

    def make_permissions(self, module_params_permissions, smb_permissions):
        """Compare permission dict & return only the changed"""

        try:
            LOG.info("making permissions")
            user_smb_permissions, group_smb_permissions, \
                wellknown_smb_permissions = self.get_smb_permissions_dict(
                    smb_permissions)

            user_params_permissions, group_params_permissions, \
                wellknown_params_permissions = \
                self.get_module_params_permissions_dict(
                    module_params_permissions)

            common_users = set(user_smb_permissions.keys()) \
                .intersection(user_params_permissions.keys())
            common_groups = set(group_smb_permissions.keys()) \
                .intersection(group_params_permissions.keys())
            common_wellknowns = set(wellknown_smb_permissions.keys()) \
                .intersection(wellknown_params_permissions.keys())

            new_users = set(user_params_permissions) - set(
                user_smb_permissions)

            new_groups = set(group_params_permissions) - set(
                group_smb_permissions)

            new_wellknowns = set(wellknown_params_permissions) - set(
                wellknown_smb_permissions)

            remaining_users = set(user_smb_permissions) - set(
                user_params_permissions)
            remaining_groups = set(group_smb_permissions) - set(
                group_params_permissions)
            remaining_wellknowns = set(wellknown_smb_permissions) - set(
                wellknown_params_permissions)

            list_permissions = []

            if common_users is not None:
                list_permissions.append(self.create_permissions_object(
                    common_users, user_params_permissions, 'USER'))

            if new_users is not None:
                list_permissions.append(
                    self.create_permissions_object(
                        new_users, user_params_permissions, 'USER'))

            if remaining_users is not None:
                list_permissions.append(
                    self.create_permissions_object(
                        remaining_users, user_smb_permissions, 'USER'))

            if common_groups is not None:
                list_permissions.append(self.create_permissions_object(
                    common_groups, group_params_permissions, 'GROUP'))

            if new_groups is not None:
                list_permissions.append(self.create_permissions_object(
                    new_groups, group_params_permissions, 'GROUP'))

            if remaining_groups is not None:
                list_permissions.append(
                    self.create_permissions_object(
                        remaining_groups, group_smb_permissions, 'GROUP'))

            if common_wellknowns is not None:
                list_permissions.append(
                    self.create_permissions_object(
                        common_wellknowns, wellknown_params_permissions,
                        'WELLKNOWN'))

            if new_wellknowns is not None:
                list_permissions.append(
                    self.create_permissions_object(
                        new_wellknowns, wellknown_params_permissions,
                        'WELLKNOWN'))

            if remaining_wellknowns is not None:
                list_permissions.append(
                    self.create_permissions_object(
                        remaining_wellknowns, wellknown_smb_permissions,
                        'WELLKNOWN'))

            flat_list_permissions = \
                [item for sublist in list_permissions for item in sublist]
            return flat_list_permissions

        except Exception as e:
            error_message = 'Failed to make_permission with ' \
                            'error: {0}'.format(self.determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_smb_params_from_details(self, smb_details):
        """Creating SMB params dict only with the parameters used in our
        module for better readability & passing it to other methods"""
        try:
            LOG.info("Creating SMB Dictionary")
            smb_params = {
                'name': smb_details['name'],
                'path': smb_details['path'],
                'permissions': smb_details['permissions'],
                'description': smb_details['description'],
                'directory_create_mask': smb_details['directory_create_mask'],
                'directory_create_mode': smb_details['directory_create_mode'],
                'file_create_mask': smb_details['file_create_mask'],
                'file_create_mode': smb_details['file_create_mode'],
                'ntfs_acl_support': smb_details['ntfs_acl_support'],
                'access_based_enumeration':
                    smb_details['access_based_enumeration'],
                'access_based_enumeration_root_only':
                    smb_details['access_based_enumeration_root_only'],
                'browsable': smb_details['browsable']
            }

            return smb_params
        except Exception as e:

            error_message = 'Failed to get SMB params from details' \
                            ' with error: {0}'.format(self.determine_error(e))
            LOG.error(error_message)
            return None

    def get_smb_permissions_dict(self, permissions):
        """Creates a Dict with SMB Permission from permission object"""
        try:
            LOG.info("Creating Permission Dictionary")
            users_permissions = {}
            groups_permissions = {}
            wellknown_permissions = {}
            for smb_permission in permissions:
                temp_permission = {
                    'permission_type': smb_permission['permission_type'],
                    'permission': smb_permission['permission']}
                sid = smb_permission['trustee']['id']

                if smb_permission['trustee']['type'] == 'user':
                    users_permissions[sid] = temp_permission
                elif smb_permission['trustee']['type'] == 'group':
                    groups_permissions[sid] = temp_permission
                elif smb_permission['trustee']['type'] == 'wellknown':
                    wellknown_name = smb_permission['trustee']['name'].lower()
                    wellknown_permissions[wellknown_name] = temp_permission

            LOG.info("smb_permissions_dict created, user: %s , group: %s,"
                     " wellknown: %s ", users_permissions, groups_permissions,
                     wellknown_permissions)

            return users_permissions, groups_permissions, \
                wellknown_permissions

        except Exception as e:
            error_message = 'Failed get_smb permissions dictionary ' \
                            'with error: {0}'.format(self.determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_sid(self, name, type, provider):
        """Get the User Account Details in PowerScale"""
        try:
            zone = self.module.params['access_zone']
            if type == 'USER':
                api_response = self.auth_api_instance.get_auth_user(
                    auth_user_id='USER:' + name,
                    zone=zone, provider=provider)
                return api_response.users[0].sid.id
            elif type == 'GROUP':
                api_response = self.auth_api_instance.get_auth_group(
                    auth_group_id='GROUP:' + name, zone=zone,
                    provider=provider)
                return api_response.groups[0].sid.id
        except Exception as e:
            error_message = "Failed to get {0}:{1} details for " \
                            "AccessZone:{2} and Provider:{3} " \
                            "with error {4}".format(
                                type,
                                name,
                                self.module.params['access_zone'],
                                provider,
                                self.determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_module_params_permissions_dict(self, permissions):
        """Creates a Dict with SMB Permission from module parameter"""
        try:
            users_permissions = {}
            groups_permissions = {}
            wellknown_permissions = {}
            for smb_permission in permissions:
                temp_permission = {
                    'permission': smb_permission['permission'],
                    'permission_type': smb_permission['permission_type']}
                if 'user_name' in smb_permission:
                    sid = self.get_sid(smb_permission['user_name'],
                                       'USER',
                                       smb_permission['provider_type'])
                    users_permissions[sid] = temp_permission

                elif 'group_name' in smb_permission:
                    sid = self.get_sid(smb_permission['group_name'],
                                       'GROUP',
                                       smb_permission['provider_type'])
                    groups_permissions[sid] = temp_permission

                elif 'wellknown' in smb_permission:
                    wellknown_name = smb_permission['wellknown'].lower()
                    wellknown_permissions[wellknown_name] = temp_permission

            LOG.info(
                "module_params_permissions_dict created, user: %s"
                " , group: %s, wellknown: %s", users_permissions,
                groups_permissions, wellknown_permissions)

            return users_permissions, \
                groups_permissions, wellknown_permissions

        except Exception as e:
            error_message = 'Failed get module params ' \
                            'permissions dict with error: ' \
                            '{0}'.format(self.determine_error(e))
            LOG.error(error_message)
            return None, None, None

    def is_permission_modified(self, smb_params_permissions):
        """checking if the permission is changed"""
        try:
            LOG.info("Checking if permission_modified")
            user_permissions, group_permissions, wellknown_permissions = \
                self.get_smb_permissions_dict(smb_params_permissions)
            for params_permission in self.module.params['permissions']:

                # workaround to map "write" to "change"
                if params_permission['permission'].lower() == "write":
                    params_permission['permission'] = "change"

                if 'user_name' in params_permission:
                    user_sid = self.get_sid(
                        params_permission['user_name'], 'USER',
                        params_permission['provider_type'])

                    if user_sid in user_permissions.keys():
                        permission_type = \
                            params_permission['permission_type'].lower()

                        permission = params_permission['permission'].lower()

                        if permission_type != \
                                user_permissions[user_sid][
                                    'permission_type']:

                            return True
                        if permission != \
                                user_permissions[user_sid]['permission']:
                            return True
                    else:
                        return True
                elif 'group_name' in params_permission:
                    group_sid = self.get_sid(
                        params_permission['group_name'], 'GROUP',

                        params_permission['provider_type'])

                    if group_sid in group_permissions.keys():
                        permission_type = params_permission[
                            'permission_type'].lower()
                        permission = params_permission['permission'].lower()
                        if permission_type != \
                                group_permissions[group_sid][
                                    'permission_type']:
                            return True
                        if permission != \
                                group_permissions[group_sid]['permission']:
                            return True
                    else:
                        return True

                elif 'wellknown' in params_permission:
                    wellknown = params_permission['wellknown'].lower()
                    if wellknown in wellknown_permissions.keys():
                        permission_type = params_permission[
                            'permission_type'].lower()
                        permission = params_permission['permission'].lower()
                        if permission_type != \
                                wellknown_permissions[
                                    wellknown]['permission_type']:
                            return True
                        if permission != \
                                wellknown_permissions[wellknown][
                                    'permission']:
                            return True
                    else:
                        return True

            return False
        except Exception as e:
            error_message = 'Failed to validate if permission modified' \
                            ' with error {0}'.format(self.determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def is_smb_modified(self, smb_params):
        """Checking if SMB attribute has changed & if modification required"""
        try:

            LOG.debug("is_smb_modified called with "
                      "params: %s", smb_params)

            if self.module.params['permissions'] and \
                    self.is_permission_modified(smb_params['permissions']):
                return True

            if self.module.params['new_share_name'] \
                    and (self.module.params['new_share_name'].lower()
                         != smb_params['name'].lower()):
                return True

            if self.module.params['path'] and\
                    self.module.params['path'] != smb_params['path']:
                error_message = "Modifying path for a SMB Share is not " \
                                "allowed through Ansible Module"
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

            if self.module.params['description'] and \
                    self.module.params['description'] != \
                    smb_params['description']:
                return True

            if self.module.params['ntfs_acl_support'] and \
                    self.module.params['ntfs_acl_support'] != \
                    smb_params['ntfs_acl_support']:
                return True

            if self.module.params['access_based_enumeration'] and \
                    self.module.params['access_based_enumeration']\
                    != smb_params['access_based_enumeration']:
                return True

            if self.module.params['access_based_enumeration_root_only'] and\
                    self.module.params[
                        'access_based_enumeration_root_only'] != \
                    smb_params['access_based_enumeration_root_only']:
                return True

            if self.module.params['browsable'] and \
                    self.module.params['browsable'] != \
                    smb_params['browsable']:
                return True

            if self.module.params['directory_create_mask'] and \
                    int(self.module.params['directory_create_mask'], 8) != \
                    smb_params['directory_create_mask']:
                return True

            if self.module.params['directory_create_mode'] and \
                    int(self.module.params['directory_create_mode'], 8) != \
                    smb_params['directory_create_mode']:
                return True

            if self.module.params['file_create_mask'] and \
                    int(self.module.params['file_create_mask'], 8) != \
                    smb_params['file_create_mask']:
                return True

            if self.module.params['file_create_mode'] and \
                    int(self.module.params['file_create_mode'], 8) != \
                    smb_params['file_create_mode']:
                return True

            LOG.info("modify not required")
            return False

        except Exception as e:
            error_message = 'Failed to determine if any modification' \
                            ' required for SMB attributes with error: ' \
                            '{0}'.format(self.determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def update_smb_details(self, smb_share_id, smb_details):
        """Updating SMB attributes"""
        try:

            LOG.debug("updating SMB: %s details with : %s ", smb_share_id,
                      smb_details)
            if self.module.params['permissions'] is not None:

                permissions = self.make_permissions(
                    self.module.params['permissions'],
                    smb_details['permissions'])
            else:
                permissions = None

            smb_share = self.isi_sdk.SmbShare(
                permissions=permissions,
                description=self.module.params['description'],
                ntfs_acl_support=self.module.params['ntfs_acl_support'],
                access_based_enumeration=self.module.params[
                    'access_based_enumeration'],
                access_based_enumeration_root_only=self.module.params[
                    'access_based_enumeration_root_only'],
                browsable=self.module.params['browsable'],
                name=self.module.params['new_share_name'])

            if self.module.params['directory_create_mask']:
                smb_share.directory_create_mask = \
                    int(self.module.params['directory_create_mask'], 8)
            if self.module.params['directory_create_mode']:
                smb_share.directory_create_mode = \
                    int(self.module.params['directory_create_mode'], 8)
            if self.module.params['file_create_mask']:
                smb_share.file_create_mask = \
                    int(self.module.params['file_create_mask'], 8)
            if self.module.params['file_create_mode']:
                smb_share.file_create_mode = \
                    int(self.module.params['file_create_mode'], 8)

            smb_share_id = self.module.params['share_name']

            self.protocol_api.update_smb_share(
                smb_share, smb_share_id,
                zone=self.module.params['access_zone'])

        except Exception as e:
            error_message = "Failed to update the SMB share: {0} with " \
                            "error: {1}".format(smb_share_id,
                                                self.determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete_smb_share(self):
        """Deletes a SMB share"""
        smb_share_id = self.module.params['share_name']
        zone = self.module.params['access_zone']
        try:
            self.protocol_api.delete_smb_share(
                smb_share_id, zone=zone)
            return True
        except Exception as e:
            error_message = 'Failed to delete a SMB share: ' \
                            '{0} with error: ' \
                            '{1}'.format(smb_share_id,
                                         self.determine_error(e))

            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def validate_permission_dict(self):
        """Validate permission and add default provider_type """
        permissions = self.module.params['permissions']
        for i in range(len(permissions)):
            if "user_name" in permissions[i] and not (
                    "provider_type" in permissions[i].keys()):
                self.module.params['permissions'][i][
                    'provider_type'] = 'local'
            if "group_name" in permissions[i] and not (
                    "provider_type" in permissions[i].keys()):
                self.module.params['permissions'][i][
                    'provider_type'] = 'local'
            if "wellknown" in permissions[i] and (
                    "provider_type" in permissions[i].keys()):
                LOG.warn("'provider_type' for wellknown will be ignored")

        LOG.info("Default provider_type added to permission  : %s",
                 self.module.params['permissions'])

    def determine_error(self, error_obj):
        """Format the error object"""
        if isinstance(error_obj, utils.ApiException):
            error = re.sub("[\n \"]+", " ", str(error_obj.body))
        else:
            error = str(error_obj)
        return error

    def perform_module_operation(self):
        """
        Perform different actions on SMB share based on user
        parameter provided in the playbook
        """

        share_name = self.module.params['share_name']
        path = self.module.params['path']
        access_zone = self.module.params['access_zone']
        state = self.module.params['state']
        new_share_name = self.module.params['new_share_name']
        permissions = self.module.params['permissions']

        result = {'changed': False,
                  'smb_details': None}

        if (not share_name) or ' ' in share_name:
            error_message = "Invalid share name {0}".format(share_name)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

        if access_zone and path:
            effective_path = path
            if access_zone.lower() == "system":
                if not path.startswith('/'):
                    err_msg = "Invalid path {0}, Path must start " \
                              "with '/'".format(path)
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)
            else:
                if not path.startswith('/'):
                    path = "/{0}".format(path)
                effective_path = self.get_zone_base_path(
                    access_zone) + path
            path = effective_path
            self.module.params['path'] = effective_path

        if permissions:
            self.validate_permission_dict()

        smb_details = self.get_smb_details(share_name, access_zone)

        LOG.debug('SMB Details with unmodified mode/mask '
                  'bits : %s', smb_details)
        to_modify = False

        if smb_details:
            smb_params = self.get_smb_params_from_details(
                smb_details['shares'][0])
            to_modify = self.is_smb_modified(smb_params)
            LOG.info("To modify check: %s", str(to_modify))

        if state == 'present' and not smb_details:
            LOG.info("Creating new SMB share %s", share_name)
            if not path or path == '' or ' ' in path:
                self.module.fail_json(msg="Invalid path.Valid path is "
                                          "required to create a smb share ")
            smb_details = self.create_smb_share()
            if smb_details:
                share_name = smb_details['id']
                smb_details = self.get_smb_details(share_name, access_zone)
                result['changed'] = True

        if state == 'absent' and smb_details:
            LOG.info("Deleting SMB share %s", share_name)
            self.delete_smb_share()
            result['changed'] = True
            smb_details = None

        if state == 'present' and smb_details and to_modify:
            LOG.info("Modify SMB share the details")
            self.update_smb_details(share_name, smb_params)
            if new_share_name:
                smb_details = self.get_smb_details(
                    new_share_name, access_zone)
            else:
                smb_details = self.get_smb_details(
                    share_name, access_zone)
            share_name = smb_details['shares'][0]['name']
            result['changed'] = True

        if state == 'present' and smb_details:
            LOG.info('Getting Details for SMB : %s : ', share_name)

            smb_details['shares'][0]['directory_create_mask(octal)'] = \
                "{0:o}".format(smb_details['shares'][0]
                               ['directory_create_mask'])
            smb_details['shares'][0]['directory_create_mode(octal)'] = \
                "{0:o}".format(smb_details['shares'][0]
                               ['directory_create_mode'])
            smb_details['shares'][0]['file_create_mask(octal)'] = \
                "{0:o}".format(smb_details['shares'][0]
                               ['file_create_mask'])
            smb_details['shares'][0]['file_create_mode(octal)'] = \
                "{0:o}".format(smb_details['shares'][0]
                               ['file_create_mode'])

            LOG.debug('SMB Details : %s ', smb_details)
            result['smb_details'] = smb_details

        self.module.exit_json(**result)


def get_powerscale_smb_parameters():
    return dict(
        share_name=dict(required=True, type='str'),
        path=dict(type='str', no_log=True),
        access_zone=dict(type='str', default='System'),
        description=dict(type='str'),
        permissions=dict(type='list', elements='dict'),
        state=dict(required=True, type='str', choices=['present', 'absent']),
        new_share_name=dict(type='str'),
        access_based_enumeration=dict(type='bool'),
        access_based_enumeration_root_only=dict(type='bool'),
        browsable=dict(type='bool'),
        ntfs_acl_support=dict(type='bool'),
        directory_create_mask=dict(type='str'),
        directory_create_mode=dict(type='str'),
        file_create_mask=dict(type='str'),
        file_create_mode=dict(type='str'),
    )


def main():
    """Create PowerScale Smb object and perform action on it
        based on user input from playbook"""
    obj = PowerScaleSMB()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
