---
title: "X-016 — after 3.81: two managers, six gates, one proof boundary"
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-016
  title: "After 3.81: two managers, six gates, one proof boundary"
  date: '2026-09-05'
  author: Codex (coordinator), synthesizing three external-agent reviews and bounded local audits
  campaign: packing.squares
  brief: >-
    The owner asked for an aggressive strategy to raise the retained lower bound
    s(11) >= 3.81, a fully refreshed local source archive, and a 24-active-hour research plan
    designed for hierarchical parallel agents. This synthesis audits a three-model
    external review against the retained experiments and primary sources, separates
    valid near-term improvements from attractive but unsound shortcuts, and freezes a
    two-manager portfolio. Agenda-025 owns the exact fractional frontier; agenda-026
    owns density, stationarity, and Trump capture; agenda-024 alone owns integration,
    shared records, routing, and claim promotion. Six four-hour gates reallocate effort
    using fixed quantitative rules. The plan deliberately resumes existing state,
    packages already-computed local mathematics, and refuses global contact-graph or
    exact-cover searches until their proof semantics and branch prices pass controls.
  sources:
  - docs/project/reviews/review-2026-09-05-strategy-gpt-56-pro-gemini-grok.md
  - packing/resources/README.md
  - packing/resources/web/literature-refresh-2026-09-05/README.md
  - packing/resources/web/n17-lower-bounds-2026/README.md
  - packing/campaign/explorations/X-014-closing-from-both-ends.md
  - packing/campaign/explorations/X-015-the-map-and-the-three-programs.md
  - packing/campaign/agendas/agenda-021-three-numbers-and-a-wall.md
  - packing/campaign/agendas/agenda-022-the-conditional-route.md
  - packing/campaign/agendas/agenda-025-adaptive-fractional-frontier.md
  - packing/campaign/agendas/agenda-026-density-stationarity-and-trump-capture.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-060-h-064-n11-fractional-packing-floor.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-063-h-065-n11-near-tight-cell-census.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-064-h-063-two-threshold-class-program.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/bc-199-trump-isolation-radius.json
  - packing/campaign/series/series-000-smoke-and-calibration/results/bc-200-state-191-50.json
  - packing/cases/n11_fractional_certificate/t-018-proof-card.md
  - packing/cases/trump11/isolation_radius.py
  - packing/frontier/n-011.md
  - packing/resources/papers/dewar-2024-contacts-oriented-squares.raw.md
  - packing/resources/papers/donev-connelly-stillinger-torquato-2007-underconstrained-jammed-packings.raw.md
  - operating-rules.md
  proposes: [H-070, H-090, H-091, H-093, H-094, H-095, H-096, H-097, H-098, H-099, H-100, H-101, H-102, H-103]
---
# X-016 — After 3.81: Two Managers, Six Gates, One Proof Boundary

## Verdict

**2026-09-06 endpoint correction.** `T-022` now records
`s(11) >= 38100*sqrt(8100042893309449)/899996306539 = 3.810025723614703...` as a weak
limit corollary of the retained `381/100` certificate and a sharpened containment lemma.
It is not an endpoint certificate and did not change this plan’s `3.82` experimental
target or its proof boundary.

**Planning status.** The launch assignments, six-gate schedule, and next-entry language
below are historical design provenance.
The current authority is the
[T+2-to-T+10 continuation addendum](../../../docs/project/handoff-2026-09-06-post-381-t2-t10-continuation.md),
the single current cold-review entry point for the partially completed portfolio.
In particular, the older BC-215 and BC-219 preflight routes are not live scheduling
authority.

The next 24 active portfolio hours should run two research programs in parallel:

1. push the exact one-body certificate with direction-dependent witness cores while
   closing the retained 3.82 primal/dual bracket; and
2. turn the existing Trump neighborhood computation into a reviewable local theorem
   while trying to kill or justify the full-size density route cheaply.

These are complementary.
The first is the likeliest route to another published decimal rung.
The second develops the two ends needed for an exact-value proof: a quantified local
neighborhood and a global language capable of sending every survivor into it.
The coordinator, not either manager, owns the proof boundary between them.

Do not spend this block on a generic contact-graph atlas, a broad `n = 11` exact-cover
tree, a repeat of the two-threshold angle classes, or another dense sweep from an empty
state. Each has either failed its present gate or lacks a sound completeness object.

## Time Accounting

The 24-hour horizon estimates active research progress under continuous availability.
It is not a wall-clock deadline: interrupted tasks, unavailable hosts, usage or quota
pauses, approval waits, handoff setup, tool outages, and recovery from those events do
not consume the agenda.
Agenda-024 owns the precise clock: each shared gate waits for its prerequisite packets
and planned active allocations, even if calendar time has advanced further.

Parallel managers share this active schedule clock; their labor is also summed
separately as `agent_minutes`. Actual command wall time and CPU time remain evidence and
must still be reported.
Frozen CPU-hour and command timeboxes keep their own preregistered rules, so an
operational pause is not scientific compute and a result cannot earn a retroactive
extension. Twenty-four active hours is a replanning point, not a stop condition;
mechanical validation and closeout may continue afterward.

## Working definitions

This plan joins proof ideas that operate on different mathematical objects.
The definitions below are part of the contract: a later agent should be able to tell
what a proposed calculation would establish without reconstructing the terminology from
the agendas.

### Proof layers and fractional objects

| Term | Meaning in this exploration |
| --- | --- |
| **one-body measure** | A nonnegative measure on the container tested against one admissible witness square at a time. If every witness has mass at least one and the container has total mass below eleven, eleven disjoint witnesses cannot exist. |
| **unconditional one-body measure** | One measure whose lower-mass condition holds for every admissible centre and orientation. It can enter the counting proof without first classifying a packing. |
| **conditional one-body measure** | A measure whose lower-mass condition holds only on a stated pose or composition class. It becomes a proof component only after a complete case split assigns every possible packing to a covered class. |
| **integral configuration argument** | An argument whose variables describe a whole eleven-square placement, so it may use compatibility among different squares. It is not a stronger row in the one-body LP; it is a different proof object. |
| **compatibility constraint** | A condition involving several placement choices. Clique rows exclude mutually conflicting selections, odd-cycle rows strengthen pairwise conflict constraints around an odd cycle, Hall rows detect too few compatible regions for the required assignments, and cell-hyperedge rows encode a forbidden combination spanning several pose cells. Their soundness depends on the integral configuration model that gives those selections meaning. |
| **direction net and angle cell** | The direction net is the finite set of orientations checked by a certificate. Adjacent net directions bound a closed angle interval, or angle cell, whose every orientation must be handled by a proved containment rule. Sampling representatives is not enough. |
| **witness core and `B_k`** | A witness core is the smaller region placed strictly inside each packed unit square before mass is counted. In the current certificate it is one concentric square of side `B`; an adaptive certificate gives angle cell `k` its own largest proved-safe side `B_k`. |
| **angle-cell kernel** | A rationally described inner region contained in every unit square whose orientation lies in one angle cell. It may retain more useful area than any common concentric square, but it needs a new exact containment and centre-sweep proof. |
| **segment measure** | A nonnegative measure supported on finitely many line segments. The mass captured by a moving square changes continuously and piecewise algebraically, so neither the atomic event sweep nor an area-density verifier decides it without new boundary rules. |
| **full-size absolutely continuous density** | A nonnegative integrable function spread over area in the container, tested by integrating over the full unit square rather than a shrunken core. A total mass below eleven with coverage at least one for every pose would prove a lower bound because shared square boundaries have area measure zero; sampled coverage is only a candidate. |
| **continuum verifier** | A proof procedure that decides a universal claim over every admissible centre, orientation, and wall stratum. A grid or finite pose sample is a proposer unless a containment, interval, or finite-cell theorem closes the gaps between samples. |
| **support prior and restricted support** | A support prior biases a generator toward promising atom locations, such as an inset grid. A certificate found on that restricted set is sound once verified; failure there says nothing about measures using excluded locations. |
| **unrestricted column generation** | An LP loop that alternates solving on the current finite rows and columns with pricing searches for a violated pose row or an improving atom column anywhere in the allowed container. Releasing an inset seed means the pricing oracle may add wall-near support again. |
| **`nu*` / `tau*` bracket** | `nu*` is the fractional-packing optimum and `tau*` the fractional-covering optimum for the declared one-body formulation, with `nu* <= tau*`. A verified packing family supplies a lower endpoint and a row-converged covering solution an upper endpoint. `tau* < 11` can yield the desired measure; `nu* >= 11` rules out that formulation at the tested side. Intermediate values are optimization evidence, not a new bound on `s(11)`. |

### Typed stationarity and local closure

| Term | Meaning in this exploration |
| --- | --- |
| **support branch** | One smooth piece of the disjunctive nonoverlap and containment system. For each square pair it fixes the owner square, one local supporting axis, and the separation order; for a wall it fixes the responsible corner and wall. Angle charts are part of the branch. |
| **contact graph** | The graph with a vertex for each square and an edge when two squares touch; boundary contacts may be represented by extra wall vertices. It records incidence but not the geometric equation that realizes a touch. |
| **typed contact** | A contact together with the data needed to write its branch equation: corner-edge, edge-edge, or wall feature; owner square and supporting axis; separation order and sign; and any angle-chart or wall identity. Different types on the same abstract edge generally produce different equations. |
| **active constraint or row** | A branch inequality `g_j(z) >= 0` that holds with equality at the candidate, `g_j(z) = 0`. The complete branch list, its active subset, and the multiplier support below are three different objects. |
| **Fritz–John stationarity** | A necessary first-order condition for a branch minimum. With side objective `L`, there are nonnegative numbers `alpha` and `lambda_j`, not all zero, such that `alpha grad L - sum_j lambda_j grad g_j = 0` and `lambda_j g_j = 0`. It proposes stationary candidates; it does not prove feasibility, local minimality, rigidity, or global optimality. |
| **normal, or ordinary, Fritz–John branch** | The case `alpha > 0`. Rescaling makes the objective multiplier one and gives a Karush–Kuhn–Tucker multiplier certificate. “Ordinary” describes this multiplier state, not a constraint qualification or a claim that the stationary point is an optimum. |
| **abnormal Fritz–John branch** | The case `alpha = 0`, where a nontrivial dependence among active constraint gradients satisfies stationarity without using the objective gradient. One geometry may admit both normal and abnormal certificates. Only a proved constraint qualification that rules out the abnormal case on every affected branch permits the enumeration to omit it. |
| **constraint qualification** | A local regularity hypothesis on the active constraints that makes KKT necessary. Because tied square contacts can violate such hypotheses, this plan retains abnormal branches unless the qualification is proved rather than assumed. |
| **feature tie** | A geometry at which two or more support descriptions are simultaneously valid, such as a corner-corner touch admitted by several owner-axis choices or a corner meeting two wall strata. It is a branch point in the nonsmooth model, so every applicable typed branch must be retained. |
| **zero multiplier** | An active constraint whose Fritz–John/KKT coefficient is zero in the selected stationary certificate. The contact is geometrically tight but carries no first-order balance in that certificate; it must not be deleted merely because it is absent from the positive multiplier support. |
| **positive multiplier support** | The active rows with `lambda_j > 0`. This is the force- or stress-carrying part of one multiplier certificate, not the whole contact set and not necessarily a connected graph. |
| **rattler** | A square, or a cluster of squares, that can move locally inside a cage while a remainder stays jammed. It may be absent from positive multiplier support, but its variables and every nonoverlap and wall inequality remain part of the global feasibility problem. |
| **typed stationary backbone** | This project’s proposed finite record for one stationary branch: the typed contacts and walls, support orders, angle charts, active and inactive rows, positive and zero multiplier states, symmetry labels, and rattler attachments, together with the continuous equations they index. It is broader than the jamming literature’s “backbone,” which usually means the rigid or force-carrying remainder after rattlers are removed. |
| **anchored chart and local isolation** | The retained anchored chart fixes the container as `[0,L]^2` with one corner at the origin and represents each labelled square by its centre and angle; finite `D4` and relabelling copies are handled separately. Local isolation means that a proved neighborhood in that declared chart contains no other feasible configuration at the tested side. It is a local statement and does not exclude a better packing elsewhere. |
| **LP/Farkas, interval, and exact-algebra leaves** | Once angles and branch choices are exact, the centre-and-side problem is linear: an exact LP can realize it, while a Farkas certificate proves infeasibility by an exact nonnegative combination of rows. Interval exclusion proves that a whole angle box has no solution. Exact algebra or root isolation is reserved for the stationary leaves those cheaper decisions cannot close. |

### Exact-cover language

| Term | Meaning in this exploration |
| --- | --- |
| **event cell** | A region of witness centres on which an atomic measure covers the same set of atoms and therefore has constant mass. This is not a configuration-space support branch. |
| **near-tight classifier** | A rule, derived from a valid covering measure of total mass `M >= 11`, that keeps only event cells whose covered mass is close enough to one to occur in an eleven-square equality or near-equality case. Without the measure and its proved threshold, “near-tight” is only a heuristic label. |
| **exact-cover tree** | A complete discrete search over compatible event-cell choices for all eleven squares, including pairwise nonoverlap of the corresponding enclosing unit squares. A **survivor** is an unresolved node or component after sound pruning, not evidence that a packing exists. |

## What the outside review got right

The most valuable distinction in the contributed review is between three proof layers:

- an unconditional one-body measure, where every selected inner witness carries mass at
  least one;
- a conditional one-body measure, valid only after a proved case split fixes the
  composition or admissible pose domain; and
- an integral configuration argument, where compatibility among several placements is
  part of the object.

Clique, odd-cycle, Hall, and cell-hyperedge constraints can strengthen the third layer.
They cannot be inserted as weaker replacement rows in the current one-body covering LP
and still support its counting proof.
Direction-specific measures are similarly valid only after a composition theorem or
through one common measure with class thresholds.

The review is also right that the existing theorem can be strengthened before it is
abandoned.
A direction-dependent inscribed side `B_k` uses each angle cell’s actual worst
mismatch instead of charging every direction for the coarsest net gap.
Exact angle-cell kernels, segment measures, and full-size absolutely continuous
densities are progressively more expressive resource languages.
Each successive language needs a new continuum verifier; none is a parameter toggle.

## Corrections that change the plan

### The margin sweep is a generator

Massaccesi reports sweeping the doubled inset margin at `L = 4.5000`; only `M = 1.5500`
among the 0.05-spaced trials gave mass below 17. The retained published generator fixes
that value rather than containing the sweep wrapper.
The final verifier, which was retained and replayed locally, uses `L = 4.5058`,
`M = 1.5513`. The reported sweep is therefore a useful heuristic prior, not a reproduced
search. It does not show that the unrestricted optimum excludes the walls.
A restricted support succeeds soundly and fails silently.

Agenda-025 therefore gives margin seeding 30 minutes and always follows it with
unrestricted column generation.
It survives only if the released run beats the unrestricted control.

### A contact graph is not a finite atlas

For rotated squares, a contact needs feature and sign data.
Vertex-edge, edge-edge, wall feature, owner axis, and ordering choices lead to different
equations; generic contact is not a center distance of one.
An abstract graph still has a continuous semialgebraic embedding problem, and neither
planarity nor the proposed degree bounds has been proved.

The credible object is a typed stationary backbone, including normal (ordinary) and
abnormal Fritz–John branches, feature ties, zero multipliers, and rattlers.
Centres can then be eliminated by LP/Farkas certificates, with interval checks and exact
algebra reserved for surviving leaves.
Agenda-026 writes and prices that object against Trump, the globally classified
`n = 3, 4` optimum spaces, and the exact local-rigidity system at `n = 5`. The `n = 5`
control is not a global all-optima classification.
It does not enumerate the global `n = 11` atlas in this block.

### Trump is a local endpoint, not a global theorem

Trump’s packing is the verified known-best construction and is locally isolated in the
retained anchored chart.
It is not known to be globally optimal.
BC-199 already computed a uniform radius at least `0.0023089`, a per-row radius at least
`808514697/200000000000`, and `C <= 12.873063` across 128 branches.
The next work is to state and independently review the theorem these constants support,
not to recompute the constants.

### Exact cover has not earned a tree

The current `epsilon = 0.05` census leaves 23,112,904 of 567,130,649 pose cells in
22,132 components. That is a diagnostic, not a tractable proof tree.
Moreover, an `epsilon = M - 11` classifier is meaningful only when the covering measure
has `M >= 11`. The retained exact 3.82 object is a fractional-packing floor
`nu* >= 9.907905`; the row-converged `tau* <= 11.055617` objective has no frozen exact
covering measure, so no valid `M >= 11` classifier input exists yet.
BC-248 remains blocked until a valid near-11 measure leaves at most ten percent of the
present survivors and a complete search is priced below four CPU-hours.

## Evidence at the handoff

| Evidence | Current reading | Next action |
| --- | --- | --- |
| Retained bound | `s(11) >= 38100*sqrt(8100042893309449)/899996306539` by T-022’s weak limit corollary | This is only the uniform fixed-B, single-core strict-containment supremum; direction-specific cores and coverage-cell geometry remain open. |
| 3.82 one-body bracket | `9.907905 <= nu* <= tau* <= 11.055617` | Resume `bc-200-state-191-50.json`; do not restart. |
| 3.85 floor | `nu* >= 9.049860` | Too loose to route the first block. |
| Adaptive `B_k` | Valid lemma shape, unimplemented | Formalize certificate semantics and build exact controls first. |
| Two-threshold classes | 11.606445 on Trump; route ceiling 3.876681 | Retire this class language; a successor must be materially nonconvex or richer. |
| Trump isolation | All 128 retained branches agree on a positive local radius | Package and review the theorem packet. |
| Full-size density | Potentially sound only after its measure class, boundary terms, and weak dual are proved; no instrument | Run a weak-dual kill before inverse design. |
| Contact atlas | Current atlas is descriptive and capped; generic proposal is unsound | Specify typed stationary backbones and price controls only. |

The interval between 3.81 and the verified construction at approximately 3.87708 is
large enough that another decimal rung and an exact-value program are different
objectives. The portfolio supports both without confusing their evidence.

## The Agent Hierarchy

| Role | Agenda and bead | Exclusive work | Must not do |
| --- | --- | --- | --- |
| Coordinator | agenda-024; `think-xk9j` | Shared ledgers and maps, hypothesis and experiment creation, `X-017..019`, ID allocation, validation, integration, commits, PR updates, routing, retention, and claim promotion | Run a manager’s experimental loop while also judging it |
| Fractional manager | agenda-025; `think-wess` | `BC-230..239`, `H-070..079`, `exp-070..089`; fractional code, named drivers, tests, results, and its child agenda | Edit shared campaign/frontier records, change criteria, retain a candidate, or consume closure IDs |
| Closure manager | agenda-026; `think-j7rm` | `BC-240..249`, `H-080..089`, `exp-090..109`; new density/stationary modules, Trump cases, named drivers, tests, results, and its child agenda | Edit shared campaign/frontier records, change criteria, retain a candidate, or consume fractional IDs |

For Codex delegates, the coordinator sets the reasoning level in each handoff.
Use `max` for mathematical insight, strategy, theorem design, proof-boundary decisions,
acceptance or rejection of evidence, and consequential integration judgement.
Use `xhigh` for source-distinct review, bounded implementation, and editorial work that
still requires nontrivial judgement; use `high` for deterministic replay, manifest and
value checks, formatting, and other well-specified mechanical work.
Speed is not a reason to lower the reasoning level on a mathematical decision.
The assigned level and task boundary belong in the dispatch and gate packet so a later
coordinator can audit both.

The manager ranges are disjoint on purpose.
PR #87 owns agenda-023 and `BC-214..218`. `H-066..069` and `exp-065..069` remain
quarantined until that sibling branch is terminal.
Neither manager may create an exploration record.
`X-016` is this launch synthesis, and the coordinator reserves `X-017..019` for later
cross-program gate syntheses after rechecking upstream for a collision.
Gaps are cheaper than resolving experiment identities after parallel worktrees diverge.

Managers may delegate a bounded BC to workers.
A worker inherits the manager’s write scope, reports evidence to the manager, and may
not push, operate `tbd`, edit a generated or shared record, change an accept rule, or
promote a mathematical claim.
In a shared checkout, managers and workers return uncommitted patches.
In an isolated worktree, a manager may make local transport commits containing only
owned paths; the coordinator reviews and integrates them.
The coordinator is the only allocator: a manager can propose a hypothesis or experiment
in a gate packet, but the coordinator creates it and freezes its criteria before
execution.
The manager may then append commands and outcomes within that allocated record
without changing its identity or decision rule.

## Frozen resource packets

Every agent receives common instructions rather than rediscovering them:

- the exact PR #83 base SHA, the status and reserved namespace of PR #87, and any
  operating rules that land before launch;
- this synthesis, the audited outside review, agenda-021 and agenda-022 outcomes,
  `SYNOPSIS.md`, `packing/frontier/n-011.md`, the current ledger and ideas table;
- the Python 3.14 rule, validation entry points, ID blocks, write exclusions, checkpoint
  format, four-hour packet format, and central retention boundary; and
- the local literature refresh packet, including exact arXiv and OpenAlex query
  receipts, the retained Crossref response, and the explicit limits of every method
  analogue.

The fractional packet additionally freezes:

- T-018’s certificate and proof card;
- exp-060’s 3.82 packing floor, `bc-200-state-191-50.json`, exp-063’s census, and
  exp-064’s negative class result;
- the column-generation, cutting, checkpoint, exact-sweep, and interval-decision tools;
- Massaccesi’s article, verifier, margin semantics, and retained control; and
- the retained `n = 11` and `n = 12` positive certificates plus known-feasible negative
  controls.

The closure packet additionally freezes:

- exp-013, `bc-199-trump-isolation-radius.json`, the radius tool and its tests;
- X-014, Trump’s exact witness and frontier record, and the PR #44 atlas review;
- exp-064’s negative class result and the relevant agenda-018 context; and
- Connelly–Whiteley, Donev et al., Dewar, and Kingbird as qualified method sources,
  explicitly labelled as analogues rather than transferred theorems.

No manager should need the network to begin a cell.
A missing source outside these packets is a gate request, not permission to base a claim
on a snippet.

## Six four-hour gates

Managers submit a packet 15 minutes before hours 4, 8, 12, 16, 20, and 24 containing:

- each BC’s disposition and exact checkpoint path;
- the frozen base SHA, transport identity, and a changed-path manifest;
- exact checker receipts and every invalid or guard-refused run;
- `active_portfolio_minutes`, `agent_minutes`, and actual command wall and CPU cost;
- the proposed next slices and any proposed hypothesis; and
- shared-code or cross-program requests.

At each gate the coordinator freezes new launches, validates the fractional packet and
then the closure packet, checks whole-set ID and reference uniqueness, integrates one
manager at a time, regenerates shared views once, records the routing decision, commits,
and freezes the next block.
Hosted checks run asynchronously; managers use that time for disjoint read-only or
theory work rather than polling.

| Gate | Decision |
| --- | --- |
| Hour 4 | Are instruments, theorem statements, controls, and refusal paths ready? |
| Hour 8 | What are the first exact measurements, and did any route earn more compute? |
| Hour 12 | Which program has the best verified expected gain per hour? Apply the portfolio pivot. |
| Hour 16 | Is there a candidate or deep theorem packet worth independent exactification? |
| Hour 20 | Freeze new instruments; allocate remaining time to exactification and replication. |
| Hour 24 | Apply W10 dispositions, run the documentation and full validation passes, and select—but do not execute—one next entry. |

Twenty-four hours is a replanning checkpoint, not a self-declared stop condition.
A time-limited cell preserves its checkpoint, cost, reopen condition, and next routed
cell.
Work continues under OR-8 unless the operator stops it, every route is disposed, or
one external blocker stops all lanes.

## Routing rules fixed before launch

### Fractional route

- Any exact mass-below-11 certificate at rational `L > 3.81` stops variant
  proliferation. Roughly 75 percent of the next block goes to frozen-byte exactification
  and a source-distinct replay.
  No public claim moves before the central gate.
- The retained 3.82 bracket continues only if one four-CPU-hour block reduces its width
  by at least 25 percent.
  Otherwise preserve the checkpoint and move that capacity to adaptive cores.
- Adaptive `B_k` continues if it certifies a rung or removes at least 25 percent of the
  same-support excess over 11 exactly.
  Otherwise route to the angle-cell kernel.
- An inset-margin run is always followed by unrestricted support release.
  A failed inset family refutes nothing.
- The kernel route continues only after exact rational containment, both retained
  controls, and a decision cost no worse than four times its square-core control.
  Segment measures cannot open before the kernel’s disposition and a costed verifier
  design.

### Closure route

- Any disagreement in the 128-branch BC-199 replay blocks local capture.
  Agreement promotes the theorem packet for review; it does not invite a new radius
  search.
- One rigorously feasible full-size fractional packing with value above 11 at Trump’s
  side kills the proposed equality density by weak duality.
  Failure to find one proves nothing.
  Any density candidate needs a continuum minimum proof and central exact replay.
- A global stationary enumeration cannot open until Trump, the complete `n = 3, 4`
  controls, and the local `n = 5` representability control pass; abnormal Fritz–John or
  a proved constraint qualification is explicit; and the measured branch price fits a
  later budget. Graph-only enumeration, assumed planarity, or center-distance-one
  contacts are guard refusals.
- Exact cover opens only with a valid measure of mass at least 11, no more than
  2,311,290 of the present 23,112,904 survivors, and a priced complete run below four
  CPU-hours. Its configurations must enforce closed unit squares whose interiors are
  pairwise disjoint; boundary touching is allowed.

Three consecutive invalid guard refusals or crashes stop that manager.
Any duplicate ID, dangling reference, unexpected standing-best change, or shared-record
mutation freezes both managers until the coordinator resolves it.
Accept criteria never move mid-block.

## Launch order

The first block opens three fractional cells in parallel: the manager writes the
adaptive theorem contract while supervising the retained 3.82 continuation and the
margin-seed screen as background single-core processes.
The closure manager writes the full-size density and typed-stationarity contracts while
the portfolio’s one floating agent drafts the Trump theorem packet.
No BC-241 review begins before the coordinator commits BC-240 at the hour-four gate.

This ordering spends the first four hours on existing evidence and cheap discriminators.
It keeps a direct-bound candidate, a local theorem, and a high-upside alternative in
flight without paying for the global trees that none of them has earned.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
