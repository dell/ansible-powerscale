# Copyright: (c) 2021-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for access zone module on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock import (
    utils,
)
from mock.mock import MagicMock

from ansible_collections.dellemc.powerscale.plugins.modules.accesszone import AccessZone
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils import (
    mock_accesszone_api as MockAccessZoneApi,
)
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_sdk_response import (
    MockSDKResponse,
)
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception import (
    MockApiException,
)
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import (
    PowerScaleUnitBase,
)


class TestAccessZone(PowerScaleUnitBase):
    get_access_zone_args = {
        "az_name": None,
        "groupnet": None,
        "path": None,
        "state": None,
        "create_path": None,
        "provider_state": None,
        "auth_providers": [{"provider_name": None, "provider_type": None}],
    }

    @pytest.fixture
    def module_object(self):
        return AccessZone

    def test_create_access_zone_parmset1(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {
                "az_name": "testaz",
                "groupnet": "groupnet1",
                "path": "/ifs",
                "smb": None,
                "nfs": None,
                "force_overlap": True,
                "state": "present",
                "create_path": False,
                "provider_state": "add",
                "auth_providers": [
                    {"provider_name": "System", "provider_type": "file"}
                ],
            },
        )
        powerscale_module_mock.get_details = MagicMock(return_value=[])
        powerscale_module_mock.api_instance.create_zone = MagicMock(
            return_value=MockSDKResponse(
                MockAccessZoneApi.ACCESS_ZONE_DETAILS_1["zones"][0]
            )
        )
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_create_access_zone_parmset2(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {
                "az_name": "testaz",
                "groupnet": "groupnet1",
                "path": "/ifs",
                "smb": None,
                "nfs": None,
                "force_overlap": False,
                "state": "present",
                "create_path": True,
                "provider_state": "add",
                "auth_providers": [
                    {"provider_name": "System", "provider_type": "local"}
                ],
            },
        )
        powerscale_module_mock.api_instance.get_zone().to_dict = MagicMock(
            side_effect=MockApiException(404)
        )
        powerscale_module_mock.api_instance.create_zone = MagicMock(
            return_value=MockSDKResponse(
                MockAccessZoneApi.ACCESS_ZONE_DETAILS_1["zones"][0]
            )
        )
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_create_access_zone_parmset3(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {
                "az_name": "testaz",
                "groupnet": "groupnet1",
                "path": "/ifs",
                "smb": None,
                "nfs": None,
                "force_overlap": True,
                "state": "present",
                "create_path": False,
                "provider_state": "add",
                "auth_providers": [
                    {"provider_name": "nis-server", "provider_type": "nis"}
                ],
            },
        )
        powerscale_module_mock.get_details = MagicMock(return_value=[])
        powerscale_module_mock.api_instance.create_zone = MagicMock(
            return_value=MockSDKResponse(
                MockAccessZoneApi.ACCESS_ZONE_DETAILS_1["zones"][0]
            )
        )
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_create_access_zone_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {
                "az_name": "testaz",
                "groupnet": "groupnet1",
                "path": "/ifs",
                "smb": None,
                "nfs": None,
                "force_overlap": False,
                "state": "present",
                "create_path": True,
                "provider_state": "add",
                "auth_providers": [
                    {"provider_name": "System", "provider_type": "file"}
                ],
            },
        )
        powerscale_module_mock.get_details = MagicMock(return_value=[])
        powerscale_module_mock.api_instance.create_zone = MagicMock(
            side_effect=utils.ApiException
        )
        self.capture_fail_json_method(
            MockAccessZoneApi.get_error_message(
                "create_zone_exception", az_name="testaz"
            ),
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_create_access_zone_without_path_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {
                "az_name": "testaz",
                "groupnet": "groupnet1",
                "path": None,
                "smb": None,
                "nfs": None,
                "force_overlap": False,
                "state": "present",
                "create_path": True,
                "provider_state": "add",
                "auth_providers": [
                    {"provider_name": "System", "provider_type": "file"}
                ],
            },
        )
        powerscale_module_mock.get_details = MagicMock(return_value=[])
        self.capture_fail_json_method(
            MockAccessZoneApi.get_error_message(
                "create_zone_without_path_exception", az_name="testaz"
            ),
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_delete_access_zone(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {
                "az_name": "testaz",
                "groupnet": "groupnet1",
                "path": "/ifs",
                "smb": None,
                "nfs": None,
                "force_overlap": True,
                "state": "absent",
                "create_path": False,
                "provider_state": "add",
                "auth_providers": [
                    {"provider_name": "System", "provider_type": "file"}
                ],
            },
        )
        powerscale_module_mock.get_details = MagicMock(
            return_value=MockAccessZoneApi.ACCESS_ZONE_DETAILS_1
        )
        powerscale_module_mock.api_instance.delete_zone = MagicMock(return_value=None)
        powerscale_module_mock.perform_module_operation()
        powerscale_module_mock.api_instance.delete_zone.assert_called()
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_delete_access_zone_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {
                "az_name": "testaz",
                "groupnet": "groupnet1",
                "path": "/ifs",
                "smb": None,
                "nfs": None,
                "force_overlap": True,
                "state": "absent",
                "create_path": False,
                "provider_state": "add",
                "auth_providers": [
                    {"provider_name": "System", "provider_type": "file"}
                ],
            },
        )
        powerscale_module_mock.get_details = MagicMock(
            return_value=MockAccessZoneApi.ACCESS_ZONE_DETAILS_1
        )
        powerscale_module_mock.api_instance.delete_zone = MagicMock(
            side_effect=MockApiException
        )
        self.capture_fail_json_method(
            MockAccessZoneApi.get_error_message(
                "delete_zone_exception",
            ),
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_get_access_zone_details(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {"az_name": "testaz", "smb": None, "nfs": None, "state": "present"},
        )
        powerscale_module_mock.api_instance.get_zone().to_dict = MagicMock(
            return_value=MockAccessZoneApi.ACCESS_ZONE_DETAILS_1
        )
        powerscale_module_mock.api_protocol.get_nfs_settings_export().to_dict = (
            MagicMock(return_value=MockAccessZoneApi.NFS_EXPORT_SETTINGS)
        )
        powerscale_module_mock.api_protocol.get_nfs_settings_zone().to_dict = MagicMock(
            return_value=MockAccessZoneApi.NFS_ZONE_SETTINGS
        )
        powerscale_module_mock.api_protocol.get_smb_settings_share().to_dict = (
            MagicMock(return_value=MockAccessZoneApi.SMB_SHARE_SETTINGS)
        )
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is False

    def test_get_access_zone_details_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {"az_name": "testaz", "smb": None, "nfs": None, "state": "present"},
        )
        powerscale_module_mock.api_instance.get_zone().to_dict = MagicMock(
            side_effect=Exception
        )
        self.capture_fail_json_method(
            MockAccessZoneApi.get_error_message("get_zone_exception", az_name="testaz"),
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_get_access_zone_details_api_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {"az_name": "testaz", "smb": None, "nfs": None, "state": "present"},
        )
        powerscale_module_mock.api_instance.get_zone().to_dict = MagicMock(
            side_effect=utils.ApiException
        )
        self.capture_fail_json_method(
            MockAccessZoneApi.get_error_message("get_zone_exception", az_name="testaz"),
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_add_provider_type_no_exist_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {
                "az_name": "testaz",
                "groupnet": "groupnet1",
                "path": "/ifs",
                "smb": None,
                "nfs": None,
                "state": "present",
                "provider_state": "add",
                "auth_providers": [
                    {"provider_name": "System", "provider_type": "file"}
                ],
            },
        )
        powerscale_module_mock.get_details = MagicMock(
            return_value=MockAccessZoneApi.ACCESS_ZONE_DETAILS_1
        )
        self.capture_fail_json_method(
            MockAccessZoneApi.get_error_message(
                "provider_type_no_exist_exception", az_name="testaz"
            ),
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_add_provider1(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {
                "az_name": "testaz",
                "groupnet": "groupnet1",
                "path": "/ifs",
                "smb": None,
                "nfs": None,
                "state": "present",
                "provider_state": "add",
                "auth_providers": [
                    {
                        "provider_name": "System",
                        "provider_type": "file",
                        "priority": None,
                    }
                ],
            },
        )
        provider1 = MockAccessZoneApi.ProviderSummary(
            id="test_id", name="System", type="file"
        )
        provider_summary = MagicMock(spec=MockAccessZoneApi.ProviderSummary)
        provider_summary.provider_instances = [provider1]
        powerscale_module_mock.get_details = MagicMock(
            return_value=MockAccessZoneApi.ACCESS_ZONE_DETAILS_1
        )
        powerscale_module_mock.api_auth.get_providers_summary = MagicMock(
            return_value=provider_summary
        )
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_add_provider2(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {
                "az_name": "testaz",
                "groupnet": "groupnet1",
                "path": "/ifs",
                "smb": None,
                "nfs": None,
                "state": "present",
                "provider_state": "add",
                "auth_providers": [
                    {
                        "provider_name": "LDAP",
                        "provider_type": "ldap",
                        "priority": 2,
                    },
                    {
                        "provider_name": "ADS",
                        "provider_type": "ads",
                        "priority": 1,
                    },
                ],
            },
        )
        provider1 = MockAccessZoneApi.ProviderSummary(
            id="ldap:ansildap", name="LDAP", type="ldap"
        )
        provider2 = MockAccessZoneApi.ProviderSummary(
            id="test_ad_provider", name="ADS", type="ads"
        )
        provider_summary = MagicMock(spec=MockAccessZoneApi.ProviderSummary)
        provider_summary.provider_instances = [provider1, provider2]
        powerscale_module_mock.get_details = MagicMock(
            return_value=MockAccessZoneApi.ACCESS_ZONE_DETAILS_1
        )
        powerscale_module_mock.api_auth.get_providers_summary = MagicMock(
            return_value=provider_summary
        )
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_add_provider_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {
                "az_name": "testaz",
                "groupnet": "groupnet1",
                "path": "/ifs",
                "smb": None,
                "nfs": None,
                "state": "present",
                "provider_state": "add",
                "auth_providers": [
                    {
                        "provider_name": "System",
                        "provider_type": "file",
                        "priority": None,
                    }
                ],
            },
        )
        provider1 = MockAccessZoneApi.ProviderSummary(
            id="test_id", name="System", type="file"
        )
        provider_summary = MagicMock(spec=MockAccessZoneApi.ProviderSummary)
        provider_summary.provider_instances = [provider1]
        powerscale_module_mock.get_details = MagicMock(
            return_value=MockAccessZoneApi.ACCESS_ZONE_DETAILS_1
        )
        powerscale_module_mock.api_auth.get_providers_summary = MagicMock(
            return_value=provider_summary
        )
        powerscale_module_mock.reorder_auth_providers = MagicMock(
            side_effect=MockApiException
        )
        self.capture_fail_json_method(
            MockAccessZoneApi.get_error_message(
                "add_provider_exception", az_name="testaz"
            ),
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_remove_provider_type_no_exist_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {
                "az_name": "testaz",
                "groupnet": "groupnet1",
                "path": "/ifs",
                "smb": None,
                "nfs": None,
                "state": "present",
                "provider_state": "remove",
                "auth_providers": [
                    {"provider_name": "System", "provider_type": "file"}
                ],
            },
        )
        powerscale_module_mock.get_details = MagicMock(
            return_value=MockAccessZoneApi.ACCESS_ZONE_DETAILS_1
        )
        self.capture_fail_json_method(
            MockAccessZoneApi.get_error_message(
                "provider_type_no_exist_exception", az_name="testaz"
            ),
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_remove_provider(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {
                "az_name": "testaz",
                "groupnet": "groupnet1",
                "path": "/ifs",
                "smb": None,
                "nfs": None,
                "state": "present",
                "provider_state": "remove",
                "auth_providers": [
                    {"provider_name": "ansildap", "provider_type": "ldap"}
                ],
            },
        )
        provider1 = MockAccessZoneApi.ProviderSummary(
            id="ldap:ansildap", name="ansildap", type="ldap"
        )
        provider_summary = MagicMock(spec=MockAccessZoneApi.ProviderSummary)
        provider_summary.provider_instances = [provider1]
        powerscale_module_mock.get_details = MagicMock(
            return_value=MockAccessZoneApi.ACCESS_ZONE_DETAILS_1
        )
        powerscale_module_mock.api_auth.get_providers_summary = MagicMock(
            return_value=provider_summary
        )
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_modify_smb(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {
                "az_name": "testaz",
                "groupnet": "groupnet1",
                "path": "/ifs",
                "smb": {
                    "create_permissions": "default acl",
                    "directory_create_mask": "777",
                    "directory_create_mode": "700",
                    "file_create_mask": "700",
                    "file_create_mode": "100",
                    "access_based_enumeration": True,
                    "access_based_enumeration_root_only": True,
                    "ntfs_acl_support": True,
                    "oplocks": True,
                },
                "nfs": None,
                "state": "present",
            },
        )
        powerscale_module_mock.get_details = MagicMock(
            return_value=MockAccessZoneApi.ACCESS_ZONE_DETAILS_1
        )
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_modify_smb_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {
                "az_name": "testaz",
                "groupnet": "groupnet1",
                "path": "/ifs",
                "smb": {
                    "create_permissions": "default acl",
                    "directory_create_mask": "777",
                    "directory_create_mode": "700",
                    "file_create_mask": "700",
                    "file_create_mode": "100",
                    "access_based_enumeration": True,
                    "access_based_enumeration_root_only": True,
                    "ntfs_acl_support": True,
                    "oplocks": True,
                },
                "nfs": None,
                "state": "present",
            },
        )
        powerscale_module_mock.get_details = MagicMock(
            return_value=MockAccessZoneApi.ACCESS_ZONE_DETAILS_1
        )
        powerscale_module_mock.api_protocol.update_smb_settings_share = MagicMock(
            side_effect=MockApiException
        )
        self.capture_fail_json_method(
            MockAccessZoneApi.get_error_message(
                "modify_smb_exception", az_name="testaz"
            ),
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_modify_smb_conversion_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {
                "az_name": "testaz",
                "groupnet": "groupnet1",
                "path": "/ifs",
                "smb": {
                    "create_permissions": "default acl",
                    "directory_create_mask": "xxx",
                    "directory_create_mode": "700",
                    "file_create_mask": "700",
                    "file_create_mode": "100",
                    "access_based_enumeration": True,
                    "access_based_enumeration_root_only": True,
                    "ntfs_acl_support": True,
                    "oplocks": True,
                },
                "nfs": None,
                "state": "present",
            },
        )
        powerscale_module_mock.get_details = MagicMock(
            return_value=MockAccessZoneApi.ACCESS_ZONE_DETAILS_1
        )
        powerscale_module_mock.api_protocol.update_smb_settings_share = MagicMock(
            side_effect=MockApiException
        )
        self.capture_fail_json_method(
            MockAccessZoneApi.get_error_message("modify_smb_conversion_exception"),
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_modify_nfs(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {
                "az_name": "testaz",
                "groupnet": "groupnet1",
                "path": "/ifs",
                "smb": None,
                "nfs": {
                    "commit_asynchronous": False,
                    "nfsv4_allow_numeric_ids": False,
                    "nfsv4_domain": "localhost",
                    "nfsv4_no_domain": False,
                    "nfsv4_no_domain_uids": False,
                    "nfsv4_no_names": False,
                },
                "state": "present",
            },
        )
        powerscale_module_mock.get_details = MagicMock(
            return_value=MockAccessZoneApi.ACCESS_ZONE_DETAILS_1
        )
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True

    def test_modify_nfs_exception(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {
                "az_name": "testaz",
                "groupnet": "groupnet1",
                "path": "/ifs",
                "smb": None,
                "nfs": {
                    "commit_asynchronous": False,
                    "nfsv4_allow_numeric_ids": False,
                    "nfsv4_domain": "localhost",
                    "nfsv4_no_domain": False,
                    "nfsv4_no_domain_uids": False,
                    "nfsv4_no_names": False,
                },
                "state": "present",
            },
        )
        powerscale_module_mock.get_details = MagicMock(
            return_value=MockAccessZoneApi.ACCESS_ZONE_DETAILS_1
        )
        powerscale_module_mock.api_protocol.update_nfs_settings_export = MagicMock(
            side_effect=MockApiException
        )
        self.capture_fail_json_method(
            MockAccessZoneApi.get_error_message(
                "modify_nfs_exception", az_name="testaz"
            ),
            powerscale_module_mock,
            "perform_module_operation",
        )

    def test_modify_smb_and_nfs(self, powerscale_module_mock):
        self.set_module_params(
            powerscale_module_mock,
            self.get_access_zone_args,
            {
                "az_name": "testaz",
                "groupnet": "groupnet1",
                "path": "/ifs",
                "smb": {
                    "access_based_enumeration": False,
                    "access_based_enumeration_root_only": False,
                    "ntfs_acl_support": False,
                    "oplocks": False,
                },
                "nfs": {
                    "commit_asynchronous": True,
                    "nfsv4_no_names": False,
                },
                "state": "present",
            },
        )
        powerscale_module_mock.get_details = MagicMock(
            return_value=MockAccessZoneApi.ACCESS_ZONE_DETAILS_1
        )
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
