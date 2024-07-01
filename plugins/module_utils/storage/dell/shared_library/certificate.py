# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('certificate')


class Certificate:

    '''Class with shared Certificate operations'''

    def __init__(self, certificate_api, module):
        """
        Initialize the certificate class
        :param certificate_api: The certificate sdk instance
        :param module: Ansible module object
        """
        self.certificate_api = certificate_api
        self.module = module

    def get_server_certificate_with_default(self):
        """
        Get details of Server certificate.
        """
        try:
            certificate = self.certificate_api.list_certificate_server().to_dict()
            default_certificate = self.certificate_api.get_certificate_settings().to_dict()
            if certificate and default_certificate:
                for each_cert in certificate['certificates']:
                    if each_cert['id'] == default_certificate['settings']['default_https_certificate']:
                        each_cert['certificate_monitor_enabled'] = default_certificate['settings']['certificate_monitor_enabled']
                        each_cert['certificate_pre_expiration_threshold'] = \
                            default_certificate['settings']['certificate_pre_expiration_threshold']
                        break
                msg = f"Server certificate details are: {certificate}"
                LOG.info(msg)
                return certificate['certificates']
        except Exception as e:
            error_msg = f"Got error {utils.determine_error(e)} while getting Server certificate details."
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)
