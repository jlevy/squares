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
    state: ready
    priority: 1
    question: >-
      Can every guard that stopped guarding be repaired in one pipeline slice, and can the
      class of failure be closed rather than only its three instances?
    hypotheses: []
    budget: one W7 pipeline-improvement slice of at most 45 minutes, plus one full gate
    entry: >-
      the full gate is green and the three known instances are individually reproducible
    exit: >-
      Every child bead closed or explicitly deferred with a reason, one full
      `packing-validate` green, and the full-tier cadence decision written down rather
      than left as folklore.
    bead: think-cja6
    depends_on: []
    next_evidence: >-
      Build the declared-command guard under think-ldy8, fix the terminal-round contract
      under think-306i, decide whether to pin lefthook the way flowmark is pinned, and
      decide whether `controls.yaml` anchors that embed generated values should be derived
      rather than literal. The last item is the actual class defect: a literal anchor on a
      number the checker itself moves is what silently disabled one of 76 controls.
    note: >-
      Three of the four bugs found on 2026-08-27 were guards that had stopped guarding,
      and none was visible to the `--fast` edit loop that broke them. Repairing them
      separately would repeat that: the point of one slice is that they land against one
      full-tier run.
  - id: BC-036
    purpose: tool_validation
    owner_focus: correctness
    instances: [5]
    state: ready
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
    note: >-
      This commitment gates both remaining research lanes. exp-045 cannot run without it, and
      BC-038 must not touch the shared row-jet path while exp-045 is frozen, so BC-036 is
      the single highest-leverage item in this agenda.
  - id: BC-037
    purpose: research
    owner_focus: correctness
    instances: [5]
    state: blocked
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
    note: >-
      This continues agenda-003's BC-029 rather than replacing it, the way BC-029 itself
      continued agenda-001's BC-010 under the same bead.
  - id: BC-038
    purpose: tool_validation
    owner_focus: efficiency
    instances: [5]
    state: blocked
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
    state: ready
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
    depends_on: []
    next_evidence: >-
      Six verified promotions at `rational_digits` 18 through 60 all beat the recorded
      4.9339e-11 relaxation, tracking the ladder rung 10^-(d-5) exactly down to
      4.933851e-55. The route has no minimum, so the choice is a policy decision traded
      against literal artifact size, and it must be argued rather than maximized.
    note: >-
      The claim boundary does not move. This remains an upper bound at a relaxed rational
      side, weaker than the reported record; it certifies no source decimal and proves no
      optimality.
  - id: BC-040
    purpose: tool_validation
    owner_focus: process
    instances: [5, 11, 29]
    state: blocked
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
| BC-036 | W7 `pipeline-improvement` | think-oyn9 | Builds a missing research instrument before it is used, which is instrument work rather than a measurement. |
| BC-037 | W6 `research-loop` | think-1s0h | The only commitment here that asks a question about the packing landscape. |
| BC-038 | W5 `efficiency-loop` | think-kdil | A measured bottleneck with a declared accept bar. |
| BC-039 | W7 `pipeline-improvement` | think-uzmh | Regenerates a durable artifact through an existing gated route. |
| BC-040 | W4 `process-review` | think-qibu | Reconstructability and merge discipline, not new evidence. |

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
Four of its six commitments repair or complete instruments, one regenerates an artifact
inside an unchanged claim boundary, and only BC-037 can produce a scientific result.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
