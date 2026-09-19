---
title: session-140 — n<=100 lower-bound survey
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-140
  title: N<=100 Lower-Bound Survey
  date: '2026-09-19'
  started_at: '2026-09-19T02:42:00Z'
  deadline_at: '2026-09-19T07:02:00Z'
  ended_at: '2026-09-19T06:53:00Z'
  branch: cursor/lb-survey-stacked-f02a
  primary_bead: think-8x4t
  status: stopped
  goal: >-
    Survey every n<=100 verified lower bound, rank which open floors the stock colgen
    can still raise, and run that queue for at least four hours on a stacked PR.
    Land T-028 only if decide_certificate prints RETAINABLE.
  resource_usage_unmeasured:
    reason: native_harness_data_unavailable
    detail: >-
      This Cursor cloud-agent run has no ClaudeEfficiencyRollup or CodexTaskTreeDelta
      receipt. Session clocks and covering walls are not a substitute.
    disposition_bead: think-8x4t
    handoff_role: work_handoff
  resource_rollups: []
  workflow_phases:
  - workflow: review-planning-oversight
    focus: process
    recording: contemporaneous
    clock_role: work
    bead: think-u5tk
    objective: >-
      Write X-038, register H-218 and exp-162, file the probe beads, and open the
      stacked PR off the session-139 branch.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 20
    started_at: '2026-09-19T02:42:00Z'
    deadline_at: '2026-09-19T03:02:00Z'
    expected_output: >-
      X-038, H-218, exp-162 with a live lease, session-140, beads under think-8x4t,
      and a draft stacked PR.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-ledger check &&
      uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      Stop planning at 03:02Z even if the PR is still drafting. Do not start a
      covering LP before X-038 names the ranked queue.
    fallback: Keep the survey and beads and start the research phase on the first rank.
    outcome: >-
      X-038 ranks n=20 at 973/200, then n=12 at 397/100, n=17 at 23/5, n=19 at
      481/100. H-218 and exp-162 are registered. Parent bead think-8x4t.
    evidence:
      - packing/campaign/explorations/X-038-n100-lower-bound-survey.md
      - packing/campaign/hypotheses/H-218-existing-colgen-raises-a-small-n-floor.md
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-162-h218-stock-colgen-small-n-floors.md
    stop_reason: Planning artifacts written; research phase opened.
    next_action: Run the X-038 ranked covering queue under phase 2.
  - workflow: research-loop
    focus: insight
    recording: contemporaneous
    clock_role: work
    bead: think-8x4t
    objective: >-
      Run the X-038 first-wave probes. Record every restricted optimum. Freeze and
      decide only when mass is below n. Land T-028 only on RETAINABLE.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: Planning artifacts and beads are in the tree.
    budget_minutes: 238
    started_at: '2026-09-19T02:44:00Z'
    deadline_at: '2026-09-19T06:42:00Z'
    expected_output: >-
      Covering receipts under agenda-038, covering-values rows for every finished
      probe, and a T-028 landing only if the gate accepts.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-ledger check &&
      uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      Stop new probes at 06:42Z. Do not --search. Do not close think-qqzs,
      think-g3j7, think-gyzw, or think-jwb1. Do not land a non-retainable freeze.
    fallback: Keep the survey, the finished covering rows, and an unresolved exp-162.
    outcome: >-
      T-028 retained s(18) >= 187/40. First-wave and leftover n=19, n=17, n=20,
      and n=12 finished without an H-218 retain. Leftover n=18 and second-wave
      did not start.
    evidence:
      - packing/cases/n18_fractional_certificate/certificate.json
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/leftover-side-ranking.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n12-3969-1000-t017-grid4-windows7-receipt.md
    stop_reason: Research wall 06:42Z. Leftover n=12 exited with remain -4 s.
    next_action: Closeout under phase 3. Do not close think-qqzs.
  - workflow: review-planning-oversight
    focus: process
    recording: contemporaneous
    clock_role: finalization
    bead: think-8x4t
    objective: >-
      Terminalize this session, mark exp-162 abandoned, regenerate the campaign
      views, and leave a reviewable stacked PR.
    status: stopped
    entered_by: planned_checkpoint
    switch_reason: >-
      Research wall 06:42Z. Leftover n=12 finished above 12. No pending retain.
    budget_minutes: 20
    started_at: '2026-09-19T06:42:00Z'
    deadline_at: '2026-09-19T07:02:00Z'
    expected_output: >-
      Terminal session-140, exp-162 abandoned without a lease, leftover n=12
      row recorded, regenerated ledger and session-close report.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-ledger check &&
      uv run --frozen --all-extras --group dev packing-validate --records &&
      uv run --frozen --all-extras --group dev python -m devtools.close_session --check
    kill_condition: >-
      Stop at 07:02Z even if a generated view is stale. Do not --search. Do not
      close think-qqzs, think-g3j7, think-gyzw, or think-jwb1.
    fallback: Leave the records uncommitted with the failing check named.
    outcome: >-
      Session stopped at 06:53:00Z. T-028 stands. exp-162 is abandoned; H-218
      is unconfirmed. Leftover n=18 and second-wave did not start. Native
      harness usage is unmeasured.
    evidence:
      - packing/campaign/agent-sessions/session-140-lb-survey.md
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-162-h218-stock-colgen-small-n-floors.md
      - packing/cases/n18_fractional_certificate/certificate.json
    stop_reason: >-
      Research wall passed, leftover queue stopped, and the closeout records
      are written.
    next_action: Continue H-216 under think-qqzs.
  budget:
    wall_minutes: 260
    max_cycles: 3
    orientation_minutes: 20
    checkpoint_minutes: 60
    slice_minutes: 40
    finalization_minutes: 20
  stop_conditions:
  - Close by 2026-09-19T07:02:00Z with records and a reviewable stacked PR.
  - Do not close think-qqzs, think-g3j7, think-gyzw, or think-jwb1.
  - Do not allocate exp-161 to this session; do not --search.
  - Do not mutate T-025 or T-026 verify_claim.py.
  - Do not change accept rules, thresholds, or metrics.
  - packing-campaign numeric unattended remains NO-GO.
  - T-028 only if decide_certificate prints RETAINABLE.
  - n=11 stays T-026; H-216 is not an n=11 result.
  progress:
    metric: >-
      Open n<=100 floors ranked, and first-wave covering rows recorded; a verified
      floor moves only on RETAINABLE
    before: >-
      Session-139 closed with T-027 at n=18. Covering register has rows at n=6, 11,
      12, 17, 18, 19, 20, 21. No n<=100 survey. T-028 not landed.
    after: >-
      T-028 retained s(18) >= 187/40. H-218 unconfirmed: leftover n=20 971/200
      stopped at 19.910044 unconverged below 20; leftover n=12 3969/1000 stopped
      at 12.091168 after crossing 12. Covering unique sides 33. Leftover n=18
      and second-wave did not start. think-qqzs stays the selected next entry.
  delegations:
  - task: Extract n<=100 verified gaps and covering surplus
    operator: session-140 coordinator
    status: completed
    recording: contemporaneous
    outcome: >-
      32 proved, 68 open. First-wave ranks n=20 at 973/200, n=12 at 397/100, n=17 at
      23/5, n=19 at 481/100.
    evidence:
      - packing/campaign/explorations/X-038-n100-lower-bound-survey.md
    files:
      - packing/campaign/explorations/X-038-n100-lower-bound-survey.md
    checks:
      - >-
        uv run --frozen python extract of frontier n-001..n-100 verified bounds
        against covering-values.yaml
    uncertainty: >-
      Reported uppers (n=17 at 4.675) are not verified ceilings and do not decide
      the remaining window.
    elapsed_seconds: 480
    elapsed_quality: operator_reported_approximate
    next_action: Run rank 1.
    phase: 1
    budget_minutes: 15
    started_at: '2026-09-19T02:42:00Z'
    deadline_at: '2026-09-19T02:57:00Z'
  - task: n=20 973/200 four-grid plus windows 7
    operator: session-140 covering lane
    status: completed
    recording: contemporaneous
    outcome: >-
      Unconverged 19.930198 after 34 LP rounds, 492 still violated, no crossing.
      Not a freeze. T-021 unchanged.
    evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-973-200-t021-grid4-windows7-receipt.md
    files:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-973-200-t021-grid4-windows7-run.json
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-973-200-t021-grid4-windows7-receipt.md
    checks:
      - run JSON objective 19.930197728018545; no freeze file
    uncertainty: >-
      Remaining rows can only raise the restricted optimum, so this is not a
      covering below 20.
    elapsed_seconds: 1212
    elapsed_quality: platform_measured
    next_action: Leave think-d2ad open for a longer wall or denser set.
    phase: 2
    budget_minutes: 40
    started_at: '2026-09-19T02:45:23Z'
    deadline_at: '2026-09-19T03:05:23Z'
    expected_output: >-
      agenda-038 n=20 973/200 four-grid plus windows 7 run JSON, log, and a receipt
      if the loop stops.
    validation_command: >-
      test -f packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-973-200-t021-grid4-windows7-run.json
    kill_condition: Stop at 1200 s or when the row loop converges.
    fallback: Record the restricted optimum and take rank 2.
    write_scope:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/
    excluded_commands:
      - packing-campaign
  - task: n=12 397/100 four-grid plus windows 7
    operator: session-140 covering lane
    status: completed
    recording: contemporaneous
    outcome: >-
      Converged 12.133391; freeze mass 48534459/4000000. Site set refuted. No
      retain.
    evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n12-397-100-t017-grid4-windows7-receipt.md
    files:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n12-397-100-t017-grid4-windows7-run.json
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n12-397-100-t017-grid4-windows7-receipt.md
    checks:
      - run JSON converged true; total_mass 48534459/4000000; decide_certificate not run
    uncertainty: Adding sites can still lower the covering value at 397/100.
    elapsed_seconds: 1079
    elapsed_quality: platform_measured
    next_action: Leave think-h02v open for a different site set; n=17 is next.
    phase: 2
    budget_minutes: 40
    started_at: '2026-09-19T03:06:01Z'
    deadline_at: '2026-09-19T03:26:01Z'
    expected_output: >-
      agenda-038 n=12 397/100 four-grid plus windows 7 run JSON and a receipt
      if the loop stops.
    validation_command: >-
      test -f packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n12-397-100-t017-grid4-windows7-run.json
    kill_condition: Stop at 1200 s or when the row loop converges.
    fallback: Record the restricted optimum and take rank 3.
    write_scope:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/
    excluded_commands:
      - packing-campaign
  - task: n=17 23/5 four-grid plus windows 8
    operator: session-140 covering lane
    status: completed
    recording: contemporaneous
    outcome: >-
      Unconverged 17.120106 after 46 LP rounds, 237 still violated, crossed 17 at
      round 19. Worse than session-139 windows 5 at 17.042346. No freeze. T-019
      unchanged.
    evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n17-23-5-t019-grid4-windows8-receipt.md
    files:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n17-23-5-t019-grid4-windows8-run.json
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n17-23-5-t019-grid4-windows8-receipt.md
    checks:
      - run JSON objective 17.12010567113054; no freeze file
    uncertainty: >-
      Remaining rows can only raise the restricted optimum, so this is not a
      covering below 17.
    elapsed_seconds: 1216
    elapsed_quality: platform_measured
    next_action: Leave think-5q81 open for a different site set; n=19 is next.
    phase: 2
    budget_minutes: 40
    started_at: '2026-09-19T03:24:40Z'
    deadline_at: '2026-09-19T03:44:40Z'
    expected_output: >-
      agenda-038 n=17 23/5 four-grid plus windows 8 run JSON and a receipt if
      the loop stops.
    validation_command: >-
      test -f packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n17-23-5-t019-grid4-windows8-run.json
    kill_condition: Stop at 1200 s or when the row loop converges.
    fallback: Record the restricted optimum and take rank 4.
    write_scope:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/
    excluded_commands:
      - packing-campaign
  - task: n=19 481/100 T-020 auto plus windows 6
    operator: session-140 covering lane
    status: completed
    recording: contemporaneous
    outcome: >-
      Unconverged 19.132115 after 37 LP rounds, 333 still violated, crossed 19 at
      round 16. Closer than 97/20 at 19.808958. No freeze. T-020 unchanged.
    evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n19-481-100-t020-auto-windows6-receipt.md
    files:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n19-481-100-t020-auto-windows6-run.json
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n19-481-100-t020-auto-windows6-receipt.md
    checks:
      - run JSON objective 19.132114728968762; no freeze file
    uncertainty: >-
      Remaining rows can only raise the restricted optimum, so this is not a
      covering below 19.
    elapsed_seconds: 1227
    elapsed_quality: platform_measured
    next_action: Leave think-zoq4 open for more wall or 97/20; n=18 is next.
    phase: 2
    budget_minutes: 40
    started_at: '2026-09-19T03:44:56Z'
    deadline_at: '2026-09-19T04:04:56Z'
    expected_output: >-
      agenda-038 n=19 481/100 T-020 auto plus windows 6 run JSON and a receipt if
      the loop stops.
    validation_command: >-
      test -f packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n19-481-100-t020-auto-windows6-run.json
    kill_condition: Stop at 1200 s or when the row loop converges.
    fallback: Record the restricted optimum and take rank 5.
    write_scope:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/
    excluded_commands:
      - packing-campaign
  - task: n=18 4675/1000 T-027 auto plus windows 5
    operator: session-140 covering lane
    status: completed
    recording: contemporaneous
    outcome: >-
      Converged 17.879034; freeze mass 35758287/2000000. decide_certificate
      printed RETAINABLE. T-028 lands s(18) >= 187/40. Does not confirm H-218.
    evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n18-4675-1000-t027-auto-windows5-receipt.md
    files:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n18-4675-1000-t027-auto-windows5-run.json
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n18-4675-1000-t027-auto-windows5-receipt.md
      - packing/cases/n18_fractional_certificate/certificate.json
    checks:
      - run JSON converged true; total_mass 35758287/2000000; decide_certificate RETAINABLE
    uncertainty: n=18 is off the H-218 sweep.
    elapsed_seconds: 320
    elapsed_quality: platform_measured
    next_action: Land T-028; start the n=20 2400 s follow-up.
    phase: 2
    budget_minutes: 40
    started_at: '2026-09-19T04:05:23Z'
    deadline_at: '2026-09-19T04:25:23Z'
    expected_output: >-
      agenda-038 n=18 4675/1000 T-027 auto plus windows 5 run JSON and a receipt
      if the loop stops.
    validation_command: >-
      test -f packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n18-4675-1000-t027-auto-windows5-run.json
    kill_condition: Stop at 1200 s or when the row loop converges.
    fallback: Record the restricted optimum and take the n=20 longer wall.
    write_scope:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/
    excluded_commands:
      - packing-campaign
  - task: Land T-028 n=18 187/40
    operator: session-140 coordinator
    status: completed
    recording: contemporaneous
    outcome: >-
      T-028 retained s(18) >= 187/40 = 4.675 at V4/C4/S3. T-027 bytes moved to
      certificate-467-100.json. H-218 remains unconfirmed.
    evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n18-4675-1000-t027-auto-windows5-receipt.md
      - packing/frontier/results.yaml
    files:
      - packing/cases/n18_fractional_certificate/certificate.json
      - packing/cases/n18_fractional_certificate/certificate-187-40.json
      - packing/cases/n18_fractional_certificate/certificate-467-100.json
    checks:
      - decide_certificate RETAINABLE; sha256 9507659fa55a48869f060bff07e8d0e4f088cf70320f571afdca1bb460d9bb7b
    uncertainty: C5 is not claimed; no mapped review.
    elapsed_seconds: 1800
    elapsed_quality: platform_measured
    next_action: Leave think-8ujs closable; keep the n=20 2400 s probe running.
    phase: 2
    budget_minutes: 40
    started_at: '2026-09-19T04:13:00Z'
    deadline_at: '2026-09-19T04:53:00Z'
    expected_output: >-
      T-028 in results.yaml, n-018.md verified_lower 187/40, covering-values row
      with frozen_artifact on the live n=18 certificate.
    validation_command: >-
      test -f packing/cases/n18_fractional_certificate/certificate-187-40.json
    kill_condition: Do not land unless decide_certificate printed RETAINABLE.
    fallback: Keep the freeze under agenda-038 and do not mint a T-id.
    write_scope:
      - packing/cases/n18_fractional_certificate/
      - packing/frontier/
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/
    excluded_commands:
      - packing-campaign
  - task: n=20 973/200 four-grid plus windows 7, 2400 s
    operator: session-140 covering lane
    status: completed
    recording: contemporaneous
    outcome: >-
      Unconverged 19.939212 after 45 LP rounds, 255 still violated, no crossing.
      Same site set as the 1200 s run; more wall raised 19.930198 to 19.939212.
      Not a freeze. T-021 unchanged. H-218 unconfirmed.
    evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-973-200-t021-grid4-windows7-2400-receipt.md
    files:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-973-200-t021-grid4-windows7-2400-run.json
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-973-200-t021-grid4-windows7-2400-receipt.md
    checks:
      - run JSON objective 19.93921181902003; no freeze file
    uncertainty: >-
      Remaining rows can only raise the restricted optimum, so this is not a
      covering below 20.
    elapsed_seconds: 2535
    elapsed_quality: platform_measured
    next_action: Leave think-d2ad open for leftover 971/200; n=21 is next.
    phase: 2
    budget_minutes: 50
    started_at: '2026-09-19T04:15:36Z'
    deadline_at: '2026-09-19T05:05:36Z'
    expected_output: >-
      agenda-038 n=20 973/200 four-grid plus windows 7 2400 s run JSON and a
      receipt if the loop stops.
    validation_command: >-
      test -f packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-973-200-t021-grid4-windows7-2400-run.json
    kill_condition: Stop at 2400 s or when the row loop converges.
    fallback: Record the restricted optimum and take n=21.
    write_scope:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/
    excluded_commands:
      - packing-campaign
  - task: n=21 97/20 T-021 auto plus windows 6
    operator: session-140 covering lane
    status: completed
    recording: contemporaneous
    outcome: >-
      Unconverged 19.814820 after 45 LP rounds, 162 still violated, flat from
      round 39. No crossing of 21. Same side as T-021; not a floor raise.
    evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n21-97-20-t021-auto-windows6-receipt.md
    files:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n21-97-20-t021-auto-windows6-run.json
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n21-97-20-t021-auto-windows6-receipt.md
    checks:
      - run JSON objective 19.81481978286421; no freeze file
    uncertainty: >-
      Remaining rows can only raise the restricted optimum. Adding sites can
      still lower it.
    elapsed_seconds: 1228
    elapsed_quality: platform_measured
    next_action: Start leftover-queue.yaml.
    phase: 2
    budget_minutes: 25
    started_at: '2026-09-19T04:57:51Z'
    deadline_at: '2026-09-19T05:22:51Z'
    expected_output: >-
      agenda-038 n=21 97/20 T-021 auto plus windows 6 run JSON and a receipt if
      the loop stops.
    validation_command: >-
      test -f packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n21-97-20-t021-auto-windows6-run.json
    kill_condition: Stop at 1200 s or when the row loop converges.
    fallback: Record the restricted optimum and start leftover-queue.yaml.
    write_scope:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/
    excluded_commands:
      - packing-campaign
  - task: leftover n=19 241/50 T-020 auto plus windows 6
    operator: session-140 covering lane
    status: completed
    recording: contemporaneous
    outcome: >-
      Unconverged 19.247109 after 38 LP rounds, 291 still violated. Crossed 19 at
      round 12 (19.011201). Farther than 481/100 at 19.132115. No freeze. T-020
      unchanged. T-029 not offered. H-218 unconfirmed.
    evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n19-241-50-t020-auto-windows6-receipt.md
    files:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n19-241-50-t020-auto-windows6-run.json
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n19-241-50-t020-auto-windows6-receipt.md
    checks:
      - run JSON objective 19.247108839615727; no freeze file
    uncertainty: >-
      Remaining rows can only raise the restricted optimum, so this is not a
      covering below 19.
    elapsed_seconds: 1259
    elapsed_quality: platform_measured
    next_action: Leave think-zoq4 open for a different site set; leftover n=17 is next.
    phase: 2
    budget_minutes: 25
    started_at: '2026-09-19T05:18:51Z'
    deadline_at: '2026-09-19T05:43:51Z'
    expected_output: >-
      agenda-038 n=19 241/50 T-020 auto plus windows 6 run JSON and a receipt if
      the loop stops.
    validation_command: >-
      test -f packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n19-241-50-t020-auto-windows6-run.json
    kill_condition: Stop at 1200 s or when the row loop converges.
    fallback: Record the restricted optimum and take leftover n=17 461/100.
    write_scope:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/
    excluded_commands:
      - packing-campaign
  - task: leftover n=17 461/100 T-019 auto plus windows 5
    operator: session-140 covering lane
    status: completed
    recording: contemporaneous
    outcome: >-
      Unconverged 17.195968 after 56 LP rounds, 18 still violated. Crossed 17 at
      round 11 (17.030928). Sat on 17.195968 from round 45. No freeze. T-019
      unchanged. T-029 not offered. H-218 unconfirmed. New covering side 4.61.
    evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n17-461-100-t019-auto-windows5-receipt.md
    files:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n17-461-100-t019-auto-windows5-run.json
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n17-461-100-t019-auto-windows5-receipt.md
    checks:
      - run JSON objective 17.19596785593193; no freeze file
    uncertainty: >-
      Remaining rows can only raise the restricted optimum, so this is not a
      covering below 17.
    elapsed_seconds: 1238
    elapsed_quality: platform_measured
    next_action: Leave think-5q81 open for a different site set; leftover n=20 is next.
    phase: 2
    budget_minutes: 25
    started_at: '2026-09-19T05:39:51Z'
    deadline_at: '2026-09-19T06:04:51Z'
    expected_output: >-
      agenda-038 n=17 461/100 T-019 auto plus windows 5 run JSON and a receipt if
      the loop stops.
    validation_command: >-
      test -f packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n17-461-100-t019-auto-windows5-run.json
    kill_condition: Stop at 1200 s or when the row loop converges.
    fallback: Record the restricted optimum and take leftover n=20 971/200.
    write_scope:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/
    excluded_commands:
      - packing-campaign
  - task: leftover n=20 971/200 T-021 auto plus windows 6
    operator: session-140 covering lane
    status: completed
    recording: contemporaneous
    outcome: >-
      Unconverged 19.910044 after 48 LP rounds, 6 still violated. Sat on
      19.910044 from round 40. Did not cross 20. No freeze. T-021 unchanged.
      T-029 not offered. H-218 unconfirmed. New covering side 4.855.
    evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-971-200-t021-auto-windows6-receipt.md
    files:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-971-200-t021-auto-windows6-run.json
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-971-200-t021-auto-windows6-receipt.md
    checks:
      - run JSON objective 19.91004422499408; no freeze file
    uncertainty: >-
      Remaining rows can only raise the restricted optimum, so this is not a
      covering below 20.
    elapsed_seconds: 1243
    elapsed_quality: platform_measured
    next_action: Leave think-d2ad open for a different site set; leftover n=12 is next.
    phase: 2
    budget_minutes: 25
    started_at: '2026-09-19T06:00:29Z'
    deadline_at: '2026-09-19T06:25:29Z'
    expected_output: >-
      agenda-038 n=20 971/200 T-021 auto plus windows 6 run JSON and a receipt if
      the loop stops.
    validation_command: >-
      test -f packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-971-200-t021-auto-windows6-run.json
    kill_condition: Stop at 1200 s or when the row loop converges.
    fallback: Record the restricted optimum and take leftover n=12 3969/1000.
    write_scope:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/
    excluded_commands:
      - packing-campaign
  - task: leftover n=12 3969/1000 T-017 four-grid plus windows 7
    operator: session-140 covering lane
    status: completed
    recording: contemporaneous
    outcome: >-
      Unconverged 12.091168 after 36 LP rounds, 54 still violated. Crossed 12
      at round 11 (12.000732). Lower than the no-windows four-grid 12.116115.
      No freeze. T-017 unchanged. T-029 not offered. H-218 unconfirmed.
      Leftover n=18 did not start (remain -4 s).
    evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n12-3969-1000-t017-grid4-windows7-receipt.md
    files:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n12-3969-1000-t017-grid4-windows7-run.json
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n12-3969-1000-t017-grid4-windows7-receipt.md
    checks:
      - run JSON objective 12.091167832966642; no freeze file
    uncertainty: >-
      Remaining rows can only raise the restricted optimum, so this is not a
      covering below 12.
    elapsed_seconds: 1252
    elapsed_quality: platform_measured
    next_action: Leave think-h02v open for a different site set. Closeout is next.
    phase: 2
    budget_minutes: 21
    started_at: '2026-09-19T06:21:12Z'
    deadline_at: '2026-09-19T06:42:00Z'
    expected_output: >-
      agenda-038 n=12 3969/1000 T-017 four-grid plus windows 7 run JSON and a
      receipt if the loop stops.
    validation_command: >-
      test -f packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n12-3969-1000-t017-grid4-windows7-run.json
    kill_condition: Stop at 1200 s, at 06:42Z, or when the row loop converges.
    fallback: Record the restricted optimum. Start leftover n=18 only if remain is at least 60 s.
    write_scope:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/
    excluded_commands:
      - packing-campaign
  outputs:
  - packing/campaign/explorations/X-038-n100-lower-bound-survey.md
  - packing/campaign/hypotheses/H-218-existing-colgen-raises-a-small-n-floor.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-162-h218-stock-colgen-small-n-floors.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-973-200-t021-grid4-windows7-receipt.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n12-397-100-t017-grid4-windows7-receipt.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n17-23-5-t019-grid4-windows8-receipt.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n19-481-100-t020-auto-windows6-receipt.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n18-4675-1000-t027-auto-windows5-receipt.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/leftover-side-ranking.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-973-200-t021-grid4-windows7-2400-receipt.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n21-97-20-t021-auto-windows6-receipt.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n19-241-50-t020-auto-windows6-receipt.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n17-461-100-t019-auto-windows5-receipt.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n20-971-200-t021-auto-windows6-receipt.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/n12-3969-1000-t017-grid4-windows7-receipt.md
  checks:
  - Planning artifacts written; research phase closed at 06:42Z.
  - >-
    full gate: fast at 9748caa255eed7e432d0ac25340b503a0a7c7e24: passed (GitHub
    Actions packing-required success on the leftover n=17 docs head)
  - >-
    n=20 973/200 four-grid plus windows 7 stopped at 19.939212 unconverged after
    2400 s, no freeze. n=12 397/100 converged at 12.133391, freeze above 12, no
    retain. n=17 23/5 four-grid plus windows 8 stopped at 17.120106 unconverged,
    no freeze. n=19 481/100 T-020 auto plus windows 6 stopped at 19.132115
    unconverged, no freeze; new covering side 4.81. n=18 4675/1000 converged
    17.879034, freeze mass 35758287/2000000, RETAINABLE; T-028 lands 187/40.
    n=21 97/20 stopped at 19.814820 unconverged. Leftover n=19 241/50 stopped at
    19.247109 unconverged, new covering side 4.82. Leftover n=17 461/100 stopped
    at 17.195968 unconverged, new covering side 4.61. Leftover n=20 971/200
    stopped at 19.910044 unconverged, still below 20, new covering side 4.855.
    Leftover n=12 3969/1000 stopped at 12.091168 unconverged after crossing 12.
    Leftover n=18 and second-wave did not start. H-218 unconfirmed.
  stop_reason: >-
    Research wall 06:42Z. T-028 is retained. exp-162 is abandoned. Native
    harness usage is unmeasured.
  next_action: Continue H-216 under think-qqzs.
---
# Session 140: N<=100 Lower-Bound Survey

Workflow entry: **W10 planning, then a research loop**. This record is the closed
four-hour stacked PR. The latest terminal handoff remains
[session-139](session-139-n11-overnight-research.md); its selected next entry is still
`think-qqzs`. This session does not close that bead.

Branch: `cursor/lb-survey-stacked-f02a`, stacked on `cursor/n11-overnight-8h-f02a`.

## Block schedule

| Block | Window (UTC) | Kind | Work |
| --- | --- | --- | --- |
| 0 | 02:42–03:02 | W10 | X-038, H-218, exp-162, beads, stacked PR |
| 1–6 | 02:50–06:42 | research loop | Ranked covering queue, 40-minute slices |
| 7 | 06:42–07:02 | W10 closeout | Freeze-then-decide any pending retain, render, reviewable PR |

Hourly watchdog: `lb-survey-hourly`. Closeout timer: `lb-survey-4h-closeout`.

## Hard constraints

- Project Python 3.14 via `uv run --frozen` from `packing/` only.
- Do not close `think-qqzs`, `think-g3j7`, `think-gyzw`, or `think-jwb1`.
- `exp-161` is not this session.
  Do not `--search`.
- Do not mutate T-025/T-026 `verify_claim.py`.
- `packing-campaign` numeric unattended is NO-GO.
- T-028 only if `decide_certificate` prints `RETAINABLE`.
- n=11 stays T-026. H-216 is not an n=11 result.

## Ranked queue

See [X-038](../explorations/X-038-n100-lower-bound-survey.md).
First probe: n=20 at `973/200` with the T-021 seed, a four-grid, and windows 7.

## T-029 recipe if the 2400 s n=20 freeze is RETAINABLE

n=20 is on the H-218 sweep.
Confirm H-218 only if `decide_certificate` prints `RETAINABLE` at `973/200`. Copy the
T-021 landing, not a new case class.

- Copy live `cases/n20_fractional_certificate/certificate.json` to
  `certificate-97-20.json` before replacing the pointer.
  There is no named 97/20 file today.
- Live plus `certificate-973-200.json` hold the new bytes.
- Do not overwrite `certificate-24-5.json`.
- `produced_by.session` is `session-140`. Score S3.
- If freeze mass is in `[19, 20)`, the claim is `s(20) >= 973/200` and
  `s(21) >= 973/200`. T-020 still holds n=19.
- DS7 hardcodes n=21 verified `4.85`; that line moves with the pointer.
- `4.865` is already a covering unique side.
- Next T-id is T-029. Do not mint it on an unconverged or above-20 freeze.

## Leftover ranking

See
[leftover-side-ranking.md](../series/series-000-smoke-and-calibration/results/agenda-038/leftover-side-ranking.md).
A restricted optimum already above `n` cannot retain on more wall of the same site set.
After n=21, walk `leftover-queue.yaml`: n=19 `241/50` (done, `19.247109`), n=17
`461/100` (done, `17.195968`), n=20 `971/200` (done, `19.910044`), n=12
`3969/1000` four-grid plus windows 7 (done, `12.091168`), n=18 `1871/400`
(not started).

## T-029 leftover recipes

T-029 is still free. Confirm H-218 only on `RETAINABLE` at n in `{12, 17, 19, 20}`.

- Leftover n=19 `241/50` did not retain. Do not mint T-029 from that probe.
- Leftover n=17 `461/100` did not retain. Do not mint T-029 from that probe.
- Leftover n=20 `971/200` did not retain. Do not mint T-029 from that probe.
- Leftover n=12 `3969/1000` did not retain. Do not mint T-029 from that probe.
- Leftover n=18 `1871/400` is off the H-218 sweep. A retain there is the next T-id
  and does not confirm H-218.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
