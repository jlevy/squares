---
title: session-030 — map the work model and retire the cell collision
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-030
  title: Make the three-layer work model explicit and re-gloss BC
  date: '2026-08-27'
  started_at: '2026-08-27T13:18:51-07:00'
  deadline_at: '2026-08-27T14:18:51-07:00'
  goal: >-
    Remove the `cell` terminology collision, state the bead / bounded-commitment / phase
    layering explicitly in the orientation docs, and correct four stale or misleading
    entries, without touching any identifier, schema pattern, test, or archived record.
  workflow_phases:
  - workflow: process-review
    recording: contemporaneous
    clock_role: work
    focus: process
    objective: >-
      Re-gloss `BC` from "bounded cell" to "bounded commitment" in live prose only, add
      the missing agenda / commitment / bead layers to the work-unit map, and repair the
      stale BC-NNN gloss, the stale agenda-ownership row, and the workflow handoff column
      that reads as a rule but behaves as advice.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 45
    started_at: '2026-08-27T13:18:51-07:00'
    deadline_at: '2026-08-27T14:03:51-07:00'
    expected_output: >-
      Orientation docs in which a reader can tell a bounded commitment from a workflow
      phase from a bead, and in which `cell` means only the linear-programming object.
    validation_command: >-
      uv run --directory explorations/packing --frozen python -m devtools.check_synopsis
    kill_condition: >-
      Stop on editing any `BC-NNN` identifier, the `^BC-[0-9]{3}$` schema patterns, test
      fixtures, frozen evidence strings, or any terminal session record; on renaming the
      mathematical `cell`; or on adding a new work-model layer rather than documenting the
      three that already exist.
    fallback: >-
      Retain the collision as a typed documentation defect and change nothing, rather than
      renaming an identifier that is embedded in verified artifacts.
    outcome: >-
      `BC` now reads "bounded commitment" everywhere it is glossed in live prose, the
      work-unit map states the bead / commitment / phase layering explicitly, and four
      stale or misleading entries are corrected. No identifier, schema pattern, test,
      frozen evidence string, or terminal session record was touched.
    evidence:
    - Fourteen live occurrences were re-glossed in total. The initial survey found only the five instances of the exact phrase "bounded cell"; a second sweep of the bare word found nine more carrying the same sense, in the campaign runbook and in agenda-004's own body. The four occurrences inside terminal session records were deliberately left as recorded.
    - >-
      The word turned out to carry four unrelated senses in this tree, which is why one
      grep was not enough: the linear-programming object and its raw, canonical, active
      and full variants; the planning unit now called a commitment; the instance-axis rows
      at `n = 5, 10, 11, 16, 17` described as "standing cells" and "proved ladder cells";
      and the experimental-design sense in "control cells" and "five seeds per cell".
      Only the second was re-glossed. The third and fourth are left as found and are not
      yet tracked.
    - The work-unit table gained agenda, bounded commitment and bead rows, plus a comparison of the three by lifetime, typing and falsifier, so the layer a reader is looking at is now stated rather than inferred.
    - 'The `cell` term entry now says outright that it is the only meaning of the word here and that `BC-NNN` is not a cell.'
    - The BC-NNN gloss no longer describes agenda-001 as the only agenda, and the document-ownership table points at the agendas directory rather than a single ladder.
    - The workflow handoff column is now labelled the usual successor rather than a rule, with the measured 31 percent conformance across 171 phases stated so a reader is not misled by it.
    stop_reason: >-
      Every declared edit landed inside the slice budget, and the identifier, schema and
      archived-record boundaries were held.
    next_action: >-
      Under BC-036 and think-oyn9, build exp-045's four missing pre-certificate mutations
      so the enforced count matches the declared twelve. The work-model repairs this pass
      identified are tracked as think-hpf7 and think-p6fu under think-cja6.
  primary_bead: think-qxmo
  status: completed
  budget:
    wall_minutes: 60
    slice_minutes: 45
    finalization_minutes: 15
  stop_conditions:
  - No identifier, schema pattern, test, or frozen evidence string is edited.
  - No terminal session record is rewritten; historical prose stands as recorded.
  - The full gate must be green before the session is terminalized.
  progress:
    metric: a reader can distinguish the three work-model layers from the orientation docs alone
    before: >-
      `BC` expands to "bounded cell" while `cell` is separately defined as a linear
      program in the same README, twenty lines apart. The work-unit table omits agendas,
      bounded commitments and beads entirely. The BC-NNN gloss still describes agenda-001
      as the only agenda, and the workflow table presents a handoff graph that measured
      31 percent conformance across 171 recorded phases.
    after: >-
      A reader can now tell the three layers apart from the orientation docs alone, and
      `cell` means only the linear-programming object. Two structural gaps this pass
      surfaced are tracked rather than fixed here: at most one live commitment per bead
      (think-hpf7) and a machine-checkable commitment-to-phase join (think-p6fu).
  delegations: []
  outputs:
  - README.md
  - campaign/README.md
  - campaign/agendas/agenda-001-basin-confidence-ladder.md
  - campaign/agendas/agenda-004-guard-repair-and-instrument-unblock.md
  - campaign/agendas/agenda-003-balanced-ten-hour-research-program.md
  - campaign/agent-sessions/session-030-work-model-and-cell-collision.md
  - campaign/schemas/agenda.schema.yaml
  checks:
  - The full gate passed all 36 steps at 3f2e1c8 before this session opened.
  - 'Measured blast radius before choosing: the identifier appears 646 times across 49 files, the phrase 9 times, of which 4 are in terminal records.'
  stop_reason: >-
    The declared documentation slice is complete and its boundaries held; the two
    structural defects it surfaced are tracked as beads rather than pulled into a prose
    pass.
  next_action: >-
    Under BC-036 and think-oyn9, build exp-045's four missing pre-certificate mutations so
    the enforced count matches the declared twelve.
---
# Session 030 — Map the Work Model and Retire the `cell` Collision

`BC` has always meant “bounded cell”, while `cell` independently names the
linear-programming object at the centre of the enumeration work: 235 `cell` identifiers
in source, and four distinct technical senses (`raw`, `canonical`, `active`, `full`).

The identifier is not the problem.
`BC-035` collides with nothing, appears 646 times across 49 files, is pinned by two
schema patterns and by frozen evidence strings that tests assert byte-exactly, and is
written into twenty-one terminal session records that must not be rewritten.
The expansion is the problem, and it is written just nine times.

So this session changes the words and leaves every identifier alone.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
