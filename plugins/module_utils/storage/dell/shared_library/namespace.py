# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('namespace')


class Namespace:

    '''Class with shared namespace operations'''

    def __init__(self, namespace_api, module):
        """
        Initialize the namespace class
        :param namespace_api: The namespace sdk instance
        :param module: Ansible module object
        """
        self.namespace_api = namespace_api
        self.module = module

    def get_filesystem(self, path):
        """Gets a FileSystem on PowerScale."""
        try:
            resp = self.namespace_api.get_directory_metadata(
                path,
                metadata=True)
            return resp.to_dict()
        except utils.ApiException as e:
            if str(e.status) == "404":
                log_msg = "Filesystem {0} status is " \
                          "{1}".format(path, e.status)
                LOG.info(log_msg)
                return None
            else:
                error_msg = self.determine_error(error_obj=e)
                error_message = "Failed to get details of Filesystem " \
                                "{0} with error {1} ".format(
                                    path,
                                    str(error_msg))
                LOG.error(error_message)
                self.module.fail_json(msg=error_message)

        except Exception as e:
            error_message = "Failed to get details of Filesystem {0} with" \
                            " error {1} ".format(path, str(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_acl(self, effective_path):
        """Retrieves ACL rights of filesystem"""
        try:
            if not self.module.check_mode:
                filesystem_acl = \
                    (self.namespace_api.get_acl(effective_path,
                                                acl=True)).to_dict()
                return filesystem_acl
            return True
        except Exception as e:
            error_message = 'Error %s while retrieving the access control list for ' \
                            'namespace object.' % utils.determine_error(error_obj=e)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

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

    def get_filesystem_snapshots(self, effective_path):
        """Get snapshots for a given filesystem"""
        try:
            snapshot_list = \
                self.snapshot_api.list_snapshot_snapshots().to_dict()
            snapshots = []

            for snap in snapshot_list['snapshots']:
                if snap['path'] == '/' + effective_path:
                    snapshots.append(snap)
            return snapshots
        except Exception as e:
            error_msg = self.determine_error(error_obj=e)
            error_message = 'Failed to get filesystem snapshots ' \
                            'due to error {0}'.format((str(error_msg)))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
