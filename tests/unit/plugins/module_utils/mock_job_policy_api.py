# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Mock Api response for Unit tests of Job Policy module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockJobPolicyApi:
    """MockJobPolicyApi definition."""
    MODULE_UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'

    JOB_POLICY_COMMON_ARGS = {
        "onefs_host": "**.***.**.***",
        "policy_name": None,
        "policy_id": None,
        "state": "present",
        "intervals": None,
        "description": None
    }

    CREATE_JOB_POLICY_ARGS = {
        "policy_name": "LOW_IMPACT",
        "intervals": [
            {"begin": "Monday 18:00", "end": "Monday 06:00", "impact": "Low"}
        ],
        "state": "present"
    }

    CREATE_JOB_POLICY_WITH_DESC_ARGS = {
        "policy_name": "NIGHT_OPS",
        "description": "Night operations",
        "intervals": [
            {"begin": "Monday 22:00", "end": "Tuesday 06:00", "impact": "Medium"}
        ],
        "state": "present"
    }

    MODIFY_JOB_POLICY_INTERVALS_ARGS = {
        "policy_name": "LOW_IMPACT_HOURS",
        "intervals": [
            {"begin": "Monday 20:00", "end": "Tuesday 08:00", "impact": "Low"},
            {"begin": "Wednesday 20:00", "end": "Thursday 08:00", "impact": "Low"}
        ],
        "state": "present"
    }

    MODIFY_JOB_POLICY_DESC_ARGS = {
        "policy_name": "LOW_IMPACT_HOURS",
        "description": "Updated description for low impact hours policy",
        "state": "present"
    }

    DELETE_JOB_POLICY_ARGS = {
        "policy_name": "LOW_IMPACT",
        "state": "absent"
    }

    GET_JOB_POLICY_ARGS = {
        "policy_name": "LOW_IMPACT"
    }

    GET_JOB_POLICY_BY_ID_ARGS = {
        "policy_id": "LOW_IMPACT"
    }

    CREATE_JOB_POLICY_RESPONSE = {
        "id": "LOW_IMPACT"
    }

    GET_JOB_POLICY_RESPONSE = {
        "id": "LOW_IMPACT_HOURS",
        "name": "LOW_IMPACT_HOURS",
        "description": "",
        "intervals": [
            {"begin": "Monday 18:00", "end": "Monday 06:00", "impact": "Low"}
        ]
    }

    LIST_JOB_POLICIES_RESPONSE = {
        "policies": [
            {
                "id": "LOW",
                "name": "LOW",
                "description": "Impact-throttled to use fewer cluster resources",
                "intervals": []
            },
            {
                "id": "MEDIUM",
                "name": "MEDIUM",
                "description": "Balanced between throughput and impact",
                "intervals": []
            },
            {
                "id": "HIGH",
                "name": "HIGH",
                "description": "Optimized for throughput",
                "intervals": []
            },
            {
                "id": "LOW_IMPACT",
                "name": "LOW_IMPACT",
                "description": "",
                "intervals": [
                    {"begin": "Monday 18:00", "end": "Monday 06:00", "impact": "Low"}
                ]
            },
            {
                "id": "LOW_IMPACT_HOURS",
                "name": "LOW_IMPACT_HOURS",
                "description": "",
                "intervals": [
                    {"begin": "Monday 18:00", "end": "Monday 06:00", "impact": "Low"}
                ]
            }
        ]
    }

    @staticmethod
    def get_job_policy_exception_response(response_type):
        """Get job policy exception response."""
        if response_type == 'create_exception':
            return "Failed to create policy with error:"
        elif response_type == 'get_exception':
            return "Failed to get job policy details with error:"
        elif response_type == 'modify_exception':
            return "Failed to modify job policy with error:"
        elif response_type == 'delete_exception':
            return "Failed to delete job policy with error:"
        elif response_type == 'list_exception':
            return "Failed to list job policies with error:"
        elif response_type == 'policy_name_required':
            return "policy_name is required to create or modify a job policy"
        elif response_type == 'invalid_policy_name':
            return "Invalid policy_name provided"
