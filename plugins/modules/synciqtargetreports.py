#!/usr/bin/python
# Copyright: (c) 2021, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

""" Ansible module for managing SyncIQ target reports on PowerScale"""
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: synciqtargetreports
short_description: Provides the SyncIQ target reports for PowerScale Storage System
description:
- This module provides the SyncIQ target reports for PowerScale Storage System.
version_added: "1.3.0"
extends_documentation_fragment:
  - dellemc.powerscale.powerscale
author:
- Meenakshi Dembi (@dembim) <ansible.team@dell.com>
options:
  name:
    description:
    - The name of the SyncIQ target report.
    type: str
  id:
    description:
    - The id of the SyncIQ target report.
    type: str
  sub_report_id:
    description:
    - The id of the SyncIQ target sub report.
    type: str
  include_sub_reports:
    description:
    - This flag is used to fetch the list of target sub reports.
    type: bool
    default: false
  state:
    description:
    - The state option is used to mention the existence of target reports.
    type: str
    required: true
    choices: [absent, present]
notes:
- The I(check_mode) is not supported.
'''

EXAMPLES = r'''
  - name: Get a single SyncIQ target report with id
    dellemc.powerscale.synciqtargetreports:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      id: "2-sample_policy"
      state: "present"

  - name: Get a single SyncIQ target report with name
    dellemc.powerscale.synciqtargetreports:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      name: "sample_policy"
      state: "present"

  - name: Get all SyncIQ target sub-reports with report id
    dellemc.powerscale.synciqtargetreports:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      id: "2-sample_policy"
      include_sub_reports: true
      state: "present"

  - name: Get all SyncIQ target sub-reports with report name
    dellemc.powerscale.synciqtargetreports:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      name: "sample_policy"
      include_sub_reports: true
      state: "present"

  - name: Get a single SyncIQ target sub-report with sub-report id
    dellemc.powerscale.synciqtargetreports:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      id: "2-sample_policy"
      sub_report_id: "1"
      state: "present"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
synciq_target_report:
    description: Details of the SyncIQ target report.
    returned: When SyncIQ target report exists
    type: complex
    contains:
        action:
            description: The action to be taken by this job.
            type: str
        ads_streams_replicated:
            description: The number of ads streams replicated by this job.
            type: int
        block_specs_replicated:
            description: The number of block specs replicated by this job.
            type: int
        bytes_recoverable:
            description: The number of bytes recoverable by this job.
            type: int
        bytes_transferred:
            description: The number of bytes that have been transferred by this job.
            type: int
        char_specs_replicated:
            description: The number of char specs replicated by this job.
            type: int
        committed_files:
            description: The number of WORM committed files.
            type: int
        corrected_lins:
            description: The number of LINs corrected by this job.
            type: int
        dead_node:
            description: This field is true if the node running this job is dead.
            type: bool
        directories_replicated:
            description: The number of directories replicated.
            type: int
        dirs_changed:
            description: The number of directories changed by this job.
            type: int
        dirs_deleted:
            description: The number of directories deleted by this job.
            type: int
        dirs_moved:
            description: The number of directories moved by this job.
            type: int
        dirs_new:
            description: The number of directories created by this job.
            type: int
        duration:
            description: The amount of time in seconds between when the job was started and when it ended.
                         If the job has not yet ended, this is the amount of time since the job started.
                         This field is null if the job has not yet started.
            type: int
        encrypted:
            description: If true, syncs will be encrypted.
            type: bool
        end_time:
            description: The time the job ended in unix epoch seconds.
                         The field is null if the job hasn't ended.
            type: int
        error:
            description: The primary error message for this job.
            type: str
        error_checksum_files_skipped:
            description: The number of files with checksum errors skipped by this job.
            type: int
        error_io_files_skipped:
            description: The number of files with io errors skipped by this job.
            type: int
        error_net_files_skipped:
            description: The number of files with network errors skipped by this job.
            type: int
        errors:
            description: A list of error messages for this job.
            type: list
            elements: str
        failed_chunks:
            description: The number of data chunks that failed transmission.
            type: int
        fifos_replicated:
            description: The number of fifos replicated by this job.
            type: int
        file_data_bytes:
            description: The number of bytes transferred that belong to files.
            type: int
        files_changed:
            description: The number of files changed by this job.
            type: int
        files_linked:
            description: The number of files linked by this job.
            type: int
        files_new:
            description: The number of files created by this job.
            type: int
        files_selected:
            description: The number of files selected by this job.
            type: int
        files_transferred:
            description: The number of files transferred by this job.
            type: int
        files_unlinked:
            description: The number of files unlinked by this job.
            type: int
        files_with_ads_replicated:
            description: The number of files with ads replicated by this job.
            type: int
        flipped_lins:
            description: The number of LINs flipped by this job.
            type: int
        hard_links_replicated:
            description: The number of hard links replicated by this job.
            type: int
        hash_exceptions_fixed:
            description: The number of hash exceptions fixed by this job.
            type: int
        hash_exceptions_found:
            description: The number of hash exceptions found by this job.
            type: int
        id:
            description: A unique identifier for this object.
            type: str
        job_id:
            description: The ID of the job.
            type: int
        lins_total:
            description: The number of LINs transferred by this job.
            type: int
        network_bytes_to_source:
            description: The total number of bytes sent to the source by this job.
            type: int
        network_bytes_to_target:
            description: The total number of bytes sent to the target by this job.
            type: int
        new_files_replicated:
            description: The number of new files replicated by this job.
            type: int
        num_retransmitted_files:
            description: The number of files that have been retransmitted by this job.
            type: int
        phases:
            description: Data for each phase of this job.
            type: complex
            contains:
                phase:
                    description: The phase that the job was in.
                    type: str
                end_time:
                    description: The time the job ended this phase.
                    type: int
                start_time:
                    description: The time the job began this phase.
                    type: int
        policy:
            description: Policy details
            type: complex
            contains:
                name:
                    description: User-assigned name of this sync policy.
                    type: str
                source_root_path:
                    description: The root directory on the source cluster the files will be synced from.
                    type: str
                target_host:
                    description: Hostname or IP address of sync target cluster.
                    type: str
        policy_action:
            description: This is the action the policy is configured to perform.
            type: str
        policy_id:
            description: The ID of the policy.
            type: str
        policy_name:
            description: The name of the policy.
            type: str
        quotas_deleted:
            description: The number of quotas removed from the target.
            type: int
        regular_files_replicated:
            description: The number of regular files replicated by this job.
            type: int
        resynced_lins:
            description: The number of LINs resynched by this job.
            type: int
        retransmitted_files:
            description: The files that have been retransmitted by this job.
            type: list
            elements: str
        retry:
            description: The number of times the job has been retried.
            type: int
        running_chunks:
            description: The number of data chunks currently being transmitted.
            type: int
        service_report:
            description: Data for each component exported as part of service replication.
            type: complex
            contains:
                status:
                    description: The current status of export for this component.
                    type: str
                start_time:
                    description: The time the job began this component.
                    type: int
                end_time:
                    description: The time the job end this component.
                    type: int
        sockets_replicated:
            description: The number of sockets replicated by this job.
            type: int
        source_bytes_recovered:
            description: The number of bytes recovered on the source.
            type: int
        source_directories_created:
            description: The number of directories created on the source.
            type: int
        source_directories_deleted:
            description: The number of directories deleted on the source.
            type: int
        source_directories_linked:
            description: The number of directories linked on the source.
            type: int
        source_directories_unlinked:
            description: The number of directories unlinked on the source.
            type: int
        source_directories_visited:
            description: The number of directories visited on the source.
            type: int
        source_files_deleted:
            description: The number of files deleted on the source.
            type: int
        source_files_linked:
            description: The number of files linked on the source.
            type: int
        source_files_unlinked:
            description: The number of sparse data bytes transferred by this job.
            type: int
        start_time:
            description: The time the job started in unix epoch seconds. The field is null if the job hasn't started.
            type: int
        state:
            description: The state of the job.
            type: str
        subreport_count:
            description: The number of subreports that are available for this job report.
            type: int
        succeeded_chunks:
            description: The number of data chunks that have been transmitted successfully.
            type: int
        symlinks_replicated:
            description: The number of symlinks replicated by this job.
            type: int
        sync_type:
            description: The type of sync being performed by this job.
            type: str
        target_bytes_recovered:
            description: The number of bytes recovered on the target.
            type: int
        target_directories_created:
            description: The number of directories created on the target.
            type: int
        target_directories_deleted:
            description: The number of directories deleted on the target.
            type: int
        target_directories_linked:
            description: The number of directories linked on the target.
            type: int
        target_directories_unlinked:
            description: The number of directories unlinked on the target.
            type: int
        target_files_deleted:
            description: The number of files deleted on the target.
            type: int
        target_files_linked:
            description: The number of files linked on the target.
            type: int
        target_files_unlinked:
            description: The number of files unlinked on the target.
            type: int
        target_snapshots:
            description: The target snapshots created by this job.
            type: list
            elements: str
        total_chunks:
            description: The total number of data chunks transmitted by this job.
            type: int
        total_data_bytes:
            description: The total number of bytes transferred by this job.
            type: int
        total_exported_services:
            description: The total number of components exported as part of service replication.
            type: int
        total_files:
            description: The number of files affected by this job.
            type: int
        total_network_bytes:
            description: The total number of bytes sent over the network by this job.
            type: int
        total_phases:
            description: The total number of phases for this job.
            type: int
        unchanged_data_bytes:
            description: The number of bytes unchanged by this job.
            type: int
        up_to_date_files_skipped:
            description: The number of up-to-date files skipped by this job.
            type: int
        updated_files_replicated:
            description: The number of updated files replicated by this job.
            type: int
        user_conflict_files_skipped:
            description: The number of files with user conflicts skipped by this job.
            type: int
        warnings:
            description: A list of warning messages for this job.
            type: list
            elements: str
        worm_committed_file_conflicts:
            description: The number of WORM committed files which needed to be reverted.
                         Since WORM committed files cannot be reverted,
                         this is the number of files that were preserved in the compliance store.
            type: int
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils


LOG = utils.get_logger('synciqtargetreports')


class SyncIQTargetReports(object):
    """Class with SyncIQ Target Reports"""

    def __init__(self):
        """ Define all parameters required by this module"""

        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_synciq_target_reports_parameters())

        mutually_exclusive = [['id', 'name']]

        required_one_of = [
            ['id', 'name']
        ]

        # initialize the ansible module
        self.module = AnsibleModule(argument_spec=self.module_params,
                                    mutually_exclusive=mutually_exclusive,
                                    required_one_of=required_one_of)

        # result is a dictionary that contains changed status and
        # SyncIQ report details
        self.result = {"changed": False}
        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        LOG.info('Got python SDK instance for provisioning on PowerScale ')
        self.synciq_api = self.isi_sdk.SyncApi(self.api_client)
        self.synciq_target_reports_api = self.isi_sdk.SyncTargetApi(self.api_client)

    def get_synciq_target_report(self, id):
        """
        Get SyncIQ target report.
        :param id: Specifies id of SyncIQ target report.
        :return: if exists returns details of the SyncIQ target report
        else returns None.
        """
        try:
            if id:
                target_report_details = self.synciq_api.get_target_report(id)
                return target_report_details.to_dict()
        except Exception as e:
            error_message = ("Get details of SyncIQ target report with id %s failed with "
                             "error: %s" % (id, str(e)))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_synciq_target_sub_reports(self, id):
        """
        Get all syncIQ target sub reports.
        :param id: Specifies id of SyncIQ target report.
        :return: if exists returns details of the all SyncIQ target sub-reports
        else returns None.
        """
        try:
            if id:
                synciq_target_sub_report_details = self.synciq_target_reports_api.get_reports_report_subreports(id)
                return synciq_target_sub_report_details.to_dict()
        except Exception as e:
            error_message = ("Get details of SyncIQ target sub reports failed for report id %s with "
                             "error: %s" % (id, str(e)))
            self.module.fail_json(msg=error_message)

    def get_synciq_taget_sub_report(self, synciq_sub_report_id, id):
        """
        Get a single SyncIQ target sub report.
        :param synciq_sub_report_id: Specifies id of SyncIQ target sub report.
        :param id: specifies id of SyncIQ target report.
        :return: if exists returns details of the SyncIQ target sub report
        else returns None.
        """
        try:
            if synciq_sub_report_id and id:
                sub_report_detail = self.synciq_target_reports_api.get_reports_report_subreport(synciq_sub_report_id, id)
                return sub_report_detail.to_dict()
        except Exception as e:
            error_message = ("Get details of SyncIQ target report with report id %s and sub report id %s failed with "
                             "error: %s" % (id, synciq_sub_report_id, str(e)))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_target_report_id(self, name):
        """
        Get report id for SyncIQ target report when report name is mentioned.
        :param name: Specifies name of SyncIQ target report.
        :return: if exists returns id of the SyncIQ target report
        else returns None.
        """
        try:
            id_report = None
            all_reports = (self.synciq_api.get_target_reports()).to_dict()
            for items in range(len(all_reports['reports'])):
                if all_reports['reports'][items]['policy_name'] == name:
                    id_report = all_reports['reports'][items]['id']
                    break
            if id_report:
                return id_report
            else:
                error_message = ("Failed to get the id of the target report for specified name %s "
                                 % (name))
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
        except Exception as e:
            error_message = ("Getting SyncIQ target reports failed with "
                             "error: %s" % (str(e)))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def perform_module_operation(self):
        """
        Perform different actions on syncIQ report module based on parameters
        chosen in playbook
        """
        id = self.module.params['id']
        state = self.module.params['state']
        name = self.module.params['name']
        sub_report_id = self.module.params['sub_report_id']
        include_sub_reports = self.module.params['include_sub_reports']
        synciq_target_report = None
        synciq_target_sub_report_details = None

        if not id and not name:
            error_message = 'Please provide a valid report id or valid report name'
            self.module.fail_json(msg=error_message)

        if state != 'present':
            error_message = 'Please provide a valid value for state'
            self.module.fail_json(msg=error_message)

        if not include_sub_reports and not sub_report_id:
            if id:
                synciq_target_report = self.get_synciq_target_report(id)

            if name:
                id = self.get_target_report_id(name)
                synciq_target_report = self.get_synciq_target_report(id)

        if include_sub_reports:
            if id:
                synciq_target_sub_report_details = self.get_synciq_target_sub_reports(id)

            if name:
                id = self.get_target_report_id(name)
                synciq_target_sub_report_details = self.get_synciq_target_sub_reports(id)

        if sub_report_id and (id or name):
            if id:
                synciq_target_sub_report_detail = self.get_synciq_taget_sub_report(sub_report_id, id)
            elif name:
                id = self.get_target_report_id(name)
                synciq_target_sub_report_detail = self.get_synciq_taget_sub_report(sub_report_id, id)

        if synciq_target_report:
            self.result["synciq_target_report_details"] = synciq_target_report
            self.module.exit_json(**self.result)

        if synciq_target_sub_report_details:
            self.result["synciq_target_subreport_details"] = synciq_target_sub_report_details
            self.module.exit_json(**self.result)

        if synciq_target_sub_report_detail:
            self.result["synciq_subreport_detail"] = synciq_target_sub_report_detail
            self.module.exit_json(**self.result)


def get_synciq_target_reports_parameters():
    """This method provide parameter required for the ansible SyncIQ
    reports modules on PowerScale"""
    return dict(
        id=dict(required=False, type='str'),
        name=dict(required=False, type='str'),
        state=dict(required=True, type='str', choices=['present', 'absent']),
        sub_report_id=dict(required=False, type='str'),
        include_sub_reports=dict(required=False, type='bool', default=False))


def main():
    """ Create PowerScale SyncIQ Report object and perform actions on it
        based on user input from playbook"""
    obj = SyncIQTargetReports()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
