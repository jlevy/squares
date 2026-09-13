---
title: Annealing as Search
description: Repairing the evidence contract, separating the search machinery, and exposing measured multi-run search in the workbench
author: Claude (agent), for the repository maintainer
---
# Feature: Annealing as Search

**Date:** 2026-09-11

**Updated:** 2026-09-12

**Author:** Claude (agent), for the repository maintainer

**Status:** Active; the seeded harness and exploratory campaign exist, but record and
validity repairs block further search claims

**Workflow:** W7 instrument repair, W2 evidence review, then W6 for separately
registered measurement rounds.
The current phase is planning; no new experiment is authorized by this document alone.

**Tracking:** `think-7umw` (research epic), `think-o13k` (Pack, Search and Animate)

## Scope

The [workbench plan](plan-2026-09-11-workbench-from-spike-to-product.md) governs the
end-to-end product outcomes and implementation phases.
This document supplies the research and measurement contracts: sections A/B feed its
Phase 1, section C feeds Phases 2/3, and section D feeds Phase 5. It does not
independently release Search.

The workbench’s blind physics is an incremental, record-conditioned search.
It starts from the retained packing for `n`, withholds the destination poses for
`n + 1`, places the added square with a coarse-grid proposal, and runs the contact
dynamics while contracting toward the atlas reference side.
The reference side is available to the run.

That scope is narrower than rediscovering a packing from nothing.
The benchmark asks whether this proposal and physics can improve a previous packing
toward a known reference under a stated budget and seed schedule.
Any claim in the campaign or workbench must use that wording.

The same mechanics support three products with different responsibilities:

- **Pack** performs one prescriptive run and exposes the settings that shape it.
- **Search** schedules many Pack runs and reports valid outcome distributions and work.
- **Animate** presents a trace or finished records without deciding whether either is
  valid evidence.

The current implementation and record issues are detailed in the
[workbench stack architecture review](../../reviews/review-2026-09-12-workbench-stack-architecture.md).
The package layout and product migration belong to the
[workbench product plan](plan-2026-09-11-workbench-from-spike-to-product.md).

## Current State and Evidence Limits

The seeded page API and `devtools.bench_annealing` make repeatable multi-run execution
possible. The exploratory records established useful questions about the proposal,
schedule, repair and contact law.
They do not yet support fresh comparative claims because the evidence contract is
incomplete.

The review found these distinct cases:

| observation | status | disposition |
| --- | --- | --- |
| The retained summaries include `n = 17` cells at anneal level 8. Those cells are sweep outputs marked unresolved, while the retained deep level-8 artifact contains `n = 11` only. | The earlier note that `n = 17` ran only at level 6 is false. The stronger deep-run claim in `exp-208` is not supported by the retained summary layout. | `think-jdgu` reconciles the experiment narrative with the actual cells, parameters and sample counts before any numerical conclusion is repeated. |
| The report validator admits non-finite metrics, and the sweep path ranks results without applying that validator. | Demonstrated implementation defect. It can turn an invalid or non-finite outcome into a reported best. The retained aggregates do not show whether it changed a published result. | `think-1fpa` fixes every harness path; `think-nals` makes the definition fail closed and identical at every later ranking and display boundary. |
| Large accepted seed values can alias in the generated JavaScript because the seed mix loses integer precision before the 32-bit operation. | Demonstrated public reproducibility defect. The small seed ranges in the recorded campaign are not known to be affected. | `think-dq1l` fixes the mixer and supported seed domain; `think-karf` enforces seed receipt and replay semantics at the strategy boundary. |
| Raw annealing JSONL files are ignored and absent; retained summaries cannot reconstruct per-seed trials or disjoint blocks. | Deliberate storage choice with a material audit limitation. | `think-3eha` repairs the record contract, and `think-4z7d` produces distributions from durable inputs. Existing records remain in place for annotation. |
| `exp-209` records an inline compaction pass whose program and outputs were deliberately not retained. | Historical exploratory note, not replayable evidence under OR-1. | `think-3eha` marks the evidential limit; `think-3hb7` supplies the missing instrument before the algorithm or negative result is reused. |
| Imported animation entries can acquire numerical assurance from an asserted `feasible` flag, and intermediate strategy frames can be relabelled with a later container side. | Demonstrated provenance and trace-semantics defects. | `think-sdmi` validates imported evidence; `think-karf` enforces executable strategy and trace semantics. |
| Revision probes, research instruments and product entry points overlap. | Cleanup risk: deleting a probe can also delete its only semantic assertion. | `think-cqfc` inventories consumers and preserves unique controls before retiring obsolete code. |

These dispositions preserve the exploratory record.
Corrections add annotations and replacement measurements; they do not erase old records
or silently rewrite the conditions under which they were produced.

## Evidence Contract

A search result is reviewable only when its inputs, work, outcomes and aggregation are
connected by retained artifacts generated by committed code.

### Run identity and provenance

Every trial block records:

- the exact seeds and their ordering, the supported seed domain, and the seed-mixing
  version;
- the engine commit, browser and browser build, runtime, operating system, and relevant
  package or lockfile identity;
- `n`, the source packing identity, the reference side, every physics and repair
  parameter, and the proposal and scheduler versions; and
- the requested trial count, completed trial count, interruption state and artifact
  path.

The browser must return the effective seed and configuration it used.
Recording only the requested values is insufficient for replay.

### Raw result, repair and validity

The raw physics state and the repaired state are separate records.
Repair never overwrites the state that the physics produced.
Both states carry a validation result against one definition:

- exactly `n` uniquely identified poses;
- finite coordinates and angles;
- containment by all four walls at the stated side; and
- every pairwise overlap within the declared tolerance.

Validation fails closed on missing or non-finite measurements.
Reports include the accepted count, rejected count and total attempted count, with
failure counts for non-finite data, pose count, walls and pair overlap.
An objective may rank only states that pass the applicable validation stage.

### Work and distributions

Cost includes CPU work, not wall time alone.
At minimum the record carries proposal attempts, physics steps, repair iterations and
completed trials; wall time remains useful operational context.
Acceptance rates always name their denominator.

The existing best-of prefixes are correlated views of one ordered stream.
They do not establish a best-of-`k` distribution.
The measurement tool partitions a declared seed range into disjoint blocks, computes one
best per block, and reports the block count and distribution.
Comparisons use the same blocks and work budget.
When a result guides parameter choice, an optional held-out seed block or held-out `n`
checks whether the conclusion survives outside the tuning set.

Raw trial records remain available long enough to reproduce the aggregate, or the
repository retains a compact lossless equivalent or durable artifact reference with the
manifest needed to verify it.
The summariser is committed code and its output links back to those inputs.

## Reusable Building Blocks

The next implementation separates policy from mechanics so Pack, Search and Animate do
not grow three versions of the physics or validity rules.

1. **Proposal** creates an initial candidate from the source packing and a seed.
2. **Physics** advances that candidate and emits a raw state and trace.
3. **Validation** checks count, finiteness, walls and pair overlap for any stated side.
4. **Repair** is a deterministic transformation from a raw state to a distinct repaired
   state, with its own status and work counters.
5. **Objective** scores a state only after the required validation passes.
6. **Scheduler** owns seeds, restarts, parameter cells, work budgets and disjoint
   blocks; it aggregates results but does not alter them.
7. **Animation** consumes labelled states and traces.
   It can display validation and provenance, but cannot grant assurance or change the
   side attached to a frame.

The standalone follow-on package will live at `packages/workbench` under `think-zisr`,
after the semantic cleanups.
The workbench product plan owns its internal module layout, build integration and move
sequence. This plan requires only that the extracted interfaces above remain
independently testable and usable by thin command-line and browser adapters.

## Ordered Work

Before implementation resumes, `think-5pv0` integrates the current workbench parent into
the annealing-search leaf and reruns its affected checks.
The reviewed leaf was based before the parent’s Python-floor and
retained-timing-artifact changes, so results from the older combination are not a clean
integration baseline.
`think-kpvc` then makes the existing behavioral checker part of the normal validation
path so this contract does not depend on a manual run.

### A. Repair the record contract — `think-3eha`

Inventory the experiment entries, summaries, raw-artifact policy and claim documents.
Make every surviving claim resolve to a retained output and exact run manifest.
Annotate records whose original per-trial evidence is absent or whose measurement was
left in one-off code.
Run the existing `packing-ledger check` and `packing-validate --records` gates in the
runbook’s round loop.
Repair the duplicate experiment ID, hypothesis index, numerical and effort blocks, stale
ledger and SYNOPSIS, and broken source revision.
Extend an existing gate only where a demonstrated provenance gap needs coverage.

No new experiment starts in this phase.

### B. Rebuild measurement and correct the narrative — `think-4z7d`, `think-jdgu`, `think-3hb7`

`think-4z7d` supplies the committed reporter for acceptance rates, CPU work and
disjoint-block distributions.
It distinguishes prefix summaries from independent block estimates and can optionally
reserve held-out blocks.

`think-jdgu` reconciles `exp-208` and dependent prose with the retained `n`, parameter
and sample layout. It records both parts of the `n = 17` correction: level 8 is present
in the sweep, and a retained resolved deep block is not.
Numerical claims are restated only after the repaired tool derives them from durable
inputs.

`think-3hb7` turns the unretained `exp-209` compaction pass into a reusable instrument
with its control and outputs.
Until then, the historical negative does not rule out a reusable compaction algorithm.

Existing files are retained for later annotation.
A rerun is justified only when phase A shows that the required input cannot be recovered
and the claim is still worth testing.

### C. Establish shared semantics, then extract the package

`think-1fpa` first closes the harness’s non-finite and sweep-ranking paths.
`think-nals` then supplies one resolver and one fail-closed validity contract for the
benchmark and workbench.
Parity fixtures cover valid arrangements and failures for count, non-finite values,
walls and pairs. The API returns raw and repaired states separately, with acceptance and
work counters. `think-kpvc` keeps the resulting behavioral controls in the project
validation path.

Three related cleanups land around that contract:

- `think-sdmi` prevents imported animation metadata from manufacturing numerical
  evidence.
- `think-dq1l` removes seed aliases; `think-karf` makes strategy, seed receipt,
  trace-side and animation semantics executable.
- `think-cqfc` inventories obsolete probes and duplicate entry points before extraction;
  removal follows migration of live consumers and preservation of unique assertions and
  research records.

After the semantic repairs and `think-4ylo`’s full language-floor checks, `think-zisr`
extracts the reusable code into `packages/workbench` according to the workbench product
plan.

### D. Add Search after the foundation — `think-vhgz`, `think-o13k`

Search remains explicitly deferred until phases A through C and the standalone package
extraction are complete.
It then becomes a third workbench mode built from the shared proposal, physics,
validation, repair, objective and scheduler.

The mode shows the best valid arrangement, acceptance and failure counts, CPU work and
the disjoint-block outcome distribution.
It exposes trial count, seed range, parameter cells and held-out blocks when used.
Its reference-side label states that the comparison is atlas-conditioned.
The mode does not introduce another resolver, validator or physics path.

## Acceptance Gates

| phase | gate |
| --- | --- |
| A | Each active claim resolves to retained evidence and a complete manifest, or is explicitly annotated as unsupported or historical. New incomplete records fail validation. |
| B | A committed tool reproduces acceptance, work and disjoint-block distributions from durable inputs. The `n = 17` narrative matches the retained cells and their resolved status. |
| C | Benchmark and browser adapters agree on raw and repaired states and on every validity fixture, including non-finite values, pose counts, walls and pairs. Seed and trace replay tests pass. The standalone package is the shared source. |
| D | Search displays only valid ranked outcomes, accounts for every attempted trial, reproduces an exact seed and configuration, and reports independent blocks rather than a correlated prefix as a distribution. |

## Questions for the Next Measured Round

- Does the proposal determine most of the outcome, or does added physics work improve
  the disjoint-block distribution at equal total CPU work?
- Does a repair that can rotate squares change the result after translation-only repair
  reaches a local jam?
- Which conclusions survive a held-out seed block or held-out `n` after parameters are
  selected?
- Which metrics help tune search while keeping animation quality a separate product
  decision?

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
