---
title: "session-057 — block 6 of the overnight run: the Green sizes ladder"
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-057
  primary_bead: think-q6vy
  status: completed
  title: "Block 6 of the overnight run: the Green sizes ladder"
  date: '2026-08-31'
  started_at: '2026-08-31T09:42:00Z'
  deadline_at: '2026-08-31T12:12:00Z'
  goal: >-
    BC-101, about 135 minutes: move the verified lower lane at n = 17 for the
    first time since 2005. DS7 records Green's Theorem 9 --
    s(17) >= (40 sqrt 2 + 19)/17, about 4.4452 -- with Figure 34 unextractable
    and no primary source (private communication), so certifying a set of our
    own is the only adoptable route. The coordinator's scouting settles the
    frame: a Bentz-style rational grid (rows at y0 = 457/500 + k * 433/500,
    unit x spacing) certifies through the bentz13 machinery with everything
    rational, a plain 14-point grid cannot exceed side 4 (the scaled 4x4 grid
    packing yields a concrete escaping box, consistent with s(16) = 4), and the
    16-point budget for n = 17 leaves two reinforcement points for the loose
    edge. The loop is CEGIS: the falsifier screens candidate sets in float, the
    certifier promotes the survivor exactly. Any certified side above
    Nagamochi's closed form (about 4.1623 at n = 17) meets the cell's exit;
    Green's own value is the stretch goal.
  workflow_phases:
  - workflow: research-loop
    recording: contemporaneous
    clock_role: work
    focus: insight
    commitment: BC-101
    bead: think-q6vy
    objective: >-
      Slice 1: parameterize the rational cover machinery (side and boundary as
      parameters; the bentz13 kinds -- corner pentagons, wall rectangles,
      Lemma 5 quads, margin, near, triangles -- already carry every needed
      premise), build the candidate generator for grid-plus-reinforcement sets
      at rational sides above 4, and run the falsifier screen to find the
      escape zones that fix the reinforcement placement. Certify the best
      surviving set exactly.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 75
    started_at: '2026-08-31T09:42:00Z'
    deadline_at: '2026-08-31T10:57:00Z'
    expected_output: >-
      cases/green17 with an exactly certified unavoidable set of at most 16
      points at a rational side above 4.1623, wired as tests and held
      unresolved with needs_review; or the typed report naming the best side
      reached and the escaping pose that defeated every candidate above it.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      A candidate that certifies only by weakening a premise check, or an edge
      zone no kit lemma covers -- either stops the slice and records the
      configuration rather than inventing a premise. No verified_* or frontier
      field moves tonight; adoption is a reviewed evidence-contract change.
    fallback: >-
      Retain the parameterized builder and the falsifier screen results as the
      instrument, with the best certified side (even 4) as the calibration and
      the remainder typed on think-q6vy.
    outcome: >-
      The verified lower lane moves: sixteen points make [0, 17/4]^2 unavoidable,
      certified exactly on the first complete run -- s(17) >= 17/4 = 4.25 and
      s(18) >= 17/4, above Nagamochi's 4.1623 -- held unresolved with
      needs_review; any frontier move is a reviewed evidence-contract change.
      The design was derived first-hand rather than searched: a rationalized
      Bentz grid (rows at 457/500 + k*433/500, diagonals squared 249989/250000)
      with an x = 7/2 column appended to every row, wall strips with
      wall-vertex ends (the Theorem 8 justification ported into the shared
      certifier), three left-wall Lemma 5 quads at the paper's own (433/500,
      1/2) family, a right margin band of exactly 1/2, and four near-slabs
      whose worst corners sit at squared distance 249989/1000000 -- slack
      11/1000000, which pins the side to exactly 17/4: the same structure
      refuses at any larger rational side, and the certifier proves that too
      (the pushed-margin control). The falsifier corroborates independently:
      393,216 poses plus refinements saturate at best margin -1e-4, tightest at
      the wall corner against p0_0, with its not-a-proof caveat intact. The
      certifier gained left-wall Lemma 5 orientation, wall-vertex Lemma 4 outs,
      and Lemma 2 faces with collinear boundary vertices; five tests pin the
      certificate, the saturation, and three refusal controls.
    evidence:
    - packing/cases/green17/packing.py
    - packing/cases/green17/verify_cover.py
    - packing/tests/test_green17.py
    - packing/cases/bentz13/verify_cover.py
    stop_reason: >-
      The cell's exit is met one hour inside the phase budget: a certified set
      above the closed form at both target sizes, with the escaping-pose
      control and instrument growth recorded.
    next_action: >-
      Close the session and the block; the remaining wall goes to the
      finalization reserve and, if the owner's review reopens it, the
      seventeen-point n = 19 variant typed on think-q6vy.
  budget:
    wall_minutes: 150
    finalization_minutes: 15
  progress:
    metric: >-
      The best exactly certified side for an at-most-16-point unavoidable set,
      against Nagamochi's 4.1623 and Green's unadoptable 4.4452 at n = 17.
    before: >-
      No certified set above the closed form exists at any open n; the verified
      lower lane has not moved at n = 17 since 2005; the instruments (certifier
      with six cell kinds, falsifier with exact escape certificates) are green
      from blocks 1 and 5.
    after: >-
      s(17) >= 17/4 and s(18) >= 17/4, certified exactly by a sixteen-point set
      whose side is pinned by an 11/1000000 slack, corroborated by falsifier
      saturation, held unresolved with needs_review. The best certified side for
      this structure is exactly 17/4; pushing further needs either more points
      (the n = 19 variant has one spare) or a genuinely different edge
      structure, and Green's 4.4452 remains the stretch mark.
  stop_conditions:
  - >-
    Any candidate mathematical verdict is recorded unresolved with needs_review;
    no verified_* field moves tonight.
  - >-
    Nothing is pushed without packing-validate --push green on the exact tree.
  - >-
    The 20-minute continuity reminder and the 14:07Z finalization alarm are the
    owner's; this run may not delete or disable either (OR-8, D-395).
  delegations: []
  outputs:
  - packing/campaign/agent-sessions/session-057-block6-green-sizes.md
  - packing/cases/green17/packing.py
  - packing/cases/green17/verify_cover.py
  - packing/tests/test_green17.py
  checks:
  - uv run --frozen --all-extras --group dev packing-validate --records
  resource_rollups:
  - packing/campaign/resource-usage/913a5de0-f775-52cc-8f42-a03fcbd8234b.yaml
  stop_reason: >-
    Block objective met an hour inside the wall; the run's committed blocks are
    all discharged, so what remains goes to finalization per the agenda.
  next_action: >-
    Finalization: close every open record, refresh PR #66 per OR-9 on `BC-101`
    under `think-q6vy`, and write the handoff.
---
# Session-057 — Block 6: The Green Sizes Ladder

Contemporaneous record; the frontmatter is the session.
The scouting that framed this block is recorded in the goal: the plain grid's
side-4 ceiling was established by a concrete scaled-grid escape before any code,
so the block's question is what the two reinforcement points buy above it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
