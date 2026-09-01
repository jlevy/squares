---
title: "agenda-013 — nine-hour autonomous W3/W6 research run and review"
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-013
  title: "Nine-hour autonomous W3/W6 research run and review"
  updated: '2026-09-01'
  status: active
  objective: >-
    Execute agenda-012 end to end during one owner-authorized nine-hour wall, on one pull
    request, with a durable result at every branch. Short W3 insight passes frame each
    lane and interpret each result; longer W6 research loops freeze, implement and test
    the selected claims. The first 150 minutes run BC-108, BC-109 and BC-110 concurrently.
    BC-122 then measures their research throughput and admits only an improvement that
    can repay itself inside the remaining wall. BC-111 spends 30 minutes checking their
    retained exits and routes exactly one
    180-minute continuation per lane: BC-112 or BC-116 for n = 17, BC-113 or BC-117 for
    n = 68, and BC-114 or BC-118 for the cross-scale lane. BC-119 reconciles those
    outcomes in 30 minutes, BC-120 gives three independent reviewers 90 minutes to replay
    and challenge them, and BC-121 spends the final 45 minutes on synthesis, validation,
    PR state and handoff. The committed wall is exactly 540 minutes.

    Each research block works in 15--30 minute cells and records artifact, result, guard
    and next step before another cell begins. Executed positive and negative outcomes are
    `complete`; only a guard firing before measurement is `stopped`. No lane invents a
    replacement target to consume spare time, no task closure becomes scientific success,
    and no review repairs a disagreement in prose. The pull request is updated at every
    wave boundary with the exact revision, branch cost, validation receipt, lane states
    and next entry points. The final checkpoint may leave a claim unresolved or a bead
    blocked; it may not extend the nine-hour wall.
  items:
  - id: BC-122
    purpose: tool_validation
    owner_focus: efficiency
    instances: [17, 50, 68]
    state: blocked
    priority: 0
    question: >-
      Which measured agent, coordination, validation, CI or tool bottleneck from the
      first wave can be removed soon enough to increase the remaining W6 throughput?
    hypotheses: []
    budget: >-
      One 15-minute W5 measurement slice after the first wave. During 0--5, extract
      per-lane cell count, artifact yield, rework, idle or coordination time and handoff
      defects from the three contemporaneous AgentSessions. During 5--10, compare
      validation, CI and repeated-tool wall times and name the dominant measured
      bottleneck. During 10--15, retain the baseline and repayment decision. At most one
      bounded implementation slice of 20 minutes may run concurrently with the next W3
      lane-shaping cells.
    entry: >-
      BC-108, BC-109 and BC-110 are terminal with session timestamps, command durations,
      retained artifact counts and exact revisions. The coordinator measures one common
      baseline and does not infer performance from subjective agent reports alone.
    exit: >-
      A durable W5 receipt naming throughput, dominant bottleneck, guard and one of two
      decisions: no change, or one bounded optimization whose predicted remaining-wall
      savings exceed its build and validation cost. Implementation requires a profiled
      hot path, an equivalence guard and a rollback seam. It may simplify coordination or
      tools but cannot weaken an evidence gate, alter a frozen experiment fixture or
      delay BC-111. BC-119 measures the resulting second-wave throughput whether or not
      a change was admitted. After retaining the decision, mark BC-122 `complete` and
      close think-iv3e with the measured W5 outcome, then mark agenda-012 BC-111 `ready`
      before claiming think-1dm8. A guard that prevents the measurement leaves BC-122
      `stopped`, keeps BC-111 and think-1dm8 blocked, and invokes agenda-013's repository-
      wide stop rather than bypassing the receipt.
    bead: think-iv3e
    depends_on: []
    blocked_on: >-
      BC-108, BC-109 and BC-110 in agenda-012 must be terminal with their session and
      timing receipts retained.
    workflows: [efficiency-loop]
    next_evidence: >-
      Blocked on the three first-wave exits. The coordinator owns the W5 receipt and any
      admitted shared-tool change; lane owners supply timestamps and artifact counts but
      do not optimize their own in-flight measurement.
  - id: BC-116
    purpose: research
    owner_focus: correctness
    instances: [17, 18, 19]
    state: blocked
    priority: 1
    question: >-
      If BC-108 disagrees with the published n = 17 certificate or stops on a guard, what
      is the smallest reproducible discrepancy and which evidence layer owns it?
    hypotheses: []
    budget: >-
      180 minutes in six 30-minute cells: freeze the smallest mismatch or guard and all
      source hashes; reproduce it through the source-faithful path; reproduce it through
      an implementation-independent scalar path; bisect to the first divergent angle or
      event cell; fire one source-faithful control and one mutation; retain the typed
      adjudication, validation receipt and handoff.
    entry: >-
      BC-108 is terminal without the all-invariant agreement required by BC-112, and
      BC-111 routes the n = 17 lane here. Before the coordinator removes think-9zgs's
      blocked hold, it marks BC-112 `stopped` and puts think-5q0v on `paused` hold with the
      same routing reason. The block starts from BC-108's exact revision and smallest
      retained discrepancy or premeasurement guard; it does not broaden into a new proof
      search.
    exit: >-
      A retained source-defect, implementation-defect, contract-defect, reproduced-
      agreement, or unresolved adjudication with the first divergent invariant and exact
      replay command. An executed adjudication marks BC-116 `complete`; a new guard before
      measurement marks it `stopped`. Neither result adopts the bound, transfers it to n =
      18 or 19, clears BC-115, or changes the frontier.
    bead: think-9zgs
    depends_on: []
    blocked_on: >-
      BC-111 must route the n = 17 lane away from BC-112 and explicitly remove the manual
      hold.
    workflows: [insight-iteration, research-loop, factual-review]
    next_evidence: >-
      Held `blocked`. If routed here, own the BC-108 case package and tests, the next free
      experiment/result record under packing/campaign/series/series-000-smoke-and-calibration/,
      and one AgentSession. Do not edit frontier records or generic certificate code.
    parallel_group: agenda013-second-wave-n17
  - id: BC-117
    purpose: tool_validation
    owner_focus: correctness
    instances: [68, 69]
    state: blocked
    priority: 1
    question: >-
      If BC-109 cannot freeze a child-independent compatible parent arm, which provenance,
      transform or serialization assumption is the smallest reproducible refusal?
    hypotheses: []
    budget: >-
      180 minutes in six 30-minute cells: freeze the refusal and hashes; reduce it to one
      parent and one smallest polygon fixture; test the SVG-to-unit-square transform on a
      synthetic exact square; test the implicated rounding/export model and a mutation;
      separate source limitation from instrument defect; retain the repair seam, typed
      refusal, validation and handoff.
    entry: >-
      BC-109 is terminal without a compatible, independently valid parent model selected
      from parent-only facts, and BC-111 routes the n = 68 lane here. Before removing
      think-t7v1's blocked hold, the coordinator marks BC-113 `stopped` and places
      think-gbkd on `paused` hold with the same reason. Raw Kingbird bytes remain
      ephemeral and every normalized fact follows the existing retention policy.
    exit: >-
      A deterministic known-answer fixture plus a typed provenance, affine-transform,
      serialization, pose-compatibility, or unresolved source limitation. An executed
      result marks BC-117 `complete`; a guard before measurement marks it `stopped`.
      H-051 remains undisposed, no surgery runs, and no child-qualified alternative model
      may rescue the arm.
    bead: think-t7v1
    depends_on: []
    blocked_on: >-
      BC-111 must route the precision lane away from BC-113 and explicitly remove the
      manual hold.
    workflows: [insight-iteration, pipeline-improvement, research-loop, factual-review]
    next_evidence: >-
      Held `blocked`. If routed here, own
      packing/cases/unitsquare_precision/refusal/, the implicated tests in
      packing/tests/test_unitsquare_precision.py, one AgentSession, and no H-051 result
      file. Preserve all parent-source retention constraints.
    parallel_group: agenda013-second-wave-n68
  - id: BC-118
    purpose: tool_validation
    owner_focus: correctness
    instances: [19, 50]
    state: blocked
    priority: 1
    question: >-
      If n = 50 does not become an exact cross-scale control, is the limiting seam source
      availability, representation, verifier correctness or priced reconstruction cost?
    hypotheses: []
    budget: >-
      180 minutes in six 30-minute cells: freeze BC-110's typed refusal; select exactly
      one dispatch branch; retain the smallest deterministic fixture; replay the n = 19
      mechanism-matched control; repair or bound the selected seam; fire one mutation;
      record the resulting candidate or refusal, validation and handoff.
    entry: >-
      BC-110 is terminal without the exact verified n = 50 control required by BC-114,
      and BC-111 routes the cross-scale lane here. The coordinator records exactly one
      dispatch before removing think-8pjf's blocked hold: E1 source/provenance absence, E2
      representation mismatch, E3 verifier defect, or E4 priced exhaustion. It marks
      BC-114 `stopped` and puts think-dao9 on `paused` hold with the same reason.
    exit: >-
      One replayable seam result with a mechanism-matched control and mutation: repaired
      candidate for later adoption, typed source/representation/verifier refusal, priced
      ceiling, or unresolved result. An executed result marks BC-118 `complete`; a guard
      before measurement marks it `stopped`. This block does not silently update the n =
      50 frontier or switch to n = 39 or 54.
    bead: think-8pjf
    depends_on: []
    blocked_on: >-
      BC-111 must route the cross-scale lane away from BC-114, name one refusal dispatch,
      and explicitly remove the manual hold.
    workflows: [insight-iteration, pipeline-improvement, research-loop]
    next_evidence: >-
      Held `blocked`. If routed here, own packing/cases/n050_exact/,
      packing/tests/test_n050_exact.py, one next-free experiment/result record if a
      measurement executes, and one AgentSession. Shared frontier files remain untouched.
    parallel_group: agenda013-second-wave-scale
  - id: BC-119
    purpose: research
    owner_focus: process
    instances: [17, 39, 50, 54, 68]
    state: blocked
    priority: 0
    question: >-
      Are all three second-wave outcomes terminal, internally consistent and ready for an
      independent review at one exact revision?
    hypotheses: []
    budget: >-
      30 minutes: 0--10 run the second W5 measurement against BC-122's baseline and
      record whether the admitted change, if any, improved research-loop throughput;
      10--20 reconcile one terminal continuation per lane and every sibling hold; 20--30
      freeze the revision-keyed review packets, update rows and beads, regenerate the map
      and ledger, sync tbd, and make BC-120 ready.
    entry: >-
      BC-111 is complete, and exactly one member of each pair is terminal with retained
      evidence: BC-112 or BC-116, BC-113 or BC-117, and BC-114 or BC-118. Each unselected
      sibling is `stopped` with its bead on `paused` hold, every selected task bead is
      closed for its actual task outcome, and no experiment or hypothesis disposition is
      waiting only in chat or task notes.
    exit: >-
      Three immutable review packets at one commit, including every proposed frontier or
      hypothesis transition, with all agenda and tbd transitions reconciled and generated
      views current. After the review revision is committed,
      mark BC-119 `complete` and close think-47xw with the reconciliation outcome; only
      then mark BC-120 `ready` and remove think-722v's hold. The checkpoint runs no
      experiment, repairs no finding and makes no mathematical promotion.
    bead: think-47xw
    depends_on: []
    blocked_on: >-
      Exactly one declared second-wave continuation in each of the three lanes must be
      terminal and its sibling explicitly stopped.
    workflows: [efficiency-loop, insight-iteration, process-review, documentation-pass]
    next_evidence: >-
      Held `blocked` until the 06:15 wall-clock checkpoint. The coordinator owns shared
      agenda edits, review-packet hashes, generated views, bead transitions and PR update.
  - id: BC-120
    purpose: measurement_validation
    owner_focus: correctness
    instances: [17, 39, 50, 54, 68]
    state: blocked
    priority: 0
    question: >-
      Do three independent reviewers reproduce the lane outcomes and accept their claim
      boundaries, controls and recorded limitations at the frozen revision?
    hypotheses: []
    budget: >-
      90 minutes. During 0--15, assign three read-only reviewers and freeze their packet
      hashes. During 15--60, each reviewer independently replays the named command or
      checker, fires at least one named mutation or negative control, and audits the claim
      boundary. During 60--75, the coordinator reconciles determinations without changing
      source artifacts. During 75--90, retain one review document, route discrepancies,
      update the PR, and make BC-121 ready.
    entry: >-
      BC-119 is complete and provides three revision-keyed packets. Use three sub-agents,
      one per lane, with read-only ownership of the retained result and no shared authorship
      of the source under review. Each reviewer reports pass, bounded caveat, discrepancy,
      or cannot-reproduce with exact evidence. The coordinator may fix clerical review-
      packet errors but may not rewrite a scientific result to obtain a pass.
    exit: >-
      A durable review determination for every lane naming revision, replay result,
      mutation/control, evidence status, claim boundary, proposed transition and any
      blocking finding. Only an explicit pass grants promotion or hypothesis-disposition
      clearance; for H-051 that means permission to clear `needs_review` without changing
      the pre-frozen decision. Bounded caveat, discrepancy and cannot-reproduce leave the
      proposed transition unapplied. After retaining the review,
      mark BC-120 `complete` and close think-722v with the review determination; only
      then mark BC-121 `ready` and remove think-0sif's blocked hold. Leave source-result
      repairs to a separately registered follow-up.
    bead: think-722v
    depends_on: [BC-119]
    workflows: [factual-review, process-review]
    next_evidence: >-
      Held `blocked`. The future review coordinator owns one new document under
      docs/project/reviews/, the BC-120 row, the BC-121 transition and the PR checkpoint;
      reviewers do not edit the artifacts they inspect.
  - id: BC-121
    purpose: research
    owner_focus: process
    instances: [17, 39, 50, 54, 68]
    state: blocked
    priority: 0
    question: >-
      What did the nine-hour run establish, refuse or leave unresolved, and what exact
      entry point should the next agent take?
    hypotheses: []
    budget: >-
      45 minutes. During 0--15, reconcile experiment, hypothesis, result, agenda and tbd
      state against BC-120 and apply only its pre-frozen, explicitly cleared frontier or
      hypothesis transitions. During 15--30, retain the synthesis, render generated views,
      run documentation and records checks, terminalize the coordinator AgentSession,
      update every outer and delegated resource rollup, and run `close_session --render`.
      During 30--45, commit, run `packing-validate --push` on that exact commit, push,
      lead the PR with the rendered branch-cost block, sync tbd, record the next entry
      point and wait for the final hosted checks.
    entry: >-
      BC-120 is complete, every review finding has a disposition or a blocking follow-up,
      all lane task sessions are closed, and at least 45 minutes remain inside the owner-
      authorized wall. Applying a pre-frozen transition that BC-120 explicitly cleared is
      allowed; no new experiment, substantive repair or target starts in this gate.
    exit: >-
      A revision-keyed overnight synthesis separating proved, repository-verified,
      source-backed, measured-negative and unresolved claims; current agenda map and
      ledger; green formatting, records, edit and push gates; a PR updated with exact
      branch cost, checkpoint history and remaining blockers; and `tbd sync --status`
      clean. Apply only BC-120-cleared provisional promotions and hypothesis dispositions;
      for H-051, application changes only `needs_review` from true to false on the frozen
      decision. Leave every disputed claim unapplied, H-051 registered when its
      disposition lacks clearance, and BC-115 blocked when the n = 17 adoption lacks
      clearance. The coordinator session is terminal, its outer and sub-agent rollups are
      declared, the session-close report and synopsis block are rendered, and
      `gh pr checks --watch` reports the final pushed revision green. Mark BC-121 and
      think-0sif complete only after all conditions hold.
    bead: think-0sif
    depends_on: [BC-120]
    workflows: [insight-iteration, documentation-pass, process-review]
    next_evidence: >-
      Held `blocked` for the 08:15--09:00 terminal window. Own one overnight synthesis
      under packing/campaign/explorations/ or docs/project/reviews/, shared generated
      views, final validation, tbd synchronization and the PR description.
---
# Agenda-013 — Nine-Hour Autonomous W3/W6 Research Run

## Workflow entry point

Start from one clean branch and pull request containing agenda-012 and this agenda.
Run `tbd prime`, `tbd sync --status`, and the edit-tier validation before claiming work.
The coordinator opens one AgentSession for the whole run and each lane owner opens its
own contemporaneous AgentSession before touching a target.
Allocate session and experiment ids only when the file is created; do not reserve empty
records.

The coordinator claims BC-108, BC-109 and BC-110 from agenda-012, then gives their
launch cards and disjoint write scopes to the three first-wave owners.
Lane owners edit only their owned code, case, test and AgentSession paths and return
terminal receipts. Only the coordinator edits agendas, generated views, shared frontier
records, the PR description or tbd state.

## Exact wall-clock schedule

The offsets are measured from the coordinator’s recorded start time.
The nine-hour wall is owner-authorized and therefore a real terminal condition.

| Offset | Wall | Workflow | Work | Required PR checkpoint |
| --- | ---: | --- | --- | --- |
| 00:00--00:20 | 20m | W3 insight iteration | Frame the three first-wave questions, mechanisms and falsifiers in parallel | — |
| 00:20--02:10 | 110m | W6 research loops | Execute BC-108, BC-109 and BC-110 in parallel; use only the declared W7 instrument work needed by their measurements | — |
| 02:10--02:30 | 20m | W3 insight iteration | Explain each result, map the live uncertainty and prepare the lane handoffs | Commit the lane receipts, run `packing-validate --push` on the exact commit, push and refresh the PR |
| 02:30--02:45 | 15m | W5 efficiency loop | Run BC-122 against measured first-wave agent, coordination, validation, CI and tool costs | Commit the receipt, run `packing-validate --push`, push and refresh the PR |
| 02:45--03:15 | 30m | W3 insight iteration | Run BC-111’s evidence checkpoint and route one continuation per lane | Commit row and hold transitions, render map and ledger, run `packing-validate --push`, push and refresh the PR |
| 03:15--03:35 | 20m | W3 insight iteration, plus conditional W5 | Shape each selected continuation; concurrently apply at most one BC-122 improvement if its repayment trigger passed | — |
| 03:35--05:55 | 140m | W6 research loops | Implement and execute the three selected continuations in parallel | — |
| 05:55--06:15 | 20m | W3 insight iteration | Interpret mechanisms, preserve successor ideas and close the three lane handoffs | Commit every positive, negative or refusal, run `packing-validate --push`, push and refresh the PR |
| 06:15--06:25 | 10m | W5 efficiency loop | Compare second-wave throughput with BC-122 and retain agent and tool bottlenecks for the next agenda | — |
| 06:25--06:45 | 20m | W4 process review | Finish BC-119 reconciliation and freeze the review packets | Commit the exact review revision, sync tbd, run `packing-validate --push`, push and refresh the PR |
| 06:45--08:15 | 90m | W2 factual review | Run BC-120 as three independent replay and challenge reviews | Commit review determinations, run `packing-validate --push`, push and refresh the PR |
| 08:15--09:00 | 45m | W3 insight iteration and W4 closeout | Run BC-121 synthesis, session close, full validation and handoff | Close and render the coordinator session, commit, run `packing-validate --push`, push, update the generated PR cost, sync tbd and require final CI green |

If a W6 loop reaches its primary verdict early, its owner uses the remaining declared
cells for preregistered robustness checks, mutations or sensitivity bounds on that same
claim. Once those are exhausted, the owner closes the session, prepares the required
review packet and may perform read-only review support.
It does not start another target before the W3 checkpoint routes a successor.
If a lane overruns, it stops at the next 15--30 minute boundary, records the unfinished
criterion and hands the partial artifact to the checkpoint; the wall does not move.

## Outcome routing at BC-111

BC-111 routes each lane once and records the decision in both agendas and tbd before any
second-wave agent claims work.

| Lane | First-wave outcome | Run during 03:15--06:15 | Sibling disposition |
| --- | --- | --- | --- |
| n = 17 certificate | all fixed invariants agree and shared assumptions are named | BC-112 provisional adoption determination | BC-116 stopped; think-9zgs paused |
| n = 17 certificate | discrepancy, cannot-reproduce or guard stop | BC-116 adjudication | BC-112 stopped; think-5q0v paused |
| n = 68 precision | compatible and valid parent arm freezes from parent-only facts | BC-113 blinded H-051 pilot | BC-117 stopped; think-t7v1 paused |
| n = 68 precision | no compatible parent arm or a parent provenance/transform refusal | BC-117 refusal localization | BC-113 stopped; think-gbkd paused |
| n = 50 control | exact reconstruction and independent validity pass | BC-114 one-case n = 54 or n = 39 continuation | BC-118 stopped; think-8pjf paused |
| n = 50 control | source, representation, verifier or price refusal | BC-118 refusal localization | BC-114 stopped; think-dao9 paused |

Child qualification never routes the n = 68 lane.
BC-113 uses the frozen parent arm, and only after proposer output is immutable applies
the gain-relative precision contract to that parent and its corresponding child.
A precision failure is H-051’s unresolved refusal, not permission to select another arm.

## Cell and experiment contract

W3 and W6 are complementary rather than equal quotas.
A W3 cell maps the current mechanism, uncertainty, falsifier and highest-information
successor.
It may inspect retained evidence, but it does not execute a target or issue an
experiment verdict. A W6 cell starts only after its claim, fixture, metric, threshold,
budget, refusal conditions and control are frozen.
It builds the required instrument, executes the measurement and records positive,
negative or unresolved evidence under the experiment-loop contract.
Every valid W6 result receives the scheduled W3 mechanism pass before a successor is
routed. W2, W4 and W7 enter only where the table names an evidence review, process gate
or measurement-enabling instrument; they are not time quotas.

W5 is mandatory after the first parallel wave and repeats at BC-119. Its currency is
retained artifacts per wall-hour under unchanged evidence gates, supported by cell,
command and coordination timings.
It covers agent behavior as well as code: duplicated work, unclear ownership, late guard
discovery, handoff repair, idle gate time, validation latency, CI latency and slow
research tools all qualify.
An optimization enters only when its measured repayment fits inside the remaining wall.
A no-change decision is a valid W5 result and returns the time to W3/W6 work.

Every 15--30 minute cell writes these four fields in its AgentSession before proceeding:

- **Artifact:** durable file, hash or review packet created in the cell;
- **Result:** measured fact, refusal, discrepancy or unresolved ambiguity;
- **Guard:** independent check, mutation or negative control that fired;
- **Next:** next declared cell or stop transition.

Before reading target output, a measurement cell freezes its fixture, metric, threshold,
budget, refusal conditions and control in the next experiment record.
The experiment-loop registry remains authoritative for hypotheses and verdicts.
An agenda row owns scheduling, not scientific truth.
Every miss and exhausted budget is retained; rerunning with a different grammar, model,
field or target requires a new registration.

## Review and PR contract

At every checkpoint-bearing row in the schedule, the coordinator:

1. reconciles row state, bead state and AgentSession state;
2. regenerates the agenda map and campaign ledger;
3. regenerates this run’s `CodexTaskTreeDelta/v1` from the coordinator AgentSession
   start to the current snapshot, lists it in `resource_rollups`, and runs
   `close_session --render --session <coordinator-session>` so the declared live lower
   bound is current; a Claude-hosted replay uses `close_session --update` with the outer
   and delegated logs instead;
4. commits, runs `packing-validate --push` on the exact commit, and refuses to push on a
   failure;
5. runs `tbd sync` and records whether it is clean;
6. pushes the commit to this one PR, leads the description with the generated branch-
   cost block, and updates lane outcomes, validation receipt and next exact entry point;
   and
7. observes the hosted checks asynchronously while useful in-scope work remains.

The first PR publication uses the same mid-session rollup snapshot.
At BC-121, set the coordinator session terminal and update its rollups before the final
render. After the final push, run `gh pr checks <PR> --watch`; a non-green or unfinished
final summary leaves BC-121 and think-0sif incomplete with the exact hosted check named
in the handoff.

BC-120’s reviewers work from immutable commit hashes and do not edit the source
artifacts they judge.
A pass requires a replay plus a named mutation or negative control.
A discrepancy is an output, not a request to soften the claim.
The coordinator can correct paths or hashes in a review packet, but substantive repairs
become future registered work after BC-121. Second-wave frontier changes and hypothesis
dispositions remain provisional until BC-120 explicitly clears them and BC-121 applies
the already-frozen transition.

## Terminal conditions

BC-121 closes the run only when the PR, repo records and tbd graph tell the same story.
The synthesis separates proof, repository verification, source report, measured result,
negative result and unresolved status.
If validation or synchronization cannot be made green inside the final window, BC-121
remains incomplete and the handoff names the exact failing command and revision.
The agent does not merge the PR without separate owner authorization.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
