---
title: exp-268 — same-claim n11 first round after CLI startup repair
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-268
  series: series-000
  title: Same-claim n11 first-round control after startup invocation repair
  date: '2026-10-07'
  hypotheses:
  - H-281
  tier: confirmatory
  subject:
    label: Pinned n11 case 438 from its actual sixteen-cell cover at the accepted rational cap.
    engine: devtools.pilot_n17_capture and repaired sqpack.hull_kernel producer; freeze source before
      launch.
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, Python 3.14.7, gmpy2==2.3.1, one process per phase; external scratch.
    selftest_passed: true
  instance:
    axis: n
    point: 11
    role: positive_control
  method:
    control: Focused endpoint/dependency control passed in 0.85 seconds; actual CLI round 1 resume regression
      passed in 2.24 seconds, forbidding new producer/seed work and requiring saved-seed admission, complete
      replay, identical state identities; native current-vs-peak RSS and fail-closed memory-guard controls
      already pass.
    candidate: One complete repaired-producer round from cells followed by fresh process replay of that
      exact saved node.
    runs_per_condition: 1
    interleaved: false
    operator: Sol coordinator executes Astra-approved readiness contract in Session 184 phase 5.
    entry_point: packing/devtools/pilot_n17_capture.py
    command: From packing/ with required external scratch variables, production uses /Volumes/spud-ext1/agent-scratch/n17-w3-01a114fb/venv/bin/python3
      -m devtools.pilot_n17_capture --system n11 --cap capture --bins 32 --max-rounds 1 --max-live 64
      --min-width-log2 22 --hull-limit 48 --core octagon --seed-grid 0 --max-seconds 900 --replay-share
      0 --max-memory-mib 4096 --checkpoints campaign/series/series-000-smoke-and-calibration/results/exp-268-n11-first-round-control/checkpoints
      --save-objects campaign/series/series-000-smoke-and-calibration/results/exp-268-n11-first-round-control/production-objects
      --output campaign/series/series-000-smoke-and-calibration/results/exp-268-n11-first-round-control/production.json.
      Fresh process uses the same scientific parameters, --max-seconds 300 --replay-share 0.5 --resume
      campaign/series/series-000-smoke-and-calibration/results/exp-268-n11-first-round-control/checkpoints/checkpoint-round-001.json.gz,
      separate replay-objects and fresh-replay.json destinations. Both phases use GNU gtimeout -k10s with
      their respective900s/300s wall ceilings; the CLI derives its partial file from --output. Unique
      checkpoints and objects are retained there.
    budget: 900-second production ceiling followed by 300-second fresh replay ceiling; current-RSS4096
      MiB per process, checked cooperatively at phase boundaries. Freeze actual argv, RUN_DIR and owned-process
      timeout/cleanup before launch. Partial updates and complete checkpoints survive interruption; do
      not treat a memory-stop checkpoint as resumable. No continuation or target retuning.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-268-n11-first-round-control
  lease:
    expires: '2026-10-07T09:25:00Z'
    host: macOS arm64
  results: []
  verdict:
    decision: in-progress
    primary_criterion: First complete eleven-owner round, endpoint retained after seed/every update, producer/checker
      agreement; fresh saved-seed admission and eleven-step replay, final_state_agrees=true, same seed/node
      and round/update records, no new production.
    reason: Registered before scientific work; unchanged H281 settings and900/300second budgets. Correct
      the unsupported startup flag only; exp265 remains blocked with original logs.
---
# exp-268: n11 First-Round Readiness and Cost

This registration precedes the target.
Session 184 phase 5 is 08:42:46–09:12:46 UTC; a running fixed-budget control continues
across the slice boundary.
Production and fresh replay are sequential, each with its own wall/RSS limits.
Production has `--replay-share 0`; the separately budgeted fresh replay is the
acceptance replay. No source/input/parameter change or round-2 production is allowed
between them.

## Exact Inputs

The production frame is `--system n11 --cap capture`, with no `--box`, `--resume`,
owner-specific cap or grid seed.
The state is case 438, owners `[0, 1, 2, 3, 4, 8, 9, 10, 11, 13, 15]`. The exact cap is
$U=387708359002281417731/10^{20}$, $L=191/50$ and $B=L/U$. The endpoint uses the
`trump11` construction and exact root interval, transformed by the inverse quarter-turn
pose map. Every corner of all eleven center boxes lie in their assigned cells, and the
checked endpoint side is strictly below the cap by less than $10^{-20}$.

`check_hull_kernel_mask0.load_sources()` calls the frozen loader and admissions.
Its retained inputs are the field packet, audit, cover, D4 receipt and corresponding
checker, with compressed/raw byte bounds and identity checks.
Cover raw identity: `df7938d9ba27095a38fabe45f8b26b259a2cc896c2ae4aac6bae874f417adc4e`.
The additional pose receipt is
`packing/resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json`,
SHA-256 `c5b970458135847f5790f2311e4861faf720924ad7e62f5bafb6d1978743144c`. Freeze its
exact bytes/status/roles before production and confirm unchanged inputs before fresh
replay.
The large historical source node is not an input to this fresh cell-seed control;
no claim about its ancestry is made.

The external environment reports Python 3.14.7 and gmpy2 2.3.1, matching the project
pins. The repository `.venv` lacks gmpy2 at this checkpoint and is not the launch
interpreter. Retain source/runtime provenance for the pilot, repaired producer, exact
kernel, pose construction/loader and native RSS adapter.
The launch receipt captures source/runtime provenance automatically; it is not a
mathematical acceptance test.

## Acceptance and Measurements

Require exactly eleven distinct certified round-1 owner updates, a complete round-1
summary/checkpoint and the endpoint held after the seed and every update.
The producer prediction must match the exact checker state.
The fresh resume invocation keeps `--max-rounds 1`, so its first possible new round is 2
and no producer update is executed.
Require replay status `PASS_REPLAYED`, eleven steps, `final_state_agrees: true`,
identical seed/node identities, unchanged round/update records and empty source drift.
Do not accept a top-level `PASS_PILOT_MEASURED` with an incomplete round or absent
replay.

Endpoint loss, exact input refusal, producer/checker disagreement or rejected replay
refuses acceptance. A ceiling or current-memory stop before completing the required
round/replay is incomplete; preserve the retained partial records without a contraction
verdict.
The RSS guard observes current memory at checked boundaries, not every transient
allocation, and lifetime peak is reporting only.
A hard owned-process timeout must preserve previous partial files and cleanup only the
owned child.

Record $E_r$, the maximum of all eleven owners’ x/y two-sided extents, $E_0$, $E_1$ and
$E_1/E_0$, without replacing this ratio by a maximum of per-owner ratios.
Retain per-owner live rows, owned-hull vertices, splits, update wall/CPU, total
wall/CPU, current/peak RSS, saved-object sizes and fresh replay time/work.
This first-round cost is the evidence for a later allocation; the old 2–4 CPU-hour
forecast is not used.

The known exact packing must remain present throughout; neither this control nor a
successful fresh replay establishes n17 capture, a new exclusion or the 15-round R9
contraction criterion.

The original exp-265 refused its unsupported startup argument before loading scientific
inputs. This successor changes the invocation only; the underlying instrument,
hypothesis, exact inputs and complete-round/fresh-replay criterion are unchanged.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
