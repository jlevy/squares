# Feature: Unattended Square-Packing Research Readiness

**Date:** 2026-08-23; rebuilt from the merged baseline on 2026-08-24

**Author:** Codex agents

**Status:** Active agenda; numeric launch is **NO-GO**

## Outcome

There is enough organized work for an autonomous **agent** to make useful progress for
eight or twenty-four hours.
There is not yet enough admissible, executable numerical work for
[`campaign/runner.py`](../../../../campaign/runner.py) to run unattended.

The distinction matters:

- the persistent agent goal is the controller for research, implementation, review,
  delegation, verification, recording, and choosing the next ready bead;
- `runner.py` is only the executor for preregistered numerical cells whose instruments,
  evaluators, budgets, and validity paths already exist.

The runner currently reports one executable recipe, H-017. On the recorded local M1 Pro
rate it is about **2.8 hours** of work, not a night.
More importantly, D-044 and D-046 remain open: the current path trusts producer-reported
validity and does not yet form a closed, checked lifecycle.
The scientifically admissible unattended queue is therefore zero.

This document is the single launch agenda.
It supersedes the earlier “build Half A, then drain the census” schedule and the two
older overlapping overnight epics.
Existing beads retain their history and now sit under `think-ydus`.

## What success means

The goal is not to keep a machine busy.
It is to make the next morning’s state more truthful, more informative, or more capable
without requiring a person to reconstruct what happened.

An eight-hour session is ready when:

1. a persistent agent can drain dependency-ready research and implementation beads,
   committing bounded evidence-backed changes as it goes; and
2. if numerical work is delegated to the runner, its **measured unresolved-cell queue**
   has at least ten hours of useful work on the target host and every cell passes the
   launch gate below.

A twenty-four-hour session raises the second threshold to thirty hours.
The 1.25× reserve absorbs runtime variance and finalization without changing criteria at
night.

## The four focuses

Agents normally own one focus at a time.
The handoffs between them are explicit because one dimension cannot substitute for
another.

| Focus | Governing question | Durable outputs | Veto |
| --- | --- | --- | --- |
| **Correctness** | Is the mathematical or computational claim supported? | primary-source notes, certificates, independent checks, soundness defects | may reject a promotion or result |
| **Process** | Can another agent reconstruct the decision and continue it? | hypothesis, experiment, session and defect artifacts; beads and generated views | may reject an unregistered or irreproducible run |
| **Insight** | Which sharp experiment or proof idea buys the most information? | hypotheses, open questions, mechanism metrics, strategy changes | may reject low-information scaling |
| **Efficiency** | What measured bottleneck limits useful iterations? | timings, budgets, profiles, resumable execution, visualizations | may reject unmeasured infrastructure work |

Visualization belongs to both Insight and Efficiency: the infrastructure must render the
atlas, ambiguity graph, discovery curve, and continuation tree, while the research work
decides which views expose mechanisms rather than decorate a report.

## Current measured state

Measured on the merged PR 15 baseline unless stated otherwise:

| Item | Current fact | Consequence |
| --- | --- | --- |
| Scientific registry | 24 artifacts: H-001 through H-024, including two explicit open questions | The standing review’s fifteen hypotheses no longer live only in prose |
| Recorded campaign | 11 rounds, 275 agent-minutes, 1,380.674 machine seconds (23.0 wall-minutes) | The historical loop is about 12:1 agent-bound |
| Operational runner queue | one H-017 cell, five seeds, recipe timebox 8h | “Queue nonempty” is not an overnight-readiness test |
| Estimated H-017 runtime | 2.80h at 39.7M moves/s locally; 7.46h at the recorded 14.9M moves/s cloud rate | Target-host calibration is mandatory |
| Fast checks | status 0.22–0.24s; preflight 0.12s; ledger 0.23s; schemas 1.60s; engine selftest 1.43s | Orientation and focused feedback are already cheap |
| Normal gate | recent single runs 108–126s | Profile repeated samples before optimizing further |
| Canonicalizer | 0.098s at `n=7`, 7.91s at `n=9` in one audit | Likely census bottleneck; confirm under `think-xzew` before redesign |

The existing preflight is useful but not a launch decision.
It proves that its current guards fire and that at least one recipe is visible.
It does not independently verify a pose, price the queue, bind the session deadline, or
rehearse crash persistence.

## The scientific portfolio

The registry artifact is authoritative for each claim’s wording, metric, threshold,
regime, prerequisites, and status.
The table below is a routing view, not a second registry.

### First: define and validate the counted object

| Order | Artifact | Question | Why now | Runnable? |
| ---: | --- | --- | --- | --- |
| 1 | [H-023](../../../../campaign/hypotheses/H-023-n5-terminal-connectivity.md) | Which observed `n=5` endpoints are connected at the proved optimum? | Focused ambiguity at the first nontrivial census cell | No; local geometry study |
| 2 | [H-021](../../../../campaign/hypotheses/H-021-endpoint-identifiability.md) | Can the classifier resolve at least 95% of endpoint support through `n=8`? | Measurement-system gate; failure redirects the program | No; classifier and controls absent |
| 3 | [H-011](../../../../campaign/hypotheses/H-011-small-n-census.md) | Does unseen terminal-component mass fall below 0.05 by `n=8`? | Builds the atlas and tests whether census is viable | No; waits on identity, events and estimator |
| 4 | [H-007](../../../../campaign/hypotheses/H-007-saturation-curves.md) | Do preregistered coverage estimates predict held-out discovery? | Makes negative search results quantitative | No; waits on H-011 data |
| 5 | [H-012](../../../../campaign/hypotheses/H-012-record-basins-are-rare.md) | Is the record-to-modal attraction ratio below 0.1 under named `P/Q/E`? | Kills or supports the cartography premise directly | No; waits on H-011 plus `n=11` sampling |

H-009’s raw-to-canonical ratio and H-008’s stronger-verifier rejection rate are
mandatory companion measurements.
H-003’s contact-count predictor comes later and must use held-out data; contact count is
not component identity or a rigidity certificate.

### Search strategies after the measurement spine

| Priority | Artifact | Registered comparison | Gate or kill line |
| ---: | --- | --- | --- |
| 1 | [H-004](../../../../campaign/hypotheses/H-004-neighbor-transfer-seeding.md) | neighbor transfer versus cold starts at `n=11` | median best-side improvement at least 0.01; the old `n=12` side-4 target was vacuous |
| 1 | [H-013](../../../../campaign/hypotheses/H-013-delta-continuation.md) | continuation versus direct starts, `n=10` before `n=11` | retire as a discovery method if it cannot win on the proved gate |
| 1 | [H-001](../../../../campaign/hypotheses/H-001-angle-class-reduction.md) | angle-class proposer versus free-coordinate annealing | pass proved and oblique calibration before interpreting `n=11` |
| 2 | [H-015](../../../../campaign/hypotheses/H-015-map-elites-illumination.md) | quality diversity versus matched restarts | at least 1.5× certified components per pair-test |
| 2 | [H-005](../../../../campaign/hypotheses/H-005-m2-minus-3-construction.md) | analytic 3-4-5-tilt construction at `n=97` | analytic geometry first; no numerical rescue of a failed family |
| 3 | [H-014](../../../../campaign/hypotheses/H-014-superdisk-continuation.md) | circle-to-square continuation versus direct square starts | last because it alone needs a new geometry model |

H-024 separately tests the descriptive claim that verified record packings through
`n=30` use at most three orientation classes.
The primary `n=29` SVG is now a six-class counterexample candidate, so verify that one
pose before funding the full corpus sweep.
It neither proves nor is proved by H-001’s algorithmic performance; a refutation should
produce a successor about effective angular rank or compressibility.

H-017 remains a low-priority scaling fallback after the validity boundary is repaired.
H-016, H-018, H-019, and H-020 are resolved for their registered regimes and should not
be silently rerun as fresh hypotheses.

### Proof lane

| Priority | Artifact | Output | Boundary |
| ---: | --- | --- | --- |
| 1 | [H-010](../../../../campaign/hypotheses/H-010-stromquist-triple.md) | known escape, censored hard case, then independently checked PoseBox certificate | search saturation is never proof |
| 1 | [H-022](../../../../campaign/hypotheses/H-022-trump-local-geometry.md) | active-system rank/tangent evidence and an interval-local certificate or continuation witness | local geometry is distinct from global optimality |
| 2 | [H-006](../../../../campaign/hypotheses/H-006-lp-dual-unavoidable-sets.md) | quantitative, refinement-stable dual support for candidate loci | discretized LP generates proof objects; it proves no bound |

After H-010 validates the falsifier/certificate loop, the most tractable new theorem
targets are a certified restricted-orientation or contact family, a local certificate
around Trump’s packing, and a cutting-plane improvement to the `n=12` lower bound.
Each must become its own registered hypothesis before compute begins.

## The autonomous agent loop

This loop can run now under a persistent goal.

1. Read `tbd ready` and choose one P0 item from one focus.
2. State the intended evidence and stopping condition before implementation.
3. Delegate bounded mechanical work—formatting, lint repair, data extraction, repeated
   checks—while the primary agent owns mathematical and integration judgment.
4. Work in the smallest loop that bears on the change: source inspection, focused check,
   then the normal gate only at a real checkpoint.
5. Record any actual error in `defects.yaml` by its substantive class and link an open
   bead when work remains.
6. Update the hypothesis, experiment, or session artifact that owns the result; do not
   leave a conclusion in chat or a bead description alone.
7. Commit and push a bounded checkpoint, then re-read the ready queue.
   Stop or switch focus when the evidence demands a handoff.

For an eight-hour goal, take the first dependency-ready slice of H-023/H-021 and carry
it to a retained measurement or explicit blocker.
For a twenty-four-hour goal, continue through the classifier/event/evaluator contract
and one supervised H-011 cell.
Do not fill the time with H-017 merely because it is executable.

## The numeric runner launch gate

No unwatched numeric cell starts until every applicable line is true.

### Scientific admissibility

- [ ] The hypothesis and exact cell are registered before execution.
- [ ] The evaluator is typed for the hypothesis’s criterion; positive and negative
  fixtures have been watched passing and failing.
- [ ] The command archives full poses or content-addressed pose artifacts.
- [ ] A separate verifier recomputes containment and non-overlap from the archived pose.
- [ ] The actual engine selftest, binary digest, source revision, dirty state, host,
  seeds, and budget are recorded.
- [ ] Prerequisites are satisfied; an instrument-ready flag changes only with the
  implementation that makes it true.

### Lifecycle and persistence

- [ ] One cell maps to one experiment and one per-cell deadline.
- [ ] The session deadline bounds the round deadline; no fresh full timebox starts after
  most of the session is spent.
- [ ] Claim, execute, record, release, and terminal states enforce legal transitions.
- [ ] Guard failures, command crashes, timeouts, and persistence failures all count
  toward the three-consecutive-failure stop and leave a durable non-scientific outcome.
- [ ] Narrow checked commits persist claims before long compute, checkpoints at each
  seed or thirty minutes, terminal artifacts, releases, and the final report.
- [ ] The cooperative D-035 recovery path handles timeout and interruption without
  leaving a deliberate negative-control mutation.
  No hostile isolation is required.

### Rehearsal and capacity

- [ ] A cheap known-answer claim → execute → record → commit → report round passes under
  supervision on the shipped code.
- [ ] Invalid-pose, false-overlap, timeout, mid-round kill/release, three guard
  failures, three crashes, short-session budget, and failed-commit rehearsals reach the
  expected refusals.
- [ ] `./test.sh --strict` and the deep checks pass with zero skips from a clean
  checkout.
- [ ] Three representative cold/warm target-host calibrations retain p50/p95 runtime and
  the exact binary/toolchain fingerprint.
- [ ] The generated unresolved-cell queue costs at least 10h for an 8h session or 30h
  for a 24h session at p95.

The queue must be materialized by unresolved **cell**, not merely by hypothesis.
A multi-cell universal claim is accepted only after every cell passes and refuted when a
registered counterexample cell fails.
This corrects the current mismatch in which the schema permits several cells while
execution shares one deadline and the artifact names only the first.

## Stop rules

The agent or runner stops and records why when any of these occurs:

- queue empty or session budget exhausted;
- three consecutive guard, execution, or persistence failures;
- a known-answer control or independent verifier disagrees;
- the frontier or acceptance rule moved after preregistration;
- a result requires human mathematical judgment;
- the evidence invalidates the current strategy or counted object.

Thresholds, controls, tolerances, and evaluators do not adapt during an unattended
session. A result that passes mechanical clauses but needs judgment is held unresolved
for review.

## Morning artifacts

The handoff must be unique, durable, and committed.
It leads with:

1. **Needs review** — candidates, ambiguity, or mathematical judgments;
2. **What moved** — metric deltas against the standing baseline;
3. **What died** — rejected hypotheses, guard failures, crashes, or exhausted regimes;
4. **What ran** — exact cells, seeds, budgets, revisions, artifacts, and verdicts;
5. **Queue now** — recomputed after the final transition, priced on the same host;
6. **Health** — recovery, persistence, and gate status;
7. **Next action** — one dependency-ready bead and the evidence it needs.

`campaign/session-report.md` currently overwrites its predecessor and is not durable;
D-071 and `think-y37w` own that correction.

## Efficiency agenda

The optimization order follows measured leverage:

1. **Make one valuable scientific cell runnable.** An empty admissible queue has
   infinite effective overhead.
2. **Profile the complete agent and numeric loops** under `think-xzew`, including time
   in build, execute, analysis, record, recovery, and gates.
3. **Measure canonicalization scaling.** The observed `n=7` to `n=9` jump may dominate
   `n=10`; optimize only after representative profiles.
4. **Bind pair-test accounting** (`think-krqi`/`think-b4jc`) so proposer comparisons use
   the declared machine-independent currency.
5. **Reduce agent time per recorded round** toward ten minutes through recipes,
   generated views, and delegated mechanical checks.
6. **Then** evaluate sharding, cache reuse, or compiled verification against declared
   speedup and identical-output criteria.

Do not build fleet coordination, per-run worktrees, repository copies, generalized
leases, or caches for a one-item queue.
One runner plus a cooperative activity refusal is the intended architecture until
measured concurrency demand says otherwise.

## Bead map

The canonical readiness epic is `think-ydus`.

| Lane | Beads | Exit evidence |
| --- | --- | --- |
| Portfolio and agenda | `think-1sxv`, `think-isa3` | registry, idea board, exploration source and this spec reconcile |
| Counted object | `think-1s0h` → `think-0yo9`; `think-3szr`, `think-aans` | H-023/H-021 classification evidence and ambiguity bounds |
| Events and evaluator | `think-31k1`, `think-rrht`, `think-apwt`, `think-jxx8` | full observations, named `P/Q/E`, held-out coverage evaluator |
| Validity and lifecycle | `think-ldq2`, `think-97pp`, `think-5zwm`, `think-ouf0`, `think-osyp` | independent pose checks, real selftest, transitions, interruption and control rehearsals |
| Budget and reporting | `think-krqi`, `think-b4jc`, `think-kmn2`, `think-y37w`, `think-xzew` | pair-test budget, priced queue, durable report, measured loop |
| First supervised cell | `think-l4z5` | H-011 instrument and recipe become true together; one complete cell retained |
| Launch and morning | `think-4jnv`, `think-20z4` | all launch checks green, then reviewed morning artifact |

`think-tosv`, `think-z9jq`, and `think-srym` are closed as superseded scheduling
surfaces. Their open implementation children were reparented; no work was discarded.
The new H-024 corpus reconstruction is `think-w5rb` under the Insight focus.

## Revision history

- **2026-08-23:** first plan proposed a watched build half followed by an unattended
  H-011 census.
- **2026-08-24:** rebuilt after PR 15 merged.
  Corrected the historical total from ten rounds/16.4 wall-minutes to eleven rounds/23.0
  wall-minutes; recognized that one nominal eight-hour recipe is about 2.8 hours
  locally; separated the autonomous agent loop from the numeric runner; codified H-003
  through H-015 plus H-021 through H-024; and replaced a premature schedule with the
  explicit scientific, lifecycle, capacity, and morning-artifact gate above.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
