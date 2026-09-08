---
type: is
id: is-01m21c9b3envq2cwh5q5s7wvgs
title: Stabilize prepared math line carriers during print font loading
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
delegate: caption_rendering
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T20:45:22.413Z
updated_at: 2026-09-08T21:20:34.978Z
---
Pages run 34274946315 retains print-loading movement of 29.953px in custom-serif and 7.0625px in both system settings. Base x positions, widths, heights and font sizes remain fixed while baseline/y drift accumulates through the document. Diagnose and reserve the remaining inline carrier/line-strut geometry under print CSS, preserving final layout and wrapping. Delegate caption_rendering; do not relax the one-pixel tolerance.
