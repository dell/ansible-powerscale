# Copyright: (c) 2023, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('synciq')


class SyncIQ:

    '''Class with shared Sync operations'''

    def __init__(self, synciq_api, module):
        """
        Initialize the synciq class
        :param synciq_api: The sync sdk instance
        :param module: Ansible module object
        """
        self.synciq_api = synciq_api
        self.module = module

    def get_synciq_global_settings(self):
        """
        Get details of SyncIQ global settings
        """
        try:
            synciq_global_obj = self.synciq_api.get_sync_settings()
            if synciq_global_obj:
                msg = f"SyncIQ global settings details are: {synciq_global_obj.settings.to_dict()}"
                LOG.info(msg)
                return synciq_global_obj.settings.to_dict()

        except Exception as e:
            error_msg = f"Got error {utils.determine_error(e)} while getting" \
                        f" SyncIQ global setings details "
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)
