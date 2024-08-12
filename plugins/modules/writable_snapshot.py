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
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.powerscale_base \
    import PowerScaleBase

LOG = utils.get_logger('writable_snapshot')


class WritableSnapshot(PowerScaleBase):
    def __init__(self):
        """
        Initializes the class instance.

        :param self: The class instance.
        """

        ansible_module_params = {
            'argument_spec': self.get_writable_snapshot_parameters(),
            'supports_check_mode': True
        }
        super().__init__(AnsibleModule, ansible_module_params)

        self.result.update({
            "writable_snapshot_details": {}
        })

        if self.module._diff:
            self.result.update({"diff": {"before": [], "after": []}})

    def get_writable_snapshot_parameters(self):
        return {
            "writable_snapshot":
            {"type": 'list', "elements": 'dict', "options":
             {"dst_path": {"type": 'path', "required": True},
              "src_snap": {"type": 'str', "required": False},
              "state": {"type": 'str', "required": False, "choices": ['present', 'absent'], "default": 'present'},
              },
             "required_if": [("state", "present", ("src_snap",))]
             }
        }

    def segregate_snapshots(self, module_params):
        writable_snapshot = module_params.get('writable_snapshot')
        snapshots_to_create, snapshots_to_delete, invalid_snapshots = [], [], []
        create_paths = set()
        delete_paths = set()
        for snapshot_dict in writable_snapshot:
            if snapshot_dict.get('state') == 'present':
                if not self.validate_src_snap(snapshot_dict.get('src_snap')):
                    invalid_snapshots.append(snapshot_dict)
                else:
                    create_paths.add(snapshot_dict.get("dst_path"))
                    snapshots_to_create.append(snapshot_dict)
            else:
                delete_paths.add(snapshot_dict.get("dst_path"))
                snapshots_to_delete.append(snapshot_dict)
        common_paths = create_paths & delete_paths
        create_snapshots = [s for s in snapshots_to_create if s['dst_path'] not in common_paths]
        delete_snapshots = [s for s in snapshots_to_delete if s['dst_path'] not in common_paths]
        return create_snapshots, delete_snapshots, invalid_snapshots

    def validate_src_snap(self, snapshot_name):
        try:
            return self.snapshot_api.get_snapshot_snapshot(snapshot_name)
        except Exception:
            return False

    def get_writable_snapshot(self, dst_path):
        try:
            snapshot_out = self.snapshot_api.get_snapshot_writable_wspath(
                snapshot_writable_wspath=dst_path
            ).to_dict().get("writable")
            writable_snapshot_exists = True if snapshot_out else False
            return writable_snapshot_exists, snapshot_out
        except Exception:
            return False, []

    def create_filesystem_snapshot(self, snapshots_to_create):
        """Create a writable snapshot on PowerScale"""
        create_result = []
        existing_snapshot_list = []
        changed_flag = False
        for create_snapshot_dict in snapshots_to_create:
            try:
                snapshot_exits, existing_snapshot = self.get_writable_snapshot(create_snapshot_dict.get("dst_path"))
                if not snapshot_exits:
                    if not self.module.check_mode:
                        writable_snapshot_create_item = self.isi_sdk.SnapshotWritableItem(
                            dst_path=create_snapshot_dict.get("dst_path"),
                            src_snap=create_snapshot_dict.get("src_snap")
                        )
                        output = self.snapshot_api.create_snapshot_writable_item(writable_snapshot_create_item)
                        create_result.append(output.to_dict())
                    changed_flag = True
                else:
                    existing_snapshot_list.append(existing_snapshot)
            except Exception as e:
                error_msg = utils.determine_error(error_obj=e)
                error_message = 'Failed to create writable snapshot: {0} for ' \
                    'with error: {1}'.format(create_snapshot_dict.get("dst_path"), str(error_msg))
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
        if self.module._diff:
            self.result["diff"]["before"].extend(existing_snapshot_list)
            self.result["diff"]["after"].extend(create_result)
        return changed_flag, create_result

    def delete_writable_snapshot(self, snapshots_to_delete):
        changed_flag = False
        existing_snpashot_list = []
        for delete_snapshot_dict in snapshots_to_delete:
            dst_path = delete_snapshot_dict.get('dst_path')
            try:
                snapshot_exits, existing_snapshot = self.get_writable_snapshot(dst_path)
                if snapshot_exits:
                    if not self.module.check_mode:
                        self.snapshot_api.delete_snapshot_writable_wspath(snapshot_writable_wspath=dst_path)
                    changed_flag = True
                existing_snpashot_list.append(existing_snapshot)
            except Exception as e:
                error_msg = utils.determine_error(error_obj=e)
                error_message = 'Failed to delete ' \
                                'snapshot: {0} with ' \
                                'error: {1}'.format(dst_path, str(error_msg))
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
        if self.module._diff:
            self.result["diff"]["before"].extend(existing_snpashot_list)
        return changed_flag


class WritableSnapshotHandler:
    def handle(self, writable_snapshot_obj, module_params):
        """
        Handles the writable_snapshot object based on the given module parameters.

        Args:
            writable_snapshot_obj (writable_snapshot): The writable_snapshot object to be handled.
            module_params (dict): The module parameters containing the writable_snapshot details.

        Returns:
            None
        """
        create_snapshots, delete_snapshots, invalid_snapshots = writable_snapshot_obj.segregate_snapshots(module_params)
        writable_snapshot_obj.result['changed'] = False
        WritableSnapshotCreateHandler().handle(writable_snapshot_obj, create_snapshots, delete_snapshots, invalid_snapshots)


class WritableSnapshotCreateHandler:
    def handle(self, writable_snapshot_obj, create_snapshots, delete_snapshots, invalid_snapshots):
        """
        Handles the writable_snapshot object and its details.

        Args:
            writable_snapshot_obj (writable_snapshot): The writable_snapshot object to be handled.
            writable_snapshot_details (dict): The details of the writable_snapshot.

        Returns:
            None
        """
        create_details = []
        if create_snapshots:
            writable_snapshot_obj.result['changed'], create_details = writable_snapshot_obj.create_filesystem_snapshot(create_snapshots)
        WritableSnapshotDeleteHandler().handle(writable_snapshot_obj, delete_snapshots, invalid_snapshots, create_details)


class WritableSnapshotDeleteHandler:
    def handle(self, writable_snapshot_obj, delete_snapshots, invalid_snapshots, details):
        """
        Deletes a writable_snapshot using the provided writable_snapshot details.

        Args:
            writable_snapshot_obj (writable_snapshot): The writable_snapshot object to delete.
            writable_snapshot_details (dict): The details of the writable_snapshot to delete.

        Returns:
            tuple: A tuple containing a boolean indicating
            if the writable_snapshot was deleted successfully,
            and a dictionary of details about the deletion process.
        """
        if delete_snapshots:
            changed = writable_snapshot_obj.delete_writable_snapshot(delete_snapshots)
            writable_snapshot_obj.result['changed'] = changed or writable_snapshot_obj.result['changed']
        WritableSnapshotExitHandler().handle(writable_snapshot_obj, invalid_snapshots, details)


class WritableSnapshotExitHandler:

    def handle(self, writable_snapshot_obj, invalid_snapshots, writable_snapshot_details):
        """
        Handles the writable_snapshot object and writable_snapshot details.

        Args:
            writable_snapshot_obj (writable_snapshot): The writable_snapshot object.
            writable_snapshot_details (dict): The details of the writable_snapshot.

        Returns:
            None
        """
        writable_snapshot_obj.result['writable_snapshot_details'] = writable_snapshot_details
        if invalid_snapshots:
            writable_snapshot_obj.result['failed_writable_snapshots'] = invalid_snapshots
            writable_snapshot_obj.result['changed'] = False
            writable_snapshot_obj.module.fail_json(
                msg="Few writable snapshots are not able to be created because the source path is invalid:",
                **writable_snapshot_obj.result)
        writable_snapshot_obj.module.exit_json(**writable_snapshot_obj.result)


def main():
    """Create PowerScale WritableSnapshot object and perform action on it
        based on user input from playbook"""
    obj = WritableSnapshot()
    WritableSnapshotHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
