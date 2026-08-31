---
title: "session-050 — block 1 of the two-lane overnight run: the certifier instrument and the falsifier"
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-050
  primary_bead: think-y2ju
  status: in_progress
  title: "Block 1 of the two-lane overnight run: the certifier instrument and the falsifier"
  date: '2026-08-31'
  started_at: '2026-08-31T05:40:00Z'
  deadline_at: '2026-08-31T08:10:00Z'
  goal: >-
    Agenda-010 block 1, 150 minutes: BC-093 (generalize the Stromquist
    certifier-falsifier pair into a resource-system instrument, exit on the exp-016 and
    exp-017 controls replayed byte-stable through the general core with the bespoke
    module reduced to a caller) then BC-094 (the escaping-pose search with think-yrvm's
    known-answer triple). The run's continuity floor is a 20-minute recurring reminder
    the owner armed; per OR-8 it is not this run's to delete. The nine-hour wall is
    14:40Z with finalization from 14:10Z, owner-imposed.
  workflow_phases:
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-093
    bead: think-y2ju
    objective: >-
      Extract the reusable exact core from cases/stromquist -- resource declarations
      (points now; weighted points, segments, threshold charges, moving families as
      typed not-yet-supported refusals where the Stromquist proof does not exercise
      them), a box family at a declared container side, and replayable cover
      certificates -- into a general instrument, with the bespoke Q(sqrt 5) module
      reduced to a caller and the field seam against sqpack.field resolved or its
      refusal recorded.
    status: in_progress
    entered_by: session_start
    switch_reason: null
    budget_minutes: 90
    started_at: '2026-08-31T05:40:00Z'
    deadline_at: '2026-08-31T07:10:00Z'
    expected_output: >-
      A general certifier module with the exp-016 printed-set refusal and the exp-017
      repaired-set certificate both replayed through it byte-stable, tests for the
      general core, and the bespoke module calling into it.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --push
    kill_condition: >-
      Any behavioral difference between the general core's replay and the retained
      exp-016/exp-017 records, or the extraction growing past reduction into rewrite --
      a slice that cannot keep the old module's outputs byte-identical stops and records
      what diverged rather than relaxing the comparison.
    fallback: >-
      Retain the bespoke module untouched, land the general core beside it with the
      divergence recorded as the block's finding, and hand BC-094 the search interface
      only.
    outcome: null
    evidence: []
    stop_reason: null
    next_action: >-
      Slice 1 under think-y2ju: first-hand read of repaired_cover.py's structure
      against the delegated read-only map, then the core-extraction cut list.
  budget:
    wall_minutes: 150
    finalization_minutes: 15
  progress:
    metric: >-
      Whether block 1's two instruments exist with their controls green: the general
      certifier replaying exp-016/exp-017 byte-stable, and the falsifier passing
      think-yrvm's known-answer triple.
    before: >-
      The certifier is 2,645 lines hard-wired to one figure of one paper over a bespoke
      Q(sqrt 5); no escaping-pose search exists; both exp controls pass only through
      the bespoke module.
    after: null
  stop_conditions:
  - >-
    Any candidate mathematical verdict this session produces is recorded unresolved
    with needs_review rather than promoted, and no verified_* field moves tonight.
  - >-
    Nothing is pushed without packing-validate --push green on the exact tree; --records
    runs before every push and the push goes out before slower checks finish (OR-3).
  - >-
    The 20-minute continuity reminder and the 14:07Z finalization alarm are the owner's;
    this run may not delete or disable either (OR-8, D-395).
  delegations:
  - task: >-
      Read-only structural map of cases/stromquist for the BC-093 extraction: general
      versus Stromquist-specific inventory, the exact-arithmetic layer against
      sqpack.field, the cover-check core's decomposition, the certificate/replay
      plumbing, resource kinds actually exercised, and a recommended minimal cut with
      the three riskiest couplings for byte-stable replay.
    operator: claude-sub-agent-certifier-map
    status: completed
    recording: contemporaneous
    outcome: >-
      Full inventory of both files with general/Stromquist tags per function. Load-bearing
      findings: the cover check is two-stage (exact polygonal tiling validation, then a
      per-cell lemma certificate), with the tiling/mesh/partition validators, geometry
      primitives, escape predicates, and record/replay plumbing all general and the point
      data, K4 symmetry, and Lemma 3/4/6 specifics Stromquist-bound; the Q5 scalar is
      standalone with closed-form sign while FieldElement lacks only comparison operators
      and a text() serializer; no resource kind beyond capacity-1 points with an integer
      forced-triple parameter exists in code. Three byte-stability risks named: Q5.text()
      formatting, fraction_text/exact_value float formatting, and the certificate dict
      structure the replay compares recursively.
    evidence:
    - packing/cases/stromquist/printed_cover.py
    - packing/cases/stromquist/repaired_cover.py
    - packing/src/sqpack/field.py
    files:
    - no repository file written; read-only investigation
    checks:
    - report reviewed under OR-2 before any cut lands; parse claims verified by parsing
    uncertainty: >-
      A report is evidence, not a verdict (OR-2): the general/Stromquist tagging and the
      three byte-stability risks are re-verified first-hand before the cut lands.
    elapsed_seconds: 236
    elapsed_quality: platform_measured
    next_action: >-
      Reconcile against the coordinator's own read of the cover-check core, then cut.
    kill_condition: >-
      The report contradicting the coordinator's first-hand read of the certificate
      core, or any parse claim not verified by parsing (the OR-2 trap).
    fallback: >-
      Discard the map and cut from the first-hand read alone, slower.
    write_scope:
    - no repository writes; read-only investigation
    phase: 1
    started_at: '2026-08-31T05:52:00Z'
    deadline_at: '2026-08-31T06:40:00Z'
    excluded_commands: [git, tbd, packing-validate]
  - task: >-
      Read-only design reconnaissance for the BC-094 falsifier: H-010 and H-041
      registered criteria, exp-016's strict-escape representation and verification,
      existing search primitives in sqpack, the code's own avoidance predicates, a
      10-15 line recommended design, and the negative controls that would catch a wrong
      falsifier.
    operator: claude-sub-agent-falsifier-recon
    status: completed
    recording: contemporaneous
    outcome: >-
      H-010/H-041 criteria and regimes extracted verbatim; the escape representation is
      (center, cosine, sine, side L > 1) with strictness decided by exact sign on the
      local-frame L-infinity margin and container fit via verify_packing with
      check_shapes=False; the avoidance predicate is inline in both escape functions and
      not yet factored; the quench is not reusable for the falsifier (different problem)
      but scipy is available for coarse-grid-plus-Nelder-Mead search over (x, y, theta)
      with theta in [0, pi/4]; no controls.yaml negative controls exist for a wrong
      falsifier, so the known-answer triple must land as the falsifier's own tests; a
      saturation report must carry resolution, candidates, best margin, defeating pose,
      and the not-a-proof caveat.
    evidence:
    - packing/campaign/hypotheses/H-010-stromquist-triple.md
    - packing/campaign/hypotheses/H-041-repaired-stromquist-point-set.md
    - packing/cases/stromquist/printed_cover.py
    - packing/src/sqpack/verify.py
    files:
    - no repository file written; read-only investigation
    checks:
    - report reviewed under OR-2 before the design is adopted
    uncertainty: >-
      Same OR-2 posture; the claim that no standalone box-avoidance verifier exists is
      re-checked against the tree before the falsifier interface is fixed.
    elapsed_seconds: 223
    elapsed_quality: platform_measured
    next_action: >-
      Fold into the BC-094 slice when phase 2 opens.
    kill_condition: >-
      A recommended design that contradicts the retained escape records or H-010's
      registered criteria on a first-hand check.
    fallback: >-
      Design the falsifier from exp-016's construction alone.
    write_scope:
    - no repository writes; read-only investigation
    phase: 1
    started_at: '2026-08-31T05:52:00Z'
    deadline_at: '2026-08-31T06:40:00Z'
    excluded_commands: [git, tbd, packing-validate]
  outputs:
  - packing/campaign/agent-sessions/session-050-block1-certifier-and-falsifier.md
  checks:
  - uv run --frozen --all-extras --group dev packing-validate --records
  stop_reason: null
  next_action: >-
    The session is in progress on `BC-093` under `think-y2ju`: slice 1 reads the
    certifier core first-hand and produces the extraction cut list; `think-yrvm`
    opens phase 2.
---
# Session-050 — Block 1: the Certifier Instrument and the Falsifier

Contemporaneous record; the frontmatter is the session.
Agenda-010 owns the block plan, X-010 owns the argument, think-y2ju and think-yrvm own
the work items.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
