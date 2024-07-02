# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('cluster')


class Cluster:

    '''Class with shared Cluster operations'''

    def __init__(self, cluster_api, module):
        """
        Initialize the cluster class
        :param cluster_api: The cluster sdk instance
        :param module: Ansible module object
        """
        self.cluster_api = cluster_api
        self.module = module

    def get_email_settings(self):
        """
        Get cluster email settings
        :return: Cluster email settings.
        """
        try:
            email_details = self.cluster_api.get_cluster_email()
            return email_details.to_dict()
        except Exception as e:
            error_message = f"Failed to get the details of email settings with error: {utils.determine_error(e)}"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_cluster_identity_details(self):
        """
        Get cluster email settings
        :return: Cluster identity details.
        """
        try:
            cluster_identity = self.cluster_api.get_cluster_identity()
            return cluster_identity.to_dict()
        except Exception as e:
            error_message = f"Failed to get the details of cluster identity details with error: {utils.determine_error(e)}"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_cluster_owner_details(self):
        """
        Get cluster email settings
        :return: Cluster owner details.
        """
        try:
            cluster_owner = self.cluster_api.get_cluster_owner()
            return cluster_owner.to_dict()
        except Exception as e:
            error_message = f"Failed to get the details of cluster owner details with error: {utils.determine_error(e)}"
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
