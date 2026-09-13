---
type: is
id: is-01m2ckzxahng9d3m19w6bp5hfa
title: Extract deterministic illustration timeline and trace capture adapters
kind: task
status: open
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-phase-3
  - workbench-roadmap
dependencies:
  - type: blocks
    target: is-01m24pase6ebcw856v6d8mbvnk
  - type: blocks
    target: is-01m229am4r6vrcj7djyt78e85w
  - type: blocks
    target: is-01m291gkje2c7x07x2ah4fdpxn
  - type: blocks
    target: is-01m28rzfz3nnrjrqw0zdg5xvxm
parent_id: is-01m2chahf57z4w9tj5gehbs0td
created_at: 2026-09-13T05:31:40.752Z
updated_at: 2026-09-13T05:43:47.815Z
---
Own pure animation timeline, interpolation and SVG view adapters under packages/workbench. Replay recorded traces or hand-authored illustrations without running a solver during draw. Preserve dwell/rearrange/correct/settle phases, explicit square arrival, variable side and rotation, overlays/palette and guidance/evidence labels. Capture tool uses the same seek API and records input/config/source identity. Acceptance: seek and capture agree at fixed times including boundaries; replay works with solver unavailable; physics-free illustrations work; invalid or illustrative motion is never promoted to checked evidence; reduced-motion path is explicit.
