---
title: "Session 182 — n17 overnight lanes"
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-182
  title: n17 Overnight Lanes
  date: '2026-10-05'
  started_at: '2026-10-05T08:14:04Z'
  deadline_at: '2026-10-06T08:14:04Z'
  branch: claude/n17-session-182-overnight
  primary_bead: think-tmz6
  status: stopped
  goal: >-
    Make as much measured progress on s(17) = S* as one night on this container allows:
    certified exclusions that lower the residue below 126,168 states in 15,953 orbits,
    each admitted by a standing verifier's full pass, and the decisive planning evidence
    of H-264's per-state price, lane R9's capture route and the mixed-flag stalls.
  workflow_phases:
  - workflow: review-planning-oversight
    focus: insight
    recording: contemporaneous
    clock_role: work
    commitment: BC-418
    objective: >-
      The run's declared OR-5 entry point. Codify H-264 by rewriting it in place,
      register BC-419 and BC-420, freeze lane K's target list from the census at the
      registration commit, read the OR-12 count, create the lane beads and publish the
      registration before the first target run.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 60
    started_at: '2026-10-05T08:14:04Z'
    deadline_at: '2026-10-05T09:14:04Z'
    expected_output: >-
      The registration commit: H-264 rewritten, BC-419, BC-420 and BC-422, the frozen
      kernel target list, this record and the plan.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: The records tier fails on something the registration cannot repair.
    fallback: Hold every target run and report the refusal to the coordinator.
    outcome: >-
      H-264 rewritten with instrument_ready true on the seed-182 draw (10 counted, 2 at
      distance 2). Nine kernel targets frozen: the plan's filter at this tree admits one
      class more than the review's eight, at best penetration 0.0050045 on the default
      receipts against 0.0049995 on the recheck list the review read. The OR-12 count
      is past eight (34 cells terminal since BC-369; nine sessions since session-180's
      efficiency-loop phase), so BC-422 adds the W5 block without dedicated compute.
    evidence:
    - packing/campaign/hypotheses/H-264-n17-geometric-exclusion-cost-per-leaf.md
    - packing/campaign/agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md
    - packing/campaign/explorations/X048-session-182-overnight/kernel-targets.txt
    stop_reason: The registration is committed and pushed before the first target run.
    next_action: W6 coordination of lanes A and K and the dispatched lanes.
  - workflow: research-loop
    focus: correctness
    recording: contemporaneous
    clock_role: work
    commitment: BC-418
    objective: >-
      Run lanes A (BC-419) and K (BC-420) from the clean run worktree on three compute
      slots, admit each closure a standing verifier passes in full, and coordinate the
      dispatched lanes R, D and H; re-plan only future slices at each check-in.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: The registration is published, so measurement may begin.
    budget_minutes: 360
    started_at: '2026-10-05T08:30:00Z'
    deadline_at: '2026-10-05T14:30:00Z'
    expected_output: >-
      Per-target and per-state receipts for lanes A and K, admitted certificates with
      their verifier receipts, and the census before and after.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      A soundness alarm: the kernel closes the endpoint's state or endpoint7, the branch
      and bound certifies an endpoint control, or a census reports the endpoint not
      surviving.
    fallback: >-
      Preserve every object, record a defect, admit nothing from that instrument, and
      escalate to the owner in the handoff.
    outcome: >-
      Thirteen admissions, each on the standing kernel verifier's full pass from the
      clean run worktree: lane K's targets 1 and 3 to 9 and five of lane A's draws. The
      certified census fell from 126,168 states in 15,953 orbits to 72,272 states in
      9,165 orbits, the endpoint surviving, and the arity-at-most-7 entries leave 10,173
      orbits against H-267's 10^4. H-264 is accepted in exp-252, confirmed with
      corrections by its W2 review. Lanes R, D and H filed; BC-423, BC-424 and lane E
      (H-273, BC-421) registered and started. Three container restarts, each recovered
      by re-running the killed jobs from scratch.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-251-h267-n17-overnight-flag-certification.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-252-h264-n17-overnight-per-state-price.md
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-252-n17-overnight-per-state-price/census.json
    - packing/campaign/explorations/X048-session-182-overnight/receipts/K/census-arity7-after-k9.json
    - docs/project/reviews/review-2026-10-05-exp-252-h264.md
    stop_reason: >-
      The morning checkpoint at 14:30 UTC, which wrote the handoff below without
      stopping the run (OR-8).
    next_action: The continued research loop of phase 3.
  - workflow: research-loop
    focus: correctness
    recording: contemporaneous
    clock_role: work
    commitment: BC-418
    objective: >-
      Continue the run on the slices registered at check-ins, lanes A and K's frozen
      lists being exhausted: BC-423 (K-k2 at 48 rounds) and BC-424 (lane A's counted
      stalls under SW9's recipe), each control running beside its first target with
      admission gated on it, then lane E's H-273 shards and the branch-and-bound queue.
      Admit each closure a standing verifier passes in full.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      The morning checkpoint handed off without stopping the run (OR-8), and the work
      left is the slices added at check-ins.
    budget_minutes: 1005
    started_at: '2026-10-05T14:30:00Z'
    deadline_at: '2026-10-06T07:14:04Z'
    expected_output: >-
      Receipts for BC-423, BC-424, lane E's shards and the branch-and-bound queue, an
      admission commit for each gated closure that verifies, and the census after each.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      A soundness alarm: the kernel closes the endpoint's state or endpoint7, the branch
      and bound certifies an endpoint control, or a census reports the endpoint not
      surviving.
    fallback: >-
      Preserve every object, record a defect, admit nothing from that instrument, and
      escalate to the owner.
    outcome: >-
      39 admissions, each on the standing kernel verifier's full pass from the clean run
      worktree: BC-424's four (all four of H-264's counted stalls; H-274 accepted in
      exp-253 and confirmed with corrections by its W2 review), BC-425's eight arity-8
      targets (exp-254, unresolved for H-267), BC-427's targets 4 and 6 (exp-256
      accepted) and BC-428's 25 draws (exp-257 accepted, needs review). The certified
      census fell from 72,272 states in 9,165 orbits to 36,800 states in 4,687 orbits,
      the endpoint surviving. H-267 is confirmed (exp-251, W2 review with corrections),
      its arity-at-most-7 line at 8,191 orbits. Lane E searched all 95 distance-2 orbits
      with no placement (exp-255, H-273 unresolved). Held for the owner: lane K's target
      2 and BC-426's two closures, which wait on BC-423's control receipt, the
      branch-and-bound recalibration and #360's merge. The stack merged into main at
      a6279886b, and the run continued on claude/n17-session-182-continued.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-251-h267-n17-overnight-flag-certification.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-253-h274-n17-stalls-under-adaptive-rows.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-254-h267-n17-second-tranche-flags.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-255-h273-n17-distance-two-survey.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-256-h267-n17-third-tranche-flags.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-257-h275-n17-unsampled-strata.md
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-257-n17-unsampled-strata/census.json
    - docs/project/reviews/review-2026-10-05-exp-251-h267.md
    - docs/project/reviews/review-2026-10-05-exp-253-h274.md
    stop_reason: >-
      The work deadline at the finalization reserve, 07:14:04Z. BC-428 ended there, and
      exp-257's verdict is written in the commit that completes this phase.
    next_action: Phase 4 closes the session.
  - workflow: review-planning-oversight
    focus: correctness
    recording: contemporaneous
    clock_role: finalization
    commitment: BC-418
    objective: >-
      Write exp-257's verdict and close Session 182 before its deadline: stopped, its
      resource rollups withheld because they carry model identifiers (think-h8oz), and
      certified by the fast gate if it can run inside the reserve, otherwise pending
      under its own bead.
    status: stopped
    entered_by: planned_checkpoint
    switch_reason: >-
      The work deadline at the start of the finalization reserve, 07:14:04Z, ends the
      research loop; what remains is the record.
    budget_minutes: 60
    started_at: '2026-10-06T07:14:31Z'
    deadline_at: '2026-10-06T08:14:04Z'
    expected_output: >-
      exp-257's verdict, pushed; then the session stopped, with
      resource_usage_unmeasured (rollup_withheld_model_identifiers), the close report
      and SYNOPSIS view from close_session --render, and either a passed fast gate or
      certification_pending.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      The session deadline at 08:14:04Z: no commit after it, and no gate run past it.
    fallback: >-
      Leave the session for the owner to close, with this phase's next_action naming
      what remains.
    outcome: >-
      exp-257's verdict is a0ff1cd9f, pushed. The session closes stopped, its resource
      rollups withheld because they carry model identifiers (think-h8oz), its
      certification pending under think-b8hb.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-257-h275-n17-unsampled-strata.md
    - packing/campaign/session-close-report.yaml
    stop_reason: >-
      The session closes before its deadline; the owner adds the resource rollups
      (think-h8oz).
    next_action: >-
      The owner adds the rollups (think-h8oz) and certifies the handover (think-b8hb);
      the coordinator commissions exp-257's W2 review.
  budget:
    wall_minutes: 1440
    slice_minutes: 30
    checkpoint_minutes: 240
    finalization_minutes: 60
  stop_conditions:
  - Only the owner, an external blocker or exhausted work ends the run; a self-declared budget is not a stop condition (OR-8).
  - A soundness alarm stops that instrument at once; its objects are preserved, a defect is recorded and nothing from it is admitted.
  - A verifier FAIL on a producer closure stops admissions from that producer until a review.
  - Three consecutive crashes or refusals of one instrument stop that instrument.
  - Below 1.5 GB of available memory or 2.0 GB of free disk, no new job launches; a resource kill is recorded, never read as an outcome.
  - Frozen criteria and a running job's ceiling are never changed; only future slices are re-planned.
  progress:
    metric: >-
      The certified n17 census (states and orbits under admitted sub-pattern
      certificates, the endpoint surviving), and H-264's counted closures against its
      falsifier.
    before: >-
      126,168 states in 15,953 orbits certified (W7, A, SW9 and N1 admitted); H-264
      without a ready registration; the adaptive-row recipe that closed SW9 never run
      on the mixed arity-7 flags.
    after: >-
      36,800 states in 4,687 orbits certified, the endpoint surviving, under 56 admitted
      entries; H-267 confirmed at 8,191 orbits under the entries of arity at most seven;
      H-264 and H-274 accepted, H-275 accepted pending its W2 review, H-273 unresolved.
  delegations:
  - task: >-
      W3 status review of X-048 on the stack top (the draft addition, a phase-1 report
      and notes), followed by an adversarial Opus review of the draft
    operator: Opus sub-agents
    status: completed
    recording: retrospective
    outcome: >-
      Written before this run's clock started; recorded as the history this W10 phase
      acts on. The review's findings F1 to F19 found H-264 unready and mis-scoped, the
      capture continuation unresumable, three instruments needing tool changes, and
      flag certification the cheapest direct census progress.
    evidence:
    - docs/project/specs/done/plan-2026-10-05-n17-overnight.md
    files: []
    checks:
    - The review re-ran the certified census at 451154f60 and the seed-182 draw (strata only).
    uncertainty: >-
      The draft and review live in the coordinator's scratchpad; the plan carries the
      consequences that the night acts on.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Lane H integrates the corrected addition into X-048 (H3).
    phase: 1
  - task: >-
      Run operator: preflight, the registration commit and draft PR, the clean run
      worktree, and the background queues for lanes A and K
    operator: Opus sub-agent at high effort
    status: completed
    recording: contemporaneous
    outcome: >-
      Preflight, the registration commit cebb5d15a and draft PR 365, the clean run
      worktree, and lanes A and K's queues to the end of both frozen lists. Thirteen
      closures admitted, one commit each, on the standing verifier's full pass; three
      container restarts recovered by re-running the killed jobs from scratch.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-251-h267-n17-overnight-flag-certification.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-252-h264-n17-overnight-per-state-price.md
    files:
    - packing/campaign/hypotheses/H-264-n17-geometric-exclusion-cost-per-leaf.md
    - packing/campaign/agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md
    - packing/campaign/explorations/X048-session-182-overnight/kernel-targets.txt
    - packing/campaign/agent-sessions/session-182-n17-overnight-lanes.md
    - docs/project/specs/done/plan-2026-10-05-n17-overnight.md
    checks:
    - packing-validate --records before every push, and the census and negative-control test files on the admissions.
    uncertainty: >-
      The 26 certificate objects of the 13 admissions exist only on this container's
      disk until the hosted release is published (think-jhgi).
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: The run operator's continuation in phase 3.
    phase: 2
    budget_minutes: 380
    started_at: '2026-10-05T08:14:04Z'
    deadline_at: '2026-10-05T14:30:00Z'
    expected_output: >-
      The pushed registration commit and draft PR, lane A and K receipts under the
      scratch output tree, and verifier receipts for every closure.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: A soundness alarm, or the resource guards of the plan.
    fallback: Stop the affected queue, preserve its objects and report to the coordinator.
    write_scope:
    - The registration files above, admissions in the session checkout, and scratch outputs outside every worktree.
    excluded_commands:
    - Edits in the run worktree; changes to the wtn17stack or wt307fix worktrees.
  - task: >-
      Run operator, continued: BC-423's and BC-424's queues with gated admission, lane
      E's shards and the branch-and-bound queue, admitting each released closure and
      reporting to the coordinator every 30 minutes
    operator: Opus sub-agent at high effort
    status: completed
    recording: contemporaneous
    outcome: >-
      Ran BC-423's and BC-424's gated queues, lane E's shards, the branch-and-bound
      queue until it stopped under its frozen rule (BB-MISCALIBRATED), and the queues of
      BC-425, BC-426, BC-427 and BC-428: 39 admissions, one commit each, on the standing
      verifier's full pass. BC-423's target 2 was voided by its gate and is held with
      BC-426's two closures for the owner. Pushes went out hourly after --records.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-257-h275-n17-unsampled-strata.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-256-h267-n17-third-tranche-flags.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-254-h267-n17-second-tranche-flags.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-253-h274-n17-stalls-under-adaptive-rows.md
    files:
    - packing/campaign/explorations/X048-session-168-pilots/certified-sub-patterns.yaml
    - packing/hosted/n17-x048-session-168-certificates.yaml
    - packing/campaign/agent-sessions/session-182-n17-overnight-lanes.md
    checks:
    - >-
      packing-validate --records, check_retained_json, the hosted-data manifest check
      and the census, negative-control and hosted-data test files (90 tests) before
      every admission commit and push.
    uncertainty: >-
      The certificate objects of the 39 admissions exist only on this container's disk
      until the hosted release is published (think-jhgi); every non-closure's node is
      kept in scratch.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: None for the run operator; phase 4 closes the session.
    phase: 3
    budget_minutes: 1005
    started_at: '2026-10-05T14:30:00Z'
    deadline_at: '2026-10-06T07:14:04Z'
    expected_output: >-
      Receipts for BC-423, BC-424, lane E and the branch-and-bound queue under the
      scratch output tree, and an admission commit for every released closure.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: A soundness alarm, or the resource guards of the plan.
    fallback: Stop the affected queue, preserve its objects and report to the coordinator.
    write_scope:
    - Admissions and record updates in the session checkout, and scratch outputs outside every worktree.
    excluded_commands:
    - Edits in the run worktrees; changes to the wtn17stack or wt307fix worktrees.
  - task: Lane R, the capture route (lane R9, think-g2qn), from committed receipts
    operator: Fable sub-agent at max effort
    status: completed
    recording: contemporaneous
    outcome: >-
      Undecidable from the receipts with most of the question decided: none of the four
      named producer candidates is the limit, and an unnamed producer loss (the owned-hull
      compression toward the vertex mean, about 1.22e-4 at unit scale) is present and
      quantified; the review specifies the discriminating measurement for a later slice.
    evidence:
    - docs/project/reviews/review-2026-10-05-n17-capture-r9.md
    files:
    - docs/project/reviews/review-2026-10-05-n17-capture-r9.md
    - packing/campaign/explorations/X048-session-182-overnight/receipts/R9/score-pilot2-need-r9.json
    - packing/campaign/explorations/X048-session-182-overnight/receipts/R9/score-pilot2-need-r9.txt
    checks:
    - One run of devtools.score_n17_capture at 451154f60 reproduced the committed score table.
    uncertainty: >-
      The verdict rests on committed receipts; the measurement it specifies has not run.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: The coordinator codifies any candidate at the morning W10.
    phase: 2
  - task: Lane D, classification of lane K's and lane A's kernel stalls
    operator: Fable sub-agent at extra-high effort
    status: completed
    recording: contemporaneous
    outcome: >-
      K-k2 is loss-limited (knot owners interior-NW and interior-W at 0.5 and 4.5 per cent
      support, median cut margins near 0.010 against the 1/512 core loss), stopped at its
      round cap with producer time unused. The distance-4 and distance-6 per-state stalls
      share a wall knot whose margins (about 0.011 to 0.015) sit below the 1/32 losses of
      N1's recipe but above a 1/512 cut; the distance-2 draw 1964767 is
      consistency-limited at a true fixed point. C2 (aimed splits) is selected before C5.
    evidence:
    - docs/project/reviews/review-2026-10-05-n17-stall-classification.md
    files:
    - docs/project/reviews/review-2026-10-05-n17-stall-classification.md
    - packing/campaign/explorations/X048-session-182-overnight/receipts/stall-diagnosis/
    checks:
    - diagnose_n17_flag support and domains on each stall node, at nice 19 while the one-minute load was below 6.
    uncertainty: >-
      Deviation: the per-state nodes were diagnosed at 100 poses per owner, not 400, because
      400 did not finish inside the 1,200 s ceiling at the night's load (the receipts are
      suffixed -s100); the share estimates widen to about 5 percentage points.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: BC-423 and BC-424 test its two readings; the nodes were deleted once its receipts named them.
    phase: 2
  - task: Lane H, census reads the recheck, the survey distance filter, and the X-048 addition
    operator: Opus sub-agent at high effort
    status: completed
    recording: contemporaneous
    outcome: >-
      H1, the census projects the selector recheck's still-flagged classes by default; H2,
      survey_n17_residue --distance D with --sample 0; H3, the X-048 October 5 status
      addition. The coordinator committed and merged them on the session branch.
    evidence:
    - packing/devtools/census_n17_certified.py
    - packing/devtools/survey_n17_residue.py
    - packing/campaign/explorations/X-048-n17-optimality-after-n11.md
    files:
    - packing/devtools/census_n17_certified.py
    - packing/devtools/survey_n17_residue.py
    - packing/tests/test_census_n17_certified.py
    - packing/tests/test_survey_n17_residue.py
    - packing/campaign/explorations/X-048-n17-optimality-after-n11.md
    checks:
    - The census and survey test files pass on the session branch.
    uncertainty: >-
      The survey later gained --shard K/N in this session (504a84464) for lane E, outside
      lane H's own commits.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: None for the lane.
    phase: 2
  outputs:
  - packing/campaign/hypotheses/H-264-n17-geometric-exclusion-cost-per-leaf.md
  - packing/campaign/agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md
  - packing/campaign/explorations/X048-session-182-overnight/kernel-targets.txt
  - docs/project/specs/done/plan-2026-10-05-n17-overnight.md
  checks:
  - >-
    census_n17_certified at the session checkout (451154f60 plus the registration's
    record edits): 126,168 states in 15,953 orbits, 4 admitted, endpoint surviving; the
    plan's kernel-target filter selects nine classes.
  - >-
    survey_n17_residue --flag-set arity8 --sample 12 --seed 182 --strata-only: the
    endpoint control plus 12 draws, 2 at distance 2, 7 at 4 and 3 at 6 (draw only, no
    search).
  - 'full gate: fast at b68744cba08d770c50f3c4494f9e40c13db724cf: passed (hosted Packing validation
    run 37433376429 on PR 379, the head after this session''s close commit 9e7021715, carrying
    the handed-over source with exp-257''s W2 corrections and a merge of main)'
  stop_reason: >-
    The deadline: the overnight run ended at the finalization reserve with exp-257's
    verdict, and the session closes stopped because its resource rollups are withheld
    (they carry model identifiers; think-h8oz) and its certification is pending
    (think-b8hb).
  next_action: >-
    BC-418 continues under think-tmz6: the owner's decisions recorded here come first (the
    resource rollups that resource_usage_unmeasured names, lane K's target 2 with the two
    held re-runs, and the branch-and-bound recalibration); exp-257 resumes at u31
    (think-2pjf).
  ended_at: '2026-10-06T07:21:24Z'
  resource_rollups: []
  resource_usage_unmeasured:
    reason: rollup_withheld_model_identifiers
    detail: >-
      Measured, not committed: the harness and sub-agent logs exist, but every rollup
      this repository's contract writes is keyed by model identifier, which this
      session's agents may not commit. The owner can add the rollups with close_session
      --update. The logs, on the run container under
      /root/.claude/projects/-home-user-squares/: the harness log
      6b1ed85f-ba08-5540-8095-4fd66881916f.jsonl, from 2026-10-04T05:54Z to the close,
      so it also spans work before this session; and the 15 sub-agent logs started at or
      after 2026-10-05T08:13:53Z under its subagents/ folder
      (agent-a0b0e4ddf405acc39.jsonl, agent-a3ad468c1d0eaa494.jsonl,
      agent-a4c8fa035f1ffcdfe.jsonl, agent-a53bf696b86d675e4.jsonl,
      agent-a5876044abe43c05d.jsonl, agent-a76f70717495baf45.jsonl,
      agent-a819f6f47909bde6a.jsonl, agent-a9984cf91e54e97ec.jsonl,
      agent-aa7f27534be946dec.jsonl, agent-ab2288a20d80178d9.jsonl,
      agent-ab708fe86a4d2a573.jsonl, agent-ac87a45cbae726fa6.jsonl,
      agent-acf4d10a9500316cf.jsonl, agent-af38a7dfb4a15a2aa.jsonl,
      agent-af521cc6fd2b8c3aa.jsonl). Excluded: agent-af4f5ec641151fc81.jsonl and
      agent-ab6ed7d52f8584026.jsonl, started at 2026-10-05T04:46Z, before the session.
    disposition_bead: think-h8oz
    handoff_role: work_handoff
---
# Session 182: n17 Overnight Lanes

This session executes the
[n17 overnight plan](../../../docs/project/specs/done/plan-2026-10-05-n17-overnight.md)
under BC-418 (`think-tmz6`). It opened with a W10 phase, the declared entry point, which
rewrote [H-264](../hypotheses/H-264-n17-geometric-exclusion-cost-per-leaf.md) in place
and registered the night’s cells in
[agenda-042](../agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md) before
any target ran.

## Lanes

| Lane | Cell and bead | Workflow | What it runs |
| --- | --- | --- | --- |
| K, flag certification | BC-420, `think-035m` | W6 under H-267 | The endpoint7 control, then the nine frozen targets in [kernel-targets.txt](../explorations/X048-session-182-overnight/kernel-targets.txt) under SW9’s adaptive-row recipe. |
| A, per-state price | BC-419, `think-z8an` | W6 under H-264 | The float pre-screen on the seed-182 draw, the kernel control on the endpoint’s state, then twelve draws two at a time. |
| R, capture route | `think-jcte` | W3 | Lane R9’s verdict from committed receipts. |
| D, stall diagnosis | `think-023x` | W3 | Lane K’s stall nodes, loss- or consistency-limited. |
| H, records and tools | `think-ahe4` | W9 | The census reading the recheck, the survey’s distance filter, and the X-048 addition. |
| W5 block | BC-422, `think-9ntw` | W5 | Gate walls from the registration’s validation runs and per-row costs from the lanes’ receipts. |

Lanes A and K run only from a detached run worktree at the registration commit, which is
never edited. Every closure is re-proved there by a standing verifier in full before the
coordinator admits it in the session checkout.
Certificate objects stay out of Git (OR-18).

## Notes for the Morning Record

- For exp-251’s reviewer: lane K’s first target, K-k1, started at 09:07:12 UTC, after
  the registration commit `cebb5d15a` but about four minutes before its push; the commit
  hash, which every receipt names, still fixes the order.
- A container restart at about 10:32 UTC killed every process.
  Three jobs without receipts (A-m1964767, A-m2878207, K-k6) re-ran from scratch; every
  closure already had its verification receipt, and the queues resumed by skipping
  completed receipts.
- A second container restart killed every process: they stopped writing at about 12:45
  UTC and the container rebooted at 13:24:55. BC-423’s endpoint7 control (started 11:29,
  its producer done and its checker mid-run), BC-424’s endpoint-state control (started
  12:07) and lane E’s shard 3 left no receipts and re-ran from scratch at 13:29.
- Procedure changed at the coordinator’s direction after that restart: BC-423’s and
  BC-424’s controls now run beside their first target instead of before it, and
  admission, not launch, is gated on the control.
  A closure verified while its lane’s control is still running waits until the control
  finishes without closing; a control closure is still a soundness alarm that stops the
  instrument and voids the lane’s closures.
  Every soundness gate is kept.
  The reason: two container restarts in a day, and controls under the 48-round settings
  run to near their 7,000 s ceiling, so running controls serially doubled each lane’s
  exposure to a restart.
- K-k2 stopped at its 24-round cap with producer time unused, so `--max-rounds` is a
  free lever for lane K’s stalls; BC-423 tests it with lane D’s settings.
- Lane D diagnosed the per-state stall nodes at 100 poses per owner instead of 400,
  because 400 did not finish inside its 1,200 s ceiling at the night’s load.
- exp-252 (H-264) is accepted, confirmed with corrections by its W2 factual review; the
  review’s F1 corrects the attribution in the message of `6717b0b11`: state 5500414’s
  orbit was already excluded by SW9 (exp-250), not by lane K’s flags.
- Slices added at check-ins, each registered before its first run: BC-423 (K-k2 with
  lane D’s settings), H-273 and BC-421 (lane E, on slot 4, with the survey’s new
  `--shard`), and H-274 and BC-424 (lane A’s counted stalls under SW9’s recipe).
- The branch-and-bound queue’s Knuth list is frozen in `s182/K/bb/knuth-targets.txt`:
  the 34 flags with at most two wall cells (the recheck’s placed flag excluded) and
  kernel target 2. It waits for the slot after BC-423.

## Morning Handoff, 5 October 14:30 UTC

Written at 14:40 UTC from the branch head `4a49f464b`, the run’s logs and receipts, tbd
and GitHub. The run is not stopped (OR-8).

### What Changed Scientifically

- **The certified residue fell by 43 per cent.** 126,168 states in 15,953 orbits at the
  registration (`cebb5d15a`) became 72,272 states in 9,165 orbits at `dfd38187c`, the
  endpoint surviving. Thirteen admissions, each re-proved in full by the standing kernel
  verifier from the clean run worktree.
- **H-267 is 173 orbits above its threshold.** The arity-at-most-7 entries alone leave
  10,173 orbits (80,260 states), down from exp-249’s 17,690, against $10^4$. Lane K
  closed 8 of its 9 frozen arity-7 flags under SW9’s adaptive-row recipe; target 2 hit
  its 24-round cap. BC-423 is re-running target 2, and the census projects that a closure
  would remove 1,372 orbits at arity 7 or less.
  No H-267 verdict before a W2 review of exp-251.
- **H-264 is accepted:** 5 of the 10 counted draws closed inside 7,000 s, confirmed with
  corrections by its W2 review.
  A closed state cost 352 to 869 s of process CPU plus 151 to 676 s of verification.
  Every non-closure was a producer fixed point well inside its ceiling.
- **Planning evidence:** lane R found an unnamed producer loss and left the capture
  route undecidable from receipts, with a staged measurement specified.
  Lane D found most stalls limited by row width and selected two zero-build re-runs,
  then C2, then C5.
- Nothing moves a bound, a frontier field or a register rung.
  No soundness alarm, no verifier FAIL, no stop marker.

### Census and Admissions

Every verifier receipt is
`packing/campaign/explorations/X048-session-168-pilots/certificates/<entry>/verification.json`:
`status: PASS`, `mode: full`, revision `cebb5d15a`, `dirty: false`, listing
`kernel-streamed`.

| # | Entry | Source | Producer CPU | Verifier (full pass) | Commit | Census after (states, orbits) |
| --- | --- | --- | ---: | --- | --- | --- |
| — | registration | — | — | — | `cebb5d15a` | 126,168, 15,953 |
| 1 | `s182-k1` | K target 1, arity 7 | 276 s | 173 s, 1,664 rows | `8a84c09fe` | 102,124, 12,929 |
| 2 | `s182-m5683195` | A index 2, distance 4 | 869 s | 676 s, 4,247 rows | `ec71f6977` | 102,116, 12,928 |
| 3 | `s182-k3` | K target 3 | 165 s | 124 s, 1,169 rows | `3646aad39` | 89,456, 11,336 |
| 4 | `s182-k4` | K target 4 | 422 s | 269 s, 3,976 rows | `f0a034429` | 83,148, 10,546 |
| 5 | `s182-k5` | K target 5 | 149 s | 82 s, 1,534 rows | `affa75535` | 81,684, 10,360 |
| 6 | `s182-k6` | K target 6 | 207 s | 175 s, 2,209 rows | `f1cffc4df` | 79,872, 10,132 |
| 7 | `s182-k7` | K target 7 | 231 s | 163 s, 1,154 rows | `9a059bb4f` | 78,852, 10,003 |
| 8 | `s182-k8` | K target 8 | 113 s | 69 s, 1,120 rows | `7f19493d1` | 73,236, 9,291 |
| 9 | `s182-k9` | K target 9 | 562 s | 506 s, 5,894 rows | `b9a24903b` | 72,296, 9,168 |
| 10 | `s182-m5500414` | A index 3, distance 6 | 594 s | 328 s, 3,536 rows | `6717b0b11` | 72,296, 9,168 (orbit already excluded by SW9) |
| 11 | `s182-m7844815` | A index 12, distance 6 | 395 s | 184 s, 2,337 rows | `dbb840a15` | 72,288, 9,167 |
| 12 | `s182-m4028335` | A index 11, distance 4 | 545 s | 252 s, 2,579 rows | `2b06c8d3c` | 72,280, 9,166 |
| 13 | `s182-m2601983` | A index 7, distance 4 | 352 s | 151 s, 2,485 rows | `dfd38187c` | 72,272, 9,165 |

The final line is the committed
`results/exp-252-n17-overnight-per-state-price/census.json` (17 admitted entries) and
the W2 review’s `census-head.json`. Of the 79 flags still projecting, certifying all
would leave 17,136 states in 2,193 orbits.

### Lane K and H-267 (exp-251, BC-420, BC-423)

- **Controls:** endpoint7 under the frozen recipe returned `PASS_CONTROL_STALLED` in
  1,245 s of wall.
- **Targets:** 1 and 3 to 9 closed in 113 to 562 s of process CPU each, rows finest at
  1/64 to 1/512. Target 2 (corner-SW, side-N0, side-W0, side-W1, interior-SW,
  interior-NW, interior-W) stopped at its 24-round cap after 3,048 s of wall and 2,331 s
  of CPU with producer time unused.
- **H-267’s count:** 10,173 orbits under W7, A, `s182-k1` and `s182-k3` to `s182-k9`.
  The receipt is `s182/K/census-arity7-after-k9.json` with its ledger
  `s182/K/ledger-arity7-scratch.yaml`, both in the scratchpad and not committed; exp-251
  quotes the figure without a filed receipt.
- **Target 2’s weight:** BC-423’s cell and the PR body cite 2,917 orbits, the
  registration-time projection.
  Against today’s certified line it projects 1,252 orbits, and against the arity-7
  ledger 1,372, so a closure would leave about 8,800 at arity 7 or less (a projection,
  not a count).
- **BC-423:** registered in `75327a0b9` (48 rounds, 2,304 rows, octagon core).
  Its control and target are on their third launch, both since 14:20 UTC; the target
  reached round 24 within 12 minutes.
- **Branch and bound:** never started.
  queue-B paused on its load guard at 11:27 (15-minute load 7.55) and then yielded its
  slot to BC-423. The Knuth list is frozen at 35 entries in
  `s182/K/bb/knuth-targets.txt`.
- **exp-251** is still recorded `in-progress`.

### H-264 (exp-252, BC-419) and H-274 (BC-424)

- **Verdict:** accepted at `9bcddf6e9` once the fifth closure was verified (12:02 UTC);
  all twelve draws had run by 12:07. The endpoint-state control stalled in 333 s; the
  float pre-screen placed only the endpoint.
- **W2:**
  [the factual review](../../../docs/project/reviews/review-2026-10-05-exp-252-h264.md)
  confirmed the verdict with corrections, applied in `1676daa64`. F1, 5500414’s orbit
  was already excluded by SW9, not by lane K’s flags (the message of `6717b0b11` is
  wrong). F2, five counted non-closures at 634 to 1,297 s, not four.
  F3, the round’s wall is 12,041 s. F4, rounding, the wall-to-CPU ratio (1.86 over 13
  runs) and the control’s mask.
  F5, the missing extrapolation, which the operator then added.
- **Per-state cost:** closures 5683195 (869 s), 5500414 (594 s), 7844815 (395 s),
  4028335 (545 s), 2601983 (352 s); counted non-closures 3063677 (634 s), 2817021 (828
  s), 2784767 (828 s), 2878207 (925 s), 1949551 (1,297 s); distance-2 draws 1964767 (623
  s) and 851903 (77 s), neither closed.
  All process CPU; the full table is in exp-252.
- **Extrapolation over drawn strata:** the counted draws come from 8 strata holding
  1,354 of the frame’s 2,255 non-endpoint orbits.
  The size-weighted point estimate is about 686 closing at about 730 s of CPU per state
  run. Six of the eight strata rest on one draw each, so this is a description scaled to
  strata, not a measured rate.
- **Unsampled:** 21 strata holding 827 orbits, 430 at distance 8 or more and 397 in 12
  strata at distances 2 to 6. H-264’s regime counted only the first 430 because it read
  strata as distance bands.
  No price for the residue tail is claimed.
- **H-274 (BC-424):** registered in `9e624b845` with the four counted stalls that
  existed then (2784767, 2817021, 2878207, 3063677) under SW9’s recipe; 1949551 stalled
  later and is not in it.
  The control and 2784767 are on their third launch since 14:20 UTC.

### Lane R: The Capture Route

[The R9 review](../../../docs/project/reviews/review-2026-10-05-n17-capture-r9.md)
(`think-jcte`):

- **Verdict:** undecidable from the receipts, with most of the question decided.
  None of the four named producer candidates is the limit: hull cap, octagon core loss,
  one-sided measurement and partner pruning are all ruled out.
- **New loss:** the producer pulls every owned-hull vertex $2^{-12}$ of its distance
  toward the vertex mean, about $1.22\times10^{-4}$ at unit scale.
  That is 61 per cent of H-261’s radius $1/5000$ and 36 per cent of the position floor
  $1/3072$. It caps the reachable radius but does not explain the stall; `think-juy9`
  tracks the repair.
- **The fixpoint is set by the box, not the rows,** down to the finest rows run.
  The stuck quantities are the tilted squares’ turn ranges.
- **Next build it selects:** a staged measurement, nothing run.
  Stage 0 is n11’s case-438 positive control with the pull repaired (2 to 4 CPU-hours).
  Stage 1 reads the angle ranges at two and four times the rows: about 20 CPU-hours in
  one process, started from round 0 with `--checkpoints`. Reading B ends the kernel’s
  capture route and selects the patch counter of section 7; reading A goes to stage 2.

### Lane D: Stall Classification

[The classification](../../../docs/project/reviews/review-2026-10-05-n17-stall-classification.md)
(`think-023x`) covers all eight stalls:

| Class | Runs | Reading |
| --- | --- | --- |
| Loss-limited flag | K-k2 | interior-NW and interior-W 0.5 and 4.5 per cent supported, cut margins about 0.010 against the 1/512 core loss of 0.00097; stopped at the round cap with 2,400 s of producer share unused |
| Wall crowd, mixed by the rule | A-m2817021, A-m3063677, A-m2878207, A-m2784767 | one or two wall neighbours 15 to 39 per cent supported, margins 0.011 to 0.018: below the 1/32 losses of N1’s recipe, two to four times the 1/512 losses |
| Consistency-limited | A-m1964767, A-m851903 (distance 2), A-m1949551 | every owner at least 63, 72 and 66 per cent supported, at true fixed points |

Build order: two zero-build re-runs first (BC-423 and BC-424, both running), then C2
(aimed splits, a producer policy with nothing new for a verifier), then C5 (branch
predicates, first tested on the three consistency-limited nodes).
Deviation: the per-state nodes were sampled at 100 poses per owner, not 400, which
widens the shares to about ±5 points.

### Lane E: H-273 (BC-421)

Shards 0 to 2 are complete: 30 of the 95 distance-2 orbits searched, no placement, each
shard’s endpoint control placed.
Shard 3 was lost at 4 of its 10 orbits in the second restart.
Shards 3 to 9 wait for a free slot (four busy since 14:20). Float search can refute
H-273 but never confirm it.

### Lane H

Done and committed: the census reads the selector recheck (`6bfd419ec`), the survey
takes `--distance` and `--sample 0` (`da0d91b00`) and later `--shard K/N` (`504a84464`),
and X-048 gained its October 5 addition (`f6f4f3d8b`). X-048’s census row is dated at
`s182-k1` (102,124 states, 12,929 orbits).

### Costs

CPU from completed receipts: kernel `process_cpu_seconds`, survey per-state seconds,
verifier wall as an upper bound.
Agent elapsed time is not recorded in the session record; the spans run from the lane
bead’s start to its filing commit.

| Lane | CPU-hours | Budget | Agent and span |
| --- | ---: | --- | --- |
| K (BC-420) | 1.95 (kernel 1.51, verifier 0.43) | 17 kernel, 14 branch and bound | run operator’s queue, 08:46 to 11:21 |
| A (BC-419) | 3.81 (survey 1.07, kernel 2.30, verifier 0.44) | 26 | run operator’s queue, 08:46 to 12:07 |
| E (BC-421) | 1.53 | 6 | queue, 11:41 to 12:40, then restarts |
| D | 0.66 (17 diagnosis jobs) | 2 | Fable, extra-high, 08:20 to 12:23 |
| R | one scorer run | none | Fable, max, 08:20 to 09:21 |
| H | tests only | minutes | Opus, high, 08:20 to 09:59 |
| W2 of exp-252 | about 0.07 | — | strong tier, 12:08 to 12:33 |
| BC-423, BC-424 | no receipt yet | about 5 and 10 | queues |
| **Total completed** | **about 7.9** |  | coordinator since 08:14 |

The restarts cost about 3.2 job-hours of wall with no receipt (0.6, 2.1 and 0.5) and
about 90 minutes of host time with nothing running.

### Still Running at 14:40 UTC

| Job | Started | Ends by | Note |
| --- | --- | --- | --- |
| BC-423 endpoint7 control | 14:19:55 | 16:17 (7,000 s ceiling) | must not close; gates BC-423’s admission |
| BC-423 K-k2 | 14:20:00 | 16:17 | a closure verifies (at most 4,000 s) and waits for the control |
| BC-424 endpoint-state control | 14:19:55 | 16:17 | gates BC-424’s admissions |
| BC-424 stall 2784767 | 14:20:00 | 16:17 | 2817021, 2878207 and 3063677 follow on two slots; worst case about 20:10 |
| Lane E shards 3 to 9 | waiting since 14:20:10 | at most 3,900 s each | shards 0 to 2 took 17 to 23 minutes |
| queue-B (branch and bound) | waiting since 14:20:10 | — | starts when BC-423’s queue releases its lock; 35 Knuth estimates at 420 s each, then certificate runs |

The watchdog and guard were relaunched at 14:19:55. The coordinator’s heartbeat loop
started at 14:18:47 with a 7,000 s window, which ends at 16:15:27.

### Incidents: Three Container Restarts

| # | Last watchdog line | Reboot | Killed without a receipt | Relaunch |
| --- | --- | --- | --- | --- |
| 1 | 10:31:20 | 10:32:48 | K-k6, A-m1964767 (checker mid-run), A-m2878207 | 10:36:30 |
| 2 | 12:45:35 | 13:24:55 | BC-423’s control (round 9, node saved at 4,376 s, checker mid-run), BC-424’s control (round 16), lane E shard 3, the queue-B waiter, watchdog and guard | 13:29:16 |
| 3 | 13:36:16 | 14:17:08 | BC-423’s control (round 4) and K-k2 (round 19), BC-424’s control (round 3) and 2784767 (round 3) | 14:19:55 |

- **Diagnosis, the coordinator’s:** the container is suspended while no session has an
  active turn or tracked background work.
  Restarts 2 and 3 each began with a freeze of about 40 minutes before the reboot;
  restart 1 did not.
- **Lost work:** the jobs above re-ran from scratch, and every closure already had its
  verifier receipt. The kernel producer has no checkpoint, so each kill costs the whole
  job.
- **Procedural change** (recorded in `4a49f464b`): BC-423’s and BC-424’s controls run
  beside their first target, not before it.
  Admission, not launch, is gated on the control: a verified closure waits until its
  control finishes without closing, and a control closure is still a soundness alarm
  that voids the lane’s closures.

### Stack State

Every red job is a wall-time verdict with every test passing.
That is read from the job logs for #347, #360 and #365, and from the PR bodies’
Validation sections for #354, #355, #356 and #350. `packing-required` fails as a
consequence in each.

| PR | Head | Latest run | Red jobs | Notes |
| --- | --- | --- | --- | --- |
| [#347](https://github.com/jlevy/squares/pull/347), stack base | `40aa3be3a` | 37303411703 | suite-c 161.7 s of 154 (3,859 passed) | B1 open (`think-jhgi`); main `dee22b882` merged in |
| [#354](https://github.com/jlevy/squares/pull/354) | `8b73c70e0` | 37304183235 | suite-a 136.2 s of 131; `test_the_render_is_deterministic` 12.12 s of 12 |  |
| [#355](https://github.com/jlevy/squares/pull/355), draft | `7b2f3ba85` | 37304649789 | suite-c 161.4 s of 154 | Sessions 170 to 172 certified at `405e12a88` (run 37297540063) |
| [#356](https://github.com/jlevy/squares/pull/356), draft | `c3cc143ae` | 37305130479 | suite-a 132.2 s of 131; the same test at 12.36 s | Sessions 174 to 176 pending: no #356 run has passed its shard walls |
| [#360](https://github.com/jlevy/squares/pull/360), draft | `db1556daf` | 37306449499 | suite-a 136.8 s of 131; the same test at 12.20 s | Sessions 177 to 179 certified at `3b5edcdd9` (run 37305598332) |
| [#365](https://github.com/jlevy/squares/pull/365), draft | `4a49f464b` | 37317444019 | suite-a 136.2 s of 131, suite-c 165.9 s of 154, suite-d 131.8 s of 131 | lacks #360’s `db1556daf`; title and body stale |
| [#350](https://github.com/jlevy/squares/pull/350), leaf on #347 | `83947edc0` | 37306020053 | suite-a 134.7 s of 131; the same test at 12.21 s | all required passed at `bc29657cd` |
| [#336](https://github.com/jlevy/squares/pull/336), on main | `11cf1f3e7` | — | none | mergeable, clean |

- **Stack 357** holds #347, #354, #355, #356, #360 and #365 on main.
  GitHub reports every PR mergeable.
- **Snapshot prune:** #347’s composite-vector prune (`40aa3be3a`, 8,559,777 bytes)
  replaced #360’s interim folder prune (`93a6839ca`, reverted in `06c2ba450`). suite-b,
  which carries the snapshot-cap test, passes on every layer and on #365.
- **Merge readiness: not ready.** Three things block: #347 B1, the wall verdicts on
  every layer (`think-umlx`, the owner’s `think-p684`), and the certification of
  Sessions 174 to 176 (`think-q0z7`).
- **#365’s body is stale:** it says fourteen admissions (there are 13), 120 manifest
  objects (118), four ledger entries, a closure CPU range of 351 to 868 s and four
  non-closures, and that the W2 review is still pending.

### Decisions for the Owner

1. **Publish the hosted objects** (`think-jhgi`). Allow `uploads.github.com` in the
   environment, then run `python -m devtools.hosted_data publish --manifest
   hosted/n17-x048-session-168-certificates.yaml` from `packing/` and a fetch round
   trip. Release `data/n17-x048-session-168-certificates-v1` has 0 assets.
   #347’s manifest (B1) is 92 objects, 112,285,110 bytes; #365’s is 118 objects,
   307,697,692 bytes (293 MiB), adding 26 for tonight’s 13 certificates.
   Those 26 exist only on this container’s disk.
2. **Behavioural-lane capacity** (`think-p684`, `think-umlx`, `think-skka`). A fifth
   shard, ceilings about 9 per cent higher, or a smaller footprint for #347.
   Re-recording `suite-file-costs.json` needs the hosted run artifacts, and this
   environment cannot download them: the artifact host
   `productionresultssa19.blob.core.windows.net` is denied by egress policy.
3. **Negative-control red baseline** (`think-nns5`). Forty-nine controls (4 on
   `check_readme`, 10 on `validate_schemas`, 35 on `ledger check`) are scored over
   commands that exit 1 unmutated in the worker snapshot, with or without the composite
   prune. The dead directory link from exp-249 comes with #347’s folder prune.
   Decide its priority and whether it gates stack 357.
4. **The R9 route** (`think-g2qn`, `think-juy9`). Either repair the pull and run stage 0
   (2 to 4 CPU-hours), then stage 1 (about 20 CPU-hours in one checkpointed process), or
   defer capture. A 20-hour process on a host that suspends when idle needs
   `--checkpoints` and a keepalive.
5. **A W2 review of exp-251 before any H-267 claim.** It should file the arity-7 census
   receipt and note that K-k1 started 4 minutes before the registration push (the commit
   hash still fixes the order).
   BC-423 decides whether the count can cross $10^4$.
6. **Merge order** (`github-merge` is `confirm-session`). #336 any time.
   Stack 357 by `gh stack merge 360 --yes --merge` once #347 B1 is resolved or
   explicitly waived, the wall verdicts are resolved or accepted, and Sessions 174 to
   176 are certified. Then #350 retargeted to main.
   Then #365 after its own review and a cascade of `db1556daf`.
7. **Whether the run continues** to its deadline, 2026-10-06T08:14:04Z. Running: BC-423
   and BC-424. Queued: lane E shards 3 to 9 and the branch-and-bound queue.
   Budget left: K kernel about 15.5 CPU-hours, branch and bound 14, A 22, E 4.5. It
   needs a keepalive while unattended; the current heartbeat ends at 16:15 UTC.

### Beads, Links and Gate

- **Beads at 14:35:** created this session `think-035m`, `think-z8an`, `think-jcte`,
  `think-023x`, `think-ahe4` and `think-9ntw` (08:19), `think-p684` (08:52),
  `think-juy9` (09:12) and `think-nns5` (11:31). `think-q0z7` was updated at 12:04
  (Sessions 177 to 179 certified).
  `think-jcte`, `think-023x` and `think-ahe4` are still `in_progress` though this record
  marks lanes R, D and H complete.
  `think-jhgi`’s title still says 92 objects.
  `think-e17c` (H-264) is open after exp-252’s verdict.
- **PR:** [#365](https://github.com/jlevy/squares/pull/365), stacked on #360 in stack
  357\.
- **Local validation:** `packing-validate --records` passes at `4a49f464b` (44 steps, 41
  s). The last local `--push` (11:00) failed on the bead tree, which #360’s merge fixed,
  and on reachable tests timing out at load near 10. The hosted fast gate at `4a49f464b`
  fails only on wall verdicts.
- **Gate declaration:** pending certification.
  The full checkpoint did not run; the plan keeps it off this host while compute runs.

### Since the Handoff

- `1e986d053` merges #360’s `db1556daf`, so #365 no longer lacks it.
- `76f78b826` files H-267’s arity-at-most-7 count under
  [receipts/K](../explorations/X048-session-182-overnight/receipts/K/): the census and
  the derived ledger it ran on, whose header names the command that writes it.
  exp-251 cites both, so its 10,173 orbits now rest on a filed receipt.
- #365’s title and body carry the corrected figures: 13 admissions, 118 manifest objects
  (307,697,692 bytes), closure CPU 352 to 869 s and five counted non-closures.
- `think-jcte`, `think-023x` and `think-ahe4` are closed, each citing its filing
  commits, and `think-jhgi`’s title names 118 objects.

## After the Handoff

- **H-274 is accepted**
  ([exp-253](../series/series-000-smoke-and-calibration/experiments/exp-253-h274-n17-stalls-under-adaptive-rows.md)),
  confirmed with corrections by its
  [W2 factual review](../../../docs/project/reviews/review-2026-10-05-exp-253-h274.md).
  BC-424’s endpoint-state control stalled at its 24-round cap in 6,599 s and passed at
  16:09:56 UTC, releasing states 2784767 and 2817021 (`36c081a4d`, `3396efda0`); the
  verdict is `90a031fb6`. State 2878207’s producer closed at 16:08:36, before the
  control ended and before the verdict; it was verified at 16:15:37 and admitted after
  the verdict (`400c57176`). The fourth, 3063677, closed at 17:08:53 and was verified at
  17:36:03, so all four frozen states closed, and BC-424 is complete.
  The certified census is 72,248 states in 9,162 orbits, the endpoint surviving.
- **BC-423’s control is undecided, so target 2 is not admitted.** Target 2 closed under
  BC-423’s settings at 15:02:59 (46 rounds, 33,834 rows, finest row 1/512), and the
  standing verifier passed it in full at 15:22:50 in 1,190 s. Its endpoint7 control
  under the same settings ended INCOMPLETE at 16:16:40. The producer stopped at its time
  share after step 64 of round 9, at 4,280 s, with every owner’s rows still live (192 or
  512). It saved its node, and the checker then ran out of the 7,000 s ceiling (“indexed
  event construction timed out after 1013 edges”). An INCOMPLETE control is not a pass,
  so the gate voided the closure.
  The certificate and every object are kept.
  The receipt and the producer’s progress records are filed beside the other lane K
  receipts in [receipts/K](../explorations/X048-session-182-overnight/receipts/K/).
- **The saved control node is re-checked at 14,000 s**, at the coordinator’s decision.
  `check_n17_subpattern --check-saved` runs the checker alone, never importing the
  producer, on the kept seed and node from the clean run worktree; it started at
  16:20:26. The two-hour single-process limit is relaxed for this one job because the
  session’s heartbeat now prevents the container from suspending.
  A stall on the endpoint7 node is the control’s pass and releases target 2 for
  admission. A closure would be a soundness alarm.
- **The branch-and-bound queue stopped under its frozen rule.** It started in BC-423’s
  slot at 16:16:41. Its endpoint-north control returned unresolved-at-budget in 90 s.
  The Knuth calibration on A then estimated a mean of 13,532 nodes against the 41,598
  recorded, 3.07 times low, just outside the factor-of-three band.
  W7’s estimate was 2.0e9 nodes.
  The queue wrote BB-MISCALIBRATED and stopped routing, so no branch-and-bound
  certificate run started.
  At the coordinator’s direction it stays stopped; recalibration is a decision for the
  morning.
- **BC-425, lane K’s second tranche, is registered before its first run.** It takes the
  ten standing flags with the highest projected gain against the certified line at
  `18b7c5ae1`, using lane K’s filter widened only in arity: at most 8 cells, at least
  three wall or corner cells, best penetration at least 0.005. All ten are arity 8, so
  their closures count for the census but not toward H-267’s arity-at-most-7 criterion.
  They run under lane K’s frozen SW9 recipe, which lane K’s passed endpoint7 control
  covers. One slot ran from 16:37, and a second joined at 17:36 when BC-424’s queue
  ended, ahead of lane E’s second worker.
  By 18:04, four targets had closed and been admitted (t1, t2, t4, t5), and t3 had
  stopped at its 24-round cap at 17:52:42 without closing, its node kept for a stall
  diagnosis. The certified census then stood at 50,728 states in 6,453 orbits.
- **Lane E’s shards differ in size.** Shards 0 to 4 hold 10 distance-2 orbits each and
  shards 5 to 9 hold 9, each with the endpoint’s control besides.
  After shard 8, 86 of the 95 orbits were searched with no placement, and every control
  placed.
- **Lane E is complete, and H-273 is unresolved**
  ([exp-255](../series/series-000-smoke-and-calibration/experiments/exp-255-h273-n17-distance-two-survey.md)).
  Shard 9 ended at 18:10:46. All 95 distance-2 orbits were searched, and none placed,
  while every shard’s control placed.
  Under the frozen criterion that is no placement in 95 searches, not a proof.
  The closest miss is mask 3963647, at penetration 0.00027. BC-421 is complete.
- **BC-425’s target 6 also stopped at its round cap**, at 18:15:37, without closing; its
  node is kept for a stall diagnosis.
- **BC-425 is complete**
  ([exp-254](../series/series-000-smoke-and-calibration/experiments/exp-254-h267-n17-second-tranche-flags.md),
  unresolved for H-267). Targets 8, 9 and 10 closed and were admitted, the last verified
  at 18:43:02. In all, eight of ten closed and two stopped at the round cap.
  The certified census stands at 39,656 states in 5,057 orbits, the endpoint surviving,
  and the manifest at 142 objects, 799,004,544 bytes.
- **The saved-node re-check of BC-423’s control found no closure, but target 2 stays
  voided.** It returned PASS_SAVED_STALL at 17:40:21 in 4,793 s on the endpoint7 node:
  its cells and its seed and node ids are those of the kept control, and it checked the
  producer’s 65 steps.
  The queue’s identity comparison then failed on a JSON formatting difference and left
  target 2 voided. Releasing it by hand is the user’s decision, and the receipt is filed
  beside the other lane K receipts.
- **BC-426 re-runs BC-425’s two round-cap stalls under BC-423’s recipe**, registered
  before its runs. Any closure is verified and held, not admitted, because its only
  control evidence is the same receipt target 2 waits on.
  Both re-runs closed: target 6 at 18:30:04 in 202 s of wall, and target 3 at 18:35:35
  in 538 s, each where SW9’s recipe had stopped at its 24-round cap.
  The standing verifier passed both in full (124 s and 293 s). They are held with target
  2 for the user’s ruling, so they change neither the census nor the manifest.
  Alone they would exclude 71,448 and 81,052 states.
- **BC-427, lane K’s third tranche, is registered before its first run**, with exp-256.
  It takes the sixteen remaining flags of arity at most seven with the most projected
  gain against the certified line at `71b1d0363`: fourteen of arity 7 and two of arity
  6, with target 2 left out.
  They run under lane K’s frozen SW9 recipe on two workers, aimed at H-267 independently
  of target 2. Without target 2, any one of ten listed flags would take the arity-7
  count below $10^4$ alone.
- **H-267’s arity-7 line crossed $10^4$ at 20:04.** BC-427’s target 4 (side-E1 and six
  interior cells) closed in 171 s and was admitted on the standing verifier’s full pass
  (`488c72d77`), taking the arity-at-most-7 count from 10,173 to 9,990 orbits, the
  endpoint surviving, independently of lane K’s target 2. Targets 1 and 2 had stalled,
  target 1 at a producer fixed point and target 2 at the round cap.
  At the coordinator’s direction, exp-251 then accepted H-267 with needs_review true,
  for the W2 review the coordinator commissions.
- **The W2 review of exp-251 confirmed H-267 with corrections**
  ([review](../../../docs/project/reviews/review-2026-10-05-exp-251-h267.md)), and
  exp-251 carries them with needs_review false.
  The count includes A, certified by the branch and bound under exp-249’s recorded
  deviation, and is 10,173 without it.
  Target 2 would take 1,344 orbits from the 9,990 line
  (`census-arity7-after-bc427-t4.json`); the handoff’s 1,372 is against the 10,173 line
  after `s182-k9`. After `s182-bc427-t6` the line is 8,191, which no longer depends on
  A, and only W7 is individually decisive.
- **BC-427 closes after targets 8 and 10, and BC-428 opens on H-264’s unsampled
  strata.** At the coordinator’s re-plan at 21:43, BC-427’s queue stopped launching
  after target 10; the targets past 10 are recorded as not run, and the cap stalls are
  left for BC-423’s recipe once the user rules on its control.
  BC-428 registers H-275 and exp-257 before its first run: a seeded draw of 31 residue
  states from the 21 strata H-264’s seed-182 draw never reached, under SW9’s frozen
  recipe on two workers to the deadline.
  H-275 is a new hypothesis because H-264’s claim fixes its draw and its 32-bin
  instrument.
- **BC-427 is complete** (exp-256 accepted, needs_review false on exp-251’s W2
  recounts). Target 8 stalled at a producer fixed point at 22:02:37, the last run.
  Of the ten run, targets 4 and 6 closed, six stopped at the round cap and two at fixed
  points; targets 11 to 16 were not run.
- **The session checkout’s certificate copies are hard-linked to the run worktree’s**,
  at the coordinator’s direction, after the coordinator cleared finished pytest temp
  runs. Each of the 56 objects present on both sides (the seeds and nodes of the 28
  certificates admitted tonight) had its SHA-256 checked against the hosted-data
  manifest on both sides before linking.
  None mismatched, and 752,602,970 bytes were freed.
  Every certificate object stays in place, and the 92 objects of #347’s manifest are not
  present on this host.
  Stall nodes are kept; the coordinator decides any deletion if free space falls below
  3.5 GB.
- **BC-428 is complete, and
  [exp-257](../series/series-000-smoke-and-calibration/experiments/exp-257-h275-n17-unsampled-strata.md)
  accepts H-275 with needs_review true**, for the W2 review the coordinator commissions.
  24 of the 27 counted draws closed and were admitted on the standing verifier’s full
  pass; u6 and u12 reached producer fixed points and u15 ended INCOMPLETE at its
  ceiling. Of the distance-2 draws, u8 closed and u1 ended INCOMPLETE. Every stratum has
  a finished draw. At the coordinator’s re-plan no draw started after 06:17 UTC, when a
  7,000 s ceiling would have ended after the session deadline, so u31 was not run.
  u29 closed at the end, with its standing verification still running at the verdict, so
  it is not counted. The certified census stands at 36,800 states in 4,687 orbits, the
  endpoint surviving.
- **The session closes stopped at 2026-10-06T07:21:24Z**, before its deadline.
  Its resource rollups are withheld because every rollup the contract writes keys turns
  by model identifier, which this session’s agents may not commit
  (resource_usage_unmeasured, `think-h8oz`): the coordinator’s harness log and the 15
  sub-agent logs started during the session exist on the run container, named in the
  record, for the owner’s `close_session --update`. Certification is pending under
  `think-b8hb`: a timed `packing-validate --fast` trial at `fc9774dcb`, with both kernel
  workers running, had not finished when its 900 s timeout stopped it, against the
  tier’s 600 s ceiling, so no qualifying gate fit the finalization reserve.
  The Current Handoff in SYNOPSIS now starts from this session.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
