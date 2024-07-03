# Copyright: (c) 2023-2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for SyncIQ target cluster certificate module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.synciqcertificate import SyncIQCertificate
from ansible_collections.dellemc.powerscale.plugins.modules.synciqcertificate import SyncIQCertificateHandler
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_synciqcertificate_api \
    import MockSyncIQCertificateApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase


class TestSyncIQCertificate(PowerScaleUnitBase):
    synciq_certificate_args = MockSyncIQCertificateApi.SYNCIQ_CERTIFICATE_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return SyncIQCertificate

    def test_get_certificate_details_with_certificate_id(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.synciq_certificate_args, {'certificate_id': 'ywqeqwe76898y98wqwe'})
        powerscale_module_mock.get_certificate = MagicMock(return_value=MockSyncIQCertificateApi.GET_SYNCIQ_CERTIFICATE_RESPONSE)
        SyncIQCertificateHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.get_certificate.assert_called()

    def test_get_certificate_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock,
                               self.synciq_certificate_args, {})
        powerscale_module_mock.synciq_api.get_certificates_peer_by_id = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSyncIQCertificateApi.get_synciq_certificate_exception_response('get_details_exception'),
            powerscale_module_mock, SyncIQCertificateHandler)

    def test_import_certificate(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.synciq_certificate_args, {})
        powerscale_module_mock.synciq_api.create_certificates_peer_item.to_dict = MagicMock(return_value=MockSyncIQCertificateApi.CREATE_CERTIFICATE_ID)
        powerscale_module_mock.synciq_api.get_certificate = MagicMock(return_value=MockSyncIQCertificateApi.GET_SYNCIQ_CERTIFICATE_RESPONSE)
        SyncIQCertificateHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.synciq_api.create_certificates_peer_item.assert_called()

    def test_import_certificate_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.synciq_certificate_args, {})
        powerscale_module_mock.synciq_api.create_certificates_peer_item = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSyncIQCertificateApi.get_synciq_certificate_exception_response('import_exception'),
            powerscale_module_mock, SyncIQCertificateHandler)

    def test_import_certificate_format_error(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.synciq_certificate_args, {})
        powerscale_module_mock.synciq_api.create_certificates_peer_item = MagicMock()
        self.capture_fail_json_call(MockSyncIQCertificateApi.import_certificate_format_error_msg(), powerscale_module_mock, SyncIQCertificateHandler)

    def test_import_name_error(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.synciq_certificate_args,
                               {"alias_name": "Test 1 2 3"})
        powerscale_module_mock.synciq_api.create_certificates_peer_item = MagicMock()
        self.capture_fail_json_call(MockSyncIQCertificateApi.alias_name_error_msg("alias_name"), powerscale_module_mock, SyncIQCertificateHandler)

    def test_import_new_alias_name_error(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.synciq_certificate_args,
                               {'new_alias_name': 'new name 3 4 5 6 @'})
        powerscale_module_mock.synciq_api.create_certificates_peer_item = MagicMock()
        self.capture_fail_json_call(MockSyncIQCertificateApi.alias_name_error_msg("new_alias_name"), powerscale_module_mock, SyncIQCertificateHandler)

    def test_description_error(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.synciq_certificate_args,
                               {"description": 'From python From python From python From python From python From python'
                                               'From python From python From python From python From python From python From python From python'})
        powerscale_module_mock.synciq_api.create_certificates_peer_item = MagicMock()
        self.capture_fail_json_call(MockSyncIQCertificateApi.description_error_msg(), powerscale_module_mock, SyncIQCertificateHandler)

    def test_delete_certificate(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.synciq_certificate_args,
                               {"state": "absent"})
        powerscale_module_mock.synciq_api.get_certificate = MagicMock(return_value=MockSyncIQCertificateApi.GET_SYNCIQ_CERTIFICATE_RESPONSE)
        powerscale_module_mock.get_certificate_id = MagicMock(return_value="ywqeqwe76898y98wqwe")
        powerscale_module_mock.synciq_api.delete_certificates_peer_by_id = MagicMock()
        SyncIQCertificateHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.synciq_api.delete_certificates_peer_by_id.assert_called()

    def test_delete_certificate_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.synciq_certificate_args,
                               {"state": "absent"})
        powerscale_module_mock.synciq_api.get_certificate = MagicMock(return_value=MockSyncIQCertificateApi.GET_SYNCIQ_CERTIFICATE_RESPONSE)
        powerscale_module_mock.synciq_api.delete_certificates_peer_by_id = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSyncIQCertificateApi.get_synciq_certificate_exception_response('delete_exception'),
            powerscale_module_mock, SyncIQCertificateHandler)

    def test_modify_certificate(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.synciq_certificate_args,
                               {'new_alias_name': 'new_name',
                                'description': 'new_description'})
        SyncIQCertificateHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.synciq_api.get_certificates_peer_by_id = MagicMock(return_value=MockSyncIQCertificateApi.GET_SYNCIQ_CERTIFICATE_RESPONSE)
        powerscale_module_mock.synciq_api.update_certificates_peer_by_id = MagicMock(return_value=MockSyncIQCertificateApi.MODIFY_CERTIFICATE_DETAILS)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_certificate_exception(self, powerscale_module_mock):
        self.set_module_params(powerscale_module_mock, self.synciq_certificate_args,
                               {'new_alias_name': 'new_name',
                                'description': 'new_description'})
        powerscale_module_mock.synciq_api.get_certificate = MagicMock(return_value=MockSyncIQCertificateApi.GET_SYNCIQ_CERTIFICATE_RESPONSE)
        powerscale_module_mock.synciq_api.update_certificates_peer_by_id = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSyncIQCertificateApi.get_synciq_certificate_exception_response('update_exception'),
            powerscale_module_mock, SyncIQCertificateHandler)
