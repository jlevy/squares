---
type: is
id: is-01m0tzzrpy2hcdcjs6ncbx7b0d
title: "Spec: deterministic SVG rendering toolkit"
kind: epic
status: closed
priority: 1
version: 21
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-deterministic-svg-rendering-toolkit.md
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
updated_at: 2026-08-25T07:16:00.450Z
closed_at: 2026-08-25T03:00:05.499Z
close_reason: "All implementation children are complete in PR #25; the full 31-step packing gate, 33 focused SVG controls, Ruff, BasedPyright, Flowmark, and artifact replay pass."
resolution: null
duplicate_of: null
---
Implement the plan's zero-dependency deterministic SVG spine, progressive overview/comparison/trajectory views, exact metadata and comments, known-answer n=3 migration, and portability checks. Acceptance is the spec's full criteria: byte-repeatable fixtures, honest evidence labels, safe self-contained SVG, useful static fallbacks, measured size/render cost, and a green repository gate.

## Notes

Planning is in PR #25, stacked on PR #24 through commit 15aad42. The active spec includes the official-library survey, exact file/function map, CSS reduced-motion fallback, deterministic metrics split, n=5 fixture ownership, and an 11-child dependency graph. The full 30-step packing gate passed with 42 negative controls; implementation remains open and begins at think-5681.
