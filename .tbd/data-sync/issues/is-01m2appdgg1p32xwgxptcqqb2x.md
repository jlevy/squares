---
type: is
id: is-01m2appdgg1p32xwgxptcqqb2x
title: Measure the full-shape fixed-core calibration profile
kind: task
status: open
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - calibration
dependencies:
  - type: blocks
    target: is-01m2appm2nx1m700ky98ytzv4z
parent_id: is-01m2aj2ewckram8ww4458w74hr
child_order_hints:
  - is-01m2b883ztxn7qazs98bndea6b
  - is-01m2b884n0ms50xp93q6aaps1g
created_at: 2026-09-12T11:40:26.511Z
updated_at: 2026-09-12T16:48:35.832Z
---
Run at least three fresh full-profile positive controls on the intended host after the calibration command is admitted. Each run must execute 2,881 raw, 2,881 normalized-exact, 5,761 reflected-interval, and 2,881 dilation direction records and pass independent readback. Retain per-phase wall clocks; requested and effective workers by route; scoped CPU observations; sampled process-group sum-of-RSS peak with sample count, max gap, observer errors and limitations; artifact inventory counts, bytes and digests; deadline relationships and headroom; process-group exit/reaping evidence; source/runtime manifests. Report median and range. Do not infer BC329 compute time from this deliberately easy fixture or run the scientific target.

## Notes

Execution remains blocked. Independent read-only run-sheet review at /private/tmp/bc329-three-profile-run-sheet-review.md refused the current sheet before any profile: configured workers are not observed, true command-return wall time is not retained, run-set summaries/readbacks are one-off heredocs, and the source-distinct reader command is absent. Follow-ups are think-gscz, think-5dql, think-n4gh, and think-pp3j. The 4/5400/7200/2 tuple and 14,404-row accounting otherwise passed review. No profile or BC329 target ran.
