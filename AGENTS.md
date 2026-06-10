# AGENTS.md - Dell Ansible Collection for PowerScale

## Project Overview

This is the Ansible Galaxy collection for Dell PowerScale (Isilon) scale-out NAS storage. It provides Ansible modules for automating provisioning and management of PowerScale clusters.

- **Language:** Python
- **Collection namespace:** `dellemc.powerscale`
- **SDK:** `isilon-sdk` v0.6.0
- **License:** GNU General Public License v3.0

## Architecture

The collection follows the standard Ansible Galaxy collection layout. Each module is a self-contained Python file under `plugins/modules/` that communicates with the PowerScale Platform API through the `isilon-sdk` Python SDK.

### Authentication

Modules authenticate to a PowerScale cluster using `onefs_host`, `username`, `password`, `port` (typically 8080), and optional `verify_ssl` and `api_version` parameters.

### SDK Strategy

Uses `isilon-sdk` — a Dell-published Python SDK for the PowerScale OneFS Platform API, installed via `pip`. The required version is pinned in `requirements.txt`. Also requires `urllib3` and `packaging`.

### Module Count

The collection includes approximately 113 modules covering PowerScale entities such as access zones, quotas, SMB shares, NFS exports, snapshot schedules, user groups, file pools, NDMP, SyncIQ, network settings, authentication providers, and more.

## Directory Structure

```
galaxy.yml                        Collection metadata (namespace, name, version)
plugins/
  modules/                        Ansible modules (one .py file per resource)
  module_utils/
    storage/                      Shared utility classes and SDK wrappers
  doc_fragments/                  Shared documentation fragments
meta/                             Collection metadata (runtime.yml)
tests/
  unit/
    plugins/                      Unit tests (pytest)
    utils/                        Test utility helpers
playbooks/                        Example playbooks
docs/                             Module documentation
changelogs/                       Release changelog fragments
requirements.txt                  Python dependencies (isilon-sdk, urllib3, packaging)
requirements.yml                  Ansible collection dependencies
```

## Build Commands

| Command | Description |
|---------|-------------|
| `ansible-galaxy collection build` | Build the collection tarball |
| `ansible-galaxy collection install <tarball>` | Install the collection locally |
| `pytest tests/unit/` | Run unit tests |

## Testing

### Unit Tests

- Test files follow `test_*.py` convention in `tests/unit/plugins/`.
- Framework: `pytest` with `unittest.mock` for mocking SDK calls.
- No hardware required.

### Running Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run unit tests
pytest tests/unit/ -v
```

## Code Style and Conventions

### Module Pattern

Each module follows the standard Ansible module pattern:
1. `DOCUMENTATION`, `EXAMPLES`, and `RETURN` docstrings at the top.
2. An `AnsibleModule` argument spec defining parameters.
3. A main class that wraps SDK calls and handles idempotency.
4. `module.exit_json()` for success, `module.fail_json()` for errors.

### Shared Utilities

- `plugins/module_utils/storage/` contains shared base classes and SDK initialization code.
- `plugins/doc_fragments/` contains reusable documentation for common parameters.

### File Header

All source files must include the Dell copyright and GPL v3.0 license header.

## Common Development Tasks

### Adding a New Module

1. Create `plugins/modules/<resource>.py` following the Ansible module pattern.
2. Add unit tests in `tests/unit/plugins/`.
3. Add example playbooks in `playbooks/`.
4. Update `changelogs/` with a changelog fragment.

### Updating the SDK

Update `requirements.txt` with the new `isilon-sdk` version.

## CI/CD

GitHub Actions workflows in `.github/workflows/`. Code coverage tracked via `codecov.yml`.

## Code Ownership

All files are owned by the maintainers defined in `.github/CODEOWNERS`.
