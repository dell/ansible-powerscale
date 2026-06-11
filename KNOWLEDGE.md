# KNOWLEDGE.md — ansible-powerscale

<!-- yaml-metadata-start -->
scope_paths: ["./"]
capture_git_sha: "c117cc5c803f9b58d19cc9f081cb616f15396acf"
status: "current"
auto_update: false
preview_before_apply: true
scaffold_version: "1.0"
# session_state: { is_complete: true }
<!-- yaml-metadata-end -->

<!-- quick-reference-start -->
## Agent Quick Reference

| Section | Heading | Summary | never_again_count |
|---------|---------|---------|-------------------|
| Component Overview | `## Component Overview` | dellemc.powerscale collection for PowerScale | — |
| Architectural Rationale | `## Architectural Rationale` | isilon-sdk SDK; Ansible collection pattern | — |
| Failure Modes & Gotchas | `## Failure Modes & Gotchas` | SDK coupling, idempotency, verify_ssl | 0 |
| Implicit Contracts | `## Implicit Contracts` | Connection params, ordering, action groups | — |
<!-- quick-reference-end -->

## Five Questions Quick Reference

### What does it do?
Ansible Galaxy collection `dellemc.powerscale` (v3.9.1). Provides 56 modules for declarative, idempotent management of Dell PowerScale (Isilon) scale-out NAS storage. Uses `isilon-sdk` (==0.6.0) Python SDK.

### How do you modify it?
Create module file in `plugins/modules/`, add example playbook in `playbooks/modules/`, add unit test in `tests/unit/plugins/modules/`, append module FQCN to `meta/runtime.yml` action group.

### What breaks?
SDK version mismatch is a blocking defect. Missing action group entry causes `module_defaults` to silently skip the module. `verify_ssl: false` in production violates security constitution.

### What depends on it?
`isilon-sdk` ==0.6.0, Ansible >= 2.15.0. Ordering: dependent resources must exist before referencing them.

### What's undocumented?
`powerscale_base.py` (base class) + 12 per-API-domain helpers: `auth.py`, `certificate.py`, `cluster.py`, `events.py`, `ipmi.py`, `namespace.py`, `protocol.py`, `quota.py`, `snapshot.py`, `support_assist.py`, `synciq.py`, `zones_summary.py`. Uses `logging.basicConfig` with `CustomRotatingFileHandler`. Writes `ansible_powerscale.log` by default (5 MB rotate, 5 backups).

---

## Component Overview

Ansible Galaxy collection `dellemc.powerscale` (v3.9.1) for Dell PowerScale (Isilon) scale-out NAS storage. 56 modules covering access zones, ACLs, quotas, SMB shares, NFS exports, snapshot schedules, user groups, file systems, network settings, cluster configuration, S3 buckets, SyncIQ policies, NDMP, support assist, LDAP, ADS, certificates, and more.

---

## Architectural Rationale

Standard Ansible Galaxy collection layout. Each module is a self-contained Python file under `plugins/modules/` that communicates with the PowerScale REST API through the `isilon-sdk` SDK.

**SDK strategy:** **Dynamic** — `importlib.import_module('isilon_sdk.<version>')` at runtime. Static analysis cannot detect this dependency.. Version pinned at `==0.6.0` in `requirements.txt`.

---

## Failure Modes & Gotchas

### 1. SDK version coupling

Each collection release is tested against exactly one SDK version (or tight range for PyU4V). A mismatch between collection and SDK version is a blocking defect. Never update `requirements.txt` SDK versions without verifying against the corresponding collection release notes.

### 2. Idempotency assumptions

Modules are designed to be idempotent but some parameters may be accepted by the module yet ignored by the underlying API. Always verify with a second run.

### 3. Verify SSL setting

`verify_ssl: false` is used in example playbooks but is a lab-only setting. Production requires `true`. Modules must not default to skipping verification.

### 4. Acceptance test cleanup

If tests fail mid-run, resources may be left on the array. Clean up manually before re-running.

### Dynamic SDK Import

The `isilon-sdk` package uses version-specific module names (e.g. `isilon_sdk.v9_5_0`). The collection imports it at runtime via `importlib.import_module()`. Static analysis tools (linters, dependency scanners) will **not** detect this dependency. It is declared only in `requirements.txt`. Agents adding imports must not assume static import is feasible.

### Port Configuration

The provider defaults to port 8080 for the Platform API. This is configurable via the `port_no` parameter (unique to PowerScale among storage collections).

### Never Again

No incident-derived constraints recorded.

---

## Performance Characteristics

TBD — requires SME input.

---

## Implicit Contracts

**Connection parameters required:** All modules require `onefs_host`, `api_user`, `api_password`, `verify_ssl` — these are not optional.

**Resource ordering:** Dependent resources must exist before being referenced (e.g., filesystem before snapshot, volume group before volumes, policies before assignment).

**Action group registration:** Every new module must be appended to the `dellemc.powerscale.all` action group in `meta/runtime.yml`.

---

## Threading & Synchronization

Ansible handles concurrency via forks at the play level. Individual module executions are single-threaded.

---

## Build System & Configuration

| Command | Description |
|---------|-------------|
| `ansible-galaxy collection build` | Build collection tarball |
| `ansible-galaxy collection install <tarball>` | Install locally |
| `pytest tests/unit/` | Run unit tests |
| `ansible-playbook --syntax-check` | Validate playbook syntax |

---

## Operational Knowledge

Uses `logging.basicConfig` with `CustomRotatingFileHandler`. Writes `ansible_powerscale.log` by default (5 MB rotate, 5 backups).

---

## General Context

No additional context beyond what has been captured.

---

## References

- [Ansible Galaxy — dellemc.powerscale](https://galaxy.ansible.com/dellemc/powerscale)
- [Ansible Collection Developer Guide](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html)

---

## Governance Spec Discrepancies

No discrepancies detected.
