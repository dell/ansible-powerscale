#!/usr/bin/python
# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing SMB global settings on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: smb_global_settings
version_added: '2.4.0'
short_description: Manage SMB global settings on a PowerScale Storage System
description:
- Managing SMB global settings on a PowerScale system includes retrieving details of
  SMB global settings and modifying SMB global settings.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
  - Sachin Apagundi (@sachin-apa) <ansible.team@dell.com>
options:
  access_based_share_enum:
    description: Only enumerate files and folders the requesting user has access to.
    type: bool
  dot_snap_accessible_child:
    description: Allow access to .snapshot directories in share subdirectories.
    type: bool
  dot_snap_accessible_root:
    description: Allow access to the .snapshot directory in the root of the share.
    type: bool
  dot_snap_visible_child:
    description: Show .snapshot directories in share subdirectories.
    type: bool
  dot_snap_visible_root:
    description: Show the .snapshot directory in the root of a share.
    type: bool
  enable_security_signatures:
    description: Indicates whether the server supports signed SMB packets.
    type: bool
  guest_user:
    description: Specifies the fully-qualified user to use for guest access.
    type: str
  ignore_eas:
    description: Specify whether to ignore EAs on files.
    type: bool
  onefs_cpu_multiplier:
    description: Specify the number of OneFS driver worker threads per CPU.
    type: int
  onefs_num_workers:
    description: Set the maximum number of OneFS driver worker threads.
    type: int
  reject_unencrypted_access:
    description: If SMB3 encryption is enabled, reject unencrypted access from clients.
    type: bool
  require_security_signatures:
    description: Indicates whether the server requires signed SMB packets.
    type: bool
  server_side_copy:
    description: Enable Server Side Copy.
    type: bool
  server_string:
    description: Provides a description of the server.
    type: str
  service:
    description: Specify whether service is enabled.
    type: bool
  support_multichannel:
    description: Support multichannel.
    type: bool
  support_netbios:
    description: Support NetBIOS.
    type: bool
  support_smb2:
    description: The support SMB2 attribute.
    type: bool
  support_smb3_encryption:
    description: Support the SMB3 encryption on the server.
    type: bool
notes:
- The I(check_mode) is supported.
'''

EXAMPLES = r'''
- name: Get SMB global settings
  dellemc.powerscale.smb_global_settings:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"

- name: Update SMB global settings
  dellemc.powerscale.smb_global_settings:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    access_based_share_enum: true
    dot_snap_accessible_child: true
    dot_snap_accessible_root: false
    dot_snap_visible_child: false
    dot_snap_visible_root: true
    enable_security_signatures: true
    guest_user: user
    ignore_eas: false
    onefs_cpu_multiplier: 2
    onefs_num_workers: 4
    reject_unencrypted_access: true
    require_security_signatures: true
    server_side_copy: true
    server_string: 'PowerScale Server'
    service: true
    support_multichannel: true
    support_netbios: true
    support_smb2: true
    support_smb3_encryption: true
'''

RETURN = r'''
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
smb_global_settings_details:
    description: The updated SMB global settings details.
    type: dict
    returned: always
    contains:
      access_based_share_enum:
        description: Only enumerate files and folders the requesting user has access to.
        type: bool
      audit_fileshare:
        description: Specify level of file share audit events to log.
        type: str
      audit_logon:
        description: Specify the level of logon audit events to log.
        type: str
      dot_snap_accessible_child:
        description: Allow access to .snapshot directories in share subdirectories.
        type: bool
      dot_snap_accessible_root:
        description: Allow access to the .snapshot directory in the root of the share.
        type: bool
      dot_snap_visible_child:
        description: Show .snapshot directories in share subdirectories.
        type: bool
      dot_snap_visible_root:
        description: Show the .snapshot directory in the root of a share.
        type: bool
      enable_security_signatures:
        description: Indicates whether the server supports signed SMB packets.
        type: bool
      guest_user:
        description: Specifies the fully-qualified user to use for guest access.
        type: str
      ignore_eas:
        description: Specify whether to ignore EAs on files.
        type: bool
      onefs_cpu_multiplier:
        description: Specify the number of OneFS driver worker threads per CPU.
        type: int
      onefs_num_workers:
        description: Set the maximum number of OneFS driver worker threads.
        type: int
      reject_unencrypted_access:
        description: If SMB3 encryption is enabled, reject unencrypted access from clients.
        type: bool
      require_security_signatures:
        description: Indicates whether the server requires signed SMB packets.
        type: bool
      server_side_copy:
        description: Enable Server Side Copy.
        type: bool
      server_string:
        description: Provides a description of the server.
        type: str
      service:
        description: Specify whether service is enabled.
        type: bool
      srv_cpu_multiplier:
        description: Specify the number of SRV service worker threads per CPU.
        type: int
      srv_num_workers:
        description: Set the maximum number of SRV service worker threads.
        type: int
      support_multichannel:
        description: Support multichannel.
        type: bool
      support_netbios:
        description: Support NetBIOS.
        type: bool
      support_smb2:
        description: The support SMB2 attribute.
        type: bool
      support_smb3_encryption:
        description: Support the SMB3 encryption on the server.
        type: bool
    sample: {
      "access_based_share_enum": false,
      "audit_fileshare": null,
      "audit_logon": null,
      "dot_snap_accessible_child": true,
      "dot_snap_accessible_root": true,
      "dot_snap_visible_child": false,
      "dot_snap_visible_root": true,
      "enable_security_signatures": false,
      "guest_user": "nobody",
      "ignore_eas": false,
      "onefs_cpu_multiplier": 4,
      "onefs_num_workers": 0,
      "reject_unencrypted_access": false,
      "require_security_signatures": false,
      "server_side_copy": false,
      "server_string": "PowerScale Server",
      "service": true,
      "srv_cpu_multiplier": null,
      "srv_num_workers": null,
      "support_multichannel": true,
      "support_netbios": false,
      "support_smb2": true,
      "support_smb3_encryption": true
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.powerscale_base \
    import PowerScaleBase
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.protocol \
    import Protocol

LOG = utils.get_logger('smb_global_settings')


class SMBGlobalSettings(PowerScaleBase):
    """Class with SMB global settings operations"""

    def __init__(self):
        """ Define all parameters required by the SMB global settings module"""

        ansible_module_params = {
            'argument_spec': self.get_smb_global_settings_parameters(),
            'supports_check_mode': True,
        }
        super().__init__(AnsibleModule, ansible_module_params)

        # Result is a dictionary that contains changed status and SMB global
        # settings details
        self.result.update({
            "smb_global_settings_details": {}
        })

    def get_smb_global_settings_details(self):
        """
        Get details of SMB global settings
        """
        return Protocol(self.protocol_api, self.module).get_smb_global_settings()

    def modify_smb_global_settings(self, modify_dict):
        """
        Modify the SMB global settings based on modify dict
        :param modify_dict: dict containing parameters to be modfied
        """
        try:
            msg = "Modify SMB global settings with parameters"
            LOG.info(msg)
            if not self.module.check_mode:
                self.protocol_api.update_smb_settings_global(
                    smb_settings_global=modify_dict)
                LOG.info("Successfully modified the SMB global settings.")
            return True

        except Exception as e:
            error_msg = f"Modify SMB global settings failed with " \
                        f"error: {utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def is_smb_global_modify_required(self, settings_params, settings_details):
        """
        Check whether modification is required in SMB global settings
        """
        modify_dict = {}
        for key in self.get_smb_keys():
            if settings_params.get(key) is not None and \
                    settings_details[key] != settings_params[key]:
                modify_dict[key] = settings_params[key]
        return modify_dict

    def get_smb_keys(self):
        """
          Returns a list of SMB keys.
        """
        return ["access_based_share_enum", "dot_snap_accessible_child",
                "dot_snap_accessible_root", "dot_snap_visible_child",
                "dot_snap_visible_root", "enable_security_signatures",
                "guest_user", "ignore_eas", "onefs_cpu_multiplier",
                "onefs_num_workers", "reject_unencrypted_access",
                "require_security_signatures", "server_side_copy",
                "server_string", "service", "support_multichannel",
                "support_netbios", "support_smb2", "support_smb3_encryption"]

    def get_smb_global_settings_parameters(self):
        return dict(
            access_based_share_enum=dict(type='bool'),
            dot_snap_accessible_child=dict(type='bool'),
            dot_snap_accessible_root=dict(type='bool'),
            dot_snap_visible_child=dict(type='bool'),
            dot_snap_visible_root=dict(type='bool'),
            enable_security_signatures=dict(type='bool'),
            guest_user=dict(type='str'),
            ignore_eas=dict(type='bool'),
            onefs_cpu_multiplier=dict(type='int'),
            onefs_num_workers=dict(type='int'),
            reject_unencrypted_access=dict(type='bool'),
            require_security_signatures=dict(type='bool'),
            server_side_copy=dict(type='bool'),
            server_string=dict(type='str'),
            service=dict(type='bool'),
            support_multichannel=dict(type='bool'),
            support_netbios=dict(type='bool'),
            support_smb2=dict(type='bool'),
            support_smb3_encryption=dict(type='bool')
        )


class SMBGlobalSettingsExitHandler:
    def handle(self, smb_global_obj, smb_global_details):
        smb_global_obj.result["smb_global_settings_details"] = smb_global_details
        smb_global_obj.module.exit_json(**smb_global_obj.result)


class SMBGlobalSettingsModifyHandler:
    def handle(self, smb_global_obj, smb_global_params, smb_global_details):
        modify_params = smb_global_obj.is_smb_global_modify_required(smb_global_params,
                                                                     smb_global_details)
        if modify_params:
            changed = smb_global_obj.modify_smb_global_settings(
                modify_dict=modify_params)
            smb_global_details = smb_global_obj.get_smb_global_settings_details()
            smb_global_obj.result["changed"] = changed
            smb_global_obj.result["smb_global_settings_details"] = smb_global_details

        SMBGlobalSettingsExitHandler().handle(smb_global_obj, smb_global_details)


class SMBGlobalSettingsHandler:
    def handle(self, smb_global_obj, smb_global_params):
        smb_global_details = smb_global_obj.get_smb_global_settings_details()
        SMBGlobalSettingsModifyHandler().handle(
            smb_global_obj=smb_global_obj, smb_global_params=smb_global_params,
            smb_global_details=smb_global_details)


def main():
    """ perform action on PowerScale SMB Global settings and perform action on it
        based on user input from playbook."""
    obj = SMBGlobalSettings()
    SMBGlobalSettingsHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
