# Developer Guide

This guide covers how to run unit tests, sanity checks, and linting for the `dellemc.powerscale` Ansible collection.

## Prerequisites

- Python 3.11+ (3.13 recommended; 3.14 also works)
- Docker (required for `ansible-test sanity`)
- A virtual environment at the repo root (`.venv/`)

### Setting up the virtual environment

```bash
cd /root/ansible_collections/dellemc/powerscale
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt -r tests/unit/requirements.txt ansible-lint ansible-core
```

## Unit Tests

Unit tests live under `tests/unit/plugins/modules/` and use `pytest`. Mock API responses are in `tests/unit/plugins/module_utils/`.

### Running all unit tests

```bash
cd ansible_collections/dellemc/powerscale
source .venv/bin/activate
export ANSIBLE_COLLECTIONS_PATH=../../../
export PYTHONPATH=../../../
python -m pytest tests/unit/plugins/modules/ -v
```

> **Note:** Both `ANSIBLE_COLLECTIONS_PATH` and `PYTHONPATH` must point to the parent of `ansible_collections/` (using `../../../` from the collection directory) so that `ansible_collections.dellemc.powerscale` imports resolve correctly.

### Running tests for a specific module

```bash
cd ansible_collections/dellemc/powerscale
source .venv/bin/activate
export ANSIBLE_COLLECTIONS_PATH=../../../
export PYTHONPATH=../../../
python -m pytest tests/unit/plugins/modules/test_s3_global_settings.py -v
```

### Running tests with coverage

```bash
cd ansible_collections/dellemc/powerscale
source .venv/bin/activate
export ANSIBLE_COLLECTIONS_PATH=../../../
export PYTHONPATH=../../../
python -m pytest \
    tests/unit/plugins/modules/test_s3_global_settings.py \
    tests/unit/plugins/modules/test_s3_zone_settings.py \
    --cov=ansible_collections.dellemc.powerscale.plugins.modules.s3_global_settings \
    --cov=ansible_collections.dellemc.powerscale.plugins.modules.s3_zone_settings \
    --cov-report=term-missing
```

The `--cov` argument must use the full dotted module path (not relative file paths) for coverage to work.

### Running unit tests via ansible-test (CI-equivalent)

```bash
ansible-test units --docker default
```

This runs all unit tests inside a Docker container matching the CI environment.

## Sanity Tests

Sanity tests check for coding standards, import correctness, documentation validity, and more (34 tests total).

### Running sanity on all files

```bash
ansible-test sanity --docker default
```

### Running sanity on specific files only

```bash
ansible-test sanity --docker default plugins/modules/s3_global_settings.py plugins/modules/s3_zone_settings.py
```

### Common sanity failures and fixes

| Test | Typical issue | Fix |
|------|--------------|-----|
| `pep8` | Indentation, line length | Follow PEP 8 style |
| `validate-modules` | DOCUMENTATION block issues | Ensure `author` field uses `Name (@github-handle) <email>` format |
| `pylint` | Unused imports, etc. | Remove unused imports or add `# pylint: disable=...` |
| `line-endings` | `\r\n` instead of `\n` | Convert to Unix line endings |

## Ansible Lint

Ansible-lint validates playbooks and module code against Ansible best practices.

### Running ansible-lint

```bash
.venv/bin/ansible-lint
```

### Running on specific files

```bash
.venv/bin/ansible-lint plugins/modules/s3_global_settings.py playbooks/modules/s3_global_settings.yml
```

### Configuration

The `.ansible-lint` file at the repo root controls lint settings. Currently it excludes `.github/`:

```yaml
exclude_paths:
  - .github/
```

## CI Workflow

The GitHub Actions workflow (`.github/workflows/ansible-test.yml`) runs on every PR and push to `main`:

1. **Build** - Builds the collection tarball (Python 3.13, Ansible stable-2.19)
2. **Unit Tests** (optional) - Runs across Python 3.11/3.12/3.13 and Ansible stable-2.17/2.18/2.19/devel
3. **Sanity** (required) - Uses the `ansible/ansible-content-actions` reusable workflow
4. **Ansible Lint** (required) - Uses the `ansible/ansible-content-actions` reusable workflow

## Test File Conventions

- Module test files: `tests/unit/plugins/modules/test_<module_name>.py`
- Mock API files: `tests/unit/plugins/module_utils/mock_<module_name>_api.py`
- Example playbooks: `playbooks/modules/<module_name>.yml`
- Test classes extend `PowerScaleUnitBase` (in `tests/unit/plugins/module_utils/shared_library/powerscale_unit_base.py`)
- Mock setup is handled by `tests/unit/plugins/module_utils/shared_library/initial_mock.py` which patches `AnsibleModule`, SDK imports, and utility functions

## Dependencies

**Runtime dependencies** are defined in `requirements.txt` at the repository root.

**Test dependencies** are defined in `tests/unit/requirements.txt`.
