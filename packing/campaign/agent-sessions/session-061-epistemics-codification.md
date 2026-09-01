---
title: "session-061 — the epistemics codification: ladders, register, checker, orientation"
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-061
  primary_bead: think-n8vl
  status: completed
  title: "The epistemics codification: ladders, register, checker, orientation"
  date: '2026-08-31'
  started_at: '2026-08-31T22:28:00Z'
  deadline_at: '2026-09-01T02:58:00Z'
  goal: >-
    BC-107: turn the epistemic vocabulary the verification review applied by
    hand into a codified, machine-enforced rubric. One root document
    (epistemics.md) owns the four axes; a T-NNN results register makes results
    first-class; a derivation checker grants confirmation rungs from recorded
    atoms so levels are committed after an effort rather than judged; the
    README tells a visitor whether this repository carries novel results and
    which ones at which levels, and the SYNOPSIS matches. New PR from the
    branch restarted on the merged main.
  workflow_phases:
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-107
    bead: think-n8vl
    objective: >-
      Author the codification surface: epistemics.md (the vocabulary's single
      owner: V0-V5, C0-C5 with per-rung machine-checkable promotion
      checklists, S1-S5 anchored and non-gating, novelty by reference; the
      compound-claim minimum rule; the bridging table from the evidence
      atoms; the four review rubric-gap resolutions), then the results
      register (frontier/results.yaml, schema, initial T-records), the
      derivation checker with tests and a negative control, and the generated
      RESULTS view.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 150
    started_at: '2026-08-31T22:28:00Z'
    deadline_at: '2026-09-01T00:58:00Z'
    expected_output: >-
      epistemics.md; frontier/results.yaml validating against its schema with
      the initial records; devtools checker deriving V/C and failing on
      unsupported declarations, wired into the records tier with a firing
      control; frontier/RESULTS.md generated and gated.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      If a rung cannot be expressed as predicates over recorded atoms without
      distorting it, the rung is documented as declared-not-derived rather
      than force-fitted, and the gap is typed on think-n8vl.
    fallback: >-
      Land the document and register with the checker enforcing whatever
      subset derives cleanly; type the rest.
    outcome: >-
      The codification surface exists and every rung on it is earned.
      epistemics.md landed at the root as the vocabulary's single owner: V0-V5
      (strongest verification anywhere), C0-C5 (ours, end-to-end, each rung a
      conjunction of machine-checkable predicates over recorded atoms), S1-S5
      anchored and never gating, novelty by reference to the evidence
      contract, the compound-claim minimum rule, the atoms-to-rungs bridging
      table, and the review's four rubric-gap resolutions. The register
      (frontier/results.yaml, ResultsRegister/v1 schema) declares T-001
      through T-013 -- the review's determinations, the green17 upgrade at
      V4/C4, and the legacy first-party theorems including the Stromquist
      repair at S4 -- and devtools/check_results.py re-derives every V and C
      from the cited atoms: inflation fails, unexplained understatement
      fails, C3-or-better requires named adversarial controls, V0/V2 are
      declared-not-derived and require notes. The generated RESULTS.md view,
      a firing negative control (a C4 claimed past its atoms), five pytest
      cases, and the gate step 'results rungs are earned and the view agrees'
      are all in the records tier. Two candidate register entries were
      deferred rather than force-fitted, exactly per the kill condition: the
      Trump local-isolation theorem derives C3 but has no adversarial
      control test to name, and the translation-escape observation is a
      numerically-checked survey fact with no single registered claim shape;
      both typed on think-n8vl.
      softschema upgraded 0.6.2 -> 0.8.0 across the schema toolchain in the
      same slice (the CLI now validates pure-yaml profiles and allOf
      composition, so the workaround rationale comments were rewritten to
      retained-by-choice).
    evidence:
    - epistemics.md
    - packing/frontier/results.yaml
    - packing/frontier/results.schema.yaml
    - packing/frontier/RESULTS.md
    - packing/devtools/check_results.py
    - packing/devtools/render_results.py
    - packing/tests/test_results_register.py
    stop_reason: >-
      The phase's exit is met with the budget mostly unspent: the checker
      derives, refuses, and passes on the live register.
    next_action: >-
      The integration phase: conventions.md section 4 shrink, the T-NNN
      identity row, README orientation, SYNOPSIS, document map, validation,
      and the new PR.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-107
    bead: think-n8vl
    objective: >-
      Integrate the codified vocabulary into the reader tier: register the
      legacy first-party theorems whose adversarial controls exist, reduce
      conventions.md section 4 to field formats with pointers to
      epistemics.md, repoint the T-NNN identity row at the register, rewrite
      the README's What Has Been Established as a survey-versus-first-party
      orientation grounded in T-ids, defer SYNOPSIS's results section to the
      register while keeping its legacy shorthand, update the document map
      and the current handoff, and close the record.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      Phase 1's exit is met; the remaining exit criteria of BC-107 are
      reader-tier integration, which is this planned phase.
    budget_minutes: 60
    started_at: '2026-08-31T22:50:00Z'
    deadline_at: '2026-08-31T23:50:00Z'
    expected_output: >-
      conventions.md, README.md, SYNOPSIS.md, the active plan handoff, and
      the document map all agreeing with the register; check_results'
      reader-tier mention check and check_synopsis green; the session and
      cell closed.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      If a reader-tier claim cannot be grounded in a registered result or a
      cited atom, it is cut or downgraded rather than retained on style.
    fallback: >-
      Land the conventions and README reorientation and type any remaining
      SYNOPSIS reconciliation on think-n8vl.
    outcome: >-
      Four legacy results registered with existing adversarial controls
      (T-010 the Stromquist repair, T-011 the Trump validity check, T-012 the
      n = 5 second-order rigidity, T-013 the n = 40 flexibility bracket);
      conventions.md section 4 now points result-level semantics at
      epistemics.md and the identity row points T-NNN at the register with
      the SYNOPSIS single-digit ids as declared shorthand; the README's What
      Has Been Established separates first-established-here from
      audited-from-the-literature by T-id with counts derived from the
      register; SYNOPSIS's results section defers to the register and the
      night handoff block names this session; the document map carries
      epistemics.md (conventions, definitive) and RESULTS.md
      (generated-view); check_results, check_documentation and check_synopsis
      all green.
    evidence:
    - conventions.md
    - README.md
    - SYNOPSIS.md
    - docs/project/document-map.yaml
    - docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
    - packing/devtools/run_negative_controls.py
    - packing/defects.yaml
    stop_reason: >-
      BC-107's exit criteria are all met on a green records tier, and the
      one-shot post-merge check's finding rode along: main's full surface was
      still red on one negative control (the pruned-rendering link gap and a
      stale expected message, D-409/D-410), fixed and defect-logged here with
      epistemics.md added to the worker snapshot's root documents; what
      remains is the push gate and the PR, which are finalization.
    next_action: >-
      Finalization: rollups regenerated, packing-validate --push on the
      committed tree, push, and the new PR for the owner's review.
  budget:
    wall_minutes: 270
    finalization_minutes: 30
  progress:
    metric: >-
      Whether a result's confirmation level is granted by the gate from
      recorded atoms, and whether a README visitor can tell survey content
      from first-party results by level.
    before: >-
      The atoms exist across five evidence fields; conventions.md section 4
      carries semantics outside its scope; T-N is reserved in the identity
      table with no registry; results have no prioritized surface; the README
      does not say whether the project carries novel results.
    after: >-
      Thirteen results T-001 through T-013 carry declared V and C rungs that
      devtools/check_results.py re-derives from cited atoms on every records
      run, refusing inflation and unexplained understatement, with a firing
      negative control and five pytest cases; the README opens What Has Been
      Established with the survey-versus-first-party split, the register's
      counts, and per-result T-ids in two lists (first established here;
      audited from the literature); the two candidate entries that resisted
      their checklists are deferred as typed follow-ons instead of
      force-fitted.
  stop_conditions:
  - >-
    Nothing is pushed without packing-validate --push green on the exact tree.
  - >-
    Levels are granted by recorded atoms and the checker, never asserted past
    them; any rung that resists mechanization is documented as
    declared-not-derived rather than force-fitted.
  - >-
    The 20-minute continuity reminder and the finalization alarm are the
    owner's; this session may not delete or disable either (OR-8, D-395).
  delegations: []
  outputs:
  - packing/campaign/agent-sessions/session-061-epistemics-codification.md
  - packing/campaign/agendas/agenda-011-verification-review.md
  checks:
  - uv run --frozen --all-extras --group dev packing-validate --records
  - uv run --frozen --all-extras --group dev packing-validate --push
  resource_rollups:
  - packing/campaign/resource-usage/913a5de0-f775-52cc-8f42-a03fcbd8234b.yaml
  stop_reason: >-
    BC-107 is discharged: the vocabulary has one owner, the register's rungs
    are granted by the gate from recorded atoms, the reader tier is oriented
    around it, and validation is green on the exact tree.
  next_action: >-
    The owner's whole-PR review of the codification; BC-107 under think-n8vl
    is the cell of record, and the two deferred register candidates wait on
    the controls that would earn their rungs.
---
# Session-061 — The Epistemics Codification

Contemporaneous record; the frontmatter is the session.
The owner’s approvals that scope it: the four-axis design and the verified/confirmed
split from the in-session design review, epistemics.md as a new root document because
conventions.md’s scope is formats and naming, levels committable after an effort because
the rubric rather than a reviewer grants them, and a README orientation so a visitor can
tell survey content from novel results.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
