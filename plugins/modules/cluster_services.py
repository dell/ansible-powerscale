#!/usr/bin/python
# Copyright: (c) 2026, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing cluster services on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: cluster_services
version_added: '4.0.0'
short_description: Manage cluster services on a PowerScale Storage System
description:
- Managing cluster services on a PowerScale system includes enabling or disabling
  NFS, SMB, S3, HDFS, and Antivirus services, and retrieving the current status
  of all cluster services.
- When no service parameters are provided, the module retrieves the current state
  of all services (facts gathering).

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Saksham Nautiyal (@Saksham-Nautiyal) <ansible.team@dell.com>

options:
  nfs_service:
    description:
    - Specifies if the NFS service should be enabled or disabled.
    - When set to C(true), the NFS service is enabled.
    - When set to C(false), the NFS service is disabled.
    type: bool
  smb_service:
    description:
    - Specifies if the SMB service should be enabled or disabled.
    - When set to C(true), the SMB service is enabled.
    - When set to C(false), the SMB service is disabled.
    type: bool
  s3_service:
    description:
    - Specifies if the S3 service should be enabled or disabled.
    - When set to C(true), the S3 service is enabled.
    - When set to C(false), the S3 service is disabled.
    type: bool
  hdfs_service:
    description:
    - Specifies if the HDFS service should be enabled or disabled.
    - When set to C(true), the HDFS service is enabled.
    - When set to C(false), the HDFS service is disabled.
    type: bool
  antivirus_service:
    description:
    - Specifies if the Antivirus service should be enabled or disabled.
    - When set to C(true), the Antivirus service is enabled.
    - When set to C(false), the Antivirus service is disabled.
    type: bool
notes:
- The I(check_mode) is supported.
- The I(diff_mode) is supported.
'''

EXAMPLES = r'''
- name: Get cluster services status (facts gathering)
  dellemc.powerscale.cluster_services:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"  # example
    verify_ssl: "{{ verify_ssl }}"

- name: Enable NFS and S3 services, disable SMB service
  dellemc.powerscale.cluster_services:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"  # example
    verify_ssl: "{{ verify_ssl }}"
    nfs_service: true
    s3_service: true
    smb_service: false

- name: Enable Antivirus service
  dellemc.powerscale.cluster_services:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"  # example
    verify_ssl: "{{ verify_ssl }}"
    antivirus_service: true
'''

RETURN = r'''
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
cluster_services_details:
    description: The cluster services details.
    type: dict
    returned: always
    contains:
        nfs_service:
            description: Whether the NFS service is enabled.
            type: bool
        smb_service:
            description: Whether the SMB service is enabled.
            type: bool
        s3_service:
            description: Whether the S3 service is enabled.
            type: bool
        hdfs_service:
            description: Whether the HDFS service is enabled.
            type: bool
        antivirus_service:
            description: Whether the Antivirus service is enabled.
            type: bool
    sample: {
        "nfs_service": true,
        "smb_service": true,
        "s3_service": false,
        "hdfs_service": false,
        "antivirus_service": true
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('cluster_services')

SERVICE_KEYS = ['nfs_service', 'smb_service', 's3_service', 'hdfs_service', 'antivirus_service']


class ClusterServices:
    """Class with cluster services operations for PowerScale."""

    SERVICE_MAP = {
        'nfs_service': {
            'get': 'get_nfs_settings_global',
            'update': 'update_nfs_settings_global',
            'update_kwarg': 'nfs_settings_global',
            'api_attr': 'protocol_api',
            'label': 'NFS',
        },
        'smb_service': {
            'get': 'get_smb_settings_global',
            'update': 'update_smb_settings_global',
            'update_kwarg': 'smb_settings_global',
            'api_attr': 'protocol_api',
            'label': 'SMB',
        },
        's3_service': {
            'get': 'get_s3_settings_global',
            'update': 'update_s3_settings_global',
            'update_kwarg': 's3_settings_global',
            'api_attr': 'protocol_api',
            'label': 'S3',
        },
        'hdfs_service': {
            'get': 'get_hdfs_settings',
            'update': 'update_hdfs_settings',
            'update_kwarg': 'hdfs_settings',
            'api_attr': 'protocol_api',
            'label': 'HDFS',
        },
        'antivirus_service': {
            'get': 'get_antivirus_settings',
            'update': 'update_antivirus_settings',
            'update_kwarg': 'antivirus_settings',
            'api_attr': 'antivirus_api',
            'label': 'Antivirus',
        },
    }

    def __init__(self):
        """Define all parameters required by this module."""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(self.get_cluster_services_parameters())
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=True
        )
        self.result = {
            "changed": False,
            "cluster_services_details": {}
        }

        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        LOG.info('Got python SDK instance for provisioning on PowerScale ')
        check_mode_msg = f'Check mode flag is {self.module.check_mode}'
        LOG.info(check_mode_msg)

        self.protocol_api = self.isi_sdk.ProtocolsApi(self.api_client)
        self.antivirus_api = self.isi_sdk.AntivirusApi(self.api_client)

    def validate_input(self):
        """Validate input parameters. All params are optional booleans."""
        pass

    def get_service_status(self, service_name):
        """Get single service enabled/disabled status using SERVICE_MAP."""
        svc = self.SERVICE_MAP[service_name]
        api_obj = getattr(self, svc['api_attr'])
        get_method = getattr(api_obj, svc['get'])
        label = svc['label']
        msg = f"Getting {label} service details"
        LOG.info(msg)
        try:
            response = get_method()
            if response:
                raw = response.to_dict() if hasattr(response, 'to_dict') else {}
                settings = raw.get('settings', raw) if isinstance(raw, dict) else raw
                return settings.get('service', None)
        except Exception as e:
            error_msg = f"Got error {utils.determine_error(e)} while " \
                        f"getting {label} service details"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_cluster_services_details(self):
        """Get all service statuses and return combined dict."""
        details = {}
        for service_name in SERVICE_KEYS:
            params = self.module.params
            if params.get(service_name) is not None or \
                    all(params.get(k) is None for k in SERVICE_KEYS):
                status = self.get_service_status(service_name)
                details[service_name] = status
        return details

    def modify_service(self, service_name, enabled):
        """Enable or disable a single service using SERVICE_MAP."""
        svc = self.SERVICE_MAP[service_name]
        api_obj = getattr(self, svc['api_attr'])
        update_method = getattr(api_obj, svc['update'])
        label = svc['label']
        try:
            msg = f"Modify {label} service with service={enabled}"
            LOG.info(msg)
            if not self.module.check_mode:
                kwargs = {svc['update_kwarg']: {'service': enabled}}
                update_method(**kwargs)
                LOG.info("Successfully modified the %s service.", label)
            return True
        except Exception as e:
            error_msg = f"Modify {label} service failed with " \
                        f"error: {utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def is_modify_required(self, params, current_details):
        """Compare current vs desired state and return dict of changes needed."""
        modify_dict = {}
        for key in SERVICE_KEYS:
            if key in params and params[key] is not None and \
                    current_details.get(key) != params[key]:
                modify_dict[key] = params[key]
        return modify_dict

    def get_cluster_services_parameters(self):
        """Return argument_spec for module-specific parameters."""
        return dict(
            nfs_service=dict(type='bool'),
            smb_service=dict(type='bool'),
            s3_service=dict(type='bool'),
            hdfs_service=dict(type='bool'),
            antivirus_service=dict(type='bool')
        )


class ClusterServicesExitHandler:
    """ClusterServicesExitHandler definition."""
    def handle(self, cs_obj, cs_details):
        """Handle."""
        cs_obj.result["cluster_services_details"] = cs_details
        cs_obj.module.exit_json(**cs_obj.result)


class ClusterServicesModifyHandler:
    """ClusterServicesModifyHandler definition."""
    def handle(self, cs_obj, cs_params, cs_details):
        """Handle."""
        modify_params = cs_obj.is_modify_required(cs_params, cs_details)
        if modify_params:
            if hasattr(cs_obj.module, '_diff') and cs_obj.module._diff:
                before = {}
                after = {}
                for key in modify_params:
                    before[key] = cs_details.get(key)
                    after[key] = modify_params[key]
                cs_obj.result['diff'] = {
                    'before': before,
                    'after': after
                }
            for service_name, enabled in modify_params.items():
                cs_obj.modify_service(service_name, enabled)
            cs_details = cs_obj.get_cluster_services_details()
            cs_obj.result["changed"] = True
            cs_obj.result["cluster_services_details"] = cs_details

        ClusterServicesExitHandler().handle(cs_obj, cs_details)


class ClusterServicesHandler:
    """ClusterServicesHandler definition."""
    def handle(self, cs_obj, cs_params):
        """Handle."""
        cs_obj.validate_input()
        cs_details = cs_obj.get_cluster_services_details()
        ClusterServicesModifyHandler().handle(
            cs_obj=cs_obj, cs_params=cs_params,
            cs_details=cs_details)


def main():
    """Perform action on PowerScale cluster services."""
    obj = ClusterServices()
    ClusterServicesHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
