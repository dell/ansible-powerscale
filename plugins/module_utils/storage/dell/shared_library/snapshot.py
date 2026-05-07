# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('snapshot')


class Snapshot:

    '''Class with shared snapshot operations'''

    def __init__(self, snapshot_api, module):
        """
        Initialize the snapshot class
        :param snapshot_api: The snapshot sdk instance
        :param module: Ansible module object
        """
        self.snapshot_api = snapshot_api
        self.module = module

    def get_filesystem_snapshots(self, effective_path):
        """Get snapshots for a given filesystem"""
        try:
            snapshots = []
            filtered_snapshots = []
            snapshot_list = \
                self.snapshot_api.list_snapshot_snapshots().to_dict()
            snapshots.extend(snapshot_list['snapshots'])
            resume = snapshot_list['resume']
            while resume:
                snapshot_list = \
                    self.snapshot_api.list_snapshot_snapshots(
                        resume=resume).to_dict()
                snapshots.extend(snapshot_list['snapshots'])
                resume = snapshot_list['resume']
            for snap in snapshot_list['snapshots']:
                if snap['path'] == '/' + effective_path:
                    filtered_snapshots.append(snap)
            return filtered_snapshots
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Failed to get filesystem snapshots ' \
                            'due to error {0}'.format((str(error_msg)))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def list_writable_snapshots(self):
        """
        List the writable snapshots.

        :param filter: The filter for the list.
        :type filter: dict
        :returns: The list of snapshots.
        :rtype: list
        """
        try:
            query_params = self.module.params.get('query_parameters')
            writable_snapshot_query_params = query_params.get('writable_snapshots', []) if query_params else []
            filter_params = {}
            if writable_snapshot_query_params:
                if "wspath" in writable_snapshot_query_params:
                    return self.get_writable_snapshot_by_wspath(wspath=writable_snapshot_query_params.get("wspath"))
                else:
                    filter_params = dict(writable_snapshot_query_params.items())
            writable_snapshots = []
            snapshot_list = \
                self.snapshot_api.list_snapshot_writable(**filter_params).to_dict()
            writable_snapshots.extend(snapshot_list['writable'])
            return writable_snapshots
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Failed to get writeable snapshots ' \
                            'due to error {0}'.format((str(error_msg)))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def get_writable_snapshot_by_wspath(self, wspath):
        try:
            return self.snapshot_api.get_snapshot_writable_wspath(
                snapshot_writable_wspath=wspath
            ).to_dict().get("writable")
        except utils.ApiException as e:
            return {}
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Failed to get writeable snapshot ' \
                            'due to error {0}'.format((str(error_msg)))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
