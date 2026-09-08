---
title: session-104 — a robust unavoidable set of at most eleven marks at 96/25
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-104
  title: A robust unavoidable set of at most eleven marks at 96/25 (BC-302, H-134)
  date: '2026-09-08'
  started_at: '2026-09-08T04:38:00Z'
  deadline_at: '2026-09-08T07:08:00Z'
  branch: claude/squares-n11-constraints-wl9atd
  goal: >-
    Decide BC-302 within one 2.5-hour block: build a checked falsifier for candidate mark
    sets at side 96/25 (marks thickened by 3/500), run it on the sets built from T-018's
    atom skeleton and on Stromquist-style sets, catalogue every exact escape, and either
    prove a survivor's nonavoidance regions or record the catalogue as the obstruction the
    closing route needs.
  workflow_phases:
  - workflow: research-loop
    focus: insight
    recording: contemporaneous
    clock_role: work
    objective: >-
      Orientation on the lane inputs, then the engine: a numpy grid and Nelder-Mead search
      over poses followed by exact rational verification of containment and of distance
      above 3/500 to every mark, self-tested on lane C's exact escape at q, on exp-121's
      frozen square, and on two controls that must have no escape.
    commitment: BC-302
    bead: think-qfog
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 30
    started_at: '2026-09-08T04:38:00Z'
    deadline_at: '2026-09-08T05:08:00Z'
    expected_output: escape_engine.py and its self-test, both retained verbatim in the lane document's appendix.
    validation_command: uv run --frozen --all-extras --group dev python selftest.py (from the scratch directory, with the project interpreter)
    kill_condition: The exact verifier disagrees with lane C's retained margin 14979/1060025 or with exp-121's strict escape.
    fallback: Reduce the engine to the fixed-candidate exact checker of exp-121 and search by hand.
    outcome: >-
      Engine written and self-tested: lane C's escape reproduced to the exact margin,
      exp-121's frozen square reproduced as a strict escape, the search rediscovers an
      escape of P10 at q (a larger one, at the bottom wall), and both controls report none.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-e-ownership-set-at-q.md
    stop_reason: Bounded output complete and self-tested.
    next_action: Run the candidate sets and the adversarial and exact searches.
  - workflow: research-loop
    focus: insight
    recording: contemporaneous
    clock_role: work
    objective: >-
      Candidate sets from the atom skeleton scaled by 384/381, Stromquist's ten points plus
      one, adversarial min-max over free and K4-symmetric eleven-point sets, and an exact
      branch-and-bound over test squares driven by the falsifier as a cutting-plane loop.
    commitment: BC-302
    bead: think-qfog
    status: completed
    entered_by: planned_checkpoint
    switch_reason: The engine is verified; the block's question needs the candidate sets and their escapes.
    budget_minutes: 90
    started_at: '2026-09-08T04:48:00Z'
    deadline_at: '2026-09-08T06:18:00Z'
    expected_output: The escape catalogue with exact poses and the branch-and-bound verdict, in the lane document.
    validation_command: uv run --frozen --all-extras --group dev python candidates.py, minimax.py, loop.py (scratch directory, project interpreter); every reported escape re-verified by escape_engine.exact_verify.
    kill_condition: A candidate set with no verified escape at step 0.02 and angle step 1.5 degrees, which switches the lane to the proof attempt.
    fallback: Publish the catalogue at its current scope with the resolution of every non-refutation.
    outcome: >-
      Every point set tested has an exactly verified escape (W11 0.41449, G11 0.06310,
      P10 and P10 plus one 0.03188, the polished K4 optimum 0.01401, the free optimum
      0.01720); an independent standard-library reader agrees on all 22 catalogued
      escapes; the exact branch-and-bound loop stayed alive (150 tests, 151 nodes) and
      was stopped. Segment marks: Stromquist's ten points as horizontal segments of
      length 1/10 have no escape at steps 0.02/1.5 and 0.01/0.75 degrees, and an interval
      reader over pose space certifies the cover (404613 boxes, 184756 leaves, 0
      failures), re-checked exactly leaf by leaf and discard by discard and sampled at
      6000 poses; length 9/100 certifies, 8/100 does not, 7/100 escapes.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-e-ownership-set-at-q.md
    stop_reason: The block's question is answered at its scope, with a certified survivor for the segment form and an exact escape for every point set.
    next_action: Write the lane document, the README line and this record; validate the records tier; commit.
  - workflow: documentation-pass
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: The lane document, the one-line README entry, this record, the records-tier validation and the commit.
    commitment: BC-302
    bead: think-qfog
    status: in_progress
    entered_by: planned_checkpoint
    switch_reason: The computations are at their block scope; the remaining time is the record.
    budget_minutes: 45
    started_at: '2026-09-08T05:25:00Z'
    deadline_at: '2026-09-08T06:10:00Z'
    expected_output: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-e-ownership-set-at-q.md and this record.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: The block's deadline.
    fallback: Commit what is written with the checkpoint file naming what is missing.
    outcome: >-
      Lane document with the theorem, the reader's soundness argument, the catalogue and
      every script and output in its appendix; one README line; this record; the records
      tier run from the worktree before the final commit, its result in checks. The phase
      stays open for the coordinator's integration, the ledger re-render and the rollup.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-e-ownership-set-at-q.md
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/README.md
    stop_reason: null
    next_action: The coordinator integrates the branch, allocates an experiment id if the frozen claim is registered, and closes this record with the harness rollup under think-qfog.
  primary_bead: think-qfog
  status: in_progress
  budget:
    wall_minutes: 150
    checkpoint_minutes: 30
  stop_conditions:
  - The block's 2.5-hour clock; no extension for a promising result.
  - An escape is a result only when verified exactly; a no-escape reading carries its resolution and is never a theorem.
  - No identifiers allocated, no shared registry edited, no push.
  progress:
    metric: candidate mark sets decided (exact escape, certified cover, or unrefuted with resolution)
    before: >-
      H-134 registered with a prior of about thirty per cent; the only escape instrument
      is exp-121's fixed-candidate checker; no candidate eleven-mark set at 96/25 has been
      tested.
    after: >-
      Thirteen point sets decided negatively by exact escapes (best clearance 0.01401);
      one ten-segment set and two eleven-mark segment sets certified robustly
      unavoidable at 3/500 by an exact interval reader; one set (length 8/100)
      unrefuted and uncertified; three structural lemmas proved (no LP obstruction, ten
      forced marks, symmetry). H-134's segment form is met; the claim to freeze is
      Theorem E.4 of the lane document, which needs an experiment id.
  delegations: []
  outputs:
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-e-ownership-set-at-q.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/README.md
  checks:
  - packing-validate --records from the lane worktree before the final commit (4 cpus, about 44 s wall) passes every step except three that need the coordinator's integration re-renders and that this lane may not perform, namely the document map row for the lane document (check_documentation), the session-close report and SYNOPSIS render (close_session --render), and the ledger render (packing-ledger render); the session record's own checks (schema, clocks, gate, rollups) pass. A first run had also failed on a YAML colon in this record's phase-2 stop_reason, fixed before this run.
  - A second interval reader with the Hausdorff bound (cover_reader2.py) was written; its float cover did not finish in two bounded runs of 9 and 7 minutes at load 10 to 14, and its full exact pass was stopped after 10 minutes, so it is recorded as not completed and is the next session's first replay.
  - Engine self-tests (selftest.py) passed; the independent reader agreed on all 22 catalogued escapes; the interval reader's exact mode re-decided 184756 leaves and 17551 discards with no failure; 6000 sampled poses inside certified leaves were within 3/500 of a mark by the falsifier's exact distance.
  resource_rollups: []
  stop_reason: null
  next_action: >-
    Coordinator: integrate the lane branch, register the document in the document map, and
    close this record under think-qfog once the harness rollup exists; the lane document's
    section 7 names what the next session does first.
---
# session-104 — A Robust Unavoidable Set of at Most Eleven Marks at 96/25

The lane’s question, engine, catalogue, theorem and obstructions are in
[the lane document](../series/series-000-smoke-and-calibration/results/agenda-030/lane-e-ownership-set-at-q.md);
the checkpoint file in the scratch directory records the three thirty-minute checkpoints
and the coordinator’s steering at 05:11 UTC (one computation at a time from then on,
with the load beside every wall time), which was followed.

What changed in H-134’s standing: its claim is met by ten short segments, not by points
from the atom skeleton, and the proof is a computation with an exact re-check rather
than Stromquist’s hand lemmas.
The record does not mark the hypothesis accepted; that is the coordinator’s call after
an independent replay under an experiment id, which this session did not allocate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
