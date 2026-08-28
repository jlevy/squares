---
title: agenda-004 — repair the guards, unblock the instrument, then resume research
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-004
  title: Repair the guards, unblock the instrument, then resume research
  updated: '2026-08-27'
  status: active
  objective: >-
    Close every outstanding item session 029 left, each in its own declared workflow
    rather than folded into whichever slice happens to be running. Guard repairs land as
    one pipeline slice, the frozen research instrument is completed before it is used,
    and no optimization touches a path an experiment has frozen.
  items:
  - id: BC-035
    purpose: tool_validation
    owner_focus: correctness
    instances: [5, 11, 29]
    state: complete
    priority: 1
    question: >-
      Can the guards that stopped guarding be repaired, and the class of failure closed
      rather than only its instances?
    hypotheses: []
    budget: one W7 pipeline-improvement slice of at most 45 minutes, plus one full gate
    entry: >-
      the full gate is green and the three known instances are individually reproducible
    exit: >-
      Every child bead closed or explicitly deferred with a reason, one full
      `packing-validate` green, and the full-tier cadence decision written down rather
      than left as folklore.
    bead: think-cja6
    workflows: [pipeline-improvement]
    depends_on: []
    next_evidence: >-
      Build the declared-command guard under think-ldy8, fix the terminal-round contract
      under think-306i, decide whether to pin lefthook the way flowmark is pinned, and
      decide whether `controls.yaml` anchors that embed generated values should be derived
      rather than literal. The last item is the actual class defect: a literal anchor on a
      number the checker itself moves is what silently disabled one of 76 controls. The
      record-model joins moved to BC-041 so neither commitment carries six children.
    artifacts:
    - Makefile
    - devtools/check_declared_commands.py
    - devtools/controls.yaml
    - src/sqpack/campaign/ledger.py
    - src/sqpack/cli/validate.py
    note: >-
      Three of the four bugs found on 2026-08-27 were guards that had stopped guarding,
      and none was visible to the `--fast` edit loop that broke them. Repairing them
      separately would repeat that: the point of one slice is that they land against one
      full-tier run.
  - id: BC-041
    purpose: tool_validation
    owner_focus: process
    instances: [5, 11, 29]
    state: complete
    priority: 2
    question: >-
      Can the record model's two unchecked joins be made machine-checkable, so that a
      commitment's state and the work actually done against it cannot drift apart unseen?
    hypotheses: []
    budget: one W7 pipeline-improvement slice of at most 60 minutes, plus one full gate
    entry: >-
      the guard repairs under BC-035 have landed, or are known not to touch the same
      checker surfaces
    exit: >-
      An invariant rejecting more than one live commitment per bead, and an optional
      structured join from a workflow phase to the commitment it serves, or a typed reason
      why either cannot be added without rewriting terminal records.
    bead: think-hpf7
    workflows: [pipeline-improvement]
    depends_on: []
    next_evidence: >-
      Three beads back more than one live commitment today, and `think-1s0h` is
      simultaneously ready at BC-010 and blocked at BC-029 and BC-037. Separately, phases
      carry no bead or commitment field, only 39 percent of phases name a commitment at
      all, and the session-to-commitment link is recovered by regex over `next_action`
      prose. Both fields must be optional so no terminal session record needs rewriting.
    artifacts:
    - campaign/schemas/agenda.schema.yaml
    - campaign/schemas/agent-session.schema.yaml
    - src/sqpack/campaign/ledger.py
    note: >-
      Split out of BC-035 before work started, because six children under one commitment is
      how `think-cja6` grew from two to four items in a single day.
  - id: BC-036
    purpose: tool_validation
    owner_focus: correctness
    instances: [5]
    state: complete
    priority: 0
    question: >-
      Can exp-045's four missing pre-certificate mutations be built so the enforced count
      matches the declared twelve, without weakening any frozen criterion?
    hypotheses: [H-023]
    budget: one W7 pipeline-improvement slice of at most 60 minutes
    entry: >-
      exp-045 remains preregistered and unexecuted, and its other five admission
      conditions still hold
    exit: >-
      Twelve typed pre-certificate mutations enter before certificate construction and
      match only their frozen failure identifiers, or a typed blocker explaining which
      mutation cannot be defined without inventing semantics.
    bead: think-oyn9
    depends_on: []
    next_evidence: >-
      `minus_w_obstruction` raises on any set that is not its eight `CONTROL_KEYS`; four
      further mutations must be defined, named, and given frozen failure identifiers.
      Under no circumstances amend exp-045's declared twelve down to the implemented
      eight: the criterion was frozen before implementation, and matching it to the code
      afterwards is the post-hoc weakening the admission bar exists to prevent.
    artifacts:
    - cases/n5/minus_w_obstruction.py
    - campaign/agent-sessions/session-032-block1-missing-mutations.md
    note: >-
      This commitment gates both remaining research lanes. exp-045 cannot run without it, and
      BC-038 must not touch the shared row-jet path while exp-045 is frozen, so BC-036 is
      the single highest-leverage item in this agenda.
  - id: BC-037
    purpose: research
    owner_focus: correctness
    instances: [5]
    state: complete
    priority: 0
    question: >-
      Do the frozen pure minus-W scale routes and controls advance the n = 5
      terminal-family question beyond exp-044's finite unresolved obstruction?
    hypotheses: [H-023]
    budget: one W6 research-loop mini-cycle of at most 105 minutes, with an immediate W3 pass on any valid result
    entry: >-
      all twelve mutations are present and enforced, and the remaining exp-045 admission
      conditions are re-checked rather than assumed
    exit: >-
      A valid exp-045 outcome, including a finite unresolved result, or a typed instrument
      blocker. Every valid result receives an immediate W3 mechanism pass.
    bead: think-1s0h
    depends_on: [BC-036]
    next_evidence: >-
      exp-045 with its frozen criterion, the declared controls and scale routes, retained
      raw evidence, an independent replay, and a scoped successor disposition. No
      whole-component identity or connectivity language is admitted.
    artifacts:
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-045-h-023-n5-minus-w-scale-and-controls.md
    - campaign/agent-sessions/session-033-block2-run-exp045.md
    note: >-
      This continues agenda-003's BC-029 rather than replacing it, the way BC-029 itself
      continued agenda-001's BC-010 under the same bead.
  - id: BC-038
    purpose: tool_validation
    owner_focus: efficiency
    instances: [5]
    state: ready
    priority: 1
    question: >-
      Does wiring `evaluate_stress` to the existing shared row inventory repay its build
      cost at exact semantic equality?
    hypotheses: []
    budget: at most two W5 efficiency-loop slices of 20 to 30 minutes, with three cold and five warm comparisons
    entry: >-
      exp-045 has reached a terminal disposition, so the shared row-jet path is no longer
      frozen under a preregistered experiment
    exit: >-
      Either reject the optimization with measured arithmetic, or accept it only after
      three cold and five warm comparisons show at least a five-fold improvement, warm
      median at most 45 seconds, warm p95 at most 55 seconds, and exact semantic equality.
    bead: think-kdil
    workflows: [efficiency-loop]
    depends_on: [BC-037]
    next_evidence: >-
      The trigger is already measured and passed: `active_row_jets` holds 93.0 percent of
      the `exhaustive_exact` group's cumulative time, the dominant arm is
      `evaluate_stress` to `owner_row_jets` at 57.6 percent, and the same function costs
      0.025 seconds per call inside the shared-inventory test against 11.95 on that arm.
      What is owed is the exact-output equivalence result, not another profile.
    note: >-
      Whether `evaluate_stress`'s 35 calls actually share a field identity and stratum is
      not decidable from a profile. That is this commitment's first obligation, before any
      timing claim.
  - id: BC-039
    purpose: tool_validation
    owner_focus: correctness
    instances: [29]
    state: complete
    priority: 2
    question: >-
      At which `rational_digits` should the durable n = 29 certificate be regenerated, and
      what is the honest reason for that choice rather than a smaller or larger one?
    hypotheses: []
    budget: one W7 pipeline-improvement slice of at most 30 minutes, plus one full gate
    entry: >-
      Q-BC032-a is answered and the route dependence is recorded
    exit: >-
      A regenerated witness whose certificate metadata, the
      `E-n029-schadt-rational-upper` limitations text, and both gated checker paths agree,
      with the chosen `rational_digits` and its reason recorded.
    bead: think-uzmh
    workflows: [pipeline-improvement]
    depends_on: []
    next_evidence: >-
      Six verified promotions at `rational_digits` 18 through 60 all beat the recorded
      4.9339e-11 relaxation, tracking the ladder rung 10^-(d-5) exactly down to
      4.933851e-55. The route has no minimum, so the choice is a policy decision traded
      against literal artifact size, and it must be argued rather than maximized.
    artifacts:
    - frontier/evidence.yaml
    - frontier/n-029.md
    - witnesses/schadt-n029-2025-rational.yaml
    note: >-
      The claim boundary does not move. This remains an upper bound at a relaxed rational
      side, weaker than the reported record; it certifies no source decimal and proves no
      optimality.
  - id: BC-040
    purpose: tool_validation
    owner_focus: process
    instances: [5, 11, 29]
    state: complete
    priority: 1
    question: >-
      Does the accumulated branch still pass a full gate once main is merged into it,
      rather than only against the tree the measurements were taken on?
    hypotheses: []
    budget: one W4 process-review slice of at most 30 minutes, plus one full gate
    entry: >-
      the guard repairs have landed, so the merge is tested against a guarded tree
    exit: >-
      A merged branch with a green full gate and PR 48 out of draft, or a recorded
      conflict or regression that names the next owner.
    bead: think-qibu
    depends_on: []
    next_evidence: >-
      Re-run the full gate rather than `--fast` against the merged tree. If the round
      count or any generated aggregate moved in the merge, re-check `devtools/controls.yaml`
      anchors first: that is the exact rot that silently disabled the round-aggregate
      control.
    artifacts:
    - campaign/agent-sessions/session-031-merge-main-and-land-pr48.md
    - devtools/run_negative_controls.py
    - tests/test_negative_controls.py
    note: >-
      Deliberately not done inside session 029, because merging main rewrites files
      underneath the profile, gate timings, and control anchors that session recorded.
      Originally sequenced behind BC-035 so the merge would be tested against a guarded
      tree. That dependency was dropped deliberately in session 031 at the user's
      direction: the guard repairs are independent improvements rather than merge
      prerequisites, the full gate was already green before the merge, and leaving a
      twenty-commit branch unmerged has a real and growing cost that the guard work does
      not. BC-035 keeps its own value and its own slice.
---
# Agenda-004 — Repair the Guards, Unblock the Instrument, Then Resume Research

This agenda exists because
[session 029](../agent-sessions/session-029-finish-agenda-003-cycles.md) closed
[agenda-003](agenda-003-balanced-ten-hour-research-program.md)’s remaining commitments
and left six things outstanding, each of a different kind.
Mixing them into one session is what produced the guard failures in the first place, so
each has its own declared workflow entry and its own budget.

## Workflow assignment

| Commitment | Workflow | Bead | Why this workflow |
| --- | --- | --- | --- |
| BC-035 | W7 `pipeline-improvement` | think-cja6 | Repairs the checking machinery, not a claim about packings. |
| BC-041 | W7 `pipeline-improvement` | think-hpf7 | Makes the record model’s joins checkable; process work on the machinery, not a claim. |
| BC-036 | W7 `pipeline-improvement` | think-oyn9 | Builds a missing research instrument before it is used, which is instrument work rather than a measurement. |
| BC-037 | W6 `research-loop` | think-1s0h | The only commitment here that asks a question about the packing landscape. |
| BC-038 | W5 `efficiency-loop` | think-kdil | A measured bottleneck with a declared accept bar. |
| BC-039 | W7 `pipeline-improvement` | think-uzmh | Regenerates a durable artifact through an existing gated route. |
| BC-040 | W4 `process-review` | think-qibu | Reconstructability and merge discipline, not new evidence. |

## Bounded blocks and checkpoints

The agenda runs as four blocks of about five hours.
Each ends at a terminal, verifiable state rather than mid-commitment, so a checkpoint
can ask whether the agenda is worth continuing rather than only whether the current task
is done.

| Block | Commitments | Checkpoint question |
| --- | --- | --- |
| 1 | BC-036, BC-039 | Is the research arm alive? |
| 2 | BC-037 | Does exp-045 produce a result? |
| 3 | BC-035, BC-041 | Is the pipeline debt paid? |
| 4 | BC-038, consolidation | Close out |

BC-036 leads because it is both the gate and the largest binary unknown.
Its risk is not difficulty but existence: four *genuinely distinct* pre-certificate
failure modes may not be definable, in which case the declared twelve was aspirational,
BC-037 and BC-038 never run, and the agenda collapses to its pipeline half.
That answer is worth having in the first five hours rather than the second.
BC-039 fills block 1 because it is independent of BC-036’s outcome.

### Replan triggers

- **Block 1.** If no fourth distinct failure mode can be honestly named, stop and record
  that as the finding.
  Do not amend exp-045’s declared twelve down to the implemented eight; the criterion
  was frozen before implementation.
- **Block 2.** Hard stop at the block boundary.
  If exp-045 has not reached a terminal disposition, terminalize it `stopped` rather
  than extending. A second typed blocker here is itself a signal about the `n = 5` lane
  and should be surfaced, not pushed through.
- **Block 3.** If fewer than four of BC-035’s and BC-041’s items close, split again
  rather than extend.
- **Any block.** Two consecutive blocks closing zero commitments stops the agenda for
  replanning, not the block.

### Health check at every boundary

Completion alone is the wrong metric here.
Across the recorded campaign, 68 percent of attributed effort has gone into commitments
that never closed, and the three most-worked commitments are all still open.
So each boundary measures rate, not just state:

| Check | Healthy | Warning |
| --- | --- | --- |
| Commitments closed this block | at least one | none |
| Attributed minutes per closure | at most 240 | above 360 |
| Consecutive zero-closure blocks | none | two stops the agenda |
| Full gate at block end | green | red carries into the next block |

The last row is the one to hold hardest.
On 2026-08-27 three separate generated-view drifts each stayed invisible until something
forced a check, and every one would have been caught by a full-tier gate at the commit
that introduced it rather than at merge.

## The one ordering constraint that matters

BC-036 gates both research lanes.
exp-045 cannot run until its declared twelve mutations exist, and agenda-003’s BC-028
must not touch the shared row-jet path while exp-045 is frozen against it.
So the sequence is BC-036, then BC-037, then BC-038. BC-035 and BC-039 are independent
and may run at any time; BC-040 follows BC-035.

BC-037 and BC-038 continue agenda-003’s BC-029 and BC-028 under the same beads, which is
this campaign’s existing convention for carrying a lane across agendas: `think-1s0h`
already backs BC-010 in agenda-001 and BC-029 in agenda-003. Keeping them here makes
agenda-004 self-contained, which matters because `depends_on` resolves only within a
single agenda file.

Nothing in this agenda widens a claim.
Five of its seven commitments repair or complete instruments, one regenerates an
artifact inside an unchanged claim boundary, and only BC-037 can produce a scientific
result.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
