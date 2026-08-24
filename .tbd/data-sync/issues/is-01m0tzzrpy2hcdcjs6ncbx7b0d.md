---
type: is
id: is-01m0tzzrpy2hcdcjs6ncbx7b0d
title: "Spec: deterministic SVG rendering toolkit"
kind: epic
status: open
priority: 1
version: 8
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
created_at: 2026-08-24T22:59:17.342Z
updated_at: 2026-08-24T23:16:11.115Z
---
Implement the plan's zero-dependency deterministic SVG spine, progressive overview/comparison/trajectory views, exact metadata and comments, known-answer n=3 migration, and portability checks. Acceptance is the spec's full criteria: byte-repeatable fixtures, honest evidence labels, safe self-contained SVG, useful static fallbacks, measured size/render cost, and a green repository gate.

## Notes

Planning is in PR #25, stacked on PR #24 at commit 4f766a9. The spec now includes the file/function map, library decisions, call flows, fixtures, and validation gates. Implementation begins with the typed model and numeric contract.
