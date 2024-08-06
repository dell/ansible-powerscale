#!/usr/bin/python
# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

""" Ansible module for managing writable snapshots on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: writable_snapshot
version_added: '3.3.0'
short_description: Manage writable snapshots on PowerScale
description:
- You can perform the following operations.
- Managing snapshots on PowerScale.
- Create a writable snapshot.
- Delete a writable snapshot.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Kritika Bhateja(@Kritika-Bhateja-03) <ansible.team.dell.com>

options:
  writable_snapshot:
    description:
    - List of writable snapshot details.
    required: False
    type: list
    elements: dict
    suboptions:
      state:
        description:
        - The state of the writable snapshot to create or delete.
        - I(state) is C(present) - To create a writable snapshot.
        - I(state) is C(absent) - To delete the writable snapshot.
        default: present
        choices: ['present', 'absent']
        type: str
      dst_path:
        description:
        - The /ifs of the writable snapshot.
        - The destination path should be non-existing path and it's absolute path.
        required: true
        type: path
      src_snap:
        description:
        - The source snapshot name or ID.
        - This option is required I(state) is C(present).
        required: false
        type: str
'''

EXAMPLES = r'''
- name: To create a writable snapshot using ID
  dellemc.powerscale.writable_snapshot:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    writable_snapshot:
      - dst_path: "/ifs/test_one"
        src_snap: 2
        state: present
      - dst_path: "/ifs/test_two"
        src_snap: 2
        state: present

- name: To create a writable snapshot using Name
  dellemc.powerscale.writable_snapshot:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    writable_snapshot:
      - dst_path: "/ifs/test_one"
        src_snap: "Snapshot: 2024Apr15, 4:40 PM"
        state: present
      - dst_path: "/ifs/test_two"
        src_snap: "Snapshot: 2024Apr15, 4:40 PM"
        state: present

- name: To delete writable snapshot.
  dellemc.powerscale.writable_snapshot:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    writable_snapshot:
      - dst_path: "/ifs/test_one"
        state: absent
      - dst_path: "/ifs/test_two"
        sstate: absent

- name: To create and delete writable snapshot
  dellemc.powerscale.writable_snapshot:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    writable_snapshot:
      - dst_path: "/ifs/test_test"
        src_snap: 2
        state: present
      - dst_path: "/ifs/test_one"
        state: absent
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
    sample: "true"

writable_snapshot_details:
    description: The writable snapshot details.
    type: complex
    returned: When writable snapshot is created.
    contains:
        created:
            description: The creation timestamp.
            type: int
            sample: 1578514373
        dst_path:
            description: The directory path of the writable snapshot.
            type: str
            sample: /ifs/ansible/
        id:
            description: The writable snapshot ID.
            type: int
            sample: 23
        log_size:
            description: The logical size of the writable snapshot.
            type: int
            sample: 2048
        phys_size:
            description: The physical size of the writable snapshot.
            type: int
            sample: 2048
        src_id:
            description: the source snapshot ID.
            type: int
            sample: 2
        src_path:
            description: The directory path of the source snapshot.
            type: str
            sample: "/ifs/tfacc_file_system_test"
        src_snap:
            description: The directory path of the source snapshot.
            type: str
            sample: "Snapshot: 2024Apr15, 4:40 PM"
        state:
            description: The name of the source snapshot.
            type: str
            sample: active
    sample: [
        {
            "created": 1719895971,
            "dst_path": "/ifs/test_test",
            "id": 23,
            "log_size": 0,
            "phys_size": 2048,
            "src_id": 2,
            "src_path": "/ifs/tfacc_file_system_test",
            "src_snap": "Snapshot: 2024Apr15, 4:40 PM",
            "state": "active"
            }
        ]
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils


class WritableSnapshot(object):
    def __init__(self):
        """Define all the parameters required by this module"""

        self.module_params = utils \
            .get_powerscale_management_host_parameters()
        self.module_params.update(get_writable_snapshot_parameters())

        # initialize the Ansible module
        self.module = AnsibleModule(argument_spec=self.module_params,
                                    supports_check_mode=True,
                                    )

    def perform_module_operation(self):
        pass


def get_writable_snapshot_parameters():
    return dict(
        writable_snapshot=dict(type='list',
                               required=False,
                               elements='dict',
                               options=dict(
                                   dst_path=dict(required=True, type='path'),
                                   src_snap=dict(type='str'),
                                   state=dict(required=False, type='str',
                                              choices=['present', 'absent'],
                                              default='present')))
    )


def main():
    """Create PowerScale WritableSnapshot object and perform action on it
        based on user input from playbook"""
    obj = WritableSnapshot()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
