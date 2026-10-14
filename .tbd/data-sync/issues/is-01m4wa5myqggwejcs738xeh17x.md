---
type: is
id: is-01m4wa5myqggwejcs738xeh17x
title: Preserve exact irrational-bound handling in the default-drawing cascade
kind: bug
status: closed
priority: 1
version: 3
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4w9w2vc4p0j983wvvx8pybw
hold: null
hold_until: null
created_at: 2026-10-14T04:19:17.575Z
updated_at: 2026-10-14T07:21:25.536Z
started_at: 2026-10-14T04:20:31.504Z
closed_at: 2026-10-14T07:21:25.536Z
close_reason: Fixed, independently reviewed, and merged in regularization stack main9f48ccc80cee8dcf94c7cadbcaded01408f94fa2; exact-head Packing and Pages CI pass. Deployment tracked by parent think-azzv.
resolution: null
duplicate_of: null
---
Senior handoff probe at PR5915054 plus current587203f: regularize_evand.upper_bound now rational-only, but default_drawings.decide/drawn_above_bound still call it. Counts18/26/66/85 become house/U-is-unknown or raise even though exact comparisons arepositive namedexceptions. Use verified_bound.compare/difference, share axis ABOVE_U, preserve unread-bound refusal and existing improvement_rule. Also fix the current/trailing-poster regression precondition so ordinary repins do not break it. Recompute defaults for generator replacements at180/207 (90views retained), then redraw truthful complete exports.
