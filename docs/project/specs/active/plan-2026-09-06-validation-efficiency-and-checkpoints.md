---
title: Validation Efficiency and Checkpoints
description: W5 improvement block for immediate feedback, justified checkpoint cost, and consistent validation names
author: Codex, with the repository owner
date: 2026-09-06
status: active
---
# Feature: Validation Efficiency and Checkpoints

**Date:** 2026-09-06

**Status:** Active; investigation and implementation authorized by the repository owner.

**Workflow entry:** W5 `efficiency-loop`. **Tracking:** `think-rwte`.

## Overview

Reduce the cost of obtaining trustworthy validation evidence.
Ordinary commits need immediate feedback; the final pre-merge checkpoint can run
expensive checks, but each check must justify both its independent evidence and its
implementation cost.
Twenty-seven minutes is an observed checkpoint duration, not a necessary lower bound.
This block reviews the path from local editing through CI, final review, merge, and
publication, implements measured improvements, and reconciles documentation and naming.

The retained
[exhaustive review](../../reviews/review-2026-09-06-validation-exhaustive-cost.md) and
[slow/control review](../../reviews/review-2026-09-06-validation-slow-and-controls-cost.md)
record the independent audit.
The
[engineering campaign](../../../../packing/benchmarks/validation-efficiency/README.md)
owns preregistered comparisons, raw timing receipts, and generated results.

## Goals

- Preserve distinct contracts, boundary cases, negative controls, exact decisions, and
  useful failure localization while reducing repeated work.
- Keep cheap coverage on every commit.
  Preserve the PR target of two to two and a half minutes, with three minutes triggering
  investigation; improve below it when justified.
- Separate immediate feedback from final pre-merge evidence, identifying the source and
  base each checkpoint checked.
  Changes that invalidate that evidence require a new check.
- Attribute expensive work to tests, setup, subprocesses, and algorithms; distinguish
  elapsed time from summed worker time.
- Align names, coverage descriptions, budgets, and documentation links with executable
  definitions and dated measurements.

## Non-Goals

Scientific bounds, witnesses, tolerances, and acceptance criteria remain unchanged.
Expense alone does not justify dropping a test.
Cached results must not be described as fresh execution, and skipped checks must not
become passes. Incomplete CPU accounting cannot drive thresholds.
Repository ownership and branch-protection settings are outside implementation scope;
their enforcement implications must remain explicit.

## Background and Baseline

The starting source is main commit `6b21d14b64c19003d597ed3c993c051b64336b0c`. These
observations across named runs are context, not a controlled speedup experiment.

| Surface | Observed wall time | Evidence |
| --- | --- | --- |
| PR fast surface | 2m22s overall; four Linux jobs 1m58s–2m15s including setup | [PR run](https://github.com/jlevy/squares/actions/runs/34023121156) |
| Full main checkpoint | 27m33s; integration 24m19s and exhaustive 27m28s concurrently | [Main run](https://github.com/jlevy/squares/actions/runs/34025346801) |
| Deferred checkpoint | 27m01s; deferred checks 12m32s and exhaustive 26m53s concurrently | [Deferred checkpoint run](https://github.com/jlevy/squares/actions/runs/34028227026) |
| Publication | 54s; build 36s and deployment 10s | [Pages run](https://github.com/jlevy/squares/actions/runs/34025346806) |

The complete ordinary gate has 66 steps; 62 run on PRs as 48 checks, nine geometry
checks, one quick-test lane, and four sweeps.
The remainder is slow tests, exhaustive exact tests, negative controls, and the n=40
rigidity replay. That baseline main run passed 2,197 quick tests, 95 slow tests, 55
exhaustive tests, and 163 mutation controls.

The slow lane took 1,220.91 seconds, negative controls 566.10 seconds, the n=40 replay
219.00 seconds, and exhaustive tests 1,626.32 seconds.
Exhaustive logs lack individual test durations.
Both the exhaustive and integration jobs need attention: optimizing only one leaves the
other on the critical path.

PRs [94](https://github.com/jlevy/squares/pull/94),
[95](https://github.com/jlevy/squares/pull/95), and
[96](https://github.com/jlevy/squares/pull/96) subsequently merged into main
`edccf294be375d209c431f4fb8f2eb892f22fd56`, which this block integrates.
PR95 owns the engine-build cache, worker-boundary repairs, and repeated CI baseline
measurements.
PR94 owns the early refusal that avoids an expensive degree-20 probe in one
negative control. Keep those improvements separately attributable.

The
[change-scoped coverage review](../../reviews/review-2026-09-06-change-scoped-exhaustive-validation.md)
verifies the supplied PR examples: 27m03s, 19m59s, and 22m13s for three complete
exhaustive jobs, totalling 69m15s of runner time.
Their relevance classifications remain attributed to the other agent’s report.
The PR95 review illustrates why mathematical coverage cannot replace a real
worker-boundary or CPU-attribution regression.
The original PR95 findings preceded its final exhaustive run; a passing exhaustive suite
on the buggy revision is not established by that chronology.

## Design

### Review value before changing coverage

For expensive checks, record the independent contract, real failures or mutations
caught, invalidating inputs, duplicate computation, equivalent cheaper oracles, current
placement, and disposition.
A lack of recent failures alone does not make a verifier dispensable.
Prefer shared immutable setup, bounded parallelism, algorithm improvements, and avoiding
identical computation.
Collapse duplicate execution only when retained evidence covers its contract and a
cheaper test preserves any distinct interface behavior.

Initial review candidates are exhaustive duration reporting and bounded scheduling;
per-axis mapping reuse in the float-oracle regression; local row-jet reuse in the
minus-W bridge; duplicate n=40 replay; and per-control timing in the existing mutation
harness. These are candidates, not accepted speedups.
In particular, certificate workers currently ignore `PACK_JOBS`, so adding xdist alone
can oversubscribe the runner.

### Measurement and acceptance

Reuse the validation CLI, pytest duration reports, and existing profiling tools before
adding an instrument.
Missing instruments become maintained project code with a known-failure check.
Capture source identity, dirty state, exact command, selected cases, interpreter, host,
worker limits, cache regime, status, and raw durations at run time.
Keep records under `packing/` and generate the report from them.

Every long-running test, control, benchmark, and validation phase records detailed
timings. Preserve per-unit durations, setup and execution separately, queue time where
available, worker configuration, source identity, completion status, and partial results
after failures or cancellations.
An aggregate wall time alone is insufficient.
Emit a readable slowest-work summary and retain machine-readable records with the CI
artifacts or experiment receipt.
Record timing coverage so missing units cannot look measured.

Register each candidate’s criterion before timing it.
Exploratory comparisons use at least three runs per condition, interleaved order,
median, and range.
Accept a performance candidate when ranges do not overlap, median time
improves by at least 15 percent, independent correctness guards pass, and its complexity
is justified. Smaller or noisy changes remain unresolved or rejected under this
criterion. Confirmatory percentage claims require the experiment-loop’s paired protocol.

Parallel candidates must preserve selection and failure propagation, bound inner and
outer workers, and increase summed worker time by no more than 25 percent.
A different compute tradeoff needs a separately registered criterion before measurement.
One complete CI run verifies integration but does not establish a statistical speedup.

Retain the exploration, candidate registry, raw runs, all experiment outcomes, code
entry points, and generated report.
Use an engineering benchmark record rather than inventing scientific hypothesis ids.
Link these records from this spec as they are created.

### Feedback and checkpoint placement

Keep records, edit, and change-reachable push checks usable independently of long
checkpoint work. Ordinary PR feedback retains cheap coverage.
Run the complete checkpoint when the PR is ready for final review and after changes
invalidate its evidence; identify the checked source, merge/base identity, and selected
surfaces.

Review repeated main and daily work for sound reuse without treating an incomplete
`touches` map as a safe skip map.
Reuse must account for source, data, toolchain, dependencies, configuration, and any
git-history, bead-state, time, or network inputs.
Missing or mismatched evidence falls back to execution.
Preserve main and daily backstops until a replacement demonstrates equivalent coverage
and failure behavior.

### Change-scoped exhaustive coverage and evidence reuse

The next slice extends the existing change selector instead of adding a competing
workflow engine. Its
[concrete design and fixture matrix](../../reviews/review-2026-09-06-change-scoped-exhaustive-validation.md)
are part of this spec.
Preserve the complete cheap PR surface.
First correct repository-relative configuration invalidation, then run an explained
family planner alongside complete exhaustive execution without omitting work.

Inventory every collected exhaustive node exactly once.
Declare each family’s imported code, fixtures, retained data, subprocess inputs,
relevant documents, runtime, and configuration.
Static imports alone do not establish the complete dependency graph.
Unknown inputs, unclassified cases, parser failures, and changes to the selector or
shared configuration require complete coverage.
Distinguish a known empty impacted set from an unknown selection.

After the planner passes deliberate invalidation tests and review of the PR94–96 cases,
add reusable family receipts to the existing timing evidence.
Every required family must have a fresh successful run or validated prior evidence with
matching complete input and execution manifests.
Recheck those inputs at completion, compare against the actual merged tree, and reject
missing, failed, cancelled, partial, stale, or untrusted artifacts.
A skipped job supplies no coverage.
Keep periodic complete audits.

Changed contracts also require focused regression evidence at their actual execution
boundary. An unaffected mathematical family cannot discharge a newly changed worker or
CPU-accounting contract.
Report why each family ran or was reused and retain links to both kinds of evidence.
The first implementation slice does not enable automatic reuse or change the deep-label
triggers; the current full checkpoint remains the entry point until the coverage union
is implemented and validated.

### Naming and documentation ownership

| Term | Meaning and existing interface |
| --- | --- |
| PR fast surface | `--fast`, partitioned into `--checks`, `--geometry`, `--suite`, and `--sweeps` |
| Full checkpoint | All ordinary steps, selected by the default command |
| Deferred checkpoint | Four steps outside PR fast coverage; the `Deferred checkpoint` workflow, retaining the `deep-gate` label and filename |
| Golden rebuild | `--deep`; fresh golden basin-map production and comparison |
| Strict checkpoint | `--strict`; full checkpoint, golden rebuild, and refusal of skips |

Preserve existing CLI flags and stable check contexts.
Prefer clearer displayed workflow names and help text to adding equivalent flags.
Any justified alias shares one selection implementation and tests equivalent behavior.

[development.md](../../../../development.md#validation-loops) owns the contributor
matrix. [Operating rules](../../../../operating-rules.md) own the efficiency principle:
weigh independent evidence against speed, optimize avoidable cost before deferral, and
separate per-commit feedback from final checkpoints.
Generate the AGENTS summary through `render_operating_rules`. Keep historical timings in
records and current usage in the guide.
The predecessor plans retain dated evidence; this plan owns their current checkpoint and
naming follow-up.

### Documentation changes in this block

| Document or surface | Required update |
| --- | --- |
| `development.md` | One current matrix for names, commands, coverage, measured latency, budgets, event triggers, checkpoint freshness, and retained timing artifacts. Correct historical counts and thresholds. |
| `operating-rules.md` | State fast per-commit feedback, justified final-checkpoint cost, detailed timing records for long runs, and review of evidence value versus speed as standing efficiency-block principles. |
| Generated `AGENTS.md` summary | Regenerate from operating rules; keep it brief and point to the detailed rules. |
| `README.md` and `SYNOPSIS.md` | Keep workflow entry and contributor links discoverable; link W5 to this plan without another copied validation matrix. |
| The two predecessor efficiency specs | Add a dated successor link for current targets and checkpoint policy; retain their historical experiments. |
| `docs/project/document-map.yaml` and its generated view | Register this plan and retained review/report artifacts with their actual authority and lifecycle. |
| Workflow display names, CLI help, Makefile and contributor command examples | Audit against the agreed terms; change only inconsistent references, preserve stable flags and check contexts, and test affected examples. |
| Campaign/session and logbook instructions | Link timing receipts and checkpoint identity where applicable; update conflicting live instructions without rewriting historical sessions or agenda decisions. |
| Engineering experiment runbook, registry, reviews, and generated report | Record instruments, criteria, all results, and per-candidate dispositions; link them from this plan and the guide. |
| Upstream tbd guidelines and their cross-references | Review existing guidance, propose only reusable additions, and retain the proposal and upstream disposition in this block. |

### Upstream tbd contribution

Use `tbd guidelines` to review `general-testing-rules`, `ci-and-gates-rules`,
`general-eng-agent-principles`, and `golden-testing-guidelines`; read narrower Python or
Rust guidance only for a language-specific boundary.
The testing rules already require independent evidence, fast inner loops, cheaper setup
before deferral, and explicit outer tiers.
CI guidance owns failure propagation, entry points, and gate integrity.
Reference those requirements rather than duplicating or claiming them as new insights.

Evaluate two concrete publication shapes.
A focused addition to the existing documents is preferable if the reusable material fits
a few rules. A dedicated guideline, proposed as `testing-and-ci-performance`, is
justified if the complete method needs its own reference: per-test value/cost inventory,
detailed durable timing, stage and critical-path attribution, bounded nested
parallelism, workload identity and safe reuse, statistically honest comparisons, and
separate immediate-feedback and final-checkpoint contracts.
In that case add short cross-links from testing and CI guidance, and register the new
document in tbd’s discovery metadata so agents can find it.

The completed guideline audit recommends the dedicated document.
Its
[retained proposal](../../reviews/review-2026-09-06-tbd-testing-and-ci-performance-proposal.md)
contains the full new guide and focused edits to all four existing guidelines, with
upstream source revisions and issue-search findings.
Submission awaits review of that concrete draft.
After submission, record the upstream URL here; after acceptance, verify discovery by
`tbd guidelines --list` and loading by name before reconciling local links.

Keep repository-specific test names, measurements, wall-time targets, and mathematical
contracts in this project.
Upstream examples should work across languages and projects.
Check current upstream content and existing issues before proposing changes.
Follow `tbd shortcut suggest-upstream-improvements`: inspect local forks and their
sources, retain a concrete issue or PR draft with proposed hunks and rationale, and show
that draft before filing.
File the agreed reusable change, record its URL and status here, and reconcile local
references after it ships.
A filed proposal is not an accepted guideline.

## Implementation Plan

### Phase 1: Audit and measured improvements

- [x] Establish current topology and successful hosted baseline.
- [x] Create this spec with `new-plan-spec` and link its owning bead.
- [x] Retain independent cost/value and documentation reviews with dispositions.
- [x] Add missing attribution and a reproducible engineering experiment record.
- [x] Register and measure the strongest candidates; retain negative results.
- [x] Integrate accepted optimizations with differential and regression checks.

### Phase 2: Consistency and end-to-end validation

- [x] Reconcile workflow/help names and feedback versus final-checkpoint placement.
- [x] Correct stale counts, timings, wall-time thresholds, and calibration claims.
- [x] Link this plan from the development guide, W5 entry, predecessor plans, and map.
- [x] Complete the documentation matrix, including durable long-run timing rules.
- [x] Review upstream tbd guidance, choose a dedicated guideline or focused additions,
  and prepare the reusable proposal and cross-links for upstream review.
- [x] Verify changed selection, concurrency, failure, and naming contracts.
- [ ] Run affected checks and the full final checkpoint on integrated source, reporting
  golden-rebuild and strict evidence separately.
- [ ] Publish a PR, verify fast CI and checkpoint results, generate the experiment
  report, and close or explicitly defer each item with evidence.

### Phase 3: Explained selection and complete checkpoint coverage

- [ ] Extend the existing selector with exhaustive-family planning in reporting mode;
  demonstrate complete node membership and declared code/data/fixture inputs.
- [ ] Replay the PR94–96 change sets and exercise unknown inputs, nested tests, renames,
  deletions, lock/config changes, merged upstream changes, and dynamic dependencies.
- [ ] Add validated family receipts, end-of-run input checks, trusted provenance, and
  explicit fresh/reused/unresolved dispositions to the existing timing/report tools.
- [ ] Require complete family coverage at the final checkpoint and retain full periodic
  audits. Verify that missing evidence and workflow failures cannot appear as success.
- [ ] Update `development.md`, local PR shortcuts, workflow contract tests, and the
  upstream guideline/shortcut proposal together, as listed in the design matrix.
- [ ] Measure total feedback latency and runner work across ordinary pushes and the
  final checkpoint; accept rollout only with equivalent coverage and useful savings.

These are planned additional cleanups in this block, tracked with `think-xejq`; they are
not claims that selection or reuse is already operational.

The coordinator owns shared records, integration, commits, and external updates.
Sub-agents own bounded investigations or disjoint code paths.
The owning bead records session slices and integration boundaries; replanning changes
future work, not frozen experimental criteria.

The
[implementation review](../../reviews/review-2026-09-06-validation-efficiency-implementation.md)
records two timing failure-path fixes, the preserved candidate contracts,
source-evidence limitations, and the worker-cap latency risk.
The n=40 duplicate replay remains intact: its proposed replacement changes standalone
pytest coverage and needs a separate coverage decision.
Exhaustive scheduling remains a follow-up until the new per-test profile can justify it
under the declared total-work guard.

## Testing Strategy

Run correctness guards before timing comparisons.
Parallel runs preserve selected tests, nonzero exits, process cleanup, deterministic
artifacts, and explicit skip counts.
Exercise worker failure, stale or missing evidence, and empty selection where those
boundaries change. Apply representative negative controls to rewritten oracles.

Use the project’s frozen Python 3.14 environment.
Run records, edit, and reachable tests while developing and the full checkpoint at final
integration. Compare performance only within declared regimes; do not rerun unchanged
producers merely to refresh a summary.

## Rollout Plan

Land coherent changes through a PR from `codex/validation-efficiency-block`, with
measured results, coverage mappings, unresolved cases, and the final command matrix.
Existing entry points remain usable during naming cleanup.
Settings changes and other open PRs remain separately attributable work.

## Open Questions

- How much exhaustive cost is setup, repeated work, or one dominant exact decision?
- Which expensive tests duplicate whole-gate decisions, and which protect independent
  implementations or interfaces?
- Can bounded scheduling shorten both long jobs without oversubscription?
- Which results have complete, stable inputs and could safely be reused?
- What checkpoint target does the measured lower bound support after optimization?

## References

- [W5 contract](../../../../SYNOPSIS.md#workflow-entry-contracts) and
  [workflow overview](../../../../README.md#workflow-entry-points).
- [Validation loops](../../../../development.md#validation-loops),
  [gate budgets](../../../../packing/devtools/gate-budgets.yaml), and
  [implementation](../../../../packing/src/sqpack/cli/validate.py).
- [Operating rules](../../../../operating-rules.md), especially OR-12 through OR-15.
- [Gate validation speed](plan-2026-08-29-gate-validation-speed.md) and
  [research-loop efficiency infrastructure](plan-2026-08-25-research-loop-efficiency-infrastructure.md).
- [Agenda 023](../../../../packing/campaign/agendas/agenda-023-efficiency-block-the-gate-itself.md).
- [Session records](../../../../packing/campaign/agent-sessions/README.md) and
  [logbook ownership](../../../../packing/campaign/research-loop-logbook/README.md#record-topology).
- [Repeated-work instrument](../../../../packing/devtools/measure_gate_repetition.py).
- [Experiment-loop skill](../../../../.agents/skills/experiment-loop/SKILL.md).
- [PR #93 review](https://github.com/jlevy/squares/pull/93#issuecomment-5558207513).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
