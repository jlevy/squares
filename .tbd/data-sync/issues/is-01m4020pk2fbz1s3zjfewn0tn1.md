---
type: is
id: is-01m4020pk2fbz1s3zjfewn0tn1
title: "Optimality paper: figures too wide at phone widths"
kind: bug
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-03T04:58:02.721Z
updated_at: 2026-10-03T14:38:07.365Z
closed_at: 2026-10-03T14:38:07.365Z
close_reason: Merged in jlevy/squares#312 (c831b4ee0), after a correctness and engineering review round (419a1db5d)
resolution: null
duplicate_of: null
---
Owner, 2026-10-03: 'the figures on the n=11 optimal proof explainer page are very wide on mobile widths' (papers/n11-optimality-review.html). Measure each figure's width at 390 and 320, find what sets it (an intrinsic SVG width, a min-width, a wide table or a fixed-size canvas), and make every figure fit the column or scroll inside its own box; shots at 390 and 1280, a geometry test.
