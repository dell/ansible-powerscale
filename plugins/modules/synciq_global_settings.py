#!/usr/bin/python
# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Ansible module for managing SyncIQ global settings on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: synciq_global_settings
version_added: '2.3.0'
short_description:  Manage SyncIQ global settings on a PowerScale Storage System
description:
- Managing SyncIQ global settings on an PowerScale system includes retrieving details of
  SyncIQ global settings and modifying SyncIQ global settings.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Pavan Mudunuri(@Pavan-Mudunuri) <ansible.team@dell.com>

options:
  service:
    description:
    - Specifies if the SyncIQ service currently C(on), C(paused), or C(off).
    - If C(paused), all sync jobs will be paused. If turned C(off), all jobs will be canceled.
    type: str
    choices: ['on', 'off', 'paused']
    default: 'on'
  encryption_required:
    description:
    - If true, requires all SyncIQ policies to utilize encrypted communications.
    type: bool
    default: false
notes:
- The I(check_mode) is supported.
'''

EXAMPLES = r'''
- name: Get SyncIQ global settings
  dellemc.powerscale.synciq_global_settings:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"

- name: Update service of SyncIQ global settings
  dellemc.powerscale.synciq_global_settings:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    service: "on"
    encryption_required: true
'''

RETURN = r'''
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
synciq_global_settings:
    description: The SyncIQ global settings details.
    type: dict
    returned: always
    contains:
        bandwidth_reservation_reserve_absolute:
            description: The absolute bandwidth reservation for SyncIQ.
            type: int
        bandwidth_reservation_reserve_percentage:
            description: The percentage-based bandwidth reservation for SyncIQ.
            type: int
        cluster_certificate_id:
            description: The ID of the cluster certificate used for SyncIQ.
            type: str
        encryption_cipher_list:
            description: The list of encryption ciphers used for SyncIQ.
            type: str
        encryption_required:
            description: Whether encryption is required or not for SyncIQ.
            type: bool
        force_interface:
            description: Whether the force interface is enabled or not for SyncIQ.
            type: bool
        max_concurrent_jobs:
            description: The maximum number of concurrent jobs for SyncIQ.
            type: int
        ocsp_address:
            description: The address of the OCSP server used for SyncIQ certificate validation.
            type: str
        ocsp_issuer_certificate_id:
            description: The ID of the issuer certificate used for OCSP validation in SyncIQ.
            type: str
        preferred_rpo_alert:
            description: Whether the preferred RPO alert is enabled or not for SyncIQ.
            type: bool
        renegotiation_period:
            description: The renegotiation period in seconds for SyncIQ.
            type: int
        report_email:
            description: The email address to which SyncIQ reports are sent.
            type: str
        report_max_age:
            description: The maximum age in days of reports that are retained by SyncIQ.
            type: int
        report_max_count:
            description: The maximum number of reports that are retained by SyncIQ.
            type: int
        restrict_target_network:
            description: Whether to restrict the target network in SyncIQ.
            type: bool
        rpo_alerts:
            description: Whether RPO alerts are enabled or not in SyncIQ.
            type: bool
        service:
            description: Specifies whether the SyncIQ service is currently on, off, or paused.
            type: str
        service_history_max_age:
            description: The maximum age in days of service history that is retained by SyncIQ.
            type: int
        service_history_max_count:
            description: The maximum number of service history records that are retained by SyncIQ.
            type: int
        source_network:
            description: The source network used by SyncIQ.
            type: str
        tw_chkpt_interval:
            description: The interval between checkpoints in seconds in SyncIQ.
            type: int
        use_workers_per_node:
           description : Whether to use workers per node in SyncIQ or not.
           type : bool
    sample: {
              "bandwidth_reservation_reserve_absolute": null,
              "bandwidth_reservation_reserve_percentage": 1,
              "cluster_certificate_id": "xxxx",
              "encryption_cipher_list": "",
              "encryption_required": true,
              "force_interface": false,
              "max_concurrent_jobs": 16,
              "ocsp_address": "",
              "ocsp_issuer_certificate_id": "",
              "preferred_rpo_alert": 0,
              "renegotiation_period": 28800,
              "report_email": [],
              "report_max_age": 31536000,
              "report_max_count": 2000,
              "restrict_target_network": false,
              "rpo_alerts": true,
              "service": "off",
              "service_history_max_age": 31536000,
              "service_history_max_count": 2000,
              "source_network": null,
              "tw_chkpt_interval": null,
              "use_workers_per_node": false
            }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.powerscale_base \
    import PowerScaleBase
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.synciq \
    import SyncIQ
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('synciq_global_settings')


class SyncIQGlobalSettings(PowerScaleBase):
    """Class with SyncIQ global settings operations"""

    def __init__(self):
        ''' Define all parameters required by this module'''

        ansible_module_params = {
            'argument_spec': self.get_synciq_global_settings_parameters(),
            'supports_check_mode': True
        }

        super().__init__(AnsibleModule, ansible_module_params)

        self.result["synciq_global_settings"] = dict()

    def get_synciq_global_settings(self):
        """
        Get details of SyncIQ global settings.
        :return: SyncIQ global settings
        :rtype: dict
        """
        return SyncIQ(self.synciq_api, self.module).get_synciq_global_settings()

    def modify_synciq_global_settings(self, modify_dict):
        """
        Modify the SyncIQ global settings based on modify dict
        :param modify_dict: dict containing parameters to be modfied
        """
        try:
            msg = "Modify SyncIQ global settings with parameters"
            LOG.info(msg)
            if not self.module.check_mode:
                self.synciq_api.update_sync_settings(
                    sync_settings=modify_dict)
                LOG.info("Successfully modified the SyncIQ global settings.")
            return True

        except Exception as e:
            error_msg = f"Modify SyncIQ global settings failed with " \
                        f"error: {utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def is_synciq_global_modify_required(self, settings_params, settings_details):
        """
        Check whether modification is required in SyncIQ global settings
        """
        modify_dict = {}
        keys = ["service", "encryption_required"]
        for key in keys:
            if settings_params[key] is not None and \
                    settings_details[key] != settings_params[key]:
                modify_dict[key] = settings_params[key]

        return modify_dict

    def get_synciq_global_settings_parameters(self):
        return dict(
            service=dict(type='str', choices=['on', 'off', 'paused'], default='on'),
            encryption_required=dict(type='bool', default='false')
        )


class SyncIQGlobalSettingsExitHandler:
    def handle(self, synciq_global_obj, synciq_global_details):
        synciq_global_obj.result["synciq_global_settings"] = synciq_global_details
        synciq_global_obj.module.exit_json(**synciq_global_obj.result)


class SyncIQGlobalSettingsModifyHandler:
    def handle(self, synciq_global_obj, synciq_global_params, synciq_global_details):
        modify_params = synciq_global_obj.is_synciq_global_modify_required(synciq_global_params,
                                                                           synciq_global_details)
        if modify_params:
            changed = synciq_global_obj.modify_synciq_global_settings(
                modify_dict=modify_params)
            synciq_global_details = synciq_global_obj.get_synciq_global_settings()
            synciq_global_obj.result["changed"] = changed
            synciq_global_obj.result["synciq_global_settings"] = synciq_global_details

        SyncIQGlobalSettingsExitHandler().handle(synciq_global_obj, synciq_global_details)


class SyncIQGlobalSettingsHandler:
    def handle(self, synciq_global_obj, synciq_global_params):
        synciq_global_details = synciq_global_obj.get_synciq_global_settings()
        SyncIQGlobalSettingsModifyHandler().handle(
            synciq_global_obj=synciq_global_obj, synciq_global_params=synciq_global_params,
            synciq_global_details=synciq_global_details)


def main():
    """ perform action on PowerScale SyncIQ Global settings and perform action on it
        based on user input from playbook."""
    obj = SyncIQGlobalSettings()
    SyncIQGlobalSettingsHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
