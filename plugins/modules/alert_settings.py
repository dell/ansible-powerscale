#!/usr/bin/python
# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing alert settings on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: alert_settings
version_added: '3.2.0'
short_description: Manage alert settings on a PowerScale Storage System
description:
- Managing alert settings on a PowerScale system includes retrieving details of
  alert settings and enabling or disabling the alert settings.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
  - Bhavneet Sharma (@Bhavneet-Sharma) <ansible.team@dell.com>
options:
  enable_celog_maintenance_mode:
    description:
    - Enabling CELOG maintenance mode will start a CELOG maintenance window.
    - During a CELOG maintenance window, the system will continue to log
      events, but no alerts will be generated.
    - You will have the opportunity to review all events that took place
      during the maintenance window when disabling maintenance mode.
    - Active event groups will automatically resume generating alerts when
      the scheduled maintenance period ends.
    type: bool
  prune:
    description:
    - Removes all maintenance mode history that is greater than set number of days.
    - Range of I(prune) is 0 to 4294967295.
    - If I(prune) is set in task, then I(changed) will be C(true) always.
    type: int

notes:
- The I(check_mode) and idempotency is supported.
- Idempotency is not supported with I(prune) option.
'''

EXAMPLES = r'''
- name: Enable CELOG maintenance mode
  dellemc.powerscale.alert_settings:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    enable_celog_maintenance_mode: true

- name: Disable CELOG and prune all history of maintenance mode
  dellemc.powerscale.alert_settings:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    enable_celog_maintenance_mode: false
    prune: 0
'''

RETURN = r'''
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
alert_settings_details:
    description: The updated alert settings details.
    type: dict
    returned: always
    contains:
      history:
        description: History list of CELOG maintenance mode windows.
        type: list
        contains:
          end:
            description:
              - End time of CELOG maintenance mode, as a UNIX
                timestamp in seconds.
              - Value 0 indicates that maintenance mode is still enabled.
              - Refer alert setting sample playbook examples to convert
                UNIX timestamp to human readable format.
            type: int
          start:
            description:
              - Start time of CELOG maintenance mode, as a UNIX
                timestamp in seconds.
              - Refer alert setting sample playbook examples to convert
                UNIX timestamp to human readable format.
            type: int
      maintenance:
        description: Indicates if maintenance mode is enabled.
        type: bool
    sample: {
      history: [
        {
          "end": 0,
          "start": 1719822336
        }
      ],
      "maintenance": false
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.powerscale_base \
    import PowerScaleBase
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.cluster \
    import Cluster
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.events \
    import Events

LOG = utils.get_logger('alert_settings')


class AlertSettings(PowerScaleBase):
    """Class with alert settings operations"""

    def __init__(self):
        """ Define all parameters required by the alert settings module"""

        ansible_module_params = {
            'argument_spec': self.get_alert_setting_parameters(),
            'supports_check_mode': True,
        }
        super().__init__(AnsibleModule, ansible_module_params)

        self.major = self.isi_sdk.major
        self.minor = self.isi_sdk.minor

        # Result is a dictionary that contains changed status and alert
        # settings details
        self.result.update({
            "alert_settings_details": {}
        })

    def get_alert_settings_details(self):
        """
        Get details of alert settings
        """
        msg = "Getting alert settings details"
        LOG.info(msg)
        if self.major > 9 or (self.major == 9 and self.minor > 9):
            return Cluster(self.cluster_api, self.module).get_maintenance_settings_details()
        else:
            return Events(self.event_api, self.module).get_event_maintenance()

    def modify_alert_settings(self, modify_dict):
        """
        Modify the alert settings based on modify dict
        :param modify_dict: dict containing parameters to be modfied
        """
        try:
            msg = "Modifing maintenance mode with parameters"
            LOG.info(msg)
            if self.major > 9 or (self.major == 9 and self.minor > 9):
                if modify_dict.get('prune') is not None:
                  event_settings = self.isi_sdk.EventSettingsSettings(retention_days=modify_dict.get('prune'))
                  if not self.module.check_mode:
                    self.event_api.update_event_settings(event_settings=event_settings)
                  LOG.info("Successfully modified the event settings retention_days.")
                if modify_dict.get('enable_celog_maintenance_mode') is not None:
                  cluster_maintenance = self.isi_sdk.MaintenanceSettingsExtended(active=modify_dict.get('enable_celog_maintenance_mode'))
                  if not self.module.check_mode:
                      self.cluster_api.update_maintenance_settings(maintenance_settings=cluster_maintenance)
                  LOG.info("Successfully modified the cluster maintenance mode.")
            else:
                event_maintenance = self.isi_sdk.EventMaintenanceExtended(
                    maintenance=modify_dict.get('enable_celog_maintenance_mode'),
                    prune=modify_dict.get('prune'))
                if not self.module.check_mode:
                    self.event_api.update_event_maintenance(event_maintenance=event_maintenance)
                LOG.info("Successfully modified the event maintenance.")
            return True

        except Exception as e:
            error_msg = f"Modify alert settings failed with " \
                        f"error: {utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def is_alert_setting_modify_required(self, settings_params, settings_details):
        """
        Check if alert setting modify is required
        :param settings_params: contains params passed through playbook
        :param settings_details: contains alert settings details
        """
        modify_dict = {}
        pb_maintenance = settings_params.get('enable_celog_maintenance_mode')
        cluster_maintenance_active_resp = settings_details.get('active')
        event_settings_maintenance_resp = settings_details.get('maintenance')

        if pb_maintenance is not None:
          if cluster_maintenance_active_resp is not None and cluster_maintenance_active_resp != pb_maintenance \
            or event_settings_maintenance_resp is not None and event_settings_maintenance_resp != pb_maintenance:
              modify_dict['enable_celog_maintenance_mode'] = pb_maintenance

        if settings_params.get('prune') is not None:
            modify_dict['prune'] = settings_params.get('prune')
        return modify_dict

    def get_alert_setting_parameters(self):
        return dict(
            enable_celog_maintenance_mode=dict(type='bool'),
            prune=dict(type='int'))


class AlertSettingsExitHandler:
    def handle(self, alert_setting_obj, alert_setting_details):
        alert_setting_obj.result["alert_settings_details"] = alert_setting_details
        alert_setting_obj.module.exit_json(**alert_setting_obj.result)


class AlertSettingsModifyHandler:
    def handle(self, alert_setting_obj, alert_setting_params):
        alert_setting_details = alert_setting_obj.get_alert_settings_details()
        modify_params = alert_setting_obj.is_alert_setting_modify_required(
            settings_params=alert_setting_params,
            settings_details=alert_setting_details)
        if modify_params:
            changed = alert_setting_obj.modify_alert_settings(
                modify_dict=modify_params)
            alert_setting_details = alert_setting_obj.get_alert_settings_details()
            alert_setting_obj.result["changed"] = changed

        AlertSettingsExitHandler().handle(alert_setting_obj, alert_setting_details)


def main():
    """ perform action on PowerScale Alert Settings object and perform action on it
        based on user input from playbook."""
    obj = AlertSettings()
    AlertSettingsModifyHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
