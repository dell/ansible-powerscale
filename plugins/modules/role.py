#!/usr/bin/python
# Copyright: (c) 2024, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Ansible module for managing auth roles on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: role
version_added: '3.1.0'
short_description:  Manage Auth Roles on a PowerScale Storage System
description:
- Managing Auth Roles on an PowerScale system includes retrieving details of
  auth role, creating auth role, modifying and deleting auth role.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Meenakshi Dembi (@dembim) <ansible.team@dell.com>

options:
  access_zone:
    description:
    - Specifies the access zone in which the auth role exists.
    - Access zone once set cannot be changed.
    type: str
    default: System
  role_name:
    description:
    - Name of the Auth Role.
    type: str
    required: true
  new_role_name:
    description:
    - Name of the Auth Role to be used for modify or copy the role.
    type: str
  description:
    description:
    - Specifies the description of the auth role.
    - Pass empty string to remove the I(description).
    type: str
  copy_role:
    description:
    - Copy the role
    - C(true) will copy the role from the I(role_name).
    type: bool
  privileges:
    description:
    - Specifies the privileges granted for this role.
    type: list
    elements: dict
    suboptions:
      permission:
        description:
        - Specifies the permission being allowed for auth role.
        - C(r) indicates read permission.
        - C(w) indicates writepermission.
        - C(x) indicates execute permission.
        - C(-) indicates none permission.
        type: str
        choices: ['r', 'x', 'w', '-']
      name:
        description:
        - Specifies the name of the permission.
        type: str
      state:
        description:
        - Specifies if the permission is to be added or removed.
        type: str
        choices: ['absent', 'present']
        default: present
  members:
    description:
    - Specifies the members of the auth role.
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Specifies the name of the member.
        type: str
      state:
        description:
        - Specifies if the member is to be added or removed.
        type: str
        choices: ['absent', 'present']
        default: present
      provider_type:
        description:
        - Specifies the provider type of the member.
        type: str
        choices: ['local', 'file', 'ldap', 'ads','nis']
        default: local
      type:
        description:
        - Specifies the type of the member.
        type: str
        choices: ['user', 'group', 'wellknown']
  state:
    description:
    - Defines whether the auth role should exist or not.
    - Value C(present) indicates that the auth role should exist in system.
    - Value C(absent) indicates that the auth role should not exist in system.
    type: str
    choices: ['absent', 'present']
    default: present
notes:
- The I(check_mode) is supported.
'''

EXAMPLES = r'''
- name: Create Role
  dellemc.powerscale.role:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    role_name: "Test_Role123sdfsdfsdf"
    description: "Test_Description"
    access_zone: "System"
    privileges:
      - name: "Antivirus"
        permission: "w"
        state: "present"
    members:
      - name: "esa"
        provider_type: "local"
        type: "user"
        state: "present"
      - name: "admin"
        provider_type: "local"
        type: "user"
        state: "present"
    state: "present"

- name: Get Role
  dellemc.powerscale.role:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    role_name: "Test_Role"
    access_zone: "{{access_zone}}"

- name: Modify Role
  dellemc.powerscale.role:
    onefs_host: "{{ onefs_host }}"
    port_no: "{{ port_no }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    role_name: "Test_Role"
    new_role_name: "Test_Role2"
    description: "Test_Description_Modify"
    access_zone: "System"
    privileges:
      - name: "Antivirus"
        permission: "w"
        state: "absent"
    members:
      - name: "User11_Ansible_Test_SMB"
        type: "user"
        state: "absent"
    state: "present"

- name: Delete Role
  dellemc.powerscale.role:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    role_name: "Test_Role"
    access_zone: "{{access_zone}}"
    state: "absent"
'''

RETURN = r'''
changed:
    description: A boolean indicating if the task had to make changes.
    returned: always
    type: bool
    sample: "false"
role_details:
    description: The updated auth role details.
    type: complex
    returned: always
    contains:
        description:
            description: Specifies the description of the auth role.
            type: str
        id:
            description: Auth Role ID.
            type: str
        name:
            description: Auth Role name.
            type: str
        members:
            description: Specifies the members of auth role.
            type: list
            contains:
                id:
                    description: ID of the member.
                    type: str
                name:
                    description: Name of the member.
                    type: str
                type:
                    description: Specifies the type of the member.
                    type: str
        privileges:
            description: Specifies the privileges of auth role.
            type: list
            contains:
                id:
                    description: ID of the privilege.
                    type: str
                name:
                    description: Name of the privilege.
                    type: str
                permission:
                    description: Specifies the permission of the privilege.
                    type: str
    sample: {
        "description": "Test_Description",
        "id": "Test_Role2",
        "members": [
            {
                "id": "UID:1XXX",
                "name": "admin",
                "type": "user"
            },
            {
                "id": "UID:2XXX",
                "name": "esa",
                "type": "user"
            }
        ],
        "name": "Test_Role2",
        "privileges": [
            {
                "id": "ISI_PRIV_ANTIVIRUS",
                "name": "Antivirus",
                "permission": "w"
            }
        ]
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.powerscale_base \
    import PowerScaleBase
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.auth \
    import Auth
import copy

LOG = utils.get_logger('role')


class Role(PowerScaleBase):
    """Class with auth role operations"""

    def __init__(self):
        """ Define all parameters required by this module"""
        ansible_module_params = {
            'argument_spec': self.get_role_parameters(),
            'supports_check_mode': True
        }

        super().__init__(AnsibleModule, ansible_module_params)

        self.result = {
            "changed": False,
            "role_details": {}
        }

    def get_role_details(self, role_name, access_zone):
        """
        Get details of a Role
        """
        msg = f"Getting Role details {role_name}"
        LOG.info(msg)
        try:
            role_obj = self.auth_api.get_auth_role(
                auth_role_id=role_name, zone=access_zone)
            if role_obj:
                role_details = role_obj.roles[0]
                role_details = role_details.to_dict()
                msg = f"Role details are: {role_details}"
                LOG.info(msg)
                return role_details

        except utils.ApiException as e:
            if str(e.status) == "404":
                log_msg = f"Role {role_name} status is {e.status}"
                LOG.info(log_msg)
                return None
            else:
                error_msg = utils.determine_error(error_obj=e)
                error_message = f"Failed to get details of Role " \
                                f"{role_name} with error {str(error_msg)}"
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

        except Exception as e:
            error_msg = f"Got error {utils.determine_error(e)} while getting" \
                        f" Role details: {role_name}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def remove_duplicate_entries(self, entry):
        """Remove duplicate members"""
        new_entry = []
        for item in entry:
            if item not in new_entry:
                new_entry.append(item)
        return new_entry

    def update_member(self, member_dict):
        """
        :param grantee_dict: dict contains grantee
        """
        new_member_dict = {}
        user_details = {}
        if 'provider_type' in member_dict.keys():
            if member_dict['type'] == "user":
                user_details = Auth.get_user_details(
                    self, name=member_dict['name'],
                    zone=self.module.params["access_zone"],
                    provider=member_dict['provider_type'])['users'][0]['uid']
            elif member_dict['type'] == "group":
                user_details = Auth.get_group_details(
                    self, name=member_dict['name'],
                    zone=self.module.params["access_zone"],
                    provider=member_dict['provider_type'])['groups'][0]['gid']
            else:
                user_details = Auth.get_wellknown_details(
                    self, name=member_dict['name'])
        else:
            user_details['id'] = member_dict['id']
            user_details['name'] = member_dict['name']
            user_details['type'] = member_dict['type']
        keys = ['id', 'name', 'type']
        for key in keys:
            new_member_dict[key] = user_details[key]
        return new_member_dict

    def update_privileges(self, privilege_dict):
        """
        :param grantee_dict: dict contains grantee
        """
        new_privilege_dict = {}
        new_privilege_dict_new = {}
        new_privilege_dict = self.auth_api.get_auth_privileges(zone=self.module.params["access_zone"],).to_dict()
        is_name_found = False
        for item in new_privilege_dict['privileges']:
            if item['name'] == privilege_dict['name']:
                is_name_found = True
                id = item['id']

        if is_name_found:
            new_privilege_dict_new['id'] = id
            new_privilege_dict_new['name'] = privilege_dict['name']
            new_privilege_dict_new['permission'] = privilege_dict['permission']
        else:
            err_msg = "Privilege " + privilege_dict['name'] + " is either invalid or cannot be added to role in non-System access zone."
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)

        return new_privilege_dict_new

    def _create_role_params_object(self, role_params_1):
        """Create params for role"""
        role_params = copy.deepcopy(role_params_1)
        if role_params['description'] is None:
            role_params['description'] = ''
        role_input_params = {
            'name': role_params['role_name'],
            'description': role_params['description'],
            'members': [],
            'privileges': []
        }

        if 'members' in role_params and role_params['members'] is not None:
            new_members = self.remove_duplicate_entries(role_params['members'])
            role_input_params['members'] = [
                self.update_member(member)
                for member in new_members if member['state'] == 'present'
            ]
        if 'privileges' in role_params and role_params['privileges'] is not None:
            new_privileges = self.remove_duplicate_entries(role_params['privileges'])
            role_input_params['privileges'] = [
                self.update_privileges(privilege)
                for privilege in new_privileges if privilege['state'] == 'present'
            ]

        return role_input_params

    def create_role(self, role_params):
        """Create Role"""
        role = self._create_role_params_object(role_params)
        try:
            msg = f'Creating Role with parameters: {role})'
            LOG.info(msg)
            role_details = {}
            if not self.module.check_mode:
                response = self.auth_api.create_auth_role(role, zone=role_params['access_zone'])
                msg = f'reponse from array: {response})'
                LOG.info(msg)
                if response:
                    role_details = self.get_role_details(role_params['role_name'], role_params['access_zone'])
                msg = f"Successfully created auth role with " \
                      f"details {role_details}."
                LOG.info(msg)
                return role_details

        except Exception as e:
            error_msg = f"Create role with failed with error" \
                        f": {utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def delete_role(self, role_name, access_zone):
        """
        Delete the role
        :param role_name: Name of the role
        :param zone: Access zone name
        """
        try:
            msg = f"Deleting Role with identifier {role_name}."
            LOG.info(msg)
            if not self.module.check_mode:
                role_obj = self.auth_api.delete_auth_role(
                    auth_role_id=role_name, zone=access_zone)
                if role_obj:
                    role_details = role_obj.to_dict()
                    msg = f"Role details are: {role_details}"
                    LOG.info(msg)
                    return role_details

                LOG.info("Successfully Deleted the role.")
                return self.get_role_details(role_name, access_zone)

        except Exception as e:
            error_msg = f"Delete role {role_name}failed with " \
                        f"error: {utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def modify_role(self, modify_params, name_existing, role_params):
        """
        Modify the role based on modify dict
        :param modify_params: contains parameter which needs to be modified
        :param role_params: contains params passed through playbook
        """
        try:
            msg = f'Modify role with parameters: {modify_params})'
            LOG.info(msg)
            if role_params['copy_role']:
                name = name_existing
            else:
                name = role_params['role_name']

            if not self.module.check_mode:
                self.auth_api.update_auth_role(modify_params, name, zone=role_params['access_zone'])
                LOG.info("Successfully modified role.")
            return True

        except Exception as e:
            error_msg = f"Modify role with {modify_params} " \
                        f"failed with " \
                        f"error: {utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def modify_member_list(self, role_params, role_details, role_details_draft, modify_role_dict):
        existing_member_names = [member['name'] for member in role_details['members']]
        new_members_to_add = self.get_new_members_to_add(role_params, existing_member_names)
        existing_members_to_remove = [m for m in role_params['members'] if m['state'] == 'absent' and m['name'] in existing_member_names]
        existing_members_to_remove_names = [m['name'] for m in existing_members_to_remove]
        members_to_remove = [m for m in role_details['members'] if m['name'] in existing_members_to_remove_names]

        for item in members_to_remove:
            role_details_draft['members'].remove(item)

        for item in new_members_to_add:
            role_details_draft['members'].append(item)

        if len(new_members_to_add) > 0 or len(existing_members_to_remove) > 0:
            temp = self.remove_duplicate_entries(role_details_draft['members'])
            target_member_list = []
            for item in temp:
                temp1 = self.update_member(item)
                target_member_list.append(temp1)
            modify_role_dict['members'] = target_member_list
        return modify_role_dict

    def get_new_members_to_add(self, role_params, existing_member_names):
        to_remove = [p for p in role_params['members'] if p['state'] == 'absent']
        to_add = [p for p in role_params['members'] if p['state'] == 'present']
        for item in to_remove:
            temp = [p for p in to_add if p['name'] == item['name']]
            if len(temp) > 0:
                to_add.remove(temp[0])
        return [p for p in to_add if p['name'] not in existing_member_names]

    def get_new_privileges_to_add(self, role_params, existing_privileges_names):
        to_remove = [p for p in role_params['privileges'] if p['state'] == 'absent']
        to_add = [p for p in role_params['privileges'] if p['state'] == 'present']
        for item in to_remove:
            temp = [p for p in to_add if p['name'] == item['name']]
            if len(temp) > 0:
                to_add.remove(temp[0])
        return [p for p in to_add if p['name'] not in existing_privileges_names]

    def get_existing_privileges_to_remove(self, role_params, role_details):
        privileges_to_remove = [p for p in role_params['privileges'] if p['state'] == 'absent']
        privileges_to_remove_names = [p['name'] for p in privileges_to_remove]
        return [p for p in role_details['privileges'] if p['name'] in privileges_to_remove_names]

    def modify_privileges_list(self, role_params, role_details, role_details_draft, modify_role_dict):
        existing_privileges_names = [privileges['name'] for privileges in role_details['privileges']]
        new_privileges_to_add = self.get_new_privileges_to_add(role_params, existing_privileges_names)
        for item in new_privileges_to_add:
            role_details_draft['privileges'].append(item)

        existing_privileges = role_details['privileges']
        privileges_to_remove = self.get_existing_privileges_to_remove(role_params, role_details)
        for item in privileges_to_remove:
            role_details_draft['privileges'].remove(item)

        existing_privileges_to_update = []
        if len(existing_privileges) > 0:
            for item in role_params['privileges']:
                privilege = [p for p in existing_privileges if p['name'] == item['name'] and p['permission'] != item['permission']]
                if len(privilege) > 0:
                    item['id'] = privilege[0]['id']
                    existing_privileges_to_update.append(item)
            for item in existing_privileges_to_update:
                item.pop('state')
                permission = [p for p in role_details_draft['privileges'] if p['name'] == item['name']]
                if len(permission) > 0:
                    role_details_draft['privileges'].remove(permission[0])
                    role_details_draft['privileges'].append(item)

        if len(new_privileges_to_add) > 0 or len(privileges_to_remove) > 0 or len(existing_privileges_to_update) > 0:
            temp = self.remove_duplicate_entries(role_details_draft['privileges'])
            target_privileges_list = []
            for item in temp:
                temp1 = self.update_privileges(item)
                target_privileges_list.append(temp1)
            modify_role_dict['privileges'] = target_privileges_list
        return modify_role_dict

    def is_role_modify_required(self, role_params, role_details):
        """
        Check whether modification is required in role
        """
        modify_role_dict = self.check_modify_for_common_params(role_params, role_details)
        role_details_draft = copy.deepcopy(role_details)
        if role_params.get('members'):
            modify_role_dict = self.modify_member_list(role_params, role_details, role_details_draft, modify_role_dict)

        if role_params.get('privileges'):
            modify_role_dict = self.modify_privileges_list(role_params, role_details, role_details_draft, modify_role_dict)

        return modify_role_dict

    def check_modify_for_common_params(self, role_params, role_details):
        """
        Check whether modification is required in common parameters
        """
        modify_role_dict = {}

        role_keys = {
            'new_role_name': (role_details['name'], 'name'),
            'description': (role_details.get('description'), 'description')
        }

        for key, (role_details_value, role_details_key) in role_keys.items():
            if role_params.get(key) and role_params[key] != role_details_value:
                modify_role_dict[role_details_key] = role_params[key]

        return modify_role_dict

    def do_update(self, source, target):
        return source != target

    def validate_create_role_params(self, role_params):
        """validate the input parameter for creating the Role"""
        if utils.is_input_empty(role_params["role_name"]):
            err_msg = "Role name cannot be empty"
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)

        params = ['role_name', 'description', 'new_role_name']

        for item in params:
            if role_params[item]:
                if not utils.is_param_length_valid(role_params.get(item)):
                    err_msg = item + " must be less than or equal to 255 characters."
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)

        for item in params:
            if role_params[item]:
                if not utils.is_param_length_valid(role_params.get(item)):
                    err_msg = item + " must be less than or equal to 255 characters."
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)

        if role_params.get('privileges'):
            existing_privileges_names = set(p['name'] for p in role_params['privileges'])
            duplicate_privileges = [privilege for privilege in role_params['privileges']
                                    if privilege['name'] in existing_privileges_names and
                                    any(privilege['permission'] != p['permission']
                                        for p in role_params['privileges']
                                        if p['name'] == privilege['name'])]
            if duplicate_privileges:
                err_msg = "Duplicate privileges with different permissions are not allowed."
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)

    def create_copy_params(self, new_name, role_params, role_details):
        """Create payload for copying the role"""
        copy_role = {}
        if role_details is not None:
            copy_role = role_details
            copy_role['name'] = new_name

            if role_params['description'] is not None and role_params['description'] != "":
                copy_role['description'] = role_params['description']
            elif role_details['description'] is not None and role_details['description'] != "":
                copy_role['description'] = role_details['description']
            else:
                copy_role['description'] = ''

            if copy_role['id'] is not None:
                copy_role.pop("id")
        return copy_role

    def copy_role(self, new_name, role_params, role_details):
        """Copy the role"""
        copy_role = self.create_copy_params(new_name, role_params, role_details)
        try:
            msg = f'Creating Role with parameters in copy: {copy_role})'
            LOG.info(msg)
            role_details = {}
            if not self.module.check_mode:
                response = self.auth_api.create_auth_role(copy_role, zone=role_params['access_zone'])
                msg = f'reponse from array: {response})'
                LOG.info(msg)
                if response:
                    role_details = self.get_role_details(new_name, role_params['access_zone'])
                msg = f"Successfully created auth role with " \
                    f"details {role_details}."
                LOG.info(msg)
                return role_details
        except Exception as e:
            error_msg = f"Create role with failed with error" \
                        f": {utils.determine_error(e)}"
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def get_role_parameters(self):
        return dict(
            role_name=dict(type='str', required=True),
            new_role_name=dict(type='str'),
            access_zone=dict(type='str', default='System'),
            copy_role=dict(type='bool'),
            description=dict(type='str'),
            privileges=dict(type='list', elements='dict', options=dict(
                            name=dict(type='str'),
                            permission=dict(type='str', choices=['r', 'w', 'x', '-']),
                            state=dict(type='str', choices=['present', 'absent'], default='present'))),
            members=dict(type='list', elements='dict', options=dict(
                         name=dict(type='str'),
                         type=dict(type='str', choices=['user', 'group', 'wellknown']),
                         provider_type=dict(type='str', choices=['local', 'file', 'ldap', 'ads', 'nis'], default='local'),
                         state=dict(type='str', choices=['present', 'absent'], default='present'))),
            state=dict(type='str', choices=['present', 'absent'], default='present')
        )


class RoleExitHandler():
    def handle(self, role_obj, role_details):
        role_obj.result["role_details"] = role_details
        role_obj.module.exit_json(**role_obj.result)


class RoleDeleteHandler():
    def handle(self, role_obj, role_params, role_details):
        if role_params["state"] == "absent" and role_details:
            role_details = role_obj.delete_role(
                role_params['role_name'], role_params['access_zone'])
            role_obj.result["changed"] = True
        RoleExitHandler().handle(role_obj, role_details)


class RoleModifyHandler():
    def handle(self, role_obj, name, role_params, role_details):
        if role_params["state"] == "present" and role_details:
            modify_params = role_obj.is_role_modify_required(role_params,
                                                             role_details)
            if modify_params:
                role_obj.modify_role(modify_params, name, role_params)
                if role_params['copy_role']:
                    role_details = role_obj.get_role_details(name, role_params['access_zone'])
                elif role_params['new_role_name']:
                    role_details = role_obj.get_role_details(role_params['new_role_name'], role_params['access_zone'])
                else:
                    role_details = role_obj.get_role_details(role_params['role_name'], role_params['access_zone'])
                role_obj.result["changed"] = True
                role_obj.result["role_details"] = role_details

        RoleDeleteHandler().handle(role_obj=role_obj, role_params=role_params, role_details=role_details)


class RoleCopyHandler():
    def handle(self, role_obj, role_params, role_details):
        details = role_details
        new_name = role_params['role_name']
        if role_params["state"] == "present" and role_params['copy_role']:
            if role_params['new_role_name'] is None or role_params['new_role_name'] == "":
                new_name = "Copy of " + role_params['role_name']
            else:
                new_name = role_params['new_role_name']
            copyied_role_details = role_obj.get_role_details(new_name, role_params['access_zone'])
            if copyied_role_details is None:
                role_details = role_obj.copy_role(new_name, role_params, role_details)
                role_obj.result["changed"] = True
                role_obj.result["role_details"] = role_details
                details = role_details
            else:
                role_obj.result["role_details"] = copyied_role_details
                details = copyied_role_details

        RoleModifyHandler().handle(role_obj=role_obj, name=new_name, role_params=role_params, role_details=details)


class RoleCreateHandler():
    def handle(self, role_obj, role_params, role_details):
        if role_params["state"] == "present" and role_details is None:
            role_details = role_obj.create_role(role_params)
            role_obj.result["changed"] = True

        RoleCopyHandler().handle(role_obj=role_obj, role_params=role_params, role_details=role_details)


class RoleHandler():
    def handle(self, role_obj, role_params):
        role_obj.validate_create_role_params(role_params)
        role_details = role_obj.get_role_details(role_params['role_name'], role_params['access_zone'])
        RoleCreateHandler().handle(role_obj=role_obj, role_params=role_params, role_details=role_details)


def main():
    """ Create PowerScale Role object and perform action on it
        based on user input from playbook."""
    obj = Role()
    RoleHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
