#!/usr/bin/python
# Copyright: (c) 2019-2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
    - This option defines the type of the authentication provider for
      the group itself.
    - Creation, Deletion and Modification is allowed only for local group.
    - Details of groups of all provider types can be fetched.
    - If the I(provider_type) is C(ads) then the domain name of the Active
      Directory Server has to be mentioned in the group_name.
      The format for the group_name should be 'DOMAIN_NAME\group_name'
      or "DOMAIN_NAME\\group_name".
    - This option acts as a filter for all operations except creation.
    - When a member in I(users) omits its own C(provider_type), this
      group-level provider is used as the default for member resolution.
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
    - Each element may optionally include a C(provider_type) key to add or
      remove a member from a different authentication provider (cross-provider
      membership). This requires OneFS 9.11.0 or later.
    type: list
    elements: dict
    suboptions:
      user_name:
        description:
        - The name of the user to add or remove.
        - Mutually exclusive with I(user_id).
        type: str
      user_id:
        description:
        - The numeric UID of the user to add or remove.
        - Mutually exclusive with I(user_name).
        type: str
      provider_type:
        description:
        - The authentication provider in which to resolve the user.
        - When omitted the group-level I(provider_type) is used.
        - When specified the module validates that the provider is
          configured in the target I(access_zone) and that the cluster
          runs OneFS 9.11.0 or later.
        type: str
        choices: [ 'local', 'file', 'ldap', 'ads', 'nis']
  user_state:
    description:
    - The I(user_state) option is used to  determine whether the users
      will exist for a particular group or not.
    - It is required when users are added or removed from a group.
    type: str
    choices: ['present-in-group', 'absent-in-group']
attributes:
  check_mode:
    description: Runs task to validate without performing action on the target machine.
    support: full
  diff_mode:
    description: Runs the task to report the changes made or to be made.
    support: full
notes:
- Cross-provider group membership requires OneFS 9.11.0 or later.
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

- name: Add an LDAP user to a local group (cross-provider, requires OneFS 9.11+)
  dellemc.powerscale.group:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    provider_type: "local"
    access_zone: "{{access_zone}}"
    group_name: "{{group_name}}"
    users:
      - user_name: "{{ldap_user_name}}"
        provider_type: "ldap"
    user_state: "present-in-group"
    state: "present"

- name: Add mixed-provider members in a single task
  dellemc.powerscale.group:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    provider_type: "local"
    access_zone: "{{access_zone}}"
    group_name: "{{group_name}}"
    users:
      - user_name: "{{user_name}}"
      - user_name: "{{ldap_user_name}}"
        provider_type: "ldap"
    user_state: "present-in-group"
    state: "present"

- name: Remove an LDAP user from a local group
  dellemc.powerscale.group:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    provider_type: "local"
    access_zone: "{{access_zone}}"
    group_name: "{{group_name}}"
    users:
      - user_name: "{{ldap_user_name}}"
        provider_type: "ldap"
    user_state: "absent-in-group"
    state: "present"

- name: Check mode with diff - preview cross-provider membership changes
  dellemc.powerscale.group:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    provider_type: "local"
    access_zone: "{{access_zone}}"
    group_name: "{{group_name}}"
    users:
      - user_name: "{{ldap_user_name}}"
        provider_type: "ldap"
    user_state: "present-in-group"
    state: "present"
  check_mode: true
  diff: true
  register: result

- name: Backward-compatible legacy usage (no per-member provider_type)
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
    user_state: "present-in-group"
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
diff:
    description: The membership diff computed when diff mode is enabled.
    returned: When diff mode is active and membership changes are requested.
    type: dict
    contains:
        before:
            description: The group membership state before the operation.
            type: dict
            contains:
                members:
                    description: Sorted list of member names before the operation.
                    type: list
                    elements: str
        after:
            description: The group membership state after the operation.
            type: dict
            contains:
                members:
                    description: Sorted list of member names after the operation.
                    type: list
                    elements: str
    sample:
        {
            "before": {"members": ["Guest", "ldap_user"]},
            "after": {"members": ["Guest"]}
        }

'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils
import re

LOG = utils.get_logger('group')
GET_GROUP_ERR_MSG = "Get Group Details %s failed with %s"
# Cross-provider group membership requires OneFS to resolve a member by its
# unique id across authentication providers, supported from OneFS 9.11.0.
MIN_ONEFS_VERSION_CROSS_PROVIDER = '9.11.0'
VALID_PROVIDER_TYPES = ['local', 'file', 'ldap', 'ads', 'nis']


class Group(object):
    """Class with group operations"""

    def __init__(self):
        """ Define all parameters required by this module"""

        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_group_parameters())

        required_one_of = [['group_name', 'group_id']]
        # initialize the ansible module
        self.module = AnsibleModule(argument_spec=self.module_params,
                                    supports_check_mode=True,
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
        self.cluster_api_instance = utils.isi_sdk.ClusterApi(self.api_client)
        # Caches for the cross-provider preflight checks. Both are populated
        # lazily -- a playbook that never specifies a per-member provider_type
        # makes no additional API calls at all.
        self._providers_cache = {}
        self._members_cache = {}
        self._onefs_version_validated = False
        LOG.info('Got the isi_sdk instance for authorization on to PowerScale')

    def _get_providers_summary(self, access_zone):
        """Fetch the authentication providers configured in an access zone.

        The summary is cached per access zone so that a task adding several
        cross-provider members issues a single API call rather than one per
        member.

        :param access_zone: the access zone to inspect.
        :return: list of provider type names (e.g. ``['local', 'ldap']``).
        """
        if access_zone in self._providers_cache:
            return self._providers_cache[access_zone]
        try:
            api_response = self.api_instance.get_providers_summary(
                zone=access_zone)
            instances = api_response.to_dict().get('provider_instances') or []
            provider_types = [
                instance.get('type') for instance in instances
                if (instance.get('zone_name') or '').lower()
                == access_zone.lower()
                and instance.get('type')
            ]
            LOG.info("Providers configured in access zone %s: %s",
                     access_zone, provider_types)
            self._providers_cache[access_zone] = provider_types
            return provider_types
        except Exception as e:
            error = self.determine_error(error_obj=e)
            error_message = "Failed to fetch authentication providers for" \
                            " access zone '%s': %s" % (access_zone, error)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def _validate_onefs_version(self):
        """Validate that the cluster meets the minimum OneFS version.

        Cross-provider group membership relies on OneFS resolving a member by
        its unique id across providers, which is only supported from
        OneFS 9.11.0. The check runs once per module invocation.
        """
        if self._onefs_version_validated:
            return
        # fail_json raises SystemExit, which derives from BaseException and so
        # passes straight through `except Exception`. That lets the version
        # comparison live inside the try without the below-minimum failure
        # being mistaken for an unparseable release.
        try:
            api_response = self.cluster_api_instance.get_cluster_config()
            release = api_response.to_dict()['onefs_version']['release']
            # OneFS reports a dotted release such as "9.13.0.0"; some builds
            # prefix it with "v". The original string is kept for the error
            # message so it matches what the cluster and UI report.
            detected_version = utils.parse_version(str(release).lstrip('vV'))
            minimum_version = utils.parse_version(
                MIN_ONEFS_VERSION_CROSS_PROVIDER)
            LOG.info("Detected OneFS version %s", release)
            if detected_version < minimum_version:
                error_message = "OneFS version %s is below the required" \
                                " minimum %s for cross-provider group" \
                                " membership" \
                                % (release, MIN_ONEFS_VERSION_CROSS_PROVIDER)
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
        except Exception as e:
            error = self.determine_error(error_obj=e)
            error_message = "Failed to determine the OneFS version of the" \
                            " cluster: %s" % error
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
        self._onefs_version_validated = True

    def _validate_provider_exists(self, provider_type, access_zone):
        """Validate that a provider type is configured in the access zone.

        Fails the module before any membership API call is issued when the
        requested provider is not present in the target zone.

        :param provider_type: bare provider type (local, file, ldap, ads, nis).
        :param access_zone: the access zone the group lives in.
        """
        provider_types = self._get_providers_summary(access_zone)
        if provider_type not in provider_types:
            error_message = "Provider '%s' is not configured in access" \
                            " zone '%s'" % (provider_type, access_zone)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def _preflight_cross_provider(self, access_zone, member_provider):
        """Run the cross-provider preflight checks, if they are needed at all.

        This is the single gate for cross-provider behaviour. When a user dict
        omits ``provider_type`` the module resolves members exactly as it
        always has, so no validation call is made and existing playbooks incur
        no extra API traffic (NFR-1, NFR-2).

        The OneFS version is checked before provider existence: on a cluster
        that cannot support cross-provider membership at all, the version is
        the actionable error, and reporting a missing provider first would
        send the operator chasing the wrong problem.

        :param access_zone: the access zone the group lives in.
        :param member_provider: per-member provider type, or None when the
            member did not specify one.
        """
        if not member_provider:
            return
        self._validate_onefs_version()
        self._validate_provider_exists(member_provider, access_zone)

    def _resolve_member_id(self, user_name, user_id, provider_type, access_zone):
        """Resolve a user to its unique identity in a specific provider.

        Uses ``AuthApi.get_auth_user`` with the given provider so the cluster
        looks up the user in the correct authentication backend. Returns the
        SID string (e.g. ``SID:S-1-5-…``) that can be passed directly to the
        group-membership API.

        :param user_name: the human-readable user name, or ``None``.
        :param user_id:   the numeric UID as a string, or ``None``.
        :param provider_type: bare provider type (local, ldap, …).
        :param access_zone: the access zone the group lives in.
        :return: the user's ``SID:…`` identifier string.
        """
        auth_user_id = ("USER:" + user_name) if user_name else ("UID:" + user_id)
        display_name = user_name or user_id
        try:
            api_response = self.api_instance.get_auth_user(
                auth_user_id=auth_user_id,
                zone=access_zone, provider=provider_type)
            users = api_response.to_dict().get('users') or []
            if not users:
                error_message = "User '%s' could not be resolved in" \
                                " access zone '%s'" % (display_name, access_zone)
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
            resolved_id = users[0]['sid']['id']
            LOG.info("Resolved user '%s' in provider '%s' zone '%s' to %s",
                     display_name, provider_type, access_zone, resolved_id)
            return resolved_id
        except Exception as e:
            error = self.determine_error(error_obj=e)
            error_message = "Failed to resolve user '%s' in provider" \
                            " '%s', access zone '%s': %s" \
                            % (display_name, provider_type, access_zone, error)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def resolve_group_id(self, group_name, provider_type, access_zone):
        """Resolve a child group to its unique SID identifier.

        Uses ``AuthApi.get_auth_group`` with the given provider so the cluster
        looks up the group in the correct authentication backend. Returns the
        SID string (e.g. ``SID:S-1-5-…``) that can be passed directly to the
        group-membership API.

        :param group_name: the name of the child group to resolve.
        :param provider_type: bare provider type (local, file, ldap, ads, nis).
        :param access_zone: the access zone the parent group lives in.
        :return: the group's ``SID:…`` identifier string.
        """
        auth_group_id = "GROUP:" + group_name
        try:
            api_response = self.api_instance.get_auth_group(
                auth_group_id=auth_group_id,
                zone=access_zone, provider=provider_type)
            groups = api_response.to_dict().get('groups') or []
            if not groups:
                error_message = (
                    "Group '%s' could not be resolved in provider '%s'"
                    " in access zone '%s'"
                    % (group_name, provider_type, access_zone))
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
            resolved_id = groups[0]['sid']['id']
            LOG.info("Resolved group '%s' in provider '%s' zone '%s' to %s",
                     group_name, provider_type, access_zone, resolved_id)
            return resolved_id
        except Exception as e:
            error = self.determine_error(error_obj=e)
            error_message = (
                "Group '%s' could not be resolved in provider '%s'"
                " in access zone '%s': %s"
                % (group_name, provider_type, access_zone, error))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def add_group_member_to_group(self, group, resolved_id, member_name,
                                  access_zone, provider_type):
        """Add a child group to a parent group in PowerScale.

        Checks current membership first for idempotency. If the child group
        is already a member, returns False without making any API call.

        :param group: the parent group identifier (e.g. ``GROUP:parent``).
        :param resolved_id: the resolved SID of the child group.
        :param member_name: display name for logging.
        :param access_zone: the access zone.
        :param provider_type: the parent group's provider type.
        :return: True if the member was added, False if already present.
        """
        # Check current membership for idempotency
        current_members = self.get_group_members(group, access_zone,
                                                 provider_type)
        for member in (current_members or []):
            if member.get('name', '').lower() == member_name.lower():
                LOG.info("Group member '%s' is already in group %s",
                         member_name, group)
                return False
        LOG.info("Adding group member '%s' to group %s", member_name, group)
        if self.module.check_mode:
            LOG.info("Check mode: skipping create_group_member for %s",
                     member_name)
            return True
        group_member = utils.isi_sdk.AuthAccessAccessItemFileGroup(resolved_id)
        self.group_api_instance.create_group_member(
            group_member, group, zone=access_zone, provider=provider_type)
        self._invalidate_members_cache()
        return True

    def remove_group_member_from_group(self, group, resolved_id, member_name,
                                       access_zone, provider_type):
        """Remove a child group from a parent group in PowerScale.

        Checks current membership first for idempotency. If the child group
        is not a member, returns False without making any API call.

        :param group: the parent group identifier (e.g. ``GROUP:parent``).
        :param resolved_id: the resolved SID of the child group.
        :param member_name: display name for logging.
        :param access_zone: the access zone.
        :param provider_type: the parent group's provider type.
        :return: True if the member was removed, False if not present.
        """
        # Check current membership for idempotency
        current_members = self.get_group_members(group, access_zone,
                                                 provider_type)
        is_member = False
        for member in (current_members or []):
            if member.get('name', '').lower() == member_name.lower():
                is_member = True
                break
        if not is_member:
            LOG.info("Group member '%s' is not in group %s, nothing to remove",
                     member_name, group)
            return False
        LOG.info("Removing group member '%s' from group %s",
                 member_name, group)
        if self.module.check_mode:
            LOG.info("Check mode: skipping delete_group_member for %s",
                     member_name)
            return True
        self.group_api_instance.delete_group_member(
            resolved_id, group, zone=access_zone, provider=provider_type)
        self._invalidate_members_cache()
        return True

    def resolve_well_known_sid(self, value):
        """Resolve a well-known SID display name or SID string.

        Matches display names case-insensitively and SID strings exactly.

        :param value: a display name (e.g. ``"Everyone"``) or SID string
            (e.g. ``"S-1-1-0"``).
        :return: ``(sid_id, display_name)`` tuple where *sid_id* is the
            ``SID:…`` identifier and *display_name* is the canonical
            display name from the cluster.
        """
        wellknowns = self._get_wellknowns()
        # Try case-insensitive display name match first
        for wk in wellknowns:
            if wk['name'].lower() == value.lower():
                resolved = "SID:" + wk['sid']
                LOG.info("Resolved well-known SID '%s' to %s",
                         value, resolved)
                return resolved, wk['name']
        # Try exact SID string match
        for wk in wellknowns:
            if wk['sid'] == value:
                resolved = "SID:" + wk['sid']
                LOG.info("Resolved well-known SID string '%s' to %s",
                         value, resolved)
                return resolved, wk['name']
        error_message = ("'%s' is not a recognised well-known SID name"
                         " or SID string" % value)
        LOG.error(error_message)
        self.module.fail_json(msg=error_message)

    def add_wellknown_to_group(self, group, resolved_id, member_name,
                               access_zone, provider_type):
        """Add a well-known SID to a group in PowerScale.

        Checks current membership first for idempotency.

        :param group: the parent group identifier (e.g. ``GROUP:parent``).
        :param resolved_id: the resolved SID identifier (e.g. ``SID:S-1-1-0``).
        :param member_name: display name for logging.
        :param access_zone: the access zone.
        :param provider_type: the parent group's provider type.
        :return: True if the member was added, False if already present.
        """
        current_members = self.get_group_members(group, access_zone,
                                                 provider_type)
        for member in (current_members or []):
            if member.get('name', '').lower() == member_name.lower():
                LOG.info("Well-known SID '%s' is already in group %s",
                         member_name, group)
                return False
        LOG.info("Adding well-known SID '%s' to group %s",
                 member_name, group)
        if self.module.check_mode:
            LOG.info("Check mode: skipping create_group_member for %s",
                     member_name)
            return True
        group_member = utils.isi_sdk.AuthAccessAccessItemFileGroup(resolved_id)
        self.group_api_instance.create_group_member(
            group_member, group, zone=access_zone, provider=provider_type)
        self._invalidate_members_cache()
        return True

    def remove_wellknown_from_group(self, group, resolved_id, member_name,
                                    access_zone, provider_type):
        """Remove a well-known SID from a group in PowerScale.

        Checks current membership first for idempotency.

        :param group: the parent group identifier (e.g. ``GROUP:parent``).
        :param resolved_id: the resolved SID identifier.
        :param member_name: display name for logging.
        :param access_zone: the access zone.
        :param provider_type: the parent group's provider type.
        :return: True if the member was removed, False if not present.
        """
        current_members = self.get_group_members(group, access_zone,
                                                 provider_type)
        is_member = False
        for member in (current_members or []):
            if member.get('name', '').lower() == member_name.lower():
                is_member = True
                break
        if not is_member:
            LOG.info("Well-known SID '%s' is not in group %s,"
                     " nothing to remove", member_name, group)
            return False
        LOG.info("Removing well-known SID '%s' from group %s",
                 member_name, group)
        if self.module.check_mode:
            LOG.info("Check mode: skipping delete_group_member for %s",
                     member_name)
            return True
        self.group_api_instance.delete_group_member(
            resolved_id, group, zone=access_zone, provider=provider_type)
        self._invalidate_members_cache()
        return True

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
                error_message = GET_GROUP_ERR_MSG % (
                    group, self.determine_error(e))
                LOG.info(error_message)
                return None
            else:
                error_message = GET_GROUP_ERR_MSG % (
                    group, self.determine_error(e))
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

        except Exception as e:
            error_message = GET_GROUP_ERR_MSG % (
                group, self.determine_error(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_group_members(self, group, zone, provider):
        """Get the Group Member Details in PowerScale.

        Results are cached per ``(group, zone, provider)`` tuple so that
        multiple helpers (add/remove for groups, users, SIDs) share a
        single API call per invocation (NFR-1).
        """
        provider = 'local' if not provider else provider
        cache_key = (group, zone, provider)
        if cache_key in self._members_cache:
            LOG.info("Returning cached members for %s", group)
            return self._members_cache[cache_key]
        try:
            LOG.info("Getting members of group %s", group)
            api_response = self.group_api_instance.list_group_members(
                group, zone=zone, provider=provider)
            api_response_dict = api_response.to_dict()
            LOG.info("Group Members: %s", api_response_dict['members'])
            self._members_cache[cache_key] = api_response_dict['members']
            return api_response_dict['members']
        except Exception as e:
            error = self.determine_error(error_obj=e)
            error_message = "Get Users for group %s failed with %s" \
                            % (group, error)
            LOG.info(error_message)
            self.module.fail_json(msg=error_message)

    def _invalidate_members_cache(self):
        """Clear the members cache after a membership write operation."""
        self._members_cache.clear()

    def add_user_to_group(self, group, user,
                          zone, provider, cross_provider=False):
        """ Add a User to a Group in PowerScale """
        try:
            message = "Adding user %s to group %s" % (user, group)
            LOG.info(message)
            if self.module.check_mode:
                LOG.info("Check mode: skipping create_group_member for %s", user)
                return True
            group_member = utils.isi_sdk.AuthAccessAccessItemFileGroup(user)
            if cross_provider:
                api_response = self.group_api_instance.create_group_member(
                    group_member, group, zone=zone)
            else:
                provider = self.check_provider_type(provider, 'Add User to')
                api_response = self.group_api_instance.create_group_member(
                    group_member, group, zone=zone, provider=provider)
            LOG.info(api_response)
            self._invalidate_members_cache()
            return True
        except Exception as e:
            error = self.determine_error(error_obj=e)
            error_message = "Add user %s to group failed with %s " \
                            % (user, error)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def remove_user_from_group(self, group, user, zone, provider,
                               cross_provider=False):
        """ Remove a user from a Group in PowerScale"""
        try:
            message = "Removing user %s from group %s" % (user, group)
            LOG.info(message)
            if self.module.check_mode:
                LOG.info("Check mode: skipping delete_group_member for %s", user)
                return True
            if cross_provider:
                self.group_api_instance.delete_group_member(
                    user, group, zone=zone)
            else:
                provider = self.check_provider_type(provider, 'Remove User from')
                self.group_api_instance.delete_group_member(
                    user, group, zone=zone, provider=provider)
            self._invalidate_members_cache()
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
                     user_state, access_zone, provider_type,
                     member_provider=None):
        """Update the group members in PowerScale.

        :param member_provider: when set, the member is resolved via the
            cross-provider path (preflight + resolve to SID + add/remove
            without the ``provider`` query parameter). When ``None``, the
            legacy local-provider path is used (FR-6 backward compat).
        """
        changed = False
        if member_provider:
            # Cross-provider path: resolve the member in the requested
            # provider and use the unique SID for add/remove.
            self._preflight_cross_provider(access_zone, member_provider)
            resolved_id = self._resolve_member_id(
                user_name, user_id, member_provider, access_zone)
            # Check membership by matching the resolved name against the
            # current member list (fetched with the group's own provider).
            user_flag = self.is_user_part_of_group(
                group, user_name, user_id, access_zone, provider_type)
            if user_state == 'present-in-group' and not user_flag:
                changed = self.add_user_to_group(
                    group, resolved_id, access_zone, provider_type,
                    cross_provider=True)
            if user_state == 'absent-in-group' and user_flag:
                changed = self.remove_user_from_group(
                    group, resolved_id, access_zone, provider_type,
                    cross_provider=True)
        else:
            # Legacy path: resolve as USER:<name> or UID:<id>, scoped to
            # the group's own provider.
            user_flag = self.is_user_part_of_group(
                group, user_name, user_id, access_zone, provider_type)
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
        if group_name is not None and group_details['gid']['name'] is not None \
                and group_name.lower() == group_details['gid']['name'].lower():
            return False
        return True

    def _build_member_diff(self, group, access_zone, provider_type,
                           users, user_state):
        """Build the membership diff for the result when diff mode is active.

        Computes the *before* member list from the current group membership,
        and the *after* list by projecting the additions/removals described
        by ``users`` / ``user_state``, ``group_members`` /
        ``group_member_state``, and ``well_known_sids`` /
        ``well_known_sid_state``.

        :return: dict with ``before`` and ``after`` keys, each containing
            ``members``, ``group_members``, and ``well_known_sids`` lists.
            Returns ``None`` when diff mode is not active.
        """
        if not getattr(self.module, '_diff', False):
            return None
        current_members = self.get_group_members(
            group, access_zone, provider_type)

        # --- users diff (existing behaviour) ---
        before_names = [m.get('name', '') for m in (current_members or [])]
        after_names = list(before_names)
        for user in (users or []):
            if not isinstance(user, dict):
                continue
            name = user.get('user_name') or user.get('user_id', '')
            if user_state == 'present-in-group':
                if name.lower() not in [n.lower() for n in after_names]:
                    after_names.append(name)
            elif user_state == 'absent-in-group':
                after_names = [n for n in after_names
                               if n.lower() != name.lower()]

        # --- group_members diff ---
        group_members = self.module.params.get('group_members') or []
        group_member_state = self.module.params.get('group_member_state')
        before_groups = [
            m.get('name', '') for m in (current_members or [])
            if m.get('type') == 'group']
        after_groups = list(before_groups)
        for entry in group_members:
            if not isinstance(entry, dict):
                continue
            gname = entry.get('group_name', '')
            if group_member_state == 'present-in-group':
                if gname.lower() not in [g.lower() for g in after_groups]:
                    after_groups.append(gname)
            elif group_member_state == 'absent-in-group':
                after_groups = [g for g in after_groups
                                if g.lower() != gname.lower()]

        # --- well_known_sids diff ---
        well_known_sids = self.module.params.get('well_known_sids') or []
        wk_sid_state = self.module.params.get('well_known_sid_state')
        before_sids = [
            m.get('name', '') for m in (current_members or [])
            if m.get('type') == 'wellknown']
        after_sids = list(before_sids)
        for sid_value in well_known_sids:
            try:
                _, display_name = self.resolve_well_known_sid(sid_value)
            except SystemExit:
                continue
            if wk_sid_state == 'present-in-group':
                if display_name.lower() not in [
                        s.lower() for s in after_sids]:
                    after_sids.append(display_name)
            elif wk_sid_state == 'absent-in-group':
                after_sids = [s for s in after_sids
                              if s.lower() != display_name.lower()]

        return {
            'before': {
                'members': sorted(before_names),
                'group_members': sorted(before_groups),
                'well_known_sids': sorted(before_sids),
            },
            'after': {
                'members': sorted(after_names),
                'group_members': sorted(after_groups),
                'well_known_sids': sorted(after_sids),
            },
        }

    def _validate_group_params(self, group, users, user_state):
        """Validate group module input parameters."""
        if group is None:
            self.module.fail_json(msg="Invalid group_name or group_id provided.")
        if not users and user_state:
            self.module.fail_json(msg="'user_state' is given,"
                                      " 'users' are not specified")
        if not user_state and users:
            self.module.fail_json(msg="'user_state' is not specified,"
                                      " 'users' are given")
        # Validate group_members / group_member_state pairing
        group_members = self.module.params.get('group_members') or []
        group_member_state = self.module.params.get('group_member_state')
        if not group_members and group_member_state:
            self.module.fail_json(
                msg="'group_member_state' is given,"
                    " 'group_members' are not specified")
        if not group_member_state and group_members:
            self.module.fail_json(
                msg="'group_member_state' is not specified,"
                    " 'group_members' are given")
        # Validate well_known_sids / well_known_sid_state pairing
        well_known_sids = self.module.params.get('well_known_sids') or []
        well_known_sid_state = self.module.params.get('well_known_sid_state')
        if not well_known_sids and well_known_sid_state:
            self.module.fail_json(
                msg="'well_known_sid_state' is given,"
                    " 'well_known_sids' are not specified")
        if not well_known_sid_state and well_known_sids:
            self.module.fail_json(
                msg="'well_known_sid_state' is not specified,"
                    " 'well_known_sids' are given")

    def _validate_group_members_entries(self, group_members):
        """Validate each entry in the group_members list (FR-6.1).

        Each entry must be a dict with ``group_name`` (required) and optional
        ``provider_type``. No unsupported keys are allowed. Validation runs
        upfront before any write API call.
        """
        allowed_keys = {'group_name', 'provider_type'}
        for idx, entry in enumerate(group_members):
            if not isinstance(entry, dict):
                self.module.fail_json(
                    msg="group_members entry at index %d must be a dict,"
                        " got %s" % (idx, type(entry).__name__))
            unsupported = set(entry.keys()) - allowed_keys
            if unsupported:
                self.module.fail_json(
                    msg="group_members entry at index %d contains unsupported"
                        " keys. Supported keys are: group_name,"
                        " provider_type." % idx)
            if 'group_name' not in entry:
                self.module.fail_json(
                    msg="group_members entry at index %d is missing required"
                        " key 'group_name'" % idx)
            provider = entry.get('provider_type')
            if provider and provider not in VALID_PROVIDER_TYPES:
                self.module.fail_json(
                    msg="group_members entry at index %d has invalid"
                        " provider_type '%s'. Valid values are: %s."
                        % (idx, provider,
                           ', '.join(VALID_PROVIDER_TYPES)))

    def _validate_wellknown_sids_entries(self, well_known_sids):
        """Validate each entry in the well_known_sids list (FR-6.2).

        Each value is matched against ``GET /platform/1/auth/wellknowns``:
        display names are matched case-insensitively; SID strings must match
        exactly. Unrecognised values cause immediate failure before any write.
        """
        if not well_known_sids:
            return
        wellknowns = self._get_wellknowns()
        name_map = {wk['name'].lower(): wk for wk in wellknowns}
        sid_map = {wk['sid']: wk for wk in wellknowns}
        for value in well_known_sids:
            if value.lower() not in name_map and value not in sid_map:
                self.module.fail_json(
                    msg="'%s' is not a recognised well-known SID name"
                        " or SID string" % value)

    def _get_wellknowns(self):
        """Fetch and cache well-known SID personas from the cluster.

        :return: list of dicts with ``name`` and ``sid`` keys.
        """
        if hasattr(self, '_wellknowns_cache'):
            return self._wellknowns_cache
        try:
            api_response = self.api_instance.list_auth_wellknowns()
            self._wellknowns_cache = api_response.to_dict().get(
                'wellknowns') or []
            LOG.info("Fetched %d well-known SIDs",
                     len(self._wellknowns_cache))
            return self._wellknowns_cache
        except Exception as e:
            error = self.determine_error(error_obj=e)
            error_message = "Failed to fetch well-known SIDs: %s" % error
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def _process_user_entry(self, group, user, user_state, access_zone,
                            provider_type, index=0):
        """Validate and process a single user entry, return True if modified.

        :param index: zero-based position in the ``users`` list, used in
            error messages so the operator can pinpoint the problematic entry.
        """
        if not isinstance(user, dict):
            self.module.fail_json(
                msg="Key Value pair is allowed, Provided %s." % user)
        # Allow-list: user_name, user_id, and (new) provider_type.
        allowed_keys = {'user_name', 'user_id', 'provider_type'}
        unsupported = set(user.keys()) - allowed_keys
        if unsupported:
            self.module.fail_json(
                msg="User dict at index %d contains unsupported keys."
                    " Supported keys are: user_name, user_id, provider_type."
                    % index)
        # Exactly one identifier is required.
        has_name = 'user_name' in user
        has_id = 'user_id' in user
        if has_name and has_id:
            self.module.fail_json(
                msg="User dict at index %d must contain exactly one of"
                    " 'user_name' or 'user_id', not both." % index)
        if not has_name and not has_id:
            error = 'user_id or user_name  is expected,' \
                    ' "%s" given.' % list(user.keys())[0]
            self.module.fail_json(msg=error)
        # Validate per-member provider_type when supplied.
        member_provider = user.get('provider_type')
        if member_provider and member_provider not in VALID_PROVIDER_TYPES:
            self.module.fail_json(
                msg="User dict at index %d has invalid provider_type"
                    " '%s'. Valid values are: %s."
                    % (index, member_provider,
                       ', '.join(VALID_PROVIDER_TYPES)))
        if 'user_name' in user:
            return self.update_group(
                group, user['user_name'], None, user_state, access_zone,
                provider_type, member_provider=member_provider)
        return self.update_group(
            group, None, user['user_id'], user_state, access_zone,
            provider_type, member_provider=member_provider)

    def _process_group_members(self, group, group_members, group_member_state,
                               access_zone, provider_type):
        """Process group_members entries: resolve and add/remove child groups.

        :return: True if any membership changed, False otherwise.
        """
        changed = False
        for entry in group_members:
            child_name = entry['group_name']
            child_provider = entry.get('provider_type') or 'local'
            resolved_id = self.resolve_group_id(
                child_name, child_provider, access_zone)
            if group_member_state == 'present-in-group':
                if self.add_group_member_to_group(
                        group, resolved_id, child_name,
                        access_zone, provider_type):
                    changed = True
            elif group_member_state == 'absent-in-group':
                if self.remove_group_member_from_group(
                        group, resolved_id, child_name,
                        access_zone, provider_type):
                    changed = True
        return changed

    def _process_well_known_sids(self, group, well_known_sids,
                                  well_known_sid_state, access_zone,
                                  provider_type):
        """Process well_known_sids entries: resolve and add/remove SIDs.

        :return: True if any membership changed, False otherwise.
        """
        changed = False
        for sid_value in well_known_sids:
            resolved_id, display_name = self.resolve_well_known_sid(
                sid_value)
            if well_known_sid_state == 'present-in-group':
                if self.add_wellknown_to_group(
                        group, resolved_id, display_name,
                        access_zone, provider_type):
                    changed = True
            elif well_known_sid_state == 'absent-in-group':
                if self.remove_wellknown_from_group(
                        group, resolved_id, display_name,
                        access_zone, provider_type):
                    changed = True
        return changed

    def _handle_present_state(self, group, group_name, group_id, access_zone, provider_type, users, user_state):
        """Handle present state logic. Returns (changed, group_details)."""
        group_details = self.get_group_details(group, access_zone, provider_type)
        if not group_details:
            if not group_name:
                error_message = "Unable to create a group, 'group_name' is missing"
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
            LOG.info("Create a Group %s ", group_name)
            users_list = self.create_user_objects(users, user_state)
            self.create_group(group_name, group_id, access_zone, provider_type, users_list)
            return True

        if group_id and group_name:
            if self.check_if_id_exists(group_name, group_details):
                error_message = f'Group already exists with GID {group_id}'
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

        changed = False

        # Compute the membership diff before processing, so the diff
        # reflects the intended changes even in check mode.
        diff = self._build_member_diff(
            group, access_zone, provider_type, users, user_state)
        if diff is not None:
            self.result['diff'] = diff

        # Processing order: users -> group_members -> well_known_sids (FR-3.1)

        # Step 1: Process users (existing behaviour)
        if user_state and users:
            for idx, user in enumerate(users):
                if self._process_user_entry(group, user, user_state, access_zone, provider_type, index=idx):
                    changed = True

        # Step 2: Process group_members
        group_members = self.module.params.get('group_members') or []
        group_member_state = self.module.params.get('group_member_state')
        if group_member_state and group_members:
            if self._process_group_members(
                    group, group_members, group_member_state,
                    access_zone, provider_type):
                changed = True

        # Step 3: Process well_known_sids
        well_known_sids = self.module.params.get('well_known_sids') or []
        well_known_sid_state = self.module.params.get('well_known_sid_state')
        if well_known_sid_state and well_known_sids:
            if self._process_well_known_sids(
                    group, well_known_sids, well_known_sid_state,
                    access_zone, provider_type):
                changed = True

        return changed

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

        self._validate_group_params(group, users, user_state)
        # Upfront validation for group_members and well_known_sids (FR-6)
        group_members = self.module.params.get('group_members') or []
        if group_members:
            self._validate_group_members_entries(group_members)
        well_known_sids = self.module.params.get('well_known_sids') or []
        if well_known_sids:
            self._validate_wellknown_sids_entries(well_known_sids)

        changed = False
        if state == 'present':
            changed = self._handle_present_state(
                group, group_name, group_id, access_zone, provider_type, users, user_state)
        else:
            LOG.info("Delete Group %s  ", group_name or group_id)
            group_details = self.get_group_details(group, access_zone, provider_type)
            if group_details:
                changed = self.delete_group(group, access_zone, provider_type)

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
                        choices=['present-in-group', 'absent-in-group']),
        group_members=dict(required=False, type='list', elements='dict'),
        group_member_state=dict(required=False, type='str',
                                choices=['present-in-group',
                                         'absent-in-group']),
        well_known_sids=dict(required=False, type='list', elements='str'),
        well_known_sid_state=dict(required=False, type='str',
                                  choices=['present-in-group',
                                           'absent-in-group'])
    )


def main():
    """ Create PowerScale Group object and perform actions on it
        based on user input from playbook"""
    obj = Group()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
