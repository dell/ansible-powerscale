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
            'bind_password': "bind_password"
        },
        'state': 'present'
    }

    @pytest.fixture
    def module_object(self):
        return Ldap

    def test_create(self, powerscale_module_mock):
        self.set_module_params(self.get_ldap_args, {
            'ldap_name': 'ldap1',
            "ldap_parameters": {
                'bind_dn': "cn=admin,dc=test,dc=com",
                'bind_password': "bind_password"
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
                'bind_password': "bind_password"
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
                'bind_password': "bind_password"
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
                'bind_password': "bind_password"
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
                'bind_password': "bind_password"
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
                'bind_password': "bind_password"
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
                'bind_password': "bind_password"
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
                'bind_password': "bind_password"
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
                'bind_password': "bind_password"
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
