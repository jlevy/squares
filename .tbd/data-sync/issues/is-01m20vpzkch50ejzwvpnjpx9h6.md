---
type: is
id: is-01m20vpzkch50ejzwvpnjpx9h6
title: Narrow shared KPress render readiness while preserving font and metric correctness
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies:
  - type: blocks
    target: is-01m20v1mq20k9d9p1wg9s5qdsq
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T15:55:43.595Z
updated_at: 2026-09-08T18:40:08.362Z
closed_at: 2026-09-08T18:40:08.361Z
close_reason: KPress PR61 merged at 20a7d2b after the final browser, JavaScript, lint, distribution and Python3.12/3.13/3.14 CI matrix passed (run34256487179). It adds correct per-family font readiness/hydration, the canonical architecture document, and the optional-browser availability repair.
resolution: null
duplicate_of: null
---
Under upstream kpr-prsb, remove avoidable per-render warmup of unrelated faces. Render hidden content against the matching tables, discover actual glyph face requirements, and reveal only after those faces are ready. Coordinate exact initial geometry with host; preserve opt-outs, failure fallback, latest-call-wins, font safety, and print behavior. Delegated to kpress_font_pipeline in isolated clone.
