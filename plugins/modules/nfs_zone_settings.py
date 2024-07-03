#!/usr/bin/python
# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing NFS zone settings on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: nfs_zone_settings
version_added: '2.2.0'
short_description:  Manage NFS zone settings on a PowerScale Storage System
description:
- Managing NFS zone settings on an PowerScale system includes
  retrieving details and modifying NFS zone settings.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Bhavneet Sharma(@Bhavneet-Sharma) <ansible.team@dell.com>

options:
  access_zone:
    description:
    - Specifies the access zone in which the NFS zone settings apply.
    type: str
    default: System
  nfsv4_allow_numeric_ids:
    description:
    - If C(true), send owner and groups as UIDs and GIDs when look up fails or
      I(nfsv4_no_names) is set C(rue).
    type: bool
  nfsv4_domain:
    description:
    - Specifies the domain through which users and groups are associated.
    type: str
  nfsv4_no_domain:
    description:
    - If C(true), sends owners and groups without a domain name.
    type: bool
  nfsv4_no_domain_uids:
    description:
    - If C(true), sends UIDs and GIDs without a domain name.
    type: bool
  nfsv4_no_names:
    description:
    - If C(true), sends owners and groups as UIDs and GIDs.
    type: bool
  nfsv4_replace_domain:
    description:
    - If C(true), replaces the owner or group domain with an NFS domain name.
    type: bool
notes:
- The I(check_mode) is supported.
'''

EXAMPLES = r'''
- name: Get NFS zone settings
  dellemc.powerscale.nfs_zone_settings:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    access_zone: "sample-zone"

- name: Modify NFS zone settings
  dellemc.powerscale.nfs_zone_settings:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    access_zone: "sample-zone"
    nfsv4_allow_numeric_ids: true
    nfsv4_domain: "example.com"
    nfsv4_no_domain: true
    nfsv4_no_domain_uids: false
'''

RETURN = r'''
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
nfs_zone_settings_details:
    description: The NFS zone settings details.
    type: dict
    returned: always
    contains:
        nfsv4_allow_numeric_ids:
            description: If C(true), sends owners and groups as UIDs and
                         GIDs when look up fails or if the I(nfsv4_no_names)
                         property is set to 1.
            type: bool
        nfsv4_domain:
            description: Specifies the domain through which users and groups
                         are associated.
            type: str
        nfsv4_no_domain:
            description: If C(true), sends owners and groups without a domain
                         name.
            type: bool
        nfsv4_no_domain_uids:
            description: If C(true), sends UIDs and GIDs without a domain name.
            type: bool
        nfsv4_no_names:
            description: If C(true), sends owners and groups as UIDs and GIDs.
            type: bool
        nfsv4_replace_domain:
            description: If C(true), replaces the owner or group domain with an
                         NFS domain name.
            type: bool
        zone:
            description: Specifies the access zone in which the NFS zone
                         settings apply.
            type: str
    sample: {
        "nfsv4_allow_numeric_ids": false,
        "nfsv4_domain": "",
        "nfsv4_no_domain": false,
        "nfsv4_no_domain_uids": false,
        "nfsv4_no_names": false,
        "nfsv4_replace_domain": false,
        "zone": "System"
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('nfs_zone_settings')


class NFSZoneSettings:
    """Class with NFS zone settings operations"""

    def __init__(self):
        """ Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(self.get_nfs_zone_settings_parameters())
        # Initialize the ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=True
        )
        # Result is a dictionary that contains changed status, NFS zone
        # settings details
        self.result = {
            "changed": False,
            "nfs_zone_settings_details": {}
        }

        # Validate the pre-requisites packages for the module
        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        # Initialize the connection to PowerScale
        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        LOG.info('Got python SDK instance for provisioning on PowerScale ')
        check_mode_msg = f'Check mode flag is {self.module.check_mode}'
        LOG.info(check_mode_msg)

        # Initialize the APIs
        self.protocol_api = self.isi_sdk.ProtocolsApi(self.api_client)

    def get_zone_settings_details(self, access_zone):
        """
        Get details of an NFS zone settings for a given access zone.
        :param access_zone: Access zone
        :type access_zone: str
        :return: NFS zone settings details
        :rtype: dict
        """
        msg = f"Getting NFS zone settings details for {access_zone}" \
              f" access zone"
        LOG.info(msg)
        try:
            nfs_settings_obj = self.protocol_api.get_nfs_settings_zone(
                zone=access_zone)
            if nfs_settings_obj:
                zone_settings = nfs_settings_obj.settings.to_dict()

                # Appending the Access zone
                zone_settings["zone"] = access_zone
                msg = f"NFS zone settings details are: {zone_settings}"
                LOG.info(msg)
                return zone_settings

        except Exception as e:
            error_msg = f"Got error {utils.determine_error(e)} while getting" \
                        f" NFS zone settings details for access zone" \
                        f": {access_zone}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def _prepare_zone_settings_modify_object(self, settings_params):
        """
        Prepare the NFS zone settings modify object
        :param settings_params: contains params passed through playbook
        :type settings_params: dict
        :return: NFS zone settings modify object
        :rtype: dict
        """
        try:
            nfs_settings_zone = self.isi_sdk.NfsSettingsZoneSettings(
                nfsv4_allow_numeric_ids=settings_params[
                    "nfsv4_allow_numeric_ids"],
                nfsv4_domain=settings_params["nfsv4_domain"],
                nfsv4_no_domain=settings_params["nfsv4_no_domain"],
                nfsv4_no_domain_uids=settings_params["nfsv4_no_domain_uids"],
                nfsv4_no_names=settings_params["nfsv4_no_names"],
                nfsv4_replace_domain=settings_params["nfsv4_replace_domain"],
                zone=settings_params["access_zone"])
            return nfs_settings_zone
        except Exception as e:
            error_msg = f"Got error {utils.determine_error(e)} while " \
                        f"preparing NFS zone settings modify object."
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def modify_zone_settings(self, settings_params):
        """
        Modify the NFS zone settings
        :param settings_params: contains params passed through playbook
        :type settings_params: dict
        :return: True if successful
        :rtype: bool
        """
        zone_settings_obj = self._prepare_zone_settings_modify_object(
            settings_params)
        access_zone = self.module.params["access_zone"]
        try:
            msg = f"Modify NFS zone settings with parameters: " \
                  f"{zone_settings_obj})"
            LOG.info(msg)
            if not self.module.check_mode:
                self.protocol_api.update_nfs_settings_zone(
                    zone_settings_obj, zone=access_zone)
                LOG.info("Successfully modified the NFS zone settings.")
            return True
        except Exception as e:
            error_msg = f"Modify NFS zone settings with in access zone:" \
                        f" {access_zone} failed with error: " \
                        f"{utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def is_settings_modify_required(self, settings_params, settings_details):
        """
        Check if NFS zone settings modification is required
        :param settings_params: contains params passed through playbook
        :param settings_details: contains details of the NFS zone settings
        :return: True if NFS zone settings modification is required
        """
        params = ['nfsv4_allow_numeric_ids', 'nfsv4_domain',
                  'nfsv4_no_domain', 'nfsv4_no_domain_uids', 'nfsv4_no_names',
                  'nfsv4_replace_domain']
        for param in params:
            if settings_params[param] is not None \
                    and settings_params[param] != settings_details[param]:
                return True
        return False

    def validate_zone_params(self):
        """Validate path and access zone parameters"""

        if utils.is_param_empty_spaces(self.module.params["access_zone"]):
            err_msg = "Invalid access zone provided. Provide valid access" \
                      " zone."
            self.module.fail_json(msg=err_msg)

    def get_nfs_zone_settings_parameters(self):
        return dict(
            access_zone=dict(default='System'),
            nfsv4_allow_numeric_ids=dict(type='bool'),
            nfsv4_domain=dict(type='str'),
            nfsv4_no_domain=dict(type='bool'),
            nfsv4_no_domain_uids=dict(type='bool'),
            nfsv4_no_names=dict(type='bool'),
            nfsv4_replace_domain=dict(type='bool'))


class NFSZoneSettingsExitHandler:
    def handle(self, settings_obj, settings_details):
        settings_obj.result["nfs_zone_settings_details"] = settings_details
        settings_obj.module.exit_json(**settings_obj.result)


class NFSZoneSettingsModifyHandler:
    def handle(self, settings_obj, settings_params, settings_details):
        if settings_details:
            is_modify = settings_obj.is_settings_modify_required(
                settings_params, settings_details)
            if is_modify:
                changed = settings_obj.modify_zone_settings(settings_params)
                settings_details = settings_obj.get_zone_settings_details(
                    access_zone=settings_params["access_zone"])
                settings_obj.result["changed"] = changed
                settings_obj.result["nfs_zone_settings_details"] = \
                    settings_details

        NFSZoneSettingsExitHandler().handle(settings_obj, settings_details)


class NFSZoneSettingsHandler:
    def handle(self, settings_obj, settings_params):
        settings_obj.validate_zone_params()
        settings_details = settings_obj.get_zone_settings_details(
            access_zone=settings_params["access_zone"])

        NFSZoneSettingsModifyHandler().handle(
            settings_obj=settings_obj, settings_params=settings_params,
            settings_details=settings_details)


def main():
    """ Create PowerScale NFS zone settings object and perform action on it
        based on user input from playbook."""
    obj = NFSZoneSettings()
    NFSZoneSettingsHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
