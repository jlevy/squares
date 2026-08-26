---
title: Research-Loop Efficiency Infrastructure Plan
description: Measured plan to shorten Square Packing CI, validation, exact-test, and Codex research feedback without weakening assurance
author: Codex, for the project maintainers
date: 2026-08-25
status: proposed
---
# Feature: Research-Loop Efficiency Infrastructure

**Date:** 2026-08-25 (last updated 2026-08-25)

**Author:** Codex, for the project maintainers

**Status:** Proposed for staged implementation

**Workflow entry:** W5 `efficiency-loop`

**Primary focus:** Efficiency

## Overview

Shorten the path from a research edit to trustworthy evidence.
The work covers the complete feedback system: local focused tests, the ordinary packing
gate, GitHub CI on Linux and macOS, exact symbolic fixtures, delegated-agent overlap,
model and reasoning allocation, and the repeated context needed to resume a research
loop.

This is an efficiency cycle, not a process review.
The existing W1–W7 workflow, artifact ownership, mathematical criteria, and assurance
rules remain in force.
W5 profiles measured bottlenecks and changes their implementation while holding those
contracts fixed.

The first instrument is
[`codex_log_rollup.py`](../../../../devtools/codex_log_rollup.py).
It scans Codex JSONL logs recursively, removes inherited subagent history, and reports
parent wall time, recursive agent-time, overlap, tools, commands, model and thinking
levels, token use, timed model streaming where available, and the remaining client
response envelope. The dated
[`efficiency review`](../../reviews/review-2026-08-25-research-loop-efficiency.md)
records the baseline and prioritization that this plan uses.

## Goals

- Make the required pull-request signal fast enough to support an edit-and-check loop,
  with a Linux fast lane at a target p50 of at most 60 seconds and p95 of at most 90
  seconds after the environment is warm.
- Reduce the ordinary full Linux gate from the current 182–267-second validation range
  toward p50 at most 90 seconds and p95 at most 120 seconds on comparable hosted
  runners.
- Stop duplicating the complete full gate on macOS for every pull request.
  Retain a direct, blocking portability probe when that lane is scheduled, but schedule
  it on `main`, nightly, manually, or for a deliberately portability-sensitive change.
- Profile and shorten the 65-control mutation surface without changing any control id,
  mutation, expected diagnostic, restoration behavior, or failure disposition.
- Reduce the current 103–181-second focused exact row-jet test group by at least 5× for
  a repeated research edit, with the exact values, field checks, symmetry checks, and
  scientific guards unchanged.
- Expose enough telemetry to distinguish CI, local commands, delegated-agent waits,
  concurrent agent work, model response envelopes, model and thinking allocation,
  compaction, and uninstrumented gaps.
- Make a W5 efficiency check repeatable after material gate growth, a slow research
  session, or a recurring scheduled sample.
- Preserve a fast first signal and a complete later assurance signal; neither should
  silently stand in for the other.

## Non-Goals

- Changing the W1–W7 workflow, session vocabulary, experiment protocol, hypothesis
  criteria, or artifact ownership.
- Dropping a mathematical, mutation, replay, provenance, schema, or cross-platform guard
  merely because it is expensive.
- Calling a macOS failure advisory when the portability lane is intentionally running.
  The efficiency change is when and what that lane runs, not whether its result counts.
- Treating a client-side response interval as provider-side inference latency.
  Codex JSONL does not expose a complete server timing trace.
- Selecting a cheaper model for mathematical judgment, integration ownership, or a
  high-risk correctness decision solely to improve a timing chart.
- Caching scientific conclusions or generated evidence without every semantic input in
  the key.
- Adding brittle hosted-runner wall-clock assertions to functional tests.

## Background and Baseline

### CI

Run
[`32912699602`](https://github.com/jlevy/thinking-scratchpad/actions/runs/32912699602)
is the representative current baseline.
The Linux job took 277 seconds and the macOS job took 286 seconds.
Across twelve recent successful workflow runs, end-to-end workflow time ranged from 4
minutes 50 seconds to 7 minutes 10 seconds.

The Linux validation step spent 266.24 seconds wall-clock.
Its leading steps were 183.81 seconds of negative controls, 53.63 seconds of soundness
perimeter checks, 29.73 seconds of historical regressions, 19.28 seconds of
deterministic SVG checks, 19.00 seconds of Python quality checks, and 16.00 seconds of
Trump cone checks. The macOS full gate spent 190.69 seconds, led by 134.63 seconds of
negative controls, then ran the deep golden again for 75.05 seconds.

Both jobs use `--jobs 2 --inner-jobs 1`. The inner cap forces all 65 private-snapshot
mutation controls through one worker on each architecture.
The macOS job also repeats the entire ordinary surface before its one genuinely
platform-focused deep-golden probe.

### Research loops

The old research task spans 45 hours 28 minutes of envelope time and 37 hours 2 minutes
of parent active time across 27 turns.
Its recursive tree contains 139 sessions and 57 hours 8 minutes of agent-time, with 20
hours 6 minutes overlapped under the parent wall clock.
The parent issued 8,369 token-accounted model responses, almost entirely
`gpt-5.6-sol/max`, and recorded 77 compactions.

The active loop-2 snapshot used for the review had already accumulated more than three
hours of parent active time and more than seven hours of recursive agent-time.
All recorded model work in that tree used `gpt-5.6-sol/xhigh`. Its parent spent roughly
an hour waiting for delegates, but the recursive overlap shows that most of that wait
represented concurrent work rather than idle critical-path time.
The hot local commands were a 17-test exact row-jet group at 103–181 seconds per run and
exact diagnostic probes at 20–58 seconds.

### Existing work to preserve

This plan continues, rather than duplicates, the existing Efficiency epic `think-r1yl`
and its measured work:

- `think-xzew` owns the end-to-end baseline and profile;
- `think-rthe` owns mutation-control latency;
- `think-qk9w` owns sound validation and build caching;
- `think-l3ds` records the earlier 480→152-second gate reduction; and
- `think-u9r5` records the earlier limited delegation-timing extraction.

This review adds the missing bounded work packages under `think-r1yl`:

- `think-ma71` owns the recursive Codex JSONL rollup delivered with this plan;
- `think-l7hi` owns CI lane tiering and timing artifacts;
- `think-kdil` owns the exact row-jet profile and speedup;
- `think-xuk8` owns the recurring joined efficiency report and depends on the scanner
  and CI timing surface; and
- `think-5zgv` owns freshness-checked resume packets and measured model routing.

## Design

### 1. One telemetry vocabulary

Use four clocks and keep them separate:

| Clock | Meaning |
| --- | --- |
| Parent active time | Union of active turns in the coordinating Codex task |
| Recursive agent-time | Sum of active parent and descendant task intervals; concurrent work adds agent-seconds |
| Active union | Union of all parent and descendant intervals; approximates occupied wall time without double counting overlap |
| Response envelope | Active task time after explicit tool and compaction intervals; an upper bound that still includes API, dispatch, suspension, and uninstrumented gaps |

Where current logs expose `Reasoning` and `AgentMessage` item timing, report their sum
as the lower-bound timed model stream and report the difference as unattributed.
Never label the whole response envelope as inference time.

CI and local validation should emit the same step names, status, seconds, worker
settings, platform, revision, and selected surface in JSON. Historical trend reports
consume those records rather than scraping terminal prose.

### 2. Tier the CI signal by purpose

Create three explicit lanes:

1. **Required PR fast lane, Linux.** Run the fast packing surface plus workflow-contract
   and change-selection tests.
   Publish its JSON timings in the job summary.
2. **Full Linux assurance lane.** Run the complete ordinary surface with the optimized
   scheduler. Initially keep it visible on pull requests while measuring false-negative
   risk and latency; make it mandatory at the integration boundary and on `main`.
3. **macOS portability lane.** Run only named portability consumers, beginning with the
   semantic deep-golden probe and any dedicated platform/process controls.
   Run it on `main`, nightly, manually, or under an explicit portability trigger.
   When invoked it remains direct and blocking: no `continue-on-error`, masked exit, or
   expected-failure wrapper.

The existing workflow contract test must be changed with the workflow.
It should enforce the new lane purposes, not preserve the old duplication accidentally.
D-272 and D-273 remain historical evidence for why an invoked portability check must
count; D-320 and its focused YAML regression explain why the deep check no longer needs
to block every unrelated pull request.

### 3. Make validation resource-aware

Profile negative controls at worker counts 1, 2, and the hosted-runner-safe maximum.
Record per-control and aggregate distributions for at least three comparable runs per
configuration. Choose the smallest repeated speedup that keeps every result identical.

The ordinary gate currently has independent outer steps and internally parallel steps
but only a shared cap, not a resource scheduler.
Add one of these in evidence order:

- pass a measured dedicated worker count to mutation controls;
- schedule the mutation lane when other CPU-heavy pools are not competing; or
- add a small weighted resource scheduler if the two simpler designs cannot meet the
  budget reproducibly.

Do not begin with a generalized executor.
The accepted implementation must preserve stable output order, bounded process-group
cleanup, private snapshots, fresh bytecode caches, and exact mutation-to-diagnostic
matching.

### 4. Remove repeated exact symbolic construction

Profile the current row-jet test group before editing.
The first suspects are repeated `active_row_jets()` and `owner_row_jets()` construction,
dense exact 15×15 Hessian work, and `SecondOrderJet` field and symmetry validation on
every immutable intermediate.

Prefer immutable, input-keyed reuse at the narrowest correct boundary:

- module- or session-scoped pytest fixtures for unchanged exact source geometry;
- pure memoization for deterministic row-jet builders whose key includes every source
  coordinate, stratum, owner, correction, and field identity; and
- construction APIs that validate once at a trusted boundary while retaining focused
  tests for incompatible fields and asymmetric Hessians.

Compare exact serialized rows, gradients, Hessians, stresses, scale records, mutation
failures, and positive controls before and after.
Warm speed is useful only after a cold run and invalidation checks establish that the
cache is sound.

### 5. Shorten agent feedback without changing authority

The long tasks repeatedly reload the same skill contracts, run overlapping gates, and
use frontier reasoning for mechanical inventory and formatting work.
Provide a generated, freshness-checked resume packet that points to the active phase,
bead, exact validation command, branch, and only the contract fragments required for
that phase. The definitive documents remain the source; the packet fails closed when
their content identity changes.

Record model and thinking allocation by task role.
Use lower-cost settings only for bounded mechanical inventory, formatting, log
extraction, or CI observation with an explicit output contract.
Keep frontier reasoning for mathematical derivation, adversarial review, and final
integration judgment.
Measure retained-result latency and correction rate, not merely token cost.

Balance delegated work by the parent’s critical path.
Agent wait is not automatically waste: loop 2 shows substantial overlap.
The target is fewer idle tails, duplicate assignments, and repeated integration reads,
while preserving independent audits that catch correctness defects.

### 6. Make efficiency review recurring

Add a repository command that combines:

- selected Codex root task ids and their recursive JSONL rollups;
- recent GitHub workflow and job timing records;
- local validation benchmark records; and
- declared budgets with a change from the prior median.

Run it after a clocked research session, after a material validation-surface change, and
on a recurring scheduled sample.
Open or renew a W5 phase only when the report identifies a measured regression or a
budget miss with a preserved equivalence guard.
Store compact reviewed summaries, not raw prompts or complete private Codex logs.

## API Changes

The first CLI is:

```shell
uv run --frozen python -m devtools.codex_log_rollup \
  --sessions-root ~/.codex/sessions \
  --root-id <codex-task-id> \
  --format markdown
```

Repeat `--root-id` to compare trees, use `--format json` for `CodexEfficiencyRollup/v1`,
and add `--include-turns` for the complete turn tree.
Default Markdown keeps the recursive session and model tree compact.

The later repository-level efficiency command should consume this JSON rather than
import private parser internals.
No AgentSession schema change is required: a session’s type remains the ordered
`workflow_phases[].workflow` plus `focus`. The detailed telemetry stays linked evidence
because it has a different cardinality and lifecycle from the session record.

## Implementation Plan

### Phase 1: Establish comparable evidence

- [x] Land the recursive Codex JSONL rollup with legacy/current history de-duplication,
  live and interrupted turn handling, model/thinking/token summaries, tool and command
  timing, stream/envelope bounds, tests, and developer documentation.
- [x] Retain the dated loop-1, loop-2, and CI baseline review and link the existing
  Efficiency beads to this plan.
- [ ] Emit structured CI timing artifacts and job summaries with platform, revision,
  selected surface, worker settings, step timings, and total wall time.
- [ ] Establish rolling p50/p95 baselines without making hosted-runner wall time a
  functional pass/fail assertion.

### Phase 2: Shorten the blocking path

- [ ] Add the required Linux PR fast lane and change the macOS lane from a duplicated
  every-PR full gate to selected portability checks at the declared integration and
  scheduled triggers.
- [ ] Profile and tune the outer/inner validation scheduler, beginning with `think-rthe`
  and the 65 negative controls.
- [ ] Profile and remove repeated exact row-jet construction with exact equivalence and
  cache-invalidation tests.
- [ ] Re-measure Linux full, macOS portability, local fast, local full, and the focused
  exact test group under unchanged inputs.

### Phase 3: Keep the gains visible

- [ ] Add the freshness-checked research resume packet and role-aware model/thinking
  guidance, then compare retained-result latency and correction rate on a later loop.
- [ ] Add the recurring efficiency report that joins Codex, CI, and local validation
  records and highlights budget regressions.
- [ ] Document the W5 trigger and require a measured delta, preserved guards, and an
  explicit rejection when an optimization is not reproducible.
- [ ] Close or re-prioritize the linked beads from measured post-change evidence.

## Testing Strategy

- Use synthetic current- and legacy-format JSONL fixtures to test recursive discovery,
  replay-history removal, live and interrupted turns, model/thinking splits, token
  totals, command polling attribution, overlap, and timing semantics.
- Compare scanner output with manually inspected event sequences from both named
  research tasks.
- Add workflow-contract tests for lane triggers, exact commands, blocking semantics,
  worker settings, and timing artifact upload.
- Run every mutation control serially and under the candidate schedule; require the same
  ordered ids, statuses, expected diagnostics, and clean source state after normal exit,
  failure, timeout, and interruption.
- Characterize exact row-jet values before optimization and compare all exact outputs
  after each cache or construction change.
- Benchmark cold and warm runs on an unloaded host, recording revision, platform,
  command, worker settings, samples, median, dispersion, and input identity.
- Run the full Linux and selected macOS assurance surfaces before changing required
  status policy.

## Rollout Plan

1. Land telemetry and the new PR fast lane without removing the existing full jobs.
2. Measure several representative pull requests and confirm the fast lane catches its
   named mutation and workflow controls.
3. Land negative-control and exact-fixture improvements independently, each with a
   before/after receipt and easy code rollback.
4. Move macOS to selected integration and scheduled triggers only after the dedicated
   portability lane is green and visible.
5. Change required status policy last, retaining full Linux and macOS evidence at the
   declared integration boundary.

Rollback is configuration-first: restore the prior trigger or worker setting while
keeping the telemetry that diagnosed the regression.
Never accept a golden, weaken a mutation expectation, or reclassify a failed portability
result to make a performance rollout green.

## Framework Limitations

AgentSession/v2 already records the session type correctly through workflow phases and
focus, so this session can be unambiguously W5 `efficiency-loop` / `efficiency`. It
deliberately cannot represent thousands of model responses, nested task intervals,
overlapping agent-seconds, token use, or per-command timing.
Adding those arrays would turn a concise portable handoff into a private telemetry
archive. The scanner’s versioned JSON and this review are therefore linked evidence.

The framework also has no current repository-native recurring scheduler for an
efficiency audit and no schema for CI timing history.
Those are implementation gaps in this plan, not reasons to relabel the work as W4.

## Open Questions

- Should full Linux assurance remain visible on every pull request after the fast lane
  is required, or run only for paths classified as high consequence plus the integration
  boundary?
- Which macOS paths, labels, or explicit dispatch inputs should trigger an immediate
  portability run before merge?
- Can a dedicated mutation-control worker count meet the budget, or is a weighted outer
  scheduler needed to avoid oversubscription?
- Which exact row-jet object is the narrowest sound cache key after profiling?
- What retained-result and correction metrics are sufficient to approve lower-cost model
  routing for a bounded task role?

## References

- [Dated efficiency review](../../reviews/review-2026-08-25-research-loop-efficiency.md)
- [Development guide](../../../../development.md)
- [Workflow contracts](../../../../SYNOPSIS.md#workflow-entry-contracts)
- [Agent-session guide](../../../../campaign/agent-sessions/README.md)
- [Prior engineering efficiency review](../../reviews/review-2026-08-23-engineering-loops-and-efficiency.md)
- [Representative CI run](https://github.com/jlevy/thinking-scratchpad/actions/runs/32912699602)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
