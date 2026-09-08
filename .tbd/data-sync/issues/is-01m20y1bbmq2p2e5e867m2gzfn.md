---
type: is
id: is-01m20y1bbmq2p2e5e867m2gzfn
title: Lower list bullets slightly to align with the text crossbars
kind: bug
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T16:36:20.460Z
updated_at: 2026-09-08T16:36:36.394Z
---
User reports the list bullets are very slightly too high and wants their optical center nearer the region between the A and E crossbars. Inspect the actual shipped marker glyph/CSS and apply the smallest downward adjustment in the cleanest owner. Verify both screen and PDF, preserving list wrapping, alignment, and marker font provenance. Assigned to caption_rendering; include the fix in the current PR integration and final default-browser HTML/PDF preview.
