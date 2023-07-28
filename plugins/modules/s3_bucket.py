#!/usr/bin/python
# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Ansible module for managing S3 bucket on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: s3_bucket
version_added: '2.1.0'
short_description:  Manage S3 buckets on a PowerScale Storage System
description:
- Managing S3 buckets on an PowerScale system includes retrieving details of
  S3 bucket, creating S3 bucket, modifying and deleting S3 bucket.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Bhavneet Sharma(@Bhavneet-Sharma) <ansible.team@dell.com>

options:
  path:
    description:
    - Specifies path on which the S3 bucket will be created. It is the absolute
      path for System access zone and it is relative if using non-system access
      zone.
    - For example, if your access zone is 'Ansible' and it has a base path
      '/ifs/ansible' and the path specified is '/user1', then the effective
      path would be '/ifs/ansible/user1'.
    - If your access zone is System, and you have 'directory1' in the access
      zone, the path provided should be '/ifs/directory1'.
    - I(path) is required while creating a S3 bucket.
    - The S3 bucket path can not be modified after creation.
    type: str
  create_path:
    description:
    - Will create the path if does not exist.
    - API default is C(false).
    type: bool
  access_zone:
    description:
    - Specifies the access zone in which the S3 bucket exists.
    - Access zone once set cannot be changed.
    type: str
    default: System
  s3_bucket_name:
    description:
    - Name of the S3 bucket.
    - I(s3_bucket_name) while creating the S3 bucket.
    type: str
    required: true
  owner:
    description:
    - Specifies the owner of the S3 bucket.
    - If I(owner) not passed, then C(root) will be default I(owner) for
      C(System) access zone only.
    - If owner belongs to another provider domain, it should be mentioned along
      with domain name as "DOMAIN_NAME\\username" or DOMAIN_NAME\username.
    type: str
  description:
    description:
    - Specifies the description of the S3 bucket.
    - Pass empty string to remove the I(description).
    type: str
  object_acl_policy:
    description:
    - Set behaviour of object acls for a specified S3 bucket.
    type: str
    choices: ['replace', 'deny']
  acl:
    description:
    - Specifies the permissions and grantees in the S3 bucket.
    type: list
    elements: dict
    suboptions:
      permission:
        description:
        - Specifies the S3 permission being allowed.
        - I(permission) and I(grantee) are required together.
        type: str
        required: true
        choices: ['READ', 'WRITE', 'READ_ACP', 'WRITE_ACP', 'FULL_CONTROL']
      grantee:
        description:
        - Specifies the properties of grantee.
        - I(permission) and I(grantee) are required together.
        - It consists of I(name), I(type), and I(provider_type).
        type: dict
        required: true
        suboptions:
          name:
            description:
            - Specifies the name of grantee (user, group or wellknown).
            type: str
            required: true
          type:
            description:
            - Specifies the type of grantee.
            type: str
            choices: ['user', 'group', 'wellknown']
            default: user
          provider_type:
            description:
            - Specifies the provider type of grantee.
            type: str
            choices: ['local', 'file', 'ldap', 'ads', 'nis']
            default: local
      acl_state:
        description:
        - Specifies if the acls are to be added or removed.
        type: str
        choices: ['present', 'absent']
        default: present
  state:
    description:
    - Defines whether the S3 bucket should exist or not.
    - Value C(present) indicates that the S3 bucket should exist in system.
    - Value C(absent) indicates that the S3 bucket should not exist in system.
    type: str
    choices: ['absent', 'present']
    default: present
notes:
- To delete the S3 bucket, the S3 service must be enabled.
- The I(check_mode) is supported.
'''

EXAMPLES = r'''
- name: Create S3 Bucket
  dellemc.powerscale.s3_bucket:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    s3_bucket_name: "Anisble_S3_bucket"
    path: "/sample_bucket_path"
    access_zone: "sample-zone"
    owner: "sample-user"
    description: "the S3 bucket created."
    object_acl_policy: "replace"
    acl:
      - permission: "READ"
        grantee:
          name: "everyone"
          type: "wellknown"
      - permission: "READ_ACL"
        grantee:
          name: "sample-user"
          type: "user"
          provider_type: "local"
        acl_state: "present"
    state: "present"

- name: Create S3 Bucket
  dellemc.powerscale.s3_bucket:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    s3_bucket_name: "Anisble_S3_bucket_1"
    path: "/ifs/sample_bucket_path_1"
    create_path: true
    access_zone: "System"
    owner: "sample-user"
    acl:
      - permission: "READ"
        grantee:
          name: "everyone"
          type: "wellknown"
    state: "present"

- name: Get S3 Bucket
  dellemc.powerscale.s3_bucket:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    s3_bucket_name: "Anisble_S3_bucket"
    access_zone: "sample-zone"

- name: Modify S3 bucket
  dellemc.powerscale.s3_bucket:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    s3_bucket_name: "Anisble_S3_bucket"
    access_zone: "sample-zone"
    description: "the S3 bucket updated."
    object_acl_policy: "deny"
    acl:
      - permission: "WRITE"
        grantee:
          name: "sample-group"
          type: "group"
          provider_type: "ads"

- name: Remove grantee from S3 bucket
  dellemc.powerscale.s3_bucket:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    s3_bucket_name: "Anisble_S3_bucket"
    access_zone: "sample-zone"
    acl:
      - permission: "WRITE"
        grantee:
          name: "sample-group"
          type: "group"
          provider_type: "ads"
        acl_state: "absent"

- name: Delete S3 Bucket
  dellemc.powerscale.s3_bucket:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    s3_bucket_name: "Anisble_S3_bucket"
    access_zone: "sample-zone"
    state: "absent"
'''

RETURN = r'''
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
S3_bucket_details:
    description: The updated S3 Bucket details.
    type: complex
    returned: always
    contains:
        acl:
            description: Specifies the properties of S3 access controls.
            type: list
            contains:
                grantee:
                    description: Specifies details of grantee.
                    type: dict
                    contains:
                        id:
                            description: ID of the grantee.
                            type: str
                        name:
                            description: Name of the grantee.
                            type: str
                        type:
                            description: Specifies the type of the grantee.
                            type: str
                permission:
                    description: Specifies the S3 permission being allowed.
                    type: str
        description:
            description: Specifies the description of the S3 bucket.
            type: str
        id:
            description: S3 bucket ID.
            type: str
        name:
            description: S3 bucket name.
            type: str
        object_acl_policy:
            description: Set behaviour of object acls for a specified S3
                         bucket.
            type: str
        owner:
            description: Specifies the owner of the S3 bucket.
            type: str
        path:
            description: Path of S3 bucket with in C('/ifs').
            type: str
        zid:
            description: Zone id.
            type: int
        zone:
            description: Access zone name.
            type: str
    sample: {
        "access_zone": "System",
        "acl": [{
            "grantee": {
                "id": "ID",
                "name": "ansible-user",
                "type": "user"
                },
            "permission": "READ"
        }],
        "description": "description",
        "id": "ansible_S3_bucket",
        "name": "ansible_S3_bucket",
        "object_acl_policy": "replace",
        "owner": "ansible-user",
        "path": "/ifs/<sample-path>",
        "zid": 1
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('s3_bucket')


class S3Bucket(object):
    """Class with S3 Bucket operations"""

    def __init__(self):
        """ Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(self.get_s3_bucket_parameters())
        # Initialize the ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=True
        )
        # Result is a dictionary that contains changed status, S3 Bucket
        # details
        self.result = {
            "changed": False,
            "S3_bucket_details": {}
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
        self.zone_summary_api = self.isi_sdk.ZonesSummaryApi(self.api_client)
        self.auth_api = self.isi_sdk.AuthApi(self.api_client)

    def get_zone_base_path(self, access_zone):
        """Returns the base path of the Access Zone."""
        try:
            zone_path = (self.zone_summary_api.
                         get_zones_summary_zone(access_zone)).to_dict()
            return zone_path["summary"]["path"]
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Unable to fetch base path of Access' \
                            f' Zone {access_zone} failed with' \
                            f' error: {str(error_msg)}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_bucket_details(self, bucket_id, access_zone):
        """
        Get details of an S3 Bucket using S3 Bucket ID and access zone
        """
        msg = f"Getting S3 Bucket details {bucket_id} and access zone:" \
              f" {access_zone}"
        LOG.info(msg)
        try:
            s3_bucket_obj = self.protocol_api.get_s3_bucket(
                s3_bucket_id=bucket_id, zone=access_zone)
            if s3_bucket_obj:
                s3_bucket = s3_bucket_obj.buckets[0]
                msg = f"s3 details are: {s3_bucket.to_dict()}"
                LOG.info(msg)
                # Appending the Access zone
                bucket_details = s3_bucket.to_dict()
                bucket_details['access_zone'] = access_zone
                return bucket_details

        except utils.ApiException as e:
            if str(e.status) == "404":
                log_msg = f"S3 bucket {bucket_id} status is {e.status}"
                LOG.info(log_msg)
                return None
            else:
                error_msg = utils.determine_error(error_obj=e)
                error_message = f"Failed to get details of S3 bucket " \
                                f"{bucket_id} with error {str(error_msg)}"
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

        except Exception as e:
            error_msg = f"Got error {utils.determine_error(e)} while getting" \
                        f" S3 Bucket details for ID: {bucket_id} and" \
                        f" access zone: {access_zone}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_wellknown_id(self, name):
        """Get the wellknown account details in PowerScale
        :param name: name of wellknown
        """
        try:
            resp = self.auth_api.get_auth_wellknowns().to_dict()
            for wellknown in resp['wellknowns']:
                if wellknown['name'].lower() == name.lower():
                    return wellknown
            error_message = (f'Wellknown {name} does not exist. '
                             f'Provide valid wellknown.')
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = (f'Failed to get the wellknown id for wellknown '
                             f'{name} due to error {str(error_msg)}.')
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_group_id(self, name, zone, provider):
        """
        get details of the group
        :param name: name of the group
        :param zone: zone in which group exists
        :param provider: provider type of the group
        """
        LOG.info("Getting group details.")
        try:
            resp = self.auth_api.get_auth_group(
                auth_group_id='GROUP:' + name,
                zone=zone, provider=provider).to_dict()
            return resp['groups']
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Failed to get the group id for group {name} ' \
                            f'in zone {zone} and provider {provider} due to' \
                            f' error {str(error_msg)}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_user_id(self, name, zone, provider):
        """
        get details of the user
        :param name: name of the user
        :param zone: zone in which user exists
        :param provider: provider type of the user
        """
        LOG.info("Getting user details.")
        try:
            resp = self.auth_api.get_auth_user(
                auth_user_id='USER:' + name,
                zone=zone, provider=provider).to_dict()
            return resp['users']
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Failed to get the owner id for {name} in zone ' \
                            f'{zone} and provider {provider} due to error ' \
                            f'{error_msg}.'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def update_grantee(self, grantee_dict):
        """
        :param grantee_dict: dict contains grantee
        """
        new_grantee = {}
        if grantee_dict['type'] == "user":
            grantee_details = self.get_user_id(
                name=grantee_dict['name'],
                zone=self.module.params["access_zone"],
                provider=grantee_dict['provider_type'])[0]['uid']
        elif grantee_dict['type'] == "group":
            grantee_details = self.get_group_id(
                name=grantee_dict['name'],
                zone=self.module.params["access_zone"],
                provider=grantee_dict['provider_type'])[0]['gid']
        else:
            grantee_details = self.get_wellknown_id(
                name=grantee_dict['name'])

        grantee_dict['id'] = None
        grantee_dict['name'] = grantee_details['name']
        keys = ['id', 'name', 'type']
        for key in keys:
            new_grantee[key] = grantee_dict[key]
        return new_grantee

    def get_acls(self, pb_acl):
        """prepare the payload for acl"""
        final_acls = []

        for acl in pb_acl:
            grantee = acl['grantee'].copy()
            new_grantee = self.update_grantee(grantee)
            new_acl = acl.copy()
            new_acl['grantee'] = new_grantee
            final_acls.append(new_acl)
        return final_acls

    def _create_s3_params_object(self, name, path):
        """Create params for s3 bucket"""
        acl = []
        if 'acl' in self.module.params and \
                self.module.params['acl'] is not None:
            new_acl = remove_duplicate_acl(self.module.params['acl'])
            for item in new_acl:
                if item['acl_state'] == 'present':
                    temp_acl = item.copy()
                    temp_grantee = item['grantee'].copy()
                    new_grantee = self.update_grantee(temp_grantee)
                    temp_acl['grantee'] = new_grantee
                    acl.append(temp_acl)
                    acl = remove_none_or_acl_state_key_from_acl(
                        acl, remove_acl_state=True)
        try:
            s3_bucket = self.isi_sdk.S3BucketCreateParams(
                path=path,
                description=self.module.params['description'],
                object_acl_policy=self.module.params['object_acl_policy'],
                create_path=self.module.params['create_path'], name=name,
                owner=self.module.params['owner'], acl=acl)
            return s3_bucket
        except Exception as e:
            error_msg = f'Create S3BucketCreateParams object failed with ' \
                        f'error {utils.determine_error(e)}'
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def create_bucket(self, name, path, zone):
        """Create S3 Bucket"""
        s3_bucket = self._create_s3_params_object(name, path)
        try:
            msg = f'Creating S3 Bucket with parameters: {s3_bucket})'
            LOG.info(msg)
            bucket_details = {}
            if not self.module.check_mode:
                response = self.protocol_api.create_s3_bucket(
                    s3_bucket, zone=zone)
                if response:
                    bucket_details = self.get_bucket_details(
                        bucket_id=response.id, access_zone=zone)
                msg = f"Successfully created the S3 bucket with " \
                      f"details {bucket_details}."
                LOG.info(msg)
            return bucket_details

        except Exception as e:
            error_msg = f"Create S3 Bucket with {name} for path: {path} " \
                        f"and access zone: {zone} failed with error" \
                        f": {utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def delete_bucket(self, bucket_id, zone):
        """
        Delete the S3 bucket
        :param bucket_id: ID of the S3 bucket
        :param zone: Access zone of the S3 bucket
        """
        try:
            msg = f"Deleting S3 Bucket with identifier {bucket_id}."
            LOG.info(msg)
            if not self.module.check_mode:
                self.protocol_api.delete_s3_bucket(
                    s3_bucket_id=bucket_id, zone=zone)
                LOG.info("Successfully Deleted the S3 bucket.")
            return self.get_bucket_details(bucket_id=bucket_id,
                                           access_zone=zone)

        except Exception as e:
            error_msg = f"Delete S3 Bucket with {bucket_id} in access zone:" \
                        f" {zone} failed with " \
                        f"error: {utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def _prepare_s3_modify_params_object(self, modify_dict):
        """
        prepare modify params dict object for S3 bucket
        """
        try:
            description = object_acl_policy = None
            acl = []
            if "description" in modify_dict:
                description = modify_dict["description"]
            if "object_acl_policy" in modify_dict:
                object_acl_policy = modify_dict["object_acl_policy"]
            if "acl" in modify_dict:
                acl = modify_dict["acl"]
            s3_bucket = self.isi_sdk.S3Bucket(
                description=description,
                object_acl_policy=object_acl_policy,
                acl=acl)
            return s3_bucket
        except Exception as e:
            error_msg = f'Modify S3Bucket object failed with ' \
                        f'error {utils.determine_error(e)}'
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def modify_bucket(self, bucket_id, bucket_params, modify_dict):
        """
        Modify the S3 bucket based on modify dict
        :param bucket_id: ID of the S3 bucket
        :param bucket_params: contains params passed through playbook
        :param modify_dict: dict containing parameters to be modfied
        """
        s3_bucket = self._prepare_s3_modify_params_object(modify_dict)
        zone = bucket_params['access_zone']
        try:
            msg = f'Modify S3 Bucket with parameters: {s3_bucket})'
            LOG.info(msg)
            if not self.module.check_mode:
                self.protocol_api.update_s3_bucket(
                    s3_bucket=s3_bucket, s3_bucket_id=bucket_id, zone=zone)
                LOG.info("Successfully modified the S3 bucket.")
            return True

        except Exception as e:
            error_msg = f"Modify S3 Bucket with {bucket_id} in access " \
                        f"zone: {zone} failed with " \
                        f"error: {utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def set_add_acls(self, ply_acl, bucket_acl):
        """find acls for add operation"""
        add_acl_list = []
        for acl_item in ply_acl:
            if acl_item['acl_state'] == "present":
                temp_dict = acl_item.copy()
                del temp_dict["acl_state"]
                if temp_dict not in bucket_acl:
                    add_acl_list.append(temp_dict)
        return add_acl_list

    def create_acl_list(self, pb_acl, buck_acl):
        """prepare the list of acls
        :param pb_acl: acls given in the playbook
        :param buck_acl: acls present in the S3 bucket
        """
        acls_all = list()
        acls_all.extend(buck_acl)

        # preparing list for add acls operation
        add_acls = self.set_add_acls(ply_acl=pb_acl, bucket_acl=buck_acl)

        if add_acls:
            acls_all.extend(add_acls)
            acls_all = remove_duplicate_acl(acls_all)

        # preparing list for remove acls operation
        remove_acls = []
        for item1 in pb_acl:
            if item1["acl_state"] == "absent":
                temp_dict1 = item1.copy()
                del temp_dict1["acl_state"]
                if temp_dict1 in acls_all:
                    remove_acls.append(temp_dict1)

        final_acl = []
        for item2 in acls_all:
            if item2 not in remove_acls:
                final_acl.append(item2)

        if final_acl != buck_acl:
            msg = f"Final_acls for S3 bucket are : {final_acl}"
            LOG.info(msg)
            return True, final_acl
        return False, None

    def is_acl_modified(self, bucket_params, bucket_details):
        """
        check whether acl modified
        """
        existing_acl = bucket_details["acl"]
        existing_acl = remove_none_or_acl_state_key_from_acl(existing_acl)
        if "acl" in self.module.params and \
                self.module.params["acl"] is not None:
            pb_acl = bucket_params["acl"]
            unique_pb_acl = remove_duplicate_acl(pb_acl)
            unique_pb_acl = self.get_acls(unique_pb_acl)
            unique_pb_acl = remove_none_or_acl_state_key_from_acl(
                unique_pb_acl)
            return self.create_acl_list(unique_pb_acl, existing_acl)
        return False, None

    def is_s3_modify_required(self, bucket_params, bucket_details):
        """
        Check whether modification is required in bucket
        """
        modify_dict = {}
        is_acl_modified, new_acl = self.is_acl_modified(bucket_params,
                                                        bucket_details)
        keys = ["description", "object_acl_policy"]
        for key in keys:
            if bucket_params[key] is not None and \
                    bucket_params[key] != bucket_details[key]:
                modify_dict[key] = bucket_params[key]
        if is_acl_modified:
            modify_dict["acl"] = new_acl

        return modify_dict

    def determine_path(self):
        """fetch the effective path for access zone"""
        path = self.module.params['path']
        access_zone = self.module.params["access_zone"]

        if access_zone is not None and access_zone.lower() == "system":
            if path is not None and not path.startswith('/'):
                err_msg = (f"Invalid path {path}, Path must start "
                           f"with '/'")
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
        elif access_zone is not None and access_zone.lower() != "system":
            if path is not None and not path.startswith('/'):
                path = f"/{path}"
            path = self.get_zone_base_path(access_zone) + path
        return path

    def validate_zone_path_params(self):
        """Validate path and access zone parameters"""
        param_list = ['access_zone', 'path', 's3_bucket_name']
        for param in param_list:
            if self.module.params[param] is not None and \
                    (self.module.params[param].count(" ") > 0 or
                     len(self.module.params[param].strip()) == 0):
                err_msg = f"Invalid {param} provided. Provide valid {param}."
                self.module.fail_json(msg=err_msg)

    def validate_create_bucket(self, bucket_params):
        """validate the input parameter for create the S3 bucket"""
        if bucket_params["path"] is None:
            err_msg = "Path is required to create the S3 bucket"
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)

    def validate_path_owner_in_modify(self, buck_params, buck_details):
        """Validate whether user trying to modify path and owner"""
        path = None
        if "path" in buck_params and buck_params["path"] is not None:
            path = self.determine_path()
            if path.endswith("/"):
                path = path[0:len(path) - 1]

        msg = "{0} of the S3 bucket is not modifiable after creation."
        if "owner" in buck_params and buck_params["owner"] is not None and \
                buck_params["owner"] != buck_details["owner"]:
            err_msg = msg.format("owner")
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)
        elif "path" in buck_params and buck_params["path"] is not None and \
                path != buck_details["path"]:
            err_msg = msg.format("path")
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)

    def get_s3_bucket_parameters(self):
        return dict(
            path=dict(type='str'), s3_bucket_name=dict(required=True),
            access_zone=dict(type='str', default='System'),
            description=dict(), create_path=dict(type='bool'),
            owner=dict(type='str'),
            object_acl_policy=dict(type='str', choices=['replace', 'deny']),
            acl=dict(
                type='list', elements='dict', options=dict(
                    grantee=dict(
                        type='dict', required=True, options=dict(
                            name=dict(type='str', required=True),
                            type=dict(
                                type='str',
                                choices=['user', 'group', 'wellknown'],
                                default='user'),
                            provider_type=dict(
                                type='str',
                                choices=['local', 'file', 'ldap', 'ads',
                                         'nis'],
                                default='local'))),
                    permission=dict(
                        type='str', required=True,
                        choices=['READ', 'WRITE', 'READ_ACP', 'WRITE_ACP',
                                 'FULL_CONTROL']),
                    acl_state=dict(type='str', choices=['present', 'absent'],
                                   default='present'))),
            state=dict(type='str', choices=['present', 'absent'],
                       default='present')
        )


def remove_duplicate_acl(acl_list):
    """Remove the duplicate items form the acl list"""
    unique_acl = []
    for acl in acl_list:
        if acl not in unique_acl:
            unique_acl.append(acl)
    return unique_acl


def remove_none_or_acl_state_key_from_acl(acls, remove_acl_state=False):
    """
    Remove the id if it is none value
    """
    updated_acl = []
    for acl in acls:
        grantee = acl['grantee'].copy()
        if 'id' in grantee and grantee['id'] is None:
            del grantee['id']
        new_acl = acl.copy()
        new_acl['grantee'] = grantee
        if remove_acl_state and "acl_state" in new_acl and \
                new_acl["acl_state"] in ["present", "absent"]:
            del new_acl["acl_state"]
        updated_acl.append(new_acl)
    return updated_acl


class S3BucketExitHandler():
    def handle(self, bucket_obj, bucket_details):
        bucket_obj.result["S3_bucket_details"] = bucket_details
        bucket_obj.module.exit_json(**bucket_obj.result)


class S3BucketDeleteHandler():
    def handle(self, bucket_obj, bucket_params, bucket_details):
        if bucket_params["state"] == "absent" and bucket_details:
            bucket_details = bucket_obj.delete_bucket(
                bucket_id=bucket_details["id"],
                zone=bucket_params["access_zone"])
            bucket_obj.result["changed"] = True
        S3BucketExitHandler().handle(bucket_obj, bucket_details)


class S3BucketModifyHandler():
    def handle(self, bucket_obj, bucket_params, bucket_details):
        if bucket_params["state"] == "present" and bucket_details:
            bucket_obj.validate_path_owner_in_modify(
                bucket_params, bucket_details)
            modify_params = bucket_obj.is_s3_modify_required(bucket_params,
                                                             bucket_details)
            if modify_params:
                changed = bucket_obj.modify_bucket(
                    bucket_details["id"], bucket_details, modify_params)
                bucket_details = bucket_obj.get_bucket_details(
                    bucket_details["id"],
                    access_zone=bucket_params['access_zone'])
                bucket_obj.result["changed"] = changed
                bucket_obj.result["S3_bucket_details"] = bucket_details

        S3BucketDeleteHandler().handle(
            bucket_obj, bucket_params, bucket_details)


class S3BucketCreateHandler():
    def handle(self, bucket_obj, bucket_params, bucket_details):
        if bucket_params["state"] == "present" and bucket_details is None:
            path = bucket_obj.determine_path()
            bucket_obj.validate_create_bucket(bucket_params)
            bucket_details = bucket_obj.create_bucket(
                name=bucket_params["s3_bucket_name"], path=path,
                zone=bucket_params['access_zone'])
            bucket_obj.result["changed"] = True

        S3BucketModifyHandler().handle(
            bucket_obj=bucket_obj, bucket_params=bucket_params,
            bucket_details=bucket_details)


class S3BucketHandler():
    def handle(self, bucket_obj, bucket_params):
        bucket_obj.validate_zone_path_params()
        bucket_details = bucket_obj.get_bucket_details(
            bucket_params['s3_bucket_name'],
            access_zone=bucket_params['access_zone'])
        S3BucketCreateHandler().handle(
            bucket_obj=bucket_obj, bucket_params=bucket_params,
            bucket_details=bucket_details)


def main():
    """ Create PowerScale S3 Bucket object and perform action on it
        based on user input from playbook."""
    obj = S3Bucket()
    S3BucketHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
