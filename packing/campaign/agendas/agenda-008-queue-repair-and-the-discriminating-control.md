---
title: agenda-008 — repair the queue, then ask the one question the controls cannot currently answer
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-008
  title: Repair the queue, then ask the one question the controls cannot currently answer
  updated: '2026-08-30'
  status: active
  objective: >-
    Eight to nine hours in four blocks. Block 1 is first because the queue is currently
    wrong in a way that sends a session to redo finished work: four agenda-005
    commitments were discharged by agenda-006 and still read `ready`, and OR-4 tells a
    session to take its next slice from exactly that queue. Everything after block 1
    depends on the queue meaning what it says. Blocks 2 and 3 are the science the
    handoff names, in dependency order: the n = 4 labelled control cannot score the
    relation the atlas actually uses until exp-015 retains per-sample keys, and the
    n = 5 question cannot be asked well until that scoring works. Block 4 is the last
    genuine efficiency commitment left in agenda-005. This agenda owns the clock and the
    ordering; agenda-005 BC-051 owns block 4's scientific exit, and D-373 owns block 3's.
  items:
  - id: BC-081
    purpose: tool_validation
    owner_focus: process
    instances: [3, 5, 29]
    state: complete
    priority: 0
    question: >-
      Can a commitment's discharge be an edge the records carry, rather than prose in a
      later agenda that nothing reads?
    hypotheses: []
    budget: >-
      about 120 minutes, in slices of 15 to 30 minutes, W5 for the schema and renderer
      and W2 for the reconciliation itself
    entry: >-
      `devtools.render_agenda_map` now renders every agenda's commitments from their own
      frontmatter, and its first run reported both defects this commitment repairs: four
      blocked commitments naming no predecessor, and six of seven agendas declaring
      themselves active
    exit: >-
      A `discharged_by` edge in the agenda schema, carried by every commitment another
      agenda actually discharged, with the renderer refusing a `ready` commitment that
      names one; agenda-006 marked `completed`; the four unnamed blockers either given a
      predecessor or restated as what they truly wait on; and a negative control proving
      the refusal fires. Or a typed statement of which discharges cannot be expressed as
      an edge, which is itself the useful answer.
    bead: think-s424
    depends_on: []
    workflows: [pipeline-improvement, process-review]
    next_evidence: >-
      Measured on 2026-08-30 by the map's first run. agenda-005 BC-045's exit is n = 5,
      n = 10 and n = 11 interval certificates with refusal controls and n = 29 recorded
      unresolved; agenda-006 BC-053's exit is the same, and BC-053 is complete. The same
      holds for BC-043 against BC-054, BC-044 against BC-060, and BC-048 against BC-061.
      Four of the eleven commitments the queue offers as takeable are finished work.
    note: >-
      This is the same failure family as D-372, one level down: there the front door
      described the artifacts wrongly, here the queue does. The difference is the
      consequence. A wrong sentence misleads a reader; a wrong queue misdirects a session
      that is following OR-4 correctly. Only agenda-007 declared its discharges, and it
      declared them in a `note`, which is prose and which no checker reads.
    artifacts:
    - devtools/render_agenda_map.py
    - campaign/agenda-map.md
    - campaign/schemas/agenda.schema.yaml
    - tests/test_agenda_map.py
    - src/sqpack/campaign/ledger.py

  - id: BC-082
    purpose: measurement_validation
    owner_focus: correctness
    instances: [3, 4]
    state: complete
    priority: 0
    question: >-
      Can the n = 4 labelled control score the relation the atlas uses today, rather than
      reporting it undecidable?
    hypotheses: [H-032]
    budget: >-
      about 120 minutes, in slices of 15 to 30 minutes, W3 throughout, with no re-run of
      any proved count
    entry: >-
      X-005 scored four candidate relations and left one cell undecidable for want of
      retained detail rather than for want of an argument; exp-014 records four
      per-sample keys and exp-015 records none, and
      `devtools.check_identity_relation.Control` already carries a `samples` field that
      is empty for n = 4
    exit: >-
      Per-sample geometric keys and contact certificates for exp-015's 24 labelled
      states, in the shape exp-014 already uses, and a scored verdict for
      `geometric + contact` on the n = 4 labelled control whose answer is 24 -- or a
      typed statement of which retained quantity the labelled states cannot supply.
    bead: think-m2j8
    depends_on: [BC-081]
    workflows: [research-loop, insight-iteration]
    next_evidence: >-
      `geometric + contact` is the relation `Atlas.add` implements, and n = 4 labelled is
      the control that most directly tests it: 24 isolated labelled grids, so a correct
      labelled relation must report 24. It is currently the one control that relation
      cannot be scored against, which means the atlas's own rule is the least-tested of
      the four candidates.
    note: >-
      No proved count moves. exp-015's determination and acceptance rule are terminal;
      this adds retained detail to an existing result rather than re-running it. If the
      scoring refutes `geometric + contact`, that is a finding about the atlas and not a
      reason to revisit the experiment.

      It did refute it, and it also corrected the level the relation had been scored at,
      which is D-375. No proved count moved: exp-014 regenerates byte-identically after
      the shared-sampler refactor, and exp-015 differs only by the added `samples` key.
    artifacts:
    - cases/small_n/optimal_moduli.py
    - campaign/series/series-000-smoke-and-calibration/results/exp-015-h-032-n4-optimal-moduli.json
    - devtools/check_identity_relation.py
    - tests/test_identity_relation.py
    - campaign/explorations/X-005-identity-relation-and-its-controls.md

  - id: BC-083
    purpose: research
    owner_focus: insight
    instances: [5]
    state: complete
    priority: 0
    question: >-
      Does n = 5 admit a discriminating identity control -- one whose proved component
      count is neither one nor equal to its labelled count?
    hypotheses: [H-032]
    budget: >-
      about 150 minutes, in slices of 15 to 30 minutes, opening W3 and entering W6 only
      if a criterion is frozen first
    entry: >-
      X-005 declares `contact + closure` the surviving relation and D-373 records that
      the rule which was meant to establish it could not have, because every control it
      named has component count one; the n = 5 face, sheet, obstruction and polytope
      results are retained, and D-034's two n = 5 rows sharing side 2.767766952966 are
      the known counterexample any candidate relation must not merge
    exit: >-
      Either a declared n = 5 control with a proved component count that is neither one
      nor its labelled count, scored against all four candidate relations, or a typed
      statement of what about n = 5 prevents one -- naming which quantity would have to
      be proved and what it would cost.
    bead: think-6zaz
    depends_on: [BC-082]
    workflows: [research-loop, insight-iteration]
    next_evidence: >-
      Until such a control exists, any n = 5 identity claim is validated against a
      constant: three of the four candidates survive the rule as written, and `side
      alone`, which merges everything, is among them. D-034 cannot be closed against a
      rule a merge-everything relation would have passed.
    note: >-
      The exit's second branch is not a fallback. X-005's second branch fired and
      produced the more useful result of that block, and the same is plausible here: a
      typed statement of why n = 5 cannot be given a discriminating control is a sharper
      object than a census, and it is what would justify spending the next block
      somewhere else.

      The second branch fired, and it carried more than a refusal usually does. The typed
      statement names the missing quantity exactly -- exp-042's declared scope refusal
      `A_to_B_stationary_connection` -- and prices the two routes that cannot supply it.
      Alongside it, a *candidate* control was retained: the pair the record had been
      quoting since 2026-08-23 without ever keeping its endpoints, which is D-376. Both of
      its possible answers separate the candidate relations, and the branch where the count
      is two refutes contact + closure, the relation X-005 declared.

      It is a candidate and not a control because the first branch requires a proved count
      and `component_count` is null. D-378 records the related finding that no retained
      control can separate contact + closure from a relation that merges everything, which
      is why this pair reaches something nothing else does.
    artifacts:
    - devtools/build_n5_identity_pair.py
    - campaign/series/series-000-smoke-and-calibration/results/bc-083-n5-identity-pair.json
    - devtools/check_identity_relation.py
    - tests/test_identity_relation.py
    - campaign/explorations/X-006-the-discriminating-control-at-n5.md

  - id: BC-084
    purpose: tool_validation
    owner_focus: efficiency
    instances: [5, 11, 29]
    state: ready
    priority: 1
    question: >-
      Can verification run only the steps a change can reach, without any chance of
      running fewer than it should?
    hypotheses: []
    budget: about 90 minutes, one W5 efficiency-loop slice against a measured baseline
    entry: >-
      `packing-validate --only` already selects steps by name but has nothing mapping a
      change to the names it should select; BC-079's tiers classify steps by what they
      catch, which is change-agnostic and therefore a different instrument
    exit: >-
      A change-scoped selector that is conservative by construction -- an unrecognized
      path selects the full gate rather than an empty set -- with a negative control
      proving it cannot silently under-select, and a check that every step is reachable
      from at least one declared path pattern. Or a typed statement of which steps cannot
      be attributed to sources.
    bead: think-9qtn
    depends_on: [BC-081]
    workflows: [efficiency-loop]
    next_evidence: >-
      Measured on 2026-08-28: a two-file edit to the rigidity assessor was verified with a
      979.79s full gate, while the two steps that edit can affect run together in 12.06s.
      BC-079 has since cut the pre-push tier to 4.1s and added `--edit` at 26s, so the
      remaining gap is the full gate at a commit boundary, not the edit loop.
    note: >-
      Discharges agenda-005 BC-051, unchanged in scope, on a new bead because
      `think-ej1d` predates the tier work that changed what the baseline is. Last because
      BC-079 already took most of what this commitment was worth: the edit loop is fast
      now, so this is about the commit boundary, and its value dropped accordingly.
    artifacts: []
---
# Agenda-008 — Repair the Queue, Then Ask the Question the Controls Cannot Answer

## Why This Order

The ordering rule from agenda-007 held up and is reused: run the block that makes every
later block cheaper first, not the most important one.

Here that is block 1, and for a sharper reason than cost.
The queue is *wrong*, not merely slow.
[`OR-4`](../../../operating-rules.md) tells a session to take its next slice from the
agenda queue rather than from `tbd ready`, and four of the eleven commitments that queue
currently offers as takeable were discharged by agenda-006 and never marked.
A session following the operating rule correctly would be sent to redo finished work.
Repairing that is not tidying before the real work; it is the precondition for the
handoff meaning anything.

Blocks 2 and 3 are the science, in dependency order rather than in interest order.
The n = 5 question is the one the handoff names, but asking it well requires the n = 4
labelled control to be scoreable first, because that control is the only one that tests
the relation the atlas actually implements.
Asking the harder question against an instrument with a known blind spot is how
[`D-373`](../../../defects.md) happened in the first place.

Block 4 is last and is deliberately the smallest, because `BC-079` already took most of
what it was worth.

## What This Agenda Does Not Own

It does not own a scientific exit.
[`D-373`](../../../defects.md) owns block 3’s, agenda-005 `BC-051` owns block 4’s, and
`H-032` owns the identity question that blocks 2 and 3 both serve.
This agenda owns the clock, the ordering, and what each block must leave behind.

It also does not reopen any proved count.
`exp-014` and `exp-015` are terminal.
Block 2 adds retained detail to an existing result; if that detail refutes the relation
the atlas implements, the refutation is a finding about the atlas.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
