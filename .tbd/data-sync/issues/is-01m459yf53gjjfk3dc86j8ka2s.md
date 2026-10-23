---
type: is
id: is-01m459yf53gjjfk3dc86j8ka2s
title: "wand125 card tally: keys [wand125 tools 2026] and [wand125 rectangle bounds 2026-09-28] cited by results but not tied to a source-coverage URL"
kind: task
status: closed
priority: 2
version: 4
delegate: c-gates-1023
labels: []
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
hold: null
hold_until: null
created_at: 2026-10-05T05:52:50.339Z
updated_at: 2026-10-23T09:08:19.283Z
started_at: 2026-10-23T06:19:06.785Z
closed_at: 2026-10-23T09:08:19.283Z
close_reason: "Delivered: [wand125 rectangle bounds 2026-09-28] and [wand125 tools 2026] have coverage sources wand125-rectangles-2026-09-28 and wand125-tools-2026-09-29, and the gate refuses an uncovered key (eab870f8c). PR #748 head 417ba331b, CI green (Packing validation run 39927824318, Certificate page 39927824335)."
resolution: null
duplicate_of: null
---

## Notes

2026-10-23 c-gates-1023 (PR #748): both keys now have coverage sources, wand125-rectangles-2026-09-28 ([wand125 rectangle bounds 2026-09-28], T-046, T-070) and wand125-tools-2026-09-29 ([wand125 tools 2026], T-058, T-059), and check_source_coverage refuses a recent cited key with none (think-g6d5). Commit eab870f8c.
