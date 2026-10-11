---
type: is
id: is-01m3qtxksrtmt2kc5qqnxf6t97
title: Measure proof-review orchestration and exact-verifier runtime separately
kind: task
status: open
priority: 2
version: 7
labels:
  - W7
dependencies: []
parent_id: is-01m3p04ndehpya7g3mbmmad36g
created_at: 2026-09-30T00:20:06.071Z
updated_at: 2026-09-30T00:54:45.670Z
---
Build a focused, reusable proof-review cost baseline using existing Codex task-tree rollups and exact-verifier receipts. Separate observed model/tool/agent-wait intervals, overlap-safe critical-path wall, validation elapsed and process CPU, setup/parsing/replay/kernel/serialization cost, and worker idle time. Do not interpret model reasoning tokens as elapsed analysis time or add overlapping agent/tool intervals. Fixed source/input/config, bounded workloads, exact outcome equivalence, environment and warm/cold labels, and repeated comparable samples precede performance claims. General slow repository gates are batched outside this loop. Profile first; choose algorithm, Rust kernel, scheduling, or orchestration changes according to measured bottleneck. Preserve partial/unresolved outcomes and complete-coverage requirements.

## Notes

2026-09-29 read-only baseline: session-164 Codex task-tree delta spans 9850.000 s wall envelope, 9835.202 s active interval union, 27020.360 agent-s, 17185.158 overlapping agent-s; 7449.598 s timed model stream, 713.462 s recorded first-token wait, 6290.491 s command tool intervals, and 1962.057 s agent-wait intervals overlap across agents and are not additive wall. Four live sessions make the snapshot incomplete; no branch/proof attribution. Retained n11 angle-1 1000-node result has 428 accepted and 78 unresolved (67 depth-capped, 11 queued) but no elapsed or CPU. Nine-box comparison is 1.420134 s total: 0.985860 s replay, 0.035566 s common-core sums, 0.398307 s corner-min sums, zero new closures. Two-level 67-parent/268-child diagnostic took 8.994229 s including replay; 15 parents closed, but no replay/kernel phase split or CPU. Do not extrapolate angle 1 to 201 angles. Smallest reusable instrument: opt-in proof CLI phase timing using monotonic wall plus process CPU for read/hash, parse/admission, verification, and serialization, with per-angle/counter aggregate in verifier and comparable outer process wall/CPU for startup/import; add replay vs child-kernel timing to existing diagnostics. Record fixed hashes/config/outcomes, warm/cold host regime, repeated samples, worker intervals and overlap-safe task-tree wall before bottleneck claims. No benchmark or code changes made in this audit.

2026-09-29 W7 timing implementation: the exact rectangle CLI now supports opt-in --timing, reporting perf_counter wall and process_time CPU for input read/hash, admission, verify_candidate, and source recheck. Output explicitly excludes module startup, argument parsing, receipt build, serialization, and output. Default golden bytes and decisions are unchanged. Focused CLI golden module: 4 passed; scoped Ruff and BasedPyright: zero findings; Ruff format and diff check pass. One bounded angle-1 n11/1000-node run was launched before independent review and its full stdout was not retained. The jq tool-output summary reported INCONCLUSIVE, 1000 nodes, 428 accepted, 78 unresolved, checker source SHA 1d41fa6aaa9cd9d5dfb95b54fe0cc3598af52c3d3c3f400fd78d83ccf98ca7aa, verification 6.585033458 s wall and 6.531895 s process CPU. This is one unreviewed diagnostic observation, not a matched benchmark, whole-angle projection, or proof receipt; CLI source hash at execution and full pending-box output were not captured. Future retained timing evidence must capture complete stdout and source/input identity at launch. No general slow repository tests, commit, or push.

2026-09-29 priority checkpoint: new packing/devtools/diagnose_rectangle_density_frontier.py was drafted for a supervised verifier child and exact all-pending-box midpoint/common-core diagnostics. It is UNVALIDATED and remains unstaged. No diagnostic run or receipt was produced. Scoped BasedPyright reported 0 errors; Ruff found 6 lint findings and format check found drift. Work was stopped on root priority change to the actual optimality verifier; do not invoke or publish this draft until it is completed, reviewed, and tested.

2026-09-29 W7 checkpoint: the unvalidated rectangle diagnostic draft was moved out of active devtools to ignored attic/wip/diagnose_rectangle_density_frontier.py, preserving unique source without lint/test discovery. It remains untested and must not be invoked as evidence.
