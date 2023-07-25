#!/usr/bin/python
# Copyright: (c) 2021, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Ansible module for managing LDAP authentication provider on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ldap

version_added: '1.2.0'

short_description: Manage LDAP authentication provider on PowerScale
description:
- Managing LDAP authentication provider on PowerScale storage
  system includes creating, modifying, deleting and retrieving details
  of LDAP provider.

extends_documentation_fragment:
  - dellemc.powerscale.powerscale

author:
- Jennifer John (@johnj9) <ansible.team@dell.com>

options:
  ldap_name:
    description:
    - Specifies the name of the LDAP provider.
    type: str
    required: true

  server_uris:
    description:
    - Specifies the server URIs.
    - This parameter is mandatory during create.
    - I(server_uris) should begin with ldap:// or ldaps:// if not validation
      error will be displayed.
    type: list
    elements: str

  server_uri_state:
    description:
    - Specifies if the I(server_uris) need to be added or removed from the
      provider.
    - This parameter is mandatory if I(server_uris) is specified.
    - While creating LDAP provider, this parameter value should be
      specified as C(present-in-ldap).
    choices: ['present-in-ldap', 'absent-in-ldap']
    type: str

  base_dn:
    description:
    - Specifies the root of the tree in which to search identities.
    - This parameter is mandatory during create.
    type: str

  ldap_parameters:
    description:
    - Specify additional parameters to configure LDAP domain.
    type: dict
    suboptions:
      groupnet:
        description:
        - Groupnet identifier.
        - This is an optional parameter and defaults to groupnet0.
        type: str
      bind_dn:
        description:
        - Specifies the distinguished name for binding to the LDAP server.
        type: str
      bind_password:
        description:
        - Specifies the password for the distinguished name for binding to
          the LDAP server.
        type: str

  state:
    description:
    - The state of the LDAP provider after the task is performed.
    - C(present) - indicates that the LDAP provider should exist on the system.
    - C(absent) - indicates that the LDAP provider should not exist on the system.
    choices: ['absent', 'present']
    type: str
    required: true

notes:
- This module does not support modification of I(bind_password) of LDAP provider.
- The value specified for I(bind_password) will be ignored during modify.
- The I(check_mode) is not supported.
'''

EXAMPLES = r'''
- name: Add an LDAP provider
  dellemc.powerscale.ldap:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    ldap_name: "ldap_test"
    server_uris:
      - "{{server_uri_1}}"
      - "{{server_uri_2}}"
    server_uri_state: 'present-in-ldap'
    base_dn: "DC=ansildap,DC=com"
    ldap_parameters:
      groupnet: "groupnet_ansildap"
      bind_dn: "cn=admin,dc=example,dc=com"
      bind_password: "{{bind_password}}"
    state: "present"

- name: Add server_uris to an LDAP provider
  dellemc.powerscale.ldap:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    ldap_name: "ldap_test"
    server_uris:
      - "{{server_uri_1}}"
    server_uri_state: "present-in-ldap"
    state: "present"

- name: Remove server_uris from an LDAP provider
  dellemc.powerscale.ldap:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    ldap_name: "ldap_test"
    server_uris:
      - "{{server_uri_1}}"
    server_uri_state: "absent-in-ldap"
    state: "present"

- name: Modify LDAP provider
  dellemc.powerscale.ldap:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    ldap_name: "ldap_test"
    base_dn: "DC=ansi_ldap,DC=com"
    ldap_parameters:
      bind_dn: "cn=admin,dc=test,dc=com"
    state: "present"

- name: Get LDAP provider details
  dellemc.powerscale.ldap:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    ldap_name: "ldap_test"
    state: "present"

- name: Delete a LDAP provider
  dellemc.powerscale.ldap:
    onefs_host: "{{onefs_host}}"
    api_user: "{{api_user}}"
    api_password: "{{api_password}}"
    verify_ssl: "{{verify_ssl}}"
    ldap_name: "ldap_test"
    state: "absent"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
    sample: "false"

ldap_provider_details:
    description: The LDAP provider details.
    returned: When LDAP provider exists
    type: complex
    contains:
       linked_access_zones:
            description: List of access zones linked to the authentication
                  provider.
            type: list
       base_dn:
           description: Specifies the root of the tree in which to search
                        identities.
           type: str
       bind_dn:
           description: Specifies the distinguished name for binding to the
                        LDAP server.
           type: str
       groupnet:
           description: Groupnet identifier.
           type: str
       name:
           description: Specifies the name of the LDAP provider.
           type: str
       server_uris:
           description: Specifies the server URIs.
           type: str
       status:
           description: Specifies the status of the provider.
           type: str
    sample: {
        "linked_access_zones": [
            "System"
        ],
        "base_dn": "dc=sample,dc=ldap,dc=domain,dc=com",
        "bind_dn": "cn=administrator,dc=sample,dc=ldap,dc=domain,dc=com",
        "groupnet": "groupnet",
        "name": "sample-ldap",
        "server_uris": "ldap://xx.xx.xx.xx",
        "status": "online"
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('ldap')


class Ldap(object):
    """Class with LDAP provider operations"""

    def __init__(self):
        """ Define all parameters required by this module"""
        self.module_params = utils.get_powerscale_management_host_parameters()
        self.module_params.update(get_ldap_parameters())

        required_together = [['server_uris', 'server_uri_state']]

        # initialize the Ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False,
            required_together=required_together
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

    def create(self, ldap_name, server_uris, server_uri_state, base_dn,
               ldap_parameters):
        """
        Add an LDAP provider.
        :param ldap_name: Specifies the LDAP provider name.
        :param server_uris: Specifies the server URIs.
        :param server_uri_state: Specifies if server_uris need to be added or
         removed from the provider. During create the parameter should be
         specifed as present-in-ldap.
        :param base_dn: Specifies the root of the tree in which to search
         identities.
        :param ldap_parameters: Specify additional parameters to configure
         LDAP domain.
        :return: LDAP Id.
        """
        if not base_dn:
            self.module.fail_json(
                msg="The parameter base_dn is mandatory while creating"
                " LDAP provider.")

        if not server_uris:
            self.module.fail_json(
                msg="The parameter server_uris is mandatory while creating"
                " LDAP provider.")

        self.validate_input(server_uris)
        if server_uri_state != 'present-in-ldap':
            self.module.fail_json(
                msg="Please specify the server_uri_state as present-in-ldap."
                    " Server_uris is mandatory while creating LDAP prodiver.")

        ldap_create_params = {
            'name': ldap_name, 'server_uris': server_uris,
            'base_dn': base_dn
        }
        if ldap_parameters:
            if ldap_parameters['groupnet']:
                ldap_create_params['groupnet'] = ldap_parameters['groupnet']
            if ldap_parameters['bind_dn']:
                ldap_create_params['bind_dn'] = ldap_parameters['bind_dn']
            if ldap_parameters['bind_password']:
                ldap_create_params['bind_password'] = \
                    ldap_parameters['bind_password']

        ldap_provider_obj = \
            utils.isi_sdk.ProvidersLdapItem(**ldap_create_params)
        try:
            api_response = self.auth_api_instance.create_providers_ldap_item(
                providers_ldap_item=ldap_provider_obj)
            message = "LDAP domain created, %s" % api_response
            LOG.info(message)
            return api_response
        except utils.ApiException as e:
            error_message = "Add an LDAP provider failed with" + \
                utils.determine_error(error_obj=e)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def update(self, ldap_name, modified_ldap):
        """
         Modify the details of the LDAP provider.
        :param ldap_name: Specifies the LDAP provider name.
        :param modified_ldap: Parameters to modify.
        :return: True if the operation is successful.
        """
        ldap_update_params = {}

        try:
            for key in modified_ldap:
                ldap_update_params[key] = modified_ldap[key]

            ldap_provider_params = utils.isi_sdk.ProvidersLdapIdParams(
                **ldap_update_params)

            self.auth_api_instance.update_providers_ldap_by_id(
                providers_ldap_id_params=ldap_provider_params,
                providers_ldap_id=ldap_name)
            message = "LDAP provider updated successfully."
            LOG.info(message)
            return True
        except utils.ApiException as e:
            error_message = "Modifying LDAP provider failed with" + \
                utils.determine_error(error_obj=e)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete(self, ldap_name):
        """
         Delete the details of the LDAP provider.
        :param ldap_name: Specifies the LDAP provider name.
        :return: True if the operation is successful.
        """
        try:
            self.auth_api_instance.delete_providers_ldap_by_id(
                providers_ldap_id=ldap_name)
            message = "LDAP provider deleted successfully."
            LOG.info(message)
            return True
        except utils.ApiException as e:
            error_message = "Deleting LDAP provider failed with" + \
                utils.determine_error(error_obj=e)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_ldap_details(self, ldap_name):
        """
        Get the details of the LDAP provider.
        :param ldap_name: Specifies the LDAP provider name.
        :return: if exists returns details of the LDAP provider
        else returns None.
        """
        try:
            api_response = self.auth_api_instance.get_providers_ldap_by_id(
                ldap_name)
            return api_response.ldap[0].to_dict()
        except utils.ApiException as e:
            if str(e.status) == '404':
                error_message = "LDAP provider {0} details are not found".\
                    format(ldap_name)
                LOG.info(error_message)
                return None

            error_message = 'Get details of LDAP provider {0} failed with ' \
                            'error: {1}'.format(ldap_name,
                                                utils.determine_error
                                                (error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
        except Exception as e:
            error_message = 'Get details of LDAP provider {0} failed with ' \
                            'error: {1}'.format(ldap_name,
                                                utils.determine_error
                                                (error_obj=e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_modified_ldap(self, server_uris, server_uri_state,
                          base_dn, input_ldap, array_ldap):
        """
        :param server_uris: Specifies the server URIs.
        :param server_uri_state: Specifies if server_uris need to be added or
         removed from the provider.
        :param base_dn: Specifies the root of the tree in which to search
         identities.
        :param input_ldap: LDAP dictionary passed by the user.
        :param array_ldap: LDAP dictionary returned from the PowerScale array.
        :return: LDAP dictionary with values that are modified.
        """
        if input_ldap:
            for key in list(input_ldap):
                if key.lower() == "groupnet":
                    if input_ldap[key] and input_ldap[key] != array_ldap[key]:
                        self.module.fail_json(msg='Modification of'
                                              ' groupnet is not supported.')
                    del input_ldap[key]
                elif key.lower() == "bind_password":
                    del input_ldap[key]
                elif input_ldap[key] is None or \
                        input_ldap[key] == array_ldap[key]:
                    del input_ldap[key]
        else:
            input_ldap = {}

        if base_dn and base_dn != array_ldap["base_dn"]:
            input_ldap["base_dn"] = base_dn

        if server_uris:
            self.validate_input(server_uris)
            server_uri_exists = all(uri in array_ldap['server_uris'] for uri
                                    in server_uris)
            if server_uri_state == 'present-in-ldap':
                if not server_uri_exists:
                    input_ldap["server_uris"] = array_ldap['server_uris'] + \
                        server_uris
            elif server_uri_state == 'absent-in-ldap':
                uris = list(set(array_ldap['server_uris']).difference(server_uris))
                if not uris:
                    self.module.fail_json(msg='Server_uris is a'
                                          ' required field. All'
                                          ' server_uris mapped to the LDAP'
                                          ' provider cannot be removed.')
                if server_uri_exists:
                    input_ldap['server_uris'] = uris

        return input_ldap

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

    def update_ldap_access_zone_info(self, ldap_name, ldap_details):
        """Update LDAP with access zone details"""
        try:
            zone_api_response = self.zones_api_instance.list_zones()
            if zone_api_response:
                providers_summary = self.get_auth_providers_summary()
                provider_ids = [provider.id for provider in
                                providers_summary if provider.type == "ldap" and
                                provider.name.lower() == ldap_name.lower()]
                zone_ids = []
                if provider_ids:
                    zone_ids = [zone.id for zone in zone_api_response.zones
                                if set(provider_ids).issubset(
                                    zone.auth_providers)]
                ldap_details.update(linked_access_zones=zone_ids)
        except utils.ApiException as e:
            error_message = "Update LDAP with access zone details " \
                "failed with" + utils.determine_error(error_obj=e)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def validate_input(self, server_uris):
        """Validate input parameters"""
        for server_uri in server_uris:
            if not server_uri.startswith("ldap://") and not \
                    server_uri.startswith("ldaps://"):
                self.module.fail_json(msg='The value for server_uris is '
                                      'invalid. URIs should begin with '
                                      'ldap:// or ldaps://')

    def perform_module_operation(self):
        """
        Perform different actions on LDAP module based on parameters
        chosen in playbook
        """
        ldap_name = self.module.params['ldap_name']
        server_uris = self.module.params['server_uris']
        server_uri_state = self.module.params['server_uri_state']
        base_dn = self.module.params['base_dn']
        ldap_parameters = self.module.params['ldap_parameters']

        ldap_details = self.get_ldap_details(ldap_name)
        state = self.module.params['state']
        changed = False

        # Add LDAP provider
        if state == "present" and not ldap_details:
            LOG.info("Add an LDAP provider.")
            self.create(ldap_name, server_uris, server_uri_state, base_dn,
                        ldap_parameters)
            changed = True

        # Modify LDAP provider
        if state == "present" and ldap_details:
            modified_ldap = self.get_modified_ldap(server_uris, server_uri_state,
                                                   base_dn,
                                                   ldap_parameters,
                                                   ldap_details)
            if modified_ldap:
                LOG.info('Modifying LDAP provider.')
                changed = self.update(ldap_name, modified_ldap)

        # Delete LDAP provider
        if state == "absent" and ldap_details:
            LOG.info('Deleting LDAP provider.')
            changed = self.delete(ldap_name)

        ldap_details = self.get_ldap_details(ldap_name)
        if ldap_details:
            self.update_ldap_access_zone_info(ldap_name, ldap_details)
        self.result["changed"] = changed
        self.result["ldap_provider_details"] = ldap_details
        self.module.exit_json(**self.result)


def get_ldap_parameters():
    """
    This method provides parameters required for the ansible LDAP auth
    module on PowerScale
    """
    return dict(
        ldap_name=dict(type='str', required=True),
        server_uris=dict(type='list', elements='str', no_log=True),
        server_uri_state=dict(type='str', choices=['present-in-ldap',
                                                   'absent-in-ldap']),
        base_dn=dict(type='str'),
        ldap_parameters=dict(
            type='dict', options=dict(
                groupnet=dict(type='str'),
                bind_dn=dict(type='str'),
                bind_password=dict(type='str', no_log=True),
            )
        ),
        state=dict(required=True, type='str', choices=['present', 'absent'])
    )


def main():
    """ Create PowerScale LDAP object and perform action on it
        based on user input from playbook"""
    obj = Ldap()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
