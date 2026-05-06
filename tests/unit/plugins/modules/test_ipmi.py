# Copyright: (c) 2026, Dell Technologies

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
            "user": {"username": "admin", "password": "test_password_placeholder"},
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
            "user": {"username": "newadmin", "password": "test_password_placeholder"},
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
            "user": {"username": "admin", "password": "test_password_placeholder"},
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
            "user": {"username": "newuser", "password": "test_password_placeholder"},
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

    def test_diff_mode_settings_change(self, powerscale_module_mock):
        """Test diff mode output when settings change."""
        powerscale_module_mock.module.params = self._get_args({
            "settings": {"enabled": True, "allocation_type": "dhcp"},
        })
        powerscale_module_mock.module._diff = True
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)
        updated_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)
        updated_config["settings"]["allocation_type"] = "dhcp"

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            side_effect=[current_config, updated_config]
        )

        IpmiHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result["changed"] is True
        assert "diff" in result
        assert "before" in result["diff"]
        assert "after" in result["diff"]
        assert result["diff"]["before"]["settings"]["allocation_type"] == "static"
        assert result["diff"]["after"]["settings"]["allocation_type"] == "dhcp"

    def test_diff_mode_user_password_excluded(self, powerscale_module_mock):
        """Test that diff mode excludes password from user state."""
        powerscale_module_mock.module.params = self._get_args({
            "user": {"username": "newadmin", "password": "test_password_placeholder"},
        })
        powerscale_module_mock.module._diff = True
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)
        updated_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)
        updated_config["user"]["username"] = "newadmin"

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            side_effect=[current_config, updated_config]
        )

        IpmiHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert "diff" in result
        assert "password" not in result["diff"]["before"].get("user", {})
        assert "password" not in result["diff"]["after"].get("user", {})

    def test_diff_mode_no_change_no_diff(self, powerscale_module_mock):
        """Test that diff output is absent when no changes are made."""
        powerscale_module_mock.module.params = self._get_args()
        powerscale_module_mock.module._diff = True
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            return_value=current_config
        )

        IpmiHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result["changed"] is False
        assert "diff" not in result

    def test_diff_mode_all_domains(self, powerscale_module_mock):
        """Test diff mode with changes across all domains."""
        powerscale_module_mock.module.params = self._get_args({
            "settings": {"enabled": False},
            "network": {"gateway": "10.0.0.2"},
            "user": {"username": "newadmin", "password": "test_password_placeholder"},
            "features": [{"id": "sol", "enabled": True}],
        })
        powerscale_module_mock.module._diff = True
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)
        updated_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)
        updated_config["settings"]["enabled"] = False
        updated_config["network"]["gateway"] = "10.0.0.2"
        updated_config["user"]["username"] = "newadmin"
        updated_config["features"][1]["enabled"] = True

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            side_effect=[current_config, updated_config]
        )

        IpmiHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        result = powerscale_module_mock.module.exit_json.call_args[1]
        assert result["changed"] is True
        assert "diff" in result
        assert result["diff"]["before"]["settings"]["enabled"] is True
        assert result["diff"]["after"]["settings"]["enabled"] is False
        assert result["diff"]["before"]["network"]["gateway"] == "10.0.0.1"
        assert result["diff"]["after"]["network"]["gateway"] == "10.0.0.2"
        assert "features" in result["diff"]["after"]

    def test_feature_name_fallback(self, powerscale_module_mock):
        """Test feature comparison when current features use 'name' instead of 'id'."""
        powerscale_module_mock.module.params = self._get_args({
            "features": [{"id": "power_control", "enabled": False}],
        })
        current_config = copy.deepcopy(MockIpmiApi.IPMI_FULL_CONFIG_RESPONSE)
        current_config["features"] = [
            {"name": "power_control", "enabled": True},
            {"name": "sol", "enabled": False},
        ]

        powerscale_module_mock.ipmi_api = MagicMock()
        powerscale_module_mock.ipmi_api.get_all_ipmi_config = MagicMock(
            return_value=current_config
        )

        IpmiHandler().handle(
            powerscale_module_mock, powerscale_module_mock.module.params
        )
        assert powerscale_module_mock.module.exit_json.call_args[1]["changed"] is True
        powerscale_module_mock.ipmi_api.update_ipmi_feature.assert_called_once_with(
            "power_control", {"enabled": False}
        )

    def test_feature_not_in_current(self, powerscale_module_mock):
        """Test feature update when desired feature is not in current config."""
        powerscale_module_mock.module.params = self._get_args({
            "features": [{"id": "new_feature", "enabled": True}],
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
            "new_feature", {"enabled": True}
        )

    def test_settings_partial_none_values(self, powerscale_module_mock):
        """Test settings comparison when some desired values are None."""
        powerscale_module_mock.module.params = self._get_args({
            "settings": {"enabled": None, "allocation_type": "dhcp"},
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
        call_args = powerscale_module_mock.ipmi_api.update_ipmi_settings.call_args[0][0]
        assert "enabled" not in call_args
        assert call_args["allocation_type"] == "dhcp"

    def test_network_matching_ip_ranges_idempotent(self, powerscale_module_mock):
        """Test no network update when ip_ranges match current."""
        powerscale_module_mock.module.params = self._get_args({
            "network": {
                "gateway": None,
                "prefixlen": None,
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

    def test_user_password_only_update(self, powerscale_module_mock):
        """Test user update with only password (no username)."""
        powerscale_module_mock.module.params = self._get_args({
            "user": {"username": None, "password": "test_password_placeholder"},
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
        call_args = powerscale_module_mock.ipmi_api.update_ipmi_user.call_args[0][0]
        assert "username" not in call_args
        assert call_args["password"] == "newpass"


class TestIpmiApi:
    """Unit tests for IpmiApi helper class."""

    def _make_module_mock(self):
        """Create a mock module with standard params."""
        module = MagicMock()
        module.params = {
            'onefs_host': '10.0.0.1',
            'port_no': '8080',
            'api_user': 'admin',
            'api_password': 'test_api_password_placeholder',
            'verify_ssl': False,
        }
        return module

    def _make_api(self, module=None):
        """Create an IpmiApi instance with mocked module."""
        from ansible_collections.dellemc.powerscale.plugins.module_utils.storage.dell.shared_library.ipmi import (
            IpmiApi,
        )
        if module is None:
            module = self._make_module_mock()
        return IpmiApi(module)

    def test_init(self):
        """Test IpmiApi initialisation."""
        api = self._make_api()
        assert api.host == '10.0.0.1'
        assert api.port == '8080'
        assert api.base_url == 'https://10.0.0.1:8080'
        assert api._session_id is None
        assert api._csrf_token is None

    def test_get_url(self):
        """Test URL construction."""
        api = self._make_api()
        assert api._get_url('/foo') == 'https://10.0.0.1:8080/foo'

    @pytest.fixture
    def mock_open_url(self, monkeypatch):
        """Patch open_url in the ipmi module_utils."""
        mock = MagicMock()
        monkeypatch.setattr(
            'ansible_collections.dellemc.powerscale.plugins.module_utils'
            '.storage.dell.shared_library.ipmi.open_url',
            mock,
        )
        return mock

    def _setup_session_response(self, mock_open_url):
        """Configure mock_open_url to return valid session response."""
        session_resp = MagicMock()
        session_resp.read.return_value = b'{"services": ["platform"]}'
        session_resp.headers = {
            'Set-Cookie': 'isisessid=abc123; path=/',
            'X-CSRF-Token': 'csrf-token-value',
        }
        mock_open_url.return_value = session_resp
        return session_resp

    def test_create_session(self, mock_open_url):
        """Test session creation extracts cookie and CSRF token."""
        self._setup_session_response(mock_open_url)
        api = self._make_api()
        api._create_session()
        assert api._session_id == 'isisessid=abc123'
        assert api._csrf_token == 'csrf-token-value'
        mock_open_url.assert_called_once()
        call_kwargs = mock_open_url.call_args
        assert 'POST' in str(call_kwargs)

    def test_create_session_no_csrf(self, mock_open_url):
        """Test session creation when CSRF token is missing."""
        resp = MagicMock()
        resp.read.return_value = b'{}'
        resp.headers = {'Set-Cookie': 'isisessid=abc123; path=/'}
        mock_open_url.return_value = resp
        api = self._make_api()
        api._create_session()
        assert api._session_id == 'isisessid=abc123'
        assert api._csrf_token is None

    def test_delete_session(self, mock_open_url):
        """Test session deletion."""
        api = self._make_api()
        api._session_id = 'isisessid=abc123'
        api._csrf_token = 'csrf-token'
        api._delete_session()
        assert api._session_id is None
        assert api._csrf_token is None
        mock_open_url.assert_called_once()

    def test_delete_session_no_session(self, mock_open_url):
        """Test session deletion when no session exists."""
        api = self._make_api()
        api._session_id = None
        api._delete_session()
        mock_open_url.assert_not_called()

    def test_delete_session_exception_suppressed(self, mock_open_url):
        """Test session deletion suppresses exceptions."""
        mock_open_url.side_effect = Exception("connection lost")
        api = self._make_api()
        api._session_id = 'isisessid=abc123'
        api._delete_session()
        assert api._session_id is None
        assert api._csrf_token is None

    def test_request_get_with_data(self, mock_open_url):
        """Test _request GET returns parsed JSON."""
        session_resp = MagicMock()
        session_resp.read.return_value = b'{}'
        session_resp.headers = {
            'Set-Cookie': 'isisessid=abc; path=/',
            'X-CSRF-Token': 'csrf',
        }
        data_resp = MagicMock()
        data_resp.read.return_value = b'{"settings": {"enabled": true}}'
        mock_open_url.side_effect = [session_resp, data_resp, MagicMock()]
        api = self._make_api()
        result = api._request('/platform/10/ipmi/config/settings')
        assert result == {"settings": {"enabled": True}}

    def test_request_empty_response(self, mock_open_url):
        """Test _request returns empty dict for empty response."""
        session_resp = MagicMock()
        session_resp.read.return_value = b'{}'
        session_resp.headers = {
            'Set-Cookie': 'isisessid=abc; path=/',
            'X-CSRF-Token': 'csrf',
        }
        data_resp = MagicMock()
        data_resp.read.return_value = b''
        mock_open_url.side_effect = [session_resp, data_resp, MagicMock()]
        api = self._make_api()
        result = api._request('/platform/10/ipmi/config/settings', method='PUT', data={'enabled': True})
        assert result == {}

    def test_request_http_error_with_body(self, mock_open_url):
        """Test _request raises on HTTPError with response body."""
        from ansible.module_utils.six.moves.urllib.error import HTTPError
        import io
        session_resp = MagicMock()
        session_resp.read.return_value = b'{}'
        session_resp.headers = {
            'Set-Cookie': 'isisessid=abc; path=/',
            'X-CSRF-Token': 'csrf',
        }
        http_err = HTTPError(
            'https://host/api', 403, 'Forbidden', {},
            io.BytesIO(b'{"message": "access denied"}')
        )
        mock_open_url.side_effect = [session_resp, http_err, MagicMock()]
        api = self._make_api()
        with pytest.raises(Exception, match="failed with HTTP 403"):
            api._request('/platform/10/ipmi/config/settings')

    def test_request_http_error_empty_body(self, mock_open_url):
        """Test _request raises on HTTPError with empty body."""
        from ansible.module_utils.six.moves.urllib.error import HTTPError
        import io
        session_resp = MagicMock()
        session_resp.read.return_value = b'{}'
        session_resp.headers = {
            'Set-Cookie': 'isisessid=abc; path=/',
            'X-CSRF-Token': 'csrf',
        }
        http_err = HTTPError(
            'https://host/api', 500, 'Server Error', {},
            io.BytesIO(b'')
        )
        mock_open_url.side_effect = [session_resp, http_err, MagicMock()]
        api = self._make_api()
        with pytest.raises(Exception, match="failed with HTTP 500"):
            api._request('/platform/10/ipmi/config/settings')

    def test_request_url_error(self, mock_open_url):
        """Test _request raises on URLError."""
        from ansible.module_utils.six.moves.urllib.error import URLError
        session_resp = MagicMock()
        session_resp.read.return_value = b'{}'
        session_resp.headers = {
            'Set-Cookie': 'isisessid=abc; path=/',
            'X-CSRF-Token': 'csrf',
        }
        mock_open_url.side_effect = [session_resp, URLError("timed out"), MagicMock()]
        api = self._make_api()
        with pytest.raises(Exception, match="connection error"):
            api._request('/platform/10/ipmi/config/settings')

    def _setup_request_mock(self, mock_open_url, return_data):
        """Setup mock for a full request cycle (session + data + delete)."""
        session_resp = MagicMock()
        session_resp.read.return_value = b'{}'
        session_resp.headers = {
            'Set-Cookie': 'isisessid=abc; path=/',
            'X-CSRF-Token': 'csrf',
        }
        import json as json_mod
        data_resp = MagicMock()
        data_resp.read.return_value = json_mod.dumps(return_data).encode()
        mock_open_url.side_effect = [session_resp, data_resp, MagicMock()]

    def test_get_ipmi_settings(self, mock_open_url):
        """Test get_ipmi_settings returns settings dict."""
        self._setup_request_mock(mock_open_url, {"settings": {"enabled": True}})
        api = self._make_api()
        result = api.get_ipmi_settings()
        assert result == {"enabled": True}

    def test_get_ipmi_settings_exception(self, mock_open_url):
        """Test get_ipmi_settings calls fail_json on error."""
        mock_open_url.side_effect = Exception("network error")
        api = self._make_api()
        api.get_ipmi_settings()
        api.module.fail_json.assert_called_once()
        assert "Failed to get IPMI settings" in api.module.fail_json.call_args[1]["msg"]

    def test_update_ipmi_settings(self, mock_open_url):
        """Test update_ipmi_settings makes PUT request."""
        self._setup_request_mock(mock_open_url, {})
        api = self._make_api()
        api.update_ipmi_settings({"enabled": False})
        assert mock_open_url.call_count == 3

    def test_update_ipmi_settings_exception(self, mock_open_url):
        """Test update_ipmi_settings calls fail_json on error."""
        mock_open_url.side_effect = Exception("network error")
        api = self._make_api()
        api.update_ipmi_settings({"enabled": False})
        api.module.fail_json.assert_called_once()
        assert "Failed to update IPMI settings" in api.module.fail_json.call_args[1]["msg"]

    def test_get_ipmi_network(self, mock_open_url):
        """Test get_ipmi_network returns network dict."""
        self._setup_request_mock(mock_open_url, {"network": {"gateway": "10.0.0.1"}})
        api = self._make_api()
        result = api.get_ipmi_network()
        assert result == {"gateway": "10.0.0.1"}

    def test_get_ipmi_network_not_configured(self, mock_open_url):
        """Test get_ipmi_network returns empty dict on 'not configured' error."""
        mock_open_url.side_effect = Exception("IPMI is not configured on this cluster")
        api = self._make_api()
        result = api.get_ipmi_network()
        assert result == {}
        api.module.fail_json.assert_not_called()

    def test_get_ipmi_network_exception(self, mock_open_url):
        """Test get_ipmi_network calls fail_json on other errors."""
        mock_open_url.side_effect = Exception("server error")
        api = self._make_api()
        api.get_ipmi_network()
        api.module.fail_json.assert_called_once()

    def test_update_ipmi_network(self, mock_open_url):
        """Test update_ipmi_network makes PUT request."""
        self._setup_request_mock(mock_open_url, {})
        api = self._make_api()
        api.update_ipmi_network({"gateway": "10.0.0.2"})
        assert mock_open_url.call_count == 3

    def test_update_ipmi_network_exception(self, mock_open_url):
        """Test update_ipmi_network calls fail_json on error."""
        mock_open_url.side_effect = Exception("network error")
        api = self._make_api()
        api.update_ipmi_network({"gateway": "10.0.0.2"})
        api.module.fail_json.assert_called_once()

    def test_get_ipmi_user(self, mock_open_url):
        """Test get_ipmi_user returns user dict."""
        self._setup_request_mock(mock_open_url, {"user": {"username": "admin"}})
        api = self._make_api()
        result = api.get_ipmi_user()
        assert result == {"username": "admin"}

    def test_get_ipmi_user_not_configured(self, mock_open_url):
        """Test get_ipmi_user returns empty dict on 'not configured' error."""
        mock_open_url.side_effect = Exception("IPMI user is not configured")
        api = self._make_api()
        result = api.get_ipmi_user()
        assert result == {}

    def test_get_ipmi_user_exception(self, mock_open_url):
        """Test get_ipmi_user calls fail_json on other errors."""
        mock_open_url.side_effect = Exception("server error")
        api = self._make_api()
        api.get_ipmi_user()
        api.module.fail_json.assert_called_once()

    def test_update_ipmi_user(self, mock_open_url):
        """Test update_ipmi_user makes PUT request."""
        self._setup_request_mock(mock_open_url, {})
        api = self._make_api()
        api.update_ipmi_user({"username": "admin", "password": "test_password_placeholder"})
        assert mock_open_url.call_count == 3

    def test_update_ipmi_user_exception(self, mock_open_url):
        """Test update_ipmi_user calls fail_json on error."""
        mock_open_url.side_effect = Exception("network error")
        api = self._make_api()
        api.update_ipmi_user({"username": "admin"})
        api.module.fail_json.assert_called_once()

    def test_get_ipmi_features(self, mock_open_url):
        """Test get_ipmi_features returns features list."""
        self._setup_request_mock(mock_open_url, {
            "features": [{"id": "power_control", "enabled": True}]
        })
        api = self._make_api()
        result = api.get_ipmi_features()
        assert result == [{"id": "power_control", "enabled": True}]

    def test_get_ipmi_features_not_configured(self, mock_open_url):
        """Test get_ipmi_features returns empty list on 'not configured'."""
        mock_open_url.side_effect = Exception("Features not configured")
        api = self._make_api()
        result = api.get_ipmi_features()
        assert result == []

    def test_get_ipmi_features_exception(self, mock_open_url):
        """Test get_ipmi_features calls fail_json on other errors."""
        mock_open_url.side_effect = Exception("server error")
        api = self._make_api()
        api.get_ipmi_features()
        api.module.fail_json.assert_called_once()

    def test_update_ipmi_feature(self, mock_open_url):
        """Test update_ipmi_feature makes PUT to feature-specific endpoint."""
        self._setup_request_mock(mock_open_url, {})
        api = self._make_api()
        api.update_ipmi_feature("power_control", {"enabled": True})
        call_args = mock_open_url.call_args_list[1]
        assert "features/power_control" in str(call_args)

    def test_update_ipmi_feature_exception(self, mock_open_url):
        """Test update_ipmi_feature calls fail_json on error."""
        mock_open_url.side_effect = Exception("network error")
        api = self._make_api()
        api.update_ipmi_feature("sol", {"enabled": True})
        api.module.fail_json.assert_called_once()
        assert "sol" in api.module.fail_json.call_args[1]["msg"]

    def test_get_ipmi_nodes(self, mock_open_url):
        """Test get_ipmi_nodes returns nodes list."""
        self._setup_request_mock(mock_open_url, {
            "nodes": [{"id": 1, "ipmi_address": "10.0.0.100"}]
        })
        api = self._make_api()
        result = api.get_ipmi_nodes()
        assert result == [{"id": 1, "ipmi_address": "10.0.0.100"}]

    def test_get_ipmi_nodes_not_configured(self, mock_open_url):
        """Test get_ipmi_nodes returns empty list on 'not configured'."""
        mock_open_url.side_effect = Exception("Nodes not configured")
        api = self._make_api()
        result = api.get_ipmi_nodes()
        assert result == []

    def test_get_ipmi_nodes_exception(self, mock_open_url):
        """Test get_ipmi_nodes calls fail_json on other errors."""
        mock_open_url.side_effect = Exception("server error")
        api = self._make_api()
        api.get_ipmi_nodes()
        api.module.fail_json.assert_called_once()

    def test_get_all_ipmi_config(self, mock_open_url):
        """Test get_all_ipmi_config aggregates all domains."""
        call_count = [0]
        responses = [
            {"settings": {"enabled": True}},
            {"network": {"gateway": "10.0.0.1"}},
            {"user": {"username": "admin"}},
            {"features": [{"id": "power_control", "enabled": True}]},
            {"nodes": [{"id": 1}]},
        ]

        def side_effect_fn(*args, **kwargs):
            nonlocal call_count
            idx = call_count[0]
            call_count[0] += 1
            if idx % 3 == 0:
                resp = MagicMock()
                resp.read.return_value = b'{}'
                resp.headers = {
                    'Set-Cookie': 'isisessid=abc; path=/',
                    'X-CSRF-Token': 'csrf',
                }
                return resp
            elif idx % 3 == 1:
                import json as json_mod
                resp = MagicMock()
                data_idx = idx // 3
                resp.read.return_value = json_mod.dumps(
                    responses[data_idx] if data_idx < len(responses) else {}
                ).encode()
                return resp
            else:
                return MagicMock()

        mock_open_url.side_effect = side_effect_fn
        api = self._make_api()
        result = api.get_all_ipmi_config()
        assert 'settings' in result
        assert 'network' in result
        assert 'user' in result
        assert 'features' in result
        assert 'nodes' in result
