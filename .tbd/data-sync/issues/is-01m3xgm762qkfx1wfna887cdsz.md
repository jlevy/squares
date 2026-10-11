---
type: is
id: is-01m3xgm762qkfx1wfna887cdsz
title: "Census: why axis-aligned squares render lighter than dark green"
kind: task
status: closed
priority: 2
version: 5
labels:
  - research
dependencies:
  - type: blocks
    target: is-01m3xgm7qkkkcdckn74h9rq6c1
  - type: blocks
    target: is-01m3xgm9ccqv1h8p3j5x9ezjy0
parent_id: is-01m3xgkna3m3w1w50ky6gqyxyk
created_at: 2026-10-02T05:15:39.074Z
updated_at: 2026-10-02T06:00:21.763Z
closed_at: 2026-10-02T06:00:21.763Z
close_reason: Lane exit reached and integrated into X-049 (packing/campaign/explorations/X-049-families-shading-and-the-large-n-limit.md); coordinator verified the lane's claims, tests and checks; follow-ups are think-589i, think-hzv3, think-1n8w, think-bgkz and think-ptt7.
resolution: null
duplicate_of: null
---
W2 measurement lane, OR-1 tool. Replicate the workbench contact rule (packages/workbench/src/core/geometry.ts contactFacts; shade 0 needs four full-face contacts with walls or same-angle squares within the page's gap tolerance) in packing/devtools, with tests, over all 324 witnesses. For every axis-aligned square with fewer than four contacts, classify the cause: missing neighbour (hole or tilted neighbour), slack gap beyond tolerance, sideways offset, or numerical residual. Report the largest residual among pairs that do touch, so the inexact-arithmetic hypothesis is confirmed or refuted by number. Cases named by the owner: 102, 103, 106, 206, 268, 269.
