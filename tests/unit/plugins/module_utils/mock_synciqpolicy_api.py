# Copyright: (c) 2022, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock Api response for Unit tests of synciqpolicy module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from mock.mock import MagicMock
import copy


class MockSynciqpolicyApi:
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'
    SYNCIQPOLICY_COMMON_ARGS = {
        'onefs_host': '**.***.**.***',
        'policy_name': '',
        'policy_id': '',
        'new_policy_name': '',
        'schedule': '',
        'run_job': '',
        'rpo_alert': '',
        'rpo_alert_unit': '',
        'target_snapshot': '',
        'job_delay': '',
        'job_delay_unit': '',
        'job_params': '',
        'target_cluster': '',
        'source_cluster': '',
        'state': 'present'
    }
    GET_SYNCIQPOLICY_RESPONSE = [{
        'accelerated_failback': False, 'action': 'copy',
        'bandwidth_reservation': None, 'changelist': False,
        'check_integrity': True, 'cloud_deep_copy': 'deny',
        'conflicted': False,
        'database_mirrored': False,
        'delete_quotas': True,
        'description': 'Creating a policy',
        'disable_file_split': False,
        'disable_fofb': False,
        'disable_quota_tmp_dir': False,
        'disable_stf': False,
        'enable_hash_tmpdir': False,
        'enabled': True,
        'encrypted': False,
        'encryption_cipher_list': '',
        'expected_dataloss': False,
        'file_matching_pattern': {'or_criteria': None},
        'force_interface': False,
        'has_sync_state': False,
        'id': 'policy_id_1',
        'job_delay': None,
        'last_job_state': 'unknown',
        'name': 'Policy_SP',
        'priority': 0,
        'restrict_target_network': True,
        'rpo_alert': None,
        'schedule': '',
        'service_policy': False,
        'skip_lookup': None,
        'skip_when_source_unmodified': False,
        'snapshot_sync_existing': False,
        'snapshot_sync_pattern': '*',
        'source_certificate_id': 'source_certificate_id_1',
        'source_domain_marked': False,
        'source_exclude_directories': [],
        'source_include_directories': [],
        'source_network': None,
        'source_root_path': '/test/home',
        'source_snapshot_archive': False,
        'source_snapshot_expiration': 0,
        'source_snapshot_pattern': '',
        'target_certificate_id': '',
        'target_compare_initial_sync': False,
        'target_detect_modifications': True,
        'target_host': 'target_host-1',
        'target_path': '/test/target',
        'target_snapshot_alias': 'SIQ-%{SrcCluster}-%{PolicyName}-latest',
        'target_snapshot_archive': False,
        'target_snapshot_expiration': 0,
        'target_snapshot_pattern': 'SIQ-%{SrcCluster}-%{PolicyName}-%Y-%m-%d_%H-%M-%S',
        'workers_per_node': 3
    }]

    @staticmethod
    def get_synciqpolicy_modify_response():
        synciqpolicy_response = copy.deepcopy(MockSynciqpolicyApi.GET_SYNCIQPOLICY_RESPONSE[0])
        synciqpolicy_response['accelerated_failback'] = True
        return synciqpolicy_response

    @staticmethod
    def get_api_exception_messages(response_type):
        if response_type == 'create':
            return 'Creating SyncIQ policy Policy_SP failed with error : SDK Error message'
        elif response_type == 'modify':
            return 'Failed to modify SyncIQ policy with error : SDK Error message'
