# Copyright: (c) 2025, Dell Technologies

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit Tests for IPMI module on PowerScale"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import copy
import pytest
from mock.mock import MagicMock

# pylint: disable=unused-import
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.initial_mock import (
    utils,
)
from ansible.module_utils import basic

from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.shared_library.powerscale_unit_base import (
    PowerScaleUnitBase,
)

basic.AnsibleModule = MagicMock()

from ansible_collections.dellemc.powerscale.plugins.modules.ipmi import (
    Ipmi,
    IpmiHandler,
)
from ansible_collections.dellemc.powerscale.tests.unit.plugins.module_utils.mock_ipmi_api import (
    MockIpmiApi,
)


class TestIpmi(PowerScaleUnitBase):
    """IPMI module tests"""

    ipmi_args = MockIpmiApi.IPMI_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return Ipmi

    def _get_args(self, overrides=None):
        """Return a fresh copy of args with optional overrides."""
        args = copy.deepcopy(MockIpmiApi.IPMI_COMMON_ARGS)
        if overrides:
            args.update(overrides)
        return args

    def test_get_ipmi_config_no_changes(self, powerscale_module_mock):
        """Test retrieving IPMI config without requesting changes."""
        powerscale_module_mock.module.params = self._get_args()
        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            return_value=copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)
        )

        IpmiHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is False
        assert (
            powerscale_module_mock.module.exit_json.call_args[1]["ipmi_details"]
            == MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE
        )

    def test_update_settings_changed(self, powerscale_module_mock):
        """Test updating IPMI settings when values differ."""
        powerscale_module_mock.module.params = self._get_args({
            "settings": {"enabled": True, "allocation_type": "dhcp"},
        })
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            return_value=current_config
        )

        IpmiHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        powerscale_module_mock.ipmi_api.update_ipmi_settings.assert_called_once()
        call_args = powerscale_module_mock.ipmi_api.update_ipmi_settings.call_args[0][0]
        assert call_args["allocation_type"] == "dhcp"

    def test_update_settings_idempotent(self, powerscale_module_mock):
        """Test that no update occurs when settings already match."""
        powerscale_module_mock.module.params = self._get_args({
            "settings": {"enabled": True, "allocation_type": "static"},
        })
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            return_value=current_config
        )

        IpmiHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is False
        powerscale_module_mock.ipmi_api.update_ipmi_settings.assert_not_called()

    def test_update_network_changed(self, powerscale_module_mock):
        """Test updating IPMI network when gateway differs."""
        powerscale_module_mock.module.params = self._get_args({
            "network": {"gateway": "10.0.0.2", "prefixlen": 24},
        })
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            return_value=current_config
        )

        IpmiHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        powerscale_module_mock.ipmi_api.update_ipmi_network.assert_called_once()
        call_args = powerscale_module_mock.ipmi_api.update_ipmi_network.call_args[0][0]
        assert call_args["gateway"] == "10.0.0.2"

    def test_update_network_idempotent(self, powerscale_module_mock):
        """Test no network update when values match."""
        powerscale_module_mock.module.params = self._get_args({
            "network": {
                "gateway": "10.0.0.1",
                "prefixlen": 24,
                "ip_ranges": [{"low": "10.0.0.100", "high": "10.0.0.200"}],
            },
        })
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            return_value=current_config
        )

        IpmiHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is False
        powerscale_module_mock.ipmi_api.update_ipmi_network.assert_not_called()

    def test_update_user_password_always_changed(self, powerscale_module_mock):
        """Test that user password update always marks changed."""
        powerscale_module_mock.module.params = self._get_args({
            "user": {"username": "admin", "password": "NewP@ss123"},
        })
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            return_value=current_config
        )

        IpmiHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        powerscale_module_mock.ipmi_api.update_ipmi_user.assert_called_once()

    def test_update_user_username_only_idempotent(self, powerscale_module_mock):
        """Test no user update when only username provided and matches."""
        powerscale_module_mock.module.params = self._get_args({
            "user": {"username": "admin", "password": None},
        })
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            return_value=current_config
        )

        IpmiHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is False
        powerscale_module_mock.ipmi_api.update_ipmi_user.assert_not_called()

    def test_update_features_changed(self, powerscale_module_mock):
        """Test updating a feature that differs from current."""
        powerscale_module_mock.module.params = self._get_args({
            "features": [{"id": "sol", "enabled": True}],
        })
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            return_value=current_config
        )

        IpmiHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        powerscale_module_mock.ipmi_api.update_ipmi_feature.assert_called_once_with(
            "sol", {"enabled": True}
        )

    def test_update_features_idempotent(self, powerscale_module_mock):
        """Test no feature update when already in desired state."""
        powerscale_module_mock.module.params = self._get_args({
            "features": [{"id": "power_control", "enabled": True}],
        })
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            return_value=current_config
        )

        IpmiHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is False
        powerscale_module_mock.ipmi_api.update_ipmi_feature.assert_not_called()

    def test_check_mode_no_api_calls(self, powerscale_module_mock):
        """Test that check mode does not make API update calls."""
        powerscale_module_mock.module.params = self._get_args({
            "settings": {"enabled": True, "allocation_type": "dhcp"},
        })
        powerscale_module_mock.module.check_mode = True
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            return_value=current_config
        )

        IpmiHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        powerscale_module_mock.ipmi_api.update_ipmi_settings.assert_not_called()

    def test_update_all_domains(self, powerscale_module_mock):
        """Test updating settings, network, user, and features at once."""
        powerscale_module_mock.module.params = self._get_args({
            "settings": {"enabled": False},
            "network": {"gateway": "10.0.0.2"},
            "user": {"username": "newadmin", "password": "Pass123"},
            "features": [{"id": "sol", "enabled": True}],
        })
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            return_value=current_config
        )

        IpmiHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        powerscale_module_mock.ipmi_api.update_ipmi_settings.assert_called_once()
        powerscale_module_mock.ipmi_api.update_ipmi_network.assert_called_once()
        powerscale_module_mock.ipmi_api.update_ipmi_user.assert_called_once()
        powerscale_module_mock.ipmi_api.update_ipmi_feature.assert_called_once()

    def test_get_config_exception(self, powerscale_module_mock):
        """Test exception during config retrieval."""
        powerscale_module_mock.module.params = self._get_args()
        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            side_effect=Exception("Connection error")
        )
        with pytest.raises((SystemExit, Exception)):
            IpmiHandler().handle(
                powerscale_module_mock, powerscale_module_mock.module.params
            )

    def test_update_settings_exception(self, powerscale_module_mock):
        """Test exception during settings update."""
        powerscale_module_mock.module.params = self._get_args({
            "settings": {"enabled": False},
        })
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            return_value=current_config
        )
        powerscale_module_mock.ipmi_api.update_ipmi_settings = MagicMock(
            side_effect=Exception("API error")
        )
        with pytest.raises((SystemExit, Exception)):
            IpmiHandler().handle(
                powerscale_module_mock, powerscale_module_mock.module.params
            )

    def test_update_network_exception(self, powerscale_module_mock):
        """Test exception during network update."""
        powerscale_module_mock.module.params = self._get_args({
            "network": {"gateway": "10.0.0.2"},
        })
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            return_value=current_config
        )
        powerscale_module_mock.ipmi_api.update_ipmi_network = MagicMock(
            side_effect=Exception("API error")
        )
        with pytest.raises((SystemExit, Exception)):
            IpmiHandler().handle(
                powerscale_module_mock, powerscale_module_mock.module.params
            )

    def test_update_user_exception(self, powerscale_module_mock):
        """Test exception during user update."""
        powerscale_module_mock.module.params = self._get_args({
            "user": {"username": "admin", "password": "newpass"},
        })
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            return_value=current_config
        )
        powerscale_module_mock.ipmi_api.update_ipmi_user = MagicMock(
            side_effect=Exception("API error")
        )
        with pytest.raises((SystemExit, Exception)):
            IpmiHandler().handle(
                powerscale_module_mock, powerscale_module_mock.module.params
            )

    def test_update_feature_exception(self, powerscale_module_mock):
        """Test exception during feature update."""
        powerscale_module_mock.module.params = self._get_args({
            "features": [{"id": "sol", "enabled": True}],
        })
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            return_value=current_config
        )
        powerscale_module_mock.ipmi_api.update_ipmi_feature = MagicMock(
            side_effect=Exception("API error")
        )
        with pytest.raises((SystemExit, Exception)):
            IpmiHandler().handle(
                powerscale_module_mock, powerscale_module_mock.module.params
            )

    def test_empty_config_with_settings(self, powerscale_module_mock):
        """Test enabling IPMI when config is empty."""
        powerscale_module_mock.module.params = self._get_args({
            "settings": {"enabled": True, "allocation_type": "dhcp"},
        })
        current_config = copy.deepcopy(MockIpmiApi.IPMI_EMPTY_CONFIG_RESPONSE)

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            return_value=current_config
        )

        IpmiHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        powerscale_module_mock.ipmi_api.update_ipmi_settings.assert_called_once()

    def test_ip_ranges_change(self, powerscale_module_mock):
        """Test updating IP ranges."""
        powerscale_module_mock.module.params = self._get_args({
            "network": {
                "ip_ranges": [
                    {"low": "10.0.0.50", "high": "10.0.0.150"},
                    {"low": "10.0.0.200", "high": "10.0.0.250"},
                ],
            },
        })
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            return_value=current_config
        )

        IpmiHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        powerscale_module_mock.ipmi_api.update_ipmi_network.assert_called_once()
        call_args = powerscale_module_mock.ipmi_api.update_ipmi_network.call_args[0][0]
        assert len(call_args["ip_ranges"]) == 2

    def test_multiple_features_update(self, powerscale_module_mock):
        """Test updating multiple features at once."""
        powerscale_module_mock.module.params = self._get_args({
            "features": [
                {"id": "power_control", "enabled": False},
                {"id": "sol", "enabled": True},
            ],
        })
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            return_value=current_config
        )

        IpmiHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        assert powerscale_module_mock.ipmi_api.update_ipmi_feature.call_count == 2

    def test_check_mode_all_domains(self, powerscale_module_mock):
        """Test check mode with all domains having changes."""
        powerscale_module_mock.module.params = self._get_args({
            "settings": {"enabled": False},
            "network": {"gateway": "10.0.0.2"},
            "user": {"username": "newuser", "password": "pass"},
            "features": [{"id": "sol", "enabled": True}],
        })
        powerscale_module_mock.module.check_mode = True
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            return_value=current_config
        )

        IpmiHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        powerscale_module_mock.ipmi_api.update_ipmi_settings.assert_not_called()
        powerscale_module_mock.ipmi_api.update_ipmi_network.assert_not_called()
        powerscale_module_mock.ipmi_api.update_ipmi_user.assert_not_called()
        powerscale_module_mock.ipmi_api.update_ipmi_feature.assert_not_called()
