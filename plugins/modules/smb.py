#!/usr/bin/python
# Copyright: (c) 2019-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

""" Ansible module for managing SMB shares on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: smb

version_added: '1.2.0'

short_description: Manage SMB shares on PowerScale Storage System
description:
- Managing SMB share on PowerScale which includes.
- Create a new SMB share.
- Modify an existing SMB share.
- Get details of an existing SMB share.
- Delete an existing SMB share.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Arindam Datta (@dattaarindam) <ansible.team@dell.com>
- Trisha Datta (@Trisha-Datta) <ansible.team@dell.com>
- Bhavneet Sharma (@Bhavneet-Sharma) <ansible.team@dell.com>

options:
  share_name:
    description:
    - The name of the SMB share.
    type: str
    required: true
  path:
    description:
    - The path of the SMB share. This parameter will be mandatory only
      for the create operation. This is the absolute path for System Access
      Zone and the relative path for non-System Access Zone.
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
    - Directory creates mask bits. Octal value for owner, group, and others
      against read, write, and execute.
    type: str
  directory_create_mode:
    description:
    - Directory creates mode bits. Octal value for owner, group, and others
      against read, write, and execute.
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
    - An ACL expressing which hosts are allowed access. A deny clause must be
      the final entry.
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
  run_as_root:
    description:
    - Allow account to run as root.
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Specifies the name of persona.
        type: str
        required: true
        version_added: '3.1.0'
      type:
        description:
        - Specifies the type of persona.
        type: str
        choices: ['user', 'group', 'wellknown']
        required: true
        version_added: '3.1.0'
      provider_type:
        description:
        - Specifies the provider type of persona.
        - The supported values for I(provider_type) are C(local), C(file),
          C(ldap), C(nis) and C(ads).
        type: str
        default: local
        version_added: '3.1.0'
      state:
        description:
        - Specifies whether to add or remove the persona.
        type: str
        choices: ['allow', 'deny']
        default: allow
        version_added: '3.1.0'
  allow_delete_readonly:
    description:
    - Allow deletion of read-only files in the share.
    type: bool
    version_added: '3.1.0'
  allow_execute_always:
    description:
    - Allow users to execute files they have rigths for.
    type: bool
    version_added: '3.1.0'
  inheritable_path_acl:
    description:
    - Set inheritable acl on share path.
    type: bool
    version_added: '3.1.0'
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
    run_as_root:
      - name: "sample_user"
        type: "user"
        provider_type: "local"
        state: "present"
      - name: "sample_group"
        type: "group"
        provider_type: "nis"
        state: "present"
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
    run_as_root:
      - name: "ldap_user"
        type: "user"
        provider_type: "ldap"
        state: "absent"
      - name: "weknown_group"
        type: "wellknown"
        provider_type: "local"
        state: "present"
    allow_delete_readonly: true
    allow_execute_always: false
    inheritable_path_acl: true
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
        allow_delete_readonly:
            description: Allow deletion of read-only files in the SMB Share.
            type: bool
        allow_execute_always:
            description: Allow user to execute files they have rights for.
            type: bool
        name:
            description: Name of the SMB Share.
            type: str
        id:
            description: Id of the SMB Share.
            type: str
        description:
            description: Description of the SMB Share.
            type: str
        path:
            description: Path of the SMB Share.
            type: str
        permission:
            description: permission on the of the SMB Share for user/group/wellknown/
            type: list
        file_create_mask:
            description: File create mask bit for SMB Share.
            type: int
        file_create_mode:
            description: File create mode bit for SMB Share.
            type: int
        directory_create_mask:
            description: Directory create mask bit for SMB Share.
            type: int
        directory_create_mode:
            description: Directory create mode bit for SMB Share.
            type: int
        browsable:
            description: Share is visible in net view and the browse list.
            type: bool
        file_create_mask(octal):
            description: File create mask bit for SMB Share in octal format.
            type: str
        file_create_mode(octal):
            description: File create mode bit for SMB Share in octal format.
            type: str
        directory_create_mask(octal):
            description: Directory create mask bit for SMB Share in octal format.
            type: str
        directory_create_mode(octal):
            description: Directory create mode bit for SMB Share in octal format.
            type: str
        inheritable_path_acl:
            description: Inheritable ACL on share path.
            type: bool
        run_as_root:
            description: Allow the account to run as root.
            type: list
            contains:
                name:
                    description: Name of the persona.
                    type: str
                id:
                    description: Id of the persona.
                    type: str
                type:
                    description: Type of the persona.
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
                "run_as_root": [
                    {
                        "id": "SID:S-1-1-0",
                        "name": "Everyone",
                        "type": "wellknown"
                    },
                    {
                        "id": "SID:S-1-5-32-545",
                        "name": "sample_user",
                        "type": "user"
                    }
                ],
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

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.powerscale_base \
    import PowerScaleBase
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.auth \
    import Auth
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.zones_summary \
    import ZonesSummary
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('smb')


class SMB(PowerScaleBase):
    """Class with SMB share operations"""

    def __init__(self):
        """Define all the parameters required by this module"""

        ansible_module_params = {
            'argument_spec': get_smb_parameters(),
            'supports_check_mode': False
        }

        super().__init__(AnsibleModule, ansible_module_params)

        self.result = {
            'changed': False,
            'smb_details': {}
        }

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
        return ZonesSummary(self.zones_summary_api,
                            self.module).get_zone_base_path(access_zone)

    def ca_timeout_value(self):
        if self.module.params.get('ca_timeout'):
            ca_value = self.module.params['ca_timeout'].get('value')
            ca_unit = self.module.params['ca_timeout'].get('unit')
            if ca_unit:
                ca_timeout_value = utils.get_time_in_seconds(
                    ca_value, ca_unit)
            else:
                ca_timeout_value = ca_value
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

    def remove_duplicates(self, root_list):
        """remove duplicates"""
        unique_list = []
        if root_list:
            unique_list = [item for item in root_list if item not in unique_list]
            return unique_list

    def prepare_persona_dict_persona(self, sid, persona):
        """add persona"""
        try:
            persona_dict = self.isi_sdk.AuthAccessAccessItemFileGroup(
                name=persona['name'], id=sid, type=persona['type'])
            return persona_dict.to_dict()
        except Exception as e:
            error_message = f'Failed to create persona dict ' \
                            f'with error {utils.determine_error(e)}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def arrange_persona_dict(self, persona):
        """arrange persona dict"""
        if persona['type'] == "user" or persona['type'] == "group":
            sid = self.get_sid(name=persona['name'], type=persona['type'].upper(),
                               provider=persona.get('provider_type'))
            tmp_dict = self.prepare_persona_dict_persona(sid, persona)

        else:
            sid = Auth(self.auth_api,
                       self.module).get_wellknown_details(name=persona['name'])['id']
            tmp_dict = self.prepare_persona_dict_persona(sid, persona)

        return tmp_dict

    def set_allow_list(self, allow_rar_list, smb_rar_list):
        """set allow list"""
        add_allow_list = list()

        if allow_rar_list and len(allow_rar_list) != 0:

            for allow in allow_rar_list:

                if (len(smb_rar_list) == 0 or len(smb_rar_list) > 0) and \
                        allow not in smb_rar_list:

                    add_allow_list.append(allow)
        return add_allow_list

    def set_deny_list(self, deny_rar_list, all_smb_rar_list):
        """set deny list"""
        remove_deny_list = list()
        if deny_rar_list and len(deny_rar_list) != 0:
            for deny in deny_rar_list:
                if all_smb_rar_list and deny in all_smb_rar_list:
                    remove_deny_list.append(deny)
        return remove_deny_list

    def preare_unique_rar(self, allow_list, deny_list, smb_root_list):
        """prepare run as root list"""
        tmp_all_list = list()
        tmp_all_list.extend(smb_root_list)

        tmp_allow_list = self.set_allow_list(allow_list, smb_root_list)

        if tmp_allow_list:

            tmp_all_list.extend(tmp_allow_list)
        tmp_all_list = self.remove_duplicates(tmp_all_list)

        remove_list = list()
        tmp_deny_list = self.set_deny_list(deny_list, tmp_all_list)

        if tmp_deny_list:
            remove_list.extend(tmp_deny_list)

        final_rar_list = list()
        if tmp_all_list:

            for item2 in tmp_all_list:

                if item2 not in remove_list:

                    final_rar_list.append(item2)

        if final_rar_list != smb_root_list:
            return True, final_rar_list
        return False, None

    def prepare_run_as_root_list(self, root_list, smb_root_list):
        """prepare run as root list"""

        if root_list:
            allow_list = []
            deny_list = []

            # remove duplicate dict from root_list
            root_list = self.remove_duplicates(root_list)

            for persona in root_list:

                if persona['state'] == "allow":
                    add_dict = self.arrange_persona_dict(persona)
                    allow_list.append(add_dict)

                elif persona['state'] == "deny":
                    remove_dict = self.arrange_persona_dict(persona)
                    deny_list.append(remove_dict)

            allow_list = self.remove_duplicates(allow_list)
            deny_list = self.remove_duplicates(deny_list)

            tmp_flag, temp_list = self.preare_unique_rar(allow_list, deny_list,
                                                         smb_root_list)
            if tmp_flag:
                return True, temp_list
        return False, None

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

            run_root_list = self.module.params['run_as_root'] \
                if 'run_as_root' in self.module.params else None
            rar_flag, run_root_list = self.prepare_run_as_root_list(run_root_list, [])

            smb_share.permissions = permissions
            if rar_flag:
                smb_share.run_as_root = run_root_list

            smb_share = self.octal_param_update(smb_share)

            params_list = [
                'description', 'ntfs_acl_support', 'access_based_enumeration',
                'access_based_enumeration_root_only', 'browsable', 'create_path',
                'allow_variable_expansion', 'auto_create_directory',
                'continuously_available', 'strict_ca_lockout', 'change_notify',
                'oplocks', 'impersonate_guest', 'impersonate_user',
                'smb3_encryption_enabled', 'ca_write_integrity',
                'host_acls', 'allow_delete_readonly', 'allow_execute_always',
                'inheritable_path_acl']
            for param in params_list:
                if self.module.params.get(param):
                    setattr(smb_share, param, self.module.params[param])

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
            user_smb_permissions, group_smb_permissions, wellknown_smb_permissions = \
                self.get_smb_permissions_dict(smb_permissions)

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
                        remaining_wellknowns, wellknown_smb_permissions, 'WELLKNOWN'))

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
            params = [
                'allow_variable_expansion', 'auto_create_directory',
                'continuously_available',
                'file_filter_extensions', 'file_filter_type',
                'file_filtering_enabled', 'strict_ca_lockout',
                'ca_timeout', 'change_notify', 'oplocks', 'impersonate_guest',
                'impersonate_user', 'host_acl', 'smb3_encryption_enabled',
                'ca_write_integrity', 'allow_delete_readonly',
                'allow_execute_always', 'inheritable_path_acl']

            udpated_smb_params = {
                'name': smb_details['name'],
                'path': smb_details['path'],
                'permissions': smb_details['permissions'],
                'description': smb_details['description'],
                'run_as_root': smb_details['run_as_root'],
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
                udpated_smb_params[param] = smb_details[param]

            return udpated_smb_params
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
                api_response = Auth(
                    self.auth_api,
                    self.module).get_user_details(name=name, zone=zone,
                                                  provider=provider)
                return api_response['users'][0]['sid']['id']
            elif type == 'GROUP':
                api_response = Auth(
                    self.auth_api,
                    self.module).get_group_details(name=name, zone=zone,
                                                   provider=provider)
                return api_response['groups'][0]['sid']['id']
        except Exception as e:
            error_message = "Failed to get {0}:{1} details for AccessZone:{2} " \
                            "and Provider:{3} with error" \
                            " {4}".format(type, name,
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

    def is_sid_in_permission_list(self, permission_list, index, sid, params_permission):
        """checking if the sid is in permission list"""
        if sid in permission_list[index].keys():
            permission_type = \
                params_permission['permission_type'].lower()

            permission = params_permission['permission'].lower()
            permission_list_per = permission_list[index][sid]['permission']
            permission_list_type = permission_list[index][sid]['permission_type']

            if (permission_type != permission_list_type) or \
                    (permission != permission_list_per):
                return True
        else:
            return True

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
                permission_list = [user_permissions, group_permissions,
                                   wellknown_permissions]
                for index in range(len(permission_type_list)):
                    if permission_type_list[index] + '_name' in params_permission:
                        sid = self.get_sid(
                            params_permission[permission_type_list[index] + '_name'],
                            permission_type_list[index].upper(),
                            params_permission['provider_type'])
                        return self.is_sid_in_permission_list(
                            permission_list, index, sid, params_permission)
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
            error_message = "extensions and state are required together when" \
                            " file_filter_extension is mentioned."
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def check_newname_or_mode_bits_modified(self, smb_params):
        """Check if newname or mode bits are modified"""
        mod_flag = False
        if self.module.params['new_share_name'] and \
                (self.module.params['new_share_name'].lower() !=
                 smb_params['name'].lower()):
            return True

        smb_share_mask_mode_bit_params = [
            'directory_create_mask', 'directory_create_mode', 'file_create_mask',
            'file_create_mode']

        for param in smb_share_mask_mode_bit_params:
            if self.module.params[param] and \
                    int(self.module.params[param], 8) != smb_params[param]:
                return True
        return mod_flag

    def is_path_modified(self, smb_params):
        """Checking if SMB path has changed"""
        if self.module.params['path'] and \
                self.module.params['path'] != smb_params['path']:
            error_message = "Modifying path for a SMB Share is not allowed" \
                            " through Ansible Module"
            self.module.fail_json(msg=error_message)

    def is_file_filter_param_modified(self, smb_params):
        """Validating file filter params"""
        modify_list = []
        if self.module.params['file_filter_extension']:
            if self.module.params['file_filter_extension']['state'] == "present-in-share":
                modify_list = set(list(smb_params['file_filter_extensions']) + list(
                    self.module.params['file_filter_extension']['extensions']))

            elif self.module.params['file_filter_extension']['state'] == "absent-in-share":
                modify_list = set(list(smb_params['file_filter_extensions'])) - set(
                    list(self.module.params['file_filter_extension']['extensions']))

        if self.module.params['file_filter_extension'] and \
                set(modify_list) != set(smb_params['file_filter_extensions']):
            return True

    def is_hostacl_modified(self, smb_params):
        """Checking if hostacl has changed"""
        if self.module.params["host_acls"]:
            for host_acl in self.module.params["host_acls"]:
                if host_acl['access_type'] + ": " + host_acl['name'] not in \
                        smb_params["host_acl"]:
                    return True

    def is_bool_str_modified(self, smb_params):
        """Checking if bool or other str parameters has changed"""
        smb_share_params = [
            'allow_variable_expansion', 'auto_create_directory',
            'continuously_available', 'file_filtering_enabled',
            'strict_ca_lockout', 'change_notify', 'oplocks', 'impersonate_guest',
            'impersonate_user', 'description', 'ntfs_acl_support',
            'access_based_enumeration', 'access_based_enumeration_root_only',
            'browsable', 'smb3_encryption_enabled', 'ca_write_integrity',
            'allow_delete_readonly', 'allow_execute_always',
            'inheritable_path_acl']

        to_modify = False
        for param in smb_share_params:
            if self.module.params.get(param) is not None and \
                    self.module.params.get(param) != smb_params[param]:
                to_modify = True

        if self.module.params['file_filter_extension'] is not None and \
                (self.module.params['file_filter_extension']['type'] and
                    self.module.params['file_filter_extension']['type'] !=
                    smb_params['file_filter_type']):
            to_modify = True

        return to_modify

    def is_rar_modified(self, smb_params):
        """Checking if run_as_root has changed"""
        pb_rar_list = self.module.params.get('run_as_root')
        module_rar_list = smb_params.get('run_as_root')

        mod_flag, modify_list = self.prepare_run_as_root_list(pb_rar_list, module_rar_list)
        if mod_flag:
            return True, modify_list
        return False, None

    def is_smb_modified(self, smb_params):
        """Checking if SMB attribute has changed & if modification required"""
        try:

            LOG.debug("is_smb_modified called with "
                      "params: %s", smb_params)

            self.is_path_modified(smb_params)
            name_mode_bit_flag = False
            name_mode_bit_flag = self.check_newname_or_mode_bits_modified(smb_params)

            file_filter_flag = False
            file_filter_flag = self.is_file_filter_param_modified(smb_params)

            if self.module.params['ca_timeout'] and \
                    smb_params['ca_timeout'] != self.ca_timeout_value():
                return True

            if self.module.params['permissions'] and \
                    self.is_permission_modified(smb_params['permissions']):
                return True

            host_acl_flag = False
            host_acl_flag = self.is_hostacl_modified(smb_params)

            bool_str_flag = False
            bool_str_flag = self.is_bool_str_modified(smb_params)

            modify_flags = [name_mode_bit_flag, file_filter_flag,
                            host_acl_flag, bool_str_flag]
            return any(m_flag for m_flag in modify_flags if m_flag)

        except Exception as e:
            error_message = 'Failed to determine if any modification' \
                            ' required for SMB attributes with error: ' \
                            '{0}'.format(utils.determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def update_smb_details(self, smb_share_id, smb_details, updated_rar):
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
                description=self.module.params.get('description'),
                ntfs_acl_support=self.module.params.get('ntfs_acl_support'),
                access_based_enumeration=self.module.params.get(
                    'access_based_enumeration'),
                access_based_enumeration_root_only=self.module.params.get(
                    'access_based_enumeration_root_only'),
                browsable=self.module.params.get('browsable'),
                name=self.module.params.get('new_share_name'),
                allow_variable_expansion=self.module.params.get('allow_variable_expansion'),
                auto_create_directory=self.module.params.get('auto_create_directory'),
                file_filter_extensions=modify_list,
                file_filter_type=file_filter_type,
                file_filtering_enabled=self.module.params.get('file_filtering_enabled'),
                ca_timeout=self.ca_timeout_value(),
                strict_ca_lockout=self.module.params.get('strict_ca_lockout'),
                smb3_encryption_enabled=self.module.params.get('smb3_encryption_enabled'),
                ca_write_integrity=self.module.params.get('ca_write_integrity'),
                change_notify=self.module.params.get('change_notify'),
                oplocks=self.module.params.get('oplocks'),
                impersonate_guest=self.module.params.get('impersonate_guest'),
                impersonate_user=self.module.params.get('impersonate_user'),
                host_acl=host_acl_list,
                run_as_root=updated_rar,
                allow_execute_always=self.module.params.get('allow_execute_always'),
                allow_delete_readonly=self.module.params.get('allow_delete_readonly'),
                inheritable_path_acl=self.module.params.get('inheritable_path_acl'))

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

    def validate_run_as_root_list(self):
        """Validate run_as_root and add default provider_type"""
        run_as_root = self.module.params['run_as_root']
        for persona in run_as_root:
            if utils.is_param_empty_spaces(persona['name']):
                err_messge = "Provide valid value for persona name."
                self.module.fail_json(msg=err_messge)

    def validate_permission_dict(self):
        """Validate permission and add default provider_type"""
        permissions = self.module.params['permissions']
        for perm in permissions:
            if ("user_name" in perm or "group_name" in perm) and \
                    "provider_type" not in perm:
                perm['provider_type'] = 'local'
            if "wellknown" in perm and "provider_type" in perm:
                LOG.warn("'provider_type' for wellknown will be ignored")

        LOG.info("Default provider_type added to permission: %s",
                 self.module.params['permissions'])

    def validate_permission_and_runas_root(self):
        """validate permission and runas_root"""
        permissions = self.module.params['permissions']
        run_as_root = self.module.params['run_as_root']
        if permissions:
            self.validate_permission_dict()
        elif run_as_root:
            self.validate_run_as_root_list()

    def validate_input_params(self, share_name, access_zone, path):
        """Validate the user input parameters"""
        if (not share_name) or len(share_name) < 1 or share_name.isspace():
            error_message = f"Invalid share name {share_name}"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

        if access_zone and path:
            effective_path = path
            if access_zone.lower() == "system":
                if not path.startswith('/'):
                    err_msg = f"Invalid path {path}, Path must start " \
                              "with '/'"
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)
            else:
                if not path.startswith('/'):
                    path = f"/{path}"
                effective_path = self.get_zone_base_path(
                    access_zone) + path
            self.module.params['path'] = effective_path

    def validate_path(self, path):
        """Validate the path"""
        if not path or utils.is_param_empty_spaces(path):
            self.module.fail_json(msg="Invalid path. Valid path is "
                                  "required to create a smb share")

    def format_output(self, smb_details):
        """Format the output"""
        for key in ('directory_create_mask', 'directory_create_mode', 'file_create_mask', 'file_create_mode'):
            if smb_details['shares'][0].get(key):
                smb_details['shares'][0][f"{key}(octal)"] = "{0:o}".format(int(smb_details['shares'][0][key]))

        LOG.debug('SMB Details : %s', smb_details)
        return smb_details


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
                type=dict(default='deny', type='str', required=False,
                          choices=['allow', 'deny']),
                state=dict(type='str',
                           choices=['present-in-share', 'absent-in-share']),
            ),
            required=False
        ),
        file_filtering_enabled=dict(type='bool'),
        ca_timeout=dict(
            type='dict', options=dict(
                value=dict(type='int'),
                unit=dict(default='seconds', type='str',
                          choices=['seconds', 'minutes', 'hours']))),
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
        allow_delete_readonly=dict(type='bool'), allow_execute_always=dict(type='bool'),
        inheritable_path_acl=dict(type='bool'),
        run_as_root=dict(
            type='list', elements='dict',
            options=dict(
                name=dict(type='str', required=True),
                type=dict(type='str', choices=['user', 'group', 'wellknown'],
                          required=True),
                provider_type=dict(type='str', default='local'),
                state=dict(type='str', choices=['allow', 'deny'],
                           default='allow'))),
    )


class SMBExitHandler:
    def handle(self, smb_obj, smb_details):
        if smb_details:
            smb_details = smb_obj.format_output(smb_details)
        smb_obj.result['smb_details'] = smb_details
        smb_obj.module.exit_json(**smb_obj.result)


class SMBDeleteHandler:
    def handle(self, smb_obj, smb_params, smb_details):
        if smb_params['state'] == 'absent' and smb_details:
            info_msg = f"Deleting SMB share {smb_params['share_name']}"
            LOG.info(info_msg)
            smb_obj.delete_smb_share()
            smb_obj.result['changed'] = True
            smb_details = {}
        SMBExitHandler().handle(smb_obj, smb_details)


class SMBModifyHandler:
    def handle(self, smb_obj, smb_params, smb_details):
        state = smb_params['state']
        to_modify = False

        if smb_details and state == "present":
            all_smb_params = smb_obj.get_smb_params_from_details(
                smb_details['shares'][0])

            to_modify = smb_obj.is_smb_modified(all_smb_params)
            to_rar_modified, updated_rar_list = smb_obj.is_rar_modified(all_smb_params)

            if to_modify or to_rar_modified:
                LOG.info("Modify the SMB share details")
                smb_obj.update_smb_details(smb_params['share_name'],
                                           all_smb_params, updated_rar_list)
                if smb_params['new_share_name']:
                    smb_details = smb_obj.get_smb_details(
                        smb_params['new_share_name'],
                        smb_params['access_zone'])
                else:
                    smb_details = smb_obj.get_smb_details(
                        smb_params['share_name'], smb_params['access_zone'])
                smb_obj.result['changed'] = True
        SMBDeleteHandler().handle(smb_obj, smb_params, smb_details)


class SMBCreateHandler:
    def handle(self, smb_obj, smb_params, smb_details):
        state = smb_params['state']
        path = smb_params['path']
        access_zone = smb_params['access_zone']
        if state == 'present' and not smb_details:
            LOG.info(f"Creating a new SMB share {smb_params['share_name']}")
            smb_obj.validate_path(path)
            smb_details = smb_obj.create_smb_share()
            if smb_details:
                share_name = smb_details['id']
                smb_details = smb_obj.get_smb_details(share_name, access_zone)
                smb_obj.result['changed'] = True
        SMBModifyHandler().handle(smb_obj, smb_params, smb_details)


class SMBHandler:
    def handle(self, smb_obj, smb_params):
        share_name = smb_params['share_name']
        path = smb_params['path']
        access_zone = smb_params['access_zone']

        smb_obj.file_filter_param_validation()
        smb_obj.validate_input_params(share_name, access_zone, path)
        smb_obj.validate_permission_and_runas_root()

        smb_details = smb_obj.get_smb_details(share_name, access_zone)

        LOG.info('SMB Details with unmodified mode/mask '
                 'bits : %s', smb_details)
        SMBCreateHandler().handle(smb_obj, smb_params, smb_details)


def main():
    """Create PowerScale Smb object and perform action on it
        based on user input from playbook"""
    obj = SMB()
    SMBHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
