#!/usr/bin/python
# Copyright: (c) 2019, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

""" Ansible module for managing Groups on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: group

version_added: "1.2.0"

short_description: Manage Groups on the PowerScale Storage System
description:
- Managing Groups on the PowerScale Storage System includes create group,
  delete group,  get group, add users and remove users.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale
author:
- P Srinivas Rao (@srinivas-rao5) <ansible.team@dell.com>
options:
  group_name:
    description:
    - The name of the group.
    type: str
  group_id:
    description:
    - The I(group_id) is auto generated or can be assigned at the time of creation.
    - For all other operations either I(group_name) or I(group_id) is needed.
    type: int
  access_zone:
    description:
    - This option mentions the zone in which a group is created.
    - For creation, I(access_zone) acts as an attribute for the group.
    - For all other operations I(access_zone) acts as a filter.
    type: str
    default: 'system'
  provider_type:
    description:
    - This option defines the type which will be used to
      authenticate the group members.
    - Creation, Deletion and Modification is allowed only for local group.
    - Details of groups of all provider types can be fetched.
    - If the I(provider_type) is C(ads) then the domain name of the Active
      Directory Server has to be mentioned in the group_name.
      The format for the group_name should be 'DOMAIN_NAME\group_name'
      or "DOMAIN_NAME\\group_name".
    - This option acts as a filter for all operations except creation.
    type: str
    default: 'local'
    choices: [ 'local', 'file', 'ldap', 'ads', 'nis']
  state:
    description:
    - The state option is used to determine whether the group
      will exist or not.
    type: str
    required: true
    choices: [ 'absent', 'present']
  users:
    description:
    - Either I(user_name) or I(user_id) is needed to add or remove the user
      from the group.
    - Users can be part of multiple groups.
    type: list
    elements: dict
  user_state:
    description:
    - The I(user_state) option is used to  determine whether the users
      will exist for a particular group or not.
    - It is required when users are added or removed from a group.
    type: str
    choices: ['present-in-group', 'absent-in-group']
notes:
- The I(check_mode) is not supported.
'''

EXAMPLES = r'''
  - name: Create a Group
    dellemc.powerscale.group:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      access_zone: "{{access_zone}}"
      provider_type: "{{provider_type}}"
      group_name: "{{group_name}}"
      state: "present"

  - name: Create a Group with group id
    dellemc.powerscale.group:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      access_zone: "{{access_zone}}"
      provider_type: "{{provider_type}}"
      group_name: "Test_group"
      group_id: 7000
      state: "present"

  - name: Create Group with Users
    dellemc.powerscale.group:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      provider_type: "{{provider_type}}"
      access_zone: "{{access_zone}}"
      group_name: "{{group_name}}"
      users:
        - user_name: "{{user_name}}"
        - user_id: "{{user_id}}"
        - user_name: "{{user_name_2}}"
      user_state: "present-in-group"
      state: "present"

  - name: Get Details of the Group using Group Id
    dellemc.powerscale.group:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      provider_type: "{{provider_type}}"
      access_zone: "{{access_zone}}"
      group_id: "{{group_id}}"
      state: "present"

  - name: Delete the Group using Group Name
    dellemc.powerscale.group:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      provider_type: "{{provider_type}}"
      access_zone: "{{access_zone}}"
      group_name: "{{group_name}}"
      state: "absent"

  - name: Add Users to a Group
    dellemc.powerscale.group:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      provider_type: "{{provider_type}}"
      access_zone: "{{access_zone}}"
      group_id: "{{group_id}}"
      users:
        - user_name: "{{user_name}}"
        - user_id: "{{user_id}}"
        - user_name: "{{user_name_2}}"
      user_state: "present-in-group"
      state: "present"

  - name: Remove Users from a Group
    dellemc.powerscale.group:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      provider_type: "{{provider_type}}"
      access_zone: "{{access_zone}}"
      group_id: "{{group_id}}"
      users:
        - user_name: "{{user_name_1}}"
        - user_id: "{{user_id}}"
        - user_name: "{{user_name_2}}"
      user_state: "absent-in-group"
      state: "present"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
    sample: "false"
group_details:
    description: Details of the group.
    returned: When group exists
    type: complex
    contains:
        gid:
            description: The details of the primary group for the user.
            type: complex
            contains:
                id:
                    description: The id of the group.
                    type: str
                name:
                    description: The name of the group.
                    type: str
                type_of_resource:
                    description: The resource's type is mentioned.
                    type: str
                    sample: "group"
        name:
            description: The name of the group.
            type: str
        provider:
            description: The provider contains the provider type and access zone.
            type: str
            sample: "lsa-local-provider:system"
        members:
            description: The list of sid's the members of group.
            type: complex
            contains:
                sid:
                    description: The details of the associated resource.
                    type: complex
                    contains:
                        id:
                            description: The unique security identifier of the
                                         resource.
                            type: str
                        name:
                            description: The name of the resource.
                            type: str
                        type_of_resource:
                            description: The resource's type is mentioned.
                            type: str
                            sample: "user"
    sample:
        {
            "dn": "CN=group_11,CN=Groups,DC=VXXXXX-CX",
            "dns_domain": null,
            "domain": "VXXXXX-CX",
            "generated_gid": false,
            "gid": {
                "id": "GID:2000",
                "name": "group_11",
                "type": "group"
            },
            "id": "group_11",
            "member_of": null,
            "members": [],
            "name": "group_11",
            "object_history": [],
            "provider": "lsa-local-provider:System",
            "sam_account_name": "group_11",
            "sid": {
                "id": "SID:S-1-0-11-1111111111-1111111111-1111111111-00000",
                "name": "group_11",
                "type": "group"
            },
            "type": "group"
        }

'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
import re

LOG = utils.get_logger('group')


class Group(object):
    """Class with group operations"""

    def __init__(self):
        """ Define all parameters required by this module"""

        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_group_parameters())

        required_one_of = [['group_name', 'group_id']]
        # initialize the ansible module
        self.module = AnsibleModule(argument_spec=self.module_params,
                                    supports_check_mode=False,
                                    required_one_of=required_one_of)

        # result is a dictionary that contains changed status and
        # group details
        self.result = {"changed": False}
        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])
        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.api_instance = utils.isi_sdk.AuthApi(self.api_client)
        self.group_api_instance = utils.isi_sdk.AuthGroupsApi(
            self.api_client)
        LOG.info('Got the isi_sdk instance for authorization on to PowerScale')

    def check_provider_type(self, provider, message):
        """ Check the provider and return the updated provider"""
        if provider.lower() != "local":
            error_message = \
                "%s group is allowed only" \
                " if provider_type is local, got '%s' provider" \
                % (message, provider)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
        return provider

    def create_user_objects(self, users, user_state):
        users_list = []
        if user_state == 'present-in-group' and users:
            for user in users:
                if not isinstance(user, dict):
                    self.module.fail_json(
                        msg="Key Value pair is allowed, Provided %s."
                            % user)
                if len(user.keys()) != 1:
                    self.module.fail_json(
                        msg="One Key per dictionary is allowed, %s"
                            " given" % user.keys())
                if 'user_name' in user:
                    user = utils.isi_sdk.AuthAccessAccessItemFileGroup(
                        "USER:" + user['user_name'])
                    users_list.append(user)
                elif 'user_id' in user:
                    user = utils.isi_sdk.AuthAccessAccessItemFileGroup(
                        "UID:" + user['user_id'])
                    users_list.append(user)
                else:
                    error = 'user_id or user_name  is expected,' \
                            ' "%s" given.' % list(user.keys())[0]
                    self.module.fail_json(msg=error)
        return users_list

    def create_group(self, group_name, group_id, zone, provider, users_list):
        """Create Group in PowerScale"""
        try:
            LOG.info("Creating Group %s", group_name)
            provider = self.check_provider_type(provider, 'Create')
            auth_group = utils.isi_sdk.AuthGroupCreateParams(
                name=group_name, gid=group_id, members=users_list)
            api_response = self.api_instance.create_auth_group(
                auth_group=auth_group, zone=zone, provider=provider)
            LOG.info("The group is created with id: %s", str(api_response))
            return True
        except Exception as e:
            error = self.determine_error(error_obj=e)
            error_message = "Create Group %s failed with %s" \
                            % (group_name, error)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete_group(self, group, zone, provider):
        """Delete Group in PowerScale"""
        try:
            LOG.info("Deleting Group %s", group)
            provider = self.check_provider_type(provider, 'Delete')
            self.api_instance.delete_auth_group(
                group, zone=zone, provider=provider)
            return True
        except Exception as e:
            error = self.determine_error(error_obj=e)
            error_message = "Delete %s  failed with %s" \
                            % (group, error)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_group_details(self, group, zone, provider):
        """Get the Group Details in PowerScale"""
        try:
            LOG.info("Getting Details of group %s ", group)
            if provider != "nis":
                api_response = self.api_instance.get_auth_group(
                    auth_group_id=group,
                    provider=provider, zone=zone)
                LOG.info("Group Details: %s", str(api_response))
                api_response_dict = api_response.groups[0].to_dict()
                group_user_details = self.get_group_members(
                    group, zone, provider)
                if group_user_details:
                    api_response_dict['members'] = group_user_details
                else:
                    api_response_dict['members'] = []
                return api_response_dict
            else:
                api_response = self.api_instance.list_auth_groups(provider=provider, zone=zone)
                group = group.split(":")
                for item in api_response.groups:
                    if item.name == group[1]:
                        return item.to_dict()
        except utils.ApiException as e:
            if str(e.status) == "404":
                error_message = "Get Group Details %s failed with %s" \
                                % (group, self.determine_error(e))
                LOG.info(error_message)
                return None
            else:
                error_message = "Get Group Details %s failed with %s" \
                                % (group, self.determine_error(e))
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

        except Exception as e:
            error_message = "Get Group Details %s failed with %s" \
                            % (group, self.determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_group_members(self, group, zone, provider):
        """Get the Group Member Details in PowerScale"""
        try:
            LOG.info("Getting members of group %s", group)
            provider = 'local' if not provider else provider
            api_response = self.group_api_instance.list_group_members(
                group, zone=zone, provider=provider)
            api_response_dict = api_response.to_dict()
            LOG.info("Group Members: %s", api_response_dict['members'])
            return api_response_dict['members']
        except Exception as e:
            error = self.determine_error(error_obj=e)
            error_message = "Get Users for group %s failed with %s" \
                            % (group, error)
            LOG.info(error_message)
            self.module.fail_json(msg=error_message)

    def add_user_to_group(self, group, user,
                          zone, provider):
        """ Add a User to a Group in PowerScale """
        try:
            message = "Adding user %s to group %s" % (user, group)
            LOG.info(message)
            group_member = utils.isi_sdk.AuthAccessAccessItemFileGroup(user)
            provider = self.check_provider_type(provider, 'Add User to')
            api_response = self.group_api_instance.create_group_member(
                group_member, group, zone=zone, provider=provider)
            LOG.info(api_response)
            return True
        except Exception as e:
            error = self.determine_error(error_obj=e)
            error_message = "Add user %s to group failed with %s " \
                            % (user, error)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def remove_user_from_group(self, group, user, zone, provider):
        """ Remove a user from a Group in PowerScale"""
        try:
            message = "Removing user %s from group %s" % (user, group)
            LOG.info(message)
            provider = self.check_provider_type(provider, 'Remove User from')
            self.group_api_instance.delete_group_member(
                user, group, zone=zone, provider=provider)
            return True

        except Exception as e:
            error = self.determine_error(error_obj=e)
            error_message = "Remove user %s from group failed with %s" \
                            % (group, error)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_user_name(self, user_id, zone):
        """Get the Member Name in PowerScale"""
        try:
            LOG.info("Getting User name using User id %s", user_id)
            mapping_identity_id = 'UID:' + user_id
            api_response = self.api_instance.get_mapping_identity(
                mapping_identity_id, nocreate=True, zone=zone)
            return api_response.identities[0].targets[0].target.name
        except Exception as e:
            error = self.determine_error(error_obj=e)
            error_message = "Get user_name for %s failed with  %s" \
                            % (user_id, error)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def is_user_part_of_group(
            self, group, user_name, user_id, zone, provider):
        """Check if Member is part of the Group or not"""
        if user_id:
            LOG.info("User Id given, getting corresponding User name")
            user_name = self.get_user_name(user_id, zone)
        group_members = self.get_group_members(group, zone, provider)
        if len(group_members) == 0:
            return False
        for user_details in group_members:
            LOG.info("user_details['name'] %s", user_details['name'])
            if user_details['name'].lower() == user_name.lower():
                return True
        return False

    def update_group(self, group, user_name, user_id,
                     user_state, access_zone, provider_type):
        """Update the group members in PowerScale"""
        changed = False
        user_flag = self.is_user_part_of_group(group, user_name, user_id,
                                               access_zone, provider_type)

        user = "USER:" + user_name if user_name else "UID:" + user_id
        if user_state == 'present-in-group' and not user_flag:
            changed = self.add_user_to_group(group, user, access_zone,
                                             provider_type)

        if user_state == 'absent-in-group' and user_flag:
            changed = self.remove_user_from_group(group, user, access_zone,
                                                  provider_type)
        return changed

    def determine_error(self, error_obj):
        """Determine the error message to return"""
        if isinstance(error_obj, utils.ApiException):
            error = error_obj.body
            error = re.sub('[^A-Za-z:.,]+', ' ', str(error))
        else:
            error = str(error_obj)
        return error

    def check_if_id_exists(self, group_name, group_details):
        """
        Check if the id exists
        :param group_name: Group name
        :param group_details: Group details
        :return: True if id exists.
        """
        if group_name is not None and group_name.lower() == group_details['gid']['name'].lower():
            return False
        return True

    def perform_module_operation(self):
        """
        Perform different actions on group module based on parameters
        chosen in playbook
        """
        group_name = self.module.params['group_name']
        group_id = self.module.params['group_id']
        access_zone = self.module.params['access_zone']
        provider_type = self.module.params['provider_type']
        state = self.module.params['state']
        users = self.module.params['users']
        user_state = self.module.params['user_state']
        group = None
        if group_name:
            group = 'GROUP:' + group_name
        if group_id:
            group = 'GID:' + str(group_id)

        if group is None:
            self.module.fail_json(msg="Invalid group_name or group_id provided.")

        if not users and user_state:
            self.module.fail_json(msg="'user_state' is given,"
                                      " 'users' are not specified")

        if not user_state and users:
            self.module.fail_json(msg="'user_state' is not specified,"
                                      " 'users' are given")

        changed = False
        if state == 'present':
            group_details = self.get_group_details(
                group, access_zone, provider_type)
            if not group_details:
                if not group_name:
                    error_message = "Unable to create a group, 'group_name' is"\
                                    " missing"
                    LOG.error(error_message)
                    self.module.fail_json(msg=error_message)
                LOG.info("Create a Group %s ", group_name)
                users_list = self.create_user_objects(users, user_state)
                self.create_group(group_name, group_id, access_zone, provider_type,
                                  users_list)
                changed = True
            else:
                id_exists = self.check_if_id_exists(group_name, group_details)
                if id_exists and group_name is not None:
                    error_message = f'Group already exists with GID {group_id}'
                    LOG.error(error_message)
                    self.module.fail_json(msg=error_message)
                if user_state and users:
                    user_modified_flag = False
                    for user in users:
                        if not isinstance(user, dict):
                            self.module.fail_json(
                                msg="Key Value pair is allowed, Provided %s."
                                    % user)

                        if len(user.keys()) != 1:
                            self.module.fail_json(
                                msg="One Key per dictionary is allowed, %s"
                                    " given" % list(user.keys()))

                        if 'user_name' in user:
                            user_modified_flag = self.update_group(
                                group, user['user_name'],
                                None, user_state, access_zone, provider_type)

                        elif 'user_id' in user:
                            user_modified_flag = self.update_group(
                                group, None, user['user_id'],
                                user_state, access_zone, provider_type)
                        else:
                            error = 'user_id or user_name  is expected,' \
                                    ' "%s" given.' % list(user.keys())[0]
                            self.module.fail_json(msg=error)

                        if user_modified_flag and not changed:
                            changed = True
        else:
            if group_name:
                LOG.info("Delete Group %s  ", group_name)
            else:
                LOG.info("Delete Group %s  ", group_id)
            group_details = self.get_group_details(
                group, access_zone, provider_type)
            if group_details:
                changed = self.delete_group(
                    group, access_zone, provider_type)

        group_details = self.get_group_details(
            group, access_zone, provider_type)

        self.result["changed"] = changed
        self.result["group_details"] = group_details
        self.module.exit_json(**self.result)


def get_group_parameters():
    """This method provide parameter required for the ansible group
    module on PowerScale"""
    return dict(
        group_name=dict(required=False, type='str'),
        group_id=dict(required=False, type='int'),
        access_zone=dict(required=False, type='str', default='system'),
        provider_type=dict(required=False, type='str',
                           choices=['local', 'file', 'ldap', 'ads', 'nis'],
                           default='local'),
        state=dict(required=True, type='str', choices=['present', 'absent']),
        users=dict(required=False, type='list', elements='dict'),
        user_state=dict(required=False, type='str',
                        choices=['present-in-group', 'absent-in-group'])
    )


def main():
    """ Create PowerScale Group object and perform actions on it
        based on user input from playbook"""
    obj = Group()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
