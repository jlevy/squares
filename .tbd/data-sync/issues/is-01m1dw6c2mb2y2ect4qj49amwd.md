---
type: is
id: is-01m1dw6c2mb2y2ect4qj49amwd
title: Ledger must not disposition review-pending experiments
kind: bug
status: open
priority: 0
version: 1
spec_path: packing/campaign/agendas/agenda-013-nine-hour-autonomous-run.md
labels:
  - packing
  - correctness
  - campaign-ledger
dependencies: []
parent_id: is-01m1dtfx94hb8ndgdxmmxp3z4m
created_at: 2026-09-01T06:58:33.682Z
updated_at: 2026-09-01T06:58:33.682Z
---
status_of currently derives confirmed or refuted from verdict.decision even when verdict.needs_review is true. Make review-pending rounds visible as needs review without moving the hypothesis, preserve any prior reviewed disposition, and add focused negative tests proving a proposed H-051 decision cannot take effect before review.
