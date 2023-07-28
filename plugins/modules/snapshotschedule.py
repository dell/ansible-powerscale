#!/usr/bin/python
# Copyright: (c) 2019, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Ansible module for managing snapshot schedules on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: snapshotschedule
version_added: '1.2.0'
short_description: Manage snapshot schedules on PowerScale
description:
- You can perform the following operations.
- Managing snapshot schedules on PowerScale.
- Create snapshot schedule.
- Modify snapshot schedule.
- Get details of snapshot schedule.
- Delete snapshot schedule.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Akash Shendge (@shenda1) <ansible.team@dell.com>

options:
  name:
    description:
    - The name of the snapshot schedule.
    type: str
    required: true
  path:
    description:
    - The path on which the snapshot will be taken. This path is relative
      to the base path of the Access Zone.
    - For 'System' access zone, the path is absolute.
    - This parameter is required at the time of creation.
    - Modification of the path is not allowed through the Ansible module.
    type: str
  access_zone:
    description:
    - The effective path where the snapshot is created will
      be determined by the base path of the Access Zone and the
      path provided by the user in the playbook.
    type: str
    default: System
  new_name:
    description:
    - The new name of the snapshot schedule.
    type: str
  desired_retention:
    description:
    - The number of hours/days for which snapshots created by this snapshot
      schedule should be retained.
    - If retention is not specified at the time of creation, then the
      snapshots created by the snapshot schedule will be retained forever.
    - Minimum retention duration is 2 hours.
    - For large durations (beyond days/weeks), PowerScale may round off the
      retention to a somewhat larger value to match a whole number of
      days/weeks.
    type: int
  retention_unit:
    description:
    - The retention unit for the snapshot created by this schedule.
    type: str
    choices: [hours, days]
    default: hours
  alias:
    description:
    - The alias will point to the latest snapshot created by the snapshot
      schedule.
    type: str
  pattern:
    description:
    - Pattern expanded with strftime to create snapshot names.
    - This parameter is required at the time of creation.
    type: str
  schedule:
    description:
    - The isidate compatible natural language description of the schedule.
    - It specifies the frequency of the schedule.
    - This parameter is required at the time of creation.
    type: str
  state:
    description:
    - Defines whether the snapshot schedule should exist or not.
    type: str
    required: true
    choices: [absent, present]
notes:
- The I(check_mode) is not supported.
'''

EXAMPLES = r'''
- name: Create snapshot schedule
  dellemc.powerscale.snapshotschedule:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    name: "{{name}}"
    access_zone: '{{access_zone}}'
    path: '<path>'
    alias: "{{alias1}}"
    desired_retention: "{{desired_retention1}}"
    pattern: "{{pattern1}}"
    schedule: "{{schedule1}}"
    state: "{{state_present}}"

- name: Get details of snapshot schedule
  dellemc.powerscale.snapshotschedule:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    name: "{{name}}"
    state: "{{state_present}}"

- name: Rename snapshot schedule
  dellemc.powerscale.snapshotschedule:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    name: "{{name}}"
    new_name: "{{new_name}}"
    state: "{{state_present}}"

- name: Modify alias of snapshot schedule
  dellemc.powerscale.snapshotschedule:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    name: "{{new_name}}"
    alias: "{{alias2}}"
    state: "{{state_present}}"

- name: Modify pattern of snapshot schedule
  dellemc.powerscale.snapshotschedule:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    name: "{{new_name}}"
    pattern: "{{pattern2}}"
    state: "{{state_present}}"

- name: Modify schedule of snapshot schedule
  dellemc.powerscale.snapshotschedule:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    name: "{{new_name}}"
    schedule: "{{schedule2}}"
    state: "{{state_present}}"

- name: Modify retention of snapshot schedule
  dellemc.powerscale.snapshotschedule:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    name: "{{new_name}}"
    desired_retention: 2
    retention_unit: "{{retention_unit_days}}"
    state: "{{state_present}}"

- name: Delete snapshot schedule
  dellemc.powerscale.snapshotschedule:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    name: "{{new_name}}"
    state: "{{state_absent}}"

- name: Delete snapshot schedule - Idempotency
  dellemc.powerscale.snapshotschedule:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    name: "{{new_name}}"
    state: "{{state_absent}}"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool

snapshot_schedule_details:
    description: Details of the snapshot schedule including snapshot details.
    returned: When snapshot schedule exists
    type: complex
    contains:
        schedules:
            description: Details of snapshot schedule
            type: complex
            contains:
                duration:
                    description: Time in seconds added to creation time to construction
                                 expiration time
                    type: int
                id:
                    description: The system ID given to the schedule
                    type: int
                next_run:
                     description: Unix Epoch time of next snapshot to be created
                     type: int
                next_snapshot:
                     description: Formatted name of next snapshot to be created
                     type: str
        snapshot_list:
            description: List of snapshots taken by this schedule
            type: complex
            contains:
                snapshots:
                    description: Details of snapshot
                    type: complex
                    contains:
                        created:
                            description: The Unix Epoch time the snapshot was created
                            type: int
                        expires:
                            description: The Unix Epoch time the snapshot will expire and be
                                         eligible for automatic deletion.
                            type: int
                        id:
                            description: The system ID given to the snapshot.This is useful
                                         for tracking the status of delete pending snapshots
                            type: int
                        name:
                            description: The user or system supplied snapshot name.
                                         This will be null for snapshots pending delete
                            type: str
                        size:
                            description: The amount of storage in bytes used to store this snapshot
                            type: int
                total:
                    description: Total number of items available
                    type: int
    sample: {
        "schedules": [
            {
                "alias": null,
                "duration": 604800,
                "id": 1759,
                "name": "Atest",
                "next_run": 1687564800,
                "next_snapshot": "ScheduleName_duration_2023-06-24_00:00",
                "path": "/ifs",
                "pattern": "ScheduleName_duration_%Y-%m-%d_%H:%M",
                "schedule": "every 1 days at 12:00 AM"
            }
        ],
        "snapshot_list": {
            "resume": null,
            "snapshots": [],
            "total": 0
        }
    }
'''

import re
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('snapshotschedule')


class SnapshotSchedule(object):

    """Class with snapshot schedule operations"""

    def __init__(self):
        """ Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_snapshotschedule_parameters())

        # initialize the Ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False
        )

        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        self.api_instance = utils.isi_sdk.SnapshotApi(self.api_client)
        self.zone_summary_api = utils.isi_sdk.ZonesSummaryApi(self.api_client)
        LOG.info('Got python SDK instance for provisioning on PowerScale')

    def get_details(self, name):
        """Get snapshot schedule details"""
        try:
            api_response = self.api_instance.get_snapshot_schedule(name).\
                to_dict()
            snapshot_list = self.api_instance.list_snapshot_snapshots(
                schedule=name).to_dict()
            api_response['snapshot_list'] = snapshot_list
            return api_response
        except utils.ApiException as e:
            if str(e.status) == "404":
                error_message = "Snapshot schedule {0} details are not found"\
                    .format(name)
                LOG.info(error_message)
                return None
            else:
                error_msg = self.determine_error(error_obj=e)
                error_message = 'Get details of snapshot schedule {0} ' \
                                'failed with error: {1}'.format(name,
                                                                error_msg)
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
        except Exception as e:
            error_message = 'Get details of snapshot schedule {0} failed ' \
                            'with error: {1}'.format(name, str(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_zone_base_path(self, access_zone):
        """Returns the base path of the Access Zone."""
        try:
            zone_path = (self.zone_summary_api.
                         get_zones_summary_zone(access_zone)).to_dict()
            return zone_path['summary']['path']
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Unable to fetch base path of Access Zone {0} ' \
                            ',failed with error: {1}'.format(access_zone,
                                                             str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def validate_desired_retention(self, desired_retention):
        """Validates the specified desired retention"""
        if desired_retention <= 0:
            self.module.fail_json(msg="Please provide a valid integer "
                                      "as the desired retention.")

    def check_snapshot_schedule_modified(self, snapshot_schedule_details,
                                         alias, desired_retention,
                                         retention_unit, effective_path,
                                         pattern, schedule):
        """Determines whether the snapshot schedule needs to be modified"""
        modified = False
        snapshot_schedule_modify = {}

        if effective_path is not None and effective_path != \
                snapshot_schedule_details['schedules'][0]['path']:
            error_message = 'Modification of path of snapshot schedule is ' \
                            'not allowed through Ansible Module.'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

        if alias is not None and alias != \
                snapshot_schedule_details['schedules'][0]['alias']:
            LOG.info("Alias Modification")
            snapshot_schedule_modify['alias'] = alias
            modified = True

        if pattern is not None and pattern != snapshot_schedule_details[
                'schedules'][0]['pattern']:
            LOG.info("Pattern Modification")
            snapshot_schedule_modify['pattern'] = pattern
            modified = True

        if schedule is not None and schedule != snapshot_schedule_details[
                'schedules'][0]['schedule']:
            LOG.info("Schedule Modification")
            snapshot_schedule_modify['schedule'] = schedule
            modified = True

        if desired_retention is not None:
            retention_in_sec = 0
            if retention_unit == 'days':
                retention_in_sec = desired_retention * 24 * 60 * 60
            else:
                retention_in_sec = desired_retention * 60 * 60

            if retention_in_sec != snapshot_schedule_details['schedules'][
                    0]['duration']:
                if retention_in_sec < 7200:
                    self.module.fail_json(msg="The snapshot desired retention"
                                              " must be at least 2 hours")
                LOG.info("Retention Modification: new value=%s, old value=%s",
                         retention_in_sec, snapshot_schedule_details
                         ['schedules'][0]['duration'])
                snapshot_schedule_modify['duration'] = retention_in_sec
                modified = True
        return modified, snapshot_schedule_modify

    def create_snapshot_schedule(self, name, alias, effective_path,
                                 desired_retention, retention_unit,
                                 pattern, schedule):
        """Create snapshot schedule"""

        if effective_path is None:
            self.module.fail_json(msg="Path is mandatory while creating "
                                      "snapshot schedule")

        if pattern is None:
            self.module.fail_json(msg="Pattern is mandatory while creating "
                                      "snapshot schedule")

        if schedule is None:
            self.module.fail_json(msg="Schedule is mandatory while creating "
                                      "snapshot schedule")

        duration = 0
        if desired_retention is not None:
            if retention_unit == 'hours':
                duration = desired_retention * 60 * 60
            else:
                duration = desired_retention * 24 * 60 * 60

            if duration < 7200:
                self.module.fail_json(msg="The snapshot desired retention "
                                          "must be at least 2 hours")

        try:
            snapshot_schedule_create_param = utils.isi_sdk.\
                SnapshotScheduleCreateParams(name=name, alias=alias,
                                             path=effective_path,
                                             duration=duration,
                                             pattern=pattern,
                                             schedule=schedule)
            self.api_instance.create_snapshot_schedule(
                snapshot_schedule_create_param)
            return True
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Failed to create snapshot schedule: {0} for ' \
                            'path {1} with error: {2}'.format(
                                name, effective_path, error_msg)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def validate_new_name(self, new_name):
        """validate if the snapshot schedule with new_name already exists"""

        snapshot_schedules = self.get_details(new_name)

        if snapshot_schedules is not None:
            error_message = 'Snapshot schedule with name {0} already exists'.\
                format(new_name)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def rename_snapshot_schedule(self, snapshot_schedule_details, new_name):
        """Rename snapshot schedule"""

        try:
            snapshot_schedule_update_param = utils.isi_sdk.SnapshotSchedule(
                name=new_name)
            self.api_instance.update_snapshot_schedule(
                snapshot_schedule_update_param,
                snapshot_schedule_details['schedules'][0]['name'])
            return True
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Failed to rename snapshot schedule {0} with ' \
                            'error : {1}'.\
                format(snapshot_schedule_details['schedules'][0]['name'],
                       error_msg)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def modify_snapshot_schedule(self, name,
                                 snapshot_schedule_modification_details):
        """Modify snapshot schedule"""
        snapshot_schedule_update_param = self.isi_sdk.SnapshotSchedule()

        try:
            if 'alias' in snapshot_schedule_modification_details:
                snapshot_schedule_update_param.alias = \
                    snapshot_schedule_modification_details['alias']
            if 'pattern' in snapshot_schedule_modification_details:
                snapshot_schedule_update_param.pattern = \
                    snapshot_schedule_modification_details['pattern']
            if 'schedule' in snapshot_schedule_modification_details:
                snapshot_schedule_update_param.schedule = \
                    snapshot_schedule_modification_details['schedule']
            if 'duration' in snapshot_schedule_modification_details:
                snapshot_schedule_update_param.duration = \
                    snapshot_schedule_modification_details['duration']

            self.api_instance.update_snapshot_schedule(
                snapshot_schedule_update_param, name)
            return True
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Failed to modify snapshot schedule {0} with ' \
                            'error : {1}'.format(name, error_msg)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete_snapshot_schedule(self, name):
        """Delete snapshot schedule"""
        try:
            self.api_instance.delete_snapshot_schedule(name)
            return True
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Failed to delete snapshot schedule: {0} with ' \
                            'error: {1}'.format(name, error_msg)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def determine_error(self, error_obj):
        """Determine the error message to return"""
        if isinstance(error_obj, utils.ApiException):
            error = re.sub("[\n \"]+", ' ', str(error_obj.body))
        else:
            error = error_obj
        return error

    def perform_module_operation(self):
        """
        Perform different actions on snapshot schedule module based on
        parameters chosen in playbook
        """
        name = self.module.params['name']
        state = self.module.params['state']
        access_zone = self.module.params['access_zone']
        path = self.module.params['path']
        new_name = self.module.params['new_name']
        pattern = self.module.params['pattern']
        schedule = self.module.params['schedule']
        desired_retention = self.module.params['desired_retention']
        retention_unit = self.module.params['retention_unit']
        alias = self.module.params['alias']

        # result is a dictionary that contains changed status and snapshot
        # schedule details
        result = dict(
            changed=False,
            snapshot_schedule_details=''
        )
        effective_path = None
        if path:
            if access_zone.lower() == 'system':
                effective_path = path.rstrip("/")
            else:
                effective_path = self.get_zone_base_path(access_zone) + \
                    path.rstrip("/")
        if desired_retention:
            self.validate_desired_retention(desired_retention)

        snapshot_schedule_details = self.get_details(name)

        is_schedule_modified = False
        snapshot_schedule_modification_details = dict()

        if snapshot_schedule_details is not None:
            is_schedule_modified, snapshot_schedule_modification_details = \
                self.check_snapshot_schedule_modified(
                    snapshot_schedule_details, alias, desired_retention,
                    retention_unit, effective_path, pattern, schedule)

        if state == 'present' and not snapshot_schedule_details:
            LOG.debug("Creating new snapshot schedule: %s for path: %s",
                      name, effective_path)
            result['changed'] = self.create_snapshot_schedule(
                name, alias, effective_path, desired_retention,
                retention_unit, pattern, schedule) or result['changed']

        if state == 'present' and new_name is not None:
            if len(new_name) == 0:
                self.module.fail_json(msg="Please provide valid string for "
                                          "new_name")

            if snapshot_schedule_details is None:
                self.module.fail_json(msg="Snapshot schedule not found.")

            if snapshot_schedule_details is not None and \
                    len(snapshot_schedule_details['schedules']) != 0:
                if new_name != snapshot_schedule_details['schedules'][0]['name']:
                    self.validate_new_name(new_name)
                    LOG.info("Renaming snapshot schedule %s to new name %s",
                             name, new_name)
                    result['changed'] = self.rename_snapshot_schedule(
                        snapshot_schedule_details, new_name) or result['changed']
                    name = new_name

        if state == 'present' and is_schedule_modified:
            LOG.info("Modifying snapshot schedule %s", name)
            result['changed'] = self.modify_snapshot_schedule(
                name, snapshot_schedule_modification_details) or \
                result['changed']

        if state == 'absent' and snapshot_schedule_details:
            LOG.info("Deleting snapshot schedule %s", name)
            result['changed'] = self.delete_snapshot_schedule(name) or \
                result['changed']

        snapshot_schedule_details = self.get_details(name)
        result['snapshot_schedule_details'] = snapshot_schedule_details
        self.module.exit_json(**result)


def get_snapshotschedule_parameters():
    """This method provide parameters required for the ansible snapshot
    schedule module on PowerScale"""
    return dict(
        name=dict(required=True, type='str'),
        access_zone=dict(type='str', default='System'),
        path=dict(type='str', no_log=True),
        new_name=dict(type='str'),
        pattern=dict(type='str'),
        schedule=dict(type='str'),
        desired_retention=dict(type='int'),
        retention_unit=dict(type='str', choices=['hours', 'days'],
                            default='hours'),
        alias=dict(required=False, type='str'),
        state=dict(required=True, type='str', choices=['present', 'absent'])
    )


def main():
    """ Create PowerScale snapshot schedule object and perform action on it
        based on user input from playbook"""
    obj = SnapshotSchedule()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
