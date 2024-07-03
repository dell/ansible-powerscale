#!/usr/bin/python
# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing NFS Default Settings on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: nfs_default_settings
version_added: '2.2.0'
short_description:  Manage NFS default settings on a PowerScale Storage System
description:
- Managing NFS default settings on an PowerScale system includes getting details of an NFS default settings
  and modifying different attributes of the NFS default settings.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Ananthu S Kuttattu(@kuttattz) <ansible.team@dell.com>

options:
  map_root:
    description:
    - User and group mapping.
    - Map incoming root users to a specific user and/or group ID.
    required: False
    type: dict
    suboptions:
      enabled:
        description:
        - Indicates if user mapping is enabled or not.
        - True if the user mapping is applied.
        type: bool
        default: True
      primary_group:
        description:
        - Specifies name of the primary group.
        required: False
        type: str
      secondary_groups:
        description:
        - Specifies name and state of the secondary groups.
        type: list
        elements: dict
        required: False
        suboptions:
          name:
            description:
            - Name of the group.
            type: str
            required: True
          state:
            description:
            - State of the secondary group.
            type: str
            choices: ['present', 'absent']
            default: 'present'
      user:
        description:
        - Specifies name of the user.
        required: False
        type: str
  map_non_root:
    description:
    - User and group mapping.
    - Map non-root users to a specific user and/or group ID.
    required: False
    type: dict
    suboptions:
      enabled:
        description:
        - Indicates if user mapping is enabled or not.
        - True if the user mapping is applied.
        type: bool
        default: True
      primary_group:
        description:
        - Specifies name of the primary group.
        required: False
        type: str
      secondary_groups:
        description:
        - Specifies name and state of the secondary groups.
        type: list
        elements: dict
        required: False
        suboptions:
          name:
            description:
            - Name of the group.
            type: str
            required: True
          state:
            description:
            - State of the secondary group.
            type: str
            choices: ['present', 'absent']
            default: 'present'
      user:
        description:
        - Specifies name of the user.
        required: False
        type: str
  map_failure:
    description:
    - User and group mapping.
    - Map users to a specific user and/or group ID after a failed auth attempt.
    required: False
    type: dict
    suboptions:
      enabled:
        description:
        - Indicates if user mapping is enabled or not.
        - True if the user mapping is applied.
        type: bool
        default: True
      primary_group:
        description:
        - Specifies name of the primary group.
        required: False
        type: str
      secondary_groups:
        description:
        - Specifies name and state of the secondary groups.
        type: list
        elements: dict
        required: False
        suboptions:
          name:
            description:
            - Name of the group.
            type: str
            required: True
          state:
            description:
            - State of the secondary group.
            type: str
            choices: ['present', 'absent']
            default: 'present'
      user:
        description:
        - Specifies name of the user.
        required: False
        type: str
  file_name_max_size:
    description:
    - Specifies the reported maximum length of a file name.
    - This parameter does not affect server behavior, but is included to accommodate legacy client requirements.
    type: dict
    required: False
    suboptions:
      size_value:
        description:
        - Size value.
        type: int
        required: true
      size_unit:
        description:
        - Unit for the size value.
        type: str
        required: true
        choices: ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
  block_size:
    description:
    - Specifies the block size returned by the NFS statfs procedure.
    type: dict
    required: False
    suboptions:
      size_value:
        description:
        - Size value.
        type: int
        required: true
      size_unit:
        description:
        - Unit for the size value.
        type: str
        required: true
        choices: ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
  directory_transfer_size:
    description:
    - Specifies the preferred size for directory read operations.
    - This value is used to advise the client of optimal settings for the server, but is not enforced.
    type: dict
    required: False
    suboptions:
      size_value:
        description:
        - Size value.
        type: int
        required: true
      size_unit:
        description:
        - Unit for the size value.
        type: str
        required: true
        choices: ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
  read_transfer_max_size:
    description:
    - Specifies the maximum buffer size that clients should use on NFS read requests.
    - This value is used to advise the client of optimal settings for the server, but is not enforced.
    type: dict
    required: False
    suboptions:
      size_value:
        description:
        - Size value.
        type: int
        required: true
      size_unit:
        description:
        - Unit for the size value.
        type: str
        required: true
        choices: ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
  read_transfer_multiple:
    description:
    - Specifies the preferred multiple size for NFS read requests.
    - This value is used to advise the client of optimal settings for the server, but is not enforced.
    type: dict
    required: False
    suboptions:
      size_value:
        description:
        - Size value.
        type: int
        required: true
      size_unit:
        description:
        - Unit for the size value.
        type: str
        required: true
        choices: ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
  read_transfer_size:
    description:
    - Specifies the preferred size for NFS read requests.
    - This value is used to advise the client of optimal settings for the server, but is not enforced.
    type: dict
    required: False
    suboptions:
      size_value:
        description:
        - Size value.
        type: int
        required: true
      size_unit:
        description:
        - Unit for the size value.
        type: str
        required: true
        choices: ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
  write_transfer_max_size:
    description:
    - Specifies the maximum buffer size that clients should use on NFS write requests.
    - This value is used to advise the client of optimal settings for the server, but is not enforced.
    type: dict
    required: False
    suboptions:
      size_value:
        description:
        - Size value.
        type: int
        required: true
      size_unit:
        description:
        - Unit for the size value.
        type: str
        required: true
        choices: ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
  write_transfer_multiple:
    description:
    - Specifies the preferred multiple size for NFS write requests.
    - This value is used to advise the client of optimal settings for the server, but is not enforced.
    type: dict
    required: False
    suboptions:
      size_value:
        description:
        - Size value.
        type: int
        required: true
      size_unit:
        description:
        - Unit for the size value.
        type: str
        required: true
        choices: ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
  write_transfer_size:
    description:
    - Specifies the preferred multiple size for NFS write requests.
    - This value is used to advise the client of optimal settings for the server, but is not enforced.
    type: dict
    required: False
    suboptions:
      size_value:
        description:
        - Size value.
        type: int
        required: true
      size_unit:
        description:
        - Unit for the size value.
        type: str
        required: true
        choices: ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
  max_file_size:
    description:
    - Specifies the maximum file size for any file accessed from the export.
    - This parameter does not affect server behavior, but is included to accommodate legacy client requirements.
    type: dict
    required: False
    suboptions:
      size_value:
        description:
        - Size value.
        type: int
        required: true
      size_unit:
        description:
        - Unit for the size value.
        type: str
        required: true
        choices: ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
  security_flavors:
    description:
    - Specifies the authentication types that are supported for this export.
    type: list
    required: False
    elements: str
    choices: ['unix', 'kerberos', 'kerberos_integrity', 'kerberos_privacy']
  commit_asynchronous:
    description:
    - True if NFS commit requests execute asynchronously.
    type: bool
    required: False
  setattr_asynchronous:
    description:
    - True if set attribute operations execute asynchronously.
    type: bool
    required: False
  readdirplus:
    description:
    - True if 'readdirplus' requests are enabled.
    - Enabling this property might improve network performance and is only available for NFSv3.
    type: bool
    required: False
  return_32bit_file_ids:
    description:
    - Limits the size of file identifiers returned by NFSv3+ to 32-bit values (may require remount).
    type: bool
    required: False
  can_set_time:
    description:
    - True if the client can set file times through the NFS set attribute request.
    - This parameter does not affect server behavior, but is included to accommodate legacy client requirements.
    type: bool
    required: False
  map_lookup_uid:
    description:
    - True if incoming user IDs (UIDs) are mapped to users in the OneFS user database.
    - When set to False, incoming UIDs are applied directly to file operations.
    type: bool
    required: False
  symlinks:
    description:
    - True if symlinks are supported.
    - This value is used to advise the client of optimal settings for the server, but is not enforced.
    type: bool
    required: False
  write_datasync_action:
    description:
    - Specifies the synchronization type for datasync action.
    type: str
    choices: ['DATASYNC', 'FILESYNC', 'UNSTABLE']
  write_datasync_reply:
    description:
    - Specifies the synchronization type for datasync reply.
    type: str
    choices: ['DATASYNC', 'FILESYNC', 'UNSTABLE']
  write_filesync_action:
    description:
    - Specifies the synchronization type for filesync action.
    type: str
    choices: ['DATASYNC', 'FILESYNC', 'UNSTABLE']
  write_filesync_reply:
    description:
    - Specifies the synchronization type for filesync reply.
    type: str
    choices: ['DATASYNC', 'FILESYNC', 'UNSTABLE']
  write_unstable_action:
    description:
    - Specifies the synchronization type for unstable action.
    type: str
    choices: ['DATASYNC', 'FILESYNC', 'UNSTABLE']
  write_unstable_reply:
    description:
    - Specifies the synchronization type for unstable reply.
    type: str
    choices: ['DATASYNC', 'FILESYNC', 'UNSTABLE']
  encoding:
    description:
    - Specifies the default character set encoding of the clients connecting to the export, unless otherwise specified.
    type: str
  time_delta:
    description:
    - Specifies the resolution of all time values that are returned to the clients.
    type: dict
    required: False
    suboptions:
      time_value:
        description:
        - Time value.
        type: float
        required: true
      time_unit:
        description:
        - Unit for the time value.
        type: str
        required: true
        choices: ['seconds', 'nanoseconds', 'milliseconds', 'microseconds']
  access_zone:
    description:
    - The zone to which the NFS default settings apply.
    default: 'System'
    type: str

notes:
- The I(check_mode) is supported.

'''

EXAMPLES = r'''
- name: Get NFS default settings
  dellemc.powerscale.nfs_default_settings:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    access_zone: "sample-zone"

- name: Update the NFS default settings
  dellemc.powerscale.nfs_default_settings:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    access_zone: "sample-zone"
    block_size:
      size_value: 5
      size_unit: 'KB'
    commit_asynchronous: false
    encoding: 'UTF8'
    map_root:
      enabled: true
      primary_group: 'test_group_1'
      secondary_groups:
        - name: 'test_group_2'
        - name: 'test_group_3'
          state: 'absent'
      user: 'test_user'
    map_non_root:
      enabled: true
      primary_group: 'test_non_root_group'
      secondary_groups:
        - name: 'test_non_root_group_2'
        - name: 'test_non_root_group_3'
          state: 'absent'
      user: 'test_non_root_user'
    readdirplus: true
    time_delta:
      time_value: 5
      time_unit: 'seconds'
    write_filesync_action: 'DATASYNC'
    security_flavors:
      - unix
      - kerberos
'''

RETURN = r'''
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
nfs_default_settings:
    description: The NFS default settings.
    type: dict
    returned: always
    contains:
        map_root:
            description: Mapping of incoming root users to a specific user and/or group ID.
            type: dict
        map_non_root:
            description: Mapping of non-root users to a specific user and/or group ID.
            type: dict
        map_failure:
            description: Mapping of users to a specific user and/or group ID after a failed auth attempt.
            type: dict
        name_max_size:
            description: Specifies the reported maximum length of a file name. This parameter does
                not affect server behavior, but is included to accommodate legacy client
                requirements.
            type: dict
        block_size:
            description: Specifies the block size returned by the NFS statfs procedure.
            type: dict
        directory_transfer_size:
            description: Specifies the preferred size for directory read operations. This value is
                used to advise the client of optimal settings for the server, but is not
                enforced.
            type: dict
        read_transfer_max_size:
            description: Specifies the maximum buffer size that clients should use on NFS read
                requests. This value is used to advise the client of optimal settings for
                the server, but is not enforced.
            type: dict
        read_transfer_multiple:
            description: Specifies the preferred multiple size for NFS read requests. This value is
                used to advise the client of optimal settings for the server, but is not
                enforced.
            type: dict
        read_transfer_size:
            description: Specifies the preferred size for NFS read requests. This value is used to
                advise the client of optimal settings for the server, but is not enforced.
            type: dict
        write_transfer_max_size:
            description: Specifies the maximum buffer size that clients should use on NFS write
                requests. This value is used to advise the client of optimal settings for
                the server, but is not enforced.
            type: dict
        write_transfer_multiple:
            description: Specifies the preferred multiple size for NFS write requests. This value is
                used to advise the client of optimal settings for the server, but is not
                enforced.
            type: dict
        write_transfer_size:
            description: Specifies the preferred multiple size for NFS write requests. This value is
                used to advise the client of optimal settings for the server, but is not
                enforced.
            type: dict
        max_file_size:
            description: Specifies the maximum file size for any file accessed from the export. This
                parameter does not affect server behavior, but is included to accommodate
                legacy client requirements.
            type: dict
        security_flavors:
            description: Specifies the authentication types that are supported for this export.
            type: list
        commit_asynchronous:
            description: True if NFS commit requests execute asynchronously.
            type: bool
        setattr_asynchronous:
            description: True if set attribute operations execute asynchronously.
            type: bool
        readdirplus:
            description: True if 'readdirplus' requests are enabled. Enabling this property might
                improve network performance and is only available for NFSv3.
            type: bool
        return_32bit_file_ids:
            description: Limits the size of file identifiers returned by NFSv3+ to 32-bit values (may
                require remount).
            type: bool
        can_set_time:
            description: True if the client can set file times through the NFS set attribute
                request. This parameter does not affect server behavior, but is included to
                accommodate legacy client requirements.
            type: bool
        map_lookup_uid:
            description: True if incoming user IDs (UIDs) are mapped to users in the OneFS user
                database. When set to False, incoming UIDs are applied directly to file
                operations.
            type: bool
        symlinks:
            description: True if symlinks are supported. This value is used to advise the client of
                optimal settings for the server, but is not enforced.
            type: bool
        write_datasync_action:
            description: Specifies the synchronization type for data sync action.
            type: str
        write_datasync_reply:
            description: Specifies the synchronization type for data sync reply.
            type: str
        write_filesync_action:
            description: Specifies the synchronization type for file sync action.
            type: str
        write_filesync_reply:
            description: Specifies the synchronization type for file sync reply.
            type: str
        write_unstable_action:
            description: Specifies the synchronization type for unstable action.
            type: str
        write_unstable_reply:
            description: Specifies the synchronization type for unstable reply.
            type: str
        encoding:
            description: Specifies the default character set encoding of the clients connecting to
                the export, unless otherwise specified.
            type: str
        time_delta:
            description: Specifies the resolution of all time values that are returned to the
                clients.
            type: dict
        zone:
            description: The zone to which the NFS default settings apply.
            type: str
    sample: {
                'map_root': {
                    'enabled': True,
                    'primary_group': {
                        'id': None,
                        'name': None,
                        'type': None
                    },
                    'secondary_groups': [],
                    'user': {
                        'id': 'USER:nobody',
                        'name': None,
                        'type': None
                    }
                },
                'map_non_root': {
                    'enabled': False,
                    'primary_group': {
                        'id': None,
                        'name': None,
                        'type': None
                    },
                    'secondary_groups': [],
                    'user': {
                        'id': 'USER:nobody',
                        'name': None,
                        'type': None
                    }
                },
                'map_failure': {
                    'enabled': False,
                    'primary_group': {
                        'id': None,
                        'name': None,
                        'type': None
                    },
                    'secondary_groups': [],
                    'user': {
                        'id': 'USER:nobody',
                        'name': None,
                        'type': None
                    }
                },
                'name_max_size': 255,
                'block_size': 8192,
                'commit_asynchronous': False,
                'directory_transfer_size': 131072,
                'read_transfer_max_size': 1048576,
                'read_transfer_multiple': 512,
                'read_transfer_size': 131072,
                'setattr_asynchronous': False,
                'write_datasync_action': 'DATASYNC',
                'write_datasync_reply': 'DATASYNC',
                'write_filesync_action': 'FILESYNC',
                'write_filesync_reply': 'FILESYNC',
                'write_transfer_max_size': 1048576,
                'write_transfer_multiple': 512,
                'write_transfer_size': 524288,
                'write_unstable_action': 'UNSTABLE',
                'write_unstable_reply': 'UNSTABLE',
                'max_file_size': 9223372036854775807,
                'readdirplus': True,
                'return_32bit_file_ids': False,
                'can_set_time': True,
                'encoding': 'DEFAULT',
                'map_lookup_uid': False,
                'symlinks': True,
                'time_delta': 1e-09,
                'zone': 'sample-zone'
            }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.powerscale_base \
    import PowerScaleBase
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.protocol \
    import Protocol
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('nfs_default_settings')


class NFSDefaultSettings(PowerScaleBase):

    '''Class with NFS default settings operations'''

    def __init__(self):
        ''' Define all parameters required by this module'''

        ansible_module_params = {
            'argument_spec': self.get_nfs_default_settings_parameters(),
            'supports_check_mode': True
        }

        super().__init__(AnsibleModule, ansible_module_params)

        self.result["nfs_default_settings"] = {}

    def get_nfs_default_settings(self, access_zone):
        """
        Get details of an NFS default settings for a given access zone.
        :param access_zone: Access zone
        :type access_zone: str
        :return: NFS default settings
        :rtype: dict
        """
        return Protocol(self.protocol_api, self.module).get_nfs_default_settings(access_zone)

    def form_list_of_secondary_groups(self, existing_groups, secondary_groups, access_zone):
        """
        Form list of secondary groups
        :param existing_group: Existing groups
        :type existing_group: list
        :param secondary_groups: Secondary groups
        :type secondary_groups: list
        :param access_zone: Access zone
        :type access_zone: str
        """
        secondary_groups_list = []
        existing_groups_list = [existing_group['id'] for existing_group in existing_groups]
        old_groups_list = existing_groups
        for group in secondary_groups:
            state = group['state']
            group = {
                'id': 'GROUP:' + group['name'],
                'type': 'group'}
            if state == 'present' and group['id'] not in existing_groups_list:
                secondary_groups_list.append({'id': group['id']})
            elif state == 'absent' and group['id'] in existing_groups_list:
                existing_groups = [ex_grp for ex_grp in existing_groups if ex_grp['id'] != group['id']]
        secondary_groups_list.extend(existing_groups)
        existing_groups_id_list = [existing_group['id'] for existing_group in old_groups_list]
        secondary_groups_id_list = [secondary_group['id'] for secondary_group in secondary_groups_list]
        if set(existing_groups_id_list) != set(secondary_groups_id_list):
            return secondary_groups_list

    def form_primary_group_and_user_dict(self, persona_type, existing_map_params, name):
        """
        Form primary group or user dict
        :param persona_type: Indicating group or user
        :type persona_type: str
        :param existing_map_params: Existing map params
        :type existing_map_params: dict
        :param map_params: Map params
        :type map_params: dict
        :return: Primary group or user dict
        """
        persona_item = {
            'id': persona_type + ':' + name,
            'type': persona_type.lower()}
        if existing_map_params['id'] != persona_item['id']:
            return persona_item

    def fill_map_dict(self, map_dict, key, nfs_default_settings):
        """
        Fill map dict for update
        :param map_dict: Map dict
        :type map_dict: dict
        :param nfs_default_settings: NFS default settings
        :type nfs_default_settings: dict
        :param key: Key
        :type key: str
        """
        sub_key_list = ['enabled', 'primary_group', 'secondary_groups', 'user']
        for sub_key in sub_key_list:
            if sub_key not in map_dict[key]:
                map_dict[key][sub_key] = nfs_default_settings[key][sub_key]
        return map_dict

    def check_and_delete_map_key(self, map_dict, key):
        """
        Check and delete map dict key
        :param map_dict: Map dict
        :type map_dict: dict
        :param key: Map key
        :type key: str
        """
        if map_dict[key] is None:
            del map_dict[key]

    def check_modify_for_map_key(self, map_dict, key, nfs_default_settings, module_params):
        """
        Check and delete map dict key
        :param map_dict: Map dict
        :type map_dict: dict
        :param nfs_default_settings: NFS default settings
        :type nfs_default_settings: dict
        :param module_params: Module parameters
        :type module_params: dict
        :param key: Key
        :type key: str
        """
        if module_params[key] and 'enabled' in module_params[key] and  \
           nfs_default_settings[key]['enabled'] != module_params[key]['enabled']:
            if module_params[key]['enabled'] is False:
                map_dict[key] = {
                    'enabled': False
                }
                return map_dict
            else:
                map_dict[key]['enabled'] = module_params[key]['enabled']

        check_keys = ['primary_group', 'secondary_groups', 'user']
        persona_map = {
            'primary_group': 'GROUP',
            'user': 'USER'
        }
        for check_key in check_keys:
            if module_params[key] and check_key in module_params[key] and module_params[key][check_key]:
                if check_key == 'secondary_groups':
                    map_dict[key][check_key] = self.form_list_of_secondary_groups(nfs_default_settings[key][check_key],
                                                                                  module_params[key][check_key],
                                                                                  module_params['access_zone'])
                    self.check_and_delete_map_key(map_dict[key], check_key)
                else:
                    map_dict[key][check_key] = self.form_primary_group_and_user_dict(persona_map[check_key],
                                                                                     nfs_default_settings[key][check_key],
                                                                                     module_params[key][check_key])
                    self.check_and_delete_map_key(map_dict[key], check_key)
        return map_dict

    def form_map_dict(self, nfs_default_settings, module_params):
        """
        Form the modify dict.
        :param nfs_default_settings: NFS default settings details
        :type nfs_default_settings: dict
        :param module_params: Module parameters
        :type module_params: dict
        :return: map_dict
        :rtype: dict
        """
        LOG.info('Form modification dict for map settings')
        map_dict = {}
        map_key_list = ['map_root', 'map_non_root', 'map_failure']
        for key in map_key_list:
            if module_params[key] and 'enabled' in module_params[key] \
               and module_params[key]['enabled'] is False and module_params[key]['enabled'] == nfs_default_settings[key]['enabled']:
                continue

            map_dict[key] = {}
            map_dict = self.check_modify_for_map_key(map_dict, key, nfs_default_settings, module_params)

            if not map_dict[key]:
                del map_dict[key]
            elif 'enabled' not in map_dict[key] or ('enabled' in map_dict[key] and map_dict[key]['enabled']):
                map_dict = self.fill_map_dict(map_dict, key, nfs_default_settings)

        msg = f'Forming modification dict for map settings completed: {map_dict}'
        LOG.info(msg)
        return map_dict

    def form_size_dict(self, nfs_default_settings, module_params):
        """
        Form the modify dict.
        :param nfs_default_settings: NFS default settings details
        :type nfs_default_settings: dict
        :param module_params: Module parameters
        :type module_params: dict
        :return: size_dict
        :rtype: dict
        """
        LOG.info('Form modification dict for size settings')
        size_dict = {}
        size_params = ['block_size', 'directory_transfer_size', 'read_transfer_max_size', 'read_transfer_multiple',
                       'read_transfer_size', 'write_transfer_max_size', 'write_transfer_multiple', 'write_transfer_size',
                       'max_file_size']

        for key in size_params:
            if key in module_params and module_params[key] is not None and \
               utils.get_size_bytes(module_params[key]['size_value'], module_params[key]['size_unit']) != nfs_default_settings[key]:
                size_dict[key] = utils.get_size_bytes(module_params[key]['size_value'], module_params[key]['size_unit'])

        if 'file_name_max_size' in module_params and module_params['file_name_max_size'] and \
           utils.get_size_bytes(module_params['file_name_max_size']['size_value'],
                                module_params['file_name_max_size']['size_unit']) != nfs_default_settings['name_max_size']:
            size_dict['name_max_size'] = utils.get_size_bytes(module_params['file_name_max_size']['size_value'],
                                                              module_params['file_name_max_size']['size_unit'])
        msg = f'Forming modification dict for size settings completed: {size_dict}'
        LOG.info(msg)
        return size_dict

    def form_security_dict(self, nfs_default_settings, module_params):
        """
        Form the modify dict.
        :param nfs_default_settings: NFS default settings details
        :type nfs_default_settings: dict
        :param module_params: Module parameters
        :type module_params: dict
        :return: security_dict
        :rtype: dict
        """
        LOG.info('Form modification dict for security flavors')
        security_dict = {}
        security_flavors_mapping = {
            "unix": "unix",
            "kerberos": "krb5",
            "kerberos_integrity": "krb5i",
            "kerberos_privacy": "krb5p"
        }
        security_flavors = module_params['security_flavors']
        if security_flavors:
            security_flavors = [security_flavors_mapping[flavor] for flavor in security_flavors]
            if security_flavors != nfs_default_settings['security_flavors']:
                security_dict['security_flavors'] = security_flavors
        msg = f'Forming modification dict for security flavors completed: {security_dict}'
        LOG.info(msg)
        return security_dict

    def form_sync_bool_dict(self, nfs_default_settings, module_params):
        """
        Form the modify dict.
        :param nfs_default_settings: NFS default settings details
        :type nfs_default_settings: dict
        :param module_params: Module parameters
        :type module_params: dict
        :return: sync_bool_dict
        :rtype: dict
        """
        LOG.info('Form modification dict for bool and sync settings')
        sync_bool_dict = {}
        sync_bool_params = ['commit_asynchronous', 'setattr_asynchronous', 'readdirplus',
                            'return_32bit_file_ids', 'can_set_time', 'map_lookup_uid',
                            'symlinks', 'write_unstable_action', 'write_unstable_reply',
                            'write_filesync_action', 'write_filesync_reply',
                            'write_datasync_action', 'write_datasync_reply', 'encoding']
        for key in sync_bool_params:
            if key in module_params and module_params[key] is not None and\
               nfs_default_settings[key] != module_params[key]:
                sync_bool_dict[key] = module_params[key]
        msg = f'Forming modification dict for bool and sync settings completed: {sync_bool_dict}'
        LOG.info(msg)
        return sync_bool_dict

    def form_time_dict(self, nfs_default_settings, module_params):
        """
        Form the modify dict.
        :param nfs_default_settings: NFS default settings details
        :type nfs_default_settings: dict
        :param module_params: Module parameters
        :type module_params: dict
        :return: time_dict
        :rtype: dict
        """
        LOG.info('Form modification dict for time delta')
        time_dict = {}
        if 'time_delta' in module_params and module_params['time_delta'] and nfs_default_settings['time_delta'] \
           != utils.convert_to_seconds(module_params['time_delta']['time_value'], module_params['time_delta']['time_unit']):
            time_dict['time_delta'] = utils.convert_to_seconds(module_params['time_delta']['time_value'], module_params['time_delta']['time_unit'])
        msg = f'Forming modification dict for time delta completed: {time_dict}'
        LOG.info(msg)
        return time_dict

    def form_modify_dict(self, nfs_default_settings, module_params):
        """
        Form the modify dict.
        :param nfs_default_settings: NFS default settings details
        :type nfs_default_settings: dict
        :param module_params: Module parameters
        :type module_params: dict
        :return: modify_dict
        :rtype: dict
        """
        msg = f'Form modification dict {module_params}'
        LOG.info(msg)
        modify_dict = {}
        try:
            modify_dict.update(self.form_map_dict(nfs_default_settings, module_params))
            modify_dict.update(self.form_size_dict(nfs_default_settings, module_params))
            modify_dict.update(self.form_security_dict(nfs_default_settings, module_params))
            modify_dict.update(self.form_sync_bool_dict(nfs_default_settings, module_params))
            modify_dict.update(self.form_time_dict(nfs_default_settings, module_params))
        except Exception as exp:
            msg = f'Forming modification dict failed with error: {exp}'
            LOG.info(msg)
            self.module.fail_json(msg=msg)
        msg = f'Forming modification dict completed: {modify_dict}'
        LOG.info(msg)
        return modify_dict

    def form_nfs_default_settings_object(self, modify_dict, access_zone):
        """
        Form nfs default settings object
        :param modify_dict: NFS default settings module params
        :return: NFS default settings object.
        """
        LOG.info('Forming nfs default settings object')
        map_key_list = ['map_root', 'map_non_root', 'map_failure']
        for key in map_key_list:
            if key in modify_dict and modify_dict[key]:
                if modify_dict[key]['enabled'] is False:
                    modify_dict[key] = self.isi_sdk.NfsSettingsExportSettingsMapAll(**modify_dict[key])
                    continue
                modify_dict[key]['user'] = self.isi_sdk.AuthAccessAccessItemFileGroup(**modify_dict[key]['user'])
                modify_dict[key]['primary_group'] = self.isi_sdk.AuthAccessAccessItemFileGroup(**modify_dict[key]['primary_group'])
                secondary_groups = []
                for sec_gp in modify_dict[key]['secondary_groups']:
                    secondary_groups.append(self.isi_sdk.NfsExportMapAllSecondaryGroups(**sec_gp))
                modify_dict[key]['secondary_groups'] = secondary_groups
                modify_dict[key]['enabled'] = True
                modify_dict[key] = self.isi_sdk.NfsSettingsExportSettingsMapAll(**modify_dict[key])

        modify_dict['zone'] = access_zone
        nfs_default_settings_object = self.isi_sdk.NfsSettingsExportSettings(**modify_dict)
        LOG.info('Forming nfs default settings object completed')
        return nfs_default_settings_object

    def modify_nfs_default_settings(self, module_params, access_zone):
        """
        Modify the NFS default settings
        :param module_params: Module params
        :type module_params: dict
        :param access_zone: Access zone
        :type access_zone: str
        :return: True if successful
        :rtype: bool
        """
        try:
            modify_params_obj = self.form_nfs_default_settings_object(module_params, access_zone)
            msg = f'Modifying NFS default settings for access zone: {access_zone}'
            LOG.info(msg)
            if not self.module.check_mode:
                self.protocol_api.update_nfs_settings_export(
                    modify_params_obj, zone=access_zone)
            LOG.info("Successfully modified the NFS default settings")
            return True
        except Exception as e:
            error = utils.determine_error(e)
            error_msg = f'Modifying NFS default settings for access zone: {access_zone} failed with error: {error}'
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_size_paramters(self):
        return dict(type='dict', options=dict(
                    size_value=dict(type='int', required=True),
                    size_unit=dict(type='str', required=True, choices=['B', 'KB', 'MB', 'GB', 'TB', 'PB'])))

    def get_nfs_map_parameters(self):
        return dict(type='dict', options=dict(
            enabled=dict(type='bool', default=True),
            primary_group=dict(type='str', required=False),
            user=dict(type='str', required=False),
            secondary_groups=dict(type='list', elements='dict', options=dict(
                    name=dict(type='str', required=True),
                    state=dict(type='str', choices=['present', 'absent'], default='present')))))

    def get_sync_parameters(self):
        return dict(type='str', choices=['DATASYNC', 'FILESYNC', 'UNSTABLE'])

    def get_nfs_default_settings_parameters(self):
        return dict(
            map_root=self.get_nfs_map_parameters(),
            map_non_root=self.get_nfs_map_parameters(),
            map_failure=self.get_nfs_map_parameters(),
            file_name_max_size=self.get_size_paramters(),
            block_size=self.get_size_paramters(),
            directory_transfer_size=self.get_size_paramters(),
            read_transfer_max_size=self.get_size_paramters(),
            read_transfer_multiple=self.get_size_paramters(),
            read_transfer_size=self.get_size_paramters(),
            write_transfer_max_size=self.get_size_paramters(),
            write_transfer_multiple=self.get_size_paramters(),
            write_transfer_size=self.get_size_paramters(),
            max_file_size=self.get_size_paramters(),
            security_flavors=dict(type='list', elements='str', choices=['unix', 'kerberos', 'kerberos_integrity', 'kerberos_privacy']),
            commit_asynchronous=dict(type='bool'),
            setattr_asynchronous=dict(type='bool'),
            readdirplus=dict(type='bool'),
            return_32bit_file_ids=dict(type='bool'),
            can_set_time=dict(type='bool'),
            map_lookup_uid=dict(type='bool'),
            symlinks=dict(type='bool'),
            write_datasync_action=self.get_sync_parameters(),
            write_datasync_reply=self.get_sync_parameters(),
            write_filesync_action=self.get_sync_parameters(),
            write_filesync_reply=self.get_sync_parameters(),
            write_unstable_action=self.get_sync_parameters(),
            write_unstable_reply=self.get_sync_parameters(),
            encoding=dict(type='str'),
            time_delta=dict(type='dict', options=dict(
                time_value=dict(type='float', required=True),
                time_unit=dict(type='str', required=True, choices=['seconds', 'nanoseconds', 'milliseconds', 'microseconds']))),
            access_zone=dict(type='str', default='System')
        )


class NFSDefaultSettingsExitHandler():
    def handle(self, nfs_default_settings_obj):
        nfs_default_settings_obj.module.exit_json(**nfs_default_settings_obj.result)


class NFSDefaultSettingsModifyHandler():
    def handle(self, nfs_default_settings_obj):
        nfs_default_settings = nfs_default_settings_obj.result["nfs_default_settings"]
        if nfs_default_settings:
            module_params = nfs_default_settings_obj.module.params
            modify_dict = nfs_default_settings_obj.form_modify_dict(nfs_default_settings, module_params)
            if modify_dict:
                access_zone = nfs_default_settings_obj.module.params['access_zone']
                changed = nfs_default_settings_obj.modify_nfs_default_settings(modify_dict, access_zone)
                nfs_default_settings_obj.result["changed"] = changed
                nfs_default_settings_obj.result["nfs_default_settings"] = nfs_default_settings_obj.get_nfs_default_settings(access_zone)
        NFSDefaultSettingsExitHandler().handle(nfs_default_settings_obj)


class NFSDefaultSettingsHandler():
    def handle(self, nfs_default_settings_obj):
        access_zone = nfs_default_settings_obj.module.params['access_zone']
        nfs_default_settings = nfs_default_settings_obj.get_nfs_default_settings(access_zone)
        nfs_default_settings_obj.result["nfs_default_settings"] = nfs_default_settings
        NFSDefaultSettingsModifyHandler().handle(nfs_default_settings_obj)


def main():
    """ Create PowerScale NFS default settings object and perform action on it
        based on user input from playbook."""
    obj = NFSDefaultSettings()
    NFSDefaultSettingsHandler().handle(obj)


if __name__ == '__main__':
    main()
