#!/usr/bin/python
# Copyright: (c) 2019, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Ansible module for managing access zones on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: accesszone

version_added: '1.2.0'

short_description: Manages access zones on PowerScale

description:
- Managing access zones on the PowerScale storage system includes getting details of the
  access zone and modifying the smb and nfs settings.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Akash Shendge (@shenda1) <ansible.team@dell.com>
- Pavan Mudunuri (@Pavan-Mudunuri) <ansible.team@dell.com>
- Trisha Datta (@trisha-dell) <ansible.team@dell.com>

options:
  az_name:
    description:
    - The name of the access zone.
    type: str
    required: true
  path:
    description:
    - Specifies the access zone base directory path.
    type: str
  groupnet:
    description:
    - Name of the groupnet for create access zone.
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
        - Specifies the C(UNIX) mask bits (octal) that are removed when a directory
          is created, restricting permissions.
        - Mask bits are applied before mode bits are applied.
        type: str
      directory_create_mode:
        description:
        - Specifies the C(UNIX) mode bits (octal) that are added when a directory is
          created, enabling permissions.
        type: str
      file_create_mask:
        description:
        - Specifies the C(UNIX) mask bits (octal) that are removed when a file is
          created, restricting permissions.
        type: str
      file_create_mode:
        description:
        - Specifies the C(UNIX) mode bits (octal) that are added when a file is
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
        - Set to C(true) if NFS commit requests execute asynchronously.
        type: bool
      nfsv4_domain:
        description:
        - Specifies the domain or realm through which users and groups are
          associated.
        type: str
      nfsv4_allow_numeric_ids:
        description:
        - If C(true), sends owners and groups as UIDs and GIDs when look up
          fails or if the I(nfsv4_no_name) property is set to 1.
        type: bool
      nfsv4_no_domain:
        description:
        - If C(true), sends owners and groups without a domain name.
        type: bool
      nfsv4_no_domain_uids:
        description:
        - If C(true), sends UIDs and GIDs without a domain name.
        type: bool
      nfsv4_no_names:
        description:
        - If C(true), sends owners and groups as UIDs and GIDs.
        type: bool
  provider_state:
    description:
    - Defines whether the auth providers should be added or removed from access zone.
    - If I(auth_providers) are given, then I(provider_state) should also be specified.
    - C(add) - indicates that the auth providers should be added to the access zone.
    - C(remove) - indicates that auth providers should be removed from the access zone.
    choices: [add, remove]
    type: str
    required: false
  auth_providers:
    description:
    - Specifies the auth providers which need to be added or removed from access zone.
    - If I(auth_providers) are given, then I(provider_state) should also be specified.
    type: list
    elements: dict
    suboptions:
      provider_name:
        description:
        - Specifies the auth provider name which needs to be added or removed from access zone.
        type: str
        required: true
      provider_type:
        description:
        - Specifies the auth provider type which needs to be added or removed from access zone.
        choices: ['local', 'file', 'ldap', 'ads', 'nis']
        type: str
        required: true
      priority:
        description:
        - Specifies the order of priority of the auth provider which needs to be added to access zone.
        - C(1) denotes the topmost priority.
        - If I(priority) is not provided, authentication provider will have lowest priority.
        type: int
  state:
    description:
    - Defines whether the access zone should exist or not.
    - C(present) - indicates that the access zone should exist on the system.
    - C(absent) - indicates that the access zone should not exist on the system.
    choices: ['present', 'absent']
    type: str
    required: true

notes:
- The I(check_mode) is not supported.
- Built-in System zone cannot be deleted.
- When access zone is deleted, all associated authentication providers remain available to other zones,
  the IP addresses are not reassigned to other zones.
- When access zone is deleted, SMB shares, NFS exports, and HDFS data paths are deleted,
  the directories and data still exist, and  new shares, exports, or paths can be mapped in another access zone.
'''

EXAMPLES = r'''
- name: Get details of access zone including smb and nfs settings
  dellemc.powerscale.accesszone:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    az_name: "{{access zone}}"
    state: "present"

- name: Modify smb settings of access zone
  dellemc.powerscale.accesszone:
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
  dellemc.powerscale.accesszone:
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
  dellemc.powerscale.accesszone:
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

- name: Add Auth Providers to the access zone
  dellemc.powerscale.accesszone:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    az_name: "{{access zone}}"
    provider_state: "add"
    auth_providers:
       - provider_name: "System"
         provider_type: "file"
         priority: 3
       - provider_name: "ldap-prashant"
         provider_type: "ldap"
    state: "present"

- name: Remove Auth Providers from the  access zone
  dellemc.powerscale.accesszone:
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
  dellemc.powerscale.accesszone:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    az_name: "{{access zone}}"
    path: "/ifs/test_dir"
    groupnet: "groupnet1"
    create_path: true
    provider_state: "add"
    auth_providers:
      - provider_name: "System"
        provider_type: "file"
    state: "present"

- name: Delete Access Zone
  dellemc.powerscale.accesszone:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    az_name: "sample_name"
    state: "absent"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
    sample: "false"

smb_modify_flag:
    description: Whether or not the default SMB settings of access zone has
                 changed.
    returned: on success
    type: bool
    sample: "false"

nfs_modify_flag:
    description: Whether or not the default NFS settings of access zone has
                 changed.
    returned: on success
    type: bool
    sample: "false"

access_zone_modify_flag:
    description: Whether auth providers linked to access zone has changed.
    returned: on success
    type: bool
    sample: "false"

access_zone_details:
    description: The access zone details.
    returned: When access zone exists
    type: complex
    contains:
        Zones:
            description: Specifies the properties of Zone.
            type: list
            contains:
                name:
                    description: Specifies the access zone name.
                    type: str
                auth_providers:
                    description: Specifies the list of authentication providers available on this access zone.
                    type: list
                ifs_restricted:
                    description: Specifies a list of users and groups that have read and write access to /ifs.
                    type: list
                zone_id:
                    description: Specifies the access zone ID on the system.
                    type: int
                groupnet:
                    description: Groupnet identifier.
                    type: str
                user_mapping_rules:
                    description: Specifies the current ID mapping rules.
                    type: list
                system_provider:
                    description: Specifies the system provider for the access zone.
                    type: str
                alternate_system_provider:
                    description: Specifies an alternate system provider.
                    type: str
        nfs_settings:
            description: NFS settings of access zone
            type: complex
            contains:
                export_settings:
                    description: Default values for NFS exports
                    type: complex
                    contains:
                        commit_asynchronous:
                            description: Set to C(true) if NFS commit requests execute asynchronously
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
                            description: If C(true), sends owners and groups as UIDs and GIDs when
                                         look up fails or if the 'nfsv4_no_name' property
                                         is set to 1
                            type: bool
                        nfsv4_no_domain:
                            description: If C(true), sends owners and groups without a domain name
                            type: bool
                        nfsv4_no_domain_uids:
                            description: If C(true), sends UIDs and GIDs without a domain name
                            type: bool
                        nfsv4_no_names:
                            description: If C(true), sends owners and groups as UIDs and GIDs
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
    sample:
        {"nfs_settings": {"export_settings": {
                "all_dirs": false,
                "block_size": 8192,
                "can_set_time": true,
                "case_insensitive": false,
                "case_preserving": true,
                "chown_restricted": false,
                "commit_asynchronous": false,
                "directory_transfer_size": 131072,
                "encoding": "DEFAULT",
                "link_max": 32767,
                "map_all": null,
                "map_failure": {
                    "enabled": false,
                    "primary_group": {
                        "id": null,
                        "name": null,
                        "type": null
                    },
                    "secondary_groups": [],
                    "user": {
                        "id": "USER:nobody",
                        "name": null,
                        "type": null
                    }
                },
                "map_full": true,
                "map_lookup_uid": false,
                "map_non_root": {
                    "enabled": false,
                    "primary_group": {
                        "id": null,
                        "name": null,
                        "type": null
                    },
                    "secondary_groups": [],
                    "user": {
                        "id": "USER:nobody",
                        "name": null,
                        "type": null
                    }
                },
                "map_retry": true,
                "map_root": {
                    "enabled": true,
                    "primary_group": {
                        "id": null,
                        "name": null,
                        "type": null
                    },
                    "secondary_groups": [],
                    "user": {
                        "id": "USER:nobody",
                        "name": null,
                        "type": null
                    }
                },
                "max_file_size": 9223372036854775807,
                "name_max_size": 255,
                "no_truncate": false,
                "read_only": false,
                "read_transfer_max_size": 1048576,
                "read_transfer_multiple": 512,
                "read_transfer_size": 131072,
                "readdirplus": true,
                "readdirplus_prefetch": 10,
                "return_32bit_file_ids": false,
                "security_flavors": ["unix"],
                "setattr_asynchronous": false,
                "snapshot": "-",
                "symlinks": true,
                "time_delta": 1e-09,
                "write_datasync_action": "DATASYNC",
                "write_datasync_reply": "DATASYNC",
                "write_filesync_action": "FILESYNC",
                "write_filesync_reply": "FILESYNC",
                "write_transfer_max_size": 1048576,
                "write_transfer_multiple": 512,
                "write_transfer_size": 524288,
                "write_unstable_action": "UNSTABLE",
                "write_unstable_reply": "UNSTABLE",
                "zone": "System"},
                "zone_settings": {
                    "nfsv4_allow_numeric_ids": true,
                    "nfsv4_domain": "localhost",
                    "nfsv4_no_domain": false,
                    "nfsv4_no_domain_uids": true,
                    "nfsv4_no_names": false,
                    "nfsv4_replace_domain": true,
                    "zone": null
                }},
            "smb_settings": {
                "access_based_enumeration": false,
                "access_based_enumeration_root_only": false,
                "allow_delete_readonly": false,
                "allow_execute_always": false,
                "ca_timeout": 120,
                "ca_write_integrity": "write-read-coherent",
                "change_notify": "norecurse",
                "continuously_available": null,
                "create_permissions": "default acl",
                "csc_policy": null,
                "directory_create_mask": 448,
                "directory_create_mask(octal)": "700",
                "directory_create_mode": 0,
                "directory_create_mode(octal)": "0",
                "file_create_mask": 448,
                "file_create_mask(octal)": "700",
                "file_create_mode": 64,
                "file_create_mode(octal)": "100",
                "file_filter_extensions": [],
                "file_filter_type": "deny",
                "file_filtering_enabled": false,
                "hide_dot_files": false,
                "host_acl": [],
                "impersonate_guest": "never",
                "impersonate_user": "",
                "ntfs_acl_support": true,
                "oplocks": true,
                "smb3_encryption_enabled": false,
                "sparse_file": false,
                "strict_ca_lockout": true,
                "strict_flush": true,
                "strict_locking": false,
                "zone": null
                },
            "zones": [{
                "alternate_system_provider": "lsa-file-provider:System",
                "auth_providers": ["lsa-ldap-provider:ansildap"],
                "cache_entry_expiry": 14400,
                "create_path": null,
                "force_overlap": null,
                "groupnet": "groupnet0",
                "home_directory_umask": 63,
                "id": "System",
                "ifs_restricted": [],
                "map_untrusted": "",
                "name": "System",
                "negative_cache_entry_expiry": 60,
                "netbios_name": "",
                "path": "/ifs",
                "skeleton_directory": "/usr/share",
                "system": true,
                "system_provider": "lsa-file-provider:System",
                "user_mapping_rules": [
                    "test_user_13 ++ test_user_15 [user]",
                    "test_user_14 => test_user []",
                    "test_user_13 ++ test_user_15 [user]",
                    "test_user_12 &= test_user_13 []"
                ],
                "zone_id": 1}]}
'''
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
import copy
LOG = utils.get_logger('accesszone')


class AccessZone(object):
    """Class with access zone operations"""

    def __init__(self):
        """ Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_accesszone_parameters())

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

    def unique_auth_providers(self, existing_items, new_items):
        final_list = copy.deepcopy(existing_items)
        for key in new_items:
            if new_items[key] not in existing_items:
                final_list.append(new_items[key])
        return final_list

    def reorder_auth_providers(self, updated_auth_providers_list, new_auth_providers, no_priority_list):
        final_auth_provider_list = []
        for key in new_auth_providers:
            if new_auth_providers[key] in updated_auth_providers_list and \
                    key <= len(self.unique_auth_providers(existing_items=updated_auth_providers_list,
                                                          new_items=new_auth_providers)) + len(no_priority_list):
                updated_auth_providers_list.remove(new_auth_providers[key])
        sorted_providers_by_priority = sorted(new_auth_providers.items(), key=lambda x: x[0])
        index = 0
        index1 = 0

        for provider in no_priority_list:
            if provider not in updated_auth_providers_list:
                updated_auth_providers_list.append(provider)

        for index in range(len(updated_auth_providers_list) + len(new_auth_providers)):
            if index + 1 in new_auth_providers:
                final_auth_provider_list.append(new_auth_providers[index + 1])
            elif index + 1 not in new_auth_providers and index1 < len(updated_auth_providers_list):
                final_auth_provider_list.append(updated_auth_providers_list[index1])
                index1 = index1 + 1

        for index in new_auth_providers:
            if new_auth_providers[index] not in final_auth_provider_list:
                final_auth_provider_list.append(new_auth_providers[index])
        return final_auth_provider_list

    def add_auth_providers_to_access_zone(self, name, auth_providers, existing_auth_providers):
        """ Add auth providers to access zone """
        try:
            updated_auth_providers_list = copy.deepcopy(existing_auth_providers)
            add_auth_providers_required = False
            provider_summary = self.api_auth.get_providers_summary()
            all_providers = provider_summary.provider_instances
            new_auth_providers = {}
            no_priority_list = []
            for i in range(len(auth_providers)):
                provider = [provider.id for provider in all_providers
                            if provider.name == auth_providers[i]['provider_name'] and
                            provider.type == auth_providers[i]['provider_type']]
                if not provider:
                    error_message = 'Provider: {0} of type: {1} does not exist'.format(
                        auth_providers[i]['provider_name'], auth_providers[i]['provider_type'])
                    LOG.error(error_message)
                    self.module.fail_json(msg=error_message)
                if auth_providers[i]['priority'] is None and provider[0] not in no_priority_list:
                    no_priority_list.append(provider[0])
                else:
                    new_auth_providers[auth_providers[i]['priority']] = provider[0]
            final_provider_list = self.reorder_auth_providers(new_auth_providers=new_auth_providers,
                                                              updated_auth_providers_list=existing_auth_providers,
                                                              no_priority_list=no_priority_list)
            if final_provider_list != updated_auth_providers_list:
                add_auth_providers_required = True
            if not add_auth_providers_required:
                return False
            update_zone = utils.isi_sdk.Zone(auth_providers=final_provider_list)
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

    def delete_access_zone(self, name=None):
        try:
            self.api_instance.delete_zone(zone_id=name)
            return True
        except Exception as e:
            error_msg = f'Failed to delete access zone: {utils.determine_error(e)}'
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

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

        if state == 'present' and not access_zone_details:
            self.validate_input(az_params)
            access_zone_params = self.construct_az_params(az_params)
            result['changed'] = self.create_access_zone(access_zone_params)
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

        if state == 'absent' and access_zone_details:
            result['changed'] = self.delete_access_zone(name)

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
                result['access_zone_modify_flag'] or result['changed']:
            access_zone_details = self.get_details(name)
            result['access_zone_details'] = access_zone_details
            result['changed'] = True
        self.module.exit_json(**result)


def get_accesszone_parameters():
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
            provider_type=dict(type='str', required=True, choices=['local', 'file', 'ldap', 'ads', 'nis']),
            priority=dict(type='int')
        )),
        state=dict(required=True, type='str', choices=['present', 'absent'])
    )


def main():
    """ Create PowerScale access zone object and perform action on it
        based on user input from playbook"""
    obj = AccessZone()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
