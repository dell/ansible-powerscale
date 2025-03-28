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
        self.set_module_params(self.synciq_certificate_args, {'certificate_id': 'ywqeqwe76898y98wqwe'})
        powerscale_module_mock.get_certificate = MagicMock(return_value=MockSyncIQCertificateApi.GET_SYNCIQ_CERTIFICATE_RESPONSE)
        SyncIQCertificateHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.get_certificate.assert_called()

    def test_get_certificate_id(self, powerscale_module_mock):
        self.set_module_params(self.synciq_certificate_args, {'certificate_id': 'ywqeqwe76898y98wqwe'})
        certs = MagicMock()
        certs.to_dict.return_value = MockSyncIQCertificateApi.GET_SYNCIQ_CERTIFICATE_RESPONSE
        powerscale_module_mock.synciq_api.list_certificates_peer.return_value = certs
        SyncIQCertificateHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.synciq_api.list_certificates_peer.assert_called()

    def test_get_certificate_id_with_name(self, powerscale_module_mock):
        self.set_module_params(self.synciq_certificate_args, {'alias_name': 'Sample'})
        certs = MagicMock()
        certs.to_dict.return_value = MockSyncIQCertificateApi.GET_SYNCIQ_CERTIFICATE_RESPONSE
        powerscale_module_mock.synciq_api.list_certificates_peer.return_value = certs
        SyncIQCertificateHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.synciq_api.list_certificates_peer.assert_called()

    def test_get_certificate_id_exception(self, powerscale_module_mock):
        self.set_module_params(self.synciq_certificate_args, {'certificate_id': 'ywqeqwe76898y98wqwe'})
        powerscale_module_mock.synciq_api.list_certificates_peer = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSyncIQCertificateApi.get_synciq_certificate_exception_response('get_certificate_exception'),
            SyncIQCertificateHandler)

    def test_get_certificate_exception(self, powerscale_module_mock):
        self.set_module_params(self.synciq_certificate_args, {'certificate_id': 'ywqeqwe76898y98wqwe'})
        powerscale_module_mock.get_certificate_id = MagicMock(return_value="ywqeqwe76898y98wqwe")
        powerscale_module_mock.synciq_api.get_certificates_peer_by_id = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSyncIQCertificateApi.get_synciq_certificate_exception_response('get_details_exception'),
            SyncIQCertificateHandler)

    def test_import_certificate(self, powerscale_module_mock):
        self.set_module_params(self.synciq_certificate_args, {})
        powerscale_module_mock.get_cert_details = MagicMock(return_value=("", None))
        powerscale_module_mock.synciq_api.create_certificates_peer_item.to_dict = MagicMock(return_value=MockSyncIQCertificateApi.CREATE_CERTIFICATE_ID)
        powerscale_module_mock.get_certificate = MagicMock(return_value=MockSyncIQCertificateApi.GET_SYNCIQ_CERTIFICATE_RESPONSE)
        SyncIQCertificateHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.synciq_api.create_certificates_peer_item.assert_called()

    def test_import_certificate_exception(self, powerscale_module_mock):
        self.set_module_params(self.synciq_certificate_args, {"description": None})
        powerscale_module_mock.get_cert_details = MagicMock(return_value=("", None))
        powerscale_module_mock.synciq_api.create_certificates_peer_item = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSyncIQCertificateApi.get_synciq_certificate_exception_response('import_exception'),
            SyncIQCertificateHandler)

    def test_import_certificate_missing_field_exception(self, powerscale_module_mock):
        self.set_module_params(self.synciq_certificate_args, {"certificate_file": None})
        powerscale_module_mock.get_cert_details = MagicMock(return_value=("", None))
        self.capture_fail_json_call(
            MockSyncIQCertificateApi.get_synciq_certificate_exception_response('import_missing_exception'),
            SyncIQCertificateHandler)

    def test_import_certificate_format_error(self, powerscale_module_mock):
        self.set_module_params(self.synciq_certificate_args, {"certificate_file": "/ifs/server.pem"})
        self.capture_fail_json_call(MockSyncIQCertificateApi.import_certificate_format_error_msg(),
                                    SyncIQCertificateHandler)

    def test_import_name_error(self, powerscale_module_mock):
        self.set_module_params(self.synciq_certificate_args,
                               {"alias_name": "Test 1 2 3"})
        powerscale_module_mock.synciq_api.create_certificates_peer_item = MagicMock()
        self.capture_fail_json_call(MockSyncIQCertificateApi.alias_name_error_msg("alias_name"),
                                    SyncIQCertificateHandler)

    def test_import_new_alias_name_error(self, powerscale_module_mock):
        self.set_module_params(self.synciq_certificate_args,
                               {'new_alias_name': 'new name 3 4 5 6 @'})
        powerscale_module_mock.synciq_api.create_certificates_peer_item = MagicMock()
        self.capture_fail_json_call(MockSyncIQCertificateApi.alias_name_error_msg("new_alias_name"),
                                    SyncIQCertificateHandler)

    def test_description_error(self, powerscale_module_mock):
        self.set_module_params(self.synciq_certificate_args,
                               {"description": 'From python From python From python From python From python From python'
                                               'From python From python From python From python From python From python From python From python'})
        powerscale_module_mock.synciq_api.create_certificates_peer_item = MagicMock()
        self.capture_fail_json_call(MockSyncIQCertificateApi.description_error_msg(), SyncIQCertificateHandler)

    def test_delete_certificate(self, powerscale_module_mock):
        self.set_module_params(self.synciq_certificate_args,
                               {"state": "absent"})
        powerscale_module_mock.get_certificate = MagicMock(return_value=MockSyncIQCertificateApi.GET_SYNCIQ_CERTIFICATE_RESPONSE)
        powerscale_module_mock.get_certificate_id = MagicMock(return_value="ywqeqwe76898y98wqwe")
        powerscale_module_mock.synciq_api.delete_certificates_peer_by_id = MagicMock()
        SyncIQCertificateHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        powerscale_module_mock.synciq_api.delete_certificates_peer_by_id.assert_called()

    def test_delete_certificate_id_none(self, powerscale_module_mock):
        self.set_module_params(self.synciq_certificate_args,
                               {"state": "absent"})
        powerscale_module_mock.get_certificate_id = MagicMock(return_value=None)
        powerscale_module_mock.synciq_api.delete_certificates_peer_by_id = MagicMock()
        SyncIQCertificateHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is False

    def test_delete_certificate_exception(self, powerscale_module_mock):
        self.set_module_params(self.synciq_certificate_args,
                               {"state": "absent"})
        powerscale_module_mock.get_certificate = MagicMock(return_value=MockSyncIQCertificateApi.GET_SYNCIQ_CERTIFICATE_RESPONSE)
        powerscale_module_mock.get_certificate_id = MagicMock(return_value="ywqeqwe76898y98wqwe")
        powerscale_module_mock.synciq_api.delete_certificates_peer_by_id = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSyncIQCertificateApi.get_synciq_certificate_exception_response('delete_exception'),
            SyncIQCertificateHandler)

    def test_modify_certificate(self, powerscale_module_mock):
        self.set_module_params(self.synciq_certificate_args,
                               {'new_alias_name': 'new_name',
                                'description': 'new_description',
                                'state': 'present'})
        powerscale_module_mock.synciq_api.get_certificates_peer_by_id = MagicMock()
        powerscale_module_mock.get_certificates = MagicMock(return_value=MockSyncIQCertificateApi.GET_SYNCIQ_CERTIFICATE_RESPONSE)
        powerscale_module_mock.get_certificate_id = MagicMock(return_value="ywqeqwe76898y98wqwe")
        powerscale_module_mock.synciq_api.update_certificates_peer_by_id = MagicMock()
        SyncIQCertificateHandler().handle(powerscale_module_mock, powerscale_module_mock.module.params)
        assert powerscale_module_mock.module.exit_json.call_args[1]['changed'] is True

    def test_modify_certificate_exception(self, powerscale_module_mock):
        self.set_module_params(self.synciq_certificate_args,
                               {'new_alias_name': 'new_name',
                                'description': 'new_description'})
        powerscale_module_mock.get_certificates = MagicMock(return_value=MockSyncIQCertificateApi.GET_SYNCIQ_CERTIFICATE_RESPONSE)
        powerscale_module_mock.get_certificate_id = MagicMock(return_value="ywqeqwe76898y98wqwe")
        powerscale_module_mock.synciq_api.update_certificates_peer_by_id = MagicMock(side_effect=MockApiException)
        self.capture_fail_json_call(
            MockSyncIQCertificateApi.get_synciq_certificate_exception_response('update_exception'),
            SyncIQCertificateHandler)
