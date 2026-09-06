# Change-Scoped Exhaustive Validation

## Verified Runs

GitHub run metadata, job timestamps, and the exhaustive job logs independently confirm
these measurements. All three runs were successful `pull_request` executions of the
deferred workflow, with 55 exhaustive cases passing.
Different deselection counts reflect different source trees, not evidence that different
exhaustive cases ran.
The historical logs do not supply a case identity manifest.

| PR and run | Verified head | Exhaustive job wall | Pytest wall | Deselected |
| --- | --- | --- | --- | --- |
| [94 / 34046149472](https://github.com/jlevy/squares/actions/runs/34046149472) | `994e58426b40603a498354e3615adb5604f034ab` | 27m03s | 1605.11s, or 26m45.11s | 2307 |
| [95 / 34046947635](https://github.com/jlevy/squares/actions/runs/34046947635) | `72c0df47eb10060c57144e9cc23cc435239834a0` | 19m59s | 1177.33s, or 19m37.33s | 2303 |
| [96 / 34046191070](https://github.com/jlevy/squares/actions/runs/34046191070) | `d6d4180d027a10516128ebf1a1d4e6d19c41f77a` | 22m13s | 1315.76s, or 21m55.76s | 2314 |

The linked hosted runs retain the original job logs.
The user’s classification of PR94 as 14 directly relevant, 16 more broadly relevant, and
25 unrelated cases, and PR95/96 as having no directly relevant exhaustive cases, remains
attributed to the user.
This review verified timing and heads, not those classifications.
File-level static reachability alone cannot prove a case irrelevant.

PR94, PR96, and PR95 merged on 2026-09-06, in that order, producing main
`edccf294be375d209c431f4fb8f2eb892f22fd56`. This block integrated that main revision
after its frozen profiling run on the earlier base.
The three exhaustive jobs total 69m15s of job runner time, not elapsed review time or
measured CPU time.

## PR95: Focused Contract Evidence

The
[original senior review](https://github.com/jlevy/squares/pull/95#issuecomment-5560540217)
examined `566f0c72746a49602775936d83c5b4c5f4209605`. Required CI was green, but that
review explicitly records deep/deferred/exhaustive checks as skipped.
The 19m59s exhaustive run above belongs to repaired head `72c0df47`. These sources do
not establish that the original defects survived a completed exhaustive run.

The review does establish two gaps that mathematical certificate coverage would not
address:

- **CPU attribution:** a synchronized fixture-child control reported 6.44 seconds of
  setup wall, 0.00 seconds of call wall, and 6.23 CPU seconds charged to the call when
  it reaped earlier work.
  The new gate falsely rejected that cheap call.
  Passing certificate decisions cannot establish ownership of process/reaped-child CPU.
- **Worker boundary:** `build_cases([entry], 2)` was clamped to one worker and ran
  serially. Its test passed even if the worker payload lost the resolved retained-source
  path, because the current process still saw the monkeypatch.
  The required regression needs at least two entries, a real process boundary, the
  substituted missing-source refusal, and a mutation showing removal of the explicit
  path payload is detected.

The
[author’s response](https://github.com/jlevy/squares/pull/95#issuecomment-5560862348)
reports both repairs in `08087a18` and `72c0df47`: CPU counters became diagnostic only,
a synchronized cross-phase regression protected call-wall coverage, and the repaired
retained-source test crossed the real worker boundary and failed when its explicit
source-path payload was dropped.
The response reports 115 focused tests and final required/deep CI success.
This bounded audit verified the primary review and response; it did not independently
rerun those reproductions or mutations.

Upstream validation-plan guidance should require focused evidence for each changed
contract: identify the triggering condition, test the actual execution boundary, and
show that the regression fails when the repair is absent where practical.
State which broader suites passed separately.
A full-suite green result adds integration evidence; it does not replace the regression
that distinguishes correct and incorrect behavior for the changed contract.
Coverage-family receipts must carry those focused obligations alongside broad
mathematical coverage, so an unaffected proof family cannot discharge a new
CPU-attribution or worker-serialization obligation.

## Existing Mechanisms and Gaps

`packing/devtools/reachable_tests.py` already computes a conservative test-file import
closure, catches textual references and dynamic import/repository walkers, and runs
selected non-exhaustive tests for `--push`. Its `--run` explicitly excludes
`exhaustive_exact`; it cannot currently choose or attest exhaustive coverage.
`Step.touches` and `select_for_paths` select whole gate steps, not cases inside the
exhaustive step. Unattributed steps always run; a path no attributed step claims selects
the whole offered gate.
The exhaustive step is deliberately unattributed.

Before either mechanism can authorize reuse, fix these concrete limits:

- `SUITE_WIDE` contains `pyproject.toml`, `uv.lock`, `tests/conftest.py`, and
  `.python-version`, while `changed_paths` returns repository-relative `packing/...`
  names. `test_suite_configuration_selects_everything` tests the incorrect root
  `pyproject.toml` spelling.
  Actual lock/config paths can miss the intended fallback.
- The selector inventories only test files immediately under `packing/tests`. Nested
  future test directories need recursive discovery or a refusal guard.
- Unknown non-Python inputs select textual consumers and walkers; they do not
  automatically select everything.
  A data file opened through composed paths can be missed.
  Import reachability is not a data dependency graph.
- `Step.touches` is a manually maintained attribution, not proof of complete inputs.
  An apparently mapped path can still lack a relevant dependency edge.
  Dynamic code, environment variables, executable versions, and external inputs remain
  outside AST import analysis.
- Existing run receipts record what ran and source provenance.
  They do not attest a complete family dependency closure, and a matching selected-test
  hash does not prove an imported production module or data file was unchanged.

`changed_paths` already handles merge-base comparison, both sides of renames through
`--no-renames`, NUL-delimited paths, staged/unstaged edits, and untracked files.
Preserve those behaviors rather than adding another Git diff implementation.

## Bounded Implementation Design

Extend the existing selector to emit an explained exhaustive-family plan.
Keep the ordinary fast CI surface complete.
Initially run the planner in reporting mode beside the full exhaustive lane so missed or
unexpectedly broad dependencies are reviewable before any work is omitted.

A family starts as the exhaustive cases in one test module.
Retain separate contracts for integer certificate acceptance, witness admissibility,
interval acceptance, standalone verifier variants, the combined decision consumer, n5
symbolic identities, and n40 replay.
Parametrized cases remain explicit in the collected node manifest.
A family can be grouped more coarsely whenever complete dependencies are uncertain.

Use the import closure already built by `reachable_tests.py`, augmented with explicit
repository-relative data, fixture, subprocess, and document inputs for each family.
Put the small family metadata in that maintained module or adjacent existing selector
configuration; do not introduce a competing workflow engine or a second test registry.
Make the exhaustive-marker census in `test_module_boundaries.py` verify that collected
exhaustive nodes belong to exactly one declared family.
Unclassified nodes or inputs, parse failures, configuration changes, unresolved dynamic
loading, and selector/runner changes invalidate narrowing and require the complete lane.
A known empty impacted set must be distinct from an unknown selection.

For each family, the plan records `run`, `reuse`, or `unresolved`, with paths and
reasons. The required checkpoint succeeds only when every current family is covered by
either a fresh successful execution or validated prior evidence.
It must never equate a skipped job with an unchanged family.
Continue periodic complete runs as an independent audit of the dependency model; those
runs do not excuse missing dependencies at a merge.

Reuse the gate’s existing run ID, start/end receipts, raw logs, and JUnit.
Add a family-level coverage record containing the family/node manifest digest, full
declared input content hashes, base and tested tree identity, selector/runner version
hashes, Python/dependency lock/toolchain identities, relevant environment and worker
settings, command, successful result, and artifact provenance.
Hash added/deleted paths and exact bytes; unknown untracked inputs force execution.
Recompute the input manifest at the end and reject source movement during the run.
Failed, cancelled, timed-out, unmatched, or missing-JUnit executions provide no reusable
coverage.

Invalidate reuse on any changed input, changed family membership, changed selector or
fixture semantics, runtime/lockfile change, incompatible environment, missing artifact,
or untrusted provenance.
On a new merge base, compare the current family input manifest against the actual tested
manifest; PR-head success alone does not cover the merged result.
A reverted change can reuse evidence only if the complete content manifest and execution
contract match again.
Artifacts produced by untrusted PR code must not become trusted attestations merely
because they contain a success string; establish reuse through the trusted workflow and
verified run/source identity.
Initially require clean checkouts for reusable evidence; local dirty runs remain
diagnostic evidence until exact dirty and untracked input handling is validated.

## Concrete Changes and Fixtures

| Owner surface | Required change and regression fixtures |
| --- | --- |
| `packing/devtools/reachable_tests.py` | Correct repository-relative suite-wide paths; add explained family planning using the current graph; represent unknown and known-empty distinctly; emit machine-readable reasons and manifests. |
| `packing/tests/test_reachable_tests.py` | Real `packing/pyproject.toml`, `packing/uv.lock`, nested conftest, indirect imports, relative package imports, subprocess file inputs, composed data paths, unknown non-Python paths, and nested test discovery. |
| `packing/tests/test_change_scoped_selection.py` | Preserve merge-base, rename source/destination, deleted inputs, spaces/non-ASCII paths, staged/unstaged/untracked changes; prove a newly merged upstream input invalidates family reuse. |
| `packing/tests/test_module_boundaries.py` | Exactly-once family membership for every collected exhaustive node, including parametrization; adding an unclassified case fails the census instead of silently omitting it. |
| `packing/src/sqpack/cli/validate.py` and `packing/tests/test_validation_cli.py` | Join selection reasons, executed coverage, and reused coverage to existing receipts; reject missing/mismatched receipts, failed/cancelled/time-out runs, stale manifests, mid-run changes, duplicate or missing nodes, and unknown selection. Keep full and strict mode semantics explicit. |
| Existing workflow contract tests and `.github/workflows/deep-gate.yml` | Required context checks the complete family coverage union; fixtures for known-empty changes with valid coverage, missing prior artifact, changed base, fork provenance, cancellation, and planner failure. Start with report-only behavior. |
| `packing/benchmarks/validation_report.py` and its tests | Validate and render family receipts alongside current timing evidence; expose missing or reused coverage separately. Reuse the parser and receipt checks rather than create another report format. |
| `development.md` | Define fresh versus reused coverage, invalidation, full audit cadence, and the exact required-context rule. Correct the selector docstring’s stale claim that every CI push runs the full gate. Keep tiers and behavioral lanes distinct. |
| `docs/tbd/shortcuts/create-or-update-pr-with-validation-plan.md` and `create-or-update-pr-simple.md` | Require a reviewable selection explanation and links to executed/reused family evidence when claiming checkpoint completion. Keep the full checkpoint entry point until the new coverage contract is implemented and validated. |
| Upstream tbd shortcut sources | Propose the same distinction to `internal:shortcuts/standard/create-or-update-pr-with-validation-plan.md` and `internal:shortcuts/standard/create-or-update-pr-simple.md`, the exact sources recorded in `.tbd/doc-forks/forks.yml`. Update upstream, then reconcile forks; do not edit generated skill files or silently rewrite fork base snapshots. |

The smallest first implementation is path-normalization regression coverage plus
report-only family planning.
Coverage reuse follows after that output demonstrates complete input attribution on the
PR94/95/96 examples and deliberate invalidation fixtures.
The design is a follow-up within the W5 plan.
Automatic family selection and evidence reuse are not implemented by the first
instrumentation and optimization slice.

## Confirmed Configuration Boundary Regression

A public `select_tests` probe against the actual checkout selected only 27 of 163 test
files for `packing/pyproject.toml`, 24 for `packing/uv.lock`, 23 for
`packing/tests/conftest.py`, and 25 for `packing/.python-version`. All four returned
`everything=False`. The unknown Python path `mystery/unmapped.py` correctly returned
`everything=True`; fallback does not mask the configuration mismatch.

The first implementation slice adds the four repository-relative paths while preserving
existing root-configuration fallback paths, and replaces the misleading fixture with
parameterized actual paths.
The public-interface regression produced four failures and three passes against
unchanged source in 1.38 seconds.
Loading the candidate into an isolated process produced seven passes in 0.01 seconds,
including the unknown-Python fallback.
This correction precedes any family-selection or coverage-reuse rollout; final
integration checks are recorded with the implementation review.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
