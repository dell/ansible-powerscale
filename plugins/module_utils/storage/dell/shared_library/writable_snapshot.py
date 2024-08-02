# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell \
    import utils

LOG = utils.get_logger('snapshot')


class WritableSnapshot:

    '''Class with shared snapshot operations'''

    def __init__(self, snapshot_api, module):
        """
        Initialize the snapshot class
        :param snapshot_api: The snapshot sdk instance
        :param module: Ansible module object
        """
        self.snapshot_api = snapshot_api
        self.module = module

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
            writable_snapshot_query_params = query_params.get('writable_snapshot', []) if query_params else []
            filter_params = {}
            if writable_snapshot_query_params:
                if "wspath" in writable_snapshot_query_params:
                    return self.snapshot_api.get_snapshot_writable_wspath(
                        snapshot_writable_wspath=writable_snapshot_query_params["wspath"]
                    ).to_dict()
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
