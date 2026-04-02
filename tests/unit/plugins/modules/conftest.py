# Copyright: (c) 2025, Dell Technologies
# Conftest to handle ansible-core 2.19+ argparse compatibility with pytest

import sys
import json
import pytest
from mock.mock import MagicMock


UTILS_PATH = 'ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.utils'


@pytest.fixture(autouse=True, scope="function")
def _patch_ansible_for_unit_tests(monkeypatch, mocker):
    """Patch ansible-core 2.19 argparse and SDK connection for unit tests.

    Ansible-core 2.19 changed _load_params to use argparse which conflicts
    with pytest command-line arguments. This fixture provides the required
    module arguments via sys.argv so AnsibleModule can initialize properly.
    It also mocks SDK connection functions to prevent real API calls.
    """
    args = {
        "ANSIBLE_MODULE_ARGS": {
            "onefs_host": "test.example.com",
            "api_user": "admin",
            "api_password": "test_password",
            "verify_ssl": "False"
        }
    }
    monkeypatch.setattr(
        sys, 'argv',
        [sys.argv[0], json.dumps(args)]
    )

    # Mock SDK validation and connection to prevent real API calls
    mocker.patch(
        f'{UTILS_PATH}.validate_module_pre_reqs',
        return_value=dict(all_packages_found=True, error_message=None)
    )
    mocker.patch(
        f'{UTILS_PATH}.get_powerscale_connection',
        return_value=MagicMock()
    )
    mocker.patch(
        f'{UTILS_PATH}.get_powerscale_sdk',
        return_value=MagicMock()
    )
