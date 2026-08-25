---
title: Packing Engineering Maturity and Research-Loop Scalability
description: Implemented module segregation, Python 3.14 baseline, refactor harness, validation CLI, CI, and engineering guidance
author: Codex and project maintainers
date: 2026-08-24
status: implemented
---
# Packing Engineering Maturity and Research-Loop Scalability

**Status:** Implemented and merged through PR #23.

**Workflow entry:** `general-improvement`

**Primary focus:** Efficiency — Infrastructure

The objective is to lower repeated orientation and maintenance cost without changing the
mathematical behavior of exp-033 through exp-036. Any such semantic change is the kill
condition for this tranche; the fallback is to preserve the campaign result and isolate
the engineering change for separate diagnosis.

## Outcome

The packing project now distinguishes maintained foundations, reusable research-loop
code, retained case-specific programs, developer tooling, tests, and benchmarks in its
filesystem and import graph.
Python 3.14 is the only supported runtime.
A typed Python validation command replaces the ambiguous shell gate, the remaining shell
programs have Python command surfaces, full validation runs in CI, and
[`development.md`](../../../../development.md) owns the operating rules.

This was executed as one bounded engineering tranche, not left as a future roadmap.
It changes organization and infrastructure without changing mathematical claims,
experiment outcomes, evidence tiers, or search policy.

The governing decision is **assurance proportional to reuse and consequence**. Shared
mechanisms and trust boundaries receive stable contracts and strong tests.
Code retained for one `n`, source, theorem, hypothesis, or checkpoint remains explicit
E1 case code and is not forced through a speculative abstraction.

## Starting Evidence

The pre-change project passed its complete thirty-step shell gate.
That baseline included exact and differential checks, Rust validation, replay, schemas,
generated views, provenance, and 38 private-snapshot mutation controls.
It did not provide a clear fast Python contract surface, and the layout mixed four
different maturity levels:

- maintained arithmetic, verification, quench, identity, and atlas code under one flat
  `sqpack/` directory;
- campaign implementation inside the campaign-state directory;
- case-specific programs at project root or under generic `tools/` names;
- a 745-line `test.sh` that owned concurrency, selection, error handling, and structured
  validation policy in Bash.

Two command defects made the orientation cost concrete: `campaign/ledger.py --help`
regenerated the ledger, and `run_quench.py --help` started a research run.
The latter became a failing test before its command boundary was corrected.

## Implemented Layout and Maturity Map

| Location | Class | Responsibility and current contents |
| --- | --- | --- |
| `src/sqpack/field.py`, `verify.py` | E3 | Exact arithmetic, sign certification, and independent validity decisions. These are reusable correctness boundaries. |
| `src/sqpack/research/` | E2 | Reusable quench, canonical identity, atlas, and closed-form recognition mechanisms. They carry no named-case policy. |
| `src/sqpack/campaign/` | E3 | Campaign state machine, schema-wide invariants, persistence, and generated ledger. Durable state remains under `campaign/`. |
| `src/sqpack/cli/` | E3 | Validation orchestration and stable installed command boundaries. |
| `cases/trump11/` | E1 | Exact Trump packing, verifier limits, field derivation, independent LP reconstruction, tangent cones, and f64 seed export. |
| `cases/gobel10/`, `n5/`, `small_n/`, `stromquist/`, `kingbird29/` | E1 | Retained checks tied to a named case, source, theorem, or value of `n`. |
| `cases/campaign_smoke/` | E1 | H-002 quench, basin-event, baseline, and basin-entry experiment programs whose policy is campaign-specific. |
| `devtools/` | Developer-only | Fifteen checkers, renderers, schema tools, and the isolated mutation-control harness. No runtime package imports them. |
| `benchmarks/` | Measurement | Exact-verification performance probe, deliberately separate from pass/fail tests. |
| `tests/` | Refactor safety | Fast behavioral, CLI, arithmetic/verifier, validation-command, and architecture contracts. |
| `sqsearch/` | Maintained Rust | Tier-1 screening annealer, still independently checked against Python validity. |

The architecture test enforces these dependency rules:

1. top-level foundations do not import research, campaign, cases, or devtools;
2. research code does not import campaign, cases, or devtools;
3. campaign and CLI code do not import case or developer implementations;
4. no Python implementation returns to the old project root, `tools/`, `campaign/`, or
   flat `sqpack/` locations;
5. no Bash or shell entry point is added without changing the explicit architecture
   contract.

The two largest ambiguous programs were deliberately *not* promoted.
The former `run_quench.py` encodes H-002 and Trump-specific angle-class policy; the
former `basin_census.py` encodes a campaign event contract and named source starts.
Both now live in `cases/campaign_smoke/`. Calling them reusable because they are large
would hide their assumptions and make future agents trust the wrong layer.

## Runtime and Quality Baseline

Python support is uniformly `>=3.14,<3.15`:

- `.python-version` selects 3.14;
- `pyproject.toml` and `uv.lock` contain only the 3.14 policy;
- Ruff targets `py314` with a broad high-floor rule set;
- BasedPyright targets 3.14 and covers `src`, `cases`, `devtools`, `benchmarks`, and
  `tests`;
- CI installs 3.14 through the official uv action;
- documentation uses the same locked commands.

The project uses a `src/` package layout, ships `py.typed`, and installs three clear
commands:

- `packing-validate` for read-only project assurance;
- `packing-campaign` for preregistered round state transitions;
- `packing-ledger check|render` for campaign invariants and the generated view.

Repository-owned imports, commands, defect links, controls, and active documentation
were migrated together.
No old import wrappers or CLI shims were retained because no external consumer was
identified.

Ruff and BasedPyright both run at zero warnings.
Per-file exceptions are narrow and documented for published mathematical notation, a
benchmark that intentionally reaches internals, and Markdown renderers whose
append-shaped code is clearer than a comprehension.

## Refactor-Safety Harness

Pytest is now an explicit fast layer rather than an accidental collector.
Its configuration fixes `testpaths` and file naming, enables strict config and markers,
and fails with an actionable message if the configured test directory disappears.
A mutation control proves that missing collection is red.

The initial behavior contracts cover:

- exact arithmetic, exact and float verifier boundaries, and the closed-form helper;
- module placement and one-way imports;
- command help being read-only for campaign and case programs;
- validation selection, worker errors, strict-mode constraints, and tier discovery;
- the full mutation-control suite, including the validation command itself.

The validation command retains the independent proof scripts, property checks, replay,
schemas, goldens, differential checks, and Rust checks instead of duplicating them as
pytest tests. Its thirty-one displayed steps are the authoritative integration surface.

## Validation Command

`packing-validate` replaces `test.sh` with one tested Python implementation.
It offers:

- `--list` for exact step names and fast/full/engine tiers;
- `--fast` for the edit loop;
- repeatable `--only TEXT` for focused contracts;
- ordinary full validation for commits and CI;
- `--deep` for expensive golden reconstruction;
- `--strict` for deep, no-skip handoffs;
- validated `--jobs` and `--inner-jobs` controls;
- stable ordered human output despite concurrent execution;
- `--format json` for agents and automation;
- explicit Python 3.14 enforcement and actionable exit statuses.

The command is read-only.
Deep golden validation rebuilds and compares without accepting a new golden.
Render and update operations remain separate commands.
Engine compilation happens only when a selected step needs it.

Negative controls mutate private source snapshots, never the working tree.
One repair made during this work prevents `uv run` inside a snapshot from reinstalling
the shared editable environment against a temporary path: snapshot commands use
`UV_NO_SYNC=1` and an explicit `PYTHONPATH`. Every control has a finite deadline.
A timeout terminates and reaps the complete process group, including a child that
ignores the first termination signal, and a focused test exercises that failure path.
The final one-worker integration run also exposed timestamp-based Python bytecode reuse
between two same-size campaign-runner mutations.
Every control command now receives a fresh cache root, so it necessarily executes the
source mutation it claims to test.

## CLI, Persistence, and Shell Cleanup

The old ledger accepted `--help` as a write request.
It now requires the explicit verbs `check` and `render`, parses arguments before loading
campaign state, and renders through an atomic replacement.
The campaign command exposes its real name in help and generated artifacts.
Stable campaign artifact and report replacements are atomic.

The three remaining application-like shell programs were replaced:

| Removed | Python replacement |
| --- | --- |
| `run_baseline.sh` | `python -m cases.campaign_smoke.baseline_sweep` |
| `run_basin_entry.sh` | `python -m cases.campaign_smoke.basin_entry_experiment` |
| `frankensim-probe/run.sh` | `python frankensim-probe/run_probe.py` |

The baseline and basin-entry commands have typed arguments, actionable engine errors,
self-test guards, subprocess argument vectors, and atomic result promotion.
The FrankenSim probe refuses to overwrite an existing example, restores the external
manifest in `finally`, and removes only files it created.
The packing tree now has no tracked shell entry points.

Renderers for the ledger, defect view, and research tables write atomically and name
their current producer.
Campaign JSONL remains intentionally append-oriented: each line is validated before
retention, and a partial archive is recovery evidence rather than a complete artifact.

## CI and Documentation

`.github/workflows/packing-validation.yml` runs for packing and experiment-loop changes.
It pins checkout and the official uv setup action by commit, installs Python 3.14,
synchronizes the frozen development environment, and runs the ordinary full validation
command on Linux and macOS. The macOS job also reconstructs the expensive numerical
golden through the same validation command as a visible non-blocking diagnostic.
It is not yet a merge guard because the reproduced n=4 partition drift and n=10
post-check rejection belong to `think-sk15`, `think-lwao`, and `think-u97a`; this change
does not accept their rebuilt output.
CI does not carry a separate test recipe.

The first clean remote run and its workflow contract test found three integration
defects (D-226–D-228). Both jobs now fetch complete history because the full gate
verifies 36 historical engine commits, and the uv cache dependency glob is correctly
relative to the action’s packing working directory.
The workflow parser also treats YAML 1.1’s boolean interpretation of `on` explicitly.
A pytest architecture contract parses both jobs and enforces those settings.

The final rebase onto PR #22’s workflow-entry change retained the new resumable campaign
session contract and migrated its commands to the maturity-separated module paths.
It also expanded the private-snapshot suite from 38 baseline controls to 58 controls on
the merged tree; all fire against the rebased tree.

[`development.md`](../../../../development.md) now documents setup, E0–E3 placement,
dependency flow, commands, CLI semantics, quality tools, red-green-refactor practice,
goldens, compatibility, atomic output, shell policy, performance work, and links to the
repository `tbd` guidelines.
The packing README contains the actual module map, and
[`conventions.md`](../../../../conventions.md) names the new gate as the authoritative
checking surface.

## Compatibility Decision

- Internal module and command paths: coordinated migration; no compatibility layer.
- External Python consumers: none identified.
- Server, plugin, database, and persisted client APIs: not applicable.
- Campaign, atlas, event, and certificate formats are repository-owned and fail-fast.
  Producers, retained records, and replay checks migrate atomically in this work; there
  is no external persisted-client compatibility promise.
- Exact-record dependencies are declared by path and replay their semantic predecessors
  directly. Exp-033 through exp-036 were replayed in order after the golden producer
  migration. Their determinations are unchanged; redundant source-checksum fields and
  controls were removed because Git already owns internal artifact integrity.
- Historical experiment prose: retained when the old filename is part of the historical
  record; active entry points and reproducibility commands use the new paths.

## Acceptance Evidence

The change is complete when all of the following are green on the final tree:

- [x] Python implementation is segregated and the architecture contracts pass.
- [x] Python 3.14 is the only supported runtime in metadata, lock, tools, CI, and docs.
- [x] Ruff and BasedPyright report zero warnings.
- [x] Fast pytest contracts and the missing-collection negative control pass.
- [x] `packing-validate` replaces `test.sh` and its own failure paths are tested.
- [x] The 58 mutation controls target current paths and fire in isolated snapshots.
- [x] All application-like Bash entry points have Python replacements.
- [x] Campaign and generated-view writes use explicit atomic boundaries where a complete
  replacement is the contract.
- [x] CI runs the locked full validation command on Python 3.14.
- [x] README, synopsis, campaign record, generated views, and code references agree with
  the new layout.
- [x] The post-merge readiness review passed all 31 local `packing-validate` steps in
  113.31 seconds with 36 pytest contracts, 58 mutation controls, and the reconciled
  239-defect record.
- [x] Stacked PR checks are green on implementation commit `8f53f8e`: Linux validation
  passed in 2 minutes 48 seconds and macOS portability passed in 5 minutes 10 seconds.

All implementation and integration acceptance evidence is now recorded.

## Bead Reconciliation

`think-9a7v` owns this implementation.
The focused beads map directly to completed surfaces:

| Bead | Implemented surface |
| --- | --- |
| `think-xdyv` | Inventory and maturity classification |
| `think-jc1a` | Python 3.14-only runtime and tool alignment |
| `think-k1jj` | Pytest and characterization harness |
| `think-8waf`, `think-1eij` | Shared, research, campaign, and case-module segregation |
| `think-5u59`, `think-dbn6`, `think-9rzc` | CLI contracts, Python validation command, and shell migration |
| `think-l03z` | High lint and type floor |
| `think-hf1u` | Engineering guide and orientation map |
| `think-cns0` | Bounded process-group cleanup and isolated bytecode for mutation controls |
| `think-lrsk` | Full Linux and macOS CI, plus a second-architecture deep-golden diagnostic |

Existing numerical, campaign-lifecycle, and performance beads remain with the research
or review specs that own their scientific acceptance criteria.
They were reconciled, not absorbed into a structural cleanup that does not change their
algorithms or claims.

## References

- [Development guide](../../../../development.md)
- [Packing README](../../../../README.md)
- [Packing synopsis](../../../../SYNOPSIS.md)
- [Packing conventions](../../../../conventions.md)
- [Campaign runbook](../../../../campaign/README.md)
- [Minimal Packing Toolkit](plan-2026-08-22-minimal-packing-toolkit.md)
- `think-9a7v` — engineering-maturity epic

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
