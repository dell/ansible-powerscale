# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('quota')


class Quota:

    '''Class with shared quota operations'''

    def __init__(self, quota_api, module):
        """
        Initialize the quota class
        :param quota_api: The quota sdk instance
        :param module: Ansible module object
        """
        self.quota_api = quota_api
        self.module = module

    def get_quota(self, effective_path):
        """Gets Quota details"""
        # On a single path , you can create multiple Quotas of
        # different types (directory, user etc)
        # We are filtering Quotas on the path and the type (directory).
        # On a given path, there can be only One Quota of a given type.
        try:
            filesystem_quota = self.quota_api.list_quota_quotas(
                path='/' + effective_path,
                type='directory')
            return filesystem_quota.to_dict()
        except Exception:
            error_message = 'Unable to get Quota details on ' \
                            'path {0}'.format(effective_path)
            LOG.info(error_message)
            return None
