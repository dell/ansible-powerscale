#!/usr/bin/python
# Copyright: (c) 2019, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

""" Ansible module for managing snapshots on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: snapshot
version_added: '1.2.0'
short_description: Manage snapshots on PowerScale
description:
- You can perform the following operations.
- Managing snapshots on PowerScale.
- Create a filesystem snapshot.
- Modify a filesystem snapshot.
- Get details of a filesystem snapshot.
- Delete a filesystem snapshot.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Prashant Rakheja (@prashant-dell) <ansible.team@dell.com>

options:
  snapshot_name:
    description:
    - The name of the snapshot.
    required: true
    type: str
  path:
    description:
    - Specifies the filesystem path. It is the absolute path for System access zone
      and it is relative if using non-System access zone. For example, if your access
      zone is 'Ansible' and it has a base path '/ifs/ansible' and the path
      specified is '/user1', then the effective path would be
      '/ifs/ansible/user1'.
      If your access zone is System, and you have 'directory1' in the access
      zone, the path provided should be '/ifs/directory1'.
    type: str
  access_zone:
    description:
    - The effective path where the Snapshot is created will
      be determined by the base path of the Access Zone and the
      path provided by the user in the playbook.
    type: str
    default: 'System'
  new_snapshot_name:
    description:
    - The new name of the snapshot.
    type: str
  expiration_timestamp:
    description:
    - The timestamp on which the snapshot will expire (UTC format).
    - Either this or desired retention can be specified, but not both.
    type: str
  desired_retention:
    description:
    - The number of days for which the snapshot can be retained.
    - Either this or expiration timestamp can be specified, but not both.
    type: str
  retention_unit:
    description:
    - The retention unit for the snapshot.
    - The default value is hours.
    choices: [hours, days]
    type: str
  alias:
    description:
    - The alias for the snapshot.
    type: str
  state:
    description:
    - Defines whether the snapshot should exist or not.
    required: true
    choices: [absent, present]
    type: str
notes:
- The I(check_mode) is not supported.
'''

EXAMPLES = r'''
- name: Create a filesystem snapshot on PowerScale
  dellemc.powerscale.snapshot:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    path: "<path>"
    access_zone: "{{access_zone}}"
    snapshot_name: "{{snapshot_name}}"
    desired_retention: "{{desired_retention}}"
    retention_unit: "{{retention_unit_days}}"
    alias: "{{ansible_snap_alias}}"
    state: "{{present}}"

- name: Get details of a filesystem snapshot
  dellemc.powerscale.snapshot:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    snapshot_name: "{{snapshot_name}}"
    state: "{{present}}"

- name: Modify filesystem snapshot desired retention
  dellemc.powerscale.snapshot:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    snapshot_name: "{{snapshot_name}}"
    desired_retention: "{{desired_retention_new}}"
    retention_unit: "{{retention_unit_days}}"
    state: "{{present}}"

- name: Modify filesystem snapshot expiration timestamp
  dellemc.powerscale.snapshot:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    snapshot_name: "{{snapshot_name}}"
    expiration_timestamp: "{{expiration_timestamp_new}}"
    state: "{{present}}"

- name: Modify filesystem snapshot alias
  dellemc.powerscale.snapshot:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    snapshot_name: "{{snapshot_name}}"
    alias: "{{ansible_snap_alias_new}}"
    state: "{{present}}"

- name: Delete snapshot alias
  dellemc.powerscale.snapshot:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    snapshot_name: "{{snapshot_name}}"
    alias: ""
    state: "{{present}}"

- name: Rename filesystem snapshot
  dellemc.powerscale.snapshot:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    snapshot_name: "{{snapshot_name}}"
    new_snapshot_name: "{{new_snapshot_name}}"
    state: "{{present}}"

- name: Delete filesystem snapshot
  dellemc.powerscale.snapshot:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    snapshot_name: "{{new_snapshot_name}}"
    state: "{{absent}}"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
    sample: true

snapshot_details:
    description: The snapshot details.
    type: complex
    returned: When snapshot exists.
    contains:
        alias:
            description: Snapshot alias.
            type: str
            sample: "snapshot_alias"
        created:
            description: The creation timestamp.
            type: int
            sample: 1578514373
        expires:
            description: The expiration timestamp.
            type: int
            sample: 1578687172
        has_locks:
            description: Whether the snapshot has locks.
            type: bool
            sample: false
        id:
            description: The snapshot ID.
            type: int
            sample: 230
        name:
            description: The name of the snapshot.
            type: str
            sample: ansible_snapshot
        path:
            description: The directory path whose snapshot has been taken.
            type: str
            sample: /ifs/ansible/
        pct_filesystem:
            description: The percentage of filesystem used.
            type: float
            sample: 2.5
        pct_reserve:
            description: The percentage of filesystem reserved.
            type: float
            sample: 0.0
        size:
            description: The snapshot size.
            type: int
            sample: 4096
        state:
            description: The state of the snapshot.
            type: str
            sample: active
        target_id:
            description: target ID of snapshot whose alias it is.
            type: int
            sample: 10
        target_name:
            description: target name of snapshot whose alias it is.
            type: str
            sample: "ansible_target_snap"
    sample: {
        "snapshots": [
            {
                "alias": null,
                "created": 1628155527,
                "expires": null,
                "has_locks": false,
                "id": 936,
                "name": "Atest",
                "path": "/ifs/test_src_01",
                "pct_filesystem": 2.435778242215747e-06,
                "pct_reserve": 0.0,
                "schedule": null,
                "shadow_bytes": 0,
                "size": 4096,
                "state": "active",
                "target_id": null,
                "target_name": null
            }
        ]
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
from datetime import datetime, timedelta
import calendar
import time
import re

LOG = utils.get_logger('snapshot')


class Snapshot(object):
    """Class with Snapshot operations"""

    def __init__(self):
        """Define all the parameters required by this module"""

        self.module_params = utils \
            .get_powerscale_management_host_parameters()
        self.module_params.update(get_snapshot_parameters())

        mutually_exclusive = [
            ['desired_retention', 'expiration_timestamp'],
            ['expiration_timestamp', 'retention_unit']
        ]

        # initialize the Ansible module
        self.module = AnsibleModule(argument_spec=self.module_params,
                                    supports_check_mode=False,
                                    mutually_exclusive=mutually_exclusive
                                    )

        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        LOG.info('Got python SDK instance for provisioning on PowerScale ')
        self.snapshot_api = self.isi_sdk.SnapshotApi(self.api_client)
        self.zone_summary_api = self.isi_sdk.ZonesSummaryApi(self.api_client)

    def determine_path(self):
        path = None
        if self.module.params['path']:
            path = self.module.params['path'].rstrip("/")
        access_zone = self.module.params['access_zone']

        if access_zone.lower() != 'system':
            if path:
                path = self.get_zone_base_path(access_zone) + path

        return path

    def validate_desired_retention(self, desired_retention):
        """Validates the specified desired retention"""
        try:
            int(desired_retention)
        except ValueError:
            if desired_retention and desired_retention.lower() == 'none':
                LOG.info("Desired retention is set to 'None'")
            else:
                self.module.fail_json(msg="Please provide a valid integer"
                                      " as the desired retention.")

    def validate_expiration_timestamp(self, expiration_timestamp):
        """Validates whether the expiration timestamp is valid"""
        try:
            datetime.strptime(expiration_timestamp,
                              '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            self.module.fail_json(msg='Incorrect date format, '
                                      'should be YYYY-MM-DDTHH:MM:SSZ')

    def get_filesystem_snapshot_details(self, snapshot_name):
        """Returns details of a filesystem Snapshot"""
        try:
            return self.snapshot_api.get_snapshot_snapshot(snapshot_name)
        except utils.ApiException as e:
            if str(e.status) == "404":
                log_msg = "Snapshot {0} status is " \
                          "{1}".format(snapshot_name, e.status)
                LOG.info(log_msg)
                return None
            else:
                error_msg = self.determine_error(error_obj=e)
                error_message = "Failed to get details of Snapshot " \
                                "{0} with error {1} ".format(
                                    snapshot_name,
                                    str(error_msg))
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

        except Exception as e:
            error_message = "Failed to get details of Snapshot {0} with" \
                            " error {1} ".format(snapshot_name, str(e))
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

    def create_filesystem_snapshot(self, snapshot_name,
                                   alias,
                                   path,
                                   desired_retention,
                                   retention_unit,
                                   epoch_expiry_time,
                                   new_name):
        """Create a snapshot for a filesystem on PowerScale"""

        if desired_retention is None and epoch_expiry_time is None:
            self.module.fail_json(msg="The given snapshot {0} does not exist."
                                      "Please provide either "
                                      "desired_retention or expiration_"
                                      "timestamp for creating a "
                                      "snapshot".format(snapshot_name))

        if new_name:
            self.module.fail_json(msg="The given snapshot {0} does not exist."
                                      "Invalid param: new_name while "
                                      "creating a new snapshot.".format(
                                          snapshot_name))

        if not self.module.params['path']:
            self.module.fail_json(msg="Please provide a valid path for "
                                      "snapshot creation")

        if desired_retention and desired_retention.lower() != 'none':
            if retention_unit is None:
                expiration_timestamp = (datetime.utcnow() +
                                        timedelta(
                                            hours=int(desired_retention))
                                        )
                epoch_expiry_time = calendar.timegm(
                    time.strptime(str(expiration_timestamp),
                                  '%Y-%m-%d %H:%M:%S.%f'))

            elif retention_unit == 'days':
                expiration_timestamp = (datetime.utcnow() + timedelta(
                    days=int(desired_retention)))
                epoch_expiry_time = calendar.timegm(
                    time.strptime(str(expiration_timestamp),
                                  '%Y-%m-%d %H:%M:%S.%f'))
            elif retention_unit == 'hours':
                expiration_timestamp = (datetime.utcnow() + timedelta(
                    hours=int(desired_retention)))
                epoch_expiry_time = calendar.timegm(
                    time.strptime(str(expiration_timestamp),
                                  '%Y-%m-%d %H:%M:%S.%f'))

        elif desired_retention and \
                desired_retention.lower() == 'none':
            epoch_expiry_time = None

        try:
            snapshot_create_param = self.isi_sdk.SnapshotSnapshotCreateParams(
                alias=alias,
                expires=epoch_expiry_time,
                name=snapshot_name,
                path=path)
            self.snapshot_api.create_snapshot_snapshot(snapshot_create_param)
            return True
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Failed to create snapshot: {0} for ' \
                            'filesystem {1} with error: ' \
                            '{2}'.format(snapshot_name, path, str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete_filesystem_snapshot(self, snapshot_name):
        """Deletes a filesystem snapshot"""
        try:
            self.snapshot_api.delete_snapshot_snapshot(snapshot_name)
            return True
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Failed to delete ' \
                            'snapshot: {0} with ' \
                            'error: {1}'.format(snapshot_name, str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def rename_filesystem_snapshot(self, snapshot, new_name):
        """Renames a filesystem snapshot"""
        if snapshot is None:
            self.module.fail_json(msg="Snapshot not found.")

        snapshot = snapshot.to_dict()

        if snapshot['snapshots'][0]['name'] == new_name:
            return False
        try:
            snapshot_update_param = self.isi_sdk.SnapshotSnapshot(
                name=new_name)
            self.snapshot_api.update_snapshot_snapshot(
                snapshot_update_param,
                snapshot['snapshots'][0]['name'])
            return True
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Failed to rename snapshot: {0} ' \
                            'with error: ' \
                            '{1}'.format(snapshot['snapshots'][0]['name'],
                                         str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def check_snapshot_modified(self, snapshot, alias,
                                desired_retention,
                                retention_unit,
                                expiration_timestamp,
                                snapshot_name,
                                effective_path):
        """Determines whether the snapshot has been modified"""
        LOG.info("Determining if the snap has been modified...")
        snapshot_modification_details = dict()
        snapshot_modification_details['is_alias_modified'] = False
        snapshot_modification_details['new_alias_value'] = None
        snapshot_modification_details['is_timestamp_modified'] = False
        snapshot_modification_details['new_expiration_timestamp_value'] = None

        snap_details = snapshot.to_dict()

        if effective_path is not None:
            if self.module.params['path'] and \
                    snap_details['snapshots'][0]['path'] != effective_path:
                error_message = 'The path {0} specified in the playbook does '\
                                'not match the path of the snapshot {1} '\
                                'on the array'.format(effective_path,
                                                      snapshot_name)
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

        if desired_retention is None and expiration_timestamp is None \
                and alias is None:
            LOG.info("desired_retention and expiration_time and alias are "
                     "not provided, we do not check for snapshot modification "
                     "in this case. The snapshot details would be returned, "
                     "if available.")
            return False, snapshot_modification_details
        info_message = "The snap details are: {0}".format(snap_details)
        LOG.info(info_message)
        snap_creation_timestamp = None
        if 'created' in snap_details['snapshots'][0]:
            snap_creation_timestamp = \
                snap_details['snapshots'][0]['created']

        # Here we are calculating the desired retention.
        # If the retention unit is not specified, default is hours.
        # Expiration timestamp is calculated by adding the
        # creation timestamp of the snapshot to the desired retention
        # specified in the Playbook.
        if desired_retention and desired_retention.lower() != 'none':
            if retention_unit is None:
                expiration_timestamp = \
                    datetime.fromtimestamp(snap_creation_timestamp) + \
                    timedelta(hours=int(desired_retention))
                expiration_timestamp = \
                    time.mktime(expiration_timestamp.timetuple())

            elif retention_unit == 'days':
                expiration_timestamp = \
                    datetime.fromtimestamp(snap_creation_timestamp) + \
                    timedelta(days=int(desired_retention))
                expiration_timestamp = \
                    time.mktime(expiration_timestamp.timetuple())
            elif retention_unit == 'hours':
                expiration_timestamp = \
                    datetime.fromtimestamp(snap_creation_timestamp) + \
                    timedelta(hours=int(desired_retention))
                expiration_timestamp = \
                    time.mktime(expiration_timestamp.timetuple())
        elif desired_retention and desired_retention.lower() == 'none':
            expiration_timestamp = None
        info_message = "The new expiration " \
                       "timestamp is {0}".format(expiration_timestamp)
        LOG.info(info_message)

        modified = False
        if 'expires' in snap_details['snapshots'][0] and \
                snap_details['snapshots'][0]['expires'] is not None \
                and expiration_timestamp is not None:
            if snap_details['snapshots'][0]['expires'] \
                    != expiration_timestamp:
                # We can tolerate a delta of two minutes.
                existing_timestamp = \
                    snap_details['snapshots'][0]['expires']
                new_timestamp = expiration_timestamp
                info_message = 'The existing timestamp is: ' \
                               '{0} and the new timestamp ' \
                               'is: {1}'.format(existing_timestamp,
                                                new_timestamp)
                LOG.info(info_message)

                existing_time_obj = datetime.fromtimestamp(
                    existing_timestamp)
                new_time_obj = datetime.fromtimestamp(
                    new_timestamp)

                if existing_time_obj > new_time_obj:
                    td = utils.dateutil.relativedelta.relativedelta(
                        existing_time_obj, new_time_obj)
                else:
                    td = utils.dateutil.relativedelta.relativedelta(
                        new_time_obj, existing_time_obj)
                info_message = 'The time difference is ' \
                               '{0} minutes'.format(td.minutes)
                LOG.info(info_message)
                # A delta of two minutes is treated as idempotent
                if td.seconds > 120 or td.minutes > 2 or \
                        td.hours > 0 or td.days > 0 or td.years > 0:
                    snapshot_modification_details[
                        'is_timestamp_modified'] = True
                    snapshot_modification_details[
                        'new_expiration_timestamp_value'] = \
                        expiration_timestamp
                    modified = True
        # This is the case when expiration timestamp may not be present
        # in the snapshot details.
        # Expiration timestamp specified in the playbook is not None.
        elif 'expires' not in snap_details['snapshots'][0] \
                and expiration_timestamp is not None:
            snapshot_modification_details['is_timestamp_modified'] = True
            snapshot_modification_details[
                'new_expiration_timestamp_value'] = expiration_timestamp
            modified = True
        elif 'expires' in snap_details['snapshots'][0] \
                and desired_retention and desired_retention.lower() == 'none' \
                and expiration_timestamp is None:
            # Ensure only when desired retention is explicitly set to 'None'
            # we try to modify.
            if snap_details['snapshots'][
                    0]['expires'] is not None:
                snapshot_modification_details['is_timestamp_modified'] = True
                snapshot_modification_details[
                    'new_expiration_timestamp_value'] = expiration_timestamp
                modified = True
        elif 'expires' in snap_details['snapshots'][0] and \
                snap_details['snapshots'][0]['expires'] is \
                None and expiration_timestamp is not None:
            snapshot_modification_details['is_timestamp_modified'] = True
            snapshot_modification_details[
                'new_expiration_timestamp_value'] = expiration_timestamp
            modified = True

        snapshot_alias = self.get_snapshot_alias(snapshot_name)

        if snapshot_alias != alias:
            snapshot_modification_details['is_alias_modified'] = True
            snapshot_modification_details['new_alias_value'] = alias
            modified = True
        info_message = "Snapshot " \
                       "modified {0}, " \
                       "modification " \
                       "details: {1}".format(
                           modified,
                           snapshot_modification_details)
        LOG.info(info_message)

        return modified, snapshot_modification_details

    def modify_filesystem_snapshot(self, snapshot_name,
                                   snapshot_modification_details):
        """Modify a filesystem snapshot"""
        try:
            changed = False
            if snapshot_modification_details['is_timestamp_modified']:
                new_timestamp = \
                    snapshot_modification_details[
                        'new_expiration_timestamp_value']
                snapshot_update_param = self.isi_sdk.SnapshotSnapshot(
                    expires=int(new_timestamp))
                self.snapshot_api.update_snapshot_snapshot(
                    snapshot_update_param, snapshot_name)
                changed = True
            if snapshot_modification_details['is_alias_modified']:
                new_alias = \
                    snapshot_modification_details['new_alias_value']
                snapshot_update_param = self.isi_sdk.SnapshotSnapshot(
                    alias=new_alias)
                self.snapshot_api.update_snapshot_snapshot(
                    snapshot_update_param, snapshot_name)
                changed = True
            return changed
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Failed to modify snapshot ' \
                            '{0} with error {1}'.format(snapshot_name,
                                                        str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_snapshot_alias(self, snapshot_name):
        """Returns the alias for a given snapshot"""
        try:
            alias_name = None
            # We get a list of all aliases
            # If any alias has a target which matches the snapshot name
            # It indicates it is the alias of that snapshot
            snap_list = \
                self.snapshot_api.list_snapshot_snapshots(
                    type='alias').to_dict()
            for snap in snap_list['snapshots']:
                if snap['target_name'] == snapshot_name:
                    alias_name = snap['name']
                    break
            return alias_name
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Failed to get alias for ' \
                            'snapshot {0} with error {1}'.format(
                                snapshot_name,
                                str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def determine_error(self, error_obj):
        """Determine the error message to return"""
        if isinstance(error_obj, utils.ApiException):
            error = re.sub("[\n \"]+", ' ', str(error_obj.body))
        else:
            error = str(error_obj)
        return error

    def convert_utc_to_epoch(self, expiration_timestamp):
        """Convert UTC to Epoch time"""
        timestamp = datetime.strptime(expiration_timestamp,
                                      '%Y-%m-%dT%H:%M:%SZ')
        epoch = calendar.timegm(timestamp.utctimetuple())
        return epoch

    def perform_module_operation(self):
        """
        Perform different actions on Snapshot based on user
        parameter chosen in playbook
        """

        snapshot_name = self.module.params['snapshot_name']
        new_snapshot_name = self.module.params['new_snapshot_name']
        expiration_timestamp = self.module.params['expiration_timestamp']
        desired_retention = self.module.params['desired_retention']
        retention_unit = self.module.params['retention_unit']
        alias = self.module.params['alias']
        state = self.module.params['state']

        result = dict(
            changed=False
        )

        if not snapshot_name:
            error_message = 'Please provide a valid snapshot name'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

        effective_path = self.determine_path()

        if desired_retention is not None:
            self.validate_desired_retention(desired_retention)

        if desired_retention is None and retention_unit is not None:
            error_message = 'Specify desired retention along with ' \
                            'retention unit.'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

        if expiration_timestamp is not None:
            self.validate_expiration_timestamp(expiration_timestamp)
            expiration_timestamp = self.convert_utc_to_epoch(
                expiration_timestamp)

        snapshot = self.get_filesystem_snapshot_details(snapshot_name)

        is_snap_modified = False
        snapshot_modification_details = dict()
        if snapshot is not None:
            is_snap_modified, snapshot_modification_details = \
                self.check_snapshot_modified(snapshot,
                                             alias,
                                             desired_retention,
                                             retention_unit,
                                             expiration_timestamp,
                                             snapshot_name,
                                             effective_path)

        if state == 'present' and not snapshot:
            info_message = "Creating new snapshot: " \
                           "{0} for filesystem: {1}".format(snapshot_name,
                                                            effective_path)
            LOG.debug(info_message)
            result['changed'] = \
                self.create_filesystem_snapshot(snapshot_name,
                                                alias,
                                                effective_path,
                                                desired_retention,
                                                retention_unit,
                                                expiration_timestamp,
                                                new_snapshot_name
                                                ) or result['changed']

        if state == 'present' and new_snapshot_name:
            info_message = "Renaming snapshot {0} to new name {1}".format(
                snapshot_name, new_snapshot_name)
            LOG.info(info_message)
            result['changed'] = self.rename_filesystem_snapshot(
                snapshot, new_snapshot_name) or result['changed']
            snapshot_name = new_snapshot_name

        if state == 'absent' and snapshot:
            info_message = "Deleting snapshot {0}".format(
                snapshot_name)
            LOG.info(info_message)
            result['changed'] = \
                self.delete_filesystem_snapshot(snapshot_name) \
                or result['changed']
            result['snapshot_details'] = {}

        if state == 'present' and is_snap_modified:
            info_message = "Modifying snapshot {0}".format(snapshot_name)
            LOG.info(info_message)
            result['changed'] = \
                self.modify_filesystem_snapshot(
                    snapshot_name,
                    snapshot_modification_details) \
                or result['changed']

        if state == 'present':
            info_message = 'Getting snapshot: ' \
                           '{0} details'.format(snapshot_name)
            LOG.info(info_message)
            result['snapshot_details'] = \
                self.get_filesystem_snapshot_details(snapshot_name).to_dict()

        # Finally update the module result!
        self.module.exit_json(**result)


def get_snapshot_parameters():
    return dict(
        snapshot_name=dict(required=True, type='str'),
        path=dict(type='str', no_log=True),
        access_zone=dict(type='str', default='System'),
        new_snapshot_name=dict(type='str'),
        expiration_timestamp=dict(type='str'),
        desired_retention=dict(type='str'),
        retention_unit=dict(type='str',
                            choices=['hours', 'days']),
        alias=dict(type='str'),
        state=dict(required=True, type='str',
                   choices=['present', 'absent'])
    )


def main():
    """Create PowerScale Snapshot object and perform action on it
        based on user input from playbook"""
    obj = Snapshot()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
