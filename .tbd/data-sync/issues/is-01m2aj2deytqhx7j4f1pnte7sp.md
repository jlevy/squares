---
type: is
id: is-01m2aj2deytqhx7j4f1pnte7sp
title: Bound BC329 interval and dilation replay memory and checkpoint progress
kind: bug
status: closed
priority: 1
version: 11
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m2aj2ewckram8ww4458w74hr
  - type: blocks
    target: is-01m2aj7q4y8raaw35s0jq3ty2y
  - type: blocks
    target: is-01m2anzgc2aqn6vzx29ps3rpn2
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
hold: null
hold_until: null
created_at: 2026-09-12T10:19:36.798Z
updated_at: 2026-10-06T08:40:14.198Z
closed_at: 2026-10-06T08:40:14.197Z
close_reason: "Superseded: the interval and dilation schedulers landed with PR #156; the remaining full-shape profiles are moot. BC329's prospective endpoint 3.8267215 is below T-033's proved 3.8269975, so the packet could not move any bound even before T-060; its runner and calibration machinery is retained unexecuted on main via PR #156. s(11) is settled: T-060 (V3/C3) proves s(11) = T = 3.8770835..., packing/frontier/RESULTS.md on origin/main eb43ffe9a marks every earlier n11 lower bound 'superseded by T-060', and packing/campaign/ideas.md Orientation records n11 as settled with its older route premises historical. Its 'paused' hold (the owner's 2026-09-14 BC329/heavy-computation hold, think-zwlf) was cleared to close it: the hold's premise, a small n11 gain, no longer exists."
resolution: canceled
duplicate_of: null
---
The WIP reflected-interval executor submits a closure carrying dense ThresholdAtomData per direction, and the mandatory dilation replay serializes the full certificate per direction while exposing no progress/deadline/log callback. Measure the complete positive path, remove or bound repeated dense serialization, stream or otherwise cap retained outcomes, and make every landed dilation/interval direction atomically checkpointable under the shared scientific deadline. A timeout must leave reconstructable partial evidence and cannot silently lose completed directions. Prove bounds with adversarial controls and retain peak-memory/timing measurements before target registration.

## Notes

The interval and dilation schedulers are integrated and independently reviewed: submissions are capped at 2W, progress is published in completion order, final results are deterministic in net order, landed batches are drained, and incomplete exits terminate workers. The remaining acceptance evidence is the three fresh 14,404-row full-shape non-scientific profiles owned by think-vy5i, followed by source-distinct admission; no BC329 target has run.

Paused: 2026-09-14 owner hold (think-zwlf): BC329's prospective gain is about 0.000274 over T-026 s(11) >= 3.8264474, and heavy computer-assisted work for very small improvements is paused while the program re-strategizes toward significant n=11 improvements or a much simpler proof. The runner, reader, verifier and run sheet land as retained, unexecuted machinery with PR #156 (think-j007). Resume only by an explicit owner decision.
