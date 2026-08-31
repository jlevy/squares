---
title: session-050 — the exp-045 independent audit, the -W bridge, and the acceptance
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-050
  primary_bead: think-1s0h
  status: in_progress
  title: The exp-045 independent audit, the -W bridge, and the acceptance
  date: '2026-08-31'
  started_at: '2026-08-31T03:05:00Z'
  deadline_at: '2026-08-31T04:55:00Z'
  goal: >-
    Perform the independent post-change audit that has been exp-045's sixth admission
    condition since registration -- by an agent that built none of the instrument --
    resolve whatever the audit finds, and record the owner's accept decision if and only
    if everything comes back green. The owner directed this in conversation after
    reading the audit's first-principles account and its findings.
  workflow_phases:
  - workflow: factual-review
    recording: contemporaneous
    clock_role: work
    focus: correctness
    bead: think-1s0h
    objective: >-
      Audit the complete exp-045 instrument against its six admission conditions:
      replay the retained certificate, prove the replay non-vacuous, run the helper test
      perimeter, and check each condition against the artifacts rather than the session
      narratives that claimed them.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 40
    started_at: '2026-08-31T03:05:00Z'
    deadline_at: '2026-08-31T03:45:00Z'
    expected_output: >-
      A per-condition disposition with findings, each tied to an artifact, and a
      first-principles account of what the round establishes at what strength.
    validation_command: >-
      uv run --frozen python -m cases.n5.minus_w_obstruction --replay
      campaign/series/series-000-smoke-and-calibration/results/exp-045-h-023-n5-minus-w-scale-and-controls.json
    kill_condition: >-
      Accepting a condition on a session record's say-so where the artifact disagrees;
      the audit exists because the builder's own sessions read these conditions as
      satisfied.
    fallback: >-
      Report the findings and stop; an audit that cannot finish is itself a disposition.
    outcome: >-
      Replay green in 2.2s with byte-identical regeneration, and non-vacuous: a
      perturbed copy is refused with replay.drift. Thirty helper tests pass. Conditions
      two, four and five hold against the artifacts. Three findings: the registration's
      twelve mutation identifiers match the artifact's only five-for-twelve, with the
      substitution derived in session-032 but never mapped or amended; the driver never
      routes through the accepted production helpers (condition one not demonstrably
      met), which had run only on the +W control; and the driver's docstring still
      described the exp-043 draft. Recommended: do not accept as-is; remediate and
      re-run.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-045-h-023-n5-minus-w-scale-and-controls.md
    - packing/campaign/agent-sessions/session-032-block1-missing-mutations.md
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-045-h-023-n5-minus-w-scale-and-controls.json
    stop_reason: >-
      Every condition dispositioned against an artifact; the findings were reported to
      the owner, who directed the remediation.
    next_action: >-
      Close the condition-one gap by corroboration: run the accepted helpers on the
      actual -W direction.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    bead: think-1s0h
    objective: >-
      Build the -W bridge: the accepted row-jet, stress, scale, and owner-4 helpers run
      on the actual -W direction at every stratum, compared coefficient-by-coefficient
      against the retained certificate and the +W control, as a durable checker with
      sensitivity controls.
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      The audit's decisive gap -- condition one -- is closable by making the helpers
      decide the same question the certificate decided, which is a reusable capability
      with a named consumer (the acceptance), so it enters W7.
    budget_minutes: 35
    started_at: '2026-08-31T03:45:00Z'
    deadline_at: '2026-08-31T04:05:00Z'
    expected_output: >-
      devtools/check_minus_w_bridge.py green, held by tests/test_minus_w_bridge.py with
      controls proving a doctored direction is refused and the deciding constant is a
      genuine quadratic.
    validation_command: >-
      uv run --frozen --all-extras --group dev python -m pytest -q
      tests/test_minus_w_bridge.py
    kill_condition: >-
      Any disagreement between the helpers and the certificate: a nonzero correction
      coefficient, a non-negative deciding constant or cusp, or a +W/-W asymmetry. A
      disagreement ends the acceptance question and opens a soundness investigation.
    fallback: >-
      Retain the disagreement as a finding; the bridge failing is more important than
      the acceptance succeeding.
    outcome: >-
      The bridge agrees at every stratum. The negated production W equals the retained
      canonical_minus_W exactly; all fifteen owner-3 scale records build with every
      correction and beta coefficient exactly zero, deciding constant -1/4, and both
      cusp coefficients strictly negative (1/4 - sqrt(2)/2 and -5/4 + sqrt(2)/2); all
      three owner-4 records give the same correction-independent -1/4; and every
      coefficient equals its +W twin, deriving the sign-symmetry determination
      independently. The first control attempt taught something real: the deciding
      constant is insensitive to eight of fifteen coordinates, so the retained tests
      use the doubling law (exactly x4) and a sensitive coordinate instead. One
      duplicate-cost decision recorded in the checker: gate coverage is the test file,
      not a named step, because the check costs 75 seconds and a step would pay it
      twice.
    evidence:
    - packing/devtools/check_minus_w_bridge.py
    - packing/tests/test_minus_w_bridge.py
    stop_reason: >-
      Three tests green, checker green standalone, and the bridge's number tied to the
      certificate's obstruction_coefficient.
    next_action: >-
      Record the resolutions and the owner's acceptance.
  - workflow: factual-review
    recording: contemporaneous
    clock_role: work
    focus: process
    bead: think-1s0h
    objective: >-
      Record the audit's resolutions where the next auditor will look: the amendment in
      the experiment record (identifier map, retention equivalence, docstring), D-404,
      the verdict flip to accepted under the owner's direction, BC-029's completion,
      and the SYNOPSIS reconciliation.
    status: in_progress
    entered_by: evidence_checkpoint
    switch_reason: >-
      The bridge closed the mathematical gap; what remains is the record carrying the
      acceptance and its provenance, which is review-owned bounded correction.
    budget_minutes: 30
    started_at: '2026-08-31T04:05:00Z'
    deadline_at: '2026-08-31T04:30:00Z'
    expected_output: >-
      exp-045 accepted with the frozen criterion untouched and an Amendment section;
      D-404 rendered; agenda-003 BC-029 complete; SYNOPSIS aggregates and narratives
      reconciled; the records tier green; the branch pushed and a pull request open.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      Any wording that widens the claim boundary, or an acceptance recorded anywhere
      without naming who granted it and on what audit.
    fallback: >-
      Leave the verdict unresolved with the amendment in place and the acceptance as
      the named next action.
    outcome: null
    evidence: []
    stop_reason: null
    next_action: >-
      Push, open the pull request, and close this session with the tool.
  budget:
    wall_minutes: 110
    finalization_minutes: 20
  stop_conditions:
  - >-
    A bridge disagreement stops everything: no acceptance is recorded over a live
    soundness question.
  - >-
    The frozen primary criterion is never edited; resolutions go in the amendment, and
    the registered mutation list stays as what was registered.
  - >-
    The claim boundary does not move a word: one direction, three poses, no H-023
    disposition.
  progress:
    metric: >-
      Whether exp-045's acceptance rests on an independent audit an outsider can replay,
      and whether the gate that held BC-010 and BC-029 is genuinely cleared.
    before: >-
      exp-045 terminal at unresolved/needs_review since session-033, with the sixth
      admission condition unperformed and two P0 commitments parked behind it. The
      registration and the artifact disagreed on the mutation vocabulary and nobody had
      noticed; the accepted helpers had never run on -W.
    after: null
  delegations: []
  outputs:
  - packing/campaign/agent-sessions/session-050-exp045-audit-and-acceptance.md
  - packing/devtools/check_minus_w_bridge.py
  - packing/tests/test_minus_w_bridge.py
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-045-h-023-n5-minus-w-scale-and-controls.md
  - packing/defects.yaml
  checks:
  - uv run --frozen --all-extras --group dev packing-validate --records
  - uv run --frozen --all-extras --group dev packing-validate --push
  - uv run --frozen --all-extras --group dev python -m devtools.check_minus_w_bridge
  resource_rollups: []
  stop_reason: null
  next_action: >-
    `BC-089`'s remainder on `think-d0j1` stays the next slice, per X-009's sequencing;
    what this session changed is what comes after it: the n = 5 connectivity question
    is genuinely ready for the first time now that its instrument's acceptance gate is
    cleared.
---
# Session-050 — The exp-045 Independent Audit, the -W Bridge, and the Acceptance

The sixth admission condition sat unperformed for four days because it was the one
condition the instrument's own builder could not satisfy.
This session was the outsider: it replayed the certificate, proved the replay would
refuse a perturbed artifact, and then compared the registration against the retained
round the way an auditor does — against the artifacts, not the narratives.

Three findings came out, and the interesting one was not bookkeeping.
The accepted production helpers — the row-jet, stress, scale, and owner-4 layers the
first admission condition names — had never run on the direction the experiment is
about. They had run only on the `+W` control, per their admitted scope, while the
certificate came from a driver descended from the exp-043 draft.
Two implementations of the same mathematics, never compared.

The bridge compared them.
On the actual `-W` direction, at all three strata, the helpers rebuild all fifteen
owner-3 scale records and all three owner-4 records with strict exact contradictions
and every coefficient equal to its `+W` twin — the sign-symmetry determination derived
rather than read. The deciding constant, `-1/4`, ties to the certificate's retained
`obstruction_coefficient` by exact equality.
Agreement between independently written implementations is the strongest corroboration
this round could get short of a formal proof, and it is now a checker a future session
can re-run in seventy-five seconds.

The acceptance is the owner's, granted in conversation after the audit and recorded in
the experiment's amendment with its provenance.
The claim boundary did not move a word.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
