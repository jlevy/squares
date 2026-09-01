---
type: is
id: is-01m1dw6c2mb2y2ect4qj49amwd
title: Ledger must not disposition review-pending experiments
kind: bug
status: closed
priority: 0
version: 2
spec_path: packing/campaign/agendas/agenda-013-nine-hour-autonomous-run.md
labels:
  - packing
  - correctness
  - campaign-ledger
dependencies: []
parent_id: is-01m1dtfx94hb8ndgdxmmxp3z4m
created_at: 2026-09-01T06:58:33.682Z
updated_at: 2026-09-01T07:14:10.358Z
closed_at: 2026-09-01T07:14:10.357Z
close_reason: "Fixed with a tested derived-status guard: rounds marked needs_review cannot disposition a hypothesis or override a prior reviewed verdict; clearing the flag applies the frozen decision. Focused campaign and agenda suite passes (38 tests), with records and edit tiers green."
resolution: null
duplicate_of: null
---
status_of currently derives confirmed or refuted from verdict.decision even when verdict.needs_review is true. Make review-pending rounds visible as needs review without moving the hypothesis, preserve any prior reviewed disposition, and add focused negative tests proving a proposed H-051 decision cannot take effect before review.
