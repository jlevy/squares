---
type: is
id: is-01m2ey0d8smw4f4w72hyay9070
title: "Route C: orientation-class structure theorem near Trump's packing"
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - strategy
dependencies: []
parent_id: is-01m2exznj4k1zyz1rczby8ch2k
created_at: 2026-09-14T03:05:11.704Z
updated_at: 2026-10-06T08:42:13.988Z
closed_at: 2026-10-06T08:42:13.988Z
close_reason: "Superseded: Route C asked to prove that any packing beating 3.877 needs three orientations; T-060 proves no packing of eleven unit squares has side below T = 3.8770835, so the statement is vacuous. s(11) is settled: T-060 (V3/C3) proves s(11) = T = 3.8770835..., packing/frontier/RESULTS.md on origin/main eb43ffe9a marks every earlier n11 lower bound 'superseded by T-060', and packing/campaign/ideas.md Orientation records n11 as settled with its older route premises historical."
resolution: canceled
duplicate_of: null
---
Prove that any packing beating 3.877 needs at least three distinct orientations: exact disjunctive LP at fixed angles, robust Farkas covers over angle intervals, and the BC-240 isolation theorem near Trump's angle. Precedent: Stromquist's 0/45-degree theorem. First test: solve 6+5 globally at Trump's angle (must return U), then 1-degree bins at 3.87 to measure the exceptional window. A 150 s plain big-M HiGHS probe found no layout, so this needs seeded layouts or custom branching on the cell LP.
