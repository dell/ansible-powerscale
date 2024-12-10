# Copyright: (c) 2022-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of synciqpolicy module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockSynciqpolicyApi:
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'
    SYNCIQPOLICY_COMMON_ARGS = {
        'onefs_host': '**.***.**.***',
        'policy_name': '',
        'policy_id': '',
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

    CREATE_ARGS = {
        "action": "sync",
        "description": "Creating a policy",
        "enabled": False,
        "policy_name": "Policy1",
        "run_job": "when-source-modified",
        "job_delay": 10,
        "job_delay_unit": "hours",
        "source_cluster": {
            "source_root_path": "/test",
            "source_exclude_directories": "/test/abc2",
            "source_include_directories": [
                "/test/abc1"
            ],
            "source_network": {
                "pool": "pool0",
                "subnet": "subnet0"
            }
        },
        "target_cluster": {
            "target_host": "xx.xx.xx.xx",
            "target_path": "/test/system",
            "target_certificate_id": "xxxxxxx"
        },
        "target_snapshot": {
            "target_snapshot_archive": True,
            "target_snapshot_expiration": 90,
            "exp_time_unit": "days"
        },
        "state": "present"
    }

    DELETE_ARGS = {"policy_name": "Policy1", "state": "absent"}

    JOB_ARGS1 = {
        "job_params": {
            "workers_per_node": 3,
            "action": "allow_write",
            "source_snapshot": "test_snap",
            "wait_for_completion": False
        }
    }

    JOB_ARGS2 = {
        "job_params": {
            "action": "run",
            "source_snapshot": "test_snap",
            "wait_for_completion": True
        }
    }

    JOB_ARGS3 = {
        "job_params": {
            "workers_per_node": 3,
            "action": "run",
            "source_snapshot": "test_snap",
            "wait_for_completion": True
        }
    }

    JOB_ARGS4 = {
        "job_params": {
            "workers_per_node": 0,
            "action": "allow_write",
            "source_snapshot": "test_snap",
            "wait_for_completion": True
        }
    }

    GET_ARGS = {"policy_name": "Policy1"}

    GET_ARGS2 = {}
    GET_ARGS2.update(GET_ARGS)
    GET_ARGS2.update({"policy_id": 23})

    CREATE_ARGS2 = CREATE_ARGS.copy()
    CREATE_ARGS2["run_job"] = "manual"

    CREATE_JOB_ARGS = {}
    CREATE_JOB_ARGS.update(CREATE_ARGS)
    CREATE_JOB_ARGS.update(JOB_ARGS1)

    POLICY_ID = 'xx'
    EXCEPTION_MSG = "SyncIQ policy"
    CERT_NAME = "cert1"
