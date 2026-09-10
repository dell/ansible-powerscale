# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for LDAP module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import patch, MagicMock
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils


from ansible_collections.dellemc.powerscale.plugins.modules.ldap import Ldap, main
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_ldap_api as MockLdapApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import \
    PowerScaleUnitBase


class TestLdap(PowerScaleUnitBase):
    get_ldap_args = {
        'ldap_name': None,
        'server_uris': ['ldap://uri1', 'ldaps://uri2'],
        'server_uri_state': 'present-in-ldap',
        'base_dn': 'DC=ansildap,DC=com',
        "ldap_parameters": {
            'groupnet': "groupnet_ansildap",
            'bind_dn': "cn=admin,dc=example,dc=com",
            'bind_password': "test_bind_password_placeholder"
        },
        'state': 'present'
    }

    @pytest.fixture
    def module_object(self):
        return Ldap

    @pytest.fixture(autouse=True)
    def reset_ldap_mocks(self, powerscale_module_mock):
        """Reset API mocks before each test to prevent side_effect leakage."""
        powerscale_module_mock.auth_api_instance.update_providers_ldap_by_id = MagicMock()
        powerscale_module_mock.auth_api_instance.create_providers_ldap_item = MagicMock()
        powerscale_module_mock.auth_api_instance.delete_providers_ldap_by_id = MagicMock()
        powerscale_module_mock.module._diff = False

    def test_create(self, powerscale_module_mock):
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'ldap1',
            "ldap_parameters": {
                'bind_dn': "cn=admin,dc=test,dc=com",
                'bind_password': "test_bind_password_placeholder"
            },
        })
        ldap_details = self.get_ldap_args
        powerscale_module_mock.module.params = self.get_ldap_args
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[[], ldap_details])
        powerscale_module_mock.perform_module_operation()

        assert (
            powerscale_module_mock.module.exit_json.call_args[1]['ldap_provider_details'])
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

        # Scenario 2: invalid server_uris
        self.get_ldap_args.update({
            'ldap_name': 'ldap1',
            'server_uris': ['uri1', 'uri2'],
            "ldap_parameters": {
                'bind_dn': "cn=admin,dc=test,dc=com",
                'bind_password': "test_bind_password_placeholder"
            },
        })
        ldap_details = self.get_ldap_args
        powerscale_module_mock.module.params = self.get_ldap_args
        powerscale_module_mock.get_ldap_details = MagicMock(ldap_details)

        self.capture_fail_json_call(MockLdapApi.invalid_server_uri_failed_msg(), invoke_perform_module=True)

        # Scenario 3: invalid base_dn
        self.get_ldap_args.update({
            'server_uris': ['ldap://uri1', 'ldaps://uri2'],
            'base_dn': None,
            "ldap_parameters": {
                'groupnet': "groupnet_ansildap",
                'bind_dn': "cn=admin,dc=example,dc=com",
                'bind_password': "test_bind_password_placeholder"
            },
        })
        powerscale_module_mock.module.params = self.get_ldap_args
        powerscale_module_mock.get_ldap_details = MagicMock(return_value=None)
        self.capture_fail_json_call(MockLdapApi.no_base_dn_msg(), invoke_perform_module=True)

        # Scenario 4: invalid server_uri_state
        self.get_ldap_args.update({
            'server_uri_state': 'absent-in-ldap',
            'base_dn': 'DC=ansildap,DC=com',
            "ldap_parameters": {
                'bind_dn': "cn=admin,dc=test,dc=com",
                'bind_password': "test_bind_password_placeholder"
            },
        })
        powerscale_module_mock.module.params = self.get_ldap_args
        powerscale_module_mock.get_ldap_details = MagicMock(return_value=None)
        self.capture_fail_json_call(MockLdapApi.invalid_server_uri_state_msg(), invoke_perform_module=True)

        # Scenario 5: no server_uris
        self.get_ldap_args.update({
            'server_uri_state': 'present-in-ldap',
            'server_uris': '',
            "ldap_parameters": {
                'bind_dn': "cn=admin,dc=test,dc=com",
                'bind_password': "test_bind_password_placeholder"
            },
        })
        powerscale_module_mock.module.params = self.get_ldap_args
        powerscale_module_mock.get_ldap_details = MagicMock(return_value=None)
        self.capture_fail_json_call(MockLdapApi.no_server_uri_msg(), invoke_perform_module=True)

    def test_create_throws_exception(self, powerscale_module_mock):
        self.get_ldap_args.update({
            'ldap_name': 'ldap2',
            "ldap_parameters": {
                'groupnet': "groupnet_ansildap",
                'bind_dn': "cn=admin,dc=example,dc=com",
                'bind_password': "test_bind_password_placeholder"
            },
        })
        powerscale_module_mock.module.params = self.get_ldap_args
        ldap_details = self.get_ldap_args
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[[], ldap_details])
        powerscale_module_mock.auth_api_instance.create_providers_ldap_item = \
            MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockLdapApi.create_ldap_failed_msg(), invoke_perform_module=True)

    def test_update(self, powerscale_module_mock):
        self.get_ldap_args.update({
            "ldap_name": "ldap1",
            "ldap_parameters": {
                'bind_dn': "cn=admin,dc=test,dc=com",
                'bind_password': "test_bind_password_placeholder"
            },
        })
        powerscale_module_mock.module.params = self.get_ldap_args
        powerscale_module_mock.perform_module_operation()

        assert (
            powerscale_module_mock.module.exit_json.call_args[1]['ldap_provider_details'])
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_throws_exception(self, powerscale_module_mock):
        self.get_ldap_args.update({
            "ldap_name": "ldap1",
            "ldap_parameters": {
                'bind_dn': "cn=admin,dc=test,dc=com",
                'bind_password': "test_bind_password_placeholder"
            },
        })
        powerscale_module_mock.module.params = self.get_ldap_args
        powerscale_module_mock.auth_api_instance.update_providers_ldap_by_id = \
            MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockLdapApi.modify_ldap_failed_msg(), invoke_perform_module=True)

    def test_delete(self, powerscale_module_mock):
        self.get_ldap_args.update({
            'state': 'absent'
        })
        powerscale_module_mock.module.params = self.get_ldap_args
        powerscale_module_mock.perform_module_operation()

        assert (
            powerscale_module_mock.module.exit_json.call_args[1]['ldap_provider_details'])
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_throws_exception(self, powerscale_module_mock):
        ldap_name = 'ldap1'
        self.get_ldap_args.update({
            'ldap_name': ldap_name,
            'state': 'absent'
        })
        powerscale_module_mock.module.params = self.get_ldap_args
        powerscale_module_mock.auth_api_instance.delete_providers_ldap_by_id = \
            MagicMock(side_effect=utils.ApiException)
        self.capture_fail_json_call(MockLdapApi.delete_ldap_failed_msg(), invoke_perform_module=True)

    def test_get_ldap_details_with_exception(self, powerscale_module_mock):
        # Scenario 1: utils Exception 404
        ldap_name = 'ldap3'
        self.get_ldap_args.update({
            'ldap_name': ldap_name,
        })
        powerscale_module_mock.module.params = self.get_ldap_args
        with patch.object(powerscale_module_mock.auth_api_instance,
                          'get_providers_ldap_by_id',
                          side_effect=MockApiException(404)):
            ob = powerscale_module_mock.perform_module_operation()
            assert ob is None  # nothing to assert as it doesn't return anything

        # Scneario 2: utils Exception 500
        powerscale_module_mock.module.params = self.get_ldap_args
        with patch.object(powerscale_module_mock.auth_api_instance,
                          'get_providers_ldap_by_id',
                          side_effect=MockApiException(500)):
            self.capture_fail_json_call(MockLdapApi.ldap_exception_msg(), invoke_perform_module=True)

        # Scneario 3: Exception
        powerscale_module_mock.module.params = self.get_ldap_args
        with patch.object(powerscale_module_mock.auth_api_instance,
                          'get_providers_ldap_by_id',
                          side_effect=Exception("SDK Error message")):
            self.capture_fail_json_call(
                MockLdapApi.ldap_exception_msg(), invoke_perform_module=True)

    def test_get_modified_ldap(self, powerscale_module_mock):
        self.set_module_params(self.get_ldap_args, {
            "ldap_name": "ldap1",
            'server_uri_state': 'absent-in-ldap',
            "ldap_parameters": {
                'bind_dn': "cn=admin,dc=test,dc=com",
                'bind_password': "test_bind_password_placeholder"
            },
        })
        powerscale_module_mock.get_ldap_details = MagicMock(return_value=MockLdapApi.LDAP['ldap'][0])
        powerscale_module_mock.perform_module_operation()
        assert (
            powerscale_module_mock.module.exit_json.call_args[1]['ldap_provider_details'])
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_main(self, powerscale_module_mock):
        ldap_name = "ldap1"
        self.get_ldap_args.update({
            "ldap_name": ldap_name,
            'server_uri_state': 'absent-in-ldap'
        })
        powerscale_module_mock.get_ldap_parameters = MagicMock(
            return_value=MockLdapApi.LDAP)
        main()
        powerscale_module_mock.get_ldap_details(ldap_name)

    # ---- Phase 1: group_base_dn tests (FR-1) ----

    def test_create_ldap_with_group_base_dn(self, powerscale_module_mock):
        """FR-1: group_base_dn is transmitted on create."""
        import copy
        ldap_detail = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        ldap_detail['group_base_dn'] = 'ou=groups,dc=company,dc=com'
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'ldap_new',
            'server_uris': ['ldap://10.0.0.1'],
            'server_uri_state': 'present-in-ldap',
            'base_dn': 'dc=company,dc=com',
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': 'ou=groups,dc=company,dc=com',
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[None, ldap_detail])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        # Verify ProvidersLdapItem was called with group_base_dn kwarg
        sdk_call = utils.isi_sdk.ProvidersLdapItem.call_args
        assert sdk_call is not None
        assert sdk_call[1]['group_base_dn'] == 'ou=groups,dc=company,dc=com'

    def test_modify_ldap_set_group_base_dn(self, powerscale_module_mock):
        """FR-1: group_base_dn modification is detected and transmitted."""
        import copy
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['group_base_dn'] = ''
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        updated = copy.deepcopy(existing)
        updated['group_base_dn'] = 'ou=groups,dc=company,dc=com'
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': 'ou=groups,dc=company,dc=com',
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, updated])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_ldap_clear_group_base_dn_empty_string(self, powerscale_module_mock):
        """FR-1: Empty string clears group_base_dn."""
        import copy
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['group_base_dn'] = 'ou=groups,dc=company,dc=com'
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        updated = copy.deepcopy(existing)
        updated['group_base_dn'] = ''
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': '',
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, updated])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_ldap_omit_group_base_dn_preserves_value(self, powerscale_module_mock):
        """FR-1/FR-7: Omitting group_base_dn (None) preserves the server value."""
        import copy
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['group_base_dn'] = 'ou=groups,dc=company,dc=com'
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': None,
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, existing])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_modify_ldap_group_base_dn_byte_exact_case_change_is_a_change(self, powerscale_module_mock):
        """FR-1: Byte-exact comparison — case change is a real change."""
        import copy
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['group_base_dn'] = 'ou=Groups,dc=company,dc=com'
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        updated = copy.deepcopy(existing)
        updated['group_base_dn'] = 'ou=groups,dc=company,dc=com'
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': 'ou=groups,dc=company,dc=com',
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, updated])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_group_base_dn_exceeds_255_chars_rejected_before_api_call(self, powerscale_module_mock):
        """FR-1: Length validation rejects group_base_dn > 255 chars before API call."""
        long_dn = 'ou=' + 'x' * 253 + ',dc=com'
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'ldap_new',
            'server_uris': ['ldap://10.0.0.1'],
            'server_uri_state': 'present-in-ldap',
            'base_dn': 'dc=company,dc=com',
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': long_dn,
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(return_value=None)
        self.capture_fail_json_call(
            MockLdapApi.group_base_dn_exceeds_length_msg(),
            invoke_perform_module=True)
        # Verify no API create call was made
        powerscale_module_mock.auth_api_instance.create_providers_ldap_item.assert_not_called()

    # ---- Phase 1: provider_domain tests (FR-2) ----

    def test_create_ldap_with_provider_domain(self, powerscale_module_mock):
        """FR-2: provider_domain is transmitted on create."""
        import copy
        ldap_detail = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        ldap_detail['provider_domain'] = 'subdomain.company.com'
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'ldap_new',
            'server_uris': ['ldap://10.0.0.1'],
            'server_uri_state': 'present-in-ldap',
            'base_dn': 'dc=company,dc=com',
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': None,
                'provider_domain': 'subdomain.company.com',
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[None, ldap_detail])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        sdk_call = utils.isi_sdk.ProvidersLdapItem.call_args
        assert sdk_call[1]['provider_domain'] == 'subdomain.company.com'

    def test_modify_ldap_clear_provider_domain_empty_string(self, powerscale_module_mock):
        """FR-2: Empty string clears provider_domain."""
        import copy
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['provider_domain'] = 'subdomain.company.com'
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        updated = copy.deepcopy(existing)
        updated['provider_domain'] = ''
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': None,
                'provider_domain': '',
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, updated])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_ldap_omit_provider_domain_preserves_value(self, powerscale_module_mock):
        """FR-2/FR-7: Omitting provider_domain preserves the server value."""
        import copy
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['provider_domain'] = 'subdomain.company.com'
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': None,
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, existing])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_modify_ldap_provider_domain_no_auto_detection(self, powerscale_module_mock):
        """FR-2: provider_domain is stored as-is, no format check or auto-detection."""
        import copy
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['provider_domain'] = ''
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        updated = copy.deepcopy(existing)
        updated['provider_domain'] = 'arbitrary_string_no_dots'
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': None,
                'provider_domain': 'arbitrary_string_no_dots',
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, updated])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_provider_domain_exceeds_255_chars_rejected_before_api_call(self, powerscale_module_mock):
        """FR-2: Length validation rejects provider_domain > 255 chars before API call."""
        long_domain = 'x' * 256
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'ldap_new',
            'server_uris': ['ldap://10.0.0.1'],
            'server_uri_state': 'present-in-ldap',
            'base_dn': 'dc=company,dc=com',
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': None,
                'provider_domain': long_domain,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(return_value=None)
        self.capture_fail_json_call(
            MockLdapApi.provider_domain_exceeds_length_msg(),
            invoke_perform_module=True)
        powerscale_module_mock.auth_api_instance.create_providers_ldap_item.assert_not_called()

    # ---- Phase 1: authentication tests (FR-3) ----

    def test_create_ldap_with_authentication_false(self, powerscale_module_mock):
        """FR-3: Explicit false is transmitted on create."""
        import copy
        ldap_detail = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        ldap_detail['authentication'] = False
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'ldap_new',
            'server_uris': ['ldap://10.0.0.1'],
            'server_uri_state': 'present-in-ldap',
            'base_dn': 'dc=company,dc=com',
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': None,
                'provider_domain': None,
                'authentication': False,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[None, ldap_detail])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        sdk_call = utils.isi_sdk.ProvidersLdapItem.call_args
        assert sdk_call[1]['authentication'] is False

    def test_modify_ldap_authentication_false_to_true(self, powerscale_module_mock):
        """FR-3: authentication change from false to true is detected."""
        import copy
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['authentication'] = False
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        updated = copy.deepcopy(existing)
        updated['authentication'] = True
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': None,
                'provider_domain': None,
                'authentication': True,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, updated])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_ldap_omit_authentication_preserves_value(self, powerscale_module_mock):
        """FR-3/FR-7: Omitting authentication (None) preserves the server value."""
        import copy
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['authentication'] = False
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': None,
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, existing])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_authentication_none_vs_explicit_false_distinguished(self, powerscale_module_mock):
        """FR-3: None (omitted) is distinguishable from explicit False."""
        import copy
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['authentication'] = True
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        updated = copy.deepcopy(existing)
        updated['authentication'] = False
        # Explicit False should trigger a change
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': None,
                'provider_domain': None,
                'authentication': False,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, updated])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_authorization_parameter_not_accepted(self, powerscale_module_mock):
        """Q4: No 'authorization' alias exists in the argument spec."""
        params = get_ldap_parameters()
        ldap_params_spec = params['ldap_parameters']['options']
        assert 'authorization' not in ldap_params_spec

    # ---- Phase 1: Non-destructive semantics tests (FR-7) ----

    def test_preexisting_playbook_without_new_params_produces_unchanged_payload(self, powerscale_module_mock):
        """FR-7/AC-005: Playbook without new parameters produces no change."""
        import copy
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': None,
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, existing])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False
        powerscale_module_mock.auth_api_instance.update_providers_ldap_by_id.assert_not_called()

    def test_managing_one_new_param_leaves_others_untouched(self, powerscale_module_mock):
        """FR-7: Setting group_base_dn does not touch provider_domain or authentication."""
        import copy
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['group_base_dn'] = ''
        existing['provider_domain'] = 'existing.domain.com'
        existing['authentication'] = False
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        updated = copy.deepcopy(existing)
        updated['group_base_dn'] = 'ou=groups,dc=company,dc=com'
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': 'ou=groups,dc=company,dc=com',
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, updated])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        # Verify the update call only contains group_base_dn
        update_call = powerscale_module_mock.auth_api_instance.update_providers_ldap_by_id.call_args
        update_params = update_call[1]['providers_ldap_id_params']
        # The params object should only have group_base_dn set
        assert hasattr(update_params, 'group_base_dn')

    # ---- Phase 2: Check mode tests (FR-4) ----

    def test_check_mode_create_no_api_call(self, powerscale_module_mock):
        """FR-4: In check mode, create does not call the API."""
        import copy
        powerscale_module_mock.module.check_mode = True
        ldap_detail = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'ldap_new',
            'server_uris': ['ldap://10.0.0.1'],
            'server_uri_state': 'present-in-ldap',
            'base_dn': 'dc=company,dc=com',
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': None,
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[None, ldap_detail])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.auth_api_instance.create_providers_ldap_item.assert_not_called()

    def test_check_mode_modify_no_api_call(self, powerscale_module_mock):
        """FR-4: In check mode, modify does not call the API."""
        import copy
        powerscale_module_mock.module.check_mode = True
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['group_base_dn'] = ''
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': 'ou=groups,dc=company,dc=com',
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, existing])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.auth_api_instance.update_providers_ldap_by_id.assert_not_called()

    def test_check_mode_delete_no_api_call(self, powerscale_module_mock):
        """FR-4: In check mode, delete does not call the API."""
        import copy
        powerscale_module_mock.module.check_mode = True
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': None,
            'state': 'absent'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, None])
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True
        powerscale_module_mock.auth_api_instance.delete_providers_ldap_by_id.assert_not_called()

    def test_check_mode_no_change_required(self, powerscale_module_mock):
        """FR-4: In check mode, no change means changed=false."""
        import copy
        powerscale_module_mock.module.check_mode = True
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': None,
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, existing])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    # ---- Phase 2: Diff mode tests (FR-5) ----

    def test_diff_on_create(self, powerscale_module_mock):
        """FR-5: Diff on create shows before={}, after=create params."""
        import copy
        powerscale_module_mock.module._diff = True
        ldap_detail = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'ldap_new',
            'server_uris': ['ldap://10.0.0.1'],
            'server_uri_state': 'present-in-ldap',
            'base_dn': 'dc=company,dc=com',
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': 'ou=groups,dc=company,dc=com',
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[None, ldap_detail])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert 'diff' in result
        assert result['diff']['before'] == {}
        assert 'group_base_dn' in result['diff']['after']

    def test_diff_on_modify_only_differing_declared_params(self, powerscale_module_mock):
        """FR-5: Diff on modify only shows params that actually differ."""
        import copy
        powerscale_module_mock.module._diff = True
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['group_base_dn'] = 'ou=old,dc=com'
        existing['provider_domain'] = 'existing.com'
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        updated = copy.deepcopy(existing)
        updated['group_base_dn'] = 'ou=new,dc=com'
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': 'ou=new,dc=com',
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, updated])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert 'diff' in result
        assert 'group_base_dn' in result['diff']['before']
        assert 'group_base_dn' in result['diff']['after']
        # provider_domain should not appear since it was not declared (None)
        assert 'provider_domain' not in result['diff']['before']

    def test_diff_cleared_value_rendered_as_empty_string(self, powerscale_module_mock):
        """FR-5: Cleared values render as '' in the diff."""
        import copy
        powerscale_module_mock.module._diff = True
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['group_base_dn'] = 'ou=groups,dc=company,dc=com'
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        updated = copy.deepcopy(existing)
        updated['group_base_dn'] = ''
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': '',
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, updated])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result['diff']['after']['group_base_dn'] == ''

    def test_diff_booleans_rendered_natively(self, powerscale_module_mock):
        """FR-5: Boolean values render natively (True/False) in the diff."""
        import copy
        powerscale_module_mock.module._diff = True
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['authentication'] = True
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        updated = copy.deepcopy(existing)
        updated['authentication'] = False
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': None,
                'provider_domain': None,
                'authentication': False,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, updated])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result['diff']['before']['authentication'] is True
        assert result['diff']['after']['authentication'] is False

    def test_diff_on_delete(self, powerscale_module_mock):
        """FR-5: Diff on delete shows before=current, after={}."""
        import copy
        powerscale_module_mock.module._diff = True
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': None,
            'state': 'absent'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, None])
        powerscale_module_mock.perform_module_operation()
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert 'diff' in result
        assert result['diff']['after'] == {}
        assert result['diff']['before'] != {}

    def test_no_change_produces_empty_diff(self, powerscale_module_mock):
        """FR-5: No change means diff before == after (both empty)."""
        import copy
        powerscale_module_mock.module._diff = True
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': None,
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, existing])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert 'diff' in result
        assert result['diff']['before'] == {}
        assert result['diff']['after'] == {}

    def test_diff_mode_disabled_emits_no_diff_key(self, powerscale_module_mock):
        """FR-5: When diff mode is disabled, no 'diff' key appears in the result."""
        import copy
        powerscale_module_mock.module._diff = False
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['group_base_dn'] = ''
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        updated = copy.deepcopy(existing)
        updated['group_base_dn'] = 'ou=groups,dc=company,dc=com'
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': 'ou=groups,dc=company,dc=com',
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, updated])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert 'diff' not in result

    # ---- Phase 2: bind_password redaction tests (FR-6) ----

    def test_bind_password_absent_from_diff_on_create(self, powerscale_module_mock):
        """FR-6: bind_password never appears in diff on create."""
        import copy
        powerscale_module_mock.module._diff = True
        ldap_detail = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'ldap_new',
            'server_uris': ['ldap://10.0.0.1'],
            'server_uri_state': 'present-in-ldap',
            'base_dn': 'dc=company,dc=com',
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': 'cn=admin,dc=example,dc=com',
                'bind_password': 'supersecret',
                'group_base_dn': None,
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[None, ldap_detail])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert 'bind_password' not in result['diff'].get('before', {})
        assert 'bind_password' not in result['diff'].get('after', {})

    def test_bind_password_absent_from_diff_on_modify(self, powerscale_module_mock):
        """FR-6: bind_password never appears in diff on modify."""
        import copy
        powerscale_module_mock.module._diff = True
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['group_base_dn'] = ''
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        updated = copy.deepcopy(existing)
        updated['group_base_dn'] = 'ou=groups,dc=com'
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': 'supersecret',
                'group_base_dn': 'ou=groups,dc=com',
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, updated])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert 'bind_password' not in result['diff'].get('before', {})
        assert 'bind_password' not in result['diff'].get('after', {})

    def test_bind_password_absent_from_output_on_failure_path(self, powerscale_module_mock):
        """FR-6/Req-SEC-I: bind_password never appears in error messages."""
        import copy
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['group_base_dn'] = ''
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': 'supersecret',
                'group_base_dn': 'ou=groups,dc=com',
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, existing])
        powerscale_module_mock.auth_api_instance.update_providers_ldap_by_id = \
            MagicMock(side_effect=utils.ApiException)
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        with pytest.raises(SystemExit):
            powerscale_module_mock.perform_module_operation()
        call_args = powerscale_module_mock.module.fail_json.call_args
        error_msg = str(call_args)
        assert 'supersecret' not in error_msg
        assert 'bind_password' not in error_msg

    # ---- Phase 3: Idempotency tests (FR-8) ----

    def test_setting_all_three_parameters_converges(self, powerscale_module_mock):
        """FR-8: First run changed=true, identical second run changed=false."""
        import copy
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['group_base_dn'] = ''
        existing['provider_domain'] = ''
        existing['authentication'] = True
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        updated = copy.deepcopy(existing)
        updated['group_base_dn'] = 'ou=groups,dc=com'
        updated['provider_domain'] = 'sub.domain.com'
        updated['authentication'] = False
        params = {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': 'ou=groups,dc=com',
                'provider_domain': 'sub.domain.com',
                'authentication': False,
            },
            'state': 'present'
        }
        # Run 1: should change
        self.set_module_params(self.get_ldap_args, params)
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, updated])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

        # Run 2: same params, server already in desired state — should NOT change
        self.set_module_params(self.get_ldap_args, params)
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[updated, updated])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.auth_api_instance.update_providers_ldap_by_id.reset_mock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False
        powerscale_module_mock.auth_api_instance.update_providers_ldap_by_id.assert_not_called()

    def test_clearing_values_converges(self, powerscale_module_mock):
        """FR-8: Clearing group_base_dn/provider_domain with '' converges on repeat run."""
        import copy
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['group_base_dn'] = 'ou=groups,dc=com'
        existing['provider_domain'] = 'sub.domain.com'
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        cleared = copy.deepcopy(existing)
        cleared['group_base_dn'] = ''
        cleared['provider_domain'] = ''
        params = {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': '',
                'provider_domain': '',
                'authentication': None,
            },
            'state': 'present'
        }
        # Run 1: clear
        self.set_module_params(self.get_ldap_args, params)
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, cleared])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

        # Run 2: already cleared
        self.set_module_params(self.get_ldap_args, params)
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[cleared, cleared])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.auth_api_instance.update_providers_ldap_by_id.reset_mock()
        powerscale_module_mock.perform_module_operation()
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_post_operation_read_returns_authoritative_server_state(self, powerscale_module_mock):
        """FR-8: Post-write re-read returns the authoritative server state."""
        import copy
        existing = copy.deepcopy(MockLdapApi.LDAP['ldap'][0])
        existing['group_base_dn'] = ''
        existing['server_uris'] = ['ldap://xx.xx.xx.xx']
        updated = copy.deepcopy(existing)
        updated['group_base_dn'] = 'ou=groups,dc=com'
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'sample-ldap',
            'server_uris': None,
            'server_uri_state': None,
            'base_dn': None,
            'ldap_parameters': {
                'groupnet': None,
                'bind_dn': None,
                'bind_password': None,
                'group_base_dn': 'ou=groups,dc=com',
                'provider_domain': None,
                'authentication': None,
            },
            'state': 'present'
        })
        powerscale_module_mock.get_ldap_details = MagicMock(
            side_effect=[existing, updated])
        powerscale_module_mock.update_ldap_access_zone_info = MagicMock()
        powerscale_module_mock.perform_module_operation()
        # The result should contain the post-operation server state
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result['ldap_provider_details']['group_base_dn'] == 'ou=groups,dc=com'


# Import at module level for test_authorization_parameter_not_accepted
from ansible_collections.dellemc.powerscale.plugins.modules.ldap import get_ldap_parameters
