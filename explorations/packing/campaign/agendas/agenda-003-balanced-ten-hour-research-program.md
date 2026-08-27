---
title: agenda-003 — balanced ten-hour research program
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-003
  title: Repair the loop, then rotate across the highest-information research lanes
  updated: '2026-08-26'
  status: active
  objective: >-
    Use one mutable ten-hour agenda, with a full five-hour midpoint review, to repair
    launch-blocking pipeline defects before research, measure and improve iteration cost
    only where it is actually gating progress, complete bounded evidence-and-insight
    cycles on at least three independent scientific lanes, and leave every result and
    next action in its authoritative artifact without widening the program's claim
    boundaries.
  items:
  - id: BC-027
    purpose: tool_validation
    owner_focus: process
    instances: [5, 10, 11, 16, 26]
    state: complete
    priority: 0
    question: >-
      Can the merged validation pipeline fail at the first real error, report that error
      without a misleading success, and return to green before another scientific round
      begins?
    hypotheses: []
    budget: the first 120 minutes; four W7/W2 slices followed by one W5 checkpoint
    entry: >-
      PR 45 is merged; session 025 and the cold-start handoff require reconciliation;
      the merged-main Linux and macOS jobs failed only because session 025 remained
      active past its deadline; local free space must be rechecked before long gates;
      and think-c90t records a known fail-through bug
    exit: >-
      The merged-main failure has one typed cause, session and generated-view state are
      reconciled, the smallest pipeline repair has positive and mutation controls, and
      the applicable focused and integration checks are green. If this exit is not met,
      W7 continues and no W6 target run begins.
    bead: think-whwc
    depends_on: []
    next_evidence: >-
      Completed in session 026: D-340 retains the historical cause, the CLI regression
      and mutation control prove first-failure propagation, and the four-step
      replacement integration surface passes.
    artifacts:
    - defects.yaml
    - tests/test_validation_cli.py
    - devtools/controls.yaml
    note: >-
      Consume the existing main run before dispatching another. The first observed
      failure takes precedence over the older fail-through bug if they are different.
  - id: BC-028
    purpose: tool_validation
    owner_focus: efficiency
    instances: [5]
    state: tentative
    priority: 0
    question: >-
      Does repeated exact row-jet construction consume enough of the next scientific
      critical path that a bounded immutable-inventory reuse will repay its build cost
      during this ten-hour horizon?
    hypotheses: []
    budget: >-
      a 15-minute measurement at each efficiency checkpoint; at most two reassigned
      20-to-30-minute W5 slices if the trigger passes
    entry: >-
      BC-027 is green, the exact row-jet group is on the selected critical path, and a
      current profile shows more than 60 seconds with active_row_jets dominant
    exit: >-
      Either reject the optimization with measured arithmetic, or accept it only after
      three cold and five warm comparisons show at least a five-fold improvement, warm
      median at most 45 seconds, warm p95 at most 55 seconds, and exact semantic equality.
    bead: think-kdil
    depends_on: []
    next_evidence: >-
      checkpoint arithmetic for expected time saved in the remaining horizon, plus an
      exact-output equivalence result if implementation is admitted
    note: >-
      The known-best atlas already improved from 743.07 to 123.93 seconds and complete
      strict validation from 1,589.65 to 372.24 seconds. Do not reopen the rejected
      marginal lattice cache or optimize the atlas without a new profile. Session 026's
      first checkpoint rejected row-jet implementation: its acceptance and build cost
      requires about 11 to 16 remaining whole-group invocations to repay, versus the
      current estimate of two to four. Reconsider only if the frozen BC-029 plan changes
      that count.
  - id: BC-029
    purpose: research
    owner_focus: insight
    instances: [5]
    state: ready
    priority: 0
    question: >-
      Do the frozen minus-W scale routes and controls advance the n=5 terminal-family
      question beyond exp-044's finite unresolved obstruction without implying whole-
      component identity or connectivity?
    hypotheses: [H-023]
    budget: one 105-minute W3-W6-W2-W3 mini-cycle in session A
    entry: >-
      BC-027 is green; exp-044 remains terminal unresolved; exp-045 is preregistered and
      independently accepted before target implementation or measurement
    exit: >-
      A valid exp-045 outcome, including a finite unresolved result, or a typed
      instrument blocker. Every valid result receives an immediate W3 mechanism pass;
      an invalid instrument returns to W7.
    bead: think-1s0h
    depends_on: []
    next_evidence: >-
      exp-045 with a frozen criterion, the declared controls and scale routes, retained
      raw evidence, an independent replay, and a scoped successor disposition
    artifacts:
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-044-h-023-n5-minus-w-row-jets.md
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-045-h-023-n5-minus-w-scale-and-controls.md
    note: >-
      This remains pathwise, cell-local evidence. It cannot establish a whole terminal
      component, basin identity, connectivity frequency, or an n=11 search claim.
  - id: BC-030
    purpose: tool_validation
    owner_focus: correctness
    instances: [5, 10, 11]
    state: ready
    priority: 1
    question: >-
      Can CG-010 represent and price one complete target-free fixed-angle cell with
      declared walls, one frozen separating axis per non-edge, canonical ties, and typed
      caps before any target-sized enumeration?
    hypotheses: []
    budget: >-
      the final 30 minutes of session A for W1/W3 shaping, then 90 minutes of W7/W2/W3
      work at the start of session B
    entry: >-
      the corrected 3-established, 2-outside, 23-absent, 8-capped calibration taxonomy;
      ContactAssemblyGrammar/v1; and no consultation of target geometry
    exit: >-
      One complete target-free cell is priced and exercised under positive, omitted-
      wall, omitted-axis, tie, cap, and accidental-calibration-lookup controls. Passing
      this cell authorizes a BC-016 or BC-017 readiness decision, not BC-021.
    bead: think-6mcd
    depends_on: []
    next_evidence: >-
      a versioned full-cell label and cost vector with declared walls, non-edge axes,
      symmetry orbit, typed cap outcome, and independent mutation results
    note: >-
      The 11,013 size-five records are abstract scaffolds with no packing geometry,
      container fit, whole-packing feasibility, or optimality claim.
  - id: BC-031
    purpose: measurement_validation
    owner_focus: correctness
    instances: [11, 12]
    state: ready
    priority: 1
    question: >-
      Can one high-value missing primary source be recovered or receive a dated,
      reproducible negative search result that changes the proof or priority map?
    hypotheses: []
    budget: one 20-minute W1 slice, with W3 only if the source changes a method or claim
    entry: >-
      the canonical source-availability ledger, starting with El Moumni 1999 and Trump
      2023 before Chung-Graham or Arslanov-Bui
    exit: >-
      A retained primary with source-faithful notes, or a dated negative result that
      names the routes checked without attempting to defeat access controls.
    bead: think-4o6l
    depends_on: []
    next_evidence: >-
      an updated source-availability row and, only when warranted, one resulting proof
      question or corrected priority
  - id: BC-032
    purpose: tool_validation
    owner_focus: correctness
    instances: [11, 29]
    state: tentative
    priority: 2
    question: >-
      What is the smallest well-posed numerical witness or contact system that can test
      the next exact-or-interval promotion boundary without pretending that more decimal
      precision is a certificate?
    hypotheses: []
    budget: one checkpoint-selected W3/W7 or registered W6 mini-cycle of at most 75 minutes
    entry: >-
      ownership overlap is reconciled and the selected system has an explicit exact,
      interval, or typed-blocker criterion that fits the remaining clock
    exit: >-
      A replayable certificate, a certified escaping pose, or a typed source, importer,
      checker, field-precondition, or mathematical blocker.
    bead: think-75ll
    depends_on: []
    next_evidence: >-
      one bounded promotion contract selected from the current exact and interval gap,
      with an independent checker before any claim moves forward
  - id: BC-033
    purpose: tool_validation
    owner_focus: efficiency
    instances: [5, 10, 11]
    state: blocked
    priority: 2
    question: >-
      Can delta continuation, neighbour transfer, quality-diversity, and packing surgery
      be compared through one proposer interface at equal counted work?
    hypotheses: []
    budget: W3/W7 shaping only during this agenda unless identity and work accounting clear
    entry: >-
      a proposer interface, counted work-unit enforcement, and a measurement contract
      that does not call endpoint keys terminal components
    exit: >-
      A frozen interface and equal-work comparison contract, or a narrowed blocker that
      identifies which prerequisite owns the next implementation slice.
    bead: think-5vsz
    depends_on: []
    next_evidence: >-
      an interface decision linked to think-u97a and the equal-budget comparison harness
    note: >-
      Do not run a mechanism comparison at unequal wall-time or pair-test budgets, and
      do not infer basin frequency before the identity classifier is admissible.
  - id: BC-034
    purpose: research
    owner_focus: insight
    instances: [11, 100]
    state: ready
    priority: 2
    question: >-
      Which finite-transfer or asymptotic-waste obligation now has enough source and
      geometric support for a bounded proof step: theorem audit, effective constants,
      finite x0, synchronization, exact count, or boundary overhead?
    hypotheses: [H-037]
    budget: one checkpoint-selected W1/W3 or registered W6 mini-cycle of at most 75 minutes
    entry: >-
      the retained balance and local-sign results, with the remaining theorem and finite-
      transfer obligations kept distinct
    exit: >-
      One checked proof obligation, one falsifiable finite-transfer subclaim, or a typed
      blocker that changes the next priority without claiming the asymptotic exponent.
    bead: think-ykt7
    depends_on: []
    next_evidence: >-
      a source-faithful theorem fragment or finite-transfer calculation with every
      constant, branch, synchronization, and boundary assumption explicit
---
# Agenda 003 — Balanced Ten-Hour Research Program

This is the mutable execution layer for one ten-hour user-level research run.
It does not replace the basin confidence ladder, the constructive-enumeration agenda,
the hypothesis registry, experiment records, or beads.
It decides which bounded cell gets the clock next.

## Operating decision

Use two five-hour source sessions under one agenda and one integration bead.
The split is an operating choice, not an immutable limit: the current campaign runbook’s
eight-hour session bound is a default safety bound.
Five hours gives this run a stronger midpoint at which to review pipeline health,
throughput, evidence quality, and portfolio balance before committing the second half.

Session A must terminalize and preserve a 30-minute finalization reserve.
Session B gets a fresh absolute clock only after the midpoint decision.
If the agenda changes there, edit only future cells; never rewrite completed phase
history or a frozen experiment criterion.
One logbook entry may summarize both sessions after both are terminal.

## Known startup repair queue

BC-027 starts from observed state, in this order:

1. The merged-main Linux and macOS jobs both failed only because session 025 remained
   active after its deadline.
   Preserve that diagnosis, land the terminal session and cold-start reconciliation,
   regenerate the ledger, and do not repeat the expensive jobs merely to rediscover it.
2. Reproduce `think-c90t`: a failed subcommand inside a multi-command validation step
   may be followed by later commands and a misleading success.
   Add a mutation that fails the first subcommand, then repair first-failure propagation
   at the narrowest shared boundary.
3. If those repairs finish before their maximum allocations, reconcile stale research
   ownership before opening W6: terminal H-010 work under `think-bvy9`; the certificate
   pair `think-x9h8`/`think-0md2`; the promotion pair `think-n4f6`/`think-75ll`; the
   fractional-transversal pair `think-28sq`/`think-dsef`; and the already-discharged
   NumberField portion of `think-zcx4`. Do not close or merge an owner without reading
   its retained experiment or implementation evidence.
4. Confirm at least 4 GiB free before dependency sync or a full integration gate.
   Disk pressure is a launch blocker, not a reason to weaken or skip a check.

## Portfolio map

| Program | Present head | Later sequence | Artifact owner |
| --- | --- | --- | --- |
| Basin identity and local geometry | `BC-029`: `BC-010` / H-023 / exp-045 | `BC-011` classifier calibration, `BC-012` coverage, `BC-013` work scaling, then `BC-014` only after its blockers clear | `agenda-001`, H-023, `series-000`, `think-1s0h` |
| Constructive enumeration | `BC-030`: CG-010 target-free full cell | `BC-016` and `BC-017`; `BC-018` grammar freeze; `BC-025`, `BC-020`, and `BC-026`; target enumeration `BC-021`; exact restricted-class work `BC-022` last | `agenda-002`, X-003, `think-6mcd` and the existing cell beads |
| Sources and proof discovery | `BC-031`: highest-value missing primary | Source-faithful method extraction, unavoidable-set checks, and one bounded proof question | source-availability ledger, research notes, `think-4o6l` |
| Numerical-to-formal promotion | `BC-032`: smallest well-posed exact or interval boundary | Generic interval existence only after the selected system and checker are explicit | assurance plan, `think-75ll`; low-level certificate type remains `think-0md2` |
| Proposer and search diversity | `BC-033`: interface and equal-work contract | Delta continuation, neighbour transfer, MAP-Elites, billiard/inflation, and packing surgery | proposer plan, `think-5vsz`, `think-u97a`, `think-w6on`, `think-g2ko` |
| Asymptotic and finite transfer | `BC-034`: smallest remaining proof obligation | Full theorem audit, effective constants and finite x0, synchronization, exact count, and boundary overhead | H-037 and `think-ykt7` |

The first ten-hour run must give bounded attention to at least three independent
scientific programs.
No program gets a second consecutive target round until every other dependency-ready
program has received a bounded screen, unless the midpoint review records why one result
became dependency-critical.
No line runs for more than 75 minutes without a re-screen.

## Ten-hour agenda

The table allocates 10–30 minutes to each phase, and every allocation is a ceiling.
Finish sooner when the bounded output is complete; do not pad a small update, review, or
efficiency step to its scheduled maximum.
No continuation crosses 30 minutes without an inventory and explicit renewal.
The schedule is an agenda, not an unattended queue: checkpoints may reorder future rows,
but they may not alter completed history, frozen W6 criteria, or mathematical verdicts.

### Session A — repair, basin mini-cycle, and constructive framing

| Run time | Minutes | Workflow | Cell | Bounded output |
| --- | ---: | --- | --- | --- |
| 0:00–0:30 | 30 | W7 pipeline-improvement | BC-027 | Confirm safe disk headroom, type the merged-main failure, reconcile session 025 and generated views, and select the smallest remaining repair. |
| 0:30–0:50 | 20 | W2 factual-review | BC-027 | Independently audit the failure mechanism, trust boundary, and mutation control. Do not add theory. |
| 0:50–1:20 | 30 | W7 pipeline-improvement | BC-027 | Apply accepted corrections and make the first-failure path executable. |
| 1:20–1:45 | 25 | W7 pipeline-improvement | BC-027 | Run focused controls and the smallest integration surface; if green early, reconcile the highest-priority stale owner. Decide green or continue W7. |
| 1:45–2:00 | 15 | W5 efficiency-loop | BC-028 | Measure command, coordination, delegation, and repeated-gate time. Admit no optimization without a repayment case. |
| 2:00–2:20 | 20 | W3 insight-iteration | BC-029 | Re-screen exp-044 and shape exp-045’s mechanism, falsifier, and information value. |
| 2:20–2:50 | 30 | W6 research-loop | BC-029 | Preregister and freeze exp-045 criterion, regime, budget, stop, controls, and scale routes. |
| 2:50–3:20 | 30 | W6 research-loop | BC-029 | Build or execute the smallest retained instrument slice under the frozen contract. |
| 3:20–3:35 | 15 | W2 or W6 | BC-029 | Use W2 only for a promoted, disputed, high-risk, or changed trust boundary; otherwise perform guarded replay. |
| 3:35–3:45 | 10 | W3 insight-iteration | BC-029 | Explain what the evidence changed and shape, park, or kill the successor. Invalid instrumentation returns to W7. |
| 3:45–4:00 | 15 | W5 efficiency-loop | BC-028 | Compare throughput with the first checkpoint and re-rank only future cells. |
| 4:00–4:15 | 15 | W1 research-pass | BC-030 | Read the full-cell and corrected calibration evidence without consulting target geometry. |
| 4:15–4:30 | 15 | W3 insight-iteration | BC-030 | Shape CG-010’s smallest complete label, cap, pricing question, and falsifying mutations. |
| 4:30–5:00 | 30 | finalization | BC-027 | Reconcile records and views, run proportional gates, commit and push, sync beads, terminalize session A, and conduct the full midpoint review. |

Session B starts only if the midpoint review finds the pipeline safe and the next cells
coherent. Otherwise its first rows are prospectively reassigned to W7 repair or W5
measurement and the reason is recorded.

### Session B — constructive controls, a third program, and portfolio closeout

| Run time | Minutes | Workflow | Cell | Bounded output |
| --- | ---: | --- | --- | --- |
| 5:00–5:30 | 30 | W7 pipeline-improvement | BC-030 | Freeze and implement the target-free full-cell label and price vector. |
| 5:30–6:00 | 30 | W7 pipeline-improvement | BC-030 | Exercise one complete cell with positive and omitted-wall, omitted-axis, tie, cap, and source-isolation controls. |
| 6:00–6:15 | 15 | W2 factual-review | BC-030 | Independently audit full-cell completeness and accidental calibration lookup. |
| 6:15–6:30 | 15 | W3 insight-iteration | BC-030 | If a counterexample or cap structure is informative, shape the next grammar question; otherwise make the BC-016/017 readiness decision. |
| 6:30–6:45 | 15 | W5 efficiency-loop | BC-028 | Measure the second session’s actual throughput and admit at most one bounded W5 substitution if it repays the remaining clock. |
| 6:45–7:05 | 20 | W1 research-pass | BC-031 | Re-test the highest-value source route and retain the source or dated negative result. |
| 7:05–7:25 | 20 | W3 insight-iteration | BC-031/032/034 | Choose the highest-information third program from source, promotion/proof, or asymptotic evidence. Name one falsifiable question. |
| 7:25–7:55 | 30 | W6 or W7 | selected third program | Freeze a ready scientific round, or build the reusable instrument if the capability rather than the claim is still mutable. |
| 7:55–8:25 | 30 | W6 or W7 | selected third program | Execute and replay the bounded evidence cell; preserve negative, invalid, blocked, and unresolved outcomes. |
| 8:25–8:40 | 15 | W2 or W6 | selected third program | Audit material or high-risk output; otherwise use the time for guarded replay. |
| 8:40–8:50 | 10 | W3 insight-iteration | selected third program | Record the mechanism update and successor disposition after a valid result. |
| 8:50–9:05 | 15 | W5 efficiency-loop | BC-028 | Perform the final measured efficiency review and record what should change in the next agenda. |
| 9:05–9:20 | 15 | W3 insight-iteration | portfolio | Compare information gained across programs and rank the next ready cells, including the blocked proposer lane. |
| 9:20–9:30 | 10 | W1 or W3 | portfolio | Check the top successor’s evidence readiness; do not start work that cannot finish before finalization. |
| 9:30–10:00 | 30 | finalization | BC-027 | Terminalize session B, reconcile and regenerate shared views, run proportional gates, commit and push, sync beads, and write one logbook synthesis. |

## Midpoint and efficiency review

The five-hour review is substantive.
Record:

- pipeline status and the first unresolved failure, if any;
- completed evidence, invalid instruments, negative results, and W3 successors;
- total command wall time, longest command, repeated full/strict/row-jet commands, and
  time lost waiting for coordination or delegation;
- retained scientific artifacts per two-hour interval;
- whether the next five hours still span at least two independent programs; and
- the exact future rows being reordered, substituted, or dropped.

The shorter W5 checkpoints at about hours 2, 4, 6.5, and 9 are read-only measurements
unless they identify a blocker.
Enter implementation W5 only when a profile names the hot path, equivalence can be
guarded, and the expected time saved in the remaining horizon exceeds the build and
validation time. At most two W5 implementation slices may replace future rows; after the
second, return to research even if more optimization is possible.

## Insight loop

Every valid W6 result receives an immediate W3 pass before another target round on that
line.
The pass asks what prediction was wrong, what mechanism is now more plausible, what
observation would falsify it, and whether the next unit of time belongs to the same
program. Invalid instrumentation, source failures, and ordinary passing controls return
to W7, W1, or portfolio re-screening; they do not manufacture a scientific insight.

## Delegation

Use sub-agents for genuinely independent work that fits inside the active phase clock:
read-only source retrieval, an independent criterion or mutation audit, or disjoint
implementation with non-overlapping files.
Every delegation has a 10–30-minute delivery boundary and returns evidence, uncertainty,
and one next action.
The coordinator owns agenda mutation, shared artifacts, IDs, experiment verdicts,
integration, commits, pushes, and long or strict gates.
Do not have two agents write the same generated or coordination artifact.

## Artifact and series routing

- Create the two session artifacts at launch with actual start times, absolute
  deadlines, and enough `max_cycles` for 10-minute phases.
  Do not pre-create fictional clocks.
- Keep exp-045 in `series-000-smoke-and-calibration`. It is the current open series and
  owns comparable n=5 calibration and local-geometry work.
- Keep CG-010 and the BC-016/017/018 controls under agenda-002 and X-003. Do not create
  a constructive experiment series until the grammar and instrument are frozen.
- Route source work through `frontier/source-availability.yaml`, retained resources, and
  source-faithful research notes.
  A retrieval attempt is not an experiment.
- Route proof, promotion, proposer, and asymptotic work through their existing H, plan,
  and bead owners. Create a W6 record only after its criterion, regime, budget, and
  instrument are frozen.
- After both source sessions are terminal, create one `run-NNN` logbook entry for the
  ten-hour user-level run.
  The logbook summarizes; it does not replace source sessions or experiment verdicts.

## Claim boundaries

The `n = 1..100` atlas is calibration-only and cannot confirm H-044 or H-045. The 11,013
contact scaffolds carry no geometry or feasibility claim.
A fixed-angle local realization is not a packing-feasibility result.
No target `n = 11` constructive run starts before the grammar freeze.
Local n=5 path results do not decide whole-component identity, connectivity, or
frequency. Numerical promotion requires exact or rigorous interval evidence.
The unattended numerical runner remains **NO-GO**.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
