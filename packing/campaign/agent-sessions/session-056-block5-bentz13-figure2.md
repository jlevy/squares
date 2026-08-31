---
title: "session-056 — block 5 of the overnight run: the m = 4 foundation layer"
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-056
  primary_bead: think-1o1f
  status: completed
  title: "Block 5 of the overnight run: the m = 4 foundation layer"
  date: '2026-08-31'
  started_at: '2026-08-31T08:50:00Z'
  deadline_at: '2026-08-31T11:20:00Z'
  goal: >-
    BC-099's own question, continued: encode the foundation layer of Bentz 2010
    Section 3 (Theorem 9, s(13) = 4) against the general instrument -- Figure 2's
    sixteen-point configuration certified unavoidable, then Lemma 10 as three
    replacement-set certificates. The coordinator's first-hand read settles three
    things the block leans on: every Section 3 coordinate is a rational decimal,
    so the whole layer runs over pure Fraction scalars with radical comparisons
    squared away rationally; the wall-touch disjunct in Lemmas 1 and 4 is vacuous
    for open boxes inside the container (the same walls-uncontainable principle
    already discharged in the Theorem 8 certificate by the wall-placement check);
    and the unchargeable tiling vertex at (1, 1) is absorbed by using corner
    pentagons ([0,1]^2 minus the A-B-(1,1) sliver) as the Lemma 1 cells beside an
    A-B-D Lemma 2 triangle that contains (1,1) strictly. Figures 2-4 are
    unextractable, so the tilings are reconstructed from the prose exactly as
    Theorem 8's Figure 1 was; either outcome of any piece is a result.
  workflow_phases:
  - workflow: research-loop
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-099
    bead: think-1o1f
    objective: >-
      Slice 1: cases/bentz13 -- build Figure 2's sixteen points exactly over
      Fraction (A(1, 457/500), B, C(457/500, 2), D(33/20, 33/20) and their
      mirror orbit under x = 2, y = 2, y = x), reconstruct the cover designed
      first-hand (4 Lemma 1 corner pentagons, 8 Lemma 4 wall rectangles at
      a = 1, b = 457/500 with both inner corners set points, 18 Lemma 2
      triangles through the D orbit), validate the tiling through cover's
      validators, and certify every cell premise by exact rational sign --
      Lemma 4's a + 2b <= 2 sqrt 2 as (a + 2b)^2 <= 8, Lemma 2's sides as
      squared lengths <= 1, Lemma 1's outs as A and B lying inside the corner
      triangle spanned by (1, 1), (9/10, 1), (1, 9/10).
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 60
    started_at: '2026-08-31T08:50:00Z'
    deadline_at: '2026-08-31T09:50:00Z'
    expected_output: >-
      cases/bentz13 (packing.py construction plus a verify_cover certificate for
      the Figure 2 configuration) green with tests; or the typed report naming
      the cell that resisted and the pose that defeats it.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      Any cell premise the printed constants fail exactly, or any tiling the
      validator refuses after the falsifier corroborates the cell design --
      each stops the slice and records the defeating configuration rather than
      relaxing a check. Candidate verdicts land unresolved with needs_review.
    fallback: >-
      Retain whatever certifies (the tiling alone, or the wall-and-corner layer
      with the interior recorded as the resisting step) as a partial certificate
      with a typed remainder on think-1o1f.
    outcome: >-
      Two results, both on the first complete run. Figure 2's base configuration
      is machine-certified: cases/bentz13 builds the sixteen points exactly over
      Fraction and verify_cover certifies the thirty-cell partition of [0, 4]^2
      and every cell premise by exact rational sign -- 4 Lemma 1 corner pentagons
      (outs on the conclusion triangle), 8 Lemma 4 wall rectangles (slack
      604/250000 strictly positive, both inner corners set points), 18 Lemma 2
      triangles (longest side squared 964196/1000000) -- 16 of 16 charged,
      0.04 s, five tests pinning the
      certificate and refusals. And the Lemma 10 audit found a candidate printed
      defect: the replacement point (1, 1.74) is refuted by an exact escape
      certificate (the axis-aligned box of side 1001/1000 at (73/50, 7/10)
      avoids the entire printed replacement set), while the corrected reading
      (1.74, 1) is contained by the same box and corroborated three independent
      ways (S_A's hull needs it; Section 3.1's alternatives use its mirror; the
      printed point is exactly the y = x mirror the B-version delivers). Both
      results held unresolved with needs_review; the transcription carries the
      audit note at Lemma 10 in the Corollary 7 convention; the raw extraction
      reads the same, so paper-versus-pipeline is typed undecidable here.
    evidence:
    - packing/cases/bentz13/packing.py
    - packing/cases/bentz13/verify_cover.py
    - packing/cases/bentz13/lemma10_audit.py
    - packing/tests/test_bentz13.py
    stop_reason: >-
      Both slice objectives met inside budget; the checkpoint commit protects the
      results before phase 2 attempts the corrected replacement certificates.
    next_action: >-
      Phase 2: the margin-cell kind (box-centre-infeasible wall bands), then the
      corrected replacement certificates for (1.12, 1), (1.74, 1), and
      (1.87, 0.76), as far as the wall allows.
  - workflow: research-loop
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-099
    bead: think-1o1f
    objective: >-
      Slice 2: Lemma 10's three replacement certificates against the corrected
      reading. The instrument gains one honest cell kind first -- margin cells,
      entirely within distance 1/2 of a container wall, where no box centre can
      lie because boxes have side strictly above one and sit inside the
      container -- and each replacement set gets its own retiling near old A:
      (1.12, 1) and (1.74, 1) keep most of the Figure 2 complex, while
      (1.87, 0.76) reworks the bottom strip around its low replacement point.
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      Phase 1 met both objectives early; the audit's corrected reading is what
      the replacement certificates must now certify for Lemma 10 to hold as
      repaired.
    budget_minutes: 75
    started_at: '2026-08-31T09:03:00Z'
    deadline_at: '2026-08-31T10:18:00Z'
    expected_output: >-
      cases/bentz13 replacement certificates green as tests for as many of the
      three corrected points as the wall allows, the margin kind certified with
      its own refusal control, and the remainder typed on think-1o1f.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      Any replacement whose retiling needs a lemma the kit does not carry --
      that stops the slice and records the resisting configuration rather than
      inventing a premise. Candidate verdicts land unresolved with needs_review.
    fallback: >-
      Retain whichever replacements certify with the others typed as the next
      slice's first work.
    outcome: >-
      Lemma 10 is machine-settled both ways. The certifier gained subset
      semantics (a cell may be any subset of its declared lemma region) and two
      new honest kinds -- margin cells (within 1/2 of a wall, where no box
      centre can lie) and near cells (every vertex within 1/2 of the named
      point, which any box centred there contains via its inscribed ball) --
      plus the rational-a Lemma 5 threshold bound. With those, all three
      corrected replacement sets certify on first complete runs: (1.12, 1) with
      a Lemma 5 quad at a = 22/25, b = 457/500 (certified infimum bound
      0.936340), (1.74, 1) with margin plus near cells alone, and
      (1.87, 0.76) with the quad at a = 239/250, b = 19/25 (bound 0.780032).
      Both quads sit inside exactly the parameter families Bentz's Section 1
      lists for Lemma 5 use -- strong corroboration that the corrected reading
      matches the intended figures. Together with the escape certificate
      against the printed point, Lemma 10 is refuted as printed and certified
      as corrected; nine tests pin all of it. Held unresolved with needs_review
      per the unattended rules.
    evidence:
    - packing/cases/bentz13/lemma10_replacements.py
    - packing/cases/bentz13/verify_cover.py
    - packing/tests/test_bentz13.py
    stop_reason: >-
      All three replacements certified inside the phase budget; the block's
      remaining wall goes to closing records and the next block.
    next_action: >-
      Close the session; block 6 opens as session-057 on `BC-101` under
      `think-q6vy`, with Section 3.1's staged sets as the m = 4 continuation
      typed on think-1o1f.
  budget:
    wall_minutes: 150
    finalization_minutes: 15
  progress:
    metric: >-
      How much of Theorem 9's proof spine certifies mechanically: the Figure 2
      configuration, then Lemma 10's three replacement sets, then the staged
      Section 3.1 sets -- against none of it ever having been machine-checked.
    before: >-
      Theorem 8 is certified and held for review; Section 3 is mapped and typed
      on think-1o1f (Section 3.1 first, sliding point Z the one new premise
      type, one candidate printed gap at the Lemma 11 case split) but no m = 4
      configuration has ever been machine-certified.
    after: >-
      The foundation layer certifies whole: Figure 2's base configuration (30
      exact cells, 16/16 charged) and Lemma 10 settled both ways -- refuted as
      printed by an exact escape certificate, certified as corrected by three
      replacement covers whose Lemma 5 quads sit in exactly the parameter
      families the paper lists. The certifier's subset semantics, margin and
      near kinds, and rational-a threshold bound now exist for every later
      Section 3 configuration. All verdicts held unresolved with needs_review;
      the m = 4 continuation (Section 3.1's staged sets) is typed on
      think-1o1f.
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
  - packing/campaign/agent-sessions/session-056-block5-bentz13-figure2.md
  - packing/cases/bentz13/packing.py
  - packing/cases/bentz13/verify_cover.py
  - packing/cases/bentz13/lemma10_audit.py
  - packing/cases/bentz13/lemma10_replacements.py
  - packing/tests/test_bentz13.py
  checks:
  - uv run --frozen --all-extras --group dev packing-validate --records
  resource_rollups:
  - packing/campaign/resource-usage/913a5de0-f775-52cc-8f42-a03fcbd8234b.yaml
  stop_reason: >-
    Block objective exceeded inside the wall: the foundation layer and the full
    Lemma 10 settlement landed with two hours of block budget unspent, so the
    session closes early and the run advances to the promoted BC-101.
  next_action: >-
    Block 6 opens as session-057 on `BC-101` under `think-q6vy`: the Green
    sizes ladder, per the checkpoint's promotion.
---
# Session-056 — Block 5: The m = 4 Foundation Layer

Contemporaneous record; the frontmatter is the session.
The tiling design this block certifies was derived first-hand before any code:
corner pentagons under Lemma 1 (their conclusion triangle contains both near-corner
points, and the pentagon cut keeps the unchargeable notch vertex out of every
Lemma 2 cell), wall rectangles under Lemma 4 with both inner corners set points
(no wall-vertex outs needed at all in this figure), and an eighteen-triangle
Lemma 2 layer through the D orbit whose longest side squared is 964196/1000000
(the first draft of this note wrote 964096, a hand-arithmetic slip the certificate
caught).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
