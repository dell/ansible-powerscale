#!/usr/bin/python
# Copyright: (c) 2020, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

""" Ansible module for managing Smart Quota on PowerScale"""
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: smartquota

version_added: '1.2.0'

short_description: Manage Smart Quotas on PowerScale

description:
- Manages Smart Quotas on a PowerScale storage system. This includes getting details,
  modifying, creating and deleting Smart Quotas.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- P Srinivas Rao (@srinivas-rao5) <ansible.team@dell.com>

options:
  path:
    description:
    - The path on which the quota will be imposed.
    - For system access zone, the path is absolute. For all other access
      zones, the path is a relative path from the base of the access zone.
    type: str
    required: true
  quota_type:
    description:
    - The type of quota which will be imposed on the path.
    type: str
    required: true
    choices: ['user', 'group', 'directory', 'default-user', 'default-group']
  user_name:
    description:
    - The name of the user account for which
      quota operations will be performed.
    type: str
  group_name:
    description:
    - The name of the group for which quota operations will be performed.
    type: str
  access_zone:
    description:
    - This option mentions the zone in which the user/group exists.
    - For a non-system access zone, the path relative to the non-system Access Zone's
      base directory has to be given.
    - For a system access zone, the absolute path has to be given.
    type: str
    default: 'system'
  provider_type:
    description:
    - This option defines the type which is used to
      authenticate the user/group.
    - If the I(provider_type) is 'ads' then the domain name of the Active
      Directory Server has to be mentioned in the I(user_name).
      The format for the I(user_name) should be 'DOMAIN_NAME\user_name'
      or "DOMAIN_NAME\\user_name".
    - This option acts as a filter for all operations except creation.
    type: str
    default: 'local'
    choices: [ 'local', 'file', 'ldap', 'ads', 'nis']
  quota:
    description:
    - Specifies Smart Quota parameters.
    type: dict
    suboptions:
      include_snapshots:
        description:
        - Whether to include the snapshots in the quota or not.
        type: bool
        default: False
      include_overheads:
        description:
        - Whether to include the data protection overheads
          in the quota or not.
        - If not passed during quota creation then quota will be created
          excluding the overheads.
        - This parameter is supported for SDK 8.1.1
        type: bool
      thresholds_on:
        description:
        - For SDK 9.0.0 the parameter I(include_overheads) is deprecated and
          I(thresholds_on) is used.
        type: str
        choices: [ 'app_logical_size', 'fs_logical_size', 'physical_size']
      advisory_limit_size:
        description:
        - The threshold value after which the advisory notification
          will be sent.
        type: float
      soft_limit_size:
        description:
        - Threshold value after which the soft limit exceeded notification
          will be sent and the I(soft_grace) period will start.
        - Write access will be restricted after the grace period expires.
        - Both I(soft_grace_period) and I(soft_limit_size) are required to modify
          soft threshold for the quota.
        type: float
      soft_grace_period:
        description:
        - Grace Period after the soft limit for quota is exceeded.
        - After the grace period, the write access to the quota will be
          restricted.
        - Both I(soft_grace_period) and I(soft_limit_size) are required to modify
          soft threshold for the quota.
        type: int
      period_unit:
        description:
        - Unit of the time period for I(soft_grace_period).
        - For months the number of days is assumed to be 30 days.
        - This parameter is required only if the I(soft_grace_period),
          is specified.
        type: str
        choices: ['days', 'weeks', 'months']
      hard_limit_size:
        description:
        - Threshold value after which a hard limit exceeded
          notification will be sent.
        - Write access will be restricted after the hard limit is exceeded.
        type: float
      cap_unit:
        description:
        - Unit of storage for the hard, soft and advisory limits.
        - This parameter is required if any of the hard, soft or advisory
          limits is specified.
        type: str
        choices: ['GB', 'TB']
      container:
         description: If C(true), SMB shares using the quota directory see the quota thresholds as share size.
         type: bool
         default: false
  state:
    description:
    - Define whether the Smart Quota should exist or not.
    - C(present) - indicates that the Smart Quota should exist on the system.
    - C(absent) - indicates that the Smart Quota should not exist on the system.
    choices: ['absent', 'present']
    type: str
    required: true

notes:
- To perform any operation, path, quota_type and state are
  mandatory parameters.
- There can be two quotas for each type per directory, one with snapshots
  included and one without snapshots included.
- Once the limits are assigned, then the quota cannot be converted to
  accounting. Only modification to the threshold limits is permitted.
- The I(check_mode) is not supported.
'''
EXAMPLES = r'''
  - name: Create a Quota for a User excluding snapshot
    dellemc.powerscale.smartquota:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      path: "<path>"
      quota_type: "user"
      user_name: "{{user_name}}"
      access_zone: "sample-zone"
      provider_type: "local"
      quota:
        include_overheads: false
        advisory_limit_size: "{{advisory_limit_size}}"
        soft_limit_size: "{{soft_limit_size}}"
        soft_grace_period: "{{soft_grace_period}}"
        period_unit: "{{period_unit}}"
        hard_limit_size: "{{hard_limit_size}}"
        cap_unit: "{{cap_unit}}"
      state: "present"

  - name: Create a Quota for a Directory for accounting includes snapshots and data protection overheads
    dellemc.powerscale.smartquota:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      path: "<path>"
      quota_type: "directory"
      quota:
        include_snapshots: true
        include_overheads: true
      state: "present"

  - name: Create default-user Quota for a Directory with snaps and overheads
    dellemc.powerscale.smartquota:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      path: "<path>"
      quota_type: "default-user"
      quota:
        include_snapshots: true
        include_overheads: true
      state: "present"

  - name: Get a Quota Details for a Group
    dellemc.powerscale.smartquota:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      path: "<path>"
      quota_type: "group"
      group_name: "{{user_name}}"
      access_zone: "sample-zone"
      provider_type: "local"
      quota:
        include_snapshots: true
      state: "present"

  - name: Update Quota for a User
    dellemc.powerscale.smartquota:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      path: "<path>"
      quota_type: "user"
      user_name: "{{user_name}}"
      access_zone: "sample-zone"
      provider_type: "local"
      quota:
        include_snapshots: true
        include_overheads: true
        advisory_limit_size: "{{new_advisory_limit_size}}"
        hard_limit_size: "{{new_hard_limit_size}}"
        cap_unit: "{{cap_unit}}"
      state: "present"

  - name: Modify Soft Limit and Grace period of default-user Quota
    dellemc.powerscale.smartquota:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      path: "<path>"
      quota_type: "default-user"
      access_zone: "sample-zone"
      quota:
        include_snapshots: true
        include_overheads: true
        soft_limit_size: "{{soft_limit_size}}"
        cap_unit: "{{cap_unit}}"
        soft_grace_period: "{{soft_grace_period}}"
        period_unit: "{{period_unit}}"
      state: "present"

  - name: Delete a Quota for a Directory
    dellemc.powerscale.smartquota:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      path: "<path>"
      quota_type: "directory"
      quota:
        include_snapshots: true
      state: "absent"

  - name: Delete Quota for a default-group
    dellemc.powerscale.smartquota:
      onefs_host: "{{onefs_host}}"
      verify_ssl: "{{verify_ssl}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      path: "<path>"
      quota_type: "default-group"
      quota:
        include_snapshots: true
      state: "absent"
'''
RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
    sample: true

quota_details:
    description: The quota details.
    type: complex
    returned: When Quota exists.
    contains:
        id:
            description: The ID of the Quota.
            type: str
            sample: "2nQKAAEAAAAAAAAAAAAAQIMCAAAAAAAA"
        enforced:
            description: Whether the limits are enforced on Quota or not.
            type: bool
            sample: true
        container:
            description: If C(true), SMB shares using the quota directory see the quota thresholds as share size.
            type: bool
            sample: true
        thresholds:
            description: Includes information about all the limits imposed on quota.
                         The limits are mentioned in bytes and I(soft_grace) is in seconds.
            type: dict
            sample: {
                    "advisory": 3221225472,
                    "advisory(GB)": "3.0",
                    "advisory_exceeded": false,
                    "advisory_last_exceeded": 0,
                    "hard": 6442450944,
                    "hard(GB)": "6.0",
                    "hard_exceeded": false,
                    "hard_last_exceeded": 0,
                    "soft": 5368709120,
                    "soft(GB)": "5.0",
                    "soft_exceeded": false,
                    "soft_grace": 3024000,
                    "soft_last_exceeded": 0
                }
        type:
            description: The type of Quota.
            type: str
            sample: "directory"
        usage:
            description: The Quota usage.
            type: dict
            sample: {
                    "inodes": 1,
                    "logical": 0,
                    "physical": 2048
                }
    sample:
      {
        "container": true,
        "description": "",
        "efficiency_ratio": null,
        "enforced": false,
        "id": "iddd",
        "include_snapshots": false,
        "labels": "",
        "linked": false,
        "notifications": "default",
        "path": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
        "persona": {
          "id": "UID:9355",
          "name": "test_user_12",
          "type": "user"
        },
        "ready": true,
        "reduction_ratio": null,
        "thresholds": {
          "advisory": null,
          "advisory_exceeded": false,
          "advisory_last_exceeded": null,
          "hard": null,
          "hard_exceeded": false,
          "hard_last_exceeded": null,
          "percent_advisory": null,
          "percent_soft": null,
          "soft": null,
          "soft_exceeded": false,
          "soft_grace": null,
          "soft_last_exceeded": null
        },
        "thresholds_on": "applogicalsize",
        "type": "user",
        "usage": {
          "applogical": 0,
          "applogical_ready": true,
          "fslogical": 0,
          "fslogical_ready": true,
          "fsphysical": 0,
          "fsphysical_ready": false,
          "inodes": 0,
          "inodes_ready": true,
          "physical": 0,
          "physical_data": 0,
          "physical_data_ready": true,
          "physical_protection": 0,
          "physical_protection_ready": true,
          "physical_ready": true,
          "shadow_refs": 0,
          "shadow_refs_ready": true
        }
      }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
import re
import copy

LOG = utils.get_logger('smartquota')


class SmartQuota(object):
    """Class with Smart Quota operations"""

    def __init__(self):
        """ Define all parameters required by this module"""

        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_smartquota_parameters())
        mut_ex_args = [['group_name', 'user_name']]
        req_if_args = [
            ['quota_type', 'user', ['user_name']],
            ['quota_type', 'group', ['group_name']]
        ]

        # initialize the ansible module
        self.module = AnsibleModule(argument_spec=self.module_params,
                                    supports_check_mode=False,
                                    mutually_exclusive=mut_ex_args,
                                    required_if=req_if_args)

        # result is a dictionary that contains changed status and
        # smart quota details
        self.result = {"changed": False}
        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.auth_api_instance = utils.isi_sdk.AuthApi(self.api_client)
        self.zone_summary_api = utils.isi_sdk.ZonesSummaryApi(
            self.api_client)
        self.quota_api_instance = utils.isi_sdk.QuotaApi(self.api_client)

        LOG.info('Got the isi_sdk instance for Smart Quota Operations')

    def get_zone_base_path(self, access_zone):
        """
        Get the base path of the Access Zone.
        :param access_zone: Name of the Access Zone.
        :return: Base Path of the Access Zone.
        """
        try:
            zone_path = (self.zone_summary_api.
                         get_zones_summary_zone(access_zone)).to_dict()
            zone_base_path = zone_path['summary']['path']
            LOG.debug("Successfully got zone_base_path for %s is %s",
                      access_zone, zone_base_path)
            return zone_base_path
        except Exception as e:
            error_message = 'Unable to fetch base path of Access Zone %s' \
                            ',failed with error: %s' \
                            % (access_zone, determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def create(self, path, quota_type, zone,
               quota_dict, persona=None):
        """
        Create a Smart Quota.
        :param path: The path for which quota has to be created.
        :param quota_type: The type of the quota.
        :param zone: The zone in which user/group exists.
        :param quota_dict: Threshold limits dictionary containing all limits.
        :param persona: User/Group object.
        :return: Quota Id.
        """
        if quota_dict:
            threshold_obj = utils.isi_sdk.QuotaQuotaThresholds(
                quota_dict['advisory'], hard=quota_dict['hard'],
                soft=quota_dict['soft'],
                soft_grace=quota_dict['soft_grace'])
        else:
            threshold_obj = utils.isi_sdk.QuotaQuotaThresholds()

        enforced = False
        if quota_dict and (quota_dict['hard'] or quota_dict['soft']
                           or quota_dict['advisory']):
            enforced = True

        # if not passed during creation of Quota
        # Set include_snapshots as False
        if quota_dict is None or quota_dict['include_snapshots'] is None:
            include_snapshots = False
        else:
            include_snapshots = quota_dict['include_snapshots']

        container = False
        if quota_dict and 'container' in quota_dict and quota_dict['container'] is not None \
                and quota_type == "directory":
            container = quota_dict['container']

        quota_create_params = {
            'include_snapshots': include_snapshots, 'path': path,
            'enforced': enforced,
            'persona': persona,
            'thresholds': threshold_obj,
            'container': container, 'type': quota_type
        }
        if quota_dict is not None and quota_dict["thresholds_on"] is not None:
            quota_create_params["thresholds_on"] = quota_dict["thresholds_on"]
        quota_params_obj = utils.isi_sdk.QuotaQuotaCreateParams(**quota_create_params)
        try:
            api_response = self.quota_api_instance.create_quota_quota(
                quota_quota=quota_params_obj, zone=zone)
            message = "Quota created, %s" % api_response
            LOG.info(message)
            return api_response
        except utils.ApiException as e:
            error_message = "Create quota for %s failed with %s" \
                            % (path, determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def update(self, quota_dict, quota_id, enforced, path):
        """
        Update the attributes for a Smart Quota.
        :param quota_dict: Threshold limits dictionary containing all limits.
        :param quota_id: Id of the quota.
        :param enforced: Boolean value whether to enforce limits or not.
        :param path: The path for which quota has to be updated.
        :return: True if the operation is successful.
        """

        threshold_obj = utils.isi_sdk.QuotaQuotaThresholds(
            advisory=quota_dict['advisory'], hard=quota_dict['hard'],
            soft=quota_dict['soft'], soft_grace=quota_dict['soft_grace'])

        get_quota_params = {'enforced': enforced,
                            'thresholds_on': quota_dict["thresholds_on"],
                            'thresholds': threshold_obj}
        quota_params_obj = utils.isi_sdk.QuotaQuota(**get_quota_params)
        try:
            self.quota_api_instance.update_quota_quota(
                quota_quota=quota_params_obj, quota_quota_id=quota_id)
            msg = "Quota Updated successfully for path %s" % path
            LOG.debug(msg)
            return True
        except utils.ApiException as e:
            error_message = "Update quota for path %s failed with %s" \
                            % (path, determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_sid(self, name, type, provider, zone):
        """
        Get the User/Group Account's SID in PowerScale.
        :param name: Name of the resource.
        :param type: Whether resource is of User or Group.
        :param provider: Authentication type for the resource.
        :param zone: Access Zone in which resource exists.
        :return: sid of the resource.
        """
        try:
            if type == 'user':
                api_response = self.auth_api_instance.get_auth_user(
                    auth_user_id='USER:' + name,
                    zone=zone, provider=provider)
                msg = "SID of the user: %s" % api_response.users[0].sid.id
                LOG.info(msg)
                return api_response.users[0].sid.id

            elif type == 'group':
                api_response = self.auth_api_instance.get_auth_group(
                    auth_group_id='GROUP:' + name, zone=zone,
                    provider=provider)
                msg = "SID of the group: %s" % api_response.groups[0].sid.id
                LOG.info(msg)
                return api_response.groups[0].sid.id

        except Exception as e:
            error_message = "Failed to get {0} details for " \
                            "AccessZone:{1} and Provider:{2} " \
                            "with error {3}" \
                .format(name, zone, provider, determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_quota_details(self, include_snapshots,
                          zone, type, path, persona=None):
        """
         Get the details of the Smart Quota.
        :param include_snapshots: Whether to include snapshots or not.
        :param zone: Access Zone in which User/Group/Quota exists.
        :param type: The type of the quota.
        :param path: The path for which quota exists.
        :param persona: User/Group object.
        :return: if exists returns details of the Quota and Quota's Id,
         else returns None.
        """
        try:
            if type != 'user' and type != 'group':
                api_response = self.quota_api_instance.list_quota_quotas(
                    include_snapshots=include_snapshots, zone=zone,
                    type=type, path=path)
            else:
                api_response = self.quota_api_instance.list_quota_quotas(
                    include_snapshots=include_snapshots, zone=zone,
                    persona=persona, type=type, path=path)
            if api_response.quotas:
                quota_id = api_response.quotas[0].id
                quota = api_response.quotas[0].to_dict()
                msg = "Get Quota Details Successful. Quota Details: %s"\
                      % quota
                LOG.debug(msg)
                return quota, quota_id
            LOG.info("Get Quota Details Failed. Quota does not exist.")
            return None, None
        except Exception as e:
            error_message = "Get Quota Details for %s failed with %s" \
                            % (path, determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete(self, quota_id, path):
        """
        Delete the Smart Quota.
        :param quota_id: The Id of the Quota.
        :param path: The path for which quota exists.
        :return: True, if the delete operation is successful.
        """
        try:
            self.quota_api_instance.delete_quota_quota(quota_id)
            msg = "Quota Deleted Successfully for Path %s" % path
            LOG.debug(msg)
            return True
        except Exception as e:
            error_message = "Delete quota for %s failed with %s" \
                            % (path, determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def convert_quota_thresholds(self, quota):
        """
        Convert the threshold limits to appropriate units.
        :param quota: Threshold limits dictionary containing all limits.
        :return: Converted Threshold limits dictionary.
        """
        available_quota_args = quota.keys()

        # convert soft_grace_period
        if 'soft_grace_period' in available_quota_args and quota['soft_grace_period'] is not None:
            if quota['soft_grace_period'] <= 0:
                self.module.fail_json(msg="soft_grace_period should be greater than 0")
            quota['soft_grace_period'] = period_to_seconds(quota['soft_grace_period'], quota['period_unit'])

        # convert size limits
        limit_params = ['advisory_limit_size', 'soft_limit_size',
                        'hard_limit_size']
        for limit in available_quota_args:
            if limit in limit_params and quota[limit] is not None:
                limit_size = round(utils.get_size_bytes(
                    quota[limit], quota['cap_unit']))
                if limit_size < 1073741824:
                    self.module.fail_json(msg="%s should be greater than or equal to 1GB" % limit)
                quota[limit] = limit_size

        quota['advisory'] = quota.pop('advisory_limit_size')
        quota['soft'] = quota.pop('soft_limit_size')
        quota['hard'] = quota.pop('hard_limit_size')
        quota['soft_grace'] = quota.pop('soft_grace_period')
        return quota

    def get_user_group_sid(self):
        """Getting sid based on quota_type"""
        quota_type = self.module.params['quota_type']
        user_name = self.module.params['user_name']
        group_name = self.module.params['group_name']
        provider_type = self.module.params['provider_type']
        access_zone = self.module.params['access_zone']
        sid = None
        # Get the sid(security identifier) for User
        if quota_type == "user":
            sid = self.get_sid(user_name, quota_type, provider_type,
                               access_zone)
            return sid
        # Get the sid(security identifier) for Group
        if quota_type == "group":
            sid = self.get_sid(group_name, quota_type, provider_type,
                               access_zone)
            return sid
        return sid

    def effective_path(self, access_zone, path):
        """Get the effective path any access zone"""
        if access_zone is not None and access_zone.lower() == "system":
            if path is not None and not path.startswith('/'):
                err_msg = "Invalid path {0}, Path must start " \
                          "with '/'".format(path)
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
        elif access_zone is not None and access_zone.lower() != "system":
            if path is not None and not path.startswith('/'):
                path = "/{0}".format(path)
            path = self.get_zone_base_path(access_zone) + path
        return path

    def validate_zone_path_params(self):
        """Validate path and access zone parameters"""
        param_list = ['access_zone', 'path']
        for param in param_list:
            if self.module.params[param] is not None and \
                    (self.module.params[param].count(" ") > 0 or
                     len(self.module.params[param].strip()) == 0):
                self.module.fail_json(msg="Invalid %s provided. Provide "
                                          "valid %s." % (param, param))

    def validate_quota_cap_unit(self, quota=None):
        """Checking whether quota limits and cap_unit provided properly"""
        if quota:
            if (quota['advisory'] or quota['soft'] or quota['hard']) and \
                    not quota['cap_unit']:
                self.module.fail_json(msg="advisory/soft/hard limit provided, "
                                          "cap_unit not provided")
            elif quota['cap_unit'] and \
                    not (quota['advisory'] or quota['soft'] or quota['hard']):
                self.module.fail_json(msg="cap_unit provided, advisory/soft/"
                                          "hard limit not provided")

    def perform_module_operation(self):
        """
        Perform different actions on Smart Quota module based on parameters
        chosen in playbook
        """
        quota_type = self.module.params['quota_type']
        user_name = self.module.params['user_name']
        group_name = self.module.params['group_name']
        state = self.module.params['state']
        access_zone = self.module.params['access_zone']
        path = self.module.params['path']

        self.validate_zone_path_params()

        quota = copy.deepcopy(self.module.params['quota'])
        if quota:
            self.convert_quota_thresholds(quota)
            include_snapshots = quota.get('include_snapshots')
        else:
            include_snapshots = False
        message = "Quota Dictionary after conversion:  %s" % str(quota)
        LOG.debug(message)

        VALIDATE_THRESHOLD = utils.validate_threshold_overhead_parameter(
            quota, "include_overheads")
        if VALIDATE_THRESHOLD and not VALIDATE_THRESHOLD["param_is_valid"]:
            self.module.fail_json(msg=VALIDATE_THRESHOLD["error_message"])
        # If Access_Zone is System then absolute path is required
        # else relative path is taken
        complete_path = self.effective_path(access_zone=access_zone, path=path)

        changed = False
        # Get the sid(security identifier) for User/Group
        sid = self.get_user_group_sid()

        # Throw error if quota_type is directory/default-user/default-group
        # and parameters for user and group are provided
        if quota_type != 'user' and quota_type != 'group':
            provider_type = None
            if user_name or group_name or provider_type:
                self.module.fail_json(
                    msg="quota_type is not user/group given,"
                        " user_name/group_name/provider_type not required.")

        # Throw error if limits and cap_unit are not passed together
        self.validate_quota_cap_unit(quota=quota)

        # Get the details of the Quota
        quota_details, quota_id = self.get_quota_details(
            include_snapshots=include_snapshots, zone=access_zone,
            type=quota_type, path=complete_path, persona=sid)

        # Create a Quota
        if state == "present" and not quota_details:
            LOG.info("Create a Quota")
            persona_obj = None
            if quota_type == "user" or quota_type == "group":
                persona_obj = \
                    utils.isi_sdk.AuthAccessAccessItemFileGroup(id=sid)
            self.create(complete_path, quota_type, access_zone, quota,
                        persona_obj)
            changed = True

        # Update a Quota
        if state == "present" and quota_details and quota:
            modify_flag = False
            if quota:
                modify_flag = to_modify_quota(
                    quota, quota_details["thresholds"],
                    quota_details["thresholds_on"])
            enforce_limit = False
            if quota_details["enforced"] or quota['advisory'] or \
                    quota['hard'] or quota['soft']:
                enforce_limit = True
            if modify_flag:
                LOG.info("Updating the Quota")
                changed = self.update(quota, quota_id, enforce_limit, path)

        # Delete Quota
        if state == "absent" and quota_details:
            LOG.info("Delete Quota")
            changed = self.delete(quota_id, complete_path)

        quota_details, quota_id = self.get_quota_details(
            include_snapshots, access_zone, quota_type, complete_path, sid)
        if (quota_type == "user" or quota_type == "group") and quota_details:
            quota_details['persona']['type'] = quota_type
            quota_details['persona']['name'] = \
                user_name if user_name else group_name
        quota_details = add_limits_with_unit(quota_details)
        self.result["changed"] = changed
        self.result["quota_details"] = quota_details
        self.module.exit_json(**self.result)


def add_limits_with_unit(quota_details):
    """
    Adds limits to the quota details with units.
    :param quota_details: details of the Quota
    :return: updated quota details if quota details exists else None
    """
    if quota_details is None:
        return None
    limit_list = ['hard', 'soft', 'advisory']
    for limit in limit_list:
        if quota_details['thresholds'][limit]:
            size_with_unit = utils.convert_size_with_unit(
                quota_details['thresholds'][limit]).split(" ")
            new_limit = limit + "(" + size_with_unit[1] + ")"
            quota_details['thresholds'][new_limit] = size_with_unit[0]
    return quota_details


def to_modify_quota(input_quota, array_quota, array_include_overhead):
    """

    :param input_quota: Threshold limits dictionary passed by the user.
    :param array_quota: Threshold limits dictionary got from the PowerScale Array
    :param array_include_overhead: Whether Quota Include Overheads or not.
    :return: True if the quota is to be modified else returns False.
    """
    if input_quota["thresholds_on"] is not None \
            and input_quota["thresholds_on"] != array_include_overhead:
        return True
    for limit in input_quota:
        if limit in array_quota and input_quota[limit] is not None and\
                input_quota[limit] != array_quota[limit]:
            return True
    return False


def determine_error(error_obj):
    """Determine the error message to return"""
    if isinstance(error_obj, utils.ApiException):
        error = re.sub("[\n \"]+", ' ', str(error_obj.body))
    else:
        error = str(error_obj)
    return error


def period_to_seconds(period, period_unit):
    """ Convert the given period to seconds"""
    if period_unit == 'days':
        return period * 86400
    if period_unit == 'weeks':
        return period * 7 * 86400
    if period_unit == 'months':
        return period * 30 * 86400


def make_threshold_obj(advisory, soft, soft_grace, hard):
    """Make threshold object for quota"""
    thresholds = utils.isi_sdk.QuotaQuotaThresholds(
        advisory=advisory, hard=hard, soft=soft, soft_grace=soft_grace)
    return thresholds


def get_smartquota_parameters():
    """This method provides parameters required for the ansible Smart Quota
    module on PowerScale"""
    return dict(
        path=dict(required=True, type='str', no_log=True),
        user_name=dict(type='str'),
        group_name=dict(type='str'),
        access_zone=dict(type='str', default='system'),
        provider_type=dict(type='str', default='local',
                           choices=['local', 'file', 'ldap', 'ads', 'nis']),
        quota_type=dict(required=True, type='str',
                        choices=['user', 'group', 'directory',
                                 'default-user', 'default-group']),
        quota=dict(type='dict',
                   options=dict(include_snapshots=dict(type='bool', default=False),
                                container=dict(type='bool', default=False),
                                include_overheads=dict(type='bool'),
                                thresholds_on=dict(type='str',
                                                   choices=['app_logical_size',
                                                            'fs_logical_size',
                                                            'physical_size']),
                                advisory_limit_size=dict(type='float'),
                                soft_limit_size=dict(type='float'),
                                hard_limit_size=dict(type='float'),
                                soft_grace_period=dict(type='int'),
                                period_unit=dict(type='str',
                                                 choices=['days', 'weeks', 'months']),
                                cap_unit=dict(type='str', choices=['GB', 'TB'])),
                   required_together=[['soft_grace_period', 'period_unit'],
                                      ['soft_grace_period', 'soft_limit_size']]),
        state=dict(required=True, type='str', choices=['present', 'absent'])
    )


def main():
    """ Create PowerScale Smart Quota object and perform actions on it
        based on user input from playbook"""
    obj = SmartQuota()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
