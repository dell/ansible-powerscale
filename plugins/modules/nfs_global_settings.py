#!/usr/bin/python
# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing NFS global settings on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: nfs_global_settings
version_added: '2.2.0'
short_description:  Manage NFS global settings on a PowerScale Storage System
description:
- Managing NFS global settings on an PowerScale system includes retrieving details of
  NFS global settings and modifying NFS global settings.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Trisha Datta (@trisha-dell) <ansible.team@dell.com>

options:
  service:
    description:
    - Specifies if the NFS service needs to be enabled or not.
    type: bool
  rpc_maxthreads:
    description:
    - Specifies the maximum number of threads in the nfsd thread pool.
    type: int
  rpc_minthreads:
    description:
    - Specifies the minimum number of threads in the nfsd thread pool.
    type: int
  rquota_enabled:
    description:
    - Enable/Disable the rquota protocol.
    type: bool
  nfs_rdma_enabled:
    description:
    - Enables or disables RDMA for NFS.
    - Supported on PowerScale 9.8 and later.
    type: bool
  nfsv3:
    description:
    - Enable/disable NFSv3 protocol.
    type: dict
    suboptions:
      nfsv3_enabled:
        description:
        - Enable/disable NFSv3 protocol.
        type: bool
      nfsv3_rdma_enabled:
        description:
        - To enable/disable RDMA for NFSv3 protocol.
        - For PowerScale 9.8 I(nfsv3_rdma_enabled) is not supported
          and I(nfs_rdma_enabled) is used for both nfsv3 and nfsv4.
        type: bool
  nfsv4:
    description:
    - Specifies the minor versions of NFSv4 protocol.
    type: dict
    suboptions:
      nfsv4_enabled:
        description:
        - Enable/disable all minor versions of NFSv4 protocol.
        type: bool
      nfsv40_enabled:
        description:
        - Enable/disable minor version 0 of NFSv4 protocol.
        type: bool
      nfsv41_enabled:
        description:
        - Enable/disable minor version 1 of NFSv4 protocol.
        type: bool
      nfsv42_enabled:
        description:
        - Enable/disable minor version 2 of NFSv4 protocol.
        type: bool
notes:
- The I(check_mode) is supported.
'''

EXAMPLES = r'''
- name: Get NFS global settings
  dellemc.powerscale.nfs_global_settings:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"

- name: Update service of NFS global settings
  dellemc.powerscale.nfs_global_settings:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    service: true
    nfsv3:
      nfsv3_enabled: false
    nfsv4:
      nfsv40_enabled: true
      nfsv41_enabled: true
      nfsv42_enabled: false
    nfs_rdma_enabled: true
    rpc_minthreads: 17
    rpc_maxthreads: 20
    rquota_enabled: true
'''

RETURN = r'''
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
nfs_global_settings_details:
    description: The updated nfs global settings details.
    type: complex
    returned: always
    contains:
        nfsv3_enabled:
            description: Whether NFSv3 protocol is enabled/disabled.
            type: bool
        nfsv3_rdma_enabled:
            description: Whether rdma is enabled for NFSv3 protocol.
            type: bool
        nfsv40_enabled:
            description: Whether version 0 of NFSv4 protocol is enabled/disabled.
            type: bool
        nfsv41_enabled:
            description: Whether version 1 of NFSv4 protocol is enabled/disabled.
            type: bool
        nfsv42_enabled:
            description: Whether version 2 of NFSv4 protocol is enabled/disabled.
            type: bool
        nfsv4_enabled:
            description: Whether NFSv4 protocol is enabled/disabled.
            type: bool
        rpc_maxthreads:
            description: Specifies the maximum number of threads in the nfsd thread pool.
            type: int
        rpc_minhreads:
            description: Specifies the minimum number of threads in the nfsd thread pool.
            type: int
        rquota_enabled:
            description: Whether the rquota protocol is enabled/disabled.
            type: bool
        service:
            description: Whether the NFS service is enabled/disabled.
            type: bool
    sample: {
        "nfsv3_enabled": false,
        "nfsv3_rdma_enabled": true,
        "nfsv40_enabled": true,
        "nfsv41_enabled": true,
        "nfsv42_enabled": false,
        "nfsv4_enabled": true,
        "rpc_maxthreads": 20,
        "rpc_minthreads": 17,
        "rquota_enabled": true,
        "service": true
    }

'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('nfs_global_settings')


class NFSGlobalSettings:
    """Class with NFS global settings operations"""

    def __init__(self):
        """ Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(self.get_nfs_global_settings_parameters())
        # Initialize the ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=True
        )
        # Result is a dictionary that contains changed status, NFS global
        # settings details
        self.result = {
            "changed": False,
            "nfs_global_settings_details": {}
        }

        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        self.array_version = f"{self.isi_sdk.major}.{self.isi_sdk.minor}"

        LOG.info('Got python SDK instance for provisioning on PowerScale ')
        check_mode_msg = f'Check mode flag is {self.module.check_mode}'
        LOG.info(check_mode_msg)

        self.protocol_api = self.isi_sdk.ProtocolsApi(self.api_client)

    def validate_input(self):
        """
        Validate the input parameters based on the array version.
        This method checks whether certain parameters are allowed based on the array version.
        If the array version is 9.8 or later, the nfsv3.nfsv3_rdma_enabled parameter is not allowed.
        If the array version is earlier than 9.8, the nfs_rdma_enabled parameter is not allowed.
        """
        params = self.module.params

        if utils.parse_version(self.array_version) < utils.parse_version("9.8"):
            if params.get("nfs_rdma_enabled") is not None:
                self.module.fail_json(msg="nfs_rdma_enabled is not allowed when array version is earlier than 9.8.")
        else:
            if params.get("nfsv3") and params.get("nfsv3").get("nfsv3_rdma_enabled") is not None:
                self.module.fail_json(msg="nfsv3.nfsv3_rdma_enabled is not allowed when array version is 9.8 or later.")

    def get_nfs_global_settings_details(self):
        """
        Get details of NFS global settings
        """
        msg = "Getting NFS global settings details"
        LOG.info(msg)
        try:
            nfs_global_obj = self.protocol_api.get_nfs_settings_global()
            if nfs_global_obj:
                msg = f"NFS global settings details are: {nfs_global_obj.settings.to_dict()}"
                LOG.info(msg)
                return nfs_global_obj.settings.to_dict()

        except Exception as e:
            error_msg = f"Got error {utils.determine_error(e)} while getting" \
                        f" NFS global setings details "
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def modify_nfs_global_settings(self, modify_dict):
        """
        Modify the NFS global settings based on modify dict
        :param modify_dict: dict containing parameters to be modfied
        """
        try:
            msg = "Modify NFS global settings with parameters"
            LOG.info(msg)
            if not self.module.check_mode:
                self.protocol_api.update_nfs_settings_global(
                    nfs_settings_global=modify_dict)
                LOG.info("Successfully modified the NFS global settings.")
            return True

        except Exception as e:
            error_msg = f"Modify NFS global settings failed with " \
                        f"error: {utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def is_nfsv3v4_modify_required(self, settings_params, settings_details, modify_dict):
        """
        Check whether modification is required in NFSv3 or NFSv4
        """
        nfsv4_keys = ["nfsv4_enabled", "nfsv40_enabled", "nfsv41_enabled", "nfsv42_enabled"]
        if settings_params["nfsv4"] is not None:
            for key in nfsv4_keys:
                if key in settings_params["nfsv4"] and settings_params["nfsv4"][key] is not None and \
                        settings_details[key] != settings_params["nfsv4"][key]:
                    modify_dict[key] = settings_params["nfsv4"][key]

        nfsv3_keys = ["nfsv3_enabled", "nfsv3_rdma_enabled"]
        if settings_params["nfsv3"] is not None:
            for key in nfsv3_keys:
                if key in settings_params["nfsv3"] and settings_params["nfsv3"][key] is not None and \
                        settings_details[key] != settings_params["nfsv3"][key]:
                    modify_dict[key] = settings_params["nfsv3"][key]

        return modify_dict

    def is_nfs_global_modify_required(self, settings_params, settings_details):
        """
        Check whether modification is required in NFS global settings
        """
        modify_dict = {}
        keys = ["service", "rpc_maxthreads", "rpc_minthreads", "rquota_enabled", "nfs_rdma_enabled"]
        for key in keys:
            if key in settings_params and settings_params[key] is not None and \
                    settings_details[key] != settings_params[key]:
                modify_dict[key] = settings_params[key]

        modify_dict = self.is_nfsv3v4_modify_required(settings_params=settings_params,
                                                      settings_details=settings_details,
                                                      modify_dict=modify_dict)

        return modify_dict

    def get_nfs_global_settings_parameters(self):
        return dict(
            service=dict(type='bool'), rpc_maxthreads=dict(type='int'),
            rpc_minthreads=dict(type='int'),
            rquota_enabled=dict(type='bool'),
            nfs_rdma_enabled=dict(type='bool'),
            nfsv3=dict(
                type='dict', options=dict(
                    nfsv3_enabled=dict(type='bool'),
                    nfsv3_rdma_enabled=dict(type='bool'))),
            nfsv4=dict(
                type='dict', options=dict(
                    nfsv4_enabled=dict(type='bool'),
                    nfsv40_enabled=dict(type='bool'),
                    nfsv41_enabled=dict(type='bool'),
                    nfsv42_enabled=dict(type='bool')))
        )


class NFSGlobalSettingsExitHandler:
    def handle(self, nfs_global_obj, nfs_global_details):
        nfs_global_obj.result["nfs_global_settings_details"] = nfs_global_details
        nfs_global_obj.module.exit_json(**nfs_global_obj.result)


class NFSGlobalSettingsModifyHandler:
    def handle(self, nfs_global_obj, nfs_global_params, nfs_global_details):
        modify_params = nfs_global_obj.is_nfs_global_modify_required(nfs_global_params,
                                                                     nfs_global_details)
        if modify_params:
            changed = nfs_global_obj.modify_nfs_global_settings(
                modify_dict=modify_params)
            nfs_global_details = nfs_global_obj.get_nfs_global_settings_details()
            nfs_global_obj.result["changed"] = changed
            nfs_global_obj.result["nfs_global_settings_details"] = nfs_global_details

        NFSGlobalSettingsExitHandler().handle(nfs_global_obj, nfs_global_details)


class NFSGlobalSettingsHandler:
    def handle(self, nfs_global_obj, nfs_global_params):
        nfs_global_obj.validate_input()
        nfs_global_details = nfs_global_obj.get_nfs_global_settings_details()
        NFSGlobalSettingsModifyHandler().handle(
            nfs_global_obj=nfs_global_obj, nfs_global_params=nfs_global_params,
            nfs_global_details=nfs_global_details)


def main():
    """ perform action on PowerScale NFS Global settings and perform action on it
        based on user input from playbook."""
    obj = NFSGlobalSettings()
    NFSGlobalSettingsHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
