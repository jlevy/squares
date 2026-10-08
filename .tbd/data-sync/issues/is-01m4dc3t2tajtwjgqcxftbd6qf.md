---
type: is
id: is-01m4dc3t2tajtwjgqcxftbd6qf
title: "C16: stabilize opening prose while the regular PT Serif face loads"
kind: bug
status: in_progress
priority: 1
version: 3
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4cecqqmt13gys8265mpra32
hold: null
hold_until: null
created_at: 2026-10-08T09:04:37.977Z
updated_at: 2026-10-08T10:37:23.046Z
started_at: 2026-10-08T09:09:16.063Z
---
Pages at cf327e46c reported all-results.html 390/light CLS 0.1412386 against the existing 0.1 limit. Delaying the actual regular PT Serif face reproduced opening-prose rewrapping (CLS 0.110167 at 416 ms); local metric-adjusted Georgia and Times/Liberation fallbacks measured CLS 0 with final PT Serif preserved. Own a narrow default-prose CSS correction and real delayed-face/control/reader-mode regressions, retain original .1 and 0.04px geometry checks, and update paper-design documentation. Final exact-head Packing, Pages and full104 checkpoint remain mandatory. Source author is the original Astra reviewer; root independently reviews the CSS and tests. No font bytes, generic hide/wait, global budget increase or cached certification admission.

## Notes

The exact 8cb1f686c hosted Packing and Pages runs passed; full105 found the delayed-font synthetic fixture also enforced the production longest-task budget (313ms vs300ms) and two glyph reports required optional Georgia to exist on Linux. Narrow repair retains actual attribution/reader choices/0.04px geometry/.1 CLS and unadjusted failing control; production LCP/task/blocking guards remain in production CLI. Glyph probe identifies only exact owned local-only fallback declarations, fails closed on URLs, changed family/style/weight and duplicate rules, and reports absence separately. Real CSSOM negative cases include quoted-comma alias. Seven pure checks plus no-cache lint/types passed; final hosted browser evidence pending.
