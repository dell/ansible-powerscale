# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('protocol')


class Protocol:

    '''Class with shared protocol operations'''

    def __init__(self, protocol_api, module):
        """
        Initialize the protocol class
        :param protocol_api: The protocol sdk instance
        :param module: Ansible module object
        """
        self.protocol_api = protocol_api
        self.module = module

    def get_nfs_default_settings(self, access_zone):
        """
        Get details of an NFS default settings for a given access zone.
        :param access_zone: Access zone
        :type access_zone: str
        :return: NFS default settings
        :rtype: dict
        """
        msg = f"Getting NFS default settings for {access_zone} access zone"
        LOG.info(msg)
        try:
            nfs_settings_export = self.protocol_api.get_nfs_settings_export(zone=access_zone).to_dict()
            if nfs_settings_export:
                nfs_default_settings = nfs_settings_export['settings']
                msg = f"NFS default settings are: {nfs_default_settings}"
                LOG.info(msg)
                return nfs_default_settings
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = f'Fetching NFS default settings failed with error: {error_msg}'
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
