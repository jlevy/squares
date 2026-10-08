---
type: is
id: is-01m4dc3t2tajtwjgqcxftbd6qf
title: "C16: stabilize opening prose while the regular PT Serif face loads"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4cecqqmt13gys8265mpra32
hold: null
hold_until: null
created_at: 2026-10-08T09:04:37.977Z
updated_at: 2026-10-08T09:09:16.066Z
started_at: 2026-10-08T09:09:16.063Z
---
Pages at cf327e46c reported all-results.html 390/light CLS 0.1412386 against the existing 0.1 limit. Delaying the actual regular PT Serif face reproduced opening-prose rewrapping (CLS 0.110167 at 416 ms); local metric-adjusted Georgia and Times/Liberation fallbacks measured CLS 0 with final PT Serif preserved. Own a narrow default-prose CSS correction and real delayed-face/control/reader-mode regressions, retain original .1 and 0.04px geometry checks, and update paper-design documentation. Final exact-head Packing, Pages and full104 checkpoint remain mandatory. Source author is the original Astra reviewer; root independently reviews the CSS and tests. No font bytes, generic hide/wait, global budget increase or cached certification admission.
