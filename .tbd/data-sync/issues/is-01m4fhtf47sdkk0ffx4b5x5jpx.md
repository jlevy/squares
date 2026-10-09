---
type: is
id: is-01m4fhtf47sdkk0ffx4b5x5jpx
title: Unadopted better results render as superseded (T-128, T-130)
kind: bug
status: closed
priority: 1
version: 4
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4fdxw81pt2v4k29y9n58rn6
hold: null
hold_until: null
created_at: 2026-10-09T05:22:52.167Z
updated_at: 2026-10-09T06:01:54.652Z
started_at: 2026-10-09T05:23:17.911Z
closed_at: 2026-10-09T06:01:54.651Z
close_reason: "Standing fix at #460; upward patches assigned to integrator and #469 agent"
resolution: null
duplicate_of: null
---
render_recent_results.standing marks any result no case lane rests on as SUPERSEDED, so T-128 (#460) reads 'recorded, superseded by T-098, T-115, T-125 and T-127' and T-130 (#469) 'superseded by T-119 and T-125' although their reported sides are strictly smaller than the held bounds. Correct status should say reported/pending adoption. Fix at #460, the lowest layer where it manifests.

## Notes

Fixed at #460 657147e79 + re-pin 61359c972: superseded means replaced (cases hold a bound at least as good as each stated bound; ties stay superseded); new standing 'pending adoption' (status renders 'recorded', no mark) where a stated bound is strictly better than the case record in a lane the entry can hold (C0/C1 -> reported lane only), via check_standing.improvements() exact comparison; mixed cases pending as a whole, superseded per-case in site chains; T-128 claim states its eight exact sides; guard test requires unadopted imports to state sides. Docs: epistemics.md Status, result-import.md Stage 3 rule 'The claim states each bound it reports', article template, paper-design. Upward: T-129 sides patch at #463 (integrator), T-130 sides patch at #469 (#469 agent); re-render RESULTS.md/headline and re-pin per layer.
