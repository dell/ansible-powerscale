# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for LDAP module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils


from ansible_collections.dellemc.powerscale.plugins.modules.ldap import Ldap, main
from ansible_collections.dellemc.powerscale.tests.unit.plugins.\
    module_utils import mock_ldap_api as MockLdapApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException


class TestLdap():
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
    def ldap_module_mock(self, mocker):
        mocker.patch(MockLdapApi.MODULE_UTILS_PATH +
                     '.ApiException', new=MockApiException)
        ldap_module_mock = Ldap()
        ldap_module_mock.module = MagicMock()
        return ldap_module_mock

    def test_create(self, ldap_module_mock):
        self.get_ldap_args.update({
            'ldap_name': 'ldap1',
        })
        ldap_details = self.get_ldap_args
        ldap_module_mock.module.params = self.get_ldap_args
        ldap_module_mock.get_ldap_details = MagicMock(
            side_effect=[[], ldap_details])
        ldap_module_mock.perform_module_operation()

        assert (
            ldap_module_mock.module.exit_json.call_args[1]['ldap_provider_details'])
        assert ldap_module_mock.module.exit_json.call_args[1]['changed'] is True

        # Scenario 2: invalid server_uris
        self.get_ldap_args.update({
            'ldap_name': 'ldap1',
            'server_uris': ['uri1', 'uri2']
        })
        ldap_details = self.get_ldap_args
        ldap_module_mock.module.params = self.get_ldap_args
        ldap_module_mock.get_ldap_details = MagicMock(ldap_details)
        ldap_module_mock.perform_module_operation()

        assert MockLdapApi.invalid_server_uri_failed_msg() in \
            ldap_module_mock.module.fail_json.call_args[1]['msg']

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
        ldap_module_mock.module.params = self.get_ldap_args
        ldap_module_mock.get_ldap_details = MagicMock(return_value=None)
        ldap_module_mock.perform_module_operation()

        assert MockLdapApi.no_base_dn_msg() in \
            ldap_module_mock.module.fail_json.call_args[1]['msg']

        # Scenario 4: invalid server_uri_state
        self.get_ldap_args.update({
            'server_uri_state': 'absent-in-ldap',
            'base_dn': 'DC=ansildap,DC=com',
        })
        ldap_module_mock.module.params = self.get_ldap_args
        ldap_module_mock.get_ldap_details = MagicMock(return_value=None)
        ldap_module_mock.perform_module_operation()

        assert MockLdapApi.invalid_server_uri_state_msg() in \
            ldap_module_mock.module.fail_json.call_args[1]['msg']

        # Scenario 5: no server_uris
        self.get_ldap_args.update({
            'server_uri_state': 'present-in-ldap',
            'server_uris': ''
        })
        ldap_module_mock.module.params = self.get_ldap_args
        ldap_module_mock.get_ldap_details = MagicMock(return_value=None)
        ldap_module_mock.perform_module_operation()

        assert MockLdapApi.no_server_uri_msg() in \
            ldap_module_mock.module.fail_json.call_args[1]['msg']

    def test_create_throws_exception(self, ldap_module_mock):
        self.get_ldap_args.update({
            'ldap_name': 'ldap2',
            "ldap_parameters": {
                'groupnet': "groupnet_ansildap",
                'bind_dn': "cn=admin,dc=example,dc=com",
                'bind_password': "bind_password"
            },
        })
        ldap_module_mock.module.params = self.get_ldap_args
        ldap_details = self.get_ldap_args
        ldap_module_mock.get_ldap_details = MagicMock(
            side_effect=[[], ldap_details])
        ldap_module_mock.auth_api_instance.create_providers_ldap_item = \
            MagicMock(side_effect=utils.ApiException)
        ldap_module_mock.perform_module_operation()

        assert MockLdapApi.create_ldap_failed_msg() in \
            ldap_module_mock.module.fail_json.call_args[1]['msg']

    def test_update(self, ldap_module_mock):
        self.get_ldap_args.update({
            "ldap_name": "ldap1",
            "ldap_parameters": {
                'groupnet': "groupnet_ansildap",
                'bind_dn': "cn=admin,dc=test,dc=com",
                'bind_password': "bind_password"
            },
        })
        ldap_module_mock.module.params = self.get_ldap_args
        ldap_module_mock.perform_module_operation()

        assert (
            ldap_module_mock.module.exit_json.call_args[1]['ldap_provider_details'])
        assert ldap_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_throws_exception(self, ldap_module_mock):
        self.get_ldap_args.update({
            "ldap_name": "ldap1",
            "ldap_parameters": {
                'bind_dn': "cn=admin,dc=test,dc=com",
                'bind_password': "bind_password"
            },
        })
        ldap_module_mock.module.params = self.get_ldap_args
        ldap_module_mock.auth_api_instance.update_providers_ldap_by_id = \
            MagicMock(side_effect=utils.ApiException)
        ldap_module_mock.perform_module_operation()

        assert MockLdapApi.modify_ldap_failed_msg() in \
            ldap_module_mock.module.fail_json.call_args[1]['msg']

    def test_delete(self, ldap_module_mock):
        self.get_ldap_args.update({
            'state': 'absent'
        })
        ldap_module_mock.module.params = self.get_ldap_args
        ldap_module_mock.perform_module_operation()

        assert (
            ldap_module_mock.module.exit_json.call_args[1]['ldap_provider_details'])
        assert ldap_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_delete_throws_exception(self, ldap_module_mock):
        ldap_name = 'ldap1'
        self.get_ldap_args.update({
            'ldap_name': ldap_name,
            'state': 'absent'
        })
        ldap_module_mock.module.params = self.get_ldap_args
        ldap_module_mock.auth_api_instance.delete_providers_ldap_by_id = \
            MagicMock(side_effect=utils.ApiException)
        ldap_module_mock.perform_module_operation()

        assert MockLdapApi.delete_ldap_failed_msg() in \
            ldap_module_mock.module.fail_json.call_args[1]['msg']

    def test_get_ldap_details_with_exception(self, ldap_module_mock):
        # Scenario 1: utils Exception 404
        ldap_name = 'ldap3'
        MockApiException.status = '404'
        self.get_ldap_args.update({
            'ldap_name': ldap_name,
        })
        ldap_module_mock.module.params = self.get_ldap_args
        ldap_module_mock.auth_api_instance.get_providers_ldap_by_id = \
            MagicMock(side_effect=utils.ApiException)
        ob = ldap_module_mock.perform_module_operation()
        assert ob is None  # nothing to assert as it doesn't return anything

        # Scneario 2: utils Exception 500
        MockApiException.status = '500'
        ldap_module_mock.module.params = self.get_ldap_args
        ldap_module_mock.auth_api_instance.get_providers_ldap_by_id = \
            MagicMock(side_effect=utils.ApiException)
        ldap_module_mock.perform_module_operation()
        assert MockLdapApi.ldap_exception_msg() in \
            ldap_module_mock.module.fail_json.call_args[1]['msg']

        # Scneario 3: other Exception 500
        MockApiException.status = '500'
        ldap_module_mock.module.params = self.get_ldap_args
        ldap_module_mock.auth_api_instance.get_providers_ldap_by_id = \
            MagicMock(side_effect=Exception)
        ldap_module_mock.perform_module_operation()
        assert MockLdapApi.ldap_exception2_msg() in \
            ldap_module_mock.module.fail_json.call_args[1]['msg']

    def test_update_ldap_access_zone_info(self, ldap_module_mock):
        # Scenario 1: utils exception
        ldap_name = 'ldap3'
        self.get_ldap_args.update({
            'ldap_name': ldap_name,
        })
        ldap_module_mock.module.params = self.get_ldap_args
        ldap_module_mock.zones_api_instance.list_zones = \
            MagicMock(side_effect=utils.ApiException)
        ldap_module_mock.perform_module_operation()
        assert MockLdapApi.ldap_access_msg() in \
            ldap_module_mock.module.fail_json.call_args[1]['msg']

    def test_get_modified_ldap(self, ldap_module_mock):
        self.get_ldap_args.update({
            "ldap_name": "ldap1",
            'server_uri_state': 'absent-in-ldap'
        })
        ldap_module_mock.module.params = self.get_ldap_args
        ldap_module_mock.perform_module_operation()
        assert (
            ldap_module_mock.module.exit_json.call_args[1]['ldap_provider_details'])
        assert ldap_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_main(self, ldap_module_mock):
        ldap_name = "ldap1"
        self.get_ldap_args.update({
            "ldap_name": ldap_name,
            'server_uri_state': 'absent-in-ldap'
        })
        ldap_module_mock.get_ldap_parameters = MagicMock(
            return_value=MockLdapApi.LDAP)
        main()
        ldap_module_mock.get_ldap_details(ldap_name)
