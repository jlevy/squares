---
type: is
id: is-01m2appdgg1p32xwgxptcqqb2x
title: Measure the full-shape fixed-core calibration profile
kind: task
status: closed
priority: 1
version: 9
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
hold: null
hold_until: null
created_at: 2026-09-12T11:40:26.511Z
updated_at: 2026-10-06T08:39:59.818Z
closed_at: 2026-10-06T08:39:59.818Z
close_reason: "Superseded: no profile run is needed for a packet that cannot move a bound. BC329's prospective endpoint 3.8267215 is below T-033's proved 3.8269975, so the packet could not move any bound even before T-060; its runner and calibration machinery is retained unexecuted on main via PR #156. s(11) is settled: T-060 (V3/C3) proves s(11) = T = 3.8770835..., packing/frontier/RESULTS.md on origin/main eb43ffe9a marks every earlier n11 lower bound 'superseded by T-060', and packing/campaign/ideas.md Orientation records n11 as settled with its older route premises historical. Its 'paused' hold (the owner's 2026-09-14 BC329/heavy-computation hold, think-zwlf) was cleared to close it: the hold's premise, a small n11 gain, no longer exists."
resolution: canceled
duplicate_of: null
---
Run at least three fresh full-profile positive controls on the intended host after the calibration command is admitted. Each run must execute 2,881 raw, 2,881 normalized-exact, 5,761 reflected-interval, and 2,881 dilation direction records and pass independent readback. Retain per-phase wall clocks; requested and effective workers by route; scoped CPU observations; sampled process-group sum-of-RSS peak with sample count, max gap, observer errors and limitations; artifact inventory counts, bytes and digests; deadline relationships and headroom; process-group exit/reaping evidence; source/runtime manifests. Report median and range. Do not infer BC329 compute time from this deliberately easy fixture or run the scientific target.

## Notes

Execution remains blocked. Component reader/coordinator/verifier exact-blob reviews accept their scoped repairs; integrated-head review at fbd915fc REFUSED the run sheet because it bypassed maintained snapshot/read/join/retain/source-closure. A revised command sheet is under independent exact wiring rereview and PR156 is still local-only beyond remote 52e4ab65. The frozen tuple 4/5400/7200/2, fixture hash, 14,404 rows per profile, and 22/19 file inventories are checked. No positive profile or BC329 target ran.

Paused: 2026-09-14 owner hold (think-zwlf): BC329's prospective gain is about 0.000274 over T-026 s(11) >= 3.8264474, and heavy computer-assisted work for very small improvements is paused while the program re-strategizes toward significant n=11 improvements or a much simpler proof. The runner, reader, verifier and run sheet land as retained, unexecuted machinery with PR #156 (think-j007). Resume only by an explicit owner decision.
