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
            self.handle_apiexception(path, e)
        except Exception as e:
            error_message = "Failed to get details of Filesystem {0} with" \
                            " error {1} ".format(path, str(e))
            self.handle_exception(error_message)

    def list_all_filesystem_from_directory(self, path):
        """Lists all filesystems in a directory"""
        try:
            resp = self.namespace_api.get_directory_contents(directory_path=path)
            return resp.to_dict()
        except utils.ApiException as e:
            self.handle_apiexception(path, e)
        except Exception as e:
            error_message = "Failed to get details of Filesystem {0} with" \
                            " error {1} ".format(path, str(e))
            self.handle_exception(error_message)

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
            self.handle_exception(error_message)

    def handle_apiexception(self, path, e):
        if str(e.status) == "404":
            log_msg = "Filesystem {0} status is \
                {1}.format(path, e.status)"
            LOG.info(log_msg)
            return None
        else:
            error_msg = utils.determine_error(error_obj=e)
            error_message = "Failed to get details of Filesystem \
                {0} with error {1} ".format(path,
                                            str(error_msg))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def handle_exception(self, error_message):
        LOG.error(error_message)
        self.module.fail_json(msg=error_message)
