# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock API responses for PowerScale SyncIQ Job module"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.modules.synciqjob.utils'

SYNCIQ_JOB = {
    "job_details": [
        {
            "action": "run",
            "ads_streams_replicated": 0,
            "block_specs_replicated": 0,
            "bytes_recoverable": 0,
            "bytes_transferred": 0,
            "char_specs_replicated": 0,
            "committed_files": 0,
            "corrected_lins": 0,
            "dead_node": False,
            "directories_replicated": 0,
            "dirs_changed": 0,
            "dirs_deleted": 0,
            "dirs_moved": 0,
            "dirs_new": 0,
            "duration": 1,
            "encrypted": True,
            "end_time": 1687488893,
            "error": "",
            "error_checksum_files_skipped": 0,
            "error_io_files_skipped": 0,
            "error_net_files_skipped": 0,
            "errors": [],
            "failed_chunks": 0,
            "fifos_replicated": 0,
            "file_data_bytes": 0,
            "files_changed": 0,
            "files_linked": 0,
            "files_new": 0,
            "files_selected": 0,
            "files_transferred": 0,
            "files_unlinked": 0,
            "files_with_ads_replicated": 0,
            "flipped_lins": 0,
            "hard_links_replicated": 0,
            "hash_exceptions_fixed": 0,
            "hash_exceptions_found": 0,
            "id": "test",
            "job_id": 1,
            "lins_total": 0,
            "network_bytes_to_source": 0,
            "network_bytes_to_target": 0,
            "new_files_replicated": 0,
            "num_retransmitted_files": 0,
            "phases": [],
            "policy": {
                "action": "sync",
                "file_matching_pattern": {
                    "or_criteria": None
                },
                "name": "test",
                "source_exclude_directories": [],
                "source_include_directories": [],
                "source_root_path": "/ifs/ATest",
                "target_host": "10.**.**.**",
                "target_path": "/ifs/ATest"
            },
            "policy_action": "sync",
            "policy_id": "2ed973731814666a9d258db3a8875b5d",
            "policy_name": "test",
            "quotas_deleted": 0,
            "regular_files_replicated": 0,
            "resynced_lins": 0,
            "retransmitted_files": [],
            "retry": 1,
            "running_chunks": 0,
            "service_report": None,
            "sockets_replicated": 0,
            "source_bytes_recovered": 0,
            "source_directories_created": 0,
            "source_directories_deleted": 0,
            "source_directories_linked": 0,
            "source_directories_unlinked": 0,
            "source_directories_visited": 0,
            "source_files_deleted": 0,
            "source_files_linked": 0,
            "source_files_unlinked": 0,
            "sparse_data_bytes": 0,
            "start_time": 1687488892,
            "state": "running",
            "succeeded_chunks": 0,
            "symlinks_replicated": 0,
            "sync_type": "invalid",
            "target_bytes_recovered": 0,
            "target_directories_created": 0,
            "target_directories_deleted": 0,
            "target_directories_linked": 0,
            "target_directories_unlinked": 0,
            "target_files_deleted": 0,
            "target_files_linked": 0,
            "target_files_unlinked": 0,
            "target_snapshots": [],
            "throughput": "0 b/s",
            "total_chunks": 0,
            "total_data_bytes": 0,
            "total_exported_services": None,
            "total_files": 0,
            "total_network_bytes": 0,
            "total_phases": 0,
            "unchanged_data_bytes": 0,
            "up_to_date_files_skipped": 0,
            "updated_files_replicated": 0,
            "user_conflict_files_skipped": 0,
            "warnings": [],
            "workers": [],
            "worm_committed_file_conflicts": 0
        }
    ]
}

MODIFY_SYNCIQ_JOB_PARAMS = {"state": "pause"}


def create_synciq_job_failed_msg():
    return 'Creation of new job is not supported by this ansible module.'


def modify_synciq_job_failed_msg():
    return 'Modify state of SyncIQ job'


def get_synciq_job_empty_id_failed_msg():
    return 'Please enter a valid job_id.'


def modify_synciq_job_state_cancel_failed_msg():
    return 'Please specify the state as absent for cancel.'


def get_synciq_job_failed_msg():
    return 'Get details of SyncIQ job'


def delete_synciq_job_failed_msg():
    return 'Please specify a valid state.'
