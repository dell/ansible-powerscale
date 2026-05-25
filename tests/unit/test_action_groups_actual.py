"""
TDD tests for action_groups feature - RED state.

These tests verify the actual meta/runtime.yml and example playbook files,
and will FAIL until the implementation adds the action_groups configuration.
"""

import os
import pytest
import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUNTIME_YML = os.path.join(REPO_ROOT, "meta", "runtime.yml")
MODULES_DIR = os.path.join(REPO_ROOT, "plugins", "modules")
EXAMPLE_PLAYBOOK = os.path.join(REPO_ROOT, "playbooks", "modules", "module_defaults_example.yml")

EXPECTED_NAMESPACE = "dellemc.powerscale"
EXPECTED_GROUP = "dellemc.powerscale.all"


@pytest.fixture(scope="module")
def runtime_yml():
    with open(RUNTIME_YML, "r") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def actual_module_names():
    names = []
    for fname in sorted(os.listdir(MODULES_DIR)):
        if fname.endswith(".py") and fname != "__init__.py":
            names.append(f"{EXPECTED_NAMESPACE}.{fname[:-3]}")
    return names


class TestRuntimeYmlHasActionGroups:
    """U-003: Validate that runtime.yml has action_groups section - RED until implemented."""

    def test_plugin_routing_has_action_groups(self, runtime_yml):
        """runtime.yml plugin_routing must contain action_groups key."""
        assert "action_groups" in runtime_yml.get("plugin_routing", {}), (
            "meta/runtime.yml is missing plugin_routing.action_groups. "
            "Add action_groups section to support module_defaults."
        )

    def test_action_group_all_exists(self, runtime_yml):
        """dellemc.powerscale.all action group must be defined."""
        action_groups = runtime_yml.get("plugin_routing", {}).get("action_groups", {})
        assert EXPECTED_GROUP in action_groups, (
            f"Action group '{EXPECTED_GROUP}' not found in runtime.yml. "
            "Add it under plugin_routing.action_groups."
        )

    def test_action_group_is_list(self, runtime_yml):
        """dellemc.powerscale.all must be a direct list (Ansible action_groups schema)."""
        action_groups = runtime_yml.get("plugin_routing", {}).get("action_groups", {})
        group = action_groups.get(EXPECTED_GROUP)
        assert isinstance(group, list), (
            f"'{EXPECTED_GROUP}' must be a direct list of module names, got {type(group)}. "
            "Ansible iterates action_group entries directly — a dict-with-modules-key is not supported."
        )

    def test_action_group_not_empty(self, runtime_yml):
        """The action group list must not be empty."""
        action_groups = runtime_yml.get("plugin_routing", {}).get("action_groups", {})
        modules = action_groups.get(EXPECTED_GROUP, [])
        assert len(modules) > 0, (
            f"'{EXPECTED_GROUP}' is empty. All PowerScale modules must be listed."
        )


class TestAllModulesInActionGroup:
    """U-005: All modules in plugins/modules/ must be in action group - RED until implemented."""

    def test_all_actual_modules_in_action_group(self, runtime_yml, actual_module_names):
        """Every .py file in plugins/modules/ must appear in the action group."""
        action_groups = runtime_yml.get("plugin_routing", {}).get("action_groups", {})
        listed_modules = set(action_groups.get(EXPECTED_GROUP, []))
        missing = [m for m in actual_module_names if m not in listed_modules]
        assert not missing, (
            f"The following modules are in plugins/modules/ but missing from the action group:\n"
            + "\n".join(f"  - {m}" for m in sorted(missing))
        )

    def test_no_extra_modules_in_action_group(self, runtime_yml, actual_module_names):
        """Action group must not list modules that don't exist in plugins/modules/."""
        action_groups = runtime_yml.get("plugin_routing", {}).get("action_groups", {})
        listed_modules = set(action_groups.get(EXPECTED_GROUP, []))
        actual_set = set(actual_module_names)
        extra = listed_modules - actual_set
        assert not extra, (
            f"The following modules are listed in action group but don't exist:\n"
            + "\n".join(f"  - {m}" for m in sorted(extra))
        )

    def test_no_duplicate_modules(self, runtime_yml):
        """No module should appear twice in the action group."""
        action_groups = runtime_yml.get("plugin_routing", {}).get("action_groups", {})
        modules = action_groups.get(EXPECTED_GROUP, [])
        duplicates = [m for m in modules if modules.count(m) > 1]
        assert not duplicates, (
            f"Duplicate modules found in action group: {set(duplicates)}"
        )

    def test_module_count_matches_plugins_dir(self, runtime_yml, actual_module_names):
        """Number of modules in action group must match number of .py files in plugins/modules/."""
        action_groups = runtime_yml.get("plugin_routing", {}).get("action_groups", {})
        listed_modules = action_groups.get(EXPECTED_GROUP, [])
        assert len(listed_modules) == len(actual_module_names), (
            f"Module count mismatch: {len(listed_modules)} in action group, "
            f"{len(actual_module_names)} in plugins/modules/."
        )


class TestModuleNameFormat:
    """U-007/U-009: All module names must follow dellemc.powerscale.* format."""

    def test_all_module_names_have_correct_prefix(self, runtime_yml):
        """All entries in action group must start with 'dellemc.powerscale.'"""
        action_groups = runtime_yml.get("plugin_routing", {}).get("action_groups", {})
        modules = action_groups.get(EXPECTED_GROUP, [])
        invalid = [m for m in modules if not m.startswith(f"{EXPECTED_NAMESPACE}.")]
        assert not invalid, (
            f"Module names with incorrect format (must start with '{EXPECTED_NAMESPACE}.'):\n"
            + "\n".join(f"  - {m}" for m in sorted(invalid))
        )

    def test_action_group_name_follows_convention(self, runtime_yml):
        """Action group name must be 'dellemc.powerscale.all'."""
        action_groups = runtime_yml.get("plugin_routing", {}).get("action_groups", {})
        assert EXPECTED_GROUP in action_groups, (
            f"Action group must be named '{EXPECTED_GROUP}'. "
            f"Found: {list(action_groups.keys())}"
        )


class TestExamplePlaybookExists:
    """U-010/FR-007: Example playbook must exist - RED until implemented."""

    def test_example_playbook_file_exists(self):
        """playbooks/modules/module_defaults_example.yml must exist."""
        assert os.path.exists(EXAMPLE_PLAYBOOK), (
            f"Example playbook not found at: {EXAMPLE_PLAYBOOK}\n"
            "Create playbooks/modules/module_defaults_example.yml as part of implementation."
        )

    def test_example_playbook_is_valid_yaml(self):
        """Example playbook must be valid YAML."""
        if not os.path.exists(EXAMPLE_PLAYBOOK):
            pytest.fail(f"Example playbook not found: {EXAMPLE_PLAYBOOK}")
        with open(EXAMPLE_PLAYBOOK) as f:
            data = yaml.safe_load(f)
        assert data is not None, "Example playbook is empty."
        assert isinstance(data, list), "Example playbook must be a list of plays."

    def test_example_playbook_contains_module_defaults(self):
        """Example playbook must use module_defaults with global action group."""
        if not os.path.exists(EXAMPLE_PLAYBOOK):
            pytest.fail(f"Example playbook not found: {EXAMPLE_PLAYBOOK}")
        with open(EXAMPLE_PLAYBOOK) as f:
            content = f.read()
        assert "module_defaults" in content, (
            "Example playbook must contain a module_defaults section."
        )
        assert "group/dellemc.powerscale.all" in content, (
            "Example playbook must use 'group/dellemc.powerscale.all' in module_defaults."
        )

    def test_example_playbook_uses_powerscale_modules(self):
        """Example playbook must invoke at least one PowerScale module."""
        if not os.path.exists(EXAMPLE_PLAYBOOK):
            pytest.fail(f"Example playbook not found: {EXAMPLE_PLAYBOOK}")
        with open(EXAMPLE_PLAYBOOK) as f:
            content = f.read()
        assert "dellemc.powerscale." in content, (
            "Example playbook must use at least one dellemc.powerscale.* module."
        )
