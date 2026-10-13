---
title: Annealing as Search
description: Repairing the evidence contract, separating the search machinery, and exposing measured multi-run search in the workbench
author: Claude (agent), for the repository maintainer
---
# Feature: Annealing as Search

**Date:** 2026-09-11

**Updated:** 2026-09-16

**Author:** Claude (agent), for the repository maintainer

**Status:** Active; a bounded Search preview and the headless kinetics CLI exist, but
the shared search instrument (`think-gfqt`, `think-qx88`) does not yet meet its
contract, and registration, physical-response and graded-guidance prerequisites block
the first registered comparison

**Workflow:** W7 instrument repair, W2 evidence review, then W6 for separately
registered measurement rounds.
The current phase is planning; no new experiment is authorized by this document alone.

**Tracking:** `think-7umw` (research epic), `think-o13k` (Pack, Search and Animate),
`think-c0rm` (strategies with declared guidance), `think-0epc` (first systematic
guidance sweep)

## Scope

The [workbench plan](plan-2026-09-11-workbench-from-spike-to-product.md) governs the
end-to-end product outcomes and implementation phases.
This document supplies the research and measurement contracts: sections A/B feed its
Phase 1, section C feeds Phases 2/3, section D feeds Phase 5, and section E feeds Phase
5A. It does not independently release Search or authorize an experiment.

The workbench’s blind physics is an incremental, record-conditioned search.
It starts from the retained packing for $n$, withholds the destination poses for
$n + 1$, places the added square with a coarse-grid proposal, and runs the contact
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
| The retained summaries include $n = 17$ cells at anneal level 8, all scored before the validity check. Repaired $n = 17$ runs exist at level 6 only, and the retained deep level-8 artifact contains $n = 11$ only. | `exp-208`’s deep level-8 table for $n = 17$, 26 and 29 had no retained source. | Removed from `exp-208` and `X-034` (`think-jdgu`, `think-84m3`); the record now cites only `resolved: true` cells. |
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
- $n$, the source packing identity, the reference side, every physics and repair
  parameter, and the proposal and scheduler versions; and
- the requested trial count, completed trial count, interruption state and artifact
  path.

The browser must return the effective seed and configuration it used.
Recording only the requested values is insufficient for replay.

### Raw result, repair and validity

The raw physics state and the repaired state are separate records.
Repair never overwrites the state that the physics produced.
Both states carry a validation result against one definition:

- exactly $n$ uniquely identified poses;
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
When a result guides parameter choice, an optional held-out seed block or held-out $n$
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
touching components, its contact graph, its flush contacts, and simplified graphs whose
touching groups start parallel and pull apart as the container closes.
Each way of stitching that information into an optimisation should be a strategy,
written in the repository’s strategy format, and code should run strategies in a loop
and compare them for one $n$ and across $n$.

So the benchmark’s question becomes: **for each record, which strategies find it, and
how much of the record does each have to be given?** Tracking: `think-c0rm`.

Ordinary global stickiness and structural guidance are different experimental axes.
Stickiness is a force-law parameter between nearby squares and requires no knowledge of
a target packing. Structural guidance supplies selected relationships extracted from a
known record. A run may combine them, but its requested-guidance record and its report
name each independently, and its canonical receipt names the stickiness and whatever
guidance is in effect.

**Today the two axes are one control.** The kernel’s `relatedMask`
(`packages/workbench/src/simulation/kernel.ts`) restricts ordinary pair-law attraction
to masked pairs; repulsion is never masked.
Search’s Pack configuration accepts `related_mask`
(`packages/workbench/src/search/pack-runner.ts`), and the page builds masks from blocks
and from a record or drawn contact graph (`AtlasRelationshipKind` in
`packages/workbench/src/api/workbench-api.ts`, built in
`packages/workbench/src/application.js`). The only guidance strength is therefore the
pair law’s attraction and range.
`think-8ocb` names this path and moves mask construction into `GuidanceTarget/v1` and
the application configuration.
Until `think-os1n` adds a guidance force separate from the pair law, registered cohorts
refuse a non-null `related_mask`.

### One target contract, separate application policy

`GuidanceTarget/v1` is the JSON-safe interchange read by the nonvisual TypeScript
kernel, Node CLI and browser.
It stores target identity and provenance, a tier, stable square IDs, relative
relationships, extraction tolerances and declared ambiguity metadata.
It does not store application strength or an absolute destination pose.
Extraction returns a separate refusal result when the requested tier cannot be made
unambiguous under its correspondence rules.

A separate guidance-application configuration states, for each use:

- the use, such as start, weld, attract, shake or constraint bands;
- its strength and strength schedule, where the use has a strength; and
- how pairs or squares absent from the target are treated.

Strength belongs to a use.
`attract`, including its aligning torque, takes a continuous strength.
`start`, `weld` and `shake` are discrete, so each names its unguided control instead:
the unguided proposal at the same seed, the same run with no weld, and the uniform
shake. Constraint bands keep the strategy schema’s `band` and `weight`.

A run keeps two records.
The **requested-guidance record** carries the target content hash, the tier and the
application configuration as requested, zero strengths included.
It sits beside the receipt and never enters receipt identity.
The **canonical effective receipt** omits every inert use, so for the same base
configuration and seed a zero-strength run’s canonical receipt is byte-for-byte the
unguided receipt. That identity tests the canonicalizer, not the physics, so two kernel
controls go with it.
An un-normalized run, with the target loaded and every strength exactly zero, must
reproduce the unguided trajectory, validity and outcome exactly; its guidance-evaluation
count may differ and is reported.
Exactness requires the guidance force to run as its own pass after the pair-law pass:
folded into the pair loop, a guidance range could widen the broad-phase cell or change
the order in which forces are summed, and either can change the path at zero strength.
Over a declared short horizon, the largest pose difference from the unguided trajectory
must not increase down a declared descending strength ladder, and at the smallest
strength must be within a declared bound.
The planned defaults, once `think-8ocb` declares each use’s strength unit, are strengths
of 1e-2, 1e-4, 1e-6 and 1e-8 of that unit, a horizon of 10 base physics steps,
differences below 1e-12 counted as zero, and a bound of 1e-6 square sides.
Scheduled guidance composes explicitly with ordinary stickiness, collision, containment
and annealing.

The product exposes four comparable target tiers.
This table is also the naming table: prose uses the tier ids, and the names in the last
column mean the same thing.

| target tier | supplied information | strategy rung | other names in the record |
| --- | --- | --- | --- |
| `none` | no target relationships | `none` | — |
| `touching-component-partition` | membership in each touching component; at a label-agnostic start only the component-size profile is usable | `touching-partition` | touching-cluster partition (`think-rey9`); connected components |
| `contact-graph` | target square–square adjacency | `contact-graph` | — |
| `oriented-face-pairs` | each contact’s two features (`left_feature`, `right_feature`) and, for edge-edge contacts, their face alignment | `oriented-face-pairs`, a rung above `contact-graph-with-types` | face-to-face assignments; oriented face assignments |

Search’s `SearchPartition` value `tuning` is what these plans call calibration;
`held-out` is the same in both.

`GuidanceTarget/v1` does not store absolute centers, angles or destination poses, but a
complete oriented target can still determine them.
Where a record’s contact equations are rigid, a complete oriented target fixes the poses
locally up to congruence, and the strategy schema already notes that realising a full
contact structure is a linear program rather than a search.
Each extracted target therefore reports the degrees of freedom it leaves at the record
(`think-rey9`), and reports compare tiers by that count, not by tier name.

The `full poses` rung below is the existing record-target spring path, not a fifth
product tier. Animate’s `free` and `snap` modes attach target springs whenever the mode
is not `blind` and flag their samples `guided`
(`packages/workbench/src/simulation/trajectory.ts`); `snap` also lands on the record.
Pack’s open-ended run does the same when its `springs` flag is on (`AtlasOptimize` in
`packages/workbench/src/api/workbench-api.ts`), which a Search configuration requests
with `targets: record`. The rung stays outside `GuidanceTarget/v1`, and a report that
uses it names that rung rather than a guidance tier.
Whether the `guided` and `springs` flags are folded into the new guidance fields is
decided with the target contract under `think-8ocb`. Extraction declares symmetry and
correspondence rules and refuses a requested tier when ambiguity cannot be resolved
under those rules (`think-rey9`).

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

- **Blind is a middle rung.** It starts from the record for $n - 1$, closes its walls
  onto the record side for $n$, and in the `bodies` style the benchmark used it welds
  squares into rigid blocks chosen by matching the two records.
- **A first structure ladder already ran, on the projection solver** (2026-09-09,
  [X-025](../../../../packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md),
  `packing/devtools/sweep_structure_hints.py`). Declared as constraints, structure did
  not help. At $n = 11$ success fell as more contacts were declared and the reachable
  side got worse; at $n = 5$ and 10, declaring faces left the basin as wide as the bare
  projection; exact equalities pushed the search away from the record.
  Used to build the start, structure helped: laying out face groups first lifted a cold
  solve from 1 run in 8 to 5 in 8 at a loose side (commit `2d2a7790`). The samples were
  4 to 8 cold starts, and no registered experiment records them.
- **The workbench’s contact-graph attraction did not realise the graph.** Its pull
  reaches a quarter of a side, while target pairs start one to four units apart, and no
  torque turns a pair into face-to-face contact (`notes.md` in the v2 spike).
- **The owner’s merge-then-release is built only in part.** The projection ratchet’s
  `phased` mode holds face-contact groups tight and then releases them
  (`run_projection_ratchet.py`). No engine merges near-flush groups at a declared
  tolerance, releases them on a schedule, or has an aligning torque.
- **Near-flush groups are uncommon below $n = 30$.** In the records for $n = 5$, 10, 11,
  17 and 26, every corner contact joins squares 36–45° apart.
  Near-flush corner contacts appear at $n = 29$, seven of them within 0.3–4.5° of
  alignment, and at $n = 37$, two at 2.9° (`run_projection_ratchet.py`, the `phased`
  docstring).

So structure should **construct and stage** a run, not be held as a constraint.
Constraints stay bands, never equalities.

### Extending the format

The PackingStrategy document says where the shared target and application policy act; it
does not define a second guidance representation.
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
3. **Rungs, controls and capabilities.** The rung list grows to cover what the runs
   actually use. The `control` enum, today `none`, `thinned` and `rewired`, gains the
   controls registered below: `shuffled` membership, a split-merge partition, a
   wrong-feature assignment and a thinned graph’s rewired twin.
   Each executor declares the mechanisms and uses it supports.
   A document runs only where every phase is supported, and is refused before running
   anywhere else.
4. **A derived guidance summary.** Computed from the phases — the most informative rung
   any phase uses, and whether any phase guides onto the record — recorded with every
   run and printed with every result.
   Each document also names its catalogue entry, so results roll up by strategy family.

| rung | the run is given | exists today |
| --- | --- | --- |
| `none` | nothing but $n$ | the Rust search; the page optimiser’s random and grid starts |
| `previous` | the previous record and the reference side | blind in `physics` style |
| `blocks` | which squares move together | blind in `bodies` style |
| `touching-partition` | which squares touch, as clusters | not computed anywhere |
| `contact-graph` | square–square contacts | Python at 1e-9; the page sees only aligned full sides |
| `contact-graph-with-types` | contacts typed flush or corner | only $n = 11$ (exact) and 29 (multiprecision) |
| `with-wall-contacts` | the above, plus wall contacts | Python |
| `oriented-face-pairs` | typed square–square contacts with their features, and face alignment for edge-edge contacts | features recorded only for $n = 11$ and 29 |
| `merged-near-flush` | near-flush groups merged at a declared tolerance | not built |
| `partial-poses` | exact layouts of some rigid clusters | not built |
| full poses | every destination pose, through target springs | Animate `free` and `snap`; Pack `springs` |

The existing `partition` rung means angle classes and keeps that name.
The order is by intent; what compares rungs across $n$ is the number of degrees of
freedom a hint leaves, from the rank of its constraints at the record, which is how the
chunk census counts slide freedoms.

### The evaluation loop

The loop is the benchmark generalised from one method’s parameters to strategies
(`think-qx88`):

- **Input:** a set of strategy documents, a set of $n$, and a plan of paired,
  interleaved, disjoint seed blocks at equal work in the currency registered below.
- **Run:** each document on an implementation that supports every phase.
- **Score:** only after the shared validity contract passes, with repair recorded as its
  own step.
- **Record:** each trial carries the document’s content hash, its guidance summary, its
  catalogue entry, the effective seed and configuration, and provenance.
- **Report:** per $n$, the valid success rate at tolerance, best-of-k over disjoint
  blocks, and cost in steps; across $n$, which strategy at which guidance succeeds
  where.
- **Controls:** every structural strategy runs beside the information-changing controls
  registered for its tier below, each a document in its own right, so a gain is
  attributable to the true structure rather than to added forces.
- **Test set:** $n = 29$ and 37, where merge-then-release should matter; $n = 11$ and
  17, tilted classes without near-flush contacts; $n = 5$, 10 and 26, the 45° families;
  and one partial grid as a control.
- **Held out:** settings are selected on calibration cells by the frozen rule below, and
  only held-out cells decide.

The metric vector is registered before the first round (`think-gdkd`). Search outcomes
are packing validity, best valid side and the known-result gap.
Guards cover independent validity, finiteness, deterministic replay and the
zero-strength controls.
Cost is the enforced Search budget and the charged pair-level work below.
Component recovery, contact precision/recall, false contacts, oriented-face recovery and
contact gaps explain mechanisms; they cannot accept a search claim without a valid-side
improvement.

The first measured round is an unguided ordinary-stickiness response curve
(`think-9hdg`). The systematic guided sweep (`think-0epc`) then compares true targets
with the controls registered for each tier.
A headless partition freeze (`think-05o4`) divides known-answer cases into calibration
and held-out cells before any tuning.
Search’s presets (`think-3yma`) can load that partition, or any other manifest
partition, but they do not define it and do not wait for it.
Every rejected, invalid and no-effect round remains in the experiment record.

A result names its strategy and guidance.
A sentence of the form “given `merged-near-flush` as a start, with a release phase, the
physics reached $s(29)$ in k of m blocks” is a statement about guided search, never a
discovery.

The same nonvisual TypeScript kernel, target, application configuration, seed and
receipt drive every surface:

| surface | responsibility |
| --- | --- |
| Node API and CLI | Run one trial or a cohort without a DOM; emit raw trajectories, target-recovery metrics, work, validity and replay provenance. |
| Pack | Run one document once and show the target tier and active application settings. |
| Search | Run the loop and compare ordinary stickiness and structural guidance as separate sweep axes. |
| Animate | Replay the resulting trace and overlays without turning a supplied target into numerical evidence. |

The browser visualizes these results; it does not implement another force or receipt
path. Replay identity is claimed for Node and the pinned Chromium build the checks use;
other browsers are not claimed to replay bit for bit.

### Planned registration defaults

The choices in this section are planned defaults, not results.
`think-gdkd` freezes each one, or records its revision, before the first measured round.
No guided-versus-unguided comparison is admissible until it has declared the work
currency.

**Label-agnostic starts.** Search’s proposals are `grid`, `random` and `record-append`.
Only seeded `random` has interchangeable labels on its own.
`grid` is unseeded and places square $i$ in cell $i$ (`createGridPackStart` in
`packages/workbench/src/simulation/pack.ts`), so square numbering fixes the starting
adjacency identically in every block.
Record IDs are not in random order either: in `contact-structures.json` the two angle
classes at $n = 11$ are squares 0–5 and 6–10. A true partition or true graph at `grid`
could inherit that order as a head start.
Every structural arm at `grid` or `random` therefore relabels its target by a
permutation derived from the slot’s seed, the same permutation for every arm on that
seed, and only then are those starts label-agnostic.
Search’s one label-dependent start is `record-append`, which reads the previous record
by square ID; the strategy format’s `blocks` and a structure start that keeps the
record’s internal offsets (`think-y3o8`) would be label-dependent too.

**What the partition tier carries.** At a label-agnostic start the squares are identical
and their relabelled indices say nothing about the record, so the tier’s information is
its component-size profile.
Membership carries information only at a label-dependent start, so a `shuffled`
membership control is run only there.
At every start the information-changing control is a split-merge partition: split one
true component in two, then merge one piece with another component, keeping $n$ and
choosing sizes so the number of within-component pairs stays as close to the truth’s as
they allow. A record that is one touching component gives the partition
$\lbrace n\rbrace$, which carries nothing beyond $n$; an `attract` use over it is the
same all-pairs attraction as ordinary stickiness.
Such cells are excluded from the partition contrast.
Both records with typed contact features are single components: 14 pair contacts join
all 11 squares at $n = 11$, and 52 join all 29 at $n = 29$
(`packing/atlas/known-best/contact-structures.json`). `think-rey9` reports every
record’s component count and sizes before cells are frozen.
If no test-set cell has two or more components, `think-gdkd` drops the partition
contrast or replaces it with `merged-near-flush` before the first round.

**Graph controls.** The schema’s `keep` means different things for the two controls: for
`thinned` it counts the true edges kept, and for `rewired` the edges moved.
`rewired` keeps the edge count and moves `keep` edges to pairs that do not touch at the
record, so it is the contact graph’s information control; the planned default moves
every edge. `thinned` changes the edge count, so it never stands alone as an information
control. Its twin is defined explicitly: take the thinned true graph with its $k$ kept
edges, then move the same fraction of those $k$ edges that the full `rewired` control
moves, which by default is all of them.

**Oriented face pairs.** Face alignment is defined only for edge-edge contacts.
A corner-edge contact states which corner meets which edge, one scalar equation; a
corner-corner contact states which corners coincide, two.
Neither carries an alignment, and the aligning torque never acts on them.
The wrong-feature control keeps the same pairs and permutes features within each contact
kind, so an edge-edge contact names a different edge pair and a corner-edge contact a
different corner or edge; contact kinds, torque strength, range and schedule stay the
same, and only the information differs.
The mechanism control is the untyped graph with a label-free nearest-face torque at that
strength, range and schedule.
Both are deciding comparators.

**Known-answer coverage.** Each tier has these known-answer cells today:

| tier | known-answer cells |
| --- | --- |
| `none` | every retained record |
| `touching-component-partition` | none among the two feature-typed records, which are single components; other records are unknown until `think-rey9` reports component counts |
| `contact-graph` | `n = 11` under exact arithmetic and $n = 29$ at multiprecision; other records only at float tolerance, from `contact_edges` in `packing/devtools/known_structure.py` at 1e-9 |
| `oriented-face-pairs` | $n = 11$ and 29 only: 66 pair contacts, of which 35 are edge-edge, 25 corner-edge and 6 corner-corner |

With two cells, the oriented tier can put at most one $n$ on each side of the split, so
its held-out result is a single $n$ unless `think-rey9` extends feature extraction
first.

**Contrasts.** A candidate is accepted only if it beats every deciding comparator in its
row. Reported arms are measured and recorded but cannot accept or reject it.
The zero-strength controls are guards, not arms.
A contrast runs only if it has at least one eligible calibration cell and one eligible
held-out cell; otherwise it is recorded as ineligible, which is not a negative result.

| idea | candidate | deciding comparators | reported arms | eligible cells |
| --- | --- | --- | --- | --- |
| 182 | each level on a declared ordinary-stickiness grid | the base pair law with zero attraction | — | every frozen cell |
| 183 | true touching-component partition | the unguided arm; a split-merge partition; at label-dependent starts, `shuffled` membership | — | cells with two or more components |
| 184 | true contact graph | the unguided arm; a rewired graph at equal edge count | — | cells with a declared contact graph |
| 184, thinned | thinned true graph | the unguided arm; its rewired twin | the full true graph | cells with a declared contact graph |
| 185 | oriented face pairs | the unguided arm; a wrong-feature assignment; the untyped graph with a nearest-face torque | the untyped graph without torque | cells with features |
| 186 | each declared decay or release schedule | constant schedule with the same target and law | the unguided arm | cells of a tier that carried a strength forward; with no such tier, 186 is ineligible |

In every contrast after 182, the unguided arm runs the base pair law at the stickiness
level `think-9hdg` confirmed on held-out cells, or at zero attraction if it confirmed
none, and every guided arm uses that same level.

**Work currency.** Arms in one contrast share the enforced Search budget: the same
`physicsSteps`, `proposalAttempts` and `repairIterations` per slot (`SearchWorkBudget`
in `packages/workbench/src/search/contracts.ts`) and the same base slots per block, on
the same paired seeds.
Guidance work is charged, not exempt.
Each slot reports its pair candidates, guidance-force evaluations and repair pair tests,
and their sum is its pair-level work.
Stickiness can change that sum at fixed steps.
Any change of path changes which pairs are candidates, and the kernel widens its
broad-phase cell once √2 × square size plus the attraction range exceeds the base cell,
which for unit squares at Search’s default cell of 1.5 means a range above about 0.086.

When the two arms of a comparison differ in median pair-level work per block, the
lighter arm, candidate or comparator, also runs compensation slots in every block.
Their seeds come from a reserved range disjoint from every base, pilot, calibration and
held-out seed, and that arm’s block-best is taken over its base and compensation slots
together. Compensation is decided per comparison, so a candidate with several deciding
comparators has a separate block-best for each.
The number of compensation slots is a multiplier fixed for each contrast, arm and
candidate setting before any calibration round, from a work-only pilot on its own
reserved seeds that runs on every frozen cell, held-out included, and reads no outcome.
Every report states the realized work ratio, the comparator’s median pair-level work per
block over the candidate’s with compensation slots included, for calibration and
held-out cells separately.
A comparison whose realized ratio falls outside a declared band (planned default 0.8 to
1.25) is invalid; it is recorded and not re-tuned.
If any held-out comparison in a stage is invalid, the stage result is invalid: it is
recorded and neither accepted nor rejected.
A win that holds only at equal steps is reported and cannot be accepted.
For guided rounds this replaces the search-proposer rule’s `pair_tests` currency, which
the workbench kernel does not produce.

**Deciding statistic.** The decision applies clause 1 of the campaign’s
[search-proposer accept rule](../../../../packing/campaign/README.md#the-search-proposer-accept-rule)
to held-out cells, with each paired seed block in place of a seed and its best valid
side as `best_side`. Over at least five blocks per cell, the candidate’s median must be
below each deciding comparator’s and the two min–max ranges must not overlap, on every
eligible held-out cell.
A block with no valid state has a best valid side of +∞. Ranges that share an endpoint
overlap. The clause’s `reached_basin` alternative does not decide a guided round; basin
counts are reported as mechanism.
Paired block differences are reported as spread and decide nothing.

**Guards.** Clauses 3 and 4 of that rule name `sqsearch` controls, so guided rounds
replace them. Clause 3 becomes: every ranked state passes the shared validity contract
(`assessPackingSnapshot`) and the Python re-check `check_unit_square_packing`
(`workbench_tools.packing_contracts`), and the package’s validity fixtures pass at the
same engine commit. Clause 4 becomes: a declared positive control, such as a full-poses
run, reaches a valid state within `1e-2` of a known record side; no valid state at
$n = 16$ reports a side below 4; and deliberately invalid fixtures are rejected by the
same build.

The runner is Search’s Pack runner (`packages/workbench/src/search/pack-runner.ts` over
`packages/workbench/src/simulation/pack.ts`), driven from Node by a command that
`think-gfqt` delivers; no such command exists yet.
A Pack trial’s guards are finiteness, validity and deterministic replay.
The X-035 continuity budgets are not guards on these rounds.
They are defined on Animate’s 60 Hz presentation samples of a corpus transition
(`TrajectoryRequest` in `packages/workbench/src/simulation/trajectory.ts`), and a Search
trial has no equivalent: it starts from `grid`, `random` or `record-append` under a
squeezing container, Pack keeps no trajectory, and Pack deliberately integrates with its
own stability bound (`forceLawSubsteps`), so re-integrating a trial in Animate would
produce a different path.
Kinetic metrics on Search trials would need a retained Pack trajectory resampled at
presentation rate; that instrument does not exist, and H-215 is where it would be
registered. The measured rounds therefore do not wait on `think-o4wo` and `think-5tyy`
for a kinetic guard.
They and the guided Search receipts still wait on them through the base Phase 5
scheduler, which follows Pack/Animate merge readiness (`think-9sdr`); contract,
extraction and kernel work does not.

Registered cohorts set `timeoutMs` to null, so a wall-clock deadline cannot change a
slot’s status or partial result.
Receipt identity hashes the canonical `SearchTrialValue` or its versioned successor,
never `SearchOutcome`, which carries `elapsedMs`. The successor must store the canonical
effective configuration: today `SearchTrialValue.configuration` is a copy of the
declared configuration plus the requested and effective seeds (`effectiveConfiguration`
in `pack-runner.ts`), which would carry a zero-strength target into receipt identity.
CPU time, measured in Node only, and wall time are operational context; neither enters
receipt identity, the budget or the decision.

**Selection and the held-out gate.** On calibration cells only, each stage carries
forward the setting (a stickiness level, a guidance strength or a schedule) with the
lowest pooled median relative gap.
For each calibration block that gap is the block-best valid side minus the record side,
divided by the record side, or +∞ for a block with no valid state, and the median is
taken over every block of every eligible calibration cell together.
Ties go to lower pair-level work, then to weaker guidance.
A setting carries forward only if its pooled median is below each deciding comparator’s.
Otherwise the stage is recorded as a calibration no-effect and is not run on held-out
cells. Guided arms use the stickiness level the first stage confirmed on held-out cells,
or zero attraction if it confirmed none.
Carried-forward settings are frozen before any held-out outcome run.
Held-out confirmation, run once per stage with those settings, is the only decision
gate; calibration produces no verdict.

### What must be built

1. **The target/application and format extension** (`think-8ocb`), including the
   `relatedMask` migration and the new controls, and **today’s approaches as documents**
   (`think-w9pb`), so the first comparison has real entries.
2. **Extraction** (`think-rey9`): each rung’s hint, including oriented face pairs, from
   a record at declared tolerances, in one implementation that Python and TypeScript
   read, with every record’s component counts, feature coverage and remaining degrees of
   freedom.
3. **Kernel mechanics** (`think-os1n`): a guidance force separate from the pair law and
   applied in its own pass, weld and release, aligning torque, attraction range, shake
   per body, partial pins, and the zero-strength and small-strength controls.
4. **Starts from structure** (`think-y3o8`) that keep the record’s internal offsets.
5. **The evaluation loop and CLI** (`think-qx88`), then **guided Search receipts**
   (`think-10yz`) that carry the same configuration and canonical receipt through the
   base Phase 5 scheduler (`think-gfqt`).
6. **Strategies in Pack and Search** (`think-czav`), with controls and overlays labelled
   by guidance.
7. **Registration** (`think-gdkd`) and a **headless partition freeze** (`think-05o4`)
   that fixes calibration and held-out cells from `think-rey9`’s coverage and the
   registered eligibility rules.
8. **The measured rounds**, which consume these instruments rather than gate the
   product. The **unguided stickiness curve** (`think-9hdg`) needs item 7, the base
   scheduler with its Node command (`think-gfqt`), checkable ledgers (`think-i5pg`) and
   the successor series (`think-i08r`). The **systematic guided sweep** (`think-0epc`)
   needs the same, items 1–5, and the curve’s held-out result, which fixes the
   stickiness level guided arms use.
   Neither needs the browser controls of item 6, and neither has a kinetic guard.

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
`exp-208` and X-034 here state what the retained cells support at $n = 17$: repaired
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

Contract, extraction and kernel work (`think-8ocb`, `think-rey9`, `think-w9pb`,
`think-os1n`, `think-y3o8`) needs neither Phase 2A nor the Search scheduler and can
start now. The evaluation loop (`think-qx88`) follows that work and phase C’s shared
validity contract. Guided Search receipts (`think-10yz`) follow the loop and the base
Phase 5 scheduler, which follows Pack/Animate merge readiness and so Phase 2A; the Pack
and Search controls (`think-czav`) follow those receipts and the Search mode.
Registration (`think-gdkd`) and the headless partition freeze (`think-05o4`) follow
extraction. The measured rounds follow item 8 of
[What must be built](#what-must-be-built), and every hypothesis, contrast, selection
rule and calibration or held-out cell is frozen before the first of them.
The workbench controls and overlays consume the same configuration and receipt as the
headless loop.

## Acceptance Gates

| phase | gate |
| --- | --- |
| A | Each active claim resolves to retained evidence and a complete manifest, or is explicitly annotated as unsupported or historical. New incomplete records fail validation. |
| B | A committed tool reproduces acceptance, work and disjoint-block distributions from durable inputs. The $n = 17$ narrative matches the retained cells and their resolved status. |
| C | Benchmark and browser adapters agree on raw and repaired states and on every validity fixture, including non-finite values, pose counts, walls and pairs. Seed and trace replay tests pass. The standalone package is the shared source. |
| D | Search displays only valid ranked outcomes, accounts for every attempted trial, reproduces an exact seed and configuration, and reports independent blocks rather than a correlated prefix as a distribution. |
| E | Every approach compared is a validated strategy document with a derived guidance summary; a zero-strength canonical receipt is byte-for-byte the unguided receipt, and the un-normalized and small-strength kernel controls pass; each structural strategy runs beside the information-changing controls registered for its tier; Node and pinned-Chromium replay agree; every reported success names its strategy, ordinary stickiness and guidance, and is decided on held-out cells. |

## Questions for the Next Measured Round

- Does the proposal determine most of the outcome, or does added physics work improve
  the disjoint-block distribution at equal total CPU work?
- Does a repair that can rotate squares change the result after translation-only repair
  reaches a local jam?
- Which conclusions survive a held-out seed block or held-out $n$ after parameters are
  selected?
- Which metrics help tune search while keeping animation quality a separate product
  decision?
- At which ordinary-stickiness levels does each guidance tier improve valid best-side
  outcomes at equal work in the registered currency, rather than only reproducing target
  contacts?
- Do oriented face pairs add value over a wrong-feature assignment and over an untyped
  graph with a nearest-face torque, at the same attraction range, torque and schedule?

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
