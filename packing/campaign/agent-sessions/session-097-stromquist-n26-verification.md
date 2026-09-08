---
title: session-097 — Stromquist n26 verification and MacIver source audit
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-097
  title: Stromquist n26 verification and MacIver source audit
  date: '2026-09-07'
  started_at: '2026-09-07T22:04:11Z'
  deadline_at: '2026-09-08T00:14:28Z'
  branch: codex/stromquist-n26-verification
  goal: Resolve the author's n26 clarification against the scanned construction and live chart, verify the geometry, correct the source record, and pursue bounded
    mathematical directions. Also audit MacIver's public papers, compare their bounds with the verified record, and preserve useful methods with explicit proof-coverage
    limits.
  workflow_phases:
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: Complete a reusable exact checker for the memo's n26 geometry and its side comparison, using independent pair and wall checks and negative controls.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 30
    started_at: '2026-09-07T22:04:11Z'
    deadline_at: '2026-09-07T22:34:11Z'
    expected_output: Exact geometry replay, retained comparison output, independent review, and focused regression tests.
    validation_command: .venv/bin/pytest -q tests/test_stromquist_memo3_n26.py
    kill_condition: A failed field precondition, pair separation, wall check, or independent oracle blocks acceptance.
    fallback: Retain the source-reported construction and exact missing verification obligation.
    outcome: Exact cubic reconstruction checks all 26 unit squares, 325 pairs, and walls. Six tests pass with an independent rational-polynomial and half-plane oracle.
      Independent review accepts the strict comparison with Friedman and the scoped central-block support proof.
    evidence:
    - packing/cases/stromquist/memo3-n26.json
    - packing/tests/test_stromquist_memo3_n26.py
    - docs/project/reviews/review-2026-09-07-stromquist-n26-directions.md
    stop_reason: The known construction and its exact comparison are accepted; no new unrestricted bound is claimed.
    next_action: Integrate source corrections and research dispositions, then validate and publish the review checkpoint.
  - workflow: documentation-pass
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: Complete the prose pass, generated records, full validation, and review publication for the independently checked n26 findings.
    status: stopped
    entered_by: evidence_checkpoint
    switch_reason: All delegated source and mathematical outputs are accepted; integration and validation remain.
    budget_minutes: 30
    started_at: '2026-09-07T22:14:50Z'
    deadline_at: '2026-09-07T22:44:50Z'
    expected_output: Reviewable committed branch, full-checkpoint evidence, source-record corrections, and named next dependencies.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --push
    kill_condition: A failed check requires diagnosis; an estimated time cannot authorize an incomplete claim or skipped required validation.
    fallback: Fix the failing surface, repeat its affected checks, and retain exact source identity and any remaining limitation.
    outcome: Source attribution, private-communication credit, generated records, and the rendered acknowledgment are integrated. Pre-push checks found and drove
      corrections to record bookkeeping and the explainer's permalink wiring. The mathematical replay remains accepted.
    evidence:
    - docs/project/research/research-2026-09-07-stromquist-n26-verification.md
    - packing/devtools/templates/explainer-article.md
    stop_reason: Final validation and publication move to a separate phase against a committed scientific state; the full checkpoint is still required.
    next_action: Commit the reviewed changes, run the full checkpoint, and close the measured session after validation.
  - workflow: documentation-pass
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: Validate the committed scientific state, retain the final resource receipt, and publish the reviewed source correction with passing local and hosted
      checks.
    status: stopped
    entered_by: evidence_checkpoint
    switch_reason: The substantive source and geometry changes are complete; the permalink contract requires the new report to exist in the linked commit, and the
      full checkpoint needs a stable source identity.
    budget_minutes: 60
    started_at: '2026-09-07T22:34:51Z'
    deadline_at: '2026-09-07T23:34:51Z'
    expected_output: A committed full-checkpoint receipt, terminal session cost record, passing pre-push and hosted checks, and a reviewable pull request.
    validation_command: uv run --frozen --all-extras --group dev packing-validate
    kill_condition: A failed check blocks completion and requires diagnosis; the declared checkpoint time is not a reason to skip required validation.
    fallback: Repair the failing surface and repeat affected checks while preserving the exact source identity covered by each receipt.
    outcome: 'The clean 48a4544f full checkpoint completed 66 steps in 2565.37 seconds: 64 passed, two failed on time guards. All 3425 quick, 98 slow, and 55 exhaustive
      tests passed their assertions. Two negative controls timed out at 120 seconds and then passed unchanged in serial replay. Thirteen quick tests exceeded the
      12-second wall guard. No logic failure was found; a passing fast checkpoint remains required.'
    evidence:
    - packing/campaign/agent-sessions/session-097-validation/full-48a4544f.json
    - packing/campaign/agent-sessions/session-097-validation/reducible-control-48a4544f.jsonl
    - packing/campaign/agent-sessions/session-097-validation/pivot-control-48a4544f.jsonl
    stop_reason: The new user source request was reviewed alongside the full run; final integration and time-guard rechecking proceed in a separate phase.
    next_action: Run the unchanged fast surface with lower process concurrency after integrating the reviewed source additions.
  - workflow: factual-review
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: Audit MacIver's public square-packing papers against the source database and verified bounds, assess reusable mechanisms, and integrate a reviewed
      evidence record.
    status: completed
    entered_by: user_request
    bead: think-904u
    switch_reason: The user added MacIver's source and proof mechanisms while the committed n26 full validation was still running.
    budget_minutes: 45
    started_at: '2026-09-07T23:07:15Z'
    deadline_at: '2026-09-07T23:52:15Z'
    expected_output: Version-pinned source record, exact bound comparison, independently reviewed mechanism assessment, and explicit proof-replay limits.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: Missing evidence or a proof gap prevents promotion of the source claim to verified status.
    fallback: Retain attributable source statements and name exact unresolved proof obligations.
    outcome: Three agents identified the pinned public source, audited numerical and formal-proof coverage, and derived concrete local-capacity controls. The coordinator
      independently checked the bound comparison, counting argument, interval controls, and all proposed record changes. Three original PDFs and faithful extractions
      are ready for the integrated checkpoint.
    evidence:
    - docs/project/reviews/review-2026-09-07-maciver-square-packing.md
    - packing/resources/web/maciver-square-packing-2026-09-07/README.md
    stop_reason: The source and method assessment is accepted; no MacIver theorem is promoted and no new target experiment is claimed.
    next_action: Validate the integrated records and preserve local theorem replay as think-sske.
  - workflow: documentation-pass
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: Integrate the accepted source records and n26 design, pass the unchanged fast gate under bounded concurrency, and close the measured review for publication.
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: The full run found time-guard failures after all test assertions passed; source and mathematical reviews are complete, so the final record can
      now be integrated.
    budget_minutes: 30
    started_at: '2026-09-07T23:24:04Z'
    deadline_at: '2026-09-07T23:54:04Z'
    expected_output: Reviewed source commit, passing local fast validation, and retained full-run and replay outcomes ready for final integration and publication.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --fast --jobs 2 --inner-jobs 1
    kill_condition: A logical failure or unchanged timing failure requires diagnosis; no guard is weakened to manufacture a pass.
    fallback: Retain the precise failed run and recheck the affected surface with measured resource limits or hosted validation.
    outcome: The clean bdc28e89 source passed all 62 fast steps in 401.14 seconds with PYTHON_CPU_COUNT=3, two outer jobs and one inner job. The Linux timing-band
      comparison is reported, not enforced, for this local shape. Earlier CPU4 and native runs are retained as failures of the stale-budget check and one 12.81-second
      test guard respectively. No tests, guards, timeouts or baseline changed.
    evidence:
    - packing/campaign/agent-sessions/session-097-validation/fast-final-bdc28e89.json
    stop_reason: The scientific source integration and local fast checkpoint are accepted; main has since received typography changes touching the acknowledgment
      renderer.
    next_action: Integrate the new main branch, verify the acknowledgment in its typography, and finish publication.
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: Integrate main typography changes with the reviewed acknowledgment, verify the combined render and affected checks, and prepare the measured review
      for publication.
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: Main advanced to 373beb36 during validation; the incoming renderer and generated views need an integration check before publication.
    budget_minutes: 30
    started_at: '2026-09-07T23:44:28Z'
    deadline_at: '2026-09-08T00:14:28Z'
    expected_output: A clean integrated source commit, reviewed PDF acknowledgment, affected validation evidence, final session cost and review description.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --push --jobs 2 --inner-jobs 1
    kill_condition: An integration or rendering failure requires repair and affected rechecking before publication.
    fallback: Preserve both source changes, resolve the concrete incompatibility, and retain the tested commit identity.
    outcome: Merged main 373beb36 into 0e766bfd without conflicts and retained both the upstream typography and the acknowledgment permalink. HTML regeneration and
      drift checking passed. Print layout, two-render PDF agreement at 16 pages, and light/mobile-dark supporting typography passed; the coordinator visually checked
      the acknowledgment on page 14 and its commit-pinned link. Pre-push at 0e766bfd passed all 45 selected steps in 163.51 seconds. Independent integration review
      accepted after identifying one stale CPU-setting sentence, corrected in this closeout.
    evidence:
    - packing/campaign/agent-sessions/session-097-validation/push-0e766bfd.json
    - packing/devtools/templates/explainer-article.md
    stop_reason: The source review, mathematical verification and upstream integration are complete. Closure metadata verification and publication follow the measured
      interval.
    next_action: Check the closure delta against 0e766bfd, publish the reviewed branch, and confirm hosted checks.
  primary_bead: think-zi3g
  status: completed
  budget:
    wall_minutes: 140
    slice_minutes: 30
  stop_conditions:
  - Complete the source comparison, independently checked construction, bounded directions, and validated integration.
  - An estimated slice duration is an inventory checkpoint, not authority to abandon the user's request.
  progress:
    metric: Verified source comparison, reconstructed geometry, and explicit research dispositions.
    before: The prior review guessed the author's intent; n26 had an exact Friedman upper certificate but omitted Green's stronger source-reported lower bound.
    after: The valid historical n26 cubic packing is exactly reconstructed and remains worse than Friedman; private-communication credit is included. Green is retained
      as source-reported. Three MacIver manuscripts and their proof gaps are indexed, useful mechanisms and n26 search controls are reviewed, and no new unrestricted
      bound or executed target search is claimed.
  delegations:
  - task: Reconstruct and exactly verify Memo III's n26 construction
    phase: 1
    operator: Codex n26_geometry
    status: completed
    recording: retrospective
    outcome: Implemented exact cubic coordinates, all-pair and wall replay, historical comparisons, and independent rational-polynomial tests.
    evidence:
    - packing/cases/stromquist/memo3-n26.json
    files:
    - packing/cases/stromquist/memo3_n26.py
    - packing/tests/test_stromquist_memo3_n26.py
    checks:
    - Six focused tests passed; Ruff and BasedPyright reported zero findings; independent source reviewer accepted the geometry.
    uncertainty: This is a verified historical upper construction; optimality is not established.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Retain the exact result and prevent checked-in output drift through the CLI test.
  - task: Audit memo pages, current sources, chart, and lower-bound evidence
    phase: 1
    operator: Codex n26_sources
    status: completed
    recording: retrospective
    outcome: Confirmed the live chart, historical cubic attribution, n18 independent rediscovery, missing Green proof, exact reconstruction, and scoped block obstruction.
    evidence:
    - docs/project/research/research-2026-09-07-stromquist-n26-verification.md
    files: []
    checks:
    - Scanned memo and DS7 pages inspected; Gardner pp299–300 checked visually; six focused tests and existing n26/n18 exact replays passed independently.
    uncertainty: The primary Green proof and n26 point data remain unrecovered.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Track the missing Green evidence separately without promoting a verified lower bound.
  - task: Analyze bounded source-directed mathematical follow-up
    phase: 1
    operator: Codex n26_directions
    status: completed
    recording: retrospective
    outcome: Derived an exact restricted-family obstruction to intact central-block rotation, identified meaningful contact-release prerequisites, and separated Green
      recovery from the unresolved BC202 numerical lower-bound attempt.
    evidence:
    - docs/project/reviews/review-2026-09-07-stromquist-n26-directions.md
    files:
    - docs/project/reviews/review-2026-09-07-stromquist-n26-directions.md
    checks:
    - Independent reviewer and coordinator accepted the support proof; six-offset-domino source description corrected; Flowmark and whitespace checks passed.
    uncertainty: Changed contacts, split blocks, and moving corner frames lie outside the proved family.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Use think-z0fi for a separately specified contact-changing experiment and think-0x08 for Green evidence recovery.
  - task: Identify MacIver sources and prepare archive/database integration
    phase: 4
    operator: Codex n26_sources
    status: completed
    recording: retrospective
    outcome: Pinned the three canonical manuscripts, visually inspected title pages, retained source and CI metadata, verified missing n17 computation files, and
      prepared schema-valid historical evidence records.
    evidence:
    - docs/project/reviews/review-2026-09-07-maciver-square-packing.md
    files: []
    checks:
    - Coordinator review accepted; no source theorem is promoted and no target experiment is claimed.
    uncertainty: No local Lean build or replay of the missing n17 computation artifacts was performed.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Use think-sske for local theorem replay before adoption.
  - task: Assess MacIver mechanisms and specify a released-contact n26 family
    phase: 4
    operator: Codex n26_directions
    status: completed
    recording: retrospective
    outcome: Derived local triple-box and strip-capacity controls, checked defect/matching and correlated-support identities, rejected the unsupported broad 4.5 ceiling,
      and prepared the nine-variable n26 LP design.
    evidence:
    - docs/project/reviews/review-2026-09-07-maciver-square-packing.md
    files: []
    checks:
    - Coordinator review accepted; no source theorem is promoted and no target experiment is claimed.
    uncertainty: No local Lean build or replay of the missing n17 computation artifacts was performed.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Use think-sske for local theorem replay before adoption.
  - task: Independently review MacIver comparisons and validation failures
    phase: 4
    operator: Codex n26_geometry
    status: completed
    recording: retrospective
    outcome: Confirmed exact bound arithmetic and formal theorem coverage, reviewed the coordinator's complete assessment, and replayed both timed-out controls unchanged.
    evidence:
    - docs/project/reviews/review-2026-09-07-maciver-square-packing.md
    files: []
    checks:
    - Coordinator review accepted; no source theorem is promoted and no target experiment is claimed.
    uncertainty: No local Lean build or replay of the missing n17 computation artifacts was performed.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Use think-sske for local theorem replay before adoption.
  outputs:
  - docs/project/research/research-2026-09-07-stromquist-n26-verification.md
  - docs/project/reviews/review-2026-09-07-stromquist-n26-directions.md
  - packing/cases/stromquist/memo3-n26.json
  - packing/frontier/n-026.md
  - packing/frontier/n-027.md
  - packing/devtools/templates/explainer-article.md
  - docs/project/reviews/review-2026-09-07-maciver-square-packing.md
  - packing/resources/web/maciver-square-packing-2026-09-07/README.md
  - packing/frontier/n-017.md
  - packing/frontier/n-018.md
  checks:
  - Baseline records tier passed all 31 selected steps in 67.47 seconds after the locked Python environment and pinned submodule were initialized.
  - Existing Friedman exact replay passed all 325 pairs and walls for n26 and rejected duplicate and overfull-column controls; its companion n85 replay also passed.
  - Coordinator's six focused tests passed in 4.36 seconds, including an exact check against the retained JSON record; the author and independent reviewer separately
    passed all six.
  - Initial pre-push attempt selected 45 steps and failed on missing development tools in PATH, stale report/count/ledger views, a missing session deadline, and the
    case-prose check parsing an unparenthesized algebraic upper bound as its leading integer. Its behavioral selection had 692 passes and one failure on the stale
    synopsis count; these integration failures are corrected before rerunning.
  - Second pre-push attempt passed 43 of 45 steps in 275.69 seconds, with 750 behavioral passes and one failure. It caught an unpinned acknowledgment link and a prose
    phrase in the declared validation command; the link now uses the explainer's commit-pinned URL mechanism and the command is executable.
  - The local explainer PDF renders, its print-layout checker exits zero, and the acknowledgment and affected following pages pass visual inspection.
  - Pre-push at 48a4544f passed all 45 selected steps in 426.80 seconds, including 796 behavioral tests; the rendered explainer and print-layout check passed at that
    commit.
  - 'full gate: full at 48a4544f: failed (64 of 66 steps passed in 2565.37 seconds; all test assertions passed; two negative-control timeouts and thirteen quick-test
    wall overruns)'
  - 'The two timed-out controls passed separately on clean 48a4544f with the unchanged 120-second limit: reducible-polynomial control 86.814 seconds and pivot-budget
    control 44.715 seconds. Heavy host load was observed; the replay does not establish its sole causal role.'
  - Three independent MacIver audits and the coordinator agree on the exact bound comparison, missing computational artifacts, limited Lean coverage, and candidate
    local-capacity controls; public CI success is external evidence only.
  - The initial CPU4 fast attempt declared PYTHON_CPU_COUNT=4 with three outer workers and one inner worker, reducing process concurrency without changing tests or
    time guards.
  - 'full gate: fast at bdc28e8985663827aae2f7d8219537197cfff189: failed (CPU4 local run passed 62 of 62 steps in 254.69 seconds but failed the stale Linux timing-baseline
    comparison)'
  - 'full gate: fast at bdc28e8985663827aae2f7d8219537197cfff189: failed (native ten-CPU run passed 61 of 62 steps in 249.99 seconds; 3425 tests passed, with one
    12.81-second call exceeding the 12-second wall guard)'
  - 'full gate: fast at bdc28e8985663827aae2f7d8219537197cfff189: passed (all 62 steps in 401.14 seconds; local CPU3, jobs2, inner1 shape; Linux timing band reported
    and not enforced)'
  - Independent review accepted the lower-concurrency invocation and preservation of all earlier failures. think-mg9q tracks the reference matcher treating equal
    CPU/worker counts as comparable hardware; no speedup or causal load claim is made.
  - Final independent review accepted bdc28e89 without mathematical or source-coverage findings and checked 34 relative links/anchors. The coordinator also confirmed
    all three retained PDFs match the pinned originals and their raw extractions match fresh pdftotext output.
  - Pre-push at 0e766bfd8a6a3ff3dac43b095aecbced7d73470d passed all 45 selected steps in 163.51 seconds after main integration.
  - At 0e766bfd, HTML regeneration/check, print layout, two-render PDF agreement at 16 pages, and light/mobile-dark supporting typography passed. The coordinator
    visually checked the acknowledgment on page 14 and verified its source link names 0e766bfd.
  - 'Documentation boundary: README research index and SYNOPSIS updated; TUTORIAL, conventions, operating rules and development remain current for the source review.
    Dated-source corrections are explicit additions; generated views are refreshed. The selected BC-264 research allocation is retained.'
  stop_reason: The requested source audits, exact n26 verification, bounded mathematical directions and reviewed integration are complete; future proof recovery,
    theorem adoption and target optimization have separate named dependencies.
  next_action: Publish this review and verify hosted checks; retain think-mq0d (BC-264) as the selected research slice. think-z0fi implements and controls the specified n26 family,
    think-0x08 recovers Green evidence, think-4g6w audits the remaining source table, and think-sske replays MacIver theorem dependencies before adoption.
  resource_rollups:
  - packing/campaign/resource-usage/codex-task-tree-session-097.yaml
---
# Stromquist n26 Verification

The user selected this source review directly after clarifying Stromquist’s intended
hint.
It continues the [earlier memo review](session-096-stromquist-memos-and-helpers.md)
and leaves the separate active research agendas and their target allocations intact.

The preliminary source review and delegated assignments are reconstructed from the tool
receipts and prompts.
Their prospective clocks were not retained, so that work is reported here rather than
represented as a clocked phase.
It established the historical side comparison, Ellsworth’s attribution, and the omitted
Green report; the research report retains its evidence.
Phase 1 receives and independently checks the delegated outputs.
The clocked phase history begins at the first retained prospective declaration.
The resource interval begins earlier, at the recorded tracking checkpoint of 21:58:28
UTC; initial orientation before that checkpoint is outside the interval.

The planned slices are source comparison, exact reconstruction with independent review,
mathematical disposition and documentation, and final validation and publication.
Each slice has a thirty-minute checkpoint; later work is replanned from the returned
evidence. Known-construction verification is a pipeline control, and the analytic
restricted-family result remains a scoped review rather than an unrestricted bound.

The user added the MacIver source audit while the clean n26 full checkpoint was running.
Its initial identification work is unclocked; phase 4 begins at the retained prospective
source-audit declaration.
The full run remained on its clean source commit while all MacIver edits were prepared
and independently reviewed in temporary copies.
Phase 5 integrates those accepted copies after the full process exits.
The initial 120-minute plan is extended prospectively to 140 minutes for phase 6 after
main receives typography changes that touch the acknowledgment renderer.
The Linux timing baseline remains unchanged: CPU-count overrides on this macOS host do
not establish comparable hardware.
All three local fast receipts retain their source and invocation metadata, including the
failed runs.

The measured interval ends before closure-metadata validation, publication, and hosted
CI. Its receipt is a live task-tree lower bound, not a complete invoice for all later
publication work. The pull request records those final checks separately.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
