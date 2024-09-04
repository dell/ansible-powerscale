#!/usr/bin/python
# Copyright: (c) 2021-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing ADS authentication provider on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ads

version_added: '1.2.0'

short_description: Manages the ADS authentication provider on PowerScale
description:
- Manages the Active Directory authentication provider on the PowerScale storage
  system.
- This includes adding spn, removing spn, fixing spn, checking spn, creating, modifying,
  deleting and retreiving the details of an ADS provider.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Jennifer John (@johnj9) <ansible.team@dell.com>
- Bhavneet Sharma (@Bhavneet-Sharma) <ansible.team@dell.com>

options:
  domain_name:
    description:
    - Specifies the domain name of an Active Directory provider.
    - This parameter is mandatory during create.
    type: str

  instance_name:
    description:
    - Specifies the instance name of Active Directory provider.
    - This is an optional parameter during create, and defaults to the provider
      name if it is not specified during the create operation.
    - Get, modify and delete operations can also be performed through
      instance_name.
    - It is mutually exclusive with I(domain_name) for get, modify and delete
      operations.
    type: str

  ads_user:
    description:
    - Specifies the user name that has permission to join a machine to the
      given domain.
    - This parameter is mandatory during create.
    type: str

  ads_password:
    description:
    - Specifies the password used during domain join.
    - This parameter is mandatory during create.
    type: str

  ads_parameters:
    description:
    - Specify additional parameters to configure ADS domain.
    type: dict
    suboptions:
      allocate_gids:
        description:
        - Allocates an ID for an unmapped Active Directory (ADS) group.
        - ADS groups without GIDs can be proactively assigned a GID by
          the ID mapper.
        - If the ID mapper option is disabled, GIDs are not proactively
          assigned, and when a primary group for a user does not include a
          GID, the system may allocate one.
        type: bool
        version_added: '3.4.0'
      allocate_uids:
        description:
        - Allocates a user ID for an unmapped Active Directory (ADS) user.
        - ADS users without UIDs can be proactively assigned a UID by the
          ID mapper.
        - IF the ID mapper option is disabled, UIDs are not proactively
          assigned, and when an identify for a user does not include a UID,
          the system may allocate one.
        type: bool
        version_added: '3.4.0'
      assume_default_domain:
        description:
        - Enables lookup of unqualified user names in the primary domain.
        type: bool
        version_added: '3.4.0'
      authentication:
        description:
        - Enables authentication and identity management through the
          authentication provider.
        type: bool
        version_added: '3.4.0'
      create_home_directory:
        description:
        - Automatically creates a home directory on the first login.
        type: bool
        version_added: '3.4.0'
      check_online_interval:
        description:
        - Specifies the time in seconds between provider online checks.
        type: int
        version_added: '3.4.0'
      controller_time:
        description:
        - Specifies the current time for the domain controllers.
        type: int
        version_added: '3.4.0'
      domain_offline_alerts:
        description:
        - Sends an alert if the domain goes offline.
        type: bool
        version_added: '3.4.0'
      extra_expected_spns:
        description:
        - List of additional SPNs to expect beyond what automatic checking
          routines might find.
        type: list
        elements: str
        version_added: '3.4.0'
      findable_groups:
        description:
        - Sets list of groups that can be resolved.
        type: list
        elements: str
        version_added: '3.4.0'
      findable_users:
        description:
        - Sets list of users that can be resolved.
        type: list
        elements: str
        version_added: '3.4.0'
      groupnet:
        description:
        - Groupnet identifier.
        - This is an optional parameter and defaults to C(groupnet0).
        type: str
      home_directory_template:
        description:
        - Specifies the path to the home directory template.
        - This is an optional parameter and defaults to C(/ifs/home/%D/%U).
        type: str
      ignore_all_trusts:
        description:
        - If set to true, ignores all trusted domains.
        type: bool
        version_added: '3.4.0'
      ignored_trusted_domains:
        description:
        - Includes trusted domains when I(ignore_all_trusts) is set to C(False).
        type: list
        elements: str
        version_added: '3.4.0'
      include_trusted_domains:
        description:
        - Includes trusted domains when 'ignore_all_trusts' is set to C(True).
        type: list
        elements: str
        version_added: '3.4.0'
      login_shell:
        description:
        - Specifies the login shell path.
        - This is an optional parameter and defaults to C(/bin/zsh).
        type: str
        choices: ['/bin/sh', '/bin/csh', '/bin/tcsh', '/bin/zsh', '/bin/bash',
                  '/bin/rbash', '/sbin/nologin']
      ldap_sign_and_seal:
        description:
        - Enables encryption and signing on LDAP requests.
        type: bool
        version_added: '3.4.0'
      lookup_groups:
        description:
        - Looks up AD groups in other providers before allocating a group ID.
        type: bool
        version_added: '3.4.0'
      lookup_normalize_groups:
        description:
        - Normalizes AD group names to lowercase before look up.
        type: bool
        version_added: '3.4.0'
      lookup_normalize_users:
        description:
        - Normalize AD user names to lowercase before look up.
        type: bool
        version_added: '3.4.0'
      lookup_users:
        description:
        - Looks up AD users in other providers before allocating a user ID.
        type: bool
        version_added: '3.4.0'
      lookup_domains:
        description:
        - Limits user and group lookups to the specified domains.
        type: list
        elements: str
        version_added: '3.4.0'
      machine_account:
        description:
        - Specifies the machine account name when creating a SAM account with Active Directory.
        - The default cluster name is called C(default).
        type: str
      machine_password_changes:
        description:
        - Enables periodic changes of the machine password for security.
        type: bool
        version_added: '3.4.0'
      machine_password_lifespan:
        description:
        - Sets maximum age of a password in seconds.
        type: int
        version_added: '3.4.0'
      nss_enumeration:
        description:
        - Enables the Active Directory provider to respond to 'getpwent'
          and 'getgrent' requests.
        type: bool
        version_added: '3.4.0'
      organizational_unit:
        description:
        - Specifies the organizational unit.
        type: str
      restrict_findable:
        description:
        - Check the provider for filtered lists of findable and
          unfindable users and groups.
        type: bool
        version_added: '3.4.0'
      rpc_call_timeout:
        description:
        - The maximum amount of time (in seconds) an RPC call to
          Active Directory is allowed to take.
        type: int
        version_added: '3.4.0'
      store_sfu_mappings:
        description:
        - Stores SFU mappings permanently in the ID mapper.
        type: bool
        version_added: '3.4.0'
      server_retry_limit:
        description:
        - The number of retries attempted when a call to Active
          Directory fails due to network error.
        type: int
        version_added: '3.4.0'
      sfu_support:
        description:
        - Specifies whether to support RFC 2307 attributes on ADS domain
          controllers.
        type: str
        choices: ['none', 'rfc2307']
        version_added: '3.4.0'
      unfindable_groups:
        description:
        - Specifies groups that cannot be resolved by the provider.
        type: list
        elements: str
        version_added: '3.4.0'
      unfindable_users:
        description:
        - Specifies users that cannot be resolved by the provider.
        type: list
        elements: str
        version_added: '3.4.0'
  spns:
    description: List of SPN's to configure.
    type: list
    elements: dict
    suboptions:
        spn:
          description:
          - Service Principle Name(SPN).
          type: str
          required: true
        state:
          description:
          - The state of the SPN.
          - C(present) - indicates that the SPN should exist on the machine account.
          - C(absent) - indicates that the SPN should not exist on the machine account.
          type: str
          choices: ['absent', 'present']
          default: 'present'
  spn_command:
    description:
    - Specify command of SPN.
    - C(check) - Check for missing SPNs for an AD provider.
    - C(fix) - Adds missing SPNs for an AD provider.
    type: str
    choices: ['check', 'fix']
  state:
    description:
    - The state of the ads provider after the task is performed.
    - C(present) - indicates that the ADS provider should exist on the system.
    - C(absent) - indicates that the ADS provider should not exist on the system.
    choices: ['absent', 'present']
    type: str
    required: true
attributes:
  check_mode:
    description:
    - Runs task to validate without performing action on the target machine.
    support: full
  diff_mode:
    description:
    - Runs the task to report the changes made or to be made.
    support: full
'''

EXAMPLES = r'''
- name: Add an Active Directory provider
  dellemc.powerscale.ads:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    domain_name: "ansibleneo.com"
    instance_name: "ansibleneo.com"
    ads_user: "administrator"
    ads_password: "*****"
    ads_parameters:
      groupnet: "groupnet5"
      home_directory_template: "/ifs/home/%D/%U"
      login_shell: "/bin/zsh"
      machine_account: "test_account"
      organizational_unit: "org/sub_org"
      allocate_gids: true
      allocate_uids: false
      assume_default_domain: false
      authentication: true
      create_home_directory: true
      domain_offline_alerts: true
      ignore_all_trusts: true
      ignored_trusted_domains:
        - "example.com"
        - "example1.com"
      include_trusted_domains:
        - "trusted.com"
      ldap_sign_and_seal: true
      lookup_groups: true
      lookup_normalize_groups: true
      lookup_normalize_users: true
      lookup_users: true
      machine_password_changes: true
      nss_enumeration: true
      restrict_findable: true
      store_sfu_mappings: true
      check_online_interval: 7600
      controller_time: 760000
      machine_password_lifespan: 34567
      rpc_call_timeout: 45
      server_retry_limit: 789
      sfu_support: "rfc2307"
      extra_expected_spns:
        - span
      findable_groups:
        - "groupone"
      findable_users:
        - "userone"
      lookup_domains:
        - "example.com"
      unfindable_groups:
        - "nogroups"
      unfindable_users:
        - "nouser"
    state: "present"

- name: Modify an Active Directory provider with domain name
  dellemc.powerscale.ads:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    domain_name: "ansibleneo.com"
    ads_parameters:
      home_directory_template: "/ifs/usr_home/%D/%U"
      login_shell: "/bin/rbash"
    state: "present"

- name: Modify an Active Directory provider with instance name
  dellemc.powerscale.ads:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    instance_name: "ansibleneo.com"
    ads_parameters:
      home_directory_template: "/ifs/usr_home/%D/%U"
      login_shell: "/bin/rbash"
      allocate_gids: false
      allocate_uids: true
      assume_default_domain: true
      authentication: false
    state: "present"

- name: Get Active Directory provider details with domain name
  dellemc.powerscale.ads:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    domain_name: "ansibleneo.com"
    state: "present"

- name: Add an SPN
  dellemc.powerscale.ads:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    domain_name: "ansibleneo.com"
    spns:
      - spn: "HOST/test1"
    state: "present"

- name: Remove an SPN
  dellemc.powerscale.ads:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    domain_name: "ansibleneo.com"
    spns:
      - spn: "HOST/test1"
        state: "absent"
    state: "present"

- name: Check an SPN
  dellemc.powerscale.ads:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    domain_name: "ansibleneo.com"
    spn_command: "check"
    state: "present"

- name: Fix an SPN
  dellemc.powerscale.ads:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    domain_name: "ansibleneo.com"
    spn_command: "fix"
    state: "present"

- name: Get Active Directory provider details with instance name
  dellemc.powerscale.ads:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    instance_name: "ansibleneo.com"
    state: "present"

- name: Delete an Active Directory provider with domain name
  dellemc.powerscale.ads:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    domain_name: "ansibleneo.com"
    state: "absent"

- name: Delete an Active Directory provider with instance name
  dellemc.powerscale.ads:
    onefs_host: "{{onefs_host}}"
    verify_ssl: "{{verify_ssl}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    instance_name: "ansibleneo.com"
    state: "absent"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
    sample: "false"

spn_check:
    description: Missing SPNs for an AD provider.
    returned: When check operation is done.
    type: list
    sample: ['host/test1']

ads_provider_details:
    description: The Active Directory provider details.
    returned: When Active Directory provider exists
    type: complex
    contains:
        allocate_gids:
            description: Allocates an ID for an unmapped Active Directory (ADS)
                         group.
            type: bool
        allocate_uids:
            description: Allocates an ID for an unmapped Active Directory (ADS)
                         user.
            type: bool
        assume_default_domain:
            description: Enables lookup of unqualified user names in the
                         primary domain.
            type: bool
        authentication:
            description: Enables authentication and identity management
                         through the authentication provider.
            type: bool
        check_online_interval:
            description: Specifies the time in seconds between provider online checks.
            type: int
        controller_time:
            description: Specifies the current time for the domain controllers.
            type: int
        create_home_directory:
            description: Automatically creates a home directory on the first login.
            type: bool
        domain_offline_alerts:
            description: Sends an alert if the domain goes offline.
            type: bool
        dup_spns:
            description: Get duplicate SPNs in the provider domain.
            type: list
        extra_expected_spns:
            description: List of additional SPNs to expect beyond what automatic
                         checking routines might find.
            type: list
        findable_groups:
            description: Sets list of groups that can be resolved.
            type: list
        findable_users:
            description: Sets list of users that can be resolved.
            type: list
        forest:
            description: Specifies the Active Directory forest.
            type: str
        groupnet:
            description: Groupnet identifier.
            type: str
        home_directory_template:
            description: Specifies the path to the home directory template.
            type: str
        hostname:
            description: Specifies the fully qualified hostname stored in the
                         machine account.
            type: str
        id:
            description: Specifies the ID of the Active Directory provider
                         instance.
            type: str
        ignore_all_trusts:
            description: If set to C(true), ignores all trusted domains.
            type: bool
        ignored_trusted_domains:
            description: Includes trusted domains when I(ignore_all_trusts) is
                         set to C(false.)
            type: list
        include_trusted_domains:
            description: Includes trusted domains when I(ignore_all_trusts) is
                         set to C(true.)
            type: list
        instance:
            description: Specifies Active Directory provider instance.
            type: str
        ldap_sign_and_seal:
            description: Enables encryption and signing on LDAP requests.
            type: bool
        login_shell:
            description: Specifies the login shell path.
            type: str
        lookup_domains:
            description: Limits user and group lookups to the specified domains.
            type: list
        linked_access_zones:
            description: List of access zones linked to the authentication
                         provider.
            type: list
        lookup_groups:
            description: Looks up AD groups in other providers before allocating
                         a group ID.
            type: bool
        lookup_normalize_groups:
            description: Normalizes AD group names to lowercase before look up.
            type: bool
        lookup_normalize_users:
            description: Normalizes AD user names to lowercase before look up.
            type: bool
        lookup_users:
            description: Looks up AD users in other providers before allocating
                         a user ID.
            type: bool
        machine_account:
            description: Specifies the machine account name when creating a
                         SAM account with Active Directory.
            type: str
        machine_password_changes:
            description: Enables periodic changes of the machine password for
                         security.
            type: bool
        machine_password_lifespan:
            description: Sets maximum age of a password in seconds.
            type: int
        name:
            description: Specifies the Active Directory provider name.
            type: str
        netbios_domain:
            description: Specifies the NetBIOS domain name associated with
                         the machine account.
            type: str
        node_dc_affinity:
            description: Specifies the domain controller for which the node
                         has affinity.
            type: str
        node_dc_affinity_timeout:
            description: pecifies the timeout for the domain controller for which
                         the local node has affinity.
            type: int
        nss_enumeration:
            description: Enables the Active Directory provider to respond to
                         'getpwent' and 'getgrent' requests.
            type: bool
        primary_domain:
            description: Specifies the AD domain to which the provider is joined.
            type: str
        restrict_findable:
            description: Check the provider for filtered lists of findable and
                         unfindable users and groups.
            type: bool
        rpc_call_timeout:
            description: The maximum amount of time (in seconds) an RPC call to
                         Active Directory is allowed to take.
            type: int
        server_retry_limit:
            description: The number of retries attempted when a call to Active
                         Directory fails due to network error.
            type: int
        sfu_support:
            description: Specifies whether to support RFC 2307 attributes on
                         ADS domain controllers.
            type: str
        site:
            description: Specifies the site for the Active Directory.
            type: str
        status:
            description: Specifies the status of the provider.
            type: str
        store_sfu_mappings:
            description: Stores SFU mappings permanently in the ID mapper.
            type: bool
        system:
            description: If set to C(true), indicates that this provider instance
                         was created by OneFS and cannot be removed.
            type: bool
        unfindable_groups:
            description: Sets list of groups that cannot be resolved.
            type: list
        unfindable_users:
            description: Sets list of users that cannot be resolved.
            type: list
        zone_name:
            description: Specifies the name of the access zone in which this provider was created.
            type: str
        recommended_spns:
            description: Configuration recommended SPNs.
            type: list
        spns:
            description: Currently configured SPNs.
            type: list
    sample:
        {
            "ads_provider_details": [
                {
                    "allocate_gids": true,
                    "allocate_uids": true,
                    "assume_default_domain": false,
                    "authentication": true,
                    "check_online_interval": 300,
                    "controller_time": 1725339127,
                    "create_home_directory": false,
                    "domain_offline_alerts": false,
                    "extra_expected_spns": [
                        "HOST/test5"
                    ],
                    "findable_groups": [],
                    "findable_users": [],
                    "forest": "sample.emc.com",
                    "groupnet": "groupnet0",
                    "home_directory_template": "/ifs/home/%D/%U",
                    "hostname": "sample.emc.com",
                    "id": "SAMPLE.COM",
                    "ignore_all_trusts": false,
                    "ignored_trusted_domains": [],
                    "include_trusted_domains": [],
                    "instance": "",
                    "ldap_sign_and_seal": false,
                    "linked_access_zones": [
                        "System"
                    ],
                    "login_shell": "/bin/zsh",
                    "lookup_domains": [],
                    "lookup_groups": true,
                    "lookup_normalize_groups": true,
                    "lookup_normalize_users": true,
                    "lookup_users": true,
                    "machine_account": "PI98S$$",
                    "machine_password_changes": true,
                    "machine_password_lifespan": 31536000,
                    "name": "SAMPLE.COM",
                    "netbios_domain": "PIERTP",
                    "node_dc_affinity": null,
                    "node_dc_affinity_timeout": null,
                    "nss_enumeration": false,
                    "primary_domain": "SAMPLE.COM",
                    "recommended_spns": [
                        "HOST/test1",
                        "HOST/test2",
                        "HOST/test3",
                        "HOST/test4"
                    ],
                    "restrict_findable": false,
                    "sfu_support": "none",
                    "site": "Default-First-Site-Name",
                    "spns": [
                        "HOST/test2",
                        "HOST/test3",
                        "HOST/test4",
                        "HOST/test5"
                    ],
                    "status": "online",
                    "store_sfu_mappings": false,
                    "system": false,
                    "unfindable_groups": [],
                    "unfindable_users": [],
                    "zone_name": "System"
                }
            ]
        }
'''

import re
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('ads')


class Ads(object):
    """Class with Active Directory provider operations"""

    def __init__(self):
        """ Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_ads_parameters())

        required_one_of = [['domain_name', 'instance_name']]
        # initialize the Ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=True,
            required_one_of=required_one_of
        )

        # result is a dictionary that contains changed status
        self.result = {"changed": False}
        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params, "ads")
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.auth_api_instance = utils.isi_sdk.AuthApi(self.api_client)
        self.zones_api_instance = utils.isi_sdk.ZonesApi(self.api_client)
        LOG.info('Got the isi_sdk instance for authorization on to PowerScale')

    def get_ads_details(self, ads_name):
        """
        Get the details of the Active Directory provider.
        :param ads_name: Specifies the Active Directory provider name.
        :return: if exists returns details of the Active Directory provider
        else returns None.
        """
        try:
            ads_api_response = []
            for name in ads_name:
                api_response = self.auth_api_instance.get_providers_ads_by_id(
                    name)
                ads_api_response.append(api_response.ads[0].to_dict())

            return ads_api_response
        except utils.ApiException as e:
            if str(e.status) == '404':
                error_message = "ADS provider {0} details are not found".\
                    format(ads_name)
                LOG.info(error_message)
                return None
            else:
                error_message = 'Get details of ADS provider {0} failed with ' \
                                'error: {1}'.format(ads_name,
                                                    utils.determine_error
                                                    (error_obj=e))
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)
        except Exception as e:
            error_message = 'Get details of ADS provider {0} failed with ' \
                            'error: {1}'.format(ads_name,
                                                utils.determine_error
                                                (error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def create(self, domain, instance, ads_user, ads_password, ads_parameters):
        """
        Add an Active Directory provider.
        :param domain: Specifies the Active Directory provider name.
        :param instance: Specifies Active Directory provider instance.
        :param ads_user: Specifies the user name that has permission to join a
         machine to the given domain.
        :param ads_password: Specifies the password used during domain join.
        :param ads_parameters: Specify additional parameters to configure
         ADS domain.
        :return: ADS Id.
        """
        self.validate_create_params(domain, ads_user, ads_password, ads_parameters)
        ads_create_params = {
            'name': domain, 'user': ads_user,
            'password': ads_password
        }

        if instance:
            ads_create_params['instance'] = instance

        if ads_parameters:
            for key in ads_parameters:
                if ads_parameters[key]:
                    ads_create_params[key] = ads_parameters[key]

        ads_provider_obj = utils.isi_sdk.ProvidersAdsItem(**ads_create_params)
        try:
            api_response = self.auth_api_instance.create_providers_ads_item(
                providers_ads_item=ads_provider_obj)
            message = "ADS domain created, %s" % api_response
            LOG.info(message)
            return api_response
        except utils.ApiException as e:
            error_message = "Add an Active Directory provider failed with" + \
                utils.determine_error(error_obj=e)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def update(self, ads_name, modified_ads):
        """
         Modify the details of the Active Directory provider.
        :param ads_name: Specifies the Active Directory provider name.
        :param modified_ads: Parameters to modify.
        :return: True if the operation is successful.
        """
        ads_update_params = {}

        try:
            for key in modified_ads:
                ads_update_params[key] = modified_ads[key]

            ads_provider_params = utils.isi_sdk.ProvidersAdsIdParams(
                **ads_update_params)

            self.auth_api_instance.update_providers_ads_by_id(
                providers_ads_id_params=ads_provider_params,
                providers_ads_id=ads_name)
            message = "ADS provider updated successfully."
            LOG.info(message)
            return True
        except utils.ApiException as e:
            error_message = "Modifying ADS provider failed with" + \
                utils.determine_error(error_obj=e)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete(self, ads_name, domain, instance):
        """
         Delete the ADS provider.
        :param ads_name: Specifies the Active Directory provider name.
        :param domain: Specifies the Active Directory provider name.
        :param instance: Specifies Active Directory provider instance.
        :return: True if the operation is successful.
        """
        try:
            self.auth_api_instance.delete_providers_ads_by_id(ads_name)
            return True
        except utils.ApiException as e:
            error_message = "Deleting ADS provider failed with" + \
                utils.determine_error(error_obj=e)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def update_extra_expected_spns(self, operation, spn, extra_expected_spns, recommended_spns):
        """
        :param operation: Add or remove SPN.
        :param spn: SPN
        :param extra_expected_spns: Extra expected SPN's.
        :param recommended_spns: Recommended SPN's.
        :return: Extra expected SPN's.
        """
        if operation == 'add' and spn not in recommended_spns and spn not in extra_expected_spns:
            extra_expected_spns.append(spn)
        elif operation == 'remove' and spn in extra_expected_spns:
            extra_expected_spns.remove(spn)
        return extra_expected_spns

    def get_spns_not_in_recommended_spns(self, spns, recommended_spns):
        """
        :param spns: List of SPN's
        :param recommended_spns: Recommended SPN's.
        :return: List of SPN's.
        """
        list_difference = [spn for spn in recommended_spns if spn not in spns]
        return list_difference

    def perform_spn_operation(self, array_ads):
        """
        :param array_ads: ADS dictionary returned from the PowerScale array.
        :return: Whether ADS is modified, SPN's list and extra expected SPN's list.
        """
        spns = self.module.params['spns'] if self.module.params['spns'] else []
        existing_spns = array_ads[0]['spns']
        extra_expected_spns = array_ads[0]['extra_expected_spns']
        recommended_spns = array_ads[0]['recommended_spns']
        spn_command = self.module.params['spn_command']
        modified = False
        for spn in spns:
            if spn['state'] == 'present' and spn['spn'] not in existing_spns:
                existing_spns.append(spn['spn'])
                extra_expected_spns = self.update_extra_expected_spns('add', spn['spn'], extra_expected_spns, recommended_spns)
                modified = True
            elif spn['state'] == 'absent' and spn['spn'] in existing_spns:
                existing_spns.remove(spn['spn'])
                extra_expected_spns = self.update_extra_expected_spns('remove', spn['spn'], extra_expected_spns, recommended_spns)
                modified = True
        if spn_command == 'fix':
            spn_difference = self.get_spns_not_in_recommended_spns(existing_spns, recommended_spns)
            if spn_difference != []:
                existing_spns.extend(spn_difference)
                modified = True
        return modified, existing_spns, extra_expected_spns

    def get_modified_ads(self, input_ads, array_ads):
        """
        :param input_ads: ADS dictionary passed by the user.
        :param array_ads: ADS dictionary returned from the PowerScale array.
        :return: ADS dictionary with values that are modified.
        """
        for key in list(input_ads):
            if key in ("groupnet", "machine_account"):
                if key == 'machine_account' and input_ads[key]:
                    input_ads[key] = input_ads[key] + '$'
                if input_ads[key] and \
                        input_ads[key].lower() != array_ads[0][key].lower():
                    self.module.fail_json(msg="Modification of %s"
                                          " is not supported." % key)
                del input_ads[key]
            elif key == 'organizational_unit' or \
                    (not input_ads[key] or
                     input_ads[key] == array_ads[0][key]):
                del input_ads[key]

        return input_ads

    def get_auth_providers_summary(self):
        """Get Auth providers summary"""
        try:
            providers_summary_api_response = \
                self.auth_api_instance.get_providers_summary()
            providers_summary = \
                providers_summary_api_response.provider_instances

            return providers_summary
        except utils.ApiException as e:
            error_message = "Get auth providers summary failed with" + \
                utils.determine_error(error_obj=e)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def update_ads_access_zone_info(self, ads_name, ads_details):
        """Update ADS with access zone details"""
        try:
            zone_api_response = self.zones_api_instance.list_zones()
            if zone_api_response:
                providers_summary = self.get_auth_providers_summary()
                for name in ads_name:
                    provider_ids = [provider.id for provider in
                                    providers_summary if provider.type == "ads" and
                                    provider.name.lower() == name.lower()]
                    zone_ids = []
                    if provider_ids:
                        zone_ids = [zone.id for zone in zone_api_response.zones
                                    if set(provider_ids).issubset(
                                        zone.auth_providers)]
                    [ads_detail.update(linked_access_zones=zone_ids)
                        for ads_detail in ads_details
                        if ads_detail['id'].lower() == name.lower()]

        except utils.ApiException as e:
            error_message = "Update ADS with access zone details " \
                "failed with" + utils.determine_error(error_obj=e)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def validate_create_params(self, domain, ads_user, ads_password, ads_parameters):
        """Validates parameters for ADS create"""
        if not domain:
            self.module.fail_json(msg="The parameter domain_name is mandatory "
                                      "while creating ADS provider")

        if not ads_user:
            self.module.fail_json(msg="The parameter ads_user is mandatory "
                                      "while creating ADS provider")

        if not ads_password:
            self.module.fail_json(msg="The parameter ads_password is mandatory "
                                      "while creating ADS provider")

        if ads_parameters and 'machine_account' in ads_parameters and \
                ads_parameters['machine_account'] is not None \
                and utils.is_input_empty(ads_parameters['machine_account']):
            self.module.fail_json(msg="Please specify a valid machine_account")

        if ads_parameters and 'organizational_unit' in ads_parameters and \
                ads_parameters['organizational_unit'] is not None \
                and utils.is_input_empty(ads_parameters['organizational_unit']):
            self.module.fail_json(msg="Please specify a valid organizational_unit")

        regexp = re.compile(r'^(?!\.)(?!.*?\.\.)[0-9a-zA-Z.]*$(?<!\.)')
        if not regexp.search(domain):
            self.module.fail_json(msg='The value for domain_name is invalid')

    def validate_input(self, ads_details, domain, instance):
        """Validate input parameters"""
        if domain and instance:
            self.module.fail_json(
                msg="parameters are mutually exclusive: "
                    "domain_name|instance_name")

        if not domain and not instance:
            self.module.fail_json(msg="Please specify domain_name "
                                  "or instance_name")

        if ads_details and len(ads_details) > 1:
            self.module.fail_json(
                msg="Multiple ADS instances are returned for the given "
                    "domain_name. Please specify instance_name")

    def perform_module_operation(self):
        """
        Perform different actions on ADS module based on parameters
        chosen in playbook
        """
        ads_user = self.module.params['ads_user']
        ads_password = self.module.params['ads_password']
        domain = self.module.params['domain_name']
        instance = self.module.params['instance_name']
        ads_parameters = self.module.params['ads_parameters']
        spn_command = self.module.params['spn_command']
        ads_name = []

        if instance and not domain:
            ads_name.insert(0, instance)
        else:
            providers_summary = self.get_auth_providers_summary()
            if instance and domain:
                provider_summary = [provider for provider in
                                    providers_summary
                                    if provider.type == 'ads'
                                    and provider.forest.lower() == domain.lower()
                                    and provider.name.lower() == instance.lower()]
                for provider in provider_summary:
                    ads_name.append(provider.name)
            elif domain:
                provider_summary = [provider for provider in
                                    providers_summary
                                    if provider.type == 'ads'
                                    and provider.forest.lower() == domain.lower()]
                for provider in provider_summary:
                    ads_name.append(provider.name)

        ads_details = self.get_ads_details(ads_name)
        state = self.module.params['state']
        changed = False

        # Add an Active Directory provider
        if state == "present" and not ads_details:
            LOG.info("Add an Active Directory provider..")
            ads_create_response = self.create(domain, instance, ads_user,
                                              ads_password, ads_parameters)
            ads_name.insert(0, ads_create_response.id)
            changed = True

        # Modify an Active Directory provider
        check_modification = ads_parameters or self.module.params['spns'] or spn_command == 'fix'
        if state == "present" and ads_details and check_modification:
            modified_ads = {}
            if ads_parameters:
                modified_ads = self.get_modified_ads(ads_parameters, ads_details)
            is_spn_modified, spns, extra_spns = self.perform_spn_operation(ads_details)
            if is_spn_modified:
                modified_ads['spns'] = spns
                modified_ads['extra_expected_spns'] = extra_spns
            if modified_ads:
                LOG.info('Modifying ADS provider..')
                self.validate_input(ads_details, domain, instance)
                changed = self.update(ads_name[0], modified_ads)

        # Delete an Active Directory provider
        if state == "absent":
            self.validate_input(ads_details, domain, instance)
            if ads_details:
                LOG.info('Deleting ADS provider..')
                changed = self.delete(ads_name[0], domain, instance)

        ads_details = self.get_ads_details(ads_name)
        if ads_details:
            self.update_ads_access_zone_info(ads_name, ads_details)
        self.result["changed"] = changed
        self.result["ads_provider_details"] = ads_details
        if spn_command == 'check' and ads_details:
            self.result["spn_check"] = self.get_spns_not_in_recommended_spns(ads_details[0]['spns'],
                                                                             ads_details[0]['recommended_spns'])
        self.module.exit_json(**self.result)


def get_ads_parameters():
    """
    This method provides parameters required for the ansible ADS auth
    module on PowerScale
    """
    return dict(
        domain_name=dict(type='str'),
        instance_name=dict(type='str'),
        ads_user=dict(type='str'),
        ads_password=dict(type='str', no_log=True),
        ads_parameters=dict(
            type='dict', options=dict(
                groupnet=dict(type='str'),
                home_directory_template=dict(type='str'),
                login_shell=dict(type='str', choices=['/bin/sh', '/bin/csh',
                                                      '/bin/tcsh', '/bin/zsh',
                                                      '/bin/bash',
                                                      '/bin/rbash',
                                                      '/sbin/nologin']),
                machine_account=dict(type='str'),
                organizational_unit=dict(type='str'),
                allocate_gids=dict(type='bool'),
                allocate_uids=dict(type='bool'),
                assume_default_domain=dict(type='bool'),
                authentication=dict(type='bool'),
                check_online_interval=dict(type='int'),
                controller_time=dict(type='int'),
                create_home_directory=dict(type='bool'),
                domain_offline_alerts=dict(type='bool'),
                ignore_all_trusts=dict(type='bool'),
                ignored_trusted_domains=dict(type='list', elements='str'),
                include_trusted_domains=dict(type='list', elements='str'),
                ldap_sign_and_seal=dict(type='bool'),
                lookup_groups=dict(type='bool'),
                lookup_normalize_groups=dict(type='bool'),
                lookup_normalize_users=dict(type='bool'),
                lookup_users=dict(type='bool'),
                machine_password_changes=dict(type='bool'),
                nss_enumeration=dict(type='bool'),
                restrict_findable=dict(type='bool'),
                store_sfu_mappings=dict(type='bool'),
                machine_password_lifespan=dict(type='int', no_log=False),
                rpc_call_timeout=dict(type='int'),
                server_retry_limit=dict(type='int'),
                sfu_support=dict(type='str', choices=['none', 'rfc2307']),
                extra_expected_spns=dict(type='list', elements='str'),
                findable_groups=dict(type='list', elements='str'),
                findable_users=dict(type='list', elements='str'),
                lookup_domains=dict(type='list', elements='str'),
                unfindable_groups=dict(type='list', elements='str'),
                unfindable_users=dict(type='list', elements='str'),
            )
        ),
        spns=dict(
            type='list', elements='dict', options=dict(
                spn=dict(type='str', required=True),
                state=dict(type='str', choices=['present', 'absent'], default='present')
            )
        ),
        spn_command=dict(type='str', choices=['check', 'fix']),
        state=dict(required=True, type='str', choices=['present', 'absent'])
    )


def main():
    """ Create PowerScale ADS object and perform action on it
        based on user input from playbook"""
    obj = Ads()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
