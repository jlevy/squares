---
type: is
id: is-01m21qk3wymhc6m7g7d0fy4yfq
title: Document the tuning and replacement procedure for each typeface
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-09T00:02:57.041Z
updated_at: 2026-09-09T03:00:31.069Z
closed_at: 2026-09-09T03:00:31.069Z
close_reason: "Implemented, reviewed, merged in Squares PR #135 (merge 171bba339321b8d63d85a59ab5f2db946270be0e) with reusable work in KPress PR #68 (merge a6203389c0a6d1f6e542b1f50fa177121eae7f4a). All PR and post-merge CI passed; Pages serves edition 171bba33; live publication 34/34 and delayed-font smoke pass. HTML/PDF opened locally. Native reload retains 3000px exactly in Chromium, Firefox, and WebKit with JS on/off. Bullet raster-shape follow-up think-x65m remains open because measured geometry is already square."
resolution: null
duplicate_of: null
---
Owner requests one durable map of all serif, sans and monospace tuning so a future typeface replacement identifies exact assets, size ratios, weights, math metrics/scales, baseline/decoration controls, generators and verification commands. Put reusable settings in existing KPress font/math architecture doc and link Squares paper-specific sizing/geometry policy. Distinguish optical tuning, font-generated metrics and browser rendering policy; avoid a duplicate architecture document.

## Notes

Solmedium produced typography design-system consolidation for existing KPress kpress-design.md; Astra reviewed and required factual corrections for authored serifCSS/generatedsansCSS,650collision,baselinecontract,exacttests. Upstream docscommit125bada inPR68 includes corrected map; KPress beadkpr-6q53. MainPR66mono.82change is being reconciled in samePR, so current docshead canadvance. Squares paper-design and full active-spec handoff are committed93cf54a9.
