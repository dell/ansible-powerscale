#!/usr/bin/python
# Copyright: (c) 2019-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing filesystems on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: filesystem

version_added: '1.2.0'

short_description: Manage Filesystems on PowerScale

description:
- Managing Filesystems on PowerScale Storage System includes
  Create a new Filesystem,
  Delete a Filesystem,
  Get details of a filesystem,
  Modify a Filesystem (Quota, ACLs).

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Prashant Rakheja (@prashant-dell) <ansible.team@dell.com>
- Trisha Datta (@trisha-dell) <ansible.team@dell.com>
- Kritika Bhateja(@Kritika-Bhateja-03) <ansible.team.dell.com>)

options:
  path:
    description:
    - This is the directory path. It is the absolute path for System access zone
      and is relative if using a non-System access zone. For example, if your access
      zone is 'Ansible' and it has a base path '/ifs/ansible' and the path
      specified is '/user1', then the effective path would be
      '/ifs/ansible/user1'.
      If your access zone is System, and you have 'directory1' in the access
      zone, the path provided should be '/ifs/directory1'.
    required: true
    type: str
  access_zone:
    description:
    - The access zone. If no Access Zone is specified, the 'System' access
      zone would be taken by default.
    type: str
    default: 'System'
  owner:
    description:
    - The owner of the Filesystem.
    - This parameter is required when creating a Filesystem.
    - The following sub-options are supported for Owner.
      - I(name(str)),
      - I(provider_type(str)).
    - If you specify owner, then the corresponding name is mandatory.
    - The I(provider_type) is optional and it defaults to C(local).
    - The supported values for I(provider_type) are C(local), C(file),
      C(ldap) and C(ads).
    type: dict
  group:
    description:
    - The group of the Filesystem.
    - The following sub-options are supported for Group.
      - I(name(str)),
      - I(provider_type(str)).
    - If you specify  a group, then the corresponding name is mandatory.
    - The I(provider_type) is optional, it defaults to C(local).
    - The supported values for I(provider_type) are C(local), C(file),
      C(ldap) and C(ads).
    type: dict
  access_control:
    description:
    - The ACL value for the directory.
    - At the time of creation, users can either provide input
      such as C(private_read) , C(private) , C(public_read), C(public_read_write),
      C(public) or in C(POSIX) format (eg 0700).
    - Modification of ACL is only supported from C(POSIX) to C(POSIX) mode.
    - This field is mutually exclusive with I(access_control_rights).
    type: str
  access_control_rights:
    description:
    - Manage user rights and set ACL permissions for files and directories.
    type: dict
    suboptions:
      access_rights:
        description:
        - Provides the list of access rights that are defined for the directory.
        type: list
        elements: str
      access_type:
        description:
        - Allows or denies access to the directory based on the access rights set for
          the trustee.
        type: str
        required: true
        choices: ['allow', 'deny']
      inherit_flags:
        description:
        - Provides the inherit flags set for the directory.
        type: list
        elements: str
        choices: ['object_inherit', 'container_inherit', 'inherit_only',
                  'no_prop_inherit', 'inherited_ace']
      trustee:
        description:
        - Provides the trustee (user or group) name and trustee I(provider_type).
        type: dict
        required: true
        suboptions:
          name:
            description:
            - Provides the trustee (user or group) name.
            type: str
            required: true
          type:
            description:
            - Provides the trustee type.
            type: str
            choices: ['user', 'group', 'wellknown']
            default: user
          provider_type:
            description:
            - The I(provider_type) is optional and it defaults to C(local).
            - The supported values for I(provider_type) are C(local), C(file), C(ldap) and C(ads).
            type: str
            default: local
  access_control_rights_state:
    description:
    - Specifies if the access rights are to be added or deleted for the trustee.
    - It is required together with I(access_control_rights).
    type: str
    choices: ['add', 'remove']
  recursive:
    description:
    - Creates intermediate folders recursively when set to C(true).
    type: bool
    default: true

  recursive_force_delete:
    description:
    - Deletes sub files and folders recursively when set to C(true) even if the filesystem is not empty.
    type: bool
    default: false

  quota:
    description:
    - The Smart Quota for the filesystem. Only directory Quotas are supported.
    - The following sub-options are supported for Quota.
    type: dict
    suboptions:
      include_snap_data:
        description:
        - Whether to include the snapshots in the quota or not.
        type: bool
        default: false
      include_data_protection_overhead:
        description:
        - Whether to include the data protection overheads
          in the quota or not.
        - If not passed during quota creation then quota will be created
          excluding the overheads.
        - This parameter is supported for SDK 8.1.1
        type: bool
      thresholds_on:
        description:
        - For SDK 9.1.0 the parameter I(include_overheads) is deprecated and
          I(thresholds_on) is used.
        type: str
        choices: [ 'app_logical_size', 'fs_logical_size', 'physical_size']
      advisory_limit_size:
        description:
        - The threshold value after which the advisory notification
          will be sent.
        type: int
      soft_limit_size:
        description:
        - Threshold value after which the soft limit exceeded notification
          will be sent and the I(soft_grace) period will start.
        - Write access will be restricted after the grace period expires.
        - Both I(soft_grace_period) and I(soft_limit_size) are required to modify
          soft threshold for the quota.
        type: int
      hard_limit_size:
        description:
        - Threshold value after which a hard limit exceeded
          notification will be sent.
        - Write access will be restricted after the hard limit is exceeded.
        type: int
      cap_unit:
        description:
        - Unit of storage for the hard, soft and advisory limits.
        - This parameter is required if any of the hard, soft or advisory
          limits is specified.
        type: str
        choices: ['GB', 'TB']
      container:
         description: If C(true), SMB shares using the quota directory see the quota thresholds as share size.
         type: bool
         default: false
      quota_state:
         description: Defines whether the quota should exist or not
         choices: [absent, present]
         type: str

  state:
    description:
    -  Defines whether the Filesystem should exist or not.
    -  A filesystem with NFS exports or SMB shares cannot be deleted.
    -  Any Quotas on the Filesystem need to be removed before deleting the
       filesystem.
    required: true
    choices: [absent, present]
    type: str

  list_snapshots:
    description:
    - If set to C(true), the filesystem's snapshots are returned.
    type: bool
    default: false

notes:
- While deleting a filesystem when recursive_force_delete is set as C(true) it
  deletes all sub files and folders recursively. This is C(true)
  even if the filesystem is not empty.
- Modification of I(inherit_flags) of filesystem ACL is
  successful only if I(access_rights) is also specified in
  the I(access_control_rights) dictionary.
- I(Check_mode) is supported.
'''

EXAMPLES = r'''
- name: Create Filesystem with Quota in given access zone
  dellemc.powerscale.filesystem:
    onefs_host: "{{onefs_host}}"
    port_no: "{{powerscaleport}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    path: "<path>"
    access_zone: "{{access_zone}}"
    owner:
      name: 'ansible_user'
      provider_type: 'ldap'
    group:
      name: 'ansible_group'
      provider_type: 'ldap'
      access_control: "{{access_control}}"
    quota:
      include_snap_data: false
      include_data_protection_overhead: false
      advisory_limit_size: 2
      soft_limit_size: 5
      hard_limit_size: 10
      cap_unit: "GB"
      quota_state: "present"
      container: true
      recursive: "{{recursive}}"
    state: "{{state_present}}"

- name: Create Filesystem in default (system) access zone, without Quota
  dellemc.powerscale.filesystem:
    onefs_host: "{{onefs_host}}"
    port_no: "{{powerscaleport}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    path: "<path>"
    owner:
    name: 'ansible_user'
    provider_type: 'ldap'
    state: "{{state_present}}"

- name: Get filesystem details
  dellemc.powerscale.filesystem:
    onefs_host: "{{onefs_host}}"
    port_no: "{{powerscaleport}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    access_zone: "{{access_zone}}"
    path: "<path>"
    state: "{{state_present}}"

- name: Get filesystem details with snapshots
  dellemc.powerscale.filesystem:
    onefs_host: "{{onefs_host}}"
    port_no: "{{powerscaleport}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    access_zone: "{{access_zone}}"
    path: "<path>"
    list_snapshots: "{{list_snapshots_true}}"
    state: "{{state_present}}"

- name: Modify Filesystem Hard Quota
  dellemc.powerscale.filesystem:
    onefs_host: "{{onefs_host}}"
    port_no: "{{powerscaleport}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    path: "<path>"
    access_zone: "{{access_zone}}"
    quota:
    hard_limit_size: 15
    cap_unit: "GB"
    quota_state: "present"
    container: true
    state: "{{state_present}}"

- name: Modify Filesystem Owner, Group and ACL
  dellemc.powerscale.filesystem:
    onefs_host: "{{onefs_host}}"
    port_no: "{{powerscaleport}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    path: "<path>"
    access_zone: "{{access_zone}}"
    owner:
      name: 'ansible_user'
      provider_type: 'ldap'
    group:
      name: 'ansible_group'
      provider_type: 'ldap'
      access_control: "{{new_access_control}}"
    state: "{{state_present}}"

- name: Modify Filesystem to add access control rights
  dellemc.powerscale.filesystem:
    onefs_host: "{{onefs_host}}"
    port_no: "{{powerscaleport}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    path: "/ifs/test"
    access_zone: "{{access_zone}}"
    access_control_rights:
    access_type: "allow"
    access_rights:
      - dir_gen_all
    inherit_flags:
      - container_inherit
    trustee:
      name: test_user
      provider_type: "ldap"
    access_control_rights_state: "add"
    state: "present"

- name: Modify Filesystem to remove access control rights
  dellemc.powerscale.filesystem:
    onefs_host: "{{onefs_host}}"
    port_no: "{{powerscaleport}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    path: "/ifs/test"
    access_zone: "{{access_zone}}"
    access_control_rights:
    access_type: "allow"
    access_rights:
      - dir_gen_all
    inherit_flags:
      - container_inherit
    trustee:
      name: test_user
      provider_type: "ldap"
    access_control_rights_state: "remove"
    state: "present"

- name: Remove Quota from FS
  dellemc.powerscale.filesystem:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    path: "<path>"
    access_zone: "{{access_zone}}"
    quota:
      quota_state: "absent"
    state: "{{state_present}}"

- name: Create Filesystem with access control rights for everyone
  dellemc.powerscale.filesystem:
    onefs_host: "{{onefs_host}}"
    port_no: "{{powerscaleport}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    path: "/ifs/test"
    access_zone: "{{access_zone}}"
    access_control_rights:
    access_type: "allow"
    access_rights:
      - dir_gen_all
    inherit_flags:
      - container_inherit
    trustee:
      name: "everyone"
      type: "wellknown"
    access_control_rights_state: "add"
    state: "present"

- name: Delete filesystem
  dellemc.powerscale.filesystem:
    onefs_host: "{{onefs_host}}"
    port_no: "{{powerscaleport}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{user}}"
    api_password: "{{api_password}}"
    access_zone: "{{access_zone}}"
    path: "<path>"
    recursive_force_delete: "{{recursive_force_delete}}"
    state: "{{state_absent}}"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
    sample: "true"

filesystem_details:
    description: The filesystem details.
    type: complex
    returned: When Filesystem exists.
    contains:
        attrs:
            description: The attributes of the filesystem.
            type: dict
    sample: {
        "attrs": [
            {
                "name": "owner",
                "namespace": null,
                "value": "user"
            },
            {
                "name": "group",
                "namespace": null,
                "value": "group"
            },
            {
                "name": "mode",
                "namespace": null,
                "value": "0750"
            }
        ],
        "namespace_acl": {
            "acl": [
                {
                    "accessrights": [
                        "dir_gen_all"
                    ],
                    "accesstype": "allow",
                    "inherit_flags": [
                        "container_inherit"
                    ],
                    "op": "add",
                    "trustee": {
                        "id": "id:2001",
                        "name": "user",
                        "type": "user"
                    }
                }
            ],
            "action": "replace",
            "authoritative": "acl",
            "group": {
                "id": "123",
                "name": "group",
                "type": "group"
            },
            "mode": "0750",
            "owner": {
                "id": "123",
                "name": "user",
                "type": "user"
            }
        }
    }

quota_details:
    description: The quota details.
    type: complex
    returned: When Quota exists.
    contains:
        id:
            description: The ID of the Quota.
            type: str
            sample: "2nQKAAEAAAAAAAAAAAAAQIMCAAAAAAAA"
        enforced:
            description: Whether the Quota is enforced.
            type: bool
            sample: true
        container:
            description: If (true), SMB shares using the quota directory see the quota thresholds as share size.
            type: bool
            sample: true
        type:
            description: The type of Quota.
            type: str
            sample: "directory"
        usage:
            description: The Quota usage.
            type: dict
    sample: {
            "inodes": 1,
            "logical": 0,
            "physical": 2048
    }

filesystem_snapshots:
    description: The filesystem snapshot details.
    type: complex
    returned: When I(list_snapshots) is true.
    contains:
        created:
            description: The creation timestamp.
            type: int
            sample: 1581069354
        expires:
            description: The expiration timestamp.
            type: int
            sample: 2581069354
        name:
            description: The name of the snapshot.
            type: str
            sample: "ansible_snapshot"
        path:
            description: The path of the snapshot.
            type: str
            sample: "/ifs/ansible/ansible281825"
        id:
            description: The id of the snapshot.
            type: int
            sample: 1524
    sample: {
            "alias": null,
            "created": 1636393464,
            "expires": null,
            "has_locks": false,
            "id": 4,
            "name": "SIQ-latest",
            "path": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
            "pct_filesystem": 2.435778242215747e-06,
            "pct_reserve": 0.0,
            "schedule": null,
            "shadow_bytes": 0,
            "size": 4096,
            "state": "active",
            "target_id": null,
            "target_name": null
    }
'''

import re
import copy
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.quota \
    import Quota

LOG = utils.get_logger('filesystem')


class FileSystem(object):
    """Class with Filesystem operations"""

    def __init__(self):
        """Define all the parameters required by this module"""

        self.module_params = utils \
            .get_powerscale_management_host_parameters()
        self.module_params.update(get_filesystem_parameters())

        mutually_exclusive = [['access_control', 'access_control_rights']]
        required_together = [['access_control_rights', 'access_control_rights_state']]
        # initialize the Ansible module
        self.module = AnsibleModule(argument_spec=self.module_params,
                                    supports_check_mode=True,
                                    mutually_exclusive=mutually_exclusive,
                                    required_together=required_together
                                    )
        self.result = dict(
            changed=False,
            create_filesystem='',
            delete_filesystem='',
            modify_filesystem='',
            add_quota='',
            delete_quota='',
            modify_quota='',
            modify_owner='',
            modify_group='',
            quota_details='',
            filesystem_snapshots='',
            filesystem_details=''
        )
        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        LOG.info('Got python SDK instance for provisioning on PowerScale ')

        self.namespace_api = self.isi_sdk.NamespaceApi(self.api_client)
        self.quota_api = self.isi_sdk.QuotaApi(self.api_client)
        self.protocol_api = self.isi_sdk.ProtocolsApi(self.api_client)
        self.zone_summary_api = self.isi_sdk.ZonesSummaryApi(self.api_client)
        self.snapshot_api = self.isi_sdk.SnapshotApi(self.api_client)
        self.auth_api = self.isi_sdk.AuthApi(self.api_client)

    def get_filesystem(self, path):
        """Gets a FileSystem on PowerScale."""
        try:
            resp = self.namespace_api.get_directory_metadata(
                directory_metadata_path=path,
                zone=self.module.params['access_zone'],
                metadata=True).to_dict()
            return resp
        except utils.ApiException as e:
            if str(e.status) == "404":
                log_msg = "Filesystem {0} status is " \
                          "{1}".format(path, e.status)
                LOG.info(log_msg)
                return None
            else:
                error_msg = self.determine_error(error_obj=e)
                error_message = "Failed to get details of Filesystem " \
                                "{0} with error {1} ".format(
                                    path,
                                    str(error_msg))
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

    def get_acl(self, effective_path):
        """Retrieves ACL rights of filesystem"""
        try:
            if not self.module.check_mode:
                filesystem_acl = \
                    (self.namespace_api.get_acl(
                        namespace_path=effective_path,
                        zone=self.module.params['access_zone'],
                        acl=True)).to_dict()
                return filesystem_acl
            return True
        except Exception as e:
            error_message = 'Error %s while retrieving the access control list for ' \
                            'namespace object.' % utils.determine_error(error_obj=e)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_filesystem_snapshots(self, effective_path):
        """Get snapshots for a given filesystem"""
        try:
            snapshot_list = \
                self.snapshot_api.list_snapshot_snapshots().to_dict()
            snapshots = []

            for snap in snapshot_list['snapshots']:
                if snap['path'] == '/' + effective_path:
                    snapshots.append(snap)
            return snapshots
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Failed to get filesystem snapshots ' \
                            'due to error {0}'.format((str(error_msg)))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def determine_path(self):
        path = None
        if self.module.params['path']:
            path = self.module.params['path']
        access_zone = self.module.params['access_zone']
        if access_zone and access_zone.lower() != 'system' and path:
            path = self.get_zone_base_path(access_zone) + path

        # For Filesystem related APIs, the leading '/' is not expected.
        # Hence, we trim it. However, for all other APIs such as exports
        # this '/' is needed in the beginning of the path and we would
        # append it to the path wherever needed in this module.
        effective_path = path[1:]

        return effective_path

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

    def validate_create(self, owner, group):
        if not owner:
            error_message = 'owner is required while creating Filesystem'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

        if 'name' not in owner:
            error_message = 'Please specify a name for the owner.'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

        if group and 'name' not in group:
            error_message = 'Please specify a name for the group.'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_owner_info(self, owner):
        if 'provider_type' in owner:
            owner_provider = owner['provider_type']
        else:
            owner_provider = 'local'
        owner_id = self.get_owner_id(
            name=owner['name'],
            zone=self.module.params['access_zone'],
            provider=owner_provider)['users'][0]['on_disk_user_identity']['id']

        create_owner = {'type': 'user', 'id': owner_id,
                        'name': owner['name']}
        return create_owner

    def get_group_info(self, group):
        if 'provider_type' in group:
            group_provider = group['provider_type']
        else:
            group_provider = 'local'

        group_sid = \
            self.get_group_id(
                name=group['name'],
                zone=self.module.params['access_zone'],
                provider=group_provider)['groups'][0]['sid']['id']
        on_disk_id = self.get_identity_on_disk_id(sid=group_sid,
                                                  zone=self.module.params['access_zone'])
        group_id = on_disk_id if on_disk_id else group_sid

        create_group = {'type': 'group', 'id': group_id,
                        'name': group['name']}
        return create_group

    def create_filesystem(self, path, recursive, acl, acl_rights, quota, owner, group):
        """Creates a FileSystem on PowerScale."""
        try:
            self.validate_create(owner=owner,
                                 group=group)
            create_owner = self.get_owner_info(owner=owner)
            create_group = None
            if group:
                create_group = self.get_group_info(group=group)
            info_message = "Attempting to create new FS {0}".format(path)
            LOG.info(info_message)
            if not self.module.check_mode:
                if acl is not None:
                    self.namespace_api.create_directory(
                        path,
                        x_isi_ifs_target_type='container',
                        recursive=recursive,
                        x_isi_ifs_access_control=acl,
                        overwrite=False)
                else:
                    self.namespace_api.create_directory(
                        path,
                        x_isi_ifs_target_type='container',
                        recursive=recursive,
                        overwrite=False)
                if quota is not None and quota['quota_state'] == 'present':
                    self.create_quota(quota, path)
                permissions = \
                    self.isi_sdk.NamespaceAcl(
                        authoritative='mode',
                        owner=create_owner,
                        group=create_group)
                self.namespace_api.set_acl(namespace_path=path,
                                           zone=self.module.params['access_zone'],
                                           acl=True,
                                           namespace_acl=permissions)

                if acl_rights:
                    self.set_access_control_rights(acl_rights, path)
            return True
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Creation of Filesystem {0} failed ' \
                            'with error: {1}'.format(path, str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def set_access_control_rights(self, acl_rights, path):
        """Sets the ACL permissions on specified filesystem."""
        try:
            acl = self.get_acl_permissions(acl_rights)
            if not self.module.check_mode:
                permissions = self.isi_sdk.NamespaceAcl(
                    authoritative='acl',
                    action="update",
                    acl=acl)
                self.namespace_api.set_acl(namespace_path=path,
                                           zone=self.module.params['access_zone'],
                                           acl=True,
                                           namespace_acl=permissions)
            return True
        except Exception as e:
            error_message = 'Setting ACL rights of Filesystem %s failed ' \
                            'with error: %s' % (path, utils.determine_error(error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete_filesystem(self, path, access_zone=None, recursive_force_delete=False):
        """Deletes a FileSystem on PowerScale.
           When recursive_force_delete is true it deletes all sub files and folders recursively.
        """
        try:
            # Check for NFS exports
            nfs_exports = self.protocol_api.list_nfs_exports(
                path='/' + path, zone=access_zone).to_dict()
            if nfs_exports['exports']:
                error_message = 'The Filesystem path {0} has NFS ' \
                                'exports. Hence, deleting this directory ' \
                                'is not safe'.format(path)
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
            # Check for SMB shares
            smb_shares = self.protocol_api.list_smb_shares(zone=access_zone).to_dict()
            for share in smb_shares['shares']:
                if share['path'] == '/' + path:
                    error_message = 'The Filesystem path {0} has SMB ' \
                                    'Shares. Hence, deleting this directory ' \
                                    'is not safe'.format(path)
                    LOG.error(error_message)
                    self.module.fail_json(msg=error_message)
            if not self.module.check_mode:
                self.namespace_api.delete_directory(directory_path=path, recursive=recursive_force_delete)
            return True
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Deletion of Filesystem {0} failed ' \
                            'with error: {1}'.format(path, str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def modify_acl(self, path, mode):
        """Modifies Filesystem ACL on PowerScale."""
        try:
            if not self.module.check_mode:
                if mode == 'posix':
                    acl = self.module.params['access_control']
                    new_mode = self.isi_sdk.NamespaceAcl(
                        authoritative='mode',
                        mode=acl)
                    self.namespace_api.set_acl(namespace_path=path,
                                               zone=self.module.params['access_zone'],
                                               acl=True,
                                               namespace_acl=new_mode)
                else:
                    acl_rights = self.module.params['access_control_rights']
                    if acl_rights:
                        self.set_access_control_rights(acl_rights, path)

            return True
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Modification of ACL on path {0} failed ' \
                            'with error: {1}'.format(path, str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_container_param(self, quota):
        if 'container' in quota and quota['container'] is not None:
            container = quota['container']
        else:
            container = False
        return container

    def check_quota_params(self, quota):
        if 'cap_unit' in quota and quota['cap_unit'] is not None:
            cap_unit = quota['cap_unit']
        else:
            cap_unit = 'GB'

        enforced = False
        if 'advisory_limit_size' in quota and \
                quota['advisory_limit_size'] is not None:
            advisory_limit = utils.get_size_bytes(
                quota['advisory_limit_size'], cap_unit)
        else:
            advisory_limit = None

        if 'hard_limit_size' in quota and \
                quota['hard_limit_size'] is not None:
            hard_limit = utils.get_size_bytes(quota['hard_limit_size'],
                                              cap_unit)
            enforced = True
        else:
            hard_limit = None

        if 'soft_limit_size' in quota and \
                quota['soft_limit_size'] is not None:
            soft_limit = utils.get_size_bytes(quota['soft_limit_size'],
                                              cap_unit)
            enforced = True
            soft_grace = 604800
        else:
            soft_limit = None
            soft_grace = None

        return advisory_limit, hard_limit, enforced, soft_limit, soft_grace

    def get_quota_update_param(self, quota):
        """Returns the update params for Quota"""
        try:
            if quota is not None and quota['quota_state'] == 'present':
                advisory_limit, hard_limit, enforced, soft_limit, soft_grace = \
                    self.check_quota_params(quota=quota)

                container = self.get_container_param(quota)

                if THRESHOLD_PARAM in quota and \
                        quota[THRESHOLD_PARAM] is not None:
                    include_dp_overhead = \
                        quota[THRESHOLD_PARAM]
                else:
                    include_dp_overhead = None

                threshold = self.isi_sdk.QuotaQuotaThresholds(
                    advisory=advisory_limit,
                    hard=hard_limit,
                    soft=soft_limit,
                    soft_grace=soft_grace
                )

                quota_params = {'enforced': enforced,
                                'container': container,
                                'thresholds_on':
                                    include_dp_overhead,
                                'thresholds': threshold}
                quota_update_param = self.isi_sdk.QuotaQuota(**quota_params)

            return quota_update_param
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Creation of Quota update param failed ' \
                            'with error: {0}'.format(str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def modify_quota(self, quota, path):
        """Modifies Filesystem Quota on PowerScale"""
        try:
            LOG.info('Modifying Quota..')
            get_quotas = self.quota_api.list_quota_quotas(path='/' + path,
                                                          type='directory')
            if not self.module.check_mode:
                quota_id = get_quotas.quotas[0].id
                updated_quota = self.get_quota_update_param(quota)
                self.quota_api.update_quota_quota(
                    quota_quota=updated_quota,
                    quota_quota_id=quota_id)
            return True
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Modification of Quota on path {0} failed ' \
                            'with error: {1}'.format(path, str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete_quota(self, path):
        """Deletes Filesystem Quota on PowerScale"""
        try:
            if not self.module.check_mode:
                self.quota_api.delete_quota_quotas(
                    path='/' + path,
                    type='directory')
            return True
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Deletion of Quota on path {0} failed ' \
                            'with error: {1}'.format(path, str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_quota_param(self, quota, path):
        """Returns the object needed to create Quota"""
        try:
            if quota is not None and quota['quota_state'] == 'present':
                advisory_limit, hard_limit, enforced, soft_limit, soft_grace = \
                    self.check_quota_params(quota=quota)

                if 'include_snap_data' in quota and \
                        quota['include_snap_data'] is not None:
                    include_snap_data = quota['include_snap_data']
                else:
                    include_snap_data = False

                container = self.get_container_param(quota)
                threshold = self.isi_sdk.QuotaQuotaThresholds(
                    advisory=advisory_limit,
                    hard=hard_limit,
                    soft=soft_limit,
                    soft_grace=soft_grace
                )

                quota_create_params = {
                    'enforced': enforced,
                    'include_snapshots': include_snap_data,
                    'path': path,
                    'thresholds': threshold,
                    'container': container, 'type': 'directory'
                }

                if THRESHOLD_PARAM in quota and \
                        quota[THRESHOLD_PARAM]:
                    quota_create_params[
                        'thresholds_on'] = \
                        quota[THRESHOLD_PARAM]

                quota_param = self.isi_sdk.QuotaQuotaCreateParams(
                    **quota_create_params)

            return quota_param
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Creation of Quota param failed ' \
                            'with error: {0}'.format(str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def create_quota(self, quota, path):
        """Creates a Quota"""
        try:
            if not self.module.check_mode:
                quota_param = self.get_quota_param(quota, '/' + path)
                self.quota_api.create_quota_quota(
                    quota_quota=quota_param)
            return True
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Creation of Quota {0} failed ' \
                            'with error: {1}'.format(path, str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_acl_posix(self, access_control):
        if access_control == 'private_read':
            acl_posix = '0550'
            new_authoritative = 'acl'
        elif access_control == 'private':
            acl_posix = '0770'
            new_authoritative = 'acl'
        elif access_control == 'public_read':
            acl_posix = '0775'
            new_authoritative = 'acl'
        elif access_control == \
                'public_read_write' or self.module.params['access_control'] == 'public':
            acl_posix = '0777'
            new_authoritative = 'acl'
        else:
            acl_posix = access_control
            new_authoritative = 'mode'

        return acl_posix, new_authoritative

    def is_acl_modified(self, effective_path):
        """Determines if ACLs are modified."""
        try:
            LOG.info('Determining if the ACLs are modified..')
            filesystem_acl = self.get_acl(effective_path)
            if not isinstance(filesystem_acl, dict):
                return True, None

            info_message = 'ACL of the filesystem on ' \
                           'the array is %s' % filesystem_acl['acl']
            LOG.info(info_message)
            if self.module.params['access_control']:
                acl_posix, new_authoritative = \
                    self.get_acl_posix(
                        access_control=self.module.params['access_control'])

                info_message = 'ACL provided in the ' \
                               'playbook is {0}'.format(acl_posix)
                LOG.info(info_message)

                filesystem_acl_error_message = 'Modification of ACL from Ansible ' \
                                               'modules is only supported from ' \
                                               'POSIX to POSIX mode bits.'

                if (filesystem_acl['authoritative'] == 'acl'
                    and new_authoritative == 'mode') or \
                        (filesystem_acl['authoritative'] == 'mode'
                         and new_authoritative == 'acl') or \
                        (filesystem_acl['authoritative'] == 'acl'
                         and new_authoritative == 'acl' and filesystem_acl['mode'] != acl_posix):
                    LOG.error(filesystem_acl_error_message)
                    self.module.fail_json(msg=filesystem_acl_error_message)

                if acl_posix != filesystem_acl['mode']:
                    return True, "posix"
            if self.module.params['access_control_rights']:
                if self.is_acl_rights_modified(filesystem_acl, self.module.params['access_control_rights']):
                    return True, "acl"

            return False, None

        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Error {0} while determining if ' \
                            'ACLs are modified'.format(str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def is_acl_rights_modified(self, filesystem_acl, acl_rights):
        """Determines if acl rights of filesystem are modified"""
        acl_trustee = []
        trustee_id = self.get_trustee_id(acl_rights['trustee']['name'],
                                         acl_rights['trustee']['type'],
                                         self.module.params['access_zone'],
                                         acl_rights['trustee']['provider_type'])
        for acl in filesystem_acl['acl']:
            if not acl['trustee']['id']:
                continue
            acl_trustee.append(acl['trustee']['id'] + ":" + acl['accesstype'])
            if acl['trustee']['id'] + ":" + acl['accesstype'] == \
                    trustee_id + ":" + acl_rights['access_type'] and \
                    (self.module.params['access_control_rights_state'] == 'add' and
                     self.is_access_or_inherit_modified(acl_rights, acl)):
                return True
        if trustee_id + ":" + acl_rights['access_type'] not in acl_trustee:
            if self.module.params['access_control_rights_state'] == 'add':
                return True
        else:
            if self.module.params['access_control_rights_state'] == 'remove':
                return True

    def is_access_or_inherit_modified(self, acl_rights, acl):
        """Determines if access rights or inherit flags of ACL are modified"""
        return (acl_rights['access_rights'] and
                (list(set(acl_rights['access_rights']) - set(acl['accessrights']))) or
                (acl_rights['inherit_flags'] and (set(acl_rights['inherit_flags']) - set(acl['inherit_flags']))) or
                acl_rights['access_type'] != acl['accesstype'])

    def check_quota_param_modification(self, quota, filesystem_quota):
        if 'cap_unit' in quota and quota['cap_unit'] is not None:
            cap_unit = quota['cap_unit']
        else:
            cap_unit = 'GB'
        if 'advisory_limit_size' in quota and \
                quota['advisory_limit_size'] is not None:
            advisory_limit_size = utils.get_size_bytes(
                quota['advisory_limit_size'], cap_unit)
            if advisory_limit_size != \
                    filesystem_quota['quotas'][0]['thresholds'][
                        'advisory']:
                return True
        if 'soft_limit_size' in quota and \
                quota['soft_limit_size'] is not None:
            soft_limit_size = utils.get_size_bytes(
                quota['soft_limit_size'], cap_unit)
            if soft_limit_size != \
                    filesystem_quota['quotas'][0]['thresholds'][
                        'soft']:
                return True
        if 'hard_limit_size' in quota and \
                quota['hard_limit_size'] is not None:
            hard_limit_size = utils.get_size_bytes(
                quota['hard_limit_size'], cap_unit)
            if hard_limit_size != filesystem_quota['quotas'][0]['thresholds']['hard']:
                return True

    def is_quota_modified(self, filesystem_quota):
        """Determines if Quota is modified"""
        LOG.info('Determining if Quota is modified...')
        if self.module.params['quota'] is not None \
                and filesystem_quota is not None and filesystem_quota[
            'quotas'] and \
                self.module.params['quota']['quota_state'] == 'present':
            quota = self.module.params['quota']
            if 'include_snap_data' in quota and \
                    quota['include_snap_data'] is not None:
                include_snap_data = quota['include_snap_data']
                if include_snap_data != \
                        filesystem_quota['quotas'][0]['include_snapshots']:
                    error_message = 'The value of include_snap_data does ' \
                                    'not match the state on the array. ' \
                                    'Modifying include_snap_data is ' \
                                    'not supported.'
                    LOG.error(error_message)
                    self.module.fail_json(msg=error_message)
            if THRESHOLD_PARAM in quota and \
                    quota[THRESHOLD_PARAM] is not None:
                include_data_protection_overhead = \
                    quota[THRESHOLD_PARAM]
                if include_data_protection_overhead != \
                        filesystem_quota['quotas'][0][
                            'thresholds_on']:
                    return True
            return self.check_quota_param_modification(quota=quota, filesystem_quota=filesystem_quota)

    def validate_input(self, quota):
        """Valid input parameters"""
        global THRESHOLD_PARAM
        if 'quota' in self.module.params \
                and self.module.params['quota'] is not None:
            if self.module.params['quota']['quota_state'] is None:
                self.module.fail_json(msg='quota_state is required while '
                                          'creating, deleting or modifying '
                                          'a quota')
            if 'cap_unit' in self.module.params['quota'] \
                    and self.module.params['quota']['cap_unit'] is not None and \
                    self.module.params['quota']['cap_unit'] not in ('MB', 'mb', 'GB', 'gb', 'TB', 'tb'):
                self.module.fail_json(msg='Invalid cap_unit provided, '
                                          'only MB, GB and TB are '
                                          'supported.')

            VALIDATE_THRESHOLD = utils.validate_threshold_overhead_parameter(quota)
            if VALIDATE_THRESHOLD and not \
                    VALIDATE_THRESHOLD["param_is_valid"]:
                self.module.fail_json(msg=VALIDATE_THRESHOLD["error_message"])
            THRESHOLD_PARAM = "thresholds_on"

        if self.module.params['path'] and not self.module.params['path'].startswith('/'):
            self.module.fail_json(msg='Invalid path. '
                                      'The path provided must '
                                      'start with /')

        self.validate_access_control_rights(self.module.params['access_control_rights'],
                                            self.module.params['access_control_rights_state'])

    def validate_access_control_rights(self, acl_rights, acl_rights_state):
        """Validates access control rights input object"""
        if acl_rights and acl_rights_state == 'add' and \
                (acl_rights['access_rights'] is None and
                 acl_rights['inherit_flags'] is None):
            self.module.fail_json(msg='Please specify access_rights or '
                                      'inherit_flags to set ACL')

    def get_trustee_id(self, trustee_name, type, access_zone, provider):
        if type == 'user':
            return self.get_owner_id(name=trustee_name,
                                     zone=access_zone,
                                     provider=provider)['users'][0]['on_disk_user_identity']['id']
        elif type == 'group':
            group_sid = self.get_group_id(name=trustee_name,
                                          zone=access_zone,
                                          provider=provider)['groups'][0]['sid']['id']
            on_disk_id = self.get_identity_on_disk_id(sid=group_sid, zone=access_zone)
            return on_disk_id if on_disk_id else group_sid
        else:
            return self.get_wellknown_id(name=trustee_name)['wellknowns'][0]['id']

    def get_duplicated_trustee_id(self, trustee, access_zone, provider):
        """Returns duplicated trustee id for user or group"""
        if trustee['type'] == 'user':
            user = self.get_owner_id(name=trustee['name'],
                                     zone=access_zone,
                                     provider=provider)['users'][0]
            return user['uid']['id'] if user['uid']['id'] != trustee['id'] else user['sid']['id']
        else:
            group = self.get_group_id(name=trustee['name'],
                                      zone=access_zone,
                                      provider=provider)['groups'][0]
            return group['gid']['id'] if group['gid']['id'] != trustee['id'] else group['sid']['id']

    def get_acl_permissions(self, acl_rights):
        """Returns ACL permissions"""
        try:
            permissions = []
            acl_state = self.module.params['access_control_rights_state']
            acl_obj = utils.get_acl_object()
            acl_obj.op = "add"
            if acl_state and acl_state == 'remove':
                acl_obj.op = "delete"
            trustee_type = acl_rights['trustee']['type']
            trustee_id = \
                self.get_trustee_id(acl_rights['trustee']['name'],
                                    trustee_type,
                                    self.module.params['access_zone'],
                                    acl_rights['trustee']['provider_type'])
            trustee_type = trustee_type if trustee_type else "user"
            trustee = {"name": acl_rights['trustee']['name'], "id": trustee_id, "type": trustee_type}
            acl_obj.trustee = trustee
            acl_obj.accesstype = acl_rights['access_type']
            acl_obj.accessrights = acl_rights['access_rights']
            acl_obj.inherit_flags = acl_rights['inherit_flags']
            permissions.append(acl_obj)

            # allow customer to remove duplicated trustee
            if acl_obj.op == "delete" and trustee_type in ['user', 'group']:
                trustee_id_duplicated = \
                    self.get_duplicated_trustee_id(trustee,
                                                   self.module.params['access_zone'],
                                                   acl_rights['trustee']['provider_type'])
                acl_obj_duplicated = utils.get_acl_object()
                acl_obj_duplicated.op = "delete"
                trustee_duplicated = {"name": acl_rights['trustee']['name'],
                                      "id": trustee_id_duplicated, "type": trustee_type}
                acl_obj_duplicated.trustee = trustee_duplicated
                acl_obj_duplicated.accesstype = acl_rights['access_type']
                acl_obj_duplicated.accessrights = acl_rights['access_rights']
                acl_obj_duplicated.inherit_flags = acl_rights['inherit_flags']
                permissions.append(acl_obj_duplicated)

            return permissions
        except Exception as e:
            error_message = 'Error %s while retrieving ACL object instance ' % \
                            utils.determine_error(error_obj=e)
            self.module.fail_json(msg=error_message)

    def determine_error(self, error_obj):
        """Determine the error message to return"""
        if isinstance(error_obj, utils.ApiException):
            error = re.sub("[\n \"]+", ' ', str(error_obj.body))
        else:
            error = str(error_obj)
        return error

    def get_identity_on_disk_id(self, sid, zone):
        """Get the Identity Details in PowerScale"""
        try:
            resp = self.auth_api.get_mapping_identity(
                mapping_identity_id=sid,
                zone=zone).to_dict()
            for identity in resp['identities'][0]['targets']:
                if identity['on_disk']:
                    return identity['target']['id']
            return None
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = f'Failed to get the identity id for {sid} '\
                            f'in zone {zone} due to error {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_owner_id(self, name, zone, provider):
        """Get the User Account Details in PowerScale"""
        try:
            resp = self.auth_api.get_auth_user(
                auth_user_id='USER:' + name,
                zone=zone, provider=provider).to_dict()
            return resp
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Failed to get the owner id for ' \
                            '%s in zone %s and ' \
                            'provider %s due ' \
                            'to error %s' % (name, zone, provider,
                                             error_msg)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_group_id(self, name, zone, provider):
        """Get the group account details in PowerScale"""
        try:
            resp = self.auth_api.get_auth_group(
                auth_group_id='GROUP:' + name,
                zone=zone, provider=provider).to_dict()

            return resp
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Failed to get the group id for group ' \
                            '{0} in zone {1} and ' \
                            'provider {2} due ' \
                            'to error {3}'.format(name, zone, provider,
                                                  str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_wellknown_id(self, name):
        """Get the wellknown account details in PowerScale"""
        try:
            resp = self.auth_api.get_auth_wellknowns().to_dict()
            for wellknown in resp['wellknowns']:
                if wellknown['name'].lower() == name.lower():
                    return self.auth_api.get_auth_wellknown(
                        auth_wellknown_id=wellknown['id']).to_dict()
            error_message = (f'Wellknown {name} does not exist. '
                             f'Provide valid wellknown.')
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = (f'Failed to get the wellknown id for wellknown '
                             f'{name} due to error {str(error_msg)}.')
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def is_owner_modified(self, effective_path, owner):
        """Determines if the Owner for the FS is modified"""
        try:
            if not owner:
                return False
            LOG.info('Determining if owner is modified..')
            if 'name' not in owner:
                error_message = 'Please specify a name for the owner.'
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
            if 'provider_type' in owner:
                owner_provider = owner['provider_type']
            else:
                owner_provider = 'local'

            owner_id = self.get_owner_id(
                name=owner['name'],
                zone=self.module.params['access_zone'],
                provider=owner_provider)['users'][0]['on_disk_user_identity']['id']

            owner = {'type': 'user', 'id': owner_id,
                     'name': owner['name']}

            acl = self.get_acl(effective_path)
            modified = False
            if isinstance(acl, dict):
                file_uid = acl['owner']['id']
                info_message = 'The user ID fetched from playbook is ' \
                               '{0} and the user ID on ' \
                               'the file is {1}'.format(owner_id, file_uid)
                LOG.info(info_message)
                modified = (owner_id != file_uid)

            if modified:
                LOG.info('Modifying owner..')
                self.modify_owner(owner, effective_path)
                return True

        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Failed to determine if owner ' \
                            'is modified due to ' \
                            'error {0}'.format(str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def is_group_modified(self, effective_path, group):
        """Determines if the Group for the FS is modified"""
        try:
            if not group:
                return False
            LOG.info('Determining if group is modified..')
            if 'name' not in group:
                error_message = 'Please specify a name for the group.'
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
            if 'provider_type' in group:
                group_provider = group['provider_type']
            else:
                group_provider = 'local'

            group_sid = self.get_group_id(
                name=group['name'],
                zone=self.module.params['access_zone'],
                provider=group_provider)['groups'][0]['sid']['id']
            on_disk_id = self.get_identity_on_disk_id(
                sid=group_sid,
                zone=self.module.params['access_zone'])
            group_id = on_disk_id if on_disk_id else group_sid

            group = {'type': 'group', 'id': group_id,
                     'name': group['name']}

            acl = self.get_acl(effective_path)
            modified = False
            if isinstance(acl, dict):
                file_gid = acl['group']['id']
                info_message = 'The group ID fetched from playbook is ' \
                               '{0} and the group ID on ' \
                               'the file is {1}'.format(group_id, file_gid)
                LOG.info(info_message)
                modified = (group_id != file_gid)

            if modified:
                LOG.info('Modifying group..')
                self.modify_group(group, effective_path)
                return True
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Failed to determine if group ' \
                            'is modified due to ' \
                            'error {0}'.format(str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def modify_owner(self, owner, effective_path):
        """Modifies the FS owner"""
        try:
            if not self.module.check_mode:
                permissions = self.isi_sdk.NamespaceAcl(
                    authoritative='mode',
                    owner=owner)
                self.namespace_api.set_acl(namespace_path=effective_path,
                                           zone=self.module.params['access_zone'],
                                           acl=True,
                                           namespace_acl=permissions)
            return True
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Failed to modify owner ' \
                            'due to error {0}'.format(str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def modify_group(self, group, effective_path):
        """Modifies the FS group"""
        try:
            if not self.module.check_mode:
                permissions = self.isi_sdk.NamespaceAcl(
                    authoritative='mode',
                    group=group)
                self.namespace_api.set_acl(namespace_path=effective_path,
                                           zone=self.module.params['access_zone'],
                                           acl=True,
                                           namespace_acl=permissions)
            return True
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Failed to modify group ' \
                            'due to error {0}'.format(str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_quota(self, effective_path):
        """Returns the quota object"""
        try:
            quota = Quota(self.quota_api,
                          self.module).get_quota(effective_path)
            return quota
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Failed to get quota ' \
                            'due to error {0}'.format(str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)


def get_filesystem_parameters():
    return dict(
        path=dict(required=True, type='str'),
        access_zone=dict(required=False, type='str',
                         default='System'),
        owner=dict(required=False, type='dict'),
        group=dict(required=False, type='dict'),
        access_control=dict(required=False, type='str'),
        access_control_rights=dict(type='dict', options=dict(
            access_rights=dict(type='list', elements='str'),
            access_type=dict(required=True, type='str', choices=['allow', 'deny']),
            inherit_flags=dict(type='list', elements='str',
                               choices=['object_inherit', 'container_inherit',
                                        'inherit_only', 'no_prop_inherit',
                                        'inherited_ace']),
            trustee=dict(required=True, type='dict',
                         options=dict(name=dict(type='str', required=True),
                                      type=dict(type='str', choices=['user', 'group', 'wellknown'], default='user'),
                                      provider_type=dict(type='str', default='local'))))),
        access_control_rights_state=dict(required=False, type='str',
                                         choices=['add', 'remove']),
        recursive=dict(required=False, type='bool',
                       default=True),
        recursive_force_delete=dict(required=False, type='bool',
                                    default=False),
        quota=dict(type='dict',
                   options=dict(include_snap_data=dict(type='bool', default=False),
                                container=dict(type='bool', default=False),
                                include_data_protection_overhead=dict(type='bool'),
                                thresholds_on=dict(type='str',
                                                   choices=['app_logical_size',
                                                            'fs_logical_size',
                                                            'physical_size']),
                                advisory_limit_size=dict(type='int'),
                                soft_limit_size=dict(type='int'),
                                hard_limit_size=dict(type='int'),
                                quota_state=dict(type='str', choices=['present', 'absent']),
                                cap_unit=dict(type='str', choices=['GB', 'TB']))),

        state=dict(required=True, type='str',
                   choices=['present', 'absent']),
        list_snapshots=dict(required=False, type='bool',
                            default=False),
    )


class FilesystemExitHandler():
    def handle(self, filesystem_obj):
        if filesystem_obj.result['create_filesystem'] or filesystem_obj.result['delete_filesystem'] or \
                filesystem_obj.result['modify_filesystem'] or filesystem_obj.result['add_quota'] \
                or filesystem_obj.result['delete_quota'] or filesystem_obj.result['modify_quota'] or \
                filesystem_obj.result['modify_owner'] or filesystem_obj.result['modify_group']:
            filesystem_obj.result['changed'] = True

        # Finally update the module result!
        filesystem_obj.module.exit_json(**filesystem_obj.result)


class FilesystemDetailsHandler():
    def handle(self, filesystem_obj, filesystem_params, effective_path):
        if filesystem_params['state'] == 'present':
            filesystem_obj.result['filesystem_details'] = filesystem_obj.get_filesystem(path=effective_path)
            if filesystem_obj.result.get('filesystem_details') is None:
                filesystem_obj.result['filesystem_details'] = {}
            filesystem_obj.result['filesystem_details'].update(
                namespace_acl=filesystem_obj.get_acl(effective_path))
            filesystem_obj.result['quota_details'] = Quota(filesystem_obj.quota_api,
                                                           filesystem_obj.module).get_quota(effective_path)
            if filesystem_obj.module.params['list_snapshots']:
                filesystem_obj.result['filesystem_snapshots'] = \
                    filesystem_obj.get_filesystem_snapshots(effective_path)

        FilesystemExitHandler().handle(filesystem_obj)


class FilesystemDeleteHandler():
    def handle(self, filesystem_obj, filesystem_params, filesystem_details, effective_path):
        if filesystem_params['state'] == 'absent' and filesystem_details:
            filesystem_obj.result['delete_filesystem'] = filesystem_obj.delete_filesystem(
                effective_path,
                filesystem_params['access_zone'],
                filesystem_params['recursive_force_delete'])
        FilesystemDetailsHandler().handle(filesystem_obj, filesystem_params, effective_path)


class FilesystemDeleteQuotaHandler():
    def handle(self, filesystem_obj, filesystem_params, filesystem_details, effective_path,
               filesystem_quota, quota):
        # There is a Quota on the filesystem.
        # The user specified a Quota in the playbook to be removed.
        if filesystem_quota is not None and 'quotas' in filesystem_quota and \
                filesystem_quota['quotas'] and quota is not None and \
                filesystem_params['quota']['quota_state'] == 'absent':
            filesystem_obj.result['delete_quota'] = filesystem_obj.delete_quota(effective_path)
        FilesystemDeleteHandler().handle(
            filesystem_obj=filesystem_obj, filesystem_params=filesystem_params,
            filesystem_details=filesystem_details, effective_path=effective_path)


class FilesystemCreateQuotaHandler():
    def handle(self, filesystem_obj, filesystem_params, filesystem_details, effective_path,
               filesystem_quota, quota):
        # There is no Quota on the filesystem.
        # The user specified a Quota in the playbook to be created.
        if filesystem_quota is not None and 'quotas' in filesystem_quota \
                and not filesystem_quota['quotas'] and filesystem_details is not \
                None and quota is not None and \
                filesystem_params['quota']['quota_state'] == 'present':
            filesystem_obj.result['add_quota'] = filesystem_obj.create_quota(quota, effective_path)
        FilesystemDeleteQuotaHandler().handle(
            filesystem_obj=filesystem_obj, filesystem_params=filesystem_params,
            filesystem_details=filesystem_details, effective_path=effective_path,
            filesystem_quota=filesystem_quota, quota=quota)


class FilesystemModifyQuotaHandler():
    def handle(self, filesystem_obj, filesystem_params, filesystem_details, effective_path,
               filesystem_quota, is_quota_modified, quota):
        if filesystem_params["state"] == "present" and is_quota_modified:
            filesystem_obj.result['modify_quota'] = filesystem_obj.modify_quota(quota,
                                                                                effective_path)
        FilesystemCreateQuotaHandler().handle(
            filesystem_obj=filesystem_obj, filesystem_params=filesystem_params,
            filesystem_details=filesystem_details, effective_path=effective_path,
            filesystem_quota=filesystem_quota, quota=quota)


class FilesystemModifyACLHandler():
    def handle(self, filesystem_obj, filesystem_params, filesystem_details, effective_path,
               filesystem_quota, is_acl_modified, is_quota_modified, mode, quota):
        if filesystem_params["state"] == "present" and is_acl_modified:
            LOG.info('Modifying ACL..')
            filesystem_obj.result['modify_filesystem'] = filesystem_obj.modify_acl(effective_path, mode)
        FilesystemModifyQuotaHandler().handle(
            filesystem_obj=filesystem_obj, filesystem_params=filesystem_params,
            filesystem_details=filesystem_details, effective_path=effective_path,
            filesystem_quota=filesystem_quota,
            is_quota_modified=is_quota_modified, quota=quota)


class FilesystemCreateHandler():
    def handle(self, filesystem_obj, filesystem_params, filesystem_details, effective_path,
               filesystem_quota, is_acl_modified, is_quota_modified, mode, quota):
        if filesystem_params["state"] == "present" and not filesystem_details:
            LOG.info('Creating Filesystem...')
            filesystem_obj.result['create_filesystem'] = filesystem_obj.create_filesystem(
                path=effective_path,
                recursive=filesystem_params['recursive'],
                acl=filesystem_params['access_control'],
                acl_rights=filesystem_params['access_control_rights'],
                quota=quota,
                owner=filesystem_params['owner'],
                group=filesystem_params['group'])
        FilesystemModifyACLHandler().handle(
            filesystem_obj=filesystem_obj, filesystem_params=filesystem_params,
            filesystem_details=filesystem_details, effective_path=effective_path,
            filesystem_quota=filesystem_quota, is_acl_modified=is_acl_modified,
            is_quota_modified=is_quota_modified, mode=mode, quota=quota)


class FilesystemHandler():
    def handle(self, filesystem_obj, filesystem_params):
        quota = copy.deepcopy(filesystem_params['quota'])
        filesystem_obj.validate_input(quota)
        effective_path = filesystem_obj.determine_path()
        filesystem_details = filesystem_obj.get_filesystem(path=effective_path)
        filesystem_quota = filesystem_obj.get_quota(effective_path)

        is_acl_modified = False
        is_quota_modified = False
        mode = None
        if filesystem_details:
            is_acl_modified, mode = filesystem_obj.is_acl_modified(effective_path)
            is_quota_modified = filesystem_obj.is_quota_modified(filesystem_quota)
            filesystem_obj.result['modify_owner'] = \
                filesystem_obj.is_owner_modified(effective_path, filesystem_params['owner'])
            filesystem_obj.result['modify_group'] = \
                filesystem_obj.is_group_modified(effective_path, filesystem_params['group'])
        FilesystemCreateHandler().handle(
            filesystem_obj=filesystem_obj, filesystem_params=filesystem_params,
            filesystem_details=filesystem_details, effective_path=effective_path,
            filesystem_quota=filesystem_quota, is_acl_modified=is_acl_modified,
            is_quota_modified=is_quota_modified, mode=mode, quota=quota)


def main():
    """ Create PowerScale Filesystem object and perform action on it
        based on user input from playbook."""
    obj = FileSystem()
    FilesystemHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
