#!/usr/bin/python
# Copyright: (c) 2024, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

""" Ansible module for managing Users on PowerScale"""
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: user
short_description: Manage users on the PowerScale Storage System
description:
- Managing Users on the PowerScale Storage System includes create user,
  delete user, update user, get user, add role and remove role.
version_added: "1.2.0"
extends_documentation_fragment:
  - dellemc.powerscale.powerscale
author:
- P Srinivas Rao (@srinivas-rao5) <ansible.team@dell.com>
- Trisha Datta (@trisha-dell) <ansible.team@dell.com>
options:
  user_name:
    description:
    - The name of the user account.
    type: str
  user_id:
    description:
    - The I(user_id) is auto generated or can be assigned at the time of creation.
    - For all other operations either I(user_name) or I(user_id) is needed.
    type: int
  password:
    description:
    - The password for the user account.
    - Required only in the creation of a user account.
    - If given in other operations then the password will be ignored.
    type: str
  access_zone:
    description:
    - This option mentions the zone in which a user is created.
    - For creation, I(access_zone) acts as an attribute for the user.
    - For all other operations I(access_zone) acts as a filter.
    type: str
    default: 'system'
  provider_type:
    description:
    - This option defines the type which will be used to
      authenticate the user.
    - Creation, Modification and Deletion is allowed for local users.
    - Adding and removing roles is allowed for all users of the
      system access zone.
    - Getting user details is allowed for all users.
    - If the I(provider_type) is 'ads' then domain name of the Active
      Directory Server has to be mentioned in the I(user_name).
      The format for the I(user_name) should be 'DOMAIN_NAME\user_name'
      or "DOMAIN_NAME\\user_name".
    - This option acts as a filter for all operations except creation.
    type: str
    default: 'local'
    choices: [ 'local', 'file', 'ldap', 'ads', 'nis']
  enabled:
    description:
    - Enabled is a bool variable which is used to enable or disable
      the user account.
    type: bool
  primary_group:
    description:
    - A user can be member of multiple groups of which one group has
      to be assigned as primary group.
    - This group will be used for access checks and
      can also be used when creating files.
    - A user can be added to the group using Group Name.
    type: str
  home_directory:
    description:
    - The path specified in this option acts as a home directory
      for the user.
    - The directory which is given should not be already in use.
    - For a user in a system access zone, the absolute path has to be given.
    - For users in a non-system access zone, the path relative to
      the non-system Access Zone's base directory has to be given.
    type: str
  shell:
    description:
    - This option is for choosing the type of shell for the user account.
    type: str
  full_name:
    description:
    - The additional information about the user can be provided using
      full_name option.
    type: str
  email:
    description:
    - The email id of the user can be added using email option.
    - The email id can be set at the time of creation and modified later.
    type: str
  state:
    description:
    - The state option is used to mention the existence of
      the user account.
    type: str
    required: true
    choices: [ 'absent', 'present' ]
  role_name:
    description:
    - The name of the role which a user will be assigned.
    - User can be added to multiple roles.
    type: str
  role_state:
    description:
    - The I(role_state) option is used to mention the existence of the role
      for a particular user.
    - It is required when a role is added or removed from user.
    type: str
    choices: ['present-for-user', 'absent-for-user']
  update_password:
    description:
    - This parameter controls the way the I(password) is updated during
      the creation and modification of a user.
    - C(always) will update password for each execution.
    - C(on_create) will only set while creating a user.
    - For modifying I(password), set the I(update_password) to
      C(always).
    choices: ['always', 'on_create']
    default: always
    type: str
notes:
- The I(check_mode) is not supported.
'''

EXAMPLES = r'''
- name: Get User Details using user name
  dellemc.powerscale.user:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    access_zone: "{{access_zone}}"
    provider_type: "{{provider_type}}"
    user_name: "{{account_name}}"
    state: "present"

- name: Create User
  dellemc.powerscale.user:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    access_zone: "{{access_zone}}"
    provider_type: "{{provider_type}}"
    user_name: "{{account_name}}"
    password: "{{account_password}}"
    primary_group: "{{primary_group}}"
    enabled: "{{enabled}}"
    email: "{{email}}"
    full_name: "{{full_name}}"
    home_directory: "{{home_directory}}"
    shell: "{{shell}}"
    role_name: "{{role_name}}"
    role_state: "present-for-user"
    state: "present"

- name: Create User with user id
  dellemc.powerscale.user:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    access_zone: "{{access_zone}}"
    provider_type: "{{provider_type}}"
    user_name: "Test_User"
    user_id: 7000
    password: "{{account_password}}"
    primary_group: "{{primary_group}}"
    enabled: "{{enabled}}"
    email: "{{email}}"
    full_name: "{{full_name}}"
    home_directory: "{{home_directory}}"
    shell: "{{shell}}"
    role_name: "{{role_name}}"
    role_state: "present-for-user"
    state: "present"

- name: Update User's Full Name and email using user name
  dellemc.powerscale.user:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    access_zone: "{{access_zone}}"
    provider_type: "{{provider_type}}"
    user_name: "{{account_name}}"
    email: "{{new_email}}"
    full_name: "{{full_name}}"
    state: "present"

- name: Disable User Account using User Id
  dellemc.powerscale.user:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    access_zone: "{{access_zone}}"
    provider_type: "{{provider_type}}"
    user_id: "{{id}}"
    enabled: false
    state: "present"

- name: Add user to a role using Username
  dellemc.powerscale.user:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    user_name: "{{account_name}}"
    provider_type: "{{provider_type}}"
    role_name: "{{role_name}}"
    role_state: "present-for-user"
    state: "present"

- name: Remove user from a role using User id
  dellemc.powerscale.user:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    user_id: "{{id}}"
    role_name: "{{role_name}}"
    role_state: "absent-for-user"
    state: "present"

- name: Delete User using user name
  dellemc.powerscale.user:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    access_zone: "{{access_zone}}"
    provider_type: "{{provider_type}}"
    user_name: "{{account_name}}"
    state: "absent"

- name: Modify password in non-system access zone update_password as "always"
  dellemc.powerscale.user:
    onefs_host: "{{onefs_host}}"
    port_no: "{{port_no}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    access_zone: "{{access_zone}}"
    provider_type: "{{provider_type}}"
    user_name: "{{account_name}}"
    password: "new_password"
    update_password: "always"
    state: "present"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
user_details:
    description: Details of the user.
    returned: When user exists
    type: complex
    contains:
        email:
            description: The email of the user.
            type: str
        enabled:
            description: Enabled is a bool variable which is used to enable or
                         disable the user account.
            type: bool
        gecos:
            description: The full description of the user.
            type: str
        gid:
            description: The details of the primary group for the user.
            type: complex
            contains:
                id:
                    description: The id of the primary group.
                    type: str
                name:
                    description: The name of the primary group.
                    type: str
                type:
                    description: The resource's type is mentioned.
                    type: str
        home_directory:
            description: The directory path acts as the home directory
                         for the user's account.
            type: str
        name:
            description: The name of the user.
            type: str
        provider:
            description: The provider contains the provider type and access zone.
            type: str
        roles:
            description: The list of all the roles of which user is a member.
            returned: For all users in system access zone.
            type: list
        shell:
            description: The type of shell for the user account.
            type: str
        uid:
            description: Details about the id and name of the user.
            type: complex
            contains:
                id:
                    description: The id of the user.
                    type: str
                name:
                    description: The name of the user.
                    type: str
                type:
                    description: The resource's type is mentioned.
                    type: str
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
import re

LOG = utils.get_logger('user')


class User(object):
    """Class with user operations"""

    def __init__(self):
        """ Define all parameters required by this module"""

        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_user_parameters())

        required_one_of = [
            ['user_name', 'user_id']
        ]

        # initialize the ansible module
        self.module = AnsibleModule(argument_spec=self.module_params,
                                    supports_check_mode=False,
                                    required_one_of=required_one_of)

        # result is a dictionary that contains changed status and
        # user details
        self.result = {"changed": False}
        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.api_instance = utils.isi_sdk.AuthApi(self.api_client)
        cluster_api = utils.isi_sdk.ClusterApi(self.api_client)
        major = str(cluster_api.get_cluster_config().to_dict()['onefs_version']['release'].split('.')[0])
        minor = str(cluster_api.get_cluster_config().to_dict()['onefs_version']['release'].split('.')[1])
        self.array_version = major + "." + minor
        self.role_api_instance = utils.isi_sdk.AuthRolesApi(
            self.api_client)
        self.zone_summary_api = utils.isi_sdk.ZonesSummaryApi(self.api_client)

        LOG.info('Got the isi_sdk instance for authorization on to PowerScale')

    def get_zone_base_path(self, access_zone):
        """Returns the base path of the Access Zone."""
        try:
            zone_path = (self.zone_summary_api.
                         get_zones_summary_zone(access_zone)).to_dict()
            zone_base_path = zone_path['summary']['path']
            LOG.info("Successfully got zone_base_path for %s is %s",
                     access_zone, zone_base_path)
            return zone_base_path
        except Exception as e:
            error_message = 'Unable to fetch base path of Access Zone %s ' \
                            ',failed with error: %s', access_zone, \
                            self.determine_error(e)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def check_provider_type(self, provider, message):
        """ Check the provider and return the updated provider"""
        if provider.lower() != "local":
            error_message = \
                "%s user is allowed only" \
                " if provider_type is local, got '%s' provider" \
                % (message, provider)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
        return provider

    def determine_error(self, error_obj):
        """Determine the error message to return"""
        if isinstance(error_obj, utils.ApiException):
            error = re.sub("[\n \"]+", ' ', str(error_obj.body))
        else:
            error = str(error_obj)
        return error

    def create_user(self, user_name, user_id, password, zone, provider,
                    enabled, primary_group, home_directory, shell,
                    full_name, email):
        """Create User in PowerScale"""
        try:
            if primary_group:
                primary_group = utils.isi_sdk.AuthAccessAccessItemFileGroup(
                    "GROUP:" + primary_group)

            provider = self.check_provider_type(provider, 'Create')
            auth_user = utils.isi_sdk.AuthUserCreateParams(
                name=user_name, uid=user_id, password=password, enabled=enabled,
                primary_group=primary_group, home_directory=home_directory,
                shell=shell, gecos=full_name, email=email)

            api_response = self.api_instance.create_auth_user(
                auth_user=auth_user,
                zone=zone, provider=provider)

            LOG.info('User is created with the SID: %s', str(api_response))
        except Exception as e:
            error = self.determine_error(error_obj=e)
            error_message = \
                "Create User '%s' failed with %s" % (user_name, error)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete_user(self, auth_user_id, zone, provider):
        """Delete User in PowerScale"""
        try:
            provider = self.check_provider_type(provider, 'Delete')
            self.api_instance.delete_auth_user(
                auth_user_id=auth_user_id, zone=zone, provider=provider)
            LOG.info("User %s is deleted", auth_user_id)
            return True
        except Exception as e:
            error = self.determine_error(error_obj=e)
            error_message = "Delete User '%s' failed with %s" \
                            % (auth_user_id, error)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def is_user_modified_sensitive(self, user_details):
        """ Determines whether the user details are to be modified or not."""
        if self.module.params['enabled'] is not None:
            if self.module.params['enabled'] != user_details['enabled']:
                return True

        parameter_list = ['full_name', 'home_directory']

        for parameter in parameter_list:
            if self.module.params[parameter]:
                if user_details[parameter]:
                    if self.module.params[parameter] != \
                            user_details[parameter]:
                        return True
                else:
                    return True
        return False

    def is_user_modified_insensitive(self, user_details):
        """ Determines whether the user details are to be modified or not."""

        parameter_list = ['primary_group', 'shell', 'email']
        for parameter in parameter_list:
            if self.module.params[parameter]:
                if user_details[parameter]:
                    if self.module.params[parameter].lower() != \
                            user_details[parameter].lower():
                        return True
                else:
                    return True
        return False

    def modify_password(self, auth_user_id, zone):
        """Modifying user password if needed"""
        try:
            if self.module.params['update_password'] == "always" and \
                    self.module.params['password'] is not None:
                auth_user = utils.isi_sdk.AuthUser(password=self.module.params['password'])

                self.api_instance.update_auth_user(
                    auth_user=auth_user, auth_user_id=auth_user_id,
                    zone=zone)
                LOG.info("User %s password is updated", auth_user_id)
                return True
            return False
        except Exception as e:
            error = self.determine_error(error_obj=e)
            error_message = "Update password for User '%s' failed with %s" \
                            % (auth_user_id, error)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def update_user(self, auth_user_id, zone, provider, enabled,
                    primary_group, home_directory, shell,
                    full_name, email):
        """Update the User Account details in PowerScale"""
        try:
            if primary_group:
                primary_group = utils.isi_sdk.AuthAccessAccessItemFileGroup(
                    "GROUP:" + primary_group)
            auth_user = utils.isi_sdk.AuthUser(primary_group=primary_group,
                                               home_directory=home_directory,
                                               shell=shell, gecos=full_name,
                                               email=email, enabled=enabled)
            provider = self.check_provider_type(provider, 'Update')
            self.api_instance.update_auth_user(
                auth_user=auth_user, auth_user_id=auth_user_id,
                zone=zone, provider=provider)
            LOG.info("User %s is updated", auth_user_id)
            return True
        except Exception as e:
            error = self.determine_error(error_obj=e)
            error_message = "Update User '%s' failed with %s" \
                            % (auth_user_id, error)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_user_details(self, auth_user_id, zone, provider):
        """Get the User Account Details in PowerScale"""
        error_msg = "Get User Details %s failed with %s"
        try:
            api_response = self.api_instance.get_auth_user(
                auth_user_id=auth_user_id,
                zone=zone, provider=provider)
            LOG.info('User details are %s', str(api_response))
            api_response_dict = api_response.users[0].to_dict()

            return api_response_dict

        except utils.ApiException as e:
            if str(e.status) == "404":
                error_message = error_msg \
                    % (auth_user_id, self.determine_error(e))
                LOG.info(error_message)
                return None
            else:
                error_message = error_msg \
                    % (auth_user_id, self.determine_error(e))
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

        except Exception as e:
            error_message = error_msg \
                % (auth_user_id, self.determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def add_role_to_user(self, auth_user_id, role_name):
        """Add a Role to a User in PowerScale"""
        try:
            role_member = utils.isi_sdk.AuthAccessAccessItemFileGroup(
                id=auth_user_id)
            self.role_api_instance.create_role_member(
                role_member, role=role_name)
            message = 'User %s added to role %s ' \
                      % (auth_user_id, role_name)
            LOG.info(message)
            return True
        except Exception as e:
            error = self.determine_error(error_obj=e)
            error_message = "Add user %s to role %s failed with %s " \
                            % (auth_user_id, role_name, error)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def remove_role_from_user(self, role_member_id, role_name):
        """ Remove a Role from a User in PowerScale"""
        try:
            self.role_api_instance.delete_role_member(
                role_member_id, role=role_name)
            message = 'User %s removed from role %s ' \
                      % (role_member_id, role_name)
            LOG.info(message)
            return True
        except Exception as e:
            error = self.determine_error(error_obj=e)
            error_message = "Remove user %s from role %s failed with %s " \
                            % (role_member_id, role_name, error)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def is_user_part_of_role(self, user_name, user_id, role_name):
        """ Determines if the user is part of a given role or not."""
        if role_name:
            roles_for_user = self.get_roles_for_user(user_name, user_id)
            debug_message = "roles for users %s" % roles_for_user
            LOG.debug(debug_message)
            if role_name.lower() in roles_for_user:
                return True
            else:
                return False
        else:
            return False

    def get_roles_for_user_by_name(self, user_name, api_response):
        """ Get the roles for the user by user_name  """
        roles_for_user = []
        for role_name in api_response.roles:
            if role_name.members:
                for member in role_name.members:
                    if member.name and (member.name.lower()
                                        == user_name.lower()):
                        roles_for_user.append(role_name.id.lower())
        return roles_for_user

    def get_roles_for_user_by_id(self, user_id, api_response):
        """ Get the roles for the user by user_id """
        roles_for_user = []
        user_id = "UID:" + str(user_id)
        for role_name in api_response.roles:
            if role_name.members:
                for member in role_name.members:
                    if member.id == user_id:
                        roles_for_user.append(role_name.id.lower())
        return roles_for_user

    def get_roles_for_user(self, user_name, user_id):
        """ Get the roles for the user  """
        try:
            api_response = self.api_instance.list_auth_roles()
            if user_name is not None:
                return self.get_roles_for_user_by_name(user_name, api_response)
            else:
                return self.get_roles_for_user_by_id(user_id, api_response)
        except utils.ApiException as e:
            error_message = "Exception when calling" \
                            " AuthApi->list_auth_roles: %s\n" % e
            LOG.error(error_message)

    def collect_user_details(self, auth_user_id, access_zone, provider_type,
                             role_name, role_state, user_name, user_id):
        """Get the details of the user"""
        user_details = self.get_user_details(
            auth_user_id, access_zone, provider_type)
        if user_details:
            # Error is none so user exists, hence getting the list
            # of roles for the user if the User is in System Access Zone
            get_roles_flag = True
            if (not role_name) and (role_state is None) and \
                    (access_zone.lower() != "system"):
                get_roles_flag = False
                user_details['roles'] = []
            if get_roles_flag:
                user_details['roles'] = self.get_roles_for_user(
                    user_name, user_id)
        return user_details

    def create_new_user(self, user_name, user_id, password, access_zone,
                        provider_type, enabled, primary_group,
                        home_directory, full_name, email,
                        role_state, role_name, auth_user_id):
        """Create a new user"""

        if not user_name:
            error_message = "Unable to create a user, 'user_name' is" \
                            " missing"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
        if not password:
            error_message = "Unable to create a user, 'password' is" \
                            " missing"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
        shell = self.module.params['shell']
        self.create_user(user_name, user_id, password, access_zone,
                         provider_type, enabled, primary_group,
                         home_directory, shell, full_name, email)

        if role_state == "present-for-user":
            self.add_role_to_user(auth_user_id, role_name)

        return True

    def modify_existing_user(self, user_name, user_id, role_name, role_state,
                             auth_user_id, user_details, home_directory,
                             access_zone, provider_type, enabled,
                             primary_group, full_name, email):
        """Modifying details of a user"""

        LOG.info("Modifying the user details.")
        # Check for changes in role
        shell = self.module.params['shell']
        role_flag = self.is_user_part_of_role(
            user_name, user_id, role_name)
        role_changed = False
        message = "role_flag %s" % role_flag
        LOG.debug(message)

        if role_flag:
            if role_state == "absent-for-user":
                role_changed = self.remove_role_from_user(
                    auth_user_id, role_name)
        else:
            if role_state == "present-for-user":
                role_changed = self.add_role_to_user(
                    auth_user_id, role_name)

        old_user_details = get_user_params_from_details(user_details)
        modified_sensitive = self.is_user_modified_sensitive(old_user_details)
        modified_insensitive = self.is_user_modified_insensitive(old_user_details)
        user_details_changed = False
        if home_directory and \
                user_details['home_directory'] == home_directory:
            home_directory = None

        if modified_sensitive or modified_insensitive:
            user_details_changed = self.update_user(
                auth_user_id, access_zone, provider_type, enabled,
                primary_group, home_directory, shell, full_name, email)

        password_changed = False
        if float(self.array_version) < 9.5:
            password_changed = self.modify_password(auth_user_id, access_zone)
        return user_details_changed or role_changed or password_changed

    def delete_existing_user(self, provider_type, auth_user_id, access_zone,
                             role_name, role_state, user_name, user_id):
        """Delete the user and related objects"""

        if provider_type.lower() != 'local':
            self.module.fail_json(
                msg="Cannot delete user from %s  provider_type"
                    % provider_type)
        user_details = self.get_user_details(
            auth_user_id, access_zone, provider_type)
        if user_details:
            get_roles_flag = True
            if (not role_name) and (role_state is None) and \
                    (access_zone.lower() != "system"):
                get_roles_flag = False
            roles_for_user = []
            if get_roles_flag:
                roles_for_user = self.get_roles_for_user(
                    user_name, user_id)

            if get_roles_flag and len(roles_for_user) != 0:
                for role in roles_for_user:
                    self.remove_role_from_user(auth_user_id, role)
            return self.delete_user(auth_user_id, access_zone,
                                    provider_type)
        else:
            return False

    def set_validate_params(self, access_zone, user_name, user_id,
                            email, role_name, role_state):
        """Set and validate the params"""

        if self.module.params['home_directory'] and \
                access_zone.lower() != 'system':
            self.module.params['home_directory'] = \
                self.get_zone_base_path(access_zone) + \
                self.module.params['home_directory']

        home_directory = self.module.params['home_directory']
        auth_user_id = None
        if user_name:
            auth_user_id = 'USER:' + user_name
        if user_id:
            auth_user_id = 'UID:' + str(user_id)
        if auth_user_id is None:
            self.module.fail_json(
                msg="Invalid user_name or user_id provided.")
        if email and re.search(
                r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$',
                email) is None:
            self.module.fail_json(msg="Email is not in the correct format")
        if (role_name and role_state is None) or \
                (not role_name and role_state is not None):
            self.module.fail_json(
                msg="role_name and role_state both are required"
                    " to add or remove user from a role")

        if role_name and access_zone.lower() != 'system':
            self.module.fail_json(
                msg="roles can be assigned to users and groups of"
                    " System Access Zone, got %s" % access_zone)

        return home_directory, auth_user_id

    def check_if_id_exists(self, user_name, user_details):
        """
        Check if the id exists
        :param user_name: User name
        :param user_details: User details
        :return: True if id exists.
        """
        if user_name == user_details['uid']['name']:
            return False
        return True

    def perform_module_operation(self):
        """
        Perform different actions on user module based on parameters
        chosen in playbook
        """
        user_name = self.module.params['user_name']
        user_id = self.module.params['user_id']
        password = self.module.params['password']
        access_zone = self.module.params['access_zone']
        provider_type = self.module.params['provider_type']
        enabled = self.module.params['enabled']
        primary_group = self.module.params['primary_group']
        full_name = self.module.params['full_name']
        email = self.module.params['email']
        state = self.module.params['state']
        role_name = self.module.params['role_name']
        role_state = self.module.params['role_state']

        changed = False
        home_directory, auth_user_id = self.set_validate_params(access_zone, user_name, user_id,
                                                                email, role_name, role_state)
        if state == "present":
            user_details = self.collect_user_details(auth_user_id, access_zone,
                                                     provider_type, role_name, role_state,
                                                     user_name, user_id)
            if user_details is not None and user_name is not None:
                id_exists = self.check_if_id_exists(user_name, user_details)
                if id_exists:
                    error_message = "User already exists with UID %s" % user_id
                    LOG.error(error_message)
                    self.module.fail_json(msg=error_message)
            # If User Details is None, User is created.
            if not user_details:
                changed = self.create_new_user(user_name, user_id, password, access_zone,
                                               provider_type, enabled, primary_group,
                                               home_directory, full_name, email,
                                               role_state, role_name, auth_user_id)

            else:
                changed = self.modify_existing_user(user_name, user_id, role_name,
                                                    role_state, auth_user_id, user_details,
                                                    home_directory, access_zone, provider_type,
                                                    enabled, primary_group, full_name, email)
        # State == Absent (Delete User Account)
        else:
            changed = self.delete_existing_user(provider_type, auth_user_id,
                                                access_zone, role_name, role_state,
                                                user_name, user_id)
        '''
        Finally update the module changed state and saving updated user
        details
        '''
        user_details = self.get_user_details(
            auth_user_id, access_zone, provider_type)
        if user_details and access_zone.lower() == 'system':
            get_roles_flag = True
            if (not role_name) and (role_state is None) and \
                    (access_zone.lower() != "system"):
                get_roles_flag = False
                user_details['roles'] = []
            if get_roles_flag:
                user_details['roles'] = self.get_roles_for_user(
                    user_name, user_id)
        self.result["changed"] = changed
        self.result["user_details"] = user_details
        self.module.exit_json(**self.result)


def get_user_params_from_details(user_details):
    user_params = {
        'user_id': user_details['uid']['id'].split(":")[1],
        'user_name': user_details['id'],
        'access_zone': user_details['provider'].split(":")[1],
        "provider_type":
            user_details['provider'].split(":")[0].split("-")[1],
        'enabled': bool(user_details['enabled']),
        'primary_group': user_details['primary_group_sid']['name'],
        'home_directory': user_details['home_directory'],
        'shell': user_details['shell'],
        'full_name': user_details['gecos'],
        'email': user_details['email']}
    return user_params


def get_user_parameters():
    """This method provide parameter required for the ansible user
    modules on PowerScale"""
    return dict(
        user_name=dict(type='str'),
        user_id=dict(type='int'),
        password=dict(type='str', no_log=True),
        access_zone=dict(type='str', default='system'),
        provider_type=dict(type='str', default='local',
                           choices=['local', 'file', 'ldap', 'ads', 'nis']),
        enabled=dict(type='bool'),
        primary_group=dict(type='str'),
        home_directory=dict(type='str'),
        shell=dict(type='str'),
        full_name=dict(type='str'),
        email=dict(type='str'),
        state=dict(type='str', required=True,
                   choices=['present', 'absent']),
        role_name=dict(type='str'),
        role_state=dict(type='str',
                        choices=['present-for-user', 'absent-for-user']),
        update_password=dict(type='str', choices=['on_create', 'always'], default='always')
    )


def main():
    """ Create PowerScale User object and perform actions on it
        based on user input from playbook"""
    obj = User()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
