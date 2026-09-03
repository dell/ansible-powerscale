# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Event Alert Suppression module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock, patch
from ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression import main
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_event_alert_suppression_api import MockEventAlertSuppressionApi


class TestEventAlertSuppression:

    @pytest.fixture
    def module_args(self):
        """Returns common module arguments"""
        return {
            "onefs_host": "10.247.102.193",
            "port_no": "8080",
            "api_user": "root",
            "api_password": "Password123!",
            "verify_ssl": False
        }

    @patch('ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.utils.get_powerscale_connection')
    @patch('ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.EventApi')
    @patch('ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.AnsibleModule')
    def test_suppress_event(self, mock_ansible_module, mock_event_api, mock_get_connection, module_args):
        """Test suppressing an unsuppressed event"""
        # Setup module parameters
        module_args.update({
            "event_id": MockEventAlertSuppressionApi.EVENT_ID,
            "state": "suppressed"
        })
        
        mock_module_instance = MagicMock()
        mock_module_instance.params = module_args
        mock_module_instance.check_mode = False
        mock_ansible_module.return_value = mock_module_instance
        
        mock_api_client = MagicMock()
        mock_get_connection.return_value = mock_api_client
        mock_event_api_instance = MagicMock()
        mock_event_api.return_value = mock_event_api_instance
        
        # Mock API responses
        mock_event_api_instance.get_event_suppress_by_id.return_value.to_dict.return_value = MockEventAlertSuppressionApi.UNSUPPRESSED_EVENT
        mock_event_api_instance.update_event_suppress_by_id.return_value = None
        # Post-write verification
        mock_event_api_instance.get_event_suppress_by_id.return_value.to_dict.side_effect = [
            MockEventAlertSuppressionApi.UNSUPPRESSED_EVENT,
            MockEventAlertSuppressionApi.SUPPRESSED_EVENT
        ]
        
        with pytest.raises(SystemExit):
            main()
        
        mock_module_instance.exit_json.assert_called()
        call_args = mock_module_instance.exit_json.call_args.kwargs
        assert call_args['changed'] is True
        assert 'Successfully suppressed' in call_args['msg']

    @patch('ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.utils.get_powerscale_connection')
    @patch('ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.EventApi')
    @patch('ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.AnsibleModule')
    def test_idempotent_suppress(self, mock_ansible_module, mock_event_api, mock_get_connection, module_args):
        """Test idempotent suppress (already suppressed)"""
        module_args.update({
            "event_id": MockEventAlertSuppressionApi.EVENT_ID,
            "state": "suppressed"
        })
        
        mock_module_instance = MagicMock()
        mock_module_instance.params = module_args
        mock_module_instance.check_mode = False
        mock_ansible_module.return_value = mock_module_instance
        
        mock_api_client = MagicMock()
        mock_get_connection.return_value = mock_api_client
        mock_event_api_instance = MagicMock()
        mock_event_api.return_value = mock_event_api_instance
        
        # Mock API responses - event already suppressed
        mock_event_api_instance.get_event_suppress_by_id.return_value.to_dict.return_value = MockEventAlertSuppressionApi.SUPPRESSED_EVENT
        
        with pytest.raises(SystemExit):
            main()
        
        mock_module_instance.exit_json.assert_called()
        call_args = mock_module_instance.exit_json.call_args.kwargs
        assert call_args['changed'] is False
        assert 'already suppressed' in call_args['msg']

    @patch('ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.utils.get_powerscale_connection')
    @patch('ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.EventApi')
    @patch('ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.AnsibleModule')
    def test_unsuppress_event(self, mock_ansible_module, mock_event_api, mock_get_connection, module_args):
        """Test un-suppressing a suppressed event"""
        module_args.update({
            "event_id": MockEventAlertSuppressionApi.EVENT_ID,
            "state": "unsuppressed"
        })
        
        mock_module_instance = MagicMock()
        mock_module_instance.params = module_args
        mock_module_instance.check_mode = False
        mock_ansible_module.return_value = mock_module_instance
        
        mock_api_client = MagicMock()
        mock_get_connection.return_value = mock_api_client
        mock_event_api_instance = MagicMock()
        mock_event_api.return_value = mock_event_api_instance
        
        # Mock API responses
        mock_event_api_instance.get_event_suppress_by_id.return_value.to_dict.return_value = MockEventAlertSuppressionApi.SUPPRESSED_EVENT
        mock_event_api_instance.update_event_suppress_by_id.return_value = None
        # Post-write verification
        mock_event_api_instance.get_event_suppress_by_id.return_value.to_dict.side_effect = [
            MockEventAlertSuppressionApi.SUPPRESSED_EVENT,
            MockEventAlertSuppressionApi.UNSUPPRESSED_EVENT
        ]
        
        with pytest.raises(SystemExit):
            main()
        
        mock_module_instance.exit_json.assert_called()
        call_args = mock_module_instance.exit_json.call_args.kwargs
        assert call_args['changed'] is True
        assert 'Successfully un-suppressed' in call_args['msg']

    @patch('ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.utils.get_powerscale_connection')
    @patch('ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.EventApi')
    @patch('ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.AnsibleModule')
    def test_query_all_suppressed_events(self, mock_ansible_module, mock_event_api, mock_get_connection, module_args):
        """Test querying all suppressed events"""
        module_args.update({
            "state": "get"
        })
        
        mock_module_instance = MagicMock()
        mock_module_instance.params = module_args
        mock_module_instance.check_mode = False
        mock_ansible_module.return_value = mock_module_instance
        
        mock_api_client = MagicMock()
        mock_get_connection.return_value = mock_api_client
        mock_event_api_instance = MagicMock()
        mock_event_api.return_value = mock_event_api_instance
        
        # Mock API responses
        mock_event_api_instance.get_event_suppress.return_value.to_dict.return_value = MockEventAlertSuppressionApi.SUPPRESSED_EVENTS_LIST
        
        with pytest.raises(SystemExit):
            main()
        
        mock_module_instance.exit_json.assert_called()
        call_args = mock_module_instance.exit_json.call_args.kwargs
        assert call_args['changed'] is False
        assert 'suppressed events' in call_args['msg']

    @patch('ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.utils.get_powerscale_connection')
    @patch('ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.EventApi')
    @patch('ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.AnsibleModule')
    def test_query_specific_event(self, mock_ansible_module, mock_event_api, mock_get_connection, module_args):
        """Test querying a specific event"""
        module_args.update({
            "event_id": MockEventAlertSuppressionApi.EVENT_ID,
            "state": "get"
        })
        
        mock_module_instance = MagicMock()
        mock_module_instance.params = module_args
        mock_module_instance.check_mode = False
        mock_ansible_module.return_value = mock_module_instance
        
        mock_api_client = MagicMock()
        mock_get_connection.return_value = mock_api_client
        mock_event_api_instance = MagicMock()
        mock_event_api.return_value = mock_event_api_instance
        
        # Mock API responses
        mock_event_api_instance.get_event_suppress_by_id.return_value.to_dict.return_value = MockEventAlertSuppressionApi.SUPPRESSED_EVENT
        mock_event_api_instance.get_event_eventgroup_definitions.return_value.to_dict.return_value = MockEventAlertSuppressionApi.EVENTGROUP_DEFINITIONS
        
        with pytest.raises(SystemExit):
            main()
        
        mock_module_instance.exit_json.assert_called()
        call_args = mock_module_instance.exit_json.call_args.kwargs
        assert call_args['changed'] is False
        assert 'Successfully queried' in call_args['msg']

    @patch('ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.utils.get_powerscale_connection')
    @patch('ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.EventApi')
    @patch('ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.AnsibleModule')
    def test_invalid_event_id_error(self, mock_ansible_module, mock_event_api, mock_get_connection, module_args):
        """Test error handling for invalid event ID"""
        module_args.update({
            "event_id": "999999999",
            "state": "suppressed"
        })
        
        mock_module_instance = MagicMock()
        mock_module_instance.params = module_args
        mock_module_instance.check_mode = False
        mock_ansible_module.return_value = mock_module_instance
        
        mock_api_client = MagicMock()
        mock_get_connection.return_value = mock_api_client
        mock_event_api_instance = MagicMock()
        mock_event_api.return_value = mock_event_api_instance
        
        # Mock API to raise exception for invalid event ID
        mock_event_api_instance.get_event_suppress_by_id.side_effect = Exception("999999999 is not a valid event type ID")
        
        with pytest.raises(SystemExit):
            main()
        
        mock_module_instance.fail_json.assert_called()
        call_args = mock_module_instance.fail_json.call_args.kwargs
        assert 'failed with error' in call_args['msg']

    @patch('ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.utils.get_powerscale_connection')
    @patch('ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.EventApi')
    @patch('ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.AnsibleModule')
    def test_missing_event_id_error(self, mock_ansible_module, mock_event_api, mock_get_connection, module_args):
        """Test error handling for missing event_id"""
        module_args.update({
            "state": "suppressed"
        })
        
        mock_module_instance = MagicMock()
        mock_module_instance.params = module_args
        mock_module_instance.check_mode = False
        mock_ansible_module.return_value = mock_module_instance
        
        mock_api_client = MagicMock()
        mock_get_connection.return_value = mock_api_client
        mock_event_api_instance = MagicMock()
        mock_event_api.return_value = mock_event_api_instance
        
        # The module should fail due to required_if validation
        with pytest.raises(SystemExit):
            main()
        
        mock_module_instance.fail_json.assert_called()
