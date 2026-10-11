---
type: is
id: is-01m2b0qdwj6yj4s84apk2d1p8c
title: Derive exact BC329 core-size intervals from its terminal witnesses
kind: task
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - strategy
dependencies:
  - type: blocks
    target: is-01m2b0qe8stb62xr0zzrynqeej
parent_id: is-01m24sm7wm3s5eh8ke6vze7mw1
hold: null
hold_until: null
created_at: 2026-09-12T14:35:45.426Z
updated_at: 2026-10-06T08:40:26.700Z
closed_at: 2026-10-06T08:40:26.700Z
close_reason: "Superseded: it analyses BC329 terminal witnesses that do not exist. BC329's prospective endpoint 3.8267215 is below T-033's proved 3.8269975, so the packet could not move any bound even before T-060; its runner and calibration machinery is retained unexecuted on main via PR #156. s(11) is settled: T-060 (V3/C3) proves s(11) = T = 3.8770835..., packing/frontier/RESULTS.md on origin/main eb43ffe9a marks every earlier n11 lower bound 'superseded by T-060', and packing/campaign/ideas.md Orientation records n11 as settled with its older route premises historical. Its 'paused' hold (the owner's 2026-09-14 BC329/heavy-computation hold, think-zwlf) was cleared to close it: the hold's premise, a small n11 gain, no longer exists."
resolution: canceled
duplicate_of: null
---
After BC329 reaches a valid terminal scientific result, analyze its exact least-charge witnesses and all membership/admissibility breakpoints as the uniform core side B varies on the exact interval that could still improve T026. A rejection witness should be propagated only while its trace and admissibility persist; a retained family of exact witness intervals may exclude the declared improving B range for the fixed 2880 net and relative weights, while uncovered gaps remain unresolved. After acceptance, use exact least-charge directions and budget margin to justify at most one successor packet. Do not generalize to reoptimized weights, changed atoms, nonuniform nets, direction-dependent core sizes, or other domains.

## Notes

Paused: 2026-09-14 owner hold (think-zwlf): BC329's prospective gain is about 0.000274 over T-026 s(11) >= 3.8264474, and heavy computer-assisted work for very small improvements is paused while the program re-strategizes toward significant n=11 improvements or a much simpler proof. The runner, reader, verifier and run sheet land as retained, unexecuted machinery with PR #156 (think-j007). Resume only by an explicit owner decision.
