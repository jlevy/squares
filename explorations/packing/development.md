# Packing Development Guide

This is the engineering entry point for `explorations/packing/`. Read
[`TUTORIAL.md`](TUTORIAL.md) for the mathematics, [`SYNOPSIS.md`](SYNOPSIS.md) for
research status, and [`campaign/README.md`](campaign/README.md) before operating the
research loop. This guide owns runtime support, code placement, validation, and
refactoring practice.

The governing rule is assurance proportional to reuse and consequence.
Shared code and research-state boundaries are designed, typed, tested, and kept easy to
orient around. A retained checker for one value of `n` may stay direct and specialized.
Do not turn a one-off investigation into a framework without a second real consumer.

## Supported Environment

Python **3.14 is the only supported minor version**. Local development and CI pin the
interpreter to **3.14.7** through `.python-version` and the workflow.
Package metadata, Ruff, and BasedPyright express the broader `3.14`-only compatibility
boundary; `uv.lock` pins dependencies, not the interpreter.
macOS and Linux are supported development hosts, and CI runs the ordinary full gate on
both. The Rust search engine uses the stable Cargo toolchain.

From this directory:

```shell
uv sync --frozen --all-extras --group dev
uv run --frozen --all-extras --group dev python --version
uv run --frozen --all-extras --group dev packing-validate --fast
```

The version command must report Python 3.14.7. Do not run a bare `pip install`, commit a
second requirements file, or rely on packages from a global interpreter.
Change dependencies in `pyproject.toml`, regenerate `uv.lock`, and commit both files
together. Use `uv sync --frozen --all-extras --group dev` in CI and when reproducing the
locked development environment; the explicit development group prevents an ambient uv
configuration from omitting the test and quality tools.

## Code Maturity and Placement

The maturity class says how a module is maintained, not how important its mathematics
is.

| Class | Location | Contract |
| --- | --- | --- |
| **E0 scratch** | Untracked scratch space or the repository `attic/` | Optimize for learning. Do not import it or cite it as evidence. Delete it or promote it when the investigation ends. |
| **E1 retained case code** | `cases/<case>/` | Scope the code to a named `n`, source, theorem, hypothesis, or experiment. State its evidence limits and retain enough input and output for replay. General APIs are optional. |
| **E2 reusable research code** | `src/sqpack/research/` and shared helpers such as `workers.py` | Serve multiple research loops through typed contracts, deterministic tests, explicit errors, and case-free policy. Optimize only from representative measurements. |
| **E3 trust and persistence code** | `src/sqpack/field.py`, `verify.py`, `witness.py`, `src/sqpack/campaign/`, and `src/sqpack/cli/` | Meet E2 expectations plus independent or mutation checks, tested failures, atomic durable writes, and fail-fast persisted-format handling. Campaign and CLI modules are repository applications, not general library APIs. |

Developer infrastructure has its own explicit locations:

- `devtools/` contains repository checks, renderers, schema validation, and negative
  controls. It is not an application API.
- `benchmarks/` contains performance probes whose purpose is measurement, not pass/fail
  correctness.
- `tests/` contains fast behavior, architecture, and CLI contracts.
- `sqsearch/` contains the Rust screening engine.
- `campaign/`, `frontier/`, `atlas/`, and `golden/` contain research state and retained
  evidence, not importable implementation code.

Dependencies flow toward more foundational code:

```text
cases/ and devtools/ ──> sqpack.research ──> sqpack foundations
      campaign app ────> foundations and retained campaign state
           CLI app ────> foundations and named cases/devtools subprocesses
```

`tests/test_module_boundaries.py` enforces the important edges and rejects Python left
in the old top-level, `tools/`, `campaign/`, or `sqpack/` implementation locations.
Reusable foundations, research modules, and campaign code may not import or name a
process dependency on `cases` or `devtools`. The outer validation CLI intentionally
starts named case and developer-tool modules in subprocesses; the architecture test
inventories those string edges as well as Python imports.
A case may consume a maintained API; the maintained API may not grow a Trump-, Göbel-,
checkpoint-, or single-`n` exception to accommodate it.

The four installed commands operate on repository-owned state, so they require a valid
`explorations/packing/` checkout.
Source and editable installs locate that checkout directly; a non-editable installation
can use the current checkout or set `PACKING_PROJECT_ROOT` explicitly.
A missing or malformed project root is a hard, actionable error.
Importing reusable `sqpack` modules does not require repository state.

Promote E1 code only after identifying a shared contract and a second real consumer.
Copying ten clear lines twice is often cheaper than inventing an abstraction whose
policy is still changing.
When a supposedly reusable path loses its consumers, demote or remove it instead of
preserving an empty layer.

## Command Surfaces

The installed commands are:

| Command | Purpose |
| --- | --- |
| `packing-validate` | Read-only project validation, focused selection, and machine-readable summaries |
| `packing-campaign` | State-machine operations for preregistered numerical rounds |
| `packing-ledger` | Check campaign invariants and freshness, or atomically render the generated ledger |
| `packing-witness` | Inspect, numerically check, or formally verify a portable packing witness without changing it |

Run `COMMAND --help` before using a command in automation.
A maintained CLI must parse arguments before doing work, keep data on stdout and
diagnostics on stderr, return a nonzero status for partial or complete failure, and
expose JSON or JSONL when its output is a data contract.
Names should say what the command does without directory context.

Use these verbs consistently:

- `check` reads and compares without changing durable state; for a packing witness it
  reports numerical assurance and the actual arithmetic, precision, and tolerance;
- `verify` is reserved for a formal decision from exact arithmetic, a rigorous
  certificate, or a complete proof;
- `replay` validates retained output without rerunning the producer;
- `render` regenerates a derived view atomically;
- `run` performs the declared experiment or workflow;
- `update` replaces a reviewed golden or source-of-truth artifact.

CLI modules adapt typed operations; they do not carry a second implementation of the
algorithm. Use argument-vector subprocess calls, never shell interpolation, for normal
process execution.

## Validation Loops

Choose the smallest loop that protects the change:

```shell
# Discover the available contracts.
uv run --frozen --all-extras --group dev packing-validate --list

# Fast edit loop: pytest plus Python quality, schemas, exact witness, and cheap drift.
uv run --frozen --all-extras --group dev packing-validate --fast

# One named component. --only is repeatable and matches displayed step names.
uv run --frozen --all-extras --group dev packing-validate --only "basin identity"

# Full integration checkpoint used locally and in CI.
uv run --frozen --all-extras --group dev packing-validate

# Rebuild expensive mathematical golden producers while comparing read-only.
uv run --frozen --all-extras --group dev packing-validate --deep

# Merge or unattended-session handoff: deep checks and no skipped surface.
uv run --frozen --all-extras --group dev packing-validate --strict

# Structured result for agents and automation.
uv run --frozen --all-extras --group dev packing-validate --format json
```

The default command runs the complete ordinary surface: fast pytest contracts, Python
and Rust quality, exact and differential mathematics, replay, schemas, generated-view
drift, provenance, campaign invariants, and mutation controls.
Pytest is one layer of that gate, not a replacement for proof scripts and independent
implementations.

The validation command builds `sqsearch` only when a selected step needs it.
Checks run concurrently, but their captured output is replayed in declared order.
`--jobs` controls outer check concurrency; `--inner-jobs` caps each check’s internal
workers.
Strict mode cannot be combined with a partial selection and fails on every skip.

Every validation subprocess has a finite 600-second default deadline.
Override it with `--timeout-seconds SECONDS` or `PACKING_VALIDATE_TIMEOUT_SECONDS`;
values must be positive and finite, and an explicit smaller per-call timeout still wins.
Mutation-control commands retain their 120-second default deadline and may declare a
smaller `timeout_seconds` in `devtools/controls.yaml`. A timeout terminates and reaps
the whole process group, including a child that ignores the first termination signal.
Each command also gets an empty bytecode-cache root, so rapid same-size source mutations
cannot execute a stale control from the preceding snapshot use.

The validation deadline bounds subprocess commands on supported POSIX hosts.
It does not bound pure-Python worker code, the total duration of a step that runs
multiple commands, or detached daemons; Windows process-tree cleanup is not yet
implemented. These limits are why a subprocess timeout is not, by itself, evidence that
D-239 is resolved.

CI executes the same locked full command on Linux and macOS from
[`packing-validation.yml`](../../.github/workflows/packing-validation.yml).
The macOS job also runs the focused deep-golden step directly.
D-203’s temporary expected-failure classifier was removed after the repaired producer
passed on both architectures; the workflow test rejects its return.
Never accept a rebuilt golden to make the probe green, and do not add a second CI-only
implementation of either check.

## Focused Quality Commands

Use direct tools when their output is the point of the edit:

```shell
uv run --frozen --all-extras --group dev pytest -q
uv run --frozen --all-extras --group dev ruff check .
uv run --frozen --all-extras --group dev ruff format --check .
uv run --frozen --all-extras --group dev basedpyright

cargo test --locked --manifest-path sqsearch/Cargo.toml
cargo clippy --locked --release --all-targets --manifest-path sqsearch/Cargo.toml -- -D warnings
cargo fmt --manifest-path sqsearch/Cargo.toml --check
```

Ruff must be clean. BasedPyright runs in standard mode and must report zero diagnostics
across maintained and retained Python.
Its documented exclusions cover dynamically shaped YAML, JSON, and third-party
scientific-library boundaries; this project does not claim strict-mode coverage.
A per-file exception must name the narrow reason beside the configuration; never exempt
a maintained module from a rule family for convenience.
Use modern Python 3.14 syntax, absolute imports, `Path`, precise public-boundary types,
and exception chaining.
Comments explain non-obvious intent, invariants, units, evidence limits, and rejected
alternatives—not a line-by-line translation of the code.

Markdown is owned by Flowmark at repository root.
Durable documentation follows the common documentation guidelines and carries their
footer. Run the repository hook or `make format`; do not introduce a second Markdown
formatter.

## Safe Refactoring

Use red-green-refactor for a behavior change and characterize intended behavior before a
structural move:

1. Identify the public behavior, persisted record, or scientific claim at risk.
2. Run its focused check and capture the clean baseline.
3. Add a failing test for corrected behavior, or a characterization test for correct
   behavior that is not yet protected.
4. Make one bounded change and keep structural movement separate from semantic change.
5. Run focused tests, Ruff, formatting, types, and the relevant exact, property, replay,
   or differential check.
6. Run full validation at the integration checkpoint.
7. Review a golden diff as a behavior change.
   Never regenerate a golden merely to make validation green.

Tests should be deterministic and behavior-focused.
Avoid network access, wall-clock assertions, uncontrolled randomness,
implementation-detail mocks, and tests that only prove a mock was called.
Include boundary values and failure paths.
A bug fix gets a test that fails for the old defect.
A new guard gets a negative control showing that the named corruption reaches it.

## Hashes and Repository-Owned Artifacts

Git is the integrity boundary for repository-owned sources, golden files, and retained
results. Compare their complete content or regenerate and compare their semantic model;
do not add SHA-256 fields or checksum controls for files committed beside the checker.

A cryptographic checksum is justified only when it is compared with an independently
supplied value across a real trust boundary.
The nearby code or documentation must name that boundary and the failure the comparison
detects. Compact content identities used for deduplication, append-only event ids, or
cache correctness are not integrity claims and must name that separate function.

Pytest collection is explicit in `pyproject.toml`; `tests/conftest.py` fails if the
configured test directory disappears.
Domain programs are named by what they check, not with `_test.py`, so pytest cannot
silently collect or omit them by accident.

## Durable State and Compatibility

Repository-owned callers are migrated together.
Do not retain an alias, wrapper, old module path, or compatibility branch without a
named external consumer.
There are no known external `sqpack` consumers, server APIs, plugin APIs, or databases
at this time.

Campaign, basin-event, atlas, and certificate formats are real persisted contracts.
Version them, reject unsupported versions clearly, and migrate only when retained older
data must remain readable.
Never reinterpret historical records in place.

Write generated views and complete artifacts through `strif.atomic_output_file` so a
crash cannot expose a partial replacement.
Validate before promotion.
Append-only campaign journals are the deliberate exception: each line is independently
validated, and a partial archive is retained as recovery evidence rather than presented
as a complete result.

Generated files name their producer.
Use:

```shell
uv run --frozen packing-ledger check
uv run --frozen packing-ledger render
uv run --frozen python -m devtools.render_defects --check
uv run --frozen python -m devtools.render_research_tables --check
```

## Shell Policy

There are currently no tracked Bash or shell entry points in the packing project, and
the architecture tests guard that state.
Python is the default when a command parses structured data, owns durable state,
branches meaningfully, coordinates subprocesses, handles timeouts, or needs focused
tests. A tiny transparent launcher may be justified, but adding one requires an explicit
architecture-test exception and an explanation of why direct configuration or Python is
less clear.

## Performance Work

Optimize E2 and E3 code only against a representative research loop.
Record the command, inputs, Python and engine revisions, worker settings, warm or cold
state, and the metric being improved.
Profile first; preserve the behavioral and scientific contract; compare before and after
under the same regime.
One-off E1 code need not be optimized unless it materially blocks the experiment that
owns it.

Gate wall time, solver throughput, pair tests, and time-to-retained-result are useful
metrics. Line count, abstraction count, and test count are not performance measures.

## Governing Guidelines

This guide applies the repository guidelines rather than copying them.
Load the current text on demand with `tbd guidelines <name>`; generated `.tbd/docs`
copies are local working state and are not durable link targets.
The applicable names are:

- `general-eng-agent-principles` and `general-coding-rules`;
- `general-tdd-guidelines` and `general-testing-rules`;
- `python-rules`, `python-modern-guidelines`, and `python-cli-patterns`;
- `error-handling-rules` and `backward-compatibility-rules`;
- `golden-testing-guidelines`; and
- `common-doc-guidelines`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
