---
title: session-139 — n11 overnight research
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-139
  title: N11 Overnight Research
  date: '2026-09-18'
  started_at: '2026-09-18T05:33:00Z'
  deadline_at: '2026-09-18T18:40:00Z'
  ended_at: '2026-09-18T18:17:33Z'
  branch: cursor/n11-overnight-8h-f02a
  primary_bead: think-mcb6
  status: stopped
  goal: >-
    Make significant progress on unresolved small-n questions, especially n=11: register
    and then test Route S (H-163 / exp-161), close or tightly bound the H-216 n=6
    calibration, and land the think-g3j7 relational reader that unblocks Route F1.
  resource_usage_unmeasured:
    reason: native_harness_data_unavailable
    detail: >-
      This Cursor cloud-agent run has no ClaudeEfficiencyRollup or CodexTaskTreeDelta
      receipt. Session clocks and the encode and covering walls are not a substitute.
    disposition_bead: think-mcb6
    handoff_role: work_handoff
  workflow_phases:
  - workflow: research-loop
    focus: insight
    recording: contemporaneous
    clock_role: work
    commitment: BC-357
    bead: think-mcb6
    objective: >-
      Freeze this session, register exp-161 for H-163, and dispatch three disjoint
      lanes: H-216 freeze/polish at n=6 299/100, the think-g3j7 new reader, and Route S
      preregistration. H-216 must exit this phase.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 180
    started_at: '2026-09-18T05:33:00Z'
    deadline_at: '2026-09-18T08:33:00Z'
    expected_output: >-
      session-139, exp-161 in-progress with a live lease, an H-216 freeze or ceiling
      family receipt under agenda-037, and a think-g3j7 reader sketch or tests that do
      not touch T-025/T-026 verify_claim.py.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-ledger check &&
      uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      Stop H-216 at this phase deadline even if the bracket is open. Do not start a
      covering LP, packing-campaign numeric run, or Route S optimizer before exp-161
      exists. Do not mutate T-025/T-026 verify_claim.py.
    fallback: >-
      Retain whatever freeze, reader tests, and exp-161 contract exist, then spend
      Block 4 on think-g4n9 and Blocks 5–7 on Route S if exp-161 exists else the reader.
    outcome: >-
      exp-161 registered with a live lease. H-216 two named site sets both covering
      >= 6; freeze retained; H-216 stays open. Relational colgen skeleton landed;
      think-g3j7 stays open. W5 Chromium-early landed ahead of 08:33Z. Covering
      research filled the remaining wall: 26 covering sides, closest n=11 point-atom
      11.018646 at 191/50 with windows.
    evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-161-h163-route-s-threshold-compression.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/h216-n6-299-100-receipt.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/exp-161-block57-command.md
    stop_reason: phase deadline
    next_action: >-
      Blocks 5–7 at 09:33Z run exp-161 encode-only. Covering continues until then.
      Block 8 is closeout. Do not close think-qqzs, think-g3j7, think-gyzw, think-jwb1.
  - workflow: research-loop
    focus: insight
    recording: contemporaneous
    clock_role: work
    commitment: BC-357
    bead: think-mcb6
    objective: >-
      Covering probes until 09:33Z, then exp-161 encode-only for H-163, then
      closeout. Do not treat H-216 as an n=11 result.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: phase 1 deadline; W5 already landed
    budget_minutes: 267
    started_at: '2026-09-18T08:26:00Z'
    deadline_at: '2026-09-18T12:53:00Z'
    expected_output: >-
      Covering register updates, exp-161 encode receipt or unresolved timeout,
      morning report.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-ledger check &&
      uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      Stop at 13:33Z. Do not --search until encode-only exists. Do not close
      think-qqzs, think-g3j7, think-gyzw, or think-jwb1.
    fallback: Retain covering receipts and an unresolved encode.
    outcome: >-
      T-027 retained s(18) >= 467/100. Encode-only started 09:33Z and was still
      running at this phase deadline (timeout 10800; process later measured from
      lstart 12:24:25Z after a clock pause). No encode JSON. No --search. The
      12:53Z waiter cutoff would have skipped the covering queue.
    evidence:
      - packing/cases/n18_fractional_certificate/certificate.json
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-161-h163-route-s-threshold-compression.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/exp-161-block57-command.md
    stop_reason: phase deadline
    next_action: >-
      Owner continue after the missed 12:53/13:33 timers. Leave encode until
      process exit. Then the covering queue. Do not --search.
  - workflow: research-loop
    focus: insight
    recording: contemporaneous
    clock_role: work
    bead: think-mcb6
    objective: >-
      Owner-extended covering after encode exit: n=12 397/100 T-017 four-grid,
      n=17 23/5 windows 6 then 7 if still above 17, n=19 97/20. Copy the encode
      JSON if present. Do not --search. Hand to closeout at 18:00Z.
    status: completed
    entered_by: user_request
    switch_reason: >-
      Owner continue at 15:04Z after the original 12:53Z work deadline and
      13:33Z session deadline. Encode-only still running; covering deferred.
    budget_minutes: 176
    started_at: '2026-09-18T15:04:00Z'
    deadline_at: '2026-09-18T18:00:00Z'
    expected_output: >-
      Encode receipt or unresolved timeout, covering freeze receipts, T-028 only
      if decide_certificate prints RETAINABLE.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-ledger check &&
      uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      Stop new probes at 18:00Z. Do not --search. Do not close think-qqzs,
      think-g3j7, think-gyzw, or think-jwb1.
    fallback: Retain covering receipts and an unresolved encode, then closeout.
    outcome: >-
      Encode-only timed out at 15:24:31Z with no JSON. No --search. Post-encode
      covering finished: n=12 397/100 four-grid 12.122748; n=17 23/5 windows 6
      17.048472 and windows 7 17.046923 (windows 5 remains best at 17.042346);
      n=19 97/20 19.808958. No freeze below n. T-028 not landed. Covering
      register 60 restricted optima at 28 sides. T-027 from phase 2 stands.
    evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-161-h163-route-s-threshold-compression.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/n12-397-100-t017-grid4-receipt.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows6-receipt.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows7-receipt.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/n19-97-20-t020-windows6-receipt.md
    stop_reason: phase deadline
    next_action: >-
      Block 8 closeout. Do not --search. Do not close think-qqzs, think-g3j7,
      think-gyzw, or think-jwb1.
  - workflow: documentation-pass
    focus: process
    recording: contemporaneous
    clock_role: finalization
    bead: think-mcb6
    objective: >-
      Terminalize this session, mark exp-161 unresolved, regenerate the campaign
      views, and run the records check.
    status: stopped
    entered_by: planned_checkpoint
    switch_reason: >-
      Phase 3 covering deadline 18:00Z. Encode timeout unresolved. Covering
      queue empty. T-028 not landed.
    budget_minutes: 40
    started_at: '2026-09-18T18:00:00Z'
    deadline_at: '2026-09-18T18:40:00Z'
    expected_output: >-
      Terminal session-139, exp-161 unresolved without a lease, regenerated
      ledger and session-close report, records-tier pass.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-ledger check &&
      uv run --frozen --all-extras --group dev packing-validate --records &&
      uv run --frozen --all-extras --group dev python -m devtools.close_session --check
    kill_condition: >-
      Stop at 18:40Z even if a generated view is stale. Do not --search. Do not
      close think-qqzs, think-g3j7, think-gyzw, or think-jwb1.
    fallback: Leave the records uncommitted with the failing check named.
    outcome: >-
      Session stopped at 18:17:33Z. exp-161 encode-only timeout is unresolved;
      the lease is dropped. T-027 stands. T-028 was not landed. Native harness
      usage is unmeasured.
    evidence:
      - packing/campaign/agent-sessions/session-139-n11-overnight-research.md
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-161-h163-route-s-threshold-compression.md
      - packing/cases/n18_fractional_certificate/certificate.json
    stop_reason: >-
      Covering deadline passed, encode unresolved, and the closeout records
      are written.
    next_action: >-
      Continue H-216 under think-qqzs. Route S encode-only timed out unresolved.
  budget:
    wall_minutes: 787
    max_cycles: 8
    orientation_minutes: 15
    checkpoint_minutes: 60
    slice_minutes: 180
    finalization_minutes: 40
  stop_conditions:
  - Close by 2026-09-18T18:40:00Z with records, regenerated views, and a morning report.
  - Do not close think-qqzs, think-g3j7, think-gyzw, or think-jwb1.
  - Do not allocate exp-161 to F1 or M7; it is H-163 Route S only.
  - Do not mutate T-025 or T-026 verify_claim.py.
  - Do not change accept rules, thresholds, or metrics.
  - packing-campaign numeric unattended remains NO-GO.
  - H-216 calibration is not a significant n=11 result; cap it at this first phase.
  - Attic scratch is V0/C0 and does not decide a claim.
  progress:
    metric: >-
      Unresolved small-n questions with a retained artifact: exp-161 registered and
      either tested or still leased; H-216 confirmed, refuted, or tightly bracketed
      under both ceiling readers or both decide_certificate routes; think-g3j7 reader
      present without mutating T-025/T-026.
    before: >-
      exp-161 unallocated; H-163 open and untested; H-216 open with only attic scratch
      at n=6 299/100; F1 blocked on a missing reader, sites-1 checkpoint, and guarded
      colgen; PR walls advisory under think-g4n9.
    after: >-
      exp-161 encode-only timed out unresolved (no JSON, no --search); H-163 is
      unresolved on this family and still open for a later encode. H-216 stays
      open: two named n=6 site sets covering >= 6, not an n=11 result.
      think-g3j7 stays open with a relational colgen skeleton. T-027 retained
      s(18) >= 467/100. Covering register 60 restricted optima at 28 sides.
      n=11 stays T-026. T-028 not landed. PR walls remain advisory.
  delegations:
  - task: Register exp-161 for H-163 with source, target, budget, accept, stop, review
      boundary, and evidence paths. Build no optimizer and run no coverage until that
      artifact exists.
    operator: Cursor coordinator Lane C
    status: completed
    recording: contemporaneous
    outcome: >-
      exp-161 is registered with a live lease. The producer is in-tree, live --check
      passed, and the default path is encoding_ready with no candidate. Coverage
      encoding waits for Blocks 5–7; that is not this 90-minute registration slice.
    evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-161-h163-route-s-threshold-compression.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/exp-161-block57-command.md
    files:
      - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-161-h163-route-s-threshold-compression.md
    checks:
      - packing-ledger check (records) after exp-161 registration; live admit_threshold_compression --check exit 0 at 2026-09-18T06:05Z
    uncertainty: >-
      The 181-direction encode may exceed the three-hour scientific wall. Timeout is
      unresolved. Float HiGHS is never an H-163 verdict.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: At 09:33Z run agenda-037/exp-161-block57-command.md encode-only. Do not search until that receipt exists.
    phase: 1
    budget_minutes: 90
    started_at: '2026-09-18T05:33:00Z'
    deadline_at: '2026-09-18T07:03:00Z'
    expected_output: >-
      packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-161-h163-route-s-threshold-compression.md
      with a live lease and verdict in-progress.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-ledger check
    kill_condition: >-
      Stop before writing a candidate, running coverage, or allocating this id to H-216
      or H-217.
    fallback: Keep H-163 open and untested rather than invent a target.
    write_scope:
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-161-h163-route-s-threshold-compression.md
    - packing/campaign/hypotheses/H-163-route-s-threshold-compression.md
    - packing/campaign/agendas/agenda-036-n11-strategy-reset-roadmap.md
    - packing/campaign/ideas.md
    - packing/campaign/explorations/X-032-route-s-threshold-compression.md
    excluded_commands:
    - packing-campaign run
    - optimizer
    - coverage target
    - candidate generation
  - task: Freeze and polish a helper-free point family at n=6, side 299/100, B=9977/10000,
      181-net, and hand it to both ceiling readers or both decide_certificate routes.
    operator: Cursor Lane A H-216
    status: completed
    recording: contemporaneous
    outcome: >-
      Two named site sets at n=6 299/100 both covering >= 6 (6.08216 and 6.07724).
      Polished family 76/13 fails K3 and does not kill. H-216 stays open. Not an
      n=11 result.
    evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/h216-n6-299-100-receipt.md
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/h216-n6-299-100-sites2-receipt.md
    files:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/h216-n6-299-100-covering.json
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/h216-n6-299-100-sites2-covering.json
    checks:
      - packing-ledger check after freeze receipts
      - both site sets covering >= 6; polished 76/13 K3 fail recorded
    uncertainty: >-
      X-037 attic numbers [83/14, 6.006571] are V0/C0. A float LP or incomplete row set
      decides neither direction.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Leave H-216 open. Do not chase further this session. Not an n=11 result.
    phase: 1
    budget_minutes: 180
    started_at: '2026-09-18T05:33:00Z'
    deadline_at: '2026-09-18T08:33:00Z'
    expected_output: >-
      A named freeze or polished ceiling-family JSON under
      packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/
      plus a two-reader or two-route decision, or a recorded stall.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev python -m
      devtools.independent_ceiling_reader --help && uv run --frozen --all-extras
      --group dev python -m devtools.decide_certificate --help
    kill_condition: >-
      Exit at 08:33Z even if undecided. Do not treat a decided H-216 as an n=11 result.
      Do not allocate exp-161.
    fallback: Keep the freeze receipt and the exact bracket; leave H-216 open.
    write_scope:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/
    excluded_commands:
    - packing-campaign run
    - optimizer
    - python3
  - task: Land a new relational-certificate reader for weighted-majority, k-of-S, and
      floor atoms without mutating T-025/T-026 verify_claim.py.
    operator: Cursor Lane B F1 reader
    status: completed
    recording: contemporaneous
    outcome: >-
      Relational colgen skeleton landed. Full production reader for think-g3j7 is
      still open. T-025/T-026 verify_claim.py were not mutated.
    evidence:
      - packing/src/sqpack/fractional/relational.py
      - packing/devtools/run_relational_colgen.py
    files:
      - packing/src/sqpack/fractional/relational.py
      - packing/devtools/decide_relational_certificate.py
    checks:
      - pytest tests/test_run_relational_colgen.py
    next_action: Leave think-g3j7 open. Do not mutate T-025/T-026 verify_claim.py.
    uncertainty: >-
      think-h1ju and think-k1pe passed a private review whose candidate lived under
      /private/tmp/n11-floor-atom-prep, which is not in this checkout. Production
      adoption still has to happen in-tree.
    elapsed_seconds: null
    elapsed_quality: unavailable
    phase: 1
    budget_minutes: 180
    started_at: '2026-09-18T05:33:00Z'
    deadline_at: '2026-09-18T08:33:00Z'
    expected_output: >-
      A new reader module and tests covering threshold (S,k,w) compatibility, a 2-of-5
      atom with a four-site core, and floor atoms, without editing
      packing/cases/n11_threshold_certificate/verify_claim.py.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev pytest -q
      tests/test_decide_relational_certificate.py
    kill_condition: >-
      Stop rather than mutate T-025/T-026 verify_claim.py or decide_threshold_certificate.py.
      Do not run a covering LP or sites-1 regeneration until the reader exists.
    fallback: Keep a failing test that states the missing format; leave think-g3j7 open.
    write_scope:
    - packing/src/sqpack/fractional/relational.py
    - packing/devtools/decide_relational_certificate.py
    - packing/tests/test_decide_relational_certificate.py
    excluded_commands:
    - packing-campaign run
    - optimizer
    - coverage target
    - python3
  outputs:
  - packing/campaign/agent-sessions/session-139-n11-overnight-research.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-161-h163-route-s-threshold-compression.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/h216-n6-299-100-covering.json
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/h216-n6-299-100-family-polished.json
  - packing/devtools/compress_threshold_certificate.py
  - packing/src/sqpack/fractional/relational.py
  - packing/cases/n18_fractional_certificate/certificate.json
  - packing/frontier/RESULTS.md
  resource_rollups: []
  checks:
  - Encode-only timed out at 15:24:31Z with no JSON; no --search.
  - T-027 retained s(18) >= 467/100; T-028 was not landed.
  - Covering register has 60 restricted optima at 28 unique sides.
  - packing-ledger check and packing-validate --records passed on 70c73070 before closeout.
  - >-
    full gate: fast at f98ff7811d0b8afe678d8f81ce413c989e0b1d57: passed (GitHub
    Actions run 35371189375; packing-required success on the hour-10 head)
  stop_reason: >-
    The owner-extended covering deadline was 18:00Z. Encode-only timed out
    unresolved. T-027 is retained. T-028 was not landed. Native harness usage
    is unmeasured.
  next_action: >-
    Continue H-216 under think-qqzs. Route S encode-only timed out unresolved;
    a later block re-runs encode before --search.
---
# Session 139: N11 Overnight Research

Workflow entry: **W10 then a W6/W7/W5 mix**. This record is the live eight-hour
overnight. The latest terminal handoff remains
[session-138](session-138-n11-overnight-review.md); its selected next entry is still
`think-qqzs` / BC-357. This session executes that entry in parallel with Route S
registration and the F1 reader, because the owner authorized autonomous overnight work
whose top goal is unresolved questions, especially n=11.

## Block schedule

| Block | Window (UTC) | Kind | Work |
| --- | --- | --- | --- |
| 0 | 05:33–05:50 | W10 freeze | This record, branch `cursor/n11-overnight-8h-f02a`, hourly watchdog, 8h closeout |
| 1–3 | 05:33–08:33 | W6/W7 | Lane A H-216; Lane B `think-g3j7` reader; Lane C exp-161. H-216 exits at 08:33 |
| 4 | 08:33–09:33 | W5 | `think-g4n9` PR-wall ≤180s (OR-12) |
| 5–7 | 09:33–12:53 | W6 | Route S target if exp-161 exists; else continue the F1 reader. No covering LP until reader, sites-1, and guarded colgen exist |
| 8 | 12:53–13:33 | W10 closeout | Morning report, `packing-validate --records`, terminalize this session |

Hourly watchdog: `overnight-priority-check`. Closeout timer: `overnight-8h-closeout`.

## Hard constraints

- Project Python 3.14 via `uv run --frozen` from `packing/` only.
- Do not close `think-qqzs`, `think-g3j7`, `think-gyzw`, or `think-jwb1`.
- `exp-161` is H-163 only.
- Do not mutate T-025/T-026 `verify_claim.py`.
- `packing-campaign` numeric unattended is NO-GO (D-044/D-046; no `runner.command` on
  H-216/H-163).
- A decided H-216 does not move `s(6)=3` and is not an n=11 result.

## Lanes

**A / BC-357 / H-216.** Stock drivers on main:
`run_fractional_colgen --freeze-family --support-cap 0`, `polish_ceiling_family`,
`independent_ceiling_reader`, `verify_ceiling`, `decide_certificate`. Confirm only with
covering < 6 both gate routes; kill only with an exact depth-one family of total ≥ 6
both ceiling readers.

**B / BC-358 tooling.** New reader first (`think-g3j7`). `think-3xbr` and `think-gyzw`
wait on it. k-of-S is already T-025’s `(S,k,w)`; floor atoms are a new class.
A T-id in the new class needs two-route C4.

**C / BC-343 / H-163.** Register `exp-161`, then build the named producer, then a
target. Confirm only at `N+ <= 23`, budget < 11, least charge ≥ 1, both exact routes,
source-distinct replay.
Refute only by exact infeasibility of every `N+ <= 23` family member.
The three admission-control manifests cannot confirm.
Timeout is unresolved, never rejected.

## Hour 1 note (2026-09-18T05:55Z)

H-216 freeze covering total `76027/12500 = 6.08216` does not confirm. Polish then both
ceiling readers: exact total `76/13`, max depth 1, K3 fails. That does not kill.
H-216 stays open; not an n=11 result. exp-161 accept hole closed. Producer is in-tree
and emits no candidate. F1 reader modules are in-tree with the 2-of-5 versus floor
charge test. Hosted typecheck band is now 55.67 s / ceiling 111 s. Head `876dd80f`
is hosted-green (37 checks). A second H-216 site set on grids 18/24/29/34 froze
covering `151931/25000` = 6.07724 (does not confirm).

## Block 4 W5 plan (`think-g4n9`, 08:33Z)

Packing wall pole is **frontend** (6 of the last 8 exact-head successes). Pages
full-build is usually ≤180 s; the newest explainer-in-scope head was 190 s on
print-layout. Both walls stay **advisory**. Do not flip enforcement. Do not add
`suite-c` in this block: a third shard leaves the frontend job at 168–189 s.

Slice: start Chromium early with the existing `_submission_order` / `start_early`
tool, and stop serializing independent Chromium work.

- `packing/src/sqpack/cli/validate.py`: `start_early=True` on workbench Chromium
  behavior (hosted pair 59.09 s / 91.69 s).
- `.github/workflows/packing-validation.yml`: `playwright install --with-deps`
  in parallel with uv/Node after checkout; apt-archive cache like Pages.
- `.github/workflows/pages.yml`: print-layout self-check concurrent with
  `check_print_layout`; typography paper/startup/geometry as concurrent groups.
- Tests: `test_validation_cli.py`, `test_module_boundaries.py`,
  `test_pages_workflow.py`.
- Do not edit `gate-budgets.yaml` in the first commit.

Predicted packing wall ~150 s typical / ~169 s at 1.8× of fast Chromium, still
failing on suite-a slow runners and queue ≥30 s. `suite-c` is the follow-on.
Re-enforcement still needs five consecutive exact-head runs with **both** walls
≤180 s.

Live `admit_threshold_compression --check` passed at 2026-09-18T06:05Z (exit 0).
Coverage on frozen U025 is linear in orbit weights; the producer formulates `A w >= 1`
under `--authorize-target exp-161` and enumerates only with `--encode-coverage`.
Default still emits no candidate. sites-1 regeneration refuses: the 15,021-row matrix
and sepcore/lp383 APIs are unretained (`missing-inputs`).

## Hour 1 watchdog (2026-09-18T06:07Z)

H-216 chase is done for this phase: two named site sets, both covering ≥ 6. Not n=11.
Lane B: `devtools.regenerate_sites1_checkpoint` is in-tree and refuses. Lane C: live
`--check` passed; coverage encoding landed. Next: `think-gyzw` guarded colgen skeleton
(refuses without sites-1), G4 n-parameterised threshold producer, M3 `think-k4vb` kill
test if cheap. Block 4 at 08:33Z is Chromium-early.

## Hour 1 continuation (2026-09-18T06:15Z)

Coverage encoding is ruff-clean and type-clean; 24 tests passed.
Authorized producer default path is on the branch (`encoding_ready`, no candidate).
Three implementation lanes plus a low-n scout are in flight: guarded relational colgen,
G4 n-parameterised threshold producer (in-tree rewrite of the agenda-034 separator, not
a `.py.txt` promotion), and the M3 piercing tool. Do not start another H-216 freeze.
`--encode-coverage` waits for Blocks 5–7.

## Hour 1 scout follow-up (2026-09-18T06:18Z)

H-216 third freeze is not started (phase exit). n=7–9 are proved and have no covering
rows. n=12 grid covering at `3969/1000` converged at `12.363498` (crossed 12 at round 4;
site set refuted; side open). n=11 at `383/100` is next. Guarded
`devtools.run_relational_colgen` refuses covering without sites-1 (`think-gyzw` remains
open).

## Hour 1 n=11 383/100 (2026-09-18T06:32Z)

n=11 auto grids `(25, 34, 41)` at `383/100` converged in 82.2 s at restricted optimum
`11.192598` (rationalised `44770567/4000000`). Crossed eleven at LP round 6. Site set
refuted; side open. T-025 and T-026 unchanged. Next cheap probe: denser grids at the
same side. G4 and M3 sources are on disk, uncommitted until their tests pass.

## Hour 1 four-grid (2026-09-18T06:36Z)

n=11 `--grid-counts 25,34,41,48` at `383/100` converged in 81.7 s at `11.142857`
(rationalised `2228577/200000`). About 2,300 extra sites dropped 0.050 from the auto
grid. Still above eleven. Next: T-025-seeded grids at the same side. G4 and M3 landed.

## Hour 1 T-025 seed (2026-09-18T06:39Z)

Four-grid union T-025 (584 seed sites, 6249 total) converged at `11.140351` in 107.9 s.
Drop from four-grid: 0.0025. Point-atom covering at `383/100` is above eleven on three
named site sets. Next: scout #3, denser grids at `191/50`.

## Hour 1 191/50 four-grid (2026-09-18T06:42Z)

`--grid-counts 26,35,43,48` at `191/50` converged at `11.142857` on 6037 sites. That is
not a superset of the historical 6637-site exact-eleven grid. Next: auto `(25,34,41)`
plus count 60 (6961 sites).

## Hour 1 auto+60 (2026-09-18T06:44Z)

`--grid-counts 25,34,41,60` at `191/50` converged at `11.106195` on 6961 sites. More
sites than the historical exact-eleven grid, worse optimum. Next: T-025-seeded auto+60
at the same side, then M3 selftest.

## Hour 1 T-025 auto+60 (2026-09-18T06:47Z)

T-025-seeded auto+60 at `191/50` converged at `11.020212` after sitting at exactly
eleven through LP round 16. Closest session-139 point construction at 3.82; still not
below eleven. Point-atom densification at 3.82/3.83 is exhausted for this phase. Next:
M3 selftest.

## Hour 1 M3 selftest (2026-09-18T06:48Z)

T-018 5-direction event-cell encoding hit the 20 s limit before HiGHS ran
(`timeout` / `unresolved`). Not a kill. A 36-net search needs a larger encoding budget.
Receipt path is packing-relative. Block 4 W5 remains 08:33Z.

## Hour 1 M3 9-dir (2026-09-18T06:53Z)

`--direction-steps 8` (9 directions) with 180 s also timed out in event-cell encoding
before HiGHS. Encoding is the cost, not the MIP. Do not spend another M3 wall on a
finer net until encoding is cheaper. Point-atom densification at 3.82/3.83 is done
for this phase. Block 4 at 08:33Z.

## Hour 2 (2026-09-18T07:08Z)

Span-sweep encoding landed: covering sets are frozensets, unique rows cap at 4096,
Pareto skipped on wide site sets. T-018 5-direction selftest now finishes in 14.6 s
with HiGHS feasible piercing 9 on 19,072 truncated rows (`unresolved`, not a kill,
not an eleven-candidate). G4 n=11 at 191/50, 9 directions, grids 8/12/16: seed-row
LP dipped to 9.97 after 30 threshold-atom orbits, then two row rounds restored
11.61. Not a freeze. n=17 auto grids at 23/5: unconverged 17.331710 in 315 s, site
set refuted, side open. Blocks 5–7 Route S command is in
`agenda-037/exp-161-block57-command.md` (encode-only first; 181-direction Pareto may
exceed the 3 h wall). G4 follow-up at 17 directions, grids 10/14/18, eight row
rounds: seed-row LP dipped to 9.64, then row rounds finished at 11.45. M3 9-dir
45 s search: piercing 9 on 31,940 truncated rows, still unresolved. Block 4 W5
remains 08:33Z.

## Block 4 W5 Chromium-early (2026-09-18T07:20Z)

Landed ahead of the 08:33Z window. `start_early=True` on workbench Chromium so
`--frontend --jobs 2` submits it before biome and liveness. Frontend install overlaps
`npm ci --ignore-scripts` with Playwright Chromium apt and waits both statuses.
Pages `print-layout` runs `check_print_layout` and `--self-check` at once, same wait
rule. No `gate-budgets.yaml` edit. No wall-enforcement flip. `suite-c` remains the
follow-on. Tests: `test_workbench_chromium_starts_ahead_of_the_other_frontend_steps`,
frontend install overlap in `test_module_boundaries.py`,
`test_print_layout_runs_the_overflow_self_check_beside_the_page`.

## Hour 2 covering probes (2026-09-18T07:33Z)

Three named site sets, none a certificate.

- n=11 at `77/20` (3.85), T-025-seeded auto `(25, 34, 42)` plus 60: converged
  `11.456576` in 196 s on 7705 sites. Crossed eleven at round 2. Site set refuted.
  BC-200's vertex-seeded unconverged `11.227631` at this side is a different set.
- n=12 at `3969/1000`, T-017-seeded auto `(26, 35, 43)`: unconverged `12.118036` at
  600 s (29 LP rounds). Seed dropped the unseeded `12.363498` by 0.245. Still above
  twelve. Site set refuted; side open.
- n=18 at `467/100` (4.67), auto `(32, 43, 53)`: unconverged `18.000000` at 600 s
  (57 LP rounds; locked from round 15). Cannot confirm. Covering-values now 23 sides.

Point-atom covering at 3.82/3.85 stays at or above eleven on every session-139 set.
Blocks 5-7 Route S encode-only remains 09:33Z.

## Hour 2 n=11 31/8 (2026-09-18T07:40Z)

Same T-025-seeded auto-plus-60 construction at `31/8` = 3.875, 0.002 below the
known-best packing. Converged `11.561186` in 234.3 s on 7705 sites. Crossed eleven
at round 2. Site set refuted; side open. Covering-values now 24 sides. Point-atom
grids plus T-025 sites do not capture the packing geometry even this close to it.

## Hour 2 windows and 3.84 (2026-09-18T07:52Z)

`--seed-windows 5` on the T-025-seeded auto-plus-60 set at `191/50` converged
`11.018646` in 176.2 s on 7473 sites (809 seed). Dropped the no-windows
`11.020212` by 0.0016. Closest session-139 point-atom construction; still above
eleven. Same construction at `96/25` = 3.84 converged `11.371819` in 222.9 s.
Restricted opt at 3.82 / 3.83 / 3.84 / 3.85 / 3.875 is monotone up. G4 at
`31/8` net9 dipped to 10.17 on seed rows then restored to 14.00; same overfit,
stop G4. Covering-values now 25 sides. Next: T-026-seeded auto-plus-60 at
191/50 and T-025-seeded auto-plus-60 at 381/100. n=17 T-019 seed still in
flight. Route S encode-only remains 09:33Z.

## Hour 2 n=17 T-019 seed (2026-09-18T07:59Z)

T-019-seeded auto grids at `23/5` stopped unconverged at `17.049597` after 628 s
(40 LP rounds, 183 violated). Seed dropped the unseeded `17.331710` by 0.282.
Site set refuted; side open. T-026 seed at 191/50 and T-025 auto-plus-60 at
381/100 still in flight.

## Hour 3 T-026 seed (2026-09-18T08:03Z)

T-026-fractional-seeded auto-plus-60 at `191/50` converged `11.033743` in
265.4 s on 8081 sites. Worse than T-025 (11.020212) and T-025 plus windows
(11.018646). Site set refuted. 381/100 still sitting at exactly eleven;
n=18 T-019 seed still below 18.

## Hour 3 n=11 381/100 (2026-09-18T08:08Z)

T-025-seeded auto-plus-60 at `381/100` sat at `11.000000` from LP round 7
through the 60-round limit (120 still violated, `least_covered` 0.992). Never
crossed above eleven. Site set refuted, unconverged; new covering side 3.81.
Covering-values now 26 sides. n=18 T-019 seed row loop reached `17.875567`
with violated 0; column generation still running.

## Hour 3 phase-1 exit (2026-09-18T08:33Z)

H-216 exits open: two named site sets covering >= 6, not an n=11 result.
think-g3j7 stays open. W5 already landed. Next is Route S encode-only at
09:33Z. Covering continues: n=18 T-019 seed row loop at 17.875567 with
violated 0, still in column generation; n=12 T-017 four-grid in flight.

## Hour 3 n=12 four-grid (2026-09-18T08:28Z)

T-017-seeded four-grid at `3969/1000` stopped unconverged at `12.116115` after
634.8 s (29 LP rounds, 330 violated). Dropped the seeded auto `12.118036` by
0.002. Site set refuted; side open.

## Hour 3 n=18 T-019 seed (2026-09-18T08:31Z)

T-019-seeded auto grids at `467/100` with `--support-cap 0` converged the row
loop at `17.875567` (`least_covered` 1) on 6853 sites. Unseeded locked at 18.
`check_ceiling` on the untruncated dual was interrupted after 31 minutes.
Freeze re-run started with `--support-cap 32`. First session-139 covering
strictly below n on a named site set.

## Hour 4 T-027 (2026-09-18T08:47Z)

`declare_least_cell_mass` then `decide_certificate` accepted the freeze:
769 atoms, mass `8937839/500000 = 17.875678`, least cell mass `2000007/2000000`,
sha256 `3a11b6303e0663b502b6c1e3fc9d8da285104e199b17022937369bc781479059`.
Landed as `cases/n18_fractional_certificate/` and T-027. Verified
`s(18) >= 467/100 = 4.67`, +0.08 over T-019's 4.59 at n=18. T-019 unchanged at
n=17. n=19 stays 4.80 (T-020). H-216 is not an n=11 result. Route S encode-only
remains 09:33Z. Covering continues at 117/25 (locked 18.000000 on the T-019 seed;
windows in flight) and 469/100.

## Hour 4 covering register (2026-09-18T09:05Z)

T-027 committed (`3461922d`). T-019-seeded auto at `117/25` converged with exact
mass `18000043/1000000 = 18.000043` (float 17.999999999552305) in 180 s; cannot
certify. T-019-seeded auto at `47/10` converged `18.165413` in 390 s; cannot
certify. T-019-seeded auto plus `--seed-windows 5` at n=17 `23/5` stopped
unconverged at `17.042346` after 931.6 s (42 rounds, 9 violated), 0.007 below
the seed without windows. Site sets refuted; sides open. 4.68 windows and 4.69
seed still in flight.

## Hour 4 T-027 seed (2026-09-18T09:10Z)

T-019-seeded auto plus windows at `117/25` locked `18.000000` unconverged after
912.6 s (57 rounds, 495 violated). T-019-seeded auto at `469/100` locked
`18.000000` unconverged after 921.5 s (59 rounds, 288 violated). T-027-seeded
auto at `117/25` started 09:09Z. Route S encode-only remains 09:33Z.

## Hour 4 T-027 seed result (2026-09-18T09:24Z)

T-027-seeded auto at `117/25` locked `18.000000` unconverged after 819.5 s
(60 rounds, 465 violated, 769 seed sites). Same wall as the T-019 seed.
T-027 at `467/100` is unchanged. Route S encode-only remains 09:33Z.

## Hour 4 Blocks 5–7 start (2026-09-18T09:33Z)

Live `admit_threshold_compression --check` and producer `--selftest` both
exited 0 at 09:31:37Z. Encode-only (`--authorize-target exp-161
--encode-coverage`, no `--search`) started 09:33:00Z under `timeout` 10800 in
tmux `exp-161-encode`. Scientific wall 09:33–12:33Z; receipt copy until 12:53Z.
Timeout is unresolved. No covering colgen beside this process.

T-027 `--push` contracts: n=18 DS7 verified bound `4.67`; n=18 interval
doubled-net registered in the exhaustive marker set; Chromium-early is the
first unbudgeted `start_early` step ahead of exact verification.

## Post-encode covering queue (after 12:33Z)

Do not invent an n=17 four-grid. Do not spend another wall on the same
windows5 site set: remaining rows can only raise 17.042346. Do not probe
n=18 at 4.68/4.69 (locked 18 on T-019, windows, and T-027 seeds). Do not
probe n=11 at or below 3.826.

1. n=12 `397/100` T-017 four-grid `(26,35,43,48)`. BC-206 seeded auto crossed
   at 12.016263; session has only `3969/1000` four-grid so far.
2. n=17 `23/5` T-019 auto `(32,42,52)` plus `--seed-windows 6` (CLI
   `per_window`; windows5 was 17.042346 with 9 violated). Then windows 7 if
   windows 6 stays above 17 (adds lattice sites; do not re-run windows 5).
3. If wall remains: n=19 at T-021's recorded `97/20`, seeded from T-020's
   `certificate-24-5.json`, aiming for mass below 19. Not another `24/5`
   covering. Do not invent a new n=19 side.

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 12 --side 397/100 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 26,35,43,48 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 900 \
  --seed-certificate cases/n12_fractional_certificate/certificate.json --seed-map scale \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-037/n12-397-100-t017-grid4-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-037/n12-397-100-t017-grid4-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n12-397-100-t017-grid4-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n12-397-100-t017-grid4-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n12-397-100-t017-grid4.log
```

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 17 --side 23/5 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 32,42,52 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 900 \
  --seed-certificate cases/n17_fractional_certificate/certificate.json --seed-map scale \
  --seed-windows 6 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows6-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows6-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows6-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows6-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows6.log
```

Windows 7 only if windows 6 did not freeze below 17. Same grids, `--seed-windows 7`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 17 --side 23/5 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 32,42,52 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 900 \
  --seed-certificate cases/n17_fractional_certificate/certificate.json --seed-map scale \
  --seed-windows 7 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows7-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows7-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows7-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows7-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows7.log
```

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 19 --side 97/20 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 34,45,56 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 900 \
  --seed-certificate cases/n20_fractional_certificate/certificate-24-5.json --seed-map scale \
  --seed-windows 6 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-037/n19-97-20-t020-windows6-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-037/n19-97-20-t020-windows6-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n19-97-20-t020-windows6-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n19-97-20-t020-windows6-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n19-97-20-t020-windows6.log
```

Grid counts `34,45,56` are BC-197's recorded auto counts at `97/20`
(`bc-197-r2t.json`). T-021 converged at 19.848723 on that grid unioned with
the 24/5 atoms and `seed_windows: 0`; remaining rows raise, so windows 6 is
the site-set change. Seed the immutable `certificate-24-5.json`, not the
moving `certificate.json` pointer (now 97/20). Do not invent a new n=19
side. Do not re-cover `24/5`. Session covering stays on the 181-net.

`--freeze` is on each probe (`--support-cap 32`, never 0). A freeze file
appears only on a converged row loop. If its `total_mass` is below n, run
`declare_least_cell_mass` then `decide_certificate` on those bytes. Do not
`--verify-serial` during colgen. Do not `--search`.

If `decide_certificate` prints RETAINABLE, the next T-id is **T-028**. Do not
use BC-357. `produced_by.session` is `session-139`. Score S3 (same generator;
T-020 calibration). Copy the T-027 landing, not a new case class:

- n=12 `397/100`: add `cases/n12_fractional_certificate/certificate-397-100.json`
  and point `certificate.json` at it. Current verified lower is T-017 `99/25`.
  Keep the 99/25 bytes as a named lower rung.
- n=17 `23/5`: add a named rung under `cases/n17_fractional_certificate/`.
  T-019 `459/100` stays the n=17 bound until mass is below 17 at 23/5.
- n=19 `97/20`: new bytes, not T-021's `certificate.json` (mass 19.848723).
  Seed was `certificate-24-5.json`. T-020 stays until mass is below 19.

Then: receipt, `results.yaml`, `evidence.yaml`, `n-0NN.md` verified lower,
covering-values `frozen_artifact` matching `^packing/cases/.+\.json$`,
`python -m devtools.render_results --update`, `render_certificate_reach`,
`python -m devtools.build_composite_figure_data --update`, DS7/interval
`--push` contracts, `packing-validate --push`. Not during encode.

T-027's `produced_by` is `session: session-139` only (no `agenda_cell`). Copy
that. Do not invent a cell. `certificate.json` at n=12 **is** the 99/25
bytes; there is no `certificate-99-25.json`. Before replacing the live file,
copy it to that name. Same at n=17: live file is 459/100, no
`certificate-459-100.json` yet. n=19 has no case package; create
`cases/n19_fractional_certificate/` on the n=18 pattern. Do not overwrite
`cases/n20_fractional_certificate/certificate.json` (T-021's 97/20, mass
19.848723). `test_fractional_certificate.py` asserts the live n=12 claim is
`s(12) >= 99/25`; that line moves with the pointer. DS7 hardcodes verified
lowers only for n=17 (`4.59`) and n=18 (`4.67`). Covering `side_decimal`
`3.97`, `4.6`, and `4.85` are already in the SYNOPSIS unique-side list.
Map any new receipt Markdown in `document-map.yaml` (T-027's receipt was
mapped when the covering run was recorded). A T-id landing moves the
CURRENT-RESEARCH-STATUS frontier count from 27 to 28; unique covering sides
stay 28 unless a new `side_decimal` appears. Raised `n-0NN.md` bounds must
mark the displaced figure with a historical token (`superseded`,
`previously`, `was`, `until`). `frozen_artifact` must also appear in some
result's `artifacts`.

Sweeps composite-figure.json was regenerated at 09:39Z for n=18 4.67
(`7b9a4deb`). Do not paste the suite-b 74.1s sample into
`gate-budgets.yaml`; that job's tests passed.

## Hour 5 (2026-09-18T09:41Z)

Blocks 5–7. Encode-only still running in tmux `exp-161-encode` (pid 347502,
elapsed 08:41, ~100% CPU, peak RSS 2.45 GiB). No encoding JSON yet; the
producer writes at the end. Log still empty. No `--search`. Covering colgen
stays off this CPU. Post-encode queue is the n=12 `397/100` four-grid then
n=17 windows 6. CI on HEAD is in flight after the composite-figure refresh.

Packing validation on `335e8028` completed success at 09:45Z (suite-a, suite-b,
typecheck, validate, geometry, macos-portability, sweeps, frontend,
packing-required). A waiter in tmux `post-encode-covering` starts that queue
when encode pid 347502 exits, copies the encode JSON, and will not start a
probe inside the Block 8 closeout (12:53Z). No `--search`. The waiter then
runs n=19 `97/20` T-020 windows 6 if wall remains.

## Hour 6 (2026-09-18T10:10Z)

Encode-only still running (pid 347502, elapsed 37:41, ~100% CPU, RSS cycling
0.13–0.98 GiB per direction, peak 2.39 GiB). No JSON. Log empty. No `--search`.
Waiter `post-encode-covering` still waiting on that pid. Queue after encode:
n=12 `397/100` four-grid, n=17 windows 6 then 7 if still above 17, n=19
`97/20` T-020 windows 6; freeze at `--support-cap 32`, declare-then-decide
if mass < n. CI on `9c0156eb` succeeded. Do not land T-028 during encode.

## Hour 7 (2026-09-18T11:08Z)

Encode-only still running (pid 347502, elapsed 1:35:22, ~100% CPU, RSS
cycling 0.13–1.00 GiB per direction, peak 2.45 GiB). No JSON. Log empty. No
`--search`. Waiter still waiting on that pid. Covering queue unchanged. Do
not land T-028 during encode. Scientific wall ends 12:33Z; closeout 12:53Z.

## Late continue (2026-09-18T15:06Z)

Owner continue after the 12:33Z and 13:35Z timers. Encode-only still running
(pid 347502, process elapsed ~2:42 from `lstart` 12:24:25Z, ~18 min left on
timeout 10800). START marker is 09:33Z; the timeout is process-relative after
the clock pause. No JSON. Log empty. No `--search`.

The 12:53Z waiter cutoff is past and would skip every probe. Replaced
`CLOSEOUT_EPOCH` with 18:00Z and restarted tmux `post-encode-covering`. Queue
unchanged: n=12 `397/100` four-grid, n=17 windows 6 then 7 if still above 17,
n=19 `97/20`. Freeze at `--support-cap 32`; declare-then-decide if mass < n.
Closeout after covering. Do not land T-028 during encode.

## Hour 8 (2026-09-18T15:15Z)

Encode-only still running (pid 347502, process elapsed 2:50 from `lstart`
12:24:25Z, ~9 min left on timeout 10800, RSS 1.0 GiB, peak 2.46 GiB). No
JSON. Log empty. No `--search`. Waiter cutoff is 18:00Z. Campaign-record
clocks extended to 18:40Z (`c3d28cfd`). Queue unchanged. Do not land T-028
during encode.

## Encode timeout (2026-09-18T15:24Z)

Encode-only exited at 15:24:31Z with no JSON. Timeout unresolved. Log still
empty. No `--search`. Waiter started n=12 `397/100` T-017 four-grid
(`--support-cap 32`, deadline 900 s). Then n=17 windows 6, windows 7 if
needed, n=19 `97/20`. Covering deadline 18:00Z. Freeze-then-decide if mass
< n. T-028 only if RETAINABLE.

## n=12 397/100 four-grid (2026-09-18T15:40Z)

T-017-seeded four-grid `(26, 35, 43, 48)` at `397/100` stopped unconverged at
`12.122748` after 939.9 s (33 LP rounds, 108 violated). Crossed twelve at
round 8. No freeze. Site set refuted; side open. T-017 unchanged. Waiter
started n=17 `23/5` windows 6 at 15:40Z.

## n=17 23/5 windows 6 (2026-09-18T15:55Z)

T-019-seeded auto `(32, 42, 52)` plus `--seed-windows 6` at `23/5` stopped
unconverged at `17.048472` after 920.4 s (46 LP rounds, 54 violated). Seed
sites 1760 (1184 T-019 plus 576 lattice). Crossed seventeen at round 12 and
sat at 17 through round 18, then climbed. Slightly worse than windows 5
(`17.042346`). No freeze. Site set refuted; side open. T-019 unchanged.
Waiter started windows 7 at 15:55Z; then n=19 `97/20` if still above 17.

## n=17 23/5 windows 7 (2026-09-18T16:10Z)

T-019-seeded auto `(32, 42, 52)` plus `--seed-windows 7` at `23/5` stopped
unconverged at `17.046923` after 904.2 s (42 LP rounds, 186 violated). Seed
sites 1968 (1184 T-019 plus 784 lattice). Crossed seventeen at round 19.
Between windows 5 (`17.042346`) and windows 6 (`17.048472`). No freeze.
Site set refuted; side open. T-019 unchanged. Waiter started n=19 `97/20`
T-020 windows 6 at 16:10Z.

## n=19 97/20 T-020 windows 6 (2026-09-18T16:26Z)

T-020-seeded auto `(34, 45, 56)` plus `--seed-windows 6` at `97/20` for n=19
stopped unconverged at `19.808958` after 953.1 s (34 LP rounds, 321
violated). Seed from `certificate-24-5.json`; seed sites 2836 (2260 T-020
plus 576 lattice). Crossed nineteen at round 5 and climbed. No freeze.
Site set refuted; side open. T-020 unchanged. T-021's n=20 pointer
untouched. T-028 not landed. Waiter done. Covering queue empty.

## Hour 9 (2026-09-18T16:28Z)

Post-encode covering queue finished. Encode-only timeout unresolved. No
`--search`. T-028 not landed. `packing-ledger check` OK. `packing-validate
--records` 33/80 steps passed on `70c73070`. Atlas composites still
showed n=18 at 4.59; `build_known_best_atlas --update` wrote 4.67.
Closeout after 18:00Z.

## Hour 10 (2026-09-18T16:53Z)

Covering queue still empty. No colgen. Encode-only still unresolved. No
`--search`. T-028 not landed. CI on `f2696657`: suite-b tests passed
(3106); the job failed the cost band (72.1 s vs recorded 124.78 s).
`gate-budgets.yaml` untouched. packing-required cascaded. HEAD
`4e7dfb47` CI still in flight. Closeout after 18:00Z.

## Morning report (2026-09-18T18:17Z)

Do not `--search`. Do not merge. Do not close `think-qqzs`, `think-g3j7`,
`think-gyzw`, or `think-jwb1`. Do not allocate exp-161 to F1/M7.

**Needs review.** T-027 landing (`s(18) >= 467/100`). W5 Chromium-early.
Atlas composites now print n=18 at 4.67.

**What ran.** H-216 two named n=6 site sets, both covering ≥ 6. Relational
colgen skeleton. G4 n-parameterised producer. M3 T-018 piercing. W5
efficiency block. Route S encode-only (09:33Z start, 15:24:31Z timeout,
no JSON). Post-encode covering: n=12 `397/100` four-grid; n=17 `23/5`
windows 5/6/7; n=19 `97/20` T-020 windows 6. No `--search`.

**What moved.** T-027 retained. Atlas labels follow it. Covering register
grew to 60 restricted optima at 28 sides.

**What died.** Encode-only unresolved. n=12 `397/100` four-grid 12.122748.
n=17 windows 5/6/7 all above 17 (best windows 5 at 17.042346). n=19
`97/20` 19.808958. n=18 4.68/4.69/4.70 cannot certify. T-028 not landed.
H-216 is not an n=11 result.

**Queue after.** Route S still needs a successful encode before
`--search`. n=17 `23/5` open; n=19 `97/20` open; n=11 stays T-026
~3.826447. packing-campaign numeric remains NO-GO.

**Health.** `packing-ledger check` OK before this closeout.
`packing-validate --records` passed on `70c73070`. Hosted packing-required
on `f98ff781` succeeded (run 35371189375). Local `--push` browser floor
`.ts` failures are Node v22 versus workbench `>=24.18` on this VM.

## Block 8 closeout (2026-09-18T18:17Z)

Encode JSON is absent; timeout unresolved. This record is terminal
(`ended_at` 18:17:33Z, status `stopped`, phase 4 finalization). exp-161
drops its lease. Native harness usage is unmeasured.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
