# Copyright: (c) 2022-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of writablesnapshots module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockWritableSanpshotsApi:
    WS_COMMON_ARGS = {"onefs_host": "XX.XX.XX.XX",
                      "port_no": "8080",
                      "verify_ssl": "false"
                      }
    DSTPATH = "/ifs/ansible8/"
    WS_CREATE_ARGS = {"writable_snapshots": [{"src_snap": 2, "dst_path": DSTPATH, "state": "present"}]}
    WS_CREATE_ARGS_STR = {"writable_snapshots": [{"src_snap": "snap-2", "dst_path": DSTPATH, "state": "present"}]}
    WS_DELETE_ARGS = {"writable_snapshots": [{"src_snap": 2, "dst_path": DSTPATH, "state": "absent"}]}
    WS_INVALID_DSTPATH_ARGS = {"writable_snapshots": [{"src_snap": "invalid", "dst_path": DSTPATH, "state": "present"}]}

    @staticmethod
    def get_writeable_snpshots_error_response(response_type):
        dst_path = MockWritableSanpshotsApi.DSTPATH
        if response_type == 'delete_exception':
            return f"Failed to delete snapshot: {dst_path} with error"
        elif response_type == 'create_exception':
            return f"Failed to create writable snapshot: {dst_path} with error: SDK Error message"
        elif response_type == 'invalid_dstpath':
            return "Few writable snapshots are not able to be created because the destination path or source path is invalid:"
