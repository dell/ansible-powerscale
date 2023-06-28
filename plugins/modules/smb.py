#!/usr/bin/python
# Copyright: (c) 2019, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

""" Ansible module for managing SMB shares on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: smb

version_added: '1.2.0'

short_description: Manage SMB shares on PowerScale Storage System. You can perform these operations
description:
- Managing SMB share on PowerScale.
- Create a new SMB share.
- Modify an existing SMB share.
- Get details of an existing SMB share.
- Delete an existing SMB share.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Arindam Datta (@dattaarindam) <ansible.team@dell.com>
- Trisha Datta (@Trisha-Datta) <ansible.team@dell.com>

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
    - Description of the SMB share.
    type: str
  permissions:
    description:
    - Specifies permission for specific user, group, or trustee. Valid options
      read, write, and full.
    - This is a list of dictionaries. Each dictionry entry has 3
      mandatory values as listed below.
    - 1)I(user_name)/I(group_name)/I(wellknown) can have actual name of
      the trustee like C(user)/C(group)/C(wellknown).
    - 2)I(permission) can be C(read)/'C(write)/C(full).
    - 3)I(permission_type) can be C(allow)/C(deny).
    - The fourth entry I(provider_type) is optional (default is C(local)).
    - 4)I(provider_type) can be C(local)/C(file)/C(ads)/C(ldap)/C(nis).
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
    - Directory creates mask bits. Octal value for owner, group, and others against
      read, write, and execute.
    type: str
  directory_create_mode:
    description:
    - Directory creates mode bits. Octal value for owner, group, and others against
      read, write, and execute.
    type: str
  file_create_mask:
    description:
    - File creates mask bits. Octal value for owner, group, and others against
      read, write, and execute.
    type: str
  file_create_mode:
    description:
    - File creates mode bits. Octal value for owner, group, and others against
      read, write, and execute.
    type: str
  create_path:
    description:
    - Create path if does not exist.
    type: bool
  allow_variable_expansion:
    description:
    - Allow automatic expansion of variables for home directories.
    type: bool
  auto_create_directory:
    description:
    - Automatically create home directories.
    type: bool
  continuously_available:
    description:
    - Specify if persistent opens are allowed on the share.
    type: bool
  file_filter_extension:
    description:
    - Details of file filter extensions.
    type: dict
    suboptions:
      extensions:
        description:
        - Specifies the list of file extensions.
        type: list
        elements: str
      type:
        description:
        - Specifies if filter list is for C(deny) or C(allow). Default is C(deny).
        type: str
        default: "deny"
        choices: [allow, deny]
      state:
        description:
        - State of the file filter extensions.
        type: str
        choices: [present-in-share, absent-in-share]
  file_filtering_enabled:
    description:
    - Enables file filtering on this zone.
    type: bool
  ca_timeout:
    description:
    - Continuosly available timeout for the SMB share.
    type: dict
    suboptions:
      value:
        description:
        - Persistent open timeout for the share.
        type: int
      unit:
        description:
        - Unit of the I(ca_timeout).
        type: str
        choices: [seconds, minutes, hours]
        default: "seconds"
  strict_ca_lockout:
    description:
    - Specifies if persistent opens would do strict lockout on the share.
    type: bool
  smb3_encryption_enabled:
    description:
    - Enables SMB3 encryption for the share.
    type: bool
  ca_write_integrity:
    description:
    - Specify the level of write-integrity on continuously available shares.
    type: str
    choices: [none, full, write-read-coherent]
  change_notify:
    description:
    - Level of change notification alerts on the share.
    type: str
    choices: [all, norecurse, none]
  oplocks:
    description:
    - Support oplocks.
    type: bool
  impersonate_guest:
    description:
    - Specify the condition in which user access is done as the guest account.
    type: str
    choices: [always, never, bad_user]
  impersonate_user:
    description:
    - User account to be used as guest account.
    type: str
  host_acls:
    description:
    - An ACL expressing which hosts are allowed access. A deny clause must be the final entry.
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Name of the host ACL.
        type: str
        required: true
      access_type:
        description:
        - The access type of the host ACL.
        type: str
        required: true
  state:
    description:
    - Defines whether the SMB share should exist or not.
    required: true
    type: str
    choices: [absent, present]

notes:
- The I(check_mode) is not supported.
'''

EXAMPLES = r'''
- name: Create SMB share for non system access zone
  dellemc.powerscale.smb:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    share_name: "{{name}}"
    path: "<path>"
    access_zone: "{{non_system_access_zone}}"
    state: "present"

- name: Create SMB share for system access zone
  dellemc.powerscale.smb:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    share_name: "{{name}}"
    path: "{{system_az_path}}"
    description: "{{description}}"
    create_path: false
    allow_variable_expansion: true
    auto_create_directory: true
    continuously_available: true
    file_filter_extension:
      extensions:
        - "sample_extension_1"
      type: "allow"
      state: "present-in-share"
    file_filtering_enabled: true
    ca_timeout:
      value: 60
      unit: "minutes"
    strict_ca_lockout: true
    smb3_encryption_enabled: true
    ca_write_integrity: "write-read-coherent"
    change_notify: "all"
    oplocks: true
    impersonate_guest: "never"
    impersonate_user: "sample_user"
    host_acls:
    - name: "sample_host_acl_1"
      access_type: "allow"
    - name: "sample_host_acl_2"
      access_type: "deny"
    state: "present"

- name: Create SMB share for system access zone
  dellemc.powerscale.smb:
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
    state: "present"

- name: Modify multiple params for an existing  SMB share
  dellemc.powerscale.smb:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    share_name: "{{name}}"
    path: "/ifs"
    allow_variable_expansion: false
    auto_create_directory: false
    file_filter_extension:
      extensions:
        - 'sample_extension_2'
      type: "allow"
      state: "absent-in-share"
    file_filtering_enabled: true
    ca_timeout:
      value: 15
      unit: "minutes"
    strict_ca_lockout: false
    change_notify: "norecurse"
    oplocks: false
    impersonate_guest: "always"
    impersonate_user: "new_user_2"
    host_acls:
      - name: "sample_host_acl_1"
        access_type: "deny"
      - name: "sample_host_acl_2"
        access_type: "allow"
    state: "present"

- name: Modify user permission for SMB share
  dellemc.powerscale.smb:
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
    state: "present"

- name: Delete system access zone SMB share
  dellemc.powerscale.smb:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    share_name: "{{name}}"
    state: "absent"

- name: Get SMB share details
  dellemc.powerscale.smb:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    share_name: "{{name}}"
    state: "present"

- name: Create SMB share for non system access zone
  dellemc.powerscale.smb:
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
    state: "present"

- name: Modify description for an non system access zone SMB share
  dellemc.powerscale.smb:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    share_name: "{{name}}"
    access_zone: "{{non_system_access_zone}}"
    description: "new description"
    state: "present"

- name: Modify name for an existing non system access zone SMB share
  dellemc.powerscale.smb:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    share_name: "{{name}}"
    new_share_name: "{{new_name}}"
    access_zone: "{{non_system_access_zone}}"
    description: "new description"
    state: "present"
'''

RETURN = r'''

changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
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
    sample: {
        "shares": [
            {
                "access_based_enumeration": false,
                "access_based_enumeration_root_only": false,
                "allow_delete_readonly": false,
                "allow_execute_always": false,
                "allow_variable_expansion": false,
                "auto_create_directory": false,
                "browsable": true,
                "ca_timeout": 900,
                "ca_write_integrity": "write-read-coherent",
                "change_notify": "norecurse",
                "continuously_available": true,
                "create_permissions": "default acl",
                "csc_policy": "manual",
                "description": "smb description updated",
                "directory_create_mask": 448,
                "directory_create_mask(octal)": "700",
                "directory_create_mode": 0,
                "directory_create_mode(octal)": "0",
                "file_create_mask": 448,
                "file_create_mask(octal)": "700",
                "file_create_mode": 64,
                "file_create_mode(octal)": "100",
                "file_filter_extensions": [
                    "sample_extension_1"
                ],
                "file_filter_type": "allow",
                "file_filtering_enabled": true,
                "hide_dot_files": false,
                "host_acl": [
                    "deny: sample_host_acl_1",
                    "allow: sample_host_acl_2"
                ],
                "id": "test_sample_smb",
                "impersonate_guest": "always",
                "impersonate_user": "new_user_2",
                "inheritable_path_acl": false,
                "mangle_byte_start": 60672,
                "mangle_map": [
                    "0x01-0x1F:-1",
                    "0x22:-1",
                    "0x2A:-1",
                    "0x3A:-1",
                    "0x3C:-1",
                    "0x3E:-1",
                    "0x3F:-1",
                    "0x5C:-1"
                ],
                "name": "test_sample_smb",
                "ntfs_acl_support": true,
                "oplocks": false,
                "path": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
                "permissions": [
                    {
                        "permission": "read",
                        "permission_type": "allow",
                        "trustee": {
                            "id": "SID:S-1-1-0",
                            "name": "Everyone",
                            "type": "wellknown"
                        }
                    }
                ],
                "run_as_root": [],
                "smb3_encryption_enabled": false,
                "sparse_file": false,
                "strict_ca_lockout": false,
                "strict_flush": true,
                "strict_locking": false,
                "zid": 1
            }
        ]
    }


'''

from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
from ansible.module_utils.basic import AnsibleModule

LOG = utils.get_logger('smb')


class SMB(object):
    """Class with SMB share operations"""

    def __init__(self):
        """Define all the parameters required by this module"""

        self.module_params = utils \
            .get_powerscale_management_host_parameters()
        self.module_params.update(get_smb_parameters())

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
                                "{0} with error {1} ".format(share_name,
                                                             utils.determine_error(e))
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
                            " failed with error: {1}" \
                .format(access_zone, utils.determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def ca_timeout_value(self):
        if self.module.params['ca_timeout']:
            if self.module.params['ca_timeout']['unit']:
                ca_timeout_value = utils.get_time_in_seconds(self.module.params['ca_timeout']['value'],
                                                             self.module.params['ca_timeout']['unit'])
            else:
                ca_timeout_value = self.module.params['ca_timeout']['value']
            return ca_timeout_value
        return None

    def file_filter_details(self):
        file_filter_extensions_list = []
        file_filter_type = "deny"
        file_filtering_enabled = False
        if self.module.params['file_filter_extension']:
            if self.module.params['file_filter_extension']['extensions'] and \
                    self.module.params['file_filter_extension']['state'] == "present-in-share":
                file_filter_extensions_list = \
                    self.module.params['file_filter_extension']['extensions']
            if self.module.params['file_filter_extension']['type']:
                file_filter_type = \
                    self.module.params['file_filter_extension']['type']
        if self.module.params['file_filtering_enabled']:
            file_filtering_enabled = \
                self.module.params['file_filtering_enabled']
        return file_filter_extensions_list, file_filter_type, file_filtering_enabled

    def octal_param_update(self, smb_share):
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

        return smb_share

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

            smb_share = self.octal_param_update(smb_share)

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

            if self.module.params['create_path']:
                smb_share.create_path = self.module.params['create_path']

            if self.module.params['allow_variable_expansion']:
                smb_share.allow_variable_expansion = \
                    self.module.params['allow_variable_expansion']

            if self.module.params['auto_create_directory']:
                smb_share.auto_create_directory = \
                    self.module.params['auto_create_directory']

            if self.module.params['continuously_available']:
                smb_share.continuously_available = \
                    self.module.params['continuously_available']

            if self.module.params['strict_ca_lockout']:
                smb_share.strict_ca_lockout = \
                    self.module.params['strict_ca_lockout']

            if self.module.params['change_notify']:
                smb_share.change_notify = self.module.params['change_notify']

            if self.module.params['oplocks']:
                smb_share.oplocks = self.module.params['oplocks']

            if self.module.params['impersonate_guest']:
                smb_share.impersonate_guest = \
                    self.module.params['impersonate_guest']

            if self.module.params['impersonate_user']:
                smb_share.impersonate_user = \
                    self.module.params['impersonate_user']

            if self.module.params['smb3_encryption_enabled']:
                smb_share.smb3_encryption_enabled = \
                    self.module.params['smb3_encryption_enabled']

            if self.module.params['ca_write_integrity']:
                smb_share.ca_write_integrity = \
                    self.module.params['ca_write_integrity']

            if self.module.params['host_acls']:
                host_acl_list = []
                for host_acl in self.module.params['host_acls']:
                    host_acl_list.append(host_acl['access_type'] + ": " + host_acl['name'])
                smb_share.host_acl = host_acl_list

            smb_share.file_filter_extensions, smb_share.file_filter_type, \
                smb_share.file_filtering_enabled = self.file_filter_details()

            if self.module.params['ca_timeout']:
                smb_share.ca_timeout = self.ca_timeout_value()

            zone = self.module.params['access_zone']

            smb_share = self.protocol_api.create_smb_share(
                smb_share, zone=zone)

            if smb_share:
                return smb_share.to_dict()
            return None

        except Exception as e:
            name = self.module.params['share_name']
            error_message = 'Failed to create SMB share {0} with ' \
                            'error: {1}'.format(name, utils.determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def create_permissions_object(self, permission_names, permissions, type):
        """creating permission dict"""
        try:
            list_permissions = []
            LOG.info("Creating_permissions object")
            name_access_obj = None
            for sid in permission_names:
                if type == 'USER' or type == 'GROUP':
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
                      "error {0}".format(utils.determine_error(e))
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)

    def make_permissions(self, module_params_permissions, smb_permissions):
        """Compare permission dict & return only the changed"""

        try:
            LOG.info("making permissions")
            user_smb_permissions, group_smb_permissions, \
                wellknown_smb_permissions = self.get_smb_permissions_dict(smb_permissions)

            user_params_permissions, group_params_permissions, \
                wellknown_params_permissions = \
                self.get_module_params_permissions_dict(module_params_permissions)

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

            list_permissions.append(self.create_permissions_object(
                common_groups, group_params_permissions, 'GROUP'))

            if new_groups is not None:
                list_permissions.append(self.create_permissions_object(
                    new_groups, group_params_permissions, 'GROUP'))

            if remaining_groups is not None:
                list_permissions.append(
                    self.create_permissions_object(
                        remaining_groups, group_smb_permissions, 'GROUP'))

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
                            'error: {0}'.format(utils.determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_smb_params_from_details(self, smb_details):
        """Creating SMB params dict only with the parameters used in our
        module for better readability & passing it to other methods"""
        try:
            LOG.info("Creating SMB Dictionary")
            params = ['allow_variable_expansion', 'auto_create_directory', 'continuously_available',
                      'file_filter_extensions', 'file_filter_type', 'file_filtering_enabled', 'strict_ca_lockout',
                      'ca_timeout', 'change_notify', 'oplocks', 'impersonate_guest', 'impersonate_user', 'host_acl',
                      'smb3_encryption_enabled', 'ca_write_integrity']

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

            for param in params:
                smb_params[param] = smb_details[param]

            return smb_params
        except Exception as e:

            error_message = 'Failed to get SMB params from details' \
                            ' with error: {0}'.format(utils.determine_error(e))
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
                            'with error: {0}'.format(utils.determine_error(e))
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
                            "with error {4}".format(type, name,
                                                    self.module.params['access_zone'],
                                                    provider, utils.determine_error(e))
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
                            '{0}'.format(utils.determine_error(e))
            LOG.error(error_message)
            return None, None, None

    def is_permission_modified(self, smb_params_permissions):
        """checking if the permission is changed"""
        try:
            LOG.info("Checking if permission is modified")
            user_permissions, group_permissions, wellknown_permissions = \
                self.get_smb_permissions_dict(smb_params_permissions)
            for params_permission in self.module.params['permissions']:

                # workaround to map "write" to "change"
                if params_permission['permission'].lower() == "write":
                    params_permission['permission'] = "change"

                permission_type_list = ['user', 'group', 'wellknown']
                permission_list = [user_permissions, group_permissions, wellknown_permissions]
                for index in range(len(permission_type_list)):
                    if permission_type_list[index] + '_name' in params_permission:
                        sid = self.get_sid(
                            params_permission[permission_type_list[index] + '_name'],
                            permission_type_list[index].upper(),
                            params_permission['provider_type'])
                        if sid in permission_list[index].keys():
                            permission_type = \
                                params_permission['permission_type'].lower()

                            permission = params_permission['permission'].lower()

                            if permission_type != \
                                    permission_list[index][sid]['permission_type']:
                                return True
                            if permission != \
                                    permission_list[index][sid]['permission']:
                                return True
                        else:
                            return True
            return False
        except Exception as e:
            error_message = 'Failed to validate if permission modified' \
                            ' with error {0}'.format(utils.determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def file_filter_param_validation(self):

        if self.module.params['file_filter_extension'] is not None and \
                (not self.module.params['file_filter_extension']['state'] or
                 not self.module.params['file_filter_extension']['extensions']):
            error_message = "extensions and state are required together when file_filter_extension" \
                            " is mentioned."
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def is_smb_modified(self, smb_params):
        """Checking if SMB attribute has changed & if modification required"""
        try:

            LOG.debug("is_smb_modified called with "
                      "params: %s", smb_params)

            if self.module.params['new_share_name'] \
                    and (self.module.params['new_share_name'].lower()
                         != smb_params['name'].lower()):
                return True

            smb_share_mask_mode_bit_params = ['directory_create_mask', 'directory_create_mode', 'file_create_mask',
                                              'file_create_mode']

            for param in smb_share_mask_mode_bit_params:
                if self.module.params[param] and \
                        int(self.module.params[param], 8) != \
                        smb_params[param]:
                    return True

            modify_list = []
            if self.module.params['file_filter_extension']:
                if self.module.params['file_filter_extension']['state'] == "present-in-share":
                    modify_list = set(list(smb_params['file_filter_extensions']) + list(
                        self.module.params['file_filter_extension']['extensions']))

                elif self.module.params['file_filter_extension']['state'] == "absent-in-share":
                    modify_list = set(list(smb_params['file_filter_extensions'])) - set(
                        list(self.module.params['file_filter_extension']['extensions']))

            if self.module.params['file_filter_extension'] and set(modify_list) != set(
                    smb_params['file_filter_extensions']):
                return True

            if self.module.params['ca_timeout'] and smb_params['ca_timeout'] != self.ca_timeout_value():
                return True

            if self.module.params['permissions'] and \
                    self.is_permission_modified(smb_params['permissions']):
                return True

            if self.module.params['path'] and \
                    self.module.params['path'] != smb_params['path']:
                error_message = "Modifying path for a SMB Share is not " \
                                "allowed through Ansible Module"
                self.module.fail_json(msg=error_message)

            smb_share_params = ['allow_variable_expansion', 'auto_create_directory', 'continuously_available',
                                'file_filtering_enabled', 'strict_ca_lockout', 'change_notify', 'oplocks',
                                'impersonate_guest', 'impersonate_user', 'description', 'ntfs_acl_support',
                                'access_based_enumeration', 'access_based_enumeration_root_only', 'browsable',
                                'smb3_encryption_enabled', 'ca_write_integrity']

            if self.module.params["host_acls"]:
                for host_acl in self.module.params["host_acls"]:
                    if host_acl['access_type'] + ": " + host_acl['name'] not in smb_params["host_acl"]:
                        return True

            to_modify = False
            for param in smb_share_params:
                if self.module.params[param] and \
                        self.module.params[param] != \
                        smb_params[param]:
                    to_modify = True

            if self.module.params['file_filter_extension'] is not None and \
                    (self.module.params['file_filter_extension']['type'] and
                     self.module.params['file_filter_extension']['type'] !=
                     smb_params['file_filter_type']):
                to_modify = True

            return to_modify

        except Exception as e:
            error_message = 'Failed to determine if any modification' \
                            ' required for SMB attributes with error: ' \
                            '{0}'.format(utils.determine_error(e))
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

            host_acl_list = []
            if self.module.params["host_acls"]:
                for host_acl in self.module.params["host_acls"]:
                    host_acl_list.append(host_acl['access_type'] + ": " + host_acl['name'])

            modify_list = []

            if self.module.params['file_filter_extension']:
                if self.module.params['file_filter_extension']['state'] == "present-in-share":
                    modify_list = list(set(
                        smb_details['file_filter_extensions'] + self.module.params['file_filter_extension'][
                            'extensions']))

                elif self.module.params['file_filter_extension']['state'] == "absent-in-share":
                    modify_list = list(set(smb_details['file_filter_extensions']) - set(
                        self.module.params['file_filter_extension']['extensions']))

            if self.module.params['file_filter_extension'] is None:
                file_filter_type = None
            elif self.module.params['file_filter_extension']:
                file_filter_type = self.module.params['file_filter_extension']['type']

            smb_share = self.isi_sdk.SmbShare(
                permissions=permissions,
                description=self.module.params['description'],
                ntfs_acl_support=self.module.params['ntfs_acl_support'],
                access_based_enumeration=self.module.params[
                    'access_based_enumeration'],
                access_based_enumeration_root_only=self.module.params[
                    'access_based_enumeration_root_only'],
                browsable=self.module.params['browsable'],
                name=self.module.params['new_share_name'],
                allow_variable_expansion=self.module.params['allow_variable_expansion'],
                auto_create_directory=self.module.params['auto_create_directory'],
                file_filter_extensions=modify_list,
                file_filter_type=file_filter_type,
                file_filtering_enabled=self.module.params['file_filtering_enabled'],
                ca_timeout=self.ca_timeout_value(),
                strict_ca_lockout=self.module.params['strict_ca_lockout'],
                smb3_encryption_enabled=self.module.params['smb3_encryption_enabled'],
                ca_write_integrity=self.module.params['ca_write_integrity'],
                change_notify=self.module.params['change_notify'],
                oplocks=self.module.params['oplocks'],
                impersonate_guest=self.module.params['impersonate_guest'],
                impersonate_user=self.module.params['impersonate_user'],
                host_acl=host_acl_list)

            smb_share = self.octal_param_update(smb_share)

            smb_share_id = self.module.params['share_name']

            self.protocol_api.update_smb_share(
                smb_share, smb_share_id,
                zone=self.module.params['access_zone'])

        except Exception as e:
            error_message = "Failed to update the SMB share: {0} with " \
                            "error: {1}".format(smb_share_id,
                                                utils.determine_error(e))
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
                                         utils.determine_error(e))

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

        self.file_filter_param_validation()
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

        if smb_details and state == "present":
            smb_params = self.get_smb_params_from_details(
                smb_details['shares'][0])

            to_modify = self.is_smb_modified(smb_params)

        if state == 'present' and not smb_details:
            LOG.info("Creating a new SMB share %s", share_name)
            if not path or path == '' or ' ' in path:
                self.module.fail_json(msg="Invalid path.Valid path is "
                                          "required to create a smb share ")
            smb_details = self.create_smb_share()
            if smb_details:
                share_name = smb_details['id']
                smb_details = self.get_smb_details(share_name, access_zone)
                result['changed'] = True

        elif state == 'absent' and smb_details:
            LOG.info("Deleting the SMB share %s", share_name)
            self.delete_smb_share()
            result['changed'] = True
            smb_details = None

        elif state == 'present' and smb_details and to_modify:
            LOG.info("Modify the SMB share details")
            self.update_smb_details(share_name, smb_params)
            if new_share_name:
                smb_details = self.get_smb_details(
                    new_share_name, access_zone)
            else:
                smb_details = self.get_smb_details(
                    share_name, access_zone)
            share_name = smb_details['shares'][0]['name']
            result['changed'] = True

        octal_dict = "{0:o}"
        if state == 'present' and smb_details:
            LOG.info('Getting Details for SMB : %s : ', share_name)

            smb_details['shares'][0]['directory_create_mask(octal)'] = \
                octal_dict.format(smb_details['shares'][0]
                                  ['directory_create_mask'])
            smb_details['shares'][0]['directory_create_mode(octal)'] = \
                octal_dict.format(smb_details['shares'][0]
                                  ['directory_create_mode'])
            smb_details['shares'][0]['file_create_mask(octal)'] = \
                octal_dict.format(smb_details['shares'][0]
                                  ['file_create_mask'])
            smb_details['shares'][0]['file_create_mode(octal)'] = \
                octal_dict.format(smb_details['shares'][0]
                                  ['file_create_mode'])

            LOG.debug('SMB Details : %s ', smb_details)
            result['smb_details'] = smb_details

        self.module.exit_json(**result)


def get_smb_parameters():
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
        create_path=dict(type='bool'),
        allow_variable_expansion=dict(type='bool'),
        auto_create_directory=dict(type='bool'),
        continuously_available=dict(type='bool'),
        file_filter_extension=dict(
            type='dict', options=dict(
                extensions=dict(type='list', elements='str'),
                type=dict(default='deny', type='str', required=False, choices=['allow', 'deny']),
                state=dict(type='str', choices=['present-in-share', 'absent-in-share']),
            ),
            required=False
        ),
        file_filtering_enabled=dict(type='bool'),
        ca_timeout=dict(
            type='dict', options=dict(
                value=dict(type='int'),
                unit=dict(default='seconds', type='str', choices=['seconds', 'minutes', 'hours']))),
        strict_ca_lockout=dict(type='bool'),
        smb3_encryption_enabled=dict(type='bool'),
        ca_write_integrity=dict(type='str', choices=['none', 'full', 'write-read-coherent']),
        change_notify=dict(type='str', choices=['all', 'norecurse', 'none']),
        oplocks=dict(type='bool'),
        impersonate_guest=dict(type='str', choices=['always', 'never', 'bad_user']),
        impersonate_user=dict(type='str'),
        host_acls=dict(type='list', elements='dict',
                       options=dict(name=dict(type='str', required=True),
                                    access_type=dict(type='str', required=True))),
    )


def main():
    """Create PowerScale Smb object and perform action on it
        based on user input from playbook"""
    obj = SMB()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
