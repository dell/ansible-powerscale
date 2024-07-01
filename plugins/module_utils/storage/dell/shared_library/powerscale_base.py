# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
        self._synciq_api = None
        self._cluster_api = None
        self._certificate_api = None
        self._zones_summary_api = None
        self._support_assist_api = None

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

    @property
    def synciq_api(self):
        """
        Returns the sync API object.

        :return: The sync API object.
        :rtype: isi_sdk.AuthApi
        """
        if self._synciq_api is None:
            self._synciq_api = self.isi_sdk.SyncApi(self.api_client)
        return self._synciq_api

    @property
    def cluster_api(self):
        """
        Returns the cluster API object.

        :return: The cluster API object.
        :rtype: isi_sdk.ClusterApi
        """
        if self._cluster_api is None:
            self._cluster_api = self.isi_sdk.ClusterApi(self.api_client)
        return self._cluster_api

    @property
    def certificate_api(self):
        """Returns the certificate API object.
        :return: The certificate API object.
        :rtype: isi_sdk.CertificateApi
        """
        if self._certificate_api is None:
            self._certificate_api = self.isi_sdk.CertificateApi(self.api_client)
        return self._certificate_api

    @property
    def zones_summary_api(self):
        """Returns the zones summary API object.
        :return: The zones summary API object.
        :rtype: isi_sdk.ZonesSummaryApi
        """
        if self._zones_summary_api is None:
            self._zones_summary_api = self.isi_sdk.ZonesSummaryApi(self.api_client)
        return self._zones_summary_api

    @property
    def support_assist_api(self):
        """
        Returns the support assist API object.

        :return: The support assist API object.
        :rtype: isi_sdk.SupportassistApi
        """
        if self._support_assist_api is None:
            self._support_assist_api = self.isi_sdk.SupportassistApi(self.api_client)
        return self._support_assist_api
