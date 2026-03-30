#!/usr/bin/python
# Copyright: (c) 2020-2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing NFS Exports on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: nfs
version_added: '1.2.0'
short_description:  Manage NFS exports on a PowerScale Storage System
description:
- Managing NFS exports on an PowerScale system includes retrieving details of
  NFS export, creating NFS export in specified access zone, adding or removing
  clients, modifying and deleting NFS export.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Manisha Agrawal(@agrawm3) <ansible.team@dell.com>
- Bhavneet Sharma(@Bhavneet-Sharma) <ansible.team@dell.com>
- Trisha Datta(@trisha-dell) <ansible.team@dell.com>
- Kritika Bhateja(@Kritika-Bhateja-03) <ansible.team.dell.com>)
- Saksham Nautiyal (@Saksham-Nautiyal) <ansible.team@dell.com>

options:
  access_zone:
    description:
    - Specifies the zone in which the export is valid.
    - Access zone once set cannot be changed.
    type: str
    default: System
  clients:
    description:
    - Specifies the clients to the export. The type of access to clients in
      this list is determined by the I(read_only) parameter.
    - This list can be changed anytime during the lifetime of the NFS export.
    - I(client_state) is not provided, then the host machine will replicate the values provided in the I(clients).
    type: list
    elements: str
  client_state:
    description:
    - Defines whether the clients can access the NFS export.
    - Value C(present-in-export) indicates that the clients can access the NFS export.
    - Value C(absent-in-export) indicates that the client cannot access the NFS export.
    - Required when adding or removing access of clients from the export.
    - While removing clients, only the specified clients will be removed from
      the export, others will remain as is.
    type: str
    choices: [present-in-export, absent-in-export]
  description:
    description:
    - Optional description field for the NFS export.
    - Can be modified by passing a new value.
    type: str
  ignore_unresolvable_hosts:
    description:
    - Does not present an error condition on unresolvable hosts when creating
     or modifying an export.
    type: bool
  map_root:
    description:
    - Specifies the users and groups to which non-root and root clients are mapped.
    type: dict
    suboptions:
      enabled:
        description:
        - True if the user mapping is applied.
        type: bool
        default: true
      primary_group:
        description:
        - Specifies the primary group name.
        type: str
      secondary_groups:
        description:
        - Specifies the secondary groups.
        type: list
        elements: dict
        suboptions:
          name:
            description:
            - Specifies the group name.
            type: str
            required: true
          state:
            description:
            - Specifies the group state.
            type: str
            choices: [absent, present]
            default: present
      user:
        description:
        - Specifies the persona name.
        type: str
  map_non_root:
    description:
    - Specifies the users and groups to which non-root and root clients are mapped.
    type: dict
    suboptions:
      enabled:
        description:
        - True if the user mapping is applied.
        type: bool
        default: true
      primary_group:
        description:
        - Specifies the primary group name.
        type: str
      secondary_groups:
        description:
        - Specifies the secondary groups.
        type: list
        elements: dict
        suboptions:
          name:
            description:
            - Specifies the group name.
            type: str
            required: true
          state:
            description:
            - Specifies the group state.
            type: str
            choices: [absent, present]
            default: present
      user:
        description:
        - Specifies the persona name.
        type: str
  path:
    description:
    - Specifies the filesystem path. It is the absolute path for System access zone
      and it is relative if using non-system access zone.
    - For example, if your access zone is 'Ansible' and it has a base path
      '/ifs/ansible' and the path specified is '/user1', then the effective
      path would be '/ifs/ansible/user1'.
    - If your access zone is System, and you have 'directory1' in the access
      zone, the path provided should be '/ifs/directory1'.
    - The directory on the path must exist - the NFS module will not create
      the directory.
    - Ansible module will only support exports with a unique path.
    - If there are multiple exports present with the same path, fetching details,
      creation, modification or deletion of such exports will fail.
    required: true
    type: str
  read_only:
    description:
    - Specifies whether the export is read-only or read-write. This parameter
      only has effect on the 'clients' list and not the other three types of
      clients.
    - This setting can be modified any time. If it is not set at the time of
      creation, the export will be of type read/write.
    type: bool
  read_only_clients:
    description:
    - Specifies the clients with read-only access to the export, even when the
      export is read/write.
    - This list can be changed anytime during the lifetime of the NFS export.
    - I(client_state) is not provided, then the host machine will replicate the values provided in the I(read_only_clients).
    type: list
    elements: str
  read_write_clients:
    description:
    - Specifies the clients with both read and write access to the export,
      even when the export is set to read-only.
    - This list can be changed anytime during the lifetime of the NFS export.
    - I(client_state) is not provided, then the host machine will replicate the values provided in the I(read_write_clients).
    type: list
    elements: str
  root_clients:
    description:
    - Specifies the clients with root access to the export.
    - This list can be changed anytime during the lifetime of the NFS export.
    - I(client_state) is not provided, then the host machine will replicate the values provided in the I(root_clients).
    type: list
    elements: str
  security_flavors:
    description:
    - Specifies the authentication types that are supported for this export.
    type: list
    elements: str
    choices: ['unix', 'kerberos', 'kerberos_integrity', 'kerberos_privacy']
  state:
    description:
    - Defines whether the NFS export should exist or not.
    - Value C(present) indicates that the NFS export should exist in system.
    - Value C(absent) indicates that the NFS export should not exist in system.
    required: true
    type: str
    choices: [absent, present]
  sub_directories_mountable:
    description:
    - C(true) if all directories under the specified paths are mountable. If not
      set, sub-directories will not be mountable.
    - This setting can be modified any time.
    type: bool
  map_failure:
    description:
    - Specifies the user/group mapping to apply after a failed auth attempt for this export.
    type: dict
    suboptions:
      enabled:
        description:
        - True if the user mapping is applied.
        type: bool
        default: true
      primary_group:
        description:
        - Specifies the primary group name.
        type: str
      secondary_groups:
        description:
        - Specifies the secondary groups.
        type: list
        elements: dict
        suboptions:
          name:
            description:
            - Specifies the group name.
            type: str
            required: true
          state:
            description:
            - Specifies the group state.
            type: str
            choices: [absent, present]
            default: present
      user:
        description:
        - Specifies the persona name.
        type: str
  file_name_max_size:
    description:
    - Specifies the reported maximum length of a file name (size dict).
    type: dict
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
    - Specifies the block size returned by the NFS statfs procedure (size dict).
    type: dict
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
    - Specifies the preferred size for directory read operations (size dict).
    type: dict
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
    - Specifies the maximum buffer size that clients should use on NFS read requests (size dict).
    type: dict
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
    - Specifies the preferred multiple size for NFS read requests (size dict).
    type: dict
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
    - Specifies the preferred size for NFS read requests (size dict).
    type: dict
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
    - Specifies the maximum buffer size that clients should use on NFS write requests (size dict).
    type: dict
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
    - Specifies the preferred multiple size for NFS write requests (size dict).
    type: dict
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
    - Specifies the preferred multiple size for NFS write requests (size dict).
    type: dict
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
    - Specifies the maximum file size for any file accessed from the export (size dict).
    type: dict
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
  commit_asynchronous:
    description:
    - True if NFS commit requests execute asynchronously.
    type: bool
  setattr_asynchronous:
    description:
    - True if set attribute operations execute asynchronously.
    type: bool
  readdirplus:
    description:
    - True if 'readdirplus' requests are enabled. Enabling this property might improve network performance and is only available for NFSv3.
    type: bool
  return_32bit_file_ids:
    description:
    - Limits the size of file identifiers returned by NFSv3+ to 32-bit values (may require remount).
    type: bool
  can_set_time:
    description:
    - True if the client can set file times through the NFS set attribute request.
    type: bool
  map_lookup_uid:
    description:
    - True if incoming user IDs (UIDs) are mapped to users in the OneFS user database.
    - When set to False, incoming UIDs are applied directly to file operations.
    type: bool
  symlinks:
    description:
    - True if symlinks are supported.
    type: bool
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
    - Encoding type for filenames returned to clients.
    type: str
  time_delta:
    description:
    - Time delta object expressing time skew; expects a dict with time_value and time_unit.
    type: dict
    suboptions:
      time_value:
        description:
        - Numeric time value.
        type: float
        required: true
      time_unit:
        description:
        - Unit for time_value.
        type: str
        required: true
        choices: ['seconds', 'nanoseconds', 'milliseconds', 'microseconds']
attributes:
  check_mode:
    description:
    - Runs task to validate without performing action on the target machine.
    support: full
  diff_mode:
    description:
    - Runs the task to report the changes made or to be made.
    support: full
notes:
  - As I(ignore_unresolvable_hosts) is input only parameter, therefore idempotency is not supported for it.
'''

EXAMPLES = r'''
- name: Create NFS Export
  dellemc.powerscale.nfs:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    path: "<path>"
    access_zone: "{{access_zone}}"
    read_only_clients:
      - "{{client1}}"
      - "{{client2}}"
    read_only: true
    clients: ["{{client3}}"]
    client_state: 'present-in-export'
    state: 'present'

- name: Get NFS Export
  dellemc.powerscale.nfs:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    path: "<path>"
    access_zone: "{{access_zone}}"
    state: 'present'

- name: Add a root client
  dellemc.powerscale.nfs:
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

- name: Replace existing list of root clients
  dellemc.powerscale.nfs:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    path: "<path>"
    access_zone: "{{access_zone}}"
    root_clients:
      - "{{client4}}"
    state: 'present'

- name: Set sub_directories_mountable flag to true
  dellemc.powerscale.nfs:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    path: "<path>"
    access_zone: "{{access_zone}}"
    sub_directories_mountable: true
    state: 'present'

- name: Remove a root client
  dellemc.powerscale.nfs:
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

- name: Modify NFS Export
  dellemc.powerscale.nfs:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    path: "<path>"
    access_zone: "{{access_zone}}"
    description: "new description"
    security_flavors:
      - "kerberos_integrity"
      - "kerberos"
    state: 'present'

- name: Set read_only flag to false
  dellemc.powerscale.nfs:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    path: "<path>"
    access_zone: "{{access_zone}}"
    read_only: false
    state: 'present'

- name: Modify map_root and map_non_root
  dellemc.powerscale.nfs:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    path: "<path>"
    access_zone: "{{access_zone}}"
    map_root:
      user: "root"
      primary_group: "root"
    map_non_root:
      user: "root"
      primary_group: "root"
    secondary_groups:
      - name: "group_test"
        state: "absent"
    state: 'present'

- name: Disable map_root
  dellemc.powerscale.nfs:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    path: "<path>"
    access_zone: "{{access_zone}}"
    map_root:
      enabled: false
      state: 'present'

- name: Delete NFS Export
  dellemc.powerscale.nfs:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    path: "<path>"
    access_zone: "{{access_zone}}"
    state: 'absent'

- name: Create NFS Export with advanced settings
  dellemc.powerscale.nfs:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    path: "<path>"
    access_zone: "{{access_zone}}"
    read_only: false
    clients:
      - "10.0.0.10"
    map_lookup_uid: true
    block_size:
      size_value: 8192
      size_unit: 'B'
    map_failure:
      enabled: false
    write_filesync_action: 'FILESYNC'
    time_delta:
      time_value: 1.0
      time_unit: 'seconds'
    state: 'present'
'''

RETURN = r'''
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
NFS_export_details:
    description: The updated NFS Export details.
    type: complex
    returned: always
    contains:
        all_dirs:
            description: I(sub_directories_mountable) flag value.
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
        map_root:
            description: Specifies the users and groups to which non-root and root clients are mapped.
            type: complex
            contains:
                enabled:
                    description: True if the user mapping is applied.
                    type: bool
                user:
                    description: Specifies the persona name.
                    type: complex
                    contains:
                        id:
                            description: Specifies the persona name.
                            type: str
                primary_group:
                    description: Specifies the primary group.
                    type: complex
                    contains:
                        id:
                            description: Specifies the primary group name.
                            type: str
                secondary_groups:
                    description: Specifies the secondary groups.
                    type: list
        map_non_root:
            description: Specifies the users and groups to which non-root and root clients are mapped.
            type: complex
            contains:
                enabled:
                    description: True if the user mapping is applied.
                    type: bool
                user:
                    description: Specifies the persona details.
                    type: complex
                    contains:
                        id:
                            description: Specifies the persona name.
                            type: str
                primary_group:
                    description: Specifies the primary group details.
                    type: complex
                    contains:
                        id:
                            description: Specifies the primary group name.
                            type: str
                secondary_groups:
                    description: Specifies the secondary groups details.
                    type: list
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
    sample: {
        "all_dir": "false",
        "block_size": 8192,
        "clients": None,
        "id": 9324,
        "read_only_client": ["x.x.x.x"],
        "security_flavors": ["unix", "krb5"],
        "zone": "System",
        "map_root": {
            "enabled": true,
            "primary_group": {
                "id": GROUP:group1,
                "name": null,
                "type": null
            },
            "secondary_groups": [],
            "user": {
                "id": "USER:user",
                "name": null,
                "type": null
            }
        },
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
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.powerscale_base \
    import PowerScaleBase
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
import copy

LOG = utils.get_logger('nfs')


class NfsExport(PowerScaleBase):

    '''Class with NFS export operations'''

    def __init__(self):
        ''' Define all parameters required by this module'''

        ansible_module_params = {
            'argument_spec': self.get_nfs_parameters(),
            'supports_check_mode': True
        }
        super().__init__(AnsibleModule, ansible_module_params)
        # Result is a dictionary that contains changed status, NFS export
        # details
        self.result = {
            "changed": False,
            "NFS_export_details": {},
            "diff": {}
        }

    def get_zone_base_path(self, access_zone):
        """Returns the base path of the Access Zone."""
        try:
            zone_path = (self.zones_summary_api.
                         get_zones_summary_zone(access_zone)).to_dict()
            return zone_path["summary"]["path"]
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
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
            if path.endswith("/"):
                path = path[0:len(path) - 1]
            nfs_exports_extended_obj = self.protocol_api.list_nfs_exports(
                path=path, zone=access_zone)

            if nfs_exports_extended_obj.total > 1:
                error_msg = 'Multiple NFS Exports found'
                LOG.error(error_msg)
                self.module.fail_json(msg=error_msg)

            elif nfs_exports_extended_obj.total == 0:
                LOG.debug('NFS Export for given path: %s and access zone: %s '
                          'not found', path, access_zone)
                return {}

            else:
                nfs_export = nfs_exports_extended_obj.exports[0]
                return nfs_export.to_dict()

        except Exception as e:
            error_msg = (
                "Got error {0} while getting NFS export details for path: "
                "{1} and access zone: {2}" .format(
                    utils.determine_error(e),
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
            nfs_exports_obj = self.protocol_api.get_nfs_export(
                nfs_export_id, zone=access_zone)
            nfs_export = nfs_exports_obj.exports[0]
            return nfs_export.to_dict()

        except Exception as e:
            error_msg = (
                "Got error {0} while getting NFS export details for ID: "
                "{1} and access zone: {2}" .format(
                    utils.determine_error(e),
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
                security_flavors=get_security_keys(
                    self.module.params['security_flavors']),
                zone=self.module.params['access_zone'])
            # Apply advanced per-export settings if provided
            nfs_map_root = set_nfs_map(self.module.params.get('map_root'), 'map_root')
            if nfs_map_root:
                nfs_export.map_root = nfs_map_root
            nfs_map_non_root = set_nfs_map(self.module.params.get('map_non_root'), 'map_non_root')
            if nfs_map_non_root:
                nfs_export.map_non_root = nfs_map_non_root
            nfs_map_failure = set_nfs_map(self.module.params.get('map_failure'), 'map_failure')
            if nfs_map_failure:
                nfs_export.map_failure = nfs_map_failure

            # Size fields (convert to integer bytes using utils.get_size_bytes)
            for size_field in ['file_name_max_size', 'block_size', 'directory_transfer_size',
                               'read_transfer_max_size', 'read_transfer_multiple', 'read_transfer_size',
                               'write_transfer_max_size', 'write_transfer_multiple', 'write_transfer_size',
                               'max_file_size']:
                size_param = self.module.params.get(size_field)
                if size_param is not None:
                    try:
                        size_val = utils.get_size_bytes(size_param['size_value'], size_param['size_unit'])
                    except Exception:
                        size_val = None
                    if size_val is not None:
                        setattr(
                            nfs_export,
                            # keys in NFS export details sometimes differ (file_name_max_size -> name_max_size)
                            size_field if size_field != 'file_name_max_size' else 'name_max_size',
                            size_val,
                        )

            # Simple booleans / strings
            for simple_field in ['commit_asynchronous', 'setattr_asynchronous', 'readdirplus',
                                 'return_32bit_file_ids', 'can_set_time', 'map_lookup_uid', 'symlinks',
                                 'encoding', 'write_datasync_action', 'write_datasync_reply',
                                 'write_filesync_action', 'write_filesync_reply', 'write_unstable_action',
                                 'write_unstable_reply']:
                if self.module.params.get(simple_field) is not None:
                    setattr(nfs_export, simple_field, self.module.params.get(simple_field))

            # time_delta expects a numeric seconds value in the SDK; convert if provided
            if self.module.params.get('time_delta') is not None:
                td = self.module.params.get('time_delta')
                td_seconds = utils.convert_to_seconds(td.get('time_value'), td.get('time_unit'))
                setattr(nfs_export, 'time_delta', td_seconds)

            return nfs_export
        except Exception as e:
            error_msg = 'Create NfsExportCreateParams object for path {0}' \
                ' failed with error {1}'.format(
                    path, utils.determine_error(e))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def create_nfs_export(self, path, access_zone, ignore_unresolvable_hosts):
        '''
        Create NFS export for given path and access_zone
        '''
        nfs_export = self._create_nfs_export_create_params_object(path)
        nfs_map_root = set_nfs_map(self.module.params.get('map_root'), 'map_root')
        if nfs_map_root:
            nfs_export.map_root = nfs_map_root
        nfs_map_non_root = set_nfs_map(self.module.params.get('map_non_root'), 'map_non_root')
        if nfs_map_non_root:
            nfs_export.map_non_root = nfs_map_non_root
        if self.module._diff:
            self.result.update({"diff": {"before": {}, "after": nfs_export.to_dict()}})
        try:
            if not self.module.check_mode:
                msg = ("Creating NFS export with parameters:nfs_export=%s",
                       nfs_export)
                LOG.info(msg)
                if ignore_unresolvable_hosts is not True:
                    response = self.protocol_api.create_nfs_export(nfs_export, zone=access_zone)
                else:
                    response = self.protocol_api.create_nfs_export(nfs_export, zone=access_zone,
                                                                   ignore_unresolvable_hosts=ignore_unresolvable_hosts)
                self.result['NFS_export_details'] = self._get_nfs_export_from_id(response.id, access_zone=access_zone)
            return True

        except Exception as e:
            error_msg = 'Create NFS export for path: {0} and access zone: {1}' \
                ' failed with error: {2}'.format(
                    path, access_zone, utils.determine_error(e))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

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

    def _check_read_write_clients(self, nfs_export, playbook_client_dict, current_client_dict, mod_flag):
        '''
        Check if read-write clients are to be added/removed to/from NFS export
        '''

        client_state = self.module.params['client_state']
        if playbook_client_dict['read_write_clients'] is None:
            return mod_flag, nfs_export

        if client_state is None:
            if set(playbook_client_dict['read_write_clients']) != set(current_client_dict['read_write_clients']):
                current_client_dict['read_write_clients'] = playbook_client_dict['read_write_clients']
                mod_flag = True
        for client in playbook_client_dict['read_write_clients']:
            if client_state == 'present-in-export' and client not in current_client_dict['read_write_clients']:
                current_client_dict['read_write_clients'].append(client)
                mod_flag = True

            elif client_state == 'absent-in-export' and client in current_client_dict['read_write_clients']:
                current_client_dict['read_write_clients'].remove(client)
                mod_flag = True

        if mod_flag:
            nfs_export.read_write_clients = current_client_dict['read_write_clients']

        return mod_flag, nfs_export

    def _check_clients(self, nfs_export, playbook_client_dict, current_client_dict, mod_flag):
        '''
        Check if clients are to be added/removed to/from NFS export
        '''

        client_state = self.module.params['client_state']
        if playbook_client_dict['clients'] is None:
            return mod_flag, nfs_export

        if client_state is None:
            if playbook_client_dict['clients'] != current_client_dict['clients']:
                current_client_dict['clients'] = playbook_client_dict['clients']
                mod_flag = True
        for client in playbook_client_dict['clients']:
            if client_state == 'present-in-export' and client not in current_client_dict['clients']:
                current_client_dict['clients'].append(client)
                mod_flag = True

            elif client_state == 'absent-in-export' and client in current_client_dict['clients']:
                current_client_dict['clients'].remove(client)
                mod_flag = True

        if mod_flag:
            nfs_export.clients = current_client_dict['clients']

        return mod_flag, nfs_export

    def _check_read_only_clients(self, nfs_export, playbook_client_dict, current_client_dict, mod_flag):
        '''
        Check if read-only clients are to be added/removed to/from NFS export
        '''

        client_state = self.module.params['client_state']
        if playbook_client_dict['read_only_clients'] is None:
            return mod_flag, nfs_export

        if client_state is None:
            if sorted(playbook_client_dict['read_only_clients']) != sorted(current_client_dict['read_only_clients']):
                current_client_dict['read_only_clients'] = playbook_client_dict['read_only_clients']
                mod_flag = True
        for client in playbook_client_dict['read_only_clients']:
            if client_state == 'present-in-export' and client not in current_client_dict['read_only_clients']:
                current_client_dict['read_only_clients'].append(client)
                mod_flag = True

            elif client_state == 'absent-in-export' and client in current_client_dict['read_only_clients']:
                current_client_dict['read_only_clients'].remove(client)
                mod_flag = True

        if mod_flag:
            nfs_export.read_only_clients = current_client_dict['read_only_clients']

        return mod_flag, nfs_export

    def _check_root_clients(self, nfs_export, playbook_client_dict, current_client_dict, mod_flag):
        '''
        Check if root clients are to be added/removed to/from NFS export
        '''

        client_state = self.module.params['client_state']
        if playbook_client_dict['root_clients'] is None:
            return mod_flag, nfs_export

        if client_state is None:
            if sorted(playbook_client_dict['root_clients']) != sorted(current_client_dict['root_clients']):
                current_client_dict['root_clients'] = playbook_client_dict['root_clients']
                mod_flag = True
        for client in playbook_client_dict['root_clients']:
            if client_state == 'present-in-export' and client not in current_client_dict['root_clients']:
                current_client_dict['root_clients'].append(client)
                mod_flag = True

            elif client_state == 'absent-in-export' and client in current_client_dict['root_clients']:
                current_client_dict['root_clients'].remove(client)
                mod_flag = True

        if mod_flag:
            nfs_export.root_clients = current_client_dict['root_clients']

        return mod_flag, nfs_export

    def _check_client_status(self, nfs_export):
        '''
        Check if clients are to be added to NFS export
        '''
        playbook_client_dict = self._create_current_client_dict_from_playbook()
        current_client_dict = self._create_current_client_dict()
        mod_flag = False

        mod_flag, nfs_export = self._check_read_write_clients(nfs_export, playbook_client_dict, current_client_dict, mod_flag)
        mod_flag, nfs_export = self._check_clients(nfs_export, playbook_client_dict, current_client_dict, mod_flag)
        mod_flag, nfs_export = self._check_read_only_clients(nfs_export, playbook_client_dict, current_client_dict, mod_flag)
        mod_flag, nfs_export = self._check_root_clients(nfs_export, playbook_client_dict, current_client_dict, mod_flag)
        return mod_flag, nfs_export

    def _check_mod_field(self, field_name_playbook, field_name_powerscale):
        _field_mod = False
        # Use .get to avoid KeyError when optional playbook fields are not present
        play_val = self.module.params.get(field_name_playbook, None)
        # Safe read from result in case the powerscale field is absent
        res_details = self.result.get('NFS_export_details', {}) or {}
        res_val = res_details.get(field_name_powerscale, None)
        # Special handling for time_delta: convert playbook dict to seconds before compare
        if field_name_playbook == 'time_delta' and play_val is not None:
            try:
                play_val_converted = utils.convert_to_seconds(play_val.get('time_value'), play_val.get('time_unit'))
            except Exception:
                play_val_converted = play_val
            play_val = play_val_converted

        if play_val is None:
            field_value = res_val
        elif play_val == res_val:
            field_value = res_val
        else:
            field_value = play_val
            _field_mod = True
        return _field_mod, field_value

    def _is_security_flavour_mod(self, security_flavors, nfs_export):
        """Check whether security flavours modification required"""
        if security_flavors is not None:
            security_flavors = get_security_keys(security_flavors)
            if set(security_flavors) != set(
                    self.result['NFS_export_details']['security_flavors']):
                nfs_export.security_flavors = list(security_flavors)
                return True, nfs_export
        return False, nfs_export

    def modify_nfs_export(self, path, access_zone, ignore_unresolvable_hosts):
        '''
        Modify NFS export in system
        '''
        nfs_details = copy.deepcopy(self.result.get('NFS_export_details'))

        nfs_export = self.isi_sdk.NfsExport()
        client_flag = map_root_flag = map_non_root_flag = False
        client_flag, nfs_export = self._check_client_status(nfs_export)

        map_root = set_nfs_map(self.module.params.get('map_root'), 'map_root', self.result.get('NFS_export_details'))
        if map_root:
            nfs_export.map_root = map_root
            map_root_flag = True
        map_non_root = set_nfs_map(self.module.params.get('map_non_root'), 'map_non_root', self.result.get('NFS_export_details'))
        if map_non_root:
            nfs_export.map_non_root = map_non_root
            map_non_root_flag = True
        map_failure = set_nfs_map(self.module.params.get('map_failure'), 'map_failure', self.result.get('NFS_export_details'))
        if map_failure:
            nfs_export.map_failure = map_failure
            map_failure_flag = True
        else:
            map_failure_flag = False

        # size fields: if provided in playbook, convert to bytes and compare to existing
        size_fields = ['file_name_max_size', 'block_size', 'directory_transfer_size',
                       'read_transfer_max_size', 'read_transfer_multiple', 'read_transfer_size',
                       'write_transfer_max_size', 'write_transfer_multiple', 'write_transfer_size',
                       'max_file_size']
        size_flags = []
        for sz in size_fields:
            param = self.module.params.get(sz)
            if param is not None:
                try:
                    new_val = utils.get_size_bytes(param['size_value'], param['size_unit'])
                except Exception:
                    new_val = None
                # keys in NFS export details sometimes differ (file_name_max_size -> name_max_size)
                export_key = 'name_max_size' if sz == 'file_name_max_size' else sz
                export_value = None
                if self.result.get('NFS_export_details'):
                    export_value = self.result['NFS_export_details'].get(export_key)
                # consider modified only if the converted value differs from existing
                if new_val is None or export_value is None or new_val != export_value:
                    nfs_export.__setattr__(export_key, new_val)
                    size_flags.append(True)
                else:
                    size_flags.append(False)
            else:
                size_flags.append(False)

        # simple fields that can be compared using _check_mod_field
        read_only_flag, read_only_value = self._check_mod_field(
            'read_only', 'read_only')
        all_dirs_flag, all_dirs_value = self._check_mod_field(
            'sub_directories_mountable', 'all_dirs')
        description_flag, description_value = self._check_mod_field(
            'description', 'description')
        map_lookup_uid_flag, map_lookup_uid_value = self._check_mod_field(
            'map_lookup_uid', 'map_lookup_uid')
        commit_flag, commit_value = self._check_mod_field('commit_asynchronous', 'commit_asynchronous')
        setattr_flag, setattr_value = self._check_mod_field('setattr_asynchronous', 'setattr_asynchronous')
        readdir_flag, readdir_value = self._check_mod_field('readdirplus', 'readdirplus')
        return32_flag, return32_value = self._check_mod_field('return_32bit_file_ids', 'return_32bit_file_ids')
        can_set_time_flag, can_set_time_value = self._check_mod_field('can_set_time', 'can_set_time')
        symlinks_flag, symlinks_value = self._check_mod_field('symlinks', 'symlinks')
        encoding_flag, encoding_value = self._check_mod_field('encoding', 'encoding')
        write_datasync_action_flag, write_datasync_action_value = self._check_mod_field('write_datasync_action', 'write_datasync_action')
        write_datasync_reply_flag, write_datasync_reply_value = self._check_mod_field('write_datasync_reply', 'write_datasync_reply')
        write_filesync_action_flag, write_filesync_action_value = self._check_mod_field('write_filesync_action', 'write_filesync_action')
        write_filesync_reply_flag, write_filesync_reply_value = self._check_mod_field('write_filesync_reply', 'write_filesync_reply')
        write_unstable_action_flag, write_unstable_action_value = self._check_mod_field('write_unstable_action', 'write_unstable_action')
        write_unstable_reply_flag, write_unstable_reply_value = self._check_mod_field('write_unstable_reply', 'write_unstable_reply')
        time_delta_flag, time_delta_value = self._check_mod_field('time_delta', 'time_delta')
        security_flag, nfs_export = self._is_security_flavour_mod(
            self.module.params['security_flavors'], nfs_export)

        # consider changed if any of our flags are True
        all_flags = [client_flag, read_only_flag, all_dirs_flag, description_flag, map_root_flag,
                     map_non_root_flag, map_failure_flag, security_flag, map_lookup_uid_flag,
                     commit_flag, setattr_flag, readdir_flag, return32_flag, can_set_time_flag,
                     symlinks_flag, encoding_flag, write_datasync_action_flag, write_datasync_reply_flag,
                     write_filesync_action_flag, write_filesync_reply_flag, write_unstable_action_flag,
                     write_unstable_reply_flag, time_delta_flag] + size_flags

        if all(field_mod_flag is False for field_mod_flag in all_flags):
            LOG.info(
                'No change detected for the NFS Export, returning changed = False')
            if self.module._diff:
                self.result.update({"diff": {"before": nfs_details, "after": nfs_details}})
            return False
        else:
            nfs_export.read_only = read_only_value if read_only_flag else None
            nfs_export.all_dirs = all_dirs_value if all_dirs_flag else None
            nfs_export.description = description_value if description_flag else None
            # apply simple fields
            if map_lookup_uid_flag:
                nfs_export.map_lookup_uid = map_lookup_uid_value
            if commit_flag:
                nfs_export.commit_asynchronous = commit_value
            if setattr_flag:
                nfs_export.setattr_asynchronous = setattr_value
            if readdir_flag:
                nfs_export.readdirplus = readdir_value
            if return32_flag:
                nfs_export.return_32bit_file_ids = return32_value
            if can_set_time_flag:
                nfs_export.can_set_time = can_set_time_value
            if symlinks_flag:
                nfs_export.symlinks = symlinks_value
            if encoding_flag:
                nfs_export.encoding = encoding_value
            if write_datasync_action_flag:
                nfs_export.write_datasync_action = write_datasync_action_value
            if write_datasync_reply_flag:
                nfs_export.write_datasync_reply = write_datasync_reply_value
            if write_filesync_action_flag:
                nfs_export.write_filesync_action = write_filesync_action_value
            if write_filesync_reply_flag:
                nfs_export.write_filesync_reply = write_filesync_reply_value
            if write_unstable_action_flag:
                nfs_export.write_unstable_action = write_unstable_action_value
            if write_unstable_reply_flag:
                nfs_export.write_unstable_reply = write_unstable_reply_value
            if time_delta_flag:
                nfs_export.time_delta = time_delta_value
            # sizes already set above when present

            return self.perform_modify_nfs_export(nfs_export, path, access_zone, ignore_unresolvable_hosts, nfs_details)

    def perform_modify_nfs_export(self, nfs_export, path, access_zone, ignore_unresolvable_hosts, nfs_details):
        '''
        Modify NFS export in PowerScale system
        '''
        modified_details = copy.deepcopy(nfs_details)
        filtered_dict = {key: value for key, value in nfs_export.to_dict().items() if value is not None}
        modified_details.update(filtered_dict)

        if self.module._diff:
            self.result.update({"diff": {"before": nfs_details, "after": modified_details}})

        self.result['NFS_export_details'] = nfs_details
        try:
            if not self.module.check_mode:
                if ignore_unresolvable_hosts is not True:
                    self.protocol_api.update_nfs_export(
                        nfs_export,
                        self.result['NFS_export_details']['id'],
                        zone=self.result['NFS_export_details']['zone'])
                else:
                    self.protocol_api.update_nfs_export(
                        nfs_export,
                        self.result['NFS_export_details']['id'],
                        zone=self.result['NFS_export_details']['zone'],
                        ignore_unresolvable_hosts=ignore_unresolvable_hosts)
                # update result with updated details
                self.result['NFS_export_details'] = self.get_nfs_export(
                    path, access_zone)
            return True

        except Exception as e:
            error_msg = 'Modify NFS export for path: {0} and access zone:' \
                ' {1} failed with error: {2}'.format(
                    path, access_zone, utils.determine_error(e))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def delete_nfs_export(self):
        '''
        Delete NFS export from system
        '''
        nfs_export = self.result['NFS_export_details']
        if self.module._diff:
            self.result.update({"diff": {"before": nfs_export, "after": {}}})
        try:
            if not self.module.check_mode:
                msg = ('Deleting NFS export with path: {0}, zone: {1} and ID: {2}'.format(
                    nfs_export['paths'][0], nfs_export['zone'], nfs_export['id']))
                LOG.info(msg)
                self.protocol_api.delete_nfs_export(
                    nfs_export['id'], zone=nfs_export['zone'])

                self.result['NFS_export_details'] = {}
            return True
        except Exception as e:
            error_msg = (
                'Delete NFS export with path: {0}, zone: {1}, id: {2} failed'
                ' with error {3}'.format(
                    nfs_export['paths'][0],
                    nfs_export['zone'],
                    nfs_export['id'],
                    utils.determine_error(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def effective_path(self, access_zone, path):
        """Get the effective path for any access zone"""
        if access_zone is not None and access_zone.lower() == "system":
            if path is not None and not path.startswith('/'):
                err_msg = (f"Invalid path {path}, Path must start "
                           f"with '/'")
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
        elif access_zone is not None and access_zone.lower() != "system":
            if path is not None and not path.startswith('/'):
                path = f"/{path}"
            path = self.get_zone_base_path(access_zone) + path
        return path

    def _validate_input(self):
        all_client_list = self._create_client_lists_from_playbook()
        if self.module.params['client_state'] is not None and all(
                client_list is None for client_list in all_client_list):
            error_msg = 'Invalid input: Client state is given, clients not specified'
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_size_paramters(self):
        """Return the Ansible argument spec for size parameters (value + unit)."""
        return dict(type='dict', options=dict(
                    size_value=dict(type='int', required=True),
                    size_unit=dict(type='str', required=True, choices=['B', 'KB', 'MB', 'GB', 'TB', 'PB'])))

    def get_nfs_map_parameters(self):
        """Return the Ansible argument spec for NFS map parameters."""
        return dict(type='dict', options=dict(
            enabled=dict(type='bool', default=True),
            primary_group=dict(),
            secondary_groups=dict(type='list', elements='dict', options=dict(
                                  name=dict(required=True),
                                  state=dict(choices=['present', 'absent'], default='present'))),
            user=dict()))

    def get_sync_parameters(self):
        """Return the Ansible argument spec for write sync choice parameters."""
        return dict(type='str', choices=['DATASYNC', 'FILESYNC', 'UNSTABLE'])

    def get_nfs_parameters(self):
        return dict(
            path=dict(required=True, type='str'),
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
            ignore_unresolvable_hosts=dict(type='bool'),
            sub_directories_mountable=dict(type='bool'),
            security_flavors=dict(
                type='list', elements='str',
                choices=['unix', 'kerberos', 'kerberos_integrity',
                         'kerberos_privacy']),
            # Advanced per-export NFS settings (mirror of nfs_default_settings)
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
            map_root=self.get_nfs_map_parameters(),
            map_non_root=self.get_nfs_map_parameters(),
            state=dict(required=True, type='str', choices=['present',
                                                           'absent'])
        )


def get_security_keys(security_flavors):
    """ Get valid keys as per SDK valid values"""
    if security_flavors is not None:
        for i in range(len(security_flavors)):
            if security_flavors[i] == "kerberos":
                security_flavors[i] = "krb5"
            elif security_flavors[i] == "kerberos_integrity":
                security_flavors[i] = "krb5i"
            elif security_flavors[i] == "kerberos_privacy":
                security_flavors[i] = "krb5p"
            else:
                security_flavors[i] = "unix"
        return security_flavors
    return None


def set_nfs_map(map_params, map_type, nfs_export_details=None):
    """
    Set the map root or non-root object based on input

    Args:
        map_params (dict): The map parameters
        map_type (str): The type of map (root or non-root)
        nfs_export_details (dict, optional): The NFS export details

    Returns:
        nfs_map_object (object): The modified NFS map object
    """
    if map_params is not None:
        nfs_map_object = utils.get_nfs_map_object()
        nfs_map_object = initialize_nfs_map(nfs_map_object, nfs_export_details, map_type)
        nfs_map_object.enabled = map_params.get('enabled')
        if nfs_map_object.enabled is not False:
            nfs_map_object = set_nfs_map_object(nfs_map_object, map_params)

        changed = is_nfs_map_modified(map_type, nfs_map_object, nfs_export_details, map_params)
        if changed or not nfs_export_details:
            return nfs_map_object


def set_nfs_map_object(nfs_map_object, map_params):
    if map_params['user']:
        user = {'name': map_params.get('user')}
        nfs_map_object.user = user

    if map_params['primary_group']:
        group = {'name': map_params.get('primary_group')}
        nfs_map_object.primary_group = group

    groups = nfs_map_object.secondary_groups.copy()
    new_groups = []
    secondary_groups = map_params.get('secondary_groups') or []
    for secondary_group in secondary_groups:
        group = [nfs_map for nfs_map in groups if nfs_map.get('id').split(':')[1] == secondary_group.get('name')]
        if secondary_group.get('state') == 'absent' and group:
            groups.remove(group[0])
        elif secondary_group.get('state') != 'absent' and not group:
            group = {'id': secondary_group.get('name')}
            new_groups.append(group)
    nfs_map_object.secondary_groups = groups + new_groups
    return nfs_map_object


def initialize_nfs_map(nfs_map_object, nfs_export_details, map_type):
    """
    Initialize the map object with details from nfs_export_details.

    Args:
        nfs_map_object (object): The map object to be initialized.
        nfs_export_details (dict): The details of the NFS export.
        map_type (str): The type of map to be initialized.

    Returns:
        object: The initialized map object.

    """
    if nfs_export_details and nfs_export_details[map_type]:
        nfs_map_object.enabled = {'id': nfs_export_details[map_type].get('enabled')}
        nfs_map_object.user = {'id': nfs_export_details[map_type].get('user').get('id')} \
            if nfs_export_details[map_type].get('user').get('id') else None
        nfs_map_object.primary_group = {'id': nfs_export_details[map_type].get('primary_group').get('id')} \
            if nfs_export_details[map_type].get('primary_group').get('id') else None
        nfs_map_object.secondary_groups = nfs_export_details[map_type]['secondary_groups']
    else:
        nfs_map_object.user = nfs_map_object.primary_group = None
        nfs_map_object.secondary_groups = []
    return nfs_map_object


def is_nfs_map_modified(map_type, nfs_export_map, nfs_export_details, nfs_map_params):
    """
    Check if nfs map object is modified.

    Args:
        map_type (str): Type of the map.
        nfs_export_map (NfsExportMap): The nfs export map object.
        nfs_export_details (dict): A dictionary containing details of nfs export maps.
        nfs_map_params (dict): A dictionary containing the parameters to compare with the export map object.

    Returns:
        bool: True if the nfs map object is modified, False otherwise.
    """
    if nfs_export_map is not None and nfs_export_details:
        if nfs_map_params['enabled'] is not None and nfs_export_map.enabled != nfs_export_details[map_type]['enabled']:
            return True
        if nfs_map_params['enabled'] is not False:
            if is_map_user_modified(nfs_map_params, nfs_export_details, nfs_export_map, map_type) or \
                    is_map_primary_group_modified(nfs_map_params, nfs_export_details, nfs_export_map, map_type) or \
                    is_map_secondary_groups_modified(nfs_map_params, nfs_export_details, nfs_export_map, map_type):
                return True


def is_map_user_modified(nfs_map_params, nfs_export_details, nfs_export_map, map_type):
    if nfs_map_params['user'] is not None and \
            nfs_export_map.user.get('name') != nfs_export_details[map_type]['user']['id'].split(':')[1]:
        return True


def is_map_primary_group_modified(nfs_map_params, nfs_export_details, nfs_export_map, map_type):
    if nfs_map_params['primary_group'] is not None and \
            nfs_export_map.primary_group.get('name') != nfs_export_details[map_type]['primary_group']['id'].split(':')[1]:
        return True


def is_map_secondary_groups_modified(nfs_map_params, nfs_export_details, nfs_export_map, map_type):
    if nfs_map_params['secondary_groups'] is not None and \
            nfs_export_map.secondary_groups != nfs_export_details[map_type]['secondary_groups']:
        return True


class NFSExitHandler:
    def handle(self, nfs_obj, changed):
        LOG.info('changed %s', changed)
        nfs_obj.result['changed'] = changed
        nfs_obj.module.exit_json(**nfs_obj.result)


class NFSDeleteHandler:
    def handle(self, nfs_obj, nfs_params, changed):
        if nfs_params['state'] == 'absent' and nfs_obj.result['NFS_export_details']:
            # delete nfs export
            changed = nfs_obj.delete_nfs_export() or changed
        NFSExitHandler().handle(nfs_obj=nfs_obj, changed=changed)


class NFSCreateHandler:
    def handle(self, nfs_obj, nfs_params, path, changed):
        if nfs_params['state'] == 'present' and not nfs_obj.result['NFS_export_details']:
            changed = nfs_obj.create_nfs_export(
                path=path, access_zone=nfs_params['access_zone'],
                ignore_unresolvable_hosts=nfs_params['ignore_unresolvable_hosts'])
        NFSDeleteHandler().handle(nfs_obj=nfs_obj, nfs_params=nfs_params, changed=changed)


class NFSModifyHandler:
    def handle(self, nfs_obj, nfs_params, path, changed):
        if nfs_params['state'] == 'present' and nfs_obj.result['NFS_export_details']:
            # check for modification
            changed = nfs_obj.modify_nfs_export(path, nfs_params['access_zone'], nfs_params['ignore_unresolvable_hosts']) or changed
        NFSCreateHandler().handle(nfs_obj=nfs_obj, nfs_params=nfs_params, path=path, changed=changed)


class NFSHandler:
    def handle(self, nfs_obj, nfs_params):
        changed = False
        path = nfs_obj.effective_path(access_zone=nfs_params['access_zone'], path=nfs_params['path'])
        nfs_obj.result['NFS_export_details'] = nfs_obj.get_nfs_export(
            path=path, access_zone=nfs_params['access_zone'])
        nfs_obj._validate_input()
        NFSModifyHandler().handle(nfs_obj=nfs_obj, nfs_params=nfs_params, path=path, changed=changed)


def main():
    """ Perform action on PowerScale nfs_export object and perform action on it
        based on user input from playbook."""
    obj = NfsExport()
    NFSHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
