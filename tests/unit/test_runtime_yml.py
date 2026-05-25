"""
Unit tests for runtime.yml validation and action_groups configuration.

Tests cover the validation helper functions used to verify the
global action groups feature for module_defaults support.
"""

import os
import tempfile
import pytest
import yaml

from tests.unit.utils.runtime_yml_validator import (
    validate_runtime_yml_syntax,
    validate_action_group_structure,
    validate_module_list_completeness,
    validate_module_name_format,
)

VALID_RUNTIME_YML = """
requires_ansible: ">=2.15.0"
plugin_routing:
    action_groups:
        dellemc.powerscale.all:
            - dellemc.powerscale.accesszone
            - dellemc.powerscale.filesystem
            - dellemc.powerscale.settings
"""

INVALID_YAML = """
requires_ansible: ">=2.15.0"
plugin_routing:
    action_groups:
        dellemc.powerscale.all:
            modules:
                - dellemc.powerscale.accesszone
                  bad_indent: broken yaml: [unclosed
"""

INVALID_ACTION_GROUP_YML = """
requires_ansible: ">=2.15.0"
plugin_routing:
    action_groups:
        dellemc.powerscale.all:
            modules:
                - dellemc.powerscale.accesszone
"""


@pytest.fixture
def valid_runtime_yml_file(tmp_path):
    f = tmp_path / "runtime.yml"
    f.write_text(VALID_RUNTIME_YML)
    return str(f)


@pytest.fixture
def invalid_yaml_file(tmp_path):
    f = tmp_path / "runtime.yml"
    f.write_text(INVALID_YAML)
    return str(f)


@pytest.fixture
def valid_runtime_dict():
    return yaml.safe_load(VALID_RUNTIME_YML)


@pytest.fixture
def mock_modules_dir(tmp_path):
    modules_dir = tmp_path / "plugins" / "modules"
    modules_dir.mkdir(parents=True)
    for name in ["accesszone", "filesystem", "settings"]:
        (modules_dir / f"{name}.py").write_text("# module")
    return str(modules_dir)


class TestValidateRuntimeYmlSyntax:
    def test_validate_runtime_yml_syntax(self, valid_runtime_yml_file):
        is_valid, error = validate_runtime_yml_syntax(valid_runtime_yml_file)
        assert is_valid is True
        assert error == ""

    def test_validate_runtime_yml_syntax_invalid(self, invalid_yaml_file):
        is_valid, error = validate_runtime_yml_syntax(invalid_yaml_file)
        assert is_valid is False
        assert "YAML syntax error" in error or "error" in error.lower()

    def test_validate_runtime_yml_syntax_missing_file(self):
        is_valid, error = validate_runtime_yml_syntax("/nonexistent/path/runtime.yml")
        assert is_valid is False
        assert "not found" in error.lower() or "no such file" in error.lower()


class TestValidateActionGroupStructure:
    def test_validate_action_group_structure(self, valid_runtime_dict):
        is_valid, error = validate_action_group_structure(valid_runtime_dict)
        assert is_valid is True
        assert error == ""

    def test_validate_action_group_structure_invalid(self):
        bad_dict = yaml.safe_load(INVALID_ACTION_GROUP_YML)
        is_valid, error = validate_action_group_structure(bad_dict)
        assert is_valid is False
        assert "direct list" in error or len(error) > 0

    def test_validate_action_group_structure_missing_plugin_routing(self):
        is_valid, error = validate_action_group_structure({})
        assert is_valid is False
        assert "plugin_routing" in error

    def test_validate_action_group_structure_missing_action_groups(self):
        d = {"plugin_routing": {"modules": {}}}
        is_valid, error = validate_action_group_structure(d)
        assert is_valid is False
        assert "action_groups" in error

    def test_validate_action_group_structure_missing_group_name(self):
        d = {"plugin_routing": {"action_groups": {"other.group": {"modules": []}}}}
        is_valid, error = validate_action_group_structure(d)
        assert is_valid is False
        assert "dellemc.powerscale.all" in error


class TestValidateModuleListCompleteness:
    def test_validate_module_list_completeness(self, valid_runtime_dict, mock_modules_dir):
        is_valid, error, missing = validate_module_list_completeness(
            valid_runtime_dict, mock_modules_dir
        )
        assert is_valid is True
        assert missing == []

    def test_validate_module_list_incomplete(self, mock_modules_dir, tmp_path):
        runtime_dict = yaml.safe_load("""
plugin_routing:
    action_groups:
        dellemc.powerscale.all:
            - dellemc.powerscale.accesszone
""")
        (tmp_path / "plugins" / "modules" / "newmodule.py").write_text("# new")
        modules_dir = str(tmp_path / "plugins" / "modules")
        is_valid, error, missing = validate_module_list_completeness(
            runtime_dict, modules_dir
        )
        assert is_valid is False
        assert len(missing) > 0

    def test_validate_module_list_completeness_invalid_dir(self, valid_runtime_dict):
        is_valid, error, missing = validate_module_list_completeness(
            valid_runtime_dict, "/nonexistent/modules"
        )
        assert is_valid is False
        assert len(error) > 0


class TestValidateModuleNameFormat:
    def test_validate_module_name_format(self):
        names = [
            "dellemc.powerscale.accesszone",
            "dellemc.powerscale.filesystem",
            "dellemc.powerscale.settings",
        ]
        is_valid, error, invalid = validate_module_name_format(names)
        assert is_valid is True
        assert invalid == []

    def test_validate_module_name_format_invalid(self):
        names = [
            "dellemc.powerscale.accesszone",
            "badname",
            "also.wrong",
        ]
        is_valid, error, invalid = validate_module_name_format(names)
        assert is_valid is False
        assert "badname" in invalid
        assert "also.wrong" in invalid

    def test_validate_module_name_format_empty(self):
        is_valid, error, invalid = validate_module_name_format([])
        assert is_valid is True
        assert invalid == []


class TestActionGroupNamingConvention:
    def test_action_group_naming_convention(self, valid_runtime_dict):
        action_groups = valid_runtime_dict["plugin_routing"]["action_groups"]
        assert "dellemc.powerscale.all" in action_groups

    def test_modules_have_correct_namespace(self, valid_runtime_dict):
        modules = valid_runtime_dict["plugin_routing"]["action_groups"][
            "dellemc.powerscale.all"
        ]
        assert all(m.startswith("dellemc.powerscale.") for m in modules)


class TestExamplePlaybookSyntax:
    def test_example_playbook_syntax(self):
        playbook_path = os.path.join(
            os.path.dirname(__file__),
            "../../playbooks/modules/module_defaults_example.yml",
        )
        if not os.path.exists(playbook_path):
            pytest.skip("Example playbook not yet created (Stage 10 deliverable)")
        with open(playbook_path) as f:
            content = yaml.safe_load(f)
        assert content is not None

    def test_example_playbook_syntax_invalid(self, tmp_path):
        bad_playbook = tmp_path / "bad.yml"
        bad_playbook.write_text("- name: test\n  bad: [unclosed bracket\n")
        with pytest.raises(yaml.YAMLError):
            with open(str(bad_playbook)) as f:
                yaml.safe_load(f)
