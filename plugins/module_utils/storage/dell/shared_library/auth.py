# Copyright: (c) 2023-2024, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('auth')


class Auth:

    '''Class with shared auth operations'''

    def __init__(self, auth_api, module):
        """
        Initialize the auth class
        :param auth_api: The auth sdk instance
        :param module: Ansible module object
        """
        self.auth_api = auth_api
        self.module = module

    def get_group_details(self, name, zone, provider):
        """
        Get details of the group
        :param name: name of the group
        :param zone: zone in which group exists
        :param provider: provider type of the group
        """
        LOG.info("Getting group details.")
        try:
            resp = self.auth_api.get_auth_group(
                auth_group_id='GROUP:' + name,
                zone=zone, provider=provider).to_dict()
            return resp
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Failed to get the group details for group {name} ' \
                            f'in zone {zone} and provider {provider} due to' \
                            f' error {str(error_msg)}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_user_details(self, name, zone, provider):
        """
        Get details of the user
        :param name: name of the user
        :param zone: zone in which user exists
        :param provider: provider type of the user
        """
        LOG.info("Getting user details.")
        try:
            resp = self.auth_api.get_auth_user(
                auth_user_id='USER:' + name,
                zone=zone, provider=provider).to_dict()
            return resp
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Failed to get the user details for {name} in zone ' \
                            f'{zone} and provider {provider} due to error ' \
                            f'{error_msg}.'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_wellknown_details(self, name):
        """
        Get details of the well known
        :param name: name of the well known
        """
        LOG.info("Getting well known user details.")
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

    def get_group_user_id(self, persona, persona_type, zone):
        """
        :param persona: Name and provider type of user or group
        :type persona: dict
        :param persona_type: Indicates whether user or group
        :type persona_type: str
        :param zone: Access Zone
        :type zone: str
        """
        if persona_type == "user":
            details = self.get_user_details(
                name=persona['name'],
                zone=zone,
                provider=persona['provider_type'])['users'][0]['uid']
        elif persona_type == "group":
            details = self.get_group_details(
                name=persona['name'],
                zone=zone,
                provider=persona['provider_type'])['groups'][0]['gid']
        return details

    def get_auth_roles(self, zone):
        """
        Get details of the auth role
        """
        LOG.info("Getting auth role details.")
        try:
            resp = self.auth_api.list_auth_roles(zone=zone).to_dict()
            return resp
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Failed to get the auth role list ' \
                            f'due to error {error_msg}.'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
