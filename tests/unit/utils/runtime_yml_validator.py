"""
Runtime YAML Validation Utilities

This module provides validation functions for runtime.yml configuration,
specifically for validating action_groups structure for module_defaults support.
These are test helper functions used to validate the configuration-only change.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Tuple


def validate_runtime_yml_syntax(file_path: str) -> Tuple[bool, str]:
    """
    Validate YAML syntax of runtime.yml file.
    
    Args:
        file_path: Path to runtime.yml file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        with open(file_path, 'r') as f:
            yaml.safe_load(f)
        return True, ""
    except yaml.YAMLError as e:
        return False, f"YAML syntax error: {str(e)}"
    except FileNotFoundError:
        return False, f"File not found: {file_path}"


def validate_action_group_structure(runtime_yml_dict: Dict) -> Tuple[bool, str]:
    """
    Validate action_groups structure in runtime.yml.
    
    Args:
        runtime_yml_dict: Parsed runtime.yml as dictionary
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if 'plugin_routing' not in runtime_yml_dict:
        return False, "Missing plugin_routing section"
    
    plugin_routing = runtime_yml_dict['plugin_routing']
    if 'action_groups' not in plugin_routing:
        return False, "Missing action_groups section"
    
    action_groups = plugin_routing['action_groups']
    if not isinstance(action_groups, dict):
        return False, "action_groups must be a dictionary"
    
    if 'dellemc.powerscale.all' not in action_groups:
        return False, "Missing dellemc.powerscale.all action group"
    
    action_group = action_groups['dellemc.powerscale.all']
    if not isinstance(action_group, list):
        return False, "action group must be a direct list of module names (not a dict with 'modules' key)"
    
    return True, ""


def validate_module_list_completeness(
    runtime_yml_dict: Dict, 
    modules_dir: str
) -> Tuple[bool, str, List[str]]:
    """
    Validate that all modules in plugins/modules/ are in the action group.
    
    Args:
        runtime_yml_dict: Parsed runtime.yml as dictionary
        modules_dir: Path to plugins/modules directory
        
    Returns:
        Tuple of (is_valid, error_message, missing_modules)
    """
    try:
        # Get modules from action group (direct list format)
        action_group = runtime_yml_dict['plugin_routing']['action_groups']['dellemc.powerscale.all']
        action_group_modules = set(action_group)
        
        # Get actual module files
        modules_path = Path(modules_dir)
        if not modules_path.exists():
            return False, f"Modules directory not found: {modules_dir}", []
        actual_modules = set()
        for module_file in modules_path.glob('*.py'):
            if module_file.name != '__init__.py':
                module_name = f"dellemc.powerscale.{module_file.stem}"
                actual_modules.add(module_name)
        
        # Check for missing modules
        missing_modules = actual_modules - action_group_modules
        
        if missing_modules:
            return False, f"Missing modules in action group: {missing_modules}", sorted(missing_modules)
        
        return True, "", []
    except Exception as e:
        return False, f"Error validating module list: {str(e)}", []


def validate_module_name_format(module_names: List[str]) -> Tuple[bool, str, List[str]]:
    """
    Validate that all module names follow the dellemc.powerscale.* format.
    
    Args:
        module_names: List of module names to validate
        
    Returns:
        Tuple of (is_valid, error_message, invalid_names)
    """
    invalid_names = []
    for module_name in module_names:
        if not module_name.startswith('dellemc.powerscale.'):
            invalid_names.append(module_name)
    
    if invalid_names:
        return False, f"Invalid module name format: {invalid_names}", invalid_names
    
    return True, "", []
