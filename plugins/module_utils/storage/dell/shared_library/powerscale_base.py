# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('powerscale_base')


class PowerScaleBase:

    '''Powerscale Base Class'''

    def __init__(self, ansible_module, ansible_module_params):
        """
        Initialize the powerscale base class
        :param ansible_module: Ansible module class
        :type ansible_module: AnsibleModule
        :param ansible_module_params: Parameters for ansible module class
        :type ansible_module_params: dict
        """
        self.module_params = utils.get_powerscale_management_host_parameters()
        ansible_module_params['argument_spec'].update(self.module_params)

        # Initialize the ansible module
        self.module = ansible_module(
            **ansible_module_params
        )

        self.result = {"changed": False}

        PREREQS_VALIDATE = utils.validate_module_pre_reqs(self.module.params)
        if PREREQS_VALIDATE \
                and not PREREQS_VALIDATE["all_packages_found"]:
            self.module.fail_json(
                msg=PREREQS_VALIDATE["error_message"])

        self.api_client = utils.get_powerscale_connection(self.module.params)
        self.isi_sdk = utils.get_powerscale_sdk()
        LOG.info('Got python SDK instance for provisioning on PowerScale')
        LOG.info('Check Mode Flag: %s', self.module.check_mode)

        # Using lazy property for accessing the isi_sdk instances
        self._protocol_api = None
        self._auth_api = None

    @property
    def protocol_api(self):
        """
        Returns the protocol API object.

        :return: The protocol API object.
        :rtype: isi_sdk.ProtocolsApi
        """
        if self._protocol_api is None:
            self._protocol_api = self.isi_sdk.ProtocolsApi(self.api_client)
        return self._protocol_api

    @property
    def auth_api(self):
        """
        Returns the auth API object.

        :return: The auth API object.
        :rtype: isi_sdk.AuthApi
        """
        if self._auth_api is None:
            self._auth_api = self.isi_sdk.AuthApi(self.api_client)
        return self._auth_api
