#!/usr/bin/python
# Copyright: (c) 2021, DellEMC

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

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
  system. This includes creating, modifying, deleting and retreiving the details
  of an ADS provider.

extends_documentation_fragment:
  - dellemc.powerscale.dellemc_powerscale.powerscale

author:
- Jennifer John (@johnj9) <ansible.team@dell.com>

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
    - It is mutually exclusive with domain_name for get, modify and delete
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
      groupnet:
        description:
        - Groupnet identifier.
        - This is an optional parameter and defaults to groupnet0.
        type: str
      home_directory_template:
        description:
        - Specifies the path to the home directory template.
        - This is an optional parameter and defaults to '/ifs/home/%D/%U'.
        type: str
      login_shell:
        description:
        - Specifies the login shell path.
        - This is an optional parameter and defaults to '/bin/zsh'.
        type: str
        choices: ['/bin/sh', '/bin/csh', '/bin/tcsh', '/bin/zsh', '/bin/bash',
                  '/bin/rbash', '/sbin/nologin']
      machine_account:
        description:
        - Specifies the machine account name when creating a SAM account with Active Directory.
        - The default cluster name is called 'default'.
        type: str
      organizational_unit:
        description:
        - Specifies the organizational unit.
        type: str


  state:
    description:
    - The state of the ads provider after the task is performed.
    - present - indicates that the ADS provider should exist on the system.
    - absent - indicates that the ADS provider should not exist on the system.
    choices: ['absent', 'present']
    type: str
    required: True
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
      state: "present"

- name: Get Active Directory provider details with domain name
  dellemc.powerscale.ads:
      onefs_host: "{{onefs_host}}"
      api_user: "{{api_user}}"
      api_password: "{{api_password}}"
      verify_ssl: "{{verify_ssl}}"
      domain_name: "ansibleneo.com"
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

ads_provider_details:
    description: The Active Directory provider details.
    returned: When Active Directory provider exists
    type: complex
    contains:
        linked_access_zones:
            description: List of access zones linked to the authentication
                         provider.
            type: list
        groupnet:
            description: Groupnet identifier.
            type: str
        home_directory_template:
            description: Specifies the path to the home directory template.
            type: str
        id:
            description: Specifies the ID of the Active Directory provider
                         instance.
            type: str
        name:
            description: Specifies the Active Directory provider name.
            type: str
        login_shell:
            description: Specifies the login shell path.
            type: str
        machine_account:
            description: Specifies the machine account name when creating a
                         SAM account with Active Directory.
            type: str
'''

import re
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import dellemc_ansible_powerscale_utils as utils

LOG = utils.get_logger('dellemc_powerscale_ads')


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
            supports_check_mode=False,
            required_one_of=required_one_of
        )

        # result is a dictionary that contains changed status
        self.result = {"changed": False}
        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
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
                    if not utils.ISI_SDK_VERSION_9 and key == 'machine_account':
                        ads_create_params['account'] = ads_parameters[key]
                    else:
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
        if state == "present" and ads_details and ads_parameters:
            modified_ads = self.get_modified_ads(ads_parameters, ads_details)
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
                organizational_unit=dict(type='str')
            )
        ),
        state=dict(required=True, type='str', choices=['present', 'absent'])
    )


def main():
    """ Create PowerScale ADS object and perform action on it
        based on user input from playbook"""
    obj = Ads()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
