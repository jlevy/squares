---
type: is
id: is-01m3wrghxczsftw00my3be7mt3
title: "CI: the three behavioral shards run at their ceilings since the suite grew on 1 October"
kind: bug
status: in_progress
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
hold: null
hold_until: null
created_at: 2026-10-01T22:14:13.163Z
updated_at: 2026-10-09T00:16:50.932Z
started_at: 2026-10-05T07:29:22.908Z
---
Hosted readings on 2026-10-01 after about 450 tests were added that day: suite_a 113.9 to 132.7 s over ten runs (geometric mean 118.5) against a 131 s ceiling and an 85.03 s record at 2,213 tests (now 2,665); suite_b 91 to 139 s (mean 109.9) against 154; suite_c 90 to 147 s (mean 126.9) against 154. jlevy/squares#277 failed shard A at 132.67 s with every test passing, and needed four full re-runs for runner noise (a PyPI timeout on macOS, partial-rerun refusals, the ceiling). devtools.suite_files packs files by recorded cost and falls back to a path hash for files absent from the record, so the day's new test files are unbalanced. Fix properly: rebuild the per-file cost record from a fresh hosted cohort and repartition; decide between a fourth shard and re-recorded ceilings with attribution (check_gate_budgets' ratchet); keep OR-14's two to two and a half minute surface. Read with: python -m devtools.read_tier_walls --tier suite_a --run-id …

## Notes

jlevy/squares#287 merged 2026-10-01 (main f25a85cb5): a fourth behavioral shard, the partition rebuilt from the day's measured per-file costs (the record knew 433 of 499 test files; 66 fell to a path hash), no ceiling raised (A and D 131 s, B and C 154 s). First hosted reading under four shards, run 36939743802: A 72.11, B 105.38, C 107.33, D 104.95 s (the day's three-shard means were 118.5, 109.9, 126.9). Remaining: record suite_d's first measurement in gate-budgets.yaml (pending rule expires 2026-10-08) and re-take A, B, C from a second four-shard cohort; rebuild the cost record from a green four-shard run on main; D read 105 s against a predicted 84 s on its one reading, watch it. The frontend job (about 214 s) is now the longest job on a pull request.

2026-10-05 07:45 UTC (bead bookkeeper). Shard walls are again the only failures on the n=17 stack: on jlevy/squares#347 (run 37274037862 at 9d2f05582) suite-c took 167.4 s against its 154 s ceiling (recorded cost 132 s) and suite-d 131.5 s against 131 s, with every test passing; the stack layers fail the same way. #347's lane is root-causing it under think-umlx; main's shard-4 record is think-skka.

Historical firstsuiteDmeasurement admitted c3dc:green37613399745 attempt1 job112765857172 actual33e96ced/tree23782412,101.34s at4CPUs/jobs1/inner1,1of101steps. Pendingexpiryremoved;143ceiling/drift/topologyunchanged. Currentrootjob113593324236 actual62a361c8/tree720674de reads190.63s at1of105 and isnotpooled. Currentperformance debt remains open;no speedup or currentPASSclaim.
