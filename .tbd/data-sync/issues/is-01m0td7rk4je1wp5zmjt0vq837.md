---
type: is
id: is-01m0td7rk4je1wp5zmjt0vq837
title: Scope auxiliary-loss and duplicate-retention advice
kind: bug
status: closed
priority: 2
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - review
  - insight
dependencies: []
parent_id: is-01m0tbtgpb92e81ndvw4xm9be6
created_at: 2026-08-24T17:31:36.419Z
updated_at: 2026-08-24T17:36:31.983Z
closed_at: 2026-08-24T17:36:31.982Z
close_reason: "D-182 fixed: equivalent loss shaping remains possible with proof, and duplicate suppression is limited to exploration rather than unbiased frequency measurement; normal gate passed."
resolution: null
duplicate_of: null
---
PR20 says auxiliary losses change minimizers and never to pay twice for a named endpoint. Narrow this: equivalent/lexicographic shaping can preserve target minimizers, and repeat hits are needed for unbiased frequency estimates even if a taboo archive helps exploration. Record D-182.
