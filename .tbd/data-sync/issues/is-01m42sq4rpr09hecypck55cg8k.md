---
type: is
id: is-01m42sq4rpr09hecypck55cg8k
title: Stabilize the typecheck wall ceiling (think-4w2g)
kind: task
status: closed
priority: 2
version: 5
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m42sq026mszrdm4fwf5r8g8y
hold: null
hold_until: null
created_at: 2026-10-04T06:30:44.246Z
updated_at: 2026-10-04T08:12:20.589Z
started_at: 2026-10-04T06:32:15.376Z
closed_at: 2026-10-04T08:12:20.589Z
close_reason: "PR #338 merged (225d6b5e2): typecheck ceiling 130 s on 174 hosted serial readings; threading measured and rejected."
resolution: null
duplicate_of: null
---
Hosted typecheck breached the 111 s ceiling with 0 findings on #305 and #323 (readings 59.6-119.6 s). Measure, then set the ceiling or the step per OR-17 so routine runs do not flake. See think-4w2g.

## Notes

2026-10-04 07:24 UTC (tbd-moderate sub-agent): measured, changed, committed locally; not pushed.

Hosted evidence (serial step): 174 readings of the `typecheck` job's type-floor step, every
completed (passed or failed) pull-request run of Packing validation from 2026-10-02T07:49Z
to 10-04T06:21Z on 17 branches (175 runs, one with no typecheck job in its latest attempt),
read through the jobs API by `devtools.check_pr_wall` (setup/work split per job). Step:
min 54, p10 62, p25 73, median 93.5, p75 106, p90 111, p95 113, max 123 s; geometric mean
86.7 s. Two regimes: under 85 s n=73 (median 69 s), 85 s or more n=101 (median 104 s); no
trend by hour or branch. Over 111 s: 14/174 (8.0%); over 115 s: 3 (1.7%); over 125 s: 0. The
gate's own figure is 1.5 to 3.4 s under the API step time (83.52 vs 85 s on run 37182550037;
119.63 vs 123 s on 37165485062), so 5 to 11 of the 14 (3 to 6% of runs) were real breaches.
Latest attempts only, so the breaches re-runs hide (think-4w2g lists them) come on top. Setup
around the step: median 32 s (24 to 44 s); the step is a median 71% of the job wall
(median job wall 128 s).

Local evidence (one four-cpu box, alternating, all "0 errors, 0 warnings, 0 notes"): serial
143.2 and 151.9 s; `basedpyright --threads 4` 78.1 and 83.6 s (0.55x); `--threads 2` 88.9 s.
CPU: 4 workers about 276 s against serial 172 to 195 s. Peak summed RSS: 7.7 to 8.2 GiB
(4 workers) against 3.8 to 4.5 GiB serial. A toy project with two planted errors gives the
same diagnostics and exit code in both modes. End to end, `packing-validate --typecheck
--jobs 1 --inner-jobs 1` read 74.28 s on this box under load. (Readings taken while another
agent's `packing-validate --push` shared the box were discarded.)

Change: commit fca477d3d on local branch `claude/typecheck-ceiling` (worktree /home/user/wtc,
from origin/main e5a48b310). `_type_floor` passes `--threads N`, N = `_command_workers(jobs)`
(cpus - jobs + 1): 4 on the hosted typecheck job, 1 at a local tier's default --jobs (command
unchanged there). The 76.5 s serial record moves to history; the tier is
`pending_measurement: think-4w2g` until 2026-10-11 (the register's pending mechanism, like
suite_d and measure_verifier). The 111 s ceiling is held on purpose: at 0.55x the serial max
predicts about 68 s. Fallback if the first hosted cohort does not sit well under 111 s: the
serial readings argue for a ceiling of about 130 s. Tests: 5 new in test_validation_cli.py;
361 passed across the gate-budget, module-boundary, read-tier-walls, pr-wall and validation
CLI tests; check_gate_budgets passes; `packing-validate --edit` 54/54 steps passed.

Next: push and open the PR; the PR's own typecheck job is the first hosted reading at the new
shape. Re-take the record from that cohort (`read_tier_walls --tier typecheck`), drop the
pending fields, and tighten the ceiling to within 2x of the new record. Then close
think-4w2g and this bead.

2026-10-04 08:03 UTC: SUPERSEDED. After review of PR jlevy/squares#338, the coordinator dropped threading (hosted --threads 4 read 90.46 s on run 37185790574 job 111387285346, inside the serial spread; a reviewer's box gave 0.75-0.79x; a dead worker hangs basedpyright until the 900 s timeout; the worker count was uncapped; one test was vacuous). Commit b13c82ad7, on top of fca477d3d and not pushed, restores the serial _type_floor and removes the tests. It records the typecheck tier on the 174-reading serial cohort: measured 86.71 s (geometric mean), band 54/123, measured_on 2026-10-04, ceiling 130 s. The 76.5 s record goes to history, and the pending fields are removed. check_gate_budgets passes. 366 tests passed (gate_budgets, validation_cli, module_boundaries, read_tier_walls, pr_wall, ci_gate_recent_sampling). packing-validate --edit: 54/54 steps. packing-validate --typecheck --jobs 1 --inner-jobs 1 on this slower local 4-cpu box: 0 errors, but 136.95 s fails the 130 s ceiling there (local serial reads 137-152 s against a hosted maximum of 123 s).
