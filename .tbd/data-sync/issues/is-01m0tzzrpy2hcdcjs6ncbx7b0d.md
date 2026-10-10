---
type: is
id: is-01m0tzzrpy2hcdcjs6ncbx7b0d
title: "Spec: deterministic SVG rendering toolkit"
kind: epic
status: closed
priority: 1
version: 24
spec_path: docs/project/specs/done/plan-2026-08-24-deterministic-svg-rendering-toolkit.md
labels:
  - packing
  - visualization
  - focus-efficiency
dependencies:
  - type: blocks
    target: is-01m0r7sk41gsj2yjh80tx6324h
child_order_hints:
  - is-01m0v0y1twe93jq16rvnqw6nx4
  - is-01m0v0yf3ffe0tg78dss3cdx77
  - is-01m0v0yfcmzrkj40qhph74gk1n
  - is-01m0v0ypqc2shhf313140pqsmk
  - is-01m0v0z1kj1v09bzcd9qqk45ap
  - is-01m0v0z3ve6y0n6bc9e0ddwh1w
  - is-01m0v0zahjq54tvtm1sxr0c9yx
  - is-01m0v0zjrb1y43g07ppbgp6qhf
  - is-01m0v0ztwy527bxhn4wr64xbka
  - is-01m0v102z22dxytc6atqpnszdz
  - is-01m0v10ekmcac6c3v3wm9qtsda
  - is-01m0vwd7kt9wnndsb4jtzzvpeg
  - is-01m0vwd8ej4f7j45jk54mqmtxx
  - is-01m0vwd9a6sb0a92f46srt46q7
created_at: 2026-08-24T22:59:17.342Z
updated_at: 2026-10-10T23:02:48.757Z
closed_at: 2026-10-06T08:28:16.240Z
close_reason: "Done: the SVG toolkit spec landed in PR 25 (merged 2026-08-25, 05888b60f), sqpack.render is on main, and all 14 children, including the three reopened PR 25 follow-ups, are closed."
resolution: null
duplicate_of: null
---
Implement the plan's zero-dependency deterministic SVG spine, progressive overview/comparison/trajectory views, exact metadata and comments, known-answer n=3 migration, and portability checks. Acceptance is the spec's full criteria: byte-repeatable fixtures, honest evidence labels, safe self-contained SVG, useful static fallbacks, measured size/render cost, and a green repository gate.

## Notes

Planning is in PR #25, stacked on PR #24 through commit 15aad42. The active spec includes the official-library survey, exact file/function map, CSS reduced-motion fallback, deterministic metrics split, n=5 fixture ownership, and an 11-child dependency graph. The full 30-step packing gate passed with 42 negative controls; implementation remains open and begins at think-5681.

Reopened: Post-close review found three unresolved PR #25 soundness, validity, and porting children. Reopening the owning epic preserves the work and restores a truthful bead hierarchy; it must remain open until those children are resolved.
