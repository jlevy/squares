---
type: is
id: is-01m20vpzkch50ejzwvpnjpx9h6
title: Narrow shared KPress render readiness while preserving font and metric correctness
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies:
  - type: blocks
    target: is-01m20v1mq20k9d9p1wg9s5qdsq
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T15:55:43.595Z
updated_at: 2026-09-08T16:04:16.252Z
---
Under upstream kpr-prsb, remove avoidable per-render warmup of unrelated faces. Render hidden content against the matching tables, discover actual glyph face requirements, and reveal only after those faces are ready. Coordinate exact initial geometry with host; preserve opt-outs, failure fallback, latest-call-wins, font safety, and print behavior. Delegated to kpress_font_pipeline in isolated clone.
