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
        """ Define all parameters required by Active Directory provider module"""

        self.result = {"changed": False}
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(self.get_ads_parameters())
        required_one_of = [['domain_name', 'instance_name']]
        # initialize the Ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=True,
            required_one_of=required_one_of
        )

        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.auth_api_instance = utils.isi_sdk.AuthApi(self.api_client)
        self.zones_api_instance = utils.isi_sdk.ZonesApi(self.api_client)
        LOG.info('Got the isi_sdk instance for authorization on to PowerScale')

        # result is a dictionary that contains changed status
        self.result.update({
            "changed": False,
            "ads_provider_details": {},
            "diff": {}
        })
        self.ads_name = []

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
                api_response = utils.get_ads_provider_details(
                    user=self.module.params['api_user'],
                    password=self.module.params['api_password'],
                    hostname=self.module.params['onefs_host'],
                    port=self.module.params['port_no'],
                    ads_provider_name=name,
                    validate_certs=self.module.params['verify_ssl'],
                )
                ads_api_response.append(api_response['ads'][0])

            return ads_api_response
        except Exception as e:
            if "404" in str(e):
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

    def create_ads(self, domain, instance, ads_user, ads_password, ads_parameters):
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
        create_flag = False
        self.validate_create_params(domain, ads_user, ads_password, ads_parameters)
        ads_create_params = {
            'name': domain, 'user': ads_user,
            'password': ads_password
        }

        if instance:
            ads_create_params['instance'] = instance

        if ads_parameters:
            for key in ads_parameters:
                if ads_parameters[key] is not None:
                    ads_create_params[key] = ads_parameters[key]

        try:
            if not self.module.check_mode:
                api_response = self.auth_api_instance.create_providers_ads_item(
                    providers_ads_item=ads_create_params)
                if api_response:
                    message = "ADS domain created, %s" % api_response
                    LOG.info(message)
                    self.ads_name.insert(0, api_response.id)
            create_flag = True
        except utils.ApiException as e:
            error_message = "Add an Active Directory provider failed with " + \
                utils.determine_error(error_obj=e)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

        if self.module._diff:
            self.result.update({"diff": {"before": {}, "after": ads_create_params}})

        return create_flag

    def update_ads(self, ads_name, modified_ads, ads_details):
        """
         Modify the details of the Active Directory provider.
        :param ads_name: Specifies the Active Directory provider name.
        :param modified_ads: Parameters to modify.
        :param ads_details: Details of the Active Directory provider.
        :return: True if the operation is successful.
        """
        modify_flag = True
        try:
            if not self.module.check_mode:
                self.auth_api_instance.update_providers_ads_by_id(
                    providers_ads_id_params=modified_ads,
                    providers_ads_id=ads_name)
                message = "ADS provider updated successfully."
                LOG.info(message)
            modify_flag = True
        except utils.ApiException as e:
            error_message = "Modifying Active Directory provider failed with " + \
                utils.determine_error(error_obj=e)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

        if self.module._diff:
            self.result.update({"diff": {"before": ads_details, "after": modified_ads}})

        return modify_flag

    def delete_ads(self, ads_name, ads_details):
        """
         Delete the ADS provider.
        :param ads_name: Specifies the Active Directory provider name.
        :param ads_details: Details of the Active Directory provider.
        :return: True if the operation is successful.
        """
        delete_flag = False

        try:
            if not self.module.check_mode:
                self.auth_api_instance.delete_providers_ads_by_id(ads_name)
                message = "ADS provider deleted successfully."
                LOG.info(message)
            delete_flag = True
        except utils.ApiException as e:
            error_message = "Deleting ADS provider failed with " + \
                utils.determine_error(error_obj=e)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

        if self.module._diff:
            self.result.update({"diff": {"before": ads_details, "after": {}}})

        return delete_flag

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

    def check_for_groupnet(self, key, array_ads, input_ads):
        """
        :param key: key
        :param array_ads: ADS dictionary returned from the PowerScale array.
        :param input_ads: ADS dictionary passed by the user.
        :return: True if the operation is successful.
        """
        if input_ads[key] and input_ads[key].lower() != array_ads[0][key].lower():
            err_msg = "Modification of %s is not supported." % key
            LOG.error(msg=err_msg)
            self.module.fail_json(msg=err_msg)

    def remove_none(self, ads_key, input_ad_param):
        """
        :param ads_key: key
        :param input_ad_param: input_ad_param
        :return: True if the operation is successful.
        """
        return {k: input_ad_param.get(k) for k in ads_key if input_ad_param.get(k) is not None}

    def get_modified_ads(self, input_ads, array_ads):
        """
        :param input_ads: ADS dictionary passed by the user.
        :param array_ads: ADS dictionary returned from the PowerScale array.
        :return: ADS dictionary with values that are modified.
        """
        updated_ads_dict = {}

        ads_keys = ['allocate_gids', 'allocate_uids', 'assume_default_domain',
                    'authentication', 'create_home_directory',
                    'domain_offline_alerts', 'ignore_all_trusts',
                    'ignored_trusted_domains', 'include_trusted_domains',
                    'ldap_sign_and_seal', 'lookup_groups', 'lookup_normalize_groups',
                    'lookup_normalize_users', 'lookup_users', 'machine_password_changes',
                    'nss_enumeration', 'restrict_findable', 'store_sfu_mappings',
                    'check_online_interval', 'controller_time', 'machine_password_lifespan',
                    'rpc_call_timeout', 'server_retry_limit', 'sfu_support',
                    'extra_expected_spns', 'findable_groups', 'findable_users',
                    'lookup_domains', 'unfindable_groups', 'unfindable_users',
                    'groupnet', 'organizational_unit', 'home_directory_template',
                    'login_shell', 'machine_account']
        updated_input_ads = {}
        updated_input_ads = self.remove_none(ads_key=ads_keys, input_ad_param=input_ads)

        for key in list(updated_input_ads):
            if updated_input_ads.get(key) != array_ads[0][key]:

                updated_ads_dict[key] = updated_input_ads[key]
            if key in ("groupnet", "machine_account"):

                if key == 'machine_account' and updated_input_ads.get(key):

                    updated_ads_dict[key] = updated_input_ads[key] + '$'
                self.check_for_groupnet(key=key, array_ads=array_ads,
                                        input_ads=updated_input_ads)

                if key in updated_ads_dict:

                    del updated_ads_dict[key]
            elif key == 'organizational_unit' or \
                    (key in updated_ads_dict and updated_input_ads[key] == array_ads[0][key]):

                del updated_ads_dict[key]

        return updated_ads_dict

    def get_auth_providers_summary(self):
        """Get Auth providers summary"""
        try:
            providers_summary_api_response = \
                self.auth_api_instance.get_providers_summary()
            providers_summary = \
                providers_summary_api_response.provider_instances

            return providers_summary
        except utils.ApiException as e:
            error_message = "Get auth providers summary failed with " + \
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
                "failed with " + utils.determine_error(error_obj=e)
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

    def get_ads_parameters(self):
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
                    login_shell=dict(type='str',
                                     choices=['/bin/sh', '/bin/csh',
                                              '/bin/tcsh', '/bin/zsh',
                                              '/bin/bash', '/bin/rbash',
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


class ADSExitHandler:
    """
    This class is used to perform the action on powerscale and exit the module
    """
    def handle(self, ads_obj, ads_params, ads_details):
        """
        Handle the ADS object based on the provided parameters.

        Args:
            ads_obj (object): The ADS object.
            ads_name (str): The name of the ADS provider.
            domain (str): The domain name of the ADS provider.
            instance (str): The instance name of the ADS provider.

        Returns:
            None
        """
        ads_name = ads_obj.ads_name
        spn_command = ads_params.get('spn_command')

        if ads_details:
            ads_obj.update_ads_access_zone_info(ads_name, ads_details)
            ads_obj.result['ads_provider_details'] = ads_details
            if spn_command == 'check' and ads_details:
                ads_obj.result['spn_check'] = ads_obj.get_spns_not_in_recommended_spns(
                    ads_details[0]['spns'], ads_details[0]['recommended_spns'])
        else:
            ads_obj.result['ads_provider_details'] = {}

        ads_obj.module.exit_json(**ads_obj.result)


class ADSDeleteHandler:
    """
    This class is used to perform action on PowerScale ADS object
    """
    def handle(self, ads_obj, ads_params, ads_details):
        """
        Handle the ADS object based on the provided parameters.

        Args:
            ads_obj (object): The ADS object.
            ads_name (str): The name of the ADS provider.
            domain (str): The domain name of the ADS provider.
            instance (str): The instance name of the ADS provider.

        Returns:
            None
        """
        # Delete an Active Directory provider
        if ads_params.get('state') == "absent":
            domain = ads_params.get('domain_name')
            instance = ads_params.get('instance_name')

            ads_obj.validate_input(ads_details, domain, instance)

            if ads_details:
                changed = ads_obj.delete_ads(ads_obj.ads_name[0], ads_details[0])
                ads_obj.result['changed'] = changed
                ads_details = ads_obj.get_ads_details(ads_obj.ads_name)

        ADSExitHandler().handle(ads_obj, ads_params, ads_details)


class ADSModifyHandler:
    """
    This class is used to perform action on PowerScale ADS object
    """
    def handle(self, ads_obj, ads_params, ads_details):
        """
        Handle the ADS object based on the provided parameters.

        Args:
            ads_obj (object): The ADS object.
            ads_params (dict): The parameters for handling the ADS object.
            ads_details (dict): The details of the ADS provider object.

        Returns:
            None
        """
        domain = ads_params.get('domain_name')
        instance = ads_params.get('instance_name')
        ads_parameters = ads_params.get('ads_parameters')
        spn_command = ads_params.get('spn_command')
        # Modify an Active Directory provider
        check_modification = ads_parameters or ads_params.get('spns') or spn_command == 'fix'

        if ads_params.get('state') == "present" and ads_details and check_modification:
            modified_ads = {}

            if ads_parameters:
                modified_ads = ads_obj.get_modified_ads(ads_parameters, ads_details)
            is_spn_modified, spns, extra_spns = ads_obj.perform_spn_operation(ads_details)

            if is_spn_modified:
                modified_ads['spns'] = spns
                modified_ads['extra_expected_spns'] = extra_spns

            if modified_ads:
                LOG.info('Modifying ADS provider.')
                ads_obj.validate_input(ads_details, domain, instance)
                changed = ads_obj.update_ads(ads_obj.ads_name[0], modified_ads, ads_details[0])
                ads_obj.result['changed'] = changed
                ads_details = ads_obj.get_ads_details(ads_obj.ads_name)

            if ads_obj.module._diff and not modified_ads:
                ads_obj.result.update({"diff": {"before": {}, "after": {}}})

        ADSDeleteHandler().handle(ads_obj, ads_params, ads_details)


class ADSCreateHandler:
    def handle(self, ads_obj, ads_params, ads_details):
        """
        Handle the ADS object based on the provided parameters.

        Args:
            ads_obj (object): The ADS object.
            ads_params (dict): The parameters for handling the ADS object.
            ads_details (dict): The details of the ADS provider object.
            ads_name (list): The name of the ADS provider object.

        Returns:
            None
        """
        ads_user = ads_params.get('ads_user')
        ads_password = ads_params.get('ads_password')
        domain = ads_params.get('domain_name')
        instance = ads_params.get('instance_name')
        ads_parameters = ads_params.get('ads_parameters')

        if ads_params.get('state') == "present" and not ads_details:
            LOG.info("Add an Active Directory provider.")
            changed = ads_obj.create_ads(domain, instance, ads_user,
                                         ads_password, ads_parameters)
            ads_obj.result['changed'] = changed
            ads_details = ads_obj.get_ads_details(ads_obj.ads_name)
            ADSExitHandler().handle(ads_obj, ads_params, ads_details)

        ADSModifyHandler().handle(ads_obj, ads_params, ads_details)


class AdsHandler:
    """
    This class is used to perform action on PowerScale ADS object
    """
    def handle_ads_name(self, ads_obj, ads_params):
        """
        Retrieves the ADS name based on the given `ads_params`.

        Args:
            ads_params (dict): A dictionary containing the `domain_name` and `instance_name` keys.

        Returns:
            list: A list containing the ADS name.

        """
        domain = ads_params['domain_name']
        instance = ads_params['instance_name']
        if instance and not domain:
            ads_obj.ads_name.insert(0, instance)
        else:
            providers_summary = ads_obj.get_auth_providers_summary()
            if instance and domain:
                provider_summary = [provider for provider in
                                    providers_summary
                                    if provider.type == 'ads'
                                    and provider.forest.lower() == domain.lower()
                                    and provider.name.lower() == instance.lower()]
                for provider in provider_summary:
                    ads_obj.ads_name.append(provider.name)
            elif domain:
                provider_summary = [provider for provider in
                                    providers_summary
                                    if provider.type == 'ads'
                                    and provider.forest.lower() == domain.lower()]
                for provider in provider_summary:
                    ads_obj.ads_name.append(provider.name)

    def handle(self, ads_obj, ads_params):
        """
        Handle the ADS object based on the provided parameters.

        Args:
            ads_obj (object): The ADS object.
            ads_params (dict): The parameters for handling the ADS object.

        Returns:
            None
        """
        self.handle_ads_name(ads_obj, ads_params)

        ads_details = ads_obj.get_ads_details(ads_obj.ads_name)

        ADSCreateHandler().handle(ads_obj, ads_params, ads_details)


def main():
    """ Create PowerScale ADS object and perform action on it
        based on user input from playbook"""
    obj = Ads()
    AdsHandler().handle(obj, obj.module.params)


if __name__ == '__main__':
    main()
