#!/usr/bin/python
# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

""" Ansible module for managing writable snapshots on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: writable_snapshots
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
  writable_snapshots:
    description:
    - List of writable snapshots details.
    required: false
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
attributes:
    check_mode:
        description: Runs task to validate without performing action on the target machine.
        support: full
    diff_mode:
        description: Runs the task to report the changes made or to be made.
        support: full
notes:
- The I(writable_snapshots) parameter will follow the order of deleting operations before creating operations.
'''

EXAMPLES = r'''
- name: To create a writable snapshot using ID
  dellemc.powerscale.writable_snapshots:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    writable_snapshots:
      - dst_path: "/ifs/test_one"
        src_snap: 2
        state: present
      - dst_path: "/ifs/test_two"
        src_snap: 2
        state: present

- name: To create a writable snapshot using Name
  dellemc.powerscale.writable_snapshots:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    writable_snapshots:
      - dst_path: "/ifs/test_one"
        src_snap: "Snapshot: 2024Apr15, 4:40 PM"
        state: present
      - dst_path: "/ifs/test_two"
        src_snap: "Snapshot: 2024Apr15, 4:40 PM"
        state: present

- name: To delete writable snapshot
  dellemc.powerscale.writable_snapshots:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    writable_snapshots:
      - dst_path: "/ifs/test_one"
        state: absent
      - dst_path: "/ifs/test_two"
        sstate: absent

- name: To create and delete writable snapshot
  dellemc.powerscale.writable_snapshots:
    onefs_host: "{{ onefs_host }}"
    verify_ssl: "{{ verify_ssl }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    writable_snapshots:
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
    sample: true

writable_snapshots_details:
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

LOG = utils.get_logger('writable_snapshots')


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
            "writable_snapshots_details": {}
        })

        if self.module._diff:
            self.result.update({"diff": {"before": {"writable_snapshots": []}, "after": {"writable_snapshots": []}}})

    def get_writable_snapshot_parameters(self):
        """
        Returns a dictionary with the parameters for the writable snapshots.

        Returns:
            dict: Dictionary with the parameters for the writable snapshots.

        """
        return {
            "writable_snapshots":
            {"type": 'list', "elements": 'dict', "options":
             {"dst_path": {"type": 'path', "required": True},
              "src_snap": {"type": 'str', "required": False},
              "state": {"type": 'str', "required": False, "choices": ['present', 'absent'], "default": 'present'},
              },
             "required_if": [("state", "present", ("src_snap",))]
             }
        }

    def segregate_snapshots(self, module_params):
        """
        This function is used to segregate the writable snapshots into snapshots to
        create and snapshots to delete.

        Parameters:
            module_params (dict): The parameters of the module.

        Returns:
            tuple: A tuple containing the following:
                - unique_snapshots_to_create (list): The list of unique snapshots to
                create.
                - snapshots_to_delete (list): The list of snapshots to delete.
                - invalid_snapshots (list): The list of invalid snapshots.
        """
        writable_snapshot = module_params.get('writable_snapshots')
        snapshots_to_create, snapshots_to_delete, invalid_snapshots = [], [], []
        for snapshot_dict in writable_snapshot:
            if snapshot_dict.get('state') == 'present':
                if not self.validate_src_snap(snapshot_dict.get('src_snap')) or not snapshot_dict.get('dst_path').startswith('/ifs/'):
                    invalid_snapshots.append(snapshot_dict)
                else:
                    snapshots_to_create.append(snapshot_dict)
            else:
                snapshots_to_delete.append(snapshot_dict)
        unique_snapshots_to_create = self.check_duplicate_snapshots_to_create(snapshots_to_create)
        return unique_snapshots_to_create, snapshots_to_delete, invalid_snapshots

    def check_duplicate_snapshots_to_create(self, snapshots_to_create):
        """
        Removes duplicate snapshots to create.

        Args:
            snapshots_to_create (List[Dict[str, Any]]): A list of dictionaries representing snapshots to create.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the unique snapshots to create.
        """
        unique_data = {}
        for item in snapshots_to_create:
            unique_data[item['dst_path']] = item
        result = list(unique_data.values())
        return result

    def validate_src_snap(self, snapshot_name):
        """
        Validates the source snapshot.

        Args:
            snapshot_name (str): The name of the snapshot.

        Returns:
            The output of the API call to get the snapshot, or False if an exception occurred.
        """
        try:
            output = self.snapshot_api.get_snapshot_snapshot(snapshot_name)
            return output
        except Exception:
            return False

    def get_writable_snapshot(self, dst_path):
        """
        Retrieves the writable snapshot for the given destination path.

        Args:
            dst_path (str): The destination path of the writable snapshot.

        Returns:
            tuple: A tuple containing two values. The first value is a boolean indicating
            whether the writable snapshot exists or not. The second value is the writable
            snapshot data if it exists, otherwise an empty list.
        """
        try:
            snapshot_out = self.snapshot_api.get_snapshot_writable_wspath(
                snapshot_writable_wspath=dst_path
            ).to_dict().get("writable")
            writable_snapshot_exists = True if snapshot_out else False
            return writable_snapshot_exists, snapshot_out[0]
        except Exception:
            return False, []

    def compare_src_snap(self, existing_snapshot, src_snap):
        """
        Compares the source snapshot of an existing snapshot with a given source snapshot.

        Args:
            existing_snapshot (dict): The existing snapshot.
            src_snap (Union[int, str]): The source of writable snapshot to be created.

        Returns:
            Tuple[bool, Union[int, str]]: A tuple containing two values. The first value is a boolean
            indicating whether the source snapshots are different. The second value is the source
            snapshot of the existing snapshot.
        """
        try:
            src_snap = int(src_snap)
            src_type = int
        except ValueError:
            src_type = str
        if src_type is int:
            existing_snapshot_src_snap = existing_snapshot.get("src_id")
        else:
            existing_snapshot_src_snap = existing_snapshot.get("src_snap")
        return existing_snapshot_src_snap != src_snap, existing_snapshot_src_snap

    def update_diff_before(self, dst_path, existing_snapshot_src_snap):
        """
        Updates the "diff" dictionary in the "result" dictionary with the given "dst_path" and "existing_snapshot_src_snap" before the module operation.

        Args:
            dst_path (str): The destination path of the writable snapshot.
            existing_snapshot_src_snap (Union[int, str]): The source snapshot of the existing snapshot.

        Returns:
            None

        """
        if self.module._diff:
            before_dict = [{"dst_path": dst_path, "src_snap": existing_snapshot_src_snap}]
            self.result["diff"]["before"]["writable_snapshots"].extend(before_dict)

    def update_diff_after(self, dst_path, src_snap):
        """
        Updates the "diff" dictionary in the "result" dictionary with the given "dst_path" and "src_snap" after the module operation.

        Args:
            dst_path (str): The destination path of the writable snapshot.
            src_snap (Union[int, str]): The source snapshot of the existing snapshot.

        Returns:
            None

        """
        if self.module._diff:
            after_dict = [{"dst_path": dst_path, "src_snap": src_snap}]
            self.result["diff"]["after"]["writable_snapshots"].extend(after_dict)

    def create_writable_snapshot(self, snapshots_to_create):
        """
        Create one or more writable snapshots.

        Args:
            snapshots_to_create (list): A list of dictionaries containing the details of the snapshots to create.

        Returns:
            tuple: A tuple containing a boolean indicating if any snapshots were created and a list of dictionaries
                   containing the details of all created snapshots.
        """
        create_result, existing_snapshot_list = [], []
        changed_flag = False
        for create_snapshot_dict in snapshots_to_create:
            dst_path = create_snapshot_dict.get("dst_path")
            src_snap = create_snapshot_dict.get("src_snap")
            try:
                snapshot_exists, existing_snapshot = self.get_writable_snapshot(dst_path)
                if not snapshot_exists:
                    output = self.handle_new_snapshot(dst_path, src_snap)
                    create_result.append(output)
                    changed_flag = True
                else:
                    changed, result = self.handle_existing_snapshot(dst_path, src_snap, existing_snapshot)
                    create_result.append(result)
                    if changed:
                        changed_flag = True
                    else:
                        existing_snapshot_list.append(existing_snapshot)
            except Exception as e:
                self.log_snapshot_creation_error(dst_path, e)

        result = create_result + existing_snapshot_list
        return changed_flag, result

    def handle_new_snapshot(self, dst_path, src_snap):
        """
        Handle creation of a new snapshot.

        Args:
            dst_path (str): The destination path of the writable snapshot.
            src_snap (str): The source snapshot name or ID.

        Returns:
            dict: A dictionary containing the details of the newly created snapshot.
        """
        writable_snapshot_create_item = self.isi_sdk.SnapshotWritableItem(
            dst_path=dst_path,
            src_snap=src_snap
        )
        self.update_diff_after(dst_path, src_snap)
        if not self.module.check_mode:
            output = self.snapshot_api.create_snapshot_writable_item(writable_snapshot_create_item)
            return output.to_dict()
        return {}

    def handle_existing_snapshot(self, dst_path, src_snap, existing_snapshot):
        """
        Handle updating an existing snapshot.

        Args:
            dst_path (str): The destination path of the writable snapshot.
            src_snap (str): The source snapshot name or ID.
            existing_snapshot (dict): The existing snapshot details.

        Returns:
            Tuple[bool, dict]: A tuple containing two values. The first value is a boolean
            indicating whether the snapshot has been updated. The second value is the
            dictionary containing the updated snapshot details.
        """
        src_snap_changed, existing_snapshot_src_snap = self.compare_src_snap(existing_snapshot, src_snap)
        output = {}
        if src_snap_changed:
            self.update_diff_before(dst_path, existing_snapshot_src_snap)
            if not self.module.check_mode:
                self.snapshot_api.delete_snapshot_writable_wspath(snapshot_writable_wspath=dst_path)
            output = self.handle_new_snapshot(dst_path, src_snap)
            return True, output
        return False, output

    def log_snapshot_creation_error(self, dst_path, error_obj):
        """
        Log an error encountered during snapshot creation.

        Args:
            dst_path (str): The destination path of the snapshot.
            error_obj (Exception): The error encountered.

        Returns:
            None
        """
        error_msg = utils.determine_error(error_obj=error_obj)
        error_message = 'Failed to create writable snapshot: {0} with error: {1}'.format(dst_path, str(error_msg))
        LOG.error(error_message)
        self.module.fail_json(msg=error_message)

    def delete_writable_snapshot(self, snapshots_to_delete):
        """
        Deletes writable snapshots based on the provided snapshot paths.

        Args:
            snapshots_to_delete (List[Dict[str, str]]): A list of dictionaries containing the paths of the snapshots to delete.

        Returns:
            bool: A boolean indicating whether the snapshots were successfully deleted.

        Raises:
            Exception: If an error occurs during the deletion process.

        """
        changed_flag = False
        existing_snpashot_list = []
        for delete_snapshot_dict in snapshots_to_delete:
            dst_path = delete_snapshot_dict.get('dst_path')
            try:
                snapshot_exits, existing_snapshot = self.get_writable_snapshot(dst_path)
                if snapshot_exits:
                    if not self.module.check_mode:
                        self.snapshot_api.delete_snapshot_writable_wspath(snapshot_writable_wspath=dst_path)
                    if self.module._diff:
                        before_dict = [{"dst_path": delete_snapshot_dict.get("dst_path")}]
                        self.result["diff"]["before"]["writable_snapshots"].extend(before_dict)
                    changed_flag = True
                if existing_snapshot:
                    existing_snpashot_list.append(existing_snapshot)
            except Exception as e:
                error_msg = utils.determine_error(error_obj=e)
                error_message = 'Failed to delete ' \
                                'snapshot: {0} with ' \
                                'error: {1}'.format(dst_path, str(error_msg))
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
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
        WritableSnapshotDeleteHandler().handle(writable_snapshot_obj, create_snapshots, delete_snapshots, invalid_snapshots)


class WritableSnapshotDeleteHandler:
    def handle(self, writable_snapshot_obj, create_snapshots, delete_snapshots, invalid_snapshots):
        """
        Deletes a writable_snapshot using the provided writable_snapshot details.

        Args:
            writable_snapshot_obj (writable_snapshot): The writable_snapshot object to delete.
            writable_snapshots_details (dict): The details of the writable_snapshot to delete.

        Returns:
            tuple: A tuple containing a boolean indicating
            if the writable_snapshot was deleted successfully,
            and a dictionary of details about the deletion process.
        """
        if delete_snapshots:
            changed = writable_snapshot_obj.delete_writable_snapshot(delete_snapshots)
            writable_snapshot_obj.result['changed'] = changed or writable_snapshot_obj.result['changed']
        WritableSnapshotCreateHandler().handle(writable_snapshot_obj, create_snapshots, invalid_snapshots)


class WritableSnapshotCreateHandler:
    def handle(self, writable_snapshot_obj, create_snapshots,
               invalid_snapshots):
        """
        Handles the writable_snapshot object and its details.

        Args:
            writable_snapshot_obj (writable_snapshot): The writable_snapshot object to be handled.
            writable_snapshots_details (dict): The details of the writable_snapshot.

        Returns:
            None
        """
        create_details = []
        if create_snapshots:
            changed_flag, create_details = writable_snapshot_obj.create_writable_snapshot(create_snapshots)
            writable_snapshot_obj.result['changed'] = writable_snapshot_obj.result['changed'] or changed_flag
        details = [item for item in create_details if item]
        WritableSnapshotExitHandler().handle(writable_snapshot_obj, invalid_snapshots, details)


class WritableSnapshotExitHandler:

    def handle(self, writable_snapshot_obj, invalid_snapshots, writable_snapshots_details):
        """
        Handles the writable_snapshot object and writable_snapshot details.

        Args:
            writable_snapshot_obj (writable_snapshot): The writable_snapshot object.
            writable_snapshots_details (dict): The details of the writable_snapshot.

        Returns:
            None
        """
        writable_snapshot_obj.result['writable_snapshots_details'] = writable_snapshots_details
        if invalid_snapshots:
            writable_snapshot_obj.result['failed_writable_snapshots'] = invalid_snapshots
            writable_snapshot_obj.result['changed'] = False
            writable_snapshot_obj.module.fail_json(
                msg="Few writable snapshots are not able to be created because the destination path or source path is invalid.",
                **writable_snapshot_obj.result)
        writable_snapshot_obj.module.exit_json(**writable_snapshot_obj.result)


def main():
    """Create PowerScale WritableSnapshot object and perform action on it
        based on user input from playbook"""
    obj = WritableSnapshot()
    WritableSnapshotHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
