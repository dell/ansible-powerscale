# Copyright: (c) 2023, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of SyncIQ global settings module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockSyncIQGlobalSettingsApi:
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'

    SYNCIQ_GLOBAL_COMMON_ARGS = {
        "onefs_host": "**.***.**.***",
        "encryption_required": None,
        "service": None
    }
    GET_SYNCIQ_GLOBAL_RESPONSE = {
        "bandwidth_reservation_reserve_absolute": None,
        "bandwidth_reservation_reserve_percentage": 1,
        "cluster_certificate_id": "1234abc",
        "encryption_cipher_list": None,
        "encryption_required": False,
        "force_interface": False,
        "max_concurrent_jobs": 16,
        "ocsp_address": "",
        "ocsp_issuer_certificate_id": "",
        "preferred_rpo_alert": 0,
        "renegotiation_period": 28800,
        "report_email": [],
        "report_max_age": 31536000,
        "report_max_count": 2000,
        "restrict_target_network": False,
        "rpo_alerts": True,
        "service": "on",
        "service_history_max_age": 31536000,
        "service_history_max_count": 2000,
        "source_network": None,
        "tw_chkpt_interval": None,
        "use_workers_per_node": False
    }

    @staticmethod
    def get_synciq_global_settings_exception_response(response_type):
        if response_type == 'get_details_exception':
            return "Got error SDK Error message while getting SyncIQ global setings details "
        elif response_type == 'update_exception':
            return "Modify SyncIQ global settings failed with error: SDK Error message"
