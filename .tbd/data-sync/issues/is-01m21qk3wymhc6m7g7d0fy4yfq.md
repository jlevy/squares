---
type: is
id: is-01m21qk3wymhc6m7g7d0fy4yfq
title: Document the tuning and replacement procedure for each typeface
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-09T00:02:57.041Z
updated_at: 2026-09-09T00:16:16.459Z
---
Owner requests one durable map of all serif, sans and monospace tuning so a future typeface replacement identifies exact assets, size ratios, weights, math metrics/scales, baseline/decoration controls, generators and verification commands. Put reusable settings in existing KPress font/math architecture doc and link Squares paper-specific sizing/geometry policy. Distinguish optical tuning, font-generated metrics and browser rendering policy; avoid a duplicate architecture document.

## Notes

Solmedium produced typography design-system consolidation for existing KPress kpress-design.md; Astra reviewed and required factual corrections for authored serifCSS/generatedsansCSS,650collision,baselinecontract,exacttests. Upstream docscommit125bada inPR68 includes corrected map; KPress beadkpr-6q53. MainPR66mono.82change is being reconciled in samePR, so current docshead canadvance. Squares paper-design and full active-spec handoff are committed93cf54a9.
