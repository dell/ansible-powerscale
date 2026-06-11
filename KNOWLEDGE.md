# KNOWLEDGE.md — ansible-powerscale

<!-- yaml-metadata-start -->
scope_paths: ["./"]
capture_git_sha: "e8f4dbb257939c894bf04d794639f43269140e15"
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


### Evolution

Early collections used a flat module structure with duplicated auth
and API logic in each module. The shared base class was introduced
after initial module growth to centralize authentication, argument
parsing, and API client initialization. Major refactors include:

- Base class introduction (centralized SDK initialization)
- Module naming standardization
- SDK / REST client improvements
- Improved error handling consistency

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


### 5. Idempotency drift

Occasional idempotency failures where a module reports `changed=false`
but state actually changed on the array. Caused by incomplete state
comparison logic — some parameters accepted by the module are ignored
by the underlying API. Always verify with a second run.

### 6. SDK import failures

Dependency or version mismatches between the collection and its SDK
cause import failures at module load time. Manifests as
`ModuleNotFoundError` or `ImportError` with no actionable message
unless `-vvv` is used.

### 7. Check mode inaccuracies

Not all modules fully simulate changes correctly in check mode.
Some modules report `changed=true` in check mode but would actually
make no change, or vice versa. Treat check mode as advisory, not
authoritative.

### Never Again

#### NA-001: SDK version mismatch causing silent failures
- **Impact:** Modules loaded but returned incorrect data due to
  SDK API changes between versions.
- **Constraint:** SDK version must be pinned exactly in
  `requirements.txt`. Never update without full test pass.
- **Applies to:** All Dell Ansible collections.

#### NA-002: Idempotency regression on update operations
- **Impact:** Repeated playbook runs made unintended changes to
  array resources due to incomplete state comparison.
- **Constraint:** Every module must compare full current state
  before applying changes.
- **Applies to:** All Dell Ansible collections.

#### NA-003: Orphaned resources from test failures
- **Impact:** Test resources left on array after test failure,
  consuming capacity.
- **Constraint:** Manual cleanup required after failed test runs.
- **Applies to:** All Dell Ansible collections.
### Evolution

Failure modes evolved with the base class introduction. Error
handling was standardized across modules during the naming
convention refactor. SDK import failures became less common after
the `HAS_*` flag pattern was adopted consistently.

---

## Performance Characteristics

**Sequential execution:** Ansible executes modules sequentially per
host within a play. Large inventories with many tasks experience
linear performance degradation. No built-in batching or pipelining
at the module level.

**API rate limiting:** PowerScale arrays enforce implicit
throttling under heavy parallel execution (high Ansible fork count).
Reduce `forks` or add `throttle` to tasks hitting the same array.

**Bulk operations:** Module execution is slower for bulk operations
due to per-task API calls with no batching support. Async operations
(where supported) can mitigate but add complexity.

**No connection reuse:** Each module invocation creates a new SDK
client and HTTP session. No connection pooling across tasks.

### Evolution

Performance improved after the base class centralized SDK
initialization, reducing per-module overhead. Connection reuse
remains an open area for improvement.

---

## Implicit Contracts

**Connection parameters required:** All modules require `onefs_host`, `api_user`, `api_password`, `verify_ssl` — these are not optional.

**Resource ordering:** Dependent resources must exist before being referenced (e.g., filesystem before snapshot, volume group before volumes, policies before assignment).

**Action group registration:** Every new module must be appended to the `dellemc.powerscale.all` action group in `meta/runtime.yml`.

### Evolution

Connection parameter patterns were established early and carried
forward. Resource ordering constraints are implicit — the API
returns errors but the collection does not enforce ordering.

---

## Threading & Synchronization

Ansible handles concurrency via forks at the play level. Individual
module executions are single-threaded. However, multiple forks
hitting the same PowerScale array simultaneously causes:

**API contention:** High fork counts cause throttling or transient
errors from the array API. Mitigate with `throttle: N` on tasks
targeting the same array.

**Connection pool exhaustion:** Possible when many forks execute
without HTTP session reuse. Each fork creates independent SDK
client connections.

**Race conditions on shared resources:** Concurrent modifications
to interdependent resources (e.g., volume + host mapping,
replication configurations) can produce inconsistent state.
Serialize dependent operations with `serial: 1` or task ordering.

### Evolution

Concurrency issues became more visible as collections grew and
users ran larger playbooks with higher fork counts against single
arrays.

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

**Logging:** Enable `-vvv` for detailed output including API
request/response payloads. Correlate Ansible output with array
logs for full troubleshooting.

**Common support scenarios:**
- Authentication failures — verify `onefs_host`, credentials,
  and `verify_ssl` settings
- Idempotency issues — run playbook twice, compare `changed`
  status
- Timeout / async completion problems — increase timeout
  parameters, check array load

**Test environment requirements:**
- Dedicated PowerScale array or simulator
- Stable API version matching SDK pin
- Isolated test datasets (avoid shared resources)

### Evolution

Debugging patterns improved with `-vvv` adoption as standard
practice. Common failure patterns documented after recurring
support cases.

---

## General Context

No additional context beyond what has been captured.

### Open Issues

No TODO/FIXME/HACK markers found in non-test source files.

---

## References

- [Ansible Galaxy — dellemc.powerscale](https://galaxy.ansible.com/dellemc/powerscale)
- [Ansible Collection Developer Guide](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html)

---

## Governance Spec Discrepancies

No discrepancies detected.
