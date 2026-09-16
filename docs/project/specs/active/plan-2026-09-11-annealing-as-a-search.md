---
title: Annealing as Search
description: Repairing the evidence contract, separating the search machinery, and exposing measured multi-run search in the workbench
author: Claude (agent), for the repository maintainer
---
# Feature: Annealing as Search

**Date:** 2026-09-11

**Updated:** 2026-09-14

**Author:** Claude (agent), for the repository maintainer

**Status:** Active; the seeded harness and exploratory campaign exist, but record and
validity repairs block further search claims

**Workflow:** W7 instrument repair, W2 evidence review, then W6 for separately
registered measurement rounds.
The current phase is planning; no new experiment is authorized by this document alone.

**Tracking:** `think-7umw` (research epic), `think-o13k` (Pack, Search and Animate),
`think-c0rm` (strategies with declared guidance)

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

The seeded page API and `squares-workbench-benchmark` make repeatable multi-run
execution possible. The exploratory records established useful questions about the
proposal, schedule, repair and contact law.
They do not yet support fresh comparative claims because the evidence contract is
incomplete.

The review found these distinct cases:

| observation | status | disposition |
| --- | --- | --- |
| The retained summaries include `n = 17` cells at anneal level 8, all scored before the validity check. Repaired `n = 17` runs exist at level 6 only, and the retained deep level-8 artifact contains `n = 11` only. | `exp-208`’s deep level-8 table for `n = 17`, 26 and 29 had no retained source. | Removed from `exp-208` and `X-034` (`think-jdgu`, `think-84m3`); the record now cites only `resolved: true` cells. |
| The report validator admits non-finite metrics, and the sweep path ranks results without applying that validator. | Demonstrated implementation defect. It can turn an invalid or non-finite outcome into a reported best. The retained aggregates do not show whether it changed a published result. | Fixed on #160, not here: `think-1fpa` closed at `f9099096`, where the package benchmark replaces the harness; its review round refused below-record and non-converged successes and counted every attempt (`fbc74c0e`, `acae83c6`). `think-nals`’s one fail-closed validity contract (`ec0a0604`) is now read at the benchmark, Search and page boundaries (`c0d9db2b`). |
| Large accepted seed values can alias in the generated JavaScript because the seed mix loses integer precision before the 32-bit operation. | Demonstrated public reproducibility defect. The small seed ranges in the recorded campaign are not known to be affected. | Fixed on #160, not here: `think-dq1l` (`f9099096`) fixed the mixer and supported seed domain, and `think-karf` (`15d97a59`) enforces seed receipt and replay semantics at the strategy boundary. |
| Raw annealing JSONL files are ignored and absent; retained summaries cannot reconstruct per-seed trials or disjoint blocks. | Deliberate storage choice with a material audit limitation. | `think-3eha` repaired the record contract (`91722c3a`). `packages/workbench/tools/workbench_tools/summarize_annealing.py` rebuilds the summaries from regenerated rows. `think-4z7d` closed on #160 (`15d97a59`) with a disjoint-block reporter. Findings cite only retained cells and state what cannot be re-checked. |
| `exp-209` records an inline compaction pass whose program and outputs were deliberately not retained. | Historical exploratory note, not replayable evidence under OR-1. | `think-3eha` marks the evidential limit; `think-na2i` builds the missing instrument before the algorithm or negative result is reused (`think-3hb7` closed as a disposition without one). |
| Imported animation entries can acquire numerical assurance from an asserted `feasible` flag, and intermediate strategy frames can be relabelled with a later container side. | Demonstrated provenance and trace-semantics defects. | Fixed on #160 at `15d97a59`, not here: `think-sdmi` validates imported evidence and `think-karf` enforces executable strategy and trace semantics. |
| Revision probes, research instruments and product entry points overlap. | Cleanup risk: deleting a probe can also delete its only semantic assertion. | `think-cqfc` inventories consumers and preserves unique controls before retiring obsolete code. |

**What ships with #160.** The harness and page repairs named above are commits on PR
#160, which deletes `devtools.bench_annealing` in favour of the package benchmark.
On this branch the harness keeps those defects, so this record uses it only to reproduce
the recorded rounds, and a new comparative round waits for #160.

**Record policy.** The annealing records have not reached `main`, so under
[conventions §7](../../../../conventions.md#7-corrections) they are drafts.
On the owner’s direction of 2026-09-14, superseded claims were removed rather than
annotated, and each artifact names commit `a40d272c` for its previous text
(`think-84m3`). Ids and renumberings stay recorded as identity notes.
Once the records land on `main`, they are corrected by addition.

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

## Strategies With Declared Guidance

**Owner direction, 2026-09-14.** How well a search works depends on its structure and
strategy, and there are many midpoints between fully blind and fully guided: a record’s
connected components, its contact graph, its flush contacts, and simplified graphs whose
touching groups start parallel and pull apart as the container closes.
Each way of stitching that information into an optimisation should be a strategy,
written in the repository’s strategy format, and code should run strategies in a loop
and compare them for one `n` and across `n`.

So the benchmark’s question becomes: **for each record, which strategies find it, and
how much of the record does each have to be given?** Tracking: `think-c0rm`.

### The format already exists, and the physics is outside it

A PackingStrategy document (`packing/strategies/packing-strategy.schema.yaml`) is an
ordered list of phases.
Each phase names a mechanism (`scatter`, `grid`, `assemble`, `project`, `ratchet`,
`relax`, `guide` or `container`) and carries a `structure` block: the `rung` it was
given, the `source` of that structure, and an optional `rewired` or `thinned` control.
Constraints are declared as bands.
`workbench_tools.strategy_execution` (`squares-workbench-strategy`) executes documents
for the projection solver.
`frontier/search-strategies.yaml` separately catalogues 28 named search strategies, and
hypotheses cite catalogue entries through `strategy_refs`.

The workbench’s physics cannot be written as a document.
Blind, free and snap runs, the shake dial, `bodies`-style blocks and the contraction
that tolerates overlap all live in page code, so none of the benchmark’s runs so far is
a strategy anyone can re-run by name.

### What is already known

- **Blind is a middle rung.** It starts from the record for `n - 1`, closes its walls
  onto the record side for `n`, and in the `bodies` style the benchmark used it welds
  squares into rigid blocks chosen by matching the two records.
- **A first structure ladder already ran, on the projection solver** (2026-09-09,
  [X-025](../../../../packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md),
  `packing/devtools/sweep_structure_hints.py`). Declared as constraints, structure did
  not help. At `n = 11` success fell as more contacts were declared and the reachable
  side got worse; at `n = 5` and 10, declaring faces left the basin as wide as the bare
  projection; exact equalities pushed the search away from the record.
  Used to build the start, structure helped: laying out face groups first lifted a cold
  solve from 1 run in 8 to 5 in 8 at a loose side (commit `2d2a7790`). The samples were
  4 to 8 cold starts, and no registered experiment records them.
- **The workbench’s contact-graph attraction did not realise the graph.** Its pull
  reaches a quarter of a side, while target pairs start one to four units apart, and no
  torque turns a pair into face-to-face contact (`NOTES.md` in the v2 spike).
- **The owner’s merge-then-release is built only in part.** The projection ratchet’s
  `phased` mode holds face-contact groups tight and then releases them
  (`run_projection_ratchet.py`). No engine merges near-flush groups at a declared
  tolerance, releases them on a schedule, or has an aligning torque.
- **Near-flush groups are uncommon below `n = 30`.** In the records for `n = 5`, 10, 11,
  17 and 26, every corner contact joins squares 36–45° apart.
  Near-flush corner contacts appear at `n = 29`, seven of them within 0.3–4.5° of
  alignment, and at `n = 37`, two at 2.9° (`run_projection_ratchet.py`, the `phased`
  docstring).

So structure should **construct and stage** a run, not be held as a constraint.
Constraints stay bands, never equalities.

### Extending the format

Four additions make every approach a document (`think-8ocb`):

1. **Physics mechanisms.** `drop` places the new square by the coarse-grid proposal.
   `simulate` runs contacts, walls and a shake schedule while the walls close toward a
   side with a declared overlap tolerance.
   `resolve` repairs the result to a packing.
   Blind, free and snap become documents; snap remains a `guide` and is illustration
   only.
2. **Where guidance acts.** A rung says what a phase was given; a use says what the
   phase does with it:
   - `start` constructs the arrangement from it, the one use with positive evidence;
   - `weld` holds rigid blocks until a later phase releases them;
   - `attract` pulls along given contacts, with a range and an aligning torque;
   - `shake` sets the amplitude per body, so welded blocks hold while loose squares
     move;
   - `constraints`, the existing bands.
3. **Rungs and capabilities.** The rung list grows to cover what the runs actually use,
   and each executor declares the mechanisms and uses it supports.
   A document runs only where every phase is supported, and is refused before running
   anywhere else.
4. **A derived guidance summary.** Computed from the phases — the most informative rung
   any phase uses, and whether any phase guides onto the record — recorded with every
   run and printed with every result.
   Each document also names its catalogue entry, so results roll up by strategy family.

| rung | the run is given | exists today |
| --- | --- | --- |
| `none` | nothing but `n` | the Rust search; the page optimiser’s random and grid starts |
| `previous` | the previous record and the reference side | blind in `physics` style |
| `blocks` | which squares move together | blind in `bodies` style |
| `touching-partition` | which squares touch, as clusters | not computed anywhere |
| `contact-graph` | square–square contacts | Python at 1e-9; the page sees only aligned full sides |
| `contact-graph-with-types` | contacts typed flush or corner | exact only for `n = 11` and 29 |
| `with-wall-contacts` | the above, plus wall contacts | Python |
| `merged-near-flush` | near-flush groups merged at a declared tolerance | not built |
| `partial-poses` | exact layouts of some rigid clusters | not built |
| full poses | every destination pose, through `guide` | free and snap |

The existing `partition` rung means angle classes and keeps that name.
The order is by intent; what compares rungs across `n` is the number of degrees of
freedom a hint leaves, from the rank of its constraints at the record, which is how the
chunk census counts slide freedoms.

### The evaluation loop

The loop is the benchmark generalised from one method’s parameters to strategies
(`think-qx88`):

- **Input:** a set of strategy documents, a set of `n`, and a plan of disjoint seed
  blocks at equal work.
- **Run:** each document on an implementation that supports every phase.
- **Score:** only after the shared validity contract passes, with repair recorded as its
  own step.
- **Record:** each trial carries the document’s content hash, its guidance summary, its
  catalogue entry, the effective seed and configuration, and provenance.
- **Report:** per `n`, the valid success rate at tolerance, best-of-k over disjoint
  blocks, and cost in steps; across `n`, which strategy at which guidance succeeds
  where.
- **Controls:** every structural strategy runs beside its rewired and thinned variants,
  which are documents in their own right, so a gain is attributable to the true
  structure.
- **Test set:** `n = 29` and 37, where merge-then-release should matter; `n = 11` and
  17, tilted classes without near-flush contacts; `n = 5`, 10 and 26, the 45° families;
  and one partial grid as a control.
- **Held out:** any parameter chosen from the results is checked on `n` it was not
  chosen on.

A result names its strategy and guidance.
A sentence of the form “given `merged-near-flush` as a start, with a release phase, the
physics reached `s(29)` in k of m blocks” is a statement about guided search, never a
discovery.

The three modes are the loop’s three faces: **Pack** runs one document once; **Search**
runs the loop and shows the comparison; **Animate** plays a recorded trace.

### What must be built

1. **The format extension** (`think-8ocb`) and **today’s approaches as documents**
   (`think-w9pb`), so the first comparison has real entries.
2. **Extraction** (`think-rey9`): each rung’s hint from a record at declared tolerances,
   in one implementation that Python and the workbench both read.
3. **Kernel mechanics** (`think-os1n`): weld and release, an aligning torque, attraction
   range as a parameter, shake per body, and partial pins.
4. **Starts from structure** (`think-y3o8`) that keep the record’s internal offsets.
5. **The evaluation loop** (`think-qx88`).
6. **Strategies in Pack and Search** (`think-czav`), labelled by guidance.
7. **Hypotheses registered before the first round** (`think-gdkd`).

The same extraction serves `think-hk37`, the rigidity marks.
The shared-language plan owns the format change (`think-8ocb`) and takes this section’s
field list and rung table as its design; this plan owns the evaluation loop
(`think-qx88`).

## Ordered Work

`think-5pv0` integrated the workbench parent into this leaf at `27d2f8cc` and reran its
affected checks, so later results rest on the combined baseline.
`think-kpvc` makes the existing behavioral checker part of the normal validation path so
this contract does not depend on a manual run.

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

### B. Rebuild measurement and correct the narrative — `think-4z7d`, `think-jdgu`, `think-na2i`

`think-4z7d` closed on #160 (`f9099096`, `15d97a59`) with the committed reporter for
acceptance rates, CPU work and disjoint-block distributions.
It distinguishes prefix summaries from independent block estimates and can optionally
reserve held-out blocks.

`think-jdgu` closed on #160 (`f9099096`) with an audit of every retained cell.
`exp-208` and X-034 here state what the retained cells support at `n = 17`: repaired
runs at level 6 only, and no retained deep run at level 8. Numerical claims are restated
only after the repaired tool derives them from durable inputs.

`think-na2i` turns the unretained `exp-209` compaction pass into a reusable instrument
with its control and outputs.
Until then, the historical negative does not rule out a reusable compaction algorithm.

The narrative correction is done (`think-84m3`). A rerun is justified only when phase A
shows that the required input cannot be recovered and the claim is still worth testing.

### C. Establish shared semantics, then extract the package

`think-1fpa` closed the non-finite and sweep-ranking paths on #160 (`f9099096`), in the
package benchmark that replaces the harness.
#160’s review found that admission still counted an overlapping below-record arrangement
as an exact success, and that one malformed probe row aborted a run uncounted.
Both are fixed on #160 (`fbc74c0e`, `acae83c6`): every planned attempt is counted, and
one that fails is recorded with its reason.
`think-nals` supplies one resolver and one fail-closed validity contract for the
benchmark and workbench.
Parity fixtures cover valid arrangements and failures for count, non-finite values,
walls and pairs. The API returns raw and repaired states separately, with acceptance and
work counters. `think-kpvc` keeps the resulting behavioral controls in the project
validation path.

Three related cleanups land around that contract:

- `think-sdmi` stopped imported animation metadata from manufacturing numerical
  evidence, on #160 (`15d97a59`).
- `think-dq1l` removed seed aliases and `think-karf` made strategy, seed receipt,
  trace-side and animation semantics executable, on #160 (`f9099096`, `15d97a59`).
- `think-cqfc` inventories obsolete probes and duplicate entry points before extraction;
  removal follows migration of live consumers and preservation of unique assertions and
  research records.

After the semantic repairs and `think-4ylo`’s full language-floor checks, `think-zisr`
extracts the reusable code into `packages/workbench` according to the workbench product
plan.

### D. Add Search after the foundation — `think-vhgz`, `think-o13k`

Search remains explicitly deferred until phases A through C and the standalone package
extraction are complete.
PR #160 ships a bounded experimental Search preview (n ≤ 32, at most eight seeds and
5,000 steps per trial).
It is not this mode and does not meet gate D. It then becomes a third workbench mode
built from the shared proposal, physics, validation, repair, objective and scheduler.

The mode shows the best valid arrangement, acceptance and failure counts, CPU work and
the disjoint-block outcome distribution.
It exposes trial count, seed range, parameter cells and held-out blocks when used.
Its reference-side label states that the comparison is atlas-conditioned.
The mode does not introduce another resolver, validator or physics path.

### E. Strategies with declared guidance — `think-c0rm`

Starts after phase C supplies the shared validity contract.
The format extension and today’s approaches as documents come first, then extraction,
kernel mechanics and starts, then the evaluation loop.
Hypotheses are registered before any round, and the workbench settings follow the Search
mode.

## Acceptance Gates

| phase | gate |
| --- | --- |
| A | Each active claim resolves to retained evidence and a complete manifest, or is explicitly annotated as unsupported or historical. New incomplete records fail validation. |
| B | A committed tool reproduces acceptance, work and disjoint-block distributions from durable inputs. The `n = 17` narrative matches the retained cells and their resolved status. |
| C | Benchmark and browser adapters agree on raw and repaired states and on every validity fixture, including non-finite values, pose counts, walls and pairs. Seed and trace replay tests pass. The standalone package is the shared source. |
| D | Search displays only valid ranked outcomes, accounts for every attempted trial, reproduces an exact seed and configuration, and reports independent blocks rather than a correlated prefix as a distribution. |
| E | Every approach compared is a validated strategy document with a derived guidance summary; each structural strategy runs beside its rewired and thinned controls; every reported success names its strategy and guidance. |

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
