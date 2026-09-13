---
type: is
id: is-01m229an1fw0az9jgk0wcbg8c4
title: Benchmark the workbench simulator from the command line, without a browser
kind: task
status: open
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - packing
  - workbench-roadmap
  - workbench-phase-3
dependencies:
  - type: blocks
    target: is-01m2cm03rtrjcg98ejb9y56jn6
parent_id: is-01m2chahf57z4w9tj5gehbs0td
created_at: 2026-09-09T05:12:54.062Z
updated_at: 2026-09-13T05:43:48.002Z
---
Phase 3 under think-zisr. Benchmark the extracted DOM-free package API from packages/workbench/tools with fixed seed/configuration and declared runtime. Report steps and pair tests per second plus objective/validity/work receipts at representative n including 5, 17, 100 and 272 within measured limits. Output a retained package benchmark artifact; do not write new results into spike NOTES or drive a page through Playwright. Acceptance: no DOM dependency or copied physics; deterministic replay and browser/Node parity controls; same-work comparisons separate algorithm cost from rendering.

## Notes

2026-09-12 review: this benchmark belongs inside packages/workbench/tools and calls the DOM-free shared step API. Keep fixed seeds and reported step/pair-test work at representative n. Preserve the original measured context as historical evidence; new baseline results belong to a retained package benchmark artifact, not the spike NOTES. Validate replay and browser/Node parity before removing the old caller.
