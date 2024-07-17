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
            snapshot_list = \
                self.snapshot_api.list_snapshot_snapshots().to_dict()
            snapshots = []

            for snap in snapshot_list['snapshots']:
                if snap['path'] == '/' + effective_path:
                    snapshots.append(snap)
            return snapshots
        except Exception as e:
            error_msg = utils.determine_error(error_obj=e)
            error_message = 'Failed to get filesystem snapshots ' \
                            'due to error {0}'.format((str(error_msg)))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
