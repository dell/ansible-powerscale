# Copyright: (c) 2024, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for Event Alert Suppression module on PowerScale"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock \
    import utils

from ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression \
    import AnsibleModule, EventAlertSuppression, EventAlertSuppressionHandler, main
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_event_alert_suppression_api \
    import MockEventAlertSuppressionApi
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_api_exception \
    import MockApiException
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base \
    import PowerScaleUnitBase


class TestEventAlertSuppression(PowerScaleUnitBase):
    suppression_args = MockEventAlertSuppressionApi.SUPPRESSION_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        """
        Returns an instance of the `EventAlertSuppression` class for testing
        purposes.

        :return: An instance of the `EventAlertSuppression` class.
        :rtype: `EventAlertSuppression`
        """
        return EventAlertSuppression

    @staticmethod
    def mock_suppress_response(powerscale_module_mock, *responses):
        """Mock the get_event_suppress_by_id SDK response"""
        api_responses = []
        for response in responses:
            api_response = MagicMock()
            api_response.to_dict.return_value = response
            api_responses.append(api_response)
        powerscale_module_mock.event_api.get_event_suppress_by_id = MagicMock(
            side_effect=api_responses)

    @staticmethod
    def mock_suppress_list_response(powerscale_module_mock, *responses):
        """Mock the get_event_suppress SDK response"""
        api_responses = []
        for response in responses:
            api_response = MagicMock()
            api_response.to_dict.return_value = response
            api_responses.append(api_response)
        powerscale_module_mock.event_api.get_event_suppress = MagicMock(
            side_effect=api_responses)

    def test_suppress_event(self, powerscale_module_mock):
        """Suppress an unsuppressed event - FR-1.1 / AC-001"""
        self.set_module_params(
            self.suppression_args,
            {"event_id": MockEventAlertSuppressionApi.EVENT_ID,
             "state": "suppressed"})
        self.mock_suppress_response(
            powerscale_module_mock,
            MockEventAlertSuppressionApi.UNSUPPRESSED_EVENT)
        EventAlertSuppressionHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)

        powerscale_module_mock.event_api.update_event_suppress_by_id.assert_called()
        assert powerscale_module_mock.result['changed'] is True
        assert powerscale_module_mock.result['event_alert_suppression_details'] == {
            "event_id": MockEventAlertSuppressionApi.EVENT_ID,
            "suppressed": True}
        # NFR-1: at most one read and one write per invocation
        assert powerscale_module_mock.event_api.get_event_suppress_by_id.call_count == 1

    def test_suppress_event_idempotent(self, powerscale_module_mock):
        """Suppress an already suppressed event - FR-1.1 / AC-004"""
        self.set_module_params(
            self.suppression_args,
            {"event_id": MockEventAlertSuppressionApi.EVENT_ID,
             "state": "suppressed"})
        self.mock_suppress_response(
            powerscale_module_mock,
            MockEventAlertSuppressionApi.SUPPRESSED_EVENT)
        EventAlertSuppressionHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)

        powerscale_module_mock.event_api.update_event_suppress_by_id.assert_not_called()
        assert powerscale_module_mock.result['changed'] is False
        assert powerscale_module_mock.result['event_alert_suppression_details'] == {
            "event_id": MockEventAlertSuppressionApi.EVENT_ID,
            "suppressed": True}
        assert "already suppressed" in powerscale_module_mock.result['msg']

    def test_unsuppress_event(self, powerscale_module_mock):
        """Un-suppress a suppressed event - FR-2.1 / AC-002"""
        self.set_module_params(
            self.suppression_args,
            {"event_id": MockEventAlertSuppressionApi.EVENT_ID,
             "state": "unsuppressed"})
        self.mock_suppress_response(
            powerscale_module_mock,
            MockEventAlertSuppressionApi.SUPPRESSED_EVENT)
        EventAlertSuppressionHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)

        powerscale_module_mock.event_api.update_event_suppress_by_id.assert_called()
        assert powerscale_module_mock.result['changed'] is True
        assert powerscale_module_mock.result['event_alert_suppression_details'] == {
            "event_id": MockEventAlertSuppressionApi.EVENT_ID,
            "suppressed": False}

    def test_unsuppress_event_idempotent(self, powerscale_module_mock):
        """Un-suppress an already unsuppressed event - FR-2.1 / AC-004"""
        self.set_module_params(
            self.suppression_args,
            {"event_id": MockEventAlertSuppressionApi.EVENT_ID,
             "state": "unsuppressed"})
        self.mock_suppress_response(
            powerscale_module_mock,
            MockEventAlertSuppressionApi.UNSUPPRESSED_EVENT)
        EventAlertSuppressionHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)

        powerscale_module_mock.event_api.update_event_suppress_by_id.assert_not_called()
        assert powerscale_module_mock.result['changed'] is False
        assert "already un-suppressed" in powerscale_module_mock.result['msg']

    def test_suppress_event_exception(self, powerscale_module_mock):
        """Suppress fails when the update API errors - NFR-2"""
        self.set_module_params(
            self.suppression_args,
            {"event_id": MockEventAlertSuppressionApi.EVENT_ID,
             "state": "suppressed"})
        self.mock_suppress_response(
            powerscale_module_mock,
            MockEventAlertSuppressionApi.UNSUPPRESSED_EVENT)
        powerscale_module_mock.event_api.update_event_suppress_by_id = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockEventAlertSuppressionApi.get_event_alert_suppression_exception(
                'set_suppress_state'),
            EventAlertSuppressionHandler)

    def test_suppress_invalid_event_id_exception(self, powerscale_module_mock):
        """Suppress an invalid event ID - FR-1.2 / AC-005"""
        self.set_module_params(
            self.suppression_args,
            {"event_id": MockEventAlertSuppressionApi.INVALID_EVENT_ID,
             "state": "suppressed"})
        powerscale_module_mock.event_api.get_event_suppress_by_id = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockEventAlertSuppressionApi.get_event_alert_suppression_exception(
                'get_invalid_suppress_state'),
            EventAlertSuppressionHandler)
        powerscale_module_mock.event_api.update_event_suppress_by_id.assert_not_called()

    def test_check_mode_suppress_event(self, powerscale_module_mock):
        """Check mode preview for suppress - FR-4.1 / AC-006"""
        self.set_module_params(
            self.suppression_args,
            {"event_id": MockEventAlertSuppressionApi.EVENT_ID,
             "state": "suppressed"})
        powerscale_module_mock.module.check_mode = True
        self.mock_suppress_response(
            powerscale_module_mock,
            MockEventAlertSuppressionApi.UNSUPPRESSED_EVENT)
        EventAlertSuppressionHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)

        powerscale_module_mock.event_api.get_event_suppress_by_id.assert_called()
        powerscale_module_mock.event_api.update_event_suppress_by_id.assert_not_called()
        assert powerscale_module_mock.result['changed'] is True
        assert powerscale_module_mock.result['event_alert_suppression_details'] == {
            "event_id": MockEventAlertSuppressionApi.EVENT_ID,
            "suppressed": False,
            "would_change_to": True}

    def test_check_mode_unsuppress_event(self, powerscale_module_mock):
        """Check mode preview for un-suppress - FR-4.1 / AC-006"""
        self.set_module_params(
            self.suppression_args,
            {"event_id": MockEventAlertSuppressionApi.EVENT_ID,
             "state": "unsuppressed"})
        powerscale_module_mock.module.check_mode = True
        self.mock_suppress_response(
            powerscale_module_mock,
            MockEventAlertSuppressionApi.SUPPRESSED_EVENT)
        EventAlertSuppressionHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)

        powerscale_module_mock.event_api.update_event_suppress_by_id.assert_not_called()
        assert powerscale_module_mock.result['changed'] is True
        assert powerscale_module_mock.result['event_alert_suppression_details'] == {
            "event_id": MockEventAlertSuppressionApi.EVENT_ID,
            "suppressed": True,
            "would_change_to": False}

    def test_check_mode_idempotent_suppress(self, powerscale_module_mock):
        """Check mode reports no change when already suppressed - FR-4.1"""
        self.set_module_params(
            self.suppression_args,
            {"event_id": MockEventAlertSuppressionApi.EVENT_ID,
             "state": "suppressed"})
        powerscale_module_mock.module.check_mode = True
        self.mock_suppress_response(
            powerscale_module_mock,
            MockEventAlertSuppressionApi.SUPPRESSED_EVENT)
        EventAlertSuppressionHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)

        powerscale_module_mock.event_api.update_event_suppress_by_id.assert_not_called()
        assert powerscale_module_mock.result['changed'] is False

    def test_diff_mode_suppress_event(self, powerscale_module_mock):
        """Diff output for suppress - FR-4.2 / AC-006"""
        self.set_module_params(
            self.suppression_args,
            {"event_id": MockEventAlertSuppressionApi.EVENT_ID,
             "state": "suppressed"})
        powerscale_module_mock.module._diff = True
        self.mock_suppress_response(
            powerscale_module_mock,
            MockEventAlertSuppressionApi.UNSUPPRESSED_EVENT)
        EventAlertSuppressionHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)

        assert powerscale_module_mock.result['diff'] == {
            "before": {"event_id": MockEventAlertSuppressionApi.EVENT_ID,
                       "suppressed": False},
            "after": {"event_id": MockEventAlertSuppressionApi.EVENT_ID,
                      "suppressed": True}}

    def test_diff_mode_unsuppress_event(self, powerscale_module_mock):
        """Diff output for un-suppress - FR-4.2 / AC-006"""
        self.set_module_params(
            self.suppression_args,
            {"event_id": MockEventAlertSuppressionApi.EVENT_ID,
             "state": "unsuppressed"})
        powerscale_module_mock.module._diff = True
        self.mock_suppress_response(
            powerscale_module_mock,
            MockEventAlertSuppressionApi.SUPPRESSED_EVENT)
        EventAlertSuppressionHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)

        assert powerscale_module_mock.result['diff'] == {
            "before": {"event_id": MockEventAlertSuppressionApi.EVENT_ID,
                       "suppressed": True},
            "after": {"event_id": MockEventAlertSuppressionApi.EVENT_ID,
                      "suppressed": False}}

    def test_diff_mode_idempotent_suppress(self, powerscale_module_mock):
        """No diff is reported when no change is required - FR-4.2"""
        self.set_module_params(
            self.suppression_args,
            {"event_id": MockEventAlertSuppressionApi.EVENT_ID,
             "state": "suppressed"})
        powerscale_module_mock.module._diff = True
        self.mock_suppress_response(
            powerscale_module_mock,
            MockEventAlertSuppressionApi.SUPPRESSED_EVENT)
        EventAlertSuppressionHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)

        assert powerscale_module_mock.result['diff'] == {}

    def test_query_all_suppressed_events(self, powerscale_module_mock):
        """Query all suppressed events - FR-3.1 / AC-003"""
        self.set_module_params(self.suppression_args, {"state": "get"})
        self.mock_suppress_list_response(
            powerscale_module_mock,
            MockEventAlertSuppressionApi.SUPPRESSED_EVENTS_LIST)
        EventAlertSuppressionHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)

        powerscale_module_mock.event_api.get_event_suppress.assert_called()
        assert powerscale_module_mock.result['changed'] is False
        assert powerscale_module_mock.result['event_alert_suppression_details'] == {
            "suppressions": [MockEventAlertSuppressionApi.SUPPRESSION_ENTRY],
            "total": 1}

    def test_query_all_suppressed_events_pagination(self, powerscale_module_mock):
        """Query all suppressed events across pages - FR-3.1 / NFR-1"""
        self.set_module_params(self.suppression_args, {"state": "get"})
        self.mock_suppress_list_response(
            powerscale_module_mock,
            MockEventAlertSuppressionApi.SUPPRESSED_EVENTS_LIST_PAGE_1,
            MockEventAlertSuppressionApi.SUPPRESSED_EVENTS_LIST_PAGE_2)
        EventAlertSuppressionHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)

        assert powerscale_module_mock.event_api.get_event_suppress.call_count == 2
        assert powerscale_module_mock.result['event_alert_suppression_details'] == {
            "suppressions": [MockEventAlertSuppressionApi.SUPPRESSION_ENTRY,
                             MockEventAlertSuppressionApi.SUPPRESSION_ENTRY_2],
            "total": 2}

    def test_query_all_suppressed_events_empty(self, powerscale_module_mock):
        """Query when no event is suppressed - FR-3.1"""
        self.set_module_params(self.suppression_args, {"state": "get"})
        self.mock_suppress_list_response(
            powerscale_module_mock,
            MockEventAlertSuppressionApi.EMPTY_SUPPRESSED_EVENTS)
        EventAlertSuppressionHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)

        assert powerscale_module_mock.result['event_alert_suppression_details'] == {
            "suppressions": [], "total": 0}

    def test_query_all_suppressed_events_exception(self, powerscale_module_mock):
        """Query all suppressed events fails with an API error - NFR-2"""
        self.set_module_params(self.suppression_args, {"state": "get"})
        powerscale_module_mock.event_api.get_event_suppress = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockEventAlertSuppressionApi.get_event_alert_suppression_exception(
                'query_all_suppressed'),
            EventAlertSuppressionHandler)

    def test_query_specific_event(self, powerscale_module_mock):
        """Query a specific suppressed event - FR-3.2 / AC-003"""
        self.set_module_params(
            self.suppression_args,
            {"event_id": MockEventAlertSuppressionApi.EVENT_ID,
             "state": "get"})
        self.mock_suppress_response(
            powerscale_module_mock,
            MockEventAlertSuppressionApi.SUPPRESSED_EVENT)
        EventAlertSuppressionHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)

        powerscale_module_mock.event_api.get_event_suppress_by_id.assert_called()
        powerscale_module_mock.event_api.get_event_suppress.assert_not_called()
        assert powerscale_module_mock.result['changed'] is False
        assert powerscale_module_mock.result['event_alert_suppression_details'] == {
            "event_id": MockEventAlertSuppressionApi.EVENT_ID,
            "suppressed": True}

    def test_query_specific_unsuppressed_event(self, powerscale_module_mock):
        """Query a specific unsuppressed event - FR-3.2"""
        self.set_module_params(
            self.suppression_args,
            {"event_id": MockEventAlertSuppressionApi.EVENT_ID,
             "state": "get"})
        self.mock_suppress_response(
            powerscale_module_mock,
            MockEventAlertSuppressionApi.UNSUPPRESSED_EVENT)
        EventAlertSuppressionHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params)

        assert powerscale_module_mock.result['event_alert_suppression_details'] == {
            "event_id": MockEventAlertSuppressionApi.EVENT_ID,
            "suppressed": False}

    def test_query_specific_event_exception(self, powerscale_module_mock):
        """Query an invalid event ID - FR-3.3 / AC-005"""
        self.set_module_params(
            self.suppression_args,
            {"event_id": MockEventAlertSuppressionApi.INVALID_EVENT_ID,
             "state": "get"})
        powerscale_module_mock.event_api.get_event_suppress_by_id = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockEventAlertSuppressionApi.get_event_alert_suppression_exception(
                'get_invalid_suppress_state'),
            EventAlertSuppressionHandler)

    def test_event_id_required_for_mutation(self, powerscale_module_mock):
        """event_id is mandatory for suppress and un-suppress - FR-5.1 / AC-005"""
        module_params = powerscale_module_mock.get_event_alert_suppression_parameters()
        assert module_params['event_id']['type'] == 'str'
        assert module_params['state']['required'] is True
        assert module_params['state']['choices'] == ['suppressed',
                                                     'unsuppressed', 'get']

        ansible_module_kwargs = AnsibleModule.call_args.kwargs
        assert ansible_module_kwargs['supports_check_mode'] is True
        assert ansible_module_kwargs['required_if'] == [
            ["state", "suppressed", ["event_id"]],
            ["state", "unsuppressed", ["event_id"]]]

    def test_main(self, powerscale_module_mock, mocker):
        self.set_module_params(
            self.suppression_args,
            {"event_id": MockEventAlertSuppressionApi.EVENT_ID,
             "state": "get"})
        self.mock_suppress_response(
            powerscale_module_mock,
            MockEventAlertSuppressionApi.SUPPRESSED_EVENT)
        mocker.patch(
            'ansible_collections.dellemc.powerscale.plugins.modules.event_alert_suppression.EventAlertSuppression',
            return_value=powerscale_module_mock)
        main()
        powerscale_module_mock.module.exit_json.assert_called()
