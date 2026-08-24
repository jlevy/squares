---
title: session-009 — bounded autonomous basin mapping
softschema:
  contract: packing.squares:AgentSession/v1
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-009
  title: Make the basin-map loop scientifically admissible and run bounded cells
  date: '2026-08-24'
  goal: >-
    Close only the launch-path gaps needed for scientifically admissible basin events,
    then run and retain successively larger cells until the four-hour deadline, an
    empty admissible queue, or a declared stop condition fires.
  focus: process
  primary_bead: think-05hr
  status: in_progress
  budget:
    wall_minutes: 240
    max_cycles: 8
    orientation_minutes: 10
    checkpoint_minutes: 20
    slice_minutes: 30
    finalization_minutes: 15
  stop_conditions:
  - The session wall budget reaches its finalization reserve.
  - No dependency-ready action can produce a replayable artifact inside one bounded slice.
  - Three consecutive commands crash, time out, or fail a validity guard.
  - A scientific decision requires changing a preregistered criterion or user judgment.
  - The admissible queue is empty; blocked samples are retained but not multiplied.
  progress:
    metric: scientifically admissible terminal events and classified basin-map cells
    before: >-
      No retained per-seed basin-event stream carried full poses, independent validity,
      typed termination evidence, resumable writes, and measured event wall time.
    after: >-
      Historical v2 events remain blocked as recorded. BasinEvent/v3 now retains
      complete tool-validation blocks through n=8, one bounded n=9 performance event,
      and source-bound n=10 starts tied to the published Göbel pose. The n=10 entry point
      passes static checks and semantic replay; exp-031 converges on all four source
      perturbations at the proved side with complete receipts. The number of
      exact component controls now classify the n=3 quotient interval and n=4 quotient
      point. Exp-033 proves one exact fixed-angle face relation between the equal-side
      n=5 source poses, and exp-034 embeds it in one exact angle-and-slide sheet, while
      sampled full-component classifications remain zero. The next cone checker is
      committed but under correction before scientific execution after review exposed
      D-194 and D-195. No complete-map claim follows.
  delegations:
  - task: Audit the numerical runner for an unattended eight-hour launch
    operator: autonomous_runner_audit
    status: completed
    outcome: >-
      Confirmed the numeric runner is not launch-ready and isolated missing control-cell,
      multi-cell completeness, lifecycle, validity, and queue-pricing checks.
    evidence: [runner source audit, current preflight behavior, D-044 and D-046]
    files: []
    checks: [read-only runner trace, queue and preflight inspection]
    uncertainty: The audit did not implement the blocked runner lifecycle.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Keep the generic numerical runner disabled until its scientific path is independently admissible.
  - task: Determine the smallest meaningful basin-map sequence and its blockers
    operator: basin_sequence_audit
    status: completed
    outcome: >-
      Chose n=3 through n=5 as cheap calibration cells, distinguished optimal moduli
      from terminal-landscape mapping, and identified identity and quench-settlement
      blockers before scaling beyond n=8.
    evidence: [exact n=3 and n=4 controls, canonicalizer timing, atlas and quench audits]
    files: []
    checks: [small-n exact replay, atlas behavior inspection]
    uncertainty: Complete component identity remains unimplemented.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Promote no sampled endpoint to a complete component census without the identity criterion.
  - task: Check every live PR 19 feedback surface at the latest pushed checkpoint
    operator: pr19_comment_checkpoint_2
    status: completed
    outcome: No issue comments, reviews, inline comments, review threads, or checks exist at head 2b43498.
    evidence: [GitHub REST and GraphQL review surfaces]
    files: []
    checks: [remote head matches local head]
    uncertainty: New feedback may arrive after this checkpoint.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Repeat the sweep after the next pushed checkpoint.
  - task: Format and validate the portable bounded-loop runbook
    operator: runbook_mechanical_check
    status: completed
    outcome: The four edited Markdown documents format cleanly and all schema-backed artifacts validate.
    evidence: [Flowmark 0.3.2 output, schema validator output]
    files:
    - README.md
    - campaign/README.md
    - campaign/agent-sessions/README.md
    - docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
    checks: [Flowmark, schema validation, git diff check]
    uncertainty: The delegated format-check used the packing directory, which has no Makefile target; the parent reran the repository-root target successfully.
    elapsed_seconds: 2
    elapsed_quality: platform_measured
    next_action: Commit and push the portable runbook checkpoint.
  - task: Run static checks on the finite adjacent-cell closure implementation
    operator: d168_mechanical_check
    status: completed
    outcome: >-
      Ruff formatting, BasedPyright, byte compilation, and diff checks pass after one
      mechanical import-order repair; the parent added narrow return-count annotations.
    evidence: [frozen Ruff output, BasedPyright output, py_compile output]
    files: [sqpack/quench.py, tools/regression_test.py]
    checks: [Ruff, BasedPyright, py_compile, git diff check]
    uncertainty: The delegate did not run the scientific n=10 or mutation controls.
    elapsed_seconds: 7
    elapsed_quality: platform_measured
    next_action: Retain the n=10 closure trace and run the scientific controls separately.
  - task: Run static checks on typed LP outcomes and bounded repair
    operator: d168_mechanical_check
    status: completed
    outcome: Ruff, BasedPyright, byte compilation, and whitespace checks pass.
    evidence: [frozen Ruff output, BasedPyright output, py_compile output]
    files: [sqpack/quench.py, tools/regression_test.py]
    checks: [Ruff, BasedPyright, py_compile, git diff check]
    uncertainty: The delegate did not run the mathematical controls or choose the retry policy.
    elapsed_seconds: 6
    elapsed_quality: platform_measured
    next_action: Run retained n=3, n=10, n=11, and adversarial failure controls.
  - task: Check the source-bound n=10 BasinEvent entry point mechanically
    operator: d168_mechanical_check
    status: completed
    outcome: >-
      Ruff, BasedPyright, byte compilation, the BasinEvent selftest, shell syntax, and
      whitespace checks pass after the parent narrowed the pose input type.
    evidence: [frozen static-check output, source-start mutation selftests]
    files: [sqpack/packings/gobel10.py, tools/basin_census.py]
    checks: [Ruff, BasedPyright, py_compile, BasinEvent selftest, bash syntax, git diff check]
    uncertainty: The delegate did not run the scientific four-perturbation BC-008 cell.
    elapsed_seconds: 3
    elapsed_quality: platform_measured
    next_action: Preregister BC-008, then run its four bounded source perturbations.
  - task: Check the exact n=5 face instrument mechanically
    operator: d168_mechanical_check
    status: completed
    outcome: Ruff, BasedPyright, byte compilation, and whitespace checks pass.
    evidence: [frozen Ruff output, BasedPyright output, py_compile output]
    files: [tools/check_n5_equal_side_face.py]
    checks: [Ruff, BasedPyright, py_compile, git diff check]
    uncertainty: The delegate did not run the scientific generation or replay.
    elapsed_seconds: 1
    elapsed_quality: platform_measured
    next_action: Run only after the exp-033 criterion is committed.
  - task: Integrate the exp-033 exact replay into the focused gate
    operator: d168_mechanical_check
    status: completed
    outcome: >-
      The small-n lane replays exp-033 with nullities 0/1/0 and six passing controls.
    evidence: [focused small-n gate output]
    files: [test.sh]
    checks: [bash syntax, gate list, small-n optimal-moduli lane, git diff check]
    uncertainty: The delegate did not run the full normal gate.
    elapsed_seconds: 2
    elapsed_quality: platform_measured
    next_action: Run the normal gate after result integration.
  - task: Check and integrate the exact n=5 angle-sheet instrument mechanically
    operator: d168_mechanical_check
    status: completed
    outcome: >-
      Static checks pass, and the small-n lane replays exp-034's dimension-two
      certificate, four boundary fixtures, and five controls in two seconds.
    evidence: [frozen static-check output, focused small-n gate output]
    files: [tools/check_n5_angle_sheet.py, test.sh]
    checks: [Ruff, BasedPyright, py_compile, bash syntax, focused gate, git diff check]
    uncertainty: The delegate did not derive the universal bound or run the scientific generation.
    elapsed_seconds: 4
    elapsed_quality: platform_measured
    next_action: Run the normal gate after exp-034 result integration.
  - task: Review every PR 20 surface and compare its documentation with the current branch
    operator: pr19_comment_checkpoint_2
    status: completed
    outcome: >-
      Found no GitHub feedback or dead links. The latest stack correctly incorporated
      exp-021 through exp-023, but still predates exp-024 and agenda-001; it must preserve
      the current four-of-four n=4 control, D-171 closure, and 24-round roll-up.
    evidence: [GitHub REST and GraphQL surfaces, exact head comparison, claim-level diff audit]
    files: []
    checks: [remote head and base, comments, reviews, threads, checks, links, current artifacts]
    uncertainty: The delegate did not merge or run PR 20's documentation through the current gate.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Merge the reviewed docs onto the exp-024 checkpoint and reconcile current status.
  - task: Review PR 20's tutorial for mathematical and evidence-boundary errors
    operator: runbook_mechanical_check
    status: completed
    outcome: >-
      Found the cell-versus-fixed-angle conflation, universal interval-impossibility
      claim, event-admissibility overstatement, exact-tier n=17 wording, missing direct
      evidence links, and imprecise genuinely-oblique orientation claim.
    evidence: [claim-level tutorial review, current experiment and defect artifacts]
    files: []
    checks: [terminology consistency, evidence-tier consistency, link audit]
    uncertainty: The delegate did not edit or merge the branch; the parent independently reviewed and corrected it.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Retain all accepted findings as D-172 through D-182 and merge only the corrected docs.
  - task: Review PR 21 against the current PR 19 checkpoint and every feedback surface
    operator: pr19_comment_checkpoint_2
    status: completed
    outcome: >-
      Found no GitHub feedback or checks. PR 21 was twelve commits behind the living
      checkpoint; its three initial documentation commits and later exp-033 boundary
      delta were suitable to reapply, but its two base merges and stale status roll-ups
      were not.
    evidence: [GitHub REST and GraphQL surfaces, exact head and merge-base comparison, claim-level diff audit]
    files: []
    checks: [remote head and base, comments, reviews, threads, checks, current-status comparison]
    uncertainty: The delegate performed a read-only review and did not integrate or validate the corrected tree.
    elapsed_seconds: 240
    elapsed_quality: platform_measured
    next_action: Reapply the four substantive documentation commits, correct D-188 through D-193, and run a fresh normal gate.
  outputs:
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-018-h-021-n3-basin-event-calibration.md
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-019-h-021-n4-basin-event-calibration.md
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-020-h-021-n5-basin-event-calibration.md
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-021-h-021-n3-basin-event-v3.md
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-022-h-021-n3-basin-event-v3-completion.md
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-023-h-021-n4-basin-event-v3.md
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-024-h-021-n4-basin-event-v3-repair.md
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-025-h-021-n5-basin-event-v3.md
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-026-h-021-n6-basin-event-v3.md
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-027-h-021-n6-basin-event-v3-retention.md
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-028-h-021-n7-basin-event-v3.md
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-029-h-021-n8-basin-event-v3.md
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-030-h-021-n9-basin-event-v3.md
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-031-h-002-n10-source-return.md
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-032-h-021-terminal-component-controls.md
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-033-h-023-n5-equal-side-face.md
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-034-h-023-n5-angle-sheet.md
  - campaign/series/series-000-smoke-and-calibration/results/exp-018-h-021-n3-basin-events.jsonl
  - campaign/series/series-000-smoke-and-calibration/results/exp-019-h-021-n4-basin-events.jsonl
  - campaign/series/series-000-smoke-and-calibration/results/exp-020-h-021-n5-basin-events.jsonl
  - campaign/series/series-000-smoke-and-calibration/results/exp-021-h-021-n3-basin-event-v3.jsonl
  - campaign/series/series-000-smoke-and-calibration/results/exp-022-h-021-n3-basin-event-v3-completion.jsonl
  - campaign/series/series-000-smoke-and-calibration/results/exp-023-h-021-n4-basin-event-v3.jsonl
  - campaign/series/series-000-smoke-and-calibration/results/exp-024-h-021-n4-basin-event-v3-repair.jsonl
  - campaign/series/series-000-smoke-and-calibration/results/exp-025-h-021-n5-basin-event-v3.jsonl
  - campaign/series/series-000-smoke-and-calibration/results/exp-026-h-021-n6-basin-event-v3.jsonl
  - campaign/series/series-000-smoke-and-calibration/results/exp-027-h-021-n6-basin-event-v3-retention.jsonl
  - campaign/series/series-000-smoke-and-calibration/results/exp-028-h-021-n7-basin-event-v3.jsonl
  - campaign/series/series-000-smoke-and-calibration/results/exp-029-h-021-n8-basin-event-v3.jsonl
  - campaign/series/series-000-smoke-and-calibration/results/exp-030-h-021-n9-basin-event-v3.jsonl
  - campaign/series/series-000-smoke-and-calibration/results/exp-031-h-002-n10-source-return.jsonl
  - campaign/series/series-000-smoke-and-calibration/results/exp-032-h-021-terminal-component-controls.json
  - campaign/series/series-000-smoke-and-calibration/results/exp-033-h-023-n5-equal-side-face.json
  - campaign/series/series-000-smoke-and-calibration/results/exp-034-h-023-n5-angle-sheet.json
  - campaign/agendas/agenda-001-basin-confidence-ladder.md
  - campaign/schemas/agenda.schema.yaml
  - tools/basin_census.py
  - sqpack/packings/gobel10.py
  - README.md
  - campaign/README.md
  - campaign/agent-sessions/README.md
  - campaign/agent-sessions/session-009-autonomous-basin-map.md
  - campaign/schemas/agent-session.schema.yaml
  - TUTORIAL.md
  - docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
  - docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
  - sqpack/quench.py
  - tools/regression_test.py
  - tools/check_terminal_components.py
  - tools/check_n5_equal_side_face.py
  - tools/check_n5_angle_sheet.py
  checks:
  - Basin-event generation and replay pass for n=3, n=4, and n=5.
  - Every retained pose passes the independent floating-point geometry screen.
  - Historical v2 events state that D-165 blocks promotion; the v3 event derives its empty blocker list.
  - The portable runbook and session clocks pass Flowmark, schema, campaign-record, README, and synopsis checks.
  - >-
    A diagnostic replay classified all sixteen formerly censored n=10 probes as
    post-check rejections on pair rows 66 or 77, with residuals from 1.00000008e-10 to
    9.999996e-10; none was mathematical infeasibility or a solver failure.
  - >-
    The bounded one-retry repair keeps the original 1e-10 screen, tightens every row
    outside it in the first returned point, uses 25 retries on n=10, accepts every result
    against the original rows with worst residual 1.55e-15, and reaches the proved side
    within 1.33e-15. The retained n=3 seed-1 and n=11 controls also pass; synthetic
    infeasible, solver-failure, pair, and containment cases retain their distinct causes.
  - >-
    An independent `sqpack.verify` screen accepts the repaired n=10 terminal pose,
    checks all 45 pairs, reports no failures, and recomputes the identical side
    3.707106781186549. The quench used 4,157 actual LP calls and converged in 6.6 seconds
    on this host.
  - >-
    Replacing a nine-second full n=3 gate replay with its exact retained failing cell
    preserves the row, residual, retry, and side evidence; the historical-regression
    lane now passes in 12 seconds instead of the prior 18-second D-168 checkpoint.
  - >-
    At the D-168 checkpoint, the 36-second normal gate passed all thirty steps: the real
    n=4 quench converged and the store reported five of six converged proposals. D-165
    still blocked promotion at that checkpoint because angle probes were unaccounted.
  - >-
    With typed outcomes and the bounded retry in production, the full normal gate again
    passed all thirty steps in 57 seconds. Replacing only the slow n=3 regression with
    its retained failing cell then reduced the affected historical-regression lane to
    12 seconds; that lane and all static checks passed after the test-only change.
  - >-
    Exp-021 is the first BasinEvent/v3 supervised result: n=3 seed 1 reaches side
    2.000000000000001 in 1.90 seconds, independently validates all three pairs, and
    retains 2,037 fixed-point evaluations, all settled. Semantic replay derives
    scientific admissibility and rejects a forged all-probes flag.
  - The post-exp-021 full normal gate passes all thirty steps in 21 wall-seconds.
  - >-
    D-170 corrects the closing audit: D-165 now has dedicated bead `think-007f` instead
    of reusing the unrelated D-132 tracker; `think-9qz0` remains unchanged.
  - >-
    Exp-022 completes the fixed four-seed n=3 v3 block: all four events are admissible,
    three reach side 2, and one reaches valid nonoptimal side 2.362735797795. The three
    new events contain 8,364 settled and zero unsettled fixed-point evaluations and cost
    6.27 seconds total.
  - >-
    Exp-023 completes inside its cap in 12.51 seconds: n=4 seeds 0-2 reach proved side 2
    and are admissible; seed 3 retains one unsettled fixed-point evaluation after pair
    row 16 remains 4.209e-10 outside the screen after bounded repair. The event fails
    closed under D-171, leaving the cell 3/4 admissible.
  - >-
    D-171's retained fixed cell shows that rows 16 and 21 were already outside the
    screen together. The one-retry complete offending-set repair keeps the screen fixed;
    exp-024 then reaches proved side 2 on all four n=4 seeds with 14,301/14,301 settled
    evaluations, zero unsettled evaluations, and 16.97 seconds total wall time.
  - >-
    PR 20 was reviewed at head 5d096ae against the exp-024 checkpoint. Eight substantive
    documentation defects are recorded as D-172 through D-182; the accepted orientation
    docs preserve agenda-001 and bind project-specific claims to retained evidence.
  - >-
    Exp-025 completes BC-003 in 14.47 seconds: all four n=5 events independently replay,
    all 14,219 fixed-point evaluations are settled, and no event descriptor is promoted
    to a terminal component. The cell observes three descriptors at two side values.
  - >-
    Exp-026 retains three admissible side-3 events with 12,777 settled evaluations, then
    seed 3 fails independent validity and the batch crashes before writing its outcome.
    D-183 records the flattering retention failure and stops the size ladder.
  - >-
    Exp-027 retains and replays all four n=6 outcomes. Three converge at side 3; seed 3
    is independently valid but hits the wall-clock budget at side 3.040392660291 and is
    non-admissible. A deterministic run-path fixture closes D-183; D-126 remains open.
  - >-
    Exp-028 retains and replays four valid n=7 outcomes with 18,286 settled evaluations.
    One converges at side 3.2; three hit the time budget and remain non-admissible. This
    validates retention, not basin frequency or component completeness.
  - >-
    Exp-029 retains and replays four independently valid n=8 outcomes in 38.00 seconds.
    One converges at side 3, one retains a typed unsettled cell-cycle evaluation, and
    two hit the time budget. Four-event median screen and key batches cost 0.000684s and
    0.004956s; quench work, not canonicalization, dominates this cell.
  - The post-exp-029 full normal gate passes all thirty steps in 61 wall-seconds.
  - >-
    Exp-030 retains and replays one independently valid n=9 time-budget stop. The full
    command costs 21.36 seconds; retained quench wall is 20.062 seconds, median
    one-event screening is 0.000174 seconds, and median keying is 0.001074 seconds.
  - The post-exp-030 full normal gate passes all thirty steps in 47 wall-seconds.
  - >-
    The source-bound n=10 entry point reproduces the published Göbel pose, binds its
    source URL and SHA-256, retains deterministic perturbations, and rejects changed
    source or start data. All 36 historical events still replay. A one-second real run
    reaches a valid optimal-side endpoint and retains a typed producer time stop.
  - >-
    Exp-031 preregisters four fixed source perturbations at scale 1e-4, a 15-second
    per-seed budget, a 90-second process cap, and the distinction between optimal-side
    validity and producer convergence before observing the four outcomes.
  - >-
    Exp-031 then meets its complete criterion: 4/4 events converge, validate, replay,
    and return within 2.221e-15 of the proved side; 6,631/6,631 fixed-point evaluations
    settle in 10.337 seconds of retained quench wall.
  - >-
    Exp-032 completes BC-009 in 0.92 seconds of generation plus replay. The exact n=3
    interval remains one component across four geometric keys, two contact signatures,
    and three strata; the exact n=4 quotient is one point; all eight false-policy
    mutations fail and all 16 f64 observations remain unresolved.
  - >-
    The post-exp-032 normal gate passes all 30 steps in 34 wall-seconds: 37 negative
    controls fire, 40 BasinEvent records replay, all 32 declared engine commits are
    checked, and the 32-round campaign, 185-defect log, and nine sessions reconcile.
  - >-
    Exp-033 meets its frozen exact criterion in 0.24 seconds of generation plus replay.
    The two equal-side n=5 golden keys share one fixed-angle optimal face; exact
    fixed-side nullities are 0/1/0 across its endpoint, interior, and endpoint strata.
  - >-
    The post-exp-033 normal gate passes all 30 steps in 30 wall-seconds: 37 negative
    controls fire, 40 BasinEvents and all exact records replay, all 33 declared engine
    commits are reachable, and 33 rounds, 185 defects, and nine sessions reconcile.
  - >-
    Exp-034 meets its frozen criterion in 0.27 seconds of generation plus replay. The
    exp-033 face lies in an exact two-parameter angle-and-slide sheet of
    orientation-indexed LP optima, and all five controls fail as required.
  - >-
    The first post-exp-034 normal gate stops after 31 seconds because two synopsis
    mutation controls retained pre-D-186 numeric anchors. D-187 records the miss; the
    defect-count, soundness-direction, and gate-detector controls then all fire.
  - >-
    The corrected post-exp-034 normal gate passes all 30 steps in 35 wall-seconds: all
    37 negative controls fire, 40 BasinEvents and five exact small-n records replay,
    all 34 engine commits are reachable, and 34 rounds and 187 defects reconcile.
  - >-
    Exp-035 orientation identifies one exact non-sheet first-order direction in every
    n=5 face stratum. Its candidate checker is committed at 8aa0cbb and paused on
    think-1582 without preregistration or scientific execution.
  - >-
    PR 21's four substantive documentation commits are incorporated without either
    stale base merge. D-188 through D-193 record the review corrections, and the final
    integrated normal gate passes all 30 steps in 38 wall-seconds with 193 defects.
  - >-
    After PR 19 merged, the user shortened the remaining campaign checkpoint from eight
    hours to four. Work resumed from merged main on a fresh branch; no completed result
    or historical timing was changed by the shorter horizon.
  - >-
    Semantic review of the unexecuted exp-035 candidate found D-194 and D-195 before
    preregistration: the pair (0,4) differential changes along the slide, and the tied
    pair (3,4) support rows are conjunctive within each owner-axis branch. Both repairs
    are tracked under think-1582; the experiment remains unrun.
  stop_reason: null
  next_action: >-
    Continue BC-010 with one bounded complete wall-release and SAT-branch cone slice.
    Preserve every unsupported continuation as unresolved and stop after that slice.
---
# Session 009 — Bounded Progress Before Scale

The event pipeline now preserves useful negative evidence, but it is not yet a complete
basin mapper. The historical n=3 through n=5 v2 rounds found valid endpoints and exposed
termination behavior while remaining blocked as recorded.
BasinEvent/v3 now accounts for every fixed-point evaluation in the current n=3, n=4, and
n=5 controls and admits the narrow event claim; terminal-component identity and census
saturation remain blocked.

The session therefore stopped the size sweep after n=5. The finite n=10 tie-cell test
has now closed every observed two-, four-, and eight-cell degeneracy without claiming a
global optimum. The next slices typed all sixteen missing outcomes, added one bounded
retry, and replayed every accepted result against every original LP row.
D-171 then showed that a retry must tighten the complete initial offending set rather
than only its largest row.
Exp-021 derives complete accounting from a balanced receipt and closes D-165; exp-024
completes the n=4 v3 block.
The historical v2 block remains promotion-blocked as recorded, and no endpoint
descriptor has been promoted to a connected component.

The event stack now retains complete blocks through n=8 plus one bounded n=9 performance
event. D-126 still prevents a fixed wall-clock budget from defining reproducible
scientific work, so these cells validate retention and replay only; they do not estimate
basin frequencies. The separate n=5 connectivity question now has two exact partial
results.
Exp-033 joins the equal-side pair inside a fixed-angle optimal face, and exp-034
embeds that face in a two-parameter angle-and-slide sheet of optima.
Full nonsmooth stationary identity and unequal-side clearance remain open.
The source-bound n=10 entry path now passes its four-perturbation BC-008 known-answer
control in exp-031. The exact evidence boundary now also passes BC-009: exp-032
classifies only the complete `n = 3` and `n = 4` quotient models and refuses to infer a
component from any current floating-point event.
The next research cell is therefore the complete nonsmooth cone and continuation test
around this exact `n = 5` sheet, not a sample-count census.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
